# 02 — LangGraph Examples (`langgraph` 1.2.9)

**Prerequisite:** `00-conventions-and-baseline.md`.
**Status:** Reference examples, API surface verified against `langchain-ai/docs` via Context7 on
2026-07-26. **Partially executed 2026-07-27:** Example 1's `sacred_context` append-only reducer,
Example 2's checkpoint thread-isolation security boundary, Example 4's hierarchical Command
topology, and Example 5's handoff-tier construction invariants are proven by 4 real, passing tests
in `verification/` (a standalone project in this same folder — see its `README.md`). Example 3
(interrupt-based approval) and Example 6 (time travel) remain unexecuted here, though Example 3's
pattern is separately live-tested in `supporting/enterprise-examples/`.

---

## What this product is, in one paragraph

LangGraph is the durable-execution orchestration engine underneath LangChain v1, and it is usable
standalone. It contributes four things nothing else in the ecosystem does: **explicit graph
topology** (nodes and edges you declare, not behaviour that emerges), **checkpointed state** (an
agent can be interrupted, persisted, resumed, and time-travelled), **`interrupt()`** (the cleanest
human-approval mechanism in any agent framework), and **`Command`** (a node returning both a routing
decision and a state update). The research report named two of these as things LangGraph does
better than CC-00's current implementation, and that judgement is repeated here without softening:
a `StateGraph` _is_ the topology document, so it cannot drift from the implementation the way
`swarm_orchestrator.py`'s description can.

**Drop to raw LangGraph when the prebuilt loop no longer fits** — not on day one. If `create_agent`
covers the job, use it; it runs on this engine anyway.

---

## Example 1 — A typed four-slot state schema

**Use when:** always, for any LangGraph work in this workspace.

**ASGF requirements:** L2 four-slot structure, L2 slot priority order, L2 token budget at assembly —
**all three Mandatory**. Plus L2 sacred context (Required).

This is the deepest fix available for the sharpest risk in the research report. Middleware
(`FourSlotContextMiddleware`, `00 §7`) imposes the four slots at _call_ time. A typed state schema
imposes them at the _type_ level, so a node that fails to respect the structure is a type error
rather than a silent degradation.

```python
"""Example 1 — the four slots as a typed state schema.

Finding 8: "The L2 four-slot structure is the sharpest risk: it is
Mandatory, LangGraph's default state is an unstructured message list, and
'ad-hoc string concatenation is not acceptable' is exactly what a naive
create_agent adoption would produce."

This is the answer to that. The slots are fields. There is nowhere to put an
ad-hoc string.
"""

from operator import add
from typing import Annotated, Any, Literal, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class RetrievedItem(TypedDict):
    """One chunk in the Retrieved slot. Shape matches ContextAssembler.add_retrieved."""

    content: str
    source: str
    score: float           # relevance, 0-1
    acl_roles: list[str]   # carried through so ACL provenance survives into context


class FourSlotState(TypedDict):
    """CC-00's four-slot context window, expressed as LangGraph state.

    SLOT PRIORITY ORDER (ASGF L2 Mandatory — documented here because the standard
    requires the order to be documented AND enforced; enforcement lives in
    ContextAssembler._priority_fill, which drops lowest-scoring items first):

        1. system          never truncated
        2. sacred_context  never truncated, never compressed  (score = infinity)
        3. retrieved       truncated by relevance score, lowest first
        4. tool_outputs    truncated by recency, oldest first
        5. messages        truncated by recency, oldest first, sacred turns pinned

    The per-slot token split comes from ContextAssembler.BUDGET_PROFILES, selected
    by task_type. Do not hand-roll a split here.
    """

    # --- Slot 1: System -----------------------------------------------------------
    system: str

    # --- Slot 2: Retrieved --------------------------------------------------------
    retrieved: list[RetrievedItem]
    user_role: str                      # drives ACL filtering (L4 Required)

    # --- Slot 3: History ----------------------------------------------------------
    messages: Annotated[list[AnyMessage], add_messages]

    # --- Slot 4: Tool outputs -----------------------------------------------------
    tool_outputs: Annotated[list[tuple[str, Any]], add]

    # --- Cross-slot: sacred context (L2 Required) ---------------------------------
    # Decisions and constraints that must never be compressed away. Append-only by
    # reducer: a node CANNOT clear this list, which is the property that makes it
    # "sacred" rather than merely "important".
    sacred_context: Annotated[list[str], add]

    # --- Governance bookkeeping ---------------------------------------------------
    task_type: Literal[
        "factual_qa", "code_generation", "creative_writing",
        "tool_research", "multi_turn_reason", "orchestration",
    ]
    tokens_consumed: Annotated[int, add]
    model_calls: Annotated[int, add]
```

