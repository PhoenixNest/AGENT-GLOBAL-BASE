"""Lightweight span recorder for CC-00 LangChain agents.

Deliberately NOT LangSmith: LangSmith is a hosted commercial service and is
excluded by the CEO's open-source-only constraint (see the assessment's Out of
Scope section). `opentelemetry` is an optional dependency here, not a required
one — this project's requirements.txt does not install it, so by default
`install_tracing()` falls back to an in-memory recorder that tests can inspect
directly. If `opentelemetry-sdk` and `opentelemetry-exporter-otlp` ARE installed
in the active environment, real OTel spans are used instead and exported to
the given OTLP endpoint. Neither path was exercised against a live collector in
this deliverable — the in-memory fallback is what tests/ actually verify.

`tracer` is a stable module-level PROXY object, never rebound. Other modules do
`from .telemetry import tracer` at import time; if `install_tracing()` swapped
the name `tracer` to point at a new object afterward, every module that already
imported the old reference would keep tracing into a discarded recorder. The
proxy delegates to whichever backend is currently installed, so a single object
identity survives `install_tracing()` being called at any point.
"""

from __future__ import annotations

import contextlib
import time
from dataclasses import dataclass, field
from typing import Any, Iterator


@dataclass
class RecordedSpan:
    name: str
    attributes: dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0


class InMemoryRecorder:
    """Fallback tracer used when opentelemetry is not installed. Test-friendly."""

    def __init__(self) -> None:
        self.spans: list[RecordedSpan] = []

    @contextlib.contextmanager
    def start_as_current_span(self, name: str) -> Iterator["_SpanHandle"]:
        started = time.monotonic()
        record = RecordedSpan(name=name)
        self.spans.append(record)
        try:
            yield _SpanHandle(record)
        finally:
            record.duration_ms = (time.monotonic() - started) * 1000

    def start_span(self, name: str) -> "_SpanHandle":
        record = RecordedSpan(name=name)
        self.spans.append(record)
        return _SpanHandle(record)

    def clear(self) -> None:
        self.spans.clear()


class _SpanHandle:
    def __init__(self, record: RecordedSpan) -> None:
        self._record = record

    def set_attribute(self, key: str, value: Any) -> None:
        self._record.attributes[key] = value


class _TracerProxy:
    """Stable identity across the process. Delegates to the active backend."""

    def __init__(self) -> None:
        self._impl: Any = InMemoryRecorder()

    def start_as_current_span(self, name: str):
        return self._impl.start_as_current_span(name)

    def start_span(self, name: str):
        return self._impl.start_span(name)


tracer = _TracerProxy()


def install_tracing(service_name: str, endpoint: str = "http://localhost:4317") -> None:
    """Attempt to install real OpenTelemetry tracing; fall back silently.

    Not called by default anywhere in this package — callers opt in. The
    fallback path (opentelemetry not installed, or the exporter cannot be
    constructed) leaves the in-memory recorder in place and does not raise,
    matching the "graceful degradation, never blocks" discipline this
    workspace already applies to the agent-memory MCP server.
    """
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        return  # tracer._impl stays the InMemoryRecorder

    try:
        provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
        trace.set_tracer_provider(provider)
        tracer._impl = trace.get_tracer("cc00.langchain")
    except Exception:
        return  # exporter/collector unreachable — stay on the in-memory recorder


def reset_recorder() -> None:
    """Test helper: clear recorded spans between test cases (in-memory backend only)."""
    if isinstance(tracer._impl, InMemoryRecorder):
        tracer._impl.clear()


def recorded_spans() -> list[RecordedSpan]:
    """Test helper: read back what was recorded (in-memory backend only)."""
    if isinstance(tracer._impl, InMemoryRecorder):
        return tracer._impl.spans
    return []
