# MCP Server Setup — workspace-knowledge Lightweight RAG

> **Core Component 00 — Retrieval Augmented Generation Module**
> **Scope:** Operational setup guide for the `workspace-knowledge` MCP server (lightweight RAG
> retrieval component).
> **Audience:** Engineers initializing or re-initializing the retrieval component in a new
> environment.
> **Laboratory Director:** Dr. Elias Vance
> **Last Updated:** 2026-06-27

---

## Prerequisites

| Requirement             | Minimum Version  | Notes                                                             |
| ----------------------- | ---------------- | ----------------------------------------------------------------- |
| Docker Desktop          | Any current      | WSL2 backend required on Windows 11; must start before MCP server |
| Python                  | 3.11             | Managed by the MCP server's `.venv`                               |
| `qdrant-client`         | ≥ 1.7.0, < 2.0.0 | Installed into `.venv` (see §3)                                   |
| `sentence-transformers` | Any current      | `all-mpnet-base-v2` embedding model loaded at server startup      |

Enable WSL2 before installing Docker Desktop. Configure Docker Desktop → **Settings → General →
Start Docker Desktop when you sign in** so the container is available before the MCP server
initialises.

---

## 1. Start the Qdrant Docker Container

### 1.1 First-time setup

```powershell
# Pull the Qdrant image
docker pull qdrant/qdrant

# Create a named volume for persistent storage
# (named volumes avoid Windows path-translation issues with bind mounts)
docker volume create qdrant_workspace_knowledge

# Start the container
docker run -d `
  --name qdrant-workspace `
  -p 6333:6333 -p 6334:6334 `
  -v qdrant_workspace_knowledge:/qdrant/storage `
  qdrant/qdrant
```

Ports: `6333` = REST API + web dashboard; `6334` = gRPC API.

### 1.2 Subsequent starts

```powershell
docker start qdrant-workspace   # start existing container
docker stop qdrant-workspace    # graceful stop
```

### 1.3 Verify the container is running

```powershell
# Should return {"title":"qdrant","version":"..."}
Invoke-WebRequest -Uri "http://localhost:6333" -UseBasicParsing |
  Select-Object -ExpandProperty Content
```

The Qdrant web dashboard is available at `http://localhost:6333/dashboard`.

---

## 2. Configure the MCP Server

### 2.1 Set the active backend in `.mcp.json`

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

`SEARCH_BACKEND=qdrant` switches the server to the Qdrant primary tier. The FAISS and BM25 tiers
remain active as fallbacks — they do not need to be disabled.

### 2.2 Restart the MCP server

```powershell
# 1. Ensure Qdrant container is running
docker start qdrant-workspace

# 2. End the current agent runtime session
# 3. Start a new session — the MCP server starts automatically
```

**If the MCP server started before Docker was running:** `_init_qdrant` degrades to FAISS. Start
Docker and restart the MCP server process:

```powershell
docker start qdrant-workspace

# Stop the Python server process — the agent runtime restarts it within seconds
Get-Process -Name "python" | Where-Object {
    $_.MainWindowTitle -eq "" -and $_.CommandLine -match "server.py"
} | Stop-Process -Force
```

---

## 3. Install `qdrant-client`

```powershell
# Navigate to the MCP server directory
Set-Location "core-component-00\mcp-servers\workspace-knowledge"

# Install into the existing virtual environment
.\.venv\Scripts\python.exe -m pip install "qdrant-client>=1.7.0,<2.0.0"

# Verify
.\.venv\Scripts\python.exe -c "import qdrant_client; print(qdrant_client.__version__)"
# Expected: 1.7.x – 1.x.x (must be < 2.0.0)
```

Add to `pyproject.toml` under `[project.dependencies]`:

```toml
"qdrant-client>=1.7.0,<2.0.0",
```

---

## 4. Collection Schema Reference

The MCP server creates the `workspace_knowledge` collection automatically on first startup if it
does not exist.

| Parameter       | Value                 | Notes                                                |
| --------------- | --------------------- | ---------------------------------------------------- |
| Collection name | `workspace_knowledge` | Fixed; matches `server.py` `_collection_name`        |
| Dimensions      | `768`                 | `all-mpnet-base-v2` output dimension                 |
| Distance metric | `Cosine`              | Equivalent to FAISS `IndexFlatIP` + L2 normalization |
| On-disk vectors | `false`               | Vectors in memory; payload on disk                   |

**Payload fields per point:**

| Field       | Type      | Description                                                     |
| ----------- | --------- | --------------------------------------------------------------- |
| `rel_path`  | `string`  | Relative path from workspace root                               |
| `section`   | `string`  | Section heading at time of chunking                             |
| `chunk_idx` | `integer` | Zero-based chunk index within the file                          |
| `text`      | `string`  | Full chunk text (up to 512 words)                               |
| `file_path` | `string`  | Absolute filesystem path (for `retrieve_context` compatibility) |

---

## 5. Initial Seeding

The server seeds the collection automatically on first startup via `_seed_if_empty()`:

- **0 points in collection** → full corpus seed (all indexed `.md` files, all four KEY_DIRS)
- **Points present** → seed skipped; server uses existing collection

Seeding time scales with corpus size. At ~7,800 chunks (current workspace scale) seeding
completes in 2–5 minutes. Monitor progress via server logs.

After seeding, verify with any `search_docs` call — the `_meta` block should report
`"search_tier": "HYBRID_QDRANT"`.

---

## 6. Smoke Tests

Run these checks immediately after first seeding. All must pass before the setup is considered
complete.

