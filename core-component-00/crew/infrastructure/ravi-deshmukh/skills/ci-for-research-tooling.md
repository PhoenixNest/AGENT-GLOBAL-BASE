---
name: cc00-ci-for-research-tooling
description: Automated per-module pytest execution on every implementation change, replacing the current manual per-module test-running convention. Owned by Ravi Deshmukh (Infrastructure Engineer). Trigger: CI for research, automated testing, pytest automation.
version: "1.0.0"
---

# CI-for-Research Tooling

**Skill ID:** ci-for-research-tooling
**Role:** Infrastructure Engineer
**Seniority:** L3 — Senior

## Overview

Designs and implements automated per-module `pytest` execution triggered on every implementation
change, replacing the manual `pytest <module>/testing/ -v` convention documented in
`core-component-00/CLAUDE.md`. Proposed during vetting; pending adoption.

## Tools & Frameworks

| Tool                 | Proficiency | Use Case                                                          |
| -------------------- | ----------- | ----------------------------------------------------------------- |
| CI pipeline design   | Advanced    | Per-module trigger and isolation design                           |
| pytest orchestration | Expert      | Running module test suites without cross-module import collisions |

## Module Ownership

- Designs the CI trigger so each module's tests run in isolation, preserving the existing rule
  against running all modules together with a single root-level `pytest .`
- Coordinates with Dr. Wieczorek to wire the safety regression suite into the same CI trigger once
  both are operational
- Does not change module implementation code to make it "more testable" without the owning
  Research Engineer's involvement — infra automates existing tests, doesn't redesign them

## Scenarios & Trade-offs

### Scenario 1: A Module Change Triggers Unrelated Modules' Tests

- **Approach:** Trigger scoping is per-module-folder, matching the existing manual convention
  exactly — a change in `harness-engineering/` triggers only harness tests, not RAG's
- **Trade-off:** Misses genuine cross-module regressions that a full-suite run would catch
- **Quality Bar:** Cross-module regression risk is covered by Dr. Wieczorek's safety regression
  suite instead, not by over-triggering CI

### Scenario 2: CI Run Time Grows as the Safety Regression Suite Grows

- **Approach:** Parallelize per-module and per-suite runs rather than running everything serially
- **Trade-off:** Parallelization adds infrastructure complexity
- **Quality Bar:** CI feedback time is tracked and doesn't silently grow unbounded

## Quality Standards

- CI trigger respects the existing per-module isolation rule — never introduces a root-level
  `pytest .` run
- Every CI failure is traceable to the specific module and test that failed, no ambiguity
- Adoption is proposed to Dr. Vance and the four module owners before being made mandatory

## References

- `core-component-00/CLAUDE.md` § Running Tests (PowerShell)
- Safety Regression Testing (Dr. Wieczorek) — planned integration target
