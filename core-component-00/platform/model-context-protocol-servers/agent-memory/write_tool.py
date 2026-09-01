"""Testable core of `write_memory`, the write-capable tool for the agent-memory MCP server.

Not registered as a live MCP tool unless AGENT_MEMORY_WRITE_TOOL_ENABLED is
truthy (read once at import time). Two behavioral gaps worth knowing before
relying on this module:

- No production LLM judge exists yet, so `judge_callable` is None in every
  real call. When collision search finds a candidate existing record with no
  judge to adjudicate it, this treats it as would_collide_with_existing=True
  (routes to human confirmation) rather than guessing — see
  `_resolve_collision()`. Combined with `QdrantMemoryIndex.search()` not
  returning a similarity score to threshold on, any write resembling an
  existing record of the same type currently routes to
  confirmation_required rather than quarantined, until a real judge is wired
  in.
- `WriteConfirmationGate.check_confirmation()` alone can't distinguish
  "never requested" from "requested and since cleared" — `ConfirmationRequestTracker`
  below resolves that ambiguity so a session's first high-consequence write
  always requires an explicit confirmation round-trip, never sails through
  on an absent marker.
"""

from __future__ import annotations

import os
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from write_gate import WriteConfirmationGate
from write_provenance import (
    WriteProvenance,
    WriteRateLimiter,
    validate_provenance,
    get_default_rate_limiter,
)

_CONTEXT_ENGINEERING_ROOT = Path(__file__).resolve().parents[3] / "framework" / "02-context-engineering"
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


AGENT_MEMORY_WRITE_TOOL_ENABLED = os.getenv(
    "AGENT_MEMORY_WRITE_TOOL_ENABLED", "false"
).strip().lower() in ("1", "true", "yes")


class ConfirmationRequestTracker:
    """Tracks, per session_id, whether write_memory has already called
    `gate.request_confirmation()` for a high-consequence write in this
    session within this process's lifetime. Thread-safe."""

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


# "reflection" is deliberately excluded — that collection stays on the
# Investigator-Authored Write Path (memory_store.py's write_reflection()),
# never MCP-agent-callable.
ALLOWED_WRITE_MEMORY_TYPES = ("episodic", "semantic", "procedural")


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
    (session-scoped for episodic, cross-session otherwise) and, if one is
    found, attempts to adjudicate it via evaluate_contradiction() when a
    judge_callable is available.
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
        # No judge available to rule out a genuine conflict — conservative
        # fail-safe, not treated as safely routine.
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
    """Testable core of write_memory. Never raises — every rejection path
    returns a dict.

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

    if injection_flagged:
        # Injected content always lands in quarantine, never auto-active.
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
            # Already requested earlier and no marker is pending — treat as
            # confirmed; reset so a future write for this session starts fresh.
            confirmation_tracker.clear(session_id)
            status = "active"
        else:
            status = "quarantined"

    now = time.time()
    record_id = str(uuid.uuid4())
    record = MemoryRecord(
        id=record_id,
        memory_type=memory_type,
        content=content,
        created_at=now,
        last_accessed_at=now,
        access_count=0,
        importance=compute_write_time_importance("general"),
        confidence=1.0,
        decay_weight=1.0,
        status=status,
        source_session_id=session_id,
        source_turn=0,
        sacred=False,  # never caller-settable
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
