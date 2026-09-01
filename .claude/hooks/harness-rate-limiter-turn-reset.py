#!/usr/bin/env python3
"""
H-HE01-RESET: UserPromptSubmit -- resets per-turn tool counter and limit for H-HE01 (Python port)

Fires at the start of every new prompt, ensuring the per-turn tool-call counter
and any mid-turn extension granted by the user are wiped before the new turn begins.
The session-level counter and ceiling are NOT touched here.
Reference: core-component-00/framework/03-harness-engineering/implementations/tool_registry.py

Ported 1:1 from harness-rate-limiter-turn-reset.ps1 / harness-rate-limiter-turn-reset.sh.
Standard library only -- no third-party dependencies.

This hook is a best-effort reset, not a governance/enforcement gate: on its own it
never denies or blocks anything (the actual rate-limit enforcement lives in
harness-tool-rate-limiter.{ps1,sh}, a separate PreToolUse hook). Both originals are
written to *always* exit 0 -- they only ever short-circuit on unparsable/absent
input, and every individual file operation is allowed to fail silently -- so that a
transient temp-dir/filesystem problem here can never accidentally read as a block
signal to the harness. This port reproduces that same "always succeed" contract
exactly: every exception, expected or not, is swallowed and the process still exits
0, matching the originals' fail-open-by-design behavior rather than introducing a
new failure mode that could surface as a nonzero exit.
"""

import json
import re
import sys
import tempfile
from pathlib import Path

from _hook_log import log_invocation


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    session_id = data.get("session_id") if isinstance(data, dict) else None
    # Falsy check mirrors PowerShell's `-not $sessionId` and the bash port's
    # `d.get('session_id','') or ''`: None, "", 0, False all count as "no session id".
    if not session_id:
        return 0

    safe_id = re.sub(r"[^a-zA-Z0-9]", "-", str(session_id))
    base = Path(tempfile.gettempdir())

    # Reset per-turn counter to 0 (best-effort; mirrors Set-Content/printf, no trailing newline)
    try:
        (base / f"cc00-tool-counter-turn-{safe_id}.txt").write_text("0")
    except Exception:
        pass

    # Delete per-turn limit file so any mid-turn extension does not carry over (best-effort)
    try:
        (base / f"cc00-tool-limit-turn-{safe_id}.txt").unlink(missing_ok=True)
    except Exception:
        pass

    log_invocation("harness-rate-limiter-turn-reset", "UserPromptSubmit", decision="reset",
                    session_id=session_id)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Fail-open by design, matching both originals: never let an unexpected
        # error here surface as a nonzero exit that downstream tooling could
        # misinterpret as a block of the prompt.
        sys.exit(0)
