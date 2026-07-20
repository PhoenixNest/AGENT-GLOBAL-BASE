# ── venv bootstrap (MUST be first, before any other imports) ──────────────
import sys
import platform
from pathlib import Path as _Path

_venv = _Path(__file__).parent / ".venv"
if platform.system() == "Windows":
    _venv_sp = _venv / "Lib" / "site-packages"
else:
    _py = f"python{sys.version_info.major}.{sys.version_info.minor}"
    _venv_sp = _venv / "lib" / _py / "site-packages"
if _venv_sp.exists():
    sys.path.insert(0, str(_venv_sp))
# ─────────────────────────────────────────────────────────────────────────

import os
import threading
import time
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from fastmcp import FastMCP

# Reuses the context-engineering module's memory implementation rather than
# duplicating it — same pattern workspace-knowledge/server.py already uses
# to pull in implementations/memory_vector_store.py for its health_check tool.
_CONTEXT_ENGINEERING_ROOT = Path(__file__).resolve().parents[2] / "engineering" / "context-engineering"
if str(_CONTEXT_ENGINEERING_ROOT) not in sys.path:
    sys.path.insert(0, str(_CONTEXT_ENGINEERING_ROOT))

from implementations.memory_vector_store import (  # noqa: E402
    COLLECTION_BY_TYPE,
    MemorySyncState,
    QdrantMemoryIndex,
    _call_with_hard_timeout,
    compute_memory_instance_telemetry,
    Filter,
    FieldCondition,
    MatchAny,
)
from implementations.memory_store import ReflectionRecord  # noqa: E402
import concurrent.futures  # noqa: E402

# embedder-service client (Phase 2, telescope/2026-07-13-mcp-embedder-service-redesign).
# Same cross-module import pattern as memory_vector_store above.
_MCP_SERVERS_SHARED_ROOT = Path(__file__).resolve().parents[1] / "_shared"
if str(_MCP_SERVERS_SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(_MCP_SERVERS_SHARED_ROOT))
import embedder_client  # noqa: E402


def _diag(msg: str) -> None:
    """Unbuffered, timestamped stderr line. A blocking native call that never
    returns and never raises is invisible to a try/except — the thread simply
    never comes back to Python. This is the only way to see, after the fact,
    which of several sequential Qdrant round-trips (or the embedder-warmup
    thread's import attempts) actually stalled. Defined before the
    embedder-warmup thread is started below, since that thread calls this."""
    print(f"[DIAG {time.time():.3f}] {msg}", file=sys.stderr, flush=True)


MEMORY_QDRANT_URL = os.getenv("MEMORY_QDRANT_URL", "http://localhost:6335")
# The memory collections were created with all-MiniLM-L6-v2 (384-dim), a
# different, smaller model from workspace-knowledge's all-mpnet-base-v2
# (768-dim) — the two are not interchangeable.
#
# Standing convention (see mcp-governance.md): CC-00 MCP servers needing an
# embedding model provision it into the shared cache at
# mcp-servers/_shared/models/<slug>/ via _shared/provision_model.py, rather
# than each keeping a private per-server cache. _get_embedder() below is a
# three-tier fallback, in priority order:
#   1. Shared cache (mcp-servers/_shared/models/sentence-transformers--all-MiniLM-L6-v2/)
#   2. Hub download attempt (today's original behavior, unchanged)
#   3. None — search_memory degrades gracefully rather than failing
_SHARED_MODELS_DIR = Path(__file__).resolve().parents[1] / "_shared" / "models"
_SHARED_MODEL_SLUG = "sentence-transformers--all-MiniLM-L6-v2"

# Importing sentence_transformers pulls in torch + scipy/sklearn, taking
# anywhere from ~9s to 50+s on a cold process depending on machine state —
# far past typical MCP tool-call timeouts — and this import can also wedge
# indefinitely partway through without ever releasing CPython's import
# lock. A held import lock blocks bootstrapping of any new OS thread in the
# process, including the one QdrantClient's own constructor spawns
# internally, so an eager, always-on warmup thread starting this import at
# module-import time can stall unrelated tool calls that never needed the
# in-process embedder at all (the embedder-service path below normally
# covers that need). Loading is therefore lazy: the background thread only
# starts on-demand, the first time _get_embedder() actually needs the
# in-process fallback (see _ensure_embedder_load_started() below). Any
# search_memory call that arrives before loading finishes, or before it
# has even been triggered, degrades gracefully (embedder still None) —
# never blocks, never hangs.
#
# The load can also stall indefinitely rather than merely being slow (see
# mcp-governance.md's agent-memory row and telescope/2026-07-13-mcp-embedder-
# service-redesign/ for the investigation). _EMBEDDER_LOAD_TIMEOUT_S bounds
# each attempt well above any observed successful load time, and a stalled
# attempt is retried once in a fresh thread (the stalled thread itself is
# abandoned — _call_with_hard_timeout never waits on it) before degrading.
_EMBEDDER_LOAD_TIMEOUT_S = 60.0
_EMBEDDER_LOAD_MAX_ATTEMPTS = 2

