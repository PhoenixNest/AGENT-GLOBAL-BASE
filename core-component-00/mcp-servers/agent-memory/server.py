import os
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import psutil
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
    SearchOutcome,
    JSONLMemoryLog,
    _call_with_hard_timeout,
    compute_memory_instance_telemetry,
    bm25_rank_ids,
    keyword_search_log,
    Filter,
    FieldCondition,
    MatchAny,
)
from implementations.memory_store import ReflectionRecord  # noqa: E402
import concurrent.futures  # noqa: E402

# embedder-service client import — same cross-module import pattern as
# memory_vector_store above.
_MCP_SERVERS_SHARED_ROOT = Path(__file__).resolve().parents[1] / "_shared"
if str(_MCP_SERVERS_SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(_MCP_SERVERS_SHARED_ROOT))
import embedder_client  # noqa: E402

# write_memory (not yet a live MCP tool — see write_tool.py's module
# docstring "ACTIVATION STATUS") and the shared write-rate-limiter telemetry
# health_check() reports below regardless of activation state.
import write_tool  # noqa: E402
from write_provenance import get_default_rate_limiter  # noqa: E402


def _diag(msg: str) -> None:
    """Unbuffered, timestamped stderr line. A blocking native call that never
    returns and never raises is invisible to a try/except — the thread simply
    never comes back to Python. This is the only way to see, after the fact,
    which of several sequential Qdrant round-trips (or the embedder-warmup
    thread's import attempts) actually stalled. Defined before the
    embedder-warmup thread is started below, since that thread calls this."""
    print(f"[DIAG {time.time():.3f}] {msg}", file=sys.stderr, flush=True)


_SELF_PID = os.getpid()
# Scopes sibling-cleanup matches to processes spawned by the SAME host
# process as this one. Without this, the path-suffix match below is
# identical across every checkout of this workspace -- including git
# worktrees (CLAUDE.md section 6's own multi-agent isolation pattern) --
# so a worktree's live agent-memory process could be killed by the main
# checkout's cleanup, or vice versa, despite being unrelated servers. A
# same-session `/mcp reconnect` double-spawn shares one host process
# (the scenario this cleanup exists to fix); a separate checkout or
# worktree is opened as its own host session with a different parent PID.
_SELF_PARENT_PID = os.getppid()
_AGENT_MEMORY_SERVER_SCRIPT = str(Path(__file__).resolve())
# core-component-00/mcp-servers/agent-memory/server.py -- a workspace-root-
# relative, forward-slash-normalized suffix. Computed, not hardcoded, so it
# stays correct if the workspace itself is renamed or relocated.
_AGENT_MEMORY_RELATIVE_SUFFIX = (
    Path(__file__).resolve().relative_to(Path(__file__).resolve().parents[3]).as_posix()
)
# Floor below which the min-age gate would no longer meaningfully guard
# against a near-simultaneous double-spawn, regardless of override.
_SIBLING_CLEANUP_MIN_AGE_FLOOR_S = 10.0


def _resolve_sibling_cleanup_min_age_s() -> float:
    """Guards against two near-simultaneous sibling processes (e.g. a rapid
    host-side double-spawn on reconnect) each treating the other as stale
    and killing each other before either completes the MCP handshake. Set
    above the widest legitimate cold-start window this file allows for,
    including a retried attempt: the in-process embedder fallback retries
    once (_EMBEDDER_LOAD_MAX_ATTEMPTS = 2) at up to _EMBEDDER_LOAD_TIMEOUT_S
    (90s) each, matching the documented 2026-07-13 incident where both
    attempts stalled -- so a still-initializing legitimate process is never
    mistaken for an orphan even in that worst case. Never raises and never
    returns below the floor, even on a malformed or adversarial override
    (including NaN, whose comparisons are always False and would otherwise
    slip a plain `<` check) -- this computation runs at import time, where
    an uncaught exception would take the whole server down."""
    raw = os.getenv("AGENT_MEMORY_SIBLING_CLEANUP_MIN_AGE_S", "200")
    try:
        value = float(raw)
    except (TypeError, ValueError):
        _diag(f"sibling-cleanup: invalid AGENT_MEMORY_SIBLING_CLEANUP_MIN_AGE_S={raw!r}, using default 200.0")
        return 200.0
    if not (value >= _SIBLING_CLEANUP_MIN_AGE_FLOOR_S):
        _diag(f"sibling-cleanup: AGENT_MEMORY_SIBLING_CLEANUP_MIN_AGE_S={value!r} below floor, clamped to {_SIBLING_CLEANUP_MIN_AGE_FLOOR_S:g}")
        return _SIBLING_CLEANUP_MIN_AGE_FLOOR_S
    return value


