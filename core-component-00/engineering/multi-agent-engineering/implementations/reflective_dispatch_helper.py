#!/usr/bin/env python3
"""
Reflective Dispatch Helper — the Evaluator, wrapping SwarmOrchestrator's
already-shipped Evaluate/Reflect logic for real subagent dispatches.

Built per `core-component-00/telescope/2026-08-01-reflexion-bridge-to-real-dispatch/
supporting/implementation-plan.md` Phase 1-2 and `supporting/usage-cookbook.md` § 2
(the invocation contract this module implements verbatim). This is Surface A: an
advisory, opt-in helper the `multi-agent-orchestrator` subagent's own Execute-phase
instructions call between dispatches — not a `.claude/hooks/*.py` structural gate
(Surface B stays deferred, out of scope; see the cookbook's § 6).

Deferred import of swarm_orchestrator's public functions, mirroring
reflection_bridge.py's established shape: importing this module (e.g. for the CLI
entry point below) does not pay the cost of loading swarm_orchestrator until
evaluate_dispatch() is actually called. `swarm_orchestrator.py` has no heavy
third-party dependency (stdlib + local handoff_packet/shared_memory_log only), so
this is a convention match, not a performance requirement, in this case.

Never-raises, degrade-to-neutral contract: any internal failure (malformed input,
an import error, an unexpected exception from the wrapped evaluator) is caught and
turned into `{"passed": true, "rationale": "helper unavailable: ...", ...}` — a
helper fault can only skip the Evaluate/Reflect step for that attempt, never block
or fail a real dispatch. This mirrors reflection_bridge.py's own contract exactly.

CLI shape: JSON on stdin, a single JSON object on stdout, always exit 0. Per
`implementation-plan.md` Phase 3's review scope, the orchestrating subagent must
judge outcome from the `passed` field of well-formed stdout JSON — never from exit
code — so this entry point never signals failure via a non-zero exit; a malformed
or unreadable stdin payload degrades to the same neutral response as any other
internal fault, exactly like every other failure path in this module.

Structured stderr logging on every degrade path, mirroring error_boundary.py's own
`log_warning`/`log_error` convention (Kwame Asante's harness-engineering
convention, applied here per his Phase 3 conformance review of this module):
stdout stays a pure, single JSON object for the orchestrating subagent to parse,
while a one-line `[WARNING] ...` note goes to stderr so a degrade is
incident-traceable without polluting the machine-readable stdout contract.

Invocation-counter telemetry (`implementation-plan.md` Phase 4 § 2, per
`research-report.md` Recommendation 5): every real CLI invocation (`_main()`)
appends one JSONL record to this pilot's own telemetry file, scoped to this
Programme's `supporting/pilot/telemetry/` folder — not a permanent production
metrics path, since the pilot's own gate (Phase 4) is explicitly a bounded
exercise, not a decision to keep this telemetry indefinitely. This exists so
"the Execute phase actually invoked the helper N times" is a checked fact for
Dr. Vance's Phase 4 review, not an assumption — silent under-collection would
otherwise be indistinguishable from "the helper wasn't needed." Telemetry
writes never raise and never block the response (best-effort, same posture as
`_log_warning`) and can be disabled — e.g. for this module's own test suite,
so pytest/CLI-test runs don't pollute the pilot's real invocation count — by
setting `REFLECTIVE_DISPATCH_HELPER_TELEMETRY=0` in the environment.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_TELEMETRY_PATH = (
    Path(__file__).resolve().parents[3]
    / "telescope"
    / "2026-08-01-reflexion-bridge-to-real-dispatch"
    / "supporting"
    / "pilot"
    / "telemetry"
    / "invocations.jsonl"
)


def _record_invocation(response: Dict[str, Any]) -> None:
    """Best-effort, never-raises append of one telemetry record per real CLI
    invocation. Disabled via REFLECTIVE_DISPATCH_HELPER_TELEMETRY=0 (this
    module's own test suite sets this so repeated test runs don't inflate the
    pilot's real invocation count)."""
    if os.environ.get("REFLECTIVE_DISPATCH_HELPER_TELEMETRY", "1") == "0":
        return
    try:
        _TELEMETRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "passed": response.get("passed"),
            "retries_remaining": response.get("retries_remaining"),
            "degraded": isinstance(response.get("rationale"), str)
            and response["rationale"].startswith("helper unavailable:"),
        }
        with open(_TELEMETRY_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass


def _log_warning(message: str, **kwargs: Any) -> None:
    """Minimal structured stderr logger, matching error_boundary.py's own
    `_log`/`log_warning` shape exactly (same `[LEVEL] message k=v ...` format)
    so a degrade event here reads consistently with every other harness
    component's incident log. Never raises — logging must never become a new
    failure mode on an already-degraded path."""
    try:
        extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
        print(f"[WARNING] {message} {extra}".rstrip(), file=sys.stderr)
    except Exception:
        pass


def _load_swarm_orchestrator_symbols():
    """Deferred import — see module docstring. Inserts this module's own
    package root (multi-agent-engineering/) onto sys.path so
    `implementations.swarm_orchestrator` resolves as a package-qualified
    import, which swarm_orchestrator.py's own relative imports
    (`from .handoff_packet import HandoffPacket`) require. Matches the
    exact sys.path convention this module's own test suite already uses
    (`sys.path.insert(0, str(Path(__file__).parent.parent))` in
    test_reflection_bridge.py), so behavior is identical whether this
    helper is imported as a test dependency or run standalone via
    `uv run reflective_dispatch_helper.py`."""
    import sys as _sys
    from pathlib import Path

    module_root = Path(__file__).resolve().parent.parent
    if str(module_root) not in _sys.path:
        _sys.path.insert(0, str(module_root))

    from implementations.swarm_orchestrator import (  # noqa: E402
        SubTask,
        _reflection_note_for_attempt,
        evaluate_subtask_result,
    )

    return SubTask, evaluate_subtask_result, _reflection_note_for_attempt


def evaluate_dispatch(
    task_description: str,
    gate_criteria: List[str],
    checks: Dict[str, Any],
    attempt_number: int,
    max_reflection_retries: int = 2,
) -> Dict[str, Any]:
    """The Evaluator's single entry point — the request/response contract
    documented in usage-cookbook.md § 2.2-2.3, verbatim.

    `checks` must be real, checkable evidence the caller (the Supervisor —
    `multi-agent-orchestrator`) extracted from the Executor's actual output
    (a test exit code, a diff summary) — never the Executor's own narrative
    claim of success. This function does not and cannot enforce that; it is
    Dr. Wieczorek's Phase 3-required mitigation, restated here as a
    docstring convention, exactly as usage-cookbook.md § 2.2 documents it.

    `attempt_number` is 1-indexed and represents the dispatch attempt just
    evaluated. `retries_remaining` is computed the same way whether this
    attempt passed or failed (`max(0, max_reflection_retries -
    attempt_number)`) so a caller can read it uniformly; only a failing
    verdict actually needs it to decide whether to retry.
    """
    try:
        attempt_number = int(attempt_number)
        if attempt_number < 1:
            raise ValueError(f"attempt_number must be >= 1, got {attempt_number!r}")
        max_reflection_retries = int(max_reflection_retries)

        SubTask, evaluate_subtask_result, _reflection_note_for_attempt = (
            _load_swarm_orchestrator_symbols()
        )

        subtask = SubTask(
            description=str(task_description or ""),
            gate_criteria=list(gate_criteria or []),
        )
        result = {"checks": dict(checks or {})}
        verdict = evaluate_subtask_result(subtask, result)
        retries_remaining = max(0, max_reflection_retries - attempt_number)

        if verdict.passed:
            return {
                "passed": True,
                "rationale": verdict.rationale,
                "reflection_note": None,
                "retries_remaining": retries_remaining,
            }

        is_final_attempt = attempt_number >= max_reflection_retries
        reflection_note = _reflection_note_for_attempt(verdict.rationale, is_final_attempt)
        return {
            "passed": False,
            "rationale": verdict.rationale,
            "reflection_note": reflection_note,
            "retries_remaining": retries_remaining,
        }
    except Exception as exc:
        _log_warning(
            "reflective_dispatch_helper degraded to neutral pass",
            attempt_number=attempt_number,
            reason=exc,
        )
        return {
            "passed": True,
            "rationale": f"helper unavailable: {exc} — Evaluate skipped, subtask proceeds as if ungated.",
            "reflection_note": None,
            "retries_remaining": 0,
        }


def _read_request(stdin) -> Optional[Dict[str, Any]]:
    """Returns None (never raises) on any read/parse failure — the caller
    treats None identically to a helper-unavailable degrade."""
    try:
        raw = stdin.read()
        if not raw or not raw.strip():
            return None
        payload = json.loads(raw)
        return payload if isinstance(payload, dict) else None
    except Exception:
        return None


def _main() -> int:
    payload = _read_request(sys.stdin)
    if payload is None:
        _log_warning("reflective_dispatch_helper degraded to neutral pass", reason="malformed or empty stdin JSON")
        response: Dict[str, Any] = {
            "passed": True,
            "rationale": "helper unavailable: malformed or empty stdin JSON — Evaluate skipped, subtask proceeds as if ungated.",
            "reflection_note": None,
            "retries_remaining": 0,
        }
    else:
        response = evaluate_dispatch(
            task_description=payload.get("task_description", ""),
            gate_criteria=payload.get("gate_criteria") or [],
            checks=payload.get("checks") or {},
            attempt_number=payload.get("attempt_number", 1),
            max_reflection_retries=payload.get("max_reflection_retries", 2),
        )
    _record_invocation(response)
    json.dump(response, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
