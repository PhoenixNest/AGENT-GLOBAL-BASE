"""
Cross-platform manual supervisor for the shared embedder-service
(start/stop/status/cleanup).

2026-08-13 Python port of manage_embedder_service.ps1 (retired -- this file
is now the sole implementation), following the same `.ps1`/`.sh` -> single
`uv run` Python precedent already used for .claude/hooks/prompt-gate-enforcer.py.
See core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md.

The service is normally self-launched by the first MCP server consumer that
needs it (embedder_client.ensure_service_running(), atomic-lock guarded)
and self-shuts-down after an idle timeout -- this script is not required
for normal operation. It exists for manual control and, in particular,
orphan cleanup, mirroring the original .ps1's rationale.

Usage:
    uv run manage_embedder_service.py status
    uv run manage_embedder_service.py start
    uv run manage_embedder_service.py stop
    uv run manage_embedder_service.py cleanup
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

import psutil

_SERVICE_DIR = Path(__file__).resolve().parent
_RUN_DIR = _SERVICE_DIR / "run"
_PID_FILE = _RUN_DIR / "embedder-service.pid"
_LOCK_FILE = _RUN_DIR / "embedder-service.lock"
_SERVER_SCRIPT = _SERVICE_DIR / "server.py"

_HOST = os.environ.get("EMBEDDER_SERVICE_HOST", "127.0.0.1")
_PORT = os.environ.get("EMBEDDER_SERVICE_PORT", "8791")
_BASE_URL = f"http://{_HOST}:{_PORT}"


def _resolve_python_executable() -> tuple[str, bool]:
    """Resolves the interpreter the service is launched with, in order:
    (1) EMBEDDER_SERVICE_PYTHON -- explicit override; (2) mcp-servers/.venv
    -- the shared environment the MCP servers also use, resolved per-OS
    (Scripts/python.exe on Windows, bin/python elsewhere -- this OS branch
    is the one place that distinction belongs, unlike the former
    .mcp.json hardcoding it for every consumer); (3) "python" from PATH --
    fallback, may resolve to an interpreter without the CUDA torch build.
    Returns (executable, is_shared_venv)."""
    override = os.environ.get("EMBEDDER_SERVICE_PYTHON")
    if override:
        return override, True
    shared_venv = _SERVICE_DIR.parent.parent / ".venv"
    candidate = shared_venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    if candidate.exists():
        return str(candidate.resolve()), True
    return "python", False


def _get_service_health() -> Optional[dict]:
    try:
        with urllib.request.urlopen(f"{_BASE_URL}/health", timeout=2) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def _get_pid_file_info() -> Optional[dict]:
    if not _PID_FILE.exists():
        return None
    try:
        return json.loads(_PID_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def _cmd_status() -> None:
    health = _get_service_health()
    if health:
        models = ",".join(health.get("models_loaded", []))
        print(
            f"RUNNING — pid={health.get('pid')} models={models} "
            f"uptime_s={health.get('uptime_s')} idle_timeout_s={health.get('idle_timeout_s')}"
        )
        return
    pid_info = _get_pid_file_info()
    if pid_info:
        print(f"NOT RESPONDING — stale PID file present (pid={pid_info.get('pid')}); run cleanup")
    else:
        print("STOPPED")


def _cmd_start() -> None:
    health = _get_service_health()
    if health:
        print(f"Already running — pid={health.get('pid')}")
        return

    python_exe, is_shared_venv = _resolve_python_executable()
    print(f"Starting embedder-service ({_SERVER_SCRIPT})...")
    if not is_shared_venv:
        print(
            "WARNING: Shared venv not found at mcp-servers/.venv — falling back to PATH "
            "'python'. The service may start on a CPU-only torch. See mcp-servers/CLAUDE.md.",
            file=sys.stderr,
        )
    else:
        print(f"  interpreter: {python_exe}")

    popen_kwargs = dict(
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if sys.platform == "win32":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | getattr(
            subprocess, "DETACHED_PROCESS", 0x00000008
        )
    else:
        popen_kwargs["start_new_session"] = True
    subprocess.Popen([python_exe, str(_SERVER_SCRIPT)], **popen_kwargs)

    deadline = time.time() + 45
    health = None
    while time.time() < deadline:
        time.sleep(0.5)
        health = _get_service_health()
        if health:
            models = ",".join(health.get("models_loaded", []))
            print(f"Started — pid={health.get('pid')} models={models}")
            break
    if not health:
        print("WARNING: Service did not come up within 45s", file=sys.stderr)


def _cmd_stop() -> None:
    health = _get_service_health()
    if not health:
        print(f"Not running (no response from {_BASE_URL}/health)")
        return
    target_pid = health.get("pid")
    try:
        req = urllib.request.Request(f"{_BASE_URL}/shutdown", data=b"{}", method="POST")
        req.add_header("Content-Type", "application/json")
        urllib.request.urlopen(req, timeout=2)
    except Exception:
        # Graceful shutdown request may itself race the socket closing --
        # fall through to a hard stop below.
        pass

    deadline = time.time() + 10
    while time.time() < deadline:
        time.sleep(0.3)
        if not _get_service_health():
            break

    if _get_service_health():
        print(f"WARNING: Graceful shutdown did not take effect — force-stopping pid={target_pid}", file=sys.stderr)
        try:
            psutil.Process(target_pid).kill()
        except Exception:
            pass

    for f in (_PID_FILE, _LOCK_FILE):
        try:
            f.unlink()
        except FileNotFoundError:
            pass
        except Exception:
            pass
    print("Stopped")


def _cmd_cleanup() -> None:
    """Orphan detection: any python process whose command line references
    this server.py but which (a) has no live /health response tied to its
    pid, or (b) is not the pid currently on record in the PID file."""
    health = _get_service_health()
    live_pid = health.get("pid") if health else None

    orphan_count = 0
    for proc in psutil.process_iter(["pid", "cmdline"]):
        try:
            cmdline = proc.info.get("cmdline") or []
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        joined = " ".join(cmdline).replace("\\", "/")
        if "embedder-service" not in joined or "server.py" not in joined:
            continue
        pid = proc.info["pid"]
        if live_pid and pid == live_pid:
            continue
        print(f"Killing orphaned embedder-service process pid={pid}")
        try:
            psutil.Process(pid).kill()
        except Exception:
            pass
        orphan_count += 1

    if not live_pid:
        try:
            _PID_FILE.unlink()
        except FileNotFoundError:
            pass
    try:
        _LOCK_FILE.unlink()
    except FileNotFoundError:
        pass

    print(f"Cleanup complete — {orphan_count} orphaned process(es) removed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manual supervisor for the shared embedder-service.")
    parser.add_argument("action", choices=["start", "stop", "status", "cleanup"])
    args = parser.parse_args()

    {
        "status": _cmd_status,
        "start": _cmd_start,
        "stop": _cmd_stop,
        "cleanup": _cmd_cleanup,
    }[args.action]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
