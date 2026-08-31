"""
Executable pytest suite for
core-component-00/platform/model-context-protocol-servers/agent-memory/write_provenance.py.

No live Qdrant instance, embedder-service, or MCP server import is required
for anything in this file — write_provenance.py is pure Python with no I/O,
so these tests import it directly rather than going through the
agent_memory_server fixture in conftest.py.

Covers:
  - validate_provenance: rejects each missing/malformed field individually,
    accepts a well-formed instance.
  - WriteRateLimiter: allows writes under threshold, rejects the exact
    repeated-attempt pattern test_contradiction_adversarial.py's
    `test_repeated_poisoning_attempts_are_not_rate_limited_or_flagged` found
    unguarded (50 identical attempts, same scale as that eval), and
    get_telemetry()'s output shape is stable and never raises.

Run with:
    python -m pytest core-component-00/platform/model-context-protocol-servers/agent-memory/tests/test_write_provenance.py -v
"""
import importlib.util
import math
import sys
import threading
from pathlib import Path

import pytest

_MODULE_PATH = Path(__file__).resolve().parents[1] / "write_provenance.py"


def _load_write_provenance():
    if "write_provenance" in sys.modules:
        return sys.modules["write_provenance"]
    spec = importlib.util.spec_from_file_location("write_provenance", _MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["write_provenance"] = module
    spec.loader.exec_module(module)
    return module


wp = _load_write_provenance()


def _good_provenance(**overrides):
    defaults = dict(
        source="session-abc-123",
        triggering_context_excerpt="User asked to remember their preferred timezone is UTC+8.",
        from_external_content=False,
        confidence=0.9,
    )
    defaults.update(overrides)
    return wp.WriteProvenance(**defaults)


# ---------------------------------------------------------------------------
# WriteProvenance / validate_provenance
# ---------------------------------------------------------------------------


class TestValidateProvenanceAccepts:
    def test_well_formed_instance_is_accepted(self):
        ok, reason = wp.validate_provenance(_good_provenance())
        assert ok is True
        assert reason == "ok"

    def test_confidence_boundary_zero_is_accepted(self):
        ok, reason = wp.validate_provenance(_good_provenance(confidence=0.0))
        assert ok is True

    def test_confidence_boundary_one_is_accepted(self):
        ok, reason = wp.validate_provenance(_good_provenance(confidence=1.0))
        assert ok is True

    def test_from_external_content_true_is_accepted(self):
        ok, reason = wp.validate_provenance(_good_provenance(from_external_content=True))
        assert ok is True


class TestValidateProvenanceRejectsEachFieldIndividually:
    def test_none_provenance_is_rejected(self):
        ok, reason = wp.validate_provenance(None)
        assert ok is False
        assert "not supplied" in reason or "None" in reason

    def test_wrong_type_is_rejected(self):
        ok, reason = wp.validate_provenance("not a WriteProvenance")  # type: ignore[arg-type]
        assert ok is False
        assert "WriteProvenance" in reason

    def test_missing_source_empty_string_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(source=""))
        assert ok is False
        assert "source" in reason

    def test_source_whitespace_only_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(source="   "))
        assert ok is False
        assert "source" in reason

    def test_source_wrong_type_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(source=None))  # type: ignore[arg-type]
        assert ok is False
        assert "source" in reason

    def test_missing_triggering_context_excerpt_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(triggering_context_excerpt=""))
        assert ok is False
        assert "triggering_context_excerpt" in reason

    def test_triggering_context_excerpt_whitespace_only_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(triggering_context_excerpt="  \n "))
        assert ok is False
        assert "triggering_context_excerpt" in reason

    def test_triggering_context_excerpt_wrong_type_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(triggering_context_excerpt=None))  # type: ignore[arg-type]
        assert ok is False
        assert "triggering_context_excerpt" in reason

    def test_from_external_content_wrong_type_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(from_external_content="yes"))  # type: ignore[arg-type]
        assert ok is False
        assert "from_external_content" in reason

    def test_confidence_wrong_type_string_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(confidence="0.9"))  # type: ignore[arg-type]
        assert ok is False
        assert "confidence" in reason

    def test_confidence_bool_is_rejected(self):
        # bool is a subclass of int in Python — must be explicitly rejected
        # so True/False can't silently pass as 1.0/0.0.
        ok, reason = wp.validate_provenance(_good_provenance(confidence=True))  # type: ignore[arg-type]
        assert ok is False
        assert "confidence" in reason

    def test_confidence_below_zero_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(confidence=-0.01))
        assert ok is False
        assert "confidence" in reason

    def test_confidence_above_one_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(confidence=1.01))
        assert ok is False
        assert "confidence" in reason

    def test_confidence_nan_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(confidence=float("nan")))
        assert ok is False
        assert "finite" in reason

    def test_confidence_infinity_is_rejected(self):
        ok, reason = wp.validate_provenance(_good_provenance(confidence=float("inf")))
        assert ok is False
        assert "finite" in reason


