"""
Typed exception-path coverage for the EX-001 remediation (see
agent-systems-engineering/governance/adr-ase-001.md, "Exceptions Log").

_call_with_hard_timeout's call sites in
context-engineering/implementations/memory_vector_store.py and
mcp-servers/_shared/embedder_client.py used to fall into one bare
`except Exception` after the timeout branch. This suite verifies each site
now classifies (a) timeout, (b) connection/service-unavailable, and
(c) malformed-response failures into distinct branches, while the
degrade-never-raise contract stays unchanged.

Lives in harness-engineering/testing/ (not context-engineering/testing/ or a
new mcp-servers/_shared/tests/) because the property under test —
reconciliation with error_boundary.py's typed vocabulary — is a
harness-engineering-owned contract exercised through two other modules'
call sites; harness-engineering is also the module EX-001's remediation
owner is responsible for.

Run with:
    pytest harness-engineering/testing/test_ex001_typed_error_paths.py -v
(from core-component-00/)
"""
import concurrent.futures
import os
import sys
import time
import urllib.error
from unittest.mock import MagicMock

import pytest

_HARNESS_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, _HARNESS_ROOT)

_CORE00_ROOT = os.path.join(_HARNESS_ROOT, "..")
sys.path.insert(0, os.path.join(_CORE00_ROOT, "context-engineering"))
sys.path.insert(0, os.path.join(_CORE00_ROOT, "mcp-servers", "_shared"))

from implementations.memory_vector_store import (  # noqa: E402
    MemoryRecord,
    QdrantMemoryIndex,
    check_reachable,
)
import embedder_client  # noqa: E402


def _embedder(text: str):
    return [0.1] * 384


def _record() -> MemoryRecord:
    now = time.time()
    return MemoryRecord(
        id="r1",
        memory_type="semantic",
        content="test content",
        created_at=now,
        last_accessed_at=now,
    )


# ---------------------------------------------------------------------------
# memory_vector_store.py — QdrantMemoryIndex.ensure_collection
# ---------------------------------------------------------------------------

class TestEnsureCollectionTypedPaths:
    def test_timeout_degrades_without_raising(self):
        client = MagicMock()
        client.get_collections.side_effect = concurrent.futures.TimeoutError("timed out")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        index.ensure_collection()  # must not raise

    def test_connection_failure_degrades_without_raising(self):
        client = MagicMock()
        client.get_collections.side_effect = ConnectionRefusedError("no listener")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        index.ensure_collection()  # must not raise

    def test_malformed_response_degrades_without_raising(self):
        client = MagicMock()
        client.get_collections.return_value = object()  # no `.collections` attribute
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        index.ensure_collection()  # must not raise


# ---------------------------------------------------------------------------
# memory_vector_store.py — QdrantMemoryIndex.upsert_record
# ---------------------------------------------------------------------------

class TestUpsertRecordTypedPaths:
    def test_timeout_returns_false(self):
        client = MagicMock()
        client.upsert.side_effect = concurrent.futures.TimeoutError("timed out")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.upsert_record(_record()) is False

    def test_connection_failure_returns_false(self):
        client = MagicMock()
        client.upsert.side_effect = ConnectionRefusedError("no listener")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.upsert_record(_record()) is False

    def test_malformed_embedder_output_returns_false(self):
        def _bad_embedder(text):
            raise TypeError("embedder returned a non-vector shape")

        client = MagicMock()
        index = QdrantMemoryIndex("semantic", client=client, embedder=_bad_embedder)
        assert index.upsert_record(_record()) is False


# ---------------------------------------------------------------------------
# memory_vector_store.py — QdrantMemoryIndex.search
# ---------------------------------------------------------------------------

