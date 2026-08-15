"""Provenance enforcement and write-rate-limiting for a write-capable agent-memory MCP tool."""

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

# Bounded excerpt length: generous enough to reconstruct why a write happened,
# small enough to block using this field to smuggle an unbounded blob.
MAX_EXCERPT_CHARS = 2000
_TRUNCATION_MARKER = " …[truncated]"


@dataclass
class WriteProvenance:
    """Non-optional provenance metadata a write-producing caller must attach
    to every write attempt.

    Fields:
        source: session id / tool-call context identifier that produced
            this write. Required, non-empty.
        triggering_context_excerpt: bounded excerpt of the context that
            produced this write, for reviewer reconstruction. Required,
            non-empty; auto-truncated to MAX_EXCERPT_CHARS.
        from_external_content: True if the triggering context included
            content read from an external source (document, web fetch,
            another tool's result) rather than direct user instruction.
        confidence: float in [0.0, 1.0], derived by the write-producing
            logic — never a caller-supplied override. Distinct from
            MemoryRecord.confidence/importance (memory_vector_store.py);
            must never be plumbed through to set those fields directly.
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
    """Returns (True, "ok") if `provenance` is a well-formed WriteProvenance,
    else (False, reason). Does not raise and performs no refusal itself —
    safe to call speculatively."""
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

DEFAULT_MAX_WRITES_PER_SESSION = 20
DEFAULT_MAX_WRITES_PER_SESSION_PER_TYPE = 8
DEFAULT_WINDOW_S = 3600.0
DEFAULT_MAX_TRACKED_SESSIONS = 5000


def _prune(timestamps: Deque[float], now: float, window_s: float) -> None:
    """Drop timestamps older than the rolling window, in place, from the left."""
    while timestamps and (now - timestamps[0]) > window_s:
        timestamps.popleft()


class WriteRateLimiter:
    """In-process write-attempt counter: tracks writes per session_id (total)
    and per (session_id, memory_type), over a rolling time window, rejecting
    once either threshold is crossed.

    In-process state only — resets on server restart and does not coordinate
    across multiple concurrent server processes.
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
        self._sessions: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()

        self._total_writes_recorded = 0
        self._total_writes_rejected = 0
        self._rejections_by_reason_kind: Dict[str, int] = {
            "per_session_total": 0,
            "per_session_per_type": 0,
        }

    def _touch_session(self, session_id: str) -> Dict[str, Any]:
        """Return (creating if needed) the tracking entry for session_id and
        mark it most-recently-used for LRU eviction. Caller holds self._lock."""
        entry = self._sessions.get(session_id)
        if entry is None:
            if len(self._sessions) >= self._max_tracked_sessions:
                self._sessions.popitem(last=False)
            entry = {"total": deque(), "by_type": {}}
            self._sessions[session_id] = entry
        self._sessions.move_to_end(session_id)
        return entry

    def check_and_record(self, session_id: str, memory_type: str) -> Tuple[bool, str]:
        """Checks whether a write for (session_id, memory_type) is within
        both rolling-window thresholds. If allowed, records it and returns
        (True, "ok"); otherwise returns (False, reason) without recording."""
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
        """Returns a JSON-serializable snapshot for merging into
        health_check()'s return dict as "write_rate_limiting". Never raises —
        an internal error returns a labeled degraded snapshot instead."""
        try:
            with self._lock:
                tracked_sessions = len(self._sessions)
                recent_summary = []
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
        except Exception as exc:  # pragma: no cover - defensive
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
        """Clears all tracked session state and counters. For test isolation —
        a production caller should construct a fresh instance instead."""
        with self._lock:
            self._sessions.clear()
            self._total_writes_recorded = 0
            self._total_writes_rejected = 0
            self._rejections_by_reason_kind = {
                "per_session_total": 0,
                "per_session_per_type": 0,
            }


_default_rate_limiter_lock = threading.Lock()
_default_rate_limiter: Optional[WriteRateLimiter] = None


def get_default_rate_limiter() -> WriteRateLimiter:
    """Returns the process-wide default WriteRateLimiter, constructing it on
    first use so all write attempts in the process share one set of counters."""
    global _default_rate_limiter
    with _default_rate_limiter_lock:
        if _default_rate_limiter is None:
            _default_rate_limiter = WriteRateLimiter()
        return _default_rate_limiter
