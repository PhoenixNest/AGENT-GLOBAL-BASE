# Qdrant Deployment Guide

**Document Type:** Migration Planning Deliverable
**Investigation:** `2026-06-25-qdrant-migration-plan`
**Author:** Dr. Elias Vance — CC-00 Laboratory Director
**Date:** 2026-06-25
**Status:** Approved

---

## 1. Deployment Mode Decision

**Decision: Qdrant Docker Mode — standalone server on `localhost:6333` (CEO approved
2026-06-25)**

Qdrant offers three deployment modes. For this workspace:

| Mode                                                                           | Requirement                                                    | Decision                                                                           |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **In-memory** (`QdrantClient(":memory:")`)                                     | No persistence; lost on restart                                | ❌ Rejected — index must survive sessions                                          |
| **Embedded local** (`QdrantClient(path="./qdrant_storage")`)                   | Pure Python client, persistent disk storage, no server process | ❌ Superseded — data format incompatible with server; Python reimplementation only |
| **Standalone server via Docker** (`QdrantClient(url="http://localhost:6333")`) | Docker Desktop running; ports 6333/6334 available              | ✅ Selected — full Rust engine; production data format; CEO override               |

**Rationale:** Docker runs the full Qdrant Rust engine — not the Python reimplementation used by
embedded mode. This means the data format is compatible with any future server upgrade (embedded
mode data is explicitly incompatible with the server). The CEO's approval of Docker waives the
no-daemon-process convention for this workstation. Docker Desktop for Windows is required and
must be running before the MCP server starts.

**Critical note on embedded mode rejection:** The `qdrant-deployment-options` skill states
explicitly: _"Local mode data format is NOT compatible with server."_ Had embedded mode been used
in Phase 1 and Docker adopted later, a full collection reseed would have been required. Starting
with Docker eliminates this future migration cost entirely.

---

## 2. Hardware Compatibility Assessment

| Component      | Spec                        | Assessment                                                                                 |
| -------------- | --------------------------- | ------------------------------------------------------------------------------------------ |
| CPU            | Intel i9-13900H (14 cores)  | ✅ Qdrant server is CPU-bound; excellent fit                                               |
| RAM            | 31.6 GB                     | ✅ Docker container uses ~200–500 MB RAM for active queries; ample headroom                |
| GPU            | RTX 4060 (8 GB GDDR6, CUDA) | ⚠️ Qdrant itself is CPU-only; GPU remains used for embedding (sentence-transformers)       |
| Storage        | Local SSD (assumed)         | ✅ Qdrant Docker named volume ≈ 50–200 MB at current corpus size                           |
| OS             | Windows 11 Home             | ✅ Docker Desktop for Windows supports WSL2 backend; Qdrant Docker image is Linux-based    |
| Python         | 3.11                        | ✅ qdrant-client >= 1.7.0 supports Python 3.8+                                             |
| Docker Desktop | Required (WSL2 backend)     | ✅ Must be installed and running before MCP server starts; auto-start on login recommended |

---

## 3. Docker Setup

### 3.1 Pull the Qdrant image

```powershell
docker pull qdrant/qdrant
```

### 3.2 Create a named volume (required on Windows)

The official documentation notes that bind-mounting a local folder on Windows can cause path
translation issues. Use a named Docker volume instead:

```powershell
docker volume create qdrant_workspace_knowledge
```

### 3.3 Run the Qdrant container

```powershell
docker run -d --name qdrant-workspace `
    -p 6333:6333 -p 6334:6334 `
    -v qdrant_workspace_knowledge:/qdrant/storage `
    qdrant/qdrant
```

- `-d` — detached (background)
- `--name qdrant-workspace` — addressable by name for start/stop
- `-p 6333:6333` — REST API + web dashboard (`http://localhost:6333/dashboard`)
- `-p 6334:6334` — gRPC API
- `-v qdrant_workspace_knowledge:/qdrant/storage` — named volume for persistence

### 3.4 Start/stop the container

```powershell
docker start qdrant-workspace   # start existing container
docker stop qdrant-workspace    # graceful stop
```

Configure Docker Desktop → **Settings → General → Start Docker Desktop when you sign in** so
the container is available before the MCP server initialises.

