# Harness Engineering: Core Concepts and Foundations

## 1. What is Harness Engineering?

### Definition

**Harness Engineering** is the discipline of building production-grade LLM-powered applications that handle non-deterministic outputs safely, maintain context budgets responsibly, orchestrate tool use reliably, and implement systematic error recovery.

### The Harness Paradigm

```
User Intent → [Harness Layer] → Model Computation → Output Processing → Final Response
            └─> Context Management ─┘
            └─> Tool Orchestration ─┘
            └─> Error Handling      ┘
```

### How Harness Engineering Differs from Traditional Software Engineering

| Aspect             | Traditional SE            | Harness Engineering                 |
| ------------------ | ------------------------- | ----------------------------------- |
| **Outputs**        | Deterministic             | Stochastic (non-deterministic)      |
| **Error Handling** | Exceptions are bugs       | Errors are expected, need recovery  |
| **Context Window** | Memory allocation         | Token budget management             |
| **Tool Use**       | Synchronous API calls     | Asynchronous, rate-limited, bounded |
| **Testing**        | Unit tests are sufficient | Need deterministic test cases       |

---

## 2. The Four Pillars of Harness Engineering

### 2.1 Determinism vs. Creativity Trade-off

LLMs exist on a spectrum between deterministic and creative output. Harness Engineering matches temperature settings to task requirements:

| Task Type              | Temperature | Expected Variance | Strategy                       |
| ---------------------- | ----------- | ----------------- | ------------------------------ |
| **Data extraction**    | 0.0 - 0.2   | Fixed             | Validate against schema; cache |
| **Summarization**      | 0.3         | Low               | Schema validation + retry      |
| **Analysis/reasoning** | 0.5         | Medium            | Tiered fallback responses      |
| **Creative writing**   | 0.7 - 0.8   | High              | Manual review, no caching      |
| **Exploration**        | 0.9+        | Very High         | User selection from options    |

**Key Insight:** Higher temperature does NOT equal "smarter model." It equals more variance. Match the setting to your task requirements.

### 2.2 Context Window Management

The context window is finite and precious. Unbounded growth leads to:

1. Quality degradation (critical information pushed out)
2. Increased latency (longer decode times)
3. Token limit violations (hard failures)

**Best Practice:** Monitor at 70-80% usage; prune conversation history systematically.

```
┌─────────────────────────────────────┐
│ Context Budget Allocation            │
├─────────────────────────────────────┤
│ System instructions      ≤ 15%      │
│ User queries             Variable   │
│ Conversation history     ≤ 60%      │
│ Tool responses           ≤ 30%      │
└─────────────────────────────────────┘
```

### 2.3 Error Handling Non-Determinism

LLMs produce different errors on different runs. Harness Engineering requires:

1. **Validation layer** — Verify outputs match expected schema before use
2. **Retry with degradation** — Fallback strategies for failed calls
3. **Observability** — Track failure rates and patterns
4. **User-facing abstraction** — Hide model failures from end users

### 2.4 Tool Use Boundaries

When building tool-enabled agents:

| Pattern                  | Risk Level | Mitigation                              |
| ------------------------ | ---------- | --------------------------------------- |
| Direct tool execution    | Medium     | Add input validation, timeouts          |
| Open-ended tool search   | High       | Constrain available tools explicitly    |
| Recursive self-planning  | Very High  | Implement depth limit (≤5 calls)        |
| Unbounded thinking loops | Critical   | Add turn counter and hard exit criteria |

---

## 3. The Harness Engineering Flow

```
┌──────────────────────────────────────────────────────────┐
│                    INPUT PHASE                            │
│ ───────────────────────────────────────────────────────── │
│ 1. Parse user intent                                      │
│ 2. Classify task type (factual/creative/tool-use)         │
│ 3. Check context budget                                    │
│ 4. Select temperature based on task                       │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│                   MODEL PHASE                             │
│ ───────────────────────────────────────────────────────── │
│ 5. Build structured prompt (sandwich pattern)             │
│ 6. Call model with timeout                                │
│ 7. Stream or wait for full response                       │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│                   VALIDATION PHASE                        │
│ ───────────────────────────────────────────────────────── │
│ 8. Validate output format against schema                  │
│ 9. Sanitize PII from response                              │
│ 10. Check for prompt injection patterns                   │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│                PROCESSING PHASE                           │
│ ───────────────────────────────────────────────────────── │
│ 11. Process validated output                               │
│ 12. Execute downstream operations                          │
│ 13. Log to observability system                            │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│                 OUTPUT PHASE                              │
│ ───────────────────────────────────────────────────────── │
│ 14. Format for user                                        │
│ 15. Add human-readable error messages (if any)             │
│ 16. Send response                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Common Patterns Explained

### 4.1 Error Boundary Pattern

The **Error Boundary Pattern** wraps all LLM calls with specific error handling for each failure mode:

```python
class SafeModelCall:
    async def execute(self, prompt, schema=None):
        try:
            if not self._validate_prompt(prompt):
                raise ValidationError("Invalid prompt structure")

            response = await self._call_model(prompt)
            return self._validate_response(response, schema)

        except TimeoutError:
            log_error("Timeout on model call", duration=self.call_duration)
            return {"error": "TIMEOUT", "message": "Request timed out"}

        except RateLimitError:
            log_error("Rate limit hit", provider=self.provider)
            raise  # Let caller handle retry

        except ValidationError as e:
            log_error("Validation failed", error=e.message)
            return {"error": "FORMAT_ERROR", "message": "Response doesn't match expected format"}
