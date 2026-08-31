#!/usr/bin/env python3
# H-MAE01: PreToolUse (Bash|PowerShell) — Multi-Agent Branch Naming Guard (Python port)
#
# Detects git commands that create new branches and validates the branch name
# against the workspace multi-agent naming convention:
#   agent/<role>/<task>  or  stage<N>/agent/<role>/<task>
# Reference: core-component-00/framework/05-multi-agent-engineering/fundamentals/git-worktree-orchestration.md
#
# Python port of multi-agent-branch-naming-guard.ps1 (pwsh) and
# multi-agent-branch-naming-guard.sh (bash). Implements identical stdin handling,
# branch-name extraction, and pattern validation as both originals, using only the
# standard library.
#
# Repo-root resolution: this script itself never shells out to `git rev-parse
# --show-toplevel` — neither original does either. That resolution happens once,
# outside this script, in settings.json's invocation wrapper (`r=$(git rev-parse
# --show-toplevel 2>/dev/null) && bash "$r/.claude/hooks/multi-agent-branch-naming-guard.sh"`),
# so there is no internal repo-root logic to port here.
#
# This hook always exits 0. The actual PreToolUse "deny" is communicated via the
# hookSpecificOutput JSON printed to stdout (permissionDecision: "deny"), not via a
# nonzero process exit code — so every code path below must exit 0 by design,
# matching both originals exactly. "Fail closed" for this guard therefore means:
# print the deny JSON in every case either original would print it, and never
# silently swallow a case that should deny.
#
# Judgment call — case sensitivity: the two originals disagree on regex case
# sensitivity in two places that pull in OPPOSITE directions, so this port
# synthesizes the more fail-closed choice at each step rather than adopting one
# original wholesale:
#
#   1. Branch-creating COMMAND detection (git worktree add / checkout -b /
#      switch -c). ps1's `-match` is case-insensitive by default (PowerShell
#      comparison operators are case-insensitive unless the `-c*` variant is
#      used); sh's `re.search` (no flags) is case-sensitive. Case-insensitive
#      recognizes strictly MORE commands as "branch-creating" — failing to
#      recognize one means branch_name stays empty and the hook exits 0 with
#      NO validation performed at all, a real fail-open gap relative to ps1.
#      This port matches ps1 here: case-insensitive extraction.
#
#   2. Branch-NAME validation against the five allowed patterns. ps1's
#      `-match` is again case-insensitive; sh's `grep -qE` (no `-i`) is
#      case-sensitive. Here case-insensitive is the MORE PERMISSIVE direction
#      (e.g. it would accept "Agent/Backend/Task" as valid, where sh would
#      deny it) — the opposite of fail-closed. This port matches sh here:
#      case-sensitive validation. (sh is also the version actually wired into
#      settings.json, which invokes every hook via `bash` unconditionally,
#      regardless of host platform.)
#
# Net effect: this port denies in every case that either original would deny,
# and is never more permissive than the stricter of the two on either
# sub-decision — i.e. it fails closed relative to both originals, not just one.
#
# Secondary, non-functional judgment call: the deny JSON's key/value spacing
# differs cosmetically between originals (ps1's `ConvertTo-Json -Compress` is
# gapless; sh's `json.dumps(...)` default has spaces after `:`/`,`). Both are
# valid JSON consumed identically by the harness, so this port just uses
# Python's `json.dumps` default (matching sh's rendering) without further
# normalization.

import json
import re
import sys

from _hook_log import log_invocation

# Branch-creating command patterns. Order matters: first match wins, mirroring
# both originals' if/elif chain (ps1's if/elseif, sh's sequential `if not m:`).
_BRANCH_EXTRACT_PATTERNS = [
    r"git\s+worktree\s+add\s+\S+\s+(?:-b\s+)?([a-zA-Z0-9/._-]+)",
    r"git\s+checkout\s+-b\s+([a-zA-Z0-9/._-]+)",
    r"git\s+switch\s+(?:--create|-c)\s+([a-zA-Z0-9/._-]+)",
]

# Valid branch patterns for this workspace (case-sensitive — see judgment-call
# note above). Order doesn't matter here: any match short-circuits to valid.
_VALID_BRANCH_PATTERNS = [
    r"^agent/[^/]+/[^/]+$",  # agent/<role>/<task>
    r"^stage\d+/agent/[^/]+/[^/]+$",  # stage<N>/agent/<role>/<task>
    r"^(master|main|develop)$",  # standard trunk branches
    r"^(company|studio)/.*$",  # workspace-scoped development branches
    r"^(feature|fix|chore|docs|refactor|test)/.*$",  # standard git-flow branches
]


def _emit_deny(branch_name: str, session_id=None) -> None:
    reason = (
        "[BRANCH NAMING GUARD — H-MAE01] Branch name '"
        + branch_name
        + "' does not follow workspace conventions. Multi-agent branches must be: "
        "agent/<role>/<task> or stage<N>/agent/<role>/<task> (e.g., "
        "agent/backend/dark-mode-api). Standard branches (feature/, fix/, company/, "
        "studio/) are also accepted. Reference: core-component-00/engineering/"
        "multi-agent-engineering/fundamentals/git-worktree-orchestration.md and CLAUDE.md §6."
    )
    log_invocation("multi-agent-branch-naming-guard", "PreToolUse", decision="deny",
                    reason=branch_name, session_id=session_id)
    output = {
        "systemMessage": f"[H-MAE01: blocked branch creation — '{branch_name}' does not follow naming convention]",
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

    # Guard against non-dict top-level JSON (e.g. a JSON array/number/string),
    # which the sh original's inline `d.get(...)` helper would crash on
    # (uncaught AttributeError inside the python3 subprocess — harmlessly,
    # since the crash happens before anything is printed, so the outer bash
    # still sees an empty $command and exits 0). The ps1 original never
    # crashes here because PowerShell property access on a non-object
    # silently yields $null. We reconcile on that shared net effect — exit 0,
    # no output — without reproducing the incidental sh-side crash/traceback.
    if not isinstance(data, dict):
        return 0

    tool_input = data.get("tool_input")
    command = ""
    if isinstance(tool_input, dict):
        command = tool_input.get("command") or ""
    if not command:
        return 0
    command = str(command)

    # Extract branch name from branch-creating commands (first match wins).
    # Case-insensitive: see judgment-call note #1 above.
    branch_name = ""
    for pattern in _BRANCH_EXTRACT_PATTERNS:
        m = re.search(pattern, command, re.IGNORECASE)
        if m:
            branch_name = m.group(1)
            break

    if not branch_name:
        return 0

    # Validate against the workspace's allowed branch patterns. Case-sensitive:
    # see judgment-call note #2 above.
    is_valid = any(re.match(pattern, branch_name) for pattern in _VALID_BRANCH_PATTERNS)

    if is_valid:
        return 0

    _emit_deny(branch_name, session_id=data.get("session_id"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