### 3.5 Verify Docker is running before MCP server start

```powershell
# Quick health check — should return {"title":"qdrant","version":"..."}
Invoke-WebRequest -Uri "http://localhost:6333" -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

## 4. Dependency Changes

### 4.1 Add to `pyproject.toml`

In `.claude/mcp-servers/workspace-knowledge/pyproject.toml`, add to `[project.dependencies]`:

```toml
"qdrant-client>=1.7.0",
```

Qdrant v1.7.0 is the minimum required for hybrid search (dense + sparse vector support). Using
`>=1.7.0` rather than a pinned version allows minor-version updates.

### 4.2 Install into existing `.venv`

```powershell
Set-Location ".claude\mcp-servers\workspace-knowledge"
.\.venv\Scripts\python.exe -m pip install "qdrant-client>=1.7.0"
```

Or via `uv` (if used):

```powershell
uv pip install "qdrant-client>=1.7.0" --python .venv\Scripts\python.exe
```

### 4.3 Verify installation

```powershell
.\.venv\Scripts\python.exe -c "import qdrant_client; print(qdrant_client.__version__)"
# Expected: 1.7.x or higher
```

---

## 5. Storage Path

Qdrant data is stored in the Docker named volume `qdrant_workspace_knowledge`, not on the local
filesystem. The workspace directory only holds FAISS artifacts:

```
.claude/mcp-servers/workspace-knowledge/
└── embedding/
    ├── faiss.index           ← FAISS index (retained through Phase 2)
    ├── index_state.json      ← FAISS mtime state (retained through Phase 2)
    └── model/                ← sentence-transformers all-mpnet-base-v2

Docker named volume: qdrant_workspace_knowledge
  └── /qdrant/storage/        ← Managed by Docker; not visible in repo tree
      └── collection/
          └── workspace_knowledge/
```

No `qdrant_storage/` directory exists in the local filesystem. The `.gitignore` entry for it
is no longer needed. Updated `.gitignore`:

```gitignore
# .claude/mcp-servers/workspace-knowledge/.gitignore
.venv/
embedding/faiss.index
embedding/index_state.json
```

---

## 6. `SEARCH_BACKEND` Flag Design

The backend is controlled by an environment variable read at server startup. This allows
switching backends without modifying code and supports the rollback procedure.

### 6.1 Environment variable

```
SEARCH_BACKEND=faiss    # (default) Use FAISS + BM25 hybrid
SEARCH_BACKEND=qdrant   # Use Qdrant + BM25 hybrid
```

### 6.2 Reading the flag in `server.py`

Add near the top of `server.py` (after existing imports):

```python
import os
SEARCH_BACKEND = os.getenv("SEARCH_BACKEND", "faiss").lower()
```

### 6.3 Setting the flag

**Per-session (PowerShell):**

```powershell
$env:SEARCH_BACKEND = "qdrant"
# Then restart Claude Code to restart the MCP server
```

**Persistent (MCP server config in `.mcp.json`):**

```json
{
  "mcpServers": {
    "workspace-knowledge": {
      "command": "...",
      "env": {
        "SEARCH_BACKEND": "qdrant",
        "WORKSPACE_ROOT": "..."
      }
    }
  }
}
```

The `.mcp.json` approach is preferred for Phase 2+ as it persists across sessions without
manual PowerShell commands.

---

## 7. `server.py` Architectural Changes

### 7.1 `SearchEngine` refactor outline

The existing `SearchEngine` class gains a Qdrant backend tier alongside the FAISS tier. The
three-tier degradation chain becomes:

```
HYBRID_QDRANT → BM25 → RAWFS   (when SEARCH_BACKEND=qdrant)
HYBRID_FAISS  → BM25 → RAWFS   (when SEARCH_BACKEND=faiss, current behaviour)
```

**New attributes on `SearchEngine`:**

```python
self._qdrant_client = None      # qdrant_client.QdrantClient instance
self._collection_name = "workspace_knowledge"
self._qdrant_ready = False      # True once collection is seeded
```

**New methods:**

```python
def _init_qdrant(self):
    """Connect to the local Qdrant Docker server and seed collection if needed.
    Falls back gracefully if Docker is not running — sets _qdrant_ready=False
    so the engine degrades to BM25 rather than crashing."""
    from qdrant_client import QdrantClient
    try:
        self._qdrant_client = QdrantClient(url="http://localhost:6333")
        self._ensure_collection()
        self._seed_if_empty()
        self._qdrant_ready = True
    except Exception as exc:
        self._qdrant_ready = False
        self._degradation_reason = (
            f"Qdrant Docker unreachable — falling back to FAISS: {exc}"
        )

