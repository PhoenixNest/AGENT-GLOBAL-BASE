---
name: cc00-context-budget-monitoring
description: Token budget enforcement and backpressure signaling implementation for context_monitor.py. Owned by Kwame Asante (Senior Research Engineer, Harness Engineering). Trigger: context budget, token budget monitor, backpressure, H-CE01, budget alert.
version: "1.0.0"
---

# Context Budget Monitoring

**Skill ID:** context-budget-monitoring
**Role:** Senior Research Engineer — Harness Engineering
**Seniority:** L3 — Senior

## Overview

Production implementation of `core-component-00/harness-engineering/implementations/context_monitor.py`
— token budget enforcement and tiered alerting that signals other modules (memory eviction,
session compression) when a session approaches its context budget.

## Tools & Frameworks

| Tool                   | Proficiency | Use Case                                  |
| ---------------------- | ----------- | ----------------------------------------- |
| Python                 | Expert      | Budget tracking and threshold evaluation  |
| tiktoken               | Expert      | Real-time token accounting                |
| Event-driven signaling | Advanced    | Emitting backpressure events to consumers |

## Module Ownership

- Maintains `context_monitor.py`: threshold configuration (e.g. the 500KB H-CE01 alert tier),
  real-time token accounting, and event emission to consuming modules
- Coordinates with Mei-Ling Zhao so `context_compressor.py` and `memory_store.py` eviction
  respond correctly to emitted budget-pressure events rather than polling
- Owns the accuracy of the token accounting itself — a monitor that under-counts is a silent
  reliability defect, not a minor bug

## Scenarios & Trade-offs

### Scenario 1: Multiple Consumers of One Budget Signal

- **Approach:** Budget-pressure events are broadcast (compression, memory eviction, and any future
  consumer all subscribe) rather than the monitor picking one action to trigger directly
- **Trade-off:** Broadcast decouples the monitor from consumer-specific logic but requires each
  consumer to handle duplicate or rapid-fire events idempotently
- **Quality Bar:** No consumer double-acts on a single budget-pressure event; event de-duplication
  tested explicitly

### Scenario 2: Tokenizer Drift Across Models

- **Approach:** Token accounting is tokenizer-pluggable per target model rather than hardcoded to
  one tokenizer
- **Trade-off:** Pluggable accounting adds configuration surface but avoids silent miscounting when
  the lab's default model changes
- **Quality Bar:** Accounting error stays within 1% of the target model's actual tokenizer output

## Quality Standards

- Every threshold tier is covered by a test that crosses it and verifies the correct event fires
- Token accounting is benchmarked against real tokenizer output, not estimated
- No budget check runs synchronously on the hot path in a way that adds measurable latency

## References

- `core-component-00/harness-engineering/implementations/context_monitor.py`
- Sacred Context principles (Dr. Vance / Mei-Ling Zhao, context-engineering)
