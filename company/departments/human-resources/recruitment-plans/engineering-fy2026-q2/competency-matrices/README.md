# Engineering Competency Matrices — FY2026 Q2 Recruitment

**Document Type:** Role-Specific Competency Matrices
**Version:** 1.1 (v1.6 Recruitment Plan Alignment — i18n baseline + cultural alignment added)
**Date:** April 3, 2026
**Owner:** All Chief Officers
**Purpose:** Explicit evaluation criteria for all 57 engineering candidates. Replaces generic responsibility lists with measurable competency dimensions.
**Status:** ✅ Approved — Ready for HR Evaluation Use

---

## Universal Dimensions (Applied to ALL Matrices)

### Cultural Alignment (Non-Negotiable Minimum Bar)

| Dimension              | Assessed By           | Criteria                                                                                                                     | Minimum Bar                                                  |
| ---------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Cultural alignment** | CHRO + Hiring Manager | Low ego, high self-esteem, open-mindedness, strong communication, ruthless prioritization, psychological safety contribution | Demonstrated through behavioral interview + reference checks |

### i18n Baseline (Mobile/Cross-platform/DevOps Candidates Only)

| Dimension         | Assessed By | Criteria                                                                                                                                                                           | Minimum Bar                                                                         |
| ----------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **i18n baseline** | CTO-L + CTO | Knowledge of platform resource file conventions (`strings.xml`, `Localizable.strings`), string extraction principles, difference between hardcoded strings and resource references | Can explain resource file architecture and demonstrate basic string externalization |

---

## VP-Level Competency Matrices

### VP of Mobile Engineering

| Dimension                       | Assessed By | Criteria                                                                                             | Minimum Bar                                                                 |
| ------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Mobile platform mastery         | CTO         | 10+ years across Android + iOS; shipped 3+ apps with 1M+ users                                       | Principal-level depth                                                       |
| Multi-platform strategy         | CTO + CIO   | KMP, Flutter, native trade-off analysis; TSD alignment                                               | Can justify platform decisions with data                                    |
| Team leadership (50+ engineers) | CHRO + CTO  | Built and scaled mobile orgs; retention metrics; promotion track record                              | 2+ orgs scaled from 10→50+                                                  |
| Security awareness              | CSO         | OWASP MASVS familiarity; mobile threat modeling; secure SDLC                                         | Can lead security review of mobile codebase                                 |
| Pipeline ownership              | CTO         | Stage 5 (Development), Stage 8 (Integrity Verification) execution                                    | Can run Stage 5 without CTO hand-holding                                    |
| Cross-functional collaboration  | CPO + CDO   | Works with Product and Design; understands PRD/IDS handoff                                           | No "engineering-only" mindset                                               |
| **Product Liaison governance**  | **CPO**     | **Designates and manages Product Liaisons in each mobile chapter; ensures PRD fluency**              | **Can translate PRD intent into chapter-level engineering priorities**      |
| **i18n strategy**               | **CTO-L**   | **Understanding of multi-platform resource file architecture; string extraction pipeline awareness** | **Can articulate i18n best practices for Android, iOS, and cross-platform** |
| Cultural alignment              | CHRO + CTO  | Low ego, high self-esteem, open-mindedness, strong communication                                     | Behavioral interview + references                                           |

### VP of Web & Backend Engineering

| Dimension                       | Assessed By | Criteria                                                     | Minimum Bar                                  |
| ------------------------------- | ----------- | ------------------------------------------------------------ | -------------------------------------------- |
| Backend architecture            | CTO         | Microservices, API design, distributed systems; 10+ years    | Shipped production systems at scale          |
| Frontend architecture           | CTO + CDO   | React/Vue/Angular; design system implementation; performance | Can bridge frontend + design                 |
| Team leadership (15+ engineers) | CHRO + CTO  | Built and scaled web/backend teams; mentoring track record   | 1+ team scaled from 5→15+                    |
| Cloud infrastructure            | CTO         | AWS/GCP/Azure; containerization; CI/CD                       | Can design cloud architecture from scratch   |
| Security awareness              | CSO         | API security, auth patterns, OWASP Top 10                    | Can lead security review of backend codebase |
| Full-stack prototyping          | CPO         | Rapid prototyping; MVP delivery; user feedback integration   | Can prototype end-to-end features            |

