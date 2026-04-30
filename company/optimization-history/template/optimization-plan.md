# [Short Title] — Optimization Plan

<!-- Replace the title above with a human-readable name matching the folder slug,
     e.g. "Operating Model Review — Optimization Plan" or "i18n Pipeline Restructure — Optimization Plan" -->

| Field             | Value                                                            |
| ----------------- | ---------------------------------------------------------------- |
| **Document Type** | [e.g. Operating Model Review + Optimization Plan]                |
| **Plan ID**       | OPT-YYYY-MM-DD-NNN                                               |
| **Date**          | [Month DD, YYYY]                                                 |
| **Author**        | [Author name / role]                                             |
| **Scope**         | [One-line description of what was reviewed]                      |
| **Audience**      | CEO [Name]                                                       |
| **Status**        | Draft                                                            |
| **Version**       | 1.0                                                              |
| **Supersedes**    | None                                                             |
| **Next Review**   | Quarterly cadence — first retrospective checkpoint [Day 90 date] |

---

## 1. Executive Summary

### 1.1 Verdict at a Glance

<!-- One row per major dimension reviewed. Grade A–F. Keep headlines to one sentence. -->

| Dimension     | Grade   | Headline               |
| ------------- | ------- | ---------------------- |
| [Dimension 1] | [Grade] | [One-sentence verdict] |
| [Dimension 2] | [Grade] | [One-sentence verdict] |

### 1.2 Headline Statement

