# 04 — LangChain MCP Adapters Examples (`langchain-mcp-adapters`)

**Prerequisite:** `00-conventions-and-baseline.md`.
**Status:** Reference examples. **Not executed.** `MultiServerMCPClient` API verified against
`langchain-ai/docs` via Context7 on 2026-07-26. MCP server tool names, signatures, and `.mcp.json`
wiring verified by direct read of this workspace's files on 2026-07-26.

---

## Why this is the most important file in the folder

Finding 10 inverted the obvious integration story, and it is worth restating in full because
everything below follows from it:

> The instinct is "use LangChain for RAG" — but `retrieval-augmented-generation/` already has
> `chunker.py`, `retrieval.py` (BM25 + RRF + ACL filtering), and `pipeline.py`, and the ACL filtering
> in particular is an ASGF L4 **Required** item that CC-00 has and LangChain does not provide out of
> the box. **Replacing working, compliant CC-00 RAG with LangChain RAG would trade an ASGF asset for
> a gap.**

`langchain-mcp-adapters` is what makes the correct architecture possible. It converts MCP servers
into LangChain tools — so a LangChain agent consumes the **existing, already-three-gate-approved**
`workspace-knowledge` and `agent-memory` servers as tools, without re-implementing retrieval and
without duplicating the embedder. The governance properties established by
`.claude/rules/mcp-governance.md` carry over intact, because **they are the same tools**.

That is the whole architectural argument: LangChain sits _above_ CC-00's retrieval layer, not in
place of it.

---

## What this workspace actually exposes

Verified by reading `.mcp.json` and both `server.py` files on 2026-07-26.

### `workspace-knowledge` — 13 tools

| Tool                                                | Kind      | Notes for agent exposure                                  |
| --------------------------------------------------- | --------- | --------------------------------------------------------- |
| `search_docs(query, top_k=10)`                      | read      | The primary retrieval entry point                         |
| `retrieve_context(file_path)`                       | read      | Full document by path                                     |
| `find_related_documents(seed_doc_path, top_k=5)`    | read      | Similarity expansion from a seed                          |
| `summarize_context(topics, max_docs_per_topic=3)`   | read      | Multi-topic digest                                        |
| `list_research_by_topic(topic, format="brief")`     | read      | Telescope archive query                                   |
| `agent_knowledge_brief(agent_role, context_topics)` | read      | Role-scoped briefing                                      |
| `check_adr_precedent(technology)`                   | read      | Governance lookup                                         |
| `validate_pipeline_document(doc_path)`              | read      | Advisory validation                                       |
| `list_indexed_files()`                              | read      | Index introspection                                       |
| `rebuild_status()`                                  | read      | Index introspection                                       |
| **`rebuild_index()`**                               | **write** | **Mutates the index. See §3 — do not expose by default.** |
| **`upsert_document(file_path)`**                    | **write** | **Mutates the index. See §3 — do not expose by default.** |
| `health_check()`                                    | read      | **Name collides with `agent-memory`. See §2.**            |

### `agent-memory` — 2 tools

| Tool                                                                                                                              | Kind | Notes                                                 |
| --------------------------------------------------------------------------------------------------------------------------------- | ---- | ----------------------------------------------------- |
| `search_memory(query, memory_type, top_k=5, session_id=None, cross_session=False, include_dormant=False, include_archived=False)` | read | Read-only, never raises, degrades to `degraded=True`  |
| `health_check()`                                                                                                                  | read | **Name collides with `workspace-knowledge`. See §2.** |

Both servers are read-dominant and neither can advance a pipeline stage, modify an ADR, or change an
approval record — which is why both passed Gate 2 (Governance) of the inclusion charter. That
property is what makes them safe to hand to an agent.

---

## Example 1 — Bridging the workspace's MCP servers

**Use when:** any LangChain agent in this workspace needs knowledge or memory.

