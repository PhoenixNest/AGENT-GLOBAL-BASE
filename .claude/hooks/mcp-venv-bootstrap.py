#!/usr/bin/env python3
"""SessionStart — MCP Venv Bootstrap

Sibling to `mcp-config-platform-check.py`, deliberately kept separate rather than folded
into it (Item #8, `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/`,
log/18-log/20). That hook's entire safety contract is being cheap, read-mostly, and
fail-open on every ordinary session -- it only ever flips a stale interpreter path between
two *existing* OS-specific venvs, and explicitly declines to act (logging
`reason: "neither_os_path_exists"`) when a server's `.venv` doesn't exist at all for either
OS. `uv sync` is a different class of operation entirely -- it downloads and installs
packages and can take minutes on a cold machine -- so it lives here instead, gated strictly
behind that specific signal, so the fast hook stays fast for the overwhelming majority of
sessions where both venvs already exist.

Reads this session's own `mcp-config-platform-check` invocation record from
`.claude/hooks/.state/hook-invocations.jsonl` (written by `_hook_log.py`, same file this
hook also writes to) rather than re-deriving the same OS-path-resolution logic itself --
single source of truth for "does this server's venv exist for this OS," avoiding drift
between the two hooks. Registered in `.claude/settings.json` immediately after
`mcp-config-platform-check` within the same `SessionStart` hook group, so ordering within
one session is guaranteed: the self-heal hook always runs first and logs before this hook
reads that log.

Fail-open, matching every hook in this suite: every code path exits 0, including a `uv
sync` failure, timeout, or any unexpected exception. A failed bootstrap here leaves the
server exactly as broken as it already was -- it never makes things worse, and the existing
manual workaround (running `uv sync` by hand per each server's README) remains available
regardless of what this hook does.
"""

import json
import subprocess
import sys
from pathlib import Path

from _hook_log import log_invocation

PROJECT_DIR_TOKEN = "${CLAUDE_PROJECT_DIR:-.}"
POSIX_SUFFIX = "/.venv/bin/python"
WINDOWS_SUFFIX = "/.venv/Scripts/python.exe"
INVOCATION_LOG_RELATIVE = Path(".claude") / "hooks" / ".state" / "hook-invocations.jsonl"
UV_SYNC_TIMEOUT_SECONDS = 300


def _repo_root() -> Path:
    # Mirrors mcp-config-platform-check.py's approach: this script lives at
    # <repo_root>/.claude/hooks/<this file>, so two parents up is the repo root -- no
    # subprocess call needed.
    return Path(__file__).resolve().parent.parent.parent


def _resolve(command: str, repo_root: Path) -> Path:
    return Path(command.replace(PROJECT_DIR_TOKEN, str(repo_root)))


def _server_root(command: str) -> str | None:
    """Strips the trailing per-server venv-interpreter suffix (either OS's) off a
    `.mcp.json` `"command"` string, returning the server's root directory as a
    (still-templated) path string, or None if the suffix isn't recognized."""
    if command.endswith(POSIX_SUFFIX):
        return command[: -len(POSIX_SUFFIX)]
    if command.endswith(WINDOWS_SUFFIX):
        return command[: -len(WINDOWS_SUFFIX)]
    return None


def _find_latest_platform_check_entry(log_path: Path, session_id):
    """Returns the most recent mcp-config-platform-check log-invocation record for this
    session, or (falling back, since this hook cannot safely assume the sibling hook ran
    -- e.g. a hand-invoked test, or a future settings.json reorder) the most recent such
    record regardless of session. Returns None if the log is missing/unreadable or no
    matching record exists at all."""
    try:
        lines = log_path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None

    same_session_match = None
    any_match = None
    for line in lines:
        try:
            record = json.loads(line)
        except Exception:
            continue
        if record.get("hook") != "mcp-config-platform-check":
            continue
        any_match = record
        if session_id and record.get("session_id") == session_id:
            same_session_match = record

    return same_session_match or any_match


