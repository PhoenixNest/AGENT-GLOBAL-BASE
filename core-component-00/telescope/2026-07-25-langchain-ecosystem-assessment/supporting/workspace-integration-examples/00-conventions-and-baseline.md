# 00 — Conventions, Baseline, and the ASGF Governance Kit

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Read this first.** Every other file in `supporting/` assumes the conventions, the pinned version
floors, and the middleware kit defined here.

---

## 1. Verification Status — read before trusting any code below

| Claim class                                     | Status                                                                                                        |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| LangChain / LangGraph / DeepAgents API surface  | **Verified** against the official `langchain-ai/docs` repository via Context7 on **2026-07-26**               |
| CC-00 class names, method names, and signatures | **Verified** by direct read of the files under `core-component-00/*/implementations/` on **2026-07-26**       |
| CC-00 module import mechanics (§6)              | **Verified** by static inspection of import statements and `__init__.py` presence — see §6 for what was found |
| Version numbers and CVE floors                  | **Inherited** from `2026-07-25-langchain-ecosystem-assessment`, which retrieved them from PyPI on 2026-07-25  |
| **Whether any example here runs**               | **NOT VERIFIED — no code in this deliverable was executed.**                                                  |

**No `langchain*` package is installed in this workspace** (Finding 5 of the research report, still
true at the time of writing). Nothing here was run, imported, or tested. These are **reference
examples written against a verified API surface**, not working software. Treat every file as a
design artefact requiring a first-run shakedown before it is trusted — the same status CC-00 assigns
to any unexecuted reference implementation.

Where a claim could not be verified, it is labelled inline. Do not remove those labels when copying
code out of these documents.

---

## 2. Scope and the commercial boundary

The CEO's standing constraint from the research report applies unchanged: **open source only, no
paid content, no vendor engagement.** Concretely, for every example in this folder:

- **LangSmith is excluded.** No example sets `LANGSMITH_TRACING`, `LANGCHAIN_TRACING_V2`, or
  `LANGSMITH_API_KEY`. Observability is OpenTelemetry — see §5.
- **LangGraph Platform / Cloud is excluded.** Deployment is self-hosted; checkpointing is local
  SQLite or Postgres, never the managed service.
- **LangServe is excluded** — archived 2026-05-05, per Finding 3. Do not adopt it.

---

## 3. Pinned versions and security floors

Best practice #2 from the research report ("pin every package exactly") is not advice here, it is a
security control: Finding 7 records a three-CVE chain in the LangGraph checkpointer that
escalates from SQL injection to remote code execution.

```text
# requirements-langchain.txt
# Pinned 2026-07-26. Versions are the current releases recorded by the
# 2026-07-25 assessment (PyPI, retrieved 2026-07-25).
#
# SECURITY FLOORS — do not relax below these under any circumstance:
#   langgraph                     >= 1.0.10   (CVE-2026-28277, msgpack deserialization -> RCE)
#   langgraph-checkpoint-sqlite   >= 3.0.1    (CVE-2025-67644, SQL injection via filter dict)
#   langgraph-checkpoint-redis    >= 1.0.2    (CVE-2026-27022, query injection)
# The pins below already exceed every floor.

langchain==1.3.14
langgraph==1.2.9
langgraph-checkpoint-sqlite==3.1.0

# Provider packages — pin to the exact version you tested against.
langchain-anthropic==<pin-at-install-time>
langchain-openai==<pin-at-install-time>          # also used for LM Studio's OpenAI-compatible API

# Ecosystem components — add only the ones an example actually needs.
langchain-mcp-adapters==<pin-at-install-time>
deepagents==<pin-at-install-time>

# Observability (see §5). Not a LangChain package; no vendor coupling.
opentelemetry-sdk==<pin-at-install-time>
opentelemetry-exporter-otlp==<pin-at-install-time>
```

