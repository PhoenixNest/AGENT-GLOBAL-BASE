"""
Error Boundary Pattern Implementation

Scope: LLM application layer — Python programs making outbound LLM API calls
(Anthropic SDK, OpenAI SDK, etc.). Handles provider-side failures: HTTP 429
rate limits, request timeouts, and response validation errors.

This module does NOT govern Claude Code tool-call failures. Those are handled
by the harness-error-boundary-monitor.ps1 hook at the Claude Code session layer.
Do not use this module as a substitute for that hook, or vice versa.

This module provides wrapper classes for safely calling LLM models with
tiered error recovery paths. Each error type has a defined recovery strategy.
"""

import asyncio
import random
import sys
import time
from typing import Any, Dict, Optional


MODEL_TIER_TIMEOUTS = {
    "haiku": 15,
    "sonnet": 30,
    "opus": 90,
}


def get_timeout_for_model(model_id: str) -> int:
    model_lower = model_id.lower()
    if "haiku" in model_lower:
        return MODEL_TIER_TIMEOUTS["haiku"]
    if "opus" in model_lower:
        return MODEL_TIER_TIMEOUTS["opus"]
    return MODEL_TIER_TIMEOUTS["sonnet"]


# ---------------------------------------------------------------------------
# Minimal structured logging helpers
# In production replace with structlog, loguru, or your observability stack.
# ---------------------------------------------------------------------------
def _log(level: str, message: str, **kwargs) -> None:
    extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"[{level}] {message} {extra}".rstrip(), file=sys.stderr)


def log_error(message: str, **kwargs) -> None:
    _log("ERROR", message, **kwargs)


def log_warning(message: str, **kwargs) -> None:
    _log("WARNING", message, **kwargs)


def log_info(message: str, **kwargs) -> None:
    _log("INFO", message, **kwargs)


class ValidationError(Exception):
    """Raised when output doesn't match expected schema."""

    pass


class TimeoutError(Exception):
    """Raised when model call exceeds timeout threshold."""

    pass


class RateLimitError(Exception):
    """Raised when provider returns rate limit error (429)."""

    pass


class ServiceUnavailableError(Exception):
    """Raised when a local/self-hosted service (Qdrant, the embedder-service)
    is unreachable or refuses a connection. Distinct from RateLimitError:
    RateLimitError models a remote LLM-provider backpressure signal (HTTP
    429), which has no equivalent for a local service outage — reusing it
    here would misrepresent the failure as provider throttling rather than
    "the process/socket isn't there."""

    pass


class ContextOverflowError(Exception):
    """Raised when conversation exceeds token budget."""

    pass


def _classify_provider_error(exc: Exception) -> Optional[str]:
    """Classify a raw provider-SDK exception (anthropic.RateLimitError,
    openai.RateLimitError, their timeout equivalents, or anything shaped like one)
    into this module's typed vocabulary.

    Classified structurally (HTTP status code, exception class name) rather than via
    isinstance against imported anthropic/openai classes: neither SDK is a dependency
    of this module, and structural matching also works across SDK major versions
    without pinning to a specific class path.

    Returns "rate_limit", "timeout", or None if `exc` isn't a recognized provider error.
    """
    name = type(exc).__name__
    if getattr(exc, "status_code", None) == 429 or "RateLimit" in name:
        return "rate_limit"
    if "Timeout" in name:
        return "timeout"
    return None


from enum import Enum


