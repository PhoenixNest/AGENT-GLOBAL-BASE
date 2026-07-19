# Candidate Evaluation — Hana Kobayashi

| Field                 | Value                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------- |
| **Candidate**         | Hana Kobayashi                                                                           |
| **Role**              | Senior Research Engineer II — Context Engineering                                        |
| **Level**             | L3                                                                                       |
| **Tier Floor**        | 17/20 minimum to pass                                                                    |
| **Vetting Authority** | CHRO + Dr. Vance + Dr. Nwosu-Chen (Research Scientist) + Dr. Wieczorek (Safety Engineer) |
| **Pipeline**          | [`company/pipeline/recruitment/pipeline.md`](../../../pipeline/recruitment/pipeline.md)  |
| **Date Opened**       | 2026-07-03                                                                               |
| **Date Closed**       | 2026-07-03                                                                               |
| **Decision**          | Hired                                                                                    |

---

## Stage Scorecard

| Stage | Name                         | Score    | Pass/Fail | Reviewer      | Notes                                                                                    |
| ----- | ---------------------------- | -------- | --------- | ------------- | ---------------------------------------------------------------------------------------- |
| 1     | Resume Screen                | Pass     | Pass      | CHRO          | Memory-systems engineer, OpenAI (long-running assistant memory team)                     |
| 2     | Async Skills Challenge       | 17/20    | Pass      | Mei-Ling Zhao | Memory-tier scaling exercise: episodic-to-semantic promotion under high session volume   |
| 3     | Technical Interview Round 1  | 17/20    | Pass      | Mei-Ling Zhao | Deep on working-memory eviction policy design                                            |
| 4     | Technical Interview Round 2  | 17/20    | Pass      | Dr. Wieczorek | Adversarial scenario: probed for memory-poisoning via crafted episodic entries           |
| 5     | System Design / Architecture | 17/20    | Pass      | Dr. Vance     | Contributed a scaling proposal for `memory_store.py` under concurrent multi-agent access |
| 6     | Values & Culture Interview   | 17/20    | Pass      | CHRO          | Solid, methodical; slightly less assertive than other Phase 3 candidates but consistent  |
| 7     | Secondary Officer Review     | Approved | Pass      | CHRO          | No conflicts flagged                                                                     |
| 8     | Reference Check              | Pass     | Pass      | CHRO          | Clear                                                                                    |
| 9     | Offer & Acceptance           | Accepted | Pass      | CHRO + CEO    | Accepted at L3 band                                                                      |

**Composite Score:** 17 / 20

---

## Strengths

- Production memory-systems experience at OpenAI closes the Context Engineering bus-factor gap with a directly relevant background
- Identified a real memory-poisoning attack surface during the adversarial interview that the lab had not previously documented — immediate, concrete value
- Will take primary ownership of `memory_store.py` scaling and concurrent-access safety, freeing Zhao to focus on the Context Compression Theory and Multi-Agent Memory Coherence programmes

## Honest Gaps

- Cleared the floor without margin (17/20, exactly at the L3 tier floor) — approved, not flagged for conditions, but this is the tightest pass of the Phase 3 cohort and worth noting for the record rather than glossing over
- Less experience with compression/summarization specifically; Zhao retains lead on `context_compressor.py`

---

## Decision Record

| Field           | Value                                                                         |
| --------------- | ----------------------------------------------------------------------------- |
| **Decision**    | Hired                                                                         |
| **Final Score** | 17 / 20                                                                       |
| **Decided By**  | CHRO + CEO                                                                    |
| **Date**        | 2026-07-03                                                                    |
| **Offer Terms** | Level L3 · Senior band · Start immediate                                      |
| **Notes**       | Reports to Mei-Ling Zhao, not Dr. Vance directly, per v1.3 reporting-line fix |

---

## Amendment (2026-07-03) — Leadership Signal Correction

**Original composite score: 17/20** (Impact 4, Craft 4, Leadership 4, Standards 5).

Per CHRO's Stage 9 audit finding (`hiring-outcome-report.md`) and the resulting evidence
requirement added to `vet-candidate.md`, the Leadership Signal score was re-reviewed. This
candidate's documented background is individual-contributor memory-systems work at OpenAI; nothing
in the record establishes she grew or led others.

**Corrected Leadership Signal: 2/5 — "not established."** Corrected composite score: **15/20.**

This falls below the L3 tier floor (17/20) as a retroactive recalculation — the largest gap in the
Phase 3 cohort, since this file was already an exact-floor pass before correction. Per CHRO's
explicit governance ruling (see `hiring-outcome-report.md` § Amendment), this does **not** reopen
the hire: the Stage 5 pass gate is dimension-count based and is cleared independently on Impact,
Craft, and Standards. The sum-floor table is a screening heuristic, not the pass/fail logic
itself, and does not retroactively un-pass a candidate whose Stage 9 approval and offer acceptance
are already final. **Decision stands: Hired.**