**Why the reducers matter.** `Annotated[list[str], add]` makes `sacred_context` append-only across
node updates. A node returning `{"sacred_context": []}` appends nothing; it cannot erase what is
already there. That is a structural guarantee, not a convention — and structural guarantees are what
"Mandatory" should mean.

**Wiring it to the assembler** — one node, called before every model dispatch:

```python
from cc00_langchain.cc00_path import ContextAssembler


def assemble_context(state: FourSlotState) -> dict:
    """Build the ASGF-compliant context window from typed state."""
    assembler = ContextAssembler(max_tokens=128_000)
    assembler.set_system(state["system"])

    for decision in state["sacred_context"]:
        assembler.add_sacred_context(decision)

    if state["retrieved"]:
        assembler.add_retrieved(
            [dict(item) for item in state["retrieved"]],
            query=_latest_user_text(state["messages"]),
            relevance_scores=[item["score"] for item in state["retrieved"]],
        )

    assembler.add_history(
        [{"role": m.type, "content": m.content} for m in state["messages"]]
    )

    for tool_name, result in state["tool_outputs"]:
        assembler.add_tool_output(tool_name, result)

    assembled = assembler.build(task_type=state["task_type"])
    return {
        "assembled_messages": assembled.messages,
        "tokens_consumed": assembled.total_tokens,
    }
```

---

## Example 2 — Durable checkpointing, treated as a security boundary

**Use when:** anything multi-turn. Without a checkpointer there is no durability, no
human-in-the-loop, and no resume; with one you get all three nearly free.

**ASGF requirement:** none directly Mandatory — but it is the precondition for the L3 human-approval
gate in Example 3, and it is a **security surface** (Finding 7).

```python
"""Example 2 — SQLite checkpointing with the CVE preconditions closed.

Finding 7 records a three-CVE chain escalating from SQL injection to RCE:
  CVE-2025-67644  langgraph-checkpoint-sqlite  SQLi via user keys in the filter dict
  CVE-2026-28277  langgraph                    unsafe msgpack deserialization -> RCE
  CVE-2026-27022  langgraph-checkpoint-redis   query injection

Current pinned versions exceed every fix. The preconditions still matter, because
the SHAPE of the vulnerability outlives the patch: the checkpointer is a
deserialization boundary and a SQL boundary at the same time.
"""

import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

CHECKPOINT_DB = Path("./.cc00/checkpoints.sqlite")
CHECKPOINT_DB.parent.mkdir(parents=True, exist_ok=True)

connection = sqlite3.connect(str(CHECKPOINT_DB), check_same_thread=False)
checkpointer = SqliteSaver(connection)

graph = builder.compile(checkpointer=checkpointer)

# A thread_id scopes one durable conversation. It is a TRUST BOUNDARY: anyone who
# can supply a thread_id can resume that conversation's state. Derive it from an
# authenticated session, never from unvalidated user input.
config = {"configurable": {"thread_id": f"triage-{authenticated_session_id}"}}
```

**The three rules, restated as code review criteria:**

```python
# RULE 1 — never let user input reach get_state_history(filter=...).
# This is the exact CVE-2025-67644 precondition.

# WRONG — the vulnerability, reproduced:
history = graph.get_state_history(config, filter=request.query_params)

# RIGHT — a fixed, server-controlled filter:
ALLOWED_FILTERS = {"step", "source"}
safe_filter = {k: v for k, v in requested.items() if k in ALLOWED_FILTERS}
history = graph.get_state_history(config, filter=safe_filter)


# RULE 2 — restored state is untrusted input to the runtime. Validate it on the
# way back in, exactly as you would validate a tool result.
def resume_validated(config: dict) -> FourSlotState:
    snapshot = graph.get_state(config)
    state = snapshot.values
    if not isinstance(state.get("sacred_context"), list):
        raise ValidationError("Checkpoint state failed schema validation; refusing resume.")
    if state.get("model_calls", 0) > HARD_CALL_CEILING:
        raise ValidationError("Checkpoint reports an implausible call count; refusing resume.")
    return state


# RULE 3 — a checkpointer version bump is a security change. Route it through
# whatever review your security changes get.
```

