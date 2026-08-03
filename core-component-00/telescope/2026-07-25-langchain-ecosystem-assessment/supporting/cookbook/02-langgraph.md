# LangGraph — Enterprise User Manual

**Package:** `langgraph` · **Version:** 1.2.9 · **Stars:** 38,115 · **Status:** Active, usable
standalone

---

## 1. Introduction

### What it is

LangGraph is the durable-execution orchestration engine underneath LangChain's agent runtime, and it
is fully usable on its own, without the rest of the LangChain library. It contributes four things
nothing else in the ecosystem does as cleanly: **explicit graph topology** (nodes and edges you
declare, not behaviour that emerges), **checkpointed state** (an agent can be interrupted, persisted,
resumed, and even time-travelled — replayed from any prior point in its execution), **a durable
human-approval primitive** (a pause-and-resume mechanism that survives process restarts), and
**`Command`** (a single return value that carries both a routing decision and a state update).

### Core capabilities

| Capability            | What it gives you                                                                                                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stateful graphs**   | A `StateGraph` built from a typed state schema — the schema _is_ the contract every node reads and writes against.                                                                                       |
| **Checkpointing**     | State persists after every step to a pluggable store (in-memory, SQLite, Postgres). A run can be interrupted and resumed later, even by a different process.                                             |
| **Human-in-the-loop** | An interrupt primitive pauses a graph mid-execution and returns control to the caller; resuming continues from exactly where it paused.                                                                  |
| **Time travel**       | Because every step is checkpointed, execution can be replayed from any earlier checkpoint — useful for debugging and for testing a hypothesis about what a different input or model would have produced. |
| **Cycles**            | Unlike a strict DAG, a LangGraph graph can loop — the natural shape for an agent that calls a model, calls tools, and repeats.                                                                           |

### Why it matters as much as it does

The single most consequential thing this engine did for the wider ecosystem was answer the 2023-era
criticism of agent frameworks directly: opaque abstractions, uncontrollable behaviour, impossible
debugging. Explicit graphs, checkpointing, and interrupts are a direct, structural answer to all
three — not a policy or a best-practice document, but a runtime property. That is also precisely why
governance-conscious deployments favour it: a graph's edge set is the topology, so it cannot silently
drift from a design document the way a hand-maintained description of a system's behaviour can.

### Enterprise framing

For a non-technical stakeholder: this is the piece of infrastructure that turns "an AI that answers
one question" into "an AI system whose state survives an outage, that can pause and wait for a human
to approve something risky, and whose exact behaviour history can be replayed for an audit." Adopting
it is largely a durability and auditability decision, separate from which agent framework (if any)
sits on top of it.

---

## 2. Usage

### Installation

```powershell
pip install langgraph langgraph-checkpoint-sqlite
```

**A security note worth taking seriously:** the checkpointer is simultaneously a deserialization
boundary and a SQL boundary. A publicly disclosed vulnerability chain in checkpointer implementations
(SQL injection escalating to remote code execution via unsafe deserialization) was fixed in
`langgraph>=1.0.10` and `langgraph-checkpoint-sqlite>=3.0.1` — treat those as hard floors, not
suggestions, and treat any future checkpointer version bump as security-relevant, not routine.

### A typed state schema and a compiled graph

```python
"""Typed state is the contract. Every node reads and writes against exactly
these fields — there is no ad-hoc dictionary shape to drift out of sync.
"""

from typing import Annotated, TypedDict
from operator import add

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class TriageState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]  # reducer: appends, never overwrites
    sacred_context: Annotated[list[str], add]              # append-only — a node cannot clear this
    category: str
    model_calls: Annotated[int, add]                       # bounded via a middleware check, not here


def classify_node(state: TriageState) -> dict:
    # ... call a model, return a partial state update ...
    return {"category": "bug", "model_calls": 1}


def route(state: TriageState) -> str:
    return "escalate" if state["category"] == "unclassifiable" else "resolve"
```

### Checkpointing and durable human approval

