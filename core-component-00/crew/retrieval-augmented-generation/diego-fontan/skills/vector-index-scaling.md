---
name: cc00-vector-index-scaling
description: Vector index scaling and integrity operations for the RAG module's retrieval infrastructure. Owned by Diego Fontán (Senior Research Engineer II, RAG). Trigger: vector index scaling, index integrity, index performance.
version: "1.0.0"
---

# Vector Index Scaling

**Skill ID:** vector-index-scaling
**Role:** Senior Research Engineer II — Retrieval-Augmented Generation
**Seniority:** L3 — Senior

## Overview

Owns vector index scaling and integrity for the RAG module — ensuring index performance and
correctness hold as corpus size and query volume grow, complementing Sofia Almeida's retrieval
architecture ownership.

## Tools & Frameworks

| Tool                         | Proficiency | Use Case                                        |
| ---------------------------- | ----------- | ----------------------------------------------- |
| Vector index build tooling   | Expert      | Index construction and scaling                  |
| Index integrity verification | Expert      | Detecting orphaned/stale vectors after deletion |

## Module Ownership

- Owns index-scaling operations under Sofia Almeida's retrieval-pipeline architecture — she sets
  the design, he operates and scales the implementation
- Coordinates with Ravi Deshmukh (Infrastructure Engineer) on index storage/compute resourcing as
  corpus size grows

## Scenarios & Trade-offs

### Scenario 1: Index Rebuild Required at Scale

- **Approach:** Incremental rebuild in segments rather than a single blocking full rebuild, so
  retrieval remains available during the rebuild
- **Trade-off:** Segmented rebuilds are more complex to implement and verify than a simple
  stop-the-world rebuild
- **Quality Bar:** Retrieval availability during rebuild is measured, not assumed

### Scenario 2: Index Integrity After High-Volume Deletions

- **Approach:** Scheduled integrity verification catches orphaned vectors from deleted documents,
  rather than relying on delete operations being perfectly clean
- **Trade-off:** Verification adds periodic compute cost
- **Quality Bar:** Zero orphaned vectors survive past the next scheduled verification pass

## Quality Standards

- Index scaling changes are benchmarked against corpus-size and query-volume growth curves
- Integrity verification runs on a documented schedule, not ad-hoc
- Every scaling change is reviewed by Sofia Almeida before merge, per module co-ownership

## References

- `core-component-00/retrieval-augmented-generation/`
- Retrieval Pipeline Engineering (Sofia Almeida) — the module lead's architecture ownership
