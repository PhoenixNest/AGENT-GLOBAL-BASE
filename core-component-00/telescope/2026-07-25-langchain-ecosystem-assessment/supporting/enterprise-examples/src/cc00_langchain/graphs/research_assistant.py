"""The Telescope Research Assistant — a runnable subset of `supporting/06`.

Demonstrates, for real (see tests/test_research_assistant_graph.py, which
executes every path below with no API key required):

  - Deterministic task decomposition (ASGF L5 Mandatory) — `plan_node`
  - A tiered Context Handoff Protocol packet (ASGF L5 Mandatory) — `retrieve_node`,
    using the real `HandoffPacket`/`HandoffTier` from CC-00, not a description of one
  - ACL-filtered retrieval (ASGF L4 Required) via CC-00's `RAGPipeline`, with the
    role closure-bound per Finding 14 — `retrieve_node`
  - A model call wrapped in the full CC-00 governance middleware stack — `draft_node`
  - `interrupt()`-gated human approval before any write (ASGF L3 Required) — `approval_gate`
  - A confined, gated filesystem write — `write_node`

SCOPE BOUNDARY (honest, not hidden): `supporting/06 §4.4` demonstrates
schema-constrained structured output (`response_format=ToolStrategy(ResearchReport)`)
requiring a tool-calling-capable model. `FakeListChatModel` — the only model
available without API credentials in this environment (verified: no
ANTHROPIC_API_KEY/OPENAI_API_KEY set) — does not implement `bind_tools`, so the
`draft_node` below calls the model for plain text rather than exercising
`ToolStrategy` live. `ResearchReport` is still defined and tested directly
(`ResearchReport.model_validate_json(...)`) so the schema itself is verified;
only the live tool-calling round-trip that would populate it from a real model
is out of scope until a real provider key is supplied. See `scripts/run_demo.py`
for how to run this with a real Anthropic key when one is available.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any, Literal, Optional, TypedDict

from langchain.agents import create_agent
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from pydantic import BaseModel, Field

from ..asgf import CC00AgentState, cc00_middleware_stack
from ..cc00_path import HandoffPacket, HandoffTier, RAGPipeline
from ..rag_tool import make_corpus_search


class Citation(BaseModel):
    source: str = Field(description="Source path, verbatim from retrieval.")
    excerpt: str = Field(description="The passage supporting the claim.")


class ResearchReport(BaseModel):
    """The schema `01 §2` / `06 §4.4` describe. Validated directly in tests —
    see the module docstring's scope boundary for why it is not populated by a
    live tool-calling round-trip in this offline demo."""

    executive_summary: str
    citations: list[Citation] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class ResearchState(TypedDict, total=False):
    question: str
    user_role: str
    sacred_context: list[str]
    handoff_packets: list[dict[str, Any]]  # serialized HandoffPacket.to_dict() per hop
    retrieved: list[dict[str, Any]]
    draft_report: str
    pending_write: dict[str, Any]
    status: str  # "written" | "discarded" | None


SYSTEM_PROMPT = """\
# Role
You are the Research Supervisor for the CC-00 laboratory telescope archive.
You synthesise retrieved evidence into a short, cited finding.

# Forbidden behaviours
- Never state a claim no retrieved source supports.
- Never fabricate a citation.

