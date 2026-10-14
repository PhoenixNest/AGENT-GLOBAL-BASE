"""
Recovery from embedder-service going away while the server keeps running
(its idle self-shutdown, a crash, a manual stop).

Covers agent-memory/server.py's detection (a failed runtime embed call, a
stale cached "ready"), the non-blocking relaunch request, the in-process
fallback trigger, the bounded wait for recovery, and health_check's
call-time probe. `embedder_client` is replaced by a fake throughout: no test
here touches the network, the real embedder-service, or the lock/pid files.
"""
import threading
import time

import pytest


class _FakeEmbedderClient:
    def __init__(self):
        self.probe_result = True
        self.probe_calls = 0
        self.embed_result = [[0.5] * 384]
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


@pytest.fixture
def env(agent_memory_server, monkeypatch):
    """Server module with a fake embedder_client, service enabled and cached
    "ready" just confirmed, no in-process embedder, and the recovery wait
    disabled (individual tests opt in)."""
    m = agent_memory_server
    fake = _FakeEmbedderClient()
    fallback_loads = []
    monkeypatch.setattr(m, "embedder_client", fake)
    monkeypatch.setattr(m, "EMBEDDER_SERVICE_ENABLED", True)
    monkeypatch.setattr(m, "_embedder_service_state", "ready")
    monkeypatch.setattr(m, "_embedder_service_state_confirmed_at", time.time())
    monkeypatch.setattr(m, "_embedder_service_last_probe_at", 0.0)
    monkeypatch.setattr(m, "_embedder_cache", None)
    monkeypatch.setattr(m, "_embedder_state", "not started")
    monkeypatch.setattr(m, "_embedder_load_started", False)
    monkeypatch.setattr(m, "_embedder_recovery_wait_gave_up_at", 0.0)
    monkeypatch.setattr(m, "_EMBEDDER_RECOVERY_WAIT_S", 0.0)
    monkeypatch.setattr(m, "_EMBEDDER_RECOVERY_WAIT_POLL_S", 0.02)
    monkeypatch.setattr(m, "_ensure_embedder_load_started", lambda: fallback_loads.append(1))
    return m, fake, fallback_loads


def _service_state(m):
    with m._embedder_service_lock:
        return m._embedder_service_state


class TestServiceDiesWhileCachedReady:
    def test_failed_embed_marks_down_requests_one_restart_and_starts_fallback(self, env):
        m, fake, fallback_loads = env
        embed = m._get_embedder()
        assert embed is not None  # cached "ready" is fresh, so the service path is chosen
        fake.embed_result = None  # service has exited

        with pytest.raises(RuntimeError, match="in-process embedder not ready"):
            embed("hello")

        assert _service_state(m) == "unavailable"
        assert m._embedder_service_state_confirmed_at > time.time() - 5
        assert len(fake.restart_callbacks) == 1
        # The wait is disabled here and nothing recovered, so the resolver
        # ends by starting the in-process load.
        assert fallback_loads

    def test_failed_embed_uses_fallback_when_it_is_already_loaded(self, env):
        m, fake, _ = env
        m._embedder_cache = lambda text: [0.25] * 384
        embed = m._get_embedder()
        fake.embed_result = None

        assert embed("hello") == [0.25] * 384
        assert _service_state(m) == "unavailable"
        assert len(fake.restart_callbacks) == 1

    def test_restart_callback_flips_state_back_to_ready(self, env):
        m, fake, _ = env
        embed = m._get_embedder()
        fake.embed_result = None
        with pytest.raises(RuntimeError):
            embed("hello")
        assert _service_state(m) == "unavailable"

        fake.restart_callbacks[0](True)

        assert _service_state(m) == "ready"

    def test_recovery_returns_to_the_service_path(self, env):
        m, fake, _ = env
        embed = m._get_embedder()
        fake.embed_result = None
        with pytest.raises(RuntimeError):
            embed("hello")

        fake.embed_result = [[0.75] * 384]  # service relaunched
        fake.probe_result = True
        embed_again = m._get_embedder()  # cooldown elapsed: re-probe finds it

        assert embed_again is not None
        assert embed_again("hello") == [0.75] * 384
        assert _service_state(m) == "ready"

    def test_successful_embed_counts_as_confirmation(self, env):
        m, fake, _ = env
        embed = m._get_embedder()
        m._embedder_service_state_confirmed_at = time.time() - 20.0

        embed("hello")

        assert time.time() - m._embedder_service_state_confirmed_at < 5.0


