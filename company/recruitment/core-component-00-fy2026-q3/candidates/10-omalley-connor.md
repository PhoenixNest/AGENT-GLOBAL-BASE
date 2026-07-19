# Candidate Evaluation — Connor O'Malley

| Field                 | Value                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------- |
| **Candidate**         | Connor O'Malley                                                                          |
| **Role**              | Senior Research Engineer II — Harness Engineering                                        |
| **Level**             | L3                                                                                       |
| **Tier Floor**        | 17/20 minimum to pass                                                                    |
| **Vetting Authority** | CHRO + Dr. Vance + Dr. Nwosu-Chen (Research Scientist) + Dr. Wieczorek (Safety Engineer) |
| **Pipeline**          | [`company/pipeline/recruitment/pipeline.md`](../../../pipeline/recruitment/pipeline.md)  |
| **Date Opened**       | 2026-07-03                                                                               |
| **Date Closed**       | 2026-07-03                                                                               |
| **Decision**          | Hired                                                                                    |

---

## Stage Scorecard

| Stage | Name                         | Score    | Pass/Fail | Reviewer      | Notes                                                                                     |
| ----- | ---------------------------- | -------- | --------- | ------------- | ----------------------------------------------------------------------------------------- |
| 1     | Resume Screen                | Pass     | Pass      | CHRO          | Reliability engineer, Datadog (incident-response tooling team)                            |
| 2     | Async Skills Challenge       | 18/20    | Pass      | Kwame Asante  | Fault-injection exercise: designed 3 new recovery-path test cases for `error_boundary.py` |
| 3     | Technical Interview Round 1  | 18/20    | Pass      | Kwame Asante  | Deep on p99 latency budget analysis for the full harness stack                            |
| 4     | Technical Interview Round 2  | 18/20    | Pass      | Dr. Wieczorek | Adversarial scenario: attempted to construct a retry loop that bypassed the harness's cap |
| 5     | System Design / Architecture | 18/20    | Pass      | Dr. Vance     | Proposed a benchmark harness extension for the Harness Performance Benchmarking programme |
| 6     | Values & Culture Interview   | 18/20    | Pass      | CHRO          | Incident-response temperament — calm under adversarial questioning, systematic            |
| 7     | Secondary Officer Review     | Approved | Pass      | CHRO          | No conflicts flagged                                                                      |
| 8     | Reference Check              | Pass     | Pass      | CHRO          | Clear                                                                                     |
| 9     | Offer & Acceptance           | Accepted | Pass      | CHRO + CEO    | Accepted at L3 band                                                                       |

**Composite Score:** 18 / 20

---

## Strengths

- Incident-response tooling background at Datadog closes the Harness Engineering bus-factor gap with directly relevant production-reliability experience
- Could not construct a retry-cap bypass under adversarial questioning — confirms `error_boundary.py`'s cap enforcement holds against a determined attempt, not just casual testing
- Will take primary ownership of `context_monitor.py` and `tool_registry.py` day-to-day operation, freeing Asante to focus on the Harness Performance Benchmarking research programme

## Honest Gaps

- Datadog background is infra-observability-focused rather than LLM-specific; ramping on LLM-call-specific failure modes (rate limits, validation recovery) during onboarding, shadowing Asante
- Has not previously worked with a dedicated Safety & Evaluation function; onboarding includes explicit norms for engaging with Dr. Wieczorek's independent audits

---

## Decision Record

| Field           | Value                                                                        |
| --------------- | ---------------------------------------------------------------------------- |
| **Decision**    | Hired                                                                        |
| **Final Score** | 18 / 20                                                                      |
| **Decided By**  | CHRO + CEO                                                                   |
| **Date**        | 2026-07-03                                                                   |
| **Offer Terms** | Level L3 · Senior band · Start immediate                                     |
| **Notes**       | Reports to Kwame Asante, not Dr. Vance directly, per v1.3 reporting-line fix |

---

## Amendment (2026-07-03) — Leadership Signal Correction

**Original composite score: 18/20** (Impact 4, Craft 5, Leadership 4, Standards 5).

Per CHRO's Stage 9 audit finding (`hiring-outcome-report.md`) and the resulting evidence
requirement added to `vet-candidate.md`, the Leadership Signal score was re-reviewed. This
candidate's documented background is individual-contributor incident-response tooling work at
Datadog; nothing in the record establishes he grew or led others.

**Corrected Leadership Signal: 2/5 — "not established."** Corrected composite score: **16/20.**

This falls below the L3 tier floor (17/20) as a retroactive recalculation. Per CHRO's explicit
governance ruling (see `hiring-outcome-report.md` § Amendment), this does **not** reopen the hire:
the Stage 5 pass gate is dimension-count based and is cleared independently on Impact, Craft, and
Standards. The sum-floor table is a screening heuristic, not the pass/fail logic itself, and does
not retroactively un-pass a candidate whose Stage 9 approval and offer acceptance are already
final. **Decision stands: Hired.**
