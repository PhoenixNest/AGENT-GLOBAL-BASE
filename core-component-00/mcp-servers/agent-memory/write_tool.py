"""
write_tool.py — testable core of `write_memory`, a write-capable tool for the
`agent-memory` MCP server, built against the three reversal-condition
primitives merged ahead of it:

    - write_gate.py (Worker A): WriteConfirmationGate, quarantine promote/reject
    - production_judge.py (Worker B, context-engineering): evaluate_contradiction()
    - write_provenance.py (Worker C): WriteProvenance/validate_provenance, WriteRateLimiter

Full design context:
    core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/11-write-path-threat-model-phase1.md

---------------------------------------------------------------------------
ACTIVATION STATUS — read this before assuming this tool is live
---------------------------------------------------------------------------
`write_memory` (the `@mcp.tool()`-shaped wrapper, defined in server.py) is
built here in full, always present and always directly testable by importing
this module — but it is NOT registered as a live MCP tool by default. Its
registration in server.py is gated behind an explicit opt-in environment
flag:

    AGENT_MEMORY_WRITE_TOOL_ENABLED   default: "false" (falsy)

A future, separately-authorized activation step requires exactly one change:
set `AGENT_MEMORY_WRITE_TOOL_ENABLED=true` (or "1"/"yes") in the environment
the agent-memory server process is launched with. Nothing else needs to
change — the implementation, tests, and wiring below are already complete.
Per this same env-flag mechanism already established by
`EMBEDDER_SERVICE_ENABLED` in server.py, the flag is read once at
module-import time (see `AGENT_MEMORY_WRITE_TOOL_ENABLED` below), so a change
takes effect on the next process start, not by mutating the module global at
runtime.

---------------------------------------------------------------------------
GENUINE GAP #1 — no production LLM judge exists yet (flagged, not hidden)
---------------------------------------------------------------------------
`evaluate_contradiction()` (production_judge.py) requires an `llm_judge`
callable. That module's own docstring states plainly: "No production LLM
judge implementation exists anywhere in this workspace." This build does not
invent one — doing so under this build's own scope would be exactly the kind
of unreviewed, unadversarially-evaluated judge §7 item 1 explicitly warns
against.

Consequence: `_write_memory_impl` accepts `judge_callable` as an injectable,
optional parameter (`None` in every real call server.py makes today, since no
judge exists to inject). When collision-search below finds a candidate
existing record of the same memory_type and `judge_callable is None`, this
module CANNOT get a real ADD/UPDATE/NOOP verdict — and it does not pretend to.
Per this entire programme's fail-loud-not-fail-open discipline (write_gate.py's
`RepoRootUnresolvedError`, production_judge.py's own confidence-threshold and
order-disagreement gates, REFLECT-003's "never let an unforgeable-looking
code-level check silently pass a write through"), an un-adjudicable candidate
collision is treated as `would_collide_with_existing=True` — i.e. routed to
the human-confirmation lane rather than silently written as an unreviewed
"routine" quarantine record. See `_resolve_collision()` below.

PRACTICAL IMPLICATION, stated plainly: with no judge wired in (today's only
real configuration), any write whose content semantically resembles ANY
existing active record of the same memory_type — even one that is not
actually contradictory — will route to `confirmation_required` rather than
`quarantined`, because this module has no way to tell "genuinely conflicts"
from "merely the closest existing match" without a judge. Only writes with NO
existing candidate at all reach the quarantine lane today. This is a real,
load-bearing limitation of the current build's actual runtime behavior once
activated, not a hypothetical footnote — closing it requires a real judge
being wired in as `judge_callable`, which is future work this module does not
attempt.

---------------------------------------------------------------------------
GENUINE GAP #2 (closed, not hidden) — WriteConfirmationGate's confirmation
ambiguity, and why ConfirmationRequestTracker exists
---------------------------------------------------------------------------
`WriteConfirmationGate.check_confirmation()` returns `allowed=True` in TWO
states that are indistinguishable from its own return value alone: (a) no
confirmation has EVER been requested for this session, and (b) a
confirmation WAS requested and has since been cleared (a real
`AskUserQuestion` answered, per write-memory-gate-clear.py) or gone stale.
Trusting `allowed=True` on its face would let the FIRST-EVER high-consequence
write for a session sail straight through to `status="active"` with no human
ever having been asked anything — silently defeating the very mechanism this
tool exists to enforce.

`ConfirmationRequestTracker` (below) closes this by having `write_memory`
remember, in-process, whether IT has already called `request_confirmation()`
for a given session_id. The real per-write flow this produces:

  1st call, lane=high_consequence: check_confirmation() -> allowed=True (no
     marker) AND tracker says "never requested this session" -> call
     request_confirmation(), mark the tracker, return
     status="confirmation_required". The write does NOT happen on this call.
  (Turn ends. Per write_gate.py's own documented harness-level contract, a
   PreToolUse/PostToolUse hook pair — NOT wired into .claude/settings.json by
   this build, see write_gate.py's own note — narrows the window for a normal
   interactive session to skip asking the human. The calling agent is
   expected to surface the pending confirmation to the human, e.g. via
   AskUserQuestion, before retrying.)
  2nd call, same session_id, lane=high_consequence again: check_confirmation()
     -> allowed=True (marker was cleared, or went stale) AND tracker says
     "yes, this session already went through a request" -> tracker is reset
     for next time, write proceeds with status="active" directly (bypasses
     quarantine — a confirmed high-consequence write is not "routine").

KNOWN LIMITATION (same class as WriteRateLimiter's own, stated openly, not
hidden): ConfirmationRequestTracker state is in-process only and resets to
empty on server restart. This is the SAFE failure direction: after a
restart, every session looks "never requested" again, so the very next
high-consequence attempt for that session re-requests confirmation rather
than silently skipping it. It fails toward MORE confirmation being required,
never less.

---------------------------------------------------------------------------
GENUINE GAP #3 (documented, not silently absorbed) — collision search has no
similarity score to threshold on
---------------------------------------------------------------------------
`QdrantMemoryIndex.search()` (memory_vector_store.py) discards each Qdrant
point's `.score` when converting to `MemoryRecord` instances — it was built
for search_memory's use case, which never needed a score. This module reuses
that same method (per the build brief's explicit instruction to reuse the
existing accessor/search pattern) rather than adding a parallel
score-preserving query path, which would be new, unreviewed Qdrant-querying
surface area. The practical effect: "a candidate was found" means "this is
the single closest existing record of the same memory_type," not "this is
plausibly related above some similarity threshold" — there is no way, with
today's `search()` return shape, to distinguish a genuinely close match from
a merely top-ranked-but-unrelated one. Combined with Gap #1 above (no judge
to adjudicate what's found), this is why the practical rate of
`confirmation_required` responses is high once any records exist in a
collection. Not a bug — a documented, load-bearing consequence of two
compounding, explicitly-flagged gaps.

---------------------------------------------------------------------------
Quarantine-lane provenance storage — design choice
---------------------------------------------------------------------------
`MemoryRecord` (memory_vector_store.py) is NOT modified by this module. A
write's `WriteProvenance` fields, plus this module's own collision/injection
diagnostics, are stashed as an ADDITIONAL top-level key
(`"write_provenance"`, a nested dict) on the payload dict AFTER calling
`record.to_payload()` — never by adding a field to the `MemoryRecord`
dataclass itself. The record is then upserted via
`QdrantMemoryIndex.upsert_payload(point_id, embed_text, payload)` (which
accepts a raw payload dict and does not require it to be exactly
`MemoryRecord.to_payload()`'s shape) rather than `upsert_record()` (which
would silently drop any key not in `to_payload()`'s fixed shape).
`MemoryRecord.from_payload()` parses via `payload.get(...)` for every field
it reads — an unrecognized extra `"write_provenance"` key is simply ignored
by any existing reader, verified by reading that method directly (no
`KeyError` risk, no schema change required). This is a deliberate, additive-
only choice: Worker E is re-verifying Decision 2's constraints against this
exact code, and a wrapper-level design (never touching the shared dataclass)
keeps that review surface minimal.
"""

