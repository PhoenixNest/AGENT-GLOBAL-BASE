"""
Executable pytest suite for the memory decay/consolidation maintenance job
(implementations/memory_maintenance.py), exercised against synthetic memory
records per research-report.md Secondary Recommendation 1.

Run with:
    pytest testing/test_memory_maintenance.py -v
"""

import math
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from implementations.memory_vector_store import MemoryRecord, MemorySyncState
from implementations.memory_maintenance import (
    ARCHIVE_GRACE_DAYS,
    ARCHIVE_THRESHOLD,
    BASE_STRENGTH_DAYS,
    CONSOLIDATION_THRESHOLD,
    DORMANT_THRESHOLD,
    REINFORCEMENT_FACTOR,
    MaintenanceReport,
    apply_decay,
    check_contradiction,
    compute_decay_weight,
    consolidate_session,
    cumulative_salience,
    next_status,
    run_consolidation_pass,
    run_maintenance_pass,
)

DAY = 86_400.0


def _record(**overrides):
    now = time.time()
    defaults = dict(
        id="rec-1",
        memory_type="semantic",
        content="synthetic content",
        created_at=now,
        last_accessed_at=now,
        access_count=0,
        importance=1.0,
        confidence=1.0,
        decay_weight=1.0,
        status="active",
        sacred=False,
    )
    defaults.update(overrides)
    return MemoryRecord(**defaults)


# ---------------------------------------------------------------------------
# Decay formula — verified against hand-computed values
# ---------------------------------------------------------------------------

class TestComputeDecayWeight:
    def test_matches_hand_computed_value_at_base_strength(self):
        now = 1_000_000.0
        created_at = now - BASE_STRENGTH_DAYS * DAY  # exactly one base_strength ago
        weight = compute_decay_weight(
            importance=1.0,
            created_at=created_at,
            last_accessed_at=created_at,
            access_count=0,
            now=now,
        )
        expected = math.exp(-1.0)  # delta_t == strength when access_count == 0
        assert weight == pytest.approx(expected, rel=1e-9)

    def test_zero_elapsed_time_returns_importance_unchanged(self):
        now = 1_000_000.0
        weight = compute_decay_weight(
            importance=0.7, created_at=now, last_accessed_at=now, access_count=0, now=now
        )
        assert weight == pytest.approx(0.7, rel=1e-9)

    def test_decay_weight_scales_with_importance(self):
        now = 1_000_000.0
        created_at = now - 3 * DAY
        low = compute_decay_weight(importance=0.2, created_at=created_at, last_accessed_at=created_at, access_count=0, now=now)
        high = compute_decay_weight(importance=1.0, created_at=created_at, last_accessed_at=created_at, access_count=0, now=now)
        assert high > low
        assert high == pytest.approx(low * 5, rel=1e-9)

    def test_reinforcement_slows_decay_relative_to_unaccessed(self):
        now = 1_000_000.0
        created_at = now - 10 * DAY
        unaccessed = compute_decay_weight(
            importance=1.0, created_at=created_at, last_accessed_at=created_at, access_count=0, now=now
        )
        reinforced = compute_decay_weight(
            importance=1.0, created_at=created_at, last_accessed_at=created_at, access_count=10, now=now
        )
        assert reinforced > unaccessed

    def test_reinforcement_matches_hand_computed_formula(self):
        now = 1_000_000.0
        created_at = now - 10 * DAY
        access_count = 10
        weight = compute_decay_weight(
            importance=1.0, created_at=created_at, last_accessed_at=created_at,
            access_count=access_count, now=now,
        )
        strength = BASE_STRENGTH_DAYS * (1 + access_count * REINFORCEMENT_FACTOR)
        expected = math.exp(-10.0 / strength)
        assert weight == pytest.approx(expected, rel=1e-9)

    def test_falls_back_to_created_at_when_never_accessed(self):
        now = 1_000_000.0
        created_at = now - 7 * DAY
        weight = compute_decay_weight(
            importance=1.0, created_at=created_at, last_accessed_at=None, access_count=0, now=now
        )
        expected = math.exp(-1.0)
        assert weight == pytest.approx(expected, rel=1e-9)


# ---------------------------------------------------------------------------
# Status transitions
# ---------------------------------------------------------------------------

