"""
Integration tests for the Tier 3 (keyword-only log search) disaster-recovery
fallback wiring in _search_memory_impl — the feature
05-disaster-recovery-and-resilience.md § 3 flagged as designed but never
built (audited 2026-08-10), implemented in this build (CEO-delegated to Dr.
Vance, git worktree agent/cc00-lab/tier3-keyword-log-search).

Unit coverage for keyword_search_log()/search_with_status()/bm25_rank_ids()
themselves lives in
engineering/context-engineering/testing/test_memory_vector_store.py — this
file covers the wiring: does _search_memory_impl actually fall through to
Tier 3 when Tier 1 (Qdrant) is degraded, for both the three
MemoryRecord-shaped collections and the reflection collection's separate
code path.

Run: python -m pytest core-component-00/mcp-servers/agent-memory/tests/test_tier3_keyword_search.py -v
"""
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(
    0, str(Path(__file__).resolve().parents[3] / "engineering" / "context-engineering")
)
# server.py does a bare `import write_tool` (a sibling module in agent-memory/,
# not a package) — needs agent-memory/ itself on sys.path when this file is
# collected in isolation, matching test_read_constraints_reverification.py's
# own sys.path.insert(0, str(_AGENT_MEMORY_DIR)).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from implementations.memory_store import ReflectionRecord  # noqa: E402
from implementations.memory_vector_store import (  # noqa: E402
    EMBEDDING_DIM,
    JSONLMemoryLog,
    MemoryRecord,
)


def _embedder(text: str):
    base = ord(text[0]) / 1000 if text else 0.0
    return [round(base + i * 0.001, 6) for i in range(EMBEDDING_DIM)]


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


def _make_reflection(**overrides):
    now = time.time()
    defaults = dict(
        reflection_id="REFLECT-001",
        trigger_type="director_flagged",
        source_event_ref="core-component-00/telescope/example/mistake-log.md#MISTAKE-001",
        summary="database migration caused a brief outage",
        root_cause="missing index on foreign key",
        remediation="add index before large migrations",
        scope_of_applicability="any future schema migration",
        severity="medium",
        logged_by="tester",
        timestamp=now,
        sacred=False,
        status="active",
        migrated_from=None,
    )
    defaults.update(overrides)
    return ReflectionRecord(**defaults)


@pytest.fixture
def isolated_memory_log(agent_memory_server, tmp_path, monkeypatch):
    """Swaps the module-level _memory_log singleton for a tmp_path-backed
    instance for the duration of one test, so Tier 3 tests never read the
    real on-disk memory/ directory and are fully deterministic."""
    log = JSONLMemoryLog(root_dir=tmp_path)
    monkeypatch.setattr(agent_memory_server, "_memory_log", log)
    return log


