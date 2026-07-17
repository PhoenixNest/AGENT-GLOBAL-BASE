#!/usr/bin/env bash
# H-MAE01: PreToolUse (Bash|PowerShell) — Multi-Agent Branch Naming Guard (bash port)
# Detects git commands that create new branches and validates the branch name
# against the workspace multi-agent naming convention:
#   agent/<role>/<task>  or  stage<N>/agent/<role>/<task>
# Reference: core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md

raw_input=$(cat)

command=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print((d.get('tool_input') or {}).get('command','') or '')")

[ -z "$command" ] && exit 0

# Extract branch name from branch-creating commands
branch_name=$(echo "$command" | python3 -c "import sys,re
c=sys.stdin.read()
m=re.search(r'git\s+worktree\s+add\s+\S+\s+(?:-b\s+)?([a-zA-Z0-9/._-]+)',c)
if not m: m=re.search(r'git\s+checkout\s+-b\s+([a-zA-Z0-9/._-]+)',c)
if not m: m=re.search(r'git\s+switch\s+(?:--create|-c)\s+([a-zA-Z0-9/._-]+)',c)
print(m.group(1) if m else '')")

[ -z "$branch_name" ] && exit 0

# Valid branch patterns for this workspace
is_valid=0
echo "$branch_name" | grep -qE '^agent/[^/]+/[^/]+$' && is_valid=1
echo "$branch_name" | grep -qE '^stage[0-9]+/agent/[^/]+/[^/]+$' && is_valid=1
echo "$branch_name" | grep -qE '^(master|main|develop)$' && is_valid=1
echo "$branch_name" | grep -qE '^(company|studio)/.*$' && is_valid=1
echo "$branch_name" | grep -qE '^(feature|fix|chore|docs|refactor|test)/.*$' && is_valid=1

[ "$is_valid" -eq 1 ] && exit 0

reason="[BRANCH NAMING GUARD — H-MAE01] Branch name '$branch_name' does not follow workspace conventions. Multi-agent branches must be: agent/<role>/<task> or stage<N>/agent/<role>/<task> (e.g., agent/backend/dark-mode-api). Standard branches (feature/, fix/, company/, studio/) are also accepted. Reference: core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md and CLAUDE.md §6."

REASON="$reason" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':os.environ['REASON']}}))"
exit 0
