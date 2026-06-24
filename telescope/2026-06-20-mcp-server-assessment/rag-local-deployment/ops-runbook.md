# workspace-knowledge RAG — Production Operations Runbook

**Document Type:** Operations Runbook (Post-Commissioning)  
**Prepared By:** Core Component 00 Laboratory — Dr. Elias Vance, Laboratory Director  
**Date:** 2026-06-25  
**Status:** Active  
**Target System:** `workspace-knowledge` MCP Server — `agent-global-base`  
**Supersedes:** `telescope/2026-06-24-rag-system-ops/research-report.md`  
**Reference Documents:**

- `ops-manual.md` — Pre-commissioning deployment guide (CPU / planning baseline)
- `../research-report.md` — MCP architecture investigation and Phase 1/2 decisions
- `.claude/mcp-servers/workspace-knowledge/server.py` — Production implementation
- `.claude/mcp-servers/workspace-knowledge/build_faiss.py` — Standalone index builder
- `.claude/mcp-servers/workspace-knowledge/check_rag_status.py` — Tier health check

---

## How This Runbook Differs from `ops-manual.md`

`ops-manual.md` was written as a pre-commissioning planning document targeting CPU-only hardware
(Intel Iris Xe, no CUDA). This runbook documents the **as-built production system** on the actual
deployment machine. Key divergences from the plan:

| Topic                 | `ops-manual.md` (plan)                      | This runbook (production)                              |
| --------------------- | ------------------------------------------- | ------------------------------------------------------ |
| **Hardware**          | Intel Iris Xe — CPU only                    | NVIDIA RTX 4060 Laptop GPU — CUDA 12.4                 |
| **PyTorch wheel**     | CPU-only (`torch+cpu`) — auto-selected      | CUDA wheel required (`torch+cu124`) — manual           |
| **FAISS package**     | `faiss-cpu`                                 | `faiss-cpu` (index built offline, GPU not used)        |
| **Embed device**      | `device="cpu"`                              | `device="cuda:0"`                                      |
| **Model source**      | HuggingFace Hub (auto-download)             | Local `embedding/model/` copy (0.7 s load)             |
| **Index path**        | `.index/` via `RAG_INDEX_DIR`               | `embedding/` (hardcoded in `server.py`)                |
| **Index build path**  | Server builds index on startup (background) | Standalone `build_faiss.py` — server cannot self-build |
| **Background thread** | Not mentioned (defect undiscovered)         | Hangs silently — documented defect + workaround        |
| **Build timing**      | Estimated 30–120 s                          | Measured: ~95 s (local model) / 108.6 s (first)        |

---

## System Overview

The deployed system is a **Phase 2 hybrid RAG** server:

- **BM25** (`rank_bm25.BM25Okapi`) for keyword retrieval
- **FAISS** (`IndexFlatIP`) for semantic retrieval over 768-dim `all-mpnet-base-v2` embeddings
- **RRF fusion** (k=60) combining both rankings
- **Tier degradation**: `HYBRID → BM25 → RAWFS` if components are missing

```
workspace-knowledge/
├── server.py                   ← MCP server (FastMCP, stdio transport)
├── build_faiss.py              ← Standalone FAISS builder (run before server start)
├── check_rag_status.py         ← Tier / health check
├── .venv/                      ← Python virtual environment
└── embedding/                  ← Gitignored runtime artifacts
    ├── model/                  ← all-mpnet-base-v2 local copy (418 MB)
    ├── faiss.index             ← IndexFlatIP over 2,999 chunks (8.8 MB)
    └── index_state.json        ← mtime snapshot for delta detection (147 KB)
```

### Search Tier Reference

| Tier     | Search Mode             | Condition                                  |
| -------- | ----------------------- | ------------------------------------------ |
| `HYBRID` | BM25 + FAISS (RRF k=60) | `embedding/faiss.index` present on disk    |
| `BM25`   | BM25 keyword only       | `faiss.index` absent or FAISS import fails |
| `RAWFS`  | Raw file scan           | `rank_bm25` not installed                  |

Operational target is always `tier: hybrid`. All procedures below maintain or restore that state.

---

## Quick Reference

