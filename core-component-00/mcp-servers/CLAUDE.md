# core-component-00/mcp-servers/ — CC-00 MCP Server Implementations

Production MCP server implementations exposed to Claude Code. This is the lab's deployment
surface — architecturally distinct from the five-module research stack under `engineering/` and
`retrieval-augmented-generation/`, though it depends on them.

---

## What Lives Here

Two live MCP servers, a shared model-provisioning convention, and a shared internal embedding
process (`embedder-service`) both servers depend on but which is not itself registered in
`.mcp.json`:

```
mcp-servers/
├── workspace-knowledge/     ← Document knowledge base (BM25 + semantic search over qdrant-workspace)
├── agent-memory/            ← Persistent agent memory (episodic/semantic/procedural/reflection over qdrant-memory)
└── _shared/
    ├── provision_model.py    ← Shared embedding-model provisioning (writes to _shared/models/<slug>/)
    └── embedder-service/     ← Persistent localhost-only HTTP embedding process; both servers route
                                 embed calls through it when available, each falling back to its own
                                 private in-process model load if it isn't. Not an MCP server itself —
                                 see .claude/rules/mcp-governance.md "Shared Infrastructure" section.
```

Each server carries its own `README.md` — read that first for the server's tool contract,
configuration, and setup. This file is a thin index, not a duplicate; do not let facts drift
between here and either README.

---

## Governance

Every server registered here must pass the Three-Gate Inclusion Test (Capability, Governance,
Completeness) before being added to root `.mcp.json`. Full gate definitions, the Registered
Servers status table — including open caveats and incident history — and the retirement
procedure are the authoritative source of truth at `.claude/rules/mcp-governance.md`. Treat that
file, not this one or either server's README, as canonical if they ever disagree.

---

## Where to Look

| I need…                                      | Go to                                |
| -------------------------------------------- | ------------------------------------ |
| A server's tools, contract, setup            | `<server>/README.md`                 |
| Gate status, caveats, incident history       | `.claude/rules/mcp-governance.md`    |
| Shared embedding-model provisioning          | `_shared/provision_model.py`         |
| Shared embedding process (not an MCP server) | `_shared/embedder-service/server.py` |

---

## Ownership

Owned by **CC-00 Lab**, reporting to **Dr. Elias Vance** (Lab Director). Per-server executing
engineers are listed in each server's own README.
