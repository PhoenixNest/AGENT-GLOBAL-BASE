"""
write_provenance.py — Provenance enforcement and write-rate-limiting/anomaly-flagging
building blocks for a *hypothetical, not-yet-authorized* write-capable `agent-memory`
MCP tool.

Status (read this before wiring this module into anything): Phase 2 (a write-capable
memory tool) is **not authorized**. This module implements two of the concrete,
checkable reversal conditions listed in
`core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/11-write-path-threat-model-phase1.md`
§4 items 3 and 4 (rate limiting/anomaly flagging, and non-optional provenance
enforced in code) ahead of any Phase 2 go decision, so that a future write tool has
these primitives ready rather than needing to invent them under time pressure. Nothing
in this module registers an MCP tool, performs a write to `qdrant-memory`, or grants
Phase 2 authorization on its own.

Two independent pieces, per that document's §5:

1. ``WriteProvenance`` / ``validate_provenance`` — non-optional provenance tagging,
   enforced in code (a write attempt with missing/malformed provenance must be
   refused outright by the caller, not silently defaulted).
2. ``WriteRateLimiter`` — a real, in-process counter that closes the exact gap
   `07-adversarial-evaluation-results.md` §4's
   `test_repeated_poisoning_attempts_are_not_rate_limited_or_flagged` found: 50
   identical/near-identical repeated write attempts in one session must not all
   silently succeed.

Both pieces are pure Python with no I/O and no dependency on `server.py` or
`memory_vector_store.py`, so they can be unit-tested in isolation and imported by
whichever module ends up implementing an actual write tool (or, per the health_check
telemetry convention documented in `.claude/rules/mcp-governance.md`'s `agent-memory`
row, merged into `health_check()`'s return dict as a new ``write_rate_limiting``
block).
"""

from __future__ import annotations

import math
import threading
import time
from collections import OrderedDict, deque
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, Optional, Tuple

# ---------------------------------------------------------------------------
# 1. Provenance enforcement
# ---------------------------------------------------------------------------

# Character cap for `WriteProvenance.triggering_context_excerpt`. Chosen to be
# generous enough for a reviewer to reconstruct *why* a write happened (several
# paragraphs of surrounding transcript/tool-result context) while still being
# cheap to store per-record and impossible to use as a way to smuggle an
# unbounded blob into a provenance field. 2000 chars is roughly 300-400 words of
# English prose — enough for the triggering user turn or poisoned document
# excerpt plus a sentence or two of surrounding context, not enough to hold an
# entire multi-page fetched document. Truncation (not rejection) is applied
# automatically in `WriteProvenance.__post_init__` — an over-long excerpt is a
# caller convenience issue, not a validation failure, so it is silently capped
# with a trailing marker rather than blocking the write.
MAX_EXCERPT_CHARS = 2000
_TRUNCATION_MARKER = " …[truncated]"


