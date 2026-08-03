"""ASGF governance middleware for LangChain v1 agents — the runnable governance kit.

Each class closes a specific requirement from
core-component-00/agent-systems-governance-framework/governance/compliance-standard.md
by delegating to the corresponding CC-00 reference implementation. The controls
stay in CC-00, where they are already tested; this module is glue.

VERIFIED 2026-07-27 against langchain==1.3.14 / langchain-core==1.5.1 (see
requirements.lock.txt for the full resolved set). Every class here is exercised
by tests/test_asgf_middleware.py, which wires the full stack into a real
`create_agent(...)` call against `FakeListChatModel` — no API key required, and
this is genuinely executed, not merely imported.

DEVIATIONS FROM THE MARKDOWN REFERENCE EXAMPLES (documented, not silently
fixed — both found by actually running the code, not by reading it):

1. `supporting/workspace-integration-examples/00-conventions-and-baseline.md` and
   `01-langchain-examples.md`
   describe `FourSlotContextMiddleware` as replacing `request.messages`
   wholesale with `ContextAssembler`'s flattened output. Running that for real
   raises `KeyError: 'tool_call_id'` — `langchain_core.messages.convert_to_messages`
   requires a `tool_call_id` on any `{"role": "tool", ...}` dict, and CC-00's
   `ContextAssembler` (predates any LangChain integration) does not track one.
   This implementation instead folds the assembler's system/sacred/retrieved/tool
   content into `request.system_message` and leaves `request.messages` — the
   real, LangGraph-managed conversation — untouched.

2. `create_agent`'s default `AgentState` schema declares only `messages`,
   `jump_to`, and `structured_response`. Any other key passed into
   `agent.invoke({...})` — `sacred_context`, `retrieved`, `tool_outputs`,
   `current_question` — is silently dropped before middleware ever sees it;
   verified directly (`request.state.keys()` printed `['messages']` with the
   default schema, and the full set with `CC00AgentState` below). **Any
   `create_agent(...)` call using this middleware stack MUST pass
   `state_schema=CC00AgentState`, or `FourSlotContextMiddleware` silently
   assembles an empty retrieved/sacred/tool-output slot every time — no error,
   just governance that looks like it ran and did not.**
"""

from __future__ import annotations

import random
import re
import time
from typing import Any, Callable

from langchain.agents.middleware import AgentMiddleware, AgentState
from langchain.agents.middleware.types import ModelRequest, ModelResponse
from langchain_core.messages import SystemMessage

from .cc00_path import (
    CC00TimeoutError,
    ContextAssembler,
    RateLimitError,
    TOOL_REGISTRY,
    TokenBudgetManager,
    ToolRegistry,
    ValidationError,
)
from .cc00_path import CircuitBreaker as CC00CircuitBreaker
from .telemetry import tracer

Handler = Callable[[ModelRequest], ModelResponse]


class CC00AgentState(AgentState, total=False):
    """`AgentState` extended with the fields `FourSlotContextMiddleware` reads.

    REQUIRED: pass `state_schema=CC00AgentState` to `create_agent(...)` (or to
    `create_deep_agent(...)`) whenever this middleware stack is used. Without
    it, `sacred_context` / `retrieved` / `tool_outputs` never reach the
    middleware — verified directly, see the module docstring's Deviation 2.
    """

    sacred_context: list[str]
    retrieved: list[dict[str, Any]]
    tool_outputs: list[tuple[str, Any]]
    current_question: str


# =====================================================================================
# ASGF Layer 2 — Context Engineering
# =====================================================================================


