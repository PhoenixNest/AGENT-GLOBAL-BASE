"""
Executable pytest suite for core-component-00/platform/model-context-protocol-servers/agent-memory/write_gate.py.

No live Qdrant instance, embedder-service, or MCP host is required for anything in this file —
WriteConfirmationGate's marker I/O is redirected into pytest's own tmp_path via monkeypatching
write_gate._repo_root(), so tests never touch this worktree's real
.claude/hooks/.state/ directory or collide with a real H-P01 or memory-write marker.

Run with (from this directory, or from core-component-00/platform/model-context-protocol-servers/agent-memory/):
    python -m pytest core-component-00/platform/model-context-protocol-servers/agent-memory/tests/test_write_gate.py -v

Covers, per the build brief:
  - classify() correctness for all three high-consequence triggers and the routine case
  - request_confirmation()/check_confirmation() round trip
  - stale-marker expiry mirrors H-P01's 15-minute behavior
  - promote_quarantined_write()/reject_quarantined_write() require a valid
    ReviewerConfirmation and reject a forged/missing one
"""
import datetime
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import write_gate  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def gate(tmp_path, monkeypatch):
    """A WriteConfirmationGate whose marker directory is redirected into
    tmp_path, so tests never write into this worktree's real
    .claude/hooks/.state/ directory."""
    monkeypatch.setattr(write_gate, "_repo_root", lambda: tmp_path)
    return write_gate.WriteConfirmationGate()


def _make_record(record_id="rec-1", status="quarantined"):
    return SimpleNamespace(id=record_id, status=status)


# ---------------------------------------------------------------------------
# classify()
# ---------------------------------------------------------------------------


class TestClassify:
    def test_sacred_is_high_consequence(self, gate):
        assert (
            gate.classify(memory_type="semantic", sacred=True, would_collide_with_existing=False)
            == "high_consequence"
        )

    def test_collision_is_high_consequence(self, gate):
        assert (
            gate.classify(memory_type="semantic", sacred=False, would_collide_with_existing=True)
            == "high_consequence"
        )

    def test_reflection_memory_type_is_high_consequence(self, gate):
        assert (
            gate.classify(
                memory_type="reflection", sacred=False, would_collide_with_existing=False
            )
            == "high_consequence"
        )

    def test_reflection_high_consequence_even_with_no_other_trigger(self, gate):
        # Explicitly exercises the "memory_type == 'reflection'" branch in isolation
        # from the other two triggers, since reflection is treated as maximally
        # sensitive regardless of sacred/collision status (write_gate.py docstring).
        for sacred in (True, False):
            for collide in (True, False):
                assert (
                    gate.classify(
                        memory_type="reflection",
                        sacred=sacred,
                        would_collide_with_existing=collide,
                    )
                    == "high_consequence"
                )

    def test_routine_when_no_trigger_present(self, gate):
        for memory_type in ("episodic", "semantic", "procedural"):
            assert (
                gate.classify(
                    memory_type=memory_type, sacred=False, would_collide_with_existing=False
                )
                == "routine"
            )

    def test_multiple_triggers_still_high_consequence(self, gate):
        assert (
            gate.classify(memory_type="reflection", sacred=True, would_collide_with_existing=True)
            == "high_consequence"
        )


# ---------------------------------------------------------------------------
# request_confirmation() / check_confirmation() round trip
# ---------------------------------------------------------------------------