**Deployment note.** SQLite is right for this workspace: a single local operator, no exposed agent
surface. The moment an agent surface accepts untrusted input, the risk profile from Finding 7 stops
being theoretical, and the checkpointer choice should be revisited alongside it.

---

## Example 3 — `interrupt()` as the human-approval gate

**Use when:** any operation with irreversible consequences — data deletion, financial transactions,
external communication, anything that writes outside the agent's sandbox.

**ASGF requirement:** L3 "High-risk operations gated" — Required for high-risk. The research report
called this "a cleaner mechanism than anything currently in
`harness-engineering/implementations/`", and this example is what adopting it looks like.

```python
"""Example 3 — human approval driven by the CC-00 tool registry.

The registry already knows which tools are high-risk: TOOL_REGISTRY marks
file_write with requires_approval=True. This example makes that flag load-bearing
instead of decorative — reading a flag and not enforcing it is worse than not
reading it, because it looks like a control.
"""

from typing import Literal

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from cc00_langchain.cc00_path import TOOL_REGISTRY, ToolRegistry

registry = ToolRegistry(TOOL_REGISTRY)


def approval_gate(state: FourSlotState) -> Command[Literal["execute_tool", "reject_tool"]]:
    """Pause the graph for a human decision on any tool the registry flags."""
    pending = state["pending_tool_call"]
    tool_name = pending["name"]

    if not registry.requires_approval(tool_name):
        return Command(goto="execute_tool")

    # interrupt() persists the graph and returns control to the caller. The value
    # passed here is what the operator sees, so it must contain everything needed
    # to make the decision WITHOUT reading the code.
    decision = interrupt(
        {
            "question": f"Approve tool call: {tool_name}?",
            "tool": tool_name,
            "arguments": pending["args"],
            "why_gated": registry.get_tool_info(tool_name).get("description", ""),
            "reversible": False,
            "agent_reasoning": state["messages"][-1].content,
        }
    )

    approved = bool(decision.get("approved")) if isinstance(decision, dict) else bool(decision)
    return Command(
        goto="execute_tool" if approved else "reject_tool",
        # The decision itself is sacred: it is a human commitment, and no later
        # summarisation pass may compress it away.
        update={
            "sacred_context": [
                f"Human {'APPROVED' if approved else 'REJECTED'} {tool_name} "
                f"with args {pending['args']}."
            ]
        },
    )


def reject_tool(state: FourSlotState) -> dict:
    """Record the refusal so the agent can replan rather than retry blindly."""
    return {
        "tool_outputs": [
            (state["pending_tool_call"]["name"], "REJECTED BY HUMAN — do not retry this call.")
        ]
    }


builder = StateGraph(FourSlotState)
builder.add_node("approval_gate", approval_gate)
builder.add_node("execute_tool", execute_tool)
builder.add_node("reject_tool", reject_tool)
builder.add_edge(START, "approval_gate")
builder.add_edge("execute_tool", END)
builder.add_edge("reject_tool", END)

graph = builder.compile(checkpointer=checkpointer)   # REQUIRED — no checkpointer, no interrupt
```

**Driving it from the operator side:**

```python
# First pass — runs until the interrupt fires.
stream = graph.stream_events(initial_state, config, version="v3")
_ = stream.output                      # drive the stream to completion
print(stream.interrupts)               # -> (Interrupt(value={'question': ...}),)

# ... the graph is now durably paused. The process can exit. Resume can happen
# minutes or days later, from a different process, against the same thread_id.

resumed = graph.stream_events(
    Command(resume={"approved": True, "approver": "elias.vance"}),
    config,
    version="v3",
)
```

**Design notes that matter in production:**

- **The interrupt payload is a UI contract.** Include the arguments, the reversibility, and the
  agent's own reasoning. An operator approving a call they cannot see the arguments of is a
  rubber stamp, and a rubber stamp is not an approval gate.
- **Record the decision as sacred context.** Otherwise a later summarisation pass can compress away
  the fact that a human said no, and the agent will cheerfully re-propose it.
- **A rejection needs a distinct path.** `reject_tool` tells the agent the call was refused so it can
  replan. Silently skipping the tool produces an agent that retries the same rejected action.
- **Interrupts re-fire during time travel.** If you rewind past an approval, the node re-executes and
  `interrupt()` pauses for a fresh `Command(resume=...)`. That is correct behaviour — a replayed
  approval is not an approval — but it will surprise anyone who expects the decision to be cached.

---

