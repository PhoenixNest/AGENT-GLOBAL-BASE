# Local RAG Deployment — Operations Manual

**Document Type:** Operations Manual
**Prepared By:** Core Component 00 Laboratory — Dr. Elias Vance, Laboratory Director
**Date:** 2026-06-24
**Status:** Active
**Target System:** `workspace-knowledge` MCP Server — `agent-global-base`
**Reference Documents:**

- `../research-report.md` — Investigation and findings
- `../rag-deployment-proposal.md` — CEO-facing deployment proposal
- `.claude/mcp-servers/workspace-knowledge/server.py` — Implementation target

---

## Quick Reference

| Item                  | Value                                                           |
| --------------------- | --------------------------------------------------------------- |
| **This machine**      | Intel i9-13900H, 31.6 GB RAM, Intel Iris Xe (2 GB), 256 GB disk |
| **Hardware tier**     | Tier 3 — Full hybrid BM25 + semantic embeddings                 |
| **Recommended model** | `sentence-transformers/all-mpnet-base-v2` (420 MB, CPU)         |
| **Python version**    | 3.13.5 (detected)                                               |
| **fastmcp version**   | 3.2.4 (installed)                                               |
| **Phase 1 install**   | `pip install rank_bm25`                                         |
| **Phase 2 install**   | `pip install sentence-transformers faiss-cpu`                   |

---

## Section 1: Hardware Detection and Tier Assignment

### Why Hardware Detection Matters

The RAG system has three operating modes. The correct mode is determined by available RAM, since
the embedding model and FAISS index are held in memory during operation. Selecting too large a
model for available RAM causes swap thrashing; selecting too small a model when more RAM is
available leaves retrieval quality on the table.

The server auto-detects RAM at startup and selects the appropriate configuration tier.

### Hardware Tiers

| Tier   | RAM Available | Operating Mode                       | Recommended Embedding Model  | Index Type |
| ------ | ------------- | ------------------------------------ | ---------------------------- | ---------- |
| Tier 1 | < 4 GB        | BM25 keyword search only             | None                         | N/A        |
| Tier 2 | 4 GB – 16 GB  | Hybrid BM25 + lightweight embeddings | `all-MiniLM-L6-v2` (80 MB)   | FAISS Flat |
| Tier 3 | > 16 GB       | Hybrid BM25 + full embeddings        | `all-mpnet-base-v2` (420 MB) | FAISS Flat |

> **This machine (31.6 GB RAM) is Tier 3.** `all-mpnet-base-v2` is recommended. If Tier 3
> performance is acceptable, there is no reason to use the smaller Tier 2 model.

### RAM Detection — Python Snippet

```python
import psutil

def detect_hardware_tier() -> int:
    """Return hardware tier (1, 2, or 3) based on available system RAM."""
    ram_gb = psutil.virtual_memory().available / (1024 ** 3)
    if ram_gb < 4:
        return 1
    elif ram_gb < 16:
        return 2
    else:
        return 3
```

> **Note:** The check uses _available_ RAM (not total), accounting for the OS and other running
> processes. On this machine with 31.6 GB total, available RAM at typical load is ~22–27 GB,
> firmly in Tier 3.

---

## Section 2: Software Stack

### Full Dependency List

| Package                 | Purpose                                    | Required For | Min Version | Install Command                     |
| ----------------------- | ------------------------------------------ | ------------ | ----------- | ----------------------------------- |
| `fastmcp`               | MCP server framework                       | Phase 1 & 2  | 3.0.0       | _already installed (3.2.4)_         |
| `psutil`                | RAM detection for tier assignment          | Phase 1 & 2  | 5.9.0       | `pip install psutil`                |
| `rank_bm25`             | BM25 ranking algorithm                     | Phase 1 & 2  | 0.2.2       | `pip install rank_bm25`             |
| `sentence-transformers` | Embedding model loader and inference       | Phase 2 only | 2.7.0       | `pip install sentence-transformers` |
| `faiss-cpu`             | Vector similarity search index (CPU build) | Phase 2 only | 1.8.0       | `pip install faiss-cpu`             |
| `numpy`                 | Array operations for FAISS                 | Phase 2 only | 1.26.0      | _auto-installed with faiss-cpu_     |

