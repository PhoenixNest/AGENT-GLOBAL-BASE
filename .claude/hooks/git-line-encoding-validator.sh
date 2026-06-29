#!/usr/bin/env bash
# H-GIT01: PreToolUse (Bash|PowerShell) — Pre-Commit Line Encoding Validator (bash port)
# Detects git add / git commit commands and runs git diff --check to surface
# whitespace and line-ending warnings before the command executes.
# Non-blocking: injects additionalContext only — commit proceeds after operator review.
# Reference: .gitattributes, .claude/rules/git-workflow.md

raw_input=$(cat)

command=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print((d.get('tool_input') or {}).get('command','') or '')")

[ -z "$command" ] && exit 0

# Only intercept git staging / commit commands
echo "$command" | grep -qiE '\bgit\s+(add|commit)\b' || exit 0

cwd=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('cwd','') or '')")
[ -z "$cwd" ] && cwd="$(pwd)"

# --- 1. Check staged files for whitespace / line-ending issues ---
diff_check_output=$(git -C "$cwd" diff --check --cached 2>&1)
has_diff_issues=0
[ -n "$(echo "$diff_check_output" | tr -d '[:space:]')" ] && has_diff_issues=1

# --- 2. Identify staged .ps1 files ---
staged_files=$(git -C "$cwd" diff --cached --name-only 2>/dev/null)
has_staged_ps1=0
echo "$staged_files" | grep -qiE '\.ps1$' && has_staged_ps1=1

# --- 3. Verify .gitattributes covers .ps1 ---
ps1_rule_missing=1
gitattributes="$cwd/.gitattributes"
if [ -f "$gitattributes" ]; then
    grep -qE '^\*\.ps1[[:space:]]+text' "$gitattributes" && ps1_rule_missing=0
fi

# Exit if nothing to report
if [ "$has_diff_issues" -eq 0 ] && ! { [ "$has_staged_ps1" -eq 1 ] && [ "$ps1_rule_missing" -eq 1 ]; }; then
    exit 0
fi

# --- 4. Build additionalContext ---
msg="[LINE ENCODING VALIDATOR — H-GIT01]
Line-ending check triggered by git add/commit.
"

if [ "$has_diff_issues" -eq 1 ]; then
    msg="$msg
WHITESPACE/LINE-ENDING WARNINGS (git diff --check --cached):
$(echo "$diff_check_output" | sed -e 's/[[:space:]]*$//')

Action: Review the flagged files and normalise line endings before committing.
  - For .ps1 files: should be stored as LF (*.ps1 text eol=lf in .gitattributes).
  - For .md/.json/.py/.html: should be stored as LF, CRLF on checkout.
  - Run: git add --renormalize . && git status to see the effect.
"
fi

if [ "$has_staged_ps1" -eq 1 ] && [ "$ps1_rule_missing" -eq 1 ]; then
    msg="$msg
STAGED .ps1 FILES DETECTED — .gitattributes has no explicit *.ps1 rule.
Add \"*.ps1 text eol=lf\" to .gitattributes then re-stage:
  git add .gitattributes
  git add --renormalize <your-ps1-file>
"
fi

msg="$msg
Reference: .gitattributes, .claude/rules/git-workflow.md"

MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','additionalContext':os.environ['MSG']}}))"
exit 0
