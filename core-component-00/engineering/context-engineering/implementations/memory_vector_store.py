"""
Memory Vector Store — Qdrant Write-Through + Append-Only JSONL Log

Implements the Memory-as-Corpus principle for the three persistent memory types
(episodic, semantic, procedural): every memory write is first appended to a
durable, human-readable JSONL log (the source of truth); the Qdrant collection
is a derived, rebuildable semantic index over that log — exactly as the
existing document-corpus RAG collection is a derived index over the Markdown
corpus. This module never touches that existing collection or its retrieval
pipeline (`retrieval-augmented-generation/implementations/`).

Full design spec:
    telescope/2026-07-10-agent-memory-architecture/supporting/01-technical-options.md
    telescope/2026-07-10-agent-memory-architecture/supporting/02-deployment-guidelines.md

WorkingMemory is intentionally absent here — it is task-scoped, in-memory-only
state that should never be persisted to Qdrant or JSONL.

Dependency injection follows the same pattern as RAGPipeline
(`retrieval-augmented-generation/implementations/pipeline.py`): the Qdrant client
and embedder are injected, never imported eagerly at module scope, so every class
here is unit-testable with mocks and requires no live qdrant-memory instance.

Usage:
    log = JSONLMemoryLog()
    index = QdrantMemoryIndex("semantic", client=qdrant_client, embedder=embed_fn)
    sink = PersistentMemorySink(log=log, indices={"semantic": index})

    sm = SemanticMemory(sink=sink)   # see memory_store.py
    sm.store("user_stack", "Prefers FastAPI, PostgreSQL")
"""

from __future__ import annotations

import concurrent.futures
import json
import os
import queue
import sys
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, TYPE_CHECKING

# qdrant_client talks to Qdrant over httpx, which honors the OS-level system
# proxy by default (trust_env=True). On a machine with a local proxy/VPN
# tool configured, that can route loopback traffic through the proxy instead
# of connecting directly, which a local-only service like qdrant-memory
# cannot answer. Setting NO_PROXY/no_proxy for localhost and 127.0.0.1
# guarantees direct connections regardless of the host machine's proxy
# configuration. setdefault() so a deliberately-configured value is never
# overridden.
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
os.environ.setdefault("no_proxy", "localhost,127.0.0.1")

if TYPE_CHECKING:
    from .memory_store import EpisodicEvent, SemanticFact, ReflectionRecord

# Real (non-TYPE_CHECKING) import: PersistentMemorySink.write_reflection()'s
# identity gate (MISTAKE-2026-07-16-001 remediation item 2) needs these at
# runtime, not just for type annotations. No circular-import risk —
# memory_store.py has no dependency on this module (verified: it imports
# nothing from memory_vector_store.py).
from .memory_store import GOVERNANCE_TRIGGERS, IdentityVerification, UnverifiedReflectionError  # noqa: E402


# ---------------------------------------------------------------------------
# Reuse harness-engineering's canonical typed-exception vocabulary
# (error_boundary.py) for diagnostic classification instead of a bare
# `except Exception` — per EX-001 remediation (adr-ase-001.md). Deliberately
# does NOT import error_boundary.TimeoutError: since Python 3.10,
# concurrent.futures.TimeoutError *is* the builtin TimeoutError (verified:
# `concurrent.futures.TimeoutError is builtins.TimeoutError` == True), while
# error_boundary.TimeoutError is a distinct, unrelated class that happens to
# share the same name. Importing it bare here would shadow the name
# `_call_with_hard_timeout` actually raises and silently stop matching it —
# a correctness bug, not a style issue. The canonical timeout name at every
# call site in this module stays the fully-qualified
# `concurrent.futures.TimeoutError`, since that is what the watchdog raises;
# error_boundary.TimeoutError remains scoped to its documented domain
# (SafeModelCall/SafeToolCall's LLM-provider calls).
# ---------------------------------------------------------------------------

_HARNESS_ENGINEERING_ROOT = Path(__file__).resolve().parents[2] / "harness-engineering"
if str(_HARNESS_ENGINEERING_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ENGINEERING_ROOT))
from implementations.error_boundary import ValidationError, ServiceUnavailableError  # noqa: E402


# ---------------------------------------------------------------------------
# qdrant-client is a heavy, optional dependency (mirrors
# retrieval-augmented-generation/CLAUDE.md: "install only when actively
# needed"). When it isn't installed, fall back to minimal structural shims
# with the same constructor signatures so this module's logic — and the
# lightweight test suite, which injects a MagicMock client and must never
# require a live qdrant-memory instance or the real library — still exercises
# the real upsert/search/filter-building code paths.
# ---------------------------------------------------------------------------

try:
    from qdrant_client.models import (  # type: ignore
        Distance,
        FieldCondition,
        Filter,
        MatchAny,
        MatchValue,
        PointStruct,
        VectorParams,
    )
