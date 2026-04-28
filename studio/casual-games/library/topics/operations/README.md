# Production Bandwidth Monitoring Framework

> **Owner:** Marcus Tran-Yoshida (CPO)
> **Trigger:** Stage 2 and Stage 3 Gate Reviews
> **Participants:** CPO, Executive Producer (James Okonkwo), Studio Director (Marcus Vogel), Producer (James Mitchell), Associate Producer (Lena Müller)
> **Version:** 1.1
> **Date:** 2026-04-12

---

## 1. Executive Summary

This framework is created in direct response to **CPO Audit Condition CR-3**, which identified that **2 FTEs (James Mitchell + Lena Müller) supporting 33 individual contributors across all studio disciplines is a stretched configuration**. While James Mitchell's 12 years of senior production experience and Lena Müller's 3 years of associate-level execution competence provide a solid foundation, the ratio of 1 producer per 16.5 ICs exceeds industry norms for game development, where 1:10–1:12 is considered sustainable for coordinated multi-platform delivery.

**Purpose:** Establish a monitoring framework with clear velocity metrics, escalation triggers, and a pre-defined hiring plan for a third producer. This ensures production capacity degradation is detected early and addressed before it impacts Stage 5 content delivery or Stage 8 soft-launch timelines.

**Risk if unmonitored:** Production bottlenecks manifest as delayed sprint deliveries, increasing carryover rates, and producer burnout. By the time these symptoms are visible at Stage 5, the critical path is already compromised and a new producer cannot be onboarded fast enough to recover the schedule.

---

## 2. Current Production Staffing

| Name               | Role               | Seniority      | Experience | Vetting Score | Primary Responsibilities                                                               |
| ------------------ | ------------------ | -------------- | ---------- | ------------- | -------------------------------------------------------------------------------------- |
| **James Mitchell** | Producer           | Senior (L2)    | 12 years   | 16/20         | Sprint planning, cross-functional coordination, risk management, stakeholder reporting |
| **Lena Müller**    | Associate Producer | Mid-Level (L1) | 3 years    | 16/20         | Task tracking, meeting facilitation, documentation, dependency management              |

### Oversight Structure

| Name              | Role               | Production Support                                                                                       |
| ----------------- | ------------------ | -------------------------------------------------------------------------------------------------------- |
| **James Okonkwo** | Executive Producer | Senior oversight — reviews production health weekly, escalates to CPO/Studio Director when triggers fire |
| **Marcus Vogel**  | Studio Director    | Owns Stage 3/5/8 deliverables; shares production load during peak delivery phases; co-signs gate reviews |

### Staffing Assessment

| Metric                      | Current   | Industry Norm    | Status                     |
| --------------------------- | --------- | ---------------- | -------------------------- |
| Producers (FTE)             | 2         | 3–4 (for 33 ICs) | ⚠️ Understaffed            |
| Producer:IC Ratio           | 1:16.5    | 1:10–1:12        | ⚠️ Above sustainable       |
| Senior Producer Coverage    | 1 (James) | 1–2              | ✅ Adequate for now        |
| Associate Producer Coverage | 1 (Lena)  | 1–2              | ⚠️ Single point of failure |

---

## 3. Velocity Metrics to Monitor

The following metrics are tracked per sprint and reported to the Executive Producer weekly.

| Metric                            | Definition                                                                  | Target     | Yellow Flag                     | Orange Flag                     | Red Flag                         |
| --------------------------------- | --------------------------------------------------------------------------- | ---------- | ------------------------------- | ------------------------------- | -------------------------------- |
| **Sprint Completion Rate**        | % of committed story points completed within sprint                         | ≥ 85%      | < 80% for 2 consecutive sprints | < 75% for 2 consecutive sprints | < 70% for 2 consecutive sprints  |
| **Carryover Rate**                | % of story points carried to next sprint                                    | ≤ 15%      | —                               | > 25%                           | — (covered by sprint completion) |
| **Cycle Time**                    | Median days from "In Progress" to "Done" for standard tasks                 | ≤ 5 days   | > 6 days median                 | > 7 days median                 | > 8 days median                  |
| **Blocker Resolution Time**       | Median hours from blocker flagged to blocker resolved                       | ≤ 24 hours | > 36 hours median               | > 48 hours median               | > 72 hours median                |
| **Producer Capacity Utilization** | Self-assessed % of available working hours spent on production coordination | ≤ 80%      | > 85% for 2 consecutive weeks   | > 90% for 3 consecutive weeks   | > 95% (any week)                 |

