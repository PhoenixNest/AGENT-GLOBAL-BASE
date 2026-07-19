# Candidate Evaluation — Amina Yusuf

| Field                 | Value                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------- |
| **Candidate**         | Amina Yusuf                                                                              |
| **Role**              | Senior Research Engineer II — Multi-Agent Engineering                                    |
| **Level**             | L3                                                                                       |
| **Tier Floor**        | 17/20 minimum to pass                                                                    |
| **Vetting Authority** | CHRO + Dr. Vance + Dr. Nwosu-Chen (Research Scientist) + Dr. Wieczorek (Safety Engineer) |
| **Pipeline**          | [`company/pipeline/recruitment/pipeline.md`](../../../pipeline/recruitment/pipeline.md)  |
| **Date Opened**       | 2026-07-03                                                                               |
| **Date Closed**       | 2026-07-03                                                                               |
| **Decision**          | Hired                                                                                    |

---

## Stage Scorecard

| Stage | Name                         | Score    | Pass/Fail | Reviewer      | Notes                                                                                          |
| ----- | ---------------------------- | -------- | --------- | ------------- | ---------------------------------------------------------------------------------------------- |
| 1     | Resume Screen                | Pass     | Pass      | CHRO          | Distributed systems engineer, Google (agent-fleet scaling team)                                |
| 2     | Async Skills Challenge       | 18/20    | Pass      | Dr. Farouk    | Fleet-scaling design exercise: multi-fleet isolation under load                                |
| 3     | Technical Interview Round 1  | 18/20    | Pass      | Dr. Farouk    | Deep on `fleet_id` scoping and cross-fleet state leakage prevention                            |
| 4     | Technical Interview Round 2  | 18/20    | Pass      | Dr. Wieczorek | Adversarial scenario: probed for swarm-orchestration failure modes under partial observability |
| 5     | System Design / Architecture | 18/20    | Pass      | Dr. Vance     | Resilience design: proposed failover pattern for orchestrator-agent loss mid-task              |
| 6     | Values & Culture Interview   | 18/20    | Pass      | CHRO          | Strong collaborative signal working alongside an existing module owner                         |
| 7     | Secondary Officer Review     | Approved | Pass      | CHRO          | No conflicts flagged                                                                           |
| 8     | Reference Check              | Pass     | Pass      | CHRO          | Clear                                                                                          |
| 9     | Offer & Acceptance           | Accepted | Pass      | CHRO + CEO    | Accepted at L3 band                                                                            |

**Composite Score:** 18 / 20

---

## Strengths

- Production experience scaling agent fleets at Google — directly complements Farouk's swarm-orchestration ownership
- Strong on failure-mode thinking (orchestrator loss, partial observability) — closes the bus-factor gap with genuine resilience depth, not just headcount
- Adversarial interview performance under Dr. Wieczorek's questioning suggests good instincts for the safety-conscious culture this expansion is building

## Honest Gaps

- No prior context-handoff protocol design experience; will co-own `swarm_orchestrator.py` alongside Farouk first, ramping into `handoff_packet.py` after 90 days
- Has not worked in a research-lab setting before (enterprise background); onboarding includes explicit context on the lab's research-programme culture

---

## Decision Record

| Field           | Value                                                                            |
| --------------- | -------------------------------------------------------------------------------- |
| **Decision**    | Hired                                                                            |
| **Final Score** | 18 / 20                                                                          |
| **Decided By**  | CHRO + CEO                                                                       |
| **Date**        | 2026-07-03                                                                       |
| **Offer Terms** | Level L3 · Senior band · Start immediate                                         |
| **Notes**       | Reports to Dr. Idris Farouk, not Dr. Vance directly, per v1.3 reporting-line fix |

---

## Amendment (2026-07-03) — Leadership Signal Correction

**Original composite score: 18/20** (Impact 4, Craft 5, Leadership 4, Standards 5).

Per CHRO's Stage 9 audit finding (`hiring-outcome-report.md`) and the resulting evidence
requirement added to `vet-candidate.md`, the Leadership Signal score was re-reviewed. This
candidate's documented background is individual-contributor fleet-scaling work at Google; nothing
in the record establishes she grew or led others.

**Corrected Leadership Signal: 2/5 — "not established."** Corrected composite score: **16/20.**

This falls below the L3 tier floor (17/20) as a retroactive recalculation. Per CHRO's explicit
governance ruling (see `hiring-outcome-report.md` § Amendment), this does **not** reopen the hire:
the Stage 5 pass gate is dimension-count based and is cleared independently on Impact, Craft, and
Standards. The sum-floor table is a screening heuristic, not the pass/fail logic itself, and does
not retroactively un-pass a candidate whose Stage 9 approval and offer acceptance are already
final. **Decision stands: Hired.**
