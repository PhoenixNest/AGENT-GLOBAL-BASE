# Harness Engineering Quick Reference

## Core Patterns Decision Matrix

| Scenario                    | Recommended Pattern(s)             | Implementation File                     | Key Metrics                          |
| --------------------------- | ---------------------------------- | --------------------------------------- | ------------------------------------ |
| **Data extraction**         | Error Boundary + Schema Validation | `implementations/error_boundary.py`     | Accuracy >95%, Cacheable (T=0.0-0.2) |
| **Summarization**           | Context Budget Monitor             | `implementations/context_monitor.py`    | Latency <10s, Token use 40-60%       |
| **Tool-augmented agent**    | Tool Boundaries + Error Boundary   | `implementations/tool_registry.py`      | Success rate >95%, Timeout <30s      |
| **Long-form creative**      | Degradation Fallback               | `examples/fallback_templates.md`        | Quality gate pass >80%               |
| **Batch document analysis** | Caching + Context Pruning          | `testing/edge_cases.md` (batch section) | Throughput >10 docs/min              |
| **Multi-step reasoning**    | Chain-of-Thought + Error Boundary  | `prompts/reasoning_sandwich.md`         | Accuracy +20% over zero-shot         |

---

## Temperature Selection Matrix

| Use Case            | Temperature | Expected Variance | Cacheable? | Token Budget % | Context Allocation Target |
| ------------------- | ----------- | ----------------- | ---------- | -------------- | ------------------------- |
| Data extraction     | 0.0 - 0.2   | Fixed             | Yes        | 15%            | System ≤15%, History ≤60% |
| Summarization       | 0.3         | Low               | Yes        | 40%            | Tools ≤30%                |
| Analysis/reasoning  | 0.5         | Medium            | No         | 60%            | Keep at 70-80% usage      |
| Creative generation | 0.7 - 0.8   | High              | No         | Variable       | Warn at 75%, Prune at 80% |
| Exploration         | 0.9+        | Very High         | No         | Very High      | Manual review             |

---

## The Four Pillars of Harness Engineering

| Pillar                         | What It Addresses                | Key Principle                                   | Implementation Pattern |
| ------------------------------ | -------------------------------- | ----------------------------------------------- | ---------------------- |
| **Determinism vs. Creativity** | Matching output variance to task | "Higher temperature ≠ smarter model"            | Temperature selection  |
| **Context Window Management**  | Preventing token exhaustion      | "Monitor at 70-80%, prune proactively"          | Context Budget Monitor |
| **Error Handling**             | Recovering from non-determinism  | "Each error type needs a defined recovery path" | Error Boundary         |
| **Tool Use Boundaries**        | Mitigating tool-call risks       | "Explicit whitelist + call limits + timeouts"   | Tool Registry          |

---

## Harness Engineering Flow (8 Phases)

```
┌──────────────────────────────────────────────────────────┐
│                    INPUT PHASE                            │
│ ───────────────────────────────────────────────────────── │
│ 1. Parse user intent                                      │
│ 2. Classify task type (factual/creative/tool-use)         │
│ 3. Check context budget                                    │
│ 4. Select temperature based on task                       │
└──────────────────────────────────────────────────────────┘
                        ↓ CHECK: Context at target range?
┌──────────────────────────────────────────────────────────┐
│                   MODEL PHASE                             │
│ ───────────────────────────────────────────────────────── │
│ 5. Build structured prompt (sandwich pattern)             │
│ 6. Call model with timeout                                │
│ 7. Stream or wait for full response                       │
└──────────────────────────────────────────────────────────┘
                        ↓ CHECK: Response received in time?
┌──────────────────────────────────────────────────────────┐
│                   VALIDATION PHASE                        │
│ ───────────────────────────────────────────────────────── │
│ 8. Validate output format against schema                  │
│ 9. Sanitize PII from response                              │
│ 10. Check for prompt injection patterns                   │
└──────────────────────────────────────────────────────────┘
                        ↓ CHECK: Validation passed?
┌──────────────────────────────────────────────────────────┐
│                PROCESSING PHASE                           │
│ ───────────────────────────────────────────────────────── │
│ 11. Process validated output                               │
│ 12. Execute downstream operations                          │
│ 13. Log to observability system                            │
└──────────────────────────────────────────────────────────┘
                        ↓ CHECK: Downstream success?
┌──────────────────────────────────────────────────────────┐
│                 OUTPUT PHASE                              │
│ ───────────────────────────────────────────────────────── │
│ 14. Format for user                                        │
│ 15. Add human-readable error messages (if any)             │
│ 16. Send response                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Common Patterns Explained

### Error Boundary Pattern

**Purpose:** Wraps all LLM calls with tiered recovery paths.

```python
try:
    result = model_call(prompt)