except ImportError:
    @dataclass
    class Distance:  # type: ignore[no-redef]
        COSINE = "Cosine"

    @dataclass
    class VectorParams:  # type: ignore[no-redef]
        size: int
        distance: Any

    @dataclass
    class PointStruct:  # type: ignore[no-redef]
        id: str
        vector: List[float]
        payload: Dict[str, Any]

    @dataclass
    class MatchValue:  # type: ignore[no-redef]
        value: Any

    @dataclass
    class MatchAny:  # type: ignore[no-redef]
        any: List[Any]

    @dataclass
    class FieldCondition:  # type: ignore[no-redef]
        key: str
        match: Any

    @dataclass
    class Filter:  # type: ignore[no-redef]
        must: List[Any]


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

def _now() -> float:
    return time.time()


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def _parse_iso(s: str) -> float:
    return datetime.fromisoformat(s).timestamp()


def _new_id() -> str:
    return str(uuid.uuid4())


# Reflections use a human-readable, investigator-chosen reflection_id
# (e.g. "REFLECT-001") as their primary identifier throughout this module
# and in reflection_authoring.py -- but Qdrant point IDs must be an unsigned
# integer or a UUID (discovered live during the MISTAKE-2026-07-14-001
# Phase 3 migration: a raw "REFLECT-001" point ID was rejected with a 400).
# Deriving a deterministic UUID5 from reflection_id (fixed namespace) keeps
# upserts idempotent -- the same reflection_id always maps to the same
# point, matching the existing disaster-recovery contract for the other
# three memory types -- while reflection_id itself stays the reflection's
# real identity, carried in the payload.
_REFLECTION_POINT_ID_NAMESPACE = uuid.UUID("a3f6e2d4-6f74-4865-b265-666c65637400")


def _reflection_point_id(reflection_id: str) -> str:
    return str(uuid.uuid5(_REFLECTION_POINT_ID_NAMESPACE, reflection_id))