```python
"""Example 1 — the existing governed servers, as LangChain tools.

The .mcp.json entries use ${CLAUDE_PROJECT_DIR}, which is a Claude Code host
variable and is NOT set for a standalone Python process. Resolve it explicitly.

The interpreter is the shared venv at core-component-00/mcp-servers/.venv/ —
NOT a bare "python". A bare "python" resolves via PATH to the system interpreter
and silently reintroduces both the global dependency and a possible CPU-only
torch. This is documented as a defect in .claude/rules/mcp-governance.md and it
is just as much a defect here.
"""

import asyncio
import os
from pathlib import Path

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

WORKSPACE_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
MCP_DIR = WORKSPACE_ROOT / "core-component-00" / "mcp-servers"
VENV_PYTHON = MCP_DIR / ".venv" / "Scripts" / "python.exe"      # Windows; posix: bin/python

MCP_SERVERS = {
    "workspace_knowledge": {
        "transport": "stdio",
        "command": str(VENV_PYTHON),
        "args": [str(MCP_DIR / "workspace-knowledge" / "server.py")],
        "env": {
            "WORKSPACE_ROOT": str(WORKSPACE_ROOT),
            "FASTMCP_LOG_LEVEL": "ERROR",
            "SEARCH_BACKEND": "qdrant",
            "NO_PROXY": "localhost,127.0.0.1",
            "no_proxy": "localhost,127.0.0.1",
        },
    },
    "agent_memory": {
        "transport": "stdio",
        "command": str(VENV_PYTHON),
        "args": [str(MCP_DIR / "agent-memory" / "server.py")],
        "env": {
            "MEMORY_QDRANT_URL": "http://localhost:6335",
            "FASTMCP_LOG_LEVEL": "ERROR",
            "NO_PROXY": "localhost,127.0.0.1",
            "no_proxy": "localhost,127.0.0.1",
        },
    },
}


async def build_agent():
    client = MultiServerMCPClient(MCP_SERVERS)
    tools = await client.get_tools()
    tools = govern_mcp_tools(tools)          # §2 and §3 — do not skip this line

    return create_agent(
        model="anthropic:claude-sonnet-5",
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        middleware=cc00_middleware_stack(
            system_prompt=SYSTEM_PROMPT, task_type="tool_research"
        ),
    )
```

**Two environment facts that will bite otherwise:**

1. `${CLAUDE_PROJECT_DIR:-.}` in `.mcp.json` is expanded by the Claude Code host. A standalone
   LangChain process gets the literal string unless you resolve it, as above.
2. The Qdrant containers (`qdrant-workspace`, `qdrant-memory`) must be running. Both servers degrade
   gracefully rather than crashing when they are not — `search_memory` returns `degraded=True` with a
   reason — so **a silently degraded agent is the realistic failure mode, not a loud one.** Check for
   `degraded` in tool results; see §4.

---

## Example 2 — The `health_check` name collision

**This is a concrete hazard in this workspace, found while writing this file.**

`MultiServerMCPClient.get_tools()` returns one flat list across all servers. Both
`workspace-knowledge` and `agent-memory` define a tool named **`health_check`**. Two tools with the
same name in one list means, at best, the model cannot express which one it wants — and at worst one
shadows the other silently.

```python
"""Example 2 — disambiguate at the bridge, and fail loudly on any new collision.

ASGF L3 "Tool registry / whitelist defined" is the requirement this serves: the
agent must not be able to invoke something outside a known, named set — and two
tools sharing a name means the set is not well-defined.
"""

from collections import Counter
from typing import Any


def govern_mcp_tools(tools: list[Any], server_of: dict[str, str] | None = None) -> list[Any]:
    """Namespace collisions, drop write tools, and fail loudly on surprises."""
    names = Counter(_tool_name(t) for t in tools)
    collisions = {name for name, count in names.items() if count > 1}

    if collisions - KNOWN_COLLISIONS:
        # A NEW collision means a server changed. That is a wiring change and it
        # should stop the process, not be papered over.
        raise ValueError(
            f"Unexpected MCP tool-name collision: {sorted(collisions - KNOWN_COLLISIONS)}. "
            "Namespace it explicitly before proceeding."
        )

    governed = []
    for tool in tools:
        name = _tool_name(tool)
        if name in WRITE_CAPABLE:          # §3
            continue
        if name in collisions:
            # Rename to <server>_<tool>. The description is prompt surface, so it
            # gets the disambiguation too — a renamed tool the model cannot tell
            # apart from its twin is not disambiguated.
            server = (server_of or {}).get(id(tool), "unknown")
            tool = _rename(tool, f"{server}_{name}", suffix=f" (server: {server})")
        governed.append(tool)
    return governed


KNOWN_COLLISIONS = {"health_check"}

WRITE_CAPABLE = {"rebuild_index", "upsert_document"}
```

