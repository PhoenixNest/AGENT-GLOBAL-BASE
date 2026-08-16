#!/usr/bin/env python3
"""H-P01 enforcement — PostToolUse (matcher: AskUserQuestion): clears the pending-confirmation
marker once AskUserQuestion has been called, releasing the PreToolUse gate for this session.

Python port of prompt-gate-clear.ps1 / prompt-gate-clear.sh (identical behavior; part of the
OS-fork removal migration — one script instead of a pwsh/bash pair). Standard library only,
no third-party dependencies.

Fail-closed contract: this script only ever *removes* the pending-confirmation marker that
prompt-gate-enforcer.{ps1,sh} checks for before denying non-AskUserQuestion tool calls. On any
ambiguity or error — unparseable stdin, a JSON body that isn't an object, a missing/empty
session_id, an unresolved repo root, or a filesystem error on removal — this script does
nothing and exits 0, leaving any existing marker in place. That means the PreToolUse gate keeps
denying tool calls for that session until either a genuine AskUserQuestion call clears it or the
enforcer's own 15-minute stale-marker safety valve kicks in. It never takes the other branch
(deleting a marker it isn't sure about), which would be the fail-open direction for this gate.
"""

import json
import os
import re
import subprocess
import sys

from _hook_log import log_invocation

# tool_response shape for AskUserQuestion isn't in the Claude Code hooks reference;
# this matches the real shape observed in this workspace's own session transcripts.
_QA_RE = re.compile(r'"([^"]+)"\s*=\s*"([^"]+)"')


def _read_input():
    try:
        raw_input = sys.stdin.read()
    except Exception:
        return None

    try:
        data = json.loads(raw_input)
    except Exception:
        return None

    if not isinstance(data, dict):
        return None

    return data


def _extract_selection_summary(data):
    """Pull '<question> → <selected label>' pairs out of tool_response.
    Returns None on any shape mismatch or error."""
    try:
        tool_response = data.get("tool_response")

        text = None
        if isinstance(tool_response, str):
            text = tool_response
        elif isinstance(tool_response, dict):
            content = tool_response.get("content")
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                parts = [
                    block.get("text")
                    for block in content
                    if isinstance(block, dict) and isinstance(block.get("text"), str)
                ]
                text = "\n".join(parts) if parts else None

        if not text:
            return None

        pairs = _QA_RE.findall(text)
        if not pairs:
            return None

        return "; ".join(f"{question} → {answer}" for question, answer in pairs)
    except Exception:
        return None


def _repo_root():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return None

    if result.returncode != 0:
        return None

    root = result.stdout.strip()
    return root or None


def main():
    data = _read_input()
    if data is None:
        sys.exit(0)

    session_id = str(data.get("session_id") or "")
    if not session_id:
        sys.exit(0)

    repo_root = _repo_root()
    if not repo_root:
        sys.exit(0)

    marker_path = os.path.join(
        repo_root, ".claude", "hooks", ".state", f"h-p01-pending-{session_id}.json"
    )

    marker_existed = os.path.isfile(marker_path)

    try:
        os.remove(marker_path)
    except Exception:
        # Silent by design — mirrors `rm -f` / -ErrorAction SilentlyContinue: a missing
        # file, a permission error, etc. are all swallowed, never surfaced as a failure.
        pass

    if marker_existed:
        selection_summary = _extract_selection_summary(data)
        log_invocation("prompt-gate-clear", "PostToolUse", decision="cleared",
                        reason=selection_summary, session_id=session_id, repo_root=repo_root)
        if selection_summary:
            try:
                # hookSpecificOutput must be present alongside systemMessage on
                # PostToolUse — some clients silently drop a bare systemMessage.
                print(json.dumps({
                    "systemMessage": f"[H-P01: {selection_summary}]",
                    "hookSpecificOutput": {"hookEventName": "PostToolUse"},
                }))
            except Exception:
                pass

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        # Defensive catch-all: any unforeseen error still exits 0 without having deleted
        # anything (fail closed — the marker, if any, is left in place).
        sys.exit(0)
