# agent-memory MCP Server

MCP server for this workspace's persistent agent memory system — episodic, semantic,
procedural, and reflection memory backed by a dedicated `qdrant-memory` Qdrant instance
(`http://localhost:6335`), physically separate from `workspace-knowledge`'s document knowledge
base instance (`qdrant-workspace`).

**Status:** `search_memory` and `health_check` are implemented and registered. Both tools are
timeout-guarded (never hang, even if the underlying Qdrant call does) and degrade gracefully
rather than raise. A write-capable `write_memory` tool also exists in this codebase (see
[Tools](#tools)); its activation status, safeguard design, and independent adversarial evaluation
are documented separately —
`telescope/2026-08-08-cc00-mcp-observability-stack/research-report.md` § Related Build —
`agent-memory` Write-Path Tool Status is the source of truth for that tool's current state (moved
there 2026-08-10 from the former standalone `13-write-path-implementation.md`). Full current
status for this server generally,
including open caveats, is tracked in `.claude/rules/mcp-governance.md`'s Registered Servers
table — treat that as the source of truth if it and this file ever disagree.

---

## How the memory system works

Four independent memory types, each its own Qdrant collection. **This is a distinct taxonomy
from `memory_store.py`'s four in-context runtime memory types** (episodic, semantic, procedural,
_working_ — see `engineering/context-engineering/CLAUDE.md`); three of the four names overlap but
the fourth diverges by design, not oversight — `working` memory is inherently ephemeral and never
persisted to Qdrant, so it has no collection here, while `reflection` is inherently persisted and
cross-session, so it has no in-context runtime slot there. Do not conflate the two lists.

| Memory type    | Collection          | Lifespan                  | Scoping                                           |
| -------------- | ------------------- | ------------------------- | ------------------------------------------------- |
| **Episodic**   | `memory_episodic`   | One session               | Requires `session_id` unless `cross_session=True` |
| **Semantic**   | `memory_semantic`   | Cross-session, persistent | Never session-scoped                              |
| **Procedural** | `memory_procedural` | Cross-session, persistent | Never session-scoped                              |
| **Reflection** | `memory_reflection` | Cross-session, persistent | Never session-scoped                              |