# Escalation criteria
If the evidence is empty or contradictory, say so explicitly rather than guessing.
"""


def plan_node(state: ResearchState) -> dict[str, Any]:
    """ASGF L5 Mandatory: task decomposition, made explicit rather than emergent."""
    return {
        "sacred_context": [
            "Open-source only. No LangSmith, no LangGraph Platform.",
            "No finding without at least one citation or an explicit 'no evidence found'.",
        ],
    }


def retrieve_node(pipeline: RAGPipeline):
    """Closure factory so the compiled graph can be reused across pipelines/roles."""

    def _node(state: ResearchState) -> dict[str, Any]:
        search = make_corpus_search(pipeline, user_role=state.get("user_role", "public"))

        # ASGF L5 Mandatory: every agent-to-agent transition names its
        # handoff tier. This is a single-node "handoff" from plan -> retrieve,
        # but the packet is real and validated, not merely described.
        packet = HandoffPacket(
            tier=HandoffTier.MINIMAL,
            task=f"Retrieve evidence for: {state['question']}",
            acceptance_criteria=["Return only what the ACL-filtered search actually returns."],
            sacred_context=list(state.get("sacred_context", [])),
            budget=8_000,
        )
        issues = packet.validate()
        if issues:
            raise ValueError(f"Invalid handoff packet: {issues}")

        results = search.invoke({"query": state["question"], "top_k": 5})
        return {
            "retrieved": results,
            "handoff_packets": [packet.to_dict()],
        }

    return _node


def draft_node(model: BaseChatModel):
    """Closure factory: the drafting agent is built once per model, reused per call."""

    agent = create_agent(
        model=model,
        tools=[],
        system_prompt=SYSTEM_PROMPT,
        state_schema=CC00AgentState,
        middleware=cc00_middleware_stack(
            system_prompt=SYSTEM_PROMPT, task_type="factual_qa", max_model_calls=5
        ),
    )

    def _node(state: ResearchState) -> dict[str, Any]:
        result = agent.invoke(
            {
                "messages": [{"role": "user", "content": state["question"]}],
                "sacred_context": state.get("sacred_context", []),
                "retrieved": state.get("retrieved", []),
            }
        )
        return {"draft_report": result["messages"][-1].content}

    return _node


def approval_gate(state: ResearchState) -> Command[Literal["write", "discard"]]:
    """ASGF L3 Required: high-risk operations gated. The only write in this
    system, and it does not happen without this interrupt firing and being
    resumed with an explicit approval."""
    decision = interrupt(
        {
            "question": "Write this draft to the output directory?",
            "draft_preview": state.get("draft_report", "")[:2000],
            "evidence_count": len(state.get("retrieved", [])),
            "reversible": False,
        }
    )
    approved = bool(decision.get("approved")) if isinstance(decision, dict) else bool(decision)
    return Command(
        goto="write" if approved else "discard",
        update={
            "sacred_context": [
                f"Human {'APPROVED' if approved else 'REJECTED'} the write at the approval gate."
            ]
        },
    )


def write_node(output_dir: Path):
    """Closure factory. `output_dir` MUST be a disposable directory — never the
    repository root (see `supporting/03 §3`'s FilesystemBackend confinement
    lesson, applied here to a plain file write instead)."""

    output_dir.mkdir(parents=True, exist_ok=True)

    def _node(state: ResearchState) -> dict[str, Any]:
        # Windows forbids <>:"/\|?* in filenames; found by actually running this
        # node against a question containing "?" (OSError: Invalid argument).
        # Strip to a conservative safe set rather than a denylist, so no future
        # punctuation mark reopens the same bug.
        raw = state.get("question", "untitled")[:60].strip() or "report"
        slug = re.sub(r"[^A-Za-z0-9 _-]", "", raw).strip().replace(" ", "-") or "report"
        target = output_dir / f"{slug}.md"
        target.write_text(state.get("draft_report", ""), encoding="utf-8")
        return {"status": "written", "pending_write": {"path": str(target)}}

    return _node


def discard_node(state: ResearchState) -> dict[str, Any]:
    return {"status": "discarded"}


def build_graph(
    pipeline: RAGPipeline,
    model: BaseChatModel,
    checkpointer: BaseCheckpointSaver,
    output_dir: Path,
):
    """Compile the graph. Callers own the checkpointer's lifetime (tests pass an
    in-memory SqliteSaver; scripts/run_demo.py passes a file-backed one)."""

    builder = StateGraph(ResearchState)
    builder.add_node("plan", plan_node)
    builder.add_node("retrieve", retrieve_node(pipeline))
    builder.add_node("draft", draft_node(model))
    builder.add_node("approval_gate", approval_gate)
    builder.add_node("write", write_node(output_dir))
    builder.add_node("discard", discard_node)

    builder.add_edge(START, "plan")
    builder.add_edge("plan", "retrieve")
    builder.add_edge("retrieve", "draft")
    builder.add_edge("draft", "approval_gate")
    builder.add_edge("write", END)
    builder.add_edge("discard", END)

    return builder.compile(checkpointer=checkpointer)


def in_memory_checkpointer() -> BaseCheckpointSaver:
    """Convenience for tests and quick demos — not durable across processes."""
    return SqliteSaver(sqlite3.connect(":memory:", check_same_thread=False))


def file_checkpointer(path: Path) -> BaseCheckpointSaver:
    """Durable checkpointer for scripts/run_demo.py — pinned per the assessment's
    security floors (requirements.lock.txt records the resolved
    langgraph-checkpoint-sqlite version; see 00-conventions-and-baseline.md §3
    for why the checkpointer is treated as a security boundary, not a storage
    detail)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    return SqliteSaver(sqlite3.connect(str(path), check_same_thread=False))