```

**Key Principle:** Each error type has a defined recovery path; no catch-all exceptions.

### 4.2 Context Budget Monitor Pattern

The **Context Budget Monitor Pattern** prevents conversation history from consuming the entire token budget:

```python
class ContextMonitor:
    def __init__(self, max_tokens=128000, warn_at=0.75, prune_at=0.80):
        self.max_tokens = max_tokens
        self.warn_threshold = max_tokens * warn_at
        self.prune_threshold = max_tokens * prune_at

    def check_budget(self, messages):
        current_usage = estimate_token_count(messages)
        ratio = current_usage / self.max_tokens

        if ratio > 1.0:
            log_error("Context overflow!", usage=current_usage)
            raise ContextOverflowError()

        if ratio > self.prune_threshold:
            log_warning("At prune threshold", ratio=ratio * 100, "%")
            return self._prune_conversation()

        elif ratio > self.warn_threshold:
            log_info("Context approaching budget", ratio=ratio * 100, "%")
            return messages  # Continue normally

        return messages

    def _prune_conversation(self):
        """Summarize or remove oldest turns"""
        if len(self.history) < 3:
            return self.history  # Don't prune recent history

        summary_turn = create_summary([self.history[0], self.history[-1]])
        return [summary_turn, *self.history[-2:]]
```

**Key Principle:** Proactive pruning prevents hard failures from token limits.

### 4.3 Degradation Fallback Pattern

The **Degradation Fallback Pattern** designs graceful fallbacks when primary approach fails:

```
Tier 1 (Best): Full model reasoning with tool use
   ↓ (if unavailable)
Tier 2: Simplified prompt without tools, fixed schema
   ↓ (if still failing)
Tier 3: Static template response with placeholder data
```

**Example:** Sending emails via LLM

- Tier 1: Model composes personalized email
- Tier 2: Model uses template with placeholders
- Tier 3: Return static "Unable to send email, please try again" message

---

## 5. Security Considerations

### 5.1 Prompt Injection Defense

| Attack Vector         | Detection Method                    | Mitigation                           |
| --------------------- | ----------------------------------- | ------------------------------------ |
| System prompt leakage | Check response for `system:` prefix | Validate first token matches pattern |
| Directive override    | Scan for "ignore previous" patterns | Enforce strict output schemas        |
| Data exfiltration     | Monitor for external URLs/emails    | Block in output filter               |

### 5.2 PII Handling

- **Input sanitization:** Redact before sending to model
- **Output filtering:** Scan responses for sensitive data exposure
- **Logging compliance:** Apply same redaction as input processing

### 5.3 High-Risk Operations

Require explicit human approval for:

- Financial transactions
- Email sending
- File deletion/modification
- Network requests (POST/PUT/DELETE)

---

## 6. Performance Optimization

### 6.1 Token Efficiency

| Technique                | Savings | Implementation Effort |
| ------------------------ | ------- | --------------------- |
| Remove redundant phrases | 5-15%   | Low                   |
| Summarize context        | 20-40%  | Medium                |
| Parallel tool execution  | N/A     | High                  |

### 6.2 Latency Reduction

Batch independent queries together:

```python
# Bad: Sequential calls
result1 = await fetch_weather(city_a)
result2 = await fetch_weather(city_b)
result3 = await fetch_forecast(city_c)

# Good: Parallel execution
results = asyncio.gather(
    fetch_weather(city_a),
    fetch_weather(city_b),
    fetch_forecast(city_c)
)
```

---

## 7. Testing Strategy

### 7.1 Deterministic Test Cases

Create tests that always produce same input/output for harness reliability:

```python
def test_extraction():
    prompt = "Extract named entities from this text:"
    response = model.generate(prompt + sample_text)

    # Validate schema
    assert validate_schema(response, extraction_schema)

    # Validate content
    assert "entity" in response
    assert len(response["entity"]) > 0

def test_summarization():
    prompt = "Summarize this document:"
    response = model.generate(prompt + long_text)

    # Check length constraint
    assert len(response["summary"]) <= 500
```

### 7.2 Edge Case Coverage

Test boundaries for:

- Empty/null inputs
- Extremely long contexts (90%+ token usage)
- Missing tools in registry
- Network failures (timeout, rate limit)
- Schema violations

---

## 8. Production Checklist Summary

Before deploying a harness-engineered application:

| Category          | Check Item                          | Status |
| ----------------- | ----------------------------------- | ------ |
| **Architecture**  | All tool calls have timeouts        | ☐      |
|                   | Error recovery paths implemented    | ☐      |
|                   | Token budget monitoring in place    | ☐      |
|                   | Output validation before processing | ☐      |
| **Security**      | PII scrubbing on inputs             | ☐      |
|                   | PII scanning on outputs             | ☐      |
|                   | Prompt injection detection active   | ☐      |
| **Observability** | Full prompts logged (PII removed)   | ☐      |
|                   | Error rates tracked                 | ☐      |
|                   | User feedback mechanisms exist      | ☐      |
| **Performance**   | Caching for deterministic ops       | ☐      |
|                   | Context pruning at 70% threshold    | ☐      |

---

## 9. References

- [Prompt Engineering Reference](../../prompt-engineering/fundamentals/research.md)
- [Context Engineering — Context Window Anatomy](../../context-engineering/fundamentals/context-window-anatomy.md)
- [Context Engineering — Assembly Patterns](../../context-engineering/patterns/assembly-patterns.md)
- [Context Engineering — Integration Guide](../../context-engineering/workspace/integration-guide.md)
- [Claude API Documentation](https://docs.anthropic.com)
- [LLM Application Patterns](https://github.com/anthropics/clockwork-copilot)

---

**Version:** 1.0  
**Last Updated:** 2026-04-24  
**Maintained by:** Claude Lab Engineering Team
