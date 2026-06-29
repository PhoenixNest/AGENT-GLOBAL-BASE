#!/usr/bin/env bash
# H-P04: PreToolUse (Edit|Write|NotebookEdit) — Prompt Write Guard (bash port)
# Blocks any file write operation targeting denied paths:
# GEMINI.md, .gemini/**, or any path that matches the settings.json deny rules.
# Enforces CLAUDE.md §1 at the tool-execution layer.

raw_input=$(cat)

file_path=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print((d.get('tool_input') or {}).get('file_path','') or '')")

[ -z "$file_path" ] && exit 0

normalized_path=$(printf '%s' "$file_path" | tr '\\' '/')

blocked_rule=""
if echo "$normalized_path" | grep -qE '(^|/)GEMINI\.md$'; then
    blocked_rule='GEMINI.md is off-limits to Claude Code — CLAUDE.md §1 explicit guardrail'
elif echo "$normalized_path" | grep -qE '(^|/)\.gemini(/|$)'; then
    blocked_rule='.gemini/** is explicitly denied in settings.json deny rules — CLAUDE.md §1'
fi

[ -z "$blocked_rule" ] && exit 0

reason="[WRITE GUARD — H-P04] Write blocked to denied path. Path: $file_path | Reason: $blocked_rule | Modify CLAUDE.md or .claude/ files instead."

REASON="$reason" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':os.environ['REASON']}}))"
exit 0