from __future__ import annotations

import os
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Sibling imports (write_gate.py / write_provenance.py live in this same
# agent-memory/ directory). Works whether this module is imported via
# server.py (which already runs from / has this directory on sys.path as the
# entry script's own directory) or loaded directly/standalone by a test —
# tests that import write_tool.py directly are expected to insert this
# directory onto sys.path first, mirroring test_write_gate.py's own
# established pattern.
from write_gate import WriteConfirmationGate
from write_provenance import (
    WriteProvenance,
    WriteRateLimiter,
    validate_provenance,
    get_default_rate_limiter,
)

# production_judge.py / memory_vector_store.py live under
# engineering/context-engineering/implementations/. Defensive sys.path setup
# mirrors server.py's own identical snippet exactly, so this module is
# importable standalone (e.g. directly by a test) without depending on
# import order relative to server.py.
_CONTEXT_ENGINEERING_ROOT = Path(__file__).resolve().parents[2] / "engineering" / "context-engineering"
if str(_CONTEXT_ENGINEERING_ROOT) not in sys.path:
    sys.path.insert(0, str(_CONTEXT_ENGINEERING_ROOT))

from implementations.production_judge import (  # noqa: E402
    DEFAULT_CONFIDENCE_THRESHOLD,
    JudgeCallable,
    JudgeResult,
    _detect_injection,
    evaluate_contradiction,
)
from implementations.memory_vector_store import (  # noqa: E402
    MemoryRecord,
    QdrantMemoryIndex,
    compute_write_time_importance,
)


# ---------------------------------------------------------------------------
# Activation flag — see module docstring "ACTIVATION STATUS" above
# ---------------------------------------------------------------------------

AGENT_MEMORY_WRITE_TOOL_ENABLED = os.getenv(
    "AGENT_MEMORY_WRITE_TOOL_ENABLED", "false"
).strip().lower() in ("1", "true", "yes")


# ---------------------------------------------------------------------------
# ConfirmationRequestTracker — closes Gap #2 above
# ---------------------------------------------------------------------------


class ConfirmationRequestTracker:
    """Tracks, per session_id, whether write_memory has already called
    `gate.request_confirmation()` at least once for a high-consequence write
    in THIS session within this process's lifetime. See module docstring
    "GENUINE GAP #2" for the full rationale and the exact two-call flow this
    produces. Thread-safe; mirrors WriteRateLimiter's locking discipline."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._requested_sessions: set = set()

    def was_requested(self, session_id: str) -> bool:
        with self._lock:
            return session_id in self._requested_sessions

    def mark_requested(self, session_id: str) -> None:
        with self._lock:
            self._requested_sessions.add(session_id)

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._requested_sessions.discard(session_id)

    def reset(self) -> None:
        """Test isolation only — mirrors WriteRateLimiter.reset()'s identical
        caveat: not intended for concurrent production use."""
        with self._lock:
            self._requested_sessions.clear()


_default_confirmation_tracker_lock = threading.Lock()
_default_confirmation_tracker: Optional[ConfirmationRequestTracker] = None


def get_default_confirmation_tracker() -> ConfirmationRequestTracker:
    """Process-wide default ConfirmationRequestTracker, constructed on first
    use — same singleton-accessor shape as
    write_provenance.get_default_rate_limiter()."""
    global _default_confirmation_tracker
    with _default_confirmation_tracker_lock:
        if _default_confirmation_tracker is None:
            _default_confirmation_tracker = ConfirmationRequestTracker()
        return _default_confirmation_tracker


_default_write_gate_lock = threading.Lock()
_default_write_gate: Optional[WriteConfirmationGate] = None


def get_default_write_gate() -> WriteConfirmationGate:
    """Process-wide default WriteConfirmationGate, constructed on first use —
    same singleton-accessor shape as get_default_rate_limiter()/
    get_default_confirmation_tracker()."""
    global _default_write_gate
    with _default_write_gate_lock:
        if _default_write_gate is None:
            _default_write_gate = WriteConfirmationGate()
        return _default_write_gate


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# "reflection" is deliberately excluded — that collection stays on its own
# Investigator-Authored Write Path (memory_store.py's write_reflection()),
# never MCP-agent-callable, per that module's own module-level comment and
# write_gate.py's classify() docstring. This tool structurally cannot reach
# it: the memory_type validation below rejects anything not in this tuple
# before any other logic runs.
ALLOWED_WRITE_MEMORY_TYPES = ("episodic", "semantic", "procedural")


# ---------------------------------------------------------------------------
# Collision resolution — Gap #1 / Gap #3
# ---------------------------------------------------------------------------


def _resolve_collision(
    content: str,
    memory_type: str,
    session_id: str,
    client: Any,
    embedder: Callable[[str], List[float]],
    judge_callable: Optional[JudgeCallable],
) -> "CollisionOutcome":
    """
    Searches for the single closest existing active record of `memory_type`
    (session-scoped for episodic, matching search_memory's own scoping rule;
    cross-session otherwise) and, if one is found, attempts to adjudicate it
    via evaluate_contradiction() when a judge_callable is available.

    See module docstring "GENUINE GAP #1" / "GENUINE GAP #3" for the exact,
    honestly-stated limitations of what this can and cannot determine.
    """
    index = QdrantMemoryIndex(memory_type, client=client, embedder=embedder)
    episodic_scope = session_id if memory_type == "episodic" else None
    candidates = index.search(
        query_text=content,
        top_k=1,
        status_in=("active",),
        session_id=episodic_scope,
    )

    if not candidates:
        return CollisionOutcome(
            would_collide=False,
            note="no_existing_candidate_found",
            judge_result=None,
        )

    existing = candidates[0]

    if judge_callable is None:
        # No production judge exists yet (Gap #1) — conservative fail-safe:
        # a candidate exists and nothing can rule out a genuine conflict, so
        # this is NOT treated as safely routine.
        return CollisionOutcome(
            would_collide=True,
            note="existing_candidate_found_no_judge_configured_conservative_high_consequence",
            judge_result=None,
        )

    judge_result = evaluate_contradiction(
        new_content=content,
        existing_content=existing.content,
        llm_judge=judge_callable,
        confidence_threshold=DEFAULT_CONFIDENCE_THRESHOLD,
    )
    return CollisionOutcome(
        would_collide=judge_result.verdict == "UPDATE",
        note=f"judged_verdict={judge_result.verdict}",
        judge_result=judge_result,
    )


class CollisionOutcome:
    """Plain result holder for _resolve_collision() — not a dataclass to
    avoid an extra import; three fields, always fully populated."""

    __slots__ = ("would_collide", "note", "judge_result")

    def __init__(self, would_collide: bool, note: str, judge_result: Optional[JudgeResult]) -> None:
        self.would_collide = would_collide
        self.note = note
        self.judge_result = judge_result


# ---------------------------------------------------------------------------
# Testable core
# ---------------------------------------------------------------------------


def _write_memory_impl(
    content: str,
    memory_type: str,
    session_id: str,
    provenance_source: str,
    provenance_triggering_context_excerpt: str,
    provenance_from_external_content: bool,
    provenance_confidence: float,
    client: Any,
    embedder: Optional[Callable[[str], List[float]]],
    embedder_unavailable_reason: str,
    gate: WriteConfirmationGate,
    rate_limiter: WriteRateLimiter,
    confirmation_tracker: ConfirmationRequestTracker,
    judge_callable: Optional[JudgeCallable] = None,
) -> Dict[str, Any]:
    """
    Testable core of write_memory. See write_memory()'s docstring (server.py)
    for the full flow narrative and this module's docstring for the honestly-
    stated gaps in judge availability and collision-search precision.

    Never raises — every rejection path returns a dict; the @mcp.tool()-
    shaped wrapper in server.py additionally wraps this in try/except so no
    unexpected internal error escapes either.

    Return shape (always all five keys present):
        written        bool
        status         "active" | "quarantined" | "rejected" |
                        "confirmation_required" | "error"
        reason         str | None — populated whenever written is False, or
                        for extra context on an accepted write
        record_id      str | None — the Qdrant point id, once known
        lane            "high_consequence" | "routine" |
                        "quarantine_forced_injection" | None (unset before
                        classification runs)
    """
    if memory_type not in ALLOWED_WRITE_MEMORY_TYPES:
        return {
            "written": False,
            "status": "rejected",
            "reason": f"unsupported memory_type: {memory_type!r} (expected one of {ALLOWED_WRITE_MEMORY_TYPES})",
            "record_id": None,
            "lane": None,
        }

    if not isinstance(session_id, str) or not session_id.strip():
        return {
            "written": False,
            "status": "rejected",
            "reason": "session_id is required and must be a non-empty string",
            "record_id": None,
            "lane": None,
        }

    if not isinstance(content, str) or not content.strip():
        return {
            "written": False,
            "status": "rejected",
            "reason": "content is required and must be a non-empty string",
            "record_id": None,
            "lane": None,
        }

    provenance = WriteProvenance(
        source=provenance_source,
        triggering_context_excerpt=provenance_triggering_context_excerpt,
        from_external_content=provenance_from_external_content,
        confidence=provenance_confidence,
    )
    ok, reason = validate_provenance(provenance)
    if not ok:
        return {
            "written": False,
            "status": "rejected",
            "reason": f"invalid provenance: {reason}",
            "record_id": None,
            "lane": None,
        }

    allowed, reason = rate_limiter.check_and_record(session_id, memory_type)
    if not allowed:
        return {
            "written": False,
            "status": "rejected",
            "reason": reason,
            "record_id": None,
            "lane": None,
        }

    if client is None:
        return {
            "written": False,
            "status": "rejected",
            "reason": "qdrant-memory client unavailable — cannot search for collisions or write",
            "record_id": None,
            "lane": None,
        }

    if embedder is None:
        return {
            "written": False,
            "status": "rejected",
            "reason": f"cannot embed content for collision search or write: {embedder_unavailable_reason}",
            "record_id": None,
            "lane": None,
        }

    injection_flagged = _detect_injection(content)

    judge_result: Optional[JudgeResult] = None
    would_collide = False
    collision_note = "skipped_content_flagged_as_possible_injection"

    if not injection_flagged:
        outcome = _resolve_collision(
            content=content,
            memory_type=memory_type,
            session_id=session_id,
            client=client,
            embedder=embedder,
            judge_callable=judge_callable,
        )
        would_collide = outcome.would_collide
        collision_note = outcome.note
        judge_result = outcome.judge_result

    # -----------------------------------------------------------------
    # Classification + gate
    # -----------------------------------------------------------------
    if injection_flagged:
        # Per build brief: injected content is never routed through
        # classify()/the high-consequence confirmation path at all — it
        # always lands in quarantine, reviewable but never auto-active,
        # regardless of what a (never-invoked, in this branch) judge might
        # have said.
        lane = "quarantine_forced_injection"
        status = "quarantined"
    else:
        lane = gate.classify(memory_type=memory_type, sacred=False, would_collide_with_existing=would_collide)
        if lane == "high_consequence":
            allowed, reason = gate.check_confirmation(session_id)
            if not allowed:
                return {
                    "written": False,
                    "status": "confirmation_required",
                    "reason": reason,
                    "record_id": None,
                    "lane": lane,
                }
            # allowed == True: no pending marker right now. See module
            # docstring "GENUINE GAP #2" for why this alone is ambiguous and
            # why confirmation_tracker resolves it.
            if not confirmation_tracker.was_requested(session_id):
                summary = (
                    f"write_memory high-consequence write pending confirmation: "
                    f"memory_type={memory_type!r}, session_id={session_id!r}, "
                    f"collision_note={collision_note!r}, "
                    f"content_excerpt={content[:200]!r}"
                )
                gate.request_confirmation(session_id, summary=summary)
                confirmation_tracker.mark_requested(session_id)
                return {
                    "written": False,
                    "status": "confirmation_required",
                    "reason": (
                        "high-consequence write requires human confirmation before it can "
                        "proceed — call write_memory again with the same session_id and "
                        "content once confirmation has completed"
                    ),
                    "record_id": None,
                    "lane": lane,
                }
            # Already requested earlier in this process, and no marker is
            # present now — treat as confirmed (or the 15-minute stale-marker
            # fail-safe fired, which WriteConfirmationGate itself treats as
            # "restore pre-gate behavior"). Reset the tracker so a FUTURE
            # high-consequence write for this session starts fresh.
            confirmation_tracker.clear(session_id)
            status = "active"
        else:
            status = "quarantined"

    # -----------------------------------------------------------------
    # Build record + write
    # -----------------------------------------------------------------
    now = time.time()
    record_id = str(uuid.uuid4())
    record = MemoryRecord(
        id=record_id,
        memory_type=memory_type,
        content=content,
        created_at=now,
        last_accessed_at=now,
        access_count=0,
        # Internal write-time heuristic only — never caller-supplied. This
        # tool's signature carries no event_type/importance concept (unlike
        # PersistentMemorySink.write_episodic's event_type), so the shared
        # "general" heuristic (compute_write_time_importance's 0.2 default)
        # is applied uniformly regardless of memory_type.
        importance=compute_write_time_importance("general"),
        confidence=1.0,
        decay_weight=1.0,
        status=status,  # "active" | "quarantined" — never caller-settable
        source_session_id=session_id,
        source_turn=0,
        sacred=False,  # never caller-settable — Decision 2
        tags=["write_memory"],
        consolidated_from=[],
        modality="text",
        media_ref=None,
    )

    payload = record.to_payload()
    payload["write_provenance"] = {
        "source": provenance.source,
        "triggering_context_excerpt": provenance.triggering_context_excerpt,
        "from_external_content": provenance.from_external_content,
        "confidence": provenance.confidence,
        "injection_flagged": injection_flagged,
        "collision_note": collision_note,
        "judge_verdict": judge_result.verdict if judge_result is not None else None,
        "judge_confidence": judge_result.confidence if judge_result is not None else None,
        "written_via": "write_memory",
        "written_at": now,
    }

    index = QdrantMemoryIndex(memory_type, client=client, embedder=embedder)
    upserted = index.upsert_payload(record_id, content, payload)

    if not upserted:
        return {
            "written": False,
            "status": "rejected",
            "reason": (
                "qdrant-memory upsert failed or degraded (client/embedder unavailable, "
                "timeout, or unreachable) — see server stderr diagnostics"
            ),
            "record_id": record_id,
            "lane": lane,
        }

    return {
        "written": True,
        "status": status,
        "reason": None,
        "record_id": record_id,
        "lane": lane,
        "collision_note": collision_note,
        "injection_flagged": injection_flagged,
    }