`<pin-at-install-time>` is deliberate. Those exact versions were **not** retrieved in this
deliverable, and inventing them would be worse than leaving the placeholder. Resolve them once, in
one place, at install time — and record the resolved set alongside the pins above.

### The checkpointer is a security boundary, not a storage detail

The durable lesson from the CVE chain is structural, and it survives the patched versions:

> **The checkpointer is simultaneously a deserialization boundary and a SQL boundary.**

Three rules follow, and they apply to every example in this folder:

1. **Never pass user-controlled input into `get_state_history(filter=...)`.** That is the exact
   precondition the CVE chain requires.
2. **Treat restored checkpoint state as untrusted input to the agent runtime** — ASGF L3 territory.
   Validate it on the way back in, the same way you would validate a tool result.
3. **Treat a checkpointer version bump as a security change**, subject to whatever review your
   security changes get — not as a routine dependency refresh.

---

## 4. Environment and hardware allocation

Inherited from Findings 5 and 6, and not re-measured here:

| Tier                             | Allocation                                                                                                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Reasoning (agent brain)**      | API models. **Not** a local 8B model — sub-14B tool-calling reliability is the binding weakness in any agent loop.                |
| **GPU (RTX 4060, 8,188 MiB)**    | Embeddings + reranking, permanently resident (~570 MB today, ~1.1 GB once a cross-encoder reranker is added).                     |
| **Local generation (LM Studio)** | An explicitly scoped tier: offline work, privacy-sensitive documents, cheap bulk classification. **Never tool-calling.**          |
| **Python environment**           | The shared venv at `core-component-00/platform/model-context-protocol-servers/.venv/`. Never install these dependencies globally. |

LM Studio has no LangChain partner package. Reach it through its OpenAI-compatible endpoint:

```python
from langchain_openai import ChatOpenAI

# LM Studio scoped tier ONLY — bulk classification, offline summarisation.
# Do not attach tools to this model. See Finding 6.
local_model = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed",          # LM Studio ignores the key; it is required by the client
    model="<the model id LM Studio reports>",
    timeout=120,                    # ASGF L3 Mandatory: every model call has a timeout
)
```

**Unverified precondition:** LM Studio's presence on this machine was never confirmed by the
2026-07-25 assessment (Appendix A records it as `NOT INSTALLED / NOT MEASURED`). Any example that reaches this
endpoint will fail until that precondition is closed.

### Model identifier convention

Examples use the `provider:model` string form resolved by LangChain's `init_chat_model`, e.g.
`"anthropic:claude-sonnet-5"`. **Substitute the exact identifier your pinned provider package
supports** — the specific string was not validated against `langchain-anthropic`, and provider
packages lag model releases. This is a placeholder convention, not a compatibility claim.

---

## 5. Observability without LangSmith

The open-source-only constraint has a real cost, and the research report named it: quality is the
most-reported production blocker for agent systems, and tracing is how quality problems get
diagnosed. Giving up LangSmith means bringing your own tracing, deliberately, before you build.

The minimum viable substitute — vendor-neutral, self-hosted:

```python
# cc00_langchain/telemetry.py
"""OpenTelemetry setup for CC-00 LangChain agents.

Deliberately NOT LangSmith: LangSmith is a hosted commercial service and is
excluded by the CEO's open-source-only constraint (research report, Out of Scope).
"""

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def install_tracing(service_name: str, endpoint: str = "http://localhost:4317") -> None:
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    trace.set_tracer_provider(provider)


tracer = trace.get_tracer("cc00.langchain")
```

The `ObservabilityMiddleware` in §7 emits the spans. What it records is chosen to answer the
questions an agent post-mortem actually asks: which model was called, how many tokens each slot
consumed, which tools ran, how many times the loop went round, and where it stopped.

**Honest limitation:** this gives you traces. It does not give you LangSmith's evaluation
harness, dataset management, or regression tracking. Those remain unsolved under the
open-source-only constraint and should be scoped as their own piece of work rather than assumed away.

