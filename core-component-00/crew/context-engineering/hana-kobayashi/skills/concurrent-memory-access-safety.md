---
name: cc00-concurrent-memory-access-safety
description: Concurrent multi-agent access safety for the memory store, including memory-poisoning attack surface mitigation. Owned by Hana Kobayashi (Senior Research Engineer II, Context Engineering). Trigger: concurrent memory access, memory poisoning, multi-agent memory safety.
version: "1.0.0"
---

# Concurrent Memory Access Safety

**Skill ID:** concurrent-memory-access-safety
**Role:** Senior Research Engineer II — Context Engineering
**Seniority:** L3 — Senior

## Overview

Owns safety of concurrent multi-agent access to `memory_store.py`, including mitigation of the
memory-poisoning attack surface (crafted episodic entries designed to corrupt semantic promotion
or downstream agent behavior) identified during Phase 3 vetting.

## Tools & Frameworks

| Tool                               | Proficiency | Use Case                                           |
| ---------------------------------- | ----------- | -------------------------------------------------- |
| Concurrent access control design   | Expert      | Multi-agent read/write safety                      |
| Input validation for memory writes | Advanced    | Detecting and rejecting crafted poisoning attempts |

## Module Ownership

- Owns the memory-poisoning mitigation identified during her own vetting interview — the finding
  that got her hired becomes her first assigned implementation task
- Coordinates with Dr. Wieczorek (Safety & Evaluation) on adversarial test cases for the
  mitigation, since this is a safety-relevant fix, not just a performance one

## Scenarios & Trade-offs

### Scenario 1: Distinguishing Legitimate Unusual Episodic Entries from Poisoning Attempts

- **Approach:** Flag entries with statistically unusual promotion-triggering patterns for review
  rather than auto-rejecting anything unusual, which would also block legitimate edge cases
- **Trade-off:** Flag-for-review requires a review path to exist and be resourced, not just an
  auto-reject switch
- **Quality Bar:** False-positive rate on legitimate unusual entries is tracked, not assumed low

### Scenario 2: Multiple Agents Writing to Shared Episodic Memory Simultaneously

- **Approach:** Writes are validated independently per-agent before any promotion evaluation runs,
  so one agent's crafted entry can't influence another's legitimate promotion decision
- **Trade-off:** Independent validation adds per-write overhead
- **Quality Bar:** No promotion decision is influenced by an entry from a different agent's write
  that hasn't independently passed validation

## Quality Standards

- The memory-poisoning mitigation is verified against Dr. Wieczorek's original adversarial test
  case before being considered resolved
- Concurrent-access safety is tested under genuinely concurrent multi-agent write load, not
  simulated sequentially
- Every validation rule has a documented rationale, not an arbitrary threshold

## References

- Adversarial Evaluation Design (Dr. Wieczorek) — source of the original finding
- `core-component-00/engineering/context-engineering/implementations/memory_store.py`
