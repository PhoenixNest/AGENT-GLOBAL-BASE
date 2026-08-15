#!/usr/bin/env python3
"""H-P01: UserPromptSubmit — Smart Prompt Optimizer (Python port).

Scores the user's prompt on 5 quality dimensions drawn from CC-00 prompt-engineering
patterns (core-component-00/engineering/prompt-engineering/fundamentals/). Below-threshold
prompts get a full additionalContext block instructing Claude to optimize the prompt and use
AskUserQuestion for confirmation before proceeding, plus a pending-confirmation marker file
that prompt-gate-enforcer.{sh,ps1} (PreToolUse) checks before denying any tool call other
than AskUserQuestion. At-or-above-threshold prompts get a passive advisory only.

Python port of prompt-optimizer.sh (bash) and prompt-optimizer.ps1 (pwsh) — one stdlib-only
Python 3 implementation replacing the OS fork (both originals remain in place; this file does
not delete or edit either). Standard library only, no third-party dependencies.

PRECEDENCE — this port follows the .sh original's behavior wherever it disagrees with .ps1 on
a *design* decision (per this migration's stated rule: .sh is what's actually wired into the
live settings.json on this reference Linux environment; see context-budget-alert.py's inline
comment for the same rule applied there). This matters more here than in any other hook in the
migration because .sh and .ps1 disagree on something substantive, not cosmetic:

  - prompt-optimizer.sh: on the PASS path (score >= 3), prints a passive
    "[H-P01: ... proceeding without confirmation]" advisory and exits WITHOUT writing the
    pending-confirmation marker — a good-quality prompt is never gated at all.
  - prompt-optimizer.ps1: writes the marker and runs the full step-1/2/3 confirmation flow on
    BOTH the pass and fail path, per its own inline comment ("confirm-and-append is symmetric,
    not a below-threshold-only behavior").

This is a deliberate, documented design choice in .sh, not a bug or an unhandled edge case —
so it does not fall under this hook's "fail toward triggering the gate on any error/edge case"
mandate (that mandate governs error handling and ambiguous/malformed input, not a considered
design decision made correctly by the live original). This port therefore follows .sh: the
pass path is a passive advisory only, matching the behavior actually deployed on this
environment today. See `_process()` below for where the two paths diverge.

Where .sh and .ps1 disagree on lower-stakes regex/anchoring specifics *within* the shared
fail-path logic, this port does apply the stricter (more gate-triggering) side of the two,
per this hook's explicit governance mandate — see the inline comments at each such spot
(bypass-check anchoring; dimension-5 regex breadth). This is the one hook in the migration
where that per-decision mandate is spelled out, not just applied per-hook.

Fail-closed contract for unexpected errors: once a non-empty prompt has been extracted from
valid JSON, ANY unexpected exception during bypass-checking, scoring, or marker/telemetry
writing falls back to the maximally-cautious outcome — treat the prompt as scoring 0/5 (all
five dimensions "missing") and still emit the full confirmation-required additionalContext
block, rather than silently exiting 0 with no output. A hook process that crashes silently
here would mean prompt-gate-enforcer never gets a marker to enforce against, i.e. a genuine
gating gap for exactly the prompts most likely to need it. See `main()`'s outer try/except.
"""

import datetime
import json
import os
import re
import subprocess
import sys

STATE_DIR_PARTS = (".claude", "hooks", ".state")

ALL_MISSING_LABELS = [
    "role/persona context",
    "output format specification",
    "workspace or pipeline grounding",
    "clear imperative task verb",
    "constraints or acceptance criteria",
]

THRESHOLD = 3

