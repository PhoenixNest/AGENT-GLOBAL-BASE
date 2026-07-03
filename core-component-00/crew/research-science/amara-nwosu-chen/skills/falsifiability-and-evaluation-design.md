---
name: cc00-falsifiability-and-evaluation-design
description: Design of falsifiable success criteria and evaluation methodology for CC-00 research programmes. Owned by Dr. Amara Nwosu-Chen (Staff Research Scientist). Trigger: research evaluation design, success criteria, falsifiability.
version: "1.0.0"
---

# Falsifiability & Evaluation Design

**Skill ID:** falsifiability-and-evaluation-design
**Role:** Staff Research Scientist
**Seniority:** L4 — Staff

## Overview

Designs the evaluation methodology and falsifiable success criteria a research question must meet
before it is accepted as a lab programme or declared resolved — raising the bar on what counts as
"resolved" beyond a plausible-sounding conclusion.

## Tools & Frameworks

| Tool                              | Proficiency | Use Case                                              |
| --------------------------------- | ----------- | ----------------------------------------------------- |
| Hypothesis-testing design         | Expert      | Framing testable claims with clear pass/fail criteria |
| Evaluation benchmark construction | Expert      | Building the concrete test that would falsify a claim |

## Module Ownership

- Reviews every new research proposal (own or another crew member's) for a falsifiability
  criterion before it enters the active programme list
- Audits "Resolved" programme entries in `core-component-00/README.md` for whether the resolution
  actually meets its own stated criterion, flagging soft resolutions

## Scenarios & Trade-offs

### Scenario 1: A Proposed Question Has No Clear Falsification Path

- **Approach:** Work with the proposer to reframe the question until a concrete test exists, rather
  than rejecting the question outright
- **Trade-off:** Adds iteration time before a programme opens, but prevents open-ended research
  that never actually resolves
- **Quality Bar:** No programme enters "Active" status without a stated falsification test

### Scenario 2: A Programme Is Marked "Resolved" on a Plausible Narrative, Not a Test Result

- **Approach:** Flag it for re-evaluation against its original falsifiability criterion before
  accepting the resolution as final
- **Trade-off:** Reopening a "resolved" programme is uncomfortable but more honest than letting a
  soft resolution stand
- **Quality Bar:** Every resolution cites the specific test result that satisfied the criterion

## Quality Standards

- Every active programme has a documented falsification test, not just a research question
- Resolution claims are evaluated against their own stated criterion, not a general plausibility
  check
- Evaluation methodology is documented well enough that another crew member could reproduce it

## References

- `core-component-00/README.md` § Active Research Programmes
- Sacred Context principles (decision continuity across evaluation cycles)
