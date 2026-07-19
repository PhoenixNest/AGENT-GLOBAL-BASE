#!/usr/bin/env bash
# H-P01 enforcement — PostToolUse (matcher: AskUserQuestion): clears the pending-confirmation
# marker once AskUserQuestion has been called, releasing the PreToolUse gate for this session.

raw_input=$(cat)

session_id=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('session_id','') or '')")

[ -z "$session_id" ] && exit 0

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
rm -f "$repo_root/.claude/hooks/.state/h-p01-pending-$session_id.json"
exit 0
