#!/usr/bin/env python3
# H-HE02: PostToolUse (Bash) — Python Error Boundary Monitor (Python port)
# Scans tool_output for Python exception patterns and injects additionalContext
# presenting the three recovery actions from CC-00 error_boundary.py:
# retry-with-backoff, fallback-to-safe-default, graceful-degradation.
#
# Ports .claude/hooks/harness-error-boundary-monitor.ps1 and
# .claude/hooks/harness-error-boundary-monitor.sh to a single stdlib-only
# Python 3 implementation (no third-party dependencies). This is a purely
# advisory PostToolUse hook -- it only ever adds additionalContext, it never
# denies/blocks a tool call -- so every code path below terminates with
# exit 0, matching both originals exactly (fail-safe, not fail-closed, is
# the correct behavior for *this* hook: there is no gate to fail open on).
#
# Neither original resolves the repo root from *inside* the script -- that
# happens once in settings.json's invocation wrapper
# (`r=$(git rev-parse --show-toplevel ...) && bash/pwsh ".../<script>"`),
# and this script has no file-path-dependent logic of its own (it is a pure
# stdin -> stdout text filter), so there is nothing to port on that front.
#
# Reference: core-component-00/framework/03-harness-engineering/implementations/error_boundary.py
#
# --- Accepted risk: advisory-only by design ---------------------------------------
# This hook is advisory-only — no harness policy is enforced at the session layer.
# That is not a design gap to be closed: PostToolUse fires *after* the Bash command
# has already executed, so by the time this hook runs there is no tool call left to
# deny — advisory-only is the only coherent behavior available at this lifecycle
# position, not a fallback chosen in place of a stronger one, and not a gap to close.
# A genuine *blocking* control over dangerous Bash output would need to live at
# PreToolUse instead, gating the command before it runs — that is a separate,
# unscoped initiative, not an extension of this hook.
# -----------------------------------------------------------------------------------

import json
import re
import sys

from _hook_log import log_invocation

# Same three detection patterns, same order, as both originals.
ERROR_PATTERNS = [
    r"Traceback \(most recent call last\)",
    r"(?m)^\s*(SyntaxError|ImportError|ModuleNotFoundError|AttributeError|TypeError|ValueError|KeyError|IndexError|RuntimeError|OSError|FileNotFoundError|PermissionError|TimeoutError|ConnectionError|RecursionError):\s*\S",
    r"(?m)^(Error|Exception):\s+\S",
]

# Used to pick the first line worth surfacing as "the" matched error line.
MATCHED_LINE_HINT = re.compile(r"(Traceback|Error|Exception)")


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    tool_output = data.get("tool_output") if isinstance(data, dict) else None

    # Reconcile how the two originals handle a non-string tool_output value:
    # the ps1 original does `if (-not $toolOutput) { exit 0 }` and then
    # matches with PowerShell's `-match`, which for a non-string operand
    # coerces via .NET's default ToString() -- for a PSCustomObject that
    # comes back from ConvertFrom-Json, ToString() yields the *type name*,
    # not the content, so it effectively never matches. The bash original's
    # embedded python3 helper instead does
    # `if not isinstance(v, str): v = json.dumps(v)`, serializing the value
    # to real text before the shell-side grep/regex matching runs -- so a
    # dict/list tool_output *can* match if it happens to contain error text.
    # We follow the bash original's (more defensive) json.dumps fallback
    # here: tool_output for the Bash tool is realistically always a plain
    # string in production, so this only matters for a synthetic/malformed
    # payload, and choosing the strictly-more-detecting behavior can never
    # cause this advisory hook to miss content the other original would
    # have surfaced.
    if tool_output is None:
        tool_output = ""
    elif not isinstance(tool_output, str):
        tool_output = json.dumps(tool_output)

    if not tool_output:
        return 0

    matched = False
    for pattern in ERROR_PATTERNS:
        if re.search(pattern, tool_output):
            matched = True
            break

    if not matched:
        return 0

    # Split on bare "\n" only (mirrors ps1's `-split "`n"`), not Python's
    # broader str.splitlines(), which also breaks on \r, \v, \f, and various
    # Unicode line separators the originals do not treat as line breaks.
    matched_line = None
    for line in tool_output.split("\n"):
        if MATCHED_LINE_HINT.search(line):
            matched_line = line.strip()
            break

    if not matched_line:
        return 0

    log_invocation("harness-error-boundary-monitor", "PostToolUse", decision="error_detected",
                    reason=matched_line, session_id=data.get("session_id") if isinstance(data, dict) else None)

    msg = (
        "[ERROR BOUNDARY MONITOR — H-HE02]\n"
        f"Python error detected: {matched_line}\n"
        "\n"
        "Apply CC-00 error_boundary.py recovery protocol (Harness Engineering, Layer 3):\n"
        "\n"
        "1. RETRY (transient errors — network, timeout, rate-limit)\n"
        "   - Wait with exponential backoff: 1s, 2s, 4s (max 3 retries)\n"
        "   - Only retry idempotent operations\n"
        "\n"
        "2. FALLBACK (recoverable errors — missing module, bad input)\n"
        "   - Switch to safe-default behavior and continue session\n"
        "   - Document the fallback in your response\n"
        "\n"
        "3. GRACEFUL DEGRADATION (fatal errors — unrecoverable state)\n"
        "   - Log the error with context (session_id, tool, timestamp)\n"
        "   - Report the failure clearly to the user\n"
        "   - Stop safely — do not mask or silently swallow the error\n"
        "\n"
        "Reference: core-component-00/framework/03-harness-engineering/implementations/error_boundary.py"
    )

    output = {
        "systemMessage": f"[H-HE02: error detected in tool output — {matched_line[:120]}]",
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": msg,
        }
    }
    sys.stdout.write(json.dumps(output))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Advisory-only hook: never let an unexpected failure propagate as a
        # non-zero exit / stderr traceback into the hook chain. Both
        # originals degrade silently to `exit 0` on any failure path.
        sys.exit(0)