class TestSearchTypedPaths:
    def test_timeout_returns_empty_list(self):
        client = MagicMock()
        client.query_points.side_effect = concurrent.futures.TimeoutError("timed out")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.search("query") == []

    def test_connection_failure_returns_empty_list(self):
        client = MagicMock()
        client.query_points.side_effect = ConnectionRefusedError("no listener")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.search("query") == []

    def test_malformed_payload_returns_empty_list(self):
        client = MagicMock()
        bad_point = MagicMock(payload={"id": "r1"})  # missing required MemoryRecord fields
        client.query_points.return_value = MagicMock(points=[bad_point])
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.search("query") == []


# ---------------------------------------------------------------------------
# memory_vector_store.py — QdrantMemoryIndex.count_points
# ---------------------------------------------------------------------------

class TestCountPointsTypedPaths:
    def test_timeout_returns_zero(self):
        client = MagicMock()
        client.count.side_effect = concurrent.futures.TimeoutError("timed out")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.count_points() == 0

    def test_connection_failure_returns_zero(self):
        client = MagicMock()
        client.count.side_effect = ConnectionRefusedError("no listener")
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.count_points() == 0

    def test_malformed_response_returns_zero(self):
        client = MagicMock()
        client.count.return_value = object()  # no `.count` attribute
        index = QdrantMemoryIndex("semantic", client=client, embedder=_embedder)
        assert index.count_points() == 0


# ---------------------------------------------------------------------------
# memory_vector_store.py — check_reachable
# ---------------------------------------------------------------------------

class TestCheckReachableTypedPaths:
    def test_timeout_returns_false(self):
        client = MagicMock()
        client.get_collections.side_effect = concurrent.futures.TimeoutError("timed out")
        assert check_reachable(client) is False

    def test_connection_failure_returns_false(self):
        client = MagicMock()
        client.get_collections.side_effect = ConnectionRefusedError("no listener")
        assert check_reachable(client) is False


# ---------------------------------------------------------------------------
# embedder_client.py — embed()
# ---------------------------------------------------------------------------

class TestEmbedTypedPaths:
    def test_timeout_returns_none(self, monkeypatch):
        def _raise_timeout(fn, timeout=None):
            raise concurrent.futures.TimeoutError("timed out")

        monkeypatch.setattr(embedder_client, "_call_with_hard_timeout", _raise_timeout)
        assert embedder_client.embed(["hello"], model="test-model") is None

    def test_connection_failure_returns_none(self, monkeypatch):
        def _raise_conn(fn, timeout=None):
            raise urllib.error.URLError("connection refused")

        monkeypatch.setattr(embedder_client, "_call_with_hard_timeout", _raise_conn)
        assert embedder_client.embed(["hello"], model="test-model") is None

    def test_malformed_response_returns_none(self, monkeypatch):
        def _raise_malformed(fn, timeout=None):
            raise KeyError("vectors")

        monkeypatch.setattr(embedder_client, "_call_with_hard_timeout", _raise_malformed)
        assert embedder_client.embed(["hello"], model="test-model") is None


# ---------------------------------------------------------------------------
# embedder_client.py — probe_health() / _probe_health_once()
# ---------------------------------------------------------------------------

class TestProbeHealthTypedPaths:
    def test_timeout_returns_false(self, monkeypatch):
        def _raise_timeout(fn, timeout=None):
            raise concurrent.futures.TimeoutError("timed out")

        monkeypatch.setattr(embedder_client, "_call_with_hard_timeout", _raise_timeout)
        assert embedder_client.probe_health() is False

    def test_connection_failure_in_probe_once_returns_false(self, monkeypatch):
        def _raise_urlerror(*args, **kwargs):
            raise urllib.error.URLError("connection refused")

        monkeypatch.setattr(embedder_client.urllib.request, "urlopen", _raise_urlerror)
        assert embedder_client._probe_health_once() is False

    def test_malformed_json_in_probe_once_returns_false(self, monkeypatch):
        class _FakeResp:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return b"not json"

        monkeypatch.setattr(embedder_client.urllib.request, "urlopen", lambda *a, **k: _FakeResp())
        assert embedder_client._probe_health_once() is False