## Example 4 — Topology as a declared artefact

**Use when:** more than one agent is involved.

**ASGF requirements:** L5 "Swarm topology explicitly selected" and L5 "Task decomposition specified"
— **both Mandatory**. The standard rejects "emergent topology without design intent".

```python
"""Example 4 — a hierarchical swarm where the graph IS the topology document.

CC-00's SwarmOrchestrator DESCRIBES a topology; a StateGraph ENFORCES one, because
it is the thing that executes. This is the research report's second "LangGraph
does this better" finding, and the practical consequence is that the topology
cannot drift from the implementation.

TOPOLOGY: Hierarchical (SwarmTopology.HIERARCHICAL in CC-00's vocabulary)
SUPERVISOR: triage_supervisor — owns delegation, synthesis, conflict resolution
DECOMPOSITION (bounded, non-overlapping — ASGF L5 Mandatory/Required):
  - classifier   : ticket text            -> category + severity     (no tools)
  - cataloguer   : component name         -> owner + on-call         (catalogue tool only)
  - historian    : ticket text            -> similar prior incidents (RAG tool only)
Each specialist sees ONLY its own inputs. No specialist can call another.
"""

from typing import Literal

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command


def triage_supervisor(
    state: FourSlotState,
) -> Command[Literal["classifier", "cataloguer", "historian", "synthesise"]]:
    """Delegate to exactly one specialist, or synthesise when all have reported."""
    done = {name for name, _ in state["tool_outputs"]}
    for specialist in ("classifier", "cataloguer", "historian"):
        if specialist not in done:
            return Command(goto=specialist)
    return Command(goto="synthesise")


builder = StateGraph(FourSlotState)
builder.add_node("supervisor", triage_supervisor)
builder.add_node("classifier", classifier_node)
builder.add_node("cataloguer", cataloguer_node)
builder.add_node("historian", historian_node)
builder.add_node("synthesise", synthesise_node)

builder.add_edge(START, "supervisor")
# Specialists report back to the supervisor and ONLY to the supervisor. This edge
# set is what makes the topology hierarchical rather than mesh — and it is checkable
# by reading the file, which is the entire point.
builder.add_edge("classifier", "supervisor")
builder.add_edge("cataloguer", "supervisor")
builder.add_edge("historian", "supervisor")
builder.add_edge("synthesise", END)

graph = builder.compile(checkpointer=checkpointer)
```

**Role non-overlap is a design review item, not a runtime check.** ASGF L5 Required: agents with

> 70% skill-set overlap should be consolidated. The three specialists above take different inputs,
> hold different tools, and produce different outputs — that is what non-overlapping means in
> practice. Nothing in LangGraph verifies it for you.

**Render the topology for review:**

```python
# The graph can draw itself. Attach this to the design record so reviewers audit
# the real topology rather than a diagram someone drew and then stopped updating.
png_bytes = graph.get_graph().draw_mermaid_png()
Path("topology.png").write_bytes(png_bytes)
```

---

## Example 5 — `Command` as the Context Handoff Protocol carrier

**Use when:** any agent-to-agent transition.

**ASGF requirements:** L5 "Context Handoff Protocol implemented" — **Mandatory**; L2 "Context Handoff
Protocol specified" and L2 "Minimum Viable Context enforced" — Required.

The research report identified the gap precisely: `Command(goto=..., update=...)` is a natural
handoff carrier, but the **tier discipline** (Full / Scoped / Minimal) is CC-00's own vocabulary and
must be mapped onto it deliberately. Here is that mapping.