_embedder_cache: Optional[Callable[[str], List[float]]] = None
_embedder_lock = threading.Lock()
# "not started" | "loading" | "ready" | "failed: <exc>" — distinguishes
# "never triggered", "still warming up", and "actually broken" in the
# search_memory degraded-reason message. "Not started" is the module-import
# default now that the warmup thread is lazily triggered rather than eager
# (see _ensure_embedder_load_started() below) — it must not be conflated
# with "loading", since nothing has begun importing anything yet in that
# state. "Loading" does not imply the model is missing — provisioning and
# background-thread readiness are independent; the shared cache can be
# fully correct while this state is still "loading" for an arbitrarily
# long time on a cold process.
_embedder_state: str = "not started"
_embedder_load_started = False


def _import_and_build_embedder() -> Callable[[str], List[float]]:
    from sentence_transformers import SentenceTransformer

    cached_model_dir = _SHARED_MODELS_DIR / _SHARED_MODEL_SLUG
    if cached_model_dir.exists():
        model = SentenceTransformer(str(cached_model_dir))
    else:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return lambda text: model.encode([text])[0].tolist()  # noqa: E731


def _load_embedder_background() -> None:
    global _embedder_cache, _embedder_state
    for attempt in range(1, _EMBEDDER_LOAD_MAX_ATTEMPTS + 1):
        _diag(f"embedder-warmup: attempt {attempt}/{_EMBEDDER_LOAD_MAX_ATTEMPTS} starting")
        try:
            embedder = _call_with_hard_timeout(
                _import_and_build_embedder, timeout=_EMBEDDER_LOAD_TIMEOUT_S
            )
        except concurrent.futures.TimeoutError:
            _diag(f"embedder-warmup: attempt {attempt} TIMED OUT after {_EMBEDDER_LOAD_TIMEOUT_S}s")
            if attempt < _EMBEDDER_LOAD_MAX_ATTEMPTS:
                continue
            with _embedder_lock:
                _embedder_state = (
                    f"failed: import did not complete within {_EMBEDDER_LOAD_TIMEOUT_S}s "
                    f"across {_EMBEDDER_LOAD_MAX_ATTEMPTS} attempts"
                )
            return
        except Exception as exc:
            _diag(f"embedder-warmup: attempt {attempt} failed: {exc}")
            with _embedder_lock:
                _embedder_state = f"failed: {exc}"
            return
        else:
            _diag(f"embedder-warmup: attempt {attempt} succeeded")
            with _embedder_lock:
                _embedder_cache = embedder
                _embedder_state = "ready"
            return
        # _get_embedder() keeps returning None on any non-return path above; search_memory degrades gracefully


def _ensure_embedder_load_started() -> None:
    """
    Starts the in-process embedder-warmup thread on first need instead of
    unconditionally at module-import time. The import chain this thread
    runs (sentence_transformers -> scipy.sparse.linalg) can wedge
    indefinitely without releasing CPython's import lock, and a held
    import lock blocks bootstrapping of any new OS thread in the process —
    including the one QdrantClient's constructor spawns internally.
    Triggering the thread only from _get_embedder(), and only when the
    embedder-service path is not ready, keeps this fragile import chain
    from ever racing against unrelated startup activity in the process.
    Idempotent — safe to call on every _get_embedder() invocation; only the
    first call per process starts the thread.
    """
    global _embedder_load_started, _embedder_state
    with _embedder_lock:
        if _embedder_load_started:
            return
        _embedder_load_started = True
        _embedder_state = "loading"
    threading.Thread(target=_load_embedder_background, daemon=True, name="embedder-warmup").start()


def _get_in_process_embedder() -> Optional[Callable[[str], List[float]]]:
    with _embedder_lock:
        return _embedder_cache


# ---------------------------------------------------------------------------
# embedder-service integration (Phase 2) — feature-flagged primary path, with
# the in-process loader above kept as an unmodified automatic fallback. The
# degrade-never-block guarantee is not weakened at any point: every failure
# mode below (flag off, service unreachable, service call fails mid-request)
# falls through to the same in-process path/degradation this module already
# had before this integration, never to a hang or a raised exception.
# ---------------------------------------------------------------------------

