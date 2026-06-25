# RAG Hook System Design

**Document Type:** Migration Planning Deliverable
**Investigation:** `2026-06-25-qdrant-migration-plan`
**Author:** Dr. Elias Vance — CC-00 Laboratory Director
**Date:** 2026-06-25
**Status:** Approved

---

## 1. Purpose

The `workspace-knowledge` MCP server's search indexes are built once at server startup and are
never automatically refreshed during a running session. When Claude Code agents edit or create
workspace documentation mid-session, all subsequent `search_docs` queries return pre-edit content
— a silent correctness failure with no error signal.

**H-RAG02** (`rag-index-sync.ps1`) is a `PostToolUse` hook that detects `.md` file writes to the
four indexed directories and instructs Claude to call the appropriate index-update MCP tool. It is
designed to work across all four migration phases, adapting the update path from FAISS full-rebuild
(Phase 0–1) to Qdrant incremental upsert (Phase 2–3).

---

## 2. H-RAG02 Hook Specification

### 2.1 Hook identity

| Property              | Value                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------- |
| **File**              | `.claude/hooks/rag-index-sync.ps1`                                                      |
| **Designation**       | H-RAG02                                                                                 |
| **Event**             | `PostToolUse` on `Write` and `Edit` tool calls                                          |
| **Trigger condition** | The tool's `file_path` matches a `.md` file under any of the four KEY_DIRS              |
| **KEY_DIRS**          | `company/`, `studio/`, `core-component-00/`, `telescope/`                               |
| **Registration**      | `.claude/settings.json` under the `hooks` array for `PostToolUse` events                |
| **State file**        | `.claude/hooks/rag-sync-state.json`                                                     |
| **No new MCP tool**   | H-RAG02 calls the existing `rebuild_index` (Phase 0–1) or `upsert_document` (Phase 2–3) |

### 2.2 Operating modes

H-RAG02 behavior is governed by `.claude/hooks/rag-sync-state.json`. Three modes:

| Mode   | Behavior                                                                                    |
| ------ | ------------------------------------------------------------------------------------------- |
| `auto` | Trigger the appropriate index-update call after every qualifying file write (with debounce) |
| `warn` | Emit a passive notice only; agent must call the update tool manually                        |
| `off`  | Silent; no notification and no rebuild                                                      |

**Default mode:** `warn` — safe for batch-write scenarios and large pipeline operations.

### 2.3 State file schema

File path: `.claude/hooks/rag-sync-state.json`

```json
{
  "mode": "warn",
  "debounce_seconds": 30,
  "last_rebuild_at": 0
}
```

Create this file at Phase 0 implementation with the above initial state.

### 2.4 Debounce behavior

In `auto` mode, `last_rebuild_at` (Unix epoch seconds) is compared against the current time. If
fewer than `debounce_seconds` have elapsed since the last rebuild, the trigger is suppressed.
This prevents cascade-rebuilds in batch-write scenarios (e.g., a pipeline agent writing 20
documents in one turn).

| Migration phase | Recommended `debounce_seconds` | Rationale                                    |
| --------------- | ------------------------------ | -------------------------------------------- |
| Phase 0–1       | `30`                           | Full FAISS rebuild is slower                 |
| Phase 2–3       | `10`                           | `upsert_document` is faster; more responsive |

Use `/rag-sync threshold 10` at Phase 2 entry to recalibrate without editing the state file.

---

## 3. Phase-Adaptive Index Update Path

H-RAG02 instructs Claude to call a different MCP tool depending on the active migration phase.
The `SEARCH_BACKEND` environment variable governs which path is active:

| Phase                 | `SEARCH_BACKEND` | H-RAG02 `auto` mode action                                                             | Debounce |
| --------------------- | ---------------- | -------------------------------------------------------------------------------------- | -------- |
| 0 (current)           | `faiss`          | Instruct `rebuild_index` (full FAISS rebuild)                                          | 30 s     |
| 1 (shadow)            | `faiss`          | Instruct `rebuild_index` (FAISS primary) + shadow `upsert_document` (Qdrant, if ready) | 30 s     |
| 2 (Qdrant primary)    | `qdrant`         | Instruct `upsert_document` (Qdrant incremental) + `rebuild_index` (FAISS DR standby)   | 10 s     |
| 3 (permanent standby) | `qdrant`         | Instruct `upsert_document` (Qdrant only); FAISS self-heals via mtime on startup        | 10 s     |

