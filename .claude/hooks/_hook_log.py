#!/usr/bin/env python3
"""Shared call-history logger for .claude/hooks/*.py.

Added to close the hook-visibility gap users reported: most hooks in this suite left no
visible or durable record of having fired at all (see the hook-opacity investigation —
only 1 of 17 registered hooks unconditionally showed a real-time status message, and none
wrote to any persistent log). This module gives every hook a single, best-effort way to
append one structured JSONL record per invocation to a persistent, append-only log, so a
user can inspect a hook's call history after the fact regardless of what (if anything) the
hook also emits to stdout for Claude Code's own hook protocol.

Best-effort, fail-open by design, matching the fail-open idiom used throughout this hook
suite (e.g. harness-rate-limiter-turn-reset.py's "always succeed" contract): a failure to
write the log must never change a hook's actual decision behavior, stdout contract, or exit
code. Every exception here is swallowed; callers never need to guard their own call to
log_invocation().
"""

import datetime
import json
import os
import subprocess

LOG_FILENAME = "hook-invocations.jsonl"
_STATE_DIR_PARTS = (".claude", "hooks", ".state")

# Best-effort cap so a runaway/looping caller can never grow this file unboundedly across
# a long-lived workspace. Checked cheaply (byte size, not line count) before each append.
_MAX_LOG_BYTES = 10 * 1024 * 1024  # 10 MB


def _repo_root():
    """Best-effort `git rev-parse --show-toplevel`. Returns None on any failure — matches
    the same pattern used by prompt-optimizer.py / prompt-gate-clear.py / etc."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    root = result.stdout.strip()
    return root or None


def log_invocation(hook_name, event, decision="invoked", reason=None, session_id=None, extra=None,
                    repo_root=None):
    """Append one best-effort JSONL call-history record. Never raises.

    hook_name  -- short identifier for the hook (e.g. "prompt-optimizer")
    event      -- the Claude Code hook event (e.g. "UserPromptSubmit", "PreToolUse")
    decision   -- what the hook did on this call (e.g. "invoked", "pass", "deny", "advisory")
    reason     -- optional short human-readable reason/summary
    session_id -- optional session id, when available to the caller
    extra      -- optional small dict of additional structured detail
    repo_root  -- optional pre-resolved repo root; pass this when the caller has already
                  run `git rev-parse --show-toplevel` itself, to avoid a second subprocess
                  call on hooks that fire on every tool invocation (e.g. PreToolUse "*")
    """
    try:
        if not repo_root:
            repo_root = _repo_root()
        if not repo_root:
            return
        state_dir = os.path.join(repo_root, *_STATE_DIR_PARTS)
        os.makedirs(state_dir, exist_ok=True)
        log_path = os.path.join(state_dir, LOG_FILENAME)

        try:
            if os.path.getsize(log_path) > _MAX_LOG_BYTES:
                return
        except OSError:
            pass

        record = {
            "ts": datetime.datetime.now().isoformat(),
            "hook": hook_name,
            "event": event,
            "decision": decision,
        }
        if session_id:
            record["session_id"] = session_id
        if reason:
            record["reason"] = reason
        if extra:
            record["extra"] = extra

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass
