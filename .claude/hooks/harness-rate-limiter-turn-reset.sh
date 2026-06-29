#!/usr/bin/env bash
# H-HE01-RESET: UserPromptSubmit — resets per-turn tool counter and limit for H-HE01 (bash port)
# Fires at the start of every new prompt, ensuring the per-turn tool-call counter
# and any mid-turn extension granted by the user are wiped before the new turn begins.
# The session-level counter and ceiling are NOT touched here.
# Reference: core-component-00/harness-engineering/implementations/tool_registry.py

raw_input=$(cat)

session_id=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('session_id','') or '')")

[ -z "$session_id" ] && exit 0

safe_id=$(printf '%s' "$session_id" | tr -c 'a-zA-Z0-9' '-')
base="${TMPDIR:-/tmp}"

# Reset per-turn counter to 0
printf '0' > "$base/cc00-tool-counter-turn-$safe_id.txt"

# Delete per-turn limit file so any mid-turn extension does not carry over
rm -f "$base/cc00-tool-limit-turn-$safe_id.txt"

exit 0