---

## 6. Importing CC-00 implementations — a real constraint, and the fix

This section documents a concrete integration obstacle that the 2026-07-25 assessment phase did not
surface, found by static inspection of the CC-00 module tree on 2026-07-26. It is recorded as
Finding 11 in the research report's 2026-07-26 addendum.

**The obstacle.** All four CC-00 module roots expose a directory named `implementations/`:

```text
core-component-00/framework/02-context-engineering/implementations/
core-component-00/framework/03-harness-engineering/implementations/
core-component-00/framework/05-multi-agent-engineering/implementations/
core-component-00/framework/04-retrieval-augmented-generation/implementations/
```

CC-00's own test suites resolve this by putting **one** module root on `sys.path` and importing
`from implementations.<module>` — which is exactly why `core-component-00/CLAUDE.md` warns against
running all four test suites in a single process. A LangChain agent, however, legitimately needs
Layer 2, Layer 3, Layer 4, and Layer 5 code **in the same process at the same time**. The
`sys.path` convention cannot express that: only one module root can own the top-level name
`implementations`.

**Complicating detail** — the modules are not uniform in how they import:

| Module file                                                                                                                                  | Import style                                                    | Consequence                                |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------ |
| `context_assembler.py`, `context_compressor.py`, `error_boundary.py`, `context_monitor.py`, `tool_registry.py`, `retrieval.py`, `chunker.py` | stdlib only                                                     | Loadable straight from a file path         |
| `handoff_packet.py`, `swarm_orchestrator.py`, `pipeline.py`                                                                                  | relative (`from .shared_memory_log`, `from .chunker`)           | **Requires package context**               |
| `memory_store.py`                                                                                                                            | absolute (`from implementations.reflection_authoring import …`) | **Requires a top-level `implementations`** |

Only `multi-agent-engineering/implementations/` contains an `__init__.py`; the other three are
PEP 420 namespace packages.

**The fix.** Register each module root's `implementations/` directory as a package under a _unique_
alias, so relative imports resolve within their own module and the four roots stop colliding:

```python
# cc00_langchain/cc00_path.py
"""Loads CC-00 reference implementations under non-colliding package aliases.

Why this exists: all four CC-00 module roots contain a directory named
`implementations/`, so the sys.path convention used by CC-00's own test suites
(core-component-00/CLAUDE.md, "Import Path") can only ever expose one of them
per process. An agent needs several at once.

Verified 2026-07-26 by static inspection. NOT executed — this loader has not
been run. Shake it down before relying on it.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

# Adjust if this file is relocated. Points at the workspace's core-component-00/.
CC00 = Path(__file__).resolve().parents[2] / "core-component-00"

_MODULE_ROOTS = {
    "cc00_ce": CC00 / "engineering" / "context-engineering",
    "cc00_he": CC00 / "engineering" / "harness-engineering",
    "cc00_mae": CC00 / "engineering" / "multi-agent-engineering",
    "cc00_rag": CC00 / "retrieval-augmented-generation",
}


def _register(alias: str, module_root: Path) -> ModuleType:
    """Bind <module_root>/implementations as a package named `alias`."""
    if alias in sys.modules:
        return sys.modules[alias]

    pkg_dir = module_root / "implementations"
    if not pkg_dir.is_dir():
        raise FileNotFoundError(f"CC-00 module root has no implementations/: {module_root}")

    spec = importlib.machinery.ModuleSpec(alias, loader=None, is_package=True)
    pkg = importlib.util.module_from_spec(spec)
    pkg.__path__ = [str(pkg_dir)]          # makes `alias.<submodule>` importable
    sys.modules[alias] = pkg
    return pkg


for _alias, _root in _MODULE_ROOTS.items():
    _register(_alias, _root)

# memory_store.py uses the ABSOLUTE form `from implementations.reflection_authoring
# import ...`, so it needs a top-level `implementations` binding as well. Only one
# module root can hold that name; Context Engineering is the only module that needs
# it, so it gets it. If a second module later adopts the absolute form, this breaks
# loudly rather than silently — which is the correct failure mode.
sys.modules.setdefault("implementations", sys.modules["cc00_ce"])