EMBEDDER_SERVICE_ENABLED = os.getenv("EMBEDDER_SERVICE_ENABLED", "true").strip().lower() not in (
    "0",
    "false",
    "no",
)
_EMBEDDER_SERVICE_MODEL = "all-MiniLM-L6-v2"  # matches this server's collection dimension (384)

_embedder_service_lock = threading.Lock()
# "disabled" | "starting" | "ready" | "unavailable"
_embedder_service_state: str = "starting" if EMBEDDER_SERVICE_ENABLED else "disabled"


def _start_embedder_service_background() -> None:
    global _embedder_service_state
    ok = embedder_client.ensure_service_running()
    with _embedder_service_lock:
        _embedder_service_state = "ready" if ok else "unavailable"
    _diag(f"embedder-service background start: {'ready' if ok else 'unavailable'}")


if EMBEDDER_SERVICE_ENABLED:
    threading.Thread(
        target=_start_embedder_service_background, daemon=True, name="embedder-service-warmup"
    ).start()


def _embedder_service_ready() -> bool:
    with _embedder_service_lock:
        return _embedder_service_state == "ready"


def _get_embedder() -> Optional[Callable[[str], List[float]]]:
    """
    Composite resolver: prefers the shared embedder-service when it is ready,
    falls back to the in-process loader otherwise or on a runtime failure.
    Returns None only when neither path has anything to offer right now —
    the same signal _search_memory_impl already treats as "degrade, do not
    block or raise" via embedder_unavailable_reason.
    """
    service_ready = EMBEDDER_SERVICE_ENABLED and _embedder_service_ready()
    if not service_ready:
        # Only the in-process fallback needs this fragile import chain — no
        # reason to pay its risk when the embedder-service already has us
        # covered.
        _ensure_embedder_load_started()
    in_process = _get_in_process_embedder()

    if not service_ready and in_process is None:
        return None

    def _resilient_embed(text: str) -> List[float]:
        if service_ready:
            vector = embedder_client.embed([text], model=_EMBEDDER_SERVICE_MODEL, expected_dim=384)
            if vector is not None:
                return vector[0]
            _diag("embedder-service call failed at runtime — falling back to in-process embedder")
        fallback = _get_in_process_embedder()
        if fallback is not None:
            return fallback(text)
        raise RuntimeError("embedder-service unavailable and in-process embedder not ready")

    return _resilient_embed


def _get_embedder_unavailable_reason() -> str:
    with _embedder_lock:
        in_process_state = _embedder_state
    if EMBEDDER_SERVICE_ENABLED:
        with _embedder_service_lock:
            service_state = _embedder_service_state
        return (
            f"embedding unavailable (embedder-service: {service_state}; "
            f"in-process fallback: {in_process_state})"
        )
    if in_process_state == "not started":
        return "embedding model warmup not yet triggered (in-process fallback starts lazily on first need — retry shortly)"
    if in_process_state == "loading":
        return "embedding model still loading (background warmup in progress on this server process — retry shortly)"
    if in_process_state.startswith("failed"):
        return f"embedding model failed to load ({in_process_state})"
    return "embedding model unavailable"  # unreachable in practice: "ready" implies embedder is not None


_memory_client_cache: Any = None
_memory_client_lock = threading.Lock()


def _get_memory_client() -> Any:
    """
    Returns a QdrantClient constructed once per process and cached thereafter,
    using a plain `timeout=5` — the same construction pattern
    workspace-knowledge/server.py already uses against this same qdrant-memory
    instance without incident. QdrantClient's constructor spawns its own
    background thread internally; wrapping construction in an additional
    watchdog thread does not shorten how long that internal thread takes to
    start, and only adds a second thread that can itself be starved under
    the same conditions.
    """
    global _memory_client_cache
    with _memory_client_lock:
        if _memory_client_cache is not None:
            return _memory_client_cache
        try:
            from qdrant_client import QdrantClient

            _diag("constructing QdrantClient (plain timeout=5, process-cached)...")
            _memory_client_cache = QdrantClient(url=MEMORY_QDRANT_URL, timeout=5)
            _diag("QdrantClient constructed")
        except Exception as exc:
            _diag(f"QdrantClient construction failed: {exc}")
            return None
        return _memory_client_cache


mcp = FastMCP("agent-memory")
_memory_sync_state = MemorySyncState()


