# 06 — Ecosystem Integration Example: The Telescope Research Assistant

**Prerequisite:** all of `00`–`05`. This file composes them.
**Status:** Reference architecture and reference code. **Not executed.** See `00 §1`.

---

## 1. What this is, and why this task

One end-to-end system that uses the whole open-source LangChain ecosystem as the research report
recommends it be used: **`create_agent` + LangGraph for the loop and topology, `langchain-mcp-adapters`
to consume the existing governed MCP servers as tools, and CC-00's `retrieval-augmented-generation/`
retained as the retrieval implementation.** Nothing in CC-00 is replaced.

**The task: assist in producing a telescope research report.** Given a research question, the system
plans an investigation, retrieves evidence from workspace knowledge and an application corpus,
consults prior reflections, delegates bounded subtasks to specialists, attempts to refute its own
draft findings, and produces a report conforming to the telescope template — stopping at a human
approval gate before anything is written to disk.

**Why this task and not a toy.** The research report's Next Step #1 asks the CEO to authorise a bounded
LangChain pilot and **name the target task**. This is a concrete proposal for that slot, and it was
chosen against real criteria:

| Criterion                            | How this task scores                                                                         |
| ------------------------------------ | -------------------------------------------------------------------------------------------- |
| Exercises the ecosystem genuinely    | Uses all four libraries plus the MCP bridge — not a demo that name-drops them                |
| Bounded blast radius                 | Read-only until a human approves one file write. No code, no config, no governance documents |
| Output is verifiable by an expert    | A report either cites its sources or does not; CC-00 already reviews reports this way        |
| Failure is cheap and visible         | A bad draft is discarded. Nothing has been changed.                                          |
| CC-00 already does this work by hand | Real baseline to compare against, rather than a capability nobody needed                     |

**The honest counter-argument, stated because it is strong.** A research agent that writes confident
reports from thin evidence is worse than no research agent, because the output looks correct until
someone checks the citations. The `critic` stage and the attribution requirements below are not
decoration — they are the reason this task is proposable at all. If they are cut to ship faster,
the pilot should be cancelled instead.

---

## 2. Architecture

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  ENTRY  —  research question + authenticated operator session                 │
│  user_role bound here, from the session. Never model-chosen.                   │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  LANGGRAPH  —  StateGraph over FourSlotState        [ASGF L2 Mandatory,       │
│                                                       L5 Mandatory]           │
│                                                                               │
│   START → plan → supervisor ⇄ { retriever · analyst · critic } → draft        │
│                                    ↓                                          │
│                          approval_gate  ── interrupt() ──▶  HUMAN             │
│                                    ↓ approved                                 │
│                               write_report → END                              │
│                                                                               │
│   Checkpointer: SqliteSaver (pinned ≥3.0.1)  ·  thread_id from session         │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               │  every model call passes through:
                               │    Observability → TypedErrorBoundary →
                               │    TokenBudget → PII → ToolGovernance →
                               │    FourSlotContext        [ASGF L3 Mandatory ×4]
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  TOOL TIER                                                                    │
│                                                                               │
│  langchain-mcp-adapters ──▶ workspace-knowledge   (search_docs, …)            │
│                        └──▶ agent-memory          (search_memory)             │
│      · already three-gate approved — governance carries over unchanged        │
│      · write tools filtered out · health_check collision resolved             │
│                                                                               │
│  CC-00 RAG (first-party, retained) ──▶ search_corpus(query)                   │
│      · BM25 + RRF fusion + ACL filtering        [ASGF L4 Required: ACL]       │
│      · user_role bound in a closure, not a tool parameter                     │
│                                                                               │
│  DeepAgents middleware ──▶ TodoList (planning) · Filesystem (StateBackend)    │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  MODEL TIER                                                                   │
│    API model  ──  planning, tool selection, synthesis, refutation             │
│    LM Studio  ──  bulk source pre-classification ONLY, no tools attached      │
│                   (scoped tier; not installed — open precondition)            │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  GPU TIER (unchanged)  —  RTX 4060, embeddings + reranking, ~7 GB free        │
│  OBSERVABILITY  —  OpenTelemetry → local collector.  No LangSmith.            │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Topology: Hierarchical.** Supervisor: `supervisor`. Specialists: `retriever`, `analyst`, `critic`
— bounded, non-overlapping, no lateral edges. Declared in §4.2, reviewable as a table in `03 §2`.

