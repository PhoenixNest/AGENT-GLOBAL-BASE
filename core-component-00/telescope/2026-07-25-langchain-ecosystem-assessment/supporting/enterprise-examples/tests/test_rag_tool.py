"""Real execution tests for the ACL-closure RAG tool wrapper — Finding 14."""

from __future__ import annotations

from cc00_langchain.cc00_path import Document, FixedSizeChunker, RAGPipeline
from cc00_langchain.rag_tool import make_corpus_search


def _pipeline() -> RAGPipeline:
    pipeline = RAGPipeline(chunker=FixedSizeChunker(chunk_size=200), top_k=5)
    pipeline.ingest(
        [
            Document(id="doc-public", text="The onboarding process takes three days.", acl_roles=["public"]),
            Document(id="doc-staff", text="Internal salary bands are confidential information.", acl_roles=["staff"]),
        ]
    )
    return pipeline


def test_public_role_cannot_see_staff_only_document():
    search = make_corpus_search(_pipeline(), user_role="public")
    results = search.invoke({"query": "salary"})
    sources = {r["source"] for r in results}
    assert "doc-staff" not in sources


def test_staff_role_sees_both():
    search = make_corpus_search(_pipeline(), user_role="staff")
    results = search.invoke({"query": "salary"})
    sources = {r["source"] for r in results}
    assert "doc-staff" in sources
    assert "doc-public" in sources


def test_tool_signature_has_no_role_parameter():
    """The load-bearing property: a model cannot escalate its own role because
    the parameter through which it would do so does not exist."""
    search = make_corpus_search(_pipeline(), user_role="public")
    assert "user_role" not in search.args
    assert set(search.args.keys()) == {"query", "top_k"}


def test_top_k_is_capped_at_ten():
    pipeline = RAGPipeline(chunker=FixedSizeChunker(chunk_size=50, overlap=10), top_k=20)
    pipeline.ingest([Document(id=f"d{i}", text=f"document number {i}", acl_roles=["public"]) for i in range(15)])
    search = make_corpus_search(pipeline, user_role="public")
    results = search.invoke({"query": "document", "top_k": 50})
    assert len(results) <= 10
