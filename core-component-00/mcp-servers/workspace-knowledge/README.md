# Workspace Knowledge MCP Server

RAG server for workspace documentation search and retrieval. Provides 11 MCP tools backed by a
three-tier search stack: **Qdrant** (primary) → **FAISS** (warm DR standby) → **BM25** (keyword
fallback). The system degrades gracefully through each tier and never fails silently.

---

## Architecture

```
search_docs → HYBRID_QDRANT (Qdrant semantic + BM25)
           → HYBRID         (FAISS semantic + BM25)   ← if Qdrant Docker offline
           → BM25           (keyword only)             ← if embedding model not loaded
           → RAWFS          (raw filesystem scan)      ← last resort
```

**Active backend:** `SEARCH_BACKEND=qdrant` (Phase 3 — FAISS permanent warm standby)

---

## Folder Structure

```
workspace-knowledge/
├── server.py              ← MCP server entry point (all 11 tools)
├── pyproject.toml         ← Python project definition
├── uv.lock                ← Dependency lock file
├── README.md              ← This file
├── .gitignore             ← Excludes embedding/, .venv/, __pycache__, *.pyc
├── embedding/             ← FAISS index artifacts (gitignored — rebuilt on demand)
└── rag-system/            ← RAG subsystem utilities and runtime state
    ├── build_faiss.py     ← Builds FAISS index from scratch (run manually if index is missing)
    ├── check_rag_status.py ← Diagnostic: prints backend status and index health
    └── rag-sync-state.json ← H-RAG02 hook runtime state (mode, debounce, search_backend)
```

---

## Installation

Dependencies install into the **shared** environment at `core-component-00/mcp-servers/.venv/`,
which this server, `agent-memory`, and `embedder-service` all run from. Do not create a per-server
`.venv/` here — `server.py` no longer looks for one, and `.mcp.json` launches this server directly
with the shared interpreter. See `mcp-servers/CLAUDE.md` § Python Environment for why.

```
# from the repo root — uv picks the CUDA torch index from pyproject.toml automatically, on any OS
uv pip install -e core-component-00/mcp-servers/workspace-knowledge
```

pip equivalent (must pin the local version tag explicitly, or torch stays CPU-only) — the venv
interpreter path differs by OS, everything else is identical:

```bash
# Linux/macOS
core-component-00/mcp-servers/.venv/bin/python -m pip install -e core-component-00/mcp-servers/workspace-knowledge
core-component-00/mcp-servers/.venv/bin/python -m pip install "torch==2.13.0+cu130" --index-url https://download.pytorch.org/whl/cu130
```

```powershell
# Windows
core-component-00\mcp-servers\.venv\Scripts\python.exe -m pip install -e core-component-00\mcp-servers\workspace-knowledge
core-component-00\mcp-servers\.venv\Scripts\python.exe -m pip install "torch==2.13.0+cu130" --index-url https://download.pytorch.org/whl/cu130
```

Requires Docker Desktop (WSL2 backend on Windows) for Qdrant. Start the container before launching:

```
docker start qdrant-workspace
```

First-time setup — the line continuation differs by shell (`\` in bash/zsh, `` ` `` in PowerShell):

```bash
# Linux/macOS
docker run -d --name qdrant-workspace -p 6333:6333 -p 6334:6334 \
  -v qdrant_workspace_knowledge:/qdrant/storage qdrant/qdrant
```

```powershell
# Windows
docker run -d --name qdrant-workspace -p 6333:6333 -p 6334:6334 `
  -v qdrant_workspace_knowledge:/qdrant/storage qdrant/qdrant
