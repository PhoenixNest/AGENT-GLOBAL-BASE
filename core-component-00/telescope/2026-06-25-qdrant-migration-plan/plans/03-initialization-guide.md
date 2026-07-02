# Qdrant Initialization Guide

**Document Type:** Migration Planning Deliverable
**Investigation:** `2026-06-25-qdrant-migration-plan`
**Author:** Dr. Elias Vance — CC-00 Laboratory Director
**Date:** 2026-06-25
**Status:** Approved

---

## 1. Collection Schema

### 1.1 Collection name

```
workspace_knowledge
```

### 1.2 Vector configuration

| Parameter           | Value             | Rationale                                                                        |
| ------------------- | ----------------- | -------------------------------------------------------------------------------- |
| **Dimensions**      | `768`             | `all-mpnet-base-v2` output dimension                                             |
| **Distance metric** | `Cosine`          | Matches existing FAISS `IndexFlatIP` + L2 normalization; semantically equivalent |
| **On-disk**         | `false` (default) | Vectors kept in memory for fast query; payload stored on disk                    |

### 1.3 Payload schema

Each Qdrant point stores the following payload fields (mirroring the existing chunk dict in
`server.py`):

| Field       | Type      | Description                                                                           |
| ----------- | --------- | ------------------------------------------------------------------------------------- |
| `rel_path`  | `string`  | Relative path from workspace root (e.g., `company/pipeline/web/pipeline.md`)          |
| `section`   | `string`  | Section heading at the time of chunking (from `current_section` in `_extract_chunks`) |
| `chunk_idx` | `integer` | Zero-based chunk index within the file                                                |
| `text`      | `string`  | Full chunk text (up to 512 words)                                                     |
| `file_path` | `string`  | Absolute filesystem path (for `retrieve_context` compatibility)                       |

### 1.4 Point ID design

Each point requires a **stable, deterministic integer ID** to support idempotent upserts
(re-indexing the same file produces the same point IDs — no duplicates).

```python
def _chunk_point_id(rel_path: str, chunk_idx: int) -> int:
    """Deterministic integer ID: abs(hash) truncated to 63 bits for Qdrant compatibility."""
    import hashlib
    key = f"{rel_path}:{chunk_idx}"
    digest = hashlib.md5(key.encode()).hexdigest()
    return int(digest[:15], 16)  # 15 hex chars = 60 bits, safely within int64 range
```

Using MD5 prefix (not for security — purely for deterministic numeric ID generation). The 60-bit
range avoids signed integer overflow on all platforms.

---

## 2. Initial Seeding Procedure

### 2.1 Overview

Seeding populates the Qdrant collection from the existing workspace corpus using the same
chunking logic already in `_extract_chunks` and the same embedding model (`all-mpnet-base-v2`).
The seed script reuses the `SearchEngine._chunks` list (already built by BM25 init) so no
redundant file scanning occurs.

### 2.2 Seeding function (add to `server.py`)

```python
def _seed_qdrant_collection(self):
    """Seed Qdrant collection from existing BM25 chunks.
    Safe to call multiple times — upsert is idempotent by point ID."""
    if not self._chunks:
        raise RuntimeError("BM25 chunks must be built before seeding Qdrant")

    from qdrant_client.models import PointStruct
    import numpy as np

    BATCH_SIZE = 100
    texts = [c["text"][:512] for c in self._chunks]

    # Encode in one pass (reuses loaded model)
    embeddings = self._model.encode(texts, show_progress_bar=False, batch_size=64)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Upsert in batches
    for i in range(0, len(self._chunks), BATCH_SIZE):
        batch_chunks = self._chunks[i:i + BATCH_SIZE]
        batch_embs = embeddings[i:i + BATCH_SIZE]
        points = [
            PointStruct(
                id=_chunk_point_id(c["rel_path"], c["chunk_idx"]),
                vector=emb.astype(float).tolist(),
                payload={
                    "rel_path": c["rel_path"],
                    "section": c["section"],
                    "chunk_idx": c["chunk_idx"],
                    "text": c["text"],
                    "file_path": c["file_path"],
                },
            )
            for c, emb in zip(batch_chunks, batch_embs)
        ]
        self._qdrant_client.upsert(
            collection_name=self._collection_name,
            points=points,
        )
```

### 2.3 When seeding is triggered

| Scenario                                       | Action                                          |
| ---------------------------------------------- | ----------------------------------------------- |
| First-ever startup with Qdrant enabled         | `_seed_if_empty()` detects 0 points → full seed |
| MCP server restart (collection already seeded) | `_seed_if_empty()` detects points > 0 → skip    |
| Manual `rebuild_index` call                    | Clears and re-seeds from scratch                |
| `upsert_document(file_path)` call              | Updates only the specified file's chunks        |

```python
def _seed_if_empty(self):
    """Seed the collection only if it has zero points."""
    info = self._qdrant_client.get_collection(self._collection_name)
    if info.points_count == 0:
        self._seed_qdrant_collection()
```

---

## 3. `upsert_document` — Incremental Update

This is the key capability that justifies the migration: updating a single file's chunks without
rebuilding the full collection.

### 3.1 Implementation

