#!/usr/bin/env pwsh
# H-MAE01: PreToolUse (Bash|PowerShell) — Multi-Agent Branch Naming Guard
# Detects git commands that create new branches and validates the branch name
# against the workspace multi-agent naming convention:
#   agent/<role>/<task>  or  stage<N>/agent/<role>/<task>
# Reference: core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$command = $data.tool_input.command
if (-not $command) { exit 0 }

# Extract branch name from branch-creating commands
$branchName = $null

if ($command -match 'git\s+worktree\s+add\s+\S+\s+(?:-b\s+)?([a-zA-Z0-9/._-]+)') {
    $branchName = $Matches[1]
} elseif ($command -match 'git\s+checkout\s+-b\s+([a-zA-Z0-9/._-]+)') {
    $branchName = $Matches[1]
} elseif ($command -match 'git\s+switch\s+(?:--create|-c)\s+([a-zA-Z0-9/._-]+)') {
    $branchName = $Matches[1]
}

if (-not $branchName) { exit 0 }

# Valid branch patterns for this workspace
$validPatterns = @(
    '^agent/[^/]+/[^/]+$',              # agent/<role>/<task>
    '^stage\d+/agent/[^/]+/[^/]+$',    # stage<N>/agent/<role>/<task>
    '^(master|main|develop)$',           # standard trunk branches
    '^(company|studio)/.*$',             # workspace-scoped development branches
    '^(feature|fix|chore|docs|refactor|test)/.*$'  # standard git-flow branches
)

$isValid = $false
foreach ($pattern in $validPatterns) {
    if ($branchName -match $pattern) {
        $isValid = $true
        break
    }
}

if ($isValid) { exit 0 }

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName            = "PreToolUse"
        permissionDecision       = "deny"
        permissionDecisionReason = "[BRANCH NAMING GUARD — H-MAE01] Branch name '$branchName' does not follow workspace conventions. Multi-agent branches must be: agent/<role>/<task> or stage<N>/agent/<role>/<task> (e.g., agent/backend/dark-mode-api). Standard branches (feature/, fix/, company/, studio/) are also accepted. Reference: core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md and CLAUDE.md §6."
    }
} | ConvertTo-Json -Depth 3 -Compress

Write-Output $output
exit 0
