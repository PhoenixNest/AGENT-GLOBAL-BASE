"""
Recovery from embedder-service going away while workspace-knowledge keeps
running (its idle self-shutdown, a crash, a manual stop), plus the engine
initialisation that keeps the MCP handshake fast.

`embedder_client` is replaced by a fake throughout: no test here touches the
network, the real embedder-service, or its lock/pid files. Engines are built
with SearchEngine.__new__() like the other suites here.
"""
import sys
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import server  # noqa: E402

SearchTier = server.SearchTier
DIM = 768


class _FakeEmbedderClient:
    def __init__(self):
        self.probe_result = True
        self.probe_calls = 0
        self.embed_result = [[0.1] * DIM]
        self.embed_calls = 0
        self.restart_callbacks = []
        self.in_flight = False

    def probe_health(self):
        self.probe_calls += 1
        return self.probe_result

    def embed(self, texts, model, timeout=None, expected_dim=None):
        self.embed_calls += 1
        return self.embed_result

    def request_service_restart(self, on_done=None):
        self.restart_callbacks.append(on_done)
        return True

    def restart_in_flight(self):
        return self.in_flight

    def ensure_service_running(self):
        return True


class _FakeModel:
    def encode(self, texts, **kwargs):
        import numpy as np

        return np.full((len(texts), DIM), 0.2, dtype="float32")


def _make_engine(tier=SearchTier.HYBRID_QDRANT, model=None, **overrides):
    engine = server.SearchEngine.__new__(server.SearchEngine)
    engine._tier = tier
    engine._degradation_reason = None
    engine._max_tier = tier
    engine._last_reprobe_at = 0.0
    engine._chunks = []
    engine._model = model
    engine._init_thread = None
    engine._qdrant_ready = False
    engine._qdrant_client = None
    engine._collection_name = "workspace_knowledge"
    for name, value in overrides.items():
        setattr(engine, name, value)
    return engine


@pytest.fixture
def env(monkeypatch):
    fake = _FakeEmbedderClient()
    monkeypatch.setattr(server, "embedder_client", fake)
    monkeypatch.setattr(server, "EMBEDDER_SERVICE_ENABLED", True)
    monkeypatch.setattr(server, "_embedder_service_state", "ready")
    monkeypatch.setattr(server, "_embedder_service_state_confirmed_at", time.time())
    monkeypatch.setattr(server, "_embedder_service_last_probe_at", 0.0)
    monkeypatch.setattr(server, "_embedder_recovery_wait_gave_up_at", 0.0)
    monkeypatch.setattr(server, "_EMBEDDER_RECOVERY_WAIT_S", 0.0)
    monkeypatch.setattr(server, "_EMBEDDER_RECOVERY_WAIT_POLL_S", 0.02)
    return fake


def _state():
    with server._embedder_service_lock:
        return server._embedder_service_state


class TestServiceDiesWhileCachedReady:
    def test_failed_query_embed_marks_down_requests_one_restart_and_uses_the_model(self, env):
        engine = _make_engine(model=_FakeModel())
        env.embed_result = None  # service has exited

        vec = engine._encode_query_vector("hello")

        assert vec.shape == (1, DIM)
        assert _state() == "unavailable"
        assert len(env.restart_callbacks) == 1
        assert server._embedder_service_state_confirmed_at > time.time() - 5

    def test_failed_query_embed_without_a_model_raises_the_deferred_signal(self, env):
        engine = _make_engine(model=None)
        env.embed_result = None

        with pytest.raises(RuntimeError, match="model not ready"):
            engine._encode_query_vector("hello")

        assert _state() == "unavailable"
        assert len(env.restart_callbacks) == 1

    def test_failed_batch_embed_marks_down_and_requests_one_restart(self, env):
        engine = _make_engine(model=_FakeModel())
        env.embed_result = None

        out = engine._encode_batch_vectors(["a", "b"])

        assert out.shape == (2, DIM)
        assert _state() == "unavailable"
        assert len(env.restart_callbacks) == 1

    def test_restart_callback_flips_state_back_to_ready(self, env):
        engine = _make_engine(model=_FakeModel())
        env.embed_result = None
        engine._encode_query_vector("hello")

        env.restart_callbacks[0](True)

        assert _state() == "ready"

    def test_recovery_returns_to_the_service_path(self, env):
        engine = _make_engine(model=_FakeModel())
        env.embed_result = None
        engine._encode_query_vector("hello")

        env.embed_result = [[0.9] * DIM]  # service relaunched
        env.probe_result = True
        vec = engine._encode_query_vector("hello")

        assert abs(float(vec[0][0]) - 1 / DIM**0.5) < 1e-6  # the service's vector, normalised
        assert _state() == "ready"

    def test_successful_embed_counts_as_confirmation(self, env):
        engine = _make_engine(model=_FakeModel())
        server._embedder_service_state_confirmed_at = time.time() - 20.0

        engine._encode_query_vector("hello")

        assert time.time() - server._embedder_service_state_confirmed_at < 5.0


