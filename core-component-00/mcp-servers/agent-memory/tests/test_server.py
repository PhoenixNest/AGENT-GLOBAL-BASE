"""Executable pytest suite for core-component-00/mcp-servers/agent-memory/server.py.

No live Qdrant instance or embedder-service is required — every interaction
is injected via unittest.mock.MagicMock. See conftest.py for import setup.

Run: python -m pytest core-component-00/mcp-servers/agent-memory/tests/ -v
"""
import concurrent.futures
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(
    0, str(Path(__file__).resolve().parents[3] / "engineering" / "context-engineering")
)
from implementations.memory_store import ReflectionRecord  # noqa: E402
from implementations.memory_vector_store import EMBEDDING_DIM  # noqa: E402


def _embedder(text: str):
    base = ord(text[0]) / 1000 if text else 0.0
    return [round(base + i * 0.001, 6) for i in range(EMBEDDING_DIM)]


def _make_reflection(**overrides):
    now = time.time()
    defaults = dict(
        reflection_id="REFLECT-001",
        trigger_type="director_flagged",
        source_event_ref="core-component-00/telescope/example/mistake-log.md#MISTAKE-001",
        summary="test summary",
        root_cause="test root cause",
        remediation="test remediation",
        scope_of_applicability="test scope",
        severity="low",
        logged_by="tester",
        timestamp=now,
        sacred=False,
        status="active",
        migrated_from=None,
    )
    defaults.update(overrides)
    return ReflectionRecord(**defaults)


# ---------------------------------------------------------------------------
# _search_memory_impl
# ---------------------------------------------------------------------------