> [One paragraph. Synthesize the most important finding and the primary recommended action. Write it so the CEO can scan this alone and understand the plan's urgency and direction.]

### 1.3 Findings Distribution

| Severity                  | Count |
| ------------------------- | ----- |
| **P0 — Critical**         | 0     |
| **P1 — Important**        | 0     |
| **P2 — Polish**           | 0     |
| **Strengths to Preserve** | 0     |
| **Total Items**           | **0** |

---

## 2. Sources Reviewed

<!-- List every file, folder, or system consulted. Findings must be traceable to these sources. -->

| Category                     | Scope                       |
| ---------------------------- | --------------------------- |
| [Category, e.g. Pipelines]   | [Paths or systems reviewed] |
| [Category, e.g. Departments] | [Paths or systems reviewed] |

---

## 3. Strengths to Preserve

<!-- Explicitly name what is working well. This prevents remediation from accidentally destroying good patterns. -->

| #    | Strength               | Why It Must Be Preserved        |
| ---- | ---------------------- | ------------------------------- |
| S-01 | [Strength description] | [Business or quality rationale] |

---

## 4. Critical Findings (P0)

<!-- P0 = Must fix. Blocking production quality, security, or correctness. -->

| ID         | Finding               | Root Cause   | Impact            | Recommendation    | Owner  | Due (Day) |
| ---------- | --------------------- | ------------ | ----------------- | ----------------- | ------ | --------- |
| FIND-P0-01 | [Finding description] | [Root cause] | [Business impact] | [Specific action] | [Role] | Day 30    |

---

## 5. Important Findings (P1)

<!-- P1 = Should fix. Meaningful degradation in quality, reliability, or maintainability if left unaddressed. -->

| ID         | Finding               | Root Cause   | Impact            | Recommendation    | Owner  | Due (Day) |
| ---------- | --------------------- | ------------ | ----------------- | ----------------- | ------ | --------- |
| FIND-P1-01 | [Finding description] | [Root cause] | [Business impact] | [Specific action] | [Role] | Day 60    |

---

## 6. Polish Findings (P2)

<!-- P2 = Nice to fix. Low-risk improvements; can be deferred if higher-priority work is in flight. -->

| ID         | Finding               | Root Cause   | Impact            | Recommendation    | Owner  | Due (Day) |
| ---------- | --------------------- | ------------ | ----------------- | ----------------- | ------ | --------- |
| FIND-P2-01 | [Finding description] | [Root cause] | [Business impact] | [Specific action] | [Role] | Day 90    |

---

## 7. Out of Scope

<!-- Be explicit. Name things that were deliberately not reviewed so readers don't assume omission = endorsement. -->

- [Item explicitly excluded from this review]
- [Item explicitly excluded from this review]

---

## 8. Optimization Topics

<!-- One sub-section per major theme. Each sub-section provides a deep dive into the findings and recommendations
     for that theme. Copy §8.N as needed. -->

### 8.1 [Topic Name]

<!-- Deep-dive table covering all findings related to this topic -->

| Aspect   | Current State       | Gap                       | Recommendation    |
| -------- | ------------------- | ------------------------- | ----------------- |
| [Aspect] | [What exists today] | [What's missing or wrong] | [Specific action] |

---

## 9. 30/60/90-Day Execution Plan

<!-- Steps are sequenced by dependency and grouped into delivery windows.
     Each step must map to one or more findings above (use FIND-Px-NN IDs). -->

### 9.1 Days 0–30 (P0 Closure)

| Step | Action               | DRI    | Addresses  | Acceptance Criteria         | Status     |
| ---- | -------------------- | ------ | ---------- | --------------------------- | ---------- |
| 1    | [Action description] | [Role] | FIND-P0-01 | [Measurable done-condition] | ⬜ Pending |

### 9.2 Days 30–60 (P1 Closure)

| Step | Action               | DRI    | Addresses  | Acceptance Criteria         | Status     |
| ---- | -------------------- | ------ | ---------- | --------------------------- | ---------- |
| 2    | [Action description] | [Role] | FIND-P1-01 | [Measurable done-condition] | ⬜ Pending |

### 9.3 Days 60–90 (P2 + Verification)

| Step | Action               | DRI    | Addresses  | Acceptance Criteria         | Status     |
| ---- | -------------------- | ------ | ---------- | --------------------------- | ---------- |
| 3    | [Action description] | [Role] | FIND-P2-01 | [Measurable done-condition] | ⬜ Pending |

---

## 10. Risk Register

<!-- Risks that could derail execution. Distinct from findings — these are forward-looking execution risks. -->

| Risk ID  | Risk               | Likelihood          | Impact              | Mitigation          | Status |
| -------- | ------------------ | ------------------- | ------------------- | ------------------- | ------ |
| RISK-001 | [Risk description] | High / Medium / Low | High / Medium / Low | [Mitigation action] | Open   |

---

## 11. Success Metrics

<!-- Define measurable outcomes that confirm the plan worked. Measured at Day 30, Day 60, and Day 90. -->

| Metric        | Baseline        | Target         | Measurement Date |
| ------------- | --------------- | -------------- | ---------------- |
| [Metric name] | [Current value] | [Target value] | Day 90 ([date])  |

---

## 12. Audit & Sign-off Block

### 12.1 Audit Log

<!-- Append-only. Each CEO review, approval, or condition adds a row. Never edit existing rows. -->

| Date         | Auditor | Action               | Notes |
| ------------ | ------- | -------------------- | ----- |
| [YYYY-MM-DD] | [Name]  | Submitted for review | —     |

### 12.2 CEO Sign-off

| Field          | Value   |
| -------------- | ------- |
| **Decision**   | Pending |
| **Signed**     | —       |
| **Date**       | —       |
| **Conditions** | —       |
| **CEO Notes**  | —       |

---

## 13. Document Version History

| Version | Date         | Author   | Changes       |
| ------- | ------------ | -------- | ------------- |
| 1.0     | [YYYY-MM-DD] | [Author] | Initial draft |

---

## 14. Traceability Matrix

<!-- Cross-reference every finding to its execution step and current status.
     This is the CEO's at-a-glance view of plan completeness. -->

| Finding ID | Finding (short) | Step # | Owner  | Status     |
| ---------- | --------------- | ------ | ------ | ---------- |
| FIND-P0-01 | [Short label]   | Step 1 | [Role] | ⬜ Pending |
| FIND-P1-01 | [Short label]   | Step 2 | [Role] | ⬜ Pending |
| FIND-P2-01 | [Short label]   | Step 3 | [Role] | ⬜ Pending |
