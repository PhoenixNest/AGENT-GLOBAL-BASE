# Harness Engineering Documentation Hub

> **Harness Engineering** is the discipline of building robust, scalable, and maintainable Claude API applications using systematic design patterns, error handling, and architectural decisions.

---

## 📚 Documentation Structure

| File/Folder          | Purpose                                               | Target Audience                |
| -------------------- | ----------------------------------------------------- | ------------------------------ |
| `README.md`          | Quick start guide for Harness Engineering             | All developers                 |
| `CONCEPTS.md`        | Core theoretical foundations                          | Architects, Researchers        |
| `quick-reference.md` | Rapid lookup tables and decision matrices             | Senior Developers              |
| `reference-table.md` | Comprehensive tabular references                      | Quality Engineers              |
| `patterns/`          | Reusable implementation patterns and prompt templates | Implementers, Prompt Engineers |
| `testing/`           | Test strategies and edge case coverage guidelines     | QA Engineers                   |
| `examples/`          | Working code examples for common scenarios            | All developers                 |

---

## 🚀 Quick Start (5-Minute Tour)

### Step 1: Understand When to Use Harness Patterns

Use Harness Engineering when building **production-grade LLM applications**:

- ✅ Multi-turn conversational agents
- ✅ Tool-augmented workflows (search, file ops, API calls)
- ✅ Batch processing pipelines
- ✅ High-stakes operations (sending, financial data)
- ✅ Applications requiring deterministic output formats

### Step 2: Apply the Core Patterns

| Pattern                    | When to Use                              | Where to Find It                     |
| -------------------------- | ---------------------------------------- | ------------------------------------ |
| **Error Boundary**         | All tool calls, model responses          | `implementations/error_boundary.py`  |
| **Context Budget Monitor** | Long-running conversations (>10 turns)   | `implementations/context_monitor.py` |
| **Degradation Fallback**   | Multi-tier systems (Tier 1→2→3 fallback) | `examples/fallback-templates.md`     |
| **Tool Boundaries**        | Any agent that uses external tools       | `implementations/tool_registry.py`   |

### Step 3: Key Metrics to Track

| Metric                 | Target | Alert Threshold | Location           |
| ---------------------- | ------ | --------------- | ------------------ |
| First token latency    | < 2s   | > 5s            | Observability      |
| Full response time     | < 10s  | > 30s           | Observability      |
| Error rate             | < 1%   | > 5%            | Metrics dashboard  |
| Context budget usage   | 40-60% | > 80% warning   | `patterns/monitor` |
| Tool call success rate | > 95%  | < 90% per tool  | Per-tool tracking  |

---

## 📖 Documentation Quick Links

### For New Developers

- Start here: [`README.md`](./README.md) — This file
- Read next: [`CONCEPTS.md`](./CONCEPTS.md) — Core concepts
- Keep handy: [`quick-reference.md`](./quick-reference.md) — Lookup tables

### For Implementation

- Browse patterns: `patterns/` folder
- See examples: `examples/` folder
- Check testing guidelines: `testing/` folder

### For Quality Engineers

- Deep reference: [`reference-table.md`](./reference-table.md)
- Edge cases: `testing/edge-cases.md`

---

## 🛠️ Core Patterns Overview

### 1. Error Boundary Pattern

Wraps all LLM calls with tiered recovery paths:

```python
try:
    result = model_call(prompt)
except TimeoutError:
    return fallback_response("timeout", prompt_type)
except ValidationError:
    return regeneration_attempt(result, hint="simplify output")
```

**File:** `patterns/error_boundary.py`

### 2. Context Budget Monitor

Monitors and prunes conversation history to prevent token exhaustion:

```python
if monitor.check_budget(messages):
    proceed_normally()
elif monitor.at_warning_threshold():
    log_warning("Context at 80%, continuing")
else:
    messages = monitor.prune_conversation()
```

**File:** `patterns/context_monitor.py`

### 3. Tool Boundaries Pattern

Defines explicit whitelist and call limits:

```python
AVAILABLE_TOOLS = ["search", "file_read", "calculator"]  # Whitelist
MAX_TOOL_CALLS_PER_TASK = 5                              # Limit
TOOL_TIMEOUT_SECONDS = 30                                # Timeout
```