### Metric Calculation Notes

- **Sprint Completion Rate:** `Completed Story Points / Committed Story Points × 100`. Excludes points removed via scope change (tracked separately).
- **Carryover Rate:** `Carried-Over Story Points / Total Committed Story Points × 100`. High carryover indicates either over-commitment or production bottlenecks.
- **Cycle Time:** Calculated from Jira/board data. "Standard tasks" = 3–8 story point items. Excludes spikes and research tasks.
- **Blocker Resolution Time:** Calculated from the time a blocker tag is applied to the time it is removed. Includes weekends.
- **Producer Capacity Utilization:** Self-reported by James Mitchell and Lena Müller weekly. Calculated as `(Hours spent on production coordination) / (Total available working hours) × 100`. Includes meetings, Slack/async coordination, documentation, and unblocking work.

---

## 3a. Baseline Data Collection Plan

Baseline data collection begins at **Stage 2 entry (first sprint)**. Since this is a new studio with no prior sprint history, historical baselines are not available. All initial baseline fields will be populated during the first sprint cycle and will serve as the reference point for all subsequent trend analysis.

### Initial Baseline Fields (TBD — to be populated during Sprint 1)

| Metric                        | Baseline Value | Collection Date | Notes                                                                            |
| ----------------------------- | -------------- | --------------- | -------------------------------------------------------------------------------- |
| Sprint Completion Rate        | TBD            | End of Sprint 1 | First sprint may show volatility; document scope clarity and estimation accuracy |
| Carryover Rate                | TBD            | End of Sprint 1 | Expect higher carryover in Sprint 1 due to team calibration                      |
| Cycle Time                    | TBD            | End of Sprint 1 | Baseline median across all standard tasks (3–8 SP)                               |
| Blocker Resolution Time       | TBD            | End of Sprint 1 | Baseline median from blocker flag to resolution                                  |
| Producer Capacity Utilization | TBD            | End of Sprint 1 | Self-reported by James Mitchell and Lena Müller separately                       |

### Data Collection Method

- **Primary Source:** Jira/Confluence automated reporting — sprint burndown, cycle time histograms, blocker aging reports
- **Supplementary:** Weekly production health summary (manual compilation by Producer, reviewed by Executive Producer)
- **Baseline Lock:** Initial baseline values are locked at the end of Sprint 1. Subsequent sprints are compared against this baseline for trend direction (improving / stable / degrading).

### Historical Data Status

| Data Source                         | Available? | Notes                                                 |
| ----------------------------------- | ---------- | ----------------------------------------------------- |
| Prior sprint velocity               | ❌ No      | New studio — no prior sprints exist                   |
| Historical carryover patterns       | ❌ No      | First sprint will establish the pattern               |
| Historical cycle time               | ❌ No      | First sprint will establish the pattern               |
| Historical blocker resolution       | ❌ No      | First sprint will establish the pattern               |
| Prior producer capacity utilization | ❌ No      | First self-reporting cycle will establish the pattern |

**CPO Directive:** Do not attempt to backfill or estimate historical baselines. The first sprint's data is the only valid starting point. Trend analysis becomes meaningful from Sprint 3 onward (minimum 3 data points for directionality).

---

## 4. Monitoring Cadence

| Cadence          | Activity                          | Participants                               | Output                                                       |
| ---------------- | --------------------------------- | ------------------------------------------ | ------------------------------------------------------------ |
| **Weekly**       | Sprint metrics review             | Producer → Executive Producer              | Weekly production health summary (metrics table + narrative) |
| **Bi-weekly**    | Capacity utilization check        | Producer self-assessment                   | Capacity scorecard (James + Lena separately)                 |
| **Stage 2 Gate** | Formal production capacity review | CPO + Executive Producer + Studio Director | Gate review checklist (Section 7a)                           |
| **Stage 3 Gate** | Formal production capacity review | CPO + Executive Producer + Studio Director | Gate review checklist (Section 7b)                           |

