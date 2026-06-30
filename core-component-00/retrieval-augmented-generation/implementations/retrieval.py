"""
Retrieval — CC-00 RAG Layer 4 Reference Implementation

Pure-Python implementations of:
  - BM25 scoring  (keyword-based term weighting)
  - RRF fusion    (Reciprocal Rank Fusion across multiple result lists)
  - ACL filtering (role-based document access control)

No external dependencies required. Heavy components (vector store,
embedding model) are injected at the pipeline layer.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Document:
    id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    acl_roles: List[str] = field(default_factory=lambda: ["public"])


@dataclass
class ScoredDocument:
    document: Document
    score: float
    rank: int = 0


def _tokenize(text: str) -> List[str]:
    """Lowercase whitespace tokenizer."""
    return text.lower().split()


def bm25_score(
    query: str,
    documents: List[Document],
    k1: float = 1.5,
    b: float = 0.75,
) -> List[ScoredDocument]:
    """
    Score documents against a query using BM25.

    Args:
        query:     Query string.
        documents: Corpus to score against.
        k1:        Term frequency saturation parameter.
        b:         Length normalisation parameter.

    Returns:
        Documents sorted by descending BM25 score (ties broken by original order).
    """
    if not documents:
        return []

    query_terms = _tokenize(query)
    tokenized = [_tokenize(doc.text) for doc in documents]
    doc_lengths = [len(t) for t in tokenized]
    avg_dl = sum(doc_lengths) / len(doc_lengths)
    N = len(documents)

    # Document frequency per term
    df: Dict[str, int] = {}
    for terms in tokenized:
        for term in set(terms):
            df[term] = df.get(term, 0) + 1

    results: List[ScoredDocument] = []
    for idx, (doc, terms) in enumerate(zip(documents, tokenized)):
        tf_map = Counter(terms)
        dl = doc_lengths[idx]
        score = 0.0
        for term in query_terms:
            if term not in tf_map:
                continue
            tf = tf_map[term]
            idf = math.log((N - df.get(term, 0) + 0.5) / (df.get(term, 0) + 0.5) + 1)
            tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avg_dl))
            score += idf * tf_norm
        results.append(ScoredDocument(document=doc, score=score, rank=idx))

    results.sort(key=lambda r: (-r.score, r.rank))
    for i, r in enumerate(results):
        r.rank = i
    return results


def rrf_fusion(
    ranked_lists: List[List[ScoredDocument]],
    k: int = 60,
) -> List[ScoredDocument]:
    """
    Merge multiple ranked result lists using Reciprocal Rank Fusion.

    Args:
        ranked_lists: Each inner list is a ranked sequence of ScoredDocuments.
        k:            Smoothing constant (default 60, per the RRF paper).

    Returns:
        Documents sorted by descending RRF score, deduplicated by document id.
    """
    rrf_scores: Dict[str, float] = {}
    doc_map: Dict[str, Document] = {}

    for ranked in ranked_lists:
        for rank_pos, scored in enumerate(ranked):
            doc_id = scored.document.id
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k + rank_pos + 1)
            doc_map[doc_id] = scored.document

    merged = [
        ScoredDocument(document=doc_map[doc_id], score=score)
        for doc_id, score in rrf_scores.items()
    ]
    merged.sort(key=lambda r: -r.score)
    for i, r in enumerate(merged):
        r.rank = i
    return merged


def acl_filter(
    results: List[ScoredDocument],
    user_role: str,
) -> List[ScoredDocument]:
    """
    Filter results to documents accessible by the given user role.

    A document is accessible when:
      - Its acl_roles list contains "public", OR
      - Its acl_roles list contains the user_role.

    Args:
        results:   Ranked documents to filter.
        user_role: The requesting user's role string.

    Returns:
        Filtered list preserving original rank order.
    """
    allowed: List[ScoredDocument] = []
    for scored in results:
        roles = scored.document.acl_roles
        if "public" in roles or user_role in roles:
            allowed.append(scored)
    # Re-rank after filtering
    for i, r in enumerate(allowed):
        r.rank = i
    return allowed