_SIBLING_CLEANUP_MIN_AGE_S = _resolve_sibling_cleanup_min_age_s()


def _normalize_cmdline_arg(arg: str) -> str:
    """Slash-unifies and trims a single cmdline argument so a Windows-style
    absolute path and a POSIX-style relative one compare the same way --
    the psutil-based equivalent of the former PowerShell scan's
    `-replace '\\\\','/'` plus `.TrimEnd().TrimEnd('"')`."""
    return arg.replace("\\", "/").strip().rstrip('"')


def _sibling_matches(
    cmdline: List[str],
    create_time: float,
    ppid: int,
    now: float,
    relative_suffix: str,
    min_age: float,
    parent_pid: Optional[int],
) -> bool:
    """Cross-platform equivalent of the former PowerShell WHERE-clause
    (_build_sibling_match_filter_clause). Conditions, unchanged from the
    original: (1) the LAST cmdline argument (the launched script path) --
    not a bare substring anywhere in the command line -- ends with the
    workspace-relative server.py suffix, so a command line that references
    this file as one argument among several (e.g. a pytest or lint
    invocation covering multiple files) is never mistaken for a direct
    `python server.py` launch; (2) old enough per min_age; (3) if
    parent_pid is not None, shares this process's ParentProcessId, so a
    same-suffix process from a different checkout or worktree (see
    _SELF_PARENT_PID) is never matched. parent_pid=None omits condition
    (3) entirely -- used only by the diagnostic count below, never for
    actual kill eligibility. Pure Python, no subprocess -- testable on
    every OS, unlike the PowerShell expression it replaces."""
    if not cmdline:
        return False
    if not _normalize_cmdline_arg(cmdline[-1]).endswith(relative_suffix):
        return False
    if (now - create_time) <= min_age:
        return False
    if parent_pid is not None and ppid != parent_pid:
        return False
    return True


def _iter_sibling_candidates():
    """Isolated so tests can monkeypatch process iteration without reaching
    into psutil internals. Skips any process psutil can't fully inspect
    (already exited, permission-denied, zombie) rather than failing the
    whole scan over one uninspectable process -- psutil.process_iter can
    itself raise these mid-iteration, not just on individual .info access."""
    for proc in psutil.process_iter(["pid", "ppid", "cmdline", "create_time"]):
        try:
            yield proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


def _scan_sibling_pids(relative_suffix: str, min_age: float, parent_pid: Optional[int]) -> List[int]:
    """The actual scan, factored out so both the real kill-eligible scan and
    the PPID-less diagnostic scan share one implementation."""
    now = time.time()
    return [
        info["pid"]
        for info in _iter_sibling_candidates()
        if info["pid"] != _SELF_PID
        and _sibling_matches(
            info.get("cmdline") or [],
            info.get("create_time") or 0.0,
            info.get("ppid") if info.get("ppid") is not None else -1,
            now,
            relative_suffix,
            min_age,
            parent_pid,
        )
    ]