> **Do not install `faiss-gpu`** — the Intel Iris Xe integrated GPU does not support CUDA.
> `faiss-cpu` is the correct package for this machine.

### Python Version Compatibility

- **Minimum:** Python 3.9
- **Detected:** Python 3.13.5
- **Status:** All packages above support Python 3.13. No version conflict expected.

### Phase 1 Installation (BM25 Only)

```powershell
pip install psutil rank_bm25
```

**Expected output:** Both packages install cleanly. No compilation step; both are pure Python.

### Phase 2 Installation (Adds Embeddings)

```powershell
pip install sentence-transformers faiss-cpu
```

**Expected output:** `sentence-transformers` pulls in `transformers`, `torch` (CPU build), and
`huggingface-hub` as dependencies. Total download ~500 MB on first install.

> **PyTorch note:** `sentence-transformers` installs a CPU-only PyTorch build automatically
> when no CUDA is detected. On this machine (Intel Xe, no CUDA), this is correct behavior.
> Do not separately install `torch` with CUDA flags.

### Verification

After installation, confirm all packages are present:

```powershell
pip show rank_bm25 sentence-transformers faiss-cpu psutil
```

All four should return name/version output with no "not found" errors.

---

## Section 3: Model Registry

### Tier 1 — No Embedding Model

No model required. BM25 operates on tokenized text only.

---

### Tier 2 Model — `all-MiniLM-L6-v2`

| Field                | Value                                                           |
| -------------------- | --------------------------------------------------------------- |
| **Model ID**         | `sentence-transformers/all-MiniLM-L6-v2`                        |
| **Source**           | Hugging Face Hub                                                |
| **Model Card URL**   | `https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2` |
| **Architecture**     | MiniLM-L6 (6-layer transformer, distilled)                      |
| **Embedding Size**   | 384 dimensions                                                  |
| **Model File Size**  | ~80 MB (PyTorch weights)                                        |
| **RAM at Runtime**   | ~200 MB (model + inference buffers)                             |
| **Inference Speed**  | ~50–100 ms/batch on i9-13900H CPU                               |
| **Max Input Length** | 256 tokens (sequences truncated beyond this)                    |
| **Download Method**  | Automatic on first `SentenceTransformer()` load                 |
| **Cache Location**   | `~/.cache/huggingface/hub/`                                     |

**Integrity verification (post-download):**

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
test_vec = model.encode(["hello world"])
assert test_vec.shape == (1, 384), "Unexpected embedding dimensions"
print("Model loaded and verified.")
```

---

### Tier 3 Model — `all-mpnet-base-v2` _(Recommended for this machine)_

| Field                | Value                                                            |
| -------------------- | ---------------------------------------------------------------- |
| **Model ID**         | `sentence-transformers/all-mpnet-base-v2`                        |
| **Source**           | Hugging Face Hub                                                 |
| **Model Card URL**   | `https://huggingface.co/sentence-transformers/all-mpnet-base-v2` |
| **Architecture**     | MPNet-base (12-layer transformer)                                |
| **Embedding Size**   | 768 dimensions                                                   |
| **Model File Size**  | ~420 MB (PyTorch weights)                                        |
| **RAM at Runtime**   | ~700 MB (model + inference buffers)                              |
| **Inference Speed**  | ~150–300 ms/batch on i9-13900H CPU                               |
| **Max Input Length** | 384 tokens (sequences truncated beyond this)                     |
| **Download Method**  | Automatic on first `SentenceTransformer()` load                  |
| **Cache Location**   | `~/.cache/huggingface/hub/`                                      |

**Why Tier 3 produces better results:** MPNet-base uses a full 12-layer encoder with masked and
permuted language modelling pre-training. Benchmark scores (SBERT MTEB) show it consistently
outperforms MiniLM-L6 on semantic similarity tasks by 5–8 percentage points. On a machine with
32 GB RAM the additional memory cost (700 MB vs 200 MB) is negligible.

