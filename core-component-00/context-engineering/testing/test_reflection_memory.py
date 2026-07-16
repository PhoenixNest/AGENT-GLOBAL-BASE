"""
Executable pytest suite for the fourth memory type — ReflectionRecord /
ReflectionMemory (implementations/memory_store.py) and its JSONL/Qdrant
write-through wiring (implementations/memory_vector_store.py).

Programme: core-component-00/telescope/2026-07-14-reflexion-memory-system
Phase: 1 — see supporting/03-deployment-guidelines.md

Run with:
    pytest testing/test_reflection_memory.py -v
"""

import os
import sys
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from implementations.memory_store import (
    GOVERNANCE_TRIGGERS,
    TRIGGER_TYPES,
    IdentityVerification,
    ReflectionMemory,
    ReflectionRecord,
    UnverifiedReflectionError,
)
from implementations.memory_vector_store import (
    COLLECTION_BY_TYPE,
    EMBEDDING_DIM,
    JSONLMemoryLog,
    PersistentMemorySink,
    QdrantMemoryIndex,
)


def _embedder(text: str):
    base = ord(text[0]) / 1000 if text else 0.0
    return [round(base + i * 0.001, 6) for i in range(EMBEDDING_DIM)]


def _identity(logged_by: str, governance_confirmation=None) -> IdentityVerification:
    """A valid IdentityVerification for test purposes — this file tests
    ReflectionMemory/ReflectionRecord in isolation from
    reflection_authoring.py's actual git-identity check (that check has its
    own dedicated test file, test_reflection_authoring.py), so tests here
    construct the token directly rather than going through
    verify_authorized_identity()/require_governance_confirmation(). Pass
    governance_confirmation=<reflection_id> when recording a
    GOVERNANCE_TRIGGERS-type record."""
    return IdentityVerification(
        logged_by=logged_by,
        git_identity=("Test", "test@example.com"),
        governance_confirmation=governance_confirmation,
    )


def _make_reflection(**overrides):
    defaults = dict(
        reflection_id="REFLECT-001",
        trigger_type="process_violation",
        source_event_ref="core-component-00/telescope/x/supporting/mistake-log.md#MISTAKE-001",
        summary="A progress-tracking-file requirement was violated across a full build.",
        root_cause="No future orchestrator brief was required to consult the correction.",
        remediation="Wire a proactive retrieval hook at brief-issuance time.",
        scope_of_applicability="Any future git-worktree-orchestration brief.",
        logged_by="Mei-Ling Zhao",
    )
    defaults.update(overrides)
    return ReflectionRecord(**defaults)


# ---------------------------------------------------------------------------
# Trigger-type validation
# ---------------------------------------------------------------------------

class TestTriggerTypeValidation:
    def test_all_five_trigger_types_are_defined(self):
        assert TRIGGER_TYPES == {
            "process_violation",
            "defect_root_cause",
            "ase_exception_closure",
            "adversarial_finding",
            "director_flagged",
        }

    @pytest.mark.parametrize("trigger_type", sorted(TRIGGER_TYPES))
    def test_valid_trigger_type_constructs_record(self, trigger_type):
        record = _make_reflection(trigger_type=trigger_type)
        assert record.trigger_type == trigger_type

    def test_invalid_trigger_type_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown trigger_type"):
            _make_reflection(trigger_type="not_a_real_trigger")

    def test_empty_trigger_type_raises(self):
        with pytest.raises(ValueError):
            _make_reflection(trigger_type="")

    def test_missing_logged_by_raises_value_error(self):
        with pytest.raises(ValueError, match="logged_by"):
            _make_reflection(logged_by="")


# ---------------------------------------------------------------------------
# Sacred-default behavior for GOVERNANCE_TRIGGERS
# ---------------------------------------------------------------------------

