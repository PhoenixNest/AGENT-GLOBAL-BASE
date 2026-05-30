---
paths:
  - "**/harness-engineering/**"
  - "**/*harness*.py"
description: Harness Engineering (Layer 3) patterns and behavior rules
---

# Harness Engineering — Layer 3

**Scope:** Error boundaries, context budget monitoring, tool use boundaries, safe model execution

---

## Three Harness Components

| Component                  | Purpose                                                | Implementation       |
| -------------------------- | ------------------------------------------------------ | -------------------- |
| **Error Boundary**         | Timeout, rate-limit, validation recovery               | `error_boundary.py`  |
| **Context Budget Monitor** | Token budget enforcement                               | `context_monitor.py` |
| **Tool Registry**          | Tool whitelists, call limits, dangerous task detection | `tool_registry.py`   |

---

## Error Recovery Strategies

| Failure Mode         | Recovery                                              |
| -------------------- | ----------------------------------------------------- |
| **Timeout**          | Retry with exponential backoff (max 3 attempts)       |
| **Rate Limit**       | Wait and retry with jitter                            |
| **Validation Error** | Reject invalid input, log error, return safe fallback |

---

## Context Budget Monitoring

| Check             | Action                                                |
| ----------------- | ----------------------------------------------------- |
| Pre-call          | Verify context window fits within model's token limit |
| During session    | Track cumulative token usage                          |
| Approaching limit | Trigger `context_compressor.py`                       |
| Limit exceeded    | Reject call, log warning, suggest compression         |

---

## Tool Use Boundaries

- **Whitelist:** Only approved tools can be called
- **Call Limits:** Max calls per tool per session
- **Dangerous Tasks:** Detect and block destructive operations
- **Parameter Validation:** Validate tool parameters before execution

---

## Behavior Rules

1. All model calls go through the harness — never bypass error boundaries
2. Handle all three failure modes (timeout, rate-limit, validation)
3. Enforce token budgets with `context_monitor.py`
4. Only whitelist-approved tools may be called
5. Log all errors for post-incident analysis
6. Test error recovery paths
