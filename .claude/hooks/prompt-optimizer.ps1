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
if ($prompt -match '(?i)\b(table|list|markdown|json|yaml|bullet|numbered|in the format|structured output|prose|step.by.step)\b') {
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

# Dimension 4: Clear imperative task verb (starts with one)
if ($prompt -match '(?i)^\s*(create|write|generate|review|analyze|implement|refactor|explain|fix|update|add|remove|build|design|audit|produce|draft|summarize|compare|evaluate|plan|scaffold|describe)') {
    $score++
} else {
    $missing += 'clear imperative task verb'
}

# Dimension 5: Constraints or acceptance criteria
if ($prompt -match '(?i)\b(must|should|ensure|require|constraint|criterion|criteria|no more than|at least|follow|adhere|based on|conform|matching|per the spec)\b') {
    $score++
} else {
    $missing += 'constraints or acceptance criteria'
}

$threshold = 3
if ($score -ge $threshold) { exit 0 }

$missingStr  = $missing -join ', '
$complexity  = if ($missing.Count -le 2) { 'simple' } else { 'complex' }
$questionCount = if ($complexity -eq 'simple') { '1-2' } else { '2-4' }

$additionalContext = @"
[PROMPT OPTIMIZER — H-P01]
Quality score: $score/5 (threshold: $threshold/5)
Missing dimensions: $missingStr

MANDATORY OPTIMIZATION PROTOCOL — follow these steps before doing any other work:

STEP 1 — Generate an improved version of the user's prompt that adds the missing dimensions:
  $missingStr
  Keep the original intent exactly. Only improve clarity, specificity, and structure.
  Ground the optimized prompt in workspace conventions (CC-00 patterns, pipeline stages,
  agent roles, etc.) where relevant.

STEP 2 — Use the AskUserQuestion tool with a SINGLE question presenting:
  Option A: Your optimized version (label it "Optimized — recommended")  ← ALWAYS FIRST
  Option B: Original prompt (label it "Original")
  Ask: "Does the optimized prompt capture your intent? ⏱ Auto-selecting Optimized in ~30 seconds if no response."
  IMPORTANT — two mandatory formatting rules:
  1. Optimized MUST be listed first (Option A) so the default top-of-list selection is the
     improved prompt, preventing accidental selection of the Original.
  2. EVERY option MUST include a `preview` field containing the FULL prompt text for that
     option. This locks the UI into side-by-side layout so the user can read the complete
     prompt before choosing. Never omit the `preview` field — omitting it collapses the
     display back to a plain list with truncated descriptions.

STEP 3a — If the user approves (selects Optimized / says yes / looks good):
  Before executing, display a confirmation block in this exact format:
    ---
    **Prompt selected:** Optimized
    **Working brief:** <insert the full optimized prompt text here>
    ---
  Then proceed to execute the task using the OPTIMIZED prompt as your working brief.

STEP 3b — If the user rejects (selects Original / says no / wants changes):
  Display a confirmation block in this exact format:
    ---
    **Prompt selected:** Original
    **Working brief:** <insert the full original user prompt text here>
    ---
  Then ask $questionCount targeted clarifying questions (one per missing dimension from: $missingStr).
  Wait for answers, then re-run STEP 1 with the feedback incorporated, then STEP 2 again.
  Repeat until the user approves.

TIMEOUT / UNATTENDED FALLBACK (30-second rule) — If the user does not respond to the
AskUserQuestion within ~30 seconds, or if the session resumes with a new message that does NOT
directly answer the prompt-selection question (e.g., "continue", "I'm back", a new task, or
any off-topic reply), treat silence/bypass as approval of the Optimized version:
  1. Display the Optimized confirmation block.
  2. Proceed with the OPTIMIZED prompt as your working brief.
  Never stall the session indefinitely waiting for a prompt-selection response.

Do NOT skip this protocol. The prompt quality gate requires confirmation before task execution.
Anchored in CLAUDE.md §11 — active after every /compact. Prior summaries do not satisfy this.
"@

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "UserPromptSubmit"
        additionalContext = $additionalContext
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