class TestRelaunchBeforeInProcessLoad:
    def test_mark_down_requests_relaunch_without_starting_the_load(self, env):
        m, fake, fallback_loads = env
        m._mark_embedder_service_down("test")

        assert len(fake.restart_callbacks) == 1
        assert fallback_loads == []

    def test_failed_relaunch_starts_the_in_process_load(self, env):
        m, fake, fallback_loads = env
        m._mark_embedder_service_down("test")

        fake.restart_callbacks[0](False)

        assert _service_state(m) == "unavailable"
        assert fallback_loads == [1]

    def test_successful_relaunch_never_starts_the_load(self, env):
        m, fake, fallback_loads = env
        m._mark_embedder_service_down("test")

        fake.restart_callbacks[0](True)

        assert fallback_loads == []

    def test_resolver_waits_for_the_relaunch_before_starting_the_load(self, env):
        m, fake, fallback_loads = env
        m._EMBEDDER_RECOVERY_WAIT_S = 10.0
        m._embedder_service_state = "unavailable"
        fake.probe_result = False
        loads_seen_during_wait = []

        def _relaunch(on_done=None):
            fake.restart_callbacks.append(on_done)
            fake.in_flight = True

            def _finish():
                time.sleep(0.2)
                loads_seen_during_wait.append(list(fallback_loads))
                fake.probe_result = True
                on_done(True)
                fake.in_flight = False

            threading.Thread(target=_finish, daemon=True).start()
            return True

        fake.request_service_restart = _relaunch

        assert m._get_embedder() is not None
        assert loads_seen_during_wait == [[]]
        assert fallback_loads == []

    def test_resolver_starts_the_load_when_the_wait_times_out(self, env):
        m, fake, fallback_loads = env
        m._EMBEDDER_RECOVERY_WAIT_S = 0.3
        m._embedder_service_state = "unavailable"
        fake.probe_result = False
        fake.in_flight = True

        assert m._get_embedder() is None
        assert fallback_loads

    def test_startup_state_still_starts_the_load_immediately(self, env):
        m, fake, fallback_loads = env
        m._embedder_service_state = "starting"

        assert m._get_embedder() is None
        assert fallback_loads


class TestStaleReadyIsReprobed:
    def test_fresh_ready_is_not_probed(self, env):
        m, fake, _ = env
        assert m._embedder_service_ready() is True
        assert fake.probe_calls == 0

    def test_stale_ready_with_live_service_stays_ready_and_refreshes_timestamp(self, env):
        m, fake, _ = env
        m._embedder_service_state_confirmed_at = time.time() - 120.0
        fake.probe_result = True

        assert m._embedder_service_ready() is True
        assert fake.probe_calls == 1
        assert time.time() - m._embedder_service_state_confirmed_at < 5.0
        assert fake.restart_callbacks == []

    def test_stale_ready_with_dead_service_takes_the_mark_down_path(self, env):
        m, fake, fallback_loads = env
        m._embedder_service_state_confirmed_at = time.time() - 120.0
        fake.probe_result = False

        assert m._embedder_service_ready() is False
        assert _service_state(m) == "unavailable"
        assert len(fake.restart_callbacks) == 1
        assert fallback_loads == []  # relaunch first; no in-process load yet

    def test_get_embedder_does_not_return_the_dead_service_path(self, env):
        m, fake, _ = env
        m._embedder_service_state_confirmed_at = time.time() - 120.0
        fake.probe_result = False

        assert m._get_embedder() is None  # no in-process embedder either, wait disabled


class TestUnavailableReprobe:
    def test_unavailable_is_reprobed_on_cooldown_and_requests_restart_when_still_down(self, env):
        m, fake, _ = env
        m._embedder_service_state = "unavailable"
        fake.probe_result = False

        assert m._embedder_service_ready() is False
        assert fake.probe_calls == 1
        assert len(fake.restart_callbacks) == 1

        assert m._embedder_service_ready() is False  # inside the cooldown
        assert fake.probe_calls == 1

    def test_unavailable_recovers_when_probe_succeeds(self, env):
        m, fake, _ = env
        m._embedder_service_state = "unavailable"
        fake.probe_result = True

        assert m._embedder_service_ready() is True
        assert _service_state(m) == "ready"
        assert fake.restart_callbacks == []