---

## 3. ASGF compliance walkthrough

Where each requirement is closed. This is the table an audit would ask for, and producing it _before_
building is the point — ASGF asks for topology and decomposition to be documented **before**
implementation.

| Layer  | Requirement                                | Level         | Closed by                                                                    |
| ------ | ------------------------------------------ | ------------- | ---------------------------------------------------------------------------- |
| **L1** | Role / persona defined                     | **Mandatory** | §4.1 `SUPERVISOR_PROMPT` — Role section, bounded expertise                   |
| L1     | System prompt separated from task prompt   | **Mandatory** | System slot is `state["system"]`; task arrives as a user message             |
| L1     | Output format constrained                  | **Mandatory** | §4.4 `DraftFinding` / `ResearchReport` Pydantic schemas                      |
| L1     | Behavioural constraints enumerated         | Required      | §4.1 — Forbidden behaviours section                                          |
| L1     | Escalation criteria defined                | Required      | §4.1 — Escalation section + `requires_human` field                           |
| **L2** | Four-slot context structure                | **Mandatory** | `FourSlotState` (`02 §1`) + `FourSlotContextMiddleware` (`00 §7`)            |
| L2     | Slot priority order defined                | **Mandatory** | Documented in `FourSlotState` docstring; enforced in `_priority_fill`        |
| L2     | Token budget tracked at assembly           | **Mandatory** | `ContextAssembler` knows the budget before dispatch, by construction         |
| L2     | Minimum Viable Context enforced            | Required      | §4.3 Scoped/Minimal handoffs — no wholesale history forwarding               |
| L2     | Sacred context identified and protected    | Required      | `Annotated[list[str], add]` — append-only, cannot be cleared                 |
| L2     | History managed with compression           | Required      | `ContextAssembler` history budget + priority fill                            |
| L2     | Context Handoff Protocol specified         | Required      | §4.3 `HandoffPacket` with explicit tier per transition                       |
| **L3** | Timeout enforcement                        | **Mandatory** | `init_chat_model(..., timeout=60)` on every model                            |
| L3     | Error boundary with typed recovery         | **Mandatory** | `TypedErrorBoundaryMiddleware` — distinct Timeout/RateLimit/Validation paths |
| L3     | Token budget monitor active                | **Mandatory** | `TokenBudgetMiddleware` — per-session budget + call cap                      |
| L3     | Rate-limit retry with exponential backoff  | **Mandatory** | `TypedErrorBoundaryMiddleware._classify` → backoff **with jitter**           |
| L3     | Tool registry / whitelist                  | Required      | `ToolGovernanceMiddleware` + `govern_mcp_tools` (`04 §2`)                    |
| L3     | Tool call limits enforced                  | Required      | `max_calls_per_task` in `TOOL_REGISTRY`; `max_model_calls` cap               |
| L3     | High-risk operations gated                 | Required      | §4.5 `approval_gate` → `interrupt()` before any disk write                   |
| L3     | PII scrubbing / scanning                   | Required      | `PIIMiddleware` — **with the detector limitation in `00 §7`**                |
| **L4** | Retrieval pipeline implemented             | **Mandatory** | CC-00 `RAGPipeline` + `workspace-knowledge`                                  |
| L4     | Chunking strategy defined                  | Required      | CC-00 `chunker.py` — documented per content type                             |
| L4     | Embedding model specified and pinned       | Required      | Shared cache, `_shared/models/<slug>/`, per MCP provisioning convention      |
| L4     | **Reranking step implemented**             | Required      | ❌ **UNMET — standing gap.** See §7.                                         |
| L4     | ACL filtering applied                      | Required      | `RAGPipeline.query(user_role=...)`, role bound in a closure                  |
| L4     | Retrieval freshness documented             | Required      | Inherited from `rag-sync-state.json`; restate per corpus                     |
| **L5** | Swarm topology explicitly selected         | **Mandatory** | §2 diagram + §4.2 `StateGraph` — the graph _is_ the topology                 |
| L5     | Task decomposition specified               | **Mandatory** | §4.2 + the decomposition table in `03 §2`                                    |
| L5     | Context Handoff Protocol implemented       | **Mandatory** | §4.3 `Command(goto=, update=)` carrying a tiered `HandoffPacket`             |
| L5     | Agent roles non-overlapping                | Required      | Overlap check recorded in `03 §2` — no pair near the 70% threshold           |
| L5     | Supervisor defined for hierarchical swarms | Required      | `supervisor` node — owns delegation, synthesis, conflict resolution          |
| L5     | Anti-patterns prohibited in prompts        | Required      | §4.1 Forbidden behaviours, in every specialist prompt                        |