# --- Layer 2: Context Engineering -------------------------------------------------
_ctx = importlib.import_module("cc00_ce.context_assembler")
ContextAssembler = _ctx.ContextAssembler
AssembledContext = _ctx.AssembledContext

# --- Layer 3: Harness Engineering -------------------------------------------------
_eb = importlib.import_module("cc00_he.error_boundary")
CircuitBreaker = _eb.CircuitBreaker
RateLimitError = _eb.RateLimitError
ValidationError = _eb.ValidationError
CC00TimeoutError = _eb.TimeoutError          # shadows the builtin — alias deliberately
ServiceUnavailableError = _eb.ServiceUnavailableError

_cm = importlib.import_module("cc00_he.context_monitor")
TokenBudgetManager = _cm.TokenBudgetManager
ContextMonitor = _cm.ContextMonitor

_tr = importlib.import_module("cc00_he.tool_registry")
ToolRegistry = _tr.ToolRegistry
TOOL_REGISTRY = _tr.TOOL_REGISTRY

# --- Layer 4: RAG ------------------------------------------------------------------
_pipe = importlib.import_module("cc00_rag.pipeline")
RAGPipeline = _pipe.RAGPipeline
RetrievedContext = _pipe.RetrievedContext
Document = importlib.import_module("cc00_rag.retrieval").Document

# --- Layer 5: Multi-Agent ----------------------------------------------------------
_hp = importlib.import_module("cc00_mae.handoff_packet")
HandoffPacket = _hp.HandoffPacket
HandoffTier = _hp.HandoffTier
```

**Finding worth escalating:** this is a packaging gap in CC-00 itself, not a LangChain problem. The
durable fix is to publish the four module roots as one installable `cc00` package with distinct
subpackage names. The loader above is a workaround that makes integration possible today; it should
not become the permanent answer. Recorded in the research report's Open Questions.

---

## 7. The ASGF Governance Kit

This is the reusable asset. Every product example in this folder imports from it rather than
re-deriving governance controls, which is the whole point: **LangChain confers no ASGF compliance;
it provides places to attach it.** The kit is those attachments, written once.

Middleware is the correct attachment point because `wrap_model_call` receives both the request and
the downstream handler, so it can inspect, rewrite, short-circuit, retry, or budget every model call
— structurally the same shape as CC-00's own `error_boundary.py` and `context_monitor.py`.

| Middleware                     | ASGF requirement closed                                     | Level                      |
| ------------------------------ | ----------------------------------------------------------- | -------------------------- |
| `FourSlotContextMiddleware`    | L2 — four-slot structure, slot priority, budget at assembly | **Mandatory** (all three)  |
| `TokenBudgetMiddleware`        | L3 — token budget monitor active                            | **Mandatory**              |
| `TypedErrorBoundaryMiddleware` | L3 — typed recovery, timeout, rate-limit backoff            | **Mandatory** (all three)  |
| `ToolGovernanceMiddleware`     | L3 — tool whitelist, tool-call limits                       | Required (when tools used) |
| `PIIMiddleware`                | L3 — PII scrub on input, scan on output                     | Required                   |
| `ObservabilityMiddleware`      | Cross-layer — diagnosis without LangSmith                   | (not an ASGF item)         |

Human-approval gating (L3 Required for high-risk) is **not** middleware — it uses LangGraph's
`interrupt()`, covered in `02-langgraph-examples.md` §4. Topology and handoff (L5 Mandatory) are
graph-level, covered in `02-langgraph-examples.md` §5–6.

```python
# cc00_langchain/asgf.py
"""ASGF governance middleware for LangChain v1 agents.

Each class closes a specific requirement from
core-component-00/framework/00-agent-systems-governance-framework/governance/compliance-standard.md
by delegating to the corresponding CC-00 reference implementation. The middleware
is glue; the controls themselves stay in CC-00, where they are already tested.

API surface verified against langchain-ai/docs 2026-07-26. NOT EXECUTED.
"""