**Simpler alternative, and often the right one:** don't bridge `health_check` at all. It is an
operator tool, not an agent tool — an agent has no useful action to take on the answer. Filtering it
out removes the collision and shrinks the tool list, which helps tool-selection accuracy anyway.

---

## Example 3 — Write-capable MCP tools are an authority decision

`workspace-knowledge` exposes two tools that mutate state: `rebuild_index()` and
`upsert_document(file_path)`. Both passed the three-gate inclusion test — correctly, since neither
advances a pipeline stage nor modifies a governance record — but **passing the gate for a
human-driven Claude Code session is not the same as being safe in an autonomous agent loop.**

The distinction that matters:

| Context                                 | Who decides to call `rebuild_index()`     | Risk                                                    |
| --------------------------------------- | ----------------------------------------- | ------------------------------------------------------- |
| Claude Code session (the gated context) | A human, or a model a human is watching   | Low — a wasted rebuild, observed                        |
| Autonomous LangChain agent              | The model, unattended, possibly in a loop | An agent that rebuilds the index repeatedly, unobserved |

**Default: exclude both** (the `WRITE_CAPABLE` set in §2). If an agent genuinely needs to keep the
index fresh, gate it rather than granting it:

```python
"""Example 3 — index mutation behind a human approval gate.

ASGF L3 "High-risk operations gated" is Required for high-risk operations. A full
index rebuild is expensive and unattended-repeatable, which is enough to qualify
in an autonomous loop even though it is not destructive.
"""

from cc00_langchain.cc00_path import TOOL_REGISTRY, ToolRegistry

# Register the MCP write tools in CC-00's registry so their limits live with every
# other tool's limits — one registry, one place to audit.
TOOL_REGISTRY["rebuild_index"] = {
    "description": "Rebuild the workspace-knowledge vector index. Expensive; whole-corpus.",
    "timeout_seconds": 900,
    "max_calls_per_task": 1,        # once per task, ever
    "requires_approval": True,      # enforced by the interrupt gate in 02 §3
    "input_schema": {"type": "object", "properties": {}},
}
```

Then route it through the `approval_gate` node from `02-langgraph-examples.md` §3, which reads
`requires_approval` from exactly this registry. The flag becomes load-bearing rather than decorative.

---

## Example 4 — Detecting silent degradation

**The failure mode this workspace actually has.** `agent-memory`'s `search_memory` never raises: on
an unavailable embedder, unreachable Qdrant, unknown `memory_type`, or missing session scope it
returns an empty result with `degraded=True` and a `reason`. That is correct server design — it never
blocks a tool call — but for an agent it means **an empty answer and a broken backend look identical
unless something checks.**

```python
"""Example 4 — surface degradation instead of silently reasoning over nothing.

Without this, an agent whose memory backend is down concludes "no prior context
exists" and proceeds confidently. That is the worst available outcome: a wrong
answer delivered with full confidence and no error anywhere.
"""

from typing import Any, Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest
from langchain.agents.middleware.types import ModelResponse


class MCPDegradationMiddleware(AgentMiddleware):
    """Turn `degraded: true` into something the agent and the operator both see."""

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        degraded = [
            (name, result.get("reason", "unspecified"))
            for name, result in (request.state.get("tool_outputs") or [])
            if isinstance(result, dict) and result.get("degraded")
        ]
        if not degraded:
            return handler(request)

        # Tell the MODEL, so it stops treating an empty result as evidence of absence.
        notice = "\n".join(
            f"- `{name}` returned DEGRADED results ({reason}). Treat its empty/partial "
            f"output as UNKNOWN, not as absence of evidence."
            for name, reason in degraded
        )
        warned = request.override(
            messages=[
                *request.messages,
                {"role": "system", "content": f"# Retrieval degradation notice\n{notice}"},
            ]
        )

        # And tell the OPERATOR, because a degraded run should be visible in the trace.
        with tracer.start_as_current_span("cc00.mcp.degraded") as span:
            span.set_attribute("cc00.degraded_tools", [name for name, _ in degraded])

        return handler(warned)
```