def _diag(msg: str) -> None:
    """Unbuffered, timestamped stderr line. Each Qdrant call in this module
    logs before/after so a stalled log tail (a "calling..." line with no
    matching "returned") identifies exactly which round-trip never came
    back — a stuck native call is otherwise invisible, since it never raises."""
    print(f"[DIAG {time.time():.3f}] {msg}", file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Hard client-side watchdog. A Qdrant round-trip can block indefinitely in
# a native OS-level read() that QdrantClient's own `timeout=` parameter
# does not always enforce. A caught exception can't fix this — the
# call never raises, it just never returns. The only way to bound a call that
# won't honor its own timeout is to run it in a disposable thread and stop
# *waiting* on it after QDRANT_CALL_TIMEOUT_S, regardless of whether the
# underlying thread itself ever finishes. That thread is intentionally
# leaked on timeout (Python cannot force-kill a thread blocked in a native
# syscall) — the guarantee this provides is bounded caller latency, not
# resource reclamation. Every Qdrant call site in this module goes through
# this wrapper so no code path can hang the calling MCP tool indefinitely.
# ---------------------------------------------------------------------------

QDRANT_CALL_TIMEOUT_S = 8.0


def _call_with_hard_timeout(fn: Callable[[], Any], timeout: float = QDRANT_CALL_TIMEOUT_S) -> Any:
    """Runs fn() in a throwaway daemon thread; raises
    concurrent.futures.TimeoutError if it hasn't returned within `timeout`
    seconds, regardless of fn's own internal timeout handling. See
    module-level comment above for why this exists — every call site here
    already treats TimeoutError as just another degradation case, same as
    any other Exception.

    Deliberately NOT built on concurrent.futures.ThreadPoolExecutor: that
    class registers an atexit hook that joins every worker thread it has ever
    created at interpreter shutdown, regardless of shutdown(wait=False) — a
    hung call correctly raises TimeoutError and returns control, but the
    *process* then hangs indefinitely at exit anyway, defeating the whole
    point. A raw daemon=True thread has no such hook: the interpreter does
    not wait for daemon threads at shutdown, so a leaked thread here can only
    ever leak memory/a stuck OS handle, never block the caller or the process.
    """
    result_queue: "queue.Queue[Tuple[str, Any]]" = queue.Queue(maxsize=1)

    def _runner() -> None:
        try:
            result_queue.put(("ok", fn()))
        except Exception as exc:  # forwarded to and re-raised in the caller's thread
            result_queue.put(("error", exc))

    threading.Thread(target=_runner, daemon=True, name="qdrant-call-watchdog").start()
    try:
        kind, payload = result_queue.get(timeout=timeout)
    except queue.Empty:
        raise concurrent.futures.TimeoutError(f"call did not return within {timeout}s") from None
    if kind == "error":
        raise payload
    return payload


# ---------------------------------------------------------------------------
# Collection / schema constants
# ---------------------------------------------------------------------------

COLLECTION_BY_TYPE: Dict[str, str] = {
    "episodic": "memory_episodic",
    "semantic": "memory_semantic",
    "procedural": "memory_procedural",
    "reflection": "memory_reflection",
}
MEMORY_COLLECTIONS: List[str] = list(COLLECTION_BY_TYPE.values())
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2's output vector dimension

DEFAULT_MEMORY_ROOT = Path(__file__).resolve().parents[1] / "memory"


# ---------------------------------------------------------------------------
# Write-time importance heuristic — cheap, non-LLM scoring assigned by event type
# ---------------------------------------------------------------------------

_WRITE_TIME_IMPORTANCE: Dict[str, float] = {
    "decision": 1.0,
    "commitment": 1.0,
    "correction": 0.7,
    "preference": 0.7,
    "task_complete": 0.3,
    "error": 0.3,
    "general": 0.2,
}
DEFAULT_WRITE_TIME_IMPORTANCE = 0.2


def compute_write_time_importance(event_type: str) -> float:
    """
    Cheap, non-LLM importance heuristic assigned at write time so the synchronous
    write path stays fast — no LLM call sits on the critical path of a single
    agent turn. A richer LLM-judged reassessment is reserved for the batch
    maintenance pass (see implementations/memory_maintenance.py), not this path.
    """
    return _WRITE_TIME_IMPORTANCE.get(event_type, DEFAULT_WRITE_TIME_IMPORTANCE)


# ---------------------------------------------------------------------------
# MemoryRecord — the shared payload schema for all three memory collections
# ---------------------------------------------------------------------------

@dataclass
class MemoryRecord:
    """One point's worth of payload, shared across all three memory collections."""

    id: str
    memory_type: str  # "episodic" | "semantic" | "procedural"
    content: str
    created_at: float
    last_accessed_at: float
    access_count: int = 0
    importance: float = DEFAULT_WRITE_TIME_IMPORTANCE
    confidence: float = 1.0
    decay_weight: float = 1.0
    status: str = "active"  # "active" | "dormant" | "archived"
    source_session_id: Optional[str] = None
    source_turn: int = 0
    sacred: bool = False
    tags: List[str] = field(default_factory=list)
    consolidated_from: List[str] = field(default_factory=list)
    modality: str = "text"  # "text" | "image" | "audio"
    media_ref: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        """Serialise every field to a JSON-safe dict for JSONL/Qdrant payload storage."""
        return {
            "id": self.id,
            "memory_type": self.memory_type,
            "content": self.content,
            "created_at": _iso(self.created_at),
            "last_accessed_at": _iso(self.last_accessed_at),
            "access_count": self.access_count,
            "importance": self.importance,
            "confidence": self.confidence,
            "decay_weight": self.decay_weight,
            "status": self.status,
            "source_session_id": self.source_session_id,
            "source_turn": self.source_turn,
            "sacred": self.sacred,
            "tags": list(self.tags),
            "consolidated_from": list(self.consolidated_from),
            "modality": self.modality,
            "media_ref": self.media_ref,
        }

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "MemoryRecord":
        return cls(
            id=payload["id"],
            memory_type=payload["memory_type"],
            content=payload["content"],
            created_at=_parse_iso(payload["created_at"]),
            last_accessed_at=_parse_iso(payload["last_accessed_at"]),
            access_count=payload.get("access_count", 0),
            importance=payload.get("importance", DEFAULT_WRITE_TIME_IMPORTANCE),
            confidence=payload.get("confidence", 1.0),
            decay_weight=payload.get("decay_weight", 1.0),
            status=payload.get("status", "active"),
            source_session_id=payload.get("source_session_id"),
            source_turn=payload.get("source_turn", 0),
            sacred=payload.get("sacred", False),
            tags=list(payload.get("tags", [])),
            consolidated_from=list(payload.get("consolidated_from", [])),
            modality=payload.get("modality", "text"),
            media_ref=payload.get("media_ref"),
        )

    def to_jsonl_line(self) -> str:
        return json.dumps(self.to_payload(), ensure_ascii=False)

    @classmethod
    def from_jsonl_line(cls, line: str) -> "MemoryRecord":
        return cls.from_payload(json.loads(line))


# ---------------------------------------------------------------------------
# JSONL log — the durable, append-only source of truth
# ---------------------------------------------------------------------------

class JSONLMemoryLog:
    """
    Append-only log, one file per session for episodic, one file each for
    semantic/procedural, mirroring:

        core-component-00/engineering/context-engineering/memory/
        ├── episodic/<session_id>.jsonl
        ├── semantic.jsonl
        ├── procedural.jsonl
        ├── reflection/reflection-log.jsonl
        └── memory-sync-state.json

    Reflections use a single cross-session file
    (reflection/reflection-log.jsonl), not one file per session — unlike
    episodic memory, reflections are inherently cross-session by nature
    (02-storage-specification.md §2.1). They also carry a distinct payload
    shape (the full ReflectionRecord, not MemoryRecord — see
    01-technical-options.md §2), so they are read/written via
    append_reflection()/read_all_reflections() rather than the generic
    append()/read_all() used by the other three memory types.
    """

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = Path(root_dir) if root_dir else DEFAULT_MEMORY_ROOT
        self.root_dir.mkdir(parents=True, exist_ok=True)
        (self.root_dir / "episodic").mkdir(parents=True, exist_ok=True)
        (self.root_dir / "reflection").mkdir(parents=True, exist_ok=True)

    def _path_for(self, memory_type: str, session_id: Optional[str] = None) -> Path:
        if memory_type == "episodic":
            if not session_id:
                raise ValueError("session_id is required to address the episodic log")
            return self.root_dir / "episodic" / f"{session_id}.jsonl"
        if memory_type == "semantic":
            return self.root_dir / "semantic.jsonl"
        if memory_type == "procedural":
            return self.root_dir / "procedural.jsonl"
        raise ValueError(f"Unknown memory_type: {memory_type}")

    def append(self, record: MemoryRecord) -> None:
        path = self._path_for(record.memory_type, record.source_session_id)
        with open(path, "a", encoding="utf-8") as f:
            f.write(record.to_jsonl_line() + "\n")

    def read_all(self, memory_type: str, session_id: Optional[str] = None) -> List[MemoryRecord]:
        path = self._path_for(memory_type, session_id)
        if not path.exists():
            return []
        records: List[MemoryRecord] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(MemoryRecord.from_jsonl_line(line))
        return records

    def read_all_episodic_sessions(self) -> List[MemoryRecord]:
        """Replay every episodic session file — used by rebuild and consolidation."""
        episodic_dir = self.root_dir / "episodic"
        records: List[MemoryRecord] = []
        for path in sorted(episodic_dir.glob("*.jsonl")):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(MemoryRecord.from_jsonl_line(line))
        return records

    def episodic_sessions_by_id(self) -> Dict[str, List[MemoryRecord]]:
        """Same as read_all_episodic_sessions() but grouped by session_id — the
        shape run_consolidation_pass() (memory_maintenance.py) expects."""
        episodic_dir = self.root_dir / "episodic"
        grouped: Dict[str, List[MemoryRecord]] = {}
        for path in sorted(episodic_dir.glob("*.jsonl")):
            session_id = path.stem
            grouped[session_id] = self.read_all("episodic", session_id)
        return grouped

    def _reflection_path(self) -> Path:
        return self.root_dir / "reflection" / "reflection-log.jsonl"

    def append_reflection(self, record: "ReflectionRecord") -> None:
        """Append one reflection to the single cross-session
        reflection-log.jsonl source-of-truth log (02-storage-specification.md
        §2.1). Serialises via record.to_dict() — the full ReflectionRecord
        payload, verbatim, not the generic MemoryRecord shape used by the
        other three memory types."""
        with open(self._reflection_path(), "a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")

    def read_all_reflections(self) -> List[Dict[str, Any]]:
        """Replay reflection-log.jsonl. Returns raw payload dicts (not
        ReflectionRecord instances) so this module never needs a runtime
        import of memory_store.ReflectionRecord — callers that need
        ReflectionRecord instances construct them via
        ReflectionRecord.from_dict() (implementations/memory_store.py)."""
        path = self._reflection_path()
        if not path.exists():
            return []
        records: List[Dict[str, Any]] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records


# ---------------------------------------------------------------------------
# Memory-sync state — rebuild/consolidation bookkeeping, not a hook dispatcher
# ---------------------------------------------------------------------------

class MemorySyncState:
    """
    Records the last successful batch-rebuild timestamp and point count per
    collection. Unlike rag-sync-state.json this is NOT a hook dispatch mechanism —
    every memory write happens synchronously, inline with the write call, so
    there's no async dispatch to debounce or coordinate via IPC state.

    Also records a single top-level `last_consolidation_at` timestamp — the last
    time the maintenance job (memory_maintenance.run_maintenance_pass) completed
    a pass — surfaced by the health_check MCP tool's
    `memory_instance.last_consolidation_at` field.
    """

    def __init__(self, root_dir: Optional[Path] = None):
        base = Path(root_dir) if root_dir else DEFAULT_MEMORY_ROOT
        self.path = base / "memory-sync-state.json"

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            state: Dict[str, Any] = {
                name: {"last_rebuild_at": 0, "point_count": 0} for name in MEMORY_COLLECTIONS
            }
            state["last_consolidation_at"] = None
            return state
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, state: Dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def record_rebuild(self, collection_name: str, point_count: int, now: Optional[float] = None) -> None:
        state = self.load()
        state.setdefault(collection_name, {})
        state[collection_name]["last_rebuild_at"] = now if now is not None else _now()
        state[collection_name]["point_count"] = point_count
        self.save(state)

    def record_consolidation(self, now: Optional[float] = None) -> None:
        """Record that a maintenance pass completed, regardless of whether it
        produced any new consolidated records — last_consolidation_at means
        'the last maintenance pass ran,' not 'the last pass that consolidated
        something.'"""
        state = self.load()
        state["last_consolidation_at"] = now if now is not None else _now()
        self.save(state)

    def get_last_consolidation_at(self) -> Optional[float]:
        return self.load().get("last_consolidation_at")


# ---------------------------------------------------------------------------
# Qdrant-backed derived index — one instance per collection
# ---------------------------------------------------------------------------

class QdrantMemoryIndex:
    """
    Injectable Qdrant-backed index for one memory collection. Mirrors the DI
    pattern used by RAGPipeline: client and embedder are injected, so this class
    is fully unit-testable with mocks and never requires a live qdrant-memory
    instance (http://localhost:6335) in tests.

    Every method degrades gracefully (returns False/[]/0, logs a stderr warning)
    rather than raising when the client or embedder is absent or a call fails —
    the JSONL log is already durable by the time this class is ever invoked.
    """

    def __init__(
        self,
        memory_type: str,
        client: Any = None,
        embedder: Optional[Callable[[str], List[float]]] = None,
        dim: int = EMBEDDING_DIM,
    ):
        if memory_type not in COLLECTION_BY_TYPE:
            raise ValueError(f"Unknown memory_type: {memory_type}")
        self.memory_type = memory_type
        self.collection_name = COLLECTION_BY_TYPE[memory_type]
        self.client = client
        self.embedder = embedder
        self.dim = dim

    def ensure_collection(self) -> None:
        """Create the collection if missing. No-op without a client."""
        if self.client is None:
            return
        try:
            existing = [c.name for c in _call_with_hard_timeout(self.client.get_collections).collections]
            if self.collection_name not in existing:
                _call_with_hard_timeout(
                    lambda: self.client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=VectorParams(size=self.dim, distance=Distance.COSINE),
                    )
                )
        except concurrent.futures.TimeoutError:
            print(
                f"WARNING: Qdrant collection ensure TIMED OUT after {QDRANT_CALL_TIMEOUT_S}s for '{self.collection_name}'",
                file=sys.stderr,
            )
        except (ConnectionError, OSError) as exc:
            print(
                f"WARNING [{ServiceUnavailableError.__name__}]: Qdrant unreachable while ensuring "
                f"collection '{self.collection_name}': {exc}",
                file=sys.stderr,
            )
        except (AttributeError, TypeError, KeyError) as exc:
            print(
                f"WARNING [{ValidationError.__name__}]: malformed Qdrant response while ensuring "
                f"collection '{self.collection_name}': {exc}",
                file=sys.stderr,
            )
        except Exception as exc:
            print(
                f"WARNING: could not ensure Qdrant collection '{self.collection_name}': {exc}",
                file=sys.stderr,
            )

    def upsert_record(self, record: MemoryRecord) -> bool:
        """
        Embed and upsert one MemoryRecord-shaped record (episodic/semantic/
        procedural). Returns True on success, False on graceful degradation —
        the caller (PersistentMemorySink) treats False as "the JSONL log
        already has it, Qdrant is temporarily behind," never as a write
        failure. Thin wrapper over upsert_payload(); see that method for the
        reflection-collection case, whose payload is not MemoryRecord-shaped.
        """
        return self.upsert_payload(record.id, record.content, record.to_payload())

    def upsert_payload(self, point_id: str, embed_text: str, payload: Dict[str, Any]) -> bool:
        """
        Embed `embed_text` and upsert `payload` verbatim as the point's
        payload, keyed by `point_id`. upsert_record() wraps this for the
        MemoryRecord-shaped collections (episodic/semantic/procedural);
        memory_reflection writes go through this method directly, since a
        ReflectionRecord's payload is the full record verbatim
        (01-technical-options.md §2: "Payload fields: All ReflectionRecord
        fields verbatim"), not a MemoryRecord. Returns True on success, False
        on graceful degradation — same contract as upsert_record().
        """
        if self.client is None or self.embedder is None:
            return False
        try:
            vector = self.embedder(embed_text)
            _call_with_hard_timeout(
                lambda: self.client.upsert(
                    collection_name=self.collection_name,
                    points=[PointStruct(id=point_id, vector=vector, payload=payload)],
                )
            )
            return True
        except concurrent.futures.TimeoutError:
            print(
                f"WARNING: Qdrant upsert TIMED OUT after {QDRANT_CALL_TIMEOUT_S}s for '{self.collection_name}'",
                file=sys.stderr,
            )
            return False
        except (ConnectionError, OSError) as exc:
            print(
                f"WARNING [{ServiceUnavailableError.__name__}]: Qdrant unreachable during upsert "
                f"for '{self.collection_name}': {exc}",
                file=sys.stderr,
            )
            return False
        except (AttributeError, TypeError, KeyError, ValueError) as exc:
            print(
                f"WARNING [{ValidationError.__name__}]: malformed record or response during Qdrant "
                f"upsert for '{self.collection_name}': {exc}",
                file=sys.stderr,
            )
            return False
        except Exception as exc:
            print(f"WARNING: Qdrant upsert failed for '{self.collection_name}': {exc}", file=sys.stderr)
            return False

    def search(
        self,
        query_text: str,
        top_k: int = 5,
        status_in: Tuple[str, ...] = ("active",),
        session_id: Optional[str] = None,
    ) -> List[MemoryRecord]:
        """
        Semantic similarity search over this collection. Returns [] on any
        degradation rather than raising — callers should treat an empty result as
        "fall back to BM25/raw-scan," per the existing four-tier degradation stack.
        """
        if self.client is None or self.embedder is None:
            return []
        try:
            _diag(f"search: embedding query (collection={self.collection_name!r})")
            vector = self.embedder(query_text)
            _diag(f"search: embedded, calling client.query_points(collection={self.collection_name!r}) (hard-timeout guarded)")
            must = [FieldCondition(key="status", match=MatchAny(any=list(status_in)))]
            if session_id is not None:
                must.append(FieldCondition(key="source_session_id", match=MatchValue(value=session_id)))
            response = _call_with_hard_timeout(
                lambda: self.client.query_points(
                    collection_name=self.collection_name,
                    query=vector,
                    query_filter=Filter(must=must),
                    limit=top_k,
                    with_payload=True,
                )
            )
            _diag(f"search: query_points returned (collection={self.collection_name!r})")
            points = getattr(response, "points", response)
            return [MemoryRecord.from_payload(p.payload) for p in points]
        except concurrent.futures.TimeoutError:
            _diag(f"search: TIMED OUT after {QDRANT_CALL_TIMEOUT_S}s (collection={self.collection_name!r})")
            return []
        except (ConnectionError, OSError) as exc:
            _diag(f"search: unreachable (collection={self.collection_name!r}): {exc}")
            print(
                f"WARNING [{ServiceUnavailableError.__name__}]: Qdrant unreachable during search "
                f"for '{self.collection_name}': {exc}",
                file=sys.stderr,
            )
            return []
        except (AttributeError, TypeError, KeyError) as exc:
            _diag(f"search: malformed response (collection={self.collection_name!r}): {exc}")
            print(
                f"WARNING [{ValidationError.__name__}]: malformed Qdrant response during search "
                f"for '{self.collection_name}': {exc}",
                file=sys.stderr,
            )
            return []
        except Exception as exc:
            _diag(f"search: failed (collection={self.collection_name!r}): {exc}")
            print(f"WARNING: Qdrant search failed for '{self.collection_name}': {exc}", file=sys.stderr)
            return []

    def count_points(self, status: Optional[str] = None) -> int:
        """
        Point count for this collection, optionally filtered by `status`
        ("active" | "dormant" | "archived"). Returns 0 on any degradation (no
        client, connection failure) rather than raising — mirrors this class's
        other methods, which treat a Qdrant hiccup as "report zero," never as a
        fatal error. Backs the health_check MCP tool's
        `memory_instance.point_counts` and `dormant_ratio` fields.
        """
        if self.client is None:
            return 0
        try:
            count_filter = None
            if status is not None:
                count_filter = Filter(must=[FieldCondition(key="status", match=MatchValue(value=status))])
            _diag(f"count_points: calling client.count(collection={self.collection_name!r}, status={status!r}) (hard-timeout guarded)")
            result = _call_with_hard_timeout(
                lambda: self.client.count(
                    collection_name=self.collection_name, count_filter=count_filter, exact=True
                )
            )
            _diag(f"count_points: returned (collection={self.collection_name!r}, status={status!r}, count={result.count})")
            return result.count
        except concurrent.futures.TimeoutError:
            _diag(f"count_points: TIMED OUT after {QDRANT_CALL_TIMEOUT_S}s (collection={self.collection_name!r}, status={status!r})")
            return 0
        except (ConnectionError, OSError) as exc:
            _diag(f"count_points: unreachable (collection={self.collection_name!r}, status={status!r}): {exc}")
            print(
                f"WARNING [{ServiceUnavailableError.__name__}]: Qdrant unreachable during count "
                f"for '{self.collection_name}': {exc}",
                file=sys.stderr,
            )
            return 0
        except (AttributeError, TypeError, KeyError) as exc:
            _diag(f"count_points: malformed response (collection={self.collection_name!r}, status={status!r}): {exc}")
            print(
                f"WARNING [{ValidationError.__name__}]: malformed Qdrant response during count "
                f"for '{self.collection_name}': {exc}",
                file=sys.stderr,
            )
            return 0
        except Exception as exc:
            _diag(f"count_points: failed (collection={self.collection_name!r}, status={status!r}): {exc}")
            print(f"WARNING: Qdrant count failed for '{self.collection_name}': {exc}", file=sys.stderr)
            return 0

    def rebuild_from_log(self, log: JSONLMemoryLog, sync_state: Optional[MemorySyncState] = None) -> int:
        """
        Batch-replay every record for this collection's memory_type from the JSONL
        log into Qdrant — the disaster-recovery path when a collection is lost or
        corrupted. Recovery always means a full replay from the log, never
        point-level repair inside Qdrant.
        """
        self.ensure_collection()
        if self.memory_type == "episodic":
            records = log.read_all_episodic_sessions()
            count = sum(1 for record in records if self.upsert_record(record))
        elif self.memory_type == "reflection":
            payloads = log.read_all_reflections()
            count = sum(
                1
                for payload in payloads
                if self.upsert_payload(
                    _reflection_point_id(payload["reflection_id"]),
                    f"{payload['summary']} {payload['scope_of_applicability']}",
                    payload,
                )
            )
        else:
            records = log.read_all(self.memory_type)
            count = sum(1 for record in records if self.upsert_record(record))

        if sync_state is not None:
            sync_state.record_rebuild(self.collection_name, count)
        return count


