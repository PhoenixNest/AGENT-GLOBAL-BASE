# Product Management Division — FY2026 Q2 Recruitment Plan

**Document Type:** Recruitment Plan
**Version:** 2.0
**Date:** April 19, 2026
**Prepared By:** CPO Office (Marcus Tran-Yoshida) + CHRO Office (Dr. Evelyn Hartwell)
**Status:** Approved
**Department:** Human Resources — Recruitment Plans

---

## Executive Summary

The Product Management division is adding two VP-tier leaders to close a structural gap in how this company produces Stage 1 PRDs. Today, a single CPO with deep mobile-native craft is the named owner of Stage 1 for four pipelines. Three of those pipelines — Web, Backend API, and Full-Stack Cross-Platform — are outside the CPO's native domain. The result is a CPO-as-bottleneck problem and a quality gap in three out of four pipelines' Stage 1 output.

This plan hires a **VP Product, Web Platforms** and a **VP Product, API & Developer Platforms** in parallel, reporting directly to the CPO. Each takes primary Stage 1 authorship for their pipeline after a 90-day onboarding; the two co-author Full-Stack PRDs jointly. The CPO retains final sign-off, template stewardship, and arbitration authority when mobile enters a Full-Stack feature.

| Metric                         | Value                                                                                                                                   |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Headcount                      | 2 FTEs (VP-tier)                                                                                                                        |
| Hiring model                   | Parallel — two candidates pipelined simultaneously                                                                                      |
| Recruitment window             | ~4 weeks (target)                                                                                                                       |
| Onboarding                     | 90 days per VP (Immerse 30 → Contribute 30 → Lead 30)                                                                                   |
| Time to full pipeline coverage | ~17 weeks from approval                                                                                                                 |
| Hiring bar                     | Same 20-point vetting gate used for all Chief Officer hires. 16/20 minimum; 4/5 minimum per category; cultural alignment non-negotiable |

---

## The Problem

The CPO was recruited when the company ran a single mobile pipeline. His 19/20 vetting score reflected exceptional depth in mobile product strategy — not universal product strategy. His formal title includes "(Mobile Platforms)" in the scope. His two skills, `mobile-product-strategy.md` and `prd-authorship.md`, are mobile-native: the PRD template's Section 5 (Platform-Specific UX Constraints) mandates iOS HIG and Android Material Design adherence with no comparable treatment for web surfaces or API schemas.

Since then, the company has activated three additional pipelines:

