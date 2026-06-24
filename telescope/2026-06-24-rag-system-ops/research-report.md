# Research Report — workspace-knowledge RAG System: Operations & Initialization Runbook

---

## Metadata

| Field                | Value                                                    |
| -------------------- | -------------------------------------------------------- |
| **Investigation ID** | `2026-06-24-rag-system-ops`                              |
| **Date Started**     | 2026-06-24                                               |
| **Date Completed**   | 2026-06-24                                               |
| **Status**           | Complete                                                 |
| **Investigator**     | Dr. Elias Vance — Laboratory Director, Core Component 00 |
| **Laboratory**       | Core Component 00                                        |
| **Module(s)**        | Retrieval-Augmented Generation (Layer 4)                 |
| **Priority**         | High                                                     |
| **Requestor**        | CEO                                                      |

---

## Executive Summary

This runbook documents the complete operational lifecycle of the `workspace-knowledge` MCP RAG
server — from cold-start provisioning through normal operation and scheduled maintenance. The Phase
2 hybrid RAG system (BM25 + FAISS semantic, `all-mpnet-base-v2` on CUDA) was successfully
commissioned on 2026-06-24 against 2,999 chunks across 1,273 workspace Markdown files. A known
threading issue prevents the server's internal background thread from completing the initial FAISS
build; this runbook documents the canonical workaround and all operational procedures required to
keep the system at `tier: hybrid`.

---

## Investigation Scope

### What Was Investigated

Operational procedures for the `workspace-knowledge` MCP server covering: first-time environment
provisioning, FAISS index build (initial and incremental), server lifecycle management, tier
verification, and maintenance procedures following significant document changes.

### Why This Investigation Was Needed

The Phase 2 FAISS initialization sequence has four non-obvious failure modes — any one of which
silently degrades the server from `tier: hybrid` to `tier: bm25` with no visible error. Without
documented procedures, reproducing a working HYBRID-tier deployment requires reconstructing the
entire commissioning history from session logs. This runbook eliminates that dependency.

### Out of Scope

- BM25-only (Phase 1) operation — superseded by Phase 2
- Remote or containerized deployment (local Windows 11 only)
- Model fine-tuning or custom embeddings
- Multi-user or concurrent-access scenarios

---

## Research Questions

1. What are the exact steps to provision the server environment from scratch on a fresh machine?
2. Why does the server's internal background thread fail to build the FAISS index, and what is the
   canonical workaround?
3. What are the actual timing characteristics of the FAISS build on this hardware?
4. How does an operator verify that the server has reached `tier: hybrid`?
5. Under what conditions must the FAISS index be rebuilt, and how?

---

## Methodology

Operational data collected during the Phase 2 commissioning session on 2026-06-24. All timings
measured on the production machine (Intel i9-13900H, NVIDIA RTX 4060 Laptop GPU 8 GB GDDR6, CUDA
12.4, Windows 11). Build script (`build_faiss.py`) run directly against the live venv to produce
authoritative measurements.

---

## Findings

### Finding 1: Default pip install gives CPU-only PyTorch

When `sentence-transformers` is installed via `pip install sentence-transformers`, pip resolves
PyTorch to the CPU-only wheel (`torch 2.x+cpu`). On this machine `torch.cuda.is_available()`
returns `False` despite the RTX 4060 being present. This causes all embedding work to run on CPU,
roughly 10–30× slower than GPU.

**Evidence:**

- `torch 2.12.1+cpu` installed by default — `cuda.is_available()` = False
- After CUDA wheel install: `torch 2.6.0+cu124` — `cuda.is_available()` = True, device = `cuda:0`

**Implications:**

- The CUDA torch wheel must be installed explicitly before the first index build. See §
  Provisioning below.

---

### Finding 2: Background thread silently hangs during server-internal FAISS build

The MCP server launches FAISS init in a `threading.Thread(daemon=True)`. In production, this
thread never completes — `faiss.index` is never written after 300+ seconds. No exception is
raised; no stderr output appears. The root cause is a suspected interaction between the
`sentence-transformers` encode call and FastMCP's asyncio stdio event loop holding the GIL. The
main thread is blocked on `mcp.run()` reading stdin.

**Evidence:**

- Server PID alive for 300s; `faiss.index` absent from disk after full timeout
- Direct invocation of identical encode + write pipeline (same process, no asyncio) completes in
  108.6 s and writes `faiss.index` successfully

