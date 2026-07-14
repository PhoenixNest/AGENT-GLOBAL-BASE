"""
embedder-service — persistent, localhost-only embedding server shared by
every CC-00 MCP server that needs a sentence-transformers model.

Built to remove the trigger identified in
telescope/2026-07-13-mcp-embedder-service-redesign/research-report.md: a
heavy compiled-extension import (sentence_transformers -> torch/scipy)
happening inside a process the MCP host spawns and churns. This service is
launched once, outside that host-spawned lifecycle, and loads both models a
single time at startup; consumers talk to it over plain HTTP instead of
importing the ML stack themselves.

Endpoints:
    GET  /health              -> {status, service, version, models_loaded, uptime_s, idle_timeout_s}
    POST /embed {model, texts} -> {vectors, dim, model}
    POST /shutdown             -> graceful stop (localhost-only, no auth needed —
                                   see Phase 3 adversarial review for the threat model)

Lifecycle (implementation-plan.md §8.3):
    Stopped -> Starting -> Running -> Idle -> Stopped
Idle-timeout self-shutdown lives here, not in the supervisor script, so no
external process has to remember to stop it (per §2.1's resolved lifecycle
decision). Never shuts down mid-request: shutdown only proceeds once the
in-flight request counter is zero.

Applies the NO_PROXY lesson from
telescope/2026-07-10-agent-memory-architecture/supporting/02-deployment-guidelines.md
§1.1 to its own process environment on startup, so anything this process
itself calls out to (none today) is never routed through an invisible
Windows-side proxy either.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Apply the NO_PROXY lesson to this process's own environment, from day one —
# not retrofitted after a failure (implementation-plan.md §3).
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
os.environ.setdefault("no_proxy", "localhost,127.0.0.1")

SERVICE_NAME = "embedder-service"
SERVICE_VERSION = "1.0"

HOST = os.getenv("EMBEDDER_SERVICE_HOST", "127.0.0.1")
PORT = int(os.getenv("EMBEDDER_SERVICE_PORT", "8791"))
IDLE_TIMEOUT_S = float(os.getenv("EMBEDDER_SERVICE_IDLE_TIMEOUT_S", "600"))
IDLE_CHECK_INTERVAL_S = float(os.getenv("EMBEDDER_SERVICE_IDLE_CHECK_INTERVAL_S", "15"))

_SHARED_DIR = Path(__file__).resolve().parent.parent
MODELS_CACHE_DIR = _SHARED_DIR / "models"
RUN_DIR = Path(__file__).resolve().parent / "run"

# Short/HF-id aliases -> shared-cache slug. New models only need an entry here.
MODEL_ALIASES: Dict[str, str] = {
    "all-MiniLM-L6-v2": "sentence-transformers--all-MiniLM-L6-v2",
    "sentence-transformers/all-MiniLM-L6-v2": "sentence-transformers--all-MiniLM-L6-v2",
    "sentence-transformers--all-MiniLM-L6-v2": "sentence-transformers--all-MiniLM-L6-v2",
    "all-mpnet-base-v2": "sentence-transformers--all-mpnet-base-v2",
    "sentence-transformers/all-mpnet-base-v2": "sentence-transformers--all-mpnet-base-v2",
    "sentence-transformers--all-mpnet-base-v2": "sentence-transformers--all-mpnet-base-v2",
}


def _diag(msg: str) -> None:
    print(f"[embedder-service {time.time():.3f}] {msg}", file=sys.stderr, flush=True)


class ModelRegistry:
    """Loads every provisioned, aliased model once at construction time and
    serves encode() calls behind a per-model lock. sentence-transformers'
    encode() has no documented thread-safety guarantee for concurrent calls
    on the same instance; a lock trades a small amount of throughput for a
    correctness guarantee that does not depend on an undocumented internal
    property of a third-party library."""

    def __init__(self, models_dir: Path, aliases: Dict[str, str]):
        self._models: Dict[str, Any] = {}
        self._locks: Dict[str, threading.Lock] = {}
        self._dims: Dict[str, int] = {}
        self.aliases = aliases

        from sentence_transformers import SentenceTransformer

        slugs = sorted(set(aliases.values()))
        for slug in slugs:
            model_dir = models_dir / slug
            if not model_dir.exists():
                _diag(f"SKIP {slug}: not provisioned at {model_dir}")
                continue
            t0 = time.time()
            model = SentenceTransformer(str(model_dir))
            self._models[slug] = model
            self._locks[slug] = threading.Lock()
            self._dims[slug] = model.get_sentence_embedding_dimension()
            _diag(f"loaded {slug} in {time.time() - t0:.2f}s (dim={self._dims[slug]})")

        if not self._models:
            raise RuntimeError(
                f"no models could be loaded from {models_dir} — provision at least one "
                f"via _shared/provision_model.py before starting embedder-service"
            )

    def resolve(self, model_name: str) -> Optional[str]:
        slug = self.aliases.get(model_name, model_name if model_name in self._models else None)
        return slug if slug in self._models else None

    def loaded_slugs(self) -> List[str]:
        return sorted(self._models)

    def encode(self, slug: str, texts: List[str]) -> List[List[float]]:
        model = self._models[slug]
        lock = self._locks[slug]
        with lock:
            vectors = model.encode(texts, show_progress_bar=False)
        return [v.tolist() for v in vectors]

    def dim(self, slug: str) -> int:
        return self._dims[slug]


class IdleTracker:
    """Tracks in-flight requests and last-activity time. Idle-timeout
    self-shutdown (checked by a background thread) only fires when the
    in-flight counter is zero — this is the mechanism that satisfies the
    Phase 0 gate requirement that shutdown never interrupts a live request."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._in_flight = 0
        self._last_activity = time.time()
        self.start_time = time.time()

    def begin_request(self) -> None:
        with self._lock:
            self._in_flight += 1
            self._last_activity = time.time()

    def end_request(self) -> None:
        with self._lock:
            self._in_flight = max(0, self._in_flight - 1)
            self._last_activity = time.time()

    def idle_seconds(self) -> float:
        with self._lock:
            if self._in_flight > 0:
                return 0.0
            return time.time() - self._last_activity

    def uptime_seconds(self) -> float:
        return time.time() - self.start_time


