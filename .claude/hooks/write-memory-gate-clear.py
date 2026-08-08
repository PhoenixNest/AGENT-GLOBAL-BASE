#!/usr/bin/env python3
"""Write-Memory-Confirmation-Gate enforcement — PostToolUse (matcher: AskUserQuestion): clears
the pending memory-write-confirmation marker once AskUserQuestion has been called, releasing the
write-memory-gate-enforcer.py PreToolUse gate for this session.

Same shape as prompt-gate-clear.py (H-P01's own PostToolUse clear hook) — deliberately reused,
not reinvented. This is a NEW, INDEPENDENT hook: it only ever removes ITS OWN marker file
("mem-write-pending-<session_id>.json"), never H-P01's "h-p01-pending-<session_id>.json", and
does not modify or depend on prompt-gate-enforcer.py/prompt-gate-clear.py in any way. Standard
library only, no third-party dependencies.

NOT WIRED IN by this build — see write-memory-gate-enforcer.py's module comment for the full
settings.json wiring snippet and why it is not applied automatically here.

Fail-closed contract: this script only ever *removes* the pending-confirmation marker that
write-memory-gate-enforcer.py checks for before denying non-AskUserQuestion tool calls. On any
ambiguity or error — unparseable stdin, a JSON body that isn't an object, a missing/empty
session_id, an unresolved repo root, or a filesystem error on removal — this script does nothing
and exits 0, leaving any existing marker in place. That means the PreToolUse gate keeps denying
tool calls for that session until either a genuine AskUserQuestion call clears it or the
enforcer's own 15-minute stale-marker safety valve kicks in. It never takes the other branch
(deleting a marker it isn't sure about), which would be the fail-open direction for this gate.
"""

import json
import os
import subprocess
import sys

MARKER_PREFIX = "mem-write-pending-"


def _read_session_id():
    try:
        raw_input = sys.stdin.read()
    except Exception:
        return ""

    try:
        data = json.loads(raw_input)
    except Exception:
        return ""

    if not isinstance(data, dict):
        return ""

    session_id = data.get("session_id", "")
    if not session_id:
        return ""

    return str(session_id)


def _repo_root():
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


def main():
    session_id = _read_session_id()
    if not session_id:
        sys.exit(0)

    repo_root = _repo_root()
    if not repo_root:
        sys.exit(0)

    marker_path = os.path.join(
        repo_root, ".claude", "hooks", ".state", f"{MARKER_PREFIX}{session_id}.json"
    )

    try:
        os.remove(marker_path)
    except Exception:
        # Silent by design — mirrors prompt-gate-clear.py: a missing file, a permission
        # error, etc. are all swallowed, never surfaced as a failure.
        pass

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        # Defensive catch-all: any unforeseen error still exits 0 without having deleted
        # anything (fail closed — the marker, if any, is left in place).
        sys.exit(0)