### VP of Platform Engineering

| Dimension                      | Assessed By | Criteria                                                         | Minimum Bar                              |
| ------------------------------ | ----------- | ---------------------------------------------------------------- | ---------------------------------------- |
| Infrastructure strategy        | CTO         | Cloud architecture, IaC, service mesh, API gateway               | Designed infrastructure for 10+ services |
| CI/CD pipeline design          | CTO + Tomas | Multi-platform build systems; pipeline security; automation      | Built CI/CD for 5+ concurrent projects   |
| SRE practices                  | CTO         | Incident response, on-call, SLO/SLI, error budgets               | Run production SRE for 2+ years          |
| Developer Experience           | CTO         | Internal tooling, build optimization, onboarding automation      | Reduced developer friction measurably    |
| Security integration           | CSO         | Pipeline security, secrets management, supply chain security     | Can design secure CI/CD from scratch     |
| Team leadership (8+ engineers) | CHRO + CTO  | Built and scaled platform/infra teams                            | 1+ platform team scaled                  |
| Cultural alignment             | CHRO + CTO  | Low ego, high self-esteem, open-mindedness, strong communication | Behavioral interview + references        |

### VP of Quality Engineering

| Dimension                    | Assessed By     | Criteria                                                                                                                                                                                            | Minimum Bar                                                                           |
| ---------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Test strategy                | CTO + Priscilla | Unit, integration, E2E, regression; test pyramid design                                                                                                                                             | Designed test strategy for 3+ products                                                |
| Test automation architecture | Priscilla + CTO | Framework design, CI integration, flaky test mitigation                                                                                                                                             | Built test frameworks from scratch                                                    |
| Quality metrics              | CTO             | Defect tracking, coverage analysis, quality dashboards                                                                                                                                              | Can define and track quality KPIs                                                     |
| Team leadership (5+ SDETs)   | CHRO + CTO      | Built and scaled QA/test teams                                                                                                                                                                      | 1+ QA team scaled                                                                     |
| Mobile testing               | Priscilla       | Device farms, emulator strategy, platform-specific testing                                                                                                                                          | Tested apps on both Android + iOS                                                     |
| Release gate authority       | CTO + CPO       | Independent quality judgment; can block releases                                                                                                                                                    | No "ship it" pressure compliance                                                      |
| **Product risk calibration** | **CPO**         | **Demonstrated ability to distinguish between user-impacting defects and technical-only defects; understands that a P1 from a user perspective may be a P3 from a code perspective and vice versa** | **Can calibrate defect severity against user impact, not just technical correctness** |
| Cultural alignment           | CHRO + CTO      | Low ego, high self-esteem, open-mindedness, strong communication                                                                                                                                    | Behavioral interview + references                                                     |

---

## Chapter Lead Competency Matrices

### Android Chapter Lead (Kofi Asante-Mensah — Existing)

| Dimension            | Assessed By                  | Criteria                                                                                                       |
| -------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Kotlin mastery       | CTO                          | Coroutines, flows, KMP, memory model                                                                           |
| Android architecture | Kofi (self-assessment) + CTO | MVVM, Clean Architecture, MVI, StateFlow                                                                       |
| Team leadership      | CHRO + CTO                   | Mentoring, code review, technical decision-making                                                              |
| Security awareness   | CSO                          | OWASP MASVS, Keystore, Play Integrity API                                                                      |
| Pipeline ownership   | CTO                          | Stage 5 (Development), Stage 8 (Integrity Verification)                                                        |
| **i18n baseline**    | **CTO-L + CTO**              | **`strings.xml` conventions, string extraction, hardcoded vs. resource references, indexed format specifiers** |
| Cultural alignment   | CHRO + Hiring Manager        | Low ego, high self-esteem, open-mindedness, strong communication                                               |

