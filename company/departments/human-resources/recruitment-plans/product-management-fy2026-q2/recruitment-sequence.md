# VP Product — Recruitment Sequence

**Document Type:** Recruitment Execution Sequence
**Version:** 2.0
**Date:** April 19, 2026
**Owner:** CHRO (Dr. Evelyn Hartwell) — primary. CPO (Marcus Tran-Yoshida) — hiring manager.
**Status:** Approved
**Depends On:** [`../product-management-fy2026-q2.md`](../product-management-fy2026-q2.md), [`competency-matrices/README.md`](competency-matrices/README.md)

---

## Purpose

Step-by-step execution plan for recruiting the two VP-tier Product Leaders. Covers sourcing through offer acceptance. Once a candidate accepts, the subsequent 90-day integration is covered by [`onboarding-plan/onboarding-plan.md`](onboarding-plan/onboarding-plan.md).

---

## At a Glance

| Metric         | Value                                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Total hires    | 2                                                                                                                                   |
| Hiring model   | Parallel — both funnels run simultaneously                                                                                          |
| Target window  | 4 weeks from approval to offer acceptance (both candidates)                                                                         |
| Elastic        | Up to 8 weeks if the bar is not cleared in 4                                                                                        |
| Hiring bar     | 16/20 minimum on the 20-point vetting gate; 4/5 floor per category; PASS on Red Flag Scan; PASS on Cultural Alignment               |
| Panel          | CPO, CHRO, CTO, CIO, + CSO (for API role), + CDO (for Web role), + domain counterpart (Elena Vasquez for Web; Dev Malhotra for API) |
| Consensus rule | Unanimous PASS across the panel; single veto blocks the offer                                                                       |

---

## Prerequisites (Before Sourcing Begins)

1. User has approved the master recruitment plan.
2. CPO has approved the competency matrices.
3. CPO has approved the 90-day onboarding plan.
4. CSO, CIO, CDO, CTO have been briefed on their role in the panel.
5. `vp-product-api-platform/` folder exists at `company/departments/product-management/team/supervisors/` with empty `agent/` and `skills/` subfolders (matching the structure of the existing `vp-product-web-platform/` placeholder). CHRO creates this before sourcing begins.
6. CHRO reserves `recruit-product.md` capacity for two parallel funnels.

---

## The Two Funnels

Both funnels run independently and in parallel. Neither hire blocks the other. If one funnel closes before the other, that candidate starts onboarding immediately and the second funnel continues.

| Funnel | Role                                  | Domain Counterpart (Panel)                           | Folder Target                                               |
| ------ | ------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| **W**  | VP Product, Web Platforms             | Elena Vasquez (VP of Web & Backend Engineering, R&D) | `team/supervisors/vp-product-web-platform/` (exists)        |
| **A**  | VP Product, API & Developer Platforms | Dev Malhotra (Backend Chapter Lead, R&D)             | `team/supervisors/vp-product-api-platform/` (to be created) |

---

## Selection Stages

Each funnel passes through the same seven stages. The CPO and CHRO participate in every stage. Other Chief Officers enter at Stage D.

### Stage A — Profile Screen (CHRO)

Inbound candidate profiles (sourced, referred, or applied) are screened against the coarse filter:

- ≥ 8 years product management experience with direct product ownership
- ≥ 3 years managing other PMs (team-of-PMs experience at VP tier)
- Demonstrable domain signal: shipped web products at meaningful scale (Web funnel); shipped API products with developer adoption (API funnel)
- No obvious cultural-misalignment markers from public writing, prior references, or public employment history

Candidates clearing the screen advance to Stage B. Rough throughput assumption: 10–20 screened candidates per funnel yields 3–5 advancing to Stage B.

### Stage B — Initial Conversation (CPO)

A 45-minute conversation with the CPO. Purpose: calibrate on whether the candidate has the strategic judgment and template-stewardship posture that makes the rest of the process worth running. Not a deep-dive on craft yet.

A candidate who signals in this conversation that they would "redesign the PRD template" on arrival is ended at Stage B.

### Stage C — Domain Interview (CPO + Domain Counterpart)

A 90-minute conversation with the CPO and the R&D domain counterpart (Elena Vasquez for W; Dev Malhotra for A). Covers craft depth through live scenarios, not hypotheticals the candidate prepared. The domain counterpart is assessing whether the candidate can be a credible R&D partner for their pipeline.

### Stage D — Landscape Exercise

The candidate receives a short brief (half a page) for a real or lightly-fictionalized product opportunity in their domain. They have 5 business days to produce a 3-page **Landscape Memo** — state of the domain, top opportunities, top risks, first proposed quarterly bet. The format loosely mirrors what they will produce at Day 30 of onboarding if hired.

The CPO reads the memo and scores it qualitatively against his own standard. This is the most load-bearing signal in the process. A weak Landscape Memo ends the candidacy regardless of how strong the live conversations have been.

