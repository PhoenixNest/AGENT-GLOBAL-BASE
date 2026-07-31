#!/usr/bin/env python3
"""H-P02: UserPromptSubmit -- Pipeline Stage Context Injector (Python port).

Runs LAST in the UserPromptSubmit chain (after optimizer). Detects pipeline-stage
signals in the prompt and injects the canonical stage reference as additionalContext
so Claude reads the gate criteria before responding.

Python port of pipeline-context-injector.ps1 / pipeline-context-injector.sh.
Standard library only -- no third-party dependencies. Behavior (stdin handling,
repo-root resolution, stage-signal regex table and match order, stdout JSON shape,
and exit-code semantics) is intended to be identical to both originals. This hook
is advisory-only (it can only add additionalContext, never deny/block a tool), so
every failure path below intentionally degrades to a silent `exit 0` -- matching
the fail-safe (not fail-closed) behavior of both originals for this particular hook.
"""

import json
import os
import re
import sys

# Ordered stage detection table -- (pattern, stage, label, hint).
# First match wins. Identical pattern set/order to both originals.
STAGE_SIGNALS = [
    (
        r"(Stage 1\b|requirements gathering|PRD\b|SRD\b|product requirements|user stories|acceptance criteria doc)",
        1,
        "Requirements + PRD/SRD",
        "Deliverables: PRD + SRD (must travel together). User Approval gate at end.",
    ),
    (
        r"(Stage 2\b|prototype|IDS\b|design spec|wireframe|mockup|interaction design)",
        2,
        "Prototype + IDS",
        "Deliverable: Interaction Design Spec (IDS). CDO owns this stage.",
    ),
    (
        r"(Stage 3\b|UML\b|ADR\b|architecture decision|technology decision|TSD\b|tech stack)",
        3,
        "UML + Architecture Decisions",
        "Technology Decision Lock applies at approval. ADRs are immutable after sign-off.",
    ),
    (
        r"(Stage 4\b|implementation plan|gantt|task breakdown|sprint planning|work breakdown)",
        4,
        "Implementation Plan + Gantt",
        "Progress monitoring (progress.md, session-log.md, checkpoint.json) starts here.",
    ),
    (
        r"(Stage 5\b|\bfeature implementation\b|write the code|build the feature|android impl|ios impl|backend impl)",
        5,
        "Development",
        "CTO owns cross-team coordination. Platform engineers own platform tracks.",
    ),
    (
        r"(Stage 6\b|code review|architectural audit|review the code|code quality review|defect clas)",
        6,
        "Code Review",
        "Full review panel. Stage 6 remediation restarts the full panel — no partial re-entry.",
    ),
    (
        r"(Stage 7\b|\bQA\b|testing phase|test cases|unit tests|integration tests|test suite)",
        7,
        "Testing + QA",
        "Coverage target: 80%+ for business logic. P0/P1 defects block release.",
    ),
    (
        r"(Stage 8\b|integrity|regression|security audit|penetration|MASVS|stealthy weakening)",
        8,
        "Integrity + Security",
        "Trim-to-Pass is itself a P0 defect. No feature removal to pass this stage.",
    ),
    (
        r"(Stage 9\b|localization|i18n\b|l10n\b|translation|string extraction|RTL)",
        9,
        "Localization (i18n)",
        "CTO-L owns this stage. ICU MessageFormat for plurals and gender. All strings must be externalized.",
    ),
    (
        r"(Stage 10\b|release\b|deploy\b|ship\b|launch\b|go.no.go|store submission|production deploy)",
        10,
        "Release",
        "Final gate: all P0/P1 resolved, regression + security scan + accessibility audit complete.",
    ),
]

PIPELINE_RELATIVE_PATHS = [
    ("company", "pipeline", "mobile-development", "pipeline.md"),
    ("company", "pipeline", "web-development", "pipeline.md"),
    ("company", "pipeline", "backend-api", "pipeline.md"),
    ("company", "pipeline", "full-stack", "pipeline.md"),
]


