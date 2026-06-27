# Lightweight RAG Deployment — Retrieval Component for Agent Runtimes

> **Core Component 00 — Retrieval Augmented Generation Module**
> **Scope:** Retrieval-only RAG component — embedding, vector search, reranking, and graceful
> degradation. No local LLM, cache, or monitoring stack. Generation is handled by the host agent
> runtime.
> **Audience:** Engineers deploying a RAG retrieval component integrated into an agent runtime
> via MCP.
> **Laboratory Director:** Dr. Elias Vance
> **Last Updated:** 2026-06-27

---

## Overview

This guide covers deployment of a **lightweight RAG retrieval component** — the retrieval layer
of the full RAG pipeline, designed to integrate with an agent runtime that provides the
generation layer. The component handles document ingestion, embedding, vector search, and
reranking; it does not include a local LLM inference engine, Redis query cache, or
Prometheus/Grafana observability stack.

This is the architecture used by the `workspace-knowledge` MCP server: the agent runtime acts as
the generation layer; the MCP server delivers retrieved context on demand.

For the full self-contained RAG application (local LLM + retrieval + cache + observability), see
**[full-stack-rag-deployment.md](core-component-00/retrieval-augmented-generation/deployment/full-stack-rag-deployment.md)**.

---

## Architecture

```
Agent Runtime
    ↓  MCP tool call: search_docs / retrieve_context
Retrieval Component (workspace-knowledge MCP server)
    ↓
[Tier 1] Qdrant semantic search + BM25 keyword fusion   ← primary
    ↓ (fallback)
[Tier 2] FAISS semantic search + BM25 keyword fusion    ← hot standby
    ↓ (fallback)
[Tier 3] BM25 keyword-only search                       ← warm standby
    ↓ (fallback)
[Tier 4] Raw Corpus Scan — no index required            ← cold fallback
    ↓
Retrieved context chunks + _meta block (tier, backend, index_built_at)
    ↓
Agent Runtime (generation + response)
```

The four-tier degradation stack ensures availability even when the primary vector store is
unavailable. See `core-component-00/retrieval-augmented-generation/architecture/overview.md` §11 for the full
Graceful Degradation Stack Architecture specification.

---

## What This Component Does Not Include

| Layer                | Full-Stack System               | This Component                                    |
| -------------------- | ------------------------------- | ------------------------------------------------- |
| LLM inference engine | LM Studio / vLLM                | ❌ Not included — handled by host agent           |
| Query cache          | Redis (5-min TTL)               | ❌ Not included                                   |
| Monitoring stack     | Prometheus / Grafana            | ❌ Not included — `health_check` MCP tool instead |
| Reranking service    | bge-reranker-large (standalone) | ✅ Included (in-process)                          |
| Embedding service    | standalone service              | ✅ Included (in-process)                          |
| Vector store         | Qdrant Docker                   | ✅ Included                                       |
| Graceful degradation | N/A                             | ✅ Included — four-tier stack                     |

---

## Vector Database Deployment Mode Selection

> **This is an architecture decision with irreversible migration implications. Read before
> selecting a deployment mode.**

Qdrant exposes three distinct deployment modes. The mode selected at project inception determines
the cost of all future upgrades and is not trivially reversible.

| Mode                 | Client Instantiation                        | Persistence                 | Data Format           | Upgrade Path                                                           |
| -------------------- | ------------------------------------------- | --------------------------- | --------------------- | ---------------------------------------------------------------------- |
| **In-memory**        | `QdrantClient(":memory:")`                  | None — lost on process exit | N/A                   | Full reseed required on any upgrade                                    |
| **Embedded (local)** | `QdrantClient(path="./qdrant_storage")`     | Local filesystem            | Embedded-specific     | ❌ **Incompatible with server mode — full reseed required to upgrade** |
| **Docker / Server**  | `QdrantClient(url="http://localhost:6333")` | Docker named volume         | Production-compatible | ✅ Direct upgrade to managed cloud with no data loss                   |

### Critical Constraint: Embedded Mode Is a Deployment Dead End

The embedded mode data format is **not compatible** with the Qdrant server binary (Docker or any
managed cloud offering). A collection seeded via `QdrantClient(path="...")` cannot be read by a
`QdrantClient(url="...")` instance. Any upgrade from embedded to Docker requires:

1. Stopping all writes to the embedded collection
2. Running the full corpus seeding procedure against the new Docker instance from scratch
3. Validating collection parity (point count, spot-check MRR) before resuming reads

At small corpus sizes this cost appears negligible, but it scales linearly with corpus size. At
\> 5,000 chunks the reseed time becomes operationally significant, and the risk of introducing
quality regressions during an unplanned reseed is non-trivial.

**Select Docker standalone server mode from the start of any project, even for local single-node
deployments.** The marginal resource overhead of Docker Desktop (< 1 GB RAM, < 500 MB disk for
the Qdrant image) is recovered immediately by eliminating the future reseed cost and by ensuring
data format compatibility with any future managed cloud migration.

