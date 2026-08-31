#!/usr/bin/env python3
# H-MAE02: PreToolUse (Bash|PowerShell) — Multi-Agent Commit Format Guard (Python port)
#
# On agent/* branches, validates that git commit messages follow the required format:
#   Subject: agent/<name>: <verb-phrase>  (imperative, <=72 chars)
#   Body:    at least one hyphen-bulleted change line
# Bodyless single-line agent commits are a P2 defect per CLAUDE.md §6.
# Reference: core-component-00/framework/05-multi-agent-engineering/fundamentals/git-worktree-orchestration.md
#
# Python port of multi-agent-commit-format-guard.ps1 / multi-agent-commit-format-guard.sh —
# implements identical stdin handling, branch resolution (via `cwd` + `git -C <cwd> rev-parse
# --abbrev-ref HEAD`, falling back to a plain `git rev-parse --abbrev-ref HEAD` when no `cwd` is
# given — this hook never itself shells out to `git rev-parse --show-toplevel`; that call lives
# only in settings.json's invocation wrapper, which is out of scope here), commit-message
# extraction, and subject/body validation as both originals, using only the standard library.
#
# This hook always exits 0. The actual PreToolUse "deny" is communicated via the
# hookSpecificOutput JSON printed to stdout (permissionDecision: "deny"), not via a nonzero
# process exit code — so every early-return path below must exit 0 by design, matching both
# originals exactly. "Fail closed" for this guard therefore means: print the deny JSON in every
# case either original would print it, and never silently swallow a case that should deny.

import json
import re
import subprocess
import sys

from _hook_log import log_invocation


def _emit_deny(reason: str, session_id=None, sub_decision="deny") -> None:
    log_invocation("multi-agent-commit-format-guard", "PreToolUse", decision=sub_decision,
                    session_id=session_id)
    output = {
        "systemMessage": f"[H-MAE02: blocked commit — {sub_decision.replace('_', ' ')}]",
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(output))


def main() -> int:
    try:
        raw_input = sys.stdin.read()
    except Exception:
        return 0

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    if not isinstance(data, dict):
        return 0

    tool_input = data.get("tool_input")
    command = ""
    if isinstance(tool_input, dict):
        command = tool_input.get("command") or ""
    if not command:
        return 0

    # Only intercept git commit commands
    if not re.search(r"\bgit\s+commit\b", command, re.IGNORECASE):
        return 0

    # Determine current branch — use cwd from hook input for reliability
    cwd = data.get("cwd") or ""
    git_cmd = ["git"]
    if cwd:
        git_cmd += ["-C", cwd]
    git_cmd += ["rev-parse", "--abbrev-ref", "HEAD"]

    current_branch = ""
    try:
        result = subprocess.run(
            git_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        current_branch = (result.stdout or "").strip()
    except Exception:
        current_branch = ""

    # Only enforce on agent branches
    # CONFIRMED DIVERGENCE between the two originals: the .ps1's `-notmatch` is
    # case-insensitive by PowerShell default; the .sh's `grep -qE` (no `-i`) is
    # case-sensitive for this check (its separate git-commit-detection grep on line 21
    # does use `-i`, but this branch-name grep deliberately does not). Real branch names
    # in this workspace are always lowercase, so this never bites in practice either way.
    #
    # Per this migration's precedence rule (see context-budget-alert.py's header comment):
    # when the two originals disagree, the port follows the .sh original, since bash is
    # what settings.json actually invokes on this reference environment. An earlier
    # revision of this port got this backwards — it picked re.IGNORECASE here reasoning
    # that broader branch-name matching is "the safer, more fail-closed choice" for a
    # governance gate. That reasoning doesn't override the precedence rule: this port's
    # job is byte-for-byte behavioral parity with .sh, not a from-scratch re-derivation of
    # which original's choice is safer. Reverted to case-sensitive to match .sh exactly.
    if not re.match(r"^agent/", current_branch) and not re.match(
        r"^stage\d+/agent/", current_branch
    ):
        return 0

    # Extract commit message from -m "..." or --message "..." (simple string form only)
    # Heredoc forms (@'...'@ or <<'EOF') are allowed through — too complex to parse reliably.
    # This is a known, deliberate gap inherited unchanged from both originals, not something
    # this port should "fix": a commit using a heredoc body is simply not inspected here.
    commit_msg = None
    m = re.search(r'(?:-m|--message)\s+"((?:[^"\\]|\\.)*)"', command, re.DOTALL)
    if m:
        commit_msg = m.group(1)
    else:
        m = re.search(r"(?:-m|--message)\s+'((?:[^'\\]|\\.)*)'", command, re.DOTALL)
        if m:
            commit_msg = m.group(1)

    if not commit_msg:
        return 0

    lines = commit_msg.split("\n")
    subject = lines[0].strip()

    # Validate subject format: agent/<name>: <verb-phrase>
    # CONFIRMED DIVERGENCE between the two originals (case-sensitivity, same root cause as
    # the branch check above): the .sh's grep -qE (no -i) is case-sensitive; the .ps1's
    # -notmatch is case-insensitive by default. Per this migration's precedence rule, the
    # port follows .sh — case-sensitive — here too. (This happens to also be the stricter
    # of the two for this particular match, since it gates a pass/no-denial decision, but
    # that is a side effect of following .sh, not the reason for the choice.)
    if not re.match(r"^agent/[^:]+:\s+\S", subject):
        _emit_deny(
            "[COMMIT FORMAT GUARD — H-MAE02] Agent commit subject '"
            + subject
            + "' does not match required format 'agent/<name>: <verb-phrase>' (imperative, "
            "<=72 chars). This is a P2 defect per CLAUDE.md §6. Example: 'agent/backend: "
            "add authentication endpoint'. Reference: core-component-00/engineering/"
            "multi-agent-engineering/fundamentals/git-worktree-orchestration.md.",
            session_id=data.get("session_id"), sub_decision="deny_subject_format",
        )
        return 0

    # Validate body — at least one hyphen-bulleted line after a blank separator
    # (skip subject line + blank-line separator, i.e. lines[2:], matching PowerShell's
    # `Select-Object -Skip 2` and bash's `tail -n +3`)
    has_body = False
    for line in lines[2:]:
        if re.match(r"^-\s+\S", line.strip()):
            has_body = True
            break

    if not has_body:
        _emit_deny(
            "[COMMIT FORMAT GUARD — H-MAE02] Agent commit is missing a hyphen-bulleted body. "
            "Bodyless single-line commits are a P2 defect per CLAUDE.md §6. Add a blank line "
            "then at least one '- <discrete change>' bullet after the subject line.",
            session_id=data.get("session_id"), sub_decision="deny_missing_body",
        )
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
