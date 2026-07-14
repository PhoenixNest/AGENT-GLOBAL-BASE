# agent-memory MCP Server

MCP server for this workspace's persistent agent memory system — episodic, semantic, and
procedural memory backed by a dedicated `qdrant-memory` Qdrant instance
(`http://localhost:6335`), physically separate from `workspace-knowledge`'s document knowledge
base instance (`qdrant-workspace`).

**Status:** `search_memory` and `health_check` implemented and registered. Both tools are
timeout-guarded (never hang, even if the underlying Qdrant call does) and degrade gracefully
rather than raise. No write-capable tool yet (see [Tools](#tools)). Full current status,
including open caveats, is tracked in `.claude/rules/mcp-governance.md`'s Registered Servers
table — treat that as the source of truth if it and this file ever disagree.

---

## How the memory system works

Three independent memory types, each its own Qdrant collection, sharing one schema:

| Memory type    | Collection          | Lifespan                  | Scoping                                           |
| -------------- | ------------------- | ------------------------- | ------------------------------------------------- |
| **Episodic**   | `memory_episodic`   | One session               | Requires `session_id` unless `cross_session=True` |
| **Semantic**   | `memory_semantic`   | Cross-session, persistent | Never session-scoped                              |
| **Procedural** | `memory_procedural` | Cross-session, persistent | Never session-scoped                              |

**Write path** (not exposed via this MCP server — see below): every write goes through
`PersistentMemorySink` and always appends to a durable, human-readable JSONL log _first_
(`context-engineering/memory/episodic/<session_id>.jsonl`, `semantic.jsonl`,
`procedural.jsonl`) — that log is the source of truth. The write then embeds the content
(`all-MiniLM-L6-v2`) and upserts it into the matching Qdrant collection as a derived, rebuildable
index, exactly the same "log is truth, Qdrant is a derived index" pattern already used for the
document corpus. A Qdrant hiccup on write degrades to "index is stale until rebuild," never a
lost write.

**Read path** (this server): `search_memory` embeds the query and does a filtered semantic
search against one collection.

**Record lifecycle**, tracked per-record and relevant to what `search_memory` returns:

- `status`: `active` → `dormant` → `archived`, driven by a decay pass (not run by this server).
  `search_memory` only returns `active` records by default; pass `include_dormant=True` /
  `include_archived=True` to widen that.
- `sacred`: a record can be pinned so decay never moves it out of `active` — there is no
  parameter to exclude sacred records, since they're always already inside the default filter.
- `importance` / `confidence` / `decay_weight`: set by a write-time heuristic or the (separate)
  maintenance pass, not by this server or its callers.

Full design rationale: `telescope/2026-07-10-agent-memory-architecture/research-report.md` and
its `supporting/` folder.

---

## Why a separate server from `workspace-knowledge`

Decided by the CEO on Laboratory Director recommendation — full rationale in
`telescope/2026-07-10-agent-memory-architecture/supporting/09-mcp-architecture-decision.md`.
Short version: `workspace-knowledge` is a stable, load-bearing server; memory tooling is newer
and carries more untested surface, so it gets its own process rather than risking the proven
one — the same blast-radius reasoning that already gave `qdrant-memory` its own container
instead of a collection inside `qdrant-workspace`.

This server does not reimplement memory logic — it imports
`context-engineering/implementations/memory_vector_store.py` (and, once a maintenance-trigger
tool exists, `memory_maintenance.py`), the same way `workspace-knowledge/server.py` already
imports across module boundaries for its `health_check` tool. The engineering lives in
`context-engineering/`; this server is the thin MCP exposition layer over it.

---

## Folder Structure

```
agent-memory/
├── server.py          ← MCP server entry point (search_memory, health_check)
├── pyproject.toml     ← Python project definition
├── README.md          ← This file
├── .gitignore
└── tests/
    └── test_search_memory.py   ← Local eval harness (uncommitted, see file header)
```

No dedicated `.venv/` is currently provisioned for this server (unlike `workspace-knowledge`,
which has one) — `server.py`'s venv-bootstrap code falls back to system Python automatically if
`.venv/` is absent, and the required packages currently happen to be present there. This is a
gap against the workspace's own isolation convention, not a design choice; provisioning a proper
`.venv/` is open follow-up work.

---

## Installation

```powershell
# Start the dedicated qdrant-memory container (separate from qdrant-workspace)
docker run -d --name qdrant-memory `
  -p 6335:6333 -p 6336:6334 `
  -v qdrant_memory_store:/qdrant/storage `
  qdrant/qdrant

# Or, if already created:
docker start qdrant-memory

# Provision the embedding model into the shared cache (one-time; shared across CC-00 servers)
python core-component-00/mcp-servers/_shared/provision_model.py sentence-transformers/all-MiniLM-L6-v2

# Warm the import/OS file cache for that model (one-time per machine; run before
# starting the server for real, not reactively on its first request — see the
# background-load stall note under Embedding model below)
python core-component-00/mcp-servers/_shared/warm_embedder_cache.py
```

Full deployment detail (collection creation, Windows-specific proxy note, performance targets):
`telescope/2026-07-10-agent-memory-architecture/supporting/02-deployment-guidelines.md`.

---

## Configuration

Registered in the project-root `.mcp.json`:

```json
{
  "mcpServers": {
    "agent-memory": {
      "command": "python",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/core-component-00/mcp-servers/agent-memory/server.py"],
      "env": {
        "MEMORY_QDRANT_URL": "http://localhost:6335",
        "FASTMCP_LOG_LEVEL": "ERROR",
        "NO_PROXY": "localhost,127.0.0.1",
        "no_proxy": "localhost,127.0.0.1"
      }
    }
  }
}
```

The `NO_PROXY`/`no_proxy` pair works around a Windows-specific issue where `qdrant-client`'s
HTTP transport can be intercepted by a system proxy invisible to the usual environment
variables — see the deployment guidelines linked above for detail.

---

## Tools

### `search_memory`

Read-only semantic search over one memory collection. Never raises — every failure mode
(unknown `memory_type`, missing session scope, unavailable embedder, unreachable or slow
Qdrant) returns an empty result with `degraded: true` and a `reason`, and every underlying
Qdrant call is timeout-guarded (8s) so a stalled network call degrades the response instead of
hanging it.

| Parameter          | Default  | Notes                                               |
| ------------------ | -------- | --------------------------------------------------- |
| `query`            | required | Text to embed and search with                       |
| `memory_type`      | required | `episodic` \| `semantic` \| `procedural`            |
| `top_k`            | `5`      | Clamped to `[1, 50]`                                |
| `session_id`       | `null`   | Required for `episodic` unless `cross_session=True` |
| `cross_session`    | `false`  | `episodic` only — search across all sessions        |
| `include_dormant`  | `false`  | Widen beyond `status=active`                        |
| `include_archived` | `false`  | Widen beyond `status=active`                        |

Example call:

```json
{ "query": "what database did the user choose", "memory_type": "semantic", "top_k": 3 }
```

Example response (healthy):

```json
{
  "results": [{ "id": "...", "content": "user_stack: Prefers FastAPI, PostgreSQL", "...": "..." }],
  "count": 1,
  "degraded": false,
  "reason": null
}
```

Example response (degraded — embedder not ready yet on this process):

```json
{
  "results": [],
  "count": 0,
  "degraded": true,
  "reason": "embedding model still loading (background warmup in progress on this server process — retry shortly)"
}
```

### `health_check`

Reachability and point counts for `qdrant-memory`'s three collections, plus dormant ratio and
last consolidation time, under a `memory_instance` key:

```json
{
  "memory_instance": {
    "reachable": true,
    "point_counts": { "memory_episodic": 0, "memory_semantic": 0, "memory_procedural": 0 },
    "last_consolidation_at": null,
    "dormant_ratio": 0.0
  }
}
```

Same shape and same `compute_memory_instance_telemetry()` call as
`workspace-knowledge/server.py`'s `health_check` `memory_instance` block, so either server's
`health_check` returns identical memory telemetry — this server's version has no
`document_knowledge_base` block, since it doesn't own that data. Like `search_memory`, every
underlying Qdrant call is timeout-guarded, so an unreachable or slow `qdrant-memory` reports
`reachable: false` instead of hanging the call.

### Write tool — not implemented

Explicitly **not planned yet**. Every memory write today happens through `PersistentMemorySink`,
called by trusted internal runtime code, not through this MCP server. Exposing a write tool
changes that threat model — anything that can get an agent to call a tool could write directly
into persistent memory. Deferred until it has been through an adversarial evaluation targeting
prompt-injected write attempts, matching the rigor already applied to the contradiction-check
(`supporting/07-adversarial-evaluation-results.md`).

---

## Embedding model

The memory collections were built for `sentence-transformers/all-MiniLM-L6-v2` (384-dim) —
different and incompatible with `workspace-knowledge`'s `all-mpnet-base-v2` (768-dim). The model
is provisioned in the shared cache at
`core-component-00/mcp-servers/_shared/models/sentence-transformers--all-MiniLM-L6-v2/` via
`_shared/provision_model.py` — the standing convention for embedding-model provisioning across
all CC-00 MCP servers (see `.claude/rules/mcp-governance.md`).

`_get_embedder()` in `server.py` loads the model in a background thread at process startup so
the first `search_memory` call is never blocked on it; `search_memory` degrades gracefully with
a `reason` explaining whether the embedder is still loading, failed to load, or (if this code
path is ever reached) is genuinely unavailable — it never raises. Known caveat: on this
environment, that background load has been observed to stall indefinitely on one of its
transitive imports in a live server process, even though the same import completes in well
under a second in isolation — tracked as an open Completeness gap in
`.claude/rules/mcp-governance.md`, not yet root-caused. This server has no private per-server
model cache and no dependency on `workspace-knowledge`'s process, state, or cache — the shared
cache is a filesystem convention both read independently, not a coupling between the two
servers.

---

## Governance and Status

Registered in `.mcp.json` and `.claude/rules/mcp-governance.md`'s Registered Servers table.
Assessment Protocol: Capability ✅, Governance ✅, Completeness ⚠️. `search_memory` and
`health_check` are verified correct (22 unit tests, live-Qdrant plumbing checks, and live
end-to-end MCP calls). Open caveats, both tracked in `.claude/rules/mcp-governance.md` rather
than duplicated here to avoid drift:

1. The embedder background-load stall described above — `search_memory` currently cannot
   reliably return non-degraded results on this environment until it's root-caused.
2. The live collections still hold zero real records (no production memory writes exist yet),
   so retrieval _quality_ against real content is unverified independent of (1).

---

## Ownership

Owned and maintained by **CC-00 Lab**, reporting to **Dr. Elias Vance** (Lab Director).
Executing engineers: **Mei-Ling Zhao** (Context Engineering — memory storage/decay logic) and
**Sofia Almeida** / **Diego Fontán** (Retrieval-Augmented Generation — retrieval/embedding
integration). Full design history: `telescope/2026-07-10-agent-memory-architecture/`.
