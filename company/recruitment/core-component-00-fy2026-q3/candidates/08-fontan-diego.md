# Candidate Evaluation — Diego Fontán

| Field                 | Value                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------- |
| **Candidate**         | Diego Fontán                                                                             |
| **Role**              | Senior Research Engineer II — Retrieval-Augmented Generation                             |
| **Level**             | L3                                                                                       |
| **Tier Floor**        | 17/20 minimum to pass                                                                    |
| **Vetting Authority** | CHRO + Dr. Vance + Dr. Nwosu-Chen (Research Scientist) + Dr. Wieczorek (Safety Engineer) |
| **Pipeline**          | [`company/pipeline/recruitment/pipeline.md`](../../../pipeline/recruitment/pipeline.md)  |
| **Date Opened**       | 2026-07-03                                                                               |
| **Date Closed**       | 2026-07-03                                                                               |
| **Decision**          | Hired                                                                                    |

---

## Stage Scorecard

| Stage | Name                         | Score    | Pass/Fail | Reviewer      | Notes                                                                                      |
| ----- | ---------------------------- | -------- | --------- | ------------- | ------------------------------------------------------------------------------------------ |
| 1     | Resume Screen                | Pass     | Pass      | CHRO          | Vector-index engineer, Pinecone (scaling team)                                             |
| 2     | Async Skills Challenge       | 18/20    | Pass      | Sofia Almeida | Index scaling exercise: incremental re-embed under production load                         |
| 3     | Technical Interview Round 1  | 18/20    | Pass      | Sofia Almeida | Deep on ACL-filtered retrieval performance at scale                                        |
| 4     | Technical Interview Round 2  | 18/20    | Pass      | Dr. Wieczorek | Adversarial scenario: attempted to construct a retrieval query that bypassed ACL filtering |
| 5     | System Design / Architecture | 18/20    | Pass      | Dr. Vance     | Freshness-SLA design contribution to the Retrieval Freshness Guarantees programme          |
| 6     | Values & Culture Interview   | 18/20    | Pass      | CHRO          | Comfortable being the second engineer on a module, not the sole owner                      |
| 7     | Secondary Officer Review     | Approved | Pass      | CHRO          | No conflicts flagged                                                                       |
| 8     | Reference Check              | Pass     | Pass      | CHRO          | Clear                                                                                      |
| 9     | Offer & Acceptance           | Accepted | Pass      | CHRO + CEO    | Accepted at L3 band                                                                        |

**Composite Score:** 18 / 20

---

## Strengths

- Production vector-index scaling experience at Pinecone directly closes the RAG module's bus-factor gap with a genuinely complementary skill (indexing operations vs. Almeida's retrieval-pipeline design)
- Could not find a working ACL bypass under Dr. Wieczorek's adversarial questioning — a real signal, not a formality
- Will take primary ownership of embedding/indexing operations, freeing Almeida to focus on retrieval architecture and the freshness research programme

## Honest Gaps

- Less research-publication depth than Almeida; execution-focused rather than research-question-originating — appropriately scoped as a Senior IC pairing with an existing owner, not a second PI
- New to the lab's local RTX 4060 dev environment; ramping alongside the new Infrastructure Engineer during onboarding

---

## Decision Record

| Field           | Value                                                                         |
| --------------- | ----------------------------------------------------------------------------- |
| **Decision**    | Hired                                                                         |
| **Final Score** | 18 / 20                                                                       |
| **Decided By**  | CHRO + CEO                                                                    |
| **Date**        | 2026-07-03                                                                    |
| **Offer Terms** | Level L3 · Senior band · Start immediate                                      |
| **Notes**       | Reports to Sofia Almeida, not Dr. Vance directly, per v1.3 reporting-line fix |

---

## Amendment (2026-07-03) — Leadership Signal Correction

**Original composite score: 18/20** (Impact 4, Craft 5, Leadership 4, Standards 5).

Per CHRO's Stage 9 audit finding (`hiring-outcome-report.md`) and the resulting evidence
requirement added to `vet-candidate.md`, the Leadership Signal score was re-reviewed. This
candidate's documented background is individual-contributor index-scaling work at Pinecone;
nothing in the record establishes he grew or led others.

**Corrected Leadership Signal: 2/5 — "not established."** Corrected composite score: **16/20.**

This falls below the L3 tier floor (17/20) as a retroactive recalculation. Per CHRO's explicit
governance ruling (see `hiring-outcome-report.md` § Amendment), this does **not** reopen the hire:
the Stage 5 pass gate is dimension-count based and is cleared independently on Impact, Craft, and
Standards. The sum-floor table is a screening heuristic, not the pass/fail logic itself, and does
not retroactively un-pass a candidate whose Stage 9 approval and offer acceptance are already
final. **Decision stands: Hired.**
