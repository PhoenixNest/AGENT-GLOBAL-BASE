"""
RAG Layer 4 — Reference Implementations

Lightweight, dependency-injectable implementations of the core RAG
pipeline components. All heavy dependencies (embedding models, vector
stores) are passed in as callables, making every component testable
without GPU, CUDA, or a live Qdrant instance.

User reference deployment: core-component-00/mcp-servers/workspace-knowledge/
(BM25 + Qdrant hybrid retrieval, production-grade)
"""

from .chunker import FixedSizeChunker, SemanticChunker, HybridChunker
from .retrieval import bm25_score, rrf_fusion, acl_filter
from .pipeline import RAGPipeline

__all__ = [
    "FixedSizeChunker",
    "SemanticChunker",
    "HybridChunker",
    "bm25_score",
    "rrf_fusion",
    "acl_filter",
    "RAGPipeline",
]