### iOS Chapter Lead (Seo-Yeon Park — Existing)

| Dimension          | Assessed By                      | Criteria                                                                                                              |
| ------------------ | -------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Swift mastery      | CTO                              | Swift Concurrency, actors, Combine, async/await                                                                       |
| iOS architecture   | Seo-Yeon (self-assessment) + CTO | MVVM, TCA, SwiftUI, UIKit interoperability                                                                            |
| Team leadership    | CHRO + CTO                       | Mentoring, code review, technical decision-making                                                                     |
| Security awareness | CSO                              | OWASP MASVS, Keychain, ATS, certificate pinning                                                                       |
| Pipeline ownership | CTO                              | Stage 5 (Development), Stage 8 (Integrity Verification)                                                               |
| **i18n baseline**  | **CTO-L + CTO**                  | **`Localizable.strings` conventions, `NSLocalizedString`, format specifiers (`%@`), `stringsdict` for pluralization** |
| Cultural alignment | CHRO + Hiring Manager            | Low ego, high self-esteem, open-mindedness, strong communication                                                      |

### Cross-Platform Chapter Lead (Mei-Ling Johansson — Existing)

| Dimension               | Assessed By           | Criteria                                                                                                      |
| ----------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------- |
| KMP/Flutter mastery     | CTO                   | Shared module architecture, expect/actual, platform channels                                                  |
| Cross-platform strategy | CTO + CIO             | Native vs. cross-platform trade-off analysis                                                                  |
| Team leadership         | CHRO + CTO            | Mentoring, code review, technical decision-making                                                             |
| Security awareness      | CSO                   | Cross-platform security patterns, shared crypto                                                               |
| Pipeline ownership      | CTO                   | Stage 5 (Development), Stage 8 (Integrity Verification)                                                       |
| **i18n baseline**       | **CTO-L + CTO**       | **Cross-platform resource file conventions (KMP `StringKeys`, Flutter `.arb`), parity with native platforms** |
| Cultural alignment      | CHRO + Hiring Manager | Low ego, high self-esteem, open-mindedness, strong communication                                              |

### Frontend Chapter Lead (New Hire)

| Dimension                    | Assessed By | Criteria                                                      |
| ---------------------------- | ----------- | ------------------------------------------------------------- |
| Frontend architecture        | CTO         | React/Vue/Angular; state management; performance optimization |
| Design system implementation | CDO         | Token architecture, component libraries, responsive design    |
| Team leadership              | CHRO + CTO  | Mentoring, code review, technical decision-making             |
| Security awareness           | CSO         | XSS prevention, CSP, secure API integration                   |
| Pipeline ownership           | CTO         | Stage 5 (Development), Stage 8 (Integrity Verification)       |

### Backend Chapter Lead (New Hire)

| Dimension            | Assessed By | Criteria                                                         |
| -------------------- | ----------- | ---------------------------------------------------------------- |
| Backend architecture | CTO         | Microservices, API design, database patterns, message queues     |
| API security         | CSO         | Auth patterns, rate limiting, input validation, OWASP API Top 10 |
| Team leadership      | CHRO + CTO  | Mentoring, code review, technical decision-making                |
| DevOps awareness     | CTO         | CI/CD, containerization, monitoring                              |
| Pipeline ownership   | CTO         | Stage 5 (Development), Stage 8 (Integrity Verification)          |

### DevOps Lead (New Hire)