| Item                | Value                                                                     |
| ------------------- | ------------------------------------------------------------------------- |
| **Machine**         | Intel i9-13900H, NVIDIA RTX 4060 Laptop GPU 8 GB GDDR6, CUDA 12.4, Win 11 |
| **Embed model**     | `all-mpnet-base-v2` (768-dim, 418 MB, local path)                         |
| **Model load time** | 0.7 s (local) vs 14.1 s (HuggingFace cache)                               |
| **Index build**     | ~95 s on RTX 4060 (47 batches × 64 chunks)                                |
| **Torch wheel**     | `torch 2.6.0+cu124` — must not be replaced with CPU wheel                 |
| **Indexed dirs**    | `company/`, `studio/`, `core-component-00/`, `telescope/`                 |
| **Chunks / files**  | 2,999 chunks / 1,273 Markdown files                                       |

All PowerShell commands are run from the **workspace root** unless noted.

---

## Procedure A — First-Time Provisioning (new machine / clean clone)

### Step 1 — Create virtual environment

```powershell
cd .claude\mcp-servers\workspace-knowledge
python -m venv .venv
```

### Step 2 — Install base dependencies

```powershell
.venv\Scripts\pip install fastmcp rank_bm25 sentence-transformers faiss-cpu numpy
```

### Step 3 — Install CUDA-enabled PyTorch (critical — do not skip)

The default pip resolution gives a CPU-only `torch` wheel. Replace it:

```powershell
.venv\Scripts\pip uninstall torch -y
.venv\Scripts\pip install torch --index-url https://download.pytorch.org/whl/cu124
```

Verify CUDA is visible:

```powershell
.venv\Scripts\python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
# Expected: True  NVIDIA GeForce RTX 4060 Laptop GPU
```

> If this returns `False`, the CPU-only wheel is still active. Re-run the `uninstall` + `install`
> above and verify again before proceeding.

### Step 4 — Populate the `embedding/` folder

The `embedding/` folder is gitignored and must be reproduced on each new machine.

**Create directory structure:**

```powershell
cd ..\..\..\   # back to workspace root
New-Item -ItemType Directory -Force .claude\mcp-servers\workspace-knowledge\embedding\model\1_Pooling
```

**Copy model files from HuggingFace cache** (resolves symlinks to real blobs):

```powershell
$snap = "$env:USERPROFILE\.cache\huggingface\hub\models--sentence-transformers--all-mpnet-base-v2\snapshots"
$snap = (Get-ChildItem $snap -Directory | Select-Object -First 1).FullName
$dest = ".claude\mcp-servers\workspace-knowledge\embedding\model"

Get-ChildItem $snap -File | ForEach-Object {
    $t = if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        (Get-Item $_.FullName -Force).Target
    } else { $_.FullName }
    Copy-Item $t "$dest\$($_.Name)" -Force
}
Get-ChildItem "$snap\1_Pooling" -File | ForEach-Object {
    $t = if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        (Get-Item $_.FullName -Force).Target
    } else { $_.FullName }
    Copy-Item $t "$dest\1_Pooling\$($_.Name)" -Force
}
```

**Build the FAISS index** (~95 s on RTX 4060):

```powershell
$env:WORKSPACE_ROOT = (Get-Location).Path
.claude\mcp-servers\workspace-knowledge\.venv\Scripts\python `
  .claude\mcp-servers\workspace-knowledge\build_faiss.py
# Expected: Total: ~95s — faiss.index written (8.8 MB)
```

**Verify output:**

```powershell
Get-Item .claude\mcp-servers\workspace-knowledge\embedding\faiss.index | Select-Object Name, Length
# Expected: faiss.index  ~9,175,xxx bytes
```

### Step 5 — Connect the MCP server

The server is registered in `.mcp.json` at the workspace root. Claude Code starts it automatically
on connection. No manual start command is needed. After connecting, run Procedure D to verify tier.

---

## Procedure B — Normal Start / Restart

```powershell
# 1. Kill any running server processes
Get-Process python -ErrorAction SilentlyContinue |
  Where-Object { $_.MainWindowTitle -eq "" } |
  Stop-Process -Force

# 2. Verify index files are present
Test-Path .claude\mcp-servers\workspace-knowledge\embedding\faiss.index       # must be True
Test-Path .claude\mcp-servers\workspace-knowledge\embedding\index_state.json  # must be True

