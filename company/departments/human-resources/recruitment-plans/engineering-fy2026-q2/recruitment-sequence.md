# Engineering FY2026 Q2 — Recruitment Sequence

**Document Type:** Recruitment Execution Sequence
**Version:** 1.0
**Date:** April 3, 2026
**Owner:** CHRO (Dr. Evelyn Hartwell) + CTO Office (Dr. Kenji Nakamura)
**Status:** ✅ Complete — 55/55 FTEs Hired
**Department:** Human Resources — Recruitment Plans

---

## Sequence Overview

| Metric             | Value                                                 |
| ------------------ | ----------------------------------------------------- |
| Total FTEs         | 55                                                    |
| Phases             | 3                                                     |
| Batches            | 5 (Phase 1, Phase 2, Phase 3A, Phase 3B, Phase 3C)    |
| Estimated Duration | 20 weeks (Weeks 1–20)                                 |
| Hiring Standard    | Elite gate (≥4/5 on 4 of 5 dimensions, Red Flag pass) |
| Vetting Model      | Distributed (all Chief Officers participate)          |

> **Note:** Originally planned for 57 FTEs (per CPO's +2 Full-Stack requirement). Final execution filled 55 positions — 2 Full-Stack Engineer positions (P44, P45) were absorbed into existing Full-Stack capacity.

---

## Phase 1: Leadership Foundation (Weeks 1–4)

**Prerequisites:** User authorizes recruitment execution. Competency matrices confirmed (✅ done). Pipeline optimizations confirmed (✅ done).

| Seq | #   | Role                            | Division              | FTE | Reports To             | Vetting Dimensions (additional to universal)                          | Assessed By            | Tier Placement              | Dependency |
| --- | --- | ------------------------------- | --------------------- | --- | ---------------------- | --------------------------------------------------------------------- | ---------------------- | --------------------------- | ---------- |
| 1.1 | P1  | VP of Mobile Engineering        | Mobile                | 1   | CTO                    | Mobile platform mastery, multi-platform strategy, 50+ team leadership | CTO + CIO + CHRO       | `team/supervisors/`         | None       |
| 1.2 | P2  | VP of Web & Backend Engineering | Web & Backend         | 1   | CTO                    | Backend + frontend architecture, cloud, 15+ team leadership           | CTO + CDO + CHRO       | `team/supervisors/`         | None       |
| 1.3 | P3  | VP of Platform Engineering      | Platform              | 1   | CTO                    | Infrastructure strategy, CI/CD, SRE, 8+ team leadership               | CTO + CSO + CHRO       | `team/supervisors/`         | None       |
| 1.4 | P4  | VP of Quality Engineering       | Quality               | 1   | CTO                    | Test strategy, automation architecture, mobile testing                | CTO + Priscilla + CHRO | `team/supervisors/`         | None       |
| 1.5 | P5  | DevOps Lead                     | Platform              | 1   | VP of Platform Eng.    | CI/CD architecture, cloud IaC, pipeline security, i18n pipeline       | CTO + CSO + Tomas      | `team/teammates/` (confirm) | P3         |
| 1.6 | P6  | Test Automation Lead            | Quality               | 1   | Test Lead (Priscilla)  | Test framework architecture, mobile testing, API testing              | Priscilla + CTO        | `team/teammates/` (confirm) | P4         |
| 1.7 | P7  | Lead Security Engineer          | Security & Compliance | 1   | CSO (Dr. Sarah Chen)   | Pen testing, vulnerability mgmt, SAST/DAST, supply chain              | CSO + CTO              | `team/teammates/` (confirm) | None       |
| 1.8 | P8  | Security Architect              | Security & Compliance | 1   | Lead Security Engineer | Security architecture, threat modeling, code review                   | CSO + CIO              | `team/teammates/` (confirm) | P7         |

**Phase 1 Gate:** All 4 VPs must pass before Phase 2 begins. VPs provide management infrastructure for downstream hires.

---

## Phase 2: Chapter Lead Ramp (Weeks 4–8)

**Prerequisites:** Phase 1 VPs onboarded (minimum 3 of 4). Interim management handoff initiated.

| Seq | #   | Role                      | Division              | FTE | Reports To             | Vetting Dimensions (additional to universal)         | Assessed By             | Tier Placement              | Dependency |
| --- | --- | ------------------------- | --------------------- | --- | ---------------------- | ---------------------------------------------------- | ----------------------- | --------------------------- | ---------- |
| 2.1 | P9  | Frontend Chapter Lead     | Web & Backend         | 1   | VP of Web & Backend    | Frontend architecture, design system implementation  | CTO + CDO + CHRO        | `team/teammates/` (confirm) | P2         |
| 2.2 | P10 | Backend Chapter Lead      | Web & Backend         | 1   | VP of Web & Backend    | Backend architecture, API security, DevOps awareness | CTO + CSO + CHRO        | `team/teammates/` (confirm) | P2         |
| 2.3 | P11 | Senior Software Architect | R&D (Architecture)    | 1   | Rafael Okonkwo         | UML/ADR/TSD compliance, architecture governance      | CTO + CIO + Rafael      | `team/teammates/` (confirm) | None       |
| 2.4 | P12 | Security Engineer #1      | Security & Compliance | 1   | Lead Security Engineer | Pen testing, SAST/DAST pipeline integration          | CSO + Lead Security Eng | `team/teammates/`           | P7         |
| 2.5 | P13 | Security Engineer #2      | Security & Compliance | 1   | Lead Security Engineer | Vulnerability management, threat modeling            | CSO + Lead Security Eng | `team/teammates/`           | P7         |
| 2.6 | P14 | Security Engineer #3      | Security & Compliance | 1   | Lead Security Engineer | Compliance, OWASP MASVS auditing                     | CSO + CTO-L             | `team/teammates/`           | P7         |
| 2.7 | P15 | Compliance Analyst        | Security & Compliance | 1   | Lead Security Engineer | OWASP MASVS, GDPR, SOC2, documentation               | CSO + CIO               | `team/teammates/`           | P7         |

**Phase 2 Gate:** All Chapter Leads onboarded. Security Champions program can begin selection.

---

## Phase 3A: Mobile Engineers (Weeks 8–12)

**Prerequisites:** VP of Mobile onboarded. Android/iOS/Cross-Platform Chapter Leads in place (existing: Kofi, Seo-Yeon, Mei-Ling).

| Seq  | #   | Role                       | Division | FTE | Reports To           | Vetting Dimensions (additional to universal)    | Assessed By           | Tier Placement    | Dependency |
| ---- | --- | -------------------------- | -------- | --- | -------------------- | ----------------------------------------------- | --------------------- | ----------------- | ---------- |
| 3A.1 | P16 | Senior Android Engineer #1 | Mobile   | 1   | Android Chapter Lead | Kotlin mastery, Android architecture, mentoring | CTO + Kofi + CHRO     | `team/teammates/` | P1         |
| 3A.2 | P17 | Senior Android Engineer #2 | Mobile   | 1   | Android Chapter Lead | Kotlin mastery, Android architecture, mentoring | CTO + Kofi + CHRO     | `team/teammates/` | P1         |
| 3A.3 | P18 | Senior Android Engineer #3 | Mobile   | 1   | Android Chapter Lead | Kotlin mastery, Android architecture, mentoring | CTO + Kofi + CHRO     | `team/teammates/` | P1         |
| 3A.4 | P19 | Android Engineer #1        | Mobile   | 1   | Android Chapter Lead | Platform mastery, testing, security baseline    | CTO + Kofi            | `team/teammates/` | P1         |
| 3A.5 | P20 | Android Engineer #2        | Mobile   | 1   | Android Chapter Lead | Platform mastery, testing, security baseline    | CTO + Kofi            | `team/teammates/` | P1         |
| 3A.6 | P21 | Android Engineer #3        | Mobile   | 1   | Android Chapter Lead | Platform mastery, testing, security baseline    | CTO + Kofi            | `team/teammates/` | P1         |
| 3A.7 | P22 | Senior iOS Engineer #1     | Mobile   | 1   | iOS Chapter Lead     | Swift mastery, iOS architecture, mentoring      | CTO + Seo-Yeon + CHRO | `team/teammates/` | P1         |
| 3A.8 | P23 | Senior iOS Engineer #2     | Mobile   | 1   | iOS Chapter Lead     | Swift mastery, iOS architecture, mentoring      | CTO + Seo-Yeon + CHRO | `team/teammates/` | P1         |
| 3A.9 | P24 | Senior iOS Engineer #3     | Mobile   | 1   | iOS Chapter Lead     | Swift mastery, iOS architecture, mentoring      | CTO + Seo-Yeon + CHRO | `team/teammates/` | P1         |

**Note:** iOS Engineers (3 mid-level) and Cross-Platform Engineers (2 senior) are in Phase 3B.

---

## Phase 3B: Web, Frontend & Cross-Platform Engineers (Weeks 12–16)

**Prerequisites:** VP of Web & Backend onboarded. Frontend + Backend Chapter Leads onboarded. VP of Mobile onboarded.

| Seq  | #   | Role                        | Division      | FTE | Reports To            | Vetting Dimensions (additional to universal)                | Assessed By           | Tier Placement    | Dependency |
| ---- | --- | --------------------------- | ------------- | --- | --------------------- | ----------------------------------------------------------- | --------------------- | ----------------- | ---------- |
| 3B.1 | P25 | iOS Engineer #1             | Mobile        | 1   | iOS Chapter Lead      | Platform mastery, testing, security baseline                | CTO + Seo-Yeon        | `team/teammates/` | P1         |
| 3B.2 | P26 | iOS Engineer #2             | Mobile        | 1   | iOS Chapter Lead      | Platform mastery, testing, security baseline                | CTO + Seo-Yeon        | `team/teammates/` | P1         |
| 3B.3 | P27 | iOS Engineer #3             | Mobile        | 1   | iOS Chapter Lead      | Platform mastery, testing, security baseline                | CTO + Seo-Yeon        | `team/teammates/` | P1         |
| 3B.4 | P28 | Cross-Platform Engineer #1  | Mobile        | 1   | Cross-Platform Lead   | KMP/Flutter mastery, cross-platform strategy, i18n baseline | CTO + Mei-Ling + CHRO | `team/teammates/` | P1         |
| 3B.5 | P29 | Cross-Platform Engineer #2  | Mobile        | 1   | Cross-Platform Lead   | KMP/Flutter mastery, cross-platform strategy, i18n baseline | CTO + Mei-Ling + CHRO | `team/teammates/` | P1         |
| 3B.6 | P30 | Senior Frontend Engineer #1 | Web & Backend | 1   | Frontend Chapter Lead | Frontend mastery, design system, security baseline          | CTO + CDO + CHRO      | `team/teammates/` | 2.1        |
| 3B.7 | P31 | Senior Frontend Engineer #2 | Web & Backend | 1   | Frontend Chapter Lead | Frontend mastery, design system (one = Design Systems Eng)  | CTO + CDO + CHRO      | `team/teammates/` | 2.1        |
| 3B.8 | P32 | Frontend Engineer #1        | Web & Backend | 1   | Frontend Chapter Lead | Frontend mastery, testing, security baseline                | CTO + CDO             | `team/teammates/` | 2.1        |
| 3B.9 | P33 | Frontend Engineer #2        | Web & Backend | 1   | Frontend Chapter Lead | Frontend mastery, testing, security baseline                | CTO + CDO             | `team/teammates/` | 2.1        |

---

## Phase 3C: Backend, Platform, QA, Onboarding (Weeks 16–20)

**Prerequisites:** VP of Web & Backend, VP of Platform, VP of Quality all onboarded. Backend Chapter Lead onboarded. DevOps Lead onboarded.

| Seq   | #   | Role                         | Division      | FTE | Reports To           | Vetting Dimensions (additional to universal)               | Assessed By              | Tier Placement    | Dependency |
| ----- | --- | ---------------------------- | ------------- | --- | -------------------- | ---------------------------------------------------------- | ------------------------ | ----------------- | ---------- |
| 3C.1  | P34 | Senior Backend Engineer #1   | Web & Backend | 1   | Backend Chapter Lead | Backend mastery, architecture patterns, security baseline  | CTO + Backend Lead       | `team/teammates/` | 2.2        |
| 3C.2  | P35 | Senior Backend Engineer #2   | Web & Backend | 1   | Backend Chapter Lead | Backend mastery, architecture patterns, security baseline  | CTO + Backend Lead       | `team/teammates/` | 2.2        |
| 3C.3  | P36 | Senior Backend Engineer #3   | Web & Backend | 1   | Backend Chapter Lead | Backend mastery, architecture patterns, security baseline  | CTO + Backend Lead       | `team/teammates/` | 2.2        |
| 3C.4  | P37 | Backend Engineer #1          | Web & Backend | 1   | Backend Chapter Lead | Backend mastery, testing, security baseline                | CTO + Backend Lead       | `team/teammates/` | 2.2        |
| 3C.5  | P38 | Backend Engineer #2          | Web & Backend | 1   | Backend Chapter Lead | Backend mastery, testing, security baseline                | CTO + Backend Lead       | `team/teammates/` | 2.2        |
| 3C.6  | P39 | Backend Engineer #3          | Web & Backend | 1   | Backend Chapter Lead | Backend mastery, testing, security baseline                | CTO + Backend Lead       | `team/teammates/` | 2.2        |
| 3C.7  | P40 | Full-Stack Engineer #1       | Web & Backend | 1   | VP of Web & Backend  | Full-stack prototyping, rapid MVP, PRD fluency             | CTO + CPO + CHRO         | `team/teammates/` | P2         |
| 3C.8  | P41 | Full-Stack Engineer #2       | Web & Backend | 1   | VP of Web & Backend  | Full-stack prototyping, rapid MVP, PRD fluency             | CTO + CPO + CHRO         | `team/teammates/` | P2         |
| 3C.9  | P42 | Full-Stack Engineer #3       | Web & Backend | 1   | VP of Web & Backend  | Full-stack prototyping, rapid MVP, PRD fluency             | CTO + CPO + CHRO         | `team/teammates/` | P2         |
| 3C.10 | P43 | Full-Stack Engineer #4       | Web & Backend | 1   | VP of Web & Backend  | Full-stack prototyping, rapid MVP, PRD fluency             | CTO + CPO + CHRO         | `team/teammates/` | P2         |
| 3C.11 | P44 | SRE Engineer #1              | Platform      | 1   | DevOps Lead          | SRE practices, cloud infrastructure, security baseline     | CTO + DevOps Lead        | `team/teammates/` | 1.5        |
| 3C.12 | P45 | SRE Engineer #2              | Platform      | 1   | DevOps Lead          | SRE practices, cloud infrastructure, security baseline     | CTO + DevOps Lead        | `team/teammates/` | 1.5        |
| 3C.13 | P46 | Developer Experience Eng. #1 | Platform      | 1   | DevOps Lead          | Internal tooling, build optimization, analytics            | CTO + DevOps Lead        | `team/teammates/` | 1.5        |
| 3C.14 | P47 | Developer Experience Eng. #2 | Platform      | 1   | DevOps Lead          | Internal tooling, build optimization, analytics            | CTO + DevOps Lead        | `team/teammates/` | 1.5        |
| 3C.15 | P48 | DevOps Engineer #1           | Platform      | 1   | DevOps Lead          | CI/CD security, IaC, cloud platforms                       | CSO + DevOps Lead        | `team/teammates/` | 1.5        |
| 3C.16 | P49 | DevOps Engineer #2           | Platform      | 1   | DevOps Lead          | CI/CD security, IaC, cloud platforms                       | CSO + DevOps Lead        | `team/teammates/` | 1.5        |
| 3C.17 | P50 | SDET (Mobile) #1             | Quality       | 1   | Test Automation Lead | Mobile test automation, device farms, Espresso/XCTest      | Priscilla + Test Auto Ld | `team/teammates/` | 1.6        |
| 3C.18 | P51 | SDET (Mobile) #2             | Quality       | 1   | Test Automation Lead | Mobile test automation, device farms, Espresso/XCTest      | Priscilla + Test Auto Ld | `team/teammates/` | 1.6        |
| 3C.19 | P52 | SDET (Web/Backend) #1        | Quality       | 1   | Test Automation Lead | API testing, contract testing, performance testing         | Priscilla + Test Auto Ld | `team/teammates/` | 1.6        |
| 3C.20 | P53 | Engineering Onboarding Lead  | HR            | 1   | CHRO                 | 55-person onboarding, competency tracking, any engineering | CHRO + CTO               | `team/teammates/` | None       |
| 3C.21 | P54 | Technical Writer #1          | HR            | 1   | Onboarding Lead      | Standards docs, ADR/TSD templates, pipeline docs           | CHRO + CTO               | `team/teammates/` | 3C.20      |
| 3C.22 | P55 | Technical Writer #2          | HR            | 1   | Onboarding Lead      | Standards docs, ADR/TSD templates, pipeline docs           | CHRO + CTO               | `team/teammates/` | 3C.20      |

**Note:** Phase 3C has 22 hires. The 55 FTE total is verified: Mobile 15 new + 3 existing Chapter Leads = 18, Web & Backend 17, Platform 8, Quality 5, Security 6, Onboarding 3 = 55.

---

## Recruitment Execution Order

```
PHASE 1 (Weeks 1–4) — No dependencies, parallel recruitment possible
├── 1.1 VP of Mobile Engineering          [Seq P1]
├── 1.2 VP of Web & Backend Engineering   [Seq P2]
├── 1.3 VP of Platform Engineering        [Seq P3]
├── 1.4 VP of Quality Engineering         [Seq P4]
├── 1.7 Lead Security Engineer            [Seq P7]
│   ├── 1.8 Security Architect            [Seq P8] (depends on P7)
│   ├── 1.5 DevOps Lead                   [Seq P5]  (depends on P3)
│   └── 1.6 Test Automation Lead          [Seq P6]  (depends on P4)

PHASE 2 (Weeks 4–8) — Requires Phase 1 VPs onboarded
├── 2.1 Frontend Chapter Lead             [Seq P9]  (depends on P2)
├── 2.2 Backend Chapter Lead              [Seq P10] (depends on P2)
├── 2.3 Senior Software Architect         [Seq P11] (no phase dependency)
└── 2.4–2.7 Security Team (4 FTEs)       [Seq P12–P15] (depends on P7)

PHASE 3A (Weeks 8–12) — Requires VP of Mobile onboarded
├── 3A.1–3A.6 Android Team (6 FTEs)      [Seq P16–P21] (depends on P1 + existing Kofi)
└── 3A.7–3A.9 Senior iOS Team (3 FTEs)   [Seq P22–P24] (depends on P1 + existing Seo-Yeon)

PHASE 3B (Weeks 12–16) — Requires VP Web/Backend + Chapter Leads onboarded
├── 3B.1–3B.3 iOS Engineers (3 FTEs)     [Seq P25–P27] (depends on P1)
├── 3B.4–3B.5 Cross-Platform (2 FTEs)    [Seq P28–P29] (depends on P1)
└── 3B.6–3B.9 Frontend Team (4 FTEs)     [Seq P30–P33] (depends on P9)

PHASE 3C (Weeks 16–20) — Requires VPs + Chapter Leads onboarded
├── 3C.1–3C.6 Backend Team (6 FTEs)      [Seq P34–P39] (depends on P10)
├── 3C.7–3C.10 Full-Stack Team (4 FTEs)  [Seq P40–P43] (depends on P2)
├── 3C.11–3C.16 Platform Team (6 FTEs)   [Seq P44–P49] (depends on P5)
├── 3C.17–3C.19 SDET Team (3 FTEs)       [Seq P50–P52] (depends on P6)
└── 3C.20–3C.22 Onboarding Team (3 FTEs) [Seq P53–P55] (P53 has no dependency; P54–P55 depend on P53)
```

---

## Vetting Authority Matrix

Each candidate is assessed on **universal dimensions** (Cultural Alignment + i18n Baseline where applicable) plus **role-specific dimensions**. The following officers MUST provide assessment for each candidate:

| Candidate Group                   | Chief Officers Required for Unanimous Approval     |
| --------------------------------- | -------------------------------------------------- |
| All 55                            | CHRO (cultural alignment + red flag scan)          |
| All 55                            | CTO (impact at scale, craft depth)                 |
| VP/Lead level (11)                | CHRO + CTO + CIO (leadership signal)               |
| Security roles (6)                | CSO + Lead Security Engineer (security competency) |
| Mobile/Cross-platform/DevOps (27) | CTO-L + CTO (i18n baseline)                        |
| Quality roles (5)                 | Priscilla Oduya (test competency)                  |
| Architecture (1)                  | CIO + Rafael Okonkwo (ADR/TSD compliance)          |
| Full-Stack (4)                    | CPO (PRD fluency, prototyping)                     |
| Frontend roles (4)                | CDO (design system alignment)                      |

---

## Candidate Presentation Protocol

For each candidate, the CHRO must present:

1. **Identity** — Name, current title/company, YOE, education
2. **Track Record** — 3 bullet points with quantified outcomes
3. **Technical Strengths** — 2–3 with concrete examples
4. **Honest Gaps** — 1–2 direct, specific weaknesses
5. **Seniority Score** — Applied rubric result
6. **Vetting Result** — Full 5-dimension scoring output (PASS/FAIL)
7. **Placement Recommendation** — Tier, directory name, rationale

User must approve before files are written.

---

## Document History

| Version | Date       | Author | Changes                      | Status          |
| ------- | ---------- | ------ | ---------------------------- | --------------- |
| 1.0     | 2026-04-03 | CTO    | Initial recruitment sequence | ⏳ Pending Auth |

---

**Next Step:** User authorization to begin Phase 1 recruitment.