from __future__ import annotations

import random
import re
import time
from typing import Any, Callable

from langchain.agents.middleware import AgentMiddleware, AgentState, ModelRequest
from langchain.agents.middleware.types import ModelResponse
from langgraph.runtime import Runtime

from .cc00_path import (
    CC00TimeoutError,
    ContextAssembler,
    RateLimitError,
    ServiceUnavailableError,
    TOOL_REGISTRY,
    TokenBudgetManager,
    ToolRegistry,
    ValidationError,
)
from .telemetry import tracer


# =====================================================================================
# ASGF Layer 2 — Context Engineering
# =====================================================================================


class FourSlotContextMiddleware(AgentMiddleware):
    """Impose CC-00's four-slot context structure on LangGraph's free-form state.

    Closes THE sharpest gap identified in the research report (Finding 8): the
    four-slot structure is ASGF **Mandatory**, LangGraph's default state is an
    unstructured message list, and "ad-hoc string concatenation is not acceptable"
    describes precisely what a naive create_agent adoption produces.

    Closes, in one place:
      - Four-slot context structure ..... Mandatory
      - Slot priority order defined ..... Mandatory  (via BUDGET_PROFILES + _priority_fill)
      - Token budget tracked at assembly  Mandatory  (ContextAssembler knows the budget
                                                      before dispatch, by construction)
      - Sacred context protected ........ Required   (add_sacred_context)

    Expects these optional keys on agent state, all absent-safe:
      sacred_context: list[str]           decisions that must never be compressed away
      retrieved:      list[dict]          RAG output; each dict needs at least "content"
      tool_outputs:   list[tuple[str, Any]]
    """

    def __init__(
        self,
        system_prompt: str,
        task_type: str = "multi_turn_reason",
        max_tokens: int = 128_000,
    ) -> None:
        self.system_prompt = system_prompt
        self.task_type = task_type          # selects the CC-00 slot budget profile
        self.max_tokens = max_tokens

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        state = request.state
        assembler = ContextAssembler(max_tokens=self.max_tokens)

        # --- System slot --------------------------------------------------------
        assembler.set_system(self.system_prompt)

        # --- Sacred context: re-injected every turn, never compressed -----------
        for decision in state.get("sacred_context", []) or []:
            assembler.add_sacred_context(decision)

        # --- Retrieved slot -----------------------------------------------------
        retrieved = state.get("retrieved", []) or []
        if retrieved:
            assembler.add_retrieved(
                retrieved,
                query=_latest_user_text(state.get("messages", [])),
                relevance_scores=[d.get("score", 0.5) for d in retrieved],
            )

        # --- History slot -------------------------------------------------------
        turns = [
            {"role": _role_of(m), "content": _text_of(m)}
            for m in state.get("messages", [])
        ]
        if turns:
            assembler.add_history(turns)

        # --- Tool output slot ---------------------------------------------------
        for tool_name, result in state.get("tool_outputs", []) or []:
            assembler.add_tool_output(tool_name, result)

        assembled = assembler.build(task_type=self.task_type)

        for warning in assembled.warnings:
            # Budget warnings are operational signal, not noise. Route them.
            tracer.start_span("cc00.context.warning").set_attribute("detail", warning)

        with tracer.start_as_current_span("cc00.context.assemble") as span:
            span.set_attribute("cc00.total_tokens", assembled.total_tokens)
            for slot, used in assembled.slot_usage.items():
                span.set_attribute(f"cc00.slot.{slot}", used)

        return handler(request.override(messages=assembled.messages))


def _role_of(message: Any) -> str:
    return getattr(message, "type", None) or getattr(message, "role", "user")