```python
def _upsert_file_to_qdrant(self, file_path_str: str):
    """Re-chunk, re-embed, and upsert one file's points into Qdrant.
    Deletes old points for this file first, then inserts new ones."""
    from pathlib import Path
    from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
    import numpy as np

    file_path = Path(file_path_str)
    new_chunks = self._extract_chunks(file_path)

    if not new_chunks:
        return 0  # File deleted or unreadable

    rel_path = new_chunks[0]["rel_path"]

    # Delete all existing points for this file
    self._qdrant_client.delete(
        collection_name=self._collection_name,
        points_selector=Filter(
            must=[FieldCondition(key="rel_path", match=MatchValue(value=rel_path))]
        ),
    )

    # Encode new chunks
    texts = [c["text"][:512] for c in new_chunks]
    embeddings = self._model.encode(texts, show_progress_bar=False, batch_size=64)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Upsert new points
    points = [
        PointStruct(
            id=_chunk_point_id(c["rel_path"], c["chunk_idx"]),
            vector=emb.astype(float).tolist(),
            payload={
                "rel_path": c["rel_path"],
                "section": c["section"],
                "chunk_idx": c["chunk_idx"],
                "text": c["text"],
                "file_path": c["file_path"],
            },
        )
        for c, emb in zip(new_chunks, embeddings)
    ]
    self._qdrant_client.upsert(collection_name=self._collection_name, points=points)

    # Update in-memory BM25 chunks for this file
    self._chunks = [c for c in self._chunks if c["rel_path"] != rel_path]
    self._chunks.extend(new_chunks)
    # Rebuild BM25 index with updated chunks
    from rank_bm25 import BM25Okapi
    tokenized = [c["text"].lower().split() for c in self._chunks]
    self._bm25 = BM25Okapi(tokenized)

    return len(new_chunks)
```

> **Performance note:** The `BM25Okapi` rebuild above is O(N) over total corpus chunk count. At
> Phase 1 scale (~5,000 chunks) this is negligible (<1 s). As the corpus approaches the secondary
> trigger threshold (~10,000 chunks), this cost must be explicitly benchmarked in Phase 1 alongside
> Qdrant upsert latency — since the Phase 2 debounce target (10 s per file) assumes BM25 rebuild
> time is negligible relative to the Qdrant upsert operation.

### 3.2 MCP tool wrapper

```python
@mcp.tool()
def upsert_document(file_path: str) -> dict:
    """Re-chunk, re-embed, and upsert a single document into the Qdrant collection.
    Also updates the BM25 index for this file. Use after editing an indexed .md file
    to reflect changes without a full collection rebuild."""
    if SEARCH_BACKEND != "qdrant":
        return {"status": "skipped", "reason": "SEARCH_BACKEND is not qdrant — use rebuild_index",
                "_meta": engine._meta_block()}
    if not engine._qdrant_ready:
        return {"status": "error", "reason": "Qdrant not initialized", "_meta": engine._meta_block()}
    try:
        count = engine._upsert_file_to_qdrant(file_path)
        return {"status": "upserted", "file": file_path, "new_chunk_count": count,
                "_meta": engine._meta_block()}
    except Exception as exc:
        return {"status": "error", "error": str(exc), "_meta": engine._meta_block()}
```

---

## 4. Smoke-Test Protocol

Run these checks immediately after first seeding. All must pass before Phase 1 entry.

### Test 1 — Point count integrity

```python
info = qdrant_client.get_collection("workspace_knowledge")
assert info.points_count == len(engine._chunks), \
    f"Point count mismatch: {info.points_count} vs {len(engine._chunks)} chunks"
```

### Test 2 — Known-document retrieval

Query a term known to appear in a specific document:

```python
results = engine._search_qdrant("pipeline stage user approval", top_k=5)
assert any("pipeline" in r["file"] for r in results), \
    "Pipeline document not surfaced by known query"
```

### Test 3 — Upsert idempotency

```python
# Re-seed a file and verify point count does not change
count_before = qdrant_client.get_collection("workspace_knowledge").points_count
engine._upsert_file_to_qdrant("company/pipeline/web/pipeline.md")
count_after = qdrant_client.get_collection("workspace_knowledge").points_count
assert count_after == count_before, "Upsert changed total point count (non-idempotent)"
```

### Test 4 — MRR parity with FAISS

Run 10 representative queries against both FAISS and Qdrant backends. Verify Qdrant MRR is
within 5% of FAISS MRR. Record the baseline MRR for Phase 2 monitoring.

### Test 5 — Rollback verification

Set `SEARCH_BACKEND=faiss`, restart, run the same 10 queries. Verify FAISS results are
identical to pre-migration baseline.

---

## 5. Index Validation Checklist

Before exiting Phase 1 shadow mode:

- [ ] Point count matches BM25 chunk count exactly
- [ ] Known-document retrieval (Test 2) passes for 5 diverse query terms
- [ ] Upsert idempotency (Test 3) verified
- [ ] MRR parity (Test 4) ≥ 95% of FAISS MRR
- [ ] Rollback verification (Test 5) confirmed
- [ ] Docker named volume disk usage recorded as Phase 1 baseline (`docker system df -v | findstr qdrant_workspace_knowledge`)
- [ ] `upsert_document` latency for a single file < 5 s recorded as baseline
- [ ] No Python exceptions or Windows compatibility errors in MCP server logs
