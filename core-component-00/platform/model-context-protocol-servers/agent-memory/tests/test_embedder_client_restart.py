"""
embedder_client.request_service_restart(): non-blocking, single-flight per
process, cooldown-gated, never raises. ensure_service_running() is replaced
by a controllable stub, so no test here launches or probes a real service.
"""
import sys
import threading
import time
import types
from pathlib import Path

import pytest

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
import embedder_client  # noqa: E402


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(embedder_client, "_restart_in_flight", False)
    monkeypatch.setattr(embedder_client, "_restart_last_started_at", 0.0)
    monkeypatch.setattr(embedder_client, "_restart_waiters", [])
    monkeypatch.setattr(embedder_client, "RESTART_COOLDOWN_S", 0.3)
    return embedder_client


def _wait_until(predicate, timeout=3.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return False


def test_request_returns_immediately_while_the_launch_blocks(client, monkeypatch):
    release = threading.Event()
    monkeypatch.setattr(client, "ensure_service_running", lambda: release.wait(5) or True)
    done = []

    t0 = time.monotonic()
    started = client.request_service_restart(on_done=done.append)

    assert started is True
    assert time.monotonic() - t0 < 0.5
    assert client.restart_in_flight() is True
    release.set()
    assert _wait_until(lambda: done == [True])
    assert _wait_until(lambda: not client.restart_in_flight())


def test_concurrent_requests_share_one_launch_and_all_callbacks_fire(client, monkeypatch):
    release = threading.Event()
    launches = []

    def _ensure():
        launches.append(1)
        release.wait(5)
        return True

    monkeypatch.setattr(client, "ensure_service_running", _ensure)
    first, second = [], []

    assert client.request_service_restart(on_done=first.append) is True
    assert client.request_service_restart(on_done=second.append) is False
    release.set()

    assert _wait_until(lambda: first == [True] and second == [True])
    assert launches == [1]


def test_cooldown_suppresses_a_request_right_after_a_launch(client, monkeypatch):
    launches = []
    monkeypatch.setattr(client, "ensure_service_running", lambda: launches.append(1) or False)

    assert client.request_service_restart() is True
    assert _wait_until(lambda: not client.restart_in_flight())
    assert client.request_service_restart() is False  # inside the cooldown
    time.sleep(0.4)
    assert client.request_service_restart() is True
    assert _wait_until(lambda: len(launches) == 2)


def test_failed_launch_reports_false(client, monkeypatch):
    monkeypatch.setattr(client, "ensure_service_running", lambda: False)
    done = []

    client.request_service_restart(on_done=done.append)

    assert _wait_until(lambda: done == [False])


def test_never_raises_when_the_launch_raises(client, monkeypatch):
    def _boom():
        raise OSError("cannot spawn")

    monkeypatch.setattr(client, "ensure_service_running", _boom)
    done = []

    client.request_service_restart(on_done=done.append)

    assert _wait_until(lambda: done == [False])
    assert _wait_until(lambda: not client.restart_in_flight())


def test_a_raising_callback_does_not_stop_the_others(client, monkeypatch):
    release = threading.Event()
    monkeypatch.setattr(client, "ensure_service_running", lambda: release.wait(5) or True)
    later = []

    def _bad(ok):
        raise RuntimeError("callback bug")

    client.request_service_restart(on_done=_bad)
    client.request_service_restart(on_done=later.append)
    release.set()

    assert _wait_until(lambda: later == [True])
    assert _wait_until(lambda: not client.restart_in_flight())


def test_never_raises_when_the_thread_cannot_start(client, monkeypatch):
    class _BrokenThread:
        def __init__(self, *a, **k):
            pass

        def start(self):
            raise RuntimeError("can't start new thread")

    # Scoped to the client module's own `threading` name; the real threading
    # module (used by pytest and everything else) is untouched.
    monkeypatch.setattr(client, "threading", types.SimpleNamespace(Thread=_BrokenThread, Lock=threading.Lock))

    assert client.request_service_restart(on_done=lambda ok: None) is False
    assert client.restart_in_flight() is False
