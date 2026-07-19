#!/usr/bin/env pwsh
# H-SYS01: PreToolUse (Bash|PowerShell) — Bidirectional OS-Aware Shell Syntax Guard
# On Windows: detects bash-only constructs and suggests PowerShell equivalents.
# On macOS/Linux: detects PowerShell-only constructs and suggests POSIX equivalents.
# Non-blocking: usage may be intentional; this is a correction note, not a hard block.
# Reference: CLAUDE.md §1 — "Shell is Windows PowerShell. All terminal commands must be
# PowerShell-compatible. Avoid bash-only syntax."

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$command = $data.tool_input.command
if (-not $command) { exit 0 }

# ─── Windows path: guard against bash-only constructs ────────────────────────

if ($IsWindows) {
    # Bash-only construct detection with PowerShell equivalents
    $bashPatterns = @(
        @{
            pattern     = '(?<!\$)\brm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\b|(?<!\$)\brm\s+-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*\b'
            bash        = 'rm -rf <path>'
            powershell  = 'Remove-Item -Recurse -Force <path>'
        },
        @{
            pattern     = '(?<!\w)grep\s+'
            bash        = 'grep <pattern> <file>'
            powershell  = 'Select-String -Pattern <pattern> -Path <file>'
        },
        @{
            pattern     = '(?<!\w)sed\s+'
            bash        = "sed 's/old/new/g'"
            powershell  = "Get-Content file | ForEach-Object { `$_ -replace 'old','new' }"
        },
        @{
            pattern     = '(?<!\w)awk\s+'
            bash        = "awk '{print \$1}'"
            powershell  = "... | ForEach-Object { `$_.Split()[0] }"
        },
        @{
            pattern     = '(?<!\$)export\s+[A-Za-z_][A-Za-z0-9_]*='
            bash        = 'export VAR=value'
            powershell  = '$env:VAR = "value"'
        },
        @{
            pattern     = '(?<!\w)touch\s+[^\|&;]'
            bash        = 'touch <file>'
            powershell  = 'if (-not (Test-Path <file>)) { New-Item -ItemType File <file> }'
        },
        @{
            pattern     = '(?<!\w)which\s+\w'
            bash        = 'which <command>'
            powershell  = '(Get-Command <command>).Source'
        },
        @{
            pattern     = '2>/dev/null|>/dev/null'
            bash        = '2>/dev/null  or  >/dev/null'
            powershell  = '2>$null  or  | Out-Null'
        },
        @{
            pattern     = '(?<!\w)chmod\s+'
            bash        = 'chmod <mode> <file>'
            powershell  = 'icacls <file> /grant <user>:<perm>  (or skip — not usually needed on Windows)'
        },
        @{
            pattern     = '(?<!\w)chown\s+'
            bash        = 'chown <user> <file>'
            powershell  = 'icacls <file> /setowner <user>  (or skip — not usually needed on Windows)'
        },
        @{
            pattern     = '(?<!\w)mkdir\s+-p\s+'
            bash        = 'mkdir -p <path>'
            powershell  = 'New-Item -ItemType Directory -Force <path>'
        }
    )

    $detected = @()
    foreach ($p in $bashPatterns) {
        if ($command -match $p.pattern) {
            $detected += "  bash: $($p.bash)`n  PS:   $($p.powershell)"
        }
    }

    if ($detected.Count -eq 0) { exit 0 }

    $list = $detected -join "`n`n"

    $additionalContext = @"
[SHELL SYNTAX GUARD — H-SYS01 | Windows]
Bash-only construct(s) detected in the planned command. This workspace uses Windows PowerShell
(CLAUDE.md §1). Please substitute the PowerShell equivalents before executing:

$list

If you are intentionally targeting Git Bash or WSL, confirm explicitly in your response.
Reference: CLAUDE.md §1, .claude/rules/ (approved command set for this workspace)
"@

    $output = [ordered]@{
        hookSpecificOutput = [ordered]@{
            hookEventName     = "PreToolUse"
            additionalContext = $additionalContext
        }
    } | ConvertTo-Json -Depth 5 -Compress

    Write-Output $output
    exit 0
}