class TestSacredDefaultForGovernanceTriggers:
    def test_governance_triggers_set_is_the_documented_three(self):
        assert GOVERNANCE_TRIGGERS == {
            "process_violation",
            "defect_root_cause",
            "ase_exception_closure",
        }
        assert GOVERNANCE_TRIGGERS.issubset(TRIGGER_TYPES)

    @pytest.mark.parametrize("trigger_type", sorted(GOVERNANCE_TRIGGERS))
    def test_governance_trigger_defaults_sacred_true(self, trigger_type):
        record = _make_reflection(trigger_type=trigger_type)
        assert record.sacred is True

    @pytest.mark.parametrize("trigger_type", sorted(GOVERNANCE_TRIGGERS))
    def test_governance_trigger_forces_sacred_true_even_if_caller_passes_false(self, trigger_type):
        # __post_init__ cannot distinguish "explicitly False" from "default
        # False" on a bool field — governance triggers are always sacred,
        # by design (02-storage-specification.md §2.3).
        record = _make_reflection(trigger_type=trigger_type, sacred=False)
        assert record.sacred is True

    @pytest.mark.parametrize("trigger_type", sorted(TRIGGER_TYPES - GOVERNANCE_TRIGGERS))
    def test_non_governance_trigger_defaults_sacred_false(self, trigger_type):
        record = _make_reflection(trigger_type=trigger_type)
        assert record.sacred is False

    @pytest.mark.parametrize("trigger_type", sorted(TRIGGER_TYPES - GOVERNANCE_TRIGGERS))
    def test_non_governance_trigger_can_be_explicitly_marked_sacred(self, trigger_type):
        record = _make_reflection(trigger_type=trigger_type, sacred=True)
        assert record.sacred is True


# ---------------------------------------------------------------------------
# ReflectionRecord serialisation (to_dict / from_dict)
# ---------------------------------------------------------------------------

class TestReflectionRecordSerialisation:
    def test_to_dict_from_dict_roundtrip_preserves_fields(self):
        record = _make_reflection(
            severity="P1",
            migrated_from="mistake-log.md#MISTAKE-001",
        )
        restored = ReflectionRecord.from_dict(record.to_dict())
        assert restored.reflection_id == record.reflection_id
        assert restored.trigger_type == record.trigger_type
        assert restored.summary == record.summary
        assert restored.root_cause == record.root_cause
        assert restored.remediation == record.remediation
        assert restored.scope_of_applicability == record.scope_of_applicability
        assert restored.severity == "P1"
        assert restored.logged_by == record.logged_by
        assert restored.sacred == record.sacred
        assert restored.status == record.status
        assert restored.migrated_from == "mistake-log.md#MISTAKE-001"

    def test_from_dict_missing_optional_fields_uses_defaults(self):
        minimal = {
            "reflection_id": "REFLECT-002",
            "trigger_type": "director_flagged",
            "source_event_ref": "ref",
            "summary": "summary text",
            "root_cause": "cause",
            "remediation": "fix",
            "scope_of_applicability": "scope",
            "logged_by": "Dr. Elias Vance",
        }
        restored = ReflectionRecord.from_dict(minimal)
        assert restored.severity is None
        assert restored.sacred is False
        assert restored.status == "active"
        assert restored.migrated_from is None

    def test_from_dict_reruns_post_init_validation(self):
        bad = _make_reflection().to_dict()
        bad["trigger_type"] = "not_real"
        with pytest.raises(ValueError):
            ReflectionRecord.from_dict(bad)


# ---------------------------------------------------------------------------
# ReflectionMemory — record / get / query
# ---------------------------------------------------------------------------

