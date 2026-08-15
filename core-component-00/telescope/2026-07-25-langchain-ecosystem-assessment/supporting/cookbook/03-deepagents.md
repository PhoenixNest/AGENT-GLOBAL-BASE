# DeepAgents — Enterprise User Manual

**Package:** `deepagents` · **Stars:** 26,797 (2026-07-25) · **Status:** Active, created 2025-07-27
**Verification status:** Installed (`deepagents==0.6.12`) in this session's runnable project
(`supporting/enterprise-examples/`). Every class, function, and signature referenced below was
**introspected against the real installed package**, not recalled from documentation. The primary
usage example in §2 was **live-executed** end to end against a fake model — see the box at the top of
that section for exactly what that proves and what it doesn't.

---

## 1. Introduction

### What it is

DeepAgents is the LangChain organisation's "batteries-included agent harness." Where `create_agent`
(the base LangChain primitive) gives you an empty agent loop and somewhere to attach middleware,
`create_deep_agent` gives you an agent that already has the middleware a long-horizon, multi-step
task needs, pre-wired:

- **A planning tool** — the agent maintains an explicit todo list rather than reasoning silently
  about what it's already done
- **A virtual or real filesystem** — a place for the agent to take notes, write intermediate
  artefacts, and read them back across a long task
- **Sub-agent spawning** — the ability to delegate a bounded piece of work to a named specialist and
  get back a single synthesised result, rather than polluting the main thread with every intermediate
  step
- **Context management** — summarisation middleware that keeps a long-running conversation inside
  the model's context window

### The problem it solves

A plain `create_agent` handles a bounded, single-thread task well. It does not, by itself, handle
"go research this for the next forty tool calls, keep track of what you've tried, delegate the parts
that don't need the main thread's context, and don't let the transcript blow the context window
before you're done." That is a different, harder problem, and DeepAgents exists because enough teams
were re-solving it by hand that the LangChain organisation extracted it into a reusable harness.

### Where it sits in the ecosystem

DeepAgents is built **on top of** `create_agent` and LangGraph — it is not an alternative runtime, it
is an opinionated configuration of the same one. Everything documented in `../workspace-integration-examples/01-langchain-examples.md`
and `../workspace-integration-examples/02-langgraph-examples.md` (middleware, checkpointing, `interrupt()`, typed state) still applies
underneath it. Choosing DeepAgents is a decision about **how much of that configuration you want
pre-made for you**, not a decision to leave the LangChain/LangGraph stack.

### Enterprise framing

