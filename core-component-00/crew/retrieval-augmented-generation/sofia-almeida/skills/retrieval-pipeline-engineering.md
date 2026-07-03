---
name: cc00-retrieval-pipeline-engineering
description: Layered retrieval architecture (semantic + keyword fusion, ACL-filtered retrieval) for the RAG module. Owned by Sofia Almeida (Senior Research Engineer, RAG). Trigger: retrieval pipeline, semantic search, keyword fusion, ACL-filtered retrieval, RAG architecture.
version: "1.0.0"
---

# Retrieval Pipeline Engineering

**Skill ID:** retrieval-pipeline-engineering
**Role:** Senior Research Engineer — Retrieval-Augmented Generation
**Seniority:** L3 — Senior

## Overview

Design and production hardening of the CC-00 RAG module's layered retrieval pipeline: semantic

- keyword fusion ranking and ACL-filtered retrieval, per `core-component-00/retrieval-augmented-generation/`.

## Tools & Frameworks

| Tool                   | Proficiency | Use Case                                  |
| ---------------------- | ----------- | ----------------------------------------- |
| Python (spacy, torch)  | Expert      | Retrieval pipeline implementation         |
| Vector index libraries | Expert      | Semantic similarity search                |
| BM25 / keyword search  | Expert      | Keyword-fusion ranking                    |
| ACL-aware filtering    | Advanced    | Access-controlled retrieval at query time |

## Module Ownership

- Owns the layered retrieval design: semantic similarity + keyword (BM25) fusion, with
  configurable fusion weights per document collection
- Owns ACL-filtered retrieval — no document is returned to a query context the requester is not
  authorized to see, enforced at retrieval time, not post-filtered
- Maintains the RAG module's heavy dependency footprint (`requirements.txt`, spaCy model
  installation) and documents install/verification steps for the team

## Scenarios & Trade-offs

### Scenario 1: Semantic-Only Results Miss Exact-Match Queries

- **Approach:** Keyword (BM25) fusion runs in parallel with semantic search; results are merged
  with a tunable weight rather than semantic-only ranking
- **Trade-off:** Fusion adds latency and tuning surface vs. semantic-only simplicity
- **Quality Bar:** Exact-match benchmark queries (known-item search) resolve correctly ≥ 95% of
  the time in the fused pipeline

### Scenario 2: ACL Filtering at Retrieval vs. Post-Filter

- **Approach:** ACL checks are applied inside the retrieval query itself (index-level filtering),
  never as a post-hoc filter on already-retrieved results
- **Trade-off:** Index-level filtering is more complex to implement but eliminates the risk of a
  post-filter bug leaking unauthorized content into context
- **Quality Bar:** Zero unauthorized-document leakage in the red-team ACL test suite

## Quality Standards

- Every retrieval collection has documented fusion weights and a rationale
- ACL enforcement is tested adversarially, not just for the happy path
- GPU availability (`torch.cuda.is_available()`) is verified before assuming acceleration; CPU
  fallback path is tested

## References

- Enterprise RAG architecture: slot-priority assembly, ACL-filtered retrieval, layered retrieval
  (Dr. Vance, research contributions)
- `core-component-00/retrieval-augmented-generation/`