class TestStaleReadyIsReprobed:
    def test_fresh_ready_is_not_probed(self, env):
        assert server._embedder_service_ready() is True
        assert env.probe_calls == 0

    def test_stale_ready_with_live_service_stays_ready_and_refreshes_timestamp(self, env):
        server._embedder_service_state_confirmed_at = time.time() - 120.0

        assert server._embedder_service_ready() is True
        assert env.probe_calls == 1
        assert time.time() - server._embedder_service_state_confirmed_at < 5.0
        assert env.restart_callbacks == []

    def test_stale_ready_with_dead_service_takes_the_mark_down_path(self, env):
        server._embedder_service_state_confirmed_at = time.time() - 120.0
        env.probe_result = False

        assert server._embedder_service_ready() is False
        assert _state() == "unavailable"
        assert len(env.restart_callbacks) == 1

    def test_query_after_idle_with_a_model_loaded_still_answers(self, env):
        engine = _make_engine(model=_FakeModel())
        server._embedder_service_state_confirmed_at = time.time() - 120.0
        env.probe_result = False

        assert engine._encode_query_vector("hello").shape == (1, DIM)
        assert env.embed_calls == 0  # the dead service was never called


class TestUnavailableReprobe:
    def test_reprobes_on_cooldown_and_requests_restart_when_still_down(self, env):
        server._embedder_service_state = "unavailable"
        env.probe_result = False

        assert server._embedder_service_ready() is False
        assert env.probe_calls == 1
        assert len(env.restart_callbacks) == 1

        assert server._embedder_service_ready() is False  # inside the cooldown
        assert env.probe_calls == 1

    def test_recovers_when_probe_succeeds(self, env):
        server._embedder_service_state = "unavailable"
        env.probe_result = True

        assert server._embedder_service_ready() is True
        assert _state() == "ready"
        assert env.restart_callbacks == []