def _search_reflection(
    query: str,
    top_k: int,
    statuses: List[str],
    client: Any,
    embedder: Callable[[str], List[float]],
) -> List[ReflectionRecord]:
    """
    Reflection-collection search, returning ReflectionRecord instances.

    Does not go through QdrantMemoryIndex.search() (memory_vector_store.py):
    that method unconditionally parses each point's payload via
    MemoryRecord.from_payload(), which requires the id/content/created_at/
    last_accessed_at shape the other three collections use. A
    memory_reflection point's payload is a ReflectionRecord verbatim instead
    (01-technical-options.md §2: "Payload fields: All ReflectionRecord
    fields verbatim") — MemoryRecord.from_payload() would KeyError on it, a
    failure QdrantMemoryIndex.search()'s own except clause already catches
    and degrades to [], silently returning zero results forever rather than
    real matches. This function performs the same query
    (client.query_points, same status filter, same _call_with_hard_timeout
    wrapper) and parses the response via ReflectionRecord.from_dict()
    instead — same timeout-guarded, degrade-gracefully contract, no new
    failure-mode class: every except clause here mirrors
    QdrantMemoryIndex.search()'s own exactly.
    """
    if client is None:
        return []
    collection_name = COLLECTION_BY_TYPE["reflection"]
    try:
        vector = embedder(query)
        must = [FieldCondition(key="status", match=MatchAny(any=list(statuses)))]
        response = _call_with_hard_timeout(
            lambda: client.query_points(
                collection_name=collection_name,
                query=vector,
                query_filter=Filter(must=must),
                limit=top_k,
                with_payload=True,
            )
        )
        points = getattr(response, "points", response)
        return [ReflectionRecord.from_dict(p.payload) for p in points]
    except concurrent.futures.TimeoutError:
        _diag(f"search: TIMED OUT (collection={collection_name!r})")
        return []
    except (ConnectionError, OSError) as exc:
        _diag(f"search: unreachable (collection={collection_name!r}): {exc}")
        return []
    except (AttributeError, TypeError, KeyError, ValueError) as exc:
        _diag(f"search: malformed response or payload (collection={collection_name!r}): {exc}")
        return []
    except Exception as exc:
        _diag(f"search: failed (collection={collection_name!r}): {exc}")
        return []


def _search_memory_impl(
    query: str,
    memory_type: str,
    top_k: int,
    session_id: Optional[str],
    cross_session: bool,
    include_dormant: bool,
    include_archived: bool,
    client: Any,
    embedder: Optional[Callable[[str], List[float]]],
    embedder_unavailable_reason: str = "embedding model unavailable",
) -> Dict[str, Any]:
    """
    Testable core of search_memory — see that function's docstring for the
    usage constraints enforced here. Kept separate from the @mcp.tool()
    wrapper because FastMCP generates a JSON schema from the decorated
    function's signature at decoration time, and a Callable-typed parameter
    (needed to inject a mock embedder/client in tests) breaks that
    generation. client/embedder are real parameters here, not test-only —
    the wrapper below always passes the real production instances.
    """
    if memory_type not in COLLECTION_BY_TYPE:
        return {
            "results": [],
            "count": 0,
            "degraded": True,
            "reason": f"unknown memory_type: {memory_type!r} (expected one of {sorted(COLLECTION_BY_TYPE)})",
        }

    if memory_type == "episodic" and session_id is None and not cross_session:
        return {
            "results": [],
            "count": 0,
            "degraded": True,
            "reason": "episodic search requires session_id, or explicit cross_session=True to search all sessions",
        }

    top_k = max(1, min(top_k, 50))

    statuses = ["active"]
    if include_dormant:
        statuses.append("dormant")
    if include_archived:
        statuses.append("archived")

    if embedder is None:
        return {
            "results": [],
            "count": 0,
            "degraded": True,
            "reason": embedder_unavailable_reason,
        }

    if memory_type == "reflection":
        reflection_records = _search_reflection(
            query=query, top_k=top_k, statuses=statuses, client=client, embedder=embedder
        )
        return {
            "results": [r.to_dict() for r in reflection_records],
            "count": len(reflection_records),
            "degraded": client is None,
            "reason": None if client is not None else "qdrant-memory client unavailable",
        }

    index = QdrantMemoryIndex(memory_type, client=client, embedder=embedder)
    effective_session_id = session_id if (memory_type == "episodic" and not cross_session) else None
    records = index.search(
        query_text=query,
        top_k=top_k,
        status_in=tuple(statuses),
        session_id=effective_session_id,
    )

    return {
        "results": [r.to_payload() for r in records],
        "count": len(records),
        "degraded": client is None,
        "reason": None if client is not None else "qdrant-memory client unavailable",
    }