except TimeoutError:
    return fallback_response("timeout", prompt_type)
except ValidationError:
    return regeneration_attempt(result, hint="simplify output")
except RateLimitError:
    raise  # Let caller handle retry
```

**Key Principle:** Each error type has a defined recovery path; no catch-all exceptions.

---

### Context Budget Monitor Pattern

**Purpose:** Prevents conversation history from consuming the entire token budget.

```python
if ratio > self.prune_threshold:
    log_warning("At prune threshold", ratio=ratio * 100, "%")
    return self._prune_conversation()
elif ratio > self.warn_threshold:
    log_info("Context approaching budget", ratio=ratio * 100, "%")
    return messages  # Continue normally
```

**Key Principle:** Proactive pruning prevents hard failures from token limits.

---

### Degradation Fallback Pattern

**Purpose:** Designs graceful fallbacks when primary approach fails.

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
- Tier 3: Return static "Unable to send email" message

---

## Security Checklist (Before Deployment)

| Category             | Check Item                          | Target Threshold |
| -------------------- | ----------------------------------- | ---------------- |
| **Prompt Injection** | System prompt leakage detection     | 100% active      |
|                      | Directive override blocking         | 100% active      |
|                      | Data exfiltration monitoring        | Blocked          |
| **PII Handling**     | Input sanitization (redaction)      | All inputs       |
|                      | Output filtering (exposure scan)    | All outputs      |
|                      | Logging compliance (same redaction) | All logs         |
| **High-Risk Ops**    | Financial transactions approval     | Human-in-loop    |
|                      | Email sending approval              | Human-in-loop    |
|                      | File deletion/modification gates    | Human-in-loop    |
|                      | Network mutation (POST/PUT/DELETE)  | Human-in-loop    |

---

## Performance Optimization Checklist

| Technique                | Expected Savings  | Implementation Effort | When to Apply                  |
| ------------------------ | ----------------- | --------------------- | ------------------------------ |
| Remove redundant phrases | 5-15%             | Low                   | All prompts                    |
| Summarize context        | 20-40%            | Medium                | Long conversations (>10 turns) |
| Parallel tool execution  | Latency reduction | High                  | Independent queries            |
| Caching (deterministic)  | Up to 90%         | Low                   | T=0.0 tasks only               |

---

## Testing Strategy Matrix

| Test Type          | Deterministic Input  | Expected Output Validation | Edge Cases Covered             |
| ------------------ | -------------------- | -------------------------- | ------------------------------ |
| Schema validation  | Fixed prompts        | JSON schema match          | Missing fields, type errors    |
| Content validation | Standard queries     | Ground truth comparison    | Ambiguous inputs, negations    |
| Latency tests      | Varying context size | P95/P99 thresholds         | Context overflow scenarios     |
| Error injection    | Network failures     | Fallback path activation   | Timeout, rate limit, malformed |
| Security tests     | Attack patterns      | Injection detection        | Prompt injection, PII probes   |

---

## Production Readiness Checklist

| Category          | Check Item                          | ☐ Not Done | ☐ Done |
| ----------------- | ----------------------------------- | ---------- | ------ |
| **Architecture**  | All tool calls have timeouts        |            |        |
|                   | Error recovery paths implemented    |            |        |
|                   | Token budget monitoring in place    |            |        |
|                   | Output validation before processing |            |        |
| **Security**      | PII scrubbing on inputs             |            |        |
|                   | PII scanning on outputs             |            |        |
|                   | Prompt injection detection active   |            |        |
| **Observability** | Full prompts logged (PII removed)   |            |        |
|                   | Error rates tracked                 |            |        |
|                   | User feedback mechanisms exist      |            |        |
| **Performance**   | Caching for deterministic ops       |            |        |
|                   | Context pruning at 70% threshold    |            |        |

---

## References

- [CONCEPTS.md](./CONCEPTS.md) — Core theoretical foundations
- [README.md](./README.md) — Overview and quick start guide
- [Prompt Engineering Research](../../prompt-engineering/fundamentals/research.md) — Taxonomy of techniques

**Version:** 2.0  
**Last Updated:** 2026-04-25  
**Maintained by:** Claude Lab Engineering Team
