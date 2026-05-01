# Harness Configuration Specification — Backend API Pipeline

> **ASE Layer:** 3 — Harness Engineering (Mandatory)
> **Authority:** CTO Dr. Kenji Nakamura
> **Reference implementations:** `core-component-00/harness-engineering/implementations/`
> **Compliance standard:** `core-component-00/agent-systems-engineering/governance/compliance-standard.md` §Layer 3

This document defines the harness configuration that **every executor agent** operating in the Backend API Pipeline must apply. These are not suggestions — missing any Mandatory item is a P0 compliance gap that blocks production readiness.

---

## 1. Timeout Configuration

> **Tier:** Mandatory | **Reference:** `error_boundary.py`

| Call Type                | Timeout | On Expiry                                                    |
| :----------------------- | :-----: | :----------------------------------------------------------- |
| LLM inference call       |  30 s   | Log `TimeoutError` → retry (see §2)                          |
| Tool call (read/search)  |  10 s   | Log `TimeoutError` → retry once then skip                    |
| Tool call (write/deploy) |  20 s   | Log `TimeoutError` → escalate to stage owner                 |
| Stage gate validation    |  60 s   | Log `TimeoutError` → halt and notify CTO                     |
| API endpoint test call   |  15 s   | Log `TimeoutError` → mark endpoint as untested; alert VP API |

> Never use a blanket catch-all timeout. Each call type has its own timeout and recovery action.

---

## 2. Typed Error Boundary

> **Tier:** Mandatory | **Reference:** `core-component-00/harness-engineering/implementations/error_boundary.py`

All errors must be caught by **type** — no blanket `except Exception` handling:

| Error Type                  | Recovery Action                                             | Max Retries |
| :-------------------------- | :---------------------------------------------------------- | :---------: |
| `TimeoutError`              | Log → retry with same parameters                            |      3      |
| `RateLimitError` (HTTP 429) | Exponential backoff + jitter → retry (see §3)               |      5      |
| `ValidationError`           | Return structured error object to stage owner; do not retry |      0      |
| `AuthError`                 | Log → halt; escalate to CTO immediately                     |      0      |
| `ContextOverflowError`      | Invoke compressor (see §4) → retry                          |      1      |

> If all retries are exhausted and the error is unresolved, escalate to the stage owner with a full error log. **Silent failure is a P0 defect.**

---

## 3. Rate-Limit Retry (429 Backoff)

> **Tier:** Mandatory | **Reference:** `error_boundary.py`

```
base_delay = 1s
max_delay  = 32s

for attempt in 1..5:
    wait = min(base_delay * 2^attempt + random_jitter(0..1s), max_delay)
    retry call
    if success: break
```

After 5 failed attempts, surface a `RateLimitError` to the stage owner with timestamp and attempt count.

---

## 4. Token Budget Monitor

> **Tier:** Mandatory | **Reference:** `core-component-00/harness-engineering/implementations/context_monitor.py`

|          Threshold          | Action                                                                         |
| :-------------------------: | :----------------------------------------------------------------------------- |
| 70% of model context window | Log warning; notify stage owner                                                |
|             85%             | Prune: invoke `context_compressor.py` targeting Zone C first, then Zone B      |
|             90%             | Emergency: downgrade to Minimal handoff tier; alert CTO if in multi-agent mode |

> Zone A (Sacred Context) is **never pruned** at any threshold. See `mvc-context-profile.md` §Token Budget Allocation.

---

## 5. Tool Registry

> **Tier:** Required (when tools are invoked) | **Reference:** `core-component-00/harness-engineering/implementations/tool_registry.py`

**Whitelist principle:** agents may only invoke tools explicitly listed for their pipeline stage. Unlisted tools are silently blocked and the attempt is logged.

| Risk Level | Tool Category                                                  |          Gate Required?          |
| :--------- | :------------------------------------------------------------- | :------------------------------: |
| Low        | Read files, search, query                                      |                No                |
| Medium     | Write files, create branches                                   |           No (logged)            |
| High       | Deploy API, send external comms, delete records                |       **Yes — User gate**        |
| Critical   | Irreversible ops (production release, DB migration, data wipe) | **Yes — explicit User approval** |

Per-task call caps apply. No single task may make more than **20 tool calls** without supervisor review. Infinite loops are blocked at call cap.

---

## 6. PII Handling

> **Tier:** Required

| Step                       | Action                                                                                  |
| :------------------------- | :-------------------------------------------------------------------------------------- |
| Before LLM call            | Scrub all PII from input (names, emails, device IDs, API keys, tokens, database values) |
| After LLM response         | Scan output for PII patterns before passing to downstream stages or API specs           |
| On PII detection in output | Redact → log incident → notify CIO Dr. Priya Mehta                                      |

> PII in API specs, logs, or generated documentation is a P0 defect. Zero-tolerance — no exceptions.

---

## 7. Degradation Tiers

> **Tier:** Recommended | **Reference:** `core-component-00/harness-engineering/CONCEPTS.md` §degradation

When the full harness stack encounters sustained failures, degrade gracefully:

| Tier             | Condition                    | Behaviour                                                                   |
| :--------------- | :--------------------------- | :-------------------------------------------------------------------------- |
| Tier 1 (Full)    | Normal operation             | Full pipeline execution with all harness checks                             |
| Tier 2 (Reduced) | >2 consecutive tool failures | Disable non-critical tools; continue with core capabilities                 |
| Tier 3 (Minimal) | >3 consecutive LLM failures  | Human-in-the-loop only; surface raw inputs to stage owner for manual review |

---

## Compliance Checklist

Before any pipeline stage execution, verify:

- [ ] Timeouts configured per §1 for all call types (including API test call timeout)
- [ ] Error boundary handles all 5 error types by name (no blanket catch)
- [ ] 429 retry with exponential backoff + jitter is active (§3)
- [ ] Token budget monitor thresholds set at 70%/85%/90% (§4)
- [ ] Tool registry whitelist loaded for current stage (§5)
- [ ] PII scrubber applied to inputs; PII scanner applied to outputs (§6)
- [ ] High-risk operations gated with explicit User approval before execution (§5)
- [ ] Tool call limit (20 per task) enforced; supervisor review required if exceeded (§5)
