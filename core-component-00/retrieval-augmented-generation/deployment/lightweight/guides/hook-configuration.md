# Hook Configuration — H-RAG02 Index Sync

> **Core Component 00 — Retrieval Augmented Generation Module**
> **Scope:** Operator guide for the H-RAG02 post-write hook — installation, modes, commands,
> and usage patterns.
> **Audience:** Engineers configuring or operating the RAG index sync hook in an agent runtime.
> **Laboratory Director:** Dr. Elias Vance
> **Last Updated:** 2026-06-27

> **Reference Implementation:** This guide describes one instantiation of the
> [Phase-Adaptive Index Sync Hook pattern](core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md) —
> specifically a post-write hook implemented in PowerShell for a Windows agent runtime using
> Claude Code. The underlying pattern is runtime-agnostic. Engineers deploying on a different
> runtime or OS should consult the pattern document for the portable specification and adapt
> accordingly.

---

## What H-RAG02 Does

The `workspace-knowledge` MCP server builds its search indexes once at startup and never refreshes
them automatically during a running session. When an agent writes or edits a workspace
`.md` file mid-session, all subsequent `search_docs` queries return pre-edit content — a silent
correctness failure with no error signal.

**H-RAG02** (`rag-index-sync.ps1`) is a post-write hook that detects `.md` file writes to the
four indexed directories and instructs the agent to call the appropriate index-update MCP tool:

- **`SEARCH_BACKEND=faiss`** → instructs `rebuild_index` (full FAISS rebuild)
- **`SEARCH_BACKEND=qdrant`** → instructs `upsert_document` (incremental Qdrant upsert)

The active backend is read from the shared state file, not from an environment variable (env vars
are scoped to the MCP server process and are not visible to hook processes).

---

## Hook Identity

**Universal properties** (runtime-agnostic):

| Property        | Value                                                     |
| --------------- | --------------------------------------------------------- |
| **Designation** | H-RAG02                                                   |
| **Concept**     | Post-write hook on document write and edit events         |
| **Trigger**     | File path matches a `.md` file under any KEY_DIR          |
| **KEY_DIRS**    | `company/`, `studio/`, `core-component-00/`, `telescope/` |

**Implementation-specific values** (Claude Code + PowerShell + Windows):

| Property         | Value                                                                    |
| ---------------- | ------------------------------------------------------------------------ |
| **File**         | `.claude/hooks/rag-index-sync.ps1`                                       |
| **Event name**   | `PostToolUse` on `Write` and `Edit` tool calls                           |
| **Registration** | `.claude/settings.json` under `hooks` array for `PostToolUse` events     |
| **State file**   | `core-component-00/mcp-servers/workspace-knowledge/rag-system/rag-sync-state.json` |

---

## Operating Modes

H-RAG02 behavior is governed by the `mode` field in the state file.

| Mode   | Behavior                                                                              |
| ------ | ------------------------------------------------------------------------------------- |
| `auto` | After every qualifying file write (with debounce), instructs the appropriate MCP tool |
| `warn` | Emits a passive notice only; no automatic tool call; agent decides when to update     |
| `off`  | Silent; no notification and no index update instruction                               |

**Default mode: `warn`** — safe for batch-write scenarios. Switch to `auto` for normal single-file
editing sessions.

---

## Operator Control Interface