The honest way to describe DeepAgents to a non-technical stakeholder: it is the difference between
"an agent that can answer one question well" and "an agent that can be handed an open-ended
assignment and work it for an extended session, taking notes and asking for help from specialists
along the way." The cost of that capability is **surface area** — more moving parts, more defaults to
understand, and (per the research report's Finding 15 / Addendum) a governance obligation that a
simple agent doesn't have: DeepAgents' headline feature, dynamic sub-agent spawning, is emergent
topology by construction, and ASGF's Layer 5 standard explicitly prohibits emergent topology without
declared design intent. Adopting DeepAgents responsibly means declaring the subagent roster up front,
not letting the framework decide it at runtime.

---

## 2. Usage

### Installation

```powershell
pip install deepagents langchain langgraph
```

Resolved, tested versions in this workspace (`requirements.lock.txt` in `supporting/enterprise-examples/`):
`deepagents==0.6.12`, `langchain==1.3.14`, `langgraph==1.2.9`. Per the assessment's security floors
(`../workspace-integration-examples/00-conventions-and-baseline.md` §3), pin these exactly in any environment that persists agent
state — the floor is `langgraph>=1.0.10` and `langgraph-checkpoint-sqlite>=3.0.1`.

### What "live-executed" means for the example below

> **Read this before trusting the example.** `create_deep_agent` was called for real, with a real
> compiled LangGraph, and it ran to completion — but no real LLM was involved, because no
> Anthropic/OpenAI API key is available in this environment. A fake model was used instead, and
> getting it to run surfaced a genuine, reproducible fact about DeepAgents worth knowing before you
> build on it:
>
> **DeepAgents always registers its built-in tools (planning, filesystem) regardless of what you pass
> to `tools=`.** A bare `create_agent(tools=[])` can run against a model that doesn't support tool
> calling at all. `create_deep_agent(tools=[])` cannot — it unconditionally calls
> `model.bind_tools(...)` during its first model node, because the built-in tools are always present.
> Confirmed directly: `langchain_core`'s stock fake chat models
> (`FakeListChatModel`, `GenericFakeChatModel`) don't implement `bind_tools` and raise
> `NotImplementedError` when DeepAgents tries. **Practical implication for your own testing:** if you
> want to unit-test a DeepAgents pipeline without hitting a real provider, your fake model needs a
> `bind_tools` method (even a no-op one) — a plain `FakeListChatModel` is not enough, unlike testing a
> bare `create_agent`.

```python
"""Minimal, live-executed DeepAgents example.

Demonstrates the smallest correct invocation: a planning-and-filesystem-capable
agent with state confined to the graph (never touching the host disk), run
against a fake model. Swap `model=` for a real provider in production — see
the "Enterprise defaults" block below for what changes when you do.
"""

from typing import Any

from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from langchain_core.language_models.fake_chat_models import FakeListChatModel


class ToolCapableFakeChatModel(FakeListChatModel):
    """FakeListChatModel + a no-op bind_tools.

    DeepAgents always registers built-in tools (see the box above), so any
    fake model used to test a DeepAgents pipeline needs to survive a
    bind_tools() call. This is testing infrastructure only — never use a fake
    model in production; it is here so this example runs without an API key.
    """

    def bind_tools(self, tools: list, **kwargs: Any) -> "ToolCapableFakeChatModel":
        return self  # no-op: accept and ignore the tool schema


model = ToolCapableFakeChatModel(
    responses=["Deep agent response: task acknowledged, no tool calls needed."]
)

# StateBackend keeps the agent's "filesystem" inside checkpointed graph state.
# Nothing touches the host disk. This is the SAFE default — see §1's governance
# note and the FilesystemBackend example further down for when real disk
# access is actually warranted, and how to confine it.
agent = create_deep_agent(
    model=model,
    tools=[],  # your domain tools go here; DeepAgents' own tools are always added on top
    system_prompt=(
        "You are a research assistant. Use the todo list for anything with more "
        "than two steps. Write intermediate findings to files rather than "
        "holding them only in conversation, so they survive a context trim."
    ),
    backend=StateBackend(),
)

result = agent.invoke({"messages": [{"role": "user", "content": "Summarise the Q3 roadmap risks."}]})

print(result["messages"][-1].content)
# -> "Deep agent response: task acknowledged, no tool calls needed."
print(sorted(result.keys()))
# -> ['files', 'messages']   <- note the 'files' key: DeepAgents' state schema
#                                extends AgentState with a virtual filesystem,
#                                confirmed live in this session.
```

**Real output from this session:**

```
Deep agent response: task acknowledged, no tool calls needed.
['files', 'messages']
```

### Enterprise defaults — what to change before production

```python
"""Enterprise-configured DeepAgents instance.

Every deviation from the minimal example above is commented with WHY, not
just what — this is the reference shape for a production deployment in this
workspace, not a toy.
"""

import sqlite3
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.sqlite import SqliteSaver

# corpus_search_tool, production_model, PRODUCTION_SYSTEM_PROMPT are placeholders
# for YOUR domain tool, provider-backed chat model, and system prompt — not
# defined here. This block illustrates shape and defaults, not a runnable script.

# --- Governance: declare the subagent roster BEFORE writing this code, in a
# design review, not while writing it. ASGF L5 (Addendum Finding 15) requires
# topology to be documented before implementation; this list IS that document.
SUBAGENTS = [
    {
        "name": "retriever",
        "description": "Retrieves and cites passages from the approved corpus. Read-only.",
        "system_prompt": "Retrieve, cite verbatim, never summarise away the source.",
        "tools": [corpus_search_tool],  # a narrowly-scoped tool, not the parent's full toolset
    },
]

# --- Blast radius: FilesystemBackend touches real disk. root_dir MUST be a
# disposable, dedicated directory — never the repository root, never a home
# directory. This workspace's own governance documents (CLAUDE.md, pipeline.md
# files, .mcp.json) are Markdown/JSON an agent with unrestricted disk access
# could rewrite. See supporting/03 §3 for the full argument.
#
# virtual_mode=True is NOT optional. Verified 2026-07-27
# (workspace-integration-examples/verification/tests/test_03_deepagents_examples.py):
# the library's own default (virtual_mode=False) lets a ".." path segment or an
# absolute path escape root_dir entirely — root_dir alone does not confine anything.
backend = FilesystemBackend(root_dir=Path("./.agent-workspace/run-001"), virtual_mode=True)

# --- Durability + human-in-the-loop: without a checkpointer, interrupt_on
# does nothing (it has nowhere to persist the pause). See supporting/02 §2-3
# for why the checkpointer is itself a security boundary, not a storage detail.
checkpointer = SqliteSaver(sqlite3.connect("./.agent-workspace/checkpoints.sqlite"))

agent = create_deep_agent(
    model=production_model,          # a real, tool-calling-capable chat model
    tools=[],
    system_prompt=PRODUCTION_SYSTEM_PROMPT,
    subagents=SUBAGENTS,
    backend=backend,
    interrupt_on={
        "write_file": True,          # ASGF L3 Required: irreversible ops gated
        "edit_file": True,
        "read_file": False,          # reads are cheap and reversible — don't gate them
    },
    checkpointer=checkpointer,       # REQUIRED for interrupt_on to have any effect
)
```

Wire the CC-00 ASGF governance middleware (token budgets, PII scrubbing, the four-slot context
structure) around this the same way `supporting/enterprise-examples/src/cc00_langchain/graphs/research_assistant.py`
does for a plain `create_agent` — DeepAgents accepts a `middleware=[...]` list too, and the ordering
rule from that project (governance middleware outermost, context-assembly middleware innermost)
applies identically.

---

## 3. Alternatives and rationale

| Option                                           | Choose it when                                                                                                                                                              | Trade-off against DeepAgents                                                                                                                                                                                                          |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bare `create_agent` + hand-picked middleware** | The task is bounded and single-thread; you don't need planning, filesystem, or delegation                                                                                   | Smaller surface, easier to audit — this is `supporting/03 §4`'s recommended pattern for most CC-00 agents. Costs you re-implementing planning/delegation if the task later grows into one that needs them.                            |
| **CrewAI**                                       | You want a role/task "crew" running in an afternoon, with a gentler learning curve                                                                                          | Materially faster time-to-first-working-agent (research report, Finding 4). Costs you LangGraph's durable checkpointing and `interrupt()` — CrewAI's control primitives are less mature.                                              |
| **AutoGen**                                      | The problem is genuinely open-ended multi-agent conversation, not a bounded task with subagents                                                                             | Better fit for research on emergent multi-agent dynamics. Costs you DeepAgents' opinionated, production-shaped defaults (planning, filesystem, context management) — AutoGen assumes you'll build more of that yourself.              |
| **Hand-rolled LangGraph `StateGraph`**           | You need a topology DeepAgents' assumptions don't fit (e.g. the hierarchical supervisor pattern in `../workspace-integration-examples/06-ecosystem-integration-example.md`) | Full control over topology and state shape. Costs you DeepAgents' pre-built planning/filesystem/summarisation middleware — you write it yourself, which `../workspace-integration-examples/02-langgraph-examples.md` shows how to do. |

**Rationale for choosing DeepAgents specifically, when it is chosen:** the deciding question is not
"is DeepAgents good" (it is — 26,797 stars, actively maintained, built by the same organisation as the
underlying runtime) but "does this task need what it pre-wires." A task that needs multi-step planning
across a long session, note-taking that survives context trimming, and bounded delegation to
specialists is exactly DeepAgents' design target, and building that by hand from bare `create_agent`
means re-implementing three separate pieces of middleware DeepAgents already ships, tested, as one
package. A task that doesn't need those three things should not pay for them — see `supporting/03`'s
own framing: "adopt it when the task is long-horizon and file-shaped... do not adopt it for a bounded
single-purpose agent."

---

## 4. Integrations

| Integrates with                         | How                                                                                                                                                                                                                                                             |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LangGraph** (required, not optional)  | `create_deep_agent` compiles to a `CompiledStateGraph` — every LangGraph primitive (`interrupt()`, checkpointers, time-travel) works on it unchanged. See `../workspace-integration-examples/02-langgraph-examples.md`.                                         |
| **`langchain-mcp-adapters`**            | Tools bridged from MCP servers via `MultiServerMCPClient.get_tools()` (see `04-langchain-mcp-adapters.md` in this folder) pass into `create_deep_agent(tools=...)` exactly like any other LangChain tool.                                                       |
| **CC-00 governance middleware**         | `middleware=[...]` composes with DeepAgents' own middleware. Ordering matters — see `supporting/03 §4` and `supporting/enterprise-examples/`'s `cc00_middleware_stack()` docstring for the load-bearing rule (context-assembly middleware must stay innermost). |
| **CC-00 `RAGPipeline`**                 | Wrap it as a tool (`supporting/enterprise-examples/src/cc00_langchain/rag_tool.py`'s ACL-closure pattern) and hand it to a subagent's `tools=` list, scoped to just the subagent that needs retrieval.                                                          |
| **Vector stores / embedding providers** | Not DeepAgents-specific — reached the same way as in any LangChain agent, through whatever tools you attach. DeepAgents adds no vector-store integration of its own.                                                                                            |
| **OpenTelemetry (not LangSmith)**       | Observability middleware (`ObservabilityMiddleware` in `supporting/enterprise-examples/`) wraps DeepAgents' model calls the same as any other `AgentMiddleware`. LangSmith remains excluded per the CEO's open-source-only constraint.                          |

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
