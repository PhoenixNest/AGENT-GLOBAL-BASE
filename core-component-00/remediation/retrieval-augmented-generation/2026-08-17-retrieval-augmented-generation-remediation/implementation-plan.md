# Implementation Plan — Retrieval-Augmented Generation (Layer 4)

---

## Metadata

| Field                       | Value                                                                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Plan ID**                 | `2026-08-17-retrieval-augmented-generation-remediation`                                                                                                |
| **Layer**                   | 4 — Retrieval-Augmented Generation                                                                                                                     |
| **Source Benchmark Report** | `core-component-00/benchmarks/retrieval-augmented-generation/2026-08-16-retrieval-augmented-generation-enterprise-assessment/enterprise-assessment.md` |
| **Owner**                   | Sofia Almeida (RAG lead)                                                                                                                               |
| **Reviewer**                | Dr. Elias Vance (independent of Owner)                                                                                                                 |
| **Hook-Change Gate**        | N/A — neither item in this plan touches `.claude/hooks/*.py`                                                                                           |
| **Status**                  | Verified — see `log/05-verification-i1-i2-verified.md`                                                                                                 |

---

## Included Items

| ID  | Source Row | Gap (restated, one line)                                                                       | Severity (inherited) | Item Owner    | Approach                                                                                                                                                              | Acceptance Criteria                                                                                                | Test Plan                                                                                                            | Target Date | Item Status                                            |
| --- | ---------- | ---------------------------------------------------------------------------------------------- | -------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------ |
| I1  | RAG R1     | ACL enforced only as a post-fusion in-memory filter; no permission predicate reaches the query | P1                   | Sofia Almeida | Thread `user_role` into `vector_store.search()` as a filter predicate and into the BM25 leg's candidate selection; keep `acl_filter()` as the documented second layer | A role-restricted query never returns a candidate set containing out-of-role documents, even before post-filtering | New test asserting the vector-store-level query itself excludes out-of-role docs, not just the final filtered result | TBD         | Verified — see `log/05-verification-i1-i2-verified.md` |
| I2  | RAG R2     | PII masking entirely unimplemented despite being a mandatory ASGF control for this module      | P1                   | Diego Fontán  | Add a masking step between chunking and embedding, invoked from `RAGPipeline.ingest()` before `self.embedder(chunk.text)`                                             | Ingested chunks containing synthetic PII patterns are masked before reaching the embedder                          | New dedicated test file under `testing/` with synthetic PII fixtures, asserting no raw PII reaches the embedder call | TBD         | Verified — see `log/05-verification-i1-i2-verified.md` |

---

## Cross-Layer Dependencies

[None identified]

---

## Gate Log

| Stage            | Entry                                                                                                                                                      | Summary                                                                                                                       |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 0 — Trigger      | `core-component-00/remediation/retrieval-augmented-generation/2026-08-17-retrieval-augmented-generation-remediation/log/01-drafting-i1-i2-opened.md`       | Topic opened from the signed-off RAG benchmark's 2 in-scope P1 rows                                                           |
| 2 — Approval     | `core-component-00/remediation/retrieval-augmented-generation/2026-08-17-retrieval-augmented-generation-remediation/log/02-approval-i1-i2-approved.md`     | Dr. Vance signed off as Reviewer on I1 and I2's Approach                                                                      |
| 3 — Execution    | `core-component-00/remediation/retrieval-augmented-generation/2026-08-17-retrieval-augmented-generation-remediation/log/03-execution-i1-executed.md`       | Sofia Almeida threaded `user_role` into the BM25 candidate corpus and `vector_store.search()`; `pytest` 83 passed             |
| 3 — Execution    | `core-component-00/remediation/retrieval-augmented-generation/2026-08-17-retrieval-augmented-generation-remediation/log/04-execution-i2-executed.md`       | Diego Fontán implemented `mask_pii()` and wired it into `RAGPipeline.ingest()`; `pytest` 83 passed                            |
| 4 — Verification | `core-component-00/remediation/retrieval-augmented-generation/2026-08-17-retrieval-augmented-generation-remediation/log/05-verification-i1-i2-verified.md` | Dr. Vance independently re-read both diffs and re-ran the suite himself (83 passed); both items confirmed; `Status: Verified` |

---

## Open Follow-Up Items

[None]

---

## Related Records

- **Source benchmark report:** `core-component-00/benchmarks/retrieval-augmented-generation/2026-08-16-retrieval-augmented-generation-enterprise-assessment/enterprise-assessment.md`
- **Backlog items for this layer:** `core-component-00/remediation/README.md` § Remediation Backlog (RAG R3–R5)