| Dimension                     | Assessed By           | Criteria                                                                                                                        |
| ----------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| CI/CD architecture            | CTO                   | Multi-platform pipelines, build optimization, artifact management                                                               |
| Cloud infrastructure          | CTO                   | IaC, container orchestration, service mesh                                                                                      |
| Pipeline security             | CSO                   | Secrets management, supply chain security, SBOM                                                                                 |
| Team leadership               | CHRO + CTO            | Mentoring, code review, technical decision-making                                                                               |
| **i18n pipeline engineering** | **Tomas + CTO-L**     | **String extraction automation, TMS integration support, CI/CD i18n gate implementation, automated `key-index.csv` generation** |
| Cultural alignment            | CHRO + Hiring Manager | Low ego, high self-esteem, open-mindedness, strong communication                                                                |

### Test Automation Lead (New Hire)

| Dimension                   | Assessed By      | Criteria                                            |
| --------------------------- | ---------------- | --------------------------------------------------- |
| Test framework architecture | Priscilla + CTO  | Cross-platform test frameworks, CI integration      |
| Mobile testing              | Priscilla        | Espresso, XCTest, Maestro, Detox                    |
| API testing                 | Priscilla        | Contract testing, performance testing, load testing |
| Team leadership             | CHRO + Priscilla | Mentoring, code review, technical decision-making   |
| Pipeline ownership          | CTO              | Stage 7 (Automated Testing) execution               |

---

## Senior Engineer Competency Matrices (All Divisions)

### Senior Mobile Engineers (Android/iOS/Cross-Platform)

| Dimension             | Assessed By         | Criteria                                                 |
| --------------------- | ------------------- | -------------------------------------------------------- |
| Platform mastery      | CTO + Chapter Lead  | 5+ years in primary platform; shipped 2+ production apps |
| Architecture patterns | Chapter Lead        | MVVM, Clean Architecture, dependency injection           |
| Mentoring             | CHRO + Chapter Lead | Code review experience; junior engineer guidance         |
| Security baseline     | CSO                 | OWASP MASVS awareness; secure coding practices           |
| Testing               | Priscilla           | Unit testing, integration testing; TDD familiarity       |

### Senior Backend Engineers

| Dimension             | Assessed By         | Criteria                                      |
| --------------------- | ------------------- | --------------------------------------------- |
| Backend mastery       | CTO + Backend Lead  | 5+ years; API design; database patterns       |
| Architecture patterns | Backend Lead        | Microservices, event-driven, CQRS             |
| Security baseline     | CSO                 | OWASP Top 10; auth patterns; input validation |
| Testing               | Priscilla           | API testing; contract testing; load testing   |
| Mentoring             | CHRO + Backend Lead | Code review; junior engineer guidance         |

### Senior Frontend Engineers

| Dimension         | Assessed By          | Criteria                                            |
| ----------------- | -------------------- | --------------------------------------------------- |
| Frontend mastery  | CTO + Frontend Lead  | 5+ years; React/Vue/Angular; state management       |
| Design system     | CDO                  | Component libraries; token usage; responsive design |
| Security baseline | CSO                  | XSS prevention; CSP; secure API integration         |
| Testing           | Priscilla            | Component testing; E2E testing; visual regression   |
| Mentoring         | CHRO + Frontend Lead | Code review; junior engineer guidance               |

### Senior SRE Engineers

| Dimension            | Assessed By        | Criteria                                           |
| -------------------- | ------------------ | -------------------------------------------------- |
| SRE practices        | CTO + DevOps Lead  | Incident response; on-call; SLO/SLI; error budgets |
| Cloud infrastructure | DevOps Lead        | AWS/GCP/Azure; IaC; container orchestration        |
| Security baseline    | CSO                | Infrastructure security; secrets management        |
| Monitoring           | DevOps Lead        | Observability; alerting; dashboards                |
| Mentoring            | CHRO + DevOps Lead | Code review; junior engineer guidance              |

### Senior DevOps Engineers