**Implications:**

- The FAISS index **must be built via the standalone `build_faiss.py` script**, not by waiting for
  the server's background thread. Once `faiss.index` is present on disk, the server loads it
  instantly on startup and correctly upgrades to `tier: hybrid`.

---

### Finding 3: Measured performance on RTX 4060 Laptop GPU

Full first-run build from 2,999 chunks on the production machine (initial commissioning, model
loaded from HuggingFace cache):

| Phase                           | Duration    |
| ------------------------------- | ----------- |
| Model load (HuggingFace cache)  | 14.1 s      |
| Encode (47 batches × 64 chunks) | 93.6 s      |
| Normalize + FAISS add + write   | < 1 s       |
| **Total**                       | **108.6 s** |

After relocating the model to `embedding/model/` (local path load):

| Phase                           | Duration  |
| ------------------------------- | --------- |
| Model load (local path)         | **0.7 s** |
| Encode (47 batches × 64 chunks) | ~94 s     |
| **Total**                       | **~95 s** |

Output artifacts:

| File                         | Size     |
| ---------------------------- | -------- |
| `embedding/faiss.index`      | 8.8 MB   |
| `embedding/index_state.json` | 147.1 KB |

**Implications:**

- Plan for ~2 minutes when triggering a full rebuild. Incremental rebuilds (delta detected via
  mtime) are proportionally faster. Local model path eliminates HuggingFace network/cache overhead.

---

### Finding 4: Tier degradation hierarchy

The server degrades gracefully through three tiers. Only `HYBRID` delivers semantic search.

| Tier     | Search Mode             | Condition                               |
| -------- | ----------------------- | --------------------------------------- |
| `HYBRID` | BM25 + FAISS (RRF k=60) | `faiss.index` on disk + imports present |
| `BM25`   | BM25 keyword only       | `faiss.index` absent or imports fail    |
| `RAWFS`  | File scan               | `rank_bm25` not installed               |

---

## Analysis

### Interpretation of Findings

The two actionable issues (CPU torch wheel, background thread hang) are independent but compound:
even with the correct CUDA wheel, the server never self-builds the index due to the threading
issue. The correct operating model is therefore:

1. Provision the venv with the CUDA torch wheel once (permanent).
2. Build the FAISS index via the standalone script once (or after major doc changes).
3. Start the server — it loads the cached index in seconds and reaches `tier: hybrid` immediately.

### Risks and Limitations

- The background thread hang is a known defect — not yet root-caused at the asyncio / GIL
  boundary. Do not rely on the server to self-build its index.
- The entire `embedding/` folder is excluded from git (`.gitignore`) — model files, FAISS index,
  and state file must all be reproduced on any new machine or after a clean clone (see Procedure A,
  Steps 3–4).
- The RTX 4060 Laptop GPU runs at reduced TDP in some power plans. Ensure the machine is plugged
  in during the build step for consistent ~95 s timing.

---

## Recommendations

### Primary Recommendation

**Always build the FAISS index via the standalone script before starting the MCP server.** Follow
the Provisioning and Operations procedures below exactly.

### Secondary Recommendations

1. **Investigate the background thread hang** — profile the interaction between `model.encode()`
   and FastMCP's asyncio event loop. Candidate fix: move encode to a `ProcessPoolExecutor` to
   bypass GIL contention.
2. **Add a `/rebuild` MCP tool trigger** — allow Claude Code to request a rebuild without manual
   PowerShell steps, once the threading issue is resolved.
3. **Document in `mcp-governance.md`** — add a note that `faiss.index` is a build artifact, not a
   server-managed resource, so governance reviewers understand the two-step start sequence.

---

## Operations Procedures

### A. First-Time Provisioning (new machine / clean clone)

Run all commands from the workspace root in PowerShell.

**Step 1 — Create venv**

```powershell
cd .claude\mcp-servers\workspace-knowledge
python -m venv .venv
```

**Step 2 — Install base dependencies**

```powershell
.venv\Scripts\pip install fastmcp rank_bm25 sentence-transformers faiss-cpu numpy
```

**Step 3 — Install CUDA-enabled PyTorch (CRITICAL — do not skip)**

The default torch from step 2 is CPU-only. Replace it:

```powershell
.venv\Scripts\pip uninstall torch -y
.venv\Scripts\pip install torch --index-url https://download.pytorch.org/whl/cu124
```

Verify:

```powershell
.venv\Scripts\python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
# Expected: True  NVIDIA GeForce RTX 4060 Laptop GPU
```

**Step 4 — Populate `embedding/` folder**

The entire `embedding/` folder is gitignored and must be created on each new machine.

```powershell
cd ..\..\..\  # back to workspace root
New-Item -ItemType Directory -Force .claude\mcp-servers\workspace-knowledge\embedding\model\1_Pooling
```

Copy model files from HuggingFace cache (resolves symlinks to real blobs):

```powershell
$snap = "$env:USERPROFILE\.cache\huggingface\hub\models--sentence-transformers--all-mpnet-base-v2\snapshots"
$snap = (Get-ChildItem $snap -Directory | Select-Object -First 1).FullName
$dest = ".claude\mcp-servers\workspace-knowledge\embedding\model"
Get-ChildItem $snap -File | ForEach-Object {
    $t = if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) { (Get-Item $_.FullName -Force).Target } else { $_.FullName }
    Copy-Item $t "$dest\$($_.Name)" -Force
}
Get-ChildItem "$snap\1_Pooling" -File | ForEach-Object {
    $t = if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) { (Get-Item $_.FullName -Force).Target } else { $_.FullName }
    Copy-Item $t "$dest\1_Pooling\$($_.Name)" -Force
}
```

Then build the FAISS index:

```powershell
$env:WORKSPACE_ROOT = (Get-Location).Path
.claude\mcp-servers\workspace-knowledge\.venv\Scripts\python `
  "C:\Users\ASUS\.claude\jobs\7d1596c6\tmp\build_faiss.py"
# Expected output: Total: ~95s — faiss.index written (8.8 MB)
```

Verify output:

```powershell
Get-Item .claude\mcp-servers\workspace-knowledge\embedding\faiss.index | Select-Object Name, Length
# Expected: faiss.index, ~9,175,xxx bytes
```

**Step 5 — Register and start the MCP server**

The server is registered in `.mcp.json`. Claude Code starts it automatically on connection. No
manual start command is needed. Verify tier after connection:

```powershell
# Run the status check script
.claude\mcp-servers\workspace-knowledge\.venv\Scripts\python `
  "C:\Users\ASUS\.claude\jobs\7d1596c6\tmp\check_rag_status.py"
# Expected: tier: hybrid, chunks: 2999
```

---

### B. Normal Start / Restart

```powershell
# 1. Kill any running server processes
Get-Process python -ErrorAction SilentlyContinue |
  Where-Object { $_.MainWindowTitle -eq "" } |
  Stop-Process -Force

# 2. Verify index files are present
Test-Path .claude\mcp-servers\workspace-knowledge\embedding\faiss.index       # must be True
Test-Path .claude\mcp-servers\workspace-knowledge\embedding\index_state.json  # must be True

# 3. Reconnect Claude Code MCP — server starts automatically
# No manual start needed.
```

---

### C. Forced Full Rebuild (after large document additions)

Trigger a rebuild when significant new workspace content has been added and semantic search
coverage is stale.

```powershell
# 1. Delete existing index to force rebuild
Remove-Item .claude\mcp-servers\workspace-knowledge\embedding\faiss.index -ErrorAction SilentlyContinue
Remove-Item .claude\mcp-servers\workspace-knowledge\embedding\index_state.json -ErrorAction SilentlyContinue

# 2. Run standalone build (~109s on RTX 4060)
$env:WORKSPACE_ROOT = (Get-Location).Path
.claude\mcp-servers\workspace-knowledge\.venv\Scripts\python `
  "C:\Users\ASUS\.claude\jobs\7d1596c6\tmp\build_faiss.py"

# 3. Reconnect MCP
```

The server's mtime-based delta detection also handles incremental updates automatically on restart
when only a few files have changed — only full rebuilds require the manual delete step.

---

### D. Tier Verification

After any start or rebuild, confirm the server has reached `tier: hybrid`:

```powershell
.claude\mcp-servers\workspace-knowledge\.venv\Scripts\python `
  "C:\Users\ASUS\.claude\jobs\7d1596c6\tmp\check_rag_status.py"
```

Expected output:

