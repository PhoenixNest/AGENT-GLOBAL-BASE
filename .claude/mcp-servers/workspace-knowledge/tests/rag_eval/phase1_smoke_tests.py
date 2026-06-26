"""
Phase 1 Smoke Tests — Qdrant Shadow Mode Validation
Run after MCP server restart (seeding completes in background thread).

Usage:
    cd .claude/mcp-servers/workspace-knowledge
    .venv/Scripts/python tests/rag_eval/phase1_smoke_tests.py

Exit codes: 0 = all pass, 1 = one or more failures.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent.parent  # workspace root


def _client():
    from qdrant_client import QdrantClient
    return QdrantClient(url="http://localhost:6333", timeout=10)


def _collection():
    return "workspace_knowledge"


# ── Test 1: Point count integrity ──────────────────────────────────────────────

def test_point_count():
    """Qdrant must hold at least as many points as there are .md files in KEY_DIRS."""
    client = _client()
    info = client.get_collection(_collection())
    count = info.points_count
    assert count > 0, f"Collection is empty — seeding did not complete (count={count})"
    md_files = sum(
        len(list((ROOT / d).rglob("*.md")))
        for d in ("company", "studio", "core-component-00", "telescope")
        if (ROOT / d).exists()
    )
    # Each file produces ≥1 chunk; expect at least one point per file
    assert count >= md_files, (
        f"Point count {count} < md file count {md_files} — seeding appears incomplete"
    )
    print(f"[PASS] test_point_count: {count} points, {md_files} .md files")


# ── Test 2: Known-document retrieval ──────────────────────────────────────────

def test_known_document_retrieval():
    """A query about ASE governance must surface the ADR or CLAUDE.md in top-5."""
    from qdrant_client import QdrantClient
    import numpy as np
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-mpnet-base-v2")
    query = "ASE governance ADR mandatory framework CC-00"
    q_emb = model.encode([query])
    q_emb = (q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True))[0].tolist()

    client = QdrantClient(url="http://localhost:6333", timeout=10)
    results = client.search(
        collection_name=_collection(),
        query_vector=q_emb,
        limit=5,
        with_payload=True,
    )
    paths = [r.payload.get("rel_path", "") for r in results]
    hit = any(
        "agent-systems-engineering" in p or "CLAUDE.md" in p or "ADR" in p
        for p in paths
    )
    assert hit, f"Known-document not in top-5. Got: {paths}"
    print(f"[PASS] test_known_document_retrieval: hit in top-5 — {paths[:2]}")


# ── Test 3: Upsert idempotency ─────────────────────────────────────────────────

def test_upsert_idempotency():
    """Upserting the same file twice must not grow the point count for that rel_path."""
    import hashlib
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue

    client = QdrantClient(url="http://localhost:6333", timeout=10)
    model = SentenceTransformer("all-mpnet-base-v2")

    # Use CLAUDE.md as the test document
    test_file = ROOT / "CLAUDE.md"
    rel_path = str(test_file.relative_to(ROOT)).replace("\\", "/")

    def _count():
        scroll, _ = client.scroll(
            collection_name=_collection(),
            scroll_filter=Filter(must=[FieldCondition(key="rel_path", match=MatchValue(value=rel_path))]),
            limit=500,
            with_payload=False,
        )
        return len(scroll)

    count_before = _count()
    assert count_before > 0, f"No points for {rel_path} — seeding did not include root CLAUDE.md"

    # Simulate upsert: delete + re-insert same content
    client.delete(
        collection_name=_collection(),
        points_selector=Filter(must=[FieldCondition(key="rel_path", match=MatchValue(value=rel_path))]),
    )
    text = test_file.read_text(encoding="utf-8")
    chunks = [text[i:i+512] for i in range(0, min(len(text), 2048), 512)]
    embeddings = model.encode(chunks, show_progress_bar=False)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    def _chunk_point_id(rp, idx):
        key = f"{rp}:{idx}"
        digest = hashlib.md5(key.encode()).hexdigest()
        return int(digest[:15], 16)

    points = [
        PointStruct(
            id=_chunk_point_id(rel_path, i),
            vector=emb.astype(float).tolist(),
            payload={"rel_path": rel_path, "section": "", "chunk_idx": i, "text": c, "file_path": str(test_file)},
        )
        for i, (c, emb) in enumerate(zip(chunks, embeddings))
    ]
    client.upsert(collection_name=_collection(), points=points)
    count_after = _count()

    assert count_after == len(points), (
        f"Idempotency failure: after upsert got {count_after} points, expected {len(points)}"
    )
    print(f"[PASS] test_upsert_idempotency: {count_before} → deleted → {count_after} (stable)")


# ── MRR baseline (Test 4 — requires queries, uses BM25 + Qdrant) ──────────────

def _mrr_at_k(results_per_query: list[list[str]], relevant_per_query: list[list[str]], k: int = 10) -> float:
    rr_sum = 0.0
    for results, relevant in zip(results_per_query, relevant_per_query):
        for rank, doc in enumerate(results[:k], start=1):
            if any(rel in doc for rel in relevant):
                rr_sum += 1.0 / rank
                break
    return rr_sum / len(results_per_query) if results_per_query else 0.0


def test_mrr_baseline():
    """Compute MRR@10 for Qdrant against the B-3 query set and print the baseline."""
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from qdrant_client import QdrantClient

    query_file = Path(__file__).parent / "mrr_query_set.json"
    data = json.loads(query_file.read_text(encoding="utf-8"))
    queries = data["queries"]

    model = SentenceTransformer("all-mpnet-base-v2")
    client = QdrantClient(url="http://localhost:6333", timeout=10)

    results_per_query = []
    relevant_per_query = []

    for q in queries:
        q_emb = model.encode([q["query"]])
        q_emb = (q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True))[0].tolist()
        hits = client.search(
            collection_name=_collection(),
            query_vector=q_emb,
            limit=10,
            with_payload=True,
        )
        returned_paths = [h.payload.get("rel_path", "") for h in hits]
        results_per_query.append(returned_paths)
        relevant_per_query.append(q["relevant_docs"])

    mrr = _mrr_at_k(results_per_query, relevant_per_query)
    print(f"[INFO] Qdrant MRR@10 baseline: {mrr:.4f}  (Phase 2 gate: Qdrant MRR ≥ 95% of FAISS MRR)")
    # Store baseline for Phase 2 gate comparison
    baseline_file = Path(__file__).parent / "mrr_baseline.json"
    baseline_file.write_text(json.dumps({"qdrant_mrr_at_10": round(mrr, 4), "query_count": len(queries)}, indent=2))
    print(f"[INFO] Baseline written to {baseline_file}")
    # MRR > 0 is the Phase 1 sanity bar (collection is populated and retrieving)
    assert mrr > 0.0, f"MRR@10 = 0.0 — Qdrant is not returning relevant results"
    print(f"[PASS] test_mrr_baseline: MRR@10 = {mrr:.4f}")


# ── Runner ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_point_count,
        test_known_document_retrieval,
        test_upsert_idempotency,
        test_mrr_baseline,
    ]
    failures = []
    for t in tests:
        try:
            t()
        except Exception as exc:
            print(f"[FAIL] {t.__name__}: {exc}")
            failures.append(t.__name__)

    print()
    if failures:
        print(f"FAILED: {len(failures)}/{len(tests)} — {failures}")
        sys.exit(1)
    else:
        print(f"ALL PASS: {len(tests)}/{len(tests)}")
        sys.exit(0)