### Recommended Deployment Command (Windows / PowerShell)

```powershell
# Start Qdrant container with a persistent named volume
docker run -d `
  --name qdrant-workspace `
  -p 6333:6333 -p 6334:6334 `
  -v qdrant_workspace_knowledge:/qdrant/storage `
  qdrant/qdrant
```

```python
# Python client — connect to the running container
from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6333")
```

**Dependency pinning:** Use `qdrant-client>=1.7.0,<2.0.0` in `pyproject.toml`. The `1.x` API
surface is stable; the `2.0.0` release may introduce breaking changes and must be validated
before upgrading.

### Windows 11 Note

Docker Desktop for Windows requires the WSL2 backend. Enable WSL2 before installing Docker
Desktop. The Qdrant Docker image (`qdrant/qdrant`) has been empirically verified stable on
Windows 11 (WSL2 backend) on the RTX 4060 / i9-13900H / 31.6 GB RAM hardware profile used in
this workspace: 7,793 indexed points were seeded and queried across Phases 1–3 of the 2026-06
`workspace-knowledge` migration with no Windows 11 compatibility issues. Larger corpora are
expected to behave equivalently given the absence of any Windows 11-specific Qdrant constraints.

---

## Index Freshness and Sync

This component relies on a post-write hook (H-RAG02) to detect document writes and dispatch the
appropriate index-update tool. The hook reads a shared state file to determine the active backend
and debounce threshold.

See `core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md` for the full
Phase-Adaptive Index Sync Hook pattern, including state file contract, tool dispatch table,
debounce calibration, and operator control interface.

---

## Observability

This component does not use Prometheus or Grafana. Observability is provided by the `health_check`
MCP tool, which returns:

| Field             | Description                                                             |
| ----------------- | ----------------------------------------------------------------------- |
| `search_tier`     | Active retrieval tier (HYBRID_QDRANT / HYBRID / BM25 / Raw Corpus Scan) |
| `backend`         | Active backend identifier (`qdrant` / `faiss`)                          |
| `index_built_at`  | ISO 8601 UTC timestamp of last index build or upsert                    |
| `parity_ok`       | Whether vector store point count matches corpus chunk count             |
| `orphaned_points` | Count of points in the vector store with no corpus source               |

Call `health_check` after any document deletion, bulk restructuring, or upsert volume exceeding
20 files in a single session. See
`core-component-00/retrieval-augmented-generation/evaluation/reference-table.md`
§Orphaned Point Detection for remediation procedures.

---

## Performance Targets

| Metric                       | Target | Measurement                       |
| ---------------------------- | ------ | --------------------------------- |
| **Query Latency (p95)**      | <600ms | MCP tool round-trip timing        |
| **Retrieval Accuracy (MRR)** | ≥0.75  | Golden dataset evaluation         |
| **Index Freshness**          | ≤15s   | debounce_seconds + upsert_latency |
| **Parity Check**             | Pass   | `health_check` after bulk writes  |

---

## Relation to the Full-Stack Architecture

This component is the **retrieval layer** of the full-stack RAG architecture described in
`full-stack-rag-deployment.md`. The two systems share the same retrieval engineering principles
documented across this module:

| Principle                             | Reference                                                                                                             |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Corpus-as-Source-of-Truth             | `core-component-00/retrieval-augmented-generation/architecture/overview.md` §10                                       |
| Graceful Degradation Stack            | `core-component-00/retrieval-augmented-generation/architecture/overview.md` §11                                       |
| Index Sync Hook pattern               | `core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md`                                       |
| Incremental Upsert decision framework | `core-component-00/retrieval-augmented-generation/evaluation/reference-table.md` §Incremental Upsert vs. Full-Rebuild |
| MRR Baseline protocol                 | `core-component-00/retrieval-augmented-generation/evaluation/reference-table.md` §MRR Baseline Establishment          |

---

## References

| Resource                             | Location                                                                                   |
| ------------------------------------ | ------------------------------------------------------------------------------------------ |
| **CC-00 RAG Architecture**           | `core-component-00/retrieval-augmented-generation/architecture/overview.md`                |
| **Index Sync Hook Pattern**          | `core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md`            |
| **Evaluation Reference**             | `core-component-00/retrieval-augmented-generation/evaluation/reference-table.md`           |
| **Full-Stack RAG Deployment**        | `core-component-00/retrieval-augmented-generation/deployment/full-stack-rag-deployment.md` |
| **Qdrant Migration Research Report** | `telescope/2026-06-25-qdrant-migration-plan/research-report.md`                            |
| **Qdrant Documentation**             | https://qdrant.tech/documentation/                                                         |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Contact:** Via workspace agent activation protocol (AGENTS.md § 2.3)