# ---------------------------------------------------------------------------
# Observability — shared formula + aggregation for the health_check MCP tool's
# memory_instance block. Reused by both memory_maintenance.run_maintenance_pass
# (per-pass dormant_ratio, scoped to the records batch it just decayed) and
# compute_memory_instance_telemetry below (corpus-wide dormant_ratio, scoped to
# the live qdrant-memory collections) — one formula, two call sites, so the two
# numbers can never drift apart from using different math.
# ---------------------------------------------------------------------------

def compute_dormant_ratio(dormant_count: int, total_count: int) -> float:
    """Fraction of points with status="dormant" out of `total_count`. Returns
    0.0 for an empty corpus/batch rather than dividing by zero."""
    return (dormant_count / total_count) if total_count else 0.0


def check_reachable(client: Any) -> bool:
    """
    Connectivity check against a Qdrant instance. Never raises — a None client
    (not provisioned/not injected) or a failed round-trip both report False,
    which health_check surfaces as `memory_instance.reachable`. No live
    qdrant-memory instance is required for this to be exercised in tests: pass
    a MagicMock (success) or a MagicMock configured to raise (failure).
    """
    if client is None:
        return False
    try:
        _diag("check_reachable: calling client.get_collections() (hard-timeout guarded)")
        _call_with_hard_timeout(client.get_collections)
        _diag("check_reachable: returned")
        return True
    except concurrent.futures.TimeoutError:
        _diag(f"check_reachable: TIMED OUT after {QDRANT_CALL_TIMEOUT_S}s (call still running in a leaked thread)")
        return False
    except (ConnectionError, OSError) as exc:
        # No response body is parsed here (a bare connectivity ping), so unlike
        # the other methods above there is no separate malformed-response case
        # to distinguish — only timeout vs. unreachable vs. last-resort.
        _diag(f"check_reachable: unreachable [{ServiceUnavailableError.__name__}]: {exc}")
        return False
    except Exception as exc:
        _diag(f"check_reachable: failed: {exc}")
        return False


