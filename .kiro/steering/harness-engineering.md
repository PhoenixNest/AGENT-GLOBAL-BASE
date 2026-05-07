---
inclusion: fileMatch
fileMatchPattern: "**/harness-engineering/**,**/*harness*.py"
description: Harness Engineering (Layer 3) patterns and implementations
version: "1.0.0"
---

# Harness Engineering — Layer 3

**Steering File:** Harness Engineering (CC-00 Layer 3)  
**Inclusion:** Conditional — Activated when working in `harness-engineering/` or harness-related Python files  
**Authority:** CC-00 Laboratory — Layer 3: How to execute safely

---

## Module Identity

**Harness Engineering** is Layer 3 of the CC-00 engineering stack — the discipline of safely executing LLM model calls at runtime.

| Field          | Detail                                                                                    |
| -------------- | ----------------------------------------------------------------------------------------- |
| **Layer**      | 3 — How to execute safely                                                                 |
| **Type**       | Production framework                                                                      |
| **Scope**      | Error boundaries, context budget monitoring, tool use boundaries, safe model execution    |
| **Output**     | Error recovery patterns, monitoring implementations, tool registries                      |
| **Has Code**   | Yes — 3 Python implementations                                                            |
| **Upstream**   | Consumes assembled context windows from `context-engineering/`                            |
| **Downstream** | Feeds agent-generated artifacts back to `retrieval-augmented-generation/` (feedback loop) |

---

## Core Concepts

### The Harness is the Last Layer Before the Model Call

```
Flow: Context Engineering → Harness Engineering → LLM Model Call
                                    ↓
                            Validate · Monitor · Recover
```

The harness validates inputs, monitors execution, and recovers from errors. It is the reliability layer that wraps every model call.

### Three Harness Components

| Component                  | Purpose                                                | Implementation       |
| -------------------------- | ------------------------------------------------------ | -------------------- |
| **Error Boundary**         | Timeout, rate-limit, validation recovery               | `error_boundary.py`  |
| **Context Budget Monitor** | Token budget enforcement                               | `context_monitor.py` |
| **Tool Registry**          | Tool whitelists, call limits, dangerous task detection | `tool_registry.py`   |

---

## Key Production Implementations

All paths relative to `core-component-00/harness-engineering/implementations/`:

| File                 | Purpose                                                 | Test Suite                           |
| -------------------- | ------------------------------------------------------- | ------------------------------------ |
| `error_boundary.py`  | Timeout, rate-limit, and validation recovery            | `../testing/test_error_boundary.py`  |
| `context_monitor.py` | Token budget enforcement and context window size checks | `../testing/test_context_monitor.py` |
| `tool_registry.py`   | Tool whitelists, call limits, dangerous task detection  | —                                    |

---

## Error Boundary Patterns

The error boundary handles three failure modes:

| Failure Mode         | Recovery Strategy                                     |
| -------------------- | ----------------------------------------------------- |
| **Timeout**          | Retry with exponential backoff (max 3 attempts)       |
| **Rate Limit**       | Wait and retry with jitter                            |
| **Validation Error** | Reject invalid input, log error, return safe fallback |

See `patterns/error-recovery.md` for full recovery strategies.

---

## Context Budget Monitoring

The context monitor enforces token limits:

| Check                 | Action                                                    |
| --------------------- | --------------------------------------------------------- |
| **Pre-call**          | Verify context window fits within model's token limit     |
| **During session**    | Track cumulative token usage                              |
| **Approaching limit** | Trigger context compression (via `context_compressor.py`) |
| **Limit exceeded**    | Reject call, log warning, suggest compression             |

---

## Tool Use Boundaries

The tool registry enforces safe tool usage:

| Boundary                 | Enforcement                                            |
| ------------------------ | ------------------------------------------------------ |
| **Whitelist**            | Only approved tools can be called                      |
| **Call Limits**          | Max calls per tool per session                         |
| **Dangerous Tasks**      | Detect and block destructive operations (e.g., rm -rf) |
| **Parameter Validation** | Validate tool parameters before execution              |

---

## Agent Behavior Rules for Harness Engineering

When working with the harness:

1. **All model calls go through the harness** — Never bypass error boundaries, context monitoring, or tool registries
2. **Handle all three failure modes** — Implement timeout, rate-limit, and validation recovery
3. **Enforce token budgets** — Use `context_monitor.py` to prevent context window overflow
4. **Whitelist tools** — Only approved tools in `tool_registry.py` can be called
5. **Log all errors** — Error boundaries must log failures for post-incident analysis
6. **Test error recovery** — Verify harness handles failures gracefully

---

## Integration Points

| From                       | To                                | What Flows                                      |
| -------------------------- | --------------------------------- | ----------------------------------------------- |
| `context-engineering/`     | Harness Engineering               | Assembled, budget-compliant context window      |
| Harness Engineering        | LLM Model                         | Validated, monitored model call                 |
| Harness Engineering        | `retrieval-augmented-generation/` | Agent-generated artifacts (feedback loop)       |
| `multi-agent-engineering/` | Harness Engineering               | Every agent's model call routes through harness |

---

## Active Research Programme

**Harness Performance Benchmarking** — What is the latency cost of the full error boundary stack at p99?

See `core-component-00/README.md` § Active Research Programmes for current status.

---

## Related Steering Files

- `context-engineering.md` — Layer 2: Context window assembly before harness execution
- `multi-agent-engineering.md` — Layer 5: Every agent's model call routes through harness
- `rag-engineering.md` — Layer 4: Harness feeds artifacts back to RAG (feedback loop)
- `ase-framework.md` — ASE governance and compliance requirements
- `cc00-overview.md` — Complete CC-00 laboratory overview

---

**This steering file is automatically activated when working in `harness-engineering/` directories or harness-related Python files.**
