"""
Memory Maintenance — Decay, Consolidation, and Status-Transition Job

Standalone, testable module implementing this workspace's forgetting strategy —
full design spec:
    telescope/2026-07-10-agent-memory-architecture/supporting/03-forgetting-strategy.md

Deployed as a scheduled job (ScheduleWakeup or CronCreate), never as an inline
per-turn computation, so its decay formula stays unit-testable against
synthetic memory records independent of any live deployment.

This module implements:
    - Ebbinghaus-style exponential decay with access-based reinforcement
    - active -> dormant -> archived status transitions — soft-archival only,
      hard deletion never automatic
    - Episodic -> semantic consolidation via an injectable LLM summarizer
    - The contradiction-check LOGIC, built but structurally gated off — see
      check_contradiction() below
    - Telemetry: MaintenanceReport.dormant_ratio (via the shared
      compute_dormant_ratio formula in memory_vector_store.py, reused by the
      health_check MCP tool's corpus-wide computation) and last_consolidation_at
      (persisted via the optional `sync_state` param on run_maintenance_pass()
      below)

Explicitly not done here:
    - The LLM-judged contradiction check's production activation. Dr. Tomasz
      Wieczorek's adversarial evaluation of its false-positive UPDATE risk has
      run (telescope/2026-07-10-agent-memory-architecture/supporting/07-adversarial-evaluation-results.md)
      and found no independent safeguards against misclassification — the gate
      stays closed until the specific gaps that report lists are fixed.
      run_maintenance_pass() refuses to invoke check_contradiction() under any
      circumstance — see that function's docstring for the structural gate.
    - Threshold recalibration from real session data. The constants below are
      starting defaults, not validated values.
    - Per-collection point_counts and Qdrant reachability — those are
      qdrant-memory-specific and live in
      memory_vector_store.compute_memory_instance_telemetry() instead, since
      this module has no Qdrant client dependency by design.
"""

from __future__ import annotations

import math
import time
import uuid
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from .memory_vector_store import MemoryRecord, MemorySyncState, compute_dormant_ratio


def _now() -> float:
    return time.time()


def _new_id() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Tunable constants — deployment defaults.
# None of these are empirically validated against this workspace's actual
# session data yet — recalibrate once real usage data exists (see
# supporting/08-threshold-sensitivity-check.md for a synthetic bounds-check).
# ---------------------------------------------------------------------------

BASE_STRENGTH_DAYS = 7.0
REINFORCEMENT_FACTOR = 0.5
DORMANT_THRESHOLD = 0.5
ARCHIVE_THRESHOLD = 0.15
ARCHIVE_GRACE_DAYS = 30.0
CONSOLIDATION_THRESHOLD = 150.0  # cumulative importance x access_count, per session


# ---------------------------------------------------------------------------
# Decay formula
# ---------------------------------------------------------------------------

def compute_decay_weight(
    importance: float,
    created_at: float,
    last_accessed_at: Optional[float],
    access_count: int,
    now: Optional[float] = None,
    base_strength_days: float = BASE_STRENGTH_DAYS,
    reinforcement_factor: float = REINFORCEMENT_FACTOR,
) -> float:
    """
    decay_weight(t) = importance * e^(-delta_t / strength)
    strength = base_strength * (1 + access_count * reinforcement_factor)

    delta_t is measured from last_accessed_at (or created_at if never accessed).
    Every retrieval of a record extends `strength`, so frequently-retrieved facts
    decay slower than the global average — the spaced-repetition/rehearsal analog.
    """
    now = now if now is not None else _now()
    anchor = last_accessed_at if last_accessed_at is not None else created_at
    delta_t_days = max(0.0, (now - anchor) / 86_400.0)
    strength = base_strength_days * (1.0 + access_count * reinforcement_factor)
    if strength <= 0:
        return 0.0
    return importance * math.exp(-delta_t_days / strength)


def next_status(
    decay_weight: float,
    created_at: float,
    last_accessed_at: Optional[float],
    now: Optional[float] = None,
    archive_grace_days: float = ARCHIVE_GRACE_DAYS,
) -> str:
    """
    active -> dormant when decay_weight < 0.5 ("weakened synapse, not yet pruned").
    dormant -> archived when decay_weight < 0.15 AND no access for >= grace period.

    Never returns anything beyond "archived" — hard deletion is a separate,
    explicitly operator-confirmed step this module does not perform.
    """
    now = now if now is not None else _now()
    anchor = last_accessed_at if last_accessed_at is not None else created_at
    no_access_days = max(0.0, (now - anchor) / 86_400.0)
    if decay_weight < ARCHIVE_THRESHOLD and no_access_days >= archive_grace_days:
        return "archived"
    if decay_weight < DORMANT_THRESHOLD:
        return "dormant"
    return "active"


