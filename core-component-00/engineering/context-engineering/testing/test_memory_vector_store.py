"""
Executable pytest suite for the Qdrant/JSONL memory persistence layer
(implementations/memory_vector_store.py).

Run with:
    pytest testing/test_memory_vector_store.py -v
"""

import os
import sys
import time
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from implementations.memory_store import EpisodicEvent, SemanticFact
from implementations.memory_vector_store import (
    COLLECTION_BY_TYPE,
    EMBEDDING_DIM,
    JSONLMemoryLog,
    MemoryRecord,
    MemorySyncState,
    PersistentMemorySink,
    QdrantMemoryIndex,
    check_reachable,
    compute_dormant_ratio,
    compute_memory_instance_telemetry,
    compute_write_time_importance,
)


def _make_record(memory_type="semantic", **overrides):
    now = time.time()
    defaults = dict(
        id="rec-1",
        memory_type=memory_type,
        content="test content",
        created_at=now,
        last_accessed_at=now,
        access_count=0,
        importance=0.5,
        confidence=1.0,
        decay_weight=1.0,
        status="active",
        source_session_id="session-a" if memory_type == "episodic" else None,
        source_turn=0,
        sacred=False,
        tags=[],
        consolidated_from=[],
        modality="text",
        media_ref=None,
    )
    defaults.update(overrides)
    return MemoryRecord(**defaults)


def _embedder(text: str):
    base = ord(text[0]) / 1000 if text else 0.0
    return [round(base + i * 0.001, 6) for i in range(EMBEDDING_DIM)]


# ---------------------------------------------------------------------------
# Write-time importance heuristic
# ---------------------------------------------------------------------------

class TestWriteTimeImportance:
    def test_decision_is_maximal(self):
        assert compute_write_time_importance("decision") == 1.0

    def test_commitment_is_maximal(self):
        assert compute_write_time_importance("commitment") == 1.0

    def test_correction_is_elevated(self):
        assert compute_write_time_importance("correction") == 0.7

    def test_unknown_event_type_uses_default(self):
        assert compute_write_time_importance("something_unrecognised") == 0.2


# ---------------------------------------------------------------------------
# MemoryRecord serialisation
# ---------------------------------------------------------------------------

class TestMemoryRecordSerialisation:
    def test_payload_roundtrip_preserves_fields(self):
        record = _make_record(
            memory_type="semantic",
            tags=["a", "b"],
            consolidated_from=["ep-1", "ep-2"],
            sacred=True,
        )
        payload = record.to_payload()
        restored = MemoryRecord.from_payload(payload)
        assert restored.id == record.id
        assert restored.content == record.content
        assert restored.tags == ["a", "b"]
        assert restored.consolidated_from == ["ep-1", "ep-2"]
        assert restored.sacred is True

    def test_jsonl_roundtrip(self):
        record = _make_record()
        line = record.to_jsonl_line()
        restored = MemoryRecord.from_jsonl_line(line)
        assert restored.id == record.id
        assert restored.content == record.content

    def test_timestamps_survive_roundtrip_to_the_second(self):
        record = _make_record()
        restored = MemoryRecord.from_payload(record.to_payload())
        assert abs(restored.created_at - record.created_at) < 1.0


# ---------------------------------------------------------------------------
# JSONLMemoryLog
# ---------------------------------------------------------------------------

