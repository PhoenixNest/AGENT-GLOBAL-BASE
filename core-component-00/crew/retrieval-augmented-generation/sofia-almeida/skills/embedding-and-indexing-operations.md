---
name: cc00-embedding-and-indexing-operations
description: Production embedding and indexing pipeline operations for the RAG module. Owned by Sofia Almeida (Senior Research Engineer, RAG). Trigger: embedding pipeline, indexing, vector index, re-embedding, index freshness.
version: "1.0.0"
---

# Embedding & Indexing Operations

**Skill ID:** embedding-and-indexing-operations
**Role:** Senior Research Engineer — Retrieval-Augmented Generation
**Seniority:** L3 — Senior

## Overview

Operational ownership of the embedding generation and vector indexing pipeline that feeds
retrieval — corpus ingestion, embedding model selection, index build/update cadence, and
re-embedding on model change.

## Tools & Frameworks

| Tool                        | Proficiency | Use Case                                  |
| --------------------------- | ----------- | ----------------------------------------- |
| Sentence-transformer models | Expert      | Document/query embedding generation       |
| Vector index build tooling  | Expert      | Index construction and incremental update |
| Batch job orchestration     | Advanced    | Corpus-scale re-embedding runs            |

## Module Ownership

- Owns embedding model selection and versioning; documents the tradeoff analysis behind any
  embedding model change
- Owns index build and incremental-update cadence — new/changed documents must reach the index
  within a documented SLA, not an undefined "eventually"
- Owns re-embedding runbooks for corpus-scale operations (full re-embed on model upgrade,
  incremental re-embed on schema change)

## Scenarios & Trade-offs

### Scenario 1: Embedding Model Upgrade Mid-Corpus

- **Approach:** New and old embeddings are never mixed in one index; upgrades trigger a full
  re-embed with a documented cutover point, not a gradual blend
- **Trade-off:** Full re-embed is costly at scale but avoids silent similarity-score drift from
  mixed embedding spaces
- **Quality Bar:** Cutover is atomic from the retrieval consumer's perspective — no query ever
  compares embeddings from two different model versions

### Scenario 2: Incremental Index Update Latency

- **Approach:** New documents are embedded and indexed on a defined cadence (not real-time unless
  explicitly required); the SLA is documented and monitored
- **Trade-off:** Real-time indexing adds infrastructure complexity; batched indexing is simpler but
  introduces staleness — directly feeds the Retrieval Freshness Guarantees research question
- **Quality Bar:** Actual indexing latency is measured against the documented SLA, not assumed

## Quality Standards

- Every index has a documented freshness SLA and a monitor verifying it is met
- Re-embedding runbooks are tested on a staging corpus before production execution
- Index integrity (no orphaned/stale vectors after document deletion) is verified on a schedule

## References

- `core-component-00/retrieval-augmented-generation/`
- Retrieval Freshness Guarantees research programme (Dr. Vance, PI / Sofia Almeida, execution)
