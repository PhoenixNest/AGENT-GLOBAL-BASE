"""Loads CC-00 reference implementations under non-colliding package aliases.

Why this exists (research-report.md, § Addendum 2026-07-26, Finding 11): all four
CC-00 module roots contain a directory named `implementations/`, so the sys.path
convention used by CC-00's own test suites (core-component-00/CLAUDE.md, "Import
Path") can only ever expose one of them per process. This process needs several
at once — L2 for context assembly, L3 for the harness controls, L4 for retrieval,
L5 for handoffs — so this module registers each root's implementations/ directory
as a package under a unique alias instead.

VERIFIED 2026-07-27: this loader is exercised directly by
tests/test_cc00_path.py, which imports real classes from all four CC-00 module
roots through it and asserts they are the actual CC-00 implementations (by
checking the source file path each class was loaded from). Not a design sample —
this file is executed on every test run.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def _find_cc00_root(start: Path) -> Path:
    """Walk upward from this file until a directory named core-component-00 is found.

    Path-count arithmetic (parents[4]) breaks the moment this project moves one
    directory deeper or shallower. Walking up by name is one line longer and
    cannot silently point at the wrong directory.
    """
    for candidate in [start, *start.parents]:
        if candidate.name == "core-component-00":
            return candidate
    raise RuntimeError(
        f"Could not locate a 'core-component-00' ancestor directory above {start}. "
        "cc00_path.py must live somewhere under core-component-00/."
    )


CC00 = _find_cc00_root(Path(__file__).resolve())

_MODULE_ROOTS = {
    "cc00_ce": CC00 / "engineering" / "context-engineering",
    "cc00_he": CC00 / "engineering" / "harness-engineering",
    "cc00_mae": CC00 / "engineering" / "multi-agent-engineering",
    "cc00_rag": CC00 / "retrieval-augmented-generation",
}


def _register(alias: str, module_root: Path) -> ModuleType:
    """Bind <module_root>/implementations as a package named `alias`."""
    if alias in sys.modules:
        return sys.modules[alias]

    pkg_dir = module_root / "implementations"
    if not pkg_dir.is_dir():
        raise FileNotFoundError(f"CC-00 module root has no implementations/: {module_root}")

    spec = importlib.machinery.ModuleSpec(alias, loader=None, is_package=True)
    pkg = importlib.util.module_from_spec(spec)
    pkg.__path__ = [str(pkg_dir)]  # makes `alias.<submodule>` importable
    sys.modules[alias] = pkg
    return pkg


def _ensure_loaded() -> None:
    for alias, root in _MODULE_ROOTS.items():
        _register(alias, root)

    # memory_store.py uses the ABSOLUTE form `from implementations.reflection_authoring
    # import ...`, so it needs a top-level `implementations` binding too. Only one
    # module root can hold that name; Context Engineering is the only module that
    # needs it today. If a second module later adopts the absolute form, this fails
    # LOUDLY (ImportError from the wrong package) rather than silently importing the
    # wrong module — verified by test_cc00_path.py::test_memory_store_absolute_import.
    sys.modules.setdefault("implementations", sys.modules["cc00_ce"])


_ensure_loaded()

# --- Layer 2: Context Engineering -------------------------------------------------
_ctx = importlib.import_module("cc00_ce.context_assembler")
ContextAssembler = _ctx.ContextAssembler
AssembledContext = _ctx.AssembledContext
ContextItem = _ctx.ContextItem

# --- Layer 3: Harness Engineering -------------------------------------------------
_eb = importlib.import_module("cc00_he.error_boundary")
CircuitBreaker = _eb.CircuitBreaker
CircuitBreakerState = _eb.CircuitBreakerState
RateLimitError = _eb.RateLimitError
ValidationError = _eb.ValidationError
CC00TimeoutError = _eb.TimeoutError  # shadows the builtin — alias deliberately
ServiceUnavailableError = _eb.ServiceUnavailableError

_cm = importlib.import_module("cc00_he.context_monitor")
TokenBudgetManager = _cm.TokenBudgetManager
ContextMonitor = _cm.ContextMonitor

_tr = importlib.import_module("cc00_he.tool_registry")
ToolRegistry = _tr.ToolRegistry
TOOL_REGISTRY = _tr.TOOL_REGISTRY

# --- Layer 4: RAG ------------------------------------------------------------------
_chunker = importlib.import_module("cc00_rag.chunker")
Chunk = _chunker.Chunk
FixedSizeChunker = _chunker.FixedSizeChunker

_retrieval = importlib.import_module("cc00_rag.retrieval")
Document = _retrieval.Document
ScoredDocument = _retrieval.ScoredDocument
acl_filter = _retrieval.acl_filter
bm25_score = _retrieval.bm25_score
rrf_fusion = _retrieval.rrf_fusion

_pipe = importlib.import_module("cc00_rag.pipeline")
RAGPipeline = _pipe.RAGPipeline
RetrievedContext = _pipe.RetrievedContext

# --- Layer 5: Multi-Agent ----------------------------------------------------------
_hp = importlib.import_module("cc00_mae.handoff_packet")
HandoffPacket = _hp.HandoffPacket
HandoffTier = _hp.HandoffTier

__all__ = [
    "CC00",
    "ContextAssembler",
    "AssembledContext",
    "ContextItem",
    "CircuitBreaker",
    "CircuitBreakerState",
    "RateLimitError",
    "ValidationError",
    "CC00TimeoutError",
    "ServiceUnavailableError",
    "TokenBudgetManager",
    "ContextMonitor",
    "ToolRegistry",
    "TOOL_REGISTRY",
    "Chunk",
    "FixedSizeChunker",
    "Document",
    "ScoredDocument",
    "acl_filter",
    "bm25_score",
    "rrf_fusion",
    "RAGPipeline",
    "RetrievedContext",
    "HandoffPacket",
    "HandoffTier",
]