class TestReflectionMemory:
    def test_record_reflection_stores_and_is_retrievable(self):
        rm = ReflectionMemory()
        rm.record_reflection(
            reflection_id="REFLECT-001",
            trigger_type="process_violation",
            source_event_ref="ref#MISTAKE-001",
            summary="git worktree orchestration correction was never enforced",
            root_cause="no brief consulted the correction",
            remediation="add a proactive retrieval hook",
            scope_of_applicability="git worktree orchestration briefs",
            logged_by="Mei-Ling Zhao",
            identity=_identity("Mei-Ling Zhao", governance_confirmation="REFLECT-001"),
        )
        assert len(rm) == 1
        assert rm.get("REFLECT-001") is not None
        assert rm.get("REFLECT-001").summary.startswith("git worktree")

    def test_get_missing_id_returns_none(self):
        rm = ReflectionMemory()
        assert rm.get("REFLECT-999") is None

    def test_query_matches_on_summary_and_scope_keywords(self):
        rm = ReflectionMemory()
        rm.record_reflection(
            reflection_id="REFLECT-001",
            trigger_type="process_violation",
            source_event_ref="ref",
            summary="git worktree orchestration correction was never enforced",
            root_cause="cause",
            remediation="fix",
            scope_of_applicability="future git worktree orchestration briefs",
            logged_by="Mei-Ling Zhao",
            identity=_identity("Mei-Ling Zhao", governance_confirmation="REFLECT-001"),
        )
        rm.record_reflection(
            reflection_id="REFLECT-002",
            trigger_type="director_flagged",
            source_event_ref="ref2",
            summary="unrelated embedder cold-cache latency finding",
            root_cause="cause2",
            remediation="fix2",
            scope_of_applicability="embedder provisioning steps",
            logged_by="Dr. Elias Vance",
            identity=_identity("Dr. Elias Vance"),
        )
        results = rm.query("git worktree orchestration", top_k=5)
        assert len(results) >= 1
        assert results[0]["reflection_id"] == "REFLECT-001"

    def test_query_respects_top_k(self):
        rm = ReflectionMemory()
        for i in range(5):
            rm.record_reflection(
                reflection_id=f"REFLECT-{i:03d}",
                trigger_type="director_flagged",
                source_event_ref="ref",
                summary=f"finding about topic number {i}",
                root_cause="cause",
                remediation="fix",
                scope_of_applicability=f"topic {i} related tasks",
                logged_by="Dr. Elias Vance",
                identity=_identity("Dr. Elias Vance"),
            )
        results = rm.query("topic finding", top_k=2)
        assert len(results) <= 2

    def test_get_sacred_reflections_returns_only_sacred(self):
        rm = ReflectionMemory()
        rm.record_reflection(
            reflection_id="REFLECT-SACRED",
            trigger_type="defect_root_cause",
            source_event_ref="ref",
            summary="root cause of a P1",
            root_cause="cause",
            remediation="fix",
            scope_of_applicability="scope",
            logged_by="Kwame Asante",
            identity=_identity("Kwame Asante", governance_confirmation="REFLECT-SACRED"),
            severity="P1",
        )
        rm.record_reflection(
            reflection_id="REFLECT-NONSACRED",
            trigger_type="adversarial_finding",
            source_event_ref="ref",
            summary="a narrowly-scoped tactical finding",
            root_cause="cause",
            remediation="fix",
            scope_of_applicability="scope",
            logged_by="Dr. Tomasz Wieczorek",
            identity=_identity("Dr. Tomasz Wieczorek"),
        )
        sacred = rm.get_sacred_reflections()
        assert len(sacred) == 1
        assert sacred[0].reflection_id == "REFLECT-SACRED"


# ---------------------------------------------------------------------------
# ReflectionMemory.record_reflection()'s IdentityVerification gate —
# closes the direct-import bypass documented in mistake-log.md
# (MISTAKE-2026-07-16-001): a caller importing memory_store.py directly,
# bypassing reflection_authoring.py entirely, must still supply a genuine
# IdentityVerification token issued for the exact logged_by being recorded.
# ---------------------------------------------------------------------------