```python
"""The interrupt-and-resume cycle: a graph pauses, persists, and can be
resumed from a different process, minutes or days later, against the same
thread_id.
"""

import sqlite3
from typing import Literal

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


def approval_gate(state: TriageState) -> Command[Literal["proceed", "reject"]]:
    # interrupt() pauses the graph and hands control back to the caller. The
    # value passed here is the ENTIRE basis on which a human approves or
    # rejects — include the actual arguments and reasoning, not a bare prompt.
    decision = interrupt(
        {
            "question": "Approve this high-risk action?",
            "details": state.get("pending_action"),
            "reversible": False,
        }
    )
    approved = bool(decision.get("approved")) if isinstance(decision, dict) else bool(decision)
    return Command(
        goto="proceed" if approved else "reject",
        # Record the human's decision as append-only state — a later
        # summarisation pass must never compress away the fact a human said no.
        update={"sacred_context": [f"Human {'approved' if approved else 'rejected'} the action."]},
    )


builder = StateGraph(TriageState)
builder.add_node("classify", classify_node)
builder.add_node("approval_gate", approval_gate)
# ... add remaining nodes and edges ...
builder.add_edge(START, "classify")

# NEVER use :memory: in production — state must survive a process restart to
# be worth checkpointing at all. sqlite3.connect() to a real file, or a
# Postgres checkpointer for multi-instance deployments.
connection = sqlite3.connect("./checkpoints.sqlite", check_same_thread=False)
graph = builder.compile(checkpointer=SqliteSaver(connection))

config = {"configurable": {"thread_id": "run-001"}}  # derive thread_id from an
                                                       # AUTHENTICATED session —
                                                       # never from raw user input;
                                                       # it is a capability to
                                                       # resume someone else's run
result = graph.invoke({"messages": [...], "sacred_context": [], "category": "", "model_calls": 0}, config)

if "__interrupt__" in result:
    # ... surface the interrupt payload to a human, wait for a decision ...
    resumed = graph.invoke(Command(resume={"approved": True}), config)
```

### A hazard worth knowing before you hit it

Never let externally supplied input reach a checkpoint-history query's filter parameter unsanitised
— that is the exact precondition the disclosed vulnerability chain above required. Keep any such
filter server-controlled, from a fixed allow-list, never assembled from a request body.

---

## 3. Alternatives and rationale

| Option                                                                                           | Choose it when                                                                                                         | Trade-off                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A framework's own prebuilt agent loop** (e.g. `create_agent`, used without a hand-built graph) | The task is a bounded, single-thread agent that doesn't need custom topology                                           | Simpler — the loop compiles to a graph underneath anyway, so durability and checkpointing are not lost, only the manual graph-authoring step.                                                               |
| **A general-purpose workflow orchestrator** (e.g. Temporal, Airflow)                             | The problem is fundamentally a long-running business workflow with occasional LLM calls, not an LLM-centric agent loop | Mature, battle-tested durability tooling for non-LLM workloads. Costs you the LLM-specific ergonomics (message state, agent middleware, model-call primitives) this engine is purpose-built for.            |
| **No orchestration layer — a single, stateless model call**                                      | The task is one prompt, one response, no multi-step reasoning and no need to persist state                             | Trivial to reason about. Appropriate whenever the task genuinely doesn't need durability, cycles, or human-in-the-loop gating — paying for a graph you don't need is the most common mistake in this space. |

**Rationale:** the deciding factor is not "is this engine good at orchestration" — its explicit-topology
and durable-checkpoint design are close to best-in-class for LLM agent control — it is "does the task
need durability and explicit topology at all." A single-shot classification call does not. A
multi-step process that must survive an interruption, pause for a human, or be replayed for an audit
does, and for that category this is very hard to beat: it is the same runtime the highest-adoption
agent framework in the ecosystem is itself built on, which means choosing it is not a bet on a
secondary or competing technology.

---

## 4. Integrations

| Integrates with                      | How                                                                                                                                                 |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The higher-level agent framework** | `create_agent` and DeepAgents both compile to a graph on this engine — see `01-langchain.md` and `03-deepagents.md`.                                |
| **`langchain-mcp-adapters`**         | Tools bridged from MCP servers plug into any graph node exactly like a hand-written tool — see `04-langchain-mcp-adapters.md`.                      |
| **SQLite / Postgres checkpointers**  | Pluggable persistence backends; SQLite for single-instance deployments, Postgres for multi-instance production.                                     |
| **OpenTelemetry**                    | Checkpoint history itself doubles as a partial observability surface (what happened, replayable) even without a dedicated tracing backend wired in. |
| **Governance middleware**            | Token-budget, PII, and tool-whitelist middleware wrap every model node the same way they wrap a plain agent's model calls.                          |

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