```
tier       : hybrid
chunks     : 2999
files      : 1273
cuda_avail : True
faiss.index: exists
```

If `tier: bm25`, the FAISS index is missing or the background thread has not completed. Run
Procedure C (Forced Full Rebuild) and restart.

---

## Server Configuration Reference

| Item                  | Value                                                                             |
| --------------------- | --------------------------------------------------------------------------------- |
| Server script         | `.claude/mcp-servers/workspace-knowledge/server.py`                               |
| venv                  | `.claude/mcp-servers/workspace-knowledge/.venv/`                                  |
| Embedding folder      | `.claude/mcp-servers/workspace-knowledge/embedding/` (gitignored — entire folder) |
| Model files           | `embedding/model/` — `all-mpnet-base-v2` (418 MB, local copy, no HF cache needed) |
| FAISS index           | `embedding/faiss.index` (8.8 MB, gitignored)                                      |
| Index state           | `embedding/index_state.json` (147 KB, gitignored)                                 |
| Embedding device      | `cuda:0` — NVIDIA GeForce RTX 4060 Laptop GPU (8 GB GDDR6)                        |
| Model load time       | **0.7 s** (local path) vs 14 s (HuggingFace cache)                                |
| Torch wheel           | `torch 2.6.0+cu124` (CUDA 12.4) — **must not be replaced with CPU wheel**         |
| Indexed directories   | `company/`, `studio/`, `core-component-00/`, `telescope/`                         |
| MCP registration      | `.mcp.json` → `workspace-knowledge`                                               |
| MCP governance record | `.claude/rules/mcp-governance.md`                                                 |

---

## References

### Internal Documentation

- `.claude/rules/mcp-governance.md` — MCP Three-Gate governance record
- `.claude/mcp-servers/workspace-knowledge/server.py` — Production server implementation
- `telescope/2026-06-20-mcp-server-assessment/research-report.md` — Phase 1/2 architecture
  decisions and rag-deployment-proposal.md
- `core-component-00/retrieval-augmented-generation/CLAUDE.md` — RAG module overview
- `core-component-00/agent-systems-engineering/governance/` — ASE compliance standards

### Related Work

- Phase 1 BM25 implementation: commit `404dbd6`
- Phase 2 Hybrid RAG implementation: commit `acf5515`
- MCP timeout fix (background thread): commit `6b0ca3d`
- git-worktree-manager retirement: commit `9b661b7` / `b130762`

---

## Appendices

### Appendix A: Known Defect — Background Thread Hang

**Symptom:** Server starts at `tier: bm25`. `faiss.index` never appears on disk after 5+ minutes.
No error is logged.

**Root cause (suspected):** `model.encode()` inside a `threading.Thread(daemon=True)` interacts
with FastMCP's asyncio event loop (stdio transport). The main thread holds the GIL during
`mcp.run()` I/O processing, starving the encode loop. No exception is raised because the thread is
a daemon — when the main thread exits, it is silently killed.

**Canonical workaround:** Run `build_faiss.py` as a standalone process (not inside the server
process). The server detects `faiss.index` on startup and loads it without triggering the build
path. This is Procedure C above.

**Candidate fix (not yet implemented):** Replace `threading.Thread` with
`concurrent.futures.ProcessPoolExecutor` to bypass GIL contention, or refactor the build into an
async coroutine using `asyncio.run_in_executor`.

---

### Appendix B: Build Script

The canonical index build script is at:

```
C:\Users\ASUS\.claude\jobs\7d1596c6\tmp\build_faiss.py
```

This script stubs FastMCP, imports `server.py` to reuse chunk ingestion logic, then builds and
writes the FAISS index and mtime state file directly. It is the authoritative build path until the
background thread defect is resolved.

---

## Version History

| Version | Date       | Author          | Changes                                                                 |
| ------- | ---------- | --------------- | ----------------------------------------------------------------------- |
| 1.0     | 2026-06-24 | Dr. Elias Vance | Initial runbook — Phase 2 ops                                           |
| 1.1     | 2026-06-24 | Dr. Elias Vance | Update paths for embedding/ subfolder; model now loaded from local path |

---

**Template Version:** 1.0  
**Last Updated:** 2026-06-24  
**Maintained By:** Core Component 00 Laboratory  
**Authority:** AGENTS.md § 6. Core Component 00
