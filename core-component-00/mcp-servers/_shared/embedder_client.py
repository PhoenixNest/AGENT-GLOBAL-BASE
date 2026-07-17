"""
Thin HTTP client for the shared embedder-service
(core-component-00/mcp-servers/_shared/embedder-service/), used by both
agent-memory and workspace-knowledge behind a feature flag (Phase 2 / Phase 4).

Reuses the existing bounded-timeout-then-degrade pattern already established
by `_call_with_hard_timeout` in
context-engineering/implementations/memory_vector_store.py for Qdrant calls,
rather than inventing a second timeout mechanism — per
implementation-plan.md §3. `urllib.request.urlopen(timeout=...)` is generally
reliable for plain HTTP, but the whole premise of this service is that even a
library's own `timeout=` parameter has been observed not to be honored
(memory_vector_store.py's QDRANT_CALL_TIMEOUT_S watchdog exists for exactly
that reason) — every network call in this client goes through the same
disposable-daemon-thread hard timeout as a defense-in-depth measure, not a
redundant one.

Every public function here degrades to None/False on any failure — it never
raises and never blocks past its documented timeout. Callers (agent-memory,
workspace-knowledge) are responsible for falling back to their in-process
loader when a call here returns a degraded result.
"""
from __future__ import annotations

import concurrent.futures
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Optional

_SHARED_DIR = Path(__file__).resolve().parent
_SERVICE_DIR = _SHARED_DIR / "embedder-service"
_RUN_DIR = _SERVICE_DIR / "run"
_LOCK_FILE = _RUN_DIR / "embedder-service.lock"

# Reuse _call_with_hard_timeout rather than re-implement it. Mirrors the
# cross-module import agent-memory/server.py and workspace-knowledge/server.py
# already both do for memory_vector_store.py.
_CONTEXT_ENGINEERING_ROOT = Path(__file__).resolve().parents[2] / "engineering" / "context-engineering"
if str(_CONTEXT_ENGINEERING_ROOT) not in sys.path:
    sys.path.insert(0, str(_CONTEXT_ENGINEERING_ROOT))
from implementations.memory_vector_store import _call_with_hard_timeout  # noqa: E402

# Same typed-exception reconciliation as memory_vector_store.py (EX-001,
# adr-ase-001.md): reuse error_boundary.py's diagnostic vocabulary for
# classification, but never import its TimeoutError bare — the watchdog
# above raises concurrent.futures.TimeoutError (== builtins.TimeoutError
# since Python 3.10), a distinct class from error_boundary.TimeoutError
# despite the shared name. `concurrent.futures.TimeoutError`, fully
# qualified, stays the one canonical timeout name at every call site here.
_HARNESS_ENGINEERING_ROOT = Path(__file__).resolve().parents[2] / "engineering" / "harness-engineering"
if str(_HARNESS_ENGINEERING_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ENGINEERING_ROOT))
from implementations.error_boundary import ValidationError, ServiceUnavailableError  # noqa: E402

HOST = os.getenv("EMBEDDER_SERVICE_HOST", "127.0.0.1")
PORT = int(os.getenv("EMBEDDER_SERVICE_PORT", "8791"))
BASE_URL = f"http://{HOST}:{PORT}"

HEALTH_PROBE_TIMEOUT_S = 1.5
STARTUP_WAIT_TIMEOUT_S = 45.0
LOCK_STALE_AFTER_S = 60.0
EMBED_CALL_TIMEOUT_S = 8.0  # matches QDRANT_CALL_TIMEOUT_S's bound in memory_vector_store.py


def _diag(msg: str) -> None:
    print(f"[embedder-client {time.time():.3f}] {msg}", file=sys.stderr, flush=True)


def _probe_health_once() -> bool:
    try:
        req = urllib.request.Request(f"{BASE_URL}/health", method="GET")
        with urllib.request.urlopen(req, timeout=HEALTH_PROBE_TIMEOUT_S) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("service") == "embedder-service"
    except (urllib.error.URLError, OSError):
        return False
    except (KeyError, ValueError, json.JSONDecodeError):
        return False
    except Exception:
        return False


def probe_health() -> bool:
    """Hard-timeout-wrapped health probe — never blocks longer than
    HEALTH_PROBE_TIMEOUT_S plus the watchdog's own scheduling overhead, even
    if the underlying socket call ignores its own timeout."""
    try:
        return bool(_call_with_hard_timeout(_probe_health_once, timeout=HEALTH_PROBE_TIMEOUT_S + 2.0))
    except concurrent.futures.TimeoutError:
        return False
    except Exception:
        return False