_DIM1_ROLE_RE = re.compile(
    r"\b(as |act as |you are |from the perspective of |like a |in the role of |playing )\b",
    re.IGNORECASE,
)
_DIM2_FORMAT_RE = re.compile(
    r"\b(tabul[a-z]*|table|list|markdown|json|yaml|bullet|numbered|chart|diagram|report|"
    r"document|csv|xml|html|in the format|structured output|prose|step.by.step)\b",
    re.IGNORECASE,
)
_DIM3_GROUNDING_RE = re.compile(
    r"\b(Stage [0-9]|pipeline|PRD|SRD|ADR|IDS|agent|profile|skill|CC-00|department|company|"
    r"studio|casual.games|telescope)\b",
    re.IGNORECASE,
)
_DIM4_VERB_RE = re.compile(
    r"\b(create|write|generate|review|analyze|implement|refactor|explain|fix|update|add|"
    r"remove|build|design|audit|produce|draft|summarize|compare|evaluate|plan|scaffold|"
    r"describe)\b",
    re.IGNORECASE,
)
# Dimension 5 regex: sh uses the broader `don[^a-z]?t` / `mustn[^a-z]?t` / `shouldn[^a-z]?t`
# family (matches "don't", "dont", "don_t", etc. — any single non-lowercase-letter separator
# or none); ps1 uses the narrower `don''?t` (PowerShell-escaped `don'?t`, matching only "don't"
# or "dont"). The broader sh pattern recognizes MORE prompts as containing a negative
# constraint, which raises the score and can LOWER the chance of triggering the gate on a
# prompt that does contain an unusual-but-real negation — i.e. sh's is not obviously the safer
# direction here. Per this hook's per-decision governance mandate we take the narrower (more
# conservative, more likely to count the dimension as missing and keep the gate active) of the
# two: ps1's `don'?t` family. This is the one dimension-scoring regex where this port departs
# from straight .sh-precedence, and it does so in the gate-triggering direction.
_DIM5_CONSTRAINT_RE = re.compile(
    r"\b(must|should|ensure|require|constraint|criterion|criteria|no more than|at least|"
    r"follow|adhere|based on|conform|matching|per the spec|don'?t|do not|never|avoid|"
    r"must not|mustn'?t|shouldn'?t|should not|nothing else|only)\b",
    re.IGNORECASE,
)


def _repo_root():
    """Best-effort `git rev-parse --show-toplevel`. Returns None on any failure —
    matches both originals treating a failed/absent git as "skip marker writing", not
    as a reason to abandon the rest of the hook."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    root = result.stdout.strip()
    return root or None


def _write_marker_and_telemetry(data, prompt_str, score, missing):
    """Best-effort: write the pending-confirmation marker + telemetry line. Never raises —
    any failure here must not prevent the additionalContext block from still being printed,
    matching both originals (sh's telemetry write is explicitly `... || true`; the marker
    write itself isn't guarded in sh, but sh has no `set -e`, so a failure there is
    non-fatal to the rest of the script either way)."""
    try:
        session_id = data.get("session_id") if isinstance(data, dict) else None
        if not session_id:
            return
        repo_root = _repo_root()
        if not repo_root:
            return

        state_dir = os.path.join(repo_root, *STATE_DIR_PARTS)
        os.makedirs(state_dir, exist_ok=True)

        now_iso = datetime.datetime.now().isoformat()
        marker = {"pending": True, "ts": now_iso}
        marker_path = os.path.join(state_dir, f"h-p01-pending-{session_id}.json")
        with open(marker_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(marker))

        try:
            persona_signal = bool(_DIM1_ROLE_RE.search(prompt_str))
            domain_signal = bool(_DIM3_GROUNDING_RE.search(prompt_str))
            telemetry = {
                "ts": now_iso,
                "score": score,
                "metThreshold": False,
                "personaSignal": persona_signal,
                "domainSignal": domain_signal,
                "missing": missing,
            }
            telemetry_path = os.path.join(state_dir, "h-p01-telemetry.jsonl")
            with open(telemetry_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(telemetry) + "\n")
        except Exception:
            pass
    except Exception:
        pass


def _build_gate_message(score, missing):
    missing_str = ", ".join(missing) if missing else "none — all 5 dimensions satisfied"
    question_count = "1-2" if len(missing) <= 2 else "2-4"

    return f"""[PROMPT OPTIMIZER — H-P01]