class TestBoundedRecoveryWait:
    def _wait(self, engine):
        return server._wait_for_embedder_recovery(
            fallback_ready=lambda: engine._model is not None,
            fallback_loading=lambda: False,
        )

    def test_returns_early_when_the_service_comes_back(self, env):
        engine = _make_engine(model=None)
        server._EMBEDDER_RECOVERY_WAIT_S = 10.0
        server._embedder_service_state = "unavailable"
        env.in_flight = True

        def _service_returns():
            time.sleep(0.2)
            server._record_embedder_service_state(True)
            env.in_flight = False

        threading.Thread(target=_service_returns, daemon=True).start()
        t0 = time.monotonic()
        assert self._wait(engine) is True
        assert time.monotonic() - t0 < 3.0

    def test_returns_early_when_the_model_finishes_loading(self, env):
        engine = _make_engine(model=None)
        server._EMBEDDER_RECOVERY_WAIT_S = 10.0
        server._embedder_service_state = "unavailable"
        env.in_flight = True

        def _model_loads():
            time.sleep(0.2)
            engine._model = _FakeModel()

        threading.Thread(target=_model_loads, daemon=True).start()
        t0 = time.monotonic()
        assert self._wait(engine) is True
        assert time.monotonic() - t0 < 3.0

    def test_times_out_cleanly_then_backs_off(self, env):
        engine = _make_engine(model=None)
        server._EMBEDDER_RECOVERY_WAIT_S = 0.4
        server._embedder_service_state = "unavailable"
        env.in_flight = True

        t0 = time.monotonic()
        assert self._wait(engine) is False
        assert 0.35 <= time.monotonic() - t0 < 3.0

        t1 = time.monotonic()
        assert self._wait(engine) is False
        assert time.monotonic() - t1 < 0.2

    def test_zero_disables_the_wait(self, env):
        engine = _make_engine(model=None)
        server._EMBEDDER_RECOVERY_WAIT_S = 0.0
        server._embedder_service_state = "unavailable"
        env.in_flight = True

        t0 = time.monotonic()
        assert self._wait(engine) is False
        assert time.monotonic() - t0 < 0.2

    def test_query_after_idle_without_a_model_waits_for_the_relaunch(self, env):
        engine = _make_engine(model=None)
        server._EMBEDDER_RECOVERY_WAIT_S = 10.0
        server._embedder_service_state_confirmed_at = time.time() - 120.0
        env.probe_result = False
        env.embed_result = [[0.5] * DIM]

        def _relaunch(on_done=None):
            env.restart_callbacks.append(on_done)
            env.in_flight = True

            def _finish():
                time.sleep(0.2)
                env.probe_result = True
                on_done(True)
                env.in_flight = False

            threading.Thread(target=_finish, daemon=True).start()
            return True

        env.request_service_restart = _relaunch

        vec = engine._encode_query_vector("hello")

        assert vec.shape == (1, DIM)
        assert len(env.restart_callbacks) == 1

    def test_timeout_degrades_exactly_as_before(self, env):
        engine = _make_engine(model=None)
        server._EMBEDDER_RECOVERY_WAIT_S = 0.3
        server._embedder_service_state_confirmed_at = time.time() - 120.0
        env.probe_result = False
        env.in_flight = True

        with pytest.raises(RuntimeError, match="model not ready"):
            engine._encode_query_vector("hello")

    def test_startup_state_does_not_wait(self, env):
        """"starting" is not a discovered outage: the first query keeps
        degrading immediately while the startup launch is still deciding."""
        engine = _make_engine(model=None)
        server._EMBEDDER_RECOVERY_WAIT_S = 10.0
        server._embedder_service_state = "starting"
        env.in_flight = True

        t0 = time.monotonic()
        with pytest.raises(RuntimeError, match="model not ready"):
            engine._encode_query_vector("hello")
        assert time.monotonic() - t0 < 0.5