### Weekly Production Health Summary Template

```
Week Ending: [date]
Sprint: [number]

METRICS:
- Sprint Completion Rate: [X]% (Target: ≥ 85%)
- Carryover Rate: [X]% (Target: ≤ 15%)
- Cycle Time (median): [X] days (Target: ≤ 5)
- Blocker Resolution Time (median): [X] hours (Target: ≤ 24)
- Producer Capacity — James Mitchell: [X]% (Target: ≤ 80%)
- Producer Capacity — Lena Müller: [X]% (Target: ≤ 80%)

FLAG STATUS: [None / Yellow / Orange / Red]
NARRATIVE: [2–3 sentences on trends, blockers, and concerns]
ACTION ITEMS: [List with owner + due date]
```

---

## 5. Escalation Triggers

### 🟡 Yellow Flag — Monitor Closely

**Trigger Conditions (any one):**

- Sprint completion rate < 80% for 2 consecutive sprints
- Producer capacity utilization > 85% for 2 consecutive weeks (either James or Lena)

**Required Actions:**

1. Executive Producer conducts 1:1 with both producers to identify root causes
2. Review sprint commitment patterns — are we over-committing?
3. Identify tasks that can be deferred or delegated to non-production staff
4. Increase monitoring frequency: capacity utilization checked weekly instead of bi-weekly
5. Document in weekly production health summary with explicit Yellow Flag notation

### 🟠 Orange Flag — Prepare 3rd Producer

**Trigger Conditions (any one):**

- Sprint completion rate < 75% for 2 consecutive sprints
- Producer capacity utilization > 90% for 3 consecutive weeks (either James or Lena)
- Carryover rate > 25% in a single sprint

**Required Actions:**

1. All Yellow Flag actions, plus:
2. Executive Producer notifies CPO and Studio Director of potential hire need
3. Studio Director drafts 3rd producer job description (Section 6 profile)
4. Executive Producer contacts CHRO (Dr. Evelyn Hartwell) to initiate recruitment pipeline
5. CPO reviews and approves recruitment requisition
6. Interim mitigation: Studio Director (Marcus Vogel) absorbs overflow production coordination
7. Document in weekly production health summary with explicit Orange Flag notation

### 🔴 Red Flag — Hire 3rd Producer Immediately

**Trigger Conditions (any one):**

- Sprint completion rate < 70% for 2 consecutive sprints
- Producer capacity utilization > 95% for any single week (either James or Lena)
- Critical path tasks delayed > 1 week due to production coordination gaps

**Required Actions:**

1. All Orange Flag actions, plus:
2. CHRO fast-tracks recruitment (4–5 week SLA, non-negotiable)
3. Studio Director immediately redistributes production load: takes on Stage 5 content production coordination directly
4. CPO convenes emergency production review within 48 hours
5. If current sprint is at risk, CPO authorizes scope deferral of non-critical-path items (documented as P2/P3 deferrals, not scope removal)
6. Document in weekly production health summary with explicit Red Flag notation and escalation timestamp

---

## 6. Third Producer Profile (If Triggered)