### Test 1 — Point count parity

```python
from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6333")
info = client.get_collection("workspace_knowledge")
print(f"Points: {info.points_count}")
# Compare against bm25_chunks count from health_check MCP tool
```

Or via `health_check` MCP tool: verify `parity_ok: true`.

### Test 2 — Known-document retrieval

```python
results = engine._search_qdrant("pipeline stage user approval", top_k=5)
assert any("pipeline" in r["file"] for r in results), \
    "Pipeline document not surfaced by known query"
```

Or via `search_docs("pipeline stage user approval")` — verify a pipeline document appears in
results.

### Test 3 — Upsert idempotency

Call `upsert_document` on any indexed file, then re-run `health_check`. Point count must be
unchanged (upsert deletes old points for the file and inserts new ones; total count stays stable
when chunk count is unchanged).

### Test 4 — Rollback verification

```powershell
# Step 1: Set SEARCH_BACKEND to "faiss" in .mcp.json (edit the env block directly)
# Step 2: Update the state file so the hook also routes to the FAISS path
$stateFile = "core-component-00\mcp-servers\workspace-knowledge\rag-system\rag-sync-state.json"
$state = Get-Content $stateFile | ConvertFrom-Json
$state.search_backend   = "faiss"
$state.debounce_seconds = 30
$state | ConvertTo-Json -Compress | Set-Content $stateFile
# Step 3: Start a new session — MCP server reads SEARCH_BACKEND from .mcp.json at startup
# Verify: search_docs returns FAISS results (_meta.search_tier = "HYBRID")
```

> **Note:** Do not use `$env:SEARCH_BACKEND = "faiss"` in the shell. That variable is
> process-scoped and is not inherited by the MCP server subprocess, which reads its environment
> from `.mcp.json`. The state file and `.mcp.json` must both be updated.

---

## 7. Volume Backup and Restore

The Qdrant collection is stored in the Docker named volume `qdrant_workspace_knowledge`. Because
the markdown corpus is the canonical source of truth, a lost volume is always recoverable via
`rebuild_index` (2–5 min). Snapshots are still recommended before major operations.

**Backup** (creates `qdrant-backup.tar.gz` in the current directory):

```powershell
docker run --rm `
    -v qdrant_workspace_knowledge:/data `
    -v "${PWD}:/backup" `
    alpine tar czf /backup/qdrant-backup.tar.gz /data
```

**Restore** (overwrites the volume with the archive):

```powershell
docker run --rm `
    -v qdrant_workspace_knowledge:/data `
    -v "${PWD}:/backup" `
    alpine tar xzf /backup/qdrant-backup.tar.gz -C /
```

Store the archive outside the repository — it is a large binary and must not be committed to
version control.

**When to back up:** before any bulk reseed operation; before switching `SEARCH_BACKEND`.

---

## 8. Rollback to FAISS

```powershell
# Emergency rollback — revert to FAISS primary tier

# Step 1: Set SEARCH_BACKEND to "faiss" in .mcp.json (edit the env block directly)

# Step 2: Update the state file — both the MCP server and the hook must agree on the backend
$stateFile = "core-component-00\mcp-servers\workspace-knowledge\rag-system\rag-sync-state.json"
$state = Get-Content $stateFile | ConvertFrom-Json
$state.search_backend   = "faiss"
$state.debounce_seconds = 30        # recalibrate for full-rebuild latency
$state | ConvertTo-Json -Compress | Set-Content $stateFile

# Step 3: Start a new session — MCP server reads SEARCH_BACKEND from .mcp.json at startup
# FAISS index self-heals from corpus via mtime detection
```

> **Warning:** Do not use `$env:SEARCH_BACKEND = "faiss"` as a rollback mechanism. That
> variable is scoped to the current shell process and is not inherited by the MCP server
> subprocess. The MCP server reads its environment exclusively from `.mcp.json` at startup.
> Omitting the `.mcp.json` update leaves the server on Qdrant despite the shell variable.

FAISS retains its index on disk and rebuilds only the stale entries on restart (mtime-based
detection). Rollback is available within one MCP server restart cycle.

---

## 9. Setup Verification Checklist

- [ ] Docker Desktop installed and running on Windows 11 (WSL2 backend)
- [ ] `docker start qdrant-workspace` succeeds; container status is `Up`
- [ ] `http://localhost:6333/dashboard` loads in browser
- [ ] `qdrant-client>=1.7.0` installed in `.venv`
- [ ] `SEARCH_BACKEND=qdrant` set in `.mcp.json`
- [ ] MCP server restarted; no `_qdrant_ready=False` in logs
- [ ] `health_check` MCP tool returns `parity_ok: true`
- [ ] `search_docs("pipeline")` returns `search_tier: "HYBRID_QDRANT"` in `_meta`
- [ ] Rollback to FAISS verified (restores within one restart cycle)

---

## References

| Resource                     | Location                                                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Hook Configuration**       | `core-component-00/retrieval-augmented-generation/deployment/lightweight/guides/hook-configuration.md`       |
| **State File Schema**        | `core-component-00/retrieval-augmented-generation/deployment/lightweight/reference/rag-sync-state-schema.md` |
| **Lightweight RAG Overview** | `core-component-00/retrieval-augmented-generation/deployment/lightweight-rag-deployment.md`                  |
| **Evaluation Reference**     | `core-component-00/retrieval-augmented-generation/evaluation/reference-table.md`                             |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Contact:** Via workspace agent activation protocol (AGENTS.md § 2.3)
