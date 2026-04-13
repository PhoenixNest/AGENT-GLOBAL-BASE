# Tools Engineer Hire-or-Contract Decision

**Owner:** Dr. Kenji Nakamura, CTO — Parent Company R&D
**Studio:** Casual Games Studio
**Date:** 2026-04-12
**Pipeline Stage:** Stage 4 (Implementation Plan) — Pre-Gate Deliverable
**Audit Reference:** CTO Audit Condition **C3** — Tools Engineer Hire-or-Contract Decision by Stage 4 Gate

---

## 1. Purpose

This document establishes a structured decision framework for whether the Casual Games Studio should hire a dedicated Tools Engineer (FTE), engage a contractor, or defer the hire. It satisfies **CTO Audit Condition C3**, which requires a formal decision process with documented criteria before Stage 4 Gate approval.

The question is not "do we need tools engineering?" — we clearly do. The question is "what is the optimal resourcing model given our current trajectory, complexity, and budget?" This document provides the analytical basis for that decision.

---

## 2. Decision Criteria

Four criteria have been selected based on their direct impact on tools engineering workload. Each is scored on a 1–5 scale (1 = minimal impact, 5 = critical impact).

### 2.1 Criterion Definitions

| #   | Criterion                 | Definition                                                                                          | Data Source                            |
| --- | ------------------------- | --------------------------------------------------------------------------------------------------- | -------------------------------------- |
| C1  | **Build Complexity**      | Number of build targets, platform variants, and configuration permutations that require tooling     | Architecture UML, ADRs, TSD            |
| C2  | **Iteration Speed**       | Current developer feedback loop duration; frequency of build-related friction reports               | DEVELOPMENT-LOG.md, developer surveys  |
| C3  | **Asset Pipeline Load**   | Volume and complexity of asset processing (textures, audio, localization, DLC) requiring automation | Asset manifest, art team capacity plan |
| C4  | **Second Title Planning** | Whether a second game title is planned within 12 months, requiring scalable tooling infrastructure  | Product roadmap, Studio Director plan  |

### 2.2 Scoring Guide

| Score | Build Complexity             | Iteration Speed                    | Asset Pipeline Load                 | Second Title Planning               |
| ----- | ---------------------------- | ---------------------------------- | ----------------------------------- | ----------------------------------- |
| **1** | Single target, no variants   | < 2 min build, zero friction       | < 100 assets, no processing         | No second title planned             |
| **2** | 2 targets, 1 variant each    | 2–5 min build, occasional friction | 100–500 assets, basic processing    | Second title under discussion       |
| **3** | 3–4 targets, 2 variants each | 5–10 min build, regular friction   | 500–2000 assets, moderate pipeline  | Second title confirmed, 12+ months  |
| **4** | 5+ targets, 3+ variants      | 10–20 min build, daily friction    | 2000–5000 assets, complex pipeline  | Second title confirmed, 6–12 months |
| **5** | 5+ targets, 5+ variants, KMP | > 20 min build, blocking friction  | > 5000 assets, multi-stage pipeline | Second title confirmed, < 6 months  |

---

## 3. Options

### Option A: Hire Full-Time Employee (FTE)

| Attribute       | Detail                                                                                                   |
| --------------- | -------------------------------------------------------------------------------------------------------- |
| **Description** | Recruit a dedicated Tools Engineer as a permanent studio team member                                     |
| **Timeline**    | 8–12 weeks (recruitment via CHRO pipeline) + 4 weeks onboarding                                          |
| **Cost**        | $120K–$160K/year (salary + benefits + equipment)                                                         |
| **Pros**        | Deep institutional knowledge; full availability; long-term investment; can own tools strategy end-to-end |
| **Cons**        | Slow to hire; high fixed cost; risk if scope changes or project is cancelled                             |
| **Best when**   | Scores ≥ 3 on ≥ 3 criteria; second title confirmed within 12 months                                      |

### Option B: Contract / Freelance

| Attribute       | Detail                                                                                                          |
| --------------- | --------------------------------------------------------------------------------------------------------------- |
| **Description** | Engage a contract Tools Engineer (3–6 month engagement, renewable)                                              |
| **Timeline**    | 2–4 weeks (contractor procurement)                                                                              |
| **Cost**        | $80–$150/hour × ~160 hours/month = $12.8K–$24K/month                                                            |
| **Pros**        | Fast to onboard; flexible; no long-term commitment; bring in specialized expertise                              |
| **Cons**        | Less institutional knowledge; higher hourly cost; knowledge transfer risk; availability tied to contract period |
| **Best when**   | Scores are 2–3 on most criteria; immediate need but uncertain long-term scope                                   |

### Option C: Defer

| Attribute       | Detail                                                                                                                 |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Description** | No dedicated Tools Engineer; distribute tools work across existing team                                                |
| **Timeline**    | N/A — current state maintained                                                                                         |
| **Cost**        | $0 incremental (but hidden cost in developer productivity loss)                                                        |
| **Pros**        | No new headcount; team maintains broad skill exposure                                                                  |
| **Cons**        | Build times remain unoptimized; developer productivity loss compounds; tools debt accumulates; blocks Stage 5 velocity |
| **Best when**   | All scores ≤ 2; first title is lightweight; no second title planned                                                    |

---

## 4. Stage 4 Assessment Process

### 4.1 Data Collection (Stage 4, Weeks 1–2)