**Projected verdict: `Conditional`.** No Mandatory gap. One Required gap — L4 reranking — with an
active remediation plan (Recommendation 1, P1, 0.5 day, no LangChain dependency). That is
exactly the standard's definition of Conditional, and it matches the research report's projection.
**This is a projection, not an audit.** A real verdict requires the formal instrument in
`crew/director/elias-vance/skills/asgf-compliance-audit.md`, run against running code.

---

## 4. The implementation

### 4.1 Identity

```python
"""Telescope Research Assistant — identity documents.

ASGF L1: three Mandatory items and two Required items live in this string. It is
a governance artefact, not a greeting.
"""

SUPERVISOR_PROMPT = """\
# Role

You are the Research Supervisor for the CC-00 laboratory telescope archive. You
decompose a research question into bounded subtasks, delegate each to exactly one
named specialist, and synthesise their reports into a telescope-conformant research
report. You do not retrieve evidence yourself and you do not perform analysis
yourself — you delegate both.

# Forbidden behaviours

- Never state a finding that no retrieved source supports. If the evidence is thin,
  the finding is "not established", and you say so.
- Never fabricate a citation, a version number, a date, or a statistic.
- Never present a vendor's claim about itself as independent evidence. Label it
  "vendor-reported" and say why that matters.
- Never trim scope to finish faster. If the question is larger than the budget,
  report what was covered and name what was not.
- Never delegate outside your roster: retriever, analyst, critic.
- Never write to disk. Drafting is your job; writing is gated and not yours.

# Escalation criteria

Return control to the human when:
- Retrieved evidence is contradictory and the contradiction changes the recommendation.
- A source required to answer the question is unreachable or returns degraded results.
- The question cannot be answered within the token budget.
- Answering would require asserting something no source supports.

# Method

1. Decompose the question into research questions. Record them.
2. For each: delegate retrieval to `retriever`, then analysis to `analyst`.
3. Draft each finding with its evidence attached.
4. Send every draft finding to `critic` BEFORE including it. A finding the critic
   refutes is dropped or downgraded — never quietly kept.
5. Synthesise. State limitations explicitly, including what you could not verify.
"""
```

### 4.2 State and topology

