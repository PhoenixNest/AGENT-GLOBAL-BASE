---
name: cc00-safety-regression-testing
description: Regression testing to confirm previously-fixed safety findings stay fixed across module changes. Owned by Dr. Tomasz Wieczorek (Staff Safety & Evaluation Engineer). Trigger: safety regression, re-test finding, fix verification.
version: "1.0.0"
---

# Safety Regression Testing

**Skill ID:** safety-regression-testing
**Role:** Staff Safety & Evaluation Engineer
**Seniority:** L4 — Staff

## Overview

Maintains and re-runs a regression suite of previously-found safety issues against every
subsequent change to the four production-grade modules, confirming fixes stay fixed rather than
silently regressing.

## Tools & Frameworks

| Tool                    | Proficiency | Use Case                                                              |
| ----------------------- | ----------- | --------------------------------------------------------------------- |
| Regression suite design | Expert      | Converting one-off findings into repeatable tests                     |
| pytest integration      | Advanced    | Wiring safety regression cases into each module's existing test suite |

## Module Ownership

- Maintains a cross-module safety regression suite, separate from but complementary to each
  module's functional `pytest` coverage
- Coordinates with the new Infrastructure Engineer (Deshmukh) on the proposed CI-for-research
  pattern so safety regressions run automatically, not only when manually triggered
- Reports any regression (a previously-fixed finding that resurfaces) to Dr. Vance immediately,
  treated with the same urgency as a new finding

## Scenarios & Trade-offs

### Scenario 1: A Fix Regresses After an Unrelated Module Change

- **Approach:** Treat this as evidence the original fix was too narrowly scoped or the module
  lacks a guard against the regression path — recommend a structural fix, not just re-patching
- **Trade-off:** Structural fixes take longer than re-patching the symptom
- **Quality Bar:** Every regression report includes a root-cause hypothesis, not just "it broke again"

### Scenario 2: Regression Suite Growth Slows Down CI

- **Approach:** Prioritize regression cases by severity of the original finding; do not silently
  drop low-severity cases to save time without flagging the trade-off explicitly
- **Trade-off:** A growing suite eventually needs runtime management, in tension with fast CI
- **Quality Bar:** Any case removed or deprioritized from the regression suite is logged with
  rationale, not silently dropped

## Quality Standards

- Every closed safety finding gets a permanent regression test, not a one-time fix verification
- Regression suite runs on every module change once CI-for-research is adopted
- Regressions are reported with the same urgency and format as new findings

## References

- Adversarial Evaluation Design (this crew member) — source of findings that become regression cases
- CI-for-Research Tooling (Ravi Deshmukh, Infrastructure Engineer) — planned automation target