def _text_of(message: Any) -> str:
    content = getattr(message, "content", message)
    return content if isinstance(content, str) else str(content)


def _latest_user_text(messages: list[Any]) -> str:
    for message in reversed(messages or []):
        if _role_of(message) in ("human", "user"):
            return _text_of(message)
    return ""


# =====================================================================================
# ASGF Layer 3 — Harness Engineering
# =====================================================================================


class TokenBudgetMiddleware(AgentMiddleware):
    """Enforce a runtime token budget across the whole agent run.

    Closes: "Token budget monitor active" (Mandatory) and, by capping the loop,
    the practical half of "Tool call limits enforced".

    FourSlotContextMiddleware budgets a single call; this budgets the session.
    An agent that stays inside its per-call budget can still burn a month of
    quota by looping four hundred times.
    """

    def __init__(self, max_tokens: int = 128_000, max_model_calls: int = 25) -> None:
        self.budget = TokenBudgetManager(max_tokens=max_tokens)
        self.max_model_calls = max_model_calls
        self._calls = 0

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        self._calls += 1
        if self._calls > self.max_model_calls:
            raise RuntimeError(
                f"ASGF L3: model-call cap reached ({self.max_model_calls}). "
                "Unbounded agent loops are how a token budget disappears at 3am."
            )

        if not self.budget.is_within_budget():
            raise RuntimeError(
                f"ASGF L3: token budget exhausted "
                f"({self.budget.get_budget_percentage():.1f}% consumed)."
            )

        response = handler(request)

        usage = getattr(response, "usage_metadata", None) or {}
        self.budget.record_tokens("input", usage.get("input_tokens", 0))
        self.budget.record_tokens("output", usage.get("output_tokens", 0))
        return response


class TypedErrorBoundaryMiddleware(AgentMiddleware):
    """Distinct recovery paths per error class + circuit breaker.

    Closes:
      - Error boundary with typed recovery ...... Mandatory
      - Rate-limit retry with exponential backoff Mandatory
      - Timeout enforcement ..................... Mandatory (paired with a client timeout)

    ASGF is explicit that "catch-all exception handlers are not acceptable", which
    is why this does not wrap everything in one `except Exception`. LangChain's own
    `.with_retry()` is closer to a catch-all; this is the typed version.

    NOTE: the exception types raised by a provider package will NOT be CC-00's
    exception classes. Map them in `_classify` for the providers you actually use —
    this is the one method that MUST be adapted before production use.
    """

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0) -> None:
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.breaker = CircuitBreaker()

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        if self.breaker.is_open():
            raise ServiceUnavailableError(
                f"Circuit breaker open ({self.breaker.get_state()}); refusing the call."
            )

        for attempt in range(self.max_retries):
            started = time.monotonic()
            try:
                response = handler(request)
            except Exception as exc:                      # noqa: BLE001 — re-raised below
                kind = self._classify(exc)
                self.breaker.record_failure(kind)

                if kind == "rate_limit" and attempt < self.max_retries - 1:
                    # Exponential backoff WITH jitter. Immediate retry is a Mandatory failure.
                    delay = self.base_delay * (2**attempt) + random.uniform(0, 0.5)
                    time.sleep(delay)
                    continue

                if kind == "timeout" and attempt < self.max_retries - 1:
                    # Retry once at a reduced context footprint rather than identically.
                    continue

                if kind == "validation":
                    # Never retried blind: a schema violation repeats deterministically.
                    raise ValidationError(f"Model output failed validation: {exc}") from exc

                raise

            self.breaker.record_success((time.monotonic() - started) * 1000)
            return response

        raise ServiceUnavailableError(f"Exhausted {self.max_retries} attempts.")

    @staticmethod
    def _classify(exc: Exception) -> str:
        """Map a provider exception onto a CC-00 error class.

        ADAPT THIS. String matching is a starting point, not a design — replace it
        with `isinstance` checks against your pinned provider's exception types.
        """
        if isinstance(exc, RateLimitError):
            return "rate_limit"
        if isinstance(exc, (CC00TimeoutError, TimeoutError)):
            return "timeout"
        if isinstance(exc, ValidationError):
            return "validation"

        text = f"{type(exc).__name__} {exc}".lower()
        if "429" in text or "rate" in text and "limit" in text:
            return "rate_limit"
        if "timeout" in text or "timed out" in text:
            return "timeout"
        if "validation" in text or "schema" in text:
            return "validation"
        return "unknown"