### Stage E — Panel Interview

A round of 45-minute conversations. Each panel member evaluates against their assigned dimensions from the [`competency-matrices/README.md`](competency-matrices/README.md).

| Panel Member  | Web Funnel             | API Funnel                                |
| ------------- | ---------------------- | ----------------------------------------- |
| CPO           | ✓                      | ✓                                         |
| CHRO          | ✓                      | ✓                                         |
| CTO           | ✓                      | ✓                                         |
| CIO           | ✓                      | ✓                                         |
| CSO           | —                      | ✓ (API security product-awareness)        |
| CDO           | ✓ (design partnership) | — (lighter engagement; DevPortal UX only) |
| Elena Vasquez | ✓                      | (already Stage C)                         |
| Dev Malhotra  | —                      | (already Stage C)                         |

Each panel member records PASS / FAIL on their dimensions, with commentary.

### Stage F — References and Back-Channel

CHRO contacts three candidate-supplied references plus two independently-sourced back-channel references. Material inconsistencies between the two pools are a FAIL for Red Flag Scan. Cultural-alignment concerns surfaced through reference conversations are weighed directly into Cultural Alignment.

### Stage G — Panel Debrief, Scoring, and Decision

The full panel convenes for a structured debrief. Each panel member reports their dimension scores with brief rationale. Scores are compiled into the 20-point matrix from the competency document.

Decision rule:

- Total ≥ 16/20 **and** every category ≥ 4/5 **and** Red Flag Scan PASS **and** Cultural Alignment PASS **and** unanimous Chief Officer PASS → offer extended
- Otherwise → candidate declined; funnel continues

The decision is not appealable from within the panel; it is made by consensus.

### Stage H — Offer and Placement

On offer acceptance:

1. CHRO invokes `recruit-product.md` to produce the `agent/profile.md` artifact in the appropriate supervisor folder (`vp-product-web-platform/agent/` or `vp-product-api-platform/agent/`).
2. The `skills/` folder remains empty until Phase 3 of the 90-day onboarding (`web-product-strategy.md` or `api-product-strategy.md`, authored by the VP themselves).
3. Start date is scheduled; onboarding kickoff is Day 1.

---

## Week-by-Week Calendar (Target)

Both funnels run on the same cadence unless sourcing latency diverges.

| Week | Web Funnel                                                              | API Funnel                                                 |
| ---- | ----------------------------------------------------------------------- | ---------------------------------------------------------- |
| 1    | Sourcing + Stage A screen + Stage B initial conversations               | Sourcing + Stage A screen + Stage B initial conversations  |
| 2    | Stage C domain interview (CPO + Elena)                                  | Stage C domain interview (CPO + Dev)                       |
| 3    | Stage D landscape exercise (5 business days) + Stage E panel interviews | Stage D landscape exercise + Stage E panel interviews      |
| 4    | Stage F references + Stage G panel debrief + Stage H offer              | Stage F references + Stage G panel debrief + Stage H offer |

If Stage D or E surfaces a candidate who is close-but-not-clear, the CHRO and CPO discuss whether to extend the funnel with a second candidate from the Stage A/B pool. The funnel continues until the bar is met.

---

## The Bar

The same bar applies to both hires. See [`competency-matrices/README.md`](competency-matrices/README.md) for dimension definitions.

| Requirement                                                                                | Value                                                            |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Total score                                                                                | ≥ 16/20                                                          |
| Category floor (each of Impact at Scale, Craft Depth, Leadership Signal, Standards Signal) | ≥ 4/5                                                            |
| Red Flag Scan                                                                              | PASS                                                             |
| Cultural Alignment                                                                         | PASS (non-negotiable)                                            |
| Panel consensus                                                                            | Unanimous (every panel member PASS on their assigned dimensions) |

There is no "conditional hire" tier. A candidate is either above the bar on every requirement, or they are not hired. If the bar is not cleared within 4 weeks, the window extends — vacancy is preferable to a below-bar hire at VP tier.

---

## Failure Modes and Responses

### No qualified candidate clears the bar in 4 weeks

Extend the window. Widen the sourcing aperture (additional search firms, additional referral sources, adjacent-industry candidates). Reassess at Week 8. If still no candidate clears the bar at Week 8, escalate to the User — this may indicate the bar needs CPO review (not lowering, but refinement) or the sourcing strategy needs restructuring.

### One funnel closes and the other does not

Start the onboarding for the placed VP immediately. The second funnel continues. The CPO retains Stage 1 authority for the unfilled pipeline during the extended search (which is the current state, so no regression).

### Candidate accepts offer and then withdraws before start date

Return to Stage A/B pool; resume the funnel with the next-strongest candidate. No cascading delay to the other funnel.

### Candidate accepts, starts, and the Day 30 Landscape Memo is weak

