---
name: cc00-rag-evaluation-and-freshness
description: RAG evaluation harness design and staleness-bounding research for the Retrieval Freshness Guarantees programme. Owned by Sofia Almeida (Senior Research Engineer, RAG). Trigger: RAG evaluation, retrieval freshness, staleness bound, evaluation harness.
version: "1.0.0"
---

# RAG Evaluation & Freshness

**Skill ID:** rag-evaluation-and-freshness
**Role:** Senior Research Engineer — Retrieval-Augmented Generation
**Seniority:** L3 — Senior

## Overview

Design of the RAG module's evaluation harness (retrieval precision/recall, answer groundedness)
and execution of the lab's open Retrieval Freshness Guarantees research question: bounding
staleness of retrieved facts at inference time.

## Tools & Frameworks

| Tool                      | Proficiency | Use Case                                      |
| ------------------------- | ----------- | --------------------------------------------- |
| Retrieval eval frameworks | Expert      | Precision/recall/groundedness scoring         |
| Staleness instrumentation | Expert      | Measuring time-since-index for served results |
| Statistical analysis      | Advanced    | Bounding staleness distributions rigorously   |

## Module Ownership

- Owns the RAG module's evaluation harness: retrieval precision/recall against a labeled query
  set, and answer-groundedness scoring (does the generated answer actually derive from retrieved
  content)
- Leads execution of the Retrieval Freshness Guarantees programme — instrumenting time-since-index
  on every served retrieval result and publishing bounded-staleness guarantees per corpus type
- Reports evaluation regressions to Dr. Vance before any retrieval-pipeline change ships

## Scenarios & Trade-offs

### Scenario 1: High Recall, Low Groundedness

- **Approach:** Recall and groundedness are scored and reported separately, never collapsed into
  one composite metric that can hide a groundedness regression behind a recall improvement
- **Trade-off:** Two-metric reporting is less digestible than a single score but prevents
  Goodhart's-law optimization toward recall alone
- **Quality Bar:** Every retrieval-pipeline change reports both metrics on the evaluation set
  before merge

### Scenario 2: Bounding Staleness for Frequently-Updated Corpora

- **Approach:** Staleness bounds are corpus-specific (a rapidly-changing corpus gets a tighter
  bound and more frequent re-indexing) rather than one global guarantee
- **Trade-off:** Per-corpus bounds require more configuration but avoid over-promising freshness on
  volatile data or over-indexing static data
- **Quality Bar:** Published staleness bound for each corpus is empirically verified, not
  theoretical

## Quality Standards

- Evaluation set is versioned and reviewed quarterly for drift from real query patterns
- Every staleness-bound claim is backed by measured data, not estimated
- Evaluation harness runs are reproducible given a fixed index snapshot

## References

- Retrieval Freshness Guarantees research programme (Dr. Vance, PI / Sofia Almeida, execution)
- `core-component-00/retrieval-augmented-generation/`
