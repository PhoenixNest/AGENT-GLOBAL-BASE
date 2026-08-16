#!/usr/bin/env python3
# H-CE01: UserPromptSubmit — Context Budget Alert (Python port)
# Reads transcript_path file size as a session-length proxy. When it exceeds the
# threshold, injects additionalContext directing Claude to apply Sacred Context
# principles from CC-00 engineering/harness-engineering/implementations/context_monitor.py.
#
# Ports .claude/hooks/context-budget-alert.ps1 and .claude/hooks/context-budget-alert.sh
# to a single stdlib-only Python 3 implementation. This is a purely advisory
# UserPromptSubmit hook (it never denies/blocks a turn) — every code path below
# terminates with exit 0, matching both originals exactly.

import json
import os
import sys

from _hook_log import log_invocation


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    # Guard against non-dict top-level JSON (e.g. a JSON array/number), which
    # the bash original's inline `d.get(...)` would crash on (uncaught
    # AttributeError -> traceback on stderr, though it still nets out to
    # exit 0 for the outer bash script). The ps1 original never crashes here
    # because PowerShell property access on a non-object silently yields
    # $null. We reconcile on the ps1 original's silent behavior.
    transcript = ""
    if isinstance(data, dict):
        transcript = data.get("transcript_path", "") or ""

    if not transcript:
        return 0
    if not os.path.isfile(transcript):
        return 0

    try:
        size_bytes = os.path.getsize(transcript)
    except OSError:
        return 0

    # Round to nearest KB via the bash original's "+512, integer-divide"
    # arithmetic (round-half-up). The ps1 original instead calls
    # [math]::Round(bytes / 1KB), which is .NET banker's rounding
    # (round-half-to-even) — the two originals disagree only at an exact
    # half-KB boundary. We follow the bash original here since that is the
    # version actually wired into settings.json's UserPromptSubmit hook chain
    # (invoked via `bash ... context-budget-alert.sh` regardless of platform).
    size_kb = (size_bytes + 512) // 1024
    threshold_kb = 500

    session_id = data.get("session_id") if isinstance(data, dict) else None

    if size_kb < threshold_kb:
        log_invocation("context-budget-alert", "UserPromptSubmit", decision="under_threshold",
                        session_id=session_id, extra={"size_kb": size_kb})
        return 0

    log_invocation("context-budget-alert", "UserPromptSubmit", decision="threshold_exceeded",
                    session_id=session_id, extra={"size_kb": size_kb})

    msg = (
        "[CONTEXT BUDGET ALERT — H-CE01]\n"
        f"Session transcript size: {size_kb} KB (threshold: {threshold_kb} KB)\n"
        "\n"
        "The session context is growing large. Apply Sacred Context principles before responding:\n"
        "- Preserve decision-critical context (System and Working slots) losslessly\n"
        "- Compress or summarize non-critical Conversation context where possible\n"
        "- If approaching model context limits, invoke context_compressor.py patterns\n"
        "- Prioritize: active task state > prior decisions > background knowledge\n"
        "Reference: core-component-00/engineering/harness-engineering/implementations/context_monitor.py"
    )

    output = {
        "systemMessage": f"[H-CE01: context budget alert — transcript at {size_kb} KB (threshold {threshold_kb} KB)]",
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": msg,
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