```python
"""Graph construction. The topology is declared here and nowhere else."""

from typing import Literal

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

# FourSlotState from 02 §1, extended with this system's working fields.
class ResearchState(FourSlotState):
    question: str
    research_questions: list[str]
    findings: Annotated[list[dict], add]
    refutations: Annotated[list[dict], add]
    draft_report: str
    pending_write: dict | None


def supervisor(
    state: ResearchState,
) -> Command[Literal["retriever", "analyst", "critic", "draft"]]:
    """Delegate one subtask, or move to drafting when the evidence is complete.

    Deterministic routing. The MODEL decides what to research; the GRAPH decides
    who researches it. Keeping those separate is what makes the topology explicit
    rather than emergent.
    """
    for question in state["research_questions"]:
        if not _has_evidence(state, question):
            return Command(goto="retriever", update={"current_question": question})
        if not _has_analysis(state, question):
            return Command(goto="analyst", update={"current_question": question})

    unrefuted = [f for f in state["findings"] if not _was_criticised(state, f)]
    if unrefuted:
        return Command(goto="critic", update={"current_finding": unrefuted[0]})

    return Command(goto="draft")


builder = StateGraph(ResearchState)
builder.add_node("plan", plan_node)
builder.add_node("supervisor", supervisor)
builder.add_node("retriever", retriever_node)
builder.add_node("analyst", analyst_node)
builder.add_node("critic", critic_node)
builder.add_node("draft", draft_node)
builder.add_node("approval_gate", approval_gate)
builder.add_node("write_report", write_report_node)
builder.add_node("discard", discard_node)

builder.add_edge(START, "plan")
builder.add_edge("plan", "supervisor")
# Specialists report ONLY to the supervisor. No lateral edges. This edge set is
# the difference between hierarchical and mesh, and it is auditable by reading it.
builder.add_edge("retriever", "supervisor")
builder.add_edge("analyst", "supervisor")
builder.add_edge("critic", "supervisor")
builder.add_edge("draft", "approval_gate")
builder.add_edge("write_report", END)
builder.add_edge("discard", END)

graph = builder.compile(checkpointer=SqliteSaver(connection))
```

### 4.3 Handoffs, tiered

```python
"""Every agent-to-agent transition names its tier. ASGF L5 Mandatory."""

from cc00_langchain.cc00_path import HandoffPacket, HandoffTier


def retriever_node(state: ResearchState) -> Command[Literal["supervisor"]]:
    # MINIMAL: the retriever needs a question and the rules. It does not need the
    # conversation, the other findings, or the draft. Minimum Viable Context is an
    # ASGF Required item, and this is what enforcing it looks like.
    packet = HandoffPacket(
        tier=HandoffTier.MINIMAL,
        task=f"Retrieve evidence for: {state['current_question']}",
        acceptance_criteria=[
            "Return passages with their source path verbatim.",
            "Return an explicit 'no relevant evidence found' rather than the nearest match.",
        ],
        sacred_context=list(state["sacred_context"]),   # crosses every tier
        budget=32_000,
    )
    result = retriever_agent.invoke({"handoff": packet.to_dict()})
    return Command(goto="supervisor", update={"retrieved": result["passages"]})


def critic_node(state: ResearchState) -> Command[Literal["supervisor"]]:
    # SCOPED: the critic needs the finding AND its cited evidence — it cannot
    # evaluate support without seeing what was cited. It still gets no
    # conversation history.
    finding = state["current_finding"]
    packet = HandoffPacket(
        tier=HandoffTier.SCOPED,
        task=f"Attempt to refute this finding: {finding['claim']}",
        acceptance_criteria=[
            "Report every unsupported inference and every overstated confidence.",
            "Default to 'not established' when the evidence is ambiguous.",
        ],
        sacred_context=list(state["sacred_context"]),
        relevant_files=[c["source"] for c in finding["citations"]],
        budget=32_000,
    )
    if issues := packet.validate():
        raise ValueError(f"Invalid handoff packet: {issues}")

    result = critic_agent.invoke({"handoff": packet.to_dict()})
    return Command(goto="supervisor", update={"refutations": [result]})
```

### 4.4 Output schemas

```python
"""ASGF L1 Mandatory: output consumed downstream is schema-constrained."""

from typing import Literal

from pydantic import BaseModel, Field


class Citation(BaseModel):
    source: str = Field(description="Source path or URL, verbatim from retrieval.")
    excerpt: str = Field(description="The passage supporting the claim. Do not paraphrase.")
    retrieved_via: Literal["workspace_knowledge", "corpus_rag", "agent_memory"]


class DraftFinding(BaseModel):
    claim: str
    citations: list[Citation] = Field(description="At least one. A claim with none is not a finding.")
    confidence: Literal["established", "supported", "not-established"]
    vendor_reported: bool = Field(
        description="True if the primary evidence is a party reporting on itself."
    )


class ResearchReport(BaseModel):
    executive_summary: str
    findings: list[DraftFinding]
    limitations: list[str] = Field(
        description="What could NOT be verified. An empty list here is almost always wrong."
    )
    requires_human: bool
    unanswered: list[str] = Field(description="Research questions the evidence did not close.")
```

