#!/usr/bin/env pwsh
# H-GIT01: PreToolUse (Bash|PowerShell) — Pre-Commit Line Encoding Validator
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

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$command = $data.tool_input.command
if (-not $command) { exit 0 }

# Only intercept git staging / commit commands
if ($command -notmatch '\bgit\s+(add|commit)\b') { exit 0 }

$cwd = $data.cwd
if (-not $cwd) { $cwd = (Get-Location).Path }

# --- 1. Check staged files for whitespace / line-ending issues (advisory) ---
$diffCheckOutput = (git -C $cwd diff --check --cached 2>&1) -join "`n"
$hasDiffIssues   = ($diffCheckOutput -and $diffCheckOutput.Trim() -ne '')

# --- 2. Identify staged .ps1 files (advisory) ---
$stagedNamesRaw = @(git -C $cwd diff --cached --name-only 2>$null)
$stagedFiles    = $stagedNamesRaw -join "`n"
$hasStagedPs1   = ($stagedFiles -match '\.ps1$')

# --- 3. Verify .gitattributes covers .ps1 (advisory) ---
$gitattributes = Join-Path $cwd '.gitattributes'
$ps1RuleMissing = $true
if (Test-Path $gitattributes) {
    $content = Get-Content $gitattributes -Raw
    if ($content -match '(?m)^\*\.ps1\s+text') {
        $ps1RuleMissing = $false
    }
}

# --- 4. Byte-level checks against staged files' WORKING-TREE content (blocking) ---
$mixedEolFiles = @()
$badCrScripts  = @()

foreach ($path in ($stagedNamesRaw | Where-Object { $_ })) {
    $fullPath = Join-Path $cwd $path
    if (-not (Test-Path $fullPath -PathType Leaf)) { continue }
    $bytes = [System.IO.File]::ReadAllBytes($fullPath)
    if ($bytes.Length -eq 0) { continue }

    # Binary heuristic (mirrors git's own NUL-in-first-8000-bytes rule) — skip binaries
    $sampleLen = [Math]::Min(8000, $bytes.Length)
    $isBinary = $false
    for ($i = 0; $i -lt $sampleLen; $i++) { if ($bytes[$i] -eq 0) { $isBinary = $true; break } }
    if ($isBinary) { continue }

    $hasCrlf   = $false
    $hasLfOnly = $false
    $hasAnyCr  = $false
    for ($i = 0; $i -lt $bytes.Length; $i++) {
        if ($bytes[$i] -eq 13) { $hasAnyCr = $true }
        if ($bytes[$i] -eq 10) {
            if ($i -gt 0 -and $bytes[$i - 1] -eq 13) { $hasCrlf = $true } else { $hasLfOnly = $true }
        }
    }

    if ($hasCrlf -and $hasLfOnly) { $mixedEolFiles += $path }
    if ($path -match '\.(ps1|sh)$' -and $hasAnyCr) { $badCrScripts += $path }
}

$hasBlockingIssues = ($mixedEolFiles.Count -gt 0) -or ($badCrScripts.Count -gt 0)

# Exit if nothing to report at all
if (-not $hasDiffIssues -and -not ($hasStagedPs1 -and $ps1RuleMissing) -and -not $hasBlockingIssues) {
    exit 0
}

# --- 5. Build additionalContext ---
$contextLines = @()
$contextLines += '[LINE ENCODING VALIDATOR — H-GIT01]'
$contextLines += 'Line-ending check triggered by git add/commit.'
$contextLines += ''

if ($hasBlockingIssues) {
    $contextLines += 'BLOCKING LINE-ENDING DEFECTS:'
    if ($mixedEolFiles.Count -gt 0) {
        $contextLines += '  Mixed line endings within a single file (some lines LF, some CRLF):'
        foreach ($f in $mixedEolFiles) { $contextLines += "    - $f" }
    }
    if ($badCrScripts.Count -gt 0) {
        $contextLines += '  CR byte present in a shell/PowerShell script (breaks execution on Linux/macOS/WSL — must be pure LF):'
        foreach ($f in $badCrScripts) { $contextLines += "    - $f" }
    }
    $contextLines += ''
    $contextLines += 'Action: fix the offending file(s) (re-save with consistent LF, or run'
    $contextLines += '  git add --renormalize <path>) and re-stage before committing.'
    $contextLines += ''
}

if ($hasDiffIssues) {
    $contextLines += 'WHITESPACE/LINE-ENDING WARNINGS (git diff --check --cached):'
    $contextLines += $diffCheckOutput.Trim()
    $contextLines += ''
    $contextLines += 'Action: Review the flagged files and normalise line endings before committing.'
    $contextLines += '  - For .ps1/.sh files: must be stored as LF (*.ps1/*.sh text eol=lf in .gitattributes).'
    $contextLines += '  - For all other text files: left to `* text=auto` — normalised to the OS of whoever checks the repo out, not hardcoded.'
    $contextLines += "  - Run: git add --renormalize . && git status to see the effect."
    $contextLines += ''
}

if ($hasStagedPs1 -and $ps1RuleMissing) {
    $contextLines += 'STAGED .ps1 FILES DETECTED — .gitattributes has no explicit *.ps1 rule.'
    $contextLines += 'Add "*.ps1 text eol=lf" to .gitattributes then re-stage:'
    $contextLines += '  git add .gitattributes'
    $contextLines += '  git add --renormalize <your-ps1-file>'
    $contextLines += ''
}

$contextLines += 'Reference: .gitattributes, .claude/rules/git-workflow.md'

$additionalContext = $contextLines -join "`n"

$hookOutput = [ordered]@{ hookEventName = "PreToolUse" }

if ($hasBlockingIssues) {
    $reasonParts = @()
    if ($mixedEolFiles.Count -gt 0) { $reasonParts += "$($mixedEolFiles.Count) file(s) with mixed line endings" }
    if ($badCrScripts.Count -gt 0)  { $reasonParts += "$($badCrScripts.Count) .ps1/.sh file(s) with CR bytes" }
    $hookOutput.permissionDecision       = "deny"
    $hookOutput.permissionDecisionReason = "H-GIT01: blocking line-ending defect(s) — " + ($reasonParts -join '; ') + ". See additionalContext for details."
}

$hookOutput.additionalContext = $additionalContext

$output = [ordered]@{
    hookSpecificOutput = $hookOutput
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