# ─── macOS/Linux path: guard against PowerShell-only constructs ──────────────

if ($IsLinux -or $IsMacOS) {
    # PowerShell-only construct detection with POSIX equivalents
    $psPatterns = @(
        @{
            pattern = '\bWrite-Output\b|\bWrite-Host\b'
            ps      = 'Write-Output / Write-Host'
            posix   = 'echo or printf'
        },
        @{
            pattern = '\bGet-ChildItem\b|\bgci\b|\bdir\s+'
            ps      = 'Get-ChildItem / gci / dir'
            posix   = 'ls'
        },
        @{
            pattern = '\bRemove-Item\b'
            ps      = 'Remove-Item / Remove-Item -Recurse'
            posix   = 'rm -rf <path>'
        },
        @{
            pattern = '\bCopy-Item\b'
            ps      = 'Copy-Item'
            posix   = 'cp <src> <dst>'
        },
        @{
            pattern = '\bMove-Item\b'
            ps      = 'Move-Item'
            posix   = 'mv <src> <dst>'
        },
        @{
            pattern = '\bNew-Item\b'
            ps      = 'New-Item -ItemType'
            posix   = 'mkdir <dir>  or  touch <file>'
        },
        @{
            pattern = '\bSet-Location\b'
            ps      = 'Set-Location'
            posix   = 'cd <path>'
        },
        @{
            pattern = '\bGet-Content\b'
            ps      = 'Get-Content'
            posix   = 'cat <file>'
        },
        @{
            pattern = '\bSelect-String\b'
            ps      = 'Select-String'
            posix   = 'grep <pattern> <file>'
        },
        @{
            pattern = '\bForEach-Object\b'
            ps      = 'ForEach-Object / %'
            posix   = 'for loop  or  xargs'
        },
        @{
            pattern = '\bWhere-Object\b'
            ps      = 'Where-Object / ?'
            posix   = 'grep or awk'
        },
        @{
            pattern = '\bConvertTo-Json\b'
            ps      = 'ConvertTo-Json'
            posix   = 'python3 -c "import json; print(json.dumps(...))"'
        },
        @{
            pattern = '\bConvertFrom-Json\b'
            ps      = 'ConvertFrom-Json'
            posix   = 'python3 -c "import json; data=json.load(open(...))"'
        },
        @{
            pattern = '\$env:[A-Za-z_][A-Za-z0-9_]*'
            ps      = '$env:VAR syntax'
            posix   = '$VAR  or  export VAR=value'
        },
        @{
            pattern = '\bInvoke-WebRequest\b|\biwr\b'
            ps      = 'Invoke-WebRequest / iwr'
            posix   = 'curl <url>  or  wget <url>'
        }
    )

    $detected = @()
    foreach ($p in $psPatterns) {
        if ($command -match $p.pattern) {
            $detected += "  PS:    $($p.ps)`n  POSIX: $($p.posix)"
        }
    }

    if ($detected.Count -eq 0) { exit 0 }

    $list = $detected -join "`n`n"

    $additionalContext = @"
[SHELL SYNTAX GUARD — H-SYS01 | macOS/Linux]
PowerShell-only construct(s) detected in the planned command. This system uses POSIX bash/sh.
Please substitute the POSIX equivalents before executing:

$list

If you are intentionally targeting pwsh on this POSIX system, confirm explicitly in your response.
Reference: CLAUDE.md §1, .claude/rules/ (approved command set for this workspace)
"@

    $output = [ordered]@{
        hookSpecificOutput = [ordered]@{
            hookEventName     = "PreToolUse"
            additionalContext = $additionalContext
        }
    } | ConvertTo-Json -Depth 5 -Compress

    Write-Output $output
    exit 0
}

# Unknown platform — pass through silently
exit 0