@mcp.tool()
def search_memory(
    query: str,
    memory_type: str,
    top_k: int = 5,
    session_id: Optional[str] = None,
    cross_session: bool = False,
    include_dormant: bool = False,
    include_archived: bool = False,
) -> Dict[str, Any]:
    """
    Read-only semantic search over one memory collection
    (episodic | semantic | procedural | reflection). Never raises — every
    failure mode (unknown memory_type, missing session scope, unavailable
    embedder, unreachable Qdrant) returns an empty result with
    `degraded=True` and a `reason`, matching this module's existing
    graceful-degradation discipline.

    Usage constraints enforced here, not left to caller discipline (per
    telescope/2026-07-10-agent-memory-architecture/supporting/09-mcp-architecture-decision.md):

    - episodic search is session-scoped by default — a session_id is required
      unless the caller explicitly sets cross_session=True to opt into
      searching across every session's episodic memory
    - status defaults to "active" only; dormant/archived are excluded unless
      explicitly requested via include_dormant/include_archived — this
      mirrors QdrantMemoryIndex.search()'s own default and is not weakened
      here
    - sacred records are never separately filterable — they are always
      status="active" (apply_decay() pins them there), so the default filter
      already includes them; there is no parameter that could exclude them
    - importance/sacred are not accepted as parameters at all — those are
      set only by the internal write-time heuristic, never by a caller
    - top_k is clamped to [1, 50] — no unbounded result sets
    - reflection results are full ReflectionRecord payloads (reflection_id,
      trigger_type, summary, root_cause, remediation, scope_of_applicability,
      severity, logged_by, timestamp, sacred, status, migrated_from), not the
      episodic/semantic/procedural MemoryRecord shape — see
      telescope/2026-07-14-reflexion-memory-system/supporting/01-technical-options.md §5
    """
    try:
        return _search_memory_impl(
            query=query,
            memory_type=memory_type,
            top_k=top_k,
            session_id=session_id,
            cross_session=cross_session,
            include_dormant=include_dormant,
            include_archived=include_archived,
            client=_get_memory_client(),
            embedder=_get_embedder(),
            embedder_unavailable_reason=_get_embedder_unavailable_reason(),
        )
    except Exception as exc:
        # No exception may escape a @mcp.tool() entry point — an uncaught one
        # here kills the server process instead of returning a JSON-RPC error to
        # the caller. Mirrors this module's existing degraded=True/reason
        # discipline instead of a bare crash.
        traceback.print_exc(file=sys.stderr)
        return {
            "results": [],
            "count": 0,
            "degraded": True,
            "reason": f"search_memory failed: {exc}",
        }


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """Report reachability and point counts for the dedicated qdrant-memory
    instance (http://localhost:6335) this server reads from — episodic,
    semantic, procedural, and reflection collections, plus dormant ratio and
    last consolidation time. point_counts is driven entirely by
    COLLECTION_BY_TYPE (memory_vector_store.py), so memory_reflection is
    included automatically now that Phase 1 registered it there — no
    reflection-specific logic needed here, since QdrantMemoryIndex.count_points()
    never parses point payload shape (unlike .search(), see _search_reflection
    above). Degrades to reachable=False with zeroed counts (never raises) if
    qdrant-memory is unreachable, matching search_memory's own
    graceful-degradation discipline. Same telemetry shape as
    workspace-knowledge's health_check's memory_instance block, so callers
    can read either server's health_check for this data."""
    try:
        _diag("health_check: start")
        client = _get_memory_client()
        indices = {
            memory_type: QdrantMemoryIndex(memory_type, client=client)
            for memory_type in COLLECTION_BY_TYPE
        }
        _diag("health_check: calling compute_memory_instance_telemetry")
        result = {
            "memory_instance": compute_memory_instance_telemetry(
                client=client, indices=indices, sync_state=_memory_sync_state
            )
        }
        _diag("health_check: done")
        return result
    except Exception as exc:
        # No exception may escape a @mcp.tool() entry point — an uncaught one
        # kills the server process instead of returning a JSON-RPC error to the
        # caller (same discipline as search_memory's guard above).
        traceback.print_exc(file=sys.stderr)
        return {
            "memory_instance": {
                "reachable": False,
                "point_counts": {},
                "last_consolidation_at": None,
                "dormant_ratio": 0.0,
                "error": f"health_check failed: {exc}",
            }
        }


if __name__ == "__main__":
    mcp.run()