class TestJSONLMemoryLog:
    def test_append_and_read_semantic(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        record = _make_record(memory_type="semantic")
        log.append(record)
        results = log.read_all("semantic")
        assert len(results) == 1
        assert results[0].content == "test content"

    def test_append_and_read_procedural(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        record = _make_record(memory_type="procedural")
        log.append(record)
        results = log.read_all("procedural")
        assert len(results) == 1

    def test_episodic_requires_session_id(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        record = _make_record(memory_type="episodic", source_session_id=None)
        with pytest.raises(ValueError):
            log.append(record)

    def test_episodic_writes_per_session_file(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        r1 = _make_record(memory_type="episodic", source_session_id="session-a")
        r2 = _make_record(memory_type="episodic", source_session_id="session-b")
        log.append(r1)
        log.append(r2)
        assert (tmp_path / "episodic" / "session-a.jsonl").exists()
        assert (tmp_path / "episodic" / "session-b.jsonl").exists()

    def test_read_all_episodic_sessions_merges_all_files(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        log.append(_make_record(memory_type="episodic", source_session_id="session-a"))
        log.append(_make_record(memory_type="episodic", source_session_id="session-b"))
        all_records = log.read_all_episodic_sessions()
        assert len(all_records) == 2

    def test_episodic_sessions_by_id_groups_correctly(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        log.append(_make_record(memory_type="episodic", source_session_id="session-a", id="r1"))
        log.append(_make_record(memory_type="episodic", source_session_id="session-a", id="r2"))
        log.append(_make_record(memory_type="episodic", source_session_id="session-b", id="r3"))
        grouped = log.episodic_sessions_by_id()
        assert len(grouped["session-a"]) == 2
        assert len(grouped["session-b"]) == 1

    def test_read_all_on_missing_file_returns_empty_list(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        assert log.read_all("semantic") == []

    def test_unknown_memory_type_raises(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        record = _make_record(memory_type="working")
        with pytest.raises(ValueError):
            log.append(record)


# ---------------------------------------------------------------------------
# MemorySyncState
# ---------------------------------------------------------------------------

class TestMemorySyncState:
    def test_load_defaults_when_no_file_exists(self, tmp_path):
        state = MemorySyncState(root_dir=tmp_path)
        loaded = state.load()
        assert loaded["memory_semantic"]["point_count"] == 0

    def test_load_defaults_last_consolidation_at_to_none(self, tmp_path):
        state = MemorySyncState(root_dir=tmp_path)
        assert state.load()["last_consolidation_at"] is None

    def test_record_rebuild_persists_point_count(self, tmp_path):
        state = MemorySyncState(root_dir=tmp_path)
        state.record_rebuild("memory_semantic", point_count=42, now=1234.0)
        loaded = state.load()
        assert loaded["memory_semantic"]["point_count"] == 42
        assert loaded["memory_semantic"]["last_rebuild_at"] == 1234.0

    def test_record_consolidation_persists_timestamp(self, tmp_path):
        state = MemorySyncState(root_dir=tmp_path)
        state.record_consolidation(now=5678.0)
        assert state.get_last_consolidation_at() == 5678.0

    def test_get_last_consolidation_at_defaults_to_none(self, tmp_path):
        state = MemorySyncState(root_dir=tmp_path)
        assert state.get_last_consolidation_at() is None

    def test_record_consolidation_does_not_disturb_collection_state(self, tmp_path):
        state = MemorySyncState(root_dir=tmp_path)
        state.record_rebuild("memory_semantic", point_count=10, now=1.0)
        state.record_consolidation(now=2.0)
        loaded = state.load()
        assert loaded["memory_semantic"]["point_count"] == 10
        assert loaded["last_consolidation_at"] == 2.0


# ---------------------------------------------------------------------------
# QdrantMemoryIndex (mocked client — no live Qdrant instance required)
# ---------------------------------------------------------------------------

class TestQdrantMemoryIndex:
    def test_unknown_memory_type_raises(self):
        with pytest.raises(ValueError):
            QdrantMemoryIndex("working")

    def test_upsert_without_client_degrades_gracefully(self):
        index = QdrantMemoryIndex("semantic", client=None, embedder=_embedder)
        assert index.upsert_record(_make_record()) is False

    def test_upsert_without_embedder_degrades_gracefully(self):
        index = QdrantMemoryIndex("semantic", client=MagicMock(), embedder=None)
        assert index.upsert_record(_make_record()) is False

    def test_search_without_client_returns_empty(self):
        index = QdrantMemoryIndex("semantic", client=None, embedder=_embedder)
        assert index.search("query") == []

    def test_ensure_collection_creates_when_missing(self):
        client = MagicMock()
        client.get_collections.return_value = MagicMock(collections=[])
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        index.ensure_collection()
        client.create_collection.assert_called_once()
        _, kwargs = client.create_collection.call_args
        assert kwargs["collection_name"] == COLLECTION_BY_TYPE["semantic"]

    def test_ensure_collection_skips_when_already_exists(self):
        client = MagicMock()
        existing = MagicMock()
        existing.name = COLLECTION_BY_TYPE["semantic"]
        client.get_collections.return_value = MagicMock(collections=[existing])
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        index.ensure_collection()
        client.create_collection.assert_not_called()

    def test_ensure_collection_failure_does_not_raise(self):
        client = MagicMock()
        client.get_collections.side_effect = RuntimeError("connection refused")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        index.ensure_collection()  # must not raise

    def test_upsert_record_calls_client_upsert(self):
        client = MagicMock()
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        result = index.upsert_record(_make_record())
        assert result is True
        client.upsert.assert_called_once()
        _, kwargs = client.upsert.call_args
        assert kwargs["collection_name"] == COLLECTION_BY_TYPE["semantic"]

    def test_upsert_record_failure_degrades_gracefully(self):
        client = MagicMock()
        client.upsert.side_effect = RuntimeError("network error")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.upsert_record(_make_record()) is False

    def test_rebuild_from_log_replays_and_counts(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        log.append(_make_record(memory_type="semantic", id="r1"))
        log.append(_make_record(memory_type="semantic", id="r2"))
        client = MagicMock()
        client.get_collections.return_value = MagicMock(collections=[])
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        sync_state = MemorySyncState(root_dir=tmp_path)
        count = index.rebuild_from_log(log, sync_state=sync_state)
        assert count == 2
        assert sync_state.load()["memory_semantic"]["point_count"] == 2

    def test_rebuild_from_log_replays_episodic_across_sessions(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        log.append(_make_record(memory_type="episodic", source_session_id="s1", id="r1"))
        log.append(_make_record(memory_type="episodic", source_session_id="s2", id="r2"))
        client = MagicMock()
        client.get_collections.return_value = MagicMock(collections=[])
        index = QdrantMemoryIndex("episodic", client=client, embedder=_embedder)
        count = index.rebuild_from_log(log)
        assert count == 2


# ---------------------------------------------------------------------------
# PersistentMemorySink — write-through orchestration
# ---------------------------------------------------------------------------

class TestPersistentMemorySink:
    def test_write_episodic_appends_to_jsonl(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        event = EpisodicEvent(event_type="general", content="did a thing", turn=1)
        record = sink.write_episodic(event, session_id="session-x")
        assert record.memory_type == "episodic"
        stored = log.read_all("episodic", "session-x")
        assert len(stored) == 1
        assert stored[0].content == "did a thing"

    def test_write_episodic_sacred_event_gets_max_importance(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        event = EpisodicEvent(event_type="decision", content="Use PostgreSQL", turn=1, sacred=True)
        record = sink.write_episodic(event, session_id="session-x")
        assert record.importance == 1.0
        assert record.sacred is True

    def test_write_semantic_appends_to_jsonl(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        fact = SemanticFact(key="user_stack", value="FastAPI, PostgreSQL")
        record = sink.write_semantic(fact)
        assert record.memory_type == "semantic"
        assert "FastAPI" in record.content
        stored = log.read_all("semantic")
        assert len(stored) == 1

    def test_write_procedural_appends_to_jsonl(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log)
        record = sink.write_procedural("code_review", "Check for security issues")
        assert record.memory_type == "procedural"
        stored = log.read_all("procedural")
        assert len(stored) == 1

    def test_write_also_upserts_to_matching_index(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        client = MagicMock()
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        sink = PersistentMemorySink(log=log, indices={"semantic": index})
        fact = SemanticFact(key="k", value="v")
        sink.write_semantic(fact)
        client.upsert.assert_called_once()

    def test_write_survives_missing_index_for_type(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        sink = PersistentMemorySink(log=log, indices={})  # no semantic index registered
        fact = SemanticFact(key="k", value="v")
        record = sink.write_semantic(fact)  # must not raise
        assert record is not None

    def test_write_survives_qdrant_upsert_failure(self, tmp_path):
        log = JSONLMemoryLog(root_dir=tmp_path)
        client = MagicMock()
        client.upsert.side_effect = RuntimeError("qdrant-memory unreachable")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        sink = PersistentMemorySink(log=log, indices={"semantic": index})
        fact = SemanticFact(key="k", value="v")
        record = sink.write_semantic(fact)  # must not raise — JSONL already durable
        assert record is not None
        assert len(log.read_all("semantic")) == 1


# ---------------------------------------------------------------------------
# QdrantMemoryIndex.count_points — health_check point_counts / dormant_ratio
# ---------------------------------------------------------------------------

class TestCountPoints:
    def test_without_client_returns_zero(self):
        index = QdrantMemoryIndex("semantic", client=None, embedder=_embedder)
        assert index.count_points() == 0

    def test_calls_client_count_with_collection_name(self):
        client = MagicMock()
        client.count.return_value = MagicMock(count=7)
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.count_points() == 7
        _, kwargs = client.count.call_args
        assert kwargs["collection_name"] == COLLECTION_BY_TYPE["semantic"]
        assert kwargs["count_filter"] is None

    def test_status_filter_builds_a_field_condition(self):
        client = MagicMock()
        client.count.return_value = MagicMock(count=3)
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        count = index.count_points(status="dormant")
        assert count == 3
        _, kwargs = client.count.call_args
        assert kwargs["count_filter"] is not None

    def test_failure_degrades_to_zero(self):
        client = MagicMock()
        client.count.side_effect = RuntimeError("connection refused")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.count_points() == 0


# ---------------------------------------------------------------------------
# check_reachable
# ---------------------------------------------------------------------------

class TestCheckReachable:
    def test_none_client_is_unreachable(self):
        assert check_reachable(None) is False

    def test_successful_probe_is_reachable(self):
        client = MagicMock()
        assert check_reachable(client) is True
        client.get_collections.assert_called_once()

    def test_failed_probe_is_unreachable(self):
        client = MagicMock()
        client.get_collections.side_effect = RuntimeError("qdrant-memory unreachable")
        assert check_reachable(client) is False


# ---------------------------------------------------------------------------
# compute_dormant_ratio
# ---------------------------------------------------------------------------

class TestComputeDormantRatio:
    def test_empty_corpus_returns_zero(self):
        assert compute_dormant_ratio(0, 0) == 0.0

    def test_computes_fraction(self):
        assert compute_dormant_ratio(3, 12) == pytest.approx(0.25)

    def test_all_dormant_returns_one(self):
        assert compute_dormant_ratio(5, 5) == 1.0

    def test_none_dormant_returns_zero(self):
        assert compute_dormant_ratio(0, 10) == 0.0


# ---------------------------------------------------------------------------
# compute_memory_instance_telemetry — the health_check memory_instance block
# ---------------------------------------------------------------------------

class TestComputeMemoryInstanceTelemetry:
    def _index(self, memory_type, total, dormant, client=None):
        client = client or MagicMock()

        def _count(status=None):
            return dormant if status == "dormant" else total

        client.count.side_effect = lambda **kwargs: MagicMock(
            count=_count("dormant" if kwargs.get("count_filter") is not None else None)
        )
        return QdrantMemoryIndex(memory_type, client=client, embedder=_embedder)

    def test_unreachable_client_reports_false_with_zeroed_counts(self):
        indices = {
            "episodic": QdrantMemoryIndex("episodic", client=None),
            "semantic": QdrantMemoryIndex("semantic", client=None),
            "procedural": QdrantMemoryIndex("procedural", client=None),
        }
        result = compute_memory_instance_telemetry(client=None, indices=indices)
        assert result["reachable"] is False
        assert result["point_counts"] == {
            "memory_episodic": 0,
            "memory_semantic": 0,
            "memory_procedural": 0,
        }
        assert result["dormant_ratio"] == 0.0
        assert result["last_consolidation_at"] is None

    def test_reachable_client_reports_true(self):
        client = MagicMock()
        client.count.return_value = MagicMock(count=0)
        indices = {"semantic": QdrantMemoryIndex("semantic", client=client)}
        result = compute_memory_instance_telemetry(client=client, indices=indices)
        assert result["reachable"] is True

    def test_point_counts_keyed_by_collection_name(self):
        client = MagicMock()
        client.count.return_value = MagicMock(count=4)
        indices = {"semantic": QdrantMemoryIndex("semantic", client=client)}
        result = compute_memory_instance_telemetry(client=client, indices=indices)
        assert result["point_counts"] == {"memory_semantic": 4}

    def test_dormant_ratio_aggregates_across_collections(self):
        indices = {
            "episodic": self._index("episodic", total=8, dormant=2),
            "semantic": self._index("semantic", total=2, dormant=2),
        }
        result = compute_memory_instance_telemetry(client=MagicMock(), indices=indices)
        # total points = 10, total dormant = 4 -> 0.4
        assert result["dormant_ratio"] == pytest.approx(0.4)

    def test_last_consolidation_at_surfaced_as_iso_string(self, tmp_path):
        sync_state = MemorySyncState(root_dir=tmp_path)
        sync_state.record_consolidation(now=1_700_000_000.0)
        indices = {"semantic": QdrantMemoryIndex("semantic", client=None)}
        result = compute_memory_instance_telemetry(client=None, indices=indices, sync_state=sync_state)
        assert result["last_consolidation_at"] is not None
        assert result["last_consolidation_at"].startswith("2023-")

    def test_no_sync_state_leaves_last_consolidation_at_none(self):
        indices = {"semantic": QdrantMemoryIndex("semantic", client=None)}
        result = compute_memory_instance_telemetry(client=None, indices=indices, sync_state=None)
        assert result["last_consolidation_at"] is None

    def test_empty_indices_never_raises(self):
        result = compute_memory_instance_telemetry(client=None, indices={})
        assert result["point_counts"] == {}
        assert result["dormant_ratio"] == 0.0