def _diag_log_ppid_filtered_out_count(relative_suffix: str, min_age: float) -> None:
    """Only called when the full (suffix+age+ParentProcessId) scan finds
    nothing. Without this, "no stale siblings exist" and "siblings exist
    but no longer share this process's ParentProcessId" produce an
    identical log line -- so a future regression to the ParentProcessId
    scope silently matching nothing would be undetectable. Runs a second,
    PPID-less scan purely for this diagnostic count; never affects which
    processes get terminated, and never raises -- a failure here only
    means the diagnostic count is skipped."""
    try:
        other_ppid_count = len(
            _call_with_hard_timeout(
                lambda: _scan_sibling_pids(relative_suffix, min_age, parent_pid=None),
                timeout=20.0,
            )
            or []
        )
    except Exception:
        return
    if other_ppid_count:
        _diag(
            f"sibling-cleanup: {other_ppid_count} same-suffix process(es) old enough to match "
            "exist under a DIFFERENT ParentProcessId (different checkout/worktree, or a host-spawn "
            "behavior change) -- none terminated, verify this is expected"
        )


def _cleanup_stale_sibling_processes() -> None:
    """
    Terminates any other live process running this exact `server.py` before
    this instance proceeds. Mirrors the orphan-cleanup pattern already
    proven for embedder-service (manage_embedder_service.ps1 -Action
    cleanup / its 2026-08-13 manage_embedder_service.py port), applied here
    to agent-memory's own process.

    Rationale (2026-08-09 live investigation, mcp-governance.md's
    agent-memory row): the MCP host does not always cleanly terminate a
    prior agent-memory process on `/mcp reconnect` -- four concurrent
    instances were observed piling up in one session, each independently
    racing to import the same heavy ML stack and/or spawn embedder-service.
    That is real resource contention (CPU, disk I/O, the shared
    embedder-service launch lock), not merely a theoretical duplicate, and
    is a direct contributor to the cold-start stalls documented in that
    row. This runs once, synchronously, at module-import time -- before
    the embedder-service background thread starts further down -- so the
    process count is already trimmed by the time that race begins.

    On-demand only, per standing design: this function executes exactly
    once per process, only when a real MCP connection spins up a new
    agent-memory process. It adds no scheduled task, login trigger, or
    standalone background process, and does nothing while the system is
    not in use.

    Matches on this script's workspace-root-relative path suffix
    (core-component-00/mcp-servers/agent-memory/server.py), normalized for
    both forward and back slash separators, as a trailing-position match on
    the LAST cmdline argument (see _sibling_matches) -- not a bare
    substring anywhere in the command line, and not merely "agent-memory"
    -- so a command line that only references this file among other
    arguments (e.g. a test or lint run) is never mistaken for a direct
    launch of it. That suffix alone is identical across every checkout of
    this workspace, including git worktrees (CLAUDE.md section 6), so the
    match also requires the candidate to share this process's
    ParentProcessId (_SELF_PARENT_PID) -- scoping cleanup to siblings
    spawned by the same host session, so a different checkout's or
    worktree's live server is never killed by this one's cleanup, or vice
    versa.

    Only terminates a sibling once it is older than
    _SIBLING_CLEANUP_MIN_AGE_S, so two processes spawned seconds apart by
    the same reconnect never treat each other as stale and kill each other.

    Cross-platform via `psutil` (2026-08-13 -- previously Windows-only via
    `powershell`/`Get-CimInstance`, a no-op elsewhere; see
    core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md).
    Never raises: any failure here must not prevent this server from
    starting and serving.

    Gated by AGENT_MEMORY_ENABLE_SIBLING_CLEANUP (default true). Set to
    false by tests/conftest.py before this module is imported -- this
    module is imported for real (not mocked) by the test suite via
    importlib.exec_module(), so without this gate a test run would scan for
    and terminate any genuinely live agent-memory server process on the
    machine, including the one powering an active Claude Code session. That
    is real, unacceptable collateral damage from running `pytest`, mirroring
    exactly why conftest.py already forces EMBEDDER_SERVICE_ENABLED=false
    before import.
    """
    if os.getenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true").strip().lower() in (
        "0", "false", "no",
    ):
        _diag("sibling-cleanup: skipped (AGENT_MEMORY_ENABLE_SIBLING_CLEANUP=false)")
        return

    relative_suffix = _AGENT_MEMORY_RELATIVE_SUFFIX
    min_age = _SIBLING_CLEANUP_MIN_AGE_S

    try:
        sibling_pids = _call_with_hard_timeout(
            lambda: _scan_sibling_pids(relative_suffix, min_age, _SELF_PARENT_PID),
            timeout=20.0,
        )
    except Exception as exc:
        _diag(f"sibling-cleanup: process scan failed, skipping ({exc})")
        return

    if sibling_pids is None:
        _diag("sibling-cleanup: process scan unusable (timed out)")
        return

    if not sibling_pids:
        _diag(f"sibling-cleanup: no sibling processes older than {min_age:g}s found")
        _diag_log_ppid_filtered_out_count(relative_suffix, min_age)
        return

    for pid in sibling_pids:
        try:
            psutil.Process(pid).kill()
            _diag(f"sibling-cleanup: terminated stale agent-memory process pid={pid}")
        except Exception as exc:
            _diag(f"sibling-cleanup: failed to terminate pid={pid} ({exc})")