**Integrity verification (post-download):**

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
test_vec = model.encode(["hello world"])
assert test_vec.shape == (1, 768), "Unexpected embedding dimensions"
print("Model loaded and verified.")
```

---

### Download Procedures

#### Automatic Download (Standard)

`sentence-transformers` downloads the model from Hugging Face Hub on the first
`SentenceTransformer(model_id)` call. The download is resumable; if it is interrupted, re-run
and it will continue from where it stopped.

```python
from sentence_transformers import SentenceTransformer
# First call triggers download; subsequent calls load from cache
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
```

#### Manual Download (Offline-First Workflow)

If the target machine has internet access only during setup:

```powershell
# On a machine with internet access
pip install huggingface-hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='sentence-transformers/all-mpnet-base-v2',
    local_dir='C:/models/all-mpnet-base-v2'
)
"
```

Then point the server to the local path instead of the Hub ID:

```python
model = SentenceTransformer("C:/models/all-mpnet-base-v2")
```

#### Offline Operation After First Download

Once downloaded, `sentence-transformers` reads from `~/.cache/huggingface/hub/` with no
internet access required. Set `HF_HUB_OFFLINE=1` in the environment to prevent any network
calls at runtime:

```powershell
$env:HF_HUB_OFFLINE = "1"
```

---

## Section 4: Hardware-Adaptive Configuration

The server selects its operating profile at startup based on detected available RAM. All profile
values can be overridden via environment variables (see Section 5).

### Configuration Profiles

```python
HARDWARE_PROFILES = {
    1: {  # < 4 GB available RAM
        "mode": "bm25_only",
        "embedding_model": None,
        "chunk_size": 300,
        "chunk_overlap": 30,
        "top_k": 5,
        "bm25_k1": 1.5,
        "bm25_b": 0.75,
        "faiss_index_type": None,
        "embedding_batch_size": 0,
        "rrf_k": None,
        "persist_index": False,
    },
    2: {  # 4–16 GB available RAM
        "mode": "hybrid",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "chunk_size": 512,
        "chunk_overlap": 64,
        "top_k": 5,
        "bm25_k1": 1.5,
        "bm25_b": 0.75,
        "faiss_index_type": "Flat",
        "embedding_batch_size": 32,
        "rrf_k": 60,
        "persist_index": True,
    },
    3: {  # > 16 GB available RAM — THIS MACHINE
        "mode": "hybrid",
        "embedding_model": "sentence-transformers/all-mpnet-base-v2",
        "chunk_size": 512,
        "chunk_overlap": 64,
        "top_k": 5,
        "bm25_k1": 1.5,
        "bm25_b": 0.75,
        "faiss_index_type": "Flat",
        "embedding_batch_size": 64,
        "rrf_k": 60,
        "persist_index": True,
    },
}
```

### Startup Decision Flow

```
Server starts
    │
    ├─► psutil.virtual_memory().available → RAM check
    │         │
    │    < 4 GB ──► Tier 1: BM25 only, no model load
    │    4–16 GB ──► Tier 2: Load all-MiniLM-L6-v2, build FAISS Flat index
    │    > 16 GB ──► Tier 3: Load all-mpnet-base-v2, build FAISS Flat index
    │
    ├─► Check for env var overrides (EMBEDDING_MODEL, CHUNK_SIZE, etc.)
    │
    ├─► Load or rebuild FAISS index from disk (if persist_index=True)
    │         │
    │    Index exists and up-to-date ──► Load from disk (fast, ~2 sec)
    │    Index missing or stale ──────► Rebuild from corpus (slow, ~30–120 sec)
    │
    └─► Server ready