class ToolGovernanceMiddleware(AgentMiddleware):
    """Whitelist tools and cap per-task call counts from the CC-00 registry.

    Closes:
      - Tool registry / whitelist defined ... Required when tools used
      - Tool call limits enforced ........... Required when tools used

    The registry is the single source of truth for what an agent may call, how long
    each call may take, how often it may be called, and whether it needs a human.
    `requires_approval` is read here but ENFORCED in the graph via interrupt() —
    see 02-langgraph-examples.md §4. Reading it without enforcing it is worse than
    not reading it, because it looks like a control.
    """

    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or ToolRegistry(TOOL_REGISTRY)

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        allowed = [t for t in request.tools if self.registry.is_allowed_tool(_tool_name(t))]
        rejected = {_tool_name(t) for t in request.tools} - {_tool_name(t) for t in allowed}
        if rejected:
            # Fail loudly at wiring time. A tool silently dropped at runtime is a
            # debugging nightmare and reads as a model failure, not a config error.
            raise ValueError(
                f"Tools not in the CC-00 registry: {sorted(rejected)}. "
                "Register them in tool_registry.TOOL_REGISTRY or remove them."
            )
        return handler(request.override(tools=allowed))


def _tool_name(tool: Any) -> str:
    return getattr(tool, "name", None) or getattr(tool, "__name__", str(tool))