class TestWriteProvenanceExcerptTruncation:
    def test_excerpt_within_cap_is_untouched(self):
        excerpt = "x" * (wp.MAX_EXCERPT_CHARS - 1)
        prov = _good_provenance(triggering_context_excerpt=excerpt)
        assert prov.triggering_context_excerpt == excerpt

    def test_excerpt_over_cap_is_truncated_not_rejected(self):
        excerpt = "x" * (wp.MAX_EXCERPT_CHARS * 2)
        prov = _good_provenance(triggering_context_excerpt=excerpt)
        assert len(prov.triggering_context_excerpt) <= wp.MAX_EXCERPT_CHARS
        # Truncation, not rejection: validate_provenance must still accept it.
        ok, reason = wp.validate_provenance(prov)
        assert ok is True


# ---------------------------------------------------------------------------
# WriteRateLimiter
# ---------------------------------------------------------------------------


class TestWriteRateLimiterAllowsUnderThreshold:
    def test_writes_under_both_thresholds_are_allowed(self):
        limiter = wp.WriteRateLimiter(
            max_writes_per_session=20,
            max_writes_per_session_per_type=8,
            window_s=3600.0,
        )
        for _ in range(5):
            allowed, reason = limiter.check_and_record("session-1", "semantic")
            assert allowed is True
            assert reason == "ok"

    def test_different_types_have_independent_per_type_counters(self):
        limiter = wp.WriteRateLimiter(
            max_writes_per_session=100,
            max_writes_per_session_per_type=3,
            window_s=3600.0,
        )
        for _ in range(3):
            allowed, _ = limiter.check_and_record("session-1", "semantic")
            assert allowed is True
        for _ in range(3):
            allowed, _ = limiter.check_and_record("session-1", "episodic")
            assert allowed is True
        # 4th semantic write in this session should now be rejected even
        # though episodic has its own separate counter.
        allowed, reason = limiter.check_and_record("session-1", "semantic")
        assert allowed is False
        assert "per-session-per-type" in reason

    def test_different_sessions_have_independent_counters(self):
        limiter = wp.WriteRateLimiter(
            max_writes_per_session=2,
            max_writes_per_session_per_type=2,
            window_s=3600.0,
        )
        assert limiter.check_and_record("session-a", "semantic")[0] is True
        assert limiter.check_and_record("session-a", "semantic")[0] is True
        assert limiter.check_and_record("session-a", "semantic")[0] is False
        # session-b is unaffected by session-a's counters.
        assert limiter.check_and_record("session-b", "semantic")[0] is True


class TestWriteRateLimiterCatchesRepeatedPoisoningPattern:
    def test_50_identical_attempts_are_rejected_well_before_50(self):
        """
        Direct analog of test_contradiction_adversarial.py's
        test_repeated_poisoning_attempts_are_not_rate_limited_or_flagged,
        which found 50 consecutive identical calls to check_contradiction()
        all succeeded with no counter, log, or flag. Fires the same 50-call
        pattern against WriteRateLimiter.check_and_record with identical
        session_id/memory_type on every call, using default thresholds, and
        asserts rejection kicks in well before the 50th call.
        """
        limiter = wp.WriteRateLimiter()  # default thresholds
        results = [limiter.check_and_record("session-poison", "semantic") for _ in range(50)]
        allowed_count = sum(1 for allowed, _ in results if allowed)
        rejected_count = 50 - allowed_count

        # Must not silently allow all 50 (the exact gap the adversarial eval found).
        assert rejected_count > 0
        # Rejection must kick in well before the 50th call — allowed count
        # should be capped at the per-session-per-type default (8), which is
        # far below 50.
        assert allowed_count <= wp.DEFAULT_MAX_WRITES_PER_SESSION_PER_TYPE
        assert allowed_count < 50

        # Every rejected attempt must carry an identifying reason, not a bare
        # False — mirrors this module's "counter/log/flag" requirement.
        for allowed, reason in results:
            if not allowed:
                assert "rejected" in reason
                assert "session-poison" in reason

    def test_repeated_attempts_are_actually_counted_not_just_blocked(self):
        limiter = wp.WriteRateLimiter()
        for _ in range(50):
            limiter.check_and_record("session-poison", "semantic")
        telemetry = limiter.get_telemetry()
        assert telemetry["total_writes_rejected"] > 0
        assert telemetry["total_writes_recorded"] <= wp.DEFAULT_MAX_WRITES_PER_SESSION_PER_TYPE

    def test_per_session_total_threshold_also_catches_mixed_type_repetition(self):
        # Even spreading identical-intent attempts across many memory_types
        # to dodge the per-type counter, the per-session total still bounds
        # it well below 50.
        limiter = wp.WriteRateLimiter(
            max_writes_per_session=10,
            max_writes_per_session_per_type=100,  # effectively disabled
            window_s=3600.0,
        )
        results = [
            limiter.check_and_record("session-poison-2", f"type-{i}") for i in range(50)
        ]
        allowed_count = sum(1 for allowed, _ in results if allowed)
        assert allowed_count == 10
        rejected_reasons = [reason for allowed, reason in results if not allowed]
        assert all("per-session total" in r for r in rejected_reasons)


