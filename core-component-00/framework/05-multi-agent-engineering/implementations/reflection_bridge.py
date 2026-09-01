"""
Production wiring between SwarmOrchestrator's reflection-retrieval hook and
agent-memory's real search_memory core.

swarm_orchestrator.py deliberately never hard-imports the agent-memory MCP
server (see SwarmOrchestrator.set_reflection_search_fn's docstring) — this
module is the glue that lives outside that boundary. It loads
mcp-servers/agent-memory/server.py directly from its file path (not via
sys.path/package import, since agent-memory is a standalone script module,
not a package this module's own package hierarchy contains) and calls its
already-importable, testable core (`_search_memory_impl`) with
memory_type="reflection" — the exact same function search_memory()'s
@mcp.tool() wrapper calls, so this is the real read path, not a
reimplementation of it.

Loading is deferred to first call, not module import, for two reasons: (1)
importing server.py pulls in fastmcp, qdrant_client, and (indirectly)
sentence_transformers — dependencies this pure-orchestration package does not
otherwise require and may not have installed in every environment that runs
its test suite; (2) server.py's module body starts the same embedder-service
warm-up thread a live agent-memory MCP process starts on launch. Deferring
the import means paying that cost only when a caller actually wires this
bridge into a running orchestrator, not merely by importing this file.

Never raises: every failure mode (agent-memory's dependencies not installed,
the module file missing, qdrant-memory unreachable, the embedder still
warming up) is caught and returned as the same
{"results": [], "count": 0, "degraded": True, "reason": ...} shape
search_memory() and SwarmOrchestrator._retrieve_reflections already use —
no new failure-mode class is introduced at this call site.

Read-only. This bridge only ever calls into agent-memory's search_memory
core; it does not add, expose, or reopen any write path — agent-memory's MCP
server deliberately has no write tool (see .claude/rules/mcp-governance.md).
"""

import contextlib
import sys
import threading
import types
from pathlib import Path
from typing import Any, Callable, Dict, Optional

_AGENT_MEMORY_SERVER_PATH = (
    Path(__file__).resolve().parents[3] / "platform" / "model-context-protocol-servers" / "agent-memory" / "server.py"
)
_MODULE_NAME = "cc00_agent_memory_server_bridge"

# The two "implementations" directories agent-memory/server.py's own import
# graph actually needs: server.py imports memory_vector_store.py and
# memory_store.py (context-engineering), and memory_vector_store.py in turn
# imports error_boundary.py (harness-engineering) via
# `from implementations.error_boundary import ...`. Neither directory has an
# __init__.py — by design, these two are meant to combine into a single
# PEP 420 namespace package when both are the only things on sys.path, which
# is exactly what happens when either module's own test suite runs standalone
# (see core-component-00/CLAUDE.md's "run tests per-module" convention).
_CONTEXT_ENGINEERING_IMPLEMENTATIONS_DIR = (
    Path(__file__).resolve().parents[3] / "framework" / "02-context-engineering" / "implementations"
)
_HARNESS_ENGINEERING_IMPLEMENTATIONS_DIR = (
    Path(__file__).resolve().parents[3] / "framework" / "03-harness-engineering" / "implementations"
)

_module_lock = threading.Lock()
_module_cache: Optional[Any] = None
_module_load_error: Optional[str] = None