class TestRecordReflectionIdentityGate:
    def test_missing_identity_raises_unverified_reflection_error(self):
        rm = ReflectionMemory()
        with pytest.raises(UnverifiedReflectionError, match="verified IdentityVerification"):
            rm.record_reflection(
                reflection_id="REFLECT-001",
                trigger_type="director_flagged",
                source_event_ref="ref",
                summary="s",
                root_cause="c",
                remediation="r",
                scope_of_applicability="a",
                logged_by="Mei-Ling Zhao",
                identity=None,  # the direct-import bypass this gate closes
            )

    def test_wrong_type_for_identity_raises_unverified_reflection_error(self):
        rm = ReflectionMemory()
        with pytest.raises(UnverifiedReflectionError):
            rm.record_reflection(
                reflection_id="REFLECT-001",
                trigger_type="director_flagged",
                source_event_ref="ref",
                summary="s",
                root_cause="c",
                remediation="r",
                scope_of_applicability="a",
                logged_by="Mei-Ling Zhao",
                identity="Mei-Ling Zhao",  # a bare string is not a token
            )

    def test_mismatched_logged_by_raises_unverified_reflection_error(self):
        rm = ReflectionMemory()
        with pytest.raises(UnverifiedReflectionError, match="mismatched identity"):
            rm.record_reflection(
                reflection_id="REFLECT-001",
                trigger_type="director_flagged",
                source_event_ref="ref",
                summary="s",
                root_cause="c",
                remediation="r",
                scope_of_applicability="a",
                logged_by="Mei-Ling Zhao",
                identity=_identity("Someone Else"),  # verified for a different investigator
            )
        assert len(rm) == 0  # nothing was persisted

    def test_matching_identity_succeeds(self):
        rm = ReflectionMemory()
        record = rm.record_reflection(
            reflection_id="REFLECT-001",
            trigger_type="director_flagged",
            source_event_ref="ref",
            summary="s",
            root_cause="c",
            remediation="r",
            scope_of_applicability="a",
            logged_by="Mei-Ling Zhao",
            identity=_identity("Mei-Ling Zhao"),
        )
        assert record is not None
        assert len(rm) == 1

    def test_unverified_reflection_error_is_a_value_error(self):
        # Subclassing ValueError means existing `except ValueError` handling
        # around ReflectionRecord construction still catches this.
        rm = ReflectionMemory()
        with pytest.raises(ValueError):
            rm.record_reflection(
                reflection_id="REFLECT-001",
                trigger_type="director_flagged",
                source_event_ref="ref",
                summary="s",
                root_cause="c",
                remediation="r",
                scope_of_applicability="a",
                logged_by="Mei-Ling Zhao",
                identity=None,
            )


# ---------------------------------------------------------------------------
# The governance_confirmation composition-gap fix (MISTAKE-2026-07-16-001's
# 2026-07-16 Update, remediation item 1): a GOVERNANCE_TRIGGERS record
# requires the IdentityVerification's governance_confirmation to match the
# exact reflection_id — a plain, hand-fabricated IdentityVerification with
# correct logged_by/git_identity but no (or a mismatched) governance_
# confirmation is rejected, closing the "silently skip the confirmation
# step entirely" gap Wieczorek's second pass found. Honest framing per the
# coordinator: this raises the bar for the composition gap, it does not
# make the token unforgeable — a caller who reads the source can still set
# governance_confirmation correctly by hand without ever having gone
# through a real TTY prompt. These tests verify the composition check
# exists and works, not that it closes that broader limitation.
# ---------------------------------------------------------------------------

