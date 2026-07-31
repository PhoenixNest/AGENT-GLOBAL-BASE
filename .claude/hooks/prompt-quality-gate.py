#!/usr/bin/env python3
"""H-P03: UserPromptSubmit — ASGF Compliance Quality Gate (Python port).

Runs FIRST in the UserPromptSubmit chain. Blocks prompts that would
instruct agents to violate ASGF governance rules, skip pipeline gates,
override P0/P1 severity, or perform a Trim-to-Pass / force-push-to-master
maneuver.

Python port of prompt-quality-gate.ps1 / prompt-quality-gate.sh (identical
behavior; part of the OS-fork removal migration — one script instead of a
pwsh/bash pair). Standard library only, no third-party dependencies.

Behavior parity: stdin JSON reading, prompt extraction, the five violation
regexes (pattern text and match order), the block-reason text layout, the
stdout JSON shape (`decision`/`reason`/`hookSpecificOutput`), and exit-code
semantics are all intended to be identical to both originals.

Fail-closed contract: this is a security/governance gate that can block a
prompt via `"decision": "block"` in its stdout JSON — neither original ever
signals a block via a non-zero exit code (Claude Code's UserPromptSubmit
hooks block via that JSON `decision` field, not via exit status), and both
originals *always* exit 0 on every path, blocked or not. So "fail closed"
for this specific hook means: never let a Python-side error swallow a
would-be block. Regex evaluation here uses only fixed, known-safe patterns
against a plain string, so it cannot itself raise; the sole intentional
early-exit path (unparseable JSON / missing or empty prompt) matches both
originals, which treat "nothing to scan" as nothing to block on — not a
security bypass, since there is no prompt text to have violated a rule in
the first place. The outer guard below exists only so that a wholly
unforeseen error still exits 0 like both originals do, never with a
traceback and non-zero status that could look like something other than
"no violation detected."
"""

import json
import re
import sys

# (pattern, rule) — identical pattern text and order to both originals.
VIOLATIONS = [
    (
        r"skip.{0,40}(stage|gate|pipeline|review|approval)",
        "Pipeline stages cannot be skipped — CLAUDE.md §8 (hard stop)",
    ),
    (
        r"(downgrade|change|override|ignore|bypass).{0,40}(P0|P1|severity|defect|critical|blocker)",
        "P0/P1 defect classification is non-overridable — CLAUDE.md §8",
    ),
    (
        r"(remove|weaken|disable|trim|strip).{0,30}(feature|security|functionality|test).{0,30}(pass|review|gate|check)",
        "Trim-to-Pass is a P0 defect — removing features to pass a review is blocked — CLAUDE.md §8",
    ),
    (
        r"(force.{0,10}push|push.{0,10}--force).{0,20}(master|main)",
        "Force-pushing to master is prohibited — CLAUDE.md §6, rules/git-workflow.md",
    ),
    (
        r"auto.{0,20}advance.{0,20}(stage|gate|pipeline)",
        "Auto-advancing past User Approval gates is forbidden — CLAUDE.md §8",
    ),
]


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

    detected = []
    for pattern, rule in VIOLATIONS:
        if re.search(pattern, prompt_str, re.IGNORECASE):
            detected.append(rule)

    if not detected:
        return 0

    rule_list = "\n".join(f"  * {rule}" for rule in detected)

    reason = (
        "[PROMPT QUALITY GATE — H-P03] ASGF Compliance Violation Detected\n\n"
        "The following governance rules would be violated:\n"
        f"{rule_list}\n\n"
        "This prompt has been blocked. Please rephrase within the ASGF governance framework.\n"
        "Reference: CLAUDE.md §1, §6, §8 | core-component-00/agent-systems-governance-framework/governance/"
    )

    output = {
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
        },
    }

    # Use print() (not sys.stdout.write) so stdout gets the same trailing
    # newline the bash original's `python3 -c "...; print(json.dumps(...))"`
    # produces — a bare sys.stdout.write(json.dumps(...)) here would omit it,
    # a byte-for-byte mismatch even though most JSON consumers tolerate it.
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Defensive catch-all: both originals always exit 0 on every path
        # (there is no non-zero exit anywhere in either script). An
        # unforeseen error here must still exit 0, not surface a traceback
        # with a non-zero status that neither original could ever produce.
        sys.exit(0)