This is an onboarding concern, not a recruitment concern. Handled per the 90-day onboarding plan. Does not retroactively invalidate the recruitment.

### Stakeholder feedback during onboarding surfaces cultural-alignment concerns that weren't caught during reference checks

Concerns are surfaced to the CHRO. If they are material, they are addressed in the 30- or 60-day check-in and, if unresolved, factor into the Day 90 decision. The CHRO conducts a post-mortem on the reference process to understand what was missed.

---

## Roles and Responsibilities

| Role                                | Responsibility                                                                                                                                                            |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CPO**                             | Hiring manager. Participates in every stage from B onward. Makes final recommendation to the panel. Owns the onboarding sponsorship after hire.                           |
| **CHRO**                            | Process steward. Runs Stages A, F, G. Manages calendar, candidate communications, references. Records scores in [`recruitment-checkpoint.md`](recruitment-checkpoint.md). |
| **CTO**                             | Panel member. Evaluates Leadership Signal and cross-pipeline fluency (Stage 1 → Stage 3 handoff).                                                                         |
| **CIO**                             | Panel member. Evaluates Standards Signal and ADR-feeding discipline for the API funnel; lighter touch for Web.                                                            |
| **CSO**                             | Panel member (API funnel). Evaluates API security product-awareness. Optional consultant on Web funnel.                                                                   |
| **CDO**                             | Panel member (Web funnel). Evaluates design-partnership fluency. Lighter touch on API funnel (developer-portal UX only).                                                  |
| **Elena Vasquez** (VP W&B Eng, R&D) | Domain counterpart for Web funnel. Stage C interviewer. Panel member at Stage G.                                                                                          |
| **Dev Malhotra** (Backend CL, R&D)  | Domain counterpart for API funnel. Stage C interviewer. Panel member at Stage G.                                                                                          |

---

## Placement and Artifact Creation

### Web VP Placement

- **Folder:** `company/departments/product-management/team/supervisors/vp-product-web-platform/`
- **Status pre-hire:** Placeholder exists, `agent/` and `skills/` subfolders empty.
- **On offer acceptance:** CHRO populates `agent/profile.md` using `recruit-product.md` output. `skills/` remains empty.
- **During onboarding Phase 3:** VP authors `skills/web-product-strategy.md`; CPO reviews and merges.

### API VP Placement

- **Folder:** `company/departments/product-management/team/supervisors/vp-product-api-platform/`
- **Status pre-hire:** Does not yet exist. CHRO creates the folder + empty `agent/` and `skills/` subfolders during Prerequisites, before sourcing begins.
- **On offer acceptance:** CHRO populates `agent/profile.md`. `skills/` remains empty.
- **During onboarding Phase 3:** VP authors `skills/api-product-strategy.md`; CPO reviews and merges.

---

## Risks and Mitigations

| Risk                                                                      | Likelihood | Impact | Response                                                                                                                                                                                               |
| ------------------------------------------------------------------------- | ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| No qualified Web VP candidate in 4 weeks                                  | Low        | Medium | Extend window; widen sourcing. Do not lower bar.                                                                                                                                                       |
| No qualified API VP candidate in 4 weeks                                  | Medium     | Medium | API-as-product VP is a rarer profile. Pre-authorize an 8-week window in the master plan.                                                                                                               |
| CPO perceives VP hires as a reduction of his scope                        | Low        | High   | Pre-sourcing 1:1 between User + CPO. Reinforce: scope formalized, template stewardship preserved, authority retained as specified in [`pipeline-amendments/README.md`](pipeline-amendments/README.md). |
| Cultural friction between CPO's standards-rigor and new VP's expectations | Medium     | High   | Cultural Alignment is a panel veto. Surfaced aggressively at Stage E + F. If friction emerges during onboarding, CHRO mediates.                                                                        |
| VP Web and VP API can't work together on Full-Stack after hire            | Medium     | Medium | Stage E panel tests collaborative posture. Phase 3 Full-Stack dry-run surfaces friction before full authority transfer. If genuinely incompatible, Full-Stack stays with CPO.                          |
| Panel fatigue — too many interviews for the same two roles                | Medium     | Low    | Strict 45-minute cap per Stage E conversation. Debrief is consolidated. Each officer is asked for exactly their dimension, not a full candidate review.                                                |

---

## Document History

| Version | Date       | Changes                                                                                                                                               | Status           |
| ------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| 1.0     | 2026-04-18 | Initial sequence for 2 VP-tier hires (parallel), 30-day probationary ramp.                                                                            | Superseded       |
| 2.0     | 2026-04-18 | Rewrite. Aligned to 90-day onboarding. Removed engineering-precedent claims. Clarified panel composition per funnel. Tightened failure-mode protocol. | Pending Approval |

---

**Next step:** CPO approval. On approval, CHRO creates the `vp-product-api-platform/` folder and begins Stage A sourcing for both funnels.