The hook detects the active phase via `SEARCH_BACKEND`: `faiss` → FAISS path; `qdrant` → Qdrant
path. No code change to the hook is required at phase transition — only the env var changes.

---

## 4. PowerShell Implementation

**File:** `.claude/hooks/rag-index-sync.ps1`

```powershell
#!/usr/bin/env pwsh
# H-RAG02: PostToolUse — RAG Index Sync on Doc Write (toggle-aware, phase-adaptive)
# Fires after Write or Edit tools modify .md files in KEY_DIRS.
# Behavior is governed by .claude/hooks/rag-sync-state.json (mode: auto|warn|off).
# Phase adaptation: reads SEARCH_BACKEND env var to determine rebuild vs upsert path.

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$toolName = $data.tool_name
if ($toolName -notin @("Write", "Edit")) { exit 0 }

$filePath = $data.tool_input.file_path
if (-not $filePath) { exit 0 }

# Normalize to forward slashes for matching
$normalizedPath = $filePath -replace '\\', '/'

$keyDirs = @("company/", "studio/", "core-component-00/", "telescope/")
$inKeyDir = $false
foreach ($dir in $keyDirs) {
    if ($normalizedPath -match "(^|/)$($dir)") {
        $inKeyDir = $true
        break
    }
}

if (-not $inKeyDir) { exit 0 }
if ($normalizedPath -notmatch '\.md$') { exit 0 }

# --- Read toggle state (defaults to warn if state file absent) ---
$stateFile = Join-Path $PSScriptRoot "rag-sync-state.json"
$mode            = "warn"
$debounceSeconds = 30
$lastRebuildAt   = 0

if (Test-Path $stateFile) {
    try {
        $state           = Get-Content $stateFile -Raw | ConvertFrom-Json
        $mode            = if ($state.mode)             { $state.mode }             else { "warn" }
        $debounceSeconds = if ($state.debounce_seconds) { $state.debounce_seconds } else { 30 }
        $lastRebuildAt   = if ($state.last_rebuild_at)  { $state.last_rebuild_at }  else { 0 }
    } catch {
        $mode = "warn"
    }
}

# --- Detect active migration phase via SEARCH_BACKEND ---
$backend = if ($env:SEARCH_BACKEND) { $env:SEARCH_BACKEND } else { "faiss" }
$updateTool = if ($backend -eq "qdrant") { "upsert_document" } else { "rebuild_index" }

# --- Mode: off — exit silently ---
if ($mode -eq "off") { exit 0 }

# --- Mode: warn — passive notice only, no rebuild ---
if ($mode -eq "warn") {
    $additionalContext = @"
[RAG INDEX SYNC — H-RAG02 | MODE: WARN]
Indexed workspace document modified: $filePath

The workspace-knowledge index is now stale. Auto-sync is in WARN mode.
If you need up-to-date retrieval results this turn, call $updateTool via the
workspace-knowledge MCP before issuing search_docs, find_related_documents, or
summarize_context queries.
To enable automatic rebuilds: /rag-sync auto
"@
    $output = [ordered]@{
        hookSpecificOutput = [ordered]@{
            hookEventName     = "PostToolUse"
            additionalContext = $additionalContext
        }
    } | ConvertTo-Json -Depth 5 -Compress
    Write-Output $output
    exit 0
}

# --- Mode: auto — debounce check, then emit rebuild instruction ---
$now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
if (($now - $lastRebuildAt) -lt $debounceSeconds) { exit 0 }  # within debounce window — suppress

# Update last_rebuild_at in state file
try {
    $newState = [ordered]@{
        mode             = $mode
        debounce_seconds = $debounceSeconds
        last_rebuild_at  = $now
    }
    $newState | ConvertTo-Json -Compress | Set-Content $stateFile
} catch { }

$additionalContext = @"
[RAG INDEX SYNC — H-RAG02 | MODE: AUTO]
Indexed workspace document modified: $filePath

Before issuing any search_docs, find_related_documents, summarize_context, or agent_knowledge_brief
query this turn, call $updateTool via the workspace-knowledge MCP to ensure retrieval results
reflect your changes.
To switch to passive mode: /rag-sync warn    To disable: /rag-sync off
Reference: telescope/2026-06-25-qdrant-migration-plan/plans/05-hook-design.md
"@

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "PostToolUse"
        additionalContext = $additionalContext
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
```

---

## 5. `/rag-sync` Custom Command

### 5.1 Command file

**File:** `.claude/commands/rag-sync.md`

This command provides operator control over H-RAG02's sync behavior without touching
`.claude/settings.json`. It reads and writes `.claude/hooks/rag-sync-state.json`.

