# Harness Engineering Quick Reference

## Rapid Decision Tables

### Temperature Selection Table

| Use Case                 | Temperature | Token Budget % | Retry Strategy    | Cacheable?  |
| ------------------------ | ----------- | -------------- | ----------------- | ----------- |
| Data extraction/ parsing | 0.0         | Low (15%)      | Format validation | Yes, always |
| Summarization            | 0.3         | Medium (40%)   | Schema retry      | Yes         |
| Analysis/thinking        | 0.5         | High (60%)     | Tiered fallback   | No          |
| Creative generation      | 0.7         | Variable       | Manual review     | No          |
| Exploration/ideation     | 0.9+        | Max budget     | User selection    | No          |

### Error Handling Matrix

| Error Type       | Recovery Action                | Retry Count | Backoff Strategy        |
| ---------------- | ------------------------------ | ----------- | ----------------------- |
| Timeout          | Retry same request             | 3           | Linear: 2s, 4s, 8s      |
| Rate limit (429) | Retry with exponential backoff | 5           | Exponential + jitter    |
| Format error     | Regenerate with schema hint    | 2           | Immediate               |
| Tool not found   | Return fallback response       | 1           | None                    |
| Invalid output   | Resubmit with better prompt    | 2           | Immediate               |
| Context exceeded | Summarize history              | 1           | None (prevention-based) |

### Context Budget Thresholds

| Current Usage | Action                       | Message to Model                  |
| ------------- | ---------------------------- | --------------------------------- |
| < 60%         | Proceed normally             | —                                 |
| 60-80%        | Warn in logs                 | "Continuing with current context" |
| > 80%         | Prune old conversation turns | "Summarizing previous discussion" |
| > 95%         | Emergency prune              | Critical summary only             |

### Tool Use Safety Checklist

Before allowing an agent to use tools:

- [ ] Tool list is explicitly defined and limited
- [ ] Maximum tool call depth is set (≤ 5)
- [ ] Each tool has timeout configured
- [ ] Input validation exists for each tool
- [ ] Output format is validated after call
- [ ] High-risk tools have human approval gate

---

## Common Anti-Patterns to Avoid

| ❌ Don't                        | ✅ Do Instead                           |
| ------------------------------- | --------------------------------------- |
| Assume model will be consistent | Validate output against schema          |
| Let context grow unbounded      | Monitor and prune at 70-80%             |
| Catch-all exception handlers    | Specific handlers for each error type   |
| Infinite retry loops            | Maximum retry count with backoff        |
| No fallback responses           | Tiered degradation paths                |
| Logging full model internals    | Log sanitized inputs/outputs only       |
| Caching tool-dependent results  | Cache only deterministic operations     |
| Unbounded thinking loops        | Add turn counter and hard exit criteria |

---

## Essential Patterns

### 1. Prompt Sandwich Pattern

```
<system>
You are an expert {role}. Follow these guidelines:
</system>

<user>
Given this context: {context}
Task: {task}
</user>

<tool>
Available tools: [list]
Tool descriptions: [descriptions]
</tool>
```

### 2. Error Boundary Wrapper Pattern

```python
class SafeToolCall:
    def execute(self, tool, input_data):
        try:
            return tool.execute(timeout=30)
        except TimeoutError:
            log_error("Timeout on {tool}", tool=tool)
            return self.fallback_response(tool.name)
        except ValidationError as e:
            log_error("Validation failed", error=e)
            return self.regenerate_with_hint(input_data)
```

### 3. Context Budget Monitor Pattern

```python
class ContextMonitor:
    def __init__(self, max_tokens=128000, warn_at_0.75=True):
        self.max_tokens = max_tokens
        self.warn_at = max_tokens * 0.75

    def check_budget(self, messages):
        usage = estimate_token_count(messages)
        ratio = usage / self.max_tokens

        if ratio > 0.95:
            self.prune_conversation()
            return True  # Pruned
        elif ratio > 0.80:
            log_warning("Context at {ratio:.1%}", ratio=ratio)
            return True  # Warning issued
        else:
            return False  # OK
```

---

## Checklist: Pre-Deployment Review

### Architecture Review

- [ ] All tool calls have timeouts defined
- [ ] Error recovery paths implemented for each error type
- [ ] Token budget monitoring in place with alerts
- [ ] Output validation before downstream processing
- [ ] Rate limiting and exponential backoff configured

### Security Review

- [ ] PII scrubbing on inputs before model call
- [ ] PII scanning on outputs before returning to user
- [ ] Prompt injection detection patterns active
- [ ] Sensitive tools require explicit approval
- [ ] Model version is pinned in production config

### Observability Review

- [ ] Full prompts logged with PII removed
- [ ] Tool call results logged for traceability
- [ ] Error rates tracked per tool and prompt type
- [ ] Token usage metrics collected
- [ ] User feedback (thumbs up/down) captured

### Performance Review

- [ ] Caching implemented for deterministic operations
- [ ] Context pruning configured at 70% threshold
- [ ] Latency SLOs defined and monitored
- [ ] Parallel execution used where safe

---

## Quick Reference Commands

| Task                     | Command/Approach                            |
| ------------------------ | ------------------------------------------- |
| Check token budget       | `usage = estimate_token_count(messages)`    |
| Prune context            | `prune_conversation(conversation[:target])` |
| Validate JSON output     | `validate_json(output, schema)`             |
| Retry with backoff       | `retry_with_backoff(func, max_retries=5)`   |
| Cache deterministic call | `cache.get_or_compute(key, compute_fn)`     |

---

**Last Updated:** 2026-04-24  
**Version:** 1.0
