"""Real execution tests for the flagship runnable example: plan -> retrieve
(ACL-filtered) -> draft (governed model call) -> interrupt-gated approval ->
write (or discard). Every test here actually invokes a compiled LangGraph
StateGraph with a real SqliteSaver checkpointer. No API key required or used."""

from __future__ import annotations

from pathlib import Path

from langgraph.types import Command

from cc00_langchain.cc00_path import Document, FixedSizeChunker, RAGPipeline
from cc00_langchain.graphs.research_assistant import build_graph, in_memory_checkpointer

try:
    from langchain_core.language_models.fake_chat_models import FakeListChatModel
except ImportError:  # pragma: no cover
    FakeListChatModel = None


def _pipeline() -> RAGPipeline:
    pipeline = RAGPipeline(chunker=FixedSizeChunker(chunk_size=200), top_k=5)
    pipeline.ingest([Document(id="d1", text="LangGraph supports durable interrupts.", acl_roles=["public"])])
    return pipeline


def test_graph_pauses_at_the_approval_gate(tmp_path: Path):
    model = FakeListChatModel(responses=["Finding: LangGraph supports durable interrupts, per d1."])
    graph = build_graph(_pipeline(), model, in_memory_checkpointer(), tmp_path / "out")

    cfg = {"configurable": {"thread_id": "t-pause"}}
    result = graph.invoke({"question": "What does LangGraph support?", "user_role": "public"}, cfg)

    assert "__interrupt__" in result
    assert "LangGraph supports durable interrupts" in result["draft_report"]
    assert list((tmp_path / "out").glob("*.md")) == []  # nothing written before approval


def test_approval_writes_the_file(tmp_path: Path):
    model = FakeListChatModel(responses=["Finding: durable interrupts, per d1."])
    out_dir = tmp_path / "out"
    graph = build_graph(_pipeline(), model, in_memory_checkpointer(), out_dir)

    cfg = {"configurable": {"thread_id": "t-approve"}}
    graph.invoke({"question": "Approved question", "user_role": "public"}, cfg)
    result = graph.invoke(Command(resume={"approved": True}), cfg)

    assert result["status"] == "written"
    files = list(out_dir.glob("*.md"))
    assert len(files) == 1
    assert files[0].read_text(encoding="utf-8") == "Finding: durable interrupts, per d1."


def test_rejection_writes_nothing(tmp_path: Path):
    model = FakeListChatModel(responses=["Finding: durable interrupts, per d1."])
    out_dir = tmp_path / "out"
    graph = build_graph(_pipeline(), model, in_memory_checkpointer(), out_dir)

    cfg = {"configurable": {"thread_id": "t-reject"}}
    graph.invoke({"question": "Rejected question", "user_role": "public"}, cfg)
    result = graph.invoke(Command(resume={"approved": False}), cfg)

    assert result["status"] == "discarded"
    assert list(out_dir.glob("*.md")) == []


def test_acl_role_propagates_into_retrieval(tmp_path: Path):
    """A public-role thread must not retrieve a staff-only document, all the
    way through plan -> retrieve -> draft."""
    pipeline = RAGPipeline(chunker=FixedSizeChunker(chunk_size=200), top_k=5)
    pipeline.ingest(
        [
            Document(id="pub", text="Public fact about onboarding.", acl_roles=["public"]),
            Document(id="staff", text="Confidential staff-only compensation data.", acl_roles=["staff"]),
        ]
    )
    model = FakeListChatModel(responses=["draft"])
    graph = build_graph(pipeline, model, in_memory_checkpointer(), tmp_path / "out")

    cfg = {"configurable": {"thread_id": "t-acl"}}
    result = graph.invoke({"question": "Tell me about compensation", "user_role": "public"}, cfg)

    sources = {r["source"] for r in result["retrieved"]}
    assert "staff" not in sources


def test_handoff_packet_is_real_and_validated(tmp_path: Path):
    model = FakeListChatModel(responses=["draft"])
    graph = build_graph(_pipeline(), model, in_memory_checkpointer(), tmp_path / "out")

    cfg = {"configurable": {"thread_id": "t-handoff"}}
    result = graph.invoke({"question": "q", "user_role": "public"}, cfg)

    assert len(result["handoff_packets"]) == 1
    packet = result["handoff_packets"][0]
    assert packet["tier"] == "minimal"
    assert packet["task"].startswith("Retrieve evidence for:")


def test_filename_sanitization_handles_windows_invalid_characters(tmp_path: Path):
    """Regression test: a question containing '?' previously raised OSError on
    Windows (Invalid argument) because the filename was not sanitized."""
    model = FakeListChatModel(responses=["draft"])
    out_dir = tmp_path / "out"
    graph = build_graph(_pipeline(), model, in_memory_checkpointer(), out_dir)

    cfg = {"configurable": {"thread_id": "t-filename"}}
    graph.invoke({"question": 'What "breaks" the <filesystem>?', "user_role": "public"}, cfg)
    graph.invoke(Command(resume={"approved": True}), cfg)

    files = list(out_dir.glob("*.md"))
    assert len(files) == 1  # did not raise, and produced exactly one file
