"""
Shared fixtures for the RAG Layer 4 test suite.

All heavy dependencies are replaced with deterministic stubs so the suite
runs without GPU, CUDA, spaCy, or a live Qdrant instance.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
from unittest.mock import MagicMock

import pytest

# Insert implementations/ onto sys.path so tests import without package install.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from implementations.retrieval import Document


# ---------------------------------------------------------------------------
# Embedding stub — deterministic, dimension-384, no model required
# ---------------------------------------------------------------------------

def _make_embedder(seed: float = 0.1):
    """Return a callable that produces a fixed-length deterministic vector."""
    def embed(text: str) -> List[float]:
        # Vary the vector by the first character so different texts get different vectors.
        base = seed + (ord(text[0]) / 1000 if text else 0)
        return [round(base + i * 0.001, 6) for i in range(384)]
    return embed


@pytest.fixture
def embedder():
    return _make_embedder()


# ---------------------------------------------------------------------------
# Mock Qdrant client
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_vector_store():
    """In-memory mock of a Qdrant-compatible vector store."""
    store: Dict[str, Tuple[List[float], dict]] = {}

    client = MagicMock()

    def upsert(id: str, vector: List[float], payload: dict) -> None:
        store[id] = (vector, payload)

    def search(vector: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        # Return ids ordered by first-element similarity (trivial, deterministic).
        if not store:
            return []
        scored = sorted(
            store.items(),
            key=lambda item: -abs(item[1][0][0] - vector[0]),
        )
        return [(doc_id, round(1.0 - i * 0.1, 3)) for i, (doc_id, _) in enumerate(scored[:top_k])]

    client.upsert = upsert
    client.search = search
    return client


# ---------------------------------------------------------------------------
# Sample document corpus
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_docs():
    return [
        Document(
            id="doc-1",
            text="Context engineering defines how to structure information for LLM calls. "
                 "The four-slot model separates system, retrieved, history, and tool outputs.",
            acl_roles=["public"],
        ),
        Document(
            id="doc-2",
            text="Error boundaries wrap model calls with retry logic. "
                 "They handle rate limits, timeouts, and validation failures.",
            acl_roles=["engineering"],
        ),
        Document(
            id="doc-3",
            text="RAG pipelines retrieve relevant documents and inject them into the context window. "
                 "Hybrid retrieval combines BM25 keyword search with semantic vector search.",
            acl_roles=["public"],
        ),
        Document(
            id="doc-4",
            text="Swarm orchestration coordinates multiple agents across topologies. "
                 "Each agent receives context via the handoff packet protocol.",
            acl_roles=["research"],
        ),
    ]
