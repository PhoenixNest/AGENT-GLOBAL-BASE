"""Proves Finding 11's fix actually works: real CC-00 code, loaded from all four
module roots in one process, including the two harder cases (an absolute
`from implementations....` import and a module with its own internal relative
imports)."""

from __future__ import annotations

import importlib

from cc00_langchain import cc00_path as cp


def test_cc00_root_resolves_to_the_real_directory():
    assert cp.CC00.name == "core-component-00"
    assert (cp.CC00 / "engineering").is_dir()
    assert (cp.CC00 / "retrieval-augmented-generation").is_dir()


def test_layer2_context_assembler_is_the_real_cc00_class():
    assembler = cp.ContextAssembler(max_tokens=1000)
    assembler.set_system("system content")
    result = assembler.build(task_type="factual_qa")
    assert result.total_tokens > 0
    # Loaded from the real file, not a stand-in — assert the source location.
    source_file = importlib.import_module("cc00_ce.context_assembler").__file__
    assert "context-engineering" in source_file.replace("\\", "/")


def test_layer3_harness_classes_are_real():
    breaker = cp.CircuitBreaker()
    assert breaker.is_open() is False
    registry = cp.ToolRegistry(cp.TOOL_REGISTRY)
    assert registry.is_allowed_tool("search") is True
    assert registry.is_allowed_tool("not_a_real_tool") is False


def test_layer4_rag_pipeline_is_real():
    pipeline = cp.RAGPipeline(chunker=cp.FixedSizeChunker(chunk_size=100), top_k=3)
    doc = cp.Document(id="d1", text="hello world", acl_roles=["public"])
    n = pipeline.ingest([doc])
    assert n >= 1


def test_layer5_handoff_packet_is_real():
    packet = cp.HandoffPacket(tier=cp.HandoffTier.MINIMAL, task="do the thing")
    assert packet.validate() == []


def test_memory_store_absolute_import_fix():
    """Finding 11's second failure mode: `memory_store.py` does
    `from implementations.reflection_authoring import ...` (absolute form).
    Only works if `sys.modules["implementations"]` was registered — verify it
    resolves to the real module and not an accidental shadow."""
    memstore = importlib.import_module("cc00_ce.memory_store")
    assert hasattr(memstore, "EpisodicMemory")
    episodic = memstore.EpisodicMemory(session_id="test")
    event = episodic.record_event("decision", "chose option A")
    assert event.content == "chose option A"


def test_swarm_orchestrator_internal_relative_imports_resolve():
    """`swarm_orchestrator.py` does `from .handoff_packet import ...` and
    `from .shared_memory_log import ...` — both must resolve within the
    aliased `cc00_mae` package, not against this project's own package."""
    swarm = importlib.import_module("cc00_mae.swarm_orchestrator")
    assert hasattr(swarm, "SwarmOrchestrator")
    assert hasattr(swarm, "SwarmTopology")