# 3. Reconnect Claude Code MCP — server starts automatically
```

If either `Test-Path` returns `False`, run Procedure C before reconnecting.

---

## Procedure C — Forced Full Rebuild

Run when significant new workspace content has been added and semantic coverage is stale, or when
`faiss.index` is absent.

```powershell
# 1. Delete existing index
Remove-Item .claude\mcp-servers\workspace-knowledge\embedding\faiss.index `
  -ErrorAction SilentlyContinue
Remove-Item .claude\mcp-servers\workspace-knowledge\embedding\index_state.json `
  -ErrorAction SilentlyContinue

# 2. Rebuild (~95 s on RTX 4060)
$env:WORKSPACE_ROOT = (Get-Location).Path
.claude\mcp-servers\workspace-knowledge\.venv\Scripts\python `
  .claude\mcp-servers\workspace-knowledge\build_faiss.py

# 3. Reconnect MCP
```

> The server's mtime-based delta detection handles small incremental changes automatically on
> restart. The manual delete is only needed for a full corpus rebuild.

---

## Procedure D — Tier Verification

After any start or rebuild, confirm the server is at `tier: hybrid`:

```powershell
.claude\mcp-servers\workspace-knowledge\.venv\Scripts\python `
  .claude\mcp-servers\workspace-knowledge\check_rag_status.py
```

Expected output:

```
tier       : hybrid
chunks     : 2999
files      : 1273
cuda_avail : True
faiss.index: exists
```

If `tier: bm25`, the FAISS index is missing or not loaded. Run Procedure C and reconnect.

---

## Known Defect — Background Thread Hang

**Symptom:** Server starts at `tier: bm25`. `faiss.index` never appears on disk after 5+ minutes.
No error is logged.

**Root cause (suspected):** `model.encode()` inside a `threading.Thread(daemon=True)` interacts
with FastMCP's asyncio stdio event loop. The main thread holds the GIL during `mcp.run()` I/O
processing, starving the encode loop. No exception surfaces because the thread is a daemon.

**Canonical workaround:** Build the FAISS index via the standalone `build_faiss.py` script before
starting the server. Once `faiss.index` is on disk the server loads it at startup without entering
the broken build path (Procedure C above).

**Candidate fix (not yet implemented):** Replace `threading.Thread` with
`concurrent.futures.ProcessPoolExecutor` to bypass GIL contention, or refactor into
`asyncio.run_in_executor`.

---

## Configuration Reference

| Item              | Value                                                                             |
| ----------------- | --------------------------------------------------------------------------------- |
| Server script     | `.claude/mcp-servers/workspace-knowledge/server.py`                               |
| venv              | `.claude/mcp-servers/workspace-knowledge/.venv/`                                  |
| Embedding folder  | `.claude/mcp-servers/workspace-knowledge/embedding/` (gitignored — entire folder) |
| Model files       | `embedding/model/` — `all-mpnet-base-v2` (418 MB, local copy, no HF cache needed) |
| FAISS index       | `embedding/faiss.index` (8.8 MB)                                                  |
| Index state       | `embedding/index_state.json` (147 KB)                                             |
| Embedding device  | `cuda:0` — NVIDIA GeForce RTX 4060 Laptop GPU (8 GB GDDR6)                        |
| Model load time   | **0.7 s** (local path) vs 14.1 s (HuggingFace cache)                              |
| Torch wheel       | `torch 2.6.0+cu124` (CUDA 12.4) — must not be replaced with a CPU-only wheel      |
| MCP registration  | `.mcp.json` → `workspace-knowledge`                                               |
| Governance record | `.claude/rules/mcp-governance.md`                                                 |

### Build Timing (RTX 4060 Laptop GPU — Measured)

| Phase                           | First Run   | Subsequent |
| ------------------------------- | ----------- | ---------- |
| Model load (HuggingFace cache)  | 14.1 s      | —          |
| Model load (local path)         | **0.7 s**   | **0.7 s**  |
| Encode (47 batches × 64 chunks) | 93.6 s      | ~94 s      |
| Normalize + FAISS add + write   | < 1 s       | < 1 s      |
| **Total (first run)**           | **108.6 s** |            |
| **Total (local model)**         |             | **~95 s**  |

---

**Document version:** 1.0 — 2026-06-25  
**Maintained By:** Core Component 00 Laboratory  
**Authority:** AGENTS.md § 6. Core Component 00
