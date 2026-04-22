# VP Data / Head of Analytics — FY2026 Q2 Requisition (CLOSED — Filled)

**Document Type:** Recruitment Requisition (single-role; closed)
**Version:** 2.0
**Date Filed:** April 21, 2026
**Date Closed:** April 21, 2026
**Prepared By:** CHRO Office (Dr. Evelyn Hartwell) + CPO Office (Marcus Tran-Yoshida)
**Status:** **Closed — Filled.** Dr. Hana Sato accepted the offer on April 21, 2026; profile published at [`../../research-develop/agent/head-of-data-vp-data/profile.md`](../../research-develop/agent/head-of-data-vp-data/profile.md).
**Reporting Line Locked:** Option A — direct report to CPO, dotted line to CTO for data-platform infrastructure.
**Vetting Score:** 19/20 (cleared the L5 / VP floor of ≥ 18/20)
**Department:** Human Resources — Recruitment Plans

---

## Why This Requisition Existed

The company opened this requisition because:

1. **Experimentation governance had no owner.** Every PRD names primary and guardrail metrics; nobody was accountable for declaring statistical guardrails, MDE, sample sizes, or holdout discipline against those metrics. Without an analytical leader, the Experimentation Spec template that lives at `company/pipeline/_base/experimentation-spec-template.md` would have had no sign-off authority.
2. **Audit logging contracts had no analytical co-owner.** Every SRD's audit-logging requirement needed a single co-owner with the CSO; without that co-ownership, audit log retention, encryption-at-rest, and PII redaction were enforced ad hoc.
3. **Studio-scale event volume was on the horizon.** The casual-games studio plans 10–100× event volume vs. the rest of the company's product portfolio combined. The data platform required a credible games-telemetry-scale leader before the studio reached Stage 5.

---

## The Role (As Filled)

### Title

**VP Data / Head of Analytics** (final title locked at offer; reports to the CPO with a dotted line to the CTO for data-platform infrastructure).

### Mandate

Owns the company's data platform end-to-end:

1. **Event instrumentation contract.** Every PRD's metric block must cite a defined event in the company's analytics schema. The VP Data owns the schema, the naming convention, the pipeline, the privacy review, and the lineage documentation. PRDs cannot exit Stage 1 without a "metric definition lock" — the data analogue to the Stage 3 "technology lock."
2. **Audit logging contract.** Every SRD's audit-logging requirement must be implemented against a single, owned logging pipeline with declared retention, encryption-at-rest, and PII-redaction guarantees. The VP Data co-owns this with the CSO.
3. **Analytics platform.** The data warehouse, transformation layer (dbt or equivalent), BI surface (Looker / Mode / Metabase), and experimentation infrastructure (statistical tooling, MDE/sample-size calculators, guardrail-metrics framework). This is the foundation that the Experimentation Spec template (Stage 1 paired artefact) runs on top of.
4. **Studio scale.** The casual-games studio plans 10–100× event volume vs. the rest of the company's product portfolio combined. The VP Data must be credible at games-telemetry scale (not just product-analytics scale) — this was a hard non-negotiable in the bar.

### What This Role Is Not

- **Not a Chief Data Officer.** Tier promotion to a CDO seat is premature at the current product portfolio scale. The role opens at VP tier; tier upgrade can be revisited at the FY2027 quarterly review if scope grows.
- **Not a Chief AI Officer.** AI/ML strategy is out of scope. If/when the company adds an AI product surface, that is a separate role with separate sponsors.
- **Not a "Data Engineering Lead."** The role is platform-owner-tier with named PRD/SRD gate authority. A pure-IC data engineer hire is a downstream Phase-2 activity that this VP scopes once on board.

### Reporting Line — Decision Record

The sponsor panel evaluated three options and locked **Option A** at the close-out review:

| Option                             | Outcome    | Rationale                                                                                                                                                                                                                                       |
| :--------------------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A** — Reports to CPO             | **Locked** | Tightest coupling to the Stage 1 PRD instrumentation gate; the metric-definition-lock is fundamentally a product-decision-quality gate. Dotted line to CTO covers data-platform infrastructure. CPO span-of-control accepted as a managed cost. |
| **B** — Reports to CIO             | Rejected   | Would have placed the metric-definition-lock authority outside the Stage 1 sign-off chain, requiring a new escalation route.                                                                                                                    |
| **C** — Standalone Data department | Rejected   | Org-chart cost not yet justified at current product portfolio scale. Reconsider at FY2027 quarterly review.                                                                                                                                     |

---

## The Sponsor Panel

