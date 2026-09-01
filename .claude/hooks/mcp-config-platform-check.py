#!/usr/bin/env python3
"""SessionStart — MCP Config Platform Self-Heal

Fires at the start of every session. Root `.mcp.json` is machine-local and gitignored
(2026-08-30, Item #6 -- see the maintenance record below): it is bootstrapped once from
the committed `.mcp.json.example` template on first run (file missing entirely), and
after that only rewritten if a server's `"command"` interpreter path no longer resolves
on this machine (a genuine OS switch), by flipping it to the sibling venv-interpreter
path (`.venv/Scripts/python.exe` <-> `.venv/bin/python`). Both cases share the same
per-server correction loop below. Every other session is a cheap no-op: read, verify
each path still resolves, exit -- no write at all.

Why the file is gitignored and only conditionally written, not regenerated every
session: `.mcp.json` is static JSON and cannot branch on OS, so every prior fix to this
exact problem hardcoded one OS's path into the *committed* file and broke the other OS
the next time the workspace ran on a different machine (2026-08-13: bare "uv" broke on
the host's stale PATH; 2026-08-20: the WSL/Linux fix's `.venv/bin/python` committed as
the new default then broke a Windows session; 2026-08-30: the fix for *that* -- a
per-session self-healing hook -- turned out to leave a locally-rewritten `.mcp.json`
one accidental `git add -A` away from repeating the same failure for the next person to
pull). Gitignoring the real file removes that failure mode structurally instead of
relying on nobody committing it by mistake. Regenerating on every session (an earlier
version of this proposal) was rejected: the CEO flagged that rewriting `.mcp.json` near
an already-connected MCP server carries real risk, and OS switches are rare enough that
paying that cost every session is the wrong trade -- so this hook only ever writes when
the file is missing or a path has actually gone stale, matching the original design's
cost profile.
Full record: core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/
(see log/10-windows-reopen-and-proposed-fix.md, log/11 for this hook's original
implementation, and log/14-15 for the 2026-08-30 template/gitignore redesign).

Advisory + self-correcting, never blocking: every code path below exits 0. A missing
`.mcp.json.example` template, a `.mcp.json`/template that cannot be parsed, a server
whose command shape isn't recognized, or a server whose venv doesn't exist for either OS
is left untouched (or left missing) and only logged -- this hook fixes the one specific,
previously-incident-causing failure mode (OS-mismatched venv path), nothing else.
"""

import json
import sys
from pathlib import Path

from _hook_log import log_invocation

PROJECT_DIR_TOKEN = "${CLAUDE_PROJECT_DIR:-.}"
POSIX_SUFFIX = "/.venv/bin/python"
WINDOWS_SUFFIX = "/.venv/Scripts/python.exe"
TEMPLATE_FILENAME = ".mcp.json.example"


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
    template_path = repo_root / TEMPLATE_FILENAME

    bootstrapping = not mcp_json_path.is_file()
    source_path = template_path if bootstrapping else mcp_json_path

    try:
        raw_config = source_path.read_text(encoding="utf-8")
        config = json.loads(raw_config)
    except Exception as exc:
        decision = "template_unreadable" if bootstrapping else "unreadable"
        log_invocation("mcp-config-platform-check", "SessionStart", decision=decision,
                        session_id=session_id, extra={"error": str(exc), "source": str(source_path)})
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

    # Not bootstrapping and nothing needed correction: cheap no-op, matches every ordinary
    # session (OS switches are rare -- see module docstring for why this hook doesn't write
    # unconditionally on every SessionStart).
    if not bootstrapping and not corrected:
        log_invocation("mcp-config-platform-check", "SessionStart", decision="no_change",
                        session_id=session_id, extra={"unresolved": unresolved} if unresolved else None)
        return 0

    try:
        mcp_json_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        # Fail-open: could not write the fix back, but never block the session over it.
        decision = "bootstrap_write_failed" if bootstrapping else "write_failed"
        log_invocation("mcp-config-platform-check", "SessionStart", decision=decision,
                        session_id=session_id, extra={"error": str(exc), "would_have_corrected": corrected})
        return 0

    decision = "bootstrapped" if bootstrapping else "corrected"
    log_invocation("mcp-config-platform-check", "SessionStart", decision=decision,
                    session_id=session_id, extra={"corrected": corrected, "unresolved": unresolved})

    if bootstrapping:
        lines = [f"- {name}: {c['from']} -> {c['to']}" for name, c in corrected.items()] or [
            "- (template's default paths already matched this OS -- copied as-is)"
        ]
        message = (
            "[MCP CONFIG PLATFORM CHECK — SessionStart bootstrap]\n"
            f"root .mcp.json did not exist -- generated it from {TEMPLATE_FILENAME} for this OS "
            "before MCP servers connect:\n" + "\n".join(lines)
        )
    else:
        lines = [f"- {name}: {c['from']} -> {c['to']}" for name, c in corrected.items()]
        message = (
            "[MCP CONFIG PLATFORM CHECK — SessionStart self-heal]\n"
            "root .mcp.json referenced an interpreter path from a different operating system than "
            "this one. Corrected before MCP servers connect:\n"
            + "\n".join(lines)
        )
    system_message = (
        f"[MCP config bootstrapped from {TEMPLATE_FILENAME} for this OS]"
        if bootstrapping
        else f"[MCP config self-healed for this OS: {', '.join(corrected)}]"
    )
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
