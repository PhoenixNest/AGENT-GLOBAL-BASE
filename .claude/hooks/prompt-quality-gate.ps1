#!/usr/bin/env pwsh
# H-P03: UserPromptSubmit — ASE Compliance Quality Gate
# Runs FIRST in the UserPromptSubmit chain. Blocks prompts that would
# instruct agents to violate ASE governance rules, skip pipeline gates,
# override P0/P1 severity, or access denied files.

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$prompt = $data.prompt
if (-not $prompt) { exit 0 }

$violations = @(
    @{
        pattern = '(?i)skip.{0,40}(stage|gate|pipeline|review|approval)'
        rule    = 'Pipeline stages cannot be skipped — CLAUDE.md §8 (hard stop)'
    },
    @{
        pattern = '(?i)(downgrade|change|override|ignore|bypass).{0,40}(P0|P1|severity|defect|critical|blocker)'
        rule    = 'P0/P1 defect classification is non-overridable — CLAUDE.md §8'
    },
    @{
        pattern = '(?i)(read|open|access|load|view|check|parse).{0,30}(GEMINI\.md|\.gemini)'
        rule    = 'GEMINI.md and .gemini/** are explicitly denied to Claude Code — CLAUDE.md §1'
    },
    @{
        pattern = '(?i)(remove|weaken|disable|trim|strip).{0,30}(feature|security|functionality|test).{0,30}(pass|review|gate|check)'
        rule    = 'Trim-to-Pass is a P0 defect — removing features to pass a review is blocked — CLAUDE.md §8'
    },
    @{
        pattern = '(?i)(force.{0,10}push|push.{0,10}--force).{0,20}(master|main)'
        rule    = 'Force-pushing to master is prohibited — CLAUDE.md §6, rules/git-workflow.md'
    },
    @{
        pattern = '(?i)auto.{0,20}advance.{0,20}(stage|gate|pipeline)'
        rule    = 'Auto-advancing past User Approval gates is forbidden — CLAUDE.md §8'
    }
)

$detected = @()
foreach ($v in $violations) {
    if ($prompt -match $v.pattern) {
        $detected += $v.rule
    }
}

if ($detected.Count -eq 0) { exit 0 }

$ruleList = ($detected | ForEach-Object { "  * $_" }) -join "`n"

$output = [ordered]@{
    decision           = "block"
    reason             = "[PROMPT QUALITY GATE — H-P03] ASE Compliance Violation Detected`n`nThe following governance rules would be violated:`n$ruleList`n`nThis prompt has been blocked. Please rephrase within the ASE governance framework.`nReference: CLAUDE.md §1, §6, §8 | core-component-00/agent-systems-engineering/governance/"
    hookSpecificOutput = @{
        hookEventName = "UserPromptSubmit"
    }
} | ConvertTo-Json -Depth 3 -Compress

Write-Output $output
exit 0
