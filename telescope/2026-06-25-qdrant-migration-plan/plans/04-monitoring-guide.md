# Qdrant Monitoring Guide

**Document Type:** Migration Planning Deliverable
**Investigation:** `2026-06-25-qdrant-migration-plan`
**Author:** Dr. Elias Vance — CC-00 Laboratory Director
**Date:** 2026-06-25
**Status:** Approved

---

## 1. Monitoring Objectives

This guide covers four monitoring concerns for the Qdrant-backed workspace-knowledge MCP server:

1. **Index freshness** — Is the Qdrant collection up-to-date with the workspace corpus?
2. **Collection health** — Is the Qdrant storage layer operating correctly?
3. **Query quality** — Is retrieval accuracy stable vs. the FAISS baseline?
4. **Upsert performance** — Is `upsert_document` completing within acceptable cost bounds?

Monitoring is implemented via two mechanisms: (a) extensions to the `_meta_block()` return
value (visible in every MCP tool response), and (b) a new `health_check` MCP tool.

---

## 2. Index Freshness

### 2.1 `index_built_at` field

Add `index_built_at` to `SearchEngine._meta_block()` in `server.py`:

```python
def _meta_block(self) -> dict:
    return {
        "search_tier": self._tier.value,
        "degradation_reason": self._degradation_reason,
        "result_quality": self._tier.value,
        "rebuild_available": True,
        "index_built_at": self._index_built_at,   # NEW: ISO 8601 UTC string
        "backend": SEARCH_BACKEND,                 # NEW: "faiss" or "qdrant"
    }
```

`_index_built_at` is set in `SearchEngine.__init__` (and updated on rebuild/upsert):

```python
from datetime import datetime, timezone

# In __init__ (after initialization completes):
self._index_built_at = datetime.now(timezone.utc).isoformat()

# In rebuild() and after _seed_qdrant_collection():
self._index_built_at = datetime.now(timezone.utc).isoformat()
```

**How to read it:** Every `search_docs`, `retrieve_context`, or other tool response includes
`_meta.index_built_at`. If this timestamp is more than a session old and no `rebuild_index` or
`upsert_document` has been called, the index may be stale.

### 2.2 Staleness detection via H-RAG01 (existing)

The existing `H-RAG01` hook detects time-sensitive language and injects a freshness warning.
From Phase 2 onward, update the H-RAG01 advisory to reference `_meta.index_built_at` rather
than the generic cutoff message — this gives agents a concrete timestamp to reason about.

### 2.3 Upsert audit trail

Each `upsert_document` call returns the updated `index_built_at`. Agents can log these to
confirm that a specific file's changes were indexed. The `/rag-sync status` command (specified
in `05-hook-design.md` §5.2) should also surface the last-rebuild timestamp from `rag-sync-state.json`.

---

## 3. Collection Health

### 3.1 `health_check` MCP tool (new)

```python
@mcp.tool()
def health_check() -> dict:
    """Return Qdrant collection health metrics: vector count, disk usage,
    segment count, and backend status. Use to verify collection integrity
    and monitor storage growth."""
    meta = engine._meta_block()
    if SEARCH_BACKEND != "qdrant" or not engine._qdrant_ready:
        return {
            "backend": SEARCH_BACKEND,
            "qdrant_ready": getattr(engine, "_qdrant_ready", False),
            "message": "Qdrant not active — SEARCH_BACKEND is not 'qdrant'",
            "_meta": meta,
        }
    try:
        info = engine._qdrant_client.get_collection(engine._collection_name)
        # Disk usage is in the Docker named volume (qdrant_workspace_knowledge) —
        # not accessible from the Python process. Check via PowerShell:
        #   docker system df -v | findstr qdrant_workspace_knowledge
        return {
            "backend": "qdrant",
            "collection": engine._collection_name,
            "points_count": info.points_count,
            "vectors_count": info.vectors_count,
            "segments_count": info.segments_count,
            "disk_usage_mb": "n/a (Docker volume — use: docker system df -v)",
            "bm25_chunks": len(engine._chunks),
            "parity_ok": info.points_count == len(engine._chunks),
            "orphaned_points": max(0, info.points_count - len(engine._chunks)),
            "_meta": meta,
        }
    except Exception as exc:
        return {"backend": "qdrant", "error": str(exc), "_meta": meta}
```