```

---

## Section 5: Configuration Parameter Reference

All parameters can be overridden via environment variables in `.mcp.json`. Environment variable
names are the uppercase snake*case form prefixed with `RAG*`.

| Parameter              | Env Var                | Default (Tier 3)                                 | Valid Range                   | Description                                               |
| ---------------------- | ---------------------- | ------------------------------------------------ | ----------------------------- | --------------------------------------------------------- |
| `mode`                 | `RAG_MODE`             | `hybrid`                                         | `bm25_only`, `hybrid`         | Force operating mode, bypassing auto-detection            |
| `embedding_model`      | `RAG_EMBEDDING_MODEL`  | `sentence-transformers/all-mpnet-base-v2`        | Any HF model ID or local path | Override model selection                                  |
| `chunk_size`           | `RAG_CHUNK_SIZE`       | `512`                                            | `128` – `1024`                | Max words per document chunk                              |
| `chunk_overlap`        | `RAG_CHUNK_OVERLAP`    | `64`                                             | `0` – `256`                   | Words of overlap between adjacent chunks                  |
| `top_k`                | `RAG_TOP_K`            | `5`                                              | `1` – `20`                    | Number of results returned per query                      |
| `bm25_k1`              | `RAG_BM25_K1`          | `1.5`                                            | `0.5` – `2.5`                 | BM25 term saturation (lower = more saturation)            |
| `bm25_b`               | `RAG_BM25_B`           | `0.75`                                           | `0.0` – `1.0`                 | BM25 length normalization (1.0 = full, 0.0 = off)         |
| `faiss_index_type`     | `RAG_FAISS_INDEX_TYPE` | `Flat`                                           | `Flat`, `IVF`                 | FAISS index structure (use IVF for >5000 chunks)          |
| `embedding_batch_size` | `RAG_EMBED_BATCH_SIZE` | `64`                                             | `8` – `256`                   | Chunks embedded per batch (higher = faster, more RAM)     |
| `rrf_k`                | `RAG_RRF_K`            | `60`                                             | `10` – `100`                  | Reciprocal Rank Fusion constant (higher = smoother blend) |
| `persist_index`        | `RAG_PERSIST_INDEX`    | `true`                                           | `true`, `false`               | Save FAISS index to disk between restarts                 |
| `index_dir`            | `RAG_INDEX_DIR`        | `.claude/mcp-servers/workspace-knowledge/.index` | Any writable path             | Directory for persisted FAISS index and metadata          |
| `auto_rebuild`         | `RAG_AUTO_REBUILD`     | `true`                                           | `true`, `false`               | Rebuild index on startup if source files changed          |

### Parameter Tuning Guidance

**`chunk_size`:** Smaller chunks (256–300) give more precise snippets at the cost of losing
cross-sentence context. Larger chunks (768–1024) preserve more context but may return
less-targeted results. 512 is the standard industry default for mixed documentation corpora.

**`bm25_k1`:** Controls how quickly term frequency saturates. At k1=1.5, a term appearing 5
times scores notably higher than once but levels off. For technical documentation with repeated
domain terms, values between 1.2 and 1.8 work best.

**`bm25_b`:** At b=0.75, a very long document does not disproportionately outrank shorter ones.
Set to 0.0 if document length variation should have no effect on ranking (not recommended for
this corpus which mixes short pipeline summaries with long CC-00 module docs).

**`rrf_k`:** Higher values cause the BM25 and embedding rankings to blend more smoothly, giving
more weight to items that rank well in both. Lower values amplify items that are top-ranked in
one method. 60 is the standard default from the RRF literature.

**`faiss_index_type`:** Use `Flat` for the current corpus (estimated 200–500 chunks). Switch to
`IVF` only if the corpus grows beyond ~5,000 chunks and query latency exceeds 500 ms.

---

## Section 6: `.mcp.json` Configuration

### Phase 1 Configuration (BM25 Only)

```json
{
  "mcpServers": {
    "workspace-knowledge": {
      "command": "python",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/.claude/mcp-servers/workspace-knowledge/server.py"],
      "env": {
        "WORKSPACE_ROOT": "${CLAUDE_PROJECT_DIR:-.}",
        "FASTMCP_LOG_LEVEL": "ERROR",
        "RAG_MODE": "bm25_only"
      }
    }
  }
}
```

### Phase 2 Configuration (Hybrid — Recommended for This Machine)

```json
{
  "mcpServers": {
    "workspace-knowledge": {
      "command": "python",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/.claude/mcp-servers/workspace-knowledge/server.py"],
      "env": {
        "WORKSPACE_ROOT": "${CLAUDE_PROJECT_DIR:-.}",
        "FASTMCP_LOG_LEVEL": "ERROR",
        "RAG_EMBEDDING_MODEL": "sentence-transformers/all-mpnet-base-v2",
        "RAG_CHUNK_SIZE": "512",
        "RAG_CHUNK_OVERLAP": "64",
        "RAG_TOP_K": "5",
        "RAG_PERSIST_INDEX": "true",
        "RAG_INDEX_DIR": "${CLAUDE_PROJECT_DIR:-.}/.claude/mcp-servers/workspace-knowledge/.index",
        "RAG_AUTO_REBUILD": "true"
      }
    }
  }
}
```

> **Do not set `RAG_MODE`** in Phase 2 config — let the server auto-detect from RAM. On this
> machine it will select Tier 3 automatically.

---

## Section 7: Deployment Procedures

### Phase 1 Deployment Steps

1. **Install dependencies:**

   ```powershell
   pip install psutil rank_bm25
   ```

2. **Rewrite the server** — Replace `workspace-knowledge/server.py` with the BM25 implementation
   (see `../research-report.md` Appendix B for reference architecture).

3. **Update `.mcp.json`** — Apply Phase 1 configuration from Section 6.

4. **Verify server starts:**

   ```powershell
   python .claude/mcp-servers/workspace-knowledge/server.py
   ```

   Expected output: Server starts, logs index size (file count + chunk count), no errors.
   Press Ctrl+C to stop.

5. **Restart Claude Code** — MCP servers are loaded at session start; a restart is required to
   pick up the new server.

6. **Run acceptance queries** (see Section 8).

---

### Phase 2 Deployment Steps

> Complete Phase 1 and validate acceptance criteria before starting Phase 2.

1. **Install dependencies:**

   ```powershell
   pip install sentence-transformers faiss-cpu
   ```

2. **Download the embedding model** (requires internet, one time only):

   ```powershell
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"
   ```

   Expected output: Download progress bars, then model loaded message. The model caches to
   `~/.cache/huggingface/hub/`. Subsequent loads read from cache without internet.

3. **Extend the server** — Add the embedding + FAISS layer on top of the Phase 1 BM25 engine.

4. **Update `.mcp.json`** — Apply Phase 2 configuration from Section 6.

5. **First-run index build** — On first start after Phase 2, the server will:
   - Load the embedding model (~5–10 seconds on i9-13900H)
   - Embed all document chunks in batches (~30–90 seconds depending on corpus size)
   - Write the FAISS index to `RAG_INDEX_DIR`
   - Log: `"FAISS index built and persisted: N chunks"`

6. **Restart Claude Code** and run acceptance queries (see Section 8).

---

### Rebuilding the Index

The index should be rebuilt whenever significant new documentation is added (e.g., new telescope
research reports, new pipeline docs).

**Automatic rebuild** (if `RAG_AUTO_REBUILD=true`): The server compares file modification times
at startup and triggers a rebuild if any indexed files have changed since the last build.

**Manual rebuild via MCP tool:**

```
Tool: rebuild_index
Arguments: {}
```

This can be invoked from within a Claude Code session without restarting the server.

**Manual rebuild via Python:**

```powershell
python -c "
import sys
sys.path.insert(0, '.claude/mcp-servers/workspace-knowledge')
from server import rag_engine
rag_engine.rebuild()
print('Done')
"
```

---

## Section 8: Verification and Acceptance Testing

Run these queries after each deployment phase. All should return relevant results within the
stated latency.

### Phase 1 Acceptance Queries

| Query                                   | Expected Result                             | Pass Criterion                       |
| --------------------------------------- | ------------------------------------------- | ------------------------------------ |
| `pipeline stage 3 deliverables`         | Pipeline docs listing UML package, ADR, TSD | Top result is a pipeline.md section  |
| `MCP server assessment`                 | This investigation's research report        | `telescope/` report in top 3         |
| `context budget monitoring`             | H-CE01 hook doc or CC-00 context module     | Relevant section returned as snippet |
| `git worktree branch naming convention` | Multi-agent orchestration spec              | Correct doc returned in top 5        |

### Phase 2 Acceptance Queries (Synonym / Conceptual)

| Query                               | Expected Result                             | Pass Criterion                              |
| ----------------------------------- | ------------------------------------------- | ------------------------------------------- |
| `token budget`                      | Docs discussing context window limits       | Same results as "context window management" |
| `error recovery in agent systems`   | Harness engineering docs on fault tolerance | Returns harness module content              |
| `how investigations are documented` | Telescope README and CLAUDE.md              | Returns telescope/ docs                     |
| `who runs the LLM research lab`     | Dr. Elias Vance profile                     | Director profile returned                   |

### Disaster Recovery Acceptance Tests

Run these after Phase 1 deployment to verify the graceful-degradation architecture (§10).

| Test                                | Method                                                     | Pass Criterion                                                          |
| ----------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Raw FS fallback**                 | Uninstall `rank_bm25`; start server; run any query         | Results returned with `_meta.search_tier = "rawfs"`                     |
| **BM25 degraded mode**              | Uninstall `sentence-transformers`; start server; run query | Results returned with `_meta.search_tier = "bm25"`                      |
| **`_meta` always present**          | Run any query on any tier                                  | Every response includes `_meta.search_tier`, `_meta.degradation_reason` |
| **No server crash on missing deps** | Remove all RAG deps; start server                          | Server starts and responds (does not throw uncaught exception)          |
| **Tier logged on demotion**         | Simulate OOM in Tier A handler; run query                  | `logging.error` entry written; response tier demoted to BM25            |

### Latency Benchmarks (Target: i9-13900H)

| Operation                          | Target        | Notes                              |
| ---------------------------------- | ------------- | ---------------------------------- |
| Server cold start (Phase 1)        | < 5 seconds   | Index build from disk read         |
| Server cold start (Phase 2, warm)  | < 15 seconds  | Model load from cache + index load |
| Server cold start (Phase 2, first) | < 120 seconds | Full embed + index build           |
| Query response (Phase 1, BM25)     | < 100 ms      | Pure Python BM25                   |
| Query response (Phase 2, hybrid)   | < 500 ms      | BM25 + embedding inference + RRF   |

---

## Section 9: Troubleshooting Guide

### `ImportError: No module named 'rank_bm25'`

**Cause:** Package not installed or installed in a different Python environment.

**Fix:**

```powershell
pip install rank_bm25
# Confirm the correct Python is used:
python -c "import rank_bm25; print('OK')"
```

---

### `ImportError: No module named 'faiss'`

**Cause:** `faiss-cpu` not installed, or `faiss-gpu` was accidentally installed.

**Fix:**

```powershell
pip uninstall faiss-gpu -y 2>$null
pip install faiss-cpu
```

---

### `OSError: Can't load tokenizer for 'sentence-transformers/all-mpnet-base-v2'`

