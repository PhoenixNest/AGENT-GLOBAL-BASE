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
if echo "$prompt" | grep -qiE '\b(tabul[a-z]*|table|list|markdown|json|yaml|bullet|numbered|chart|diagram|report|document|csv|xml|html|in the format|structured output|prose|step.by.step)\b'; then
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

# Dimension 4: Clear imperative task verb (anywhere in prompt)
if echo "$prompt" | grep -qiE '\b(create|write|generate|review|analyze|implement|refactor|explain|fix|update|add|remove|build|design|audit|produce|draft|summarize|compare|evaluate|plan|scaffold|describe)\b'; then
    score=$((score + 1))
else
    add_missing 'clear imperative task verb'
fi

# Dimension 5: Constraints or acceptance criteria (including negative constraints)
negation_regex='\b(must|should|ensure|require|constraint|criterion|criteria|no more than|at least|follow|adhere|based on|conform|matching|per the spec|don[^a-z]?t|do not|never|avoid|must not|mustn[^a-z]?t|shouldn[^a-z]?t|should not|nothing else|only)\b'
if echo "$prompt" | grep -qiE "$negation_regex"; then
    score=$((score + 1))
else
    add_missing 'constraints or acceptance criteria'
fi

threshold=3
if [ "$score" -ge "$threshold" ]; then
    # Pass-path visibility: without this, a passing prompt and a non-running gate look
    # identical from the transcript. Passive signal only — no confirmation, no blocking.
    MSG="[H-P01: prompt met quality threshold ($score/5), proceeding without confirmation]" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'UserPromptSubmit','additionalContext':os.environ['MSG']}}))"
    exit 0
fi

# Structural enforcement: mark this session as having a pending confirmation.
# prompt-gate-enforcer.sh (PreToolUse) denies any tool but AskUserQuestion while this
# marker exists; prompt-gate-clear.sh (PostToolUse) removes it once that tool is called.
session_id=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('session_id','') or '')")
repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$repo_root" ] && [ -n "$session_id" ]; then
    state_dir="$repo_root/.claude/hooks/.state"
    mkdir -p "$state_dir"
    TS=$(python3 -c "import datetime; print(datetime.datetime.now().isoformat())")
    export TS
    python3 -c "import os,json; print(json.dumps({'pending': True, 'ts': os.environ['TS']}))" > "$state_dir/h-p01-pending-$session_id.json"

    # Log scoring signals for later false-routing-rate analysis. Best-effort: a logging
    # failure must never block prompt-optimization behavior.
    persona_signal=false
    echo "$prompt" | grep -qiE '\b(as |act as |you are |from the perspective of |like a |in the role of |playing )\b' && persona_signal=true
    domain_signal=false
    echo "$prompt" | grep -qiE '\b(Stage [0-9]|pipeline|PRD|SRD|ADR|IDS|agent|profile|skill|CC-00|department|company|studio|casual.games|telescope)\b' && domain_signal=true
    MISSING="$missing" PERSONA="$persona_signal" DOMAIN="$domain_signal" SCORE="$score" python3 -c "
import os, json, datetime
entry = {
    'ts': datetime.datetime.now().isoformat(),
    'score': int(os.environ['SCORE']),
    'metThreshold': False,
    'personaSignal': os.environ['PERSONA'] == 'true',
    'domainSignal': os.environ['DOMAIN'] == 'true',
    'missing': [m.strip() for m in os.environ['MISSING'].split(',') if m.strip()],
}
print(json.dumps(entry))
" >> "$state_dir/h-p01-telemetry.jsonl" 2>/dev/null || true
fi

# Count missing dimensions
missing_count=$(printf '%s' "$missing" | awk -F',' '{print NF}')
if [ "$missing_count" -le 2 ]; then
    question_count='1-2'
else
    question_count='2-4'
fi

msg="[PROMPT OPTIMIZER — H-P01]
<status>
Quality score: $score/5 (threshold: $threshold/5)
Missing dimensions: $missing
</status>

<context>
This prompt is below the quality threshold. Complete the steps below before starting the task.
A PreToolUse hook denies any tool call other than AskUserQuestion until step 2 completes, so
this is a required step, not a suggestion to weigh.
</context>

<step id=\"1\" name=\"optimize\">
Rewrite the prompt to add the missing dimensions: $missing.
Preserve the original intent exactly — improve clarity, specificity, and structure only.
Ground the rewrite in workspace conventions (CC-00 patterns, pipeline stages, agent roles)
where relevant.

  <rule name=\"negation_preservation\">
  If the original prompt contains an explicit negative constraint (don't, never, avoid, must
  not, only, nothing else), keep it verbatim. Do not rephrase, soften, generalize, or invert it.
  </rule>

  <rule name=\"relevance_guardrail\">
  Only add a dimension you can infer with high confidence from the original wording. If a
  dimension would require guessing intent, raise it as a clarifying question in step 3 instead
  of inventing content for it.
  </rule>

  <rule name=\"persona_and_delegation_resolution\">
  If the prompt names or clearly implies a specific real agent, persona, department, or module
  (not a generic invented role), apply CC-00 Prompt Engineering pattern P-013 (Persona
  Resolution): read that agent's actual profile.md and skills before responding, per the
  workspace Activation Protocol (CLAUDE.md §7, crew/CLAUDE.md) — never freehand voice or
  authority from the label alone. If the request could instead be delegated to a specific agent
  or a team of module/department leads, apply P-014 (Delegation Routing) and surface the
  proposed owner inside the step 2 confirmation, alongside the rewritten prompt — never apply
  routing silently. Never route a broad/uncategorizable fallback across an explicit
  organizational-independence boundary (e.g. ANU-00's independence from CC-00). See
  core-component-00/engineering/prompt-engineering/patterns/advanced-patterns.md.
  </rule>
</step>

<step id=\"2\" name=\"confirm\">
Call AskUserQuestion with one question and two options, using the plain list display (do NOT
set a preview field — that triggers a dual-pane panel that can truncate long text):
  - \"Optimized — recommended\" (always listed first) — description: full optimized prompt text
  - \"Original\" — description: full original prompt text
  Ask: \"Does the optimized prompt capture your intent?\"
</step>

<step id=\"3\" name=\"branch\">
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
  $question_count clarifying questions (one per missing dimension: $missing), wait for
  answers, and repeat from step 1:
    ---
    **Prompt selected:** Original
    **Working brief:** <full original text>
    ---
  </if_original>
</step>

<example>
Input: \"review the auth module\"
Optimized: \"As the backend engineer, review src/auth/ for security issues and produce a
markdown-formatted list of findings ranked by severity. Don't touch the session-token logic —
flag it for a separate review instead.\"
</example>

If the session resumes with a message that doesn't directly answer the step 2 question (e.g.
\"continue\", a new task, an off-topic reply), treat it as unanswered and re-ask before doing
any other work."

MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'UserPromptSubmit','additionalContext':os.environ['MSG']}}))"
exit 0
