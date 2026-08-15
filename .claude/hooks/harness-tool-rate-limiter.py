#!/usr/bin/env python3
"""H-HE01: PreToolUse (Bash|PowerShell) — Tool Rate Limiter v2 (per-turn + session ceiling)

(Python port — behavior-identical to harness-tool-rate-limiter.ps1 / .sh; standard
library only, no third-party dependencies.)

Maintains two independent counters per session:
  1. Per-turn counter  — resets at the start of every prompt (via H-HE01-RESET hook)
  2. Session counter   — cumulative for the entire chat session; never resets

Two independent AskUserQuestion trigger paths:
  Path A (per-turn limit, default 150):
    Block + ask: A) Extend this turn by 100  B) Set a custom limit  C) End this response
  Path B (session ceiling, default 1000):
    Block + ask: A) Extend session by 500  B) Set a custom ceiling  C) Remove ceiling
                 D) End conversation

Config files (Claude writes these to extend or cancel limits at runtime):
  cc00-tool-limit-turn-<id>.txt    — per-turn cap override (deleted on each new prompt)
  cc00-tool-limit-session-<id>.txt — session ceiling override (persists for whole session)

Exit-code contract (matches both originals exactly): this script ALWAYS exits 0.
The "deny" signal is carried entirely in the hookSpecificOutput JSON printed to
stdout (permissionDecision: "deny") — never in the process exit code. Under the
limits, nothing is printed and the tool call is allowed through implicitly.

Reference: core-component-00/engineering/harness-engineering/implementations/tool_registry.py

Fail-closed note (governance-critical hook -- see verification notes below): the .sh
original's `case "$raw" in ''|*[!0-9]*) ... esac` and its unprotected `>` write
redirects are tolerant of I/O and validation failures *by construction* -- a shell
script without `set -e` simply keeps running after a failed redirect, and a glob
`case` pattern only ever matches/doesn't-match, it can never raise. The .ps1
original is tolerant for the same reason from the other direction: PowerShell
cmdlet errors (e.g. a failed Set-Content) are non-terminating by default and the
script continues. Python has no equivalent "carry on after a failed statement"
default -- an uncaught exception anywhere here would abort the process before the
limit check runs and print nothing, which a Claude Code hook host reads as exit
code 1 ("non-blocking error"), i.e. the tool call is allowed through unlimited.
That would be a silent fail-open regression versus both originals for this
specific hook, so every fallible operation below (file reads, file writes, digit
validation) is deliberately hardened to degrade the same way the shell/PowerShell
originals do -- continue with the in-memory value -- rather than propagate.
"""

import json
import os
import re
import sys
import tempfile

from _hook_log import log_invocation

DEFAULT_TURN_LIMIT = 150
DEFAULT_SESSION_LIMIT = 1000

# ASCII-only digit check, matching bash's `case "$raw" in ''|*[!0-9]*)`, which is
# a byte-level glob against the literal characters 0-9 only. Python's str.isdigit()
# is deliberately NOT used here: it returns True for various non-ASCII "digit"
# characters (e.g. superscript "²") that int() then refuses to parse, which
# would raise an uncaught ValueError and crash the hook on a corrupted/adversarial
# state file -- exactly the fail-open regression this hook must not have.
_DIGITS_RE = re.compile(r"^[0-9]+$")


def _read_stripped(path):
    """Return whitespace-stripped file contents, or None if the file is unreadable.
    Mirrors `[ -f "$1" ] || return` + `tr -d '[:space:]'` in the .sh port: a
    missing or unreadable file is indistinguishable from an empty one, never an
    exception."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except OSError:
        return None
    return re.sub(r"\s+", "", raw)


def read_positive_int(path, default):
    """Mirror read_positive_int() in the .sh port: return the parsed positive int
    stored in `path`, or `default` if the file is missing, empty, non-numeric, or
    not strictly positive. Deliberately defensive (never raises) so a corrupted
    override file degrades to the safe default instead of crashing the hook."""
    raw = _read_stripped(path)
    if not raw or not _DIGITS_RE.match(raw):
        return default
    value = int(raw)
    return value if value > 0 else default


def read_count(path):
    """Mirror read_count() in the .sh port: return the non-negative int counter
    stored in `path`, or 0 if missing/empty/non-numeric. Never raises."""
    raw = _read_stripped(path)
    if not raw or not _DIGITS_RE.match(raw):
        return 0
    return int(raw)


def _write_best_effort(path, content):
    """Persist `content` to `path`, tolerating any I/O failure exactly like both
    originals do: the .sh port's bare `>` redirect fails silently (no `set -e`) and
    keeps going; the .ps1 port's Set-Content raises a non-terminating error and
    also keeps going. The caller always uses the in-memory count for the limit
    check regardless of whether this persist succeeded, so a read-only/full temp
    dir degrades to "counters don't survive this call" rather than "the rate
    limiter silently stops enforcing."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError:
        pass


