# RAG Sync State File — Schema Reference

> **Core Component 00 — Retrieval Augmented Generation Module**
> **Scope:** Field-by-field reference for the H-RAG02 shared state file contract.
> **Audience:** Engineers reading, editing, or debugging the RAG index sync state.
> **Laboratory Director:** Dr. Elias Vance
> **Last Updated:** 2026-06-27

> **Reference Implementation:** This document describes the state file schema for the
> [Phase-Adaptive Index Sync Hook pattern](core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md) as deployed
> in this workspace (Claude Code + PowerShell + Windows). The schema itself is universal; the
> file path and operator commands listed below are implementation-specific.

---

## File Location

```
core-component-00/mcp-servers/workspace-knowledge/rag-system/rag-sync-state.json
```

This file is the **shared inter-process communication channel** between the `workspace-knowledge`
MCP server process and the H-RAG02 post-write hook process. It must be readable and writable by
both processes. Do not use environment variables as a substitute — they are scoped to the process
that sets them and are not visible across process boundaries.

---

## Canonical Schema

```json
{
  "mode": "warn",
  "debounce_seconds": 30,
  "last_rebuild_at": 0,
  "search_backend": "faiss"
}
```

This is the initial state. Create this file at MCP server setup time if it does not exist.

---

## Field Reference

### `mode`

Controls H-RAG02 behavior after a qualifying `.md` file write.

| Value    | Behavior                                                                            |
| -------- | ----------------------------------------------------------------------------------- |
| `"auto"` | After debounce check, instructs the appropriate index-update MCP tool automatically |
| `"warn"` | Emits a passive notice only; no automatic tool call (**default**)                   |
| `"off"`  | Silent; no notification and no index update instruction                             |

**Default:** `"warn"` — safe for batch-write sessions. Use `set-mode auto` to enable automatic
updates for normal editing sessions (this implementation: `/rag-sync auto`).

**How to update:** `set-mode auto` | `set-mode warn` | `set-mode off`
_(This implementation: `/rag-sync auto` | `/rag-sync warn` | `/rag-sync off`)_

---

### `debounce_seconds`

The minimum elapsed time (in seconds) between H-RAG02 `auto`-mode index update instructions.
If a qualifying file write fires the hook within this window of the last update, the trigger is
suppressed. Prevents cascade updates during batch-write operations.

| Value | When to Use                                                  |
| ----- | ------------------------------------------------------------ |
| `30`  | FAISS backend (full rebuild is slower) — **initial default** |
| `10`  | Qdrant backend (incremental upsert is faster)                |

**How to update:** `set-threshold <N>` (e.g., `set-threshold 10`; this implementation:
`/rag-sync threshold <N>`)

At Phase 3 (Qdrant primary, current state of this workspace), the recommended value is `10`.

---

### `last_rebuild_at`

Unix epoch timestamp (integer seconds) of the last index update instruction emitted by H-RAG02
in `auto` mode. Updated by the hook itself each time it fires. Used for debounce comparison.

| Value | Meaning                                           |
| ----- | ------------------------------------------------- |
| `0`   | No update has been emitted yet in this state file |
| `N`   | Unix epoch seconds of the last emitted update     |

**Do not edit manually.** The hook maintains this field. Read it via the `status` operation
(this implementation: `/rag-sync status`) for a human-readable datetime of the last update.

---

### `search_backend`

Governs which MCP tool H-RAG02 instructs when in `auto` mode. Must match the
`SEARCH_BACKEND` environment variable set in `.mcp.json` for the `workspace-knowledge` server.

| Value      | H-RAG02 `auto` mode instructs | Current state                              |
| ---------- | ----------------------------- | ------------------------------------------ |
| `"faiss"`  | `rebuild_index`               | FAISS + BM25 primary                       |
| `"qdrant"` | `upsert_document`             | Qdrant + BM25 primary ← **Phase 3 active** |

**Critical:** This field must be updated when switching backends. H-RAG02 reads it at runtime —
no code change to the hook script is required at phase transitions.

**How to update:** Edit the JSON file directly, or use the PowerShell snippet in
`core-component-00/retrieval-augmented-generation/deployment/lightweight/guides/hook-configuration.md`
§Switching Backends.

**Do not use `$env:SEARCH_BACKEND`** to communicate the backend to the hook — environment
variables set by the MCP server process are not inherited by unrelated hook processes. The state
file is the only correct shared channel.

---

## Full Field Summary

| Field              | Type      | Default   | Editable By               | Purpose                                               |
| ------------------ | --------- | --------- | ------------------------- | ----------------------------------------------------- |
| `mode`             | `string`  | `"warn"`  | `set-mode` operation      | Controls hook behavior (auto / warn / off)            |
| `debounce_seconds` | `integer` | `30`      | `set-threshold` operation | Minimum seconds between auto-mode updates             |
| `last_rebuild_at`  | `integer` | `0`       | Hook (automatic)          | Unix epoch of last emitted update                     |
| `search_backend`   | `string`  | `"faiss"` | Manual / phase transition | Determines which index-update tool the hook instructs |

---

## Phase 3 Recommended State

Current workspace is at Phase 3 (Qdrant primary, FAISS on permanent standby). Recommended
state file for normal editing sessions:

```json
{
  "mode": "auto",
  "debounce_seconds": 10,
  "last_rebuild_at": 0,
  "search_backend": "qdrant"
}
```

Apply via the configuration manager (abstract operations):

```
set-mode auto
set-threshold 10
```

In this implementation (Claude Code): `/rag-sync auto` then `/rag-sync threshold 10`.

(The `search_backend` field must be set manually or via the PowerShell snippet in
`core-component-00/retrieval-augmented-generation/deployment/lightweight/guides/hook-configuration.md`
§Switching Backends if it has not already been updated to `"qdrant"`.)

---

## Validation

If H-RAG02 behaves unexpectedly, verify the state file with:

```powershell
Get-Content "core-component-00\mcp-servers\workspace-knowledge\rag-system\rag-sync-state.json" | ConvertFrom-Json
```

Or use the `status` operation from the configuration manager (this implementation:
`/rag-sync status`).

The hook falls back to `mode: "warn"` and `backend: "faiss"` if the state file is absent or
malformed — a safe degraded state that does not cause incorrect behavior.

---

## References

| Resource                     | Location                                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Hook Configuration Guide** | `core-component-00/retrieval-augmented-generation/deployment/lightweight/guides/hook-configuration.md` |
| **Index Sync Hook Pattern**  | `core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md`                        |
| **MCP Server Setup**         | `core-component-00/retrieval-augmented-generation/deployment/lightweight/guides/mcp-server-setup.md`   |
| **Lightweight RAG Overview** | `core-component-00/retrieval-augmented-generation/deployment/lightweight-rag-deployment.md`            |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Contact:** Via workspace agent activation protocol (AGENTS.md § 2.3)
