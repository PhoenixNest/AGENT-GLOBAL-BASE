"""
Tests for RAGPipeline end-to-end orchestration.

All I/O boundaries (embedding model, vector store) are replaced with mocks from
conftest.py. Tests verify the Layer 2 (Context Engineering) slot assembly contract:
  - pipeline.query() returns a RetrievedContext
  - RetrievedContext.chunks contains Chunk objects with populated text
  - ACL roles are enforced before chunks reach the caller
  - Scores are non-negative floats parallel to chunks
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from implementations import pipeline as pipeline_module
from implementations.chunker import FixedSizeChunker, SemanticChunker
from implementations.pipeline import RAGPipeline, RetrievedContext
from implementations.retrieval import Document


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_pipeline(embedder=None, vector_store=None, top_k=3, chunker=None):
    return RAGPipeline(
        chunker=chunker,
        embedder=embedder,
        vector_store=vector_store,
        top_k=top_k,
    )


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------

class TestIngest:
    def test_returns_chunk_count(self, sample_docs):
        pipeline = _make_pipeline()
        total = pipeline.ingest(sample_docs)
        assert total > 0

    def test_ingest_populates_internal_index(self, sample_docs):
        pipeline = _make_pipeline()
        pipeline.ingest(sample_docs)
        assert len(pipeline._documents) > 0

    def test_ingest_calls_embedder_per_chunk(self, sample_docs, embedder):
        call_count = []

        def counting_embedder(text):
            call_count.append(text)
            return embedder(text)

        pipeline = _make_pipeline(embedder=counting_embedder)
        total = pipeline.ingest(sample_docs)
        assert len(call_count) == total

    def test_ingest_calls_vector_store_upsert(self, sample_docs, embedder, mock_vector_store):
        pipeline = _make_pipeline(embedder=embedder, vector_store=mock_vector_store)
        total = pipeline.ingest(sample_docs)
        # upsert should have been called once per chunk
        stored_count = len(mock_vector_store.search([0.1] * 384, top_k=1000))
        assert stored_count > 0

    def test_chunk_ids_include_doc_id(self, sample_docs):
        pipeline = _make_pipeline()
        pipeline.ingest(sample_docs)
        for chunk_id in pipeline._documents:
            assert "::" in chunk_id
            doc_id = chunk_id.split("::")[0]
            assert any(doc_id == d.id for d in sample_docs)

    def test_acl_roles_preserved_after_ingest(self, sample_docs):
        pipeline = _make_pipeline()
        pipeline.ingest(sample_docs)
        for chunk_id, doc in pipeline._documents.items():
            src_id = chunk_id.split("::")[0]
            src_doc = next(d for d in sample_docs if d.id == src_id)
            assert doc.acl_roles == src_doc.acl_roles


# ---------------------------------------------------------------------------
# Query — Layer 2 contract
# ---------------------------------------------------------------------------

class TestQuery:
    def test_returns_retrieved_context(self, sample_docs):
        pipeline = _make_pipeline()
        pipeline.ingest(sample_docs)
        result = pipeline.query("context engineering", user_role="public")
        assert isinstance(result, RetrievedContext)

    def test_chunks_and_scores_have_equal_length(self, sample_docs):
        pipeline = _make_pipeline()
        pipeline.ingest(sample_docs)
        result = pipeline.query("retrieval", user_role="public")
        assert len(result.chunks) == len(result.scores)

    def test_scores_are_non_negative(self, sample_docs):
        pipeline = _make_pipeline()
        pipeline.ingest(sample_docs)
        result = pipeline.query("retrieval", user_role="public")
        assert all(s >= 0.0 for s in result.scores)

    def test_query_string_preserved_in_result(self, sample_docs):
        pipeline = _make_pipeline()
        pipeline.ingest(sample_docs)
        result = pipeline.query("context", user_role="public")
        assert result.query == "context"

    def test_user_role_preserved_in_result(self, sample_docs):
        pipeline = _make_pipeline()
        pipeline.ingest(sample_docs)
        result = pipeline.query("context", user_role="engineering")
        assert result.user_role == "engineering"

    def test_top_k_limit_enforced(self, sample_docs):
        pipeline = _make_pipeline(top_k=2)
        pipeline.ingest(sample_docs)
        result = pipeline.query("engineering context retrieval swarm", user_role="research")
        assert len(result.chunks) <= 2

    def test_empty_pipeline_returns_empty_context(self):
        pipeline = _make_pipeline()
        result = pipeline.query("anything")
        assert result.chunks == []
        assert result.scores == []


# ---------------------------------------------------------------------------
# ACL enforcement in pipeline
# ---------------------------------------------------------------------------

class TestPipelineACL:
    def test_public_role_excludes_private_chunks(self, sample_docs):
        pipeline = _make_pipeline()
        pipeline.ingest(sample_docs)
        result = pipeline.query("error boundaries swarm agents", user_role="public")
        for chunk in result.chunks:
            src_id = chunk.metadata.get("doc_id", "")
            # doc-2 (engineering) and doc-4 (research) should not appear for public role
            assert src_id not in ("doc-2", "doc-4")

    def test_engineering_role_can_access_engineering_chunks(self, sample_docs):
        pipeline = _make_pipeline(top_k=10)
        pipeline.ingest(sample_docs)
        result = pipeline.query("error boundaries retry", user_role="engineering")
        doc_ids = {chunk.metadata.get("doc_id") for chunk in result.chunks}
        assert "doc-2" in doc_ids

    def test_no_results_for_role_with_no_matching_docs(self):
        docs = [
            Document(id="priv", text="classified information for admins only", acl_roles=["admin"]),
        ]
        pipeline = _make_pipeline()
        pipeline.ingest(docs)
        result = pipeline.query("classified", user_role="public")
        assert result.chunks == []


# ---------------------------------------------------------------------------
# Pre-fusion ACL enforcement (RAG R1 remediation, I1)
#
# These tests inspect the candidate set BEFORE post-fusion acl_filter() runs,
# to verify the query-level ACL predicate itself excludes out-of-role
# documents — not just that the final filtered output happens to be clean.
# ---------------------------------------------------------------------------

class TestPreFusionACLEnforcement:
    def test_bm25_leg_scores_only_role_accessible_corpus(self, sample_docs, monkeypatch):
        """bm25_score() must never even see out-of-role documents."""
        pipeline = _make_pipeline(top_k=10)
        pipeline.ingest(sample_docs)

        captured = {}
        original_bm25_score = pipeline_module.bm25_score

        def spy_bm25_score(query, documents, *args, **kwargs):
            captured["documents"] = list(documents)
            return original_bm25_score(query, documents, *args, **kwargs)

        monkeypatch.setattr(pipeline_module, "bm25_score", spy_bm25_score)
        pipeline.query("error boundaries swarm agents", user_role="public")

        assert "documents" in captured
        doc_ids_seen = {doc.metadata.get("doc_id") for doc in captured["documents"]}
        # doc-2 is engineering-only, doc-4 is research-only — neither should
        # ever reach bm25_score's candidate set for a "public" query.
        assert "doc-2" not in doc_ids_seen
        assert "doc-4" not in doc_ids_seen

    def test_vector_store_search_receives_user_role(self, sample_docs, embedder, mock_vector_store):
        pipeline = _make_pipeline(embedder=embedder, vector_store=mock_vector_store, top_k=10)
        pipeline.ingest(sample_docs)

        original_search = mock_vector_store.search
        captured = {}

        def spy_search(vector, top_k=5, user_role=None):
            captured["user_role"] = user_role
            return original_search(vector, top_k=top_k, user_role=user_role)

        mock_vector_store.search = spy_search
        pipeline.query("error boundaries swarm agents", user_role="engineering")

        assert captured["user_role"] == "engineering"

    def test_vector_store_search_excludes_out_of_role_docs_directly(
        self, sample_docs, embedder, mock_vector_store
    ):
        """
        Call the vector store's search() directly (not through the pipeline)
        to confirm the raw candidate set it returns is already role-filtered,
        before any post-fusion acl_filter() step exists.
        """
        pipeline = _make_pipeline(embedder=embedder, vector_store=mock_vector_store, top_k=10)
        pipeline.ingest(sample_docs)

        q_vector = embedder("error boundaries swarm agents")
        raw = mock_vector_store.search(q_vector, top_k=10, user_role="public")
        returned_doc_ids = {doc_id.split("::")[0] for doc_id, _ in raw}

        assert "doc-2" not in returned_doc_ids
        assert "doc-4" not in returned_doc_ids

    def test_research_role_candidate_set_includes_research_docs(
        self, sample_docs, embedder, mock_vector_store
    ):
        pipeline = _make_pipeline(embedder=embedder, vector_store=mock_vector_store, top_k=10)
        pipeline.ingest(sample_docs)

        q_vector = embedder("swarm orchestration agents")
        raw = mock_vector_store.search(q_vector, top_k=10, user_role="research")
        returned_doc_ids = {doc_id.split("::")[0] for doc_id, _ in raw}

        assert "doc-4" in returned_doc_ids


# ---------------------------------------------------------------------------
# Hybrid retrieval path (with mocked vector store)
# ---------------------------------------------------------------------------

class TestHybridRetrieval:
    def test_vector_store_results_contribute_to_output(self, sample_docs, embedder, mock_vector_store):
        pipeline = _make_pipeline(embedder=embedder, vector_store=mock_vector_store, top_k=5)
        pipeline.ingest(sample_docs)
        result = pipeline.query("context window slot assembly", user_role="public")
        # With hybrid retrieval, we should get results (both BM25 and vector legs run)
        assert len(result.chunks) > 0

    def test_bm25_only_pipeline_still_works(self, sample_docs):
        """Pipeline without vector store falls back to pure BM25."""
        pipeline = _make_pipeline(embedder=None, vector_store=None, top_k=3)
        pipeline.ingest(sample_docs)
        result = pipeline.query("retrieval BM25", user_role="public")
        assert len(result.chunks) > 0

    def test_chunker_strategy_affects_chunk_count(self, sample_docs):
        fixed_pipeline = _make_pipeline(chunker=FixedSizeChunker(chunk_size=50, overlap=0))
        semantic_pipeline = _make_pipeline(chunker=SemanticChunker(max_size=500))

        fixed_count = fixed_pipeline.ingest(sample_docs)
        semantic_count = semantic_pipeline.ingest(sample_docs)

        # Fixed-size with small window creates more chunks than semantic with large window
        assert fixed_count >= semantic_count