The five abstract operations defined in the
[pattern document](core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md#operator-control-interface) are
implemented in this deployment as `/rag-sync` custom commands (Claude Code runtime-specific).
All commands read and write the state file directly — no manual JSON editing required.

| Abstract Operation  | Claude Code Invocation    | Effect                                                              |
| ------------------- | ------------------------- | ------------------------------------------------------------------- |
| `set-mode auto`     | `/rag-sync auto`          | Enable automatic index update on qualifying doc writes (debounced)  |
| `set-mode warn`     | `/rag-sync warn`          | Passive notice only; no automatic update (safe default)             |
| `set-mode off`      | `/rag-sync off`           | Silent; no notification, no update                                  |
| `status`            | `/rag-sync status`        | Report current mode, debounce threshold, and last rebuild timestamp |
| `set-threshold <N>` | `/rag-sync threshold <N>` | Set debounce window to N seconds                                    |

State file path (this workspace):
`core-component-00/mcp-servers/workspace-knowledge/rag-system/rag-sync-state.json`

---

## Debounce Behavior

In `auto` mode, the hook compares `last_rebuild_at` (Unix epoch seconds) against the current
time. If fewer than `debounce_seconds` have elapsed since the last update, the trigger is
suppressed. This prevents cascade-rebuilds when an agent writes many files in one turn.

| Backend | Recommended `debounce_seconds` | Rationale                                            |
| ------- | ------------------------------ | ---------------------------------------------------- |
| FAISS   | `30`                           | Full rebuild is slower; suppress intermediate writes |
| Qdrant  | `10`                           | Incremental upsert is fast; more responsive          |

At Phase 3 (Qdrant primary, current state), set the debounce to 10 seconds (`set-threshold 10`;
in this implementation: `/rag-sync threshold 10`). The state file retains this setting across
sessions.

---

## Recommended Usage Patterns

| Scenario                                        | Recommended Mode                                |
| ----------------------------------------------- | ----------------------------------------------- |
| Normal single-file edits                        | `auto` with threshold 10 (Qdrant) or 30 (FAISS) |
| Batch pipeline operations (10+ file writes)     | `warn` before batch; restore `auto` after       |
| Performance-sensitive / exploratory sessions    | `off` + manual tool call at session breakpoints |
| Multi-agent swarm (agents share the MCP server) | `warn` — let each agent decide when to update   |
| Phase transition (switching backends)           | `warn` during transition; `auto` after verified |

---

## When to Call Index Tools Manually

In `warn` mode (or when the debounce suppresses an `auto` trigger), call these tools before
issuing retrieval queries if you have edited indexed documents in the current turn:

| Backend (`search_backend` in state file) | Tool to call                        |
| ---------------------------------------- | ----------------------------------- |
| `"qdrant"`                               | `upsert_document(file_path=<path>)` |
| `"faiss"`                                | `rebuild_index()`                   |

Use `health_check` after any bulk write (>20 files) or document deletion to verify `parity_ok`.
See `core-component-00/retrieval-augmented-generation/evaluation/reference-table.md`
§Orphaned Point Detection for remediation if `orphaned_points > 0`.

---

## State File Location and Schema

**File:** `core-component-00/mcp-servers/workspace-knowledge/rag-system/rag-sync-state.json`

```json
{
  "mode": "warn",
  "debounce_seconds": 30,
  "last_rebuild_at": 0,
  "search_backend": "faiss"
}
```

See `core-component-00/retrieval-augmented-generation/deployment/lightweight/reference/rag-sync-state-schema.md`
for the full field-by-field reference and valid values.

---

## Switching Backends (Phase Transition)

When switching `SEARCH_BACKEND` from `faiss` to `qdrant` (or vice versa), update the
`search_backend` field in the state file to match. H-RAG02 reads this field at runtime — no code
change to the hook is required.

```powershell
# Update state file to Qdrant (set all fields before writing)
$stateFile = "core-component-00\mcp-servers\workspace-knowledge\rag-system\rag-sync-state.json"
$state = Get-Content $stateFile | ConvertFrom-Json
$state.search_backend   = "qdrant"
$state.debounce_seconds = 10        # recalibrate for Qdrant upsert speed
$state | ConvertTo-Json -Compress | Set-Content $stateFile
```

**Important:** `$env:SEARCH_BACKEND` is scoped to the MCP server process only and is not
visible to the hook process. Always use the state file as the shared channel between the server
and the hook.

---

## References

| Resource                       | Location                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| **State File Schema**          | `core-component-00/retrieval-augmented-generation/deployment/lightweight/reference/rag-sync-state-schema.md` |
| **MCP Server Setup**           | `core-component-00/retrieval-augmented-generation/deployment/lightweight/guides/mcp-server-setup.md`         |
| **Index Sync Hook Pattern**    | `core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md`                              |
| **Orphaned Point Remediation** | `core-component-00/retrieval-augmented-generation/evaluation/reference-table.md` §Orphaned Point Detection   |
| **Lightweight RAG Overview**   | `core-component-00/retrieval-augmented-generation/deployment/lightweight-rag-deployment.md`                  |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Contact:** Via workspace agent activation protocol (AGENTS.md § 2.3)