@dataclass
class WriteProvenance:
    """
    Non-optional provenance metadata a write-producing caller must attach to
    every write attempt, per threat-model §5 "Provenance tagging".

    Fields:
        source:
            Session id / tool-call context identifier that produced this
            write. Required, non-empty. This is the "which session/call
            caused this" half of the audit trail.
        triggering_context_excerpt:
            Bounded excerpt (see MAX_EXCERPT_CHARS above) of the actual
            context that produced this write — enough for a reviewer to
            reconstruct why the write happened without needing the original
            session. Required, non-empty. Automatically truncated to
            MAX_EXCERPT_CHARS in __post_init__; never rejected purely for
            being long.
        from_external_content:
            True if the triggering context included content read from an
            external source (a document, a web fetch, or another tool's
            result) as opposed to being derived purely from direct user
            instruction in the transcript. Per threat-model §5, this is the
            single field that makes attack shape 1 (§2.2 item 1 — a poisoned
            document ordering a write via embedded instruction) detectable
            after the fact even when it cannot be prevented outright: a
            reviewer scanning writes with from_external_content=True is
            scanning exactly the population where that attack shape lives.
        confidence:
            A float in [0.0, 1.0], derived by the *write-producing logic*
            (e.g. however a future write tool decides how sure it is that
            this write is a genuine, well-grounded fact), never supplied by
            the calling agent as a raw override.

            THIS IS A DIFFERENT FIELD FROM `MemoryRecord.confidence` AND
            `MemoryRecord.importance` in
            `context-engineering/implementations/memory_vector_store.py`.
            Decision 2 (`09-mcp-architecture-decision.md`) already bars
            caller-supplied `sacred`/`importance` overrides on the read
            path; this field must never be plumbed through to set
            `MemoryRecord.confidence` or `MemoryRecord.importance` directly,
            because doing so would reopen that exact hole under a new name.
            `WriteProvenance.confidence` exists solely to route between a
            future gate's high-consequence and routine lanes (per
            threat-model §3.2 — the write-then-quarantine-then-async-review
            design), not to set persisted record fields.
    """

    source: str
    triggering_context_excerpt: str
    from_external_content: bool
    confidence: float

    def __post_init__(self) -> None:
        if (
            isinstance(self.triggering_context_excerpt, str)
            and len(self.triggering_context_excerpt) > MAX_EXCERPT_CHARS
        ):
            keep = MAX_EXCERPT_CHARS - len(_TRUNCATION_MARKER)
            keep = max(keep, 0)
            self.triggering_context_excerpt = (
                self.triggering_context_excerpt[:keep] + _TRUNCATION_MARKER
            )


def validate_provenance(provenance: Optional["WriteProvenance"]) -> Tuple[bool, str]:
    """
    Non-optional, enforced-in-code validation of a WriteProvenance instance.

    Returns (True, "ok") only if `provenance` is a WriteProvenance with:
      - `source`: a non-empty string
      - `triggering_context_excerpt`: a non-empty string
      - `confidence`: a finite float (or int) in the closed range [0.0, 1.0]

    Returns (False, reason) otherwise, with `reason` identifying exactly which
    check failed. Per threat-model §4 item 4, a write attempt that fails this
    check must be refused outright by the caller (the future write tool),
    never silently defaulted or downgraded. This function only judges — it
    does not raise and it does not perform the refusal itself, so it is safe
    to call speculatively (e.g. in a health-check-style dry run) without side
    effects.
    """
    if provenance is None:
        return False, "provenance is required and was not supplied (None)"

    if not isinstance(provenance, WriteProvenance):
        return False, f"provenance must be a WriteProvenance instance, got {type(provenance).__name__}"

    if not isinstance(provenance.source, str) or not provenance.source.strip():
        return False, "provenance.source is missing or empty"

    if (
        not isinstance(provenance.triggering_context_excerpt, str)
        or not provenance.triggering_context_excerpt.strip()
    ):
        return False, "provenance.triggering_context_excerpt is missing or empty"

    if not isinstance(provenance.from_external_content, bool):
        return (
            False,
            f"provenance.from_external_content must be a bool, got {type(provenance.from_external_content).__name__}",
        )

    confidence = provenance.confidence
    # bool is a subclass of int in Python; explicitly reject it so True/False
    # can't sneak through as 1.0/0.0.
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        return False, f"provenance.confidence must be a float, got {type(confidence).__name__}"

    confidence = float(confidence)
    if not math.isfinite(confidence):
        return False, f"provenance.confidence must be finite, got {confidence!r}"

    if not (0.0 <= confidence <= 1.0):
        return False, f"provenance.confidence must be within [0.0, 1.0], got {confidence!r}"

    return True, "ok"


# ---------------------------------------------------------------------------
# 2. Rate limiting + anomaly flagging
# ---------------------------------------------------------------------------

