---
name: cc00-memory-store-engineering
description: Four-tier memory store implementation (episodic, semantic, procedural, working) for memory_store.py. Owned by Mei-Ling Zhao (Senior Research Engineer, Context Engineering). Trigger: memory store, episodic memory, semantic memory, procedural memory, working memory.
version: "1.0.0"
---

# Memory Store Engineering

**Skill ID:** memory-store-engineering
**Role:** Senior Research Engineer — Context Engineering
**Seniority:** L3 — Senior

## Overview

Design and production hardening of the four-tier memory store implemented in
`core-component-00/context-engineering/implementations/memory_store.py`, distinguishing episodic
(session events), semantic (durable facts), procedural (learned patterns), and working (current
task) memory.

## Tools & Frameworks

| Tool               | Proficiency | Use Case                                        |
| ------------------ | ----------- | ----------------------------------------------- |
| Python             | Expert      | Memory store implementation                     |
| SQLite/JSON stores | Advanced    | Episodic/semantic persistence backends          |
| pytest             | Expert      | Cross-tier retrieval and eviction test coverage |

## Module Ownership

- Maintains the four memory tiers and their read/write/eviction contracts in `memory_store.py`
- Owns tier-boundary decisions: what qualifies as semantic (durable, cross-session) vs. episodic
  (session-scoped) — ambiguous cases are documented, not guessed
- Coordinates with Dr. Farouk (Multi-Agent Engineering) on shared-memory access patterns when
  multiple agents read/write the same store

## Scenarios & Trade-offs

### Scenario 1: Episodic-to-Semantic Promotion

- **Approach:** Facts repeated across ≥ 3 episodic entries within a session are candidates for
  promotion to semantic memory, subject to an explicit confidence check
- **Trade-off:** Over-promotion pollutes durable memory with session-specific noise; under-promotion
  loses useful durable facts
- **Quality Bar:** Promoted facts are traceable to their originating episodic entries for audit

### Scenario 2: Working Memory Eviction Under Pressure

- **Approach:** Working memory evicts least-recently-used items first when the harness signals
  budget pressure via `context_monitor.py`
- **Trade-off:** LRU eviction is simple but can evict task-critical items that were set early and
  read rarely — a pinning mechanism exists for explicitly protected entries
- **Quality Bar:** No task-critical pinned item is ever evicted; eviction order is logged

## Quality Standards

- Each memory tier has an independent test suite; cross-tier promotion logic tested in isolation
- No memory tier grows unbounded — every tier has a documented eviction or expiry policy
- Store operations are idempotent under retry

## References

- CC-00 Six Pillars of Context Engineering (Dr. Vance, internal framework, 2025)
- `core-component-00/context-engineering/implementations/memory_store.py`
