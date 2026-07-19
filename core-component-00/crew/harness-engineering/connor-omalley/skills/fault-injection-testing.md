---
name: cc00-fault-injection-testing
description: Fault-injection test design for error_boundary.py recovery paths. Owned by Connor O'Malley (Senior Research Engineer II, Harness Engineering). Trigger: fault injection, recovery path testing, error boundary hardening.
version: "1.0.0"
---

# Fault-Injection Testing

**Skill ID:** fault-injection-testing
**Role:** Senior Research Engineer II — Harness Engineering
**Seniority:** L3 — Senior

## Overview

Designs and maintains fault-injection test cases for `error_boundary.py`'s recovery paths —
deliberately forcing timeout, rate-limit, and validation-failure conditions to verify recovery
behavior, rather than only testing the happy path.

## Tools & Frameworks

| Tool                       | Proficiency | Use Case                                         |
| -------------------------- | ----------- | ------------------------------------------------ |
| Fault-injection frameworks | Expert      | Simulated timeout/rate-limit/validation failures |
| Recovery-path verification | Expert      | Confirming each failure mode recovers correctly  |

## Module Ownership

- Owns the fault-injection test suite for `error_boundary.py` under Kwame Asante's recovery-logic
  design — he defines the recovery strategy; O'Malley verifies it holds under injected failure
- Coordinates with Dr. Wieczorek on adversarial fault scenarios beyond standard fault injection
  (e.g., deliberately crafted retry-cap bypass attempts)

## Scenarios & Trade-offs

### Scenario 1: A New Recovery Path Is Added Without a Corresponding Fault-Injection Test

- **Approach:** Block merge until the new path has a fault-injection test forcing that specific
  failure mode — no recovery path ships untested against its own trigger condition
- **Trade-off:** Adds a hard gate to harness changes, slowing down otherwise-ready fixes
- **Quality Bar:** Every recovery path in `error_boundary.py` has a corresponding fault-injection
  test, no exceptions

### Scenario 2: Fault Injection Reveals a Recovery Path That Masks a Deeper Bug

- **Approach:** Report the masking behavior to Asante as a design concern, not just confirm the
  recovery "worked" — recovering from a symptom while hiding its cause is a different outcome
  than genuine resilience
- **Trade-off:** Distinguishing "recovered" from "recovered but masked something" requires deeper
  investigation than a pass/fail test result
- **Quality Bar:** Every fault-injection pass includes a note on whether the underlying cause was
  also addressed, not just the symptom

## Quality Standards

- 100% of documented recovery paths have a corresponding fault-injection test
- Test suite is re-run against every `error_boundary.py` change before merge
- Findings that suggest masked root causes are escalated, not just logged as a pass

## References

- `core-component-00/engineering/harness-engineering/implementations/error_boundary.py`
- Error Boundary Implementation (Kwame Asante) — the module lead's recovery-logic design ownership