```python
"""Example 5 — CC-00 handoff tiers over LangGraph Command.

The tier is not decoration. It decides how much context crosses the boundary, and
"Minimum Viable Context" is an ASGF Required item: full conversation history is NOT
forwarded wholesale to specialist subagents.
"""

from typing import Literal

from langgraph.types import Command

from cc00_langchain.cc00_path import HandoffPacket, HandoffTier


def build_handoff(state: FourSlotState, tier: HandoffTier, task: str) -> HandoffPacket:
    """Construct a tier-appropriate packet. The tier decides what is INCLUDED."""
    packet = HandoffPacket(
        tier=tier,
        task=task,
        # Sacred context crosses EVERY tier, including Minimal. Constraints that
        # must not be overridden do not become negotiable because the handoff is small.
        sacred_context=list(state["sacred_context"]),
        acceptance_criteria=[
            "Return the declared schema and nothing else.",
            "Cite the retrieved source for every factual claim.",
        ],
        budget=32_000,
    )

    if tier is HandoffTier.FULL:
        # Full: successor continues the SAME task. Use sparingly — this is the
        # expensive tier and the one that over-shares.
        packet.conversation_history = [
            {"role": m.type, "content": m.content} for m in state["messages"]
        ]
    elif tier is HandoffTier.SCOPED:
        # Scoped: a specialist handles a subtask. Task-relevant retrieval only,
        # no conversation history.
        packet.relevant_files = [item["source"] for item in state["retrieved"]]
    # Minimal: task + acceptance criteria + sacred context. Nothing else.

    issues = packet.validate()
    if issues:
        raise ValueError(f"Handoff packet invalid: {issues}")
    return packet


def delegate_to_historian(state: FourSlotState) -> Command[Literal["historian"]]:
    """Scoped handoff — the historian needs retrieval, not the whole conversation."""
    packet = build_handoff(
        state,
        tier=HandoffTier.SCOPED,
        task="Find prior incidents matching this ticket. Return at most five, most similar first.",
    )
    return Command(
        goto="historian",
        update={"handoff": packet.to_dict()},   # to_dict() keeps it checkpoint-serializable
    )
```

**Tier selection is a decision, and it should be recorded as one:**

| Tier        | Crosses the boundary                                    | Use when                                |
| ----------- | ------------------------------------------------------- | --------------------------------------- |
| **Full**    | All four slots, including complete conversation history | The successor continues the _same_ task |
| **Scoped**  | Task-relevant retrieval + sacred context, no history    | A specialist handles a bounded subtask  |
| **Minimal** | Task + acceptance criteria + sacred context only        | An independent parallel agent           |

`HandoffPacket.validate()` enforces the tier's own invariants — Full requires
`conversation_history`, Minimal forbids it — so a mis-tiered packet fails at construction rather
than producing a subtly over-shared subagent.

**One CC-00 detail worth carrying across:** `retrieved_reflections` is deliberately _not_
`sacred_context`. A retrieved reflection is a required read, not a constraint the receiving agent is
bound by. Do not collapse the two when mapping onto `Command.update`.

---

## Example 6 — Time travel for post-incident analysis

**Use when:** an agent produced a wrong or expensive outcome and you need to know why.

Under the open-source-only constraint there is no LangSmith run viewer, so checkpoint history _is_
the debugging surface. This partially compensates — traces plus state history answer "what happened";
neither answers "is this systematically getting worse", which remains an open gap (`00 §5`).

```python
"""Example 6 — replay a run from any prior checkpoint."""

# Every superstep is a checkpoint. Walk them newest-first.
for snapshot in graph.get_state_history(config):
    print(snapshot.config["configurable"]["checkpoint_id"], snapshot.next, snapshot.values["model_calls"])

# Rewind to a specific checkpoint and re-run from there — with a changed input,
# a different model, or a fixed prompt — to test a hypothesis about the failure.
replay_config = {
    "configurable": {
        "thread_id": config["configurable"]["thread_id"],
        "checkpoint_id": suspect_checkpoint_id,
    }
}
graph.invoke(None, replay_config)      # None = resume from the checkpoint as stored

# CAUTION: if the replayed span contains an approval gate, interrupt() fires again
# and waits for a fresh decision. A replayed approval is not an approval.
```

---

## Anti-pattern summary for this product

| Anti-pattern                                        | Why it fails                                                                                         |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Hand-rolling a `StateGraph` on day one              | Buys complexity you have not earned. Start with `create_agent`; it runs on this engine anyway.       |
| Free-form `dict` state                              | The ASGF L2 Mandatory four-slot structure has nowhere to live. Type the state.                       |
| No checkpointer on a multi-turn graph               | No durability, no human-in-the-loop, no resume — and no post-incident analysis.                      |
| User input reaching `get_state_history(filter=...)` | The literal CVE-2025-67644 precondition.                                                             |
| `thread_id` taken from an unauthenticated request   | A thread id is a capability to resume someone else's conversation.                                   |
| Approval gate that hides the tool arguments         | A rubber stamp. Not a control.                                                                       |
| Forwarding full history to every subagent           | Violates L2 "Minimum Viable Context". Use Scoped or Minimal.                                         |
| Treating `Command(goto=...)` as routing only        | The tier discipline is the ASGF-load-bearing half. Routing without a tier is an unspecified handoff. |

---

**Document status:** Reference examples — unexecuted.
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-26
