#!/usr/bin/env pwsh
# H-P02: UserPromptSubmit — Pipeline Stage Context Injector
# Runs LAST in the UserPromptSubmit chain (after optimizer). Detects pipeline-stage
# signals in the prompt and injects the canonical stage reference as additionalContext
# so Claude reads the gate criteria before responding.

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$prompt = $data.prompt
if (-not $prompt) { exit 0 }
if ($prompt -match '^\s*/') { exit 0 }

# Stage keyword detection map — keyed by regex, value is stage metadata
$stageSignals = [ordered]@{
    '(?i)(Stage 1\b|requirements gathering|PRD\b|SRD\b|product requirements|user stories|acceptance criteria doc)' = @{
        stage = 1; label = 'Requirements + PRD/SRD'
        hint  = 'Deliverables: PRD + SRD (must travel together). User Approval gate at end.'
    }
    '(?i)(Stage 2\b|prototype|IDS\b|design spec|wireframe|mockup|interaction design)' = @{
        stage = 2; label = 'Prototype + IDS'
        hint  = 'Deliverable: Interaction Design Spec (IDS). CDO owns this stage.'
    }
    '(?i)(Stage 3\b|UML\b|ADR\b|architecture decision|technology decision|TSD\b|tech stack)' = @{
        stage = 3; label = 'UML + Architecture Decisions'
        hint  = 'Technology Decision Lock applies at approval. ADRs are immutable after sign-off.'
    }
    '(?i)(Stage 4\b|implementation plan|gantt|task breakdown|sprint planning|work breakdown)' = @{
        stage = 4; label = 'Implementation Plan + Gantt'
        hint  = 'Progress monitoring (progress.md, session-log.md, checkpoint.json) starts here.'
    }
    '(?i)(Stage 5\b|\bfeature implementation\b|write the code|build the feature|android impl|ios impl|backend impl)' = @{
        stage = 5; label = 'Development'
        hint  = 'CTO owns cross-team coordination. Platform engineers own platform tracks.'
    }
    '(?i)(Stage 6\b|code review|architectural audit|review the code|code quality review|defect clas)' = @{
        stage = 6; label = 'Code Review'
        hint  = 'Full review panel. Stage 6 remediation restarts the full panel — no partial re-entry.'
    }
    '(?i)(Stage 7\b|\bQA\b|testing phase|test cases|unit tests|integration tests|test suite)' = @{
        stage = 7; label = 'Testing + QA'
        hint  = 'Coverage target: 80%+ for business logic. P0/P1 defects block release.'
    }
    '(?i)(Stage 8\b|integrity|regression|security audit|penetration|MASVS|stealthy weakening)' = @{
        stage = 8; label = 'Integrity + Security'
        hint  = 'Trim-to-Pass is itself a P0 defect. No feature removal to pass this stage.'
    }
    '(?i)(Stage 9\b|localization|i18n\b|l10n\b|translation|string extraction|RTL)' = @{
        stage = 9; label = 'Localization (i18n)'
        hint  = 'CTO-L owns this stage. ICU MessageFormat for plurals and gender. All strings must be externalized.'
    }
    '(?i)(Stage 10\b|release\b|deploy\b|ship\b|launch\b|go.no.go|store submission|production deploy)' = @{
        stage = 10; label = 'Release'
        hint  = 'Final gate: all P0/P1 resolved, regression + security scan + accessibility audit complete.'
    }
}

$detected = $null
foreach ($pattern in $stageSignals.Keys) {
    if ($prompt -match $pattern) {
        $detected = $stageSignals[$pattern]
        break
    }
}

if (-not $detected) { exit 0 }

$workspaceRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$pipelinePaths = @(
    'company\pipeline\mobile-development\pipeline.md',
    'company\pipeline\web-development\pipeline.md',
    'company\pipeline\backend-api\pipeline.md',
    'company\pipeline\full-stack\pipeline.md'
)

$existingDocs = $pipelinePaths |
    ForEach-Object { Join-Path $workspaceRoot $_ } |
    Where-Object { Test-Path $_ } |
    ForEach-Object { "  - $_" }

$docList = if ($existingDocs) { $existingDocs -join "`n" } else { '  (no pipeline docs found at expected paths)' }

$contextNote = @"
[PIPELINE CONTEXT INJECTOR — H-P02]
Detected stage signal: Stage $($detected.stage) — $($detected.label)
Stage hint: $($detected.hint)

Before responding, read the Stage $($detected.stage) section of the relevant pipeline.md:
$docList

Key reminders for Stage $($detected.stage):
- Satisfy all gate criteria before presenting the deliverable
- If this stage has a User Approval gate (marked with checkmark), present the deliverable
  and explicitly request sign-off — do not auto-advance
- P0/P1 defects are non-overridable and block progression
"@

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "UserPromptSubmit"
        additionalContext = $contextNote
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
