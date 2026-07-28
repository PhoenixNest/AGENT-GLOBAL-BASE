# langchain-mcp-adapters — Enterprise User Manual

**Package:** `langchain-mcp-adapters` · **Stars:** 3,611 (2026-07-25) · **Status:** Active
**Verification status:** Installed (`langchain-mcp-adapters==0.3.0`) in this session's runnable
project. `MultiServerMCPClient`'s full constructor and `get_tools()` signatures were introspected
against the real installed package. The example in §2 is **live-executed**: a real MCP server was
started as a subprocess in this session, bridged through `MultiServerMCPClient`, and a tool call was
round-tripped successfully — the output shown is real, not illustrative.

---

## 1. Introduction

### What it is

`langchain-mcp-adapters` is a small, focused library with one job: convert MCP (Model Context
Protocol) servers into LangChain tools. An agent built on `create_agent` or `create_deep_agent` can
call `MultiServerMCPClient.get_tools()` and receive a list of ordinary `BaseTool` objects — one per
tool exposed by each connected MCP server — with no MCP-protocol code anywhere in the agent itself.

### The problem it solves

MCP is an open protocol for exposing tools, resources, and prompts to AI applications, independent of
which LLM framework the calling application uses. Without an adapter, "I have an MCP server" and "I
have a LangChain agent" are two systems that don't speak to each other without custom glue. This
library is that glue, maintained by the LangChain organisation itself, which matters because MCP's
protocol surface (session lifecycle, transport negotiation, tool-schema translation) is exactly the
kind of thing you do not want to hand-roll and then maintain against upstream protocol changes.

### Why this is the strongest integration point for this workspace specifically

The research report's Finding 10 makes the architectural case directly: this workspace already runs
two MCP servers — `workspace-knowledge` and `agent-memory` — that passed the three-gate inclusion
test in `.claude/rules/mcp-governance.md`. `langchain-mcp-adapters` means a LangChain agent can
consume those **existing, already-governed** servers as tools, without re-implementing retrieval in
LangChain and without duplicating the embedder behind them. The governance properties `mcp-governance.md`
already established carry over intact, because the tools are the same tools. This inverts the naive
"use LangChain for RAG" instinct — see `../workspace-integration-examples/04-langchain-mcp-adapters-examples.md` for the full
argument and the workspace-specific hazards (a `health_check` name collision between the two servers,
and two write-capable tools that should not reach an unattended agent) that this manual does not
repeat.

### Enterprise framing

For a non-technical stakeholder: this library is what lets "the tools we already built and secured"
and "the AI agent framework we're evaluating" work together without a rewrite on either side. It is
infrastructure glue, not a product in its own right — its value is entirely in what it connects.

---

## 2. Usage

### Installation

```powershell
pip install langchain-mcp-adapters langchain
```

Resolved, tested version: `langchain-mcp-adapters==0.3.0` (`requirements.lock.txt` in
`supporting/enterprise-examples/`).

### Live-executed example: bridging a real MCP server

```python
"""Bridge a real MCP server into LangChain tools and invoke one.

This is not illustrative — it was run in this session. `math_server.py` is a
minimal FastMCP server (part of the official `mcp` SDK, already a dependency of
langchain-mcp-adapters) exposing one tool, `add`. The pattern generalises
directly to this workspace's real MCP servers — see the production example
further down.
"""

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient


async def main() -> None:
    # "stdio" transport: the server runs as a local subprocess, communicating
    # over stdin/stdout. This is how BOTH of this workspace's production
    # servers (workspace-knowledge, agent-memory) are wired in .mcp.json.
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",          # the interpreter to launch the server with
                "args": ["/path/to/math_server.py"],
            },
        }
    )

    # get_tools() starts the subprocess, performs the MCP handshake, lists
    # available tools, and wraps each one as a langchain_core.tools.BaseTool.
    tools = await client.get_tools()
    print("Bridged tools:", [t.name for t in tools])

    # Each bridged tool is invoked exactly like any other LangChain tool.
    result = await tools[0].ainvoke({"a": 3, "b": 4})
    print("add(3, 4) via MCP ->", result)


asyncio.run(main())
```

**Real output from this session** (server: a 12-line FastMCP script exposing `add(a, b)`):

```
Bridged tools: ['add']
add(3, 4) via MCP -> [{'type': 'text', 'text': '7', 'id': 'lc_f61806d7-32a0-4788-86f2-9ff4fcd3f55d'}]
```

The return shape — a list of content blocks with `type`/`text`/`id` — is MCP's native tool-result
format, passed through by the adapter rather than flattened to a bare string. Downstream code should
extract `.text` from the blocks it expects, not assume a plain string.

### Production example: bridging this workspace's real servers, governed

