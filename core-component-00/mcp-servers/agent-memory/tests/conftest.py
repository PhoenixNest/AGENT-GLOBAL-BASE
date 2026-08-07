"""
Shared fixtures for the agent-memory test suite.

Sets EMBEDDER_SERVICE_ENABLED=false before agent-memory/server.py (or
workspace-knowledge/server.py) is first imported, so importing either module
during a unit-test run never attempts to probe for or launch the shared
embedder-service subprocess (embedder_client.ensure_service_running() spawns
a real subprocess when the service isn't already up) — per this suite's "no
live network calls required for unit tests" discipline. This only changes
what happens at *import* time; individual tests are still free to monkeypatch
EMBEDDER_SERVICE_ENABLED/_embedder_service_state back to any value to exercise
a specific state combination.

Both agent-memory/server.py and workspace-knowledge/server.py are literally
named server.py, so they cannot both be imported as a bare `import server` in
the same process — the second import would silently return the first module
from sys.modules. Both are loaded here via importlib with distinct module
names (agent_memory_server / workspace_knowledge_server) instead, and cached
in sys.modules so repeated fixture use within one test session doesn't
re-run module-level side effects (background thread starts, sys.path
mutation, SearchEngine construction) more than once.
"""
import importlib.util
import os
import sys
from pathlib import Path

import pytest

os.environ.setdefault("EMBEDDER_SERVICE_ENABLED", "false")

_MCP_SERVERS_ROOT = Path(__file__).resolve().parents[2]
_AGENT_MEMORY_SERVER_PATH = _MCP_SERVERS_ROOT / "agent-memory" / "server.py"
_WORKSPACE_KNOWLEDGE_SERVER_PATH = _MCP_SERVERS_ROOT / "workspace-knowledge" / "server.py"


def _load_module(module_name: str, file_path: Path):
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def agent_memory_server():
    """The real agent-memory/server.py module, imported once per test session."""
    return _load_module("agent_memory_server", _AGENT_MEMORY_SERVER_PATH)


@pytest.fixture
def reset_embedder_globals(agent_memory_server):
    """
    Snapshots and restores every module-level embedder-state global
    agent_memory_server exposes, so tests that intentionally set these
    globals to exercise a specific state combination (e.g.
    _get_search_capability_snapshot()'s four effective_path branches) never
    leak state into a later test. Use as a fixture dependency in any test
    that assigns to agent_memory_server.EMBEDDER_SERVICE_ENABLED,
    agent_memory_server._embedder_service_state,
    agent_memory_server._embedder_state, or
    agent_memory_server._embedder_cache.
    """
    m = agent_memory_server
    snapshot = dict(
        EMBEDDER_SERVICE_ENABLED=m.EMBEDDER_SERVICE_ENABLED,
        _embedder_service_state=m._embedder_service_state,
        _embedder_state=m._embedder_state,
        _embedder_cache=m._embedder_cache,
        _embedder_load_started=m._embedder_load_started,
    )
    yield m
    m.EMBEDDER_SERVICE_ENABLED = snapshot["EMBEDDER_SERVICE_ENABLED"]
    m._embedder_service_state = snapshot["_embedder_service_state"]
    m._embedder_state = snapshot["_embedder_state"]
    m._embedder_cache = snapshot["_embedder_cache"]
    m._embedder_load_started = snapshot["_embedder_load_started"]