def apply_decay(record: MemoryRecord, now: Optional[float] = None) -> MemoryRecord:
    """
    Recompute decay_weight and status for one record, in place, and return it.

    Sacred records (the "flashbulb memory" analog — decisions and commitments)
    are exempt entirely: pinned at decay_weight=1.0, status="active", regardless
    of elapsed time or access history — this mirrors
    EpisodicMemory.get_sacred_context()'s existing contract that
    decisions/commitments are returned verbatim every time.
    """
    if record.sacred:
        record.decay_weight = 1.0
        record.status = "active"
        return record

    now = now if now is not None else _now()
    record.decay_weight = compute_decay_weight(
        importance=record.importance,
        created_at=record.created_at,
        last_accessed_at=record.last_accessed_at,
        access_count=record.access_count,
        now=now,
    )
    record.status = next_status(
        decay_weight=record.decay_weight,
        created_at=record.created_at,
        last_accessed_at=record.last_accessed_at,
        now=now,
    )
    return record


# ---------------------------------------------------------------------------
# Consolidation — episodic -> semantic
# ---------------------------------------------------------------------------

def cumulative_salience(records: List[MemoryRecord]) -> float:
    """
    Sum of importance x access_count across a session's episodic records — the
    reflection-trigger signal, directly reusing Generative Agents' 150-point
    empirically-tuned threshold as a starting point (Park et al. 2023).
    """
    return sum(r.importance * r.access_count for r in records)


def consolidate_session(
    session_id: str,
    records: List[MemoryRecord],
    summarizer: Callable[[List[MemoryRecord]], str],
    now: Optional[float] = None,
    threshold: float = CONSOLIDATION_THRESHOLD,
) -> Optional[MemoryRecord]:
    """
    If a session's cumulative episodic salience crosses `threshold`, synthesize a
    single distilled semantic MemoryRecord via the injected `summarizer` — reuse
    ContextCompressor's summarization path in production
    (context_compressor.py's compress_with_api / _summarise_tier), injected here
    rather than imported directly so this module stays free of any live-LLM
    dependency and fully unit-testable with a stub summarizer.

    The source episodic records are NOT deleted or mutated — consolidation only
    adds a new semantic record, never removes what it was built from. Returns
    None if the session is not yet eligible.
    """
    eligible = [r for r in records if r.status != "archived"]
    if not eligible or cumulative_salience(eligible) < threshold:
        return None

    now = now if now is not None else _now()
    summary_text = summarizer(eligible)
    return MemoryRecord(
        id=_new_id(),
        memory_type="semantic",
        content=summary_text,
        created_at=now,
        last_accessed_at=now,
        access_count=0,
        importance=0.6,
        confidence=1.0,
        decay_weight=1.0,
        status="active",
        source_session_id=session_id,
        source_turn=0,
        sacred=False,
        tags=["consolidated"],
        consolidated_from=[r.id for r in eligible],
    )


def run_consolidation_pass(
    episodic_by_session: Dict[str, List[MemoryRecord]],
    summarizer: Callable[[List[MemoryRecord]], str],
    now: Optional[float] = None,
    threshold: float = CONSOLIDATION_THRESHOLD,
) -> List[MemoryRecord]:
    """Run consolidate_session() over every session; return the new semantic records."""
    results: List[MemoryRecord] = []
    for session_id, records in episodic_by_session.items():
        result = consolidate_session(session_id, records, summarizer, now=now, threshold=threshold)
        if result is not None:
            results.append(result)
    return results


# ---------------------------------------------------------------------------
# Contradiction check — LOGIC BUILT, NOT PRODUCTION-ACTIVATED
# ---------------------------------------------------------------------------

_VALID_VERDICTS = {"ADD", "UPDATE", "NOOP"}