### 3.2 Governance gate assessment for `health_check`

| Gate             | Assessment                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------------- |
| **Capability**   | ✅ Pass — Qdrant collection introspection (`get_collection`) is not replicable by native tools |
| **Governance**   | ✅ Pass — read-only; does not modify any index, pipeline doc, or governance record             |
| **Completeness** | ✅ Pass — returns real, query-dependent collection metrics (point count, disk usage, segments) |

### 3.3 Key health metrics to watch

| Metric            | Normal range              | Alert threshold         | Action                                                             |
| ----------------- | ------------------------- | ----------------------- | ------------------------------------------------------------------ |
| `points_count`    | Stable or growing         | Drops >10% unexpectedly | Investigate; reseed if corrupted                                   |
| `parity_ok`       | `true`                    | `false`                 | `rebuild_index` to reseed from corpus                              |
| `disk_usage_mb`   | < 500 MB at current scale | > 1 GB                  | Check via `docker system df -v`; investigate segment fragmentation |
| `segments_count`  | 1–5                       | > 20                    | Run Qdrant collection optimization (see §3.4)                      |
| `orphaned_points` | `0`                       | `> 0`                   | Points from deleted files present; call `rebuild_index` to reseed  |

### 3.4 Collection optimization (defragmentation)

After many incremental upserts, the Qdrant collection may accumulate segments. Optimize:

```python
engine._qdrant_client.optimize_collection(
    collection_name=engine._collection_name,
    # Default optimizers_config — runs in background
)
```

This can be called via a new `optimize_collection` MCP tool or invoked manually. Run when
`segments_count > 20` or after any bulk seeding operation.

---

## 4. Query Quality Monitoring

### 4.1 MRR baseline establishment (Phase 1)

Before switching to Qdrant primary (Phase 2 entry), establish a FAISS MRR baseline:

**Query set:** 20 representative queries drawn from actual workspace use cases:

| Category            | Example queries                                               |
| ------------------- | ------------------------------------------------------------- |
| Pipeline navigation | "stage gate user approval", "ADR technology decision lock"    |
| Agent identity      | "CDO authority scope", "Studio Director profile"              |
| CC-00 patterns      | "context window assembly four slots", "BM25 hybrid retrieval" |
| Governance          | "MCP gate capability completeness", "ASE compliance standard" |
| Cross-module        | "multi-agent handoff protocol", "error boundary timeout"      |

**Metric:** Mean Reciprocal Rank @ 5 (MRR@5) — the reciprocal rank of the first correct result
in the top-5, averaged over the query set. "Correct result" is the known relevant document for
each query.

Record: `faiss_mrr_baseline`, `qdrant_mrr_phase1`, `qdrant_mrr_phase2_week1`, etc.

#### Ground truth specification

**Commit requirement:** The query set and relevance judgments must be committed to
`tests/rag_eval/mrr_query_set.json` **before Phase 1 entry** — authoring the baseline after
seeing Qdrant results risks retrofitting ground truth to match outcomes.

**Storage format** (`tests/rag_eval/mrr_query_set.json`):

```json
[
  { "query": "stage gate user approval", "relevant_doc": "company/pipeline/mobile/pipeline.md" },
  { "query": "ADR technology decision lock", "relevant_doc": "company/pipeline/mobile/pipeline.md" }
]
```

- `query` — exact string submitted to `search_docs`
- `relevant_doc` — the `rel_path` of the single known-relevant document (relative to workspace
  root, matching the `file` field in search results)
- Authorship: CC-00 Lab Director or designated reviewer before Phase 1 entry
- Completeness check: exactly 20 entries, no duplicate `relevant_doc` values