**File:** `patterns/tool_registry.json`

---

## 📊 Decision Matrix: When to Apply Which Pattern

| Scenario                   | Recommended Pattern(s)             | File Location                           |
| -------------------------- | ---------------------------------- | --------------------------------------- |
| Data extraction task       | Error Boundary + Schema Validation | `implementations/error_boundary.py`     |
| Summarization              | Context Budget Monitor             | `implementations/context_monitor.py`    |
| Tool-augmented agent       | Tool Boundaries + Error Boundary   | `implementations/tool_registry.py`      |
| Long-form creative writing | Degradation Fallback               | `examples/fallback-templates.md`        |
| Batch document analysis    | Caching + Context Pruning          | `testing/edge-cases.md` (batch section) |
| Multi-step reasoning task  | Chain-of-Thought + Error Boundary  | `patterns/prompt-templates.md`          |

---

## 📈 Quick Reference (Rapid Lookups)

### Temperature Selection

| Use Case            | Temperature | Token Budget % | Cacheable? |
| ------------------- | ----------- | -------------- | ---------- |
| Data extraction     | 0.0         | 15%            | Yes        |
| Summarization       | 0.3         | 40%            | Yes        |
| Analysis/reasoning  | 0.5         | 60%            | No         |
| Creative generation | 0.7         | Variable       | No         |

See [`quick-reference.md`](./quick-reference.md) for full tables.

---

## 🔐 Security Checklist (Quick Reference)

Before deploying any harness-engineered application:

- [ ] Prompt injection detection active
- [ ] PII scrubbing on inputs
- [ ] PII scanning on outputs
- [ ] High-risk tools have approval gates
- [ ] Model version pinned in production
- [ ] Sensitive data redacted from logs

---

## 📦 Folder Contents Summary

```
harness-engineering/
├── README.md                           ← You are here
├── CONCEPTS.md                         ← Core theoretical foundations
├── quick-reference.md                  ← Rapid lookup tables and decision matrices
├── implementations/                    ← Runnable implementation code
│   ├── error_boundary.py               ← Error boundary wrappers
│   ├── context_monitor.py              ← Token budget monitoring
│   └── tool_registry.py                ← Tool whitelist + timeouts
├── patterns/                           ← Harness patterns and prompt templates
│   └── prompt-templates.md             ← Prompt templates for each harness pattern
├── testing/                            ← Test strategies & edge cases
│   ├── test_context_monitor.py         ← Executable pytest suite
│   ├── test_error_boundary.py          ← Executable pytest suite
│   ├── edge-cases.md                   ← Edge case coverage guide
│   └── reference-table.md              ← Testing reference
└── examples/                           ← Working code examples
    ├── fallback-templates.md           ← Fallback template guide
    └── weather_app_flow.md             ← End-to-end harness walkthrough
```

---

## 🎯 Next Steps

1. **Read [`CONCEPTS.md`](./CONCEPTS.md)** to understand core Harness concepts
2. **Review [`patterns/`](./patterns/)/** for implementation code
3. **Use [`quick-reference.md`](./quick-reference.md)\*** during development
4. **Follow the security checklist** before any deployment

---

## Related Modules

| Module                                                                                          | Relationship                                                                                                                 |
| ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| [`context-engineering/`](core-component-00/engineering/context-engineering/README.md)                       | Assembles the context window that Harness Engineering executes. Wire `ContextAssembler.build()` → `SafeModelCall.execute()`. |
| [`retrieval-augmented-generation/`](core-component-00/retrieval-augmented-generation/README.md) | Provides retrieved documents that feed into the context window via context-engineering.                                      |
| [`prompt-engineering/`](core-component-00/engineering/prompt-engineering/README.md)                         | Provides patterns for writing content within each context slot.                                                              |

---

## Document Status

| Document           | Version | Last Updated |
| ------------------ | ------- | ------------ |
| README.md          | 1.1     | 2026-04-28   |
| CONCEPTS.md        | 1.1     | 2026-04-28   |
| quick-reference.md | 1.1     | 2026-04-28   |
| error_boundary.py  | 1.1     | 2026-04-28   |
| context_monitor.py | 1.1     | 2026-04-28   |
| tool_registry.py   | 1.1     | 2026-04-28   |

**Maintained by:** Claude Lab Engineering Team
