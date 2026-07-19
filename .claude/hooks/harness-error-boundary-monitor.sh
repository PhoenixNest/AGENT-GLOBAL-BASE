#!/usr/bin/env bash
# H-HE02: PostToolUse (Bash) — Python Error Boundary Monitor (bash port)
# Scans tool_output for Python exception patterns and injects additionalContext
# presenting the three recovery actions from CC-00 error_boundary.py:
# retry-with-backoff, fallback-to-safe-default, graceful-degradation.
# Reference: core-component-00/engineering/harness-engineering/implementations/error_boundary.py

raw_input=$(cat)

tool_output=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
v=d.get('tool_output','')
if v is None: v=''
if not isinstance(v,str): v=json.dumps(v)
print(v)")

[ -z "$tool_output" ] && exit 0

matched=0
echo "$tool_output" | grep -qE 'Traceback \(most recent call last\)' && matched=1
if [ "$matched" -eq 0 ]; then
    echo "$tool_output" | grep -qE '^[[:space:]]*(SyntaxError|ImportError|ModuleNotFoundError|AttributeError|TypeError|ValueError|KeyError|IndexError|RuntimeError|OSError|FileNotFoundError|PermissionError|TimeoutError|ConnectionError|RecursionError):[[:space:]]*[^[:space:]]' && matched=1
fi
if [ "$matched" -eq 0 ]; then
    echo "$tool_output" | grep -qE '^(Error|Exception):[[:space:]]+[^[:space:]]' && matched=1
fi

[ "$matched" -eq 0 ] && exit 0

matched_line=$(echo "$tool_output" | grep -E '(Traceback|Error|Exception)' | head -n 1 | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
[ -z "$matched_line" ] && exit 0

msg="[ERROR BOUNDARY MONITOR — H-HE02]
Python error detected: $matched_line

Apply CC-00 error_boundary.py recovery protocol (Harness Engineering, Layer 3):

1. RETRY (transient errors — network, timeout, rate-limit)
   - Wait with exponential backoff: 1s, 2s, 4s (max 3 retries)
   - Only retry idempotent operations

2. FALLBACK (recoverable errors — missing module, bad input)
   - Switch to safe-default behavior and continue session
   - Document the fallback in your response

3. GRACEFUL DEGRADATION (fatal errors — unrecoverable state)
   - Log the error with context (session_id, tool, timestamp)
   - Report the failure clearly to the user
   - Stop safely — do not mask or silently swallow the error

Reference: core-component-00/engineering/harness-engineering/implementations/error_boundary.py"

MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PostToolUse','additionalContext':os.environ['MSG']}}))"
exit 0