class TestConfirmationRoundTrip:
    def test_no_marker_means_allowed(self, gate):
        allowed, reason = gate.check_confirmation("session-never-requested")
        assert allowed is True
        assert "no pending confirmation marker" in reason

    def test_pending_marker_blocks(self, gate):
        gate.request_confirmation("session-abc", summary="write semantic fact X")
        allowed, reason = gate.check_confirmation("session-abc")
        assert allowed is False
        assert "confirmation still pending" in reason

    def test_marker_file_written_with_expected_shape(self, gate):
        gate.request_confirmation("session-xyz", summary="write procedural fact Y")
        marker_path = gate.confirmation_marker_path("session-xyz")
        assert marker_path.is_file()
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        assert marker["pending"] is True
        assert marker["summary"] == "write procedural fact Y"
        # "ts" must be parseable the same way H-P01's marker is.
        datetime.datetime.fromisoformat(marker["ts"])

    def test_marker_filename_distinct_from_h_p01(self, gate):
        gate.request_confirmation("session-distinct", summary="s")
        marker_path = gate.confirmation_marker_path("session-distinct")
        assert marker_path.name.startswith("mem-write-pending-")
        assert not marker_path.name.startswith("h-p01-pending-")

    def test_clearing_marker_unblocks(self, gate):
        gate.request_confirmation("session-clear-me", summary="s")
        allowed, _ = gate.check_confirmation("session-clear-me")
        assert allowed is False

        # Simulates write-memory-gate-clear.py's own action: remove the marker.
        gate.confirmation_marker_path("session-clear-me").unlink()

        allowed, reason = gate.check_confirmation("session-clear-me")
        assert allowed is True
        assert "no pending confirmation marker" in reason

    def test_different_sessions_are_independent(self, gate):
        gate.request_confirmation("session-1", summary="s1")
        allowed_1, _ = gate.check_confirmation("session-1")
        allowed_2, _ = gate.check_confirmation("session-2")
        assert allowed_1 is False
        assert allowed_2 is True


# ---------------------------------------------------------------------------
# Stale-marker expiry — mirrors H-P01's 15-minute fail-safe
# ---------------------------------------------------------------------------


class TestStaleMarkerExpiry:
    def _write_marker_with_age(self, gate, session_id, age_seconds, summary="s"):
        marker_path = gate.confirmation_marker_path(session_id)
        marker_path.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now() - datetime.timedelta(seconds=age_seconds)
        marker = {"pending": True, "ts": ts.isoformat(), "summary": summary}
        marker_path.write_text(json.dumps(marker), encoding="utf-8")
        return marker_path

    def test_fresh_marker_still_blocks(self, gate):
        self._write_marker_with_age(gate, "session-fresh", age_seconds=60)
        allowed, reason = gate.check_confirmation("session-fresh")
        assert allowed is False
        assert "confirmation still pending" in reason

    def test_marker_just_under_threshold_still_blocks(self, gate):
        self._write_marker_with_age(gate, "session-under", age_seconds=899)
        allowed, _ = gate.check_confirmation("session-under")
        assert allowed is False

    def test_marker_over_threshold_is_stale_and_clears(self, gate):
        marker_path = self._write_marker_with_age(gate, "session-stale", age_seconds=901)
        allowed, reason = gate.check_confirmation("session-stale")
        assert allowed is True
        assert "stale" in reason
        assert not marker_path.is_file()

    def test_stale_threshold_matches_h_p01_exactly(self, gate):
        assert write_gate.STALE_MARKER_SECONDS == 900

    def test_corrupt_marker_treated_as_stale(self, gate):
        marker_path = gate.confirmation_marker_path("session-corrupt")
        marker_path.parent.mkdir(parents=True, exist_ok=True)
        marker_path.write_text("not valid json", encoding="utf-8")
        allowed, reason = gate.check_confirmation("session-corrupt")
        assert allowed is True
        assert "stale" in reason
        assert not marker_path.is_file()

    def test_missing_ts_field_treated_as_stale(self, gate):
        marker_path = gate.confirmation_marker_path("session-no-ts")
        marker_path.parent.mkdir(parents=True, exist_ok=True)
        marker_path.write_text(json.dumps({"pending": True}), encoding="utf-8")
        allowed, _ = gate.check_confirmation("session-no-ts")
        assert allowed is True
        assert not marker_path.is_file()


# ---------------------------------------------------------------------------
# Repo-root resolution failure
# ---------------------------------------------------------------------------


class TestRepoRootUnresolved:
    def test_confirmation_marker_path_raises_when_repo_root_unresolved(self, monkeypatch):
        monkeypatch.setattr(write_gate, "_repo_root", lambda: None)
        g = write_gate.WriteConfirmationGate()
        with pytest.raises(write_gate.RepoRootUnresolvedError):
            g.confirmation_marker_path("session-any")