def compute_memory_instance_telemetry(
    client: Any,
    indices: Dict[str, "QdrantMemoryIndex"],
    sync_state: Optional["MemorySyncState"] = None,
) -> Dict[str, Any]:
    """
    Assemble the `memory_instance` health_check block: `reachable`,
    per-collection `point_counts`, `last_consolidation_at` (ISO 8601 UTC), and
    a corpus-wide `dormant_ratio`.

    `client` is the shared qdrant-memory QdrantClient injected into each entry
    of `indices` — used only for the reachability ping, so a caller that has no
    live client can still pass one index's underlying client (or None).
    `indices` maps memory_type ("episodic" | "semantic" | "procedural") to its
    QdrantMemoryIndex. This block must be reported separately from any
    document-knowledge-base health block — the two Qdrant instances are
    independent (separate containers, separate ports, separate failure
    domains) and are never collapsed into one combined status.
    """
    point_counts: Dict[str, int] = {}
    total_points = 0
    total_dormant = 0
    for index in indices.values():
        count = index.count_points()
        point_counts[index.collection_name] = count
        total_points += count
        total_dormant += index.count_points(status="dormant")

    last_consolidation_at: Optional[str] = None
    if sync_state is not None:
        ts = sync_state.get_last_consolidation_at()
        if ts is not None:
            last_consolidation_at = _iso(ts)

    return {
        "reachable": check_reachable(client),
        "point_counts": point_counts,
        "last_consolidation_at": last_consolidation_at,
        "dormant_ratio": compute_dormant_ratio(total_dormant, total_points),
    }


