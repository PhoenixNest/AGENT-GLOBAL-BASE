"""
RAG Pipeline — CC-00 RAG Layer 4 Reference Implementation

Orchestrates the full RAG flow: ingest → chunk → embed → store → retrieve → filter.
All heavy components (embedding model, vector store) are injected as callables,
keeping this module free of GPU/network dependencies and fully testable with mocks.

Integration contract with Layer 2 (Context Engineering):
  - pipeline.query() returns a list of Chunk objects
  - Caller places these in the Retrieved slot of the four-slot context window
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from .chunker import Chunk, FixedSizeChunker
from .retrieval import Document, ScoredDocument, acl_filter, bm25_score, rrf_fusion


@dataclass
class RetrievedContext:
    """Output of a pipeline query — ready for injection into the Retrieved slot."""
    chunks: List[Chunk]
    scores: List[float]
    query: str
    user_role: str


class RAGPipeline:
    """
    End-to-end RAG pipeline with injectable dependencies.

    Args:
        chunker:      Object with a .chunk(text: str) -> List[Chunk] method.
        embedder:     Callable(text: str) -> List[float]. May be a mock in tests.
        vector_store: Object with .upsert(id, vector, payload) and
                      .search(vector, top_k) -> List[Tuple[str, float]] methods.
        top_k:        Maximum results to retrieve before ACL filtering.
    """

    def __init__(
        self,
        chunker=None,
        embedder: Optional[Callable[[str], List[float]]] = None,
        vector_store=None,
        top_k: int = 5,
    ) -> None:
        self.chunker = chunker or FixedSizeChunker()
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k
        self._documents: Dict[str, Document] = {}

    def ingest(self, documents: List[Document]) -> int:
        """
        Chunk, embed, and store documents.

        Returns the total number of chunks ingested.
        """
        total = 0
        for doc in documents:
            chunks = self.chunker.chunk(doc.text)
            for chunk in chunks:
                chunk_id = f"{doc.id}::{chunk.index}"
                # Embed if embedder is available
                if self.embedder is not None:
                    vector = self.embedder(chunk.text)
                    if self.vector_store is not None:
                        self.vector_store.upsert(
                            id=chunk_id,
                            vector=vector,
                            payload={"doc_id": doc.id, "text": chunk.text, "acl_roles": doc.acl_roles},
                        )
                # Keep a local index for BM25 fallback
                self._documents[chunk_id] = Document(
                    id=chunk_id,
                    text=chunk.text,
                    metadata={"doc_id": doc.id},
                    acl_roles=doc.acl_roles,
                )
            total += len(chunks)
        return total

    def query(self, query: str, user_role: str = "public") -> RetrievedContext:
        """
        Retrieve relevant chunks for a query, filtered by user role.

        Hybrid strategy:
          1. BM25 keyword ranking over the local document index.
          2. Semantic vector search via vector_store (if available).
          3. RRF fusion of both result lists.
          4. ACL filtering.

        Returns a RetrievedContext with top_k accessible chunks.
        """
        corpus = list(self._documents.values())
        if not corpus:
            return RetrievedContext(chunks=[], scores=[], query=query, user_role=user_role)

        # BM25 leg
        bm25_results = bm25_score(query, corpus)[: self.top_k * 2]

        # Semantic leg (if vector store available)
        semantic_results: List[ScoredDocument] = []
        if self.embedder is not None and self.vector_store is not None:
            q_vector = self.embedder(query)
            raw = self.vector_store.search(q_vector, top_k=self.top_k * 2)
            for doc_id, score in raw:
                if doc_id in self._documents:
                    semantic_results.append(
                        ScoredDocument(document=self._documents[doc_id], score=score)
                    )

        # Fusion
        lists_to_fuse = [bm25_results]
        if semantic_results:
            lists_to_fuse.append(semantic_results)
        fused = rrf_fusion(lists_to_fuse)[: self.top_k * 2]

        # ACL filter
        accessible = acl_filter(fused, user_role)[: self.top_k]

        # Map back to Chunk objects
        chunks: List[Chunk] = []
        scores: List[float] = []
        for scored in accessible:
            chunks.append(Chunk(
                text=scored.document.text,
                index=scored.rank,
                start_char=0,
                end_char=len(scored.document.text),
                metadata=scored.document.metadata,
            ))
            scores.append(scored.score)

        return RetrievedContext(chunks=chunks, scores=scores, query=query, user_role=user_role)