class TestHealthTellsTheTruth:
    def _block(self, monkeypatch, engine):
        monkeypatch.setattr(server, "engine", engine)
        return server._document_kb_health_block()

    def test_semantic_tier_is_not_reported_clean_when_embedding_is_impossible(self, env, monkeypatch):
        env.probe_result = False  # cache says "ready", service is gone
        block = self._block(monkeypatch, _make_engine(SearchTier.HYBRID_QDRANT, model=None))

        assert block["search_tier"] == "hybrid_qdrant"
        assert block["effective_search_tier"] == "bm25"
        assert block["degradation_reason"]
        assert block["embedder"]["embedder_service_probe"] == "failed"
        assert block["embedder"]["effective_path"] == "unavailable"
        assert block["embedder"]["query_embedding_available"] is False

    def test_loaded_model_keeps_the_semantic_tier_honest(self, env, monkeypatch):
        env.probe_result = False
        block = self._block(monkeypatch, _make_engine(SearchTier.HYBRID, model=_FakeModel()))

        assert block["effective_search_tier"] == "hybrid"
        assert block["degradation_reason"] is None
        assert block["embedder"]["effective_path"] == "in-process-fallback"
        assert block["embedder"]["query_embedding_available"] is True

    def test_live_service_is_reported_as_the_effective_path(self, env, monkeypatch):
        env.probe_result = True
        block = self._block(monkeypatch, _make_engine(SearchTier.HYBRID_QDRANT, model=None))

        assert block["embedder"]["effective_path"] == "embedder-service"
        assert block["effective_search_tier"] == "hybrid_qdrant"
        assert block["degradation_reason"] is None

    def test_an_existing_degradation_reason_is_never_overwritten(self, env, monkeypatch):
        env.probe_result = False
        engine = _make_engine(SearchTier.HYBRID, model=None)
        engine._degradation_reason = "Qdrant search failed: boom"

        assert self._block(monkeypatch, engine)["degradation_reason"] == "Qdrant search failed: boom"

    def test_bm25_tier_needs_no_embedder(self, env, monkeypatch):
        env.probe_result = False
        block = self._block(monkeypatch, _make_engine(SearchTier.BM25, model=None))

        assert block["effective_search_tier"] == "bm25"
        assert block["degradation_reason"] is None

    def test_health_never_launches_the_service(self, env, monkeypatch):
        env.probe_result = False
        self._block(monkeypatch, _make_engine(SearchTier.HYBRID_QDRANT, model=None))

        assert env.restart_callbacks == []

    def test_health_check_tool_carries_the_embedder_block(self, env, monkeypatch):
        env.probe_result = False
        monkeypatch.setattr(server, "engine", _make_engine(SearchTier.HYBRID_QDRANT, model=None))
        monkeypatch.setattr(server, "_memory_instance_health_block", lambda: {"reachable": False})

        result = server.health_check()

        assert result["document_knowledge_base"]["embedder"]["query_embedding_available"] is False


class TestServiceDisabledPathUnchanged:
    def test_disabled_never_probes_restarts_or_waits(self, env, monkeypatch):
        monkeypatch.setattr(server, "EMBEDDER_SERVICE_ENABLED", False)
        server._EMBEDDER_RECOVERY_WAIT_S = 10.0
        env.in_flight = True
        engine = _make_engine(model=None)

        t0 = time.monotonic()
        with pytest.raises(RuntimeError, match="model not ready"):
            engine._encode_query_vector("hello")
        assert time.monotonic() - t0 < 0.5
        assert (env.probe_calls, env.embed_calls, env.restart_callbacks) == (0, 0, [])

        block = server._embedder_capability_snapshot(model_loaded=False)
        assert block["embedder_service_probe"] == "not-probed"
        assert block["embedder_service_state"] == "disabled"


class TestEngineInitStaysOffTheHandshakePath:
    def test_initialisation_returns_before_the_bm25_build_finishes(self, monkeypatch):
        gate = threading.Event()
        engine = _make_engine(SearchTier.RAWFS)
        engine._rebuild_progress = {}
        monkeypatch.setattr(engine, "_build_bm25_index", lambda cls: gate.wait(10))
        monkeypatch.setattr(engine, "_init_faiss_background", lambda: None)

        t0 = time.monotonic()
        engine._initialize_search_engine()
        elapsed = time.monotonic() - t0

        assert elapsed < 1.0
        assert engine._tier == SearchTier.RAWFS
        assert "still building" in engine._degradation_reason
        assert engine._init_thread is not None and engine._init_thread.is_alive()

        gate.set()
        engine._init_thread.join(timeout=5)
        assert engine._tier == SearchTier.BM25
        assert engine._degradation_reason is None

    def test_failed_bm25_build_degrades_to_rawfs_with_the_reason(self, monkeypatch):
        engine = _make_engine(SearchTier.RAWFS)
        engine._rebuild_progress = {}

        def _fail(cls):
            raise RuntimeError("No markdown files found")

        monkeypatch.setattr(engine, "_build_bm25_index", _fail)
        monkeypatch.setattr(engine, "_init_faiss_background", lambda: pytest.fail("must not run"))

        engine._initialize_search_engine()
        engine._init_thread.join(timeout=5)

        assert engine._tier == SearchTier.RAWFS
        assert "BM25 build failed" in engine._degradation_reason