class PIIMiddleware(AgentMiddleware):
    """Redact PII from model inputs; scan model outputs for leakage.

    Closes:
      - PII scrubbing on inputs .. Required
      - PII scanning on outputs .. Required

    HONEST LIMITATION: the patterns below are a starting point covering email,
    phone, and common national-ID shapes. They are NOT a compliance-grade PII
    detector and will miss names, addresses, and free-text identifiers. Treat this
    as the hook, and put a real detector behind it before handling regulated data.
    """

    PATTERNS = {
        "email": re.compile(r"\b[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
        "phone": re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}\b"),
        "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    }

    def __init__(self, block_on_output_leak: bool = True) -> None:
        self.block_on_output_leak = block_on_output_leak

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        scrubbed = [self._scrub_message(m) for m in request.messages]
        response = handler(request.override(messages=scrubbed))

        found = self._scan(_text_of(getattr(response, "result", response)))
        if found and self.block_on_output_leak:
            raise ValidationError(f"PII detected in model output: {sorted(found)}")
        return response

    def _scrub_message(self, message: Any) -> Any:
        text = _text_of(message)
        for label, pattern in self.PATTERNS.items():
            text = pattern.sub(f"[REDACTED:{label}]", text)
        try:
            return message.model_copy(update={"content": text})
        except AttributeError:
            return {"role": _role_of(message), "content": text}

    def _scan(self, text: str) -> set[str]:
        return {label for label, pattern in self.PATTERNS.items() if pattern.search(text)}


# =====================================================================================
# Cross-layer — observability (no LangSmith)
# =====================================================================================


class ObservabilityMiddleware(AgentMiddleware):
    """Emit an OpenTelemetry span per model call.

    Not an ASGF requirement — a practical one. The research report records
    quality as the top production blocker for agent systems, and tracing is how
    quality problems get diagnosed. Under the open-source-only constraint this
    replaces LangSmith.
    """

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        with tracer.start_as_current_span("cc00.agent.model_call") as span:
            span.set_attribute("cc00.message_count", len(request.messages))
            span.set_attribute("cc00.tool_count", len(request.tools))
            response = handler(request)
            usage = getattr(response, "usage_metadata", None) or {}
            span.set_attribute("cc00.input_tokens", usage.get("input_tokens", 0))
            span.set_attribute("cc00.output_tokens", usage.get("output_tokens", 0))
            return response


# =====================================================================================
# The standard stack
# =====================================================================================


def cc00_middleware_stack(
    system_prompt: str,
    task_type: str = "multi_turn_reason",
    max_tokens: int = 128_000,
    max_model_calls: int = 25,
) -> list[AgentMiddleware]:
    """The default CC-00 governance stack. ORDER IS SIGNIFICANT.

    Middleware wraps outward-in: the first entry is the outermost wrapper and sees
    the call first. The ordering below is deliberate:

      1. Observability ...... outermost, so its span covers retries and failures
      2. TypedErrorBoundary . retries INSIDE the span, outside everything else
      3. TokenBudget ........ counts every attempt, including retried ones
      4. PII ................ scrubs after budgeting, before assembly
      5. ToolGovernance ..... filters the tool list
      6. FourSlotContext .... innermost: the LAST thing to touch messages before
                              dispatch, so nothing downstream can undo the structure

    Reordering 6 is the common mistake: any middleware that rewrites messages after
    the assembler has run silently destroys the Mandatory four-slot guarantee.
    """
    return [
        ObservabilityMiddleware(),
        TypedErrorBoundaryMiddleware(),
        TokenBudgetMiddleware(max_tokens=max_tokens, max_model_calls=max_model_calls),
        PIIMiddleware(),
        ToolGovernanceMiddleware(),
        FourSlotContextMiddleware(
            system_prompt=system_prompt, task_type=task_type, max_tokens=max_tokens
        ),
    ]
```

### Known gaps in the kit, stated plainly

| Gap                                                                 | Why it is left open                                                                                            |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `_classify` uses string matching as a fallback                      | Provider exception types are pin-specific. Mapping them requires the pinned packages, which are not installed. |
| `PIIMiddleware` patterns are shape-based only                       | Name/address detection needs a real NER model. The hook is the deliverable; the detector is separate work.     |
| `TokenBudgetMiddleware` state is per-instance, not per-thread       | Correct for a single-run agent; a multi-tenant server needs the budget keyed by `thread_id`.                   |
| `ObservabilityMiddleware` records usage, not prompt/response bodies | Deliberate — bodies carry the PII the layer above just scrubbed.                                               |
| Nothing here is tested                                              | No LangChain installed. See §1.                                                                                |

---

## 8. File map

| File                                    | Product                                      | What it demonstrates                                               |
| --------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------ |
| `00-conventions-and-baseline.md`        | —                                            | This file: pins, environment, the governance kit                   |
| `01-langchain-examples.md`              | `langchain` 1.3.14                           | `create_agent`, middleware, structured output, tools               |
| `02-langgraph-examples.md`              | `langgraph` 1.2.9                            | Typed state, checkpointing, `interrupt()`, topology, `Command`     |
| `03-deepagents-examples.md`             | `deepagents`                                 | Planning, virtual filesystem, subagents, `interrupt_on`            |
| `04-langchain-mcp-adapters-examples.md` | `langchain-mcp-adapters`                     | Bridging this workspace's governed MCP servers into tools          |
| `05-reference-applications.md`          | `open_deep_research`, `open-swe`, `openwiki` | What to harvest from them, and what not to adopt                   |
| `06-ecosystem-integration-example.md`   | **All of the above**                         | One end-to-end system integrating the ecosystem                    |
| `07-best-practices-and-asgf-mapping.md` | —                                            | The practice catalogue and the full requirement-by-requirement map |

---

**Document status:** Reference examples — unexecuted. See §1.
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-26
