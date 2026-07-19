#!/usr/bin/env bash
# H-MAE02: PreToolUse (Bash|PowerShell) — Multi-Agent Commit Format Guard (bash port)
# On agent/* branches, validates that git commit messages follow the required format:
#   Subject: agent/<name>: <verb-phrase>  (imperative, <=72 chars)
#   Body:    at least one hyphen-bulleted change line
# Bodyless single-line agent commits are a P2 defect per CLAUDE.md §6.
# Reference: core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md

raw_input=$(cat)

command=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print((d.get('tool_input') or {}).get('command','') or '')")

[ -z "$command" ] && exit 0

# Only intercept git commit commands
echo "$command" | grep -qiE '\bgit\s+commit\b' || exit 0

# Determine current branch — use cwd from hook input for reliability
cwd=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('cwd','') or '')")

if [ -n "$cwd" ]; then
    current_branch=$(git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null)
else
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
fi

# Only enforce on agent branches
if ! echo "$current_branch" | grep -qE '^agent/' && ! echo "$current_branch" | grep -qE '^stage[0-9]+/agent/'; then
    exit 0
fi

# Extract commit message from -m "..." or --message "..." (simple string form only)
# Heredoc forms are allowed through — too complex to parse reliably
commit_msg=$(echo "$command" | python3 -c "import sys,re
c=sys.stdin.read()
m=re.search(r'(?s)(?:-m|--message)\s+\"((?:[^\"\\\\]|\\\\.)*)\"',c)
if not m: m=re.search(r\"(?s)(?:-m|--message)\s+'((?:[^'\\\\]|\\\\.)*)'\",c)
print(m.group(1) if m else '')")

[ -z "$commit_msg" ] && exit 0

subject=$(printf '%s' "$commit_msg" | head -n 1 | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

# Validate subject format: agent/<name>: <verb-phrase>
if ! echo "$subject" | grep -qE '^agent/[^:]+:[[:space:]]+[^[:space:]]'; then
    reason="[COMMIT FORMAT GUARD — H-MAE02] Agent commit subject '$subject' does not match required format 'agent/<name>: <verb-phrase>' (imperative, <=72 chars). This is a P2 defect per CLAUDE.md §6. Example: 'agent/backend: add authentication endpoint'. Reference: core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md."
    REASON="$reason" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':os.environ['REASON']}}))"
    exit 0
fi

# Validate body — at least one hyphen-bulleted line after the subject (skip subject + blank line)
has_body=0
if printf '%s' "$commit_msg" | tail -n +3 | grep -qE '^[[:space:]]*-[[:space:]]+[^[:space:]]'; then
    has_body=1
fi

if [ "$has_body" -eq 0 ]; then
    reason="[COMMIT FORMAT GUARD — H-MAE02] Agent commit is missing a hyphen-bulleted body. Bodyless single-line commits are a P2 defect per CLAUDE.md §6. Add a blank line then at least one '- <discrete change>' bullet after the subject line."
    REASON="$reason" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':os.environ['REASON']}}))"
    exit 0
fi

exit 0
