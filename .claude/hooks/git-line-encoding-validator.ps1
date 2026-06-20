#!/usr/bin/env pwsh
# H-GIT01: PreToolUse (Bash|PowerShell) — Pre-Commit Line Encoding Validator
# Detects git add / git commit commands and runs git diff --check to surface
# whitespace and line-ending warnings before the command executes.
# Non-blocking: injects additionalContext only — commit proceeds after operator review.
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

# --- 1. Check staged files for whitespace / line-ending issues ---
$diffCheckOutput = (git -C $cwd diff --check --cached 2>&1) -join "`n"
$hasDiffIssues   = ($diffCheckOutput -and $diffCheckOutput.Trim() -ne '')

# --- 2. Identify staged .ps1 files ---
$stagedFiles   = (git -C $cwd diff --cached --name-only 2>$null) -join "`n"
$hasStagedPs1  = ($stagedFiles -match '\.ps1$')

# --- 3. Verify .gitattributes covers .ps1 ---
$gitattributes = Join-Path $cwd '.gitattributes'
$ps1RuleMissing = $true
if (Test-Path $gitattributes) {
    $content = Get-Content $gitattributes -Raw
    if ($content -match '(?m)^\*\.ps1\s+text') {
        $ps1RuleMissing = $false
    }
}

# Exit if nothing to report
if (-not $hasDiffIssues -and -not ($hasStagedPs1 -and $ps1RuleMissing)) {
    exit 0
}

# --- 4. Build additionalContext ---
$contextLines = @()
$contextLines += '[LINE ENCODING VALIDATOR — H-GIT01]'
$contextLines += 'Line-ending check triggered by git add/commit.'
$contextLines += ''

if ($hasDiffIssues) {
    $contextLines += 'WHITESPACE/LINE-ENDING WARNINGS (git diff --check --cached):'
    $contextLines += $diffCheckOutput.Trim()
    $contextLines += ''
    $contextLines += 'Action: Review the flagged files and normalise line endings before committing.'
    $contextLines += '  - For .ps1 files: should be stored as LF (*.ps1 text eol=lf in .gitattributes).'
    $contextLines += '  - For .md/.json/.py/.html: should be stored as LF, CRLF on checkout.'
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

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "PreToolUse"
        additionalContext = $additionalContext
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