### 5.2 Usage reference

| Command                   | Effect                                                              |
| ------------------------- | ------------------------------------------------------------------- |
| `/rag-sync auto`          | Enable automatic rebuild on qualifying doc writes (with debounce)   |
| `/rag-sync warn`          | Passive notice only; no automatic rebuild (safe default)            |
| `/rag-sync off`           | Silent; no notification, no rebuild                                 |
| `/rag-sync status`        | Report current mode, debounce threshold, and last rebuild timestamp |
| `/rag-sync threshold <N>` | Set debounce window to N seconds (default: 30)                      |

### 5.3 Command file contents

```markdown
Read the file `.claude/hooks/rag-sync-state.json`. If it does not exist, treat the
current state as `{"mode": "warn", "debounce_seconds": 30, "last_rebuild_at": 0}`.

Based on the argument provided after `/rag-sync`:

- `auto` → set mode to `"auto"`, write the updated state file, confirm:
  _"RAG sync set to AUTO — index will rebuild automatically after qualifying doc writes
  (debounce: \<N\>s)."_
- `warn` → set mode to `"warn"`, write the updated state file, confirm:
  _"RAG sync set to WARN — you will be notified of stale index but no automatic rebuild."_
- `off` → set mode to `"off"`, write the updated state file, confirm:
  _"RAG sync DISABLED — no notifications or automatic rebuilds."_
- `status` → read the state file, report: current mode, debounce threshold in seconds,
  last rebuild timestamp formatted as a human-readable datetime.
- `threshold <N>` → set `debounce_seconds` to N, write the updated state file, confirm:
  _"Debounce threshold set to \<N\> seconds."_

After writing, display the full new state as a JSON block for confirmation.
```

### 5.4 Recommended usage patterns

| Scenario                                        | Recommended mode                              |
| ----------------------------------------------- | --------------------------------------------- |
| Normal single-file edits                        | `auto` (default debounce 30 s)                |
| Batch pipeline operations (10+ file writes)     | `warn` before batch; restore after            |
| Performance-sensitive / exploratory sessions    | `off` + manual tool call at breakpoints       |
| Multi-agent swarm (agents share the MCP server) | `warn` — let each agent decide when to update |
| Phase 2 entry onwards (Qdrant primary)          | `auto` with `/rag-sync threshold 10`          |

---

## 6. `rebuild_index` MCP Governance Gate Assessment

H-RAG02 (Phase 0–1) calls the existing `rebuild_index` tool. No new MCP tool surface is
introduced at Phase 0. `upsert_document` (Phase 2–3) is governed by the assessment in
`01-migration-strategy.md` §4.

| Gate             | Assessment                                                                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Capability**   | ✅ Pass — re-encoding all markdown chunks into a FAISS vector index cannot be replicated by `Grep`, `Read`, or `Glob`                            |
| **Completeness** | ✅ Pass — returns `{"status": "rebuilt", "tier": "<actual-tier>", "_meta": {...}}` — real post-rebuild state, not a template                     |
| **Governance**   | ✅ Pass — writes only to `embedding/faiss.index` and `embedding/index_state.json`; does not touch any `pipeline.md`, ADR, or governance document |

---

## 7. Implementation Checklist

Complete in order before Phase 1 entry:

- [ ] Create `.claude/hooks/rag-sync-state.json` with initial state `{"mode": "warn", "debounce_seconds": 30, "last_rebuild_at": 0}`
- [ ] Implement `rag-index-sync.ps1` (H-RAG02) in `.claude/hooks/` per §4 above
- [ ] Register H-RAG02 in `.claude/settings.json` under `hooks` array for `PostToolUse` events
- [ ] Implement `.claude/commands/rag-sync.md` per §5.3 above
- [ ] Verify hook fires on a test `.md` write in `telescope/` — confirm `[H-RAG02 | MODE: WARN]` block appears
- [ ] Verify `/rag-sync auto` switches mode correctly
- [ ] Verify `/rag-sync status` reports current state
- [ ] At Phase 2 entry: run `/rag-sync threshold 10` to recalibrate debounce
- [ ] At Phase 2 entry: verify hook correctly emits `upsert_document` instruction (not `rebuild_index`) when `SEARCH_BACKEND=qdrant`

---

**Cross-reference:** `01-migration-strategy.md` §4 — H-RAG02 hook adaptation table per phase
**Cross-reference:** `04-monitoring-guide.md` §5.3 — Debounce recalibration after Phase 1 benchmarks