The `vendor_reported` flag and the `limitations` list exist because the research report did both by
hand — it labelled LangChain's own survey as vendor-reported and rejected four statistics
aggregators outright. Encoding those habits as **fields** is how a practice survives being handed to
an agent.

### 4.5 The approval gate

```python
"""The only write in the system, and it is gated. ASGF L3 Required."""

from langgraph.types import Command, interrupt


def approval_gate(state: ResearchState) -> Command[Literal["write_report", "discard"]]:
    report = state["draft_report"]

    decision = interrupt(
        {
            "question": "Write this draft to the telescope archive?",
            "target_path": state["pending_write"]["path"],
            "reversible": False,
            "report_preview": report[:4000],
            "finding_count": len(state["findings"]),
            "unsupported_findings": [
                f["claim"] for f in state["findings"] if not f["citations"]
            ],
            "refutations_raised": len(state["refutations"]),
            "limitations_declared": state["findings"] and state.get("limitations", []),
        }
    )

    approved = bool(decision.get("approved")) if isinstance(decision, dict) else bool(decision)
    return Command(
        goto="write_report" if approved else "discard",
        update={
            "sacred_context": [
                f"Human {'APPROVED' if approved else 'REJECTED'} writing "
                f"{state['pending_write']['path']} at the approval gate."
            ]
        },
    )
```

**Note what the operator is shown.** Not just the report — the count of findings with no citations,
the number of refutations the critic raised, and whether limitations were declared at all. Those are
the three signals that distinguish a good draft from a confident one, and an approval UI that hides
them produces rubber stamps.

### 4.6 Assembly

```python
"""Putting it together."""

import asyncio

from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

from cc00_langchain.asgf import (
    FourSlotContextMiddleware, ObservabilityMiddleware, PIIMiddleware,
    TokenBudgetMiddleware, ToolGovernanceMiddleware, TypedErrorBoundaryMiddleware,
)
from cc00_langchain.telemetry import install_tracing


async def build_system(session):
    install_tracing(service_name="cc00-telescope-research-assistant")

    # --- Tools: MCP bridge + first-party RAG ------------------------------------
    client = MultiServerMCPClient(MCP_SERVERS)          # 04 §1
    mcp_tools = govern_mcp_tools(await client.get_tools())   # 04 §2 — collisions, write tools
    corpus_search = make_corpus_search(user_role=session.role)   # 04 §5 — ACL bound here

    backend = StateBackend()      # virtual FS; nothing touches the host disk

    supervisor_agent = create_agent(
        model=init_chat_model("anthropic:claude-sonnet-5", timeout=60, max_retries=0),
        tools=[*mcp_tools, corpus_search],
        system_prompt=SUPERVISOR_PROMPT,
        response_format=ToolStrategy(ResearchReport),
        middleware=[
            ObservabilityMiddleware(),
            TypedErrorBoundaryMiddleware(),
            TokenBudgetMiddleware(max_tokens=128_000, max_model_calls=80),
            PIIMiddleware(),
            ToolGovernanceMiddleware(),
            MCPDegradationMiddleware(),          # 04 §4 — empty ≠ absent
            TodoListMiddleware(),                # DeepAgents: planning surface
            FilesystemMiddleware(backend=backend),
            # Innermost. Nothing may rewrite messages after the assembler.
            FourSlotContextMiddleware(
                system_prompt=SUPERVISOR_PROMPT, task_type="orchestration"
            ),
        ],
    )
    return supervisor_agent
```

**`task_type="orchestration"`** selects CC-00's orchestration budget profile — 20% system, 30%
retrieved, 10% history, 40% tool outputs. That is the right shape for a supervisor: it lives on tool
results, not on conversation. The specialists use different profiles (`retriever` →
`factual_qa` at 65% retrieved; `critic` → `multi_turn_reason`). **Picking the profile per role is the
whole point of having profiles**, and defaulting all four to the same one would waste the mechanism.

---

## 5. Running it