class Handler(BaseHTTPRequestHandler):
    registry: ModelRegistry
    idle: IdleTracker
    server_ref: "ThreadingHTTPServer"

    def log_message(self, fmt: str, *args: Any) -> None:  # quiet default access log
        _diag(fmt % args)

    def _send_json(self, status: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802 (stdlib method name)
        if self.path == "/health":
            self._handle_health()
        else:
            self._send_json(404, {"error": f"unknown path: {self.path}"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/embed":
            self._handle_embed()
        elif self.path == "/shutdown":
            self._handle_shutdown()
        else:
            self._send_json(404, {"error": f"unknown path: {self.path}"})

    def _handle_health(self) -> None:
        self._send_json(
            200,
            {
                "status": "ok",
                "service": SERVICE_NAME,
                "version": SERVICE_VERSION,
                "models_loaded": self.registry.loaded_slugs(),
                "uptime_s": round(self.idle.uptime_seconds(), 2),
                "idle_timeout_s": IDLE_TIMEOUT_S,
                "pid": os.getpid(),
            },
        )

    def _handle_embed(self) -> None:
        self.idle.begin_request()
        try:
            try:
                body = self._read_json_body()
            except Exception as exc:
                self._send_json(400, {"error": f"invalid JSON body: {exc}"})
                return

            model_name = body.get("model")
            texts = body.get("texts")

            if not isinstance(model_name, str) or not model_name:
                self._send_json(400, {"error": "'model' must be a non-empty string"})
                return
            if not isinstance(texts, list) or not texts or not all(isinstance(t, str) for t in texts):
                self._send_json(400, {"error": "'texts' must be a non-empty list of strings"})
                return

            slug = self.registry.resolve(model_name)
            if slug is None:
                self._send_json(
                    400,
                    {
                        "error": f"unknown model: {model_name!r} (loaded: {self.registry.loaded_slugs()})"
                    },
                )
                return

            try:
                vectors = self.registry.encode(slug, texts)
            except Exception as exc:
                _diag(f"encode failed for model={slug!r}: {exc}")
                self._send_json(500, {"error": f"encode failed: {exc}"})
                return

            self._send_json(
                200, {"vectors": vectors, "dim": self.registry.dim(slug), "model": slug}
            )
        finally:
            self.idle.end_request()

    def _handle_shutdown(self) -> None:
        # Localhost-only binding is the trust boundary here (matches the
        # existing Qdrant-over-HTTP precedent in this codebase) — see Phase 3
        # for the adversarial review of that assumption.
        self._send_json(200, {"status": "shutting down"})
        threading.Thread(target=self.server_ref.shutdown, daemon=True).start()


def _write_pid_file(port: int) -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    pid_file = RUN_DIR / "embedder-service.pid"
    pid_file.write_text(json.dumps({"pid": os.getpid(), "port": port, "started_at": time.time()}))


def _remove_pid_file() -> None:
    pid_file = RUN_DIR / "embedder-service.pid"
    try:
        pid_file.unlink(missing_ok=True)
    except Exception:
        pass


def _idle_watchdog(httpd: ThreadingHTTPServer, idle: IdleTracker) -> None:
    while True:
        time.sleep(IDLE_CHECK_INTERVAL_S)
        idle_for = idle.idle_seconds()
        if idle_for >= IDLE_TIMEOUT_S:
            _diag(f"idle for {idle_for:.0f}s >= {IDLE_TIMEOUT_S}s — self-shutdown")
            httpd.shutdown()
            return


def main() -> None:
    _diag(f"starting: loading models from {MODELS_CACHE_DIR}")
    registry = ModelRegistry(MODELS_CACHE_DIR, MODEL_ALIASES)
    idle = IdleTracker()

    handler_cls = type("BoundHandler", (Handler,), {"registry": registry, "idle": idle})

    httpd = ThreadingHTTPServer((HOST, PORT), handler_cls)
    handler_cls.server_ref = httpd

    _write_pid_file(PORT)
    watchdog = threading.Thread(target=_idle_watchdog, args=(httpd, idle), daemon=True)
    watchdog.start()

    _diag(f"listening on http://{HOST}:{PORT} (models={registry.loaded_slugs()}, idle_timeout={IDLE_TIMEOUT_S}s)")
    try:
        httpd.serve_forever()
    finally:
        _diag("server stopped")
        _remove_pid_file()


if __name__ == "__main__":
    main()