class TestSearchMemoryImpl:
    def test_unknown_memory_type_degrades(self, agent_memory_server):
        result = agent_memory_server._search_memory_impl(
            query="q",
            memory_type="working",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=MagicMock(),
            embedder=_embedder,
        )
        assert result["degraded"] is True
        assert result["count"] == 0
        assert "unknown memory_type" in result["reason"]

    def test_episodic_without_session_id_or_cross_session_degrades(self, agent_memory_server):
        result = agent_memory_server._search_memory_impl(
            query="q",
            memory_type="episodic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=MagicMock(),
            embedder=_embedder,
        )
        assert result["degraded"] is True
        assert "session_id" in result["reason"]

    def test_episodic_with_cross_session_true_and_no_session_id_proceeds(self, agent_memory_server):
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        result = agent_memory_server._search_memory_impl(
            query="q",
            memory_type="episodic",
            top_k=5,
            session_id=None,
            cross_session=True,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        assert result["degraded"] is False
        assert result["count"] == 0

    def test_no_embedder_degrades_with_given_reason(self, agent_memory_server):
        result = agent_memory_server._search_memory_impl(
            query="q",
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

    def test_top_k_is_clamped_to_50(self, agent_memory_server):
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        agent_memory_server._search_memory_impl(
            query="q",
            memory_type="semantic",
            top_k=9999,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        _, kwargs = client.query_points.call_args
        assert kwargs["limit"] == 50

    def test_top_k_is_clamped_to_1_minimum(self, agent_memory_server):
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        agent_memory_server._search_memory_impl(
            query="q",
            memory_type="semantic",
            top_k=0,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        _, kwargs = client.query_points.call_args
        assert kwargs["limit"] == 1

    def test_reflection_type_routes_through_search_reflection(self, agent_memory_server):
        client = MagicMock()
        record = _make_reflection()
        point = MagicMock(payload=record.to_dict())
        client.query_points.return_value = MagicMock(points=[point])
        result = agent_memory_server._search_memory_impl(
            query="q",
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
        assert result["count"] == 1
        assert result["results"][0]["reflection_id"] == "REFLECT-001"

    def test_non_reflection_type_uses_qdrant_memory_index_search(self, agent_memory_server):
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        result = agent_memory_server._search_memory_impl(
            query="q",
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
        assert result["count"] == 0

    def test_client_none_reports_degraded_true_with_reason(self, agent_memory_server):
        result = agent_memory_server._search_memory_impl(
            query="q",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=None,
            embedder=_embedder,
        )
        assert result["degraded"] is True
        # Reason now comes from QdrantMemoryIndex.search_with_status()
        # (memory_vector_store.py), which covers client-None and
        # embedder-None with one shared message, rather than
        # _search_memory_impl constructing a client-only-specific string
        # itself — part of the Tier 3 fallback wiring
        # (05-disaster-recovery-and-resilience.md § 3), which needs a single
        # degraded signal regardless of which of the two is missing.
        assert result["reason"] == "qdrant client/embedder not configured"
        # Tier 3 (keyword_search_log) still ran despite the degraded Tier 1 —
        # this is exactly the fallback the feature adds.
        assert result["tier"] == 3

    def test_status_filter_defaults_to_active_only(self, agent_memory_server):
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        agent_memory_server._search_memory_impl(
            query="q",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        _, kwargs = client.query_points.call_args
        statuses = kwargs["query_filter"].must[0].match.any
        assert statuses == ["active"]

    def test_include_dormant_and_archived_extend_status_filter(self, agent_memory_server):
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        agent_memory_server._search_memory_impl(
            query="q",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=True,
            include_archived=True,
            client=client,
            embedder=_embedder,
        )
        _, kwargs = client.query_points.call_args
        statuses = kwargs["query_filter"].must[0].match.any
        assert set(statuses) == {"active", "dormant", "archived"}


# ---------------------------------------------------------------------------
# _search_reflection
# ---------------------------------------------------------------------------


class TestSearchReflection:
    def test_client_none_returns_empty(self, agent_memory_server):
        result = agent_memory_server._search_reflection(
            query="q", top_k=5, statuses=["active"], client=None, embedder=_embedder
        )
        assert result == []

    def test_parses_reflection_records_from_payload(self, agent_memory_server):
        client = MagicMock()
        record = _make_reflection(reflection_id="REFLECT-002", summary="s2")
        point = MagicMock(payload=record.to_dict())
        client.query_points.return_value = MagicMock(points=[point])
        result = agent_memory_server._search_reflection(
            query="q", top_k=5, statuses=["active"], client=client, embedder=_embedder
        )
        assert len(result) == 1
        assert isinstance(result[0], ReflectionRecord)
        assert result[0].reflection_id == "REFLECT-002"

    def test_status_filter_uses_given_statuses(self, agent_memory_server):
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        agent_memory_server._search_reflection(
            query="q",
            top_k=5,
            statuses=["active", "dormant"],
            client=client,
            embedder=_embedder,
        )
        _, kwargs = client.query_points.call_args
        assert kwargs["collection_name"] == agent_memory_server.COLLECTION_BY_TYPE["reflection"]
        must = kwargs["query_filter"].must[0]
        assert set(must.match.any) == {"active", "dormant"}

    def test_timeout_degrades_to_empty_list(self, agent_memory_server, monkeypatch):
        def _raise_timeout(fn, timeout=None):
            raise concurrent.futures.TimeoutError("simulated timeout")

        monkeypatch.setattr(agent_memory_server, "_call_with_hard_timeout", _raise_timeout)
        client = MagicMock()
        result = agent_memory_server._search_reflection(
            query="q", top_k=5, statuses=["active"], client=client, embedder=_embedder
        )
        assert result == []

    def test_malformed_payload_degrades_to_empty_list(self, agent_memory_server):
        client = MagicMock()
        bad_point = MagicMock(payload={"unexpected": "shape"})
        client.query_points.return_value = MagicMock(points=[bad_point])
        result = agent_memory_server._search_reflection(
            query="q", top_k=5, statuses=["active"], client=client, embedder=_embedder
        )
        assert result == []

    def test_connection_error_degrades_to_empty_list(self, agent_memory_server):
        client = MagicMock()
        client.query_points.side_effect = ConnectionError("qdrant-memory unreachable")
        result = agent_memory_server._search_reflection(
            query="q", top_k=5, statuses=["active"], client=client, embedder=_embedder
        )
        assert result == []


# ---------------------------------------------------------------------------
# _get_embedder / _get_embedder_unavailable_reason
# ---------------------------------------------------------------------------


class TestGetEmbedder:
    def test_service_ready_returns_a_working_resilient_embedder(
        self, reset_embedder_globals, monkeypatch
    ):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = True
        m._embedder_service_state = "ready"
        monkeypatch.setattr(
            m.embedder_client, "embed", lambda texts, model, expected_dim=None: [[0.1] * 384]
        )
        embed = m._get_embedder()
        assert embed is not None
        assert embed("hello") == [0.1] * 384

    def test_service_call_failure_falls_back_to_in_process_embedder(
        self, reset_embedder_globals, monkeypatch
    ):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = True
        m._embedder_service_state = "ready"
        m._embedder_cache = _embedder
        monkeypatch.setattr(
            m.embedder_client, "embed", lambda texts, model, expected_dim=None: None
        )
        embed = m._get_embedder()
        assert embed is not None
        assert embed("h") == _embedder("h")

    def test_service_disabled_and_in_process_not_ready_returns_none_without_blocking(
        self, reset_embedder_globals, monkeypatch
    ):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = False
        m._embedder_cache = None
        # Prevent the real lazy warmup thread from actually starting an
        # import chain during this unit test — verify only that _get_embedder()
        # asks for it to start (the trigger, not the thread body itself),
        # which _ensure_embedder_load_started already unit-tests separately
        # below.
        started = {"called": False}

        def _fake_ensure_started():
            started["called"] = True

        monkeypatch.setattr(m, "_ensure_embedder_load_started", _fake_ensure_started)
        result = m._get_embedder()
        assert result is None
        assert started["called"] is True

    def test_ensure_embedder_load_started_is_idempotent(self, reset_embedder_globals, monkeypatch):
        m = reset_embedder_globals
        calls = {"n": 0}

        def _fake_load_background():
            calls["n"] += 1

        monkeypatch.setattr(m, "_load_embedder_background", _fake_load_background)
        m._embedder_load_started = False
        m._embedder_state = "not started"
        m._ensure_embedder_load_started()
        m._ensure_embedder_load_started()
        # The thread target is only assigned once — this asserts the guard
        # flag, not the background thread's own execution (which races real
        # time); the state transition to "loading" is itself the contract.
        assert m._embedder_state == "loading"


class TestGetEmbedderUnavailableReason:
    def test_service_enabled_reports_both_states(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = True
        m._embedder_service_state = "starting"
        m._embedder_state = "loading"
        reason = m._get_embedder_unavailable_reason()
        assert "embedder-service: starting" in reason
        assert "in-process fallback: loading" in reason

    def test_service_disabled_not_started_message(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = False
        m._embedder_state = "not started"
        reason = m._get_embedder_unavailable_reason()
        assert "warmup not yet triggered" in reason

    def test_service_disabled_loading_message(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = False
        m._embedder_state = "loading"
        reason = m._get_embedder_unavailable_reason()
        assert "still loading" in reason

    def test_service_disabled_failed_message_includes_original_reason(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = False
        m._embedder_state = "failed: boom"
        reason = m._get_embedder_unavailable_reason()
        assert "failed to load" in reason
        assert "failed: boom" in reason


# ---------------------------------------------------------------------------
# _get_search_capability_snapshot
# ---------------------------------------------------------------------------


class TestSearchCapabilitySnapshot:
    def test_service_ready_wins_precedence(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = True
        m._embedder_service_state = "ready"
        m._embedder_cache = _embedder  # even if in-process is ALSO ready, service wins
        snap = m._get_search_capability_snapshot()
        assert snap["effective_path"] == "embedder-service"
        assert snap["embedder_service_state"] == "ready"

    def test_service_unavailable_but_in_process_ready_falls_back(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = True
        m._embedder_service_state = "unavailable"
        m._embedder_cache = _embedder
        m._embedder_state = "ready"
        snap = m._get_search_capability_snapshot()
        assert snap["effective_path"] == "in-process-fallback"

    def test_neither_ready_reports_unavailable(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = True
        m._embedder_service_state = "starting"
        m._embedder_cache = None
        m._embedder_state = "loading"
        snap = m._get_search_capability_snapshot()
        assert snap["effective_path"] == "unavailable"

    def test_service_disabled_reports_disabled_not_unavailable(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = False
        m._embedder_cache = None
        m._embedder_state = "not started"
        snap = m._get_search_capability_snapshot()
        assert snap["embedder_service_state"] == "disabled"
        assert snap["effective_path"] == "unavailable"

    def test_snapshot_never_triggers_lazy_warmup(self, reset_embedder_globals, monkeypatch):
        """The whole point of this function is that calling health_check must
        not itself cause the eager-background-work regression the 2026-07-17
        fix removed. Fail loudly if the snapshot ever calls the trigger."""
        m = reset_embedder_globals

        def _fail_if_called():
            raise AssertionError(
                "_get_search_capability_snapshot must never call "
                "_ensure_embedder_load_started() — health_check must stay read-only"
            )

        monkeypatch.setattr(m, "_ensure_embedder_load_started", _fail_if_called)
        m.EMBEDDER_SERVICE_ENABLED = False
        m._embedder_cache = None
        m._embedder_state = "not started"
        m._get_search_capability_snapshot()  # must not raise

    def test_snapshot_degrades_gracefully_on_internal_error(self, reset_embedder_globals, monkeypatch):
        m = reset_embedder_globals

        class _ExplodingLock:
            def __enter__(self):
                raise RuntimeError("lock acquisition exploded")

            def __exit__(self, *args):
                return False

        monkeypatch.setattr(m, "_embedder_service_lock", _ExplodingLock())
        snap = m._get_search_capability_snapshot()  # must not raise
        assert snap["effective_path"] == "unavailable"
        assert "snapshot error" in snap["in_process_fallback_state"]


# ---------------------------------------------------------------------------
# health_check tool wrapper — integrates search_capability into the real
# health_check() output, still fully mocked (no live Qdrant/embedder-service).
# ---------------------------------------------------------------------------


class TestHealthCheckTool:
    def test_returns_both_memory_instance_and_search_capability_blocks(
        self, agent_memory_server, monkeypatch
    ):
        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: None)
        result = agent_memory_server.health_check()
        assert "memory_instance" in result
        assert "search_capability" in result
        assert result["memory_instance"]["reachable"] is False
        assert set(result["search_capability"].keys()) == {
            "embedder_service_enabled",
            "embedder_service_state",
            "in_process_fallback_state",
            "effective_path",
        }

    def test_reachable_client_reports_true(self, agent_memory_server, monkeypatch):
        client = MagicMock()
        client.count.return_value = MagicMock(count=0)
        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: client)
        result = agent_memory_server.health_check()
        assert result["memory_instance"]["reachable"] is True

    def test_never_raises_even_if_get_memory_client_blows_up(self, agent_memory_server, monkeypatch):
        def _explode():
            raise RuntimeError("simulated catastrophic failure")

        monkeypatch.setattr(agent_memory_server, "_get_memory_client", _explode)
        result = agent_memory_server.health_check()  # must not raise
        assert result["memory_instance"]["reachable"] is False
        assert "error" in result["memory_instance"]
        assert "search_capability" in result  # present even on the exception path


# ---------------------------------------------------------------------------
# search_memory tool wrapper — never-raises contract
# ---------------------------------------------------------------------------


class TestSearchMemoryTool:
    def test_never_raises_even_if_get_embedder_blows_up(self, agent_memory_server, monkeypatch):
        def _explode():
            raise RuntimeError("simulated embedder failure")

        # client is mocked too, purely for test isolation/speed — this test's
        # point is the embedder exception path, not real QdrantClient
        # construction (which does not itself require network I/O, but is
        # unrelated to what's being asserted here).
        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: None)
        monkeypatch.setattr(agent_memory_server, "_get_embedder", _explode)
        result = agent_memory_server.search_memory(query="q", memory_type="semantic")
        assert result["degraded"] is True
        assert "search_memory failed" in result["reason"]