class TestNextStatus:
    def test_high_decay_weight_is_active(self):
        now = 1_000_000.0
        assert next_status(decay_weight=0.9, created_at=now, last_accessed_at=now, now=now) == "active"

    def test_below_dormant_threshold_is_dormant(self):
        now = 1_000_000.0
        assert next_status(decay_weight=DORMANT_THRESHOLD - 0.01, created_at=now, last_accessed_at=now, now=now) == "dormant"

    def test_low_decay_weight_without_grace_period_stays_dormant(self):
        now = 1_000_000.0
        last_accessed = now - 5 * DAY  # below archive threshold but grace period not elapsed
        status = next_status(
            decay_weight=ARCHIVE_THRESHOLD - 0.01, created_at=last_accessed, last_accessed_at=last_accessed, now=now
        )
        assert status == "dormant"

    def test_low_decay_weight_with_grace_period_elapsed_is_archived(self):
        now = 1_000_000.0
        last_accessed = now - (ARCHIVE_GRACE_DAYS + 1) * DAY
        status = next_status(
            decay_weight=ARCHIVE_THRESHOLD - 0.01, created_at=last_accessed, last_accessed_at=last_accessed, now=now
        )
        assert status == "archived"


# ---------------------------------------------------------------------------
# apply_decay — full record mutation, including the sacred exemption
# ---------------------------------------------------------------------------

class TestApplyDecay:
    def test_sacred_record_is_pinned_regardless_of_age(self):
        now = 1_000_000.0
        ancient = now - 400 * DAY
        record = _record(sacred=True, importance=1.0, created_at=ancient, last_accessed_at=ancient, decay_weight=1.0)
        apply_decay(record, now=now)
        assert record.decay_weight == 1.0
        assert record.status == "active"

    def test_non_sacred_record_decays_and_transitions(self):
        now = 1_000_000.0
        old = now - 40 * DAY
        record = _record(sacred=False, importance=1.0, created_at=old, last_accessed_at=old, access_count=0)
        apply_decay(record, now=now)
        assert record.decay_weight < ARCHIVE_THRESHOLD
        assert record.status == "archived"

    def test_recently_written_non_sacred_record_stays_active(self):
        now = 1_000_000.0
        record = _record(sacred=False, importance=0.5, created_at=now, last_accessed_at=now)
        apply_decay(record, now=now)
        assert record.status == "active"


# ---------------------------------------------------------------------------
# Consolidation
# ---------------------------------------------------------------------------

class TestConsolidation:
    def test_cumulative_salience_sums_importance_times_access_count(self):
        records = [_record(importance=1.0, access_count=50), _record(importance=0.5, access_count=100)]
        assert cumulative_salience(records) == pytest.approx(1.0 * 50 + 0.5 * 100)

    def test_below_threshold_returns_none(self):
        records = [_record(importance=0.2, access_count=1)]
        result = consolidate_session("s1", records, summarizer=lambda recs: "summary", threshold=CONSOLIDATION_THRESHOLD)
        assert result is None

    def test_above_threshold_produces_semantic_record_with_provenance(self):
        records = [_record(id="ep-1", importance=1.0, access_count=100), _record(id="ep-2", importance=1.0, access_count=60)]
        result = consolidate_session(
            "session-x", records, summarizer=lambda recs: "distilled summary", threshold=CONSOLIDATION_THRESHOLD
        )
        assert result is not None
        assert result.memory_type == "semantic"
        assert result.content == "distilled summary"
        assert set(result.consolidated_from) == {"ep-1", "ep-2"}
        assert result.source_session_id == "session-x"

    def test_source_records_are_not_mutated_or_deleted(self):
        records = [_record(id="ep-1", importance=1.0, access_count=100)]
        original_status = records[0].status
        consolidate_session("session-x", records, summarizer=lambda recs: "summary", threshold=50.0)
        assert len(records) == 1
        assert records[0].status == original_status

    def test_archived_records_excluded_from_eligibility(self):
        records = [_record(id="ep-1", importance=1.0, access_count=1000, status="archived")]
        result = consolidate_session("session-x", records, summarizer=lambda recs: "summary", threshold=1.0)
        assert result is None

    def test_run_consolidation_pass_handles_multiple_sessions(self):
        by_session = {
            "s1": [_record(id="a", importance=1.0, access_count=200)],
            "s2": [_record(id="b", importance=0.1, access_count=1)],
        }
        results = run_consolidation_pass(by_session, summarizer=lambda recs: "s")
        assert len(results) == 1
        assert results[0].source_session_id == "s1"


# ---------------------------------------------------------------------------
# Contradiction check — built but not activated
# ---------------------------------------------------------------------------