def _acquire_lock() -> bool:
    """Atomic first-consumer launch lock. os.O_CREAT|O_EXCL is atomic at the
    OS level on both Windows and POSIX — the race Phase 0's review flagged
    (two consumers probing the port simultaneously, both finding it free,
    both spawning) is closed by this, not by the port-probe alone."""
    _RUN_DIR.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(_LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        return True
    except FileExistsError:
        try:
            age = time.time() - _LOCK_FILE.stat().st_mtime
        except FileNotFoundError:
            return _acquire_lock()  # lock vanished between the check and stat — retry once
        if age > LOCK_STALE_AFTER_S:
            # Stale lock from a crashed launcher (never itself a crash of the
            # service — the service removes its own PID file on exit). Clear
            # it and retry rather than deadlocking forever.
            try:
                _LOCK_FILE.unlink()
            except FileNotFoundError:
                pass
            return _acquire_lock()
        return False


def _release_lock() -> None:
    try:
        _LOCK_FILE.unlink()
    except FileNotFoundError:
        pass


def ensure_service_running() -> bool:
    """
    Idempotent, self-owned "first consumer" launch. Safe to call from every
    MCP server process at startup (or on every reconnect) — at most one
    process ever spawns the service, guarded by the atomic lock in
    _acquire_lock(). Intended to run in a background thread (mirrors
    agent-memory/server.py's existing `_load_embedder_background` pattern),
    never on the synchronous tool-call path: a cold start can take several
    seconds to load both models, which must never block a single MCP tool
    call.

    Returns True once /health responds, False if the service could not be
    reached or started within STARTUP_WAIT_TIMEOUT_S — callers must treat
    False as "fall back to the in-process loader," never as a reason to
    retry indefinitely or raise.
    """
    if probe_health():
        return True

    if not _acquire_lock():
        # Another process is starting it right now — wait, don't spawn a
        # second copy racing the first.
        deadline = time.time() + STARTUP_WAIT_TIMEOUT_S
        while time.time() < deadline:
            if probe_health():
                return True
            time.sleep(0.5)
        return False

    try:
        if probe_health():  # may have finished starting while we waited for the lock
            return True

        server_script = _SERVICE_DIR / "server.py"
        popen_kwargs: dict = dict(
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            close_fds=True,
        )
        if sys.platform == "win32":
            popen_kwargs["creationflags"] = (
                subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            popen_kwargs["start_new_session"] = True
        _diag(f"launching embedder-service: {sys.executable} {server_script}")
        subprocess.Popen([sys.executable, str(server_script)], **popen_kwargs)

        deadline = time.time() + STARTUP_WAIT_TIMEOUT_S
        while time.time() < deadline:
            if probe_health():
                _diag("embedder-service came up")
                return True
            time.sleep(0.5)
        _diag(f"embedder-service did not come up within {STARTUP_WAIT_TIMEOUT_S}s")
        return False
    finally:
        _release_lock()


def _embed_once(model: str, texts: List[str]) -> List[List[float]]:
    payload = json.dumps({"model": model, "texts": texts}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/embed",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=EMBED_CALL_TIMEOUT_S) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["vectors"]


def embed(
    texts: List[str], model: str, timeout: float = EMBED_CALL_TIMEOUT_S
) -> Optional[List[List[float]]]:
    """
    Returns embedding vectors for `texts` via the shared embedder-service, or
    None on any failure — unreachable service, timeout (including a
    native-level hang the socket's own timeout= failed to enforce), non-200
    response, or malformed body. Never raises, never blocks past `timeout`
    seconds (plus watchdog scheduling overhead). Callers must fall back to
    their in-process loader on None.
    """
    try:
        return _call_with_hard_timeout(lambda: _embed_once(model, texts), timeout=timeout)
    except concurrent.futures.TimeoutError:
        _diag(f"embed TIMED OUT after {timeout}s (model={model!r})")
        return None
    except (urllib.error.URLError, OSError) as exc:
        _diag(f"embed: {ServiceUnavailableError.__name__} (model={model!r}): {exc}")
        return None
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        _diag(f"embed: {ValidationError.__name__} — malformed response (model={model!r}): {exc}")
        return None
    except Exception as exc:
        _diag(f"embed failed (model={model!r}): {exc}")
        return None