class TestBoundedRecoveryWait:
    def test_returns_early_when_the_service_comes_back(self, env):
        m, fake, _ = env
        m._EMBEDDER_RECOVERY_WAIT_S = 10.0
        m._embedder_service_state = "unavailable"
        fake.in_flight = True

        def _service_returns():
            time.sleep(0.2)
            m._record_embedder_service_state(True)
            fake.in_flight = False

        threading.Thread(target=_service_returns, daemon=True).start()
        t0 = time.monotonic()
        assert m._wait_for_embedder_recovery() is True
        assert time.monotonic() - t0 < 3.0

    def test_returns_early_when_the_in_process_embedder_becomes_ready(self, env):
        m, fake, _ = env
        m._EMBEDDER_RECOVERY_WAIT_S = 10.0
        m._embedder_service_state = "unavailable"
        m._embedder_state = "loading"

        def _load_finishes():
            time.sleep(0.2)
            m._embedder_cache = lambda text: [0.0] * 384

        threading.Thread(target=_load_finishes, daemon=True).start()
        t0 = time.monotonic()
        assert m._wait_for_embedder_recovery() is True
        assert time.monotonic() - t0 < 3.0

    def test_times_out_cleanly_then_backs_off(self, env):
        m, fake, _ = env
        m._EMBEDDER_RECOVERY_WAIT_S = 0.4
        m._embedder_service_state = "unavailable"
        fake.in_flight = True  # a relaunch that never finishes

        t0 = time.monotonic()
        assert m._wait_for_embedder_recovery() is False
        assert 0.35 <= time.monotonic() - t0 < 3.0

        t1 = time.monotonic()
        assert m._wait_for_embedder_recovery() is False  # inside the backoff window
        assert time.monotonic() - t1 < 0.2

    def test_does_not_wait_when_nothing_is_in_progress(self, env):
        m, fake, _ = env
        m._EMBEDDER_RECOVERY_WAIT_S = 10.0
        m._embedder_service_state = "unavailable"
        fake.in_flight = False

        t0 = time.monotonic()
        assert m._wait_for_embedder_recovery() is False
        assert time.monotonic() - t0 < 0.5

    def test_zero_disables_the_wait(self, env):
        m, fake, _ = env
        m._EMBEDDER_RECOVERY_WAIT_S = 0.0
        m._embedder_service_state = "unavailable"
        fake.in_flight = True

        t0 = time.monotonic()
        assert m._wait_for_embedder_recovery() is False
        assert time.monotonic() - t0 < 0.2

    def test_first_call_after_idle_gets_a_full_quality_embedder(self, env):
        """Cached "ready" has gone stale and the service is gone: the tool
        call path finds it down, the relaunch completes during the bounded
        wait, and the call proceeds on the service path."""
        m, fake, _ = env
        m._EMBEDDER_RECOVERY_WAIT_S = 10.0
        m._embedder_service_state_confirmed_at = time.time() - 120.0
        fake.probe_result = False
        fake.embed_result = [[0.9] * 384]

        def _relaunch(on_done=None):
            fake.restart_callbacks.append(on_done)
            fake.in_flight = True

            def _finish():
                time.sleep(0.2)
                fake.probe_result = True
                on_done(True)
                fake.in_flight = False

            threading.Thread(target=_finish, daemon=True).start()
            return True

        fake.request_service_restart = _relaunch

        embed = m._get_embedder()

        assert embed is not None
        assert embed("hello") == [0.9] * 384
        assert len(fake.restart_callbacks) == 1

    def test_timeout_degrades_exactly_as_before(self, env):
        m, fake, _ = env
        m._EMBEDDER_RECOVERY_WAIT_S = 0.3
        m._embedder_service_state_confirmed_at = time.time() - 120.0
        fake.probe_result = False
        fake.in_flight = True

        assert m._get_embedder() is None


class TestHealthTellsTheTruth:
    def test_dead_service_is_never_reported_as_the_effective_path(self, env):
        m, fake, _ = env
        fake.probe_result = False  # cache still says "ready"

        snap = m._get_search_capability_snapshot()

        assert snap["embedder_service_probe"] == "failed"
        assert snap["embedder_service_state"] == "unavailable"
        assert snap["effective_path"] == "unavailable"

    def test_dead_service_with_loaded_fallback_reports_the_fallback(self, env):
        m, fake, _ = env
        fake.probe_result = False
        m._embedder_cache = lambda text: [0.0] * 384
        m._embedder_state = "ready"

        assert m._get_search_capability_snapshot()["effective_path"] == "in-process-fallback"

    def test_health_never_launches_the_service_or_the_fallback(self, env, monkeypatch):
        m, fake, fallback_loads = env
        fake.probe_result = False

        m._get_search_capability_snapshot()
        m._get_search_capability_snapshot()

        assert fake.restart_callbacks == []
        assert fallback_loads == []

    def test_live_service_is_reported_and_reconfirmed(self, env):
        m, fake, _ = env
        m._embedder_service_state = "unavailable"
        fake.probe_result = True

        snap = m._get_search_capability_snapshot()

        assert snap["effective_path"] == "embedder-service"
        assert snap["embedder_service_state"] == "ready"
        assert snap["embedder_service_probe"] == "ok"


class TestServiceDisabledPathUnchanged:
    def test_disabled_never_probes_restarts_or_waits(self, env):
        m, fake, fallback_loads = env
        m.EMBEDDER_SERVICE_ENABLED = False
        m._EMBEDDER_RECOVERY_WAIT_S = 10.0
        fake.in_flight = True

        t0 = time.monotonic()
        assert m._get_embedder() is None
        assert time.monotonic() - t0 < 0.5
        assert fake.probe_calls == 0
        assert fake.restart_callbacks == []
        assert fake.embed_calls == 0
        assert fallback_loads  # in-process path is the only path and still gets started
        assert m._get_search_capability_snapshot()["embedder_service_probe"] == "not-probed"