def _workspace_root() -> str:
    """Resolve the workspace root the same way both originals do: walk up two
    directories from this script's own location (hooks dir -> .claude -> repo
    root). This mirrors $PSScriptRoot/../.. (ps1) and
    $(cd "$(dirname BASH_SOURCE[0])/../.." && pwd) (sh) -- neither original
    actually shells out to `git rev-parse` from *inside* the script; the
    invocation wrapper in settings.json does that once to locate the script
    file itself, and the script then derives the root from its own path."""
    hooks_dir = os.path.dirname(os.path.abspath(__file__))
    claude_dir = os.path.dirname(hooks_dir)
    return os.path.dirname(claude_dir)


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    prompt = data.get("prompt") if isinstance(data, dict) else None
    if not prompt:
        return 0

    prompt_str = prompt if isinstance(prompt, str) else str(prompt)

    # Slash-command skip. The two originals actually DISAGREE here, and per
    # the repo-wide reconciliation rule (see context-budget-alert.py), the
    # port must follow the .sh original, since that is the version actually
    # wired into settings.json's UserPromptSubmit hook chain on this
    # reference environment:
    #   - .sh:  `echo "$prompt" | grep -qE '^[[:space:]]*/'` -- grep, with no
    #     `-z`, scans line by line, so `^` anchors to the start of EVERY
    #     line. A multi-line prompt whose FIRST line is plain text but whose
    #     SECOND (or later) line happens to start with `/` still matches and
    #     is skipped.
    #   - .ps1: `-match '^\s*/'` -- .NET regex `^` anchors to the start of
    #     the WHOLE string by default (no RegexOptions.Multiline), so only a
    #     prompt whose very first line starts with `/` is skipped.
    # Verified live: `printf 'Let us work on Stage 3\n/looks-like-a-command'`
    # matches the .sh original's grep (skips) but would not match the ps1
    # original's single-anchor regex. re.MULTILINE reproduces grep's
    # per-line anchor semantics, matching the .sh original.
    if re.search(r"^\s*/", prompt_str, re.MULTILINE):
        return 0

    detected = None
    for pattern, stage, label, hint in STAGE_SIGNALS:
        if re.search(pattern, prompt_str, re.IGNORECASE):
            detected = (stage, label, hint)
            break

    if detected is None:
        return 0

    stage, label, hint = detected

    workspace_root = _workspace_root()
    existing_docs = []
    for parts in PIPELINE_RELATIVE_PATHS:
        full_path = os.path.join(workspace_root, *parts)
        if os.path.isfile(full_path):
            existing_docs.append(f"  - {full_path}")

    doc_list = (
        "\n".join(existing_docs)
        if existing_docs
        else "  (no pipeline docs found at expected paths)"
    )

    context_note = f"""[PIPELINE CONTEXT INJECTOR — H-P02]
Detected stage signal: Stage {stage} — {label}
Stage hint: {hint}

Before responding, read the Stage {stage} section of the relevant pipeline.md:
{doc_list}

Key reminders for Stage {stage}:
- Satisfy all gate criteria before presenting the deliverable
- If this stage has a User Approval gate (marked with checkmark), present the deliverable
  and explicitly request sign-off — do not auto-advance
- P0/P1 defects are non-overridable and block progression"""

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context_note,
        }
    }

    # Both originals terminate stdout with a trailing newline here: the ps1
    # emits via `Write-Output` (always line-terminated) and the sh original's
    # inner `python3 -c "...print(json.dumps(...))"` uses `print`, which also
    # appends "\n". Use print() (not a bare sys.stdout.write) to match both.
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # This hook is advisory-only (additionalContext injection); it never
        # gates or denies a tool call. Both originals degrade to a silent,
        # no-output `exit 0` on any unexpected failure rather than propagate
        # an error into the hook chain -- preserved here as a safety net.
        sys.exit(0)
