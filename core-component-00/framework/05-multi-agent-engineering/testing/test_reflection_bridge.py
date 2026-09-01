"""
Tests for reflection_bridge — production wiring between SwarmOrchestrator's
reflection-retrieval hook and agent-memory's real search_memory core.

agent-memory/server.py's own dependencies (fastmcp, qdrant_client,
sentence_transformers) are not installed in this module's test environment
by design (see multi-agent-engineering/CLAUDE.md — this module has no
dependency on the MCP servers' stack). That absence is itself part of what
these tests verify: the bridge must degrade gracefully rather than raise
when agent-memory cannot be loaded, exactly as it would in production if
qdrant-memory or the embedder were unavailable. Delegation logic against
agent-memory's real _search_memory_impl signature is verified separately by
injecting a fake loaded module, so the exact parameter wiring is checked
without requiring those heavy dependencies to be present.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations import reflection_bridge
from implementations.swarm_orchestrator import AgentProfile, SwarmConfig, SwarmOrchestrator


@pytest.fixture(autouse=True)
def _reset_bridge_cache():
    """Each test gets a clean loader cache — otherwise whichever test loads
    (or fails to load) the real module first would leak its cached result
    into every later test."""
    reflection_bridge._module_cache = None
    reflection_bridge._module_load_error = None
    sys.modules.pop(reflection_bridge._MODULE_NAME, None)
    yield
    reflection_bridge._module_cache = None
    reflection_bridge._module_load_error = None
    sys.modules.pop(reflection_bridge._MODULE_NAME, None)


class TestGracefulDegradation:
    """agent-memory's real dependencies are not installed in this test
    environment — _load_agent_memory_server is expected to fail here, and
    the bridge must turn that into a degraded result, never an exception."""

    def test_missing_dependencies_degrade_not_raise(self):
        fn = reflection_bridge.build_agent_memory_reflection_search_fn()
        result = fn("clean up the worktree before merging")

        assert result["results"] == []
        assert result["count"] == 0
        assert result["degraded"] is True
        assert "agent-memory reflection bridge unavailable" in result["reason"]

    def test_missing_server_file_degrades_not_raise(self, monkeypatch):
        monkeypatch.setattr(
            reflection_bridge,
            "_AGENT_MEMORY_SERVER_PATH",
            Path(__file__).parent / "does-not-exist" / "server.py",
        )
        fn = reflection_bridge.build_agent_memory_reflection_search_fn()
        result = fn("task")

        assert result == {
            "results": [],
            "count": 0,
            "degraded": True,
            "reason": (
                "agent-memory reflection bridge unavailable: "
                f"agent-memory server.py not found at {reflection_bridge._AGENT_MEMORY_SERVER_PATH}"
            ),
        }

    def test_load_failure_is_cached_not_retried_every_call(self, monkeypatch):
        """A second call after a failed load must not re-attempt the
        (expensive, side-effecting) import — it should reuse the cached
        error immediately."""
        monkeypatch.setattr(
            reflection_bridge,
            "_AGENT_MEMORY_SERVER_PATH",
            Path(__file__).parent / "does-not-exist" / "server.py",
        )
        fn = reflection_bridge.build_agent_memory_reflection_search_fn()
        fn("first call")
        assert reflection_bridge._module_load_error is not None

        # Move the path back to a real (loadable-looking) location; the
        # cached failure must still win, proving no re-attempt happened.
        monkeypatch.setattr(
            reflection_bridge,
            "_AGENT_MEMORY_SERVER_PATH",
            Path(__file__).parent.parent.parent.parent
            / "platform"
            / "model-context-protocol-servers"
            / "agent-memory"
            / "server.py",
        )
        result = fn("second call")
        assert result["degraded"] is True


class TestDelegationToRealSearchCore:
    """Verifies the bridge calls agent-memory's real _search_memory_impl
    signature correctly, by injecting a fake loaded module rather than
    requiring fastmcp/qdrant_client/sentence_transformers to be installed
    in this test environment."""

    def _install_fake_module(self, monkeypatch, search_memory_impl):
        class _FakeServerModule:
            def _get_memory_client(self):
                return "fake-client"

            def _get_embedder(self):
                return "fake-embedder"

            def _get_embedder_unavailable_reason(self):
                return "unused"

            _search_memory_impl = staticmethod(search_memory_impl)

        fake_module = _FakeServerModule()
        monkeypatch.setattr(reflection_bridge, "_module_cache", fake_module)
        return fake_module

    def test_calls_search_memory_impl_with_reflection_contract(self, monkeypatch):
        captured = {}

        def fake_search_memory_impl(**kwargs):
            captured.update(kwargs)
            return {"results": [], "count": 0, "degraded": False, "reason": None}

        self._install_fake_module(monkeypatch, fake_search_memory_impl)

        fn = reflection_bridge.build_agent_memory_reflection_search_fn(top_k=7)
        result = fn("remediate the flaky CI worktree cleanup")

        assert captured["query"] == "remediate the flaky CI worktree cleanup"
        assert captured["memory_type"] == "reflection"
        assert captured["top_k"] == 7
        assert captured["include_dormant"] is False
        assert captured["include_archived"] is False
        assert captured["client"] == "fake-client"
        assert captured["embedder"] == "fake-embedder"
        assert result["degraded"] is False

    def test_default_top_k_is_five(self, monkeypatch):
        captured = {}

        def fake_search_memory_impl(**kwargs):
            captured.update(kwargs)
            return {"results": [], "count": 0, "degraded": False, "reason": None}

        self._install_fake_module(monkeypatch, fake_search_memory_impl)
        reflection_bridge.build_agent_memory_reflection_search_fn()("task")
        assert captured["top_k"] == 5

    def test_populated_reflection_result_passes_through_unchanged(self, monkeypatch):
        payload = {
            "results": [{"reflection_id": "REFLECT-004", "summary": "Check orchestrator briefs."}],
            "count": 1,
            "degraded": False,
            "reason": None,
        }
        self._install_fake_module(monkeypatch, lambda **kwargs: payload)

        result = reflection_bridge.build_agent_memory_reflection_search_fn()("task")
        assert result == payload

    def test_exception_from_real_search_core_degrades_not_raises(self, monkeypatch):
        def failing_search_memory_impl(**kwargs):
            raise TimeoutError("qdrant-memory call exceeded hard timeout")

        self._install_fake_module(monkeypatch, failing_search_memory_impl)

        result = reflection_bridge.build_agent_memory_reflection_search_fn()("task")
        assert result["degraded"] is True
        assert result["count"] == 0
        assert "qdrant-memory call exceeded hard timeout" in result["reason"]


class TestImplementationsNamespaceCollision:
    """Reproduces, with stdlib only (no fastmcp/qdrant_client needed), the
    real collision hit during a live smoke test: this test module itself
    imports `from implementations.swarm_orchestrator import ...` above,
    which registers multi-agent-engineering's *regular* package (it has
    __init__.py) under the plain name "implementations" in sys.modules.
    agent-memory's real dependency chain needs "implementations" to instead
    resolve as a namespace package spanning context-engineering/implementations
    (relative import: memory_vector_store.py's `from .memory_store import
    ...`) + harness-engineering/implementations (absolute cross-package
    import: memory_vector_store.py's `from implementations.error_boundary
    import ...`) — reproduced here with fake stand-ins for both directories
    and both import styles, so the fix is verified without needing
    agent-memory's heavy dependencies installed."""

    @pytest.fixture
    def fake_agent_memory_server(self, tmp_path, monkeypatch):
        fake_context_dir = tmp_path / "fake_context_engineering_implementations"
        fake_harness_dir = tmp_path / "fake_harness_engineering_implementations"
        fake_context_dir.mkdir()
        fake_harness_dir.mkdir()

        (fake_context_dir / "fake_memory_store.py").write_text("MARKER = 'context-value'\n")
        (fake_harness_dir / "fake_error_boundary.py").write_text("MARKER = 'harness-value'\n")
        # Mirrors memory_vector_store.py's real two import styles: relative
        # (same namespace-package "directory") and absolute cross-directory.
        (fake_context_dir / "fake_memory_vector_store.py").write_text(
            "from .fake_memory_store import MARKER as store_marker\n"
            "from implementations.fake_error_boundary import MARKER as harness_marker\n"
            "COMBINED = f'{store_marker}+{harness_marker}'\n"
        )

        server_path = tmp_path / "fake_server.py"
        server_path.write_text(
            "from implementations.fake_memory_vector_store import COMBINED\n"
            "def get_combined():\n"
            "    return COMBINED\n"
        )

        monkeypatch.setattr(reflection_bridge, "_CONTEXT_ENGINEERING_IMPLEMENTATIONS_DIR", fake_context_dir)
        monkeypatch.setattr(reflection_bridge, "_HARNESS_ENGINEERING_IMPLEMENTATIONS_DIR", fake_harness_dir)
        monkeypatch.setattr(reflection_bridge, "_AGENT_MEMORY_SERVER_PATH", server_path)
        return server_path

    def test_collision_is_isolated_and_restored(self, fake_agent_memory_server):
        # Simulate the real-world precondition: multi-agent-engineering's own
        # regular "implementations" package is already registered under the
        # plain name, exactly as it is in this test module after the
        # top-of-file `from implementations.swarm_orchestrator import ...`.
        real_implementations_pkg = sys.modules["implementations"]
        assert not hasattr(real_implementations_pkg, "fake_memory_vector_store")

        loaded = reflection_bridge._load_agent_memory_server()

        # Proves both the relative import (fake_memory_store, same
        # directory) and the absolute cross-directory import
        # (fake_error_boundary, the other directory) resolved correctly.
        assert loaded.get_combined() == "context-value+harness-value"

        # The caller's own "implementations" package must be exactly as it
        # was before the call — not replaced by the synthetic namespace pkg.
        assert sys.modules["implementations"] is real_implementations_pkg
        from implementations.swarm_orchestrator import SwarmOrchestrator  # noqa: F401 — must still resolve


class TestWireReflectionRetrieval:
    """End-to-end: wire_reflection_retrieval must bind the orchestrator's
    hook such that SwarmOrchestrator._retrieve_reflections actually calls
    through to the (fake, injected) agent-memory search core."""

    @pytest.fixture
    def agents(self):
        return [AgentProfile(agent_id="a1", name="Agent", role="backend", expertise=["backend"])]

    def test_wire_binds_orchestrator_to_bridge(self, monkeypatch, agents):
        captured = {}

        def fake_search_memory_impl(**kwargs):
            captured.update(kwargs)
            return {"results": [], "count": 0, "degraded": False, "reason": None}

        class _FakeServerModule:
            def _get_memory_client(self):
                return "fake-client"

            def _get_embedder(self):
                return "fake-embedder"

            def _get_embedder_unavailable_reason(self):
                return "unused"

            _search_memory_impl = staticmethod(fake_search_memory_impl)

        monkeypatch.setattr(reflection_bridge, "_module_cache", _FakeServerModule())

        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join")
        orch = SwarmOrchestrator(config=config, agents=agents)
        reflection_bridge.wire_reflection_retrieval(orch, top_k=3)

        notes = orch._retrieve_reflections("investigate the reflection wiring")

        assert notes == []
        assert captured["memory_type"] == "reflection"
        assert captured["top_k"] == 3
        assert captured["query"] == "investigate the reflection wiring"
