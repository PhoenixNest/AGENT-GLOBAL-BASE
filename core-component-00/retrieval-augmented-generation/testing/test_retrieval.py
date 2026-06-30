"""
Tests for BM25 scoring, RRF fusion, and ACL filtering.
All tests are pure Python — no vector store, no embeddings, no network.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from implementations.retrieval import Document, ScoredDocument, acl_filter, bm25_score, rrf_fusion


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def corpus():
    return [
        Document(id="a", text="context engineering structures information for LLM calls",
                 acl_roles=["public"]),
        Document(id="b", text="error boundaries handle rate limits and timeouts",
                 acl_roles=["engineering"]),
        Document(id="c", text="RAG retrieval combines BM25 keyword search with vector search",
                 acl_roles=["public"]),
        Document(id="d", text="swarm orchestration coordinates multiple agents",
                 acl_roles=["research"]),
    ]


# ---------------------------------------------------------------------------
# BM25 scoring
# ---------------------------------------------------------------------------

class TestBM25Score:
    def test_returns_all_documents(self, corpus):
        results = bm25_score("context engineering", corpus)
        assert len(results) == len(corpus)

    def test_relevant_document_ranks_first(self, corpus):
        results = bm25_score("context engineering", corpus)
        assert results[0].document.id == "a"

    def test_scores_are_non_negative(self, corpus):
        for result in bm25_score("context engineering", corpus):
            assert result.score >= 0.0

    def test_irrelevant_query_produces_zero_scores(self, corpus):
        results = bm25_score("xyzzy frobnitZ", corpus)
        assert all(r.score == 0.0 for r in results)

    def test_ranking_by_term_frequency(self):
        docs = [
            Document(id="once", text="retrieval"),
            Document(id="twice", text="retrieval retrieval"),
            Document(id="none", text="context engineering"),
        ]
        results = bm25_score("retrieval", docs)
        ids = [r.document.id for r in results if r.score > 0]
        assert ids[0] == "twice"

    def test_empty_corpus_returns_empty(self):
        assert bm25_score("anything", []) == []

    def test_ranks_are_sequential(self, corpus):
        results = bm25_score("context", corpus)
        for i, r in enumerate(results):
            assert r.rank == i

    def test_bm25_score_keyword_match(self, corpus):
        results = bm25_score("BM25 keyword", corpus)
        top = results[0]
        assert top.document.id == "c"


# ---------------------------------------------------------------------------
# RRF fusion
# ---------------------------------------------------------------------------

class TestRRFFusion:
    def test_deduplicates_across_lists(self):
        doc = Document(id="x", text="shared")
        sd = ScoredDocument(document=doc, score=1.0, rank=0)
        result = rrf_fusion([[sd], [sd]])
        ids = [r.document.id for r in result]
        assert ids.count("x") == 1

    def test_document_in_both_lists_ranks_higher(self):
        shared = Document(id="shared", text="shared document")
        only_a = Document(id="only_a", text="document a only")
        list_a = [
            ScoredDocument(document=shared, score=1.0, rank=0),
            ScoredDocument(document=only_a, score=0.5, rank=1),
        ]
        list_b = [
            ScoredDocument(document=shared, score=0.9, rank=0),
        ]
        result = rrf_fusion([list_a, list_b])
        assert result[0].document.id == "shared"

    def test_empty_lists_return_empty(self):
        assert rrf_fusion([[], []]) == []

    def test_single_list_preserved_in_order(self):
        docs = [
            Document(id="first", text="first"),
            Document(id="second", text="second"),
        ]
        ranked = [ScoredDocument(document=d, score=1.0 - i * 0.1, rank=i) for i, d in enumerate(docs)]
        result = rrf_fusion([ranked])
        assert result[0].document.id == "first"

    def test_rrf_scores_are_positive(self):
        doc = Document(id="z", text="test")
        ranked = [ScoredDocument(document=doc, score=0.5, rank=0)]
        result = rrf_fusion([ranked])
        assert result[0].score > 0

    def test_output_ranks_are_sequential(self):
        docs = [Document(id=str(i), text=f"doc {i}") for i in range(3)]
        ranked = [ScoredDocument(document=d, score=float(3 - i), rank=i) for i, d in enumerate(docs)]
        result = rrf_fusion([ranked])
        for i, r in enumerate(result):
            assert r.rank == i


# ---------------------------------------------------------------------------
# ACL filtering
# ---------------------------------------------------------------------------

class TestACLFilter:
    def _make_results(self, docs):
        return [ScoredDocument(document=d, score=1.0 - i * 0.1, rank=i) for i, d in enumerate(docs)]

    def test_public_role_sees_only_public(self):
        docs = [
            Document(id="pub", text="public", acl_roles=["public"]),
            Document(id="eng", text="eng-only", acl_roles=["engineering"]),
        ]
        filtered = acl_filter(self._make_results(docs), "public")
        ids = [r.document.id for r in filtered]
        assert "pub" in ids
        assert "eng" not in ids

    def test_engineering_role_sees_engineering_and_public(self):
        docs = [
            Document(id="pub", text="public", acl_roles=["public"]),
            Document(id="eng", text="eng-only", acl_roles=["engineering"]),
            Document(id="res", text="research-only", acl_roles=["research"]),
        ]
        filtered = acl_filter(self._make_results(docs), "engineering")
        ids = [r.document.id for r in filtered]
        assert "pub" in ids
        assert "eng" in ids
        assert "res" not in ids

    def test_unknown_role_sees_only_public(self):
        docs = [
            Document(id="pub", text="public", acl_roles=["public"]),
            Document(id="priv", text="private", acl_roles=["admin"]),
        ]
        filtered = acl_filter(self._make_results(docs), "stranger")
        assert len(filtered) == 1
        assert filtered[0].document.id == "pub"

    def test_empty_results_returns_empty(self):
        assert acl_filter([], "public") == []

    def test_filtered_ranks_are_sequential(self):
        docs = [
            Document(id="pub1", text="a", acl_roles=["public"]),
            Document(id="eng1", text="b", acl_roles=["engineering"]),
            Document(id="pub2", text="c", acl_roles=["public"]),
        ]
        filtered = acl_filter(self._make_results(docs), "public")
        for i, r in enumerate(filtered):
            assert r.rank == i

    def test_document_with_multiple_roles(self):
        doc = Document(id="multi", text="multi-role", acl_roles=["public", "engineering", "research"])
        result = [ScoredDocument(document=doc, score=1.0, rank=0)]
        for role in ["public", "engineering", "research", "unknown"]:
            filtered = acl_filter(result, role)
            # public is in the acl_roles, so all roles should see it
            assert len(filtered) == 1

    def test_all_private_returns_empty_for_public(self):
        docs = [
            Document(id="x", text="private", acl_roles=["engineering"]),
            Document(id="y", text="secret", acl_roles=["research"]),
        ]
        filtered = acl_filter(self._make_results(docs), "public")
        assert filtered == []