```python
"""Bridging workspace-knowledge and agent-memory — with the governance layer
this workspace's own findings (research-report.md Finding 12) require.

Do NOT skip govern_mcp_tools(). Two concrete hazards exist in this workspace's
actual servers, found by reading their source directly:
  1. Both servers export a tool literally named `health_check` — a raw
     get_tools() call ships a name collision into the agent's tool list.
  2. workspace-knowledge exposes two WRITE-capable tools (`rebuild_index`,
     `upsert_document`) that passed the three-gate test for a human-supervised
     session, which is not the same risk profile as an unattended agent loop.
See ../workspace-integration-examples/04-langchain-mcp-adapters-examples.md §2-3 for the full govern_mcp_tools
implementation this imports.
"""

import os
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient

WORKSPACE_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
MCP_DIR = WORKSPACE_ROOT / "core-component-00" / "mcp-servers"
# The shared venv, NOT a bare "python" — a bare "python" resolves via PATH to
# the system interpreter and silently drops the CUDA-enabled torch/embedder
# stack (.claude/rules/mcp-governance.md, Python Environment section).
VENV_PYTHON = MCP_DIR / ".venv" / "Scripts" / "python.exe"

client = MultiServerMCPClient(
    {
        "workspace_knowledge": {
            "transport": "stdio",
            "command": str(VENV_PYTHON),
            "args": [str(MCP_DIR / "workspace-knowledge" / "server.py")],
            "env": {"WORKSPACE_ROOT": str(WORKSPACE_ROOT), "SEARCH_BACKEND": "qdrant"},
        },
        "agent_memory": {
            "transport": "stdio",
            "command": str(VENV_PYTHON),
            "args": [str(MCP_DIR / "agent-memory" / "server.py")],
            "env": {"MEMORY_QDRANT_URL": "http://localhost:6335"},
        },
    }
)

raw_tools = await client.get_tools()          # noqa: at module top-level, wrap in async main()
tools = govern_mcp_tools(raw_tools)            # namespaces the health_check collision, drops write tools
```

---

## 3. Alternatives and rationale

| Option                                                | Choose it when                                                                                            | Trade-off against `langchain-mcp-adapters`                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Raw `mcp` SDK client, hand-wired into tools**       | You need protocol-level control the adapter doesn't expose, or you're not using LangChain at all          | Full control. Costs you re-implementing tool-schema translation and session management — exactly what this library exists to avoid re-doing.                                                                                                                                                                                            |
| **Framework-native tool definitions (no MCP)**        | The tool only ever needs to be called from LangChain, and no other framework or client will ever reuse it | Simpler for that one case. Costs you MCP's whole value proposition: the same server becomes usable from Claude Desktop, other agent frameworks, or a human operator with zero extra work. This workspace's MCP servers are already used outside LangChain (by Claude Code itself), so this trade-off does not favour skipping MCP here. |
| **Direct Python function calls (no server boundary)** | The "tool" is really just workspace code the agent process can import directly                            | Lower latency, no subprocess overhead. Costs you the process isolation and governance boundary MCP provides — `.claude/rules/mcp-governance.md`'s three-gate test exists specifically because a tool exposed as a server is easier to audit and restrict than code imported inline.                                                     |

**Rationale for choosing `langchain-mcp-adapters` in this workspace specifically:** the alternative
question is never really "MCP vs. no MCP" — this workspace already committed to MCP servers as the
governed tool-exposure mechanism, independent of any LangChain decision. Given that commitment, the
only real choice is whether a LangChain agent reaches those servers through the maintained adapter
library or through hand-rolled protocol code. There is no credible case for the latter: the library is
maintained by the same organisation that owns the framework it bridges into, it is the officially
documented pattern, and it is small enough (3,611 stars, a focused single-purpose package) that its
own maintenance burden is low.

---

## 4. Integrations

| Integrates with                                       | How                                                                                                                                                                                                                                                                                                      |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`create_agent` / `create_deep_agent`**              | `get_tools()`'s return value passes directly into `tools=[...]` — no conversion step.                                                                                                                                                                                                                    |
| **This workspace's `workspace-knowledge` MCP server** | Bridged as shown in the production example above; requires `govern_mcp_tools()` per Finding 12 before reaching an agent.                                                                                                                                                                                 |
| **This workspace's `agent-memory` MCP server**        | Same pattern. Note the degradation caveat: `search_memory` never raises, it returns `degraded=True` on failure — an agent needs `MCPDegradationMiddleware` (`../workspace-integration-examples/04-langchain-mcp-adapters-examples.md` §4) to avoid reading an empty result as "no prior context exists." |
| **Any third-party MCP server**                        | Any server implementing the open MCP spec bridges the same way — `transport: "http"` for remote servers, `"stdio"` for local subprocesses (both shown in `../workspace-integration-examples/04-langchain-mcp-adapters-examples.md` §1).                                                                  |
| **CC-00 governance middleware**                       | Bridged tools are ordinary `BaseTool` objects, so `ToolGovernanceMiddleware` (the CC-00 tool whitelist) applies to them exactly as it does to any hand-written tool.                                                                                                                                     |
| **Claude Code / other MCP clients**                   | The reverse direction: because the server side speaks standard MCP, the same `workspace-knowledge`/`agent-memory` servers this library bridges into LangChain are also the servers Claude Code itself connects to (`.mcp.json`) — one server, multiple consuming clients, no duplication.                |

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