| Dimension                 | Assessed By           | Criteria                                                         |
| ------------------------- | --------------------- | ---------------------------------------------------------------- |
| CI/CD security            | CSO                   | Pipeline hardening; supply chain security; SBOM                  |
| Infrastructure automation | DevOps Lead           | IaC; configuration management; automation scripting              |
| Cloud platforms           | DevOps Lead           | Multi-cloud; container orchestration; networking                 |
| Security baseline         | CSO                   | Secrets management; access control; audit logging                |
| Mentoring                 | CHRO + DevOps Lead    | Code review; junior engineer guidance                            |
| Cultural alignment        | CHRO + Hiring Manager | Low ego, high self-esteem, open-mindedness, strong communication |

### Senior Security Engineers

| Dimension                | Assessed By                          | Criteria                                                         |
| ------------------------ | ------------------------------------ | ---------------------------------------------------------------- |
| Penetration testing      | CSO                                  | Mobile + web + API pen testing; SAST/DAST                        |
| Vulnerability management | **CSO (via Lead Security Engineer)** | CVE tracking; remediation prioritization; risk scoring           |
| Security tooling         | **CSO (via Lead Security Engineer)** | SAST/DAST pipeline integration; security automation              |
| Threat modeling          | CSO                                  | STRIDE, DREAD, attack tree analysis                              |
| Compliance               | CSO                                  | OWASP MASVS; GDPR; SOC2 familiarity                              |
| Cultural alignment       | CHRO + Hiring Manager                | Low ego, high self-esteem, open-mindedness, strong communication |

### Senior Software Architect

| Dimension                | Assessed By   | Criteria                                                |
| ------------------------ | ------------- | ------------------------------------------------------- |
| Architecture design      | CTO + Rafael  | System design; pattern selection; trade-off analysis    |
| ADR authorship           | CIO           | Architecture Decision Record writing; decision tracking |
| TSD compliance           | CIO           | Technology Selection Document enforcement               |
| Cross-platform knowledge | CTO           | Mobile + web + backend architecture patterns            |
| Mentoring                | CHRO + Rafael | Architecture review; design guidance                    |

### Engineering Onboarding Lead

| Dimension                     | Assessed By | Criteria                                           |
| ----------------------------- | ----------- | -------------------------------------------------- |
| Onboarding program design     | CHRO + CTO  | 50+ person onboarding; competency tracking         |
| Technical communication       | CHRO        | Documentation; training material creation          |
| Cross-functional coordination | CHRO + CTO  | Works across all divisions; stakeholder management |
| Pipeline knowledge            | CTO         | 10-stage pipeline understanding; gate criteria     |
| Metrics tracking              | CHRO        | Onboarding effectiveness; time-to-productivity     |

### Technical Writers

| Dimension                  | Assessed By | Criteria                                           |
| -------------------------- | ----------- | -------------------------------------------------- |
| Technical documentation    | CHRO + CTO  | Standards docs; ADR/TSD templates; API docs        |
| Pipeline procedure writing | CTO         | Process documentation; workflow guides             |
| Cross-platform knowledge   | CTO         | Android + iOS + web + backend terminology          |
| Version control            | CHRO        | Documentation versioning; change management        |
| Collaboration              | CHRO        | Works with engineers; extracts technical knowledge |

---

## Vetting Protocol

1. **Each candidate is assessed against their role-specific matrix** — not generic criteria
2. **Minimum bar must be met on ALL dimensions** — no compensating weaknesses
3. **Unanimous Chief Officer approval required** — any officer can veto
4. **Security baseline is non-negotiable** — all 57 candidates pass CSO assessment
5. **i18n baseline is non-negotiable for Mobile/Cross-platform/DevOps candidates** — all 24 mobile/DevOps candidates pass CTO-L + CTO assessment
6. **Cultural alignment is non-negotiable** — technical excellence cannot compensate for cultural misalignment
7. **Red flag scan by CHRO** — background, references, employment history verification
