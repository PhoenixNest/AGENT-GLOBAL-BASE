# Harness Configuration Specification — Casual Games Studio Pipeline

> **ASE Layer:** 3 — Harness Engineering (Mandatory)
> **Authority:** Studio Director Dr. Marcus Vogel (co-signed: CTO Dr. Kenji Nakamura)
> **Reference implementations:** `core-component-00/harness-engineering/implementations/`
> **Compliance standard:** `core-component-00/agent-systems-engineering/governance/compliance-standard.md` §Layer 3
> **Studio ADR:** `studio/casual-games/pipeline/templates/monitoring/adr-ase-001.md`

This document defines the harness configuration that **every executor agent** operating in the Casual Games Studio Pipeline must apply. These are not suggestions — missing any Mandatory item is a P0 compliance gap that blocks production readiness.

---

## 1. Timeout Configuration

> **Tier:** Mandatory | **Reference:** `error_boundary.py`

| Call Type                 | Timeout | On Expiry                                                            |
| :------------------------ | :-----: | :------------------------------------------------------------------- |
| LLM inference call        |  30 s   | Log `TimeoutError` → retry (see §2)                                  |
| Tool call (read/search)   |  10 s   | Log `TimeoutError` → retry once then skip                            |
| Tool call (write/deploy)  |  20 s   | Log `TimeoutError` → escalate to stage owner                         |
| Kill gate evaluation      |  60 s   | Log `TimeoutError` → halt and notify Studio Director                 |
| Playtest metric ingestion |  15 s   | Log `TimeoutError` → flag metric as unconfirmed; alert Live Ops Lead |

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
| `AuthError`                 | Log → halt; escalate to Studio Director immediately         |      0      |
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

|          Threshold          | Action                                                                                    |
| :-------------------------: | :---------------------------------------------------------------------------------------- |
| 70% of model context window | Log warning; notify stage owner                                                           |
|             85%             | Prune: invoke `context_compressor.py` targeting Zone C first, then Zone B                 |
|             90%             | Emergency: downgrade to Minimal handoff tier; alert Studio Director if in multi-crew mode |

> Zone A (Sacred Context) is **never pruned** at any threshold. See `mvc-context-profile.md` §Token Budget Allocation.
>
> **Studio note:** GDD documents grow significantly through Stage 3–5. Monitor context budget
> proactively during Full Production (Stage 5) when GDD + build reports + playtest data accumulate.

---

## 5. Tool Registry

> **Tier:** Required (when tools are invoked) | **Reference:** `core-component-00/harness-engineering/implementations/tool_registry.py`

**Whitelist principle:** crew agents may only invoke tools explicitly listed for their pipeline stage. Unlisted tools are silently blocked and the attempt is logged.

| Risk Level | Tool Category                                                              |              Gate Required?               |
| :--------- | :------------------------------------------------------------------------- | :---------------------------------------: |
| Low        | Read files, search, query                                                  |                    No                     |
| Medium     | Write files, create branches                                               |                No (logged)                |
| High       | Submit to app stores, send marketing comms, delete build artifacts         |            **Yes — User gate**            |
| Critical   | Irreversible live-ops ops (global release, server shutdown, economy reset) | **Yes — Studio Director + User approval** |

Per-task call caps apply. No single task may make more than **20 tool calls** without Studio Director review. Infinite loops are blocked at call cap.

---

## 6. PII Handling

> **Tier:** Required

| Step                       | Action                                                                               |
| :------------------------- | :----------------------------------------------------------------------------------- |
| Before LLM call            | Scrub all PII from input (player data, device IDs, purchase history, API keys)       |
| After LLM response         | Scan output for PII patterns before passing to downstream stages or live ops systems |
| On PII detection in output | Redact → log incident → notify CSO Dr. Sarah Chen (parent company)                   |

> PII in playtest reports, live ops dashboards, or QBR documents is a P0 defect. Zero-tolerance — no exceptions.

---

## 7. Degradation Tiers

> **Tier:** Recommended | **Reference:** `core-component-00/harness-engineering/CONCEPTS.md` §degradation

When the full harness stack encounters sustained failures, degrade gracefully:

| Tier             | Condition                    | Behaviour                                                                       |
| :--------------- | :--------------------------- | :------------------------------------------------------------------------------ |
| Tier 1 (Full)    | Normal operation             | Full pipeline execution with all harness checks                                 |
| Tier 2 (Reduced) | >2 consecutive tool failures | Disable non-critical tools; continue with core capabilities                     |
| Tier 3 (Minimal) | >3 consecutive LLM failures  | Human-in-the-loop only; surface raw inputs to Studio Director for manual review |

---

## Compliance Checklist

Before any pipeline stage execution, verify:

- [ ] Timeouts configured per §1 for all call types (including kill gate and playtest metric timeouts)
- [ ] Error boundary handles all 5 error types by name (no blanket catch)
- [ ] 429 retry with exponential backoff + jitter is active (§3)
- [ ] Token budget monitor thresholds set at 70%/85%/90% with proactive GDD size monitoring (§4)
- [ ] Tool registry whitelist loaded for current stage (§5)
- [ ] PII scrubber applied to all player data inputs; PII scanner applied to all outputs (§6)
- [ ] High-risk operations gated with explicit User approval before execution (§5)
- [ ] Tool call limit (20 per task) enforced; supervisor review required if exceeded (§5)
