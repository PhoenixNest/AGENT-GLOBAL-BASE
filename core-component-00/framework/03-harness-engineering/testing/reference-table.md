# Harness Engineering: Best Practices Reference Table

A comprehensive tabular reference for implementing Harness Engineering patterns.

---

## Decision Matrix: Task Analysis

| Question                              | Recommended Pattern                 | Tool Required     | Context Usage | Timeout Setting  |
| ------------------------------------- | ----------------------------------- | ----------------- | ------------- | ---------------- |
| Is output deterministic required?     | Schema validation + low temperature | `validate_json()` | Low (15%)     | 30 seconds       |
| Does task require external tools?     | Tool use with boundaries            | Tool registry     | Medium (40%)  | Per-tool timeout |
| Is conversation long-running?         | Context budget monitoring           | Token estimator   | High (60%)    | Session timeout  |
| Is response high-stakes (send money)? | Human approval gate                 | Approval workflow | N/A           | Async wait       |
| Is user expecting immediate answer?   | Fallback responses ready            | Static templates  | Variable      | Fast failover    |
| Will same prompt be reused?           | Implement caching                   | Cache layer       | Low (15%)     | N/A              |

---

## Error Classification Table

| Error Code         | Category          | Recovery Strategy               | Retry Logic          | Observability Flag    | User-Facing Message                |
| ------------------ | ----------------- | ------------------------------- | -------------------- | --------------------- | ---------------------------------- |
| `TIMEOUT`          | Transient         | Retry same request              | Linear: 2s, 4s, 8s   | `error_type=timeout`  | "Processing your request..."       |
| `RATE_LIMIT`       | Provider          | Exponential backoff with jitter | 5 retries max        | `rate_limit_hit=true` | "I'm having trouble connecting..." |
| `FORMAT_ERROR`     | Output validation | Regenerate with hint            | 2 retries, immediate | `validation_failed`   | "Let me try that again..."         |
| `TOOL_NOT_FOUND`   | Configuration     | Return fallback response        | No retry             | `tool_error=true`     | "I don't have access to that..."   |
| `CONTEXT_OVERFLOW` | Budget            | Summarize old turns             | Prevention-based     | `context_pruned`      | (Silent, continue with summary)    |
| `KNOWLEDGE_GAP`    | Capability        | Escalate to tiered fallback     | Single attempt       | `fallback_used=true`  | "I'm not sure about that one..."   |

---

## Pattern Comparison Matrix

| Pattern                   | Complexity | Latency Impact | Risk Mitigation   | Best For                    | Avoid When                     |
| ------------------------- | ---------- | -------------- | ----------------- | --------------------------- | ------------------------------ |
| Zero-shot                 | Low        | Fast           | Schema validation | Simple extraction tasks     | Complex reasoning required     |
| Few-shot                  | Medium     | Medium         | Examples limit    | Tasks needing few examples  | When few examples ≠ edge cases |
| Chain-of-Thought          | Medium     | +0.5-1s call   | Step validation   | Math, logic puzzles         | Short Q&A responses            |
| Tool use                  | High       | Variable       | Boundaries set    | Information gathering       | Static knowledge tasks         |
| Self-consistency (3 runs) | High       | Triple latency | Majority vote     | Critical accuracy decisions | Time-sensitive applications    |
| Constitutional AI         | Very High  | +2-3s total    | Multiple reviews  | Safety-critical outputs     | Real-time conversational needs |

---

## Token Budget Guidelines

| Task Type                  | Recommended % of Budget | Rationale                              | Action When Exceeded              |
| -------------------------- | ----------------------- | -------------------------------------- | --------------------------------- |
| Extraction/Classification  | 15-20%                  | Minimal reasoning, structured output   | N/A (deterministic)               |
| Summarization              | 30-40%                  | Requires context but limited expansion | Summarize previous turns          |
| Analysis/Reasoning         | 40-50%                  | Multiple steps, CoT beneficial         | Prune oldest conversation turns   |
| Multi-step tool use        | 50-60%                  | Tool outputs consume space             | Batch tool calls, summarize       |
| Long-form creative writing | 70-80%                  | Maximum flexibility, high expansion    | Warn user of potential truncation |