class CircuitBreakerState(Enum):
    CLOSED = "closed"
    DEGRADED = "degraded"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """
    4-state circuit breaker with composite health scoring.
    Health = error_rate*0.4 + (1 - p99_latency_ratio)*0.4 + (1 - rate_429_ratio)*0.2
    CLOSED >= 0.8 | DEGRADED 0.5-0.8 | OPEN < 0.5 | HALF_OPEN after 60s cooldown
    """

    COOLDOWN_SECONDS = 60

    def __init__(self):
        self.state = CircuitBreakerState.CLOSED
        self._success_count = 0
        self._failure_count = 0
        self._rate_limit_count = 0
        self._total_latency_ms = 0.0
        self._sample_count = 0
        self._opened_at = None

    def record_success(self, latency_ms: float) -> None:
        self._success_count += 1
        self._total_latency_ms += latency_ms
        self._sample_count += 1
        self._update_state()

    def record_failure(self, error_type: str) -> None:
        self._failure_count += 1
        if error_type == "rate_limit":
            self._rate_limit_count += 1
        self._update_state()

    def is_open(self) -> bool:
        if self.state == CircuitBreakerState.HALF_OPEN:
            return False
        return self.state == CircuitBreakerState.OPEN

    def get_state(self) -> CircuitBreakerState:
        return self.state

    def _health_score(self) -> float:
        total = self._success_count + self._failure_count
        if total == 0:
            return 1.0
        error_rate = self._failure_count / total
        rate_429_ratio = self._rate_limit_count / total
        avg_latency = self._total_latency_ms / max(self._sample_count, 1)
        p99_ratio = min(avg_latency / 5000.0, 1.0)
        return (1 - error_rate) * 0.4 + (1 - p99_ratio) * 0.4 + (1 - rate_429_ratio) * 0.2

    def _update_state(self) -> None:
        import time

        if self.state == CircuitBreakerState.OPEN:
            if self._opened_at and (time.monotonic() - self._opened_at) >= self.COOLDOWN_SECONDS:
                self.state = CircuitBreakerState.HALF_OPEN
            return
        score = self._health_score()
        if score >= 0.8:
            self.state = CircuitBreakerState.CLOSED
        elif score >= 0.5:
            self.state = CircuitBreakerState.DEGRADED
        else:
            self.state = CircuitBreakerState.OPEN
            self._opened_at = time.monotonic()


# Process-shared circuit-breaker registry, keyed by target service. Concurrent
# SafeModelCall instances targeting the same service share one breaker's failure
# evidence instead of each starting from a fresh, per-instance CLOSED state.
_circuit_breaker_registry: Dict[str, "CircuitBreaker"] = {}


def get_circuit_breaker(service_key: str) -> "CircuitBreaker":
    """Return the shared CircuitBreaker for `service_key`, creating it on first use."""
    if service_key not in _circuit_breaker_registry:
        _circuit_breaker_registry[service_key] = CircuitBreaker()
    return _circuit_breaker_registry[service_key]


def reset_circuit_breaker_registry() -> None:
    """Clear the shared registry. Test/ops utility only — production code should not
    call this, since the registry is meant to persist failure evidence for the life
    of the process, not per-call."""
    _circuit_breaker_registry.clear()