_cleanup_stale_sibling_processes()

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
# Was 60.0. Raised 2026-08-09: a live run hit this exact bound on both
# attempts (reported "failed: import did not complete within 60.0s across 2
# attempts") under real multi-process contention, before a subsequent
# process succeeded. 90s widens the on-demand budget to match what has
# actually been observed rather than a synthetic estimate; it does not
# claim to guarantee success.
_EMBEDDER_LOAD_TIMEOUT_S = 90.0
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
# embedder-service integration — feature-flagged primary path, with the
# in-process loader above kept as an unmodified automatic fallback. The
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
_embedder_service_last_probe_at: float = 0.0
_embedder_service_process_started_at: float = time.time()

# Bounds how often _embedder_service_ready() re-probes a cached "unavailable"
# state — see that function's docstring for why "unavailable" is re-checked
# at all. Keeps a genuinely-down service from adding repeated probe latency
# (up to embedder_client.HEALTH_PROBE_TIMEOUT_S + 2s) to every tool call.
_EMBEDDER_SERVICE_REPROBE_COOLDOWN_S = 5.0

# Wording only, not a behavior change: _embedder_service_ready() already
# re-probes an "unavailable" state on the cooldown above regardless of this
# window, so recovery already works without it. This just keeps
# _get_embedder_unavailable_reason()'s human-facing text from reading as a
# flat, final failure while embedder-service (launched detached — it
# outlives the call that started it, see embedder_client.ensure_service_running)
# is plausibly still mid-launch. Matched to embedder_client.STARTUP_WAIT_TIMEOUT_S
# plus headroom for the observed variance in mcp-governance.md's agent-memory row.
_EMBEDDER_SERVICE_STARTING_GRACE_S = 150.0


def _start_embedder_service_background() -> None:
    # Runs exactly once, at process startup. An "unavailable" result here is
    # not final — _embedder_service_ready() re-probes and can overwrite it
    # with "ready" later, without a process restart (P1 fix, 2026-08-06).
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
    """
    Returns the cached embedder-service readiness state — but first
    re-probes if that cache currently says "unavailable", instead of
    trusting it forever. _start_embedder_service_background() runs its
    check exactly once, in a background thread, at process startup; if that
    single check loses the startup race against the shared embedder-service
    still coming up in another process, "unavailable" was previously a
    permanent, never-revisited verdict for the rest of this process's life
    — even after the service became healthy seconds later (P1 fix, see
    agent-memory live-validation findings, 2026-08-06). "starting" is left
    alone here: the background thread's first check is still in flight, so
    there is nothing stale to re-check yet.
    """
    global _embedder_service_state, _embedder_service_last_probe_at
    with _embedder_service_lock:
        state = _embedder_service_state
    if state != "unavailable":
        return state == "ready"

    now = time.time()
    with _embedder_service_lock:
        if now - _embedder_service_last_probe_at < _EMBEDDER_SERVICE_REPROBE_COOLDOWN_S:
            return False
        _embedder_service_last_probe_at = now

    ok = embedder_client.probe_health()
    with _embedder_service_lock:
        _embedder_service_state = "ready" if ok else "unavailable"
    if ok:
        _diag("embedder-service re-probe: now ready (was unavailable)")
    return ok


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
        if (
            service_state == "unavailable"
            and time.time() - _embedder_service_process_started_at < _EMBEDDER_SERVICE_STARTING_GRACE_S
        ):
            # Not yet a confirmed failure: embedder-service launches detached
            # (survives its launching call) and this process's own re-probe
            # (see _embedder_service_ready()) keeps checking on a cooldown —
            # recovery already happens automatically. This wording only keeps
            # a plausibly-still-launching state from reading as final.
            service_state = "starting (retry shortly)"
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