`memory_reflection` shares the collection's cross-session lifespan but not its record schema —
`search_memory` returns a differently-shaped `ReflectionRecord` payload for it (see
[`search_memory`](#search_memory) below), not the standard `MemoryRecord` shape the other three
share.

**Write path** (not exposed via this MCP server — see below): every write goes through
`PersistentMemorySink` and always appends to a durable, human-readable JSONL log _first_
(`engineering/context-engineering/memory/episodic/<session_id>.jsonl`, `semantic.jsonl`,
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
`telescope/2026-07-10-agent-memory-architecture/research-report.md` § Architecture Decisions and
Write-Path Security Posture.
Short version: `workspace-knowledge` is a stable, load-bearing server; memory tooling is newer
and carries more untested surface, so it gets its own process rather than risking the proven
one — the same blast-radius reasoning that already gave `qdrant-memory` its own container
instead of a collection inside `qdrant-workspace`.

This server does not reimplement memory logic — it imports
`engineering/context-engineering/implementations/memory_vector_store.py` (and, once a
maintenance-trigger tool exists, `memory_maintenance.py`), the same way
`workspace-knowledge/server.py` already imports across module boundaries for its `health_check`
tool. The engineering lives in `engineering/context-engineering/`; this server is the thin MCP
exposition layer over it.

---

## Folder Structure

```
agent-memory/
├── server.py             ← MCP server entry point (search_memory, health_check, write_memory)
├── write_gate.py         ← WriteConfirmationGate + quarantine promote/reject primitives
├── write_provenance.py   ← WriteProvenance/validate_provenance + WriteRateLimiter
├── write_tool.py         ← Testable core of write_memory
├── pyproject.toml        ← Python project definition
├── README.md             ← This file
├── .gitignore
├── scripts/              ← Disaster-recovery backup tooling for the JSONL memory log
│   ├── backup_memory_log.py
│   ├── register_backup_task.ps1
│   ├── register_backup_task.py    ← Linux/macOS counterpart, unverified (2026-08-14)
│   └── verify_backup_restore.py
└── tests/
    ├── conftest.py
    ├── test_server.py
    ├── test_write_gate.py
    ├── test_write_provenance.py
    ├── test_write_memory.py
    ├── test_write_path_adversarial_evaluation.py
    ├── test_read_constraints_reverification.py
    ├── health_comparison.py
    └── test_cross_server_health_comparison.py
```

This server has no dedicated `.venv/` **by design** — it runs from the shared environment at
`core-component-00/mcp-servers/.venv/`, together with `workspace-knowledge` and
`embedder-service`. `.mcp.json` points `"command"` directly at that venv's interpreter.

The environment is shared rather than per-server because `embedder_client.py` spawns
`embedder-service` with `sys.executable`: under per-server venvs the shared service's environment
would depend on whichever server started it first. See `mcp-servers/CLAUDE.md` § Python Environment
for the full rationale and the interpreter-resolution chain.

Install/repair, from the repo root — the venv interpreter path differs by OS, everything else is
identical:

```bash
# Linux/macOS
core-component-00/mcp-servers/.venv/bin/python -m pip install -e core-component-00/mcp-servers/agent-memory
```

```powershell
# Windows
core-component-00\mcp-servers\.venv\Scripts\python.exe -m pip install -e core-component-00\mcp-servers\agent-memory
```

---

## Installation

The `docker run` line continuation differs by shell (`` ` `` in PowerShell, `\` in bash/zsh) —
everything else below is identical across platforms:

```bash
# Linux/macOS — start the dedicated qdrant-memory container (separate from qdrant-workspace)
docker run -d --name qdrant-memory \
  -p 6335:6333 -p 6336:6334 \
  -v qdrant_memory_store:/qdrant/storage \
  qdrant/qdrant
```

```powershell
# Windows — start the dedicated qdrant-memory container (separate from qdrant-workspace)
docker run -d --name qdrant-memory `
  -p 6335:6333 -p 6336:6334 `
  -v qdrant_memory_store:/qdrant/storage `
  qdrant/qdrant
```

```
# Or, if already created (any OS):
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
      "command": "${CLAUDE_PROJECT_DIR:-.}/core-component-00/mcp-servers/.venv/Scripts/python.exe",
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

`command` is a direct, absolute path to the shared venv's interpreter — not a bare command name
resolved via `PATH`. A 2026-08-13 attempt to make this resolve automatically per-OS via
`uv run` + `UV_PROJECT_ENVIRONMENT` broke live `/mcp reconnect` in production (the Claude Code host
process resolves `PATH` from its own long-lived environment, which didn't include a `uv` installed
after the host started) and was reverted — see
`core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`. **A
Linux/macOS deployment must manually change this path's `Scripts/python.exe` to `bin/python`** —
this is a documented one-line edit, not automatic; see
`core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.

The `NO_PROXY`/`no_proxy` pair works around a Windows-specific issue where `qdrant-client`'s
HTTP transport can be intercepted by a system proxy invisible to the usual environment
variables — see the deployment guidelines linked above for detail.

### Shared Infrastructure Dependency

`search_memory` optionally routes embedding through `embedder-service` — a persistent,
localhost-only process shared with `workspace-knowledge` — instead of loading
`all-MiniLM-L6-v2` in-process on every launch. Full architecture, lifecycle, and config surface:
`.claude/rules/mcp-governance.md` § "Shared Infrastructure — `embedder-service`".

| Env var                    | Default | Effect                                                                                                    |
| -------------------------- | ------- | --------------------------------------------------------------------------------------------------------- |
| `EMBEDDER_SERVICE_ENABLED` | `true`  | `false` skips the service entirely and always uses `_get_in_process_embedder()`'s background-loaded copy. |

If `embedder-service` is down, unreachable, or returns a wrong-dimension vector, `search_memory`
falls back to the in-process embedder automatically — never raises, degrades per the table above.

---

## Tools

### `search_memory`

Read-only semantic search over one memory collection. Never raises — every failure mode
(unknown `memory_type`, missing session scope, unavailable embedder, unreachable or slow
Qdrant) returns an empty result with `degraded: true` and a `reason`, and every underlying
Qdrant call is timeout-guarded (8s) so a stalled network call degrades the response instead of
hanging it.

| Parameter          | Default  | Notes                                                                                                                                               |
| ------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `query`            | required | Text to embed and search with                                                                                                                       |
| `memory_type`      | required | `episodic` \| `semantic` \| `procedural` \| `reflection` — `reflection` returns a `ReflectionRecord` payload, not the standard `MemoryRecord` shape |
| `top_k`            | `5`      | Clamped to `[1, 50]`                                                                                                                                |
| `session_id`       | `null`   | Required for `episodic` unless `cross_session=True`                                                                                                 |
| `cross_session`    | `false`  | `episodic` only — search across all sessions                                                                                                        |
| `include_dormant`  | `false`  | Widen beyond `status=active`                                                                                                                        |
| `include_archived` | `false`  | Widen beyond `status=active`                                                                                                                        |

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

Reachability and point counts for `qdrant-memory`'s four collections, plus dormant ratio and
last consolidation time, under a `memory_instance` key:

```json
{
  "memory_instance": {
    "reachable": true,
    "point_counts": {
      "memory_episodic": 0,
      "memory_semantic": 0,
      "memory_procedural": 0,
      "memory_reflection": 4
    },
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

### `write_memory`

A write-capable counterpart to `search_memory`, accepting new episodic, semantic, or procedural
content plus non-optional provenance metadata (source, triggering-context excerpt, whether the
triggering context included externally-read content, and a confidence value). Every write is
rate-limited per session and per session-per-memory-type, scanned for embedded-instruction
patterns, and — depending on whether it collides with an existing record — either lands
immediately in a review-pending quarantine lane or requires a human-facing confirmation step
before becoming retrievable. There is no `sacred`, `importance`, or `status` parameter: those
fields are always derived internally, never caller-supplied.

Every write today still goes through the same durable path described above
(`PersistentMemorySink` and the JSONL log) for writes originating from trusted internal runtime
code; `write_memory` is a second, MCP-agent-callable write surface with its own independent
safeguard design. Full design rationale, safeguard mechanics, activation status, and an
independent adversarial evaluation against the real implementation:
`telescope/2026-07-10-agent-memory-architecture/supporting/13-write-path-implementation.md`.

---

## Disaster Recovery — Backup Scripts

Three standalone scripts under `scripts/` back up the JSONL memory log itself — a different
failure class from the Qdrant-outage resilience already covered by
`telescope/2026-07-10-agent-memory-architecture/supporting/05-disaster-recovery-and-resilience.md`
(that document's zero-RPO guarantee assumes the JSONL log survives; these scripts cover what
happens if it doesn't — disk failure, accidental deletion, host loss).

| Script                     | Purpose                                                                                                                                                                                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `backup_memory_log.py`     | Snapshots `engineering/context-engineering/memory/` to a dated directory, keeping a rolling window of recent snapshots                                                                                                                                      |
| `register_backup_task.ps1` | Registers a daily Windows Task Scheduler job to run the backup script                                                                                                                                                                                       |
| `register_backup_task.py`  | Linux/macOS counterpart — registers a systemd `--user` timer or crontab entry. **Written 2026-08-14, UNVERIFIED** — no non-Windows machine available to test against; see its own docstring and the maintenance-record log entry below before relying on it |
| `verify_backup_restore.py` | Replays a snapshot into a disposable test Qdrant collection via `rebuild_from_log()` and checks record counts, then cleans up                                                                                                                               |

`backup_memory_log.py` and `verify_backup_restore.py` are plain Python and already cross-platform.
`register_backup_task.ps1` (Windows Task Scheduler) and `register_backup_task.py` (Linux systemd
timer or crontab, macOS crontab only — launchd not implemented) are two separate scripts, not one
ported implementation, since `Register-ScheduledTask`, `systemctl`, and `crontab` have no shared
API to port between — see
`core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`
for the full history of both.
**Open gap, still not activated anywhere:** this whole DR-backup path is INACTIVE by default (see
each script's own `STATUS` docstring) — nothing currently depends on either script running on any
platform. `register_backup_task.py` exists now so the gap isn't indefinitely deferred, but it has
never been run for real on Linux or macOS — confirm it actually registers and fires before treating
it as DR-ready, and note the macOS launchd gap (cron is TCC-restricted on modern macOS) is still
open.

Full design, proposed RTO/RPO, and current status:
`supporting/02-deployment-guidelines.md` §9 (merged there 2026-08-10 from the former standalone
`12-dr-backup-design.md`).

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
path is ever reached) is genuinely unavailable — it never raises. A background-load stall on one
of the embedder's transitive imports was previously observed in some live server processes on
this environment; it is now resolved via a lazy embedder warmup (root-caused and fixed —
the telescope incident record was removed 2026-08-13 as a completed maintenance-operation, per
`.claude/rules/mcp-governance.md`'s `agent-memory` row). Full status, including prior
investigation history, is tracked in
`.claude/rules/mcp-governance.md`. This server has no private per-server model cache and no
dependency on `workspace-knowledge`'s process, state, or cache — the shared cache is a filesystem
convention both read independently, not a coupling between the two servers.

---

## Governance and Status

Registered in `.mcp.json` and `.claude/rules/mcp-governance.md`'s Registered Servers table.
Assessment Protocol: Capability ✅, Governance ✅, Completeness ⚠️. `search_memory` and
`health_check` are verified correct (22 unit tests, live-Qdrant plumbing checks, and live
end-to-end MCP calls). Open caveats, both tracked in `.claude/rules/mcp-governance.md` rather
than duplicated here to avoid drift:

1. The embedder background-load stall described above is now resolved (root-caused and fixed —
   see `.claude/rules/mcp-governance.md`'s `agent-memory` row; the telescope incident record was
   removed 2026-08-13 as a completed maintenance-operation).
2. `memory_reflection` holds 4 real records (`REFLECT-001`–`004`, migrated 2026-07-15 from the
   retired mistake-log); `memory_episodic`/`memory_semantic`/`memory_procedural` still hold zero
   (no production memory writes exist yet), so retrieval _quality_ against real content remains
   unverified for those three.

---

## Ownership

Owned and maintained by **CC-00 Lab**, reporting to **Dr. Elias Vance** (Lab Director).
Executing engineers: **Mei-Ling Zhao** (Context Engineering — memory storage/decay logic) and
**Sofia Almeida** / **Diego Fontán** (Retrieval-Augmented Generation — retrieval/embedding
integration). Full design history: `telescope/2026-07-10-agent-memory-architecture/`.
