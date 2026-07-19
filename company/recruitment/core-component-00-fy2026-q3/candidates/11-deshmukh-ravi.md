# Candidate Evaluation — Ravi Deshmukh

| Field                 | Value                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------- |
| **Candidate**         | Ravi Deshmukh                                                                            |
| **Role**              | Infrastructure Engineer                                                                  |
| **Level**             | L3                                                                                       |
| **Tier Floor**        | 17/20 minimum to pass                                                                    |
| **Vetting Authority** | CHRO + Dr. Vance + Dr. Nwosu-Chen (Research Scientist) + Dr. Wieczorek (Safety Engineer) |
| **Pipeline**          | [`company/pipeline/recruitment/pipeline.md`](../../../pipeline/recruitment/pipeline.md)  |
| **Date Opened**       | 2026-07-03                                                                               |
| **Date Closed**       | 2026-07-03                                                                               |
| **Decision**          | Hired                                                                                    |

---

## Stage Scorecard

| Stage | Name                         | Score    | Pass/Fail | Reviewer      | Notes                                                                                               |
| ----- | ---------------------------- | -------- | --------- | ------------- | --------------------------------------------------------------------------------------------------- |
| 1     | Resume Screen                | Pass     | Pass      | CHRO          | MLOps engineer, Hugging Face (research infra team)                                                  |
| 2     | Async Skills Challenge       | 17/20    | Pass      | Dr. Vance     | Dev-environment provisioning exercise: reproducible GPU/dependency setup across Windows + CUDA      |
| 3     | Technical Interview Round 1  | 17/20    | Pass      | Sofia Almeida | Deep on RAG module's `requirements.txt` footprint and spaCy model management                        |
| 4     | Technical Interview Round 2  | 17/20    | Pass      | Dr. Wieczorek | Adversarial scenario: probed dependency-supply-chain risk in the RAG deployment stack               |
| 5     | System Design / Architecture | 17/20    | Pass      | Dr. Vance     | Proposed CI-for-research pattern: automated `pytest` runs per module on every implementation change |
| 6     | Values & Culture Interview   | 17/20    | Pass      | CHRO          | Service-oriented; explicitly framed the role as "unblocking research," not owning research itself   |
| 7     | Secondary Officer Review     | Approved | Pass      | CHRO          | No conflicts flagged                                                                                |
| 8     | Reference Check              | Pass     | Pass      | CHRO          | Clear                                                                                               |
| 9     | Offer & Acceptance           | Accepted | Pass      | CHRO + CEO    | Accepted at L3 band                                                                                 |

**Composite Score:** 17 / 20

---

## Strengths

- Direct precedent managing GPU/dependency-heavy research infrastructure at Hugging Face — exactly the profile needed for CC-00's RTX 4060 dev environment and RAG's heavy footprint
- Correctly scoped the role as lab-dedicated infrastructure, distinct from R&D's parent-company DevOps/SRE bench, without prompting — independently arrived at the same conclusion the CEO's clarification confirmed
- Proposed CI-for-research (automated per-module `pytest` on every implementation change) — a concrete improvement over the current manual per-module test-running convention

## Honest Gaps

- Cleared the floor without margin (17/20) — the tightest pass alongside Kobayashi's; approved on strength of directly relevant experience, not composite score cushion
- No prior LLM research-lab experience specifically (came from a broader ML infra role); onboarding includes shadowing all four module owners to understand module-specific dependency needs before making infra changes unilaterally

---

## Decision Record

| Field           | Value                                                                                     |
| --------------- | ----------------------------------------------------------------------------------------- |
| **Decision**    | Hired                                                                                     |
| **Final Score** | 17 / 20                                                                                   |
| **Decided By**  | CHRO + CEO                                                                                |
| **Date**        | 2026-07-03                                                                                |
| **Offer Terms** | Level L3 · Senior band · Start immediate                                                  |
| **Notes**       | Reports to Dr. Vance directly — cross-cutting role, not paired with a single module owner |

---

## Amendment (2026-07-03) — Leadership Signal Correction

**Original composite score: 17/20** (Impact 4, Craft 4, Leadership 4, Standards 5).

Per CHRO's Stage 9 audit finding (`hiring-outcome-report.md`) and the resulting evidence
requirement added to `vet-candidate.md`, the Leadership Signal score was re-reviewed. This
candidate's documented background is individual-contributor infrastructure support work at
Hugging Face ("supported the research infrastructure team"); nothing in the record establishes he
grew or led others.

**Corrected Leadership Signal: 2/5 — "not established."** Corrected composite score: **15/20.**

This falls below the L3 tier floor (17/20) as a retroactive recalculation — the largest gap in the
Phase 3 cohort alongside Kobayashi's, since this file was also an exact-floor pass before
correction. Per CHRO's explicit governance ruling (see `hiring-outcome-report.md` § Amendment),
this does **not** reopen the hire: the Stage 5 pass gate is dimension-count based and is cleared
independently on Impact, Craft, and Standards. The sum-floor table is a screening heuristic, not
the pass/fail logic itself, and does not retroactively un-pass a candidate whose Stage 9 approval
and offer acceptance are already final. **Decision stands: Hired.**