def _get_search_capability_snapshot() -> Dict[str, Any]:
    """
    Read-only snapshot of what `_get_embedder()` would resolve to right now,
    without triggering any side effect that a plain health check should not
    cause — in particular, this must never call `_ensure_embedder_load_started()`,
    since that would reintroduce exactly the kind of eager background work the
    2026-07-17 fix (commit referenced in mcp-governance.md's agent-memory row)
    deliberately made lazy-only. Every state read here goes through the same
    module globals `_get_embedder()`/`_get_embedder_unavailable_reason()`
    already use — this function does not introduce a second source of truth,
    it only re-presents that existing state in a health_check-shaped block.

    Never raises: each state read is a plain lock-guarded attribute read, and
    any unexpected error degrades to a clearly-labeled "unavailable" reading
    rather than propagating, consistent with every other code path in this
    module.
    """
    try:
        with _embedder_service_lock:
            service_state = _embedder_service_state if EMBEDDER_SERVICE_ENABLED else "disabled"
        with _embedder_lock:
            in_process_state = _embedder_state
            in_process_ready = _embedder_cache is not None

        # Mirrors _get_embedder()'s precedence exactly, but read-only: a
        # cached "ready" service state is trusted as-is (no re-probe — a
        # network call is not something a health check should trigger), and
        # the in-process fallback is only considered "ready" if it has
        # already finished loading on its own, never started here.
        service_effectively_ready = EMBEDDER_SERVICE_ENABLED and service_state == "ready"
        if service_effectively_ready:
            effective_path = "embedder-service"
        elif in_process_ready:
            effective_path = "in-process-fallback"
        else:
            effective_path = "unavailable"

        return {
            "embedder_service_enabled": EMBEDDER_SERVICE_ENABLED,
            "embedder_service_state": service_state,
            "in_process_fallback_state": in_process_state,
            "effective_path": effective_path,
        }
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        return {
            "embedder_service_enabled": EMBEDDER_SERVICE_ENABLED,
            "embedder_service_state": "unavailable",
            "in_process_fallback_state": f"failed: snapshot error: {exc}",
            "effective_path": "unavailable",
        }


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
# Read-side handle onto the same on-disk log the write path
# (write_tool.py -> PersistentMemorySink) appends to — DEFAULT_MEMORY_ROOT is
# an absolute path derived from memory_vector_store.py's own file location,
# not cwd, so this always resolves to the same directory regardless of which
# process constructs it. Backs Tier 3 (keyword_search_log /
# keyword_search_reflection_log below) — the JSONL log, not Qdrant.
_memory_log = JSONLMemoryLog()


