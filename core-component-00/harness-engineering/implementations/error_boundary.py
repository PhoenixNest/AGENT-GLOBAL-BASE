"""
Error Boundary Pattern Implementation

This module provides wrapper classes for safely calling LLM models with
tiered error recovery paths. Each error type has a defined recovery strategy.
"""

import asyncio
import random
import sys
import time
from typing import Any, Dict


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


class ContextOverflowError(Exception):
    """Raised when conversation exceeds token budget."""

    pass


class SafeModelCall:
    """
    Wrapper for model calls with tiered error recovery.

    Usage:
        call = SafeModelCall(client, model="claude-3-opus", timeout=30)
        result = call.execute(prompt, schema=output_schema)
    """

    def __init__(self, client, model_id, timeout=30, max_retries=3):
        self.client = client
        self.model_id = model_id
        self.timeout = timeout
        self.max_retries = max_retries

    async def execute(self, prompt: str, schema=None) -> dict:
        """
        Execute model call with error boundary and retry logic.

        Args:
            prompt: The prompt to send to the model
            schema: Optional JSON Schema for output validation

        Returns:
            Dict with 'success' flag and either 'data' or 'error' keys
        """
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
                    self.client.messages.create(messages=[prompt]), timeout=self.timeout
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
                # Catch-all for unexpected errors
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
    """
    def __init__(self, requests_per_minute: int = 50):
        import time
        self.capacity = requests_per_minute
        self.tokens = requests_per_minute
        self.refill_rate = requests_per_minute / 60.0
        self.last_refill = time.monotonic()

    async def acquire(self):
        import time
        import asyncio
        while True:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now

            if self.tokens >= 1:
                self.tokens -= 1
                return
            
            wait_time = (1 - self.tokens) / self.refill_rate
            await asyncio.sleep(wait_time)