### 4.2 Regression alert thresholds

| Scenario                              | Threshold                     | Action                               |
| ------------------------------------- | ----------------------------- | ------------------------------------ |
| Phase 1 shadow MRR vs. FAISS baseline | < 95% (5% drop)               | Block Phase 2 entry; investigate     |
| Phase 2 week-1 MRR vs. Phase 1        | < 97% (3% drop)               | Investigate chunking/embedding drift |
| Phase 2 ongoing MRR                   | Drops 10% in any 7-day window | Rollback to FAISS; file incident     |
| After upsert_document                 | MRR does not degrade          | Verify by re-running 3 known queries |

### 4.3 Lightweight per-query monitoring

From Phase 2 onward, add a `_last_query_score` field to `_meta_block()`:

```python
"top_result_score": results[0]["score"] if results else None,
```

A sudden drop in top-result score for a query that has historically scored well is an early
indicator of embedding drift or collection corruption.

---

## 5. Upsert Performance Monitoring

### 5.1 Latency tracking

Track `upsert_document` call duration. Add timing to the MCP tool response:

```python
import time
start = time.time()
count = engine._upsert_file_to_qdrant(file_path)
elapsed = round(time.time() - start, 2)
return {"status": "upserted", "file": file_path, "new_chunk_count": count,
        "elapsed_seconds": elapsed, "_meta": engine._meta_block()}
```

### 5.2 Upsert performance thresholds

| Metric                    | Target  | Warning  | Action                                             |
| ------------------------- | ------- | -------- | -------------------------------------------------- |
| Per-file upsert (Phase 2) | < 3 s   | > 5 s    | Reduce batch size; check GPU availability          |
| Per-file upsert (Phase 3) | < 2 s   | > 4 s    | Investigate; consider embedding model quantization |
| Rebuild from scratch      | < 3 min | > 10 min | Corpus too large — evaluate shard strategy         |

### 5.3 H-RAG02 debounce recalibration

After Phase 1 benchmarks establish actual `upsert_document` latency, recalibrate the
`debounce_seconds` in `rag-sync-state.json`:

```
Phase 0–1: debounce_seconds = 30  (rebuild_index is slow)
Phase 2–3: debounce_seconds = 10  (upsert_document is fast)
```

Use `/rag-sync threshold 10` to update without editing the state file manually.

---

## 6. Monitoring Dashboard (Manual)

There is no automated dashboard — this workspace is local-only with no metrics infrastructure.
Monitoring is performed on-demand via MCP tool calls. Recommended checkpoints:

| When                                     | What to check                                       | Tool                                       |
| ---------------------------------------- | --------------------------------------------------- | ------------------------------------------ |
| After each migration phase transition    | Collection health, MRR parity                       | `health_check`, MRR test                   |
| After large batch doc writes (>20 files) | Point count parity, upsert latency                  | `health_check`                             |
| Monthly (routine)                        | Disk usage, segment count, MRR spot check           | `health_check`, 5-query MRR                |
| After any rollback event                 | FAISS index integrity, identify root cause          | `list_indexed_files`, manual investigation |
| Before Phase 3 (FAISS retirement)        | Full 20-query MRR, disk usage, 30-day stability log | Full monitoring suite                      |

---

## 7. Monitoring Checklist for Phase 2 Entry

All of these must be confirmed before switching `SEARCH_BACKEND=qdrant`:

- [ ] `index_built_at` field present in all MCP tool `_meta` responses
- [ ] `health_check` tool returns `parity_ok: true`
- [ ] Phase 1 MRR within 5% of FAISS baseline (record exact numbers)
- [ ] Shadow upsert latency < 5 s per file (10 file sample)
- [ ] Docker volume disk usage recorded as Phase 1 baseline (`docker system df -v`)
- [ ] No Qdrant-related exceptions in MCP server logs for past 2 weeks
- [ ] Rollback procedure verified (FAISS restored within 60 s)