| Activity                                | Owner                    | Output                              | Deadline      |
| --------------------------------------- | ------------------------ | ----------------------------------- | ------------- |
| Review UML diagrams for build targets   | CTO (Dr. Kenji Nakamura) | Build target count                  | Week 1, Day 3 |
| Review ADRs for platform decisions      | CTO (Dr. Kenji Nakamura) | Platform variant count              | Week 1, Day 5 |
| Interview Dmitri Volkov on build times  | CTO (Dr. Kenji Nakamura) | Current build metrics               | Week 2, Day 1 |
| Survey developer team on build friction | CTO (Dr. Kenji Nakamura) | Friction frequency data             | Week 2, Day 3 |
| Review asset manifest with art lead     | Studio Director          | Asset count + processing complexity | Week 2, Day 4 |
| Confirm second title roadmap            | Studio Director + CPO    | Title planning status               | Week 2, Day 5 |

### 4.2 Scoring Workshop (Stage 4, Week 3)

| Activity                          | Participants                        | Duration |
| --------------------------------- | ----------------------------------- | -------- |
| Score each criterion (C1–C4)      | CTO, Studio Director, Dmitri Volkov | 2 hours  |
| Map scores to decision matrix     | CTO                                 | 1 hour   |
| Document rationale for each score | CTO                                 | 1 hour   |

### 4.3 Decision Gate (Stage 4, Week 4)

| Decision Rule                                | Outcome                                                        |
| -------------------------------------------- | -------------------------------------------------------------- |
| **≥ 3 criteria score ≥ 4**                   | **Hire FTE** (Option A)                                        |
| **≥ 2 criteria score ≥ 3 AND any score = 4** | **Hire FTE** (Option A)                                        |
| **All scores 2–3**                           | **Contract** (Option B)                                        |
| **All scores ≤ 2**                           | **Defer** (Option C)                                           |
| **Mixed (some 5, some 1)**                   | **Contract** (Option B) with 3-month review for FTE conversion |

### 4.4 Stage 4 Gate Deliverable

The completed decision — including scores, rationale, and final recommendation — will be appended to this document and presented at the Stage 4 Gate review as evidence of **C3** compliance.

---

## 5. Preliminary Assessment (Pre-Data Collection)

_The following is a preliminary assessment based on current known information. Final scores require the Stage 4 data collection process described in Section 4._

| Criterion                 | Preliminary Score | Rationale                                                      |
| ------------------------- | :---------------: | -------------------------------------------------------------- |
| **Build Complexity**      |        TBD        | ADRs and UML still in progress; target count unknown           |
| **Iteration Speed**       |        TBD        | No builds running yet; baseline must be established in Stage 5 |
| **Asset Pipeline Load**   |        TBD        | Asset manifest not finalized; depends on game design           |
| **Second Title Planning** |        TBD        | No confirmed second title; roadmap pending CPO alignment       |
| **Preliminary Decision**  |    **Assess**     | Cannot score until Stage 4 data collection completes           |

**Important:** This preliminary assessment will be updated after the Stage 4, Week 3 scoring workshop. The final decision will be documented in Section 6 below.

---

## 6. Final Decision (Post-Assessment)

_To be completed during Stage 4, Week 4._

| Field                     | Value                                                                   |
| ------------------------- | ----------------------------------------------------------------------- |
| **Build Complexity**      |                                                                         |
| **Iteration Speed**       |                                                                         |
| **Asset Pipeline Load**   |                                                                         |
| **Second Title Planning** |                                                                         |
| **Decision Rule Met**     |                                                                         |
| **Final Decision**        | ⬜ Option A — Hire FTE<br>⬜ Option B — Contract<br>⬜ Option C — Defer |
| **Rationale**             |                                                                         |
| **Next Steps**            |                                                                         |
| **Assessed By**           | Dr. Kenji Nakamura                                                      |
| **Assessment Date**       |                                                                         |

---

## 7. Audit Condition C3 Compliance Checklist

| Requirement                                                                             | Status      | Evidence Location                                         |
| --------------------------------------------------------------------------------------- | ----------- | --------------------------------------------------------- |
| Decision framework documented                                                           | ✅ Complete | This document                                             |
| Four criteria defined (build complexity, iteration speed, asset pipeline, second title) | ✅ Complete | Section 2.1 + 2.2                                         |
| Three options evaluated (hire FTE, contract, defer)                                     | ✅ Complete | Section 3                                                 |
| Scoring methodology defined                                                             | ✅ Complete | Section 2.2 — Scoring Guide                               |
| Decision rules mapped to score thresholds                                               | ✅ Complete | Section 4.3 — Decision Gate                               |
| Stage 4 assessment process documented                                                   | ✅ Complete | Section 4 — Stages 4.1 through 4.4                        |
| Preliminary assessment placeholder                                                      | ✅ Complete | Section 5                                                 |
| Final decision section ready for completion                                             | ✅ Complete | Section 6                                                 |
| Stage 4 Gate ready                                                                      | ✅ Complete | Framework complete; data collection begins Stage 4 Week 1 |

---

## 8. Sign-Off

| Role                       | Name                | Signature | Date       |
| -------------------------- | ------------------- | --------- | ---------- |
| **CTO (Author)**           | Dr. Kenji Nakamura  |           | 2026-04-12 |
| **Studio Director**        |                     |           |            |
| **CHRO** (if FTE selected) | Dr. Evelyn Hartwell |           |            |

---

_Audit Condition C3 — Framework satisfied. Data collection and final decision to be completed during Stage 4. Document ready for Stage 4 Gate review._