class TestGovernanceConfirmationComposition:
    def test_governance_trigger_without_governance_confirmation_is_rejected(self):
        rm = ReflectionMemory()
        # Correct logged_by/git_identity, but governance_confirmation was
        # never set — exactly what a caller gets from
        # verify_authorized_identity() alone, without also calling
        # require_governance_confirmation().
        with pytest.raises(UnverifiedReflectionError, match="governance_confirmation"):
            rm.record_reflection(
                reflection_id="REFLECT-001",
                trigger_type="process_violation",
                source_event_ref="ref",
                summary="s",
                root_cause="c",
                remediation="r",
                scope_of_applicability="a",
                logged_by="Mei-Ling Zhao",
                identity=_identity("Mei-Ling Zhao"),  # governance_confirmation=None
            )
        assert len(rm) == 0

    def test_governance_trigger_with_mismatched_governance_confirmation_is_rejected(self):
        rm = ReflectionMemory()
        with pytest.raises(UnverifiedReflectionError, match="governance_confirmation"):
            rm.record_reflection(
                reflection_id="REFLECT-001",
                trigger_type="process_violation",
                source_event_ref="ref",
                summary="s",
                root_cause="c",
                remediation="r",
                scope_of_applicability="a",
                logged_by="Mei-Ling Zhao",
                # confirmed for a *different* reflection_id — e.g. reused
                # from a prior authoring call.
                identity=_identity("Mei-Ling Zhao", governance_confirmation="REFLECT-OTHER"),
            )

    @pytest.mark.parametrize("trigger_type", sorted(GOVERNANCE_TRIGGERS))
    def test_all_governance_trigger_types_require_matching_confirmation(self, trigger_type):
        rm = ReflectionMemory()
        with pytest.raises(UnverifiedReflectionError):
            rm.record_reflection(
                reflection_id="REFLECT-001",
                trigger_type=trigger_type,
                source_event_ref="ref",
                summary="s",
                root_cause="c",
                remediation="r",
                scope_of_applicability="a",
                logged_by="Mei-Ling Zhao",
                identity=_identity("Mei-Ling Zhao"),
            )

    def test_non_governance_trigger_does_not_require_governance_confirmation(self):
        rm = ReflectionMemory()
        # director_flagged is not in GOVERNANCE_TRIGGERS — must succeed with
        # a plain identity carrying no governance_confirmation at all.
        record = rm.record_reflection(
            reflection_id="REFLECT-001",
            trigger_type="director_flagged",
            source_event_ref="ref",
            summary="s",
            root_cause="c",
            remediation="r",
            scope_of_applicability="a",
            logged_by="Mei-Ling Zhao",
            identity=_identity("Mei-Ling Zhao"),
        )
        assert record is not None

    def test_governance_trigger_with_matching_confirmation_succeeds(self):
        rm = ReflectionMemory()
        record = rm.record_reflection(
            reflection_id="REFLECT-001",
            trigger_type="process_violation",
            source_event_ref="ref",
            summary="s",
            root_cause="c",
            remediation="r",
            scope_of_applicability="a",
            logged_by="Mei-Ling Zhao",
            identity=_identity("Mei-Ling Zhao", governance_confirmation="REFLECT-001"),
        )
        assert record is not None
        assert record.sacred is True


# ---------------------------------------------------------------------------
# ReflectionMemory sink write-through (mirrors test_memory_store.py's
# _RecordingSink pattern)
# ---------------------------------------------------------------------------

class _RecordingSink:
    def __init__(self, fail=False):
        self.fail = fail
        self.reflection_calls = []

    def write_reflection(self, record, identity):
        if self.fail:
            raise RuntimeError("simulated sink failure")
        self.reflection_calls.append((record, identity))


class TestReflectionMemorySinkWriteThrough:
    def test_no_sink_preserves_default_behaviour(self):
        rm = ReflectionMemory()
        rm.record_reflection(
            reflection_id="REFLECT-001",
            trigger_type="director_flagged",
            source_event_ref="ref",
            summary="s",
            root_cause="c",
            remediation="r",
            scope_of_applicability="a",
            logged_by="Dr. Elias Vance",
            identity=_identity("Dr. Elias Vance"),
        )
        assert len(rm) == 1

    def test_record_reflection_calls_sink(self):
        sink = _RecordingSink()
        rm = ReflectionMemory(sink=sink)
        rm.record_reflection(
            reflection_id="REFLECT-001",
            trigger_type="director_flagged",
            source_event_ref="ref",
            summary="s",
            root_cause="c",
            remediation="r",
            scope_of_applicability="a",
            logged_by="Dr. Elias Vance",
            identity=_identity("Dr. Elias Vance"),
        )
        assert len(sink.reflection_calls) == 1
        assert sink.reflection_calls[0][0].reflection_id == "REFLECT-001"
        assert sink.reflection_calls[0][1].logged_by == "Dr. Elias Vance"

    def test_sink_failure_does_not_break_the_write(self):
        sink = _RecordingSink(fail=True)
        rm = ReflectionMemory(sink=sink)
        record = rm.record_reflection(
            reflection_id="REFLECT-001",
            trigger_type="director_flagged",
            source_event_ref="ref",
            summary="s",
            root_cause="c",
            remediation="r",
            scope_of_applicability="a",
            logged_by="Dr. Elias Vance",
            identity=_identity("Dr. Elias Vance"),
        )
        assert record is not None
        assert len(rm) == 1


# ---------------------------------------------------------------------------
# JSONLMemoryLog — reflection log round trip
# ---------------------------------------------------------------------------

