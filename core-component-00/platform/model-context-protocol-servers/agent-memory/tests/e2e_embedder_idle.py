"""
Real end-to-end check of recovery after embedder-service's idle self-shutdown.
Run directly with agent-memory's venv interpreter:

    agent-memory/.venv/Scripts/python.exe agent-memory/tests/e2e_embedder_idle.py

Runs an isolated embedder-service (port EMBEDDER_E2E_PORT, default 8793, with
its own lock/pid directory and a 5s idle timeout) so the default instance on
8791 and its run files are never touched, then:

  1. imports agent-memory/server.py (which launches the isolated service)
     and embeds through the server's resolver;
  2. waits past the idle shutdown and confirms the port is closed;
  3. embeds again through the resolver while the cached state still says
     "ready" (runtime-failure path) and checks a real vector comes back from
     a relaunched service (different pid);
  4. repeats with an aged cache entry (stale-"ready" re-probe path);
  5. stops the isolated service.

Sibling cleanup is disabled for the imported server so it cannot terminate a
live agent-memory process. Exits 0 on success. No Qdrant is contacted.
"""
import json
import os
import socket
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

PORT = int(os.environ.get("EMBEDDER_E2E_PORT", "8793"))
RUN_DIR = tempfile.mkdtemp(prefix="embedder-e2e-run-")
os.environ.update(
    {
        "EMBEDDER_SERVICE_PORT": str(PORT),
        "EMBEDDER_SERVICE_IDLE_TIMEOUT_S": "5",
        "EMBEDDER_SERVICE_IDLE_CHECK_INTERVAL_S": "1",
        "EMBEDDER_SERVICE_RUN_DIR": RUN_DIR,
        "EMBEDDER_SERVICE_ENABLED": "true",
        "AGENT_MEMORY_ENABLE_SIBLING_CLEANUP": "false",
        "NO_PROXY": "localhost,127.0.0.1",
    }
)
assert PORT != 8791, "refusing to run against the default instance"

SERVER_PATH = Path(__file__).resolve().parents[1] / "server.py"
T0 = time.time()


def say(msg):
    print(f"[e2e +{time.time() - T0:6.2f}s] {msg}", flush=True)


def port_open():
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


def service_pid():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=2) as r:
            return json.loads(r.read())["pid"]
    except Exception:
        return None


def wait_for(predicate, timeout, what):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return
        time.sleep(0.25)
    raise SystemExit(f"FAIL: timed out waiting for {what}")


def main():
    import importlib.util

    sys.path.insert(0, str(SERVER_PATH.parent))  # server.py imports its sibling modules by bare name
    spec = importlib.util.spec_from_file_location("agent_memory_server", SERVER_PATH)
    m = importlib.util.module_from_spec(spec)
    sys.modules["agent_memory_server"] = m
    spec.loader.exec_module(m)
    say(f"imported server; isolated service port={PORT} run_dir={RUN_DIR}")

    t = time.time()
    wait_for(lambda: m._embedder_service_state == "ready", 120, "initial service launch")
    say(f"service launched and ready {time.time() - t:.2f}s after import (state={m._embedder_service_state})")
    pid1 = service_pid()

    embed = m._get_embedder()
    vec = embed("end to end idle recovery")
    assert len(vec) == 384, len(vec)
    say(f"embed #1 via resolver ok (dim={len(vec)}) service_pid={pid1}")

    for round_no, aged in ((1, False), (2, True)):
        wait_for(lambda: not port_open(), 60, "idle shutdown")
        say(f"round {round_no}: port {PORT} closed after idle shutdown (pid {service_pid()}); cached state={m._embedder_service_state}")
        if aged:
            m._embedder_service_state_confirmed_at = time.time() - 120.0
            say("round 2: cached 'ready' aged by 120s (stale re-probe path)")

        t = time.time()
        embed = m._get_embedder()
        resolver_s = time.time() - t
        assert embed is not None, "resolver returned None: no embedder path at all"
        vec = embed("after idle")
        total_s = time.time() - t
        assert len(vec) == 384, len(vec)
        in_process_ready = m._get_in_process_embedder() is not None
        say(
            f"round {round_no}: resolver took {resolver_s:.2f}s, first embed done {total_s:.2f}s after the call "
            f"(in-process embedder loaded: {in_process_ready})"
        )
        # The relaunch runs in the background; when an in-process embedder is
        # already loaded the call above does not wait for it.
        t = time.time()
        wait_for(lambda: service_pid() is not None, 60, "background relaunch")
        new_pid = service_pid()
        say(f"round {round_no}: relaunched service answering {time.time() - t:.2f}s after the embed, pid={new_pid}")
        assert new_pid != pid1, "service pid unchanged: it was not relaunched"
        wait_for(lambda: m._embedder_service_ready(), 10, "resolver to see the relaunched service")
        assert m._embedder_service_state == "ready"
        vec = m._get_embedder()("served by the relaunched service")
        assert len(vec) == 384
        pid1 = new_pid

    say("shutting down isolated service")
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{PORT}/shutdown", data=b"{}", method="POST")
        urllib.request.urlopen(req, timeout=3).read()
    except Exception:
        pass
    wait_for(lambda: not port_open(), 20, "final shutdown")
    say("PASS")


if __name__ == "__main__":
    # os._exit: the imported server may have a background model-load thread
    # running that must not hold the process open.
    try:
        main()
    except BaseException as exc:  # includes SystemExit from wait_for
        import traceback

        traceback.print_exc()
        print(f"[e2e] FAIL: {exc}", flush=True)
        sys.stdout.flush()
        os._exit(1)
    sys.stdout.flush()
    os._exit(0)