def _ensure_collection(self):
    """Create collection if it does not exist."""
    from qdrant_client.models import Distance, VectorParams
    existing = [c.name for c in self._qdrant_client.get_collections().collections]
    if self._collection_name not in existing:
        self._qdrant_client.create_collection(
            collection_name=self._collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

def _search_qdrant(self, query: str, top_k: int) -> list[dict]:
    """Dense vector search via Qdrant."""
    import numpy as np
    q_emb = self._model.encode([query])
    q_emb = (q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True))[0].tolist()
    results = self._qdrant_client.search(
        collection_name=self._collection_name,
        query_vector=q_emb,
        limit=top_k * 3,
        with_payload=True,
    )
    seen = set()
    out = []
    for r in results:
        p = r.payload
        if p["rel_path"] not in seen:
            seen.add(p["rel_path"])
            out.append({
                "file": p["rel_path"],
                "section": p.get("section", ""),
                "score": r.score,
                "snippet": p.get("text", "")[:400],
            })
        if len(out) >= top_k:
            break
    return out
```

### 7.2 `upsert_document` MCP tool (new, required Phase 1+)

```python
@mcp.tool()
def upsert_document(file_path: str) -> dict:
    """Re-chunk, re-embed, and upsert a single document into the Qdrant collection.
    Use after editing an indexed workspace .md file to update only that file's vectors
    without triggering a full collection rebuild."""
    ...
```

Full implementation specified in `03-initialization-guide.md` §3.

---

## 8. MCP Server Restart Procedure

Claude Code manages the MCP server lifecycle. To apply config changes or switch backends:

1. Ensure the Qdrant Docker container is running: `docker start qdrant-workspace`
2. Exit the current Claude Code session (or use `/exit`)
3. Update `.mcp.json` with the new `SEARCH_BACKEND` env value if needed
4. Restart Claude Code — the MCP server restarts automatically on next session start
5. Verify the backend via any `search_docs` call — the `_meta` block reports `search_tier`

**If the MCP server started before Docker was running:** `_init_qdrant` will have set
`_qdrant_ready=False` and degraded to FAISS. Start Docker, then restart the MCP server:

```powershell
# Start Docker container
docker start qdrant-workspace

# Restart the MCP server process
Get-Process -Name "python" | Where-Object {
    $_.MainWindowTitle -eq "" -and $_.CommandLine -match "server.py"
} | Stop-Process -Force
# Claude Code will restart it automatically within seconds
```

**Rollback to FAISS (emergency):**

```powershell
$env:SEARCH_BACKEND = "faiss"
# Restart Claude Code — FAISS index self-heals from corpus via mtime detection
```

---

## 9. Verification Checklist

After completing deployment setup, verify:

- [ ] Docker Desktop installed and running on Windows 11
- [ ] `docker start qdrant-workspace` succeeds; container status is `Up`
- [ ] `http://localhost:6333/dashboard` loads in browser (Qdrant web dashboard)
- [ ] `qdrant-client>=1.7.0` installed in `.venv`
- [ ] `SEARCH_BACKEND=qdrant` accepted without error (no import failures)
- [ ] `_init_qdrant()` connects successfully (no `_qdrant_ready=False` in logs)
- [ ] `workspace_knowledge` collection exists in Qdrant (see `03-initialization-guide.md`)
- [ ] `search_docs("pipeline")` returns results with `search_tier: "hybrid_qdrant"` in `_meta`
- [ ] `SEARCH_BACKEND=faiss` rollback works — restores FAISS results within one restart
- [ ] All 10 existing MCP tools return non-error responses