@contextlib.contextmanager
def _isolated_implementations_namespace():
    """
    agent-memory/server.py does `from implementations.memory_vector_store
    import ...`, and memory_vector_store.py itself does both a relative
    `from .memory_store import ...` and an absolute
    `from implementations.error_boundary import ...` (harness-engineering).
    All of that is meant to resolve against a namespace package spanning
    context-engineering/implementations/ + harness-engineering/implementations/
    — neither has an __init__.py, so PEP 420 merges them automatically when
    those are the only "implementations" directories in play.

    But this bridge lives in multi-agent-engineering/implementations/ — a
    *different*, regular package (it has __init__.py) that also happens to
    be named `implementations`. Any real caller that has already imported
    SwarmOrchestrator via `from implementations.swarm_orchestrator import
    ...` has necessarily already registered that regular package under the
    plain name "implementations" in sys.modules. Merely clearing that cache
    entry and re-resolving via sys.path is NOT sufficient — reproduced live:
    Python's import system prefers a regular package (found via __init__.py)
    over a namespace-package portion at ANY sys.path position, so as long as
    multi-agent-engineering's directory is anywhere on sys.path (which it
    always is here), a fresh "implementations" import still resolves to it,
    not to the context/harness-engineering namespace merge — raising
    `ModuleNotFoundError: No module named 'implementations.memory_vector_store'`
    regardless of insertion order.

    The fix: bypass sys.path search entirely for the duration of the load.
    Install a synthetic `implementations` module in sys.modules with
    `__path__` set explicitly to [context-engineering, harness-engineering]
    implementations dirs. Submodule imports (relative or absolute, e.g.
    `implementations.error_boundary`) resolve via the parent package's
    `__path__`, not sys.path, once the parent is already in sys.modules —
    which is exactly why this is deterministic regardless of what else is on
    sys.path. Restores exactly what was there before on exit, so a caller's
    own `implementations` package (e.g. swarm_orchestrator's) is left
    untouched on either side of the call.
    """
    saved = {
        name: mod
        for name, mod in sys.modules.items()
        if name == "implementations" or name.startswith("implementations.")
    }
    for name in saved:
        del sys.modules[name]

    fake_pkg = types.ModuleType("implementations")
    fake_pkg.__path__ = [
        str(_CONTEXT_ENGINEERING_IMPLEMENTATIONS_DIR),
        str(_HARNESS_ENGINEERING_IMPLEMENTATIONS_DIR),
    ]
    sys.modules["implementations"] = fake_pkg
    try:
        yield
    finally:
        for name in list(sys.modules.keys()):
            if name == "implementations" or name.startswith("implementations."):
                del sys.modules[name]
        sys.modules.update(saved)


def _load_agent_memory_server() -> Any:
    """
    Loads mcp-servers/agent-memory/server.py as a uniquely-named module,
    cached for the life of this process. Raises on failure — callers (below)
    are responsible for catching and degrading; this function stays a plain
    loader so its own tests can assert on the raised exception directly.
    """
    global _module_cache, _module_load_error
    with _module_lock:
        if _module_cache is not None:
            return _module_cache
        if _module_load_error is not None:
            raise RuntimeError(_module_load_error)
        import importlib.util

        if not _AGENT_MEMORY_SERVER_PATH.exists():
            _module_load_error = f"agent-memory server.py not found at {_AGENT_MEMORY_SERVER_PATH}"
            raise RuntimeError(_module_load_error)
        try:
            spec = importlib.util.spec_from_file_location(_MODULE_NAME, _AGENT_MEMORY_SERVER_PATH)
            module = importlib.util.module_from_spec(spec)
            sys.modules[_MODULE_NAME] = module
            with _isolated_implementations_namespace():
                spec.loader.exec_module(module)
        except Exception as exc:
            sys.modules.pop(_MODULE_NAME, None)
            _module_load_error = f"failed to load agent-memory server.py: {exc}"
            raise
        _module_cache = module
        return module


def build_agent_memory_reflection_search_fn(top_k: int = 5) -> Callable[[str], Dict[str, Any]]:
    """
    Returns a callable matching SwarmOrchestrator.set_reflection_search_fn's
    contract — fn(task_description) -> {"results": [...], "count": int,
    "degraded": bool, "reason": str|None} — backed by agent-memory's real
    search_memory(memory_type="reflection") core.

    session_id/cross_session are inert for memory_type="reflection" (only
    episodic search checks them, per _search_memory_impl) but are passed
    explicitly for signature clarity rather than relying on that internal
    detail.
    """

    def _search(task_description: str) -> Dict[str, Any]:
        try:
            server = _load_agent_memory_server()
            return server._search_memory_impl(
                query=task_description,
                memory_type="reflection",
                top_k=top_k,
                session_id=None,
                cross_session=True,
                include_dormant=False,
                include_archived=False,
                client=server._get_memory_client(),
                embedder=server._get_embedder(),
                embedder_unavailable_reason=server._get_embedder_unavailable_reason(),
            )
        except Exception as exc:
            return {
                "results": [],
                "count": 0,
                "degraded": True,
                "reason": f"agent-memory reflection bridge unavailable: {exc}",
            }

    return _search


def wire_reflection_retrieval(orchestrator: Any, top_k: int = 5) -> None:
    """
    Convenience one-liner for production call sites: binds `orchestrator`
    (a SwarmOrchestrator instance) to agent-memory's real reflection search.
    Equivalent to:
        orchestrator.set_reflection_search_fn(build_agent_memory_reflection_search_fn(top_k))
    """
    orchestrator.set_reflection_search_fn(build_agent_memory_reflection_search_fn(top_k))