**Cause:** Model cache corrupted or incomplete download.

**Fix:** Delete the cached model and re-download:

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.cache\huggingface\hub\models--sentence-transformers--all-mpnet-base-v2"
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-mpnet-base-v2')"
```

---

### Server selects wrong hardware tier

**Cause:** Available RAM at server start was lower than usual (many background processes).

**Fix:** Override the mode explicitly:

```json
"RAG_EMBEDDING_MODEL": "sentence-transformers/all-mpnet-base-v2"
```

Or check available RAM:

```powershell
python -c "import psutil; print(f'{psutil.virtual_memory().available / 1e9:.1f} GB available')"
```

---

### FAISS index stale — new documents not appearing in search results

**Cause:** `RAG_AUTO_REBUILD=false` and `rebuild_index` has not been called since documents were
added.

**Fix:** Invoke `rebuild_index` via the MCP tool, or set `RAG_AUTO_REBUILD=true` in `.mcp.json`.

---

### Query latency exceeds 500 ms consistently (Phase 2)

**Cause:** Corpus has grown large enough to saturate FAISS Flat index, or embedding batch
processing is a bottleneck.

**Diagnosis:**

```powershell
python -c "
import faiss, numpy as np
index = faiss.read_index('.claude/mcp-servers/workspace-knowledge/.index/faiss.index')
print(f'Index contains {index.ntotal} vectors')
"
```

**Fix (< 5,000 vectors):** Reduce `RAG_EMBED_BATCH_SIZE` to free inference memory.

**Fix (> 5,000 vectors):** Switch to IVF index:

```json
"RAG_FAISS_INDEX_TYPE": "IVF"
```

This requires a full index rebuild.

---

### `ModuleNotFoundError: No module named 'psutil'`

**Cause:** `psutil` not installed; required for hardware tier detection.

**Fix:**

```powershell
pip install psutil
```

---

### Torch CPU vs GPU confusion

**Symptom:** `sentence-transformers` attempts to use Intel Xe GPU via DirectML, causing errors
or slow performance.

**Cause:** `torch` installed with a CUDA or DirectML backend.

**Fix:** Force CPU device:

```python
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2", device="cpu")
```

Or set via environment variable:

```json
"CUDA_VISIBLE_DEVICES": ""
```

---

## Section 10: Graceful-Degradation Architecture

### Design Principle

The MCP server is the contract; the RAG engine is the implementation. If the implementation
degrades, the contract must still be honored at a lower fidelity level that is explicitly
declared to the caller. The server must never return an uncaught exception when it can still
return useful results from raw filesystem access.

---

### Failure Modes

| ID  | Failure Mode                         | Trigger                                        | Phase Affected |
| --- | ------------------------------------ | ---------------------------------------------- | -------------- |
| F1  | BM25 index not built (cold start)    | `rank_bm25` import fails or corpus scan errors | Phase 1 + 2    |
| F2  | BM25 index stale or corrupt          | Disk corruption, interrupted index build       | Phase 1 + 2    |
| F3  | `sentence-transformers` import fails | Missing install, Python environment mismatch   | Phase 2 only   |
| F4  | FAISS index missing or corrupt       | First-run embedding failed, disk full          | Phase 2 only   |
| F5  | Model file absent                    | HuggingFace cache deleted, no internet         | Phase 2 only   |
| F6  | Embedding inference OOM              | RAM spike from another process                 | Phase 2 only   |
| F7  | Corpus directory unreadable          | Permissions error, drive unmounted             | Phase 1 + 2    |

F7 is the only unrecoverable failure. All others have a viable fallback path.

---

### Three-Tier Fallback Ladder

```
Tier A — Full Hybrid (Phase 2 nominal)
         BM25 + FAISS embedding search + RRF fusion
            │  F3 / F4 / F5 / F6
            ▼