| Pipeline                  | Status | Native-domain CPO coverage  |
| ------------------------- | ------ | --------------------------- |
| Mobile                    | Active | Native (CPO's depth)        |
| Web                       | Active | Missing                     |
| Backend API               | Active | Missing                     |
| Full-Stack Cross-Platform | Active | Partial (mobile slice only) |

All four pipeline specifications name the CPO as the Stage 1 PRD producer. The CPO is therefore the sole named author for three domains in which his depth is near zero. What we ship in those three pipelines at Stage 1 is either mobile-template-imitating (the CPO writes what he knows and the template shows it) or arrives under-specified for the domain (accessibility criteria, SEO strategy, API pricing structure, developer-experience KPIs).

A placeholder folder for a `vp-product-web-platform/` supervisor tier already exists at `company/departments/product-management/team/supervisors/`, empty. The recognition of the gap is not new; the resolution is.

---

## Why We Are Not Replacing the CPO

Three considerations, each independently sufficient:

1. **The CPO's vetting score was 19/20, with 5/5 on both Craft Depth and Standards Signal.** These are the two dimensions where the cost of replacement is highest. We do not replace someone who scored 5/5 on the standards-setting dimension when the standard is already operating as a company-wide asset.
2. **The PRD template is an operating standard, and replacing its author destabilizes it.** Every shipped and in-flight PRD in the company adheres to this template. A new CPO would either adopt the template (in which case the replacement hasn't solved anything) or replace it (which would invalidate a large body of in-flight work and be a regression on standards maturity).
3. **Elite CPO candidates with equal depth across Mobile + Web + API are vanishingly rare.** The realistic outcome of a CPO replacement search is a 3/5 generalist across three domains — a strict downgrade from a 5/5 specialist augmented by domain VPs.

---

## Why Augmentation Is the Right Shape

The CPO's existing strength is a company asset. The right move is to surround that strength with complementary depth rather than trade it away for a weaker generalist.

The augmentation pattern has three structural properties worth naming:

- **Domain depth at the VP tier.** Each new VP brings native-domain depth (web or API) that no single generalist could match.
- **Consistent standards across pipelines.** The PRD template remains one standard, with platform-specific extensions authored by the VPs for their domains.
- **Clear, non-shared pipeline ownership.** After the transfer, each of Mobile / Web / API has a single named Stage 1 author. Full-Stack is the only pipeline with joint authorship, and that is a necessary consequence of the domain — not a design choice.

This is a specialist-under-specialist structure, not a generalist-over-generalists structure. The CPO remains the company's mobile product specialist and PRD standard-setter. The two new VPs are domain specialists with VP-tier seniority and direct-report authority under the CPO.

---

## The Two Roles

### VP Product, Web Platforms

Owns Stage 1 PRD authorship for the Web Development pipeline and the web slice of Full-Stack PRDs. Responsible for web-native product strategy at this company — PWA / SPA / SSR choices as product calls (not engineering calls), conversion mechanics and organic growth, multi-viewport design strategy, web accessibility as a first-class product dimension, and web-native monetization (SaaS pricing, subscription flows, no App Store tax).

Folder: `company/departments/product-management/team/supervisors/vp-product-web-platform/` (placeholder already exists, empty).

### VP Product, API & Developer Platforms

Owns Stage 1 PRD authorship for the Backend API pipeline and the API slice of Full-Stack PRDs. Responsible for API-as-product strategy — treating OpenAPI schemas, versioning policy, and deprecation lifecycle as product decisions; developer experience (SDK quality, quickstart times, error-message quality, time-to-first-successful-call) as a measured product discipline; developer relations as a product function; and API pricing and rate-limit tiering as product-strategy levers.

Folder: `company/departments/product-management/team/supervisors/vp-product-api-platform/` — to be created before recruitment begins. CHRO responsibility.

### Ownership Matrix After Transfer

| Pipeline    | Stage 1 Primary                       | Template Steward | Final Sign-Off                                    |
| ----------- | ------------------------------------- | ---------------- | ------------------------------------------------- |
| Mobile      | CPO                                   | CPO              | CPO                                               |
| Web         | VP Product, Web Platforms             | CPO              | CPO                                               |
| Backend API | VP Product, API & Developer Platforms | CPO              | CPO                                               |
| Full-Stack  | VP Web + VP API jointly               | CPO              | CPO (also arbiter when mobile enters the feature) |

Full specification of decision rights, escalation paths, and execution gates lives in [`product-management-fy2026-q2/pipeline-amendments/README.md`](product-management-fy2026-q2/pipeline-amendments/README.md).

---

## Organization Structure

### Before This Plan

```
CPO (Marcus Tran-Yoshida)
  — Stage 1 PRD author, all four pipelines (structural bottleneck)
```

### After This Plan

```
CPO (Marcus Tran-Yoshida)
  — Template stewardship, Mobile Stage 1, final sign-off all pipelines, arbiter for cross-pipeline features
  ├── VP Product, Web Platforms [NEW]
  │     — Web Stage 1, web slice of Full-Stack
  │
  └── VP Product, API & Developer Platforms [NEW]
        — API Stage 1, API slice of Full-Stack
```

Span-of-control on the CPO: 2 direct reports. Well under the 10-direct-report ceiling. Room to grow each VP's team in future quarters without span pressure.

### Reporting Impact Across the C-Suite

| Officer                    | Change                                                                                                               |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| CPO (Marcus Tran-Yoshida)  | +2 direct reports. Scope formalized as Mobile + company-wide PRD standards. No tier change.                          |
| CTO (Dr. Kenji Nakamura)   | No new direct reports. Gains two product counterparts for Web / API — tighter Stage 1 → Stage 3 coordination.        |
| CDO (Yuki Tanaka-Chen)     | No new direct reports. Stage 2 handoff partner is the relevant VP (or CPO for Mobile).                               |
| CSO (Dr. Sarah Chen)       | No new direct reports. SRD co-authorship partner for Web / API product-surface security criteria is the relevant VP. |
| CIO (Dr. Priya Mehta)      | No new direct reports. Stage 3 ADR inputs improve in domain specificity.                                             |
| CHRO (Dr. Evelyn Hartwell) | Owns recruitment execution and the onboarding process-stewardship role.                                              |

---

## Hiring Bar

The 20-point vetting gate (Impact at Scale, Craft Depth, Leadership Signal, Standards Signal, Red Flag Scan) applies to both hires. Detailed role-specific dimensions in [`product-management-fy2026-q2/competency-matrices/README.md`](product-management-fy2026-q2/competency-matrices/README.md).

| Gate                 | Requirement                                                                |
| -------------------- | -------------------------------------------------------------------------- |
| Total score          | ≥ 16/20                                                                    |
| Minimum per category | ≥ 4/5 on Impact at Scale, Craft Depth, Leadership Signal, Standards Signal |
| Red Flag Scan        | PASS                                                                       |
| Cultural Alignment   | PASS (non-negotiable)                                                      |
| Panel consensus      | Unanimous across CPO, CHRO, CTO, CIO (+ CSO for API role)                  |

Categories and the specific product-leadership dimensions within each are defined in the competency matrices. The headline: we are recruiting for strategic judgment, customer empathy, commercial literacy, storytelling, and kill-criteria discipline — in addition to domain craft.

A 20/20 candidate who fails Cultural Alignment is not hired. This matches the company-wide standard set by the engineering hiring bar and is not negotiable.

---

## Recruitment Timeline

Parallel hiring. Two candidates in each funnel simultaneously. Total expected window from approval to offer: ~4 weeks, contingent on candidate availability in each domain.

| Week   | Web Product VP funnel                                                             | API Product VP funnel                                                             |
| ------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Week 1 | Sourcing + profile screen (CHRO + CPO)                                            | Sourcing + profile screen (CHRO + CPO)                                            |
| Week 2 | Domain interview (CPO + Elena Vasquez)                                            | Domain interview (CPO + Dev Malhotra)                                             |
| Week 3 | Landscape exercise (5 business days); panel interview with CTO / CIO / CDO / CHRO | Landscape exercise (5 business days); panel interview with CTO / CIO / CSO / CHRO |
| Week 4 | Panel debrief; references + back-channel; offer                                   | Panel debrief; references + back-channel; offer                                   |

A 4-week window is the target, not a ceiling. If no candidate clears the 16/20 bar in 4 weeks, the window extends. Vacancy is preferable to a below-bar hire — particularly at VP tier, particularly with Marcus's opinionated standards, and particularly with the scrutiny a below-bar hire would receive from stakeholders who already know what "good" looks like from working with Marcus.

Full execution detail in [`product-management-fy2026-q2/recruitment-sequence.md`](product-management-fy2026-q2/recruitment-sequence.md).

---

## Onboarding

Each VP goes through a 90-day onboarding organized in three 30-day phases: Immerse (Days 1–30) → Contribute (Days 31–60) → Lead (Days 61–90). The onboarding is designed as integration, not re-qualification — the VP has already passed selection; the 90 days are about calibration with Marcus's PRD standard, relationship-building with R&D and Design, and customer-signal immersion in their domain.

The primary instruments of the 90 days are:

- A **Landscape Memo** produced at Day 30: what the VP sees after immersion, top opportunities, top risks, first proposed quarterly bet
- A **co-authored PRD** shipped to Stage 2 during Days 31–60 — real work, not an exercise
- A **solo-authored PRD** and a **Q1 product roadmap** presented at Day 90

At Day 90, the CPO + CHRO + CTO hold a structured review conversation. Three possible outcomes: full commencement (pipeline authority transfers); course correction with a 30- or 60-day extension; or mutual decision to part. The third outcome is explicit in the plan because at VP tier it has to be on the table — not as a punitive hammer but as a mature leadership transition protocol.

Full detail in [`product-management-fy2026-q2/onboarding-plan/onboarding-plan.md`](product-management-fy2026-q2/onboarding-plan/onboarding-plan.md).

### What the Onboarding Produces

In addition to the integration of the VP themselves:

- Two new skill files: `web-product-strategy.md` (in VP Web's folder) and `api-product-strategy.md` (in VP API's folder), authored by the respective VP during Phase 3 and reviewed by the CPO.
- A revised `prd-authorship.md` — still owned by the CPO, but with Section 5 (Platform-Specific UX Constraints) generalized into Mobile / Web / API sub-sections. This is the single most important artifact produced by the 90-day cycle because it is what unlocks the Stage 1 authority transfer.

---

## Decision Rights After the Transfer

The Stage 1 authority transfer is not just a document update — it is a redistribution of decision rights across Product Management. The CPO retains three specific things:

1. **Template stewardship.** `prd-authorship.md` is a company-wide standard; the CPO owns it. VPs extend Section 5 for their domain; changes to Sections 1–4 or 6–8 require CPO sign-off.
2. **Final PRD sign-off on all pipelines.** A PRD does not advance to Stage 2 without the CPO's signature. VPs are the Responsible authors; the CPO is the Accountable approver.
3. **Arbitration authority.** For Full-Stack features that touch mobile, or for deadlocks between the two VPs, the CPO decides.

The VPs hold primary authorship, domain-specific judgment, and the authority to scope / frame / kill within their pipelines.

The pipeline amendments document specifies every decision-rights question and where it is resolved. [`product-management-fy2026-q2/pipeline-amendments/README.md`](product-management-fy2026-q2/pipeline-amendments/README.md).

---

## Scalability

The shape of the division after this plan is three Product Management people for four active pipelines. That is a working configuration for the current pipeline volume.

| Pipeline count | Division size needed | Notes                                                                                                                  |
| -------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 4 (today)      | 3 (post-plan)        | CPO + 2 VPs. Working configuration.                                                                                    |
| 5–6            | 3                    | Absorb growth through VP bandwidth; monitor for strain                                                                 |
| 7–8            | 4–5                  | Add a Director-tier PM under one of the VPs                                                                            |
| 9+             | 5–6                  | Consider CPO tier upgrade (Chief Product & Strategy Officer) and promote a VP or hire a second CPO under that umbrella |

The plan is sized for the current state, not pre-emptively scaled for speculative future pipeline counts. Pre-emptive scaling is how organizations accumulate overhead that later proves unnecessary.

---

## What This Plan Is Not

To be explicit about what we are not doing:

- **Not replacing Marcus.** He remains CPO with formalized scope.
- **Not promoting Marcus to a Chief Product & Strategy Officer tier.** Tier promotion is premature at a 4-pipeline scale. Reconsider at 9+ pipelines.
- **Not fragmenting the PRD template.** There is one template, with domain extensions.
- **Not creating a shared-accountability Stage 1 across three people for non-Full-Stack pipelines.** Each single-domain pipeline has a single named author. Full-Stack is the only joint-authorship case, and that is unavoidable because the feature itself spans domains.
- **Not running a probationary exam during onboarding.** The 90-day ramp is calibration, not re-selection.

---

## Decision Requested

The plan requires approval on three points:

1. **Recruitment authorization.** CHRO proceeds with parallel sourcing for VP Product, Web Platforms and VP Product, API & Developer Platforms.
2. **Hiring bar.** 20-point gate at ≥16/20, 4/5 minimum per category, non-negotiable cultural alignment, unanimous panel consensus.
3. **Authority transfer deferred until Day 90.** The CPO retains all Stage 1 authority during the 90-day onboarding; transfer executes per the pipeline amendments document after each VP's Day 90 gate.

### Pre-Execution Checklist

Items to complete before recruitment begins:

- [ ] User approves this plan
- [ ] CPO approves the competency matrices
- [ ] CPO approves the 90-day onboarding plan
- [ ] CTO co-signs the pipeline amendments document
- [ ] CSO, CIO, CDO acknowledge their role in panel interviews and onboarding sponsorship
- [ ] CHRO creates the `vp-product-api-platform/` folder (with empty `agent/` and `skills/` subfolders, matching the existing `vp-product-web-platform/` placeholder)
- [ ] CHRO confirms `recruit-product.md` is reserved for both funnels

---

## Document History

| Version | Date       | Changes                                                                                                                                                                                                                               | Status           |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| 1.0     | 2026-04-18 | Initial proposal. Structural argument for augmentation over replacement.                                                                                                                                                              | Superseded       |
| 2.0     | 2026-04-18 | Rewrite as a standalone Product Management initiative. 90-day onboarding replaces 30-day probationary model. Competency matrices reoriented around product-leadership dimensions. Authority transfer reframed around decision rights. | Pending Approval |

---

**Next step:** User + CPO approval. On approval, CHRO creates the `vp-product-api-platform/` placeholder folder and begins parallel sourcing.
