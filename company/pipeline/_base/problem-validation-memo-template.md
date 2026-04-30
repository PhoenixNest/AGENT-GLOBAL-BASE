# Problem Validation Memo

> **Stage:** 0 — Problem Validation
> **Max Length:** 2 pages (this template; delete guidance notes before submission)
> **Responsible Producer:** CPO (or VP of the relevant product area)
> **Gate Criterion:** CPO sign-off required before Stage 1 (PRD authoring) begins

**Project Codename:** [Codename]
**Author:** [CPO / VP Name]
**Date:** YYYY-MM-DD
**Version:** v1
**Pipeline:** [Mobile / Web / Backend API / Full-Stack]

---

## 1. Problem Statement

_One paragraph. What is the specific problem being solved? Who experiences it? When? Why does the current state fail them?_

> **Example:** "Mobile users of productivity apps abandon them within 7 days because onboarding requires 15+ minutes and 12 screens. Competing apps average 3 minutes and 4 screens. Our current onboarding is 22 screens."

[Your problem statement here]

---

## 2. Customer-Discovery Evidence

_Minimum 5 interviews or equivalent observational data. Document evidence type, sample, and key findings._

| #   | Evidence Type                                            | Sample    | Key Finding | Verbatim Quote / Data Point |
| --- | -------------------------------------------------------- | --------- | ----------- | --------------------------- |
| 1   | [User interview / Support ticket cluster / NPS verbatim] | [N users] | [Finding]   | "[Quote or data]"           |
| 2   | [User interview / Observation / Analytics]               | [N users] | [Finding]   | "[Quote or data]"           |
| 3   | [User interview / Usability session]                     | [N users] | [Finding]   | "[Quote or data]"           |
| 4   | [User interview / Sales call feedback]                   | [N users] | [Finding]   | "[Quote or data]"           |
| 5   | [User interview / Churn survey]                          | [N users] | [Finding]   | "[Quote or data]"           |

**Validation rate:** [X of Y interviews confirmed the problem hypothesis] = [XX%]

> **Gate criterion:** n ≥ 5 evidence items required. Validation rate < 60% → Stage 1 does not begin.

---

## 3. Quantitative Demand Signal

_At least one quantified signal that the problem is real and material at scale._

| Signal Type                                             | Metric                           | Value   | Source             | Date       |
| ------------------------------------------------------- | -------------------------------- | ------- | ------------------ | ---------- |
| [Funnel drop-off / Search volume / Competitor adoption] | [Metric name]                    | [Value] | [Source]           | YYYY-MM-DD |
| [Support ticket volume]                                 | [Tickets/month about this issue] | [N]     | [Zendesk/Intercom] | YYYY-MM-DD |
| [Revenue at risk / Churn attributable to this problem]  | [$ or %]                         | [Value] | [Analytics]        | YYYY-MM-DD |

**Summary of signal strength:** [Strong / Moderate / Weak — brief explanation]

---

## 4. Opportunity Sizing

| Dimension                      | Estimate | Method                             | Confidence            |
| ------------------------------ | -------- | ---------------------------------- | --------------------- |
| Total Addressable Market (TAM) | [$X]     | [Bottom-up / Top-down]             | [High / Medium / Low] |
| Serviceable Market (SAM)       | [$X]     | [Defined by platform + language]   | [High / Medium / Low] |
| Initial Target Segment (SOM)   | [$X]     | [First 12-month realistic capture] | [High / Medium / Low] |

---

## 5. Kill Criteria

_Explicit, testable conditions under which Stage 1 will NOT be entered._

| #   | Kill Condition                            | Measurement                  | Threshold   |
| --- | ----------------------------------------- | ---------------------------- | ----------- |
| 1   | Interview validation rate below threshold | Validated / Total interviews | < 60%       |
| 2   | No quantitative demand signal found       | Demand signals identified    | = 0         |
| 3   | [Product-specific kill condition]         | [Metric]                     | [Threshold] |
| 4   | [Product-specific kill condition]         | [Metric]                     | [Threshold] |

**Kill status as of this memo:** ☐ No conditions triggered (safe to proceed) / ☐ Condition [N] triggered (DO NOT proceed)

---

## 6. Scope of Validation

_What was NOT tested and remains assumed. Unsurfaced assumptions are risks that will be carried into Stage 1._

| Assumption                                     | Risk if Wrong    | Mitigation Plan                      |
| ---------------------------------------------- | ---------------- | ------------------------------------ |
| [e.g., Users willing to pay for this solution] | [No revenue]     | [Willingness-to-pay test at Stage 2] |
| [e.g., This is solvable in the mobile surface] | [Wrong platform] | [Surface confirmed at Stage 1 gate]  |
| [e.g., No regulatory blocker in target market] | [Launch blocked] | [Legal review at Stage 3]            |

---

## 7. Recommended Next Step

☐ **Proceed to Stage 1** — All kill criteria clear; evidence is sufficient.

☐ **Extend validation** — Specific gap: [describe what additional evidence is needed and by when].

☐ **Kill** — Kill condition [N] triggered: [brief explanation].

---

## CPO Sign-Off

| Role | Name   | Decision                                            | Date       |
| ---- | ------ | --------------------------------------------------- | ---------- |
| CPO  | [Name] | ☐ Proceed to Stage 1 / ☐ Extend validation / ☐ Kill | YYYY-MM-DD |

---

_This memo is a Stage 0 gate artifact. It must be archived alongside the Stage 1 PRD as part of the paired artifact set._