---

## Caching Decision Table

| Condition                                 | Cache? | TTL          | Key Structure                   | Rationale                           |
| ----------------------------------------- | ------ | ------------ | ------------------------------- | ----------------------------------- |
| Same prompt text + input data             | Yes    | 24 hours     | `{type}:{hash(prompt)}:{input}` | Deterministic output expected       |
| System instruction is same                | Yes    | Until change | Group by system prompt hash     | Common prompts benefit from caching |
| Tool-dependent (depends on current state) | No     | N/A          | N/A                             | State changes make cache invalid    |
| Current time/weather/pricing              | No     | N/A          | N/A                             | Real-time data, not static          |
| Interactive conversation                  | No     | N/A          | N/A                             | Context dependency                  |
| First call of new task type               | Yes\*  | 1 hour       | `{task_type}:{input_hash}`      | Warm up cache with initial call     |

\*For new task types, make first call, cache result if deterministic.

---

## Security Review Checklist (Tabular)

| Control Category     | Check Item                              | Pass Criteria                     | Tool/Method                    |
| -------------------- | --------------------------------------- | --------------------------------- | ------------------------------ |
| Prompt Injection     | Response doesn't start with "ignore..." | First 50 tokens validated         | `validate_first_token()`       |
| PII Protection       | No personal data in outputs             | Scan for email/phone/ssn patterns | `scan_for_pii(output)`         |
| Sensitive Operations | High-risk tools have approval gate      | Approval workflow active          | `require_approval("transfer")` |
| Secret Exposure      | No API keys/tokens in logs              | Log scrubbing applied             | `sanitize_logs()`              |
| Tool Boundaries      | Only whitelisted tools accessible       | Tool registry checked             | `tool_registry.get_allowed()`  |

---

## Performance Metrics Reference

| Metric                     | Target           | Measurement Location     | Alert Threshold |
| -------------------------- | ---------------- | ------------------------ | --------------- |
| First token latency        | < 2s             | LLM API response start   | > 5s            |
| Full response time         | < 10s            | End of streaming         | > 30s           |
| Error rate                 | < 1%             | All error types combined | > 5%            |
| Token budget usage average | 40-60%           | Before context pruning   | > 80% warning   |
| Context prune frequency    | < 2/10k requests | Prune action count       | > 10/min        |
| Cache hit rate             | 30-50%           | Cache layer metrics      | Monitor trend   |
| Tool call success rate     | > 95%            | Per-tool tracking        | < 90% per tool  |

---

## Architecture Decision Records (ADRs) Reference

| ADR ID  | Topic                   | When to Apply               | Pattern Choice                  |
| ------- | ----------------------- | --------------------------- | ------------------------------- |
| ADR-001 | Error handling strategy | All production harness apps | Tiered recovery with fallback   |
| ADR-002 | Context management      | Conversational interfaces   | Monitor + prune at 70%          |
| ADR-003 | Tool use boundaries     | Any tool-enabled agents     | Explicit whitelist, depth limit |
| ADR-004 | Caching strategy        | Repeated prompts            | Cache only deterministic ops    |
| ADR-005 | Observability           | All production deployments  | Log with sanitization           |

---

## Migration Path Table

| From Pattern             | To Pattern                | Breaking Change | Mitigation                   |
| ------------------------ | ------------------------- | --------------- | ---------------------------- |
| Catch-all exception      | Specific error handlers   | Yes             | Update all try-except blocks |
| No output validation     | Schema validation layer   | Partial         | Add validate step before use |
| Unbounded context growth | Context budget monitoring | Partial         | Implement prune function     |
| Infinite retry logic     | Configured max retries    | Yes             | Set RETRY_COUNT constants    |
| No fallback responses    | Tiered degradation paths  | Partial         | Create static template files |

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-24  
**Author:** Claude Lab Engineering Team