**Known live caveat, inherited:** three of the four `agent-memory` collections
(`memory_episodic`, `memory_semantic`, `memory_procedural`) hold **zero real records** — only
`memory_reflection` has content (`REFLECT-001`–`004`). This is the standing Completeness caveat in
`.claude/rules/mcp-governance.md`. An agent querying those three will get correct, honest, empty
answers. Do not build a capability that depends on them being populated until they are.

---

## Example 5 — CC-00 RAG stays first-party

**Use when:** you need retrieval with ACL filtering — which, in an enterprise setting, is whenever
retrieval results could differ by who is asking.

The MCP bridge covers workspace knowledge. For application corpora, the CC-00 RAG pipeline stays the
implementation, wrapped as a tool. This is the concrete form of "do not replace CC-00's retrieval
layer."

```python
"""Example 5 — CC-00 RAG behind a LangChain tool, ACL intact.

ASGF L4 "ACL filtering applied" is Required, and the research report is explicit
that LangChain does not supply it out of the box. RAGPipeline.query() takes
user_role and filters on it. That parameter is the requirement.
"""

from langchain.tools import tool

from cc00_langchain.cc00_path import RAGPipeline

pipeline = RAGPipeline(
    chunker=chunker,
    embedder=embedder,          # routes through the shared embedder-service
    vector_store=vector_store,
    top_k=10,                   # retrieve wide, rerank down — see below
)


def make_corpus_search(user_role: str):
    """Bind the ACL role at construction. The MODEL never gets to choose it.

    This is the load-bearing design decision in this example. If `user_role` were a
    tool PARAMETER, the model could pass "admin" and the ACL filter would dutifully
    honour it — prompt injection escalating to privilege escalation. Binding it in a
    closure at agent-construction time, from the authenticated session, makes that
    impossible to express.
    """

    @tool
    def search_corpus(query: str, top_k: int = 5) -> list[dict]:
        """Search the application corpus. Returns only documents you may see.

        Args:
            query: Natural-language query.
            top_k: Maximum results, capped at 10.
        """
        context = pipeline.query(query, user_role=user_role)   # ACL applied here
        return [
            {"content": chunk.text, "source": chunk.metadata.get("doc_id", "unknown"), "score": score}
            for chunk, score in zip(context.chunks[:min(top_k, 10)], context.scores)
        ]

    return search_corpus
```

**The standing L4 gap this does not close.** ASGF L4 "Reranking step implemented" is **Required** and
currently **unmet** in this workspace — Recommendation 1. `RAGPipeline` does BM25 + RRF
fusion, which is hybrid retrieval, not cross-encoder reranking. The fix is a ~560 MB cross-encoder
resident on the GPU alongside the embedding stack (there is ~7 GB free), and it does **not** depend on
the LangChain adoption decision. It is listed as P1 / 0.5 day in the research report. Retrieving
`top_k=10` above and truncating to 5 is a placeholder for the rerank step, not a substitute for it.

---

## Anti-pattern summary for this product

| Anti-pattern                                                   | Why it fails                                                                             |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Passing `await client.get_tools()` straight to `create_agent`  | Ships the `health_check` collision and both write-capable tools into an autonomous loop. |
| Re-implementing workspace retrieval in LangChain               | Trades an ASGF L4 asset (ACL filtering) for a gap. Finding 10.                           |
| `user_role` as a tool parameter                                | Prompt injection becomes privilege escalation. Bind it in a closure.                     |
| Treating an empty `search_memory` result as "no prior context" | Indistinguishable from a dead backend. Check `degraded`.                                 |
| `"command": "python"` in the server config                     | Resolves via PATH to the system interpreter. Named as a defect in `mcp-governance.md`.   |
| Exposing `rebuild_index` to an unattended agent                | Gate-passing in a supervised session ≠ safe in an autonomous loop.                       |
| Assuming `${CLAUDE_PROJECT_DIR}` expands outside Claude Code   | It does not. You get the literal string.                                                 |

---

**Document status:** Reference examples — unexecuted. Server tool inventory verified 2026-07-26.
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-26