class SafeModelCall:
    """
    Wrapper for model calls with tiered error recovery.

    Usage:
        call = SafeModelCall(client, model="claude-3-opus", timeout=30)
        result = call.execute(prompt, schema=output_schema)
    """

    def __init__(self, client, model_id, timeout=None, max_retries=3, service_key=None):
        self.client = client
        self.model_id = model_id
        self.timeout = timeout if timeout is not None else get_timeout_for_model(model_id)
        self.max_retries = max_retries
        # Target service defaults to model_id — the dimension callers already provide.
        # Pass an explicit service_key when several model_ids front the same backend.
        self.circuit_breaker = get_circuit_breaker(service_key or model_id)

    async def execute(self, prompt: str, schema=None) -> dict:
        """
        Execute model call with error boundary and retry logic.

        Args:
            prompt: The prompt to send to the model
            schema: Optional JSON Schema for output validation

        Returns:
            Dict with 'success' flag and either 'data' or 'error' keys
        """
        if self.circuit_breaker.is_open():
            raise RateLimitError("Circuit breaker OPEN — request blocked")

        # Check rate limit headers from any cached responses
        if (
            hasattr(self.client, "rate_limit_remaining")
            and self.client.rate_limit_remaining == 0
        ):
            raise RateLimitError("Rate limited by provider")

        for attempt in range(self.max_retries):
            try:
                # Validate prompt structure first
                if not self._validate_prompt(prompt):
                    raise ValidationError("Invalid prompt structure")

                # Make the call with timeout
                response = await asyncio.wait_for(
                    self.client.messages.create(messages=[prompt]),
                    timeout=self.timeout,
                )

                # Validate output format against schema if provided
                if schema and not self._validate_response(response, schema):
                    raise ValidationError("Response doesn't match expected schema")

                return {
                    "success": True,
                    "model_version": self.model_id,
                    "data": response.content,
                    "attempt": attempt + 1,
                }

            except (asyncio.TimeoutError, TimeoutError):
                log_error(f"Timeout on model call (model={self.model_id})")
                return {
                    "success": False,
                    "error": {"code": "TIMEOUT", "message": "Request timed out"},
                }

            except RateLimitError as e:
                # Let caller handle retry with backoff
                raise

            except ValidationError as e:
                log_error(f"Validation failed: {e}")
                return {
                    "success": False,
                    "error": {"code": "FORMAT_ERROR", "message": str(e)},
                }

            except Exception as e:
                # Classify raw provider-SDK errors (anthropic.RateLimitError,
                # openai.RateLimitError, their timeout equivalents) before falling
                # through to the generic catch-all below.
                classification = _classify_provider_error(e)
                if classification == "rate_limit":
                    log_warning(
                        f"Provider rate limit classified from {type(e).__name__} "
                        f"(model={self.model_id})"
                    )
                    raise RateLimitError(str(e)) from e

                if classification == "timeout":
                    log_error(f"Provider timeout on model call (model={self.model_id})")
                    return {
                        "success": False,
                        "error": {"code": "TIMEOUT", "message": "Request timed out"},
                    }

                # Catch-all for genuinely unexpected errors
                log_error(f"Unexpected error: {type(e).__name__}: {e}")
                return {
                    "success": False,
                    "error": {"code": "UNKNOWN_ERROR", "message": str(e)},
                }

        # All retries exhausted
        return {
            "success": False,
            "error": {
                "code": "MAX_RETRIES_EXCEEDED",
                "message": "All retry attempts failed",
            },
        }

    def _validate_prompt(self, prompt) -> bool:
        """Basic prompt structure validation."""
        # Check for obvious prompt injection patterns
        if "ignore" in prompt.lower() and (
            "previous" in prompt.lower() or "system" in prompt.lower()
        ):
            log_warning("Potential prompt injection detected")
            return False

        # Ensure prompt has content
        if not prompt or len(prompt.strip()) == 0:
            return False

        return True

    def _validate_response(self, response, schema) -> bool:
        """Validate response against Pydantic schema or JSON schema."""
        if not response.content:
            return False
            
        if schema is None:
            return True
            
        try:
            import json
            from pydantic import BaseModel
            
            content_str = response.content
            if "```json" in content_str:
                content_str = content_str.split("```json")[1].split("```")[0].strip()
            elif "```" in content_str:
                content_str = content_str.split("```")[1].strip()
                
            data = json.loads(content_str)
            
            if isinstance(schema, type) and issubclass(schema, BaseModel):
                schema(**data)
            elif isinstance(schema, dict):
                from jsonschema import validate
                validate(instance=data, schema=schema)
                
            return True
        except Exception as e:
            return False


