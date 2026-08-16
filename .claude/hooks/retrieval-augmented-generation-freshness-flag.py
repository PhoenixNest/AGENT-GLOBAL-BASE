#!/usr/bin/env python3
# H-RAG01: UserPromptSubmit — RAG Knowledge Freshness Flag (Python port)
# Detects prompts containing time-sensitive language and injects additionalContext
# requiring Claude to disclose knowledge cutoff, flag stale claims, and cite
# retrieval dates. Grounded in CC-00 RAG Engineering freshness architecture.
#
# Behavioral parity target: .claude/hooks/retrieval-augmented-generation-freshness-flag.ps1
# and .claude/hooks/retrieval-augmented-generation-freshness-flag.sh (bash port). This hook
# is advisory-only (UserPromptSubmit, never blocks/denies) — it always exits 0. The safe
# default on any parse anomaly or unexpected error is therefore "exit 0, emit nothing"
# (no additionalContext injected), which is exactly what both originals fall back to.
#
# No repo-root resolution in this file by design: unlike prompt-gate-enforcer/-clear (which
# resolve repo_root internally to locate a session marker file), neither original here calls
# `git rev-parse --show-toplevel` itself — that resolution happens once in the settings.json
# wrapper (`r=$(git rev-parse --show-toplevel) && bash "$r/.claude/hooks/....sh"`), which then
# invokes the script by absolute path. This script needs no filesystem location of its own.

import json
import re
import sys

from _hook_log import log_invocation

FRESHNESS_PATTERNS = [
    r"\b(latest version|most recent version|current version)\b",
    r"\b(as of today|as of now|right now|currently|at the moment)\b",
    r"\b(latest release|new release|recent release)\b",
    r"\b(up to date|up-to-date|what.s new)\b",
    r"\b(this year|in \d{4}|recent changes|recently added|just released)\b",
    r"\b(what version|which version|is.+supported|does.+support)\b",
]

ADDITIONAL_CONTEXT = """[RAG FRESHNESS FLAG — H-RAG01]
This prompt contains time-sensitive language.

Before responding, apply CC-00 RAG freshness protocol:
1. Disclose your knowledge cutoff (August 2025) when it affects accuracy
2. Mark potentially stale claims with [Knowledge Cutoff - verify]
3. If workspace telescope/ research reports exist on this topic, cite them
4. Prefer workspace documents (pipeline.md, library/, CC-00 docs) over training knowledge for workspace-specific facts
5. If retrieving external information, state the retrieval date
Reference: CC-00 RAG Engineering — retrieval freshness and source attribution"""


def run() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    if not isinstance(data, dict):
        return 0

    prompt = data.get("prompt")
    if not prompt:
        return 0

    if not isinstance(prompt, str):
        # Mirror the bash port's behavior: its prompt value is round-tripped through a
        # Python print() before bash ever sees it, which stringifies non-string JSON
        # values (numbers/bools) before any pattern matching happens.
        prompt = str(prompt)

    # Skip slash commands. CONFIRMED DIVERGENCE between the two originals, live-tested:
    # the .sh port's `echo "$prompt" | grep -qE '^[[:space:]]*/'` matches per-LINE, not
    # per-string, because grep evaluates "^" against the start of every line it reads —
    # for a multi-line prompt such as "What is the current version of Node.js?\n/sub cmd",
    # bash silently swallows the freshness flag (a line further down happens to start
    # with "/"), while the .ps1's non-multiline `-match '^\s*/'` only looks at the true
    # start of the whole prompt and would emit the flag for that same input.
    #
    # Per this migration's precedence rule (see context-budget-alert.py's header comment
    # and the workspace's live settings.json wiring): when the two originals disagree,
    # the port must follow the .sh original, since bash is what settings.json actually
    # invokes on this reference environment — not whichever behavior "reads as more
    # correct." An earlier revision of this port got this backwards (deliberately chose
    # the .ps1 per-string semantics, reasoning it was the "more correct" reading of "skip
    # slash commands") — that was a real behavioral bug relative to this migration's own
    # contract, not a defensible judgment call, and has been reverted here. re.MULTILINE
    # makes Python's `^` match at the start of every line (immediately after each `\n`),
    # not just the start of the string — the direct equivalent of grep's per-line `^`
    # anchor — so this now matches the .sh original's per-line behavior exactly.
    if re.search(r"^\s*/", prompt, re.MULTILINE):
        return 0

    session_id = data.get("session_id") if isinstance(data, dict) else None

    detected = any(
        re.search(pattern, prompt, re.IGNORECASE) for pattern in FRESHNESS_PATTERNS
    )
    if not detected:
        log_invocation("retrieval-augmented-generation-freshness-flag", "UserPromptSubmit",
                        decision="no_signal", session_id=session_id)
        return 0

    log_invocation("retrieval-augmented-generation-freshness-flag", "UserPromptSubmit",
                    decision="freshness_flag", session_id=session_id)

    output = {
        "systemMessage": "[H-RAG01: time-sensitive language detected — freshness protocol applied]",
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": ADDITIONAL_CONTEXT,
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except Exception:
        # Never let an unexpected error surface as a non-zero exit for this advisory-only
        # hook — both originals only ever exit 0 (see header note).
        sys.exit(0)
