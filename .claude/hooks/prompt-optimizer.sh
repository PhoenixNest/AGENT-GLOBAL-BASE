#!/usr/bin/env bash
# H-P01: UserPromptSubmit — Smart Prompt Optimizer (bash port)
# Scores the user's prompt on 5 quality dimensions drawn from CC-00 prompt-engineering
# patterns. Below-threshold prompts trigger additionalContext instructing Claude to
# optimize the prompt and use AskUserQuestion for confirmation before proceeding.

raw_input=$(cat)

prompt=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('prompt','') or '')")

[ -z "$prompt" ] && exit 0

prompt_len=$(printf '%s' "$prompt" | wc -m | tr -d '[:space:]')

# Bypass: slash commands, short inputs, and confirmation responses
echo "$prompt" | grep -qE '^[[:space:]]*/' && exit 0
[ "$prompt_len" -lt 20 ] && exit 0
if echo "$prompt" | grep -qiE '^[[:space:]]*(yes|no|ok|approve|looks good|proceed|use it|reject|change|modify|that works|not quite|close enough|perfect)\b' && [ "$prompt_len" -lt 100 ]; then
    exit 0
fi

# Quality scoring — 5 dimensions (CC-00 Layer 1 patterns)
score=0
missing=""

add_missing() { [ -z "$missing" ] && missing="$1" || missing="$missing, $1"; }

# Dimension 1: Role / persona signal
if echo "$prompt" | grep -qiE '\b(as |act as |you are |from the perspective of |like a |in the role of |playing )\b'; then
    score=$((score + 1))
else
    add_missing 'role/persona context'
fi

# Dimension 2: Explicit output format
if echo "$prompt" | grep -qiE '\b(table|list|markdown|json|yaml|bullet|numbered|in the format|structured output|prose|step.by.step)\b'; then
    score=$((score + 1))
else
    add_missing 'output format specification'
fi

# Dimension 3: Workspace / pipeline grounding
if echo "$prompt" | grep -qiE '\b(Stage [0-9]|pipeline|PRD|SRD|ADR|IDS|agent|profile|skill|CC-00|department|company|studio|casual.games|telescope)\b'; then
    score=$((score + 1))
else
    add_missing 'workspace or pipeline grounding'
fi

# Dimension 4: Clear imperative task verb (starts with one)
if echo "$prompt" | grep -qiE '^[[:space:]]*(create|write|generate|review|analyze|implement|refactor|explain|fix|update|add|remove|build|design|audit|produce|draft|summarize|compare|evaluate|plan|scaffold|describe)'; then
    score=$((score + 1))
else
    add_missing 'clear imperative task verb'
fi

# Dimension 5: Constraints or acceptance criteria
if echo "$prompt" | grep -qiE '\b(must|should|ensure|require|constraint|criterion|criteria|no more than|at least|follow|adhere|based on|conform|matching|per the spec)\b'; then
    score=$((score + 1))
else
    add_missing 'constraints or acceptance criteria'
fi

threshold=3
[ "$score" -ge "$threshold" ] && exit 0

# Count missing dimensions
missing_count=$(printf '%s' "$missing" | awk -F',' '{print NF}')
if [ "$missing_count" -le 2 ]; then
    question_count='1-2'
else
    question_count='2-4'
fi

msg="[PROMPT OPTIMIZER — H-P01]
Quality score: $score/5 (threshold: $threshold/5)
Missing dimensions: $missing

MANDATORY OPTIMIZATION PROTOCOL — follow these steps before doing any other work:

STEP 1 — Generate an improved version of the user's prompt that adds the missing dimensions:
  $missing
  Keep the original intent exactly. Only improve clarity, specificity, and structure.
  Ground the optimized prompt in workspace conventions (CC-00 patterns, pipeline stages,
  agent roles, etc.) where relevant.

STEP 2 — Use the AskUserQuestion tool with a SINGLE question presenting:
  Option A: Your optimized version (label it \"Optimized — recommended\")  ← ALWAYS FIRST
  Option B: Original prompt (label it \"Original\")
  Ask: \"Does the optimized prompt capture your intent? ⏱ Auto-selecting Optimized in ~30 seconds if no response.\"
  IMPORTANT — two mandatory formatting rules:
  1. Optimized MUST be listed first (Option A) so the default top-of-list selection is the
     improved prompt, preventing accidental selection of the Original.
  2. EVERY option MUST include a \`preview\` field containing the FULL prompt text for that
     option. This locks the UI into side-by-side layout so the user can read the complete
     prompt before choosing. Never omit the \`preview\` field — omitting it collapses the
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
  Then ask $question_count targeted clarifying questions (one per missing dimension from: $missing).
  Wait for answers, then re-run STEP 1 with the feedback incorporated, then STEP 2 again.
  Repeat until the user approves.

TIMEOUT / UNATTENDED FALLBACK (30-second rule) — If the user does not respond to the
AskUserQuestion within ~30 seconds, or if the session resumes with a new message that does NOT
directly answer the prompt-selection question (e.g., \"continue\", \"I'm back\", a new task, or
any off-topic reply), treat silence/bypass as approval of the Optimized version:
  1. Display the Optimized confirmation block.
  2. Proceed with the OPTIMIZED prompt as your working brief.
  Never stall the session indefinitely waiting for a prompt-selection response.

Do NOT skip this protocol. The prompt quality gate requires confirmation before task execution.
Anchored in CLAUDE.md §11 — active after every /compact. Prior summaries do not satisfy this."

MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'UserPromptSubmit','additionalContext':os.environ['MSG']}}))"
exit 0