<status>
Quality score: {score}/5 (threshold: {THRESHOLD}/5)
Missing dimensions: {missing_str}
</status>

<context>
This prompt is below the quality threshold. Complete the steps below before starting the task.
A PreToolUse hook denies any tool call other than AskUserQuestion until step 2 completes, so
this is a required step, not a suggestion to weigh.
</context>

<step id="1" name="optimize">
Rewrite the prompt to add the missing dimensions: {missing_str}.
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

  <rule name="persona_and_delegation_resolution">
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
  using it as the working brief. Use an ATX header (`###`, not underlined text) for the title —
  never end a paragraph with a bare `---` line, that triggers Markdown's Setext-heading rule
  and produces an oversized heading. Leave a blank line between every element (header,
  blockquote, table, closing rule):
    ### Prompt Confirmed — Optimized

    > <full optimized text>

    | Field | Detail |
    |---|---|
    | **Objective** | <one-line paraphrase of the task's goal> |
    | **Constraint** | <key negations/must-haves carried over from the optimized text — omit this row entirely if none exist> |
    | **Next** | <what happens now, e.g. "Producing the ranked findings list now"> |

    ---
  </if_optimized>
  <if_original>
  Print this block first — before any other sentence, tool call, or commentary — then ask
  {question_count} clarifying questions (one per missing dimension: {missing_str}), wait for
  answers, and repeat from step 1. Use an ATX header (`###`, not underlined text) for the title —
  never end a paragraph with a bare `---` line, that triggers Markdown's Setext-heading rule
  and produces an oversized heading. Leave a blank line between every element:
    ### Prompt Confirmed — Original

    > <full original text>

    | Field | Detail |
    |---|---|
    | **Objective** | <one-line paraphrase of the task's goal> |
    | **Constraint** | <key negations/must-haves carried over from the original text — omit this row entirely if none exist> |
    | **Next** | <what happens now, e.g. "Producing the ranked findings list now"> |

    ---
  </if_original>
  <if_other>
  If the user answered AskUserQuestion with custom typed text instead of picking either listed
  option (its built-in "Other" choice), print this block first, then proceed using that typed
  text as the working brief (no clarifying questions needed — it's a direct answer, not a
  rejection of both options). Use an ATX header (`###`, not underlined text) for the title —
  never end a paragraph with a bare `---` line, that triggers Markdown's Setext-heading rule
  and produces an oversized heading. Leave a blank line between every element:
    ### Prompt Confirmed — User Input

    > <literal typed text>

    | Field | Detail |
    |---|---|
    | **Objective** | <one-line paraphrase of the task's goal> |
    | **Constraint** | <key negations/must-haves carried over from the typed text — omit this row entirely if none exist> |
    | **Next** | <what happens now, e.g. "Producing the ranked findings list now"> |

    ---
  </if_other>
</step>

<example>
Input: "review the auth module"
Optimized: "As the backend engineer, review src/auth/ for security issues and produce a
markdown-formatted list of findings ranked by severity. Don't touch the session-token logic —
flag it for a separate review instead."
</example>