def main():
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        sys.exit(0)

    session_id = data.get("session_id") if isinstance(data, dict) else None
    if not session_id:
        sys.exit(0)

    safe_id = re.sub(r"[^a-zA-Z0-9]", "-", str(session_id))
    base = tempfile.gettempdir()

    # --- File paths ---
    turn_counter_file = os.path.join(base, f"cc00-tool-counter-turn-{safe_id}.txt")
    turn_limit_file = os.path.join(base, f"cc00-tool-limit-turn-{safe_id}.txt")
    session_counter_file = os.path.join(base, f"cc00-tool-counter-session-{safe_id}.txt")
    session_limit_file = os.path.join(base, f"cc00-tool-limit-session-{safe_id}.txt")

    # --- Read limits ---
    max_turn_calls = read_positive_int(turn_limit_file, DEFAULT_TURN_LIMIT)
    max_session_calls = read_positive_int(session_limit_file, DEFAULT_SESSION_LIMIT)

    # --- Increment counters ---
    turn_count = read_count(turn_counter_file) + 1
    _write_best_effort(turn_counter_file, str(turn_count))

    session_count = read_count(session_counter_file) + 1
    _write_best_effort(session_counter_file, str(session_count))

    # --- Path A: Per-turn limit check ---
    if turn_count > max_turn_calls:
        new_turn_limit = max_turn_calls + 100

        additional_context = f"""[TOOL RATE LIMITER — H-HE01 PATH A] Per-turn tool-call limit reached: {turn_count} / {max_turn_calls} calls this prompt.

MANDATORY: Use the AskUserQuestion tool to ask the user:

Question: "Per-turn tool-call limit reached ({turn_count} / {max_turn_calls} this prompt). How would you like to proceed?"

Options:
  A) "Extend this turn by 100" — raise the per-turn cap to {new_turn_limit} for the remainder of this response only.
     Action: use the Write tool to write "{new_turn_limit}" to: {turn_limit_file}
     Then retry the blocked command.

  B) "Set a custom limit" — raise the per-turn cap to a number of the user's choosing.
     Action: ask the user "How many additional tool calls would you like to allow this turn?" then
     add their answer to {max_turn_calls} and use the Write tool to write the result to: {turn_limit_file}
     Then retry the blocked command.

  C) "End this response" — wrap up the current response and stop.
     Action: summarise progress and do not retry the blocked command.

NOTE: Any extension granted here is automatically removed at the start of the next prompt.
Reference: core-component-00/engineering/harness-engineering/implementations/tool_registry.py"""

        reason = (
            f"[TOOL RATE LIMITER — H-HE01] Per-turn limit reached: {turn_count} / "
            f"{max_turn_calls}. See additionalContext for AskUserQuestion instructions."
        )

        log_invocation("harness-tool-rate-limiter", "PreToolUse", decision="deny_turn_limit",
                        session_id=session_id, extra={"turn_count": turn_count, "max_turn_calls": max_turn_calls})

        output = {
            "systemMessage": f"[H-HE01: per-turn tool-call limit reached — {turn_count}/{max_turn_calls}]",
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
                "additionalContext": additional_context,
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    # --- Path B: Session ceiling check (only if Path A passed) ---
    if session_count > max_session_calls:
        new_session_limit = max_session_calls + 500

        additional_context = f"""[TOOL RATE LIMITER — H-HE01 PATH B] Session tool-call ceiling reached: {session_count} / {max_session_calls} total this session.

MANDATORY: Use the AskUserQuestion tool to ask the user:

Question: "Session tool-call ceiling reached ({session_count} / {max_session_calls} total). How would you like to proceed?"

Options:
  A) "Extend session by 500" — raise the session ceiling to {new_session_limit}.
     Action: use the Write tool to write "{new_session_limit}" to: {session_limit_file}
     Then retry the blocked command.

  B) "Set a custom session ceiling" — raise the session ceiling to a number of the user's choosing.
     Action: ask the user "How many additional session tool calls would you like to allow?" then
     add their answer to {max_session_calls} and use the Write tool to write the result to: {session_limit_file}
     Then retry the blocked command.

  C) "Remove session ceiling" — no ceiling for the rest of this session.
     Action: use the Write tool to write "999999" to: {session_limit_file}
     Then retry the blocked command.

  D) "End conversation" — wrap up and stop.
     Action: summarise progress and do not retry the blocked command.

Reference: core-component-00/engineering/harness-engineering/implementations/tool_registry.py"""

        reason = (
            f"[TOOL RATE LIMITER — H-HE01] Session ceiling reached: {session_count} / "
            f"{max_session_calls}. See additionalContext for AskUserQuestion instructions."
        )

        log_invocation("harness-tool-rate-limiter", "PreToolUse", decision="deny_session_ceiling",
                        session_id=session_id, extra={"session_count": session_count, "max_session_calls": max_session_calls})

        output = {
            "systemMessage": f"[H-HE01: session tool-call ceiling reached — {session_count}/{max_session_calls}]",
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
                "additionalContext": additional_context,
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    # Under both limits — allow through
    sys.exit(0)


if __name__ == "__main__":
    main()
