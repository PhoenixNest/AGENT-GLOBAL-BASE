#!/usr/bin/env pwsh
# H-MAE02: PreToolUse (Bash|PowerShell) — Multi-Agent Commit Format Guard
# On agent/* branches, validates that git commit messages follow the required format:
#   Subject: agent/<name>: <verb-phrase>  (imperative, ≤72 chars)
#   Body:    at least one hyphen-bulleted change line
# Bodyless single-line agent commits are a P2 defect per CLAUDE.md §6.
# Reference: core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$command = $data.tool_input.command
if (-not $command) { exit 0 }

# Only intercept git commit commands
if ($command -notmatch '\bgit\s+commit\b') { exit 0 }

# Determine current branch — use cwd from hook input for reliability
$cwd = $data.cwd
$currentBranch = $null
if ($cwd) {
    $currentBranch = (git -C $cwd rev-parse --abbrev-ref HEAD 2>$null)
} else {
    $currentBranch = (git rev-parse --abbrev-ref HEAD 2>$null)
}

# Only enforce on agent branches
if ($currentBranch -notmatch '^agent/' -and $currentBranch -notmatch '^stage\d+/agent/') {
    exit 0
}

# Extract commit message from -m "..." or --message "..." (simple string form only)
# Heredoc forms (@'...'@ or <<'EOF') are allowed through — too complex to parse reliably
$commitMsg = $null
if ($command -match '(?s)(?:-m|--message)\s+"((?:[^"\\]|\\.)*)"') {
    $commitMsg = $Matches[1]
} elseif ($command -match "(?s)(?:-m|--message)\s+'((?:[^'\\]|\\.)*)'") {
    $commitMsg = $Matches[1]
}

if (-not $commitMsg) { exit 0 }

$lines   = $commitMsg -split "`n"
$subject = $lines[0].Trim()

# Validate subject format: agent/<name>: <verb-phrase>
if ($subject -notmatch '^agent/[^:]+:\s+\S') {
    $output = [ordered]@{
        hookSpecificOutput = [ordered]@{
            hookEventName            = "PreToolUse"
            permissionDecision       = "deny"
            permissionDecisionReason = "[COMMIT FORMAT GUARD — H-MAE02] Agent commit subject '$subject' does not match required format 'agent/<name>: <verb-phrase>' (imperative, ≤72 chars). This is a P2 defect per CLAUDE.md §6. Example: 'agent/backend: add authentication endpoint'. Reference: core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md."
        }
    } | ConvertTo-Json -Depth 3 -Compress
    Write-Output $output
    exit 0
}

# Validate body — at least one hyphen-bulleted line after a blank separator
$hasBody = $false
foreach ($line in ($lines | Select-Object -Skip 2)) {
    if ($line.Trim() -match '^-\s+\S') {
        $hasBody = $true
        break
    }
}

if (-not $hasBody) {
    $output = [ordered]@{
        hookSpecificOutput = [ordered]@{
            hookEventName            = "PreToolUse"
            permissionDecision       = "deny"
            permissionDecisionReason = "[COMMIT FORMAT GUARD — H-MAE02] Agent commit is missing a hyphen-bulleted body. Bodyless single-line commits are a P2 defect per CLAUDE.md §6. Add a blank line then at least one '- <discrete change>' bullet after the subject line."
        }
    } | ConvertTo-Json -Depth 3 -Compress
    Write-Output $output
    exit 0
}

exit 0