class TestJSONLReflectionRoundTrip:
    def test_append_and_read_reflection(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        record = _make_reflection()
        log.append_reflection(record)
        payloads = log.read_all_reflections()
        assert len(payloads) == 1
        restored = ReflectionRecord.from_dict(payloads[0])
        assert restored.reflection_id == record.reflection_id
        assert restored.summary == record.summary
        assert restored.sacred == record.sacred

    def test_read_all_reflections_on_missing_file_returns_empty(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        assert log.read_all_reflections() == []

    def test_reflection_log_is_a_single_cross_session_file(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        log.append_reflection(_make_reflection(reflection_id="REFLECT-001"))
        log.append_reflection(_make_reflection(reflection_id="REFLECT-002"))
        reflection_dir = tmp_path / "reflection"
        files = list(reflection_dir.glob("*.jsonl"))
        assert len(files) == 1
        assert files[0].name == "reflection-log.jsonl"
        payloads = log.read_all_reflections()
        assert len(payloads) == 2

    def test_reflection_directory_created_on_init(self, tmp_path):
        JSONLMemoryLog(root_dir=tmp_path)
        assert (tmp_path / "reflection").is_dir()


# ---------------------------------------------------------------------------
# Collection registry — memory_reflection alongside the other three
# ---------------------------------------------------------------------------

class TestReflectionCollectionRegistry:
    def test_reflection_maps_to_memory_reflection_collection(self):
        assert COLLECTION_BY_TYPE["reflection"] == "memory_reflection"

    def test_reflection_collection_included_in_memory_collections(self):
        from implementations.memory_vector_store import MEMORY_COLLECTIONS

        assert "memory_reflection" in MEMORY_COLLECTIONS

    def test_qdrant_memory_index_accepts_reflection_type(self):
        index = QdrantMemoryIndex("reflection", client=None, embedder=_embedder)
        assert index.collection_name == "memory_reflection"


# ---------------------------------------------------------------------------
# PersistentMemorySink.write_reflection
# ---------------------------------------------------------------------------

class TestPersistentMemorySinkWriteReflection:
    def test_write_reflection_appends_to_jsonl(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        record = _make_reflection()  # default trigger_type is process_violation (governance)
        result = sink.write_reflection(
            record, _identity(record.logged_by, governance_confirmation=record.reflection_id)
        )
        assert result.reflection_id == record.reflection_id
        stored = log.read_all_reflections()
        assert len(stored) == 1
        assert stored[0]["summary"] == record.summary

    def test_write_reflection_upserts_to_matching_index(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        client = MagicMock()
        index = QdrantMemoryIndex("reflection", client=client, embedder=_embedder)
        sink = PersistentMemorySink(log=log, indices={"reflection": index})
        record = _make_reflection()
        sink.write_reflection(
            record, _identity(record.logged_by, governance_confirmation=record.reflection_id)
        )
        client.upsert.assert_called_once()
        _, kwargs = client.upsert.call_args
        assert kwargs["collection_name"] == "memory_reflection"

    def test_write_reflection_payload_contains_full_record_verbatim(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        client = MagicMock()
        index = QdrantMemoryIndex("reflection", client=client, embedder=_embedder)
        sink = PersistentMemorySink(log=log, indices={"reflection": index})
        record = _make_reflection(severity="P0")
        sink.write_reflection(
            record, _identity(record.logged_by, governance_confirmation=record.reflection_id)
        )
        _, kwargs = client.upsert.call_args
        point = kwargs["points"][0]
        assert point.payload["reflection_id"] == record.reflection_id
        assert point.payload["root_cause"] == record.root_cause
        assert point.payload["remediation"] == record.remediation
        assert point.payload["severity"] == "P0"

    def test_write_reflection_survives_missing_index(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log, indices={})
        record = _make_reflection()
        result = sink.write_reflection(
            record, _identity(record.logged_by, governance_confirmation=record.reflection_id)
        )  # must not raise
        assert result is not None

    def test_write_reflection_survives_qdrant_upsert_failure(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        client = MagicMock()
        client.upsert.side_effect = RuntimeError("qdrant-memory unreachable")
        index = QdrantMemoryIndex("reflection", client=client, embedder=_embedder)
        sink = PersistentMemorySink(log=log, indices={"reflection": index})
        record = _make_reflection()
        result = sink.write_reflection(
            record, _identity(record.logged_by, governance_confirmation=record.reflection_id)
        )  # must not raise
        assert result is not None
        assert len(log.read_all_reflections()) == 1


# ---------------------------------------------------------------------------
# PersistentMemorySink.write_reflection()'s IdentityVerification gate —
# closes the second live bypass Dr. Wieczorek's second pass found: a caller
# constructing a bare ReflectionRecord and calling this method directly,
# skipping ReflectionMemory (and therefore record_reflection()'s own gate)
# entirely. Honest framing: this is defense-in-depth, not a floor —
# JSONLMemoryLog.append_reflection() and QdrantMemoryIndex.upsert_payload()
# remain directly callable beneath this method with no check at all.
# ---------------------------------------------------------------------------

class TestWriteReflectionIdentityGate:
    def test_missing_identity_raises_unverified_reflection_error(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        record = _make_reflection(trigger_type="director_flagged")
        with pytest.raises(UnverifiedReflectionError, match="verified IdentityVerification"):
            sink.write_reflection(record, None)
        assert log.read_all_reflections() == []  # nothing was persisted

    def test_wrong_type_for_identity_raises_unverified_reflection_error(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        record = _make_reflection(trigger_type="director_flagged")
        with pytest.raises(UnverifiedReflectionError):
            sink.write_reflection(record, "Mei-Ling Zhao")  # a bare string is not a token

    def test_mismatched_logged_by_raises_unverified_reflection_error(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        record = _make_reflection(trigger_type="director_flagged", logged_by="Mei-Ling Zhao")
        with pytest.raises(UnverifiedReflectionError, match="mismatched identity"):
            sink.write_reflection(record, _identity("Someone Else"))
        assert log.read_all_reflections() == []

    def test_governance_record_without_confirmation_raises(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        record = _make_reflection()  # default trigger_type is process_violation (governance)
        with pytest.raises(UnverifiedReflectionError, match="governance_confirmation"):
            sink.write_reflection(record, _identity(record.logged_by))  # no confirmation attached
        assert log.read_all_reflections() == []

    def test_direct_bare_record_bypass_is_rejected(self, tmp_path):
        """The literal scenario Dr. Wieczorek's second pass demonstrated:
        construct a ReflectionRecord directly (never through
        ReflectionMemory.record_reflection()) and call the sink directly."""
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        bare_record = ReflectionRecord(
            reflection_id="REFLECT-BYPASS",
            trigger_type="process_violation",
            source_event_ref="ref",
            summary="s",
            root_cause="c",
            remediation="r",
            scope_of_applicability="a",
            logged_by="Mei-Ling Zhao",
        )
        with pytest.raises(UnverifiedReflectionError):
            sink.write_reflection(bare_record, None)
        assert log.read_all_reflections() == []

    def test_matching_identity_and_confirmation_succeeds(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        record = _make_reflection()
        result = sink.write_reflection(
            record, _identity(record.logged_by, governance_confirmation=record.reflection_id)
        )
        assert result is not None
        assert len(log.read_all_reflections()) == 1


# ---------------------------------------------------------------------------
# upsert_record / upsert_payload refactor — regression coverage for the
# existing three memory types (episodic/semantic/procedural must be
# unaffected by the reflection-driven refactor of QdrantMemoryIndex)
# ---------------------------------------------------------------------------

class TestUpsertRecordRegression:
    def test_upsert_record_still_calls_client_upsert_with_correct_collection(self):
        from implementations.memory_vector_store import MemoryRecord
        import time

        client = MagicMock()
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        now = time.time()
        record = MemoryRecord(
            id="rec-1",
            memory_type="semantic",
            content="test content",
            created_at=now,
            last_accessed_at=now,
        )
        result = index.upsert_record(record)
        assert result is True
        client.upsert.assert_called_once()
        _, kwargs = client.upsert.call_args
        assert kwargs["collection_name"] == "memory_semantic"

    def test_upsert_payload_without_client_degrades_gracefully(self):
        index = QdrantMemoryIndex("reflection", client=None, embedder=_embedder)
        assert index.upsert_payload("id-1", "text", {"a": 1}) is False