# ---------------------------------------------------------------------------
# Write-through orchestrator — injected into EpisodicMemory / SemanticMemory /
# ProceduralMemory as their optional `sink` (see memory_store.py)
# ---------------------------------------------------------------------------

class PersistentMemorySink:
    """
    Implements the synchronous write path:

        append JSONL line (source of truth)
            -> embed content
            -> upsert to the type-scoped Qdrant collection
            -> return to caller

    The JSONL append is the only step allowed to be load-bearing for the caller;
    a Qdrant hiccup degrades to "index is stale until the next rebuild," never to
    a lost write or a raised exception back into the agent turn.
    """

    def __init__(
        self,
        log: Optional[JSONLMemoryLog] = None,
        indices: Optional[Dict[str, QdrantMemoryIndex]] = None,
    ):
        self.log = log or JSONLMemoryLog()
        self.indices = indices or {}

    def _write(self, record: MemoryRecord) -> MemoryRecord:
        self.log.append(record)
        index = self.indices.get(record.memory_type)
        if index is not None:
            index.upsert_record(record)
        return record

    def write_episodic(self, event: "EpisodicEvent", session_id: str) -> MemoryRecord:
        importance = 1.0 if event.sacred else compute_write_time_importance(event.event_type)
        record = MemoryRecord(
            id=_new_id(),
            memory_type="episodic",
            content=event.content,
            created_at=event.timestamp,
            last_accessed_at=event.timestamp,
            access_count=0,
            importance=importance,
            confidence=1.0,
            decay_weight=1.0,
            status="active",
            source_session_id=session_id,
            source_turn=event.turn,
            sacred=event.sacred,
            tags=[event.event_type],
        )
        return self._write(record)

    def write_semantic(self, fact: "SemanticFact", importance: float = 0.5) -> MemoryRecord:
        record = MemoryRecord(
            id=_new_id(),
            memory_type="semantic",
            content=f"{fact.key}: {fact.value}",
            created_at=fact.created_at,
            last_accessed_at=fact.created_at,
            access_count=0,
            importance=importance,
            confidence=fact.confidence,
            decay_weight=1.0,
            status="active",
            source_session_id=None,
            source_turn=0,
            sacred=False,
            tags=list(fact.tags),
        )
        return self._write(record)

    def write_procedural(
        self,
        skill_name: str,
        instruction: str,
        source_session_id: Optional[str] = None,
        importance: float = 0.5,
    ) -> MemoryRecord:
        now = _now()
        record = MemoryRecord(
            id=_new_id(),
            memory_type="procedural",
            content=f"{skill_name}: {instruction}",
            created_at=now,
            last_accessed_at=now,
            access_count=0,
            importance=importance,
            confidence=1.0,
            decay_weight=1.0,
            status="active",
            source_session_id=source_session_id,
            source_turn=0,
            sacred=False,
            tags=[skill_name],
        )
        return self._write(record)

    def write_reflection(
        self, record: "ReflectionRecord", identity: "IdentityVerification"
    ) -> "ReflectionRecord":
        """
        Write-through for the fourth memory type (reflections). Same
        JSONL-first-then-Qdrant-upsert pattern as write_episodic/
        write_semantic/write_procedural (append is the only step allowed to
        be load-bearing; a Qdrant hiccup degrades, never raises), but a
        ReflectionRecord keeps its own shape end-to-end rather than being
        wrapped in MemoryRecord — the payload stored is the full
        ReflectionRecord, verbatim (01-technical-options.md §2), and the
        embedded text is `summary` + `scope_of_applicability` (the two
        fields most predictive of retrieval relevance), not a generic
        `content` field.

        Never called from an agent-callable surface — only from the
        Investigator-Authored Write Path
        (implementations/reflection_authoring.py), per the design's explicit
        rejection of an MCP write tool (01-technical-options.md §4,
        "Option A" rejected).

        Identity gate (MISTAKE-2026-07-16-001 remediation item 2, second
        Wieczorek pass): requires the same IdentityVerification token
        ReflectionMemory.record_reflection() requires, and independently
        re-checks it here rather than trusting that the caller already did
        — this is defense-in-depth against a caller who constructs a bare
        ReflectionRecord and calls this method directly, bypassing
        ReflectionMemory (and therefore record_reflection()'s own gate)
        entirely, which is exactly the second live bypass Dr. Wieczorek
        demonstrated. Honest limitation, same as everywhere else this token
        is checked: this is not a floor. JSONLMemoryLog.append_reflection()
        and QdrantMemoryIndex.upsert_payload() remain directly callable
        beneath this method with no check of any kind — per
        03-deployment-guidelines.md's revised Phase 1 gate, the actual
        security boundary for GOVERNANCE_TRIGGERS records is procedural
        (live human confirmation in the coordinating session), not this or
        any other code layer.

        Raises:
            UnverifiedReflectionError: if `identity` is not a genuine
                IdentityVerification, was issued for a different logged_by
                than `record.logged_by`, or (for GOVERNANCE_TRIGGERS trigger
                types only) does not carry a governance_confirmation
                matching `record.reflection_id`.
        """
        if not isinstance(identity, IdentityVerification):
            raise UnverifiedReflectionError(
                "PersistentMemorySink.write_reflection() requires a verified "
                "IdentityVerification token — refusing to persist a "
                "ReflectionRecord without one, regardless of whether the "
                "caller went through ReflectionMemory.record_reflection() "
                "first."
            )
        if identity.logged_by != record.logged_by:
            raise UnverifiedReflectionError(
                f"IdentityVerification was issued for logged_by="
                f"{identity.logged_by!r}, not {record.logged_by!r} — refusing "
                "to persist under a mismatched identity."
            )
        if (
            record.trigger_type in GOVERNANCE_TRIGGERS
            and identity.governance_confirmation != record.reflection_id
        ):
            raise UnverifiedReflectionError(
                f"GOVERNANCE_TRIGGERS record {record.reflection_id!r} requires "
                "an IdentityVerification carrying a governance_confirmation "
                "matching this exact reflection_id — refusing to persist."
            )

        self.log.append_reflection(record)
        index = self.indices.get("reflection")
        if index is not None:
            embed_text = f"{record.summary} {record.scope_of_applicability}"
            index.upsert_payload(
                _reflection_point_id(record.reflection_id), embed_text, record.to_dict()
            )
        return record
