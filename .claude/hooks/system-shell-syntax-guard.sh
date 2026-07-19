#!/usr/bin/env bash
# H-SYS01: PreToolUse (Bash|PowerShell) — Bidirectional OS-Aware Shell Syntax Guard (bash port)
# On macOS/Linux: detects PowerShell-only constructs and suggests POSIX equivalents.
# On Windows (Git Bash/MSYS): detects bash-only constructs and suggests PowerShell equivalents.
# Non-blocking: usage may be intentional; this is a correction note, not a hard block.
# Reference: CLAUDE.md §1.

raw_input=$(cat)

command=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print((d.get('tool_input') or {}).get('command','') or '')")

[ -z "$command" ] && exit 0

emit() {
    # $1 = additionalContext message
    MSG="$1" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','additionalContext':os.environ['MSG']}}))"
}

uname_s=$(uname -s 2>/dev/null)

case "$uname_s" in
    Linux|Darwin)
        # ─── macOS/Linux path: guard against PowerShell-only constructs ───
        ps_entries=(
            '\bWrite-Output\b|\bWrite-Host\b|||Write-Output / Write-Host|||echo or printf'
            '\bGet-ChildItem\b|\bgci\b|\bdir\s+|||Get-ChildItem / gci / dir|||ls'
            '\bRemove-Item\b|||Remove-Item / Remove-Item -Recurse|||rm -rf <path>'
            '\bCopy-Item\b|||Copy-Item|||cp <src> <dst>'
            '\bMove-Item\b|||Move-Item|||mv <src> <dst>'
            '\bNew-Item\b|||New-Item -ItemType|||mkdir <dir>  or  touch <file>'
            '\bSet-Location\b|||Set-Location|||cd <path>'
            '\bGet-Content\b|||Get-Content|||cat <file>'
            '\bSelect-String\b|||Select-String|||grep <pattern> <file>'
            '\bForEach-Object\b|||ForEach-Object / %|||for loop  or  xargs'
            '\bWhere-Object\b|||Where-Object / ?|||grep or awk'
            '\bConvertTo-Json\b|||ConvertTo-Json|||python3 -c "import json; print(json.dumps(...))"'
            '\bConvertFrom-Json\b|||ConvertFrom-Json|||python3 -c "import json; data=json.load(open(...))"'
            '\$env:[A-Za-z_][A-Za-z0-9_]*|||$env:VAR syntax|||$VAR  or  export VAR=value'
            '\bInvoke-WebRequest\b|\biwr\b|||Invoke-WebRequest / iwr|||curl <url>  or  wget <url>'
        )
        detected=""
        for entry in "${ps_entries[@]}"; do
            pattern="${entry%%|||*}"
            rest="${entry#*|||}"
            ps_label="${rest%%|||*}"
            posix_label="${rest##*|||}"
            if echo "$command" | grep -qiP "$pattern"; then
                block="  PS:    $ps_label
  POSIX: $posix_label"
                [ -z "$detected" ] && detected="$block" || detected="$detected

$block"
            fi
        done
        [ -z "$detected" ] && exit 0
        msg="[SHELL SYNTAX GUARD — H-SYS01 | macOS/Linux]
PowerShell-only construct(s) detected in the planned command. This system uses POSIX bash/sh.
Please substitute the POSIX equivalents before executing:

$detected

If you are intentionally targeting pwsh on this POSIX system, confirm explicitly in your response.
Reference: CLAUDE.md §1, .claude/rules/ (approved command set for this workspace)"
        emit "$msg"
        exit 0
        ;;
    MINGW*|MSYS*|CYGWIN*)
        # ─── Windows path: guard against bash-only constructs ───
        bash_entries=(
            '(?<!\$)\brm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\b|(?<!\$)\brm\s+-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*\b|||rm -rf <path>|||Remove-Item -Recurse -Force <path>'
            '(?<!\w)grep\s+|||grep <pattern> <file>|||Select-String -Pattern <pattern> -Path <file>'
            "(?<!\w)sed\s+|||sed 's/old/new/g'|||Get-Content file | ForEach-Object { \$_ -replace 'old','new' }"
            "(?<!\w)awk\s+|||awk '{print \$1}'|||... | ForEach-Object { \$_.Split()[0] }"
            '(?<!\$)export\s+[A-Za-z_][A-Za-z0-9_]*=|||export VAR=value|||$env:VAR = "value"'
            '(?<!\w)touch\s+[^\|&;]|||touch <file>|||if (-not (Test-Path <file>)) { New-Item -ItemType File <file> }'
            '(?<!\w)which\s+\w|||which <command>|||(Get-Command <command>).Source'
            '2>/dev/null|>/dev/null|||2>/dev/null  or  >/dev/null|||2>$null  or  | Out-Null'
            '(?<!\w)chmod\s+|||chmod <mode> <file>|||icacls <file> /grant <user>:<perm>  (or skip — not usually needed on Windows)'
            '(?<!\w)chown\s+|||chown <user> <file>|||icacls <file> /setowner <user>  (or skip — not usually needed on Windows)'
            '(?<!\w)mkdir\s+-p\s+|||mkdir -p <path>|||New-Item -ItemType Directory -Force <path>'
        )
        detected=""
        for entry in "${bash_entries[@]}"; do
            pattern="${entry%%|||*}"
            rest="${entry#*|||}"
            bash_label="${rest%%|||*}"
            ps_label="${rest##*|||}"
            if echo "$command" | grep -qP "$pattern"; then
                block="  bash: $bash_label
  PS:   $ps_label"
                [ -z "$detected" ] && detected="$block" || detected="$detected

$block"
            fi
        done
        [ -z "$detected" ] && exit 0
        msg="[SHELL SYNTAX GUARD — H-SYS01 | Windows]
Bash-only construct(s) detected in the planned command. This workspace uses Windows PowerShell
(CLAUDE.md §1). Please substitute the PowerShell equivalents before executing:

$detected

If you are intentionally targeting Git Bash or WSL, confirm explicitly in your response.
Reference: CLAUDE.md §1, .claude/rules/ (approved command set for this workspace)"
        emit "$msg"
        exit 0
        ;;
    *)
        # Unknown platform — pass through silently
        exit 0
        ;;
esac