class TestWriteRateLimiterRollingWindow:
    def test_old_entries_age_out_of_the_window(self):
        limiter = wp.WriteRateLimiter(
            max_writes_per_session=1,
            max_writes_per_session_per_type=1,
            window_s=0.05,
        )
        assert limiter.check_and_record("session-1", "semantic")[0] is True
        assert limiter.check_and_record("session-1", "semantic")[0] is False
        import time

        time.sleep(0.1)
        # After the window elapses, the earlier attempt should have aged out.
        assert limiter.check_and_record("session-1", "semantic")[0] is True


class TestWriteRateLimiterMaxTrackedSessionsBounding:
    def test_tracked_sessions_never_exceed_the_cap(self):
        limiter = wp.WriteRateLimiter(max_tracked_sessions=5)
        for i in range(50):
            limiter.check_and_record(f"session-{i}", "semantic")
        telemetry = limiter.get_telemetry()
        assert telemetry["tracked_sessions"] <= 5

    def test_eviction_is_lru_oldest_session_evicted_first(self):
        limiter = wp.WriteRateLimiter(
            max_tracked_sessions=2,
            max_writes_per_session=10,
            max_writes_per_session_per_type=10,
        )
        limiter.check_and_record("session-old", "semantic")
        limiter.check_and_record("session-mid", "semantic")
        # This should evict "session-old" (least recently touched).
        limiter.check_and_record("session-new", "semantic")
        telemetry = limiter.get_telemetry()
        tracked_ids = {s["session_id"] for s in telemetry["recent_sessions_summary"]}
        assert "session-old" not in tracked_ids
        assert "session-mid" in tracked_ids
        assert "session-new" in tracked_ids


class TestWriteRateLimiterConstructorValidation:
    @pytest.mark.parametrize(
        "kwargs",
        [
            dict(max_writes_per_session=0),
            dict(max_writes_per_session=-1),
            dict(max_writes_per_session_per_type=0),
            dict(window_s=0),
            dict(window_s=-5),
            dict(max_tracked_sessions=0),
        ],
    )
    def test_non_positive_thresholds_are_rejected(self, kwargs):
        with pytest.raises(ValueError):
            wp.WriteRateLimiter(**kwargs)


class TestWriteRateLimiterTelemetryShape:
    def test_telemetry_shape_on_empty_limiter(self):
        limiter = wp.WriteRateLimiter()
        telemetry = limiter.get_telemetry()
        expected_keys = {
            "total_writes_recorded",
            "total_writes_rejected",
            "rejections_by_reason_kind",
            "tracked_sessions",
            "max_tracked_sessions",
            "window_s",
            "max_writes_per_session",
            "max_writes_per_session_per_type",
            "recent_sessions_summary",
            "limitation",
        }
        assert expected_keys.issubset(telemetry.keys())
        assert telemetry["total_writes_recorded"] == 0
        assert telemetry["total_writes_rejected"] == 0
        assert telemetry["tracked_sessions"] == 0
        assert telemetry["recent_sessions_summary"] == []

    def test_telemetry_shape_is_stable_after_activity(self):
        limiter = wp.WriteRateLimiter()
        for i in range(3):
            limiter.check_and_record(f"session-{i}", "semantic")
        telemetry = limiter.get_telemetry()
        assert isinstance(telemetry["total_writes_recorded"], int)
        assert isinstance(telemetry["recent_sessions_summary"], list)
        for entry in telemetry["recent_sessions_summary"]:
            assert "session_id" in entry
            assert "writes_in_window" in entry
            assert "by_type" in entry

    def test_telemetry_summary_is_bounded_regardless_of_tracked_sessions(self):
        limiter = wp.WriteRateLimiter(max_tracked_sessions=5000)
        for i in range(200):
            limiter.check_and_record(f"session-{i}", "semantic")
        telemetry = limiter.get_telemetry()
        assert len(telemetry["recent_sessions_summary"]) <= 20

    def test_telemetry_never_raises_even_under_concurrent_access(self):
        limiter = wp.WriteRateLimiter()

        def _hammer(n):
            for i in range(n):
                limiter.check_and_record(f"session-{i % 10}", "semantic")
                limiter.get_telemetry()

        threads = [threading.Thread(target=_hammer, args=(25,)) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # If we got here without an exception, telemetry never raised under
        # concurrent load. Final sanity check on the shape.
        telemetry = limiter.get_telemetry()
        assert isinstance(telemetry, dict)
        assert "total_writes_recorded" in telemetry

    def test_reset_clears_all_state(self):
        limiter = wp.WriteRateLimiter()
        for _ in range(5):
            limiter.check_and_record("session-1", "semantic")
        limiter.reset()
        telemetry = limiter.get_telemetry()
        assert telemetry["total_writes_recorded"] == 0
        assert telemetry["total_writes_rejected"] == 0
        assert telemetry["tracked_sessions"] == 0


class TestGetDefaultRateLimiter:
    def test_returns_same_instance_across_calls(self):
        first = wp.get_default_rate_limiter()
        second = wp.get_default_rate_limiter()
        assert first is second