| Role                 | Person                     | Responsibility on this requisition                                                                                             |
| -------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Co-DRI (Recruitment) | CHRO — Dr. Evelyn Hartwell | Owned the funnel: sourcing, screen, panel logistics, vetting-record authorship.                                                |
| Co-DRI (Domain)      | CPO — Marcus Tran-Yoshida  | Owned the role definition and the metric-definition-lock gate. Co-ran the domain interview. Anchor sponsor.                    |
| Required Panelist    | CTO — Dr. Kenji Nakamura   | Verified engineering credibility (data platform is half infrastructure). Required at panel debrief for the placement decision. |
| Required Panelist    | CIO — Dr. Priya Mehta      | Verified infrastructure-strategy fit. Veto authority if the candidate's platform-architecture judgment had failed the bar.     |
| Required Panelist    | CSO — Dr. Sarah Chen       | Verified the candidate could co-own the audit-logging / PII-redaction contract. Veto authority on privacy posture.             |
| Recused              | CDO, CTO-L, all VPs        | Not on the panel; informed at offer-finalisation only.                                                                         |

**Panel decision rule:** unanimous across CHRO + CPO + CTO + CIO + CSO. The panel was unanimous on Dr. Sato.

---

## Hiring Bar (Met)

The 20-point vetting gate (Impact at Scale, Craft Depth, Leadership Signal, Standards Signal, Red Flag Scan) was applied at the **L5 / VP** floor:

| Gate                       | Requirement                                                                                                                                                                                                                                                                    | Outcome   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------- |
| Total score                | ≥ 18/20 (VP-tier; not the 16/20 IC-Senior floor)                                                                                                                                                                                                                               | 19/20     |
| Minimum per category       | ≥ 4/5 on **all five** dimensions (Standards Signal cannot be < 4)                                                                                                                                                                                                              | All ≥ 4   |
| Red Flag Scan              | PASS                                                                                                                                                                                                                                                                           | PASS      |
| Cultural Alignment         | PASS (non-negotiable; a 20/20 candidate failing alignment is not hired)                                                                                                                                                                                                        | PASS      |
| Domain-specific must-haves | (1) Operated a games-telemetry-scale event pipeline (10–100M events/day or higher) for ≥ 18 months; (2) Owned an experimentation platform with statistical tooling for ≥ 12 months; (3) Has shipped a "metric-definition lock"-equivalent governance artefact in a prior role. | All met   |
| Panel consensus            | Unanimous across CHRO + CPO + CTO + CIO + CSO                                                                                                                                                                                                                                  | Unanimous |

---

## Risk Register (Closed)

| Risk                                                                                                                     | Severity at filing | Disposition                                                                                                                                           |
| :----------------------------------------------------------------------------------------------------------------------- | :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **VPD-R1.** Requisition opens with no candidate in pipeline; expedited search misses the bar.                            | High               | Search converged on Dr. Sato within the same business day; vetting score 19/20 cleared the bar without compromise.                                    |
| **VPD-R2.** Sponsor panel disagrees on reporting line at offer time, blocking close.                                     | Medium             | Panel converged on Option A unanimously; Options B and C documented as rejected with rationale (see Reporting Line decision record above).            |
| **VPD-R3.** Role conflated with a CDO seat at offer-finalisation.                                                        | Medium             | Title locked at VP-tier in the offer letter; CDO escalation deferred to FY2027 review per explicit clause in the role mandate.                        |
| **VPD-R4.** First L5 hire under the reconciled leveling rubric — vetting-score / level discrepancies could surface late. | Low                | Vetting score 19/20 sat cleanly above the L5 floor; no rubric drift was observed. This requisition serves as the calibration record for the L5 floor. |
| **VPD-R5.** Definition of role drifts during sourcing — candidates pull the scope toward their last job.                 | High               | Mandate (above) was treated as locked. Panel debriefs explicitly verified Dr. Sato against the locked mandate, not her self-pitch. No drift detected. |

---

## Document History

| Version | Date       | Changes                                                                                                                                                                                                                                                                         | Status                   |
| :------ | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------- |
| 1.0     | 2026-04-21 | Initial requisition. Lean single-document scope: defined the role, named the panel, set the L5 (≥ 18/20) bar, left reporting-line decision (A/B/C) to the sponsor panel.                                                                                                        | Pending Sponsor Sign-off |
| 2.0     | 2026-04-21 | **Requisition closed.** Sponsor panel ratified the role mandate same-day; expedited search converged on Dr. Hana Sato (Senior Director, Experimentation Platform at a global mobile gaming company; vetting score 19/20). Reporting line locked to Option A. Profile published. | Closed — Filled          |

---

**Next step:** Onboarding handoff to Onboarding Lead Grace Muthoni. First Stage-1 Experimentation Spec sign-off scheduled for the first PRD entering Stage 1 after publication of the Experimentation Spec template at `company/pipeline/_base/experimentation-spec-template.md`.
