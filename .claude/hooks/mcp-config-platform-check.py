#!/usr/bin/env python3
"""SessionStart — MCP Config Platform Self-Heal

Fires at the start of every session. Reads root `.mcp.json`, and for each registered
MCP server whose `"command"` file does not exist on this machine, rewrites it to the
sibling venv-interpreter path for the OS actually running (`.venv/Scripts/python.exe`
<-> `.venv/bin/python`), then writes the corrected file back before Claude Code's own
`/mcp reconnect` runs against it.

Why this exists: `.mcp.json` is static JSON and cannot branch on OS, so every prior fix
to this exact problem hardcoded one OS's path and broke the other the next time the
workspace ran on a different machine (2026-08-13: bare "uv" broke on the host's stale
PATH; 2026-08-20: the WSL/Linux fix's `.venv/bin/python` then broke a Windows session).
This hook makes the correction automatic and self-healing instead of another manual,
error-prone one-line edit. It only ever writes a fully-resolved, on-disk-verified
absolute path -- never a bare command name -- so it cannot reintroduce the 2026-08-13
stale-host-PATH failure mode.
Full record: core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/
(see log/10-windows-reopen-and-proposed-fix.md and log/11 for this hook's own history).

Advisory + self-correcting, never blocking: every code path below exits 0. A `.mcp.json`
that cannot be parsed, a server whose command shape isn't recognized, or a server whose
venv doesn't exist for either OS is left untouched and only logged -- this hook fixes the
one specific, previously-incident-causing failure mode (OS-mismatched venv path), nothing
else.
"""

import json
import sys
from pathlib import Path

from _hook_log import log_invocation

PROJECT_DIR_TOKEN = "${CLAUDE_PROJECT_DIR:-.}"
POSIX_SUFFIX = "/.venv/bin/python"
WINDOWS_SUFFIX = "/.venv/Scripts/python.exe"


def _repo_root() -> Path:
    # Mirrors rag-index-sync.py's approach: this script lives at
    # <repo_root>/.claude/hooks/<this file>, so two parents up is the repo root --
    # no subprocess call needed.
    return Path(__file__).resolve().parent.parent.parent


def _resolve(command: str, repo_root: Path) -> Path:
    return Path(command.replace(PROJECT_DIR_TOKEN, str(repo_root)))


def _alt_command(command: str):
    """Returns the sibling-OS command string, or None if the command doesn't end in a
    recognized per-server venv interpreter suffix."""
    if command.endswith(POSIX_SUFFIX):
        return command[: -len(POSIX_SUFFIX)] + WINDOWS_SUFFIX
    if command.endswith(WINDOWS_SUFFIX):
        return command[: -len(WINDOWS_SUFFIX)] + POSIX_SUFFIX
    return None


def main() -> int:
    raw_input = sys.stdin.read()
    try:
        payload = json.loads(raw_input) if raw_input.strip() else {}
    except Exception:
        payload = {}
    session_id = payload.get("session_id") if isinstance(payload, dict) else None

    repo_root = _repo_root()
    mcp_json_path = repo_root / ".mcp.json"

    try:
        raw_config = mcp_json_path.read_text(encoding="utf-8")
        config = json.loads(raw_config)
    except Exception as exc:
        log_invocation("mcp-config-platform-check", "SessionStart", decision="unreadable",
                        session_id=session_id, extra={"error": str(exc)})
        return 0

    servers = config.get("mcpServers")
    if not isinstance(servers, dict):
        log_invocation("mcp-config-platform-check", "SessionStart", decision="no_servers",
                        session_id=session_id)
        return 0

    corrected = {}
    unresolved = []

    for name, server_cfg in servers.items():
        if not isinstance(server_cfg, dict):
            continue
        command = server_cfg.get("command")
        if not isinstance(command, str):
            continue

        if _resolve(command, repo_root).is_file():
            continue  # already correct for this OS -- no-op

        alt_command = _alt_command(command)
        if alt_command is None:
            unresolved.append({"server": name, "reason": "unrecognized_command_shape"})
            continue

        if _resolve(alt_command, repo_root).is_file():
            server_cfg["command"] = alt_command
            corrected[name] = {"from": command, "to": alt_command}
        else:
            unresolved.append({"server": name, "reason": "neither_os_path_exists"})

    if not corrected:
        log_invocation("mcp-config-platform-check", "SessionStart", decision="no_change",
                        session_id=session_id, extra={"unresolved": unresolved} if unresolved else None)
        return 0

    try:
        mcp_json_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        # Fail-open: could not write the fix back, but never block the session over it.
        log_invocation("mcp-config-platform-check", "SessionStart", decision="write_failed",
                        session_id=session_id, extra={"error": str(exc), "would_have_corrected": corrected})
        return 0

    log_invocation("mcp-config-platform-check", "SessionStart", decision="corrected",
                    session_id=session_id, extra={"corrected": corrected, "unresolved": unresolved})

    lines = [f"- {name}: {c['from']} -> {c['to']}" for name, c in corrected.items()]
    message = (
        "[MCP CONFIG PLATFORM CHECK — SessionStart self-heal]\n"
        "root .mcp.json referenced an interpreter path from a different operating system than "
        "this one. Corrected before MCP servers connect:\n"
        + "\n".join(lines)
    )
    print(
        json.dumps(
            {
                "systemMessage": f"[MCP config self-healed for this OS: {', '.join(corrected)}]",
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