| Attribute               | Specification                                                                                                  |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Role**                | Producer                                                                                                       |
| **Seniority**           | Senior (L2) — same level as James Mitchell                                                                     |
| **Compensation Band**   | $110K – $150K (matches James Mitchell's band)                                                                  |
| **Experience Required** | 8+ years game production, shipped at least 2 mobile titles, experience with agile/scrum at team scale > 20 ICs |
| **Hiring Timeline**     | 4–5 weeks (standard CHRO SLA for senior production roles)                                                      |
| **Onboarding Timeline** | 2 weeks to full productivity (shadowing James Mitchell during first sprint)                                    |

### Scope Assignment for 3rd Producer

| Responsibility                                 | Owner After Hire                                |
| ---------------------------------------------- | ----------------------------------------------- |
| Sprint planning & backlog grooming (core team) | James Mitchell                                  |
| Task tracking & documentation                  | Lena Müller                                     |
| **Stage 5 content production coordination**    | **3rd Producer (new)**                          |
| Cross-functional dependency management         | Shared (James + 3rd Producer)                   |
| Stakeholder reporting                          | James Mitchell (consolidates from 3rd Producer) |
| Risk management                                | Shared (James + 3rd Producer)                   |

**Rationale:** Stage 5 (Development) is the highest-risk phase for production overload — it involves the largest number of active ICs (33), the most concurrent workstreams (Android, iOS, cross-platform, backend, art, audio), and the longest continuous execution window. Assigning the 3rd Producer to Stage 5 content production directly addresses the bottleneck where it matters most.

---

## 6a. Single Point of Failure Mitigation

Lena Müller is currently the sole Associate Producer supporting all 33 ICs across the studio. Her departure or reassignment would create an immediate coordination vacuum, removing James Mitchell's primary execution support and overloading a already-stretched production function. This section defines the risk and three-tier mitigation strategy.

### Risk Assessment

| Risk                                                          | Impact                                                                                                                                                     | Probability | Severity    |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ----------- |
| Lena Müller departs or is reassigned before 3rd producer hire | James Mitchell loses task tracking, meeting facilitation, documentation, and dependency management support; production coordination capacity drops by ~40% | Low–Medium  | 🔴 Critical |

### Mitigation A: Cross-Train a Junior IC (Stopgap)

| Detail               | Specification                                                                                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Action**           | Cross-train a junior individual contributor to handle 10% of production coordination workload                                                                                         |
| **Recommended Role** | Economy Designer or Level Designer — roles with natural adjacency to production task flow and sprint-level visibility                                                                 |
| **Scope**            | Limited to: task status updates in Jira, meeting note-taking and action item tracking, dependency flagging to James Mitchell                                                          |
| **Duration**         | Stopgap only — valid until 3rd producer is onboarded OR Mitigation C is activated                                                                                                     |
| **Owner**            | James Mitchell (designates and trains the junior IC)                                                                                                                                  |
| **Rationale**        | This does not replace an Associate Producer. It provides minimal continuity for low-complexity coordination tasks so James Mitchell is not suddenly absorbing Lena's entire workload. |

### Mitigation B: Document All Associate Producer SOPs

| Detail                        | Specification                                                                                                                                                                 |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Action**                    | Lena Müller maintains a comprehensive Associate Producer runbook covering all standard operating procedures                                                                   |
| **Required Contents**         |                                                                                                                                                                               |
| — Task tracking templates     | Jira board structures, sprint grooming checklists, burndown reporting formats                                                                                                 |
| — Meeting facilitation guides | Standup, sprint planning, retrospective, and cross-functional sync agendas with timeboxes                                                                                     |
| — Stakeholder update formats  | Weekly production health summary template (Section 4), escalation notification formats, status report structures                                                              |
| — Jira workflow standards     | Tag conventions, blocker lifecycle, story point estimation guidelines, carryover documentation process                                                                        |
| **Maintenance Cadence**       | Updated bi-weekly; reviewed by James Mitchell monthly                                                                                                                         |
| **Location**                  | `studio/casual-games/team/operations/ap-runbook/`                                                                                                                             |
| **Owner**                     | Lena Müller (author), James Mitchell (reviewer)                                                                                                                               |
| **Rationale**                 | If Lena departs, any replacement (internal or external) can onboard against documented procedures rather than tribal knowledge. This reduces ramp-up time from weeks to days. |

### Mitigation C: Fast-Track 3rd Producer Requisition

| Detail               | Specification                                                                                                                                                                                                                          |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Trigger**          | Lena Müller gives notice or is reassigned before 3rd producer hire is complete                                                                                                                                                         |
| **Action**           | Reduce 3rd producer recruitment timeline from 4–5 weeks to 3 weeks                                                                                                                                                                     |
| **Mechanism**        | Executive Producer requests expedited CHRO approval from Dr. Evelyn Hartwell, citing single-point-of-failure risk                                                                                                                      |
| **Interim Coverage** | Studio Director (Marcus Vogel) absorbs Lena's coordination load until 3rd producer starts; Mitigation A cross-trained IC provides supplemental support                                                                                 |
| **Owner**            | Executive Producer (initiates), CHRO (approves expedited timeline)                                                                                                                                                                     |
| **Rationale**        | A 3-week timeline is achievable for a senior production role when the job description is pre-drafted (Section 6) and the CHRO pipeline is already primed. This is the only sustainable replacement for an Associate Producer at scale. |

---

## 7. Gate Review Checklists

### 7a. Stage 2 Gate — Production Capacity Review Checklist

**Conducted by:** CPO + Executive Producer + Studio Director

| #   | Check Item                                                                    | Status        | Evidence / Notes |
| --- | ----------------------------------------------------------------------------- | ------------- | ---------------- |
| 1   | Current sprint completion rate reported                                       | ☐ Pass ☐ Fail |                  |
| 2   | Sprint completion rate ≥ 85% target (or acceptable variance documented)       | ☐ Pass ☐ Fail |                  |
| 3   | Current carryover rate reported                                               | ☐ Pass ☐ Fail |                  |
| 4   | Carryover rate ≤ 15% target (or acceptable variance documented)               | ☐ Pass ☐ Fail |                  |
| 5   | Current cycle time reported                                                   | ☐ Pass ☐ Fail |                  |
| 6   | Cycle time ≤ 5 days target (or acceptable variance documented)                | ☐ Pass ☐ Fail |                  |
| 7   | Current blocker resolution time reported                                      | ☐ Pass ☐ Fail |                  |
| 8   | Blocker resolution time ≤ 24 hours target (or acceptable variance documented) | ☐ Pass ☐ Fail |                  |
| 9   | Producer capacity utilization reported (James Mitchell)                       | ☐ Pass ☐ Fail |                  |
| 10  | Producer capacity utilization reported (Lena Müller)                          | ☐ Pass ☐ Fail |                  |
| 11  | Both producers at ≤ 80% capacity (or variance explained)                      | ☐ Pass ☐ Fail |                  |
| 12  | Trend analysis: metrics improving, stable, or degrading over last 4 sprints   | ☐ Pass ☐ Fail |                  |
| 13  | Escalation trigger status: None / Yellow / Orange / Red                       | ☐ Pass ☐ Fail |                  |
| 14  | Recommendation: Continue / Monitor / Prepare Hire / Hire Immediately          | ☐ Pass ☐ Fail |                  |

**Gate Decision:**

| Decision             | Criteria                                                                                      |
| -------------------- | --------------------------------------------------------------------------------------------- |
| **Pass**             | All checks passed, no flags active, or Yellow Flag with documented mitigation plan            |
| **Conditional Pass** | Yellow or Orange Flag active with documented mitigation plan and hiring timeline initiated    |
| **Fail**             | Red Flag active with no hiring timeline; production at risk of impacting Stage 3 deliverables |

**Sign-Off:**

| Participant         | Role               | Signature | Date |
| ------------------- | ------------------ | --------- | ---- |
| Marcus Tran-Yoshida | CPO                |           |      |
| James Okonkwo       | Executive Producer |           |      |
| Marcus Vogel        | Studio Director    |           |      |

---

### 7b. Stage 3 Gate — Production Capacity Review Checklist

**Conducted by:** CPO + Executive Producer + Studio Director

| #   | Check Item                                                                                                           | Status              | Evidence / Notes |
| --- | -------------------------------------------------------------------------------------------------------------------- | ------------------- | ---------------- |
| 1   | Current sprint completion rate reported                                                                              | ☐ Pass ☐ Fail       |                  |
| 2   | Sprint completion rate ≥ 85% target (or acceptable variance documented)                                              | ☐ Pass ☐ Fail       |                  |
| 3   | Current carryover rate reported                                                                                      | ☐ Pass ☐ Fail       |                  |
| 4   | Carryover rate ≤ 15% target (or acceptable variance documented)                                                      | ☐ Pass ☐ Fail       |                  |
| 5   | Current cycle time reported                                                                                          | ☐ Pass ☐ Fail       |                  |
| 6   | Cycle time ≤ 5 days target (or acceptable variance documented)                                                       | ☐ Pass ☐ Fail       |                  |
| 7   | Current blocker resolution time reported                                                                             | ☐ Pass ☐ Fail       |                  |
| 8   | Blocker resolution time ≤ 24 hours target (or acceptable variance documented)                                        | ☐ Pass ☐ Fail       |                  |
| 9   | Producer capacity utilization reported (James Mitchell)                                                              | ☐ Pass ☐ Fail       |                  |
| 10  | Producer capacity utilization reported (Lena Müller)                                                                 | ☐ Pass ☐ Fail       |                  |
| 11  | Both producers at ≤ 80% capacity (or variance explained)                                                             | ☐ Pass ☐ Fail       |                  |
| 12  | Trend analysis: metrics improving, stable, or degrading since Stage 2 gate                                           | ☐ Pass ☐ Fail       |                  |
| 13  | If 3rd producer was triggered at Stage 2: hire status reported (sourced / interviewing / offer extended / onboarded) | ☐ Pass ☐ Fail ☐ N/A |                  |
| 14  | Escalation trigger status: None / Yellow / Orange / Red                                                              | ☐ Pass ☐ Fail       |                  |
| 15  | Recommendation: Continue / Monitor / Prepare Hire / Hire Immediately                                                 | ☐ Pass ☐ Fail       |                  |
| 16  | Stage 5 production load assessment: can current team handle 33 ICs through Stage 5?                                  | ☐ Pass ☐ Fail       |                  |

**Gate Decision:**

| Decision             | Criteria                                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Pass**             | All checks passed, no flags active, or Yellow Flag with documented mitigation plan                           |
| **Conditional Pass** | Orange Flag active with hiring timeline underway; Stage 5 load assessment acceptable with interim mitigation |
| **Fail**             | Red Flag active; Stage 5 load assessment negative; production capacity insufficient for 33 ICs               |

**Sign-Off:**

| Participant         | Role               | Signature | Date |
| ------------------- | ------------------ | --------- | ---- |
| Marcus Tran-Yoshida | CPO                |           |      |
| James Okonkwo       | Executive Producer |           |      |
| Marcus Vogel        | Studio Director    |           |      |

---

## 8. Documentation & Tracking

| Artifact                                               | Location                                              | Owner                    | Update Frequency          |
| ------------------------------------------------------ | ----------------------------------------------------- | ------------------------ | ------------------------- |
| Weekly Production Health Summary                       | `studio/casual-games/team/operations/weekly-health/`  | Producer                 | Weekly                    |
| Capacity Utilization Scorecard                         | `studio/casual-games/team/operations/capscore/`       | Producer (self-reported) | Bi-weekly                 |
| Sprint Retrospective Notes (with escalation decisions) | `studio/casual-games/team/operations/retrospectives/` | Producer                 | Per sprint                |
| Gate Review Checklists (this document, Section 7)      | `studio/casual-games/team/operations/`                | CPO                      | Stage 2 and Stage 3 gates |
| Associate Producer Runbook (Section 6a, Mitigation B)  | `studio/casual-games/team/operations/ap-runbook/`     | Lena Müller              | Bi-weekly                 |
| Shared Metrics Dashboard                               | [Dashboard URL — to be configured]                    | Executive Producer       | Real-time                 |

### Dashboard Requirements

The shared metrics dashboard must display:

1. Sprint completion rate trend (last 8 sprints, line chart)
2. Carryover rate trend (last 8 sprints, bar chart)
3. Cycle time distribution (histogram, last 4 sprints)
4. Blocker resolution time trend (last 8 sprints, line chart)
5. Producer capacity utilization (James + Lena, dual-axis gauge)
6. Current flag status (color-coded: Green / Yellow / Orange / Red)
7. Hiring status (if triggered): pipeline stage, estimated start date

---

> **CPO Note:** I am flagging this at Stage 2/3 gates because production capacity degradation is a lagging indicator. By the time sprint completion drops below 70%, the team has already absorbed months of overload and morale is eroding. The escalation triggers in this framework are designed to catch degradation at the Yellow Flag stage, when a process adjustment can still prevent a hiring emergency. But if we hit Red Flag, there is no debate — we hire the third producer immediately, no exceptions.
>
> The addition of Section 6a (Single Point of Failure Mitigation) is non-negotiable. Lena Müller is a competent AP, but competence is not redundancy. If she walks tomorrow, James Mitchell's coordination capacity drops by roughly 40%, and we cannot absorb that loss mid-sprint. Mitigation B (SOP documentation) starts today. Mitigation A (cross-training) starts within the next sprint. Mitigation C (fast-track requisition) is a contingency, not a preference — if the trigger fires, we move.
>
> — Marcus Tran-Yoshida, CPO
