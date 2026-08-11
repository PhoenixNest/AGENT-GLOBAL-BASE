#!/usr/bin/env python3
# Write-Memory-Confirmation-Gate enforcement — PreToolUse: denies any tool call other than
# AskUserQuestion while a high-consequence agent-memory write confirmation is pending for this
# session. Real enforcement companion to a future write-capable agent-memory MCP tool
# (core-component-00/mcp-servers/agent-memory/write_gate.py's WriteConfirmationGate). The
# write-path threat model required a genuinely human-facing, structurally-enforced confirmation
# step for high-consequence writes, not an in-process flag or docstring warning — see
# core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md
# § Write-Path Security.
#
# Same PreToolUse/PostToolUse hook-pair shape this workspace already built and validated for
# H-P01 (prompt-gate-enforcer.py / prompt-gate-clear.py) — deliberately reused, not reinvented.
# This is a NEW, INDEPENDENT pair: it checks its own
# marker file (see MARKER_PREFIX below), never H-P01's "h-p01-pending-<session_id>.json", and
# does not modify or depend on prompt-gate-enforcer.py/prompt-gate-clear.py in any way.
#
# NOT WIRED IN by this build. Per the build brief's scope note, modifying .claude/settings.json
# (the harness's own live hook configuration) is out of scope for this worktree's automated
# build — this script is real, working, and tested standalone, but inert until a human (or the
# orchestrator, with explicit review) adds the settings.json entries below on purpose.
#
# --- settings.json wiring snippet (apply deliberately, not automatically) --------------------
# Add to the existing "PreToolUse" -> matcher: "*" group's "hooks" array, alongside
# prompt-gate-enforcer.py's own entry:
#
#     {
#       "type": "command",
#       "command": "uv",
#       "args": ["run", "${CLAUDE_PROJECT_DIR}/.claude/hooks/write-memory-gate-enforcer.py"]
#     }
#
# See write-memory-gate-clear.py for the matching PostToolUse snippet.
# -----------------------------------------------------------------------------------------------
#
# Honest scope/limitation (see write_gate.py's module docstring "Hook enforcement boundary" for
# the full statement): this hook provides a structurally-enforced confirmation gate for writes
# initiated FROM AN INTERACTIVE CLAUDE CODE SESSION — the primary real caller of agent-memory in
# this workspace — not a guarantee that holds against every conceivable MCP client. A different
# MCP host, a direct protocol client bypassing Claude Code's own hook-executing harness, or a
# caller invoking agent-memory's Python functions directly is not touched by this mechanism at
# all. Per REFLECT-003 (core-component-00/engineering/context-engineering/memory/reflection/
# reflection-log.jsonl entry 3), no purely code-level check — this hook included — can be *the*
# security boundary against a determined bypass; it narrows the failure window for the one real,
# in-scope caller this workspace has today, and is defense-in-depth, not an unforgeable gate.
#
# Standard library only, no third-party dependencies — same constraint as the H-P01 pair. This
# hook always exits 0; the actual PreToolUse "deny" is communicated via the hookSpecificOutput
# JSON printed to stdout (permissionDecision: "deny"), not via a nonzero process exit code — so
# every early-return path below must exit 0 by design, matching prompt-gate-enforcer.py exactly.

import datetime
import json
import os
import subprocess
import sys

MARKER_PREFIX = "mem-write-pending-"
STALE_MARKER_SECONDS = 900  # mirrors H-P01's 15-minute stale-marker fail-safe exactly


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    if not isinstance(data, dict):
        return 0

    tool_name = data.get("tool_name") or ""
    if tool_name == "AskUserQuestion":
        return 0

    session_id = data.get("session_id") or ""
    if not session_id:
        return 0

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except OSError:
        return 0

    if result.returncode != 0:
        return 0

    repo_root = result.stdout.strip()

    marker_path = os.path.join(
        repo_root, ".claude", "hooks", ".state", f"{MARKER_PREFIX}{session_id}.json"
    )

    if not os.path.isfile(marker_path):
        return 0

    # Stale-marker fail-safe: identical shape and threshold to
    # prompt-gate-enforcer.py's own — if the confirmation step never completed for some other
    # reason (e.g. the turn ended without one), clear the marker and stop blocking rather than
    # deadlock the session. This does not select an answer for the user — it only restores
    # pre-gate behavior.
    try:
        with open(marker_path, "r", encoding="utf-8") as f:
            marker = json.load(f)
        ts = datetime.datetime.fromisoformat(marker["ts"])
        now = datetime.datetime.now(ts.tzinfo) if ts.tzinfo else datetime.datetime.now()
        age_seconds = (now - ts).total_seconds()
        is_stale = age_seconds > STALE_MARKER_SECONDS
    except Exception:
        is_stale = True

    if is_stale:
        try:
            os.remove(marker_path)
        except OSError:
            pass
        return 0

    summary = ""
    try:
        summary = marker.get("summary") or ""
    except Exception:
        pass

    reason = (
        "Memory-write confirmation pending — answer the pending write confirmation question "
        "(AskUserQuestion) before using other tools."
    )
    if summary:
        reason += f" Pending write: {summary}"

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