def _search_reflection_impl(
    query: str,
    top_k: int,
    statuses: List[str],
    client: Any,
    embedder: Callable[[str], List[float]],
) -> SearchOutcome:
    """
    Reflection-collection search core, returning a SearchOutcome (records +
    degraded/reason) rather than a bare list — see SearchOutcome's docstring
    (memory_vector_store.py) for why a bare [] can't tell a caller whether
    that means "no matches" or "Qdrant degraded." _search_reflection() below
    wraps this for existing callers that only want the list; search_memory's
    Tier 3 fallback wiring calls _search_reflection_with_status() to get the
    degraded signal.

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
    QdrantMemoryIndex._search_impl()'s own exactly.
    """
    if client is None:
        return SearchOutcome([], degraded=True, reason="qdrant-memory client unavailable")
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
        records = [ReflectionRecord.from_dict(p.payload) for p in points]
        return SearchOutcome(records, degraded=False)
    except concurrent.futures.TimeoutError:
        _diag(f"search: TIMED OUT (collection={collection_name!r})")
        return SearchOutcome([], degraded=True, reason="timed out")
    except (ConnectionError, OSError) as exc:
        _diag(f"search: unreachable (collection={collection_name!r}): {exc}")
        return SearchOutcome([], degraded=True, reason=f"qdrant unreachable: {exc}")
    except (AttributeError, TypeError, KeyError, ValueError) as exc:
        _diag(f"search: malformed response or payload (collection={collection_name!r}): {exc}")
        return SearchOutcome([], degraded=True, reason=f"malformed qdrant response: {exc}")
    except Exception as exc:
        _diag(f"search: failed (collection={collection_name!r}): {exc}")
        return SearchOutcome([], degraded=True, reason=f"qdrant search failed: {exc}")


def _search_reflection(
    query: str,
    top_k: int,
    statuses: List[str],
    client: Any,
    embedder: Callable[[str], List[float]],
) -> List[ReflectionRecord]:
    """Returns just the record list, dropping the degraded/reason signal —
    see _search_reflection_impl()'s docstring."""
    return _search_reflection_impl(query, top_k, statuses, client, embedder).records


def _search_reflection_with_status(
    query: str,
    top_k: int,
    statuses: List[str],
    client: Any,
    embedder: Callable[[str], List[float]],
) -> SearchOutcome:
    """search_memory's Tier 3 fallback wiring calls this to get the degraded
    signal _search_reflection() drops. See _search_reflection_impl()."""
    return _search_reflection_impl(query, top_k, statuses, client, embedder)