class SafeToolCall:
    """
    Wrapper for tool calls with error boundary.

    Usage:
        tool_call = SafeToolCall(tool_func, timeout=30, allowed_tools={"search", "calculator"})
        result = tool_call.execute(input_data)
    """

    def __init__(self, tool_func, timeout=30, require_approval=False, allowed_tools=None):
        self.tool_func = tool_func
        self.timeout = timeout
        self.require_approval = require_approval
        self.TOOL_NAME = getattr(tool_func, "__name__", "unknown")
        # Accept an explicit whitelist; fall back to the registry default set.
        # Callers should pass the set from ToolRegistry.clear_tool_whitelist() so
        # there is a single source of truth for the allowed tool list.
        self._allowed_tools = allowed_tools if allowed_tools is not None else {
            "search", "file_read", "calculator", "fetch_weather"
        }

    def execute(self, input_data) -> dict:
        """
        Execute tool call with error boundary.

        Args:
            input_data: Parameters for the tool

        Returns:
            Dict with execution result and metadata
        """
        try:
            # Check if tool is in whitelist (for tool-boundary pattern)
            if not self._is_allowed_tool():
                return {
                    "error": {
                        "code": "TOOL_NOT_FOUND",
                        "message": "Tool not in allowed list",
                    }
                }

            # Execute with timeout
            result = asyncio.wait_for(self.tool_func(input_data), timeout=self.timeout)

            # Validate output format
            if not self._validate_output(result):
                return {
                    "error": {"code": "FORMAT_ERROR", "message": "Invalid tool output"}
                }

            return {"success": True, "data": result}

        except TimeoutError:
            log_error(f"Timeout on tool call: {self.TOOL_NAME}")
            return {
                "error": {
                    "code": "TIMEOUT",
                    "message": f"Tool {self.TOOL_NAME} timed out",
                }
            }

        except Exception as e:
            log_error(f"Tool execution failed: {type(e).__name__}: {e}")
            return {"error": {"code": "EXECUTION_ERROR", "message": str(e)}}

    def _is_allowed_tool(self) -> bool:
        """Check if tool is in the injected whitelist (single source of truth)."""
        return self.TOOL_NAME in self._allowed_tools

    def _validate_output(self, output) -> bool:
        """Validate tool output format."""
        # Implement schema validation for each tool type
        if not output or (isinstance(output, dict) and len(output) == 0):
            return False
        return True


async def retry_with_backoff(func, max_retries=5, base_delay=1.0, jitter=True):
    """
    Retry a function with exponential backoff and optional jitter.

    Args:
        func: Async function to call
        max_retries: Maximum number of retries (default 5)
        base_delay: Base delay in seconds for exponential calculation
        jitter: Whether to add random jitter to delays

    Returns:
        Result of func or last error if all retries exhausted
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            return await func()
        except (TimeoutError, RateLimitError) as e:
            last_error = e
            delay = base_delay * (2**attempt)  # Exponential backoff

            # Add jitter if enabled
            if jitter:
                delay += random.uniform(0, min(delay * 0.2, 5))

            log_info(f"Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})")
            await asyncio.sleep(delay)

    # All retries exhausted
    raise last_error


# Example usage:
"""
# Usage example in production code:

async def process_user_request(request):
    # Call model safely
    model_result = await safe_call.execute(
        prompt=f"Analyze this data:\n{request.data}",
        schema=analysis_schema
    )

    if not model_result["success"]:
        return error_response(model_result["error"])

    # Process successful result
    analysis = model_result["data"]

    # Call tools safely (if needed)
    weather_data = await safe_weather_tool.execute({
        "location": analysis.get("location", "default")
    })

    return build_final_response(analysis, weather_data)
"""


class RateLimiter:
    """
    Token Bucket Rate Limiter to proactively prevent 429 errors.

    Sized in tokens/minute, not requests/minute: a single large-payload call can
    consume a large share of real provider throughput even though it is only one
    "request", so a request-count bucket reports headroom that doesn't exist. Callers
    report each call's actual or estimated token cost via `acquire(token_cost=...)`;
    the bucket drains in proportion to that cost instead of a fixed 1-unit decrement
    per call regardless of payload size.
    """
    def __init__(self, tokens_per_minute: int = 50_000):
        self.capacity = tokens_per_minute
        self.tokens = tokens_per_minute
        self.refill_rate = tokens_per_minute / 60.0
        self.last_refill = time.monotonic()

    async def acquire(self, token_cost: int = 1) -> None:
        while True:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now

            # A single call costing more than total capacity can never satisfy
            # `tokens >= token_cost` even at a full bucket — treat "bucket is full"
            # as sufficient in that case so an oversized single call isn't blocked
            # forever. It still pays its real cost: tokens go negative and must
            # refill past zero before the next call proceeds.
            threshold = min(token_cost, self.capacity)
            if self.tokens >= threshold:
                self.tokens -= token_cost
                return

            deficit = threshold - self.tokens
            wait_time = deficit / self.refill_rate
            await asyncio.sleep(wait_time)