class TestTier3FallbackWiring:
    def test_qdrant_connection_error_falls_through_to_tier3_with_real_results(
        self, agent_memory_server, isolated_memory_log
    ):
        isolated_memory_log.append(
            _make_record(memory_type="semantic", id="r1", content="user prefers FastAPI and PostgreSQL")
        )
        client = MagicMock()
        client.query_points.side_effect = ConnectionError("qdrant-memory unreachable")

        result = agent_memory_server._search_memory_impl(
            query="FastAPI PostgreSQL",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        assert result["degraded"] is True
        assert result["tier"] == 3
        assert result["count"] == 1
        assert result["results"][0]["id"] == "r1"

    def test_healthy_qdrant_uses_tier1_not_tier3(self, agent_memory_server, isolated_memory_log):
        # A record only Tier 3 could find (not in Qdrant's mocked response) —
        # if this shows up in results, Tier 3 ran when it shouldn't have.
        isolated_memory_log.append(
            _make_record(memory_type="semantic", id="log-only", content="FastAPI PostgreSQL")
        )
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])

        result = agent_memory_server._search_memory_impl(
            query="FastAPI PostgreSQL",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        assert result["degraded"] is False
        assert result["tier"] == 1
        assert result["count"] == 0

    def test_embedder_unavailable_falls_through_to_tier3(self, agent_memory_server, isolated_memory_log):
        """The gap found and fixed in this build: embedder=None used to
        short-circuit to an empty result before Tier 1/3 dispatch ever ran,
        even though Tier 3 needs no embedder at all."""
        isolated_memory_log.append(
            _make_record(memory_type="semantic", id="r1", content="Kubernetes cluster autoscaling")
        )
        result = agent_memory_server._search_memory_impl(
            query="Kubernetes autoscaling",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=MagicMock(),
            embedder=None,
            embedder_unavailable_reason="embedding model still loading",
        )
        assert result["degraded"] is True
        assert result["reason"] == "embedding model still loading"
        assert result["tier"] == 3
        assert result["count"] == 1
        assert result["results"][0]["id"] == "r1"

    def test_episodic_session_scoping_preserved_in_tier3(self, agent_memory_server, isolated_memory_log):
        isolated_memory_log.append(
            _make_record(
                memory_type="episodic", id="e1", content="deployed payments service",
                source_session_id="session-a",
            )
        )
        isolated_memory_log.append(
            _make_record(
                memory_type="episodic", id="e2", content="deployed payments service",
                source_session_id="session-b",
            )
        )
        client = MagicMock()
        client.query_points.side_effect = ConnectionError("simulated outage")

        result = agent_memory_server._search_memory_impl(
            query="deployed payments",
            memory_type="episodic",
            top_k=5,
            session_id="session-a",
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        assert result["tier"] == 3
        ids = [r["id"] for r in result["results"]]
        assert ids == ["e1"]

    def test_status_filter_preserved_in_tier3(self, agent_memory_server, isolated_memory_log):
        isolated_memory_log.append(
            _make_record(memory_type="semantic", id="active-1", content="database migration plan", status="active")
        )
        isolated_memory_log.append(
            _make_record(memory_type="semantic", id="archived-1", content="database migration plan", status="archived")
        )
        client = MagicMock()
        client.query_points.side_effect = ConnectionError("simulated outage")

        result = agent_memory_server._search_memory_impl(
            query="database migration",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        ids = [r["id"] for r in result["results"]]
        assert "active-1" in ids
        assert "archived-1" not in ids

        result_with_archived = agent_memory_server._search_memory_impl(
            query="database migration",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=True,
            client=client,
            embedder=_embedder,
        )
        ids2 = [r["id"] for r in result_with_archived["results"]]
        assert "archived-1" in ids2

    def test_sacred_record_survives_tier3_via_status_filter(self, agent_memory_server, isolated_memory_log):
        isolated_memory_log.append(
            _make_record(
                memory_type="semantic",
                id="decision-1",
                content="team decided to standardize on PostgreSQL",
                sacred=True,
                status="active",
            )
        )
        client = MagicMock()
        client.query_points.side_effect = ConnectionError("simulated outage")

        result = agent_memory_server._search_memory_impl(
            query="PostgreSQL",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        ids = [r["id"] for r in result["results"]]
        assert "decision-1" in ids


class TestTier3ReflectionFallback:
    def test_reflection_qdrant_outage_falls_through_to_tier3(self, agent_memory_server, isolated_memory_log):
        isolated_memory_log.append_reflection(
            _make_reflection(reflection_id="REFLECT-9", summary="index missing on migration", scope_of_applicability="schema changes")
        )
        client = MagicMock()
        client.query_points.side_effect = ConnectionError("qdrant-memory unreachable")

        result = agent_memory_server._search_memory_impl(
            query="index missing migration",
            memory_type="reflection",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        assert result["degraded"] is True
        assert result["tier"] == 3
        assert result["count"] == 1
        assert result["results"][0]["reflection_id"] == "REFLECT-9"

    def test_reflection_healthy_qdrant_uses_tier1(self, agent_memory_server, isolated_memory_log):
        isolated_memory_log.append_reflection(_make_reflection(reflection_id="REFLECT-LOG-ONLY"))
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])

        result = agent_memory_server._search_memory_impl(
            query="anything",
            memory_type="reflection",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        assert result["degraded"] is False
        assert result["tier"] == 1
        assert result["count"] == 0

    def test_keyword_search_reflection_log_scores_same_text_tier1_would_embed(
        self, agent_memory_server, isolated_memory_log
    ):
        """Parity check: Tier 3 ranks reflections against
        "{summary} {scope_of_applicability}" — the exact text
        QdrantMemoryIndex.rebuild_from_log()'s reflection branch embeds into
        Qdrant, not a different field."""
        isolated_memory_log.append_reflection(
            _make_reflection(
                reflection_id="R1", summary="Kubernetes autoscaling misconfigured",
                scope_of_applicability="cluster capacity planning",
            )
        )
        isolated_memory_log.append_reflection(
            _make_reflection(reflection_id="R2", summary="unrelated topic", scope_of_applicability="unrelated scope")
        )
        results = agent_memory_server.keyword_search_reflection_log(
            log=isolated_memory_log, query="Kubernetes autoscaling", top_k=1, statuses=["active"]
        )
        assert len(results) == 1
        assert results[0].reflection_id == "R1"