class TestContradictionCheckNotActivated:
    def test_returns_verdict_from_injected_judge(self):
        new_record = _record(content="User prefers dark mode")
        existing = _record(content="User prefers light mode")
        verdict = check_contradiction(new_record, existing, llm_judge=lambda a, b: "UPDATE")
        assert verdict == "UPDATE"

    def test_invalid_verdict_from_judge_raises(self):
        new_record = _record()
        existing = _record()
        with pytest.raises(ValueError):
            check_contradiction(new_record, existing, llm_judge=lambda a, b: "MAYBE")

    def test_maintenance_pass_refuses_to_enable_without_review_ack(self):
        records = [_record()]
        with pytest.raises(RuntimeError):
            run_maintenance_pass(records, enable_contradiction_check=True, i_have_completed_adversarial_review=False)

    def test_maintenance_pass_never_runs_contradiction_checks_by_default(self):
        records = [_record()]
        report, _ = run_maintenance_pass(records)
        assert report.contradiction_checks_run == 0

    def test_maintenance_pass_still_reports_zero_even_if_flags_pre_wired(self):
        # Even a caller that has (hypothetically) completed review still gets
        # contradiction_checks_run == 0 — this pass structurally never calls it.
        records = [_record()]
        report, _ = run_maintenance_pass(
            records, enable_contradiction_check=True, i_have_completed_adversarial_review=True
        )
        assert report.contradiction_checks_run == 0


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

class TestRunMaintenancePass:
    def test_report_counts_scanned_records(self):
        records = [_record(id=str(i)) for i in range(5)]
        report, _ = run_maintenance_pass(records)
        assert report.records_scanned == 5
        assert report.decayed == 5

    def test_report_counts_status_transitions(self):
        now = time.time()
        old = now - 40 * DAY
        records = [
            _record(id="fresh", created_at=now, last_accessed_at=now, importance=1.0),
            _record(id="stale", created_at=old, last_accessed_at=old, importance=1.0),
        ]
        report, _ = run_maintenance_pass(records, now=now)
        assert report.transitioned_to_archived == 1
        assert report.transitioned_to_dormant == 0  # went straight active -> archived, never observed dormant

    def test_sacred_records_never_transition(self):
        old = time.time() - 400 * DAY
        records = [_record(sacred=True, importance=1.0, created_at=old, last_accessed_at=old)]
        report, _ = run_maintenance_pass(records)
        assert report.transitioned_to_dormant == 0
        assert report.transitioned_to_archived == 0
        assert records[0].status == "active"

    def test_dormant_ratio_computed(self):
        now = time.time()
        old = now - 10 * DAY  # dormant but not archived, per TestNextStatus math
        records = [_record(id="a", importance=1.0, created_at=old, last_accessed_at=old)]
        report, _ = run_maintenance_pass(records, now=now)
        assert report.dormant_ratio == 1.0

    def test_consolidation_runs_when_wired(self):
        records = [_record()]
        by_session = {"s1": [_record(id="ep-1", importance=1.0, access_count=200)]}
        report, new_semantic = run_maintenance_pass(
            records, episodic_by_session=by_session, summarizer=lambda recs: "consolidated"
        )
        assert report.consolidated == 1
        assert len(new_semantic) == 1

    def test_consolidation_skipped_when_not_wired(self):
        records = [_record()]
        report, new_semantic = run_maintenance_pass(records)
        assert report.consolidated == 0
        assert new_semantic == []

    def test_empty_records_list_does_not_error(self):
        report, new_semantic = run_maintenance_pass([])
        assert report.records_scanned == 0
        assert report.dormant_ratio == 0.0
        assert new_semantic == []


# ---------------------------------------------------------------------------
# Telemetry — sync_state wiring (02-deployment-guidelines.md §6)
# ---------------------------------------------------------------------------

class TestRunMaintenancePassTelemetry:
    def test_sync_state_records_consolidation_timestamp(self, tmp_path):
        sync_state = MemorySyncState(root_dir=tmp_path)
        records = [_record()]
        now = 1_700_000_000.0
        run_maintenance_pass(records, now=now, sync_state=sync_state)
        assert sync_state.get_last_consolidation_at() == now

    def test_sync_state_recorded_even_without_consolidation_inputs(self, tmp_path):
        sync_state = MemorySyncState(root_dir=tmp_path)
        run_maintenance_pass([_record()], now=42.0, sync_state=sync_state)
        assert sync_state.get_last_consolidation_at() == 42.0

    def test_no_sync_state_does_not_raise(self):
        report, _ = run_maintenance_pass([_record()], sync_state=None)
        assert report.records_scanned == 1

    def test_dormant_ratio_matches_shared_formula_on_mixed_batch(self):
        now = time.time()
        old = now - 10 * DAY  # dormant but not archived
        records = [
            _record(id="fresh", created_at=now, last_accessed_at=now, importance=1.0),
            _record(id="stale", created_at=old, last_accessed_at=old, importance=1.0),
        ]
        report, _ = run_maintenance_pass(records, now=now)
        assert report.dormant_ratio == pytest.approx(0.5)
