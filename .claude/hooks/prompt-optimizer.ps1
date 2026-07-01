#!/usr/bin/env pwsh
# H-P01: UserPromptSubmit — Smart Prompt Optimizer
# Scores the user's prompt on 5 quality dimensions drawn from CC-00 prompt-engineering
# patterns (core-component-00/prompt-engineering/fundamentals/). Below-threshold prompts
# trigger additionalContext instructing Claude to optimize the prompt and use
# AskUserQuestion for confirmation before proceeding with the actual task.
#
# Confirmation flow:
#   Approve  → Claude executes against the optimized prompt
#   Reject   → Claude asks 1-4 clarifying questions (complexity-dependent), re-optimizes, re-confirms

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$prompt = $data.prompt
if (-not $prompt) { exit 0 }

# Bypass: slash commands, greetings, short inputs, and confirmation responses
if ($prompt -match '^\s*/') { exit 0 }
if ($prompt.Length -lt 20) { exit 0 }
if ($prompt -match '(?i)^\s*(yes|no|ok|approve|looks good|proceed|use it|reject|change|modify|that works|not quite|close enough|perfect)\b' `
    -and $prompt.Length -lt 100) { exit 0 }

# Quality scoring — 5 dimensions (CC-00 Layer 1 patterns)
$score = 0
$missing = @()

# Dimension 1: Role / persona signal
if ($prompt -match '(?i)\b(as |act as |you are |from the perspective of |like a |in the role of |playing )\b') {
    $score++
} else {
    $missing += 'role/persona context'
}

# Dimension 2: Explicit output format
if ($prompt -match '(?i)\b(tabul\w*|table|list|markdown|json|yaml|bullet|numbered|chart|diagram|report|document|csv|xml|html|in the format|structured output|prose|step.by.step)\b') {
    $score++
} else {
    $missing += 'output format specification'
}

# Dimension 3: Workspace / pipeline grounding
if ($prompt -match '(?i)\b(Stage \d|pipeline|PRD|SRD|ADR|IDS|agent|profile|skill|CC-00|department|company|studio|casual.games|telescope)\b') {
    $score++
} else {
    $missing += 'workspace or pipeline grounding'
}

# Dimension 4: Clear imperative task verb (anywhere in prompt)
if ($prompt -match '(?i)\b(create|write|generate|review|analyze|implement|refactor|explain|fix|update|add|remove|build|design|audit|produce|draft|summarize|compare|evaluate|plan|scaffold|describe)\b') {
    $score++
} else {
    $missing += 'clear imperative task verb'
}

# Dimension 5: Constraints or acceptance criteria (including negative constraints)
if ($prompt -match '(?i)\b(must|should|ensure|require|constraint|criterion|criteria|no more than|at least|follow|adhere|based on|conform|matching|per the spec|don''?t|do not|never|avoid|must not|mustn''?t|shouldn''?t|should not|nothing else|only)\b') {
    $score++
} else {
    $missing += 'constraints or acceptance criteria'
}

$threshold = 3
if ($score -ge $threshold) { exit 0 }

# Structural enforcement: mark this session as having a pending confirmation.
# prompt-gate-enforcer.ps1 (PreToolUse) denies any tool but AskUserQuestion while this
# marker exists; prompt-gate-clear.ps1 (PostToolUse) removes it once that tool is called.
$repoRoot = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -eq 0 -and $data.session_id) {
    $stateDir = Join-Path $repoRoot '.claude/hooks/.state'
    if (-not (Test-Path $stateDir)) { New-Item -ItemType Directory -Path $stateDir -Force | Out-Null }
    $marker = [ordered]@{ pending = $true; ts = (Get-Date).ToString('o') } | ConvertTo-Json -Compress
    Set-Content -Path (Join-Path $stateDir "h-p01-pending-$($data.session_id).json") -Value $marker -NoNewline
}

$missingStr  = $missing -join ', '
$complexity  = if ($missing.Count -le 2) { 'simple' } else { 'complex' }
$questionCount = if ($complexity -eq 'simple') { '1-2' } else { '2-4' }

$additionalContext = @"
[PROMPT OPTIMIZER — H-P01]
<status>
Quality score: $score/5 (threshold: $threshold/5)
Missing dimensions: $missingStr
</status>

<context>
This prompt is below the quality threshold. Complete the steps below before starting the task.
A PreToolUse hook denies any tool call other than AskUserQuestion until step 2 completes, so
this is a required step, not a suggestion to weigh.
</context>

<step id="1" name="optimize">
Rewrite the prompt to add the missing dimensions: $missingStr.
Preserve the original intent exactly — improve clarity, specificity, and structure only.
Ground the rewrite in workspace conventions (CC-00 patterns, pipeline stages, agent roles)
where relevant.

  <rule name="negation_preservation">
  If the original prompt contains an explicit negative constraint (don't, never, avoid, must
  not, only, nothing else), keep it verbatim. Do not rephrase, soften, generalize, or invert it.
  </rule>

  <rule name="relevance_guardrail">
  Only add a dimension you can infer with high confidence from the original wording. If a
  dimension would require guessing intent, raise it as a clarifying question in step 3 instead
  of inventing content for it.
  </rule>
</step>

<step id="2" name="confirm">
Call AskUserQuestion with one question and two options, using the plain list display (do NOT
set a preview field — that triggers a dual-pane panel that can truncate long text):
  - "Optimized — recommended" (always listed first) — description: full optimized prompt text
  - "Original" — description: full original prompt text
  Ask: "Does the optimized prompt capture your intent?"
</step>

<step id="3" name="branch">
  <if_optimized>
  Print this block first — before any other sentence, tool call, or commentary — then execute
  using it as the working brief:
    ---
    **Prompt selected:** Optimized
    **Working brief:** <full optimized text>
    ---
  </if_optimized>
  <if_original>
  Print this block first — before any other sentence, tool call, or commentary — then ask
  $questionCount clarifying questions (one per missing dimension: $missingStr), wait for
  answers, and repeat from step 1:
    ---
    **Prompt selected:** Original
    **Working brief:** <full original text>
    ---
  </if_original>
</step>

<example>
Input: "review the auth module"
Optimized: "As the backend engineer, review src/auth/ for security issues and produce a
markdown-formatted list of findings ranked by severity. Don't touch the session-token logic —
flag it for a separate review instead."
</example>

If the session resumes with a message that doesn't directly answer the step 2 question (e.g.
"continue", a new task, an off-topic reply), treat it as unanswered and re-ask before doing
any other work.
"@

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "UserPromptSubmit"
        additionalContext = $additionalContext
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