def check_contradiction(
    new_record: MemoryRecord,
    existing_record: MemoryRecord,
    llm_judge: Callable[[str, str], str],
) -> str:
    """
    Classify the relationship between a newly-written semantic fact and an
    existing one retrieved above the similarity threshold, per Mem0's
    ADD/UPDATE/NOOP three-way decision (Dwarves Memo, retrieved 2026-07-10).

    *** NOT ACTIVATED IN ANY PRODUCTION OR DEFAULT PATH. ***

    This function exists so consolidation's dependency graph is complete and
    this logic is unit-testable. Dr. Tomasz Wieczorek's adversarial evaluation
    (telescope/2026-07-10-agent-memory-architecture/supporting/07-adversarial-evaluation-results.md)
    has already run against it and found no independent safeguards: a
    representative naive judge misclassified 5/5 curated non-contradictory
    pairs as UPDATE, the verdict is order-sensitive, and an engineered
    "contradiction" can force archival of a true, unrelated fact. It must NOT
    be wired into run_maintenance_pass() or any live pipeline until the gaps
    that report lists are fixed and a follow-up evaluation clears them. Calling
    this function directly outside of tests is a policy violation, not just an
    engineering suggestion.

    Returns one of "ADD" | "UPDATE" | "NOOP".
    """
    verdict = llm_judge(new_record.content, existing_record.content)
    if verdict not in _VALID_VERDICTS:
        raise ValueError(f"llm_judge returned an invalid verdict: {verdict!r}")
    return verdict


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

@dataclass
class MaintenanceReport:
    now: float
    records_scanned: int = 0
    decayed: int = 0
    transitioned_to_dormant: int = 0
    transitioned_to_archived: int = 0
    consolidated: int = 0
    contradiction_checks_run: int = 0
    # Fraction of the scanned `records` batch left dormant after this pass —
    # computed via the shared compute_dormant_ratio() formula in
    # memory_vector_store.py, so this number and health_check's corpus-wide
    # dormant_ratio can never drift apart from using different math.
    dormant_ratio: float = 0.0


def run_maintenance_pass(
    records: List[MemoryRecord],
    episodic_by_session: Optional[Dict[str, List[MemoryRecord]]] = None,
    summarizer: Optional[Callable[[List[MemoryRecord]], str]] = None,
    now: Optional[float] = None,
    enable_contradiction_check: bool = False,
    i_have_completed_adversarial_review: bool = False,
    sync_state: Optional[MemorySyncState] = None,
) -> Tuple[MaintenanceReport, List[MemoryRecord]]:
    """
    Run one full maintenance pass: decay recomputation over `records`, then
    (if episodic_by_session + summarizer are given) episodic->semantic
    consolidation. Returns (report, new_semantic_records_from_consolidation).

    The contradiction check (check_contradiction()) is refused unconditionally
    unless the caller both opts in AND explicitly acknowledges the adversarial
    review is complete. That review has run and found the mechanism unsafe to
    activate as-is (see check_contradiction()'s docstring) — no caller may
    legitimately set i_have_completed_adversarial_review=True yet. This pass
    never calls check_contradiction() regardless of these flags; they exist
    only so a future, review-gated activation has a documented entry point
    instead of requiring a new signature.

    If `sync_state` is given, its `last_consolidation_at` is updated to `now`
    once this pass completes — regardless of whether consolidation produced any
    new records, since the field means "the last maintenance pass ran," not
    "the last pass that consolidated something." Omitting `sync_state` (the
    default) leaves this pass's behavior and return value identical to before
    this field existed.
    """
    if enable_contradiction_check and not i_have_completed_adversarial_review:
        raise RuntimeError(
            "Contradiction-check activation requires "
            "i_have_completed_adversarial_review=True. Dr. Tomasz Wieczorek's "
            "adversarial evaluation has run and found this mechanism unsafe to "
            "activate (see supporting/07-adversarial-evaluation-results.md) — "
            "the gaps it lists must be fixed and re-evaluated first. Refusing "
            "to enable it."
        )

    now = now if now is not None else _now()
    report = MaintenanceReport(now=now, records_scanned=len(records))

    for record in records:
        before_status = record.status
        apply_decay(record, now=now)
        report.decayed += 1
        if before_status != "dormant" and record.status == "dormant":
            report.transitioned_to_dormant += 1
        if before_status != "archived" and record.status == "archived":
            report.transitioned_to_archived += 1

    dormant_count = sum(1 for r in records if r.status == "dormant")
    report.dormant_ratio = compute_dormant_ratio(dormant_count, len(records))

    new_semantic: List[MemoryRecord] = []
    if episodic_by_session and summarizer is not None:
        new_semantic = run_consolidation_pass(episodic_by_session, summarizer, now=now)
        report.consolidated = len(new_semantic)

    # check_contradiction() is never invoked here — see the docstring above and
    # check_contradiction()'s own docstring for why.
    report.contradiction_checks_run = 0

    if sync_state is not None:
        sync_state.record_consolidation(now)

    return report, new_semantic
