---
name: cc00-multi-fleet-isolation
description: fleet_id-scoped isolation to prevent state leakage between concurrent independent swarms. Owned by Amina Yusuf (Senior Research Engineer II, Multi-Agent Engineering). Trigger: fleet isolation, multi-fleet, fleet_id scoping, concurrent swarms.
version: "1.0.0"
---

# Multi-Fleet Isolation

**Skill ID:** multi-fleet-isolation
**Role:** Senior Research Engineer II — Multi-Agent Engineering
**Seniority:** L3 — Senior

## Overview

Ensures `fleet_id`-scoped isolation holds under concurrent load — multiple independent swarms
running simultaneously must never leak state, context, or results across fleet boundaries.

## Tools & Frameworks

| Tool                       | Proficiency | Use Case                                    |
| -------------------------- | ----------- | ------------------------------------------- |
| Concurrent systems testing | Expert      | Verifying isolation under simultaneous load |
| State-leak detection       | Advanced    | Identifying cross-fleet contamination paths |

## Module Ownership

- Owns the test suite verifying `fleet_id` scoping holds under concurrent multi-fleet load,
  extending `test_swarm_orchestrator.py`'s existing fleet-scoping coverage
- Coordinates with Dr. Wieczorek when a potential isolation gap is found, since cross-fleet leakage
  is a safety-relevant finding, not just a functional bug

## Scenarios & Trade-offs

### Scenario 1: Two Fleets Share an Underlying Resource (e.g., a Shared Memory Store)

- **Approach:** Resource access is namespaced by `fleet_id` even when the underlying store is
  shared infrastructure — isolation is enforced at the access layer, not by assuming separate
  physical resources
- **Trade-off:** Namespacing adds a layer of indirection to every resource access
- **Quality Bar:** No test can construct a cross-fleet read/write using a shared resource

### Scenario 2: High Fleet Count Under Load

- **Approach:** Isolation guarantees are tested at increasing fleet counts, not just the 2-fleet
  minimal case, since contention patterns can differ at scale
- **Trade-off:** High-fleet-count tests take longer to run
- **Quality Bar:** Isolation holds at the highest fleet count the lab's actual usage patterns require

## Quality Standards

- Every isolation test includes a concurrent-load scenario, not just sequential fleet creation
- Any confirmed leak is treated as a safety finding, escalated to Dr. Wieczorek and Dr. Vance
  immediately, not just fixed silently
- Test coverage extends `test_swarm_orchestrator.py`, not a separate untracked suite

## References

- `core-component-00/engineering/multi-agent-engineering/testing/test_swarm_orchestrator.py`
- Adversarial Evaluation Design (Dr. Wieczorek) — escalation path for confirmed isolation gaps