Tier B — BM25 Only (Phase 1 nominal / Phase 2 degraded)
         BM25 keyword search on chunked index
            │  F1 / F2
            ▼
Tier C — Raw Filesystem (Disaster Recovery)
         Direct file read + term-frequency count
         Zero third-party dependencies — always reachable
            │  F7
            ▼
Tier D — Hard Failure (unrecoverable — F7 only)
```

---

### Implementation Pattern

```python
from enum import Enum
import logging

class SearchTier(Enum):
    HYBRID = "hybrid"
    BM25   = "bm25"
    RAWFS  = "rawfs"

_active_tier: SearchTier = SearchTier.RAWFS
_degradation_reason: str = ""

def _initialize_search_engine() -> SearchTier:
    global _active_tier, _degradation_reason

    try:
        from sentence_transformers import SentenceTransformer
        import faiss
        # load model and FAISS index ...
        _active_tier = SearchTier.HYBRID
        return SearchTier.HYBRID
    except Exception as e:
        _degradation_reason = f"Hybrid unavailable: {e}"
        logging.warning(_degradation_reason)

    try:
        from rank_bm25 import BM25Okapi
        # build BM25 index ...
        _active_tier = SearchTier.BM25
        return SearchTier.BM25
    except Exception as e:
        _degradation_reason = f"BM25 unavailable: {e}"
        logging.warning(_degradation_reason)

    _active_tier = SearchTier.RAWFS
    _degradation_reason = "Operating in disaster-recovery mode (raw filesystem)"
    logging.error(_degradation_reason)
    return SearchTier.RAWFS

