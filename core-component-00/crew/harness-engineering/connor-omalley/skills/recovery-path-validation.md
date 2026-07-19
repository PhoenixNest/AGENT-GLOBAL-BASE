---
name: cc00-recovery-path-validation
description: Operational validation of context_monitor.py and tool_registry.py under real usage patterns. Owned by Connor O'Malley (Senior Research Engineer II, Harness Engineering). Trigger: context monitor validation, tool registry validation, harness operations.
version: "1.0.0"
---

# Recovery Path Validation

**Skill ID:** recovery-path-validation
**Role:** Senior Research Engineer II — Harness Engineering
**Seniority:** L3 — Senior

## Overview

Takes primary day-to-day operational ownership of `context_monitor.py` and `tool_registry.py` —
validating budget-threshold and tool-safety behavior against real usage patterns, freeing Kwame
Asante to focus on the Harness Performance Benchmarking research programme.

## Tools & Frameworks

| Tool                               | Proficiency | Use Case                                         |
| ---------------------------------- | ----------- | ------------------------------------------------ |
| Threshold validation testing       | Expert      | Confirming budget-alert tiers fire correctly     |
| Tool-safety operational monitoring | Advanced    | Day-to-day whitelist and call-limit verification |

## Module Ownership

- Operates `context_monitor.py` and `tool_registry.py` day-to-day — threshold tuning, whitelist
  maintenance, call-limit adjustments — under Asante's original design
- Escalates any proposed threshold or whitelist change with cross-module impact to Asante before
  implementing, since design authority remains his

## Scenarios & Trade-offs

### Scenario 1: Budget-Alert Threshold Needs Tuning Based on Real Usage Data

- **Approach:** Propose threshold changes backed by measured false-positive/false-negative alert
  rates, not intuition about what "feels right"
- **Trade-off:** Data collection takes time before a tuning change can be justified
- **Quality Bar:** Every threshold change cites the measured data that motivated it

### Scenario 2: A New Tool Needs Whitelisting for a Specific Crew Member's Role

- **Approach:** Whitelist requests are scoped to the specific role and documented with the need,
  not granted as a blanket addition to a shared whitelist
- **Trade-off:** Per-role whitelist requests add administrative overhead vs. one shared list
- **Quality Bar:** No whitelist grant exists without a documented need traceable to a specific role

## Quality Standards

- Threshold and whitelist changes are logged with rationale and data, not made silently
- Operational metrics (alert accuracy, call-limit hit rate) are tracked over time, not just at
  point of initial tuning
- Design-level changes (not just operational tuning) are reviewed by Asante before merge

## References

- Context Budget Monitoring (Kwame Asante) — the module lead's design ownership
- Tool Registry Hardening (Kwame Asante) — the module lead's design ownership