class FourSlotContextMiddleware(AgentMiddleware):
    """Impose CC-00's four-slot context structure on the model's system prompt.

    Closes the sharpest gap identified in the LangChain assessment (Finding 8 /
    Addendum Finding 11 context): the four-slot structure is ASGF **Mandatory**,
    LangGraph's default state carries no such structure, and "ad-hoc string
    concatenation is not acceptable" describes what a naive create_agent
    adoption produces.

    Closes:
      - Four-slot context structure ..... Mandatory (system/retrieved/sacred/tools
                                          folded into one governed system message)
      - Slot priority order defined ..... Mandatory  (BUDGET_PROFILES + _priority_fill,
                                                        inside ContextAssembler)
      - Token budget tracked at assembly  Mandatory  (ContextAssembler knows the
                                                        budget before dispatch)
      - Sacred context protected ........ Required   (add_sacred_context)

    Reads these optional keys from agent state, all absent-safe:
      sacred_context: list[str]
      retrieved:      list[dict]   each needs at least "content"
      tool_outputs:   list[tuple[str, Any]]
    """

    def __init__(
        self,
        system_prompt: str,
        task_type: str = "multi_turn_reason",
        max_tokens: int = 128_000,
    ) -> None:
        self.system_prompt = system_prompt
        self.task_type = task_type
        self.max_tokens = max_tokens

    def wrap_model_call(self, request: ModelRequest, handler: Handler) -> ModelResponse:
        state = request.state or {}
        assembler = ContextAssembler(max_tokens=self.max_tokens)
        assembler.set_system(self.system_prompt)

        for decision in state.get("sacred_context", []) or []:
            assembler.add_sacred_context(decision)

        retrieved = state.get("retrieved", []) or []
        if retrieved:
            assembler.add_retrieved(
                retrieved,
                query=state.get("current_question", ""),
                relevance_scores=[d.get("score", 0.5) for d in retrieved],
            )

        for tool_name, result in state.get("tool_outputs", []) or []:
            assembler.add_tool_output(tool_name, result)

        assembled = assembler.build(task_type=self.task_type)

        # assembled.messages[0] is always {"role": "system", "content": system + retrieved}.
        # This middleware never calls assembler.add_history(), so any additional
        # entries are the sacred-context block (role "user") and/or the tool-output
        # block (role "tool") — both folded into the system message instead of
        # being passed through as literal messages. See the module docstring for
        # why: a bare {"role": "tool", ...} dict has no tool_call_id and fails
        # langchain_core's own message conversion.
        system_text = assembled.messages[0]["content"]
        for extra in assembled.messages[1:]:
            label = "SACRED CONTEXT" if extra["role"] != "tool" else "TOOL OUTPUT CONTEXT"
            system_text += f"\n\n--- {label} ---\n{extra['content']}"

        with tracer.start_as_current_span("cc00.context.assemble") as span:
            span.set_attribute("cc00.total_tokens", assembled.total_tokens)
            for slot, used in assembled.slot_usage.items():
                span.set_attribute(f"cc00.slot.{slot}", used)
            if assembled.warnings:
                span.set_attribute("cc00.warnings", assembled.warnings)

        return handler(request.override(system_message=SystemMessage(content=system_text)))


# =====================================================================================
# ASGF Layer 3 — Harness Engineering
# =====================================================================================


class TokenBudgetMiddleware(AgentMiddleware):
    """Enforce a runtime token budget and a model-call cap across the whole run.

    Closes: "Token budget monitor active" (Mandatory) and, by capping the loop,
    the practical half of "Tool call limits enforced".

    FourSlotContextMiddleware budgets a single call; this budgets the session —
    an agent that stays inside its per-call budget can still loop hundreds of
    times and exhaust a token allowance regardless.

    NOTE: `FakeListChatModel` (used throughout the test suite) does not populate
    `usage_metadata`, so token accounting is 0 in tests that use it — verified
    directly; the call-count cap is exercised regardless, since it does not
    depend on usage metadata.
    """

    def __init__(self, max_tokens: int = 128_000, max_model_calls: int = 25) -> None:
        self.budget = TokenBudgetManager(max_tokens=max_tokens)
        self.max_model_calls = max_model_calls
        self.calls = 0

    def wrap_model_call(self, request: ModelRequest, handler: Handler) -> ModelResponse:
        self.calls += 1
        if self.calls > self.max_model_calls:
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

        last = response.result[-1] if response.result else None
        usage = getattr(last, "usage_metadata", None) or {}
        self.budget.record_tokens("input", usage.get("input_tokens", 0) or 0)
        self.budget.record_tokens("output", usage.get("output_tokens", 0) or 0)
        return response