def _search_with_fallback(query: str, top_k: int) -> dict:
    global _active_tier
    try:
        if _active_tier == SearchTier.HYBRID:
            return _hybrid_search(query, top_k)
        if _active_tier == SearchTier.BM25:
            return _bm25_search(query, top_k)
        return _rawfs_search(query, top_k)
    except Exception as e:
        if _active_tier == SearchTier.HYBRID:
            _active_tier = SearchTier.BM25
            logging.error(f"Hybrid failed, demoting to BM25: {e}")
            return _search_with_fallback(query, top_k)
        if _active_tier == SearchTier.BM25:
            _active_tier = SearchTier.RAWFS
            logging.error(f"BM25 failed, demoting to RAWFS: {e}")
            return _search_with_fallback(query, top_k)
        raise  # F7 — unrecoverable
```

Tier demotion is **one-way per server session**. Re-elevation to a higher tier requires a server
restart (which re-runs `_initialize_search_engine`).

---

### Operational Signals (`_meta` Block)

Every tool response must include a `_meta` block regardless of active tier:

```json
{
  "results": [...],
  "_meta": {
    "search_tier": "bm25",
    "degradation_reason": "Hybrid unavailable: No module named 'sentence_transformers'",
    "result_quality": "keyword-only — synonym queries may miss relevant documents",
    "rebuild_available": true
  }
}
```

| `search_tier` | Meaning to the Caller                                             |
| ------------- | ----------------------------------------------------------------- |
| `"hybrid"`    | Full semantic + keyword — highest quality                         |
| `"bm25"`      | Keyword-only — synonym gaps exist; suggest precise terminology    |
| `"rawfs"`     | Disaster recovery — term-frequency only; results may be imprecise |

An agent receiving `"rawfs"` should surface this to the user and suggest calling `rebuild_index`
or restarting the MCP server. An agent receiving `"bm25"` should note that synonym queries may
underperform and recommend precise terminology.

---

### Recovery Procedure

1. Identify the degradation reason from `_meta.degradation_reason` or the server log.
2. Fix the root cause (install missing package, clear corrupt cache, free disk space).
3. Restart the MCP server — `_initialize_search_engine` runs on startup and re-selects the
   highest available tier automatically.
4. Verify recovery by calling `rebuild_index` and confirming `_meta.search_tier` returns to the
   expected tier.

---

### Acceptance Criteria

See §8 — Disaster Recovery Acceptance Tests.

---

## Appendix A: Complete Phase 2 Install Sequence (This Machine)

```powershell
# 1. Install all dependencies
pip install psutil rank_bm25 sentence-transformers faiss-cpu