# ---------------------------------------------------------------------------
# promote_quarantined_write() / reject_quarantined_write()
# ---------------------------------------------------------------------------


class TestPromoteRejectQuarantinedWrite:
    def test_promote_with_valid_confirmation_succeeds(self):
        record = _make_record(record_id="rec-promote", status="quarantined")
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="Dr. Elias Vance", record_id="rec-promote", decision="promote"
        )
        result = write_gate.promote_quarantined_write(record, confirmation)
        assert result is True
        assert record.status == "active"

    def test_reject_with_valid_confirmation_succeeds(self):
        record = _make_record(record_id="rec-reject", status="quarantined")
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="Dr. Elias Vance", record_id="rec-reject", decision="reject"
        )
        result = write_gate.reject_quarantined_write(record, confirmation)
        assert result is True
        assert record.status == "archived"

    def test_promote_rejects_missing_confirmation(self):
        record = _make_record()
        with pytest.raises(write_gate.InvalidReviewerConfirmationError):
            write_gate.promote_quarantined_write(record, None)

    def test_promote_rejects_forged_bare_string_confirmation(self):
        record = _make_record()
        with pytest.raises(write_gate.InvalidReviewerConfirmationError):
            write_gate.promote_quarantined_write(record, "yes, approved")  # type: ignore[arg-type]

    def test_promote_rejects_confirmation_for_different_record(self):
        record = _make_record(record_id="rec-A", status="quarantined")
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="Dr. Elias Vance", record_id="rec-B", decision="promote"
        )
        with pytest.raises(write_gate.InvalidReviewerConfirmationError):
            write_gate.promote_quarantined_write(record, confirmation)
        # Status must be unchanged on rejection.
        assert record.status == "quarantined"

    def test_promote_rejects_confirmation_with_wrong_decision(self):
        record = _make_record(record_id="rec-C", status="quarantined")
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="Dr. Elias Vance", record_id="rec-C", decision="reject"
        )
        with pytest.raises(write_gate.InvalidReviewerConfirmationError):
            write_gate.promote_quarantined_write(record, confirmation)
        assert record.status == "quarantined"

    def test_reject_rejects_confirmation_with_wrong_decision(self):
        record = _make_record(record_id="rec-D", status="quarantined")
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="Dr. Elias Vance", record_id="rec-D", decision="promote"
        )
        with pytest.raises(write_gate.InvalidReviewerConfirmationError):
            write_gate.reject_quarantined_write(record, confirmation)
        assert record.status == "quarantined"

    def test_confirmation_requires_non_empty_reviewer(self):
        record = _make_record(record_id="rec-E", status="quarantined")
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="", record_id="rec-E", decision="promote"
        )
        with pytest.raises(write_gate.InvalidReviewerConfirmationError):
            write_gate.promote_quarantined_write(record, confirmation)

    def test_promote_refuses_record_not_in_quarantined_status(self):
        record = _make_record(record_id="rec-F", status="active")
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="Dr. Elias Vance", record_id="rec-F", decision="promote"
        )
        with pytest.raises(write_gate.InvalidReviewerConfirmationError):
            write_gate.promote_quarantined_write(record, confirmation)

    def test_reject_refuses_record_not_in_quarantined_status(self):
        record = _make_record(record_id="rec-G", status="archived")
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="Dr. Elias Vance", record_id="rec-G", decision="reject"
        )
        with pytest.raises(write_gate.InvalidReviewerConfirmationError):
            write_gate.reject_quarantined_write(record, confirmation)

    def test_reviewer_confirmation_is_frozen(self):
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="Dr. Elias Vance", record_id="rec-H", decision="promote"
        )
        with pytest.raises(Exception):
            confirmation.decision = "reject"  # type: ignore[misc]

    def test_reviewer_confirmation_carries_timestamp(self):
        before = time.time()
        confirmation = write_gate.ReviewerConfirmation(
            reviewer="Dr. Elias Vance", record_id="rec-I", decision="promote"
        )
        after = time.time()
        assert before <= confirmation.confirmed_at <= after
