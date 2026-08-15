"""Regression test for SearchEngine._upsert_file_to_qdrant's encode-before-delete
ordering: an encode failure must never delete a file's existing Qdrant points
before the replacement points are ready.

Kept permanently, unlike the rest of this tests/ directory, which stays local
per .gitignore.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import server  # noqa: E402


def _make_engine(chunks):
    """Construct a SearchEngine for _upsert_file_to_qdrant testing only,
    bypassing __init__ (which triggers a full workspace BM25/FAISS/Qdrant
    initialization chain not needed here)."""
    engine = server.SearchEngine.__new__(server.SearchEngine)
    engine._chunks = []
    engine._qdrant_client = MagicMock()
    engine._collection_name = "workspace_knowledge"
    engine._extract_chunks = MagicMock(return_value=chunks)
    return engine


def _sample_chunks():
    return [
        {
            "rel_path": "docs/example.md",
            "chunk_idx": 0,
            "section": "Intro",
            "text": "hello world",
            "file_path": "/workspace/docs/example.md",
        }
    ]


def test_encode_failure_does_not_delete_existing_points():
    engine = _make_engine(_sample_chunks())
    engine._encode_batch_vectors = MagicMock(return_value=None)

    with pytest.raises(RuntimeError, match="model not ready"):
        engine._upsert_file_to_qdrant("/workspace/docs/example.md")

    engine._qdrant_client.delete.assert_not_called()
    engine._qdrant_client.upsert.assert_not_called()


def test_encode_success_deletes_then_upserts():
    engine = _make_engine(_sample_chunks())
    engine._encode_batch_vectors = MagicMock(
        return_value=[np.ones(768, dtype=np.float32)]
    )

    call_order = []
    engine._qdrant_client.delete.side_effect = lambda **_: call_order.append("delete")
    engine._qdrant_client.upsert.side_effect = lambda **_: call_order.append("upsert")

    count = engine._upsert_file_to_qdrant("/workspace/docs/example.md")

    assert count == 1
    assert call_order == ["delete", "upsert"]