```python
config = {"configurable": {"thread_id": f"research-{session.id}-{investigation_slug}"}}

stream = graph.stream_events(
    {
        "question": "Does X hold under condition Y?",
        "system": SUPERVISOR_PROMPT,
        "user_role": session.role,
        "task_type": "orchestration",
        "sacred_context": [
            "Open-source only. LangSmith and LangGraph Platform are excluded by CEO constraint.",
            "Vendor-reported figures must be labelled as vendor-reported.",
            "No finding without at least one citation.",
        ],
        "messages": [], "retrieved": [], "tool_outputs": [],
        "research_questions": [], "findings": [], "refutations": [],
    },
    config,
    version="v3",
)
_ = stream.output
print(stream.interrupts)     # the approval gate

resumed = graph.stream_events(
    Command(resume={"approved": True, "approver": "elias.vance"}), config, version="v3"
)
```

**The three sacred-context entries are the CEO's constraints, made structural.** They are
append-only, they cross every handoff tier including Minimal, and they are excluded from compression.
A constraint that lives only in the system prompt survives until the first summarisation pass; a
constraint in sacred context does not have that failure mode.

---

## 6. Deliberately not in this system

Stating exclusions is part of the design, not an omission.

| Excluded                                   | Why                                                                               |
| ------------------------------------------ | --------------------------------------------------------------------------------- |
| Any write outside the approved report path | Blast radius. The system reads everything and writes one gated file.              |
| `rebuild_index` / `upsert_document`        | Write-capable MCP tools, filtered at the bridge (`04 §3`).                        |
| Autonomous merge or commit                 | Workspace convention: no agent self-merges without review.                        |
| LangSmith                                  | Commercial. Excluded by constraint.                                               |
| A local model in the agent loop            | Sub-14B tool-calling reliability. Finding 6.                                      |
| `create_deep_agent` as the top-level agent | Composed its middleware instead, to keep middleware ordering auditable (`03 §4`). |
| Automatic README index updates             | Telescope indexing is a governance act with a Status column. It stays human.      |

---

## 7. Open gaps in this design

| Gap                                                    | Severity | Disposition                                                                             |
| ------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------- |
| **L4 reranking unmet**                                 | P1       | Standing workspace gap, not introduced here. Rec. 1 — 0.5 day, no LangChain dependency. |
| Nothing executed                                       | —        | First-run shakedown required before any claim of working.                               |
| Middleware ordering vs. DeepAgents' own                | P2       | Shakedown item #1 — log the assembled messages and confirm four slots survive.          |
| `PIIMiddleware` is pattern-based only                  | P2       | Adequate for internal corpora; insufficient for regulated data.                         |
| Three of four memory collections are empty             | —        | Inherited. The agent will get honest empty answers.                                     |
| No evaluation harness                                  | P1       | The real cost of excluding LangSmith. Needs its own scoping.                            |
| `_classify` provider-exception mapping is string-based | P2       | Must be replaced with `isinstance` checks once packages are pinned.                     |

---

## 8. Pilot acceptance criteria

If the CEO authorises this as the bounded pilot, it should be judged against criteria fixed **before**
it runs — otherwise the result is whatever the demo happened to produce.

1. **Attribution:** 100% of findings in the output carry at least one citation resolving to a real
   retrievable source. Any fabricated citation fails the pilot outright.
2. **Refutation:** the critic raises at least one substantive objection on a question where the
   evidence is genuinely thin. A critic that never objects is not working.
3. **Governance:** the approval gate fires before every disk write, without exception, across all
   runs — including resumed and time-travelled ones.
4. **Degradation honesty:** with `qdrant-memory` deliberately stopped, the system reports degraded
   retrieval rather than concluding "no prior context exists".
5. **Boundedness:** no run exceeds its token budget or model-call cap without raising.
6. **Comparison:** one report produced against a question CC-00 has already answered by hand, read
   side by side with the human original by Dr. Nwosu-Chen or Dr. Wieczorek.

Criteria 1 and 4 are the disqualifying ones. A system that invents citations or hides degradation
should not proceed regardless of how good the prose is.

---

**Document status:** Reference architecture and code — unexecuted.
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-26
