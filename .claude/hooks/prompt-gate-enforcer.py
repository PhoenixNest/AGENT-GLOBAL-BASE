#!/usr/bin/env python3
# H-P01 enforcement — PreToolUse: denies any tool other than AskUserQuestion while a
# prompt-optimizer confirmation is pending for this session. Real enforcement companion
# to prompt-optimizer.{sh,ps1}, which only injects advisory additionalContext on its own.
#
# Python port of prompt-gate-enforcer.sh / prompt-gate-enforcer.ps1 — implements
# identical stdin handling, repo-root resolution, marker-file logic, and stdout/exit-code
# semantics as both originals, using only the standard library. This hook always exits 0;
# the actual PreToolUse "deny" is communicated via the hookSpecificOutput JSON printed to
# stdout (permissionDecision: "deny"), not via a nonzero process exit code — so every
# early-return path below must exit 0 by design, matching both originals exactly.

import datetime
import json
import os
import subprocess
import sys


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    # Defensive: both originals assume a JSON object; a non-object top-level payload
    # (list/number/string/null) would crash the equivalent inline snippets in the shell
    # version rather than being caught by its try/except (which only wraps json.load).
    # In practice Claude Code always sends a JSON object here, so this never fires on a
    # real invocation — it only prevents an unhandled traceback on a malformed payload,
    # which is a defensive improvement, not a behavior change from the shell original.
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
        repo_root, ".claude", "hooks", ".state", f"h-p01-pending-{session_id}.json"
    )

    if not os.path.isfile(marker_path):
        return 0

    # Stale-marker fail-safe: if the marker is older than 15 minutes, the confirmation
    # step never completed for some other reason (e.g. the turn ended without one).
    # Clear it and stop blocking rather than deadlock the session. This does not select
    # an answer for the user — it only restores pre-gate behavior.
    try:
        with open(marker_path, "r", encoding="utf-8") as f:
            marker = json.load(f)
        ts = datetime.datetime.fromisoformat(marker["ts"])
        now = datetime.datetime.now(ts.tzinfo) if ts.tzinfo else datetime.datetime.now()
        age_seconds = (now - ts).total_seconds()
        is_stale = age_seconds > 900
    except Exception:
        is_stale = True

    if is_stale:
        try:
            os.remove(marker_path)
        except OSError:
            pass
        return 0

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "H-P01 confirmation pending — answer the prompt-optimization question "
                "(AskUserQuestion) before using other tools."
            ),
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