def _servers_needing_bootstrap(entry) -> list[str]:
    """Extracts server names whose most recent mcp-config-platform-check unresolved
    reason was exactly "neither_os_path_exists" -- the one signal this hook acts on."""
    if not entry:
        return []
    extra = entry.get("extra") or {}
    unresolved = extra.get("unresolved") or []
    return [
        item.get("server")
        for item in unresolved
        if isinstance(item, dict)
        and item.get("reason") == "neither_os_path_exists"
        and item.get("server")
    ]


def main() -> int:
    raw_input = sys.stdin.read()
    try:
        payload = json.loads(raw_input) if raw_input.strip() else {}
    except Exception:
        payload = {}
    session_id = payload.get("session_id") if isinstance(payload, dict) else None

    repo_root = _repo_root()
    mcp_json_path = repo_root / ".mcp.json"
    invocation_log_path = repo_root / INVOCATION_LOG_RELATIVE

    platform_check_entry = _find_latest_platform_check_entry(invocation_log_path, session_id)
    needing_bootstrap = _servers_needing_bootstrap(platform_check_entry)

    if not needing_bootstrap:
        # Fast no-op -- the overwhelming majority of sessions land here. No shelling out,
        # no filesystem writes beyond the log line itself.
        log_invocation("mcp-venv-bootstrap", "SessionStart", decision="no_action_needed",
                        session_id=session_id)
        return 0

    try:
        config = json.loads(mcp_json_path.read_text(encoding="utf-8"))
        servers_config = config.get("mcpServers") or {}
    except Exception as exc:
        log_invocation("mcp-venv-bootstrap", "SessionStart", decision="mcp_json_unreadable",
                        session_id=session_id,
                        extra={"error": str(exc), "needing_bootstrap": needing_bootstrap})
        return 0

    synced = []
    failed = []

    for server_name in needing_bootstrap:
        server_cfg = servers_config.get(server_name)
        command = server_cfg.get("command") if isinstance(server_cfg, dict) else None
        server_root_template = _server_root(command) if isinstance(command, str) else None
        if not server_root_template:
            failed.append({"server": server_name, "reason": "unrecognized_command_shape"})
            continue

        server_dir = _resolve(server_root_template, repo_root)
        if not server_dir.is_dir():
            failed.append({"server": server_name, "reason": "server_dir_missing", "path": str(server_dir)})
            continue

        try:
            result = subprocess.run(
                ["uv", "sync"],
                cwd=str(server_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=UV_SYNC_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            failed.append({"server": server_name, "reason": "sync_timeout"})
            continue
        except Exception as exc:
            failed.append({"server": server_name, "reason": "sync_exception", "error": str(exc)})
            continue

        if result.returncode == 0:
            synced.append(server_name)
        else:
            failed.append({
                "server": server_name,
                "reason": "sync_nonzero_exit",
                "returncode": result.returncode,
                # Keep this bounded -- uv's own output can be long; the invocation log has
                # a size cap too (_hook_log.py), no need to duplicate the full transcript.
                "tail": (result.stdout or "")[-2000:],
            })

    if synced and not failed:
        decision = "synced"
    elif synced and failed:
        decision = "partially_synced"
    else:
        decision = "sync_failed"

    log_invocation("mcp-venv-bootstrap", "SessionStart", decision=decision, session_id=session_id,
                    extra={"synced": synced, "failed": failed})

    if not synced:
        # Fail-open: nothing to tell the session that isn't already visible via the
        # servers still failing to connect -- don't add a redundant/noisy message.
        return 0

    lines = [f"- {name}: uv sync completed" for name in synced]
    if failed:
        lines += [f"- {item['server']}: NOT bootstrapped ({item['reason']})" for item in failed]
    message = (
        "[MCP VENV BOOTSTRAP — SessionStart]\n"
        "Ran `uv sync` for MCP server(s) whose .venv did not exist for either OS:\n"
        + "\n".join(lines)
        + "\n\nReconnect the affected server(s) (e.g. `/mcp`) to pick this up."
    )
    system_message = f"[MCP venv bootstrapped: {', '.join(synced)}]"
    print(
        json.dumps(
            {
                "systemMessage": system_message,
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": message,
                },
            }
        )
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Fail-open by design, matching the rest of this hook suite: never let an
        # unexpected error here surface as a nonzero exit that could be misread as a
        # session-start block.
        sys.exit(0)