```

---

## Configuration

Registered in the project-root `.mcp.json`:

```json
{
  "mcpServers": {
    "workspace-knowledge": {
      "command": "${CLAUDE_PROJECT_DIR:-.}/core-component-00/mcp-servers/workspace-knowledge/.venv/Scripts/python.exe",
      "args": [
        "${CLAUDE_PROJECT_DIR:-.}/core-component-00/mcp-servers/workspace-knowledge/server.py"
      ],
      "env": {
        "WORKSPACE_ROOT": "${CLAUDE_PROJECT_DIR:-.}",
        "SEARCH_BACKEND": "qdrant",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

`command` is a direct, absolute path to this server's own venv interpreter — not a bare command
name resolved via `PATH` (see `core-component-00/mcp-servers/CLAUDE.md` § Python Environment for
why). **A Linux/macOS deployment must manually change this path's `Scripts/python.exe` to
`bin/python`** — this is a documented one-line edit, not automatic; see
`core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.

Tool permissions are granted in `.claude/settings.json` under `permissions.allow`.

### Shared Infrastructure Dependency

Query-time embedding optionally routes through `embedder-service` — a persistent, localhost-only
process shared with `agent-memory` — instead of loading `all-mpnet-base-v2` in-process on every
launch. Full architecture, lifecycle, and config surface:
`.claude/rules/mcp-governance.md` § "Shared Infrastructure — `embedder-service`".

| Env var                    | Default                 | Effect                                                                                                                                 |
| -------------------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `EMBEDDER_SERVICE_ENABLED` | `true`                  | `false` skips the service entirely and always uses this server's own private in-process `all-mpnet-base-v2` copy (`embedding/model/`). |
| `WORKSPACE_QDRANT_URL`     | `http://localhost:6333` | Override the `qdrant-workspace` connection URL.                                                                                        |

If `embedder-service` is down, unreachable, or returns a wrong-dimension vector, this server falls
back to its private in-process model automatically — no manual intervention needed.

---

## Tools

### Search and Retrieval

| Tool                     | Description                                                                                                                       |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `search_docs`            | Hybrid semantic + BM25 search across all indexed `.md` files. Returns ranked results with file path, section, score, and snippet. |
| `retrieve_context`       | Return the full content of a specific workspace file by path.                                                                     |
| `find_related_documents` | Find documents semantically similar to a given seed document.                                                                     |
| `summarize_context`      | Summarize the content of one or more workspace files.                                                                             |
| `agent_knowledge_brief`  | Generate a pre-digested knowledge brief for an agent role across multiple topics.                                                 |

### Index Management

| Tool                 | Description                                                                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `rebuild_index`      | Full FAISS rebuild from corpus. Use for DR recovery or when FAISS index is missing. Blocks until the Qdrant re-seed fully completes.          |
| `rebuild_status`     | Poll live progress (phase, files scanned, chunks embedded) of the most recently started `rebuild_index` call from a separate call.            |
| `upsert_document`    | Re-chunk, re-embed, and upsert a single file into the Qdrant collection. Faster than a full rebuild; use after editing an indexed `.md` file. |
| `list_indexed_files` | List all files currently in the search index.                                                                                                 |

### Governance and Validation

| Tool                         | Description                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `check_adr_precedent`        | Surface prior ADRs before a technology decision. Returns matching ADR documents and whether precedent exists. |
| `validate_pipeline_document` | Validate a pipeline document against workspace conventions.                                                   |
| `list_research_by_topic`     | List research investigations in `telescope/` by topic or keyword.                                             |

---

## Tool Reference

Parameters and example calls for the most-used tools. Every tool response includes a `_meta`
block (`search_tier`, `search_backend`, `qdrant_ready`, `degradation_reason`, `rebuild_available`)
reporting which tier actually served the request — omitted below for brevity.

### `search_docs`

| Parameter | Default  | Notes                                   |
| --------- | -------- | --------------------------------------- |
| `query`   | required | Natural-language or keyword search text |
| `top_k`   | `10`     | Number of ranked results to return      |

```json
// call
{ "query": "how does the RAG index sync hook work", "top_k": 3 }

// response
{
  "query": "how does the RAG index sync hook work",
  "results": [
    {
      "file": "core-component-00/mcp-servers/workspace-knowledge/README.md",
      "section": "H-RAG02 Hook Integration",
      "score": 0.87,
      "snippet": "The PostToolUse hook at .claude/hooks/rag-index-sync.py auto-syncs..."
    }
  ],
  "_meta": { "search_tier": "hybrid_qdrant", "...": "..." }
}
```

### `retrieve_context`

| Parameter   | Default  | Notes                                                     |
| ----------- | -------- | --------------------------------------------------------- |
| `file_path` | required | Path relative to workspace root, e.g. `company/CLAUDE.md` |

Returns `{"file_path", "content", "_meta"}` on success, or `{"error", "_meta"}` if the path
doesn't exist.

### `rebuild_index`

No parameters. Re-scans every workspace markdown file from scratch and re-seeds the Qdrant
collection if Qdrant is initialized. Returns `{"status": "rebuilt", "tier", "_meta"}`. This is
the full DR rebuild path — see [Disaster Recovery](#disaster-recovery) for when to use it versus
`upsert_document`. The call blocks until the Qdrant re-seed fully completes, so the returned
`tier` reflects the true final state rather than a transient mid-rebuild reading — call
`rebuild_status` from a separate call to watch progress while it runs.

### `rebuild_status`

No parameters. Reports live progress of the most recently started `rebuild_index` call:
`{"phase", "files_scanned", "files_total", "chunks_embedded", "chunks_total", "_meta"}`, where
`phase` is one of `idle` / `bm25` / `qdrant_connect` / `faiss` / `qdrant_seed` / `done` / `error`.
Safe to poll repeatedly from a separate call while `rebuild_index` is still running — there is no
push/streaming progress channel, this is a pull-based snapshot.

### `upsert_document`

| Parameter   | Default  | Notes                               |
| ----------- | -------- | ----------------------------------- |
| `file_path` | required | Path of the single file to re-index |

Use after editing one indexed `.md` file — cheaper than a full `rebuild_index`. Returns
`{"status": "upserted", "file", "new_chunk_count", "_meta"}` on success. No-op
(`{"status": "skipped", "reason", "_meta"}`) when `SEARCH_BACKEND=faiss` — use `rebuild_index`
instead in that mode. Returns `{"status": "error", "reason", "_meta"}` if Qdrant isn't
initialized (Docker container not running).

### `check_adr_precedent`

| Parameter    | Default  | Notes                                                |
| ------------ | -------- | ---------------------------------------------------- |
| `technology` | required | Technology/tool name to check for prior ADR coverage |

```json
// call
{ "technology": "Qdrant" }

// response
{
  "technology": "Qdrant",
  "has_precedent": true,
  "adr_count": 2,
  "results": [ /* same shape as search_docs results */ ],
  "_meta": { "...": "..." }
}
```

---

## Indexed Directories (KEY_DIRS)

```
company/
studio/
core-component-00/
telescope/
```

H-RAG02 (`rag-index-sync.py`, invoked via `uv run` — a single cross-platform Python
implementation since the Phase 3 hook-migration cutover) fires after any `.md` write to these
directories and instructs `upsert_document` (Phase 3 — Qdrant mode) to keep the index current
within the session.

---

## H-RAG02 Hook Integration

The `PostToolUse` hook at `.claude/hooks/rag-index-sync.py` (invoked via `uv run
${CLAUDE_PROJECT_DIR}/.claude/hooks/rag-index-sync.py` in `settings.json`) auto-syncs the RAG
index after qualifying `.md` edits. Runtime state is stored in `rag-system/rag-sync-state.json`.

Control the hook with the `/rag-sync` custom command:

| Command                   | Effect                                                 |
| ------------------------- | ------------------------------------------------------ |
| `/rag-sync auto`          | Auto-sync after every qualifying write (10 s debounce) |
| `/rag-sync warn`          | Passive notice only — no automatic sync                |
| `/rag-sync off`           | Silent — no notification or sync                       |
| `/rag-sync status`        | Report current mode, debounce, last sync timestamp     |
| `/rag-sync threshold <N>` | Set debounce window to N seconds                       |

---

## Disaster Recovery

```
# Switch to FAISS warm standby immediately (no rebuild needed if index is on disk)
# Set SEARCH_BACKEND=faiss in .mcp.json env block, then restart Claude Code

# If FAISS index is missing, rebuild from corpus:
# Call rebuild_index via MCP, or run manually:
python rag-system/build_faiss.py

# Check current backend status:
python rag-system/check_rag_status.py
```

Recovery time: < 60 s (FAISS index on disk) or 2–5 min (fresh `rebuild_index`).

---

## Migration Status

| Phase | Description                                  | Status      |
| ----- | -------------------------------------------- | ----------- |
| 0     | H-RAG02 + `/rag-sync` toggle (FAISS only)    | ✅ Complete |
| 1     | Shadow mode — Qdrant writes, FAISS reads     | ✅ Complete |
| 2     | Qdrant primary, FAISS hot standby            | ✅ Complete |
| 3     | Qdrant primary, FAISS permanent warm standby | ✅ Active   |

---

## Ownership

Owned and maintained by **CC-00 Lab**. Primary maintainer: **Sofia Almeida**, Senior Research
Engineer and `retrieval-augmented-generation/` lead, reports to **Dr. Elias Vance** (Lab Director).
See her full profile at `core-component-00/crew/retrieval-augmented-generation/sofia-almeida/agent/profile.md`.
