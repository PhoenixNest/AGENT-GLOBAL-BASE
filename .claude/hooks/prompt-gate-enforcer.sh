#!/usr/bin/env bash
# H-P01 enforcement — PreToolUse: denies any tool other than AskUserQuestion while a
# prompt-optimizer confirmation is pending for this session. Real enforcement companion
# to prompt-optimizer.sh, which only injects advisory additionalContext on its own.

raw_input=$(cat)

tool_name=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('tool_name','') or '')")

[ "$tool_name" = "AskUserQuestion" ] && exit 0

session_id=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('session_id','') or '')")

[ -z "$session_id" ] && exit 0

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
MARKER_PATH="$repo_root/.claude/hooks/.state/h-p01-pending-$session_id.json"
export MARKER_PATH

[ -f "$MARKER_PATH" ] || exit 0

# Stale-marker fail-safe: if the marker is older than 15 minutes, the confirmation step
# never completed for some other reason. Clear it and stop blocking rather than deadlock
# the session. This does not select an answer for the user — it only restores pre-gate
# behavior.
state=$(python3 -c "import os,json,datetime
try:
    d=json.load(open(os.environ['MARKER_PATH']))
    ts=datetime.datetime.fromisoformat(d['ts'])
    now=datetime.datetime.now(ts.tzinfo) if ts.tzinfo else datetime.datetime.now()
    age=(now-ts).total_seconds()
    print('stale' if age > 900 else 'fresh')
except Exception:
    print('stale')")

if [ "$state" = "stale" ]; then
    rm -f "$MARKER_PATH"
    exit 0
fi

python3 -c "import json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':'H-P01 confirmation pending — answer the prompt-optimization question (AskUserQuestion) before using other tools.'}}))"
exit 0