def keyword_search_reflection_log(
    log: JSONLMemoryLog,
    query: str,
    top_k: int,
    statuses: List[str],
) -> List[ReflectionRecord]:
    """
    Tier 3 keyword-only search for the reflection collection — the twin of
    memory_vector_store.keyword_search_log() for the three MemoryRecord-shaped
    collections, kept here rather than there for the same reason
    _search_reflection lives here: a reflection point's payload is a
    ReflectionRecord verbatim, not MemoryRecord-shaped, so it needs its own
    log reader (JSONLMemoryLog.read_all_reflections()) and its own payload
    parser (ReflectionRecord.from_dict()).

    Scores against "{summary} {scope_of_applicability}" — the exact same text
    QdrantMemoryIndex.rebuild_from_log()'s reflection branch embeds into
    Qdrant (memory_vector_store.py), so Tier 3 ranks against the same content
    Tier 1 would have, not a different text field.
    """
    payloads = log.read_all_reflections()
    filtered = [p for p in payloads if p.get("status", "active") in statuses]
    if not filtered:
        return []

    by_id = {p["reflection_id"]: p for p in filtered}
    id_text_pairs = [
        (p["reflection_id"], f"{p['summary']} {p['scope_of_applicability']}") for p in filtered
    ]
    ranked_ids = bm25_rank_ids(query, id_text_pairs, top_k)
    return [ReflectionRecord.from_dict(by_id[i]) for i in ranked_ids if i in by_id]


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

    # Deliberately NOT an early return on embedder is None: Tier 3
    # (keyword_search_log / keyword_search_reflection_log) needs no embedder
    # at all — it's pure BM25 over the JSONL log. An embedder-service outage
    # with an unready in-process fallback (see this module's own
    # graceful-degradation table in README.md) is, if anything, a more
    # common real-world degradation than qdrant-memory itself being down.
    # Returning empty here unconditionally would skip Tier 3 in exactly the
    # case it's most likely to matter. Each branch below detects
    # embedder is None on its own (via QdrantMemoryIndex.search_with_status /
    # _search_reflection_with_status) and falls through to Tier 3 the same
    # way a Qdrant-side failure does.

    if memory_type == "reflection":
        outcome = _search_reflection_with_status(
            query=query, top_k=top_k, statuses=statuses, client=client, embedder=embedder
        )
        if outcome.degraded and embedder is None:
            # More specific than the generic reason _search_reflection_impl
            # falls back to for a None embedder (it's built for the Qdrant
            # exception paths, not this one) — callers of search_memory get
            # the same diagnostic detail _get_embedder_unavailable_reason()
            # already provides (e.g. "still loading" vs. "not started").
            outcome = SearchOutcome(outcome.records, degraded=True, reason=embedder_unavailable_reason)
        tier = 1
        reflection_records = outcome.records
        if outcome.degraded:
            # Tier 1 (Qdrant) degraded — fall through to Tier 3 (keyword
            # search over the reflection log) rather than returning an empty
            # result outright. 05-disaster-recovery-and-resilience.md § 3.
            reflection_records = keyword_search_reflection_log(
                log=_memory_log, query=query, top_k=top_k, statuses=statuses
            )
            tier = 3
        return {
            "results": [r.to_dict() for r in reflection_records],
            "count": len(reflection_records),
            "degraded": outcome.degraded,
            "reason": outcome.reason,
            "tier": tier,
        }

    index = QdrantMemoryIndex(memory_type, client=client, embedder=embedder)
    effective_session_id = session_id if (memory_type == "episodic" and not cross_session) else None
    outcome = index.search_with_status(
        query_text=query,
        top_k=top_k,
        status_in=tuple(statuses),
        session_id=effective_session_id,
    )
    if outcome.degraded and embedder is None:
        outcome = SearchOutcome(outcome.records, degraded=True, reason=embedder_unavailable_reason)
    tier = 1
    records = outcome.records
    if outcome.degraded:
        # Same Tier 1 -> Tier 3 fallback as the reflection branch above, for
        # the three MemoryRecord-shaped collections (episodic/semantic/
        # procedural). keyword_search_log lives in memory_vector_store.py
        # since it operates on MemoryRecord, not ReflectionRecord.
        records = keyword_search_log(
            log=_memory_log,
            memory_type=memory_type,
            query=query,
            top_k=top_k,
            status_in=tuple(statuses),
            session_id=effective_session_id,
        )
        tier = 3

    return {
        "results": [r.to_payload() for r in records],
        "count": len(records),
        "degraded": outcome.degraded,
        "reason": outcome.reason,
        "tier": tier,
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
    telescope/2026-07-10-agent-memory-architecture/research-report.md
    § Architecture Decisions):

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
    included automatically since it is registered there — no
    reflection-specific logic needed here, since QdrantMemoryIndex.count_points()
    never parses point payload shape (unlike .search(), see _search_reflection
    above). Degrades to reachable=False with zeroed counts (never raises) if
    qdrant-memory is unreachable, matching search_memory's own
    graceful-degradation discipline. Same telemetry shape as
    workspace-knowledge's health_check's memory_instance block, so callers
    can read either server's health_check for this data.

    Also reports `search_capability` — embedder-service / in-process-fallback
    state (see _get_search_capability_snapshot()) — the observability gap the
    2026-08-06 P1 (embedder-service readiness was one-shot and invisible to
    health_check; fixed as f655c21e) exposed: nothing in this tool's output
    previously told a caller whether search_memory's embedding path was
    actually usable right now.

    Also reports `write_rate_limiting` — WriteRateLimiter.get_telemetry()
    (write_provenance.py), per the health_check telemetry convention
    documented in .claude/rules/mcp-governance.md's agent-memory row. This is
    live and read-only regardless of whether write_memory itself is
    registered as a callable MCP tool (AGENT_MEMORY_WRITE_TOOL_ENABLED) —
    the rate limiter's counters simply stay at zero until a write is ever
    attempted."""
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
            ),
            "search_capability": _get_search_capability_snapshot(),
            "write_rate_limiting": get_default_rate_limiter().get_telemetry(),
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
            },
            "search_capability": _get_search_capability_snapshot(),
            "write_rate_limiting": get_default_rate_limiter().get_telemetry(),
        }


def write_memory(
    content: str,
    memory_type: str,
    session_id: str,
    provenance_source: str,
    provenance_triggering_context_excerpt: str,
    provenance_from_external_content: bool,
    provenance_confidence: float,
) -> Dict[str, Any]:
    """
    Write-capable counterpart to search_memory. Not registered as a live MCP
    tool unless AGENT_MEMORY_WRITE_TOOL_ENABLED is set truthy.

    memory_type must be one of "episodic" | "semantic" | "procedural" —
    "reflection" is rejected outright; that collection stays on its own
    Investigator-Authored Write Path, never MCP-agent-callable (per
    memory_store.py and write_gate.py's classify() docstring).

    There is no `sacred`, `importance`, or `status` parameter, on purpose
    (Decision 2, research-report.md § Architecture Decisions) — every one of those is
    derived internally: sacred is always False for this path, importance
    comes from the internal compute_write_time_importance("general")
    heuristic, and status ("active" | "quarantined") is determined entirely
    by WriteConfirmationGate.classify()'s routine/high_consequence
    classification plus the human-confirmation gate, never by the caller.

    Every write requires non-optional provenance (WriteProvenance, enforced
    via validate_provenance()) and is subject to per-session and
    per-session-per-type rate limiting (WriteRateLimiter) before anything
    else happens. Content is scanned for the same embedded-instruction
    patterns production_judge.py already detects; flagged content is always
    routed to the quarantine lane (never active, never silently dropped).
    A found collision against an existing record of the same memory_type is
    classified high_consequence and requires a human-facing confirmation
    (via write_tool.ConfirmationRequestTracker + WriteConfirmationGate)
    before it can land as status="active" — otherwise this call returns
    status="confirmation_required" and performs no write.

    Never raises — every failure mode (rejected input, rate limit, missing
    client/embedder, degraded upsert, or any unexpected internal error)
    returns a dict with written=False and a `reason`, matching this module's
    existing graceful-degradation discipline (see search_memory/health_check).
    """
    try:
        return write_tool._write_memory_impl(
            content=content,
            memory_type=memory_type,
            session_id=session_id,
            provenance_source=provenance_source,
            provenance_triggering_context_excerpt=provenance_triggering_context_excerpt,
            provenance_from_external_content=provenance_from_external_content,
            provenance_confidence=provenance_confidence,
            client=_get_memory_client(),
            embedder=_get_embedder(),
            embedder_unavailable_reason=_get_embedder_unavailable_reason(),
            gate=write_tool.get_default_write_gate(),
            rate_limiter=get_default_rate_limiter(),
            confirmation_tracker=write_tool.get_default_confirmation_tracker(),
            # No production LLM judge exists anywhere in this workspace yet.
            judge_callable=None,
        )
    except Exception as exc:
        # No exception may escape a @mcp.tool()-shaped entry point — mirrors
        # search_memory's/health_check's identical discipline.
        traceback.print_exc(file=sys.stderr)
        return {
            "written": False,
            "status": "error",
            "reason": f"write_memory failed: {exc}",
            "record_id": None,
            "lane": None,
        }


# NOT a live MCP tool unless AGENT_MEMORY_WRITE_TOOL_ENABLED is truthy.
if write_tool.AGENT_MEMORY_WRITE_TOOL_ENABLED:
    mcp.tool()(write_memory)


if __name__ == "__main__":
    mcp.run()