# 2. Pre-download the Tier 3 embedding model (requires internet, one time)
python -c "
from sentence_transformers import SentenceTransformer
print('Downloading all-mpnet-base-v2...')
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
vec = model.encode(['test'])
print(f'Model ready. Embedding dim: {vec.shape[1]}')
"

# 3. Verify all packages
pip show rank_bm25 sentence-transformers faiss-cpu psutil

# 4. Confirm RAM tier
python -c "
import psutil
ram = psutil.virtual_memory().available / 1e9
tier = 1 if ram < 4 else 2 if ram < 16 else 3
print(f'Available RAM: {ram:.1f} GB → Tier {tier}')
"
```

**Expected final output:**

```
Available RAM: 22.4 GB → Tier 3
```

---

## Appendix B: Environment Variables Quick Reference

```json
{
  "RAG_MODE": "hybrid",
  "RAG_EMBEDDING_MODEL": "sentence-transformers/all-mpnet-base-v2",
  "RAG_CHUNK_SIZE": "512",
  "RAG_CHUNK_OVERLAP": "64",
  "RAG_TOP_K": "5",
  "RAG_BM25_K1": "1.5",
  "RAG_BM25_B": "0.75",
  "RAG_FAISS_INDEX_TYPE": "Flat",
  "RAG_EMBED_BATCH_SIZE": "64",
  "RAG_RRF_K": "60",
  "RAG_PERSIST_INDEX": "true",
  "RAG_INDEX_DIR": ".claude/mcp-servers/workspace-knowledge/.index",
  "RAG_AUTO_REBUILD": "true",
  "HF_HUB_OFFLINE": "1"
}
```

---

## Appendix C: Corpus Size Estimation

Run this to estimate index size before deployment:

```powershell
python -c "
from pathlib import Path

KEY_DIRS = [
    'company/library',
    'company/pipeline',
    'company/departments',
    'studio/casual-games/library',
    'studio/casual-games/pipeline',
    'core-component-00',
    '.claude/rules',
    '.claude/skills',
    'telescope',
]

total_files = 0
total_chars = 0
for d in KEY_DIRS:
    p = Path(d)
    if p.exists():
        for f in p.rglob('*.md'):
            total_files += 1
            total_chars += len(f.read_text(encoding='utf-8', errors='ignore'))

avg_chunk = 512 * 4.5  # ~4.5 chars per word
estimated_chunks = int(total_chars / avg_chunk)
print(f'Files: {total_files}')
print(f'Total chars: {total_chars:,}')
print(f'Estimated chunks: {estimated_chunks}')
print(f'FAISS index type: {\"Flat\" if estimated_chunks < 5000 else \"IVF (recommended)\"}')
"
```

---

**Document version:** 1.0 — 2026-06-24
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
**Next Review:** After Phase 1 deployment validation