# Default thresholds. Chosen to comfortably cover legitimate bursty write
# behavior in a single working session (a maintenance-style pass writing a
# handful of distinct new facts across a couple of memory types) while being
# far below the 50-call scale the adversarial evaluation used to demonstrate
# the unguarded-repetition gap in `check_contradiction()` — the point isn't to
# find the "true" legitimate ceiling (nobody has produced empirical usage data
# for a write tool that doesn't exist yet), it's to guarantee rejection kicks
# in an order of magnitude before that gap's scale, which these do by a wide
# margin at both the per-session and per-session-per-type layer.
DEFAULT_MAX_WRITES_PER_SESSION = 20
DEFAULT_MAX_WRITES_PER_SESSION_PER_TYPE = 8
# 1-hour rolling window: long enough to span a realistic single working
# session end-to-end (per workspace-conventions.md session-log.md/
# checkpoint.json practice, a "session" here is a bounded piece of work, not a
# multi-day span), short enough that a session's counters age out on their own
# without needing an explicit close/reset call from the caller.
DEFAULT_WINDOW_S = 3600.0
# Caps the number of distinct session_ids this limiter will track at once, so
# an attacker (or a bug) that mints a fresh session_id per write attempt to
# dodge the per-session counters cannot also turn the limiter's own memory
# footprint into a second DoS vector. Evicted via LRU (oldest-touched session
# first) once this cap is hit — see _touch_session below.
DEFAULT_MAX_TRACKED_SESSIONS = 5000


def _prune(timestamps: Deque[float], now: float, window_s: float) -> None:
    """Drop timestamps older than the rolling window, in place, from the left
    (timestamps are always appended in increasing order, so the oldest entries
    are always at the front)."""
    while timestamps and (now - timestamps[0]) > window_s:
        timestamps.popleft()