If the session resumes with a message that doesn't directly answer the step 2 question (e.g.
"continue", a new task, an off-topic reply), treat it as unanswered and re-ask before doing
any other work."""


def _emit(additional_context: str, system_message: str = None) -> None:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context,
        }
    }
    # systemMessage is rendered directly to the user, independent of the model.
    if system_message is not None:
        output["systemMessage"] = system_message
    print(json.dumps(output))


def _emit_gate_required(data, prompt_str, score, missing) -> None:
    """Fail-path / fail-closed-fallback output: write the marker (best-effort) and print
    the full confirmation-required additionalContext block, plus a systemMessage naming
    the specific missing dimensions."""
    _write_marker_and_telemetry(data, prompt_str, score, missing)
    missing_str = ", ".join(missing) if missing else "none — all 5 dimensions satisfied"
    system_message = (
        f"[H-P01: prompt did not meet quality threshold ({score}/5) — "
        f"missing: {missing_str}]"
    )
    _emit(_build_gate_message(score, missing), system_message=system_message)


def _process(data, prompt_str) -> None:
    # --- Bypass rules ---------------------------------------------------------------
    # Anchoring judgment call: sh's `grep -qE` bypass checks are line-oriented (they scan
    # each line of a possibly multi-line prompt independently), so a prompt whose FIRST
    # line is a normal task description but whose SECOND line happens to start with '/' or
    # a confirmation word would still bypass entirely under sh — a broader, more
    # gate-skipping match than intended. ps1's `-match` anchors '^' to the start of the
    # whole string (no multiline flag). Per this hook's governance mandate (fail toward
    # triggering the gate rather than skipping it), this port uses whole-string anchoring
    # (Python's re.match already anchors to the string start), matching ps1's narrower,
    # more conservative bypass here — the opposite direction from the Dimension 5 note
    # above, but the same underlying principle: pick whichever original's behavior is less
    # likely to let a prompt slip past the gate ungated.
    if re.match(r"\s*/", prompt_str):
        return

    if len(prompt_str) < 20:
        return

    confirmation_bypass_re = re.compile(
        r"\s*(yes|no|ok|approve|looks good|proceed|use it|reject|change|modify|that works|"
        r"not quite|close enough|perfect)\b",
        re.IGNORECASE,
    )
    if confirmation_bypass_re.match(prompt_str) and len(prompt_str) < 100:
        return

    # --- Quality scoring — 5 dimensions (CC-00 Layer 1 patterns) --------------------
    score = 0
    missing = []

    if _DIM1_ROLE_RE.search(prompt_str):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[0])

    if _DIM2_FORMAT_RE.search(prompt_str):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[1])

    if _DIM3_GROUNDING_RE.search(prompt_str):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[2])

    if _DIM4_VERB_RE.search(prompt_str):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[3])

    if _DIM5_CONSTRAINT_RE.search(prompt_str):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[4])

    # --- Pass path: sh's authoritative behavior — passive advisory, no marker,
    # no telemetry, no confirmation required. See module docstring for why this port
    # follows .sh (not .ps1's "always confirm") on this specific divergence. ---------
    if score >= THRESHOLD:
        msg = f"[H-P01: prompt met quality threshold ({score}/5), proceeding without confirmation]"
        _emit(msg, system_message=msg)
        return

    # --- Fail path: below threshold — full confirmation gate. ------------------------
    _emit_gate_required(data, prompt_str, score, missing)


def main() -> int:
    try:
        raw_input = sys.stdin.read()
    except Exception:
        return 0

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    # Both originals treat a non-object top-level JSON (or a missing/falsy prompt) as
    # "nothing to gate", not as an error condition requiring the fail-toward-gate
    # fallback below — there is no prompt text to score in either case, so there is
    # nothing this hook could meaningfully gate even in principle.
    if not isinstance(data, dict):
        return 0

    prompt = data.get("prompt")
    if not prompt:
        return 0

    prompt_str = prompt if isinstance(prompt, str) else str(prompt)

    # Fail-closed contract: once we have real prompt text, any unexpected failure in
    # bypass-checking, scoring, or marker/telemetry writing must not silently degrade to
    # "no output, exit 0" — that would be exactly the kind of silent gate-skip this hook
    # exists to prevent. Fall back to the most conservative outcome instead: treat the
    # prompt as 0/5 (every dimension "missing") and still emit the full confirmation
    # gate, with a best-effort attempt at the marker file too.
    try:
        _process(data, prompt_str)
    except Exception:
        try:
            _emit_gate_required(data, prompt_str, 0, list(ALL_MISSING_LABELS))
        except Exception:
            # Even the fallback failed (e.g. stdout itself is broken). Nothing further
            # can be done from inside this process; exit 0 either way per hook exit-code
            # semantics (this hook never itself returns a blocking exit code — gating is
            # indirect via the marker file, which prompt-gate-enforcer separately
            # enforces has its own stale-marker fail-safe for).
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