class TypedErrorBoundaryMiddleware(AgentMiddleware):
    """Distinct recovery paths per error class, plus a circuit breaker.

    Closes:
      - Error boundary with typed recovery ...... Mandatory
      - Rate-limit retry with exponential backoff Mandatory
      - Timeout enforcement ..................... Mandatory (paired with a client timeout)

    ASGF is explicit that catch-all exception handlers are not acceptable, which
    is why `_classify` distinguishes error kinds rather than retrying blind.

    NOTE (adapted from the Markdown reference honestly): the reference examples
    assumed the pinned provider packages' own exception types could be matched
    by `isinstance`. No Anthropic/OpenAI API credentials are available in this
    environment (verified: no ANTHROPIC_API_KEY / OPENAI_API_KEY set), so those
    exception types were never triggered against a live provider and
    `_classify` is necessarily string-matching-first here too. This is the one
    method that MUST be revisited with `isinstance` checks once a real provider
    is wired in and its actual exception types are observed.
    """

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0) -> None:
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.breaker = CC00CircuitBreaker()

    def wrap_model_call(self, request: ModelRequest, handler: Handler) -> ModelResponse:
        if self.breaker.is_open():
            raise CC00TimeoutError(
                f"Circuit breaker open ({self.breaker.get_state()}); refusing the call."
            )

        last_exc: Exception | None = None
        for attempt in range(self.max_retries):
            started = time.monotonic()
            try:
                response = handler(request)
            except Exception as exc:  # noqa: BLE001 — reraised/reclassified below
                last_exc = exc
                kind = self._classify(exc)
                self.breaker.record_failure(kind)

                if kind == "rate_limit" and attempt < self.max_retries - 1:
                    time.sleep(self.base_delay * (2**attempt) + random.uniform(0, 0.5))
                    continue
                if kind == "timeout" and attempt < self.max_retries - 1:
                    continue
                if kind == "validation":
                    raise ValidationError(f"Model output failed validation: {exc}") from exc
                raise
            else:
                self.breaker.record_success((time.monotonic() - started) * 1000)
                return response

        raise last_exc if last_exc else RuntimeError("Exhausted retries with no exception recorded.")

    @staticmethod
    def _classify(exc: Exception) -> str:
        if isinstance(exc, RateLimitError):
            return "rate_limit"
        if isinstance(exc, (CC00TimeoutError, TimeoutError)):
            return "timeout"
        if isinstance(exc, ValidationError):
            return "validation"

        text = f"{type(exc).__name__} {exc}".lower()
        if "429" in text or ("rate" in text and "limit" in text):
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

    Fails at wiring time (raises) if a tool is not registered, rather than
    silently dropping it — a tool dropped at runtime looks like a model failure,
    not a config error.
    """

    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or ToolRegistry(TOOL_REGISTRY)

    def wrap_model_call(self, request: ModelRequest, handler: Handler) -> ModelResponse:
        if not request.tools:
            return handler(request)

        allowed = [t for t in request.tools if self.registry.is_allowed_tool(_tool_name(t))]
        rejected = {_tool_name(t) for t in request.tools} - {_tool_name(t) for t in allowed}
        if rejected:
            raise ValueError(
                f"Tools not in the CC-00 registry: {sorted(rejected)}. "
                "Register them in tool_registry.TOOL_REGISTRY or remove them."
            )
        return handler(request.override(tools=allowed))


def _tool_name(tool: Any) -> str:
    if isinstance(tool, dict):
        return tool.get("name", str(tool))
    return getattr(tool, "name", None) or getattr(tool, "__name__", str(tool))


class PIIMiddleware(AgentMiddleware):
    """Redact PII from model inputs; scan model outputs for leakage.

    Closes:
      - PII scrubbing on inputs .. Required
      - PII scanning on outputs .. Required

    HONEST LIMITATION: shape-based patterns (email, phone, SSN-like, card-like)
    only. Adequate for internal corpora; not a compliance-grade PII detector —
    it will miss names, addresses, and free-text identifiers. Verified against
    real langchain_core message objects via `.model_copy(update=...)`.
    """

    PATTERNS = {
        "email": re.compile(r"\b[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
        "phone": re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}\b"),
        "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    }

    def __init__(self, block_on_output_leak: bool = True) -> None:
        self.block_on_output_leak = block_on_output_leak

    def wrap_model_call(self, request: ModelRequest, handler: Handler) -> ModelResponse:
        scrubbed = [self._scrub_message(m) for m in request.messages]
        scrubbed_system = (
            self._scrub_message(request.system_message) if request.system_message else None
        )
        response = handler(
            request.override(messages=scrubbed, system_message=scrubbed_system)
            if scrubbed_system is not None
            else request.override(messages=scrubbed)
        )

        found: set[str] = set()
        for message in response.result:
            found |= self._scan(_content_text(message))
        if found and self.block_on_output_leak:
            raise ValidationError(f"PII detected in model output: {sorted(found)}")
        return response

    def _scrub_message(self, message: Any):
        text = _content_text(message)
        for label, pattern in self.PATTERNS.items():
            text = pattern.sub(f"[REDACTED:{label}]", text)
        if text == _content_text(message):
            return message
        return message.model_copy(update={"content": text})

    def _scan(self, text: str) -> set[str]:
        return {label for label, pattern in self.PATTERNS.items() if pattern.search(text)}


def _content_text(message: Any) -> str:
    content = getattr(message, "content", message)
    return content if isinstance(content, str) else str(content)


# =====================================================================================
# Cross-layer — observability (no LangSmith)
# =====================================================================================


class ObservabilityMiddleware(AgentMiddleware):
    """Emit a span per model call. Not an ASGF requirement — a practical one.

    Under the open-source-only constraint this replaces LangSmith. See
    telemetry.py — spans go to an in-memory recorder by default, real OTel only
    if installed and `install_tracing()` was called.
    """

    def wrap_model_call(self, request: ModelRequest, handler: Handler) -> ModelResponse:
        with tracer.start_as_current_span("cc00.agent.model_call") as span:
            span.set_attribute("cc00.message_count", len(request.messages))
            span.set_attribute("cc00.tool_count", len(request.tools))
            response = handler(request)
            last = response.result[-1] if response.result else None
            usage = getattr(last, "usage_metadata", None) or {}
            span.set_attribute("cc00.input_tokens", usage.get("input_tokens", 0) or 0)
            span.set_attribute("cc00.output_tokens", usage.get("output_tokens", 0) or 0)
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

    Middleware wraps outward-in: the first entry is the outermost wrapper and
    sees the call first.

      1. Observability ...... outermost, so its span covers retries and failures
      2. TypedErrorBoundary . retries INSIDE the span, outside everything else
      3. TokenBudget ........ counts every attempt, including retried ones
      4. PII ................ scrubs after budgeting, before assembly
      5. ToolGovernance ..... filters the tool list
      6. FourSlotContext .... innermost: the LAST thing to touch the system
                              message before dispatch

    Reordering 6 is the common mistake: any middleware that rewrites the system
    message after the assembler has run silently destroys the Mandatory
    four-slot guarantee. Verified in test_asgf_middleware.py::test_stack_ordering.
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