class WriteRateLimiter:
    """
    Real in-process write-attempt counter, per threat-model §5 "Rate limiting"
    and the gap `07-adversarial-evaluation-results.md` §4's
    `test_repeated_poisoning_attempts_are_not_rate_limited_or_flagged` found
    unguarded (50 consecutive identical calls all succeeded, no counter, log,
    or flag).

    Tracks writes per session_id (total) and per (session_id, memory_type)
    pair, over a rolling time window, and rejects once either threshold is
    crossed — the exact case that adversarial-eval finding left unguarded.

    KNOWN LIMITATIONS (stated explicitly, not a hidden gap):
      - This is in-process state. It resets to empty on server restart —
        there is no persistence layer backing these counters.
      - It does not coordinate across multiple server processes. If more
        than one `agent-memory` server process were ever run concurrently
        (e.g. two MCP host connections each spawning their own process),
        each process has its own independent counters and the *effective*
        per-session limit across all processes combined could be as high as
        (threshold × number of concurrent processes). This module does not
        attempt to solve that — it is the same single-process assumption
        `.claude/rules/mcp-governance.md`'s `agent-memory` row already
        documents for the embedder-warmup state.
      - Rate limiting alone is not a security boundary in the `REFLECT-003`
        sense (see threat-model §3.1-3.2) — it bounds *how many* attempts a
        given session gets, not whether any single attempt is legitimate.
        It is defense-in-depth, one of several checkable reversal
        conditions threat-model §4 lists, not a substitute for the others.
    """

    def __init__(
        self,
        max_writes_per_session: int = DEFAULT_MAX_WRITES_PER_SESSION,
        max_writes_per_session_per_type: int = DEFAULT_MAX_WRITES_PER_SESSION_PER_TYPE,
        window_s: float = DEFAULT_WINDOW_S,
        max_tracked_sessions: int = DEFAULT_MAX_TRACKED_SESSIONS,
    ) -> None:
        if max_writes_per_session <= 0:
            raise ValueError("max_writes_per_session must be positive")
        if max_writes_per_session_per_type <= 0:
            raise ValueError("max_writes_per_session_per_type must be positive")
        if window_s <= 0:
            raise ValueError("window_s must be positive")
        if max_tracked_sessions <= 0:
            raise ValueError("max_tracked_sessions must be positive")

        self._max_writes_per_session = max_writes_per_session
        self._max_writes_per_session_per_type = max_writes_per_session_per_type
        self._window_s = window_s
        self._max_tracked_sessions = max_tracked_sessions

        self._lock = threading.Lock()
        # LRU-ordered: session_id -> {"total": deque[float], "by_type": {memory_type: deque[float]}}
        # OrderedDict gives us cheap move-to-end (touch) and popitem(last=False) (evict oldest).
        self._sessions: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()

        # Process-lifetime counters, never pruned/evicted (small, fixed-size ints).
        self._total_writes_recorded = 0
        self._total_writes_rejected = 0
        self._rejections_by_reason_kind: Dict[str, int] = {
            "per_session_total": 0,
            "per_session_per_type": 0,
        }

    def _touch_session(self, session_id: str) -> Dict[str, Any]:
        """Return (creating if needed) the tracking entry for session_id, and
        mark it most-recently-used for LRU eviction. Must be called with
        self._lock held."""
        entry = self._sessions.get(session_id)
        if entry is None:
            if len(self._sessions) >= self._max_tracked_sessions:
                # Evict the least-recently-touched session to bound memory.
                self._sessions.popitem(last=False)
            entry = {"total": deque(), "by_type": {}}
            self._sessions[session_id] = entry
        self._sessions.move_to_end(session_id)
        return entry

    def check_and_record(self, session_id: str, memory_type: str) -> Tuple[bool, str]:
        """
        Checks whether a write attempt for (session_id, memory_type) is
        within both the per-session-total and per-session-per-type rolling-
        window thresholds. If allowed, records the attempt (increments the
        real counters) and returns (True, "ok"). If either threshold is
        already at capacity, the attempt is rejected — NOT recorded against
        the counters it would have exceeded — and (False, reason) is
        returned, with `reason` naming which threshold was crossed.

        This is the function that closes the adversarial-eval gap: calling
        this 50 times in a row with the same session_id and memory_type
        will allow only the first `max_writes_per_session_per_type` calls
        (default 8) and reject the remaining 42+, each with a reason
        identifying the per-session-per-type threshold.
        """
        now = time.monotonic()
        with self._lock:
            entry = self._touch_session(session_id)
            total_ts: Deque[float] = entry["total"]
            by_type: Dict[str, Deque[float]] = entry["by_type"]
            type_ts: Deque[float] = by_type.setdefault(memory_type, deque())

            _prune(total_ts, now, self._window_s)
            _prune(type_ts, now, self._window_s)

            if len(total_ts) >= self._max_writes_per_session:
                self._total_writes_rejected += 1
                self._rejections_by_reason_kind["per_session_total"] += 1
                return (
                    False,
                    (
                        f"rejected: per-session total write limit exceeded "
                        f"({len(total_ts)}/{self._max_writes_per_session} writes "
                        f"within {self._window_s:.0f}s for session_id={session_id!r})"
                    ),
                )

            if len(type_ts) >= self._max_writes_per_session_per_type:
                self._total_writes_rejected += 1
                self._rejections_by_reason_kind["per_session_per_type"] += 1
                return (
                    False,
                    (
                        f"rejected: per-session-per-type write limit exceeded "
                        f"({len(type_ts)}/{self._max_writes_per_session_per_type} "
                        f"writes of memory_type={memory_type!r} within "
                        f"{self._window_s:.0f}s for session_id={session_id!r})"
                    ),
                )

            total_ts.append(now)
            type_ts.append(now)
            self._total_writes_recorded += 1
            return True, "ok"

    def get_telemetry(self) -> Dict[str, Any]:
        """
        Returns a JSON-serializable snapshot shaped for direct merging into
        `health_check()`'s return dict as a new "write_rate_limiting" block,
        mirroring the existing `memory_instance` telemetry pattern (point
        counts, dormant_ratio) `.claude/rules/mcp-governance.md`'s
        `agent-memory` row documents.

        Never raises: any internal error is caught and reported as a clearly
        labeled degraded snapshot rather than propagating, consistent with
        every other telemetry function in this server (see
        `_get_search_capability_snapshot()` in server.py for the same
        discipline).

        Bounding strategy (so this function itself cannot become a memory-
        growth DoS vector): the underlying per-session state is already
        bounded by `max_tracked_sessions` (oldest-touched sessions are
        LRU-evicted in `_touch_session`) and by the rolling window (stale
        timestamps are pruned lazily on next access, not retained forever).
        This function additionally only *returns* a bounded summary — the
        20 most-recently-touched sessions, not the full tracked set — so the
        telemetry payload itself has a fixed upper size regardless of how
        many sessions are currently tracked.
        """
        try:
            with self._lock:
                tracked_sessions = len(self._sessions)
                recent_summary = []
                # OrderedDict is LRU-ordered oldest-first; take the last 20
                # (most recently touched) for the bounded summary.
                for session_id, entry in list(self._sessions.items())[-20:]:
                    by_type_counts = {
                        memory_type: len(ts) for memory_type, ts in entry["by_type"].items()
                    }
                    recent_summary.append(
                        {
                            "session_id": session_id,
                            "writes_in_window": len(entry["total"]),
                            "by_type": by_type_counts,
                        }
                    )

                return {
                    "total_writes_recorded": self._total_writes_recorded,
                    "total_writes_rejected": self._total_writes_rejected,
                    "rejections_by_reason_kind": dict(self._rejections_by_reason_kind),
                    "tracked_sessions": tracked_sessions,
                    "max_tracked_sessions": self._max_tracked_sessions,
                    "window_s": self._window_s,
                    "max_writes_per_session": self._max_writes_per_session,
                    "max_writes_per_session_per_type": self._max_writes_per_session_per_type,
                    "recent_sessions_summary": recent_summary,
                    "limitation": (
                        "in-process counters only; resets on server restart; "
                        "does not coordinate across multiple concurrent server processes"
                    ),
                }
        except Exception as exc:  # pragma: no cover - defensive, mirrors server.py discipline
            return {
                "total_writes_recorded": None,
                "total_writes_rejected": None,
                "error": f"write-rate-limiter telemetry snapshot failed: {exc}",
                "limitation": (
                    "in-process counters only; resets on server restart; "
                    "does not coordinate across multiple concurrent server processes"
                ),
            }

    def reset(self) -> None:
        """Clear all tracked session state and counters. Intended for test
        isolation, not for production use (a production caller should
        construct a fresh WriteRateLimiter rather than reset a shared one
        mid-flight, to avoid racing with in-flight check_and_record calls)."""
        with self._lock:
            self._sessions.clear()
            self._total_writes_recorded = 0
            self._total_writes_rejected = 0
            self._rejections_by_reason_kind = {
                "per_session_total": 0,
                "per_session_per_type": 0,
            }


# ---------------------------------------------------------------------------
# Module-level default instance
# ---------------------------------------------------------------------------
#
# A single shared WriteRateLimiter for the (hypothetical, not-yet-authorized)
# write tool to use, following this server's existing module-level-state
# convention (e.g. the embedder-state globals in server.py). Module-level
# state is appropriate here because this runs inside the single agent-memory
# server process — see the class docstring's "KNOWN LIMITATIONS" section for
# what that does and doesn't guarantee.
_default_rate_limiter_lock = threading.Lock()
_default_rate_limiter: Optional[WriteRateLimiter] = None


def get_default_rate_limiter() -> WriteRateLimiter:
    """Returns the process-wide default WriteRateLimiter, constructing it
    with default thresholds on first use. A future write tool can call this
    instead of constructing its own limiter, so all write attempts in the
    process share one set of counters."""
    global _default_rate_limiter
    with _default_rate_limiter_lock:
        if _default_rate_limiter is None:
            _default_rate_limiter = WriteRateLimiter()
        return _default_rate_limiter
