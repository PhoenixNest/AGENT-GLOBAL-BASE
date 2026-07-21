#!/usr/bin/env bash
# H-GIT01: PreToolUse (Bash|PowerShell) — Pre-Commit Line Encoding Validator (bash port)
# Detects git add / git commit commands and validates line-ending issues before the
# command executes.
#   - Advisory (non-blocking): git diff --check whitespace warnings, missing *.ps1 gitattributes rule.
#   - Blocking: mixed line endings within a staged file's WORKING-TREE content, or a CR
#     byte in a staged *.ps1/*.sh file's working-tree content — a CRLF shebang breaks bash
#     on Linux/macOS/WSL, so this is a correctness defect, not a style preference.
#     Checked against the working-tree file, not the staged git blob: git's own
#     text=auto/eol clean filter already normalises CR/mixed endings out of anything by
#     the time it reaches the index, so checking the blob can never observe the defect —
#     the working-tree file is what actually gets executed and what the author edited.
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

# --- 1. Check staged files for whitespace / line-ending issues (advisory) ---
diff_check_output=$(git -C "$cwd" diff --check --cached 2>&1)
has_diff_issues=0
[ -n "$(echo "$diff_check_output" | tr -d '[:space:]')" ] && has_diff_issues=1

# --- 2. Identify staged .ps1 files (advisory) ---
staged_files=$(git -C "$cwd" diff --cached --name-only 2>/dev/null)
has_staged_ps1=0
echo "$staged_files" | grep -qiE '\.ps1$' && has_staged_ps1=1

# --- 3. Verify .gitattributes covers .ps1 (advisory) ---
ps1_rule_missing=1
gitattributes="$cwd/.gitattributes"
if [ -f "$gitattributes" ]; then
    grep -qE '^\*\.ps1[[:space:]]+text' "$gitattributes" && ps1_rule_missing=0
fi

# --- 4. Byte-level checks against staged files' WORKING-TREE content (blocking) ---
# Delegates to python3 for reliable binary-safe byte scanning of each file on disk.
byte_check_json=$(CWD="$cwd" STAGED="$staged_files" python3 -c "
import os, json

cwd = os.environ.get('CWD', '.')
staged = [p for p in os.environ.get('STAGED', '').splitlines() if p]

mixed_eol_files = []
bad_cr_scripts = []

for path in staged:
    full_path = os.path.join(cwd, path)
    if not os.path.isfile(full_path):
        continue
    with open(full_path, 'rb') as f:
        data = f.read()
    if not data:
        continue

    # Binary heuristic (mirrors git's own NUL-in-first-8000-bytes rule) — skip binaries
    if b'\\x00' in data[:8000]:
        continue

    has_crlf = b'\\r\\n' in data
    has_lf_only = False
    has_any_cr = b'\\r' in data
    prev = -1
    for byte in data:
        if byte == 10 and prev != 13:
            has_lf_only = True
            break
        prev = byte

    if has_crlf and has_lf_only:
        mixed_eol_files.append(path)
    if (path.endswith('.ps1') or path.endswith('.sh')) and has_any_cr:
        bad_cr_scripts.append(path)

print(json.dumps({'mixed_eol_files': mixed_eol_files, 'bad_cr_scripts': bad_cr_scripts}))
")

mixed_eol_count=$(echo "$byte_check_json" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['mixed_eol_files']))")
bad_cr_count=$(echo "$byte_check_json" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['bad_cr_scripts']))")

has_blocking_issues=0
[ "$mixed_eol_count" -gt 0 ] 2>/dev/null && has_blocking_issues=1
[ "$bad_cr_count" -gt 0 ] 2>/dev/null && has_blocking_issues=1

# Exit if nothing to report at all
if [ "$has_diff_issues" -eq 0 ] && ! { [ "$has_staged_ps1" -eq 1 ] && [ "$ps1_rule_missing" -eq 1 ]; } && [ "$has_blocking_issues" -eq 0 ]; then
    exit 0
fi

# --- 5. Build additionalContext ---
msg="[LINE ENCODING VALIDATOR — H-GIT01]
Line-ending check triggered by git add/commit.
"

if [ "$has_blocking_issues" -eq 1 ]; then
    mixed_list=$(echo "$byte_check_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\n'.join('    - ' + p for p in d['mixed_eol_files']))")
    cr_list=$(echo "$byte_check_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\n'.join('    - ' + p for p in d['bad_cr_scripts']))")
    msg="$msg
BLOCKING LINE-ENDING DEFECTS:"
    if [ "$mixed_eol_count" -gt 0 ]; then
        msg="$msg
  Mixed line endings within a single file (some lines LF, some CRLF):
$mixed_list"
    fi
    if [ "$bad_cr_count" -gt 0 ]; then
        msg="$msg
  CR byte present in a shell/PowerShell script (breaks execution on Linux/macOS/WSL — must be pure LF):
$cr_list"
    fi
    msg="$msg

Action: fix the offending file(s) (re-save with consistent LF, or run
  git add --renormalize <path>) and re-stage before committing.
"
fi

if [ "$has_diff_issues" -eq 1 ]; then
    msg="$msg
WHITESPACE/LINE-ENDING WARNINGS (git diff --check --cached):
$(echo "$diff_check_output" | sed -e 's/[[:space:]]*$//')

Action: Review the flagged files and normalise line endings before committing.
  - For .ps1/.sh files: must be stored as LF (*.ps1/*.sh text eol=lf in .gitattributes).
  - For all other text files: left to \` * text=auto\` — normalised to the OS of whoever checks the repo out, not hardcoded.
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

if [ "$has_blocking_issues" -eq 1 ]; then
    reason="H-GIT01: blocking line-ending defect(s) —"
    [ "$mixed_eol_count" -gt 0 ] && reason="$reason $mixed_eol_count file(s) with mixed line endings;"
    [ "$bad_cr_count" -gt 0 ] && reason="$reason $bad_cr_count .ps1/.sh file(s) with CR bytes;"
    reason="$reason See additionalContext for details."
    MSG="$msg" REASON="$reason" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':os.environ['REASON'],'additionalContext':os.environ['MSG']}}))"
else
    MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','additionalContext':os.environ['MSG']}}))"
fi
exit 0
