# .cursor/ Directory Index

This directory contains the company's Cursor Agent configurations, skills, and workflow definitions for the mobile product development pipeline.

**Last Updated:** April 17, 2026 (Migrated to Cursor IDE)
**Total Cursor Agents:** 77 (role-first naming, expanded from 20 after FY2026 Q2 recruitment)
**Total Skills:** 199 (all skills authored and verified — 0 remaining gaps)

## Environment

### Hardware — Asus Zenbook Pro 14 Duo OLED (UX8402VV)

| Component             | Specification                                            |
| --------------------- | -------------------------------------------------------- |
| **CPU**               | Intel Core i9-13900H — 14 cores / 20 threads             |
| **GPU**               | NVIDIA GeForce RTX 4060 — 8 GB GDDR6                     |
| **RAM**               | 32 GB DDR5                                               |
| **Storage**           | M.2 NVMe PCIe 4.0 SSD (1 TB)                             |
| **Primary Display**   | 14.5" OLED, 2880×1800, 120 Hz, Touch                     |
| **Secondary Display** | 12.7" ScreenPad Plus, IPS, 2880×864                      |
| **Ports**             | 2× Thunderbolt 4, 1× USB 3.2 Type-A, 1× HDMI, 1× microSD |
| **Networking**        | Wi-Fi 6E, Bluetooth 5.3                                  |
| **Weight**            | 1.75 kg (3.86 lbs)                                       |
| **OS**                | Windows 11 Home Chinese Edition (家庭中文版)             |

### Software

| Component    | Value                                                                  |
| ------------ | ---------------------------------------------------------------------- |
| **Python**   | `C:\Program Files\Python\313\python.exe` (use `python`, NOT `python3`) |
| **Git Bash** | `C:\Program Files\Git\bin\bash.exe` (available)                        |

---

## Directory Structure

```
.cursor/
├── README.md                    # This index file
├── agents/                      # Cursor Agent configurations (77 agents, role-first naming)
│   ├── C-Suite (7 files)
│   ├── VP Engineering (4 files)
│   ├── R&D Supervisors (5 files)
│   ├── R&D Leads & Architects (7 files)
│   ├── R&D Engineers (37 files)
│   ├── Security (6 files)
│   ├── HR (3 files)
│   ├── Localization (7 files)
│   └── Brand Design (1 file)
├── pipeline/                    # Pipeline definitions (renamed from workflows/, restructured April 10, 2026; expanded April 14, 2026)
│   ├── mobile-development/      # 10-stage mobile development workflow
│   │   ├── pipeline.md          # 10-stage development workflow (authoritative spec)
│   │   ├── monitoring.md        # Progress Monitoring & Recovery System (3 layers)
│   │   ├── templates/           # 28 pipeline templates organized by stage
│   │   └── optimization-history/# Historical optimization plans
│   ├── web-development/         # 10-stage web application workflow (NEW - April 14, 2026)
│   │   ├── pipeline.md          # Web app development workflow (PWA/SPA/SSR)
│   │   ├── monitoring.md        # Progress Monitoring & Recovery System
│   │   └── templates/           # 11 pipeline templates organized by stage
│   ├── backend-api/             # 10-stage backend API workflow (NEW - April 14, 2026)
│   │   ├── pipeline.md          # API service development workflow (REST/GraphQL/gRPC)
│   │   ├── monitoring.md        # Progress Monitoring & Recovery System
│   │   └── templates/           # 11 pipeline templates organized by stage
│   ├── full-stack/              # 10-stage full-stack cross-platform workflow (NEW - April 14, 2026)
│   │   ├── pipeline.md          # Coordinated web + mobile + backend delivery
│   │   ├── monitoring.md        # Progress Monitoring & Recovery System
│   │   └── templates/           # 11 pipeline templates organized by stage
│   └── recruitment/             # 10-stage automated recruitment pipeline (CHRO-owned)
│       ├── pipeline.md          # Authoritative spec
│       └── templates/
│           ├── hiring-outcome-report.md   # Single user-facing review document
│           └── configuration/             # Quarterly configuration inputs
│               ├── competency-bars.md
│               ├── compensation-bands.md
│               ├── sourcing-channels.md
│               ├── assessment-parameters.md
│               ├── benchmark-calibration.md
│               ├── exception-rules.md
│               └── role-family-templates/
│                   ├── engineering.md
│                   ├── product.md
│                   ├── design.md
│                   ├── security.md
│                   ├── translation.md
│                   └── business.md
└── skills/                      # Cursor Skills (14 categories, 199 guidelines)
    ├── architecture/            # CTO/CIO/Architect skills (21 guidelines)
    ├── product-management/      # CPO skills (3 guidelines)
    ├── design/                  # CDO skills (8 guidelines)
    ├── security/                # CSO/Security skills (25 guidelines)
    ├── hr-recruiting/           # CHRO/HR skills (9 guidelines)
    ├── localization/            # CTO-L skills (8 guidelines)
    ├── android/                 # Android team skills (13 guidelines)
    ├── ios/                     # iOS team skills (16 guidelines)
    ├── cross-platform/          # KMP/Flutter skills (6 guidelines)
    │   ├── flutter/             # Flutter application development (3 guidelines)
    │   └── kmp/                 # Kotlin Multiplatform (3 guidelines)
    ├── frontend-web/            # Web frontend skills (20 guidelines)
    ├── backend/                 # Backend skills (21 guidelines)
    ├── testing-qa/              # SDET/QA skills (21 guidelines)
    ├── devops/                  # DevOps/SRE skills (21 guidelines)
    └── shared/                  # Cross-cutting skills (7 guidelines)
```

---

## SubAgent Configurations

All 77 company personnel are configured as Cursor Agents. Each agent file contains:

- **YAML frontmatter** with `name`, `description`, and `tools` array
- **Full agent profile** with background, strengths, gaps, and operating mode
- **Skills index** linking to skill files
- **Pipeline stages owned** for workflow reference

### C-Suite Supervisors (7)

| Agent                         | File                            | Skills                                                                                                                                       | Pipeline Stages      |
| ----------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| Chief Technology Officer      | `cto-dr-kenji-nakamura.md`      | `spec-development` · `software-architecture-design` · `mobile-technology-strategy` · `technical-project-management`                          | 3, 4, 5, 6, 7, 8, 10 |
| Chief Design Officer          | `cdo-yuki-tanaka-chen.md`       | `mobile-design-systems` · `interaction-design-specification-cdo` · `design-to-engineering-handoff` · `user-research-driven-design`           | 2, 6, 8, 10          |
| Chief Product Officer         | `cpo-marcus-tran-yoshida.md`    | `mobile-product-strategy` · `prd-authorship`                                                                                                 | 1, 6, 8, 10          |
| Chief Information Officer     | `cio-dr-priya-mehta.md`         | `technology-evaluation` · `mobile-architecture-strategy` · `technical-selection-documentation`                                               | 3, 6, 8, 10          |
| Chief Security Officer        | `cso-dr-sarah-chen.md`          | `mobile-security-architecture` · `application-security-hardening` · `security-risk-assessment` · `emerging-threat-evaluation`                | 1, 6, 8, 10          |
| Chief Human Resources Officer | `chro-dr-evelyn-hartwell.md`    | `vet-candidate` · `recruit-engineering` · `recruit-product` · `recruit-design` · `recruit-data` · `recruit-translation` · `recruit-business` | Recruitment only     |
| Chief Translation Officer     | `cto-l-dr-amara-osei-mensah.md` | `language-translation-module`                                                                                                                | 9, 10                |

### VP Engineering (4)

| Agent                            | File                              | Skills                                                                                     | Pipeline Stages |
| -------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------ | --------------- |
| Marcus Andersson (VP Mobile)     | `vp-mobile-marcus-andersson.md`   | `mobile-platform-strategy`                                                                 | 5, 8            |
| Elena Vasquez (VP Web & Backend) | `vp-web-backend-elena-vasquez.md` | `distributed-backend-architecture` · `adr-governance` · `ids-fluency`                      | 5, 8            |
| David Okonkwo (VP Platform)      | `vp-platform-david-okonkwo.md`    | `developer-platform-engineering` · `masvs-overview`                                        | 5, 8            |
| Aisha Patel (VP Quality)         | `vp-quality-aisha-patel.md`       | `quality-engineering-strategy` · `axe-core-wcag-testing` · `localization-testing-strategy` | 7, 8            |

### R&D Team Supervisors (5)

| Agent                           | File                                        | Skills                                                                                       | Pipeline Stages |
| ------------------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------- | --------------- |
| Software Architect              | `software-architect-rafael-okonkwo.md`      | `uml-engineering-package` · `mobile-architecture-patterns` · `architecture-decision-records` | 3, 6, 8         |
| Test Lead                       | `test-lead-priscilla-oduya.md`              | `automated-test-suite` · `defect-triage-and-classification`                                  | 7, 8            |
| Android Development Lead        | `android-lead-kofi-asante-mensah.md`        | `android-implementation`                                                                     | 5, 8            |
| iOS Development Lead            | `ios-lead-seo-yeon-park.md`                 | `ios-implementation`                                                                         | 5, 8            |
| Cross-Platform Development Lead | `cross-platform-lead-mei-ling-johansson.md` | `kmp-implementation` · `flutter-implementation`                                              | 5, 8            |

### R&D Leads & Senior Staff (7)

| Agent                                | File                                    | Skills                                                                                                                         | Pipeline Stages |
| ------------------------------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------------- |
| Dr. Elena Rostova (Senior Architect) | `senior-architect-dr-elena-rostova.md`  | `adr-governance` · `uml-engineering` · `code-review-participation` · `mobile-adr-production` · `architecture-review-shadowing` | 3, 6            |
| Rachel Kim (Test Automation Lead)    | `test-automation-lead-rachel-kim.md`    | `mobile-test-automation` · `defect-triage-protocol`                                                                            | 7, 8            |
| Thomas Zhang (DevOps Lead)           | `devops-lead-thomas-zhang.md`           | `cicd-infrastructure-engineering` · `compliance-foundations` · `mobile-scanning-tools`                                         | 5, 8            |
| Amira Voss (Frontend Chapter Lead)   | `frontend-lead-amira-voss.md`           | `design-systems` · `frontend-security` · `performance-optimization` · `frontend-performance-baseline` · `wcag-mobile-roadmap`  | 5, 8            |
| Dev Malhotra (Backend Chapter Lead)  | `backend-lead-dev-malhotra.md`          | `distributed-systems` · `api-gateway-design` · `database-architecture`                                                         | 5, 8            |
| James Wright (Security Lead)         | `security-lead-james-wright.md`         | `security-operations` · `masvs-mastery-track-a` · `mobile-scanning-tools`                                                      | 1, 6, 8, 10     |
| Natalia Petrova (Security Architect) | `security-architect-natalia-petrova.md` | `threat-modeling` · `masvs-mastery-track-b` · `mobile-threat-modeling` · `adr-governance`                                      | 1, 3, 6, 8, 10  |

### R&D Engineers (39)

| Agent                            | File                                         | Skills                                                                                     | Pipeline Stages |
| -------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------- |
| Elena Kim (Senior Frontend)      | `senior-frontend-engineer-elena-kim.md`      | `advanced-a11y` · `xss-prevention` · `pwa-engineering`                                     | 5, 8            |
| Rafael Santos (Senior Frontend)  | `senior-frontend-engineer-rafael-santos.md`  | `frontend-performance-optimization` · `react-testing` · `ssr-nextjs`                       | 5, 8            |
| Yuna Park (Frontend)             | `frontend-engineer-yuna-park.md`             | `react-state-management` · `react-testing-advanced`                                        | 5, 8            |
| Lucas Silva (Frontend)           | `frontend-engineer-lucas-silva.md`           | `vue-vite-advanced` · `vue-testing`                                                        | 5, 8            |
| Kael Jensen (Senior Backend)     | `senior-backend-engineer-kael-jensen.md`     | `real-time-architecture` · `backend-observability` · `websocket-scaling`                   | 5, 8            |
| Aisha Mohammed (Senior Backend)  | `senior-backend-engineer-aisha-mohammed.md`  | `database-sharding` · `api-testing`                                                        | 5, 8            |
| Viktor Horvath (Senior Backend)  | `senior-backend-engineer-viktor-horvath.md`  | `event-sourcing` · `security-patterns` · `cqrs-architecture`                               | 5, 8            |
| Omar Hassan (Backend)            | `backend-engineer-omar-hassan.md`            | `go-rest-api` · `go-testing` · `go-microservices`                                          | 5, 8            |
| Ingrid Nilsen (Backend)          | `backend-engineer-ingrid-nilsen.md`          | `python-fastapi` · `postgresql-basics` · `postgresql-optimization`                         | 5, 8            |
| Thabo Mokoena (Backend)          | `backend-engineer-thabo-mokoena.md`          | `graphql-apis` · `aws-fundamentals` · `aws-architecture`                                   | 5, 8            |
| Lars Eriksson (Senior iOS)       | `senior-ios-engineer-lars-eriksson.md`       | `swift-concurrency` · `tca-architecture` · `uikit-architecture`                            | 5, 8            |
| Mei Chen (Senior iOS)            | `senior-ios-engineer-mei-chen.md`            | `core-animation` · `ios-performance` · `swiftui`                                           | 5, 8            |
| Amara Diallo (Senior iOS)        | `senior-ios-engineer-amara-diallo.md`        | `ios-networking` · `ios-ci-cd` · `combine-reactive-programming`                            | 5, 8            |
| Arjun Mehta (iOS)                | `ios-engineer-arjun-mehta.md`                | `ios-testing` · `ios-accessibility` · `swiftui`                                            | 5, 8            |
| Hiroshi Tanaka (iOS)             | `ios-engineer-hiroshi-tanaka.md`             | `uikit-combine` · `core-data` · `swiftui`                                                  | 5, 8            |
| Camila Rodriguez (iOS)           | `ios-engineer-camila-rodriguez.md`           | `swiftui` · `widgetkit-extensions`                                                         | 5, 8            |
| Tariq Al-Hassan (Senior Android) | `senior-android-engineer-tariq-al-hassan.md` | `kotlin-advanced` · `android-architecture` · `jetpack-compose`                             | 5, 8            |
| Priya Narayanan (Senior Android) | `senior-android-engineer-priya-narayanan.md` | `offline-first-patterns` · `android-security` · `kmp-architecture`                         | 5, 8            |
| Sofia Rezende (Senior Android)   | `senior-android-engineer-sofia-rezende.md`   | `android-accessibility` · `android-testing` · `kmp-architecture`                           | 5, 8            |
| Jan Kowalski (Android)           | `android-engineer-jan-kowalski.md`           | `jetpack-compose` · `android-ci-cd`                                                        | 5, 8            |
| Nina Bergstrom (Android)         | `android-engineer-nina-bergstrom.md`         | `android-data-layer` · `android-test-infra`                                                | 5, 8            |
| Kwame Osei (Android)             | `android-engineer-kwame-osei.md`             | `android-networking` · `android-security-basics`                                           | 5, 8            |
| Dmitri Volkov (Cross-Platform)   | `cross-platform-engineer-dmitri-volkov.md`   | `kmp-architecture` · `kmp-shared-modules`                                                  | 5, 8            |
| Fatima Al-Zahra (Cross-Platform) | `cross-platform-engineer-fatima-al-zahra.md` | `flutter-architecture` · `flutter-i18n` · `kmp-architecture`                               | 5, 8            |
| Tobias Weber (SDET Mobile)       | `sdet-mobile-tobias-weber.md`                | `mobile-test-automation` · `visual-regression-testing` · `accessibility-testing-mobile`    | 7, 8            |
| Ananya Krishnan (SDET Mobile)    | `sdet-mobile-ananya-krishnan.md`             | `mobile-unit-testing` · `test-driven-development` · `code-coverage-analysis`               | 7, 8            |
| Priya Sharma (SDET Web/Backend)  | `sdet-web-backend-priya-sharma.md`           | `api-testing` · `pact-contract-testing` · `k6-performance` · `mobile-testing-fundamentals` | 7, 8            |
| Kai Nakamura (DevEx)             | `devex-engineer-kai-nakamura.md`             | `build-optimization` · `developer-analytics` · `bazel-build-system`                        | 5, 8            |
| Zara Okonkwo (DevEx)             | `devex-engineer-zara-okonkwo.md`             | `ci-cd-optimization` · `test-infra` · `test-sharding`                                      | 5, 7, 8         |
| Raihan Rahman (SRE)              | `sre-engineer-raihan-rahman.md`              | `sre-practices` · `cloud-infrastructure` · `gcp-multi-region`                              | 5, 8            |
| Elin Ström (SRE)                 | `sre-engineer-elin-strom.md`                 | `observability-logging` · `infrastructure-security` · `container-runtime-security`         | 5, 8            |
| Yuki Tanaka (DevOps)             | `devops-engineer-yuki-tanaka.md`             | `cicd-security` · `iac-gitops` · `kubernetes-at-scale`                                     | 5, 6, 8         |
| Leila Nasser (DevOps)            | `devops-engineer-leila-nasser.md`            | `aws-management` · `monitoring-audit` · `network-security-fundamentals`                    | 5, 8            |
| Diego Morales (Full-Stack)       | `full-stack-engineer-diego-morales.md`       | `angular-spring-boot` · `enterprise-patterns` · `angular-signals`                          | 5, 8            |
| Nina Petrova (Full-Stack)        | `full-stack-engineer-nina-petrova.md`        | `full-stack-mvp` · `prd-fluency` · `docker-orchestration`                                  | 4, 5, 8         |
| Marcus Wright (Full-Stack)       | `full-stack-engineer-marcus-wright.md`       | `vue-dotnet` · `api-versioning` · `multi-tenant-isolation`                                 | 5, 8            |
| Sora Kim (Full-Stack)            | `full-stack-engineer-sora-kim.md`            | `react-fastapi` · `react-native-prototyping` · `webauthn-biometric-auth`                   | 5, 8            |

### R&D — Transferred from HR (April 7, 2026)

| Agent                            | File                                | Skills                                              | Pipeline Stages |
| -------------------------------- | ----------------------------------- | --------------------------------------------------- | --------------- |
| Henrik Larsen (Technical Writer) | `technical-writer-henrik-larsen.md` | `adr-technical-writing` · `pipeline-documentation`  | 3, 4, 6, 8, 10  |
| Amina Razak (Technical Writer)   | `technical-writer-amina-razak.md`   | `api-technical-writing` · `developer-documentation` | 5, 6, 10        |

### Security Teammates (6)

| Agent                               | File                                   | Skills                                                                                                   | Pipeline Stages |
| ----------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------------- |
| Leila Khoury (DevOps Engineer)      | `devops-engineer-leila-khoury.md`      | `aws-monitoring` · `secrets-management`                                                                  | 1, 6, 8, 10     |
| Yuki Matsuda (DevOps Engineer)      | `devops-engineer-yuki-matsuda.md`      | `cicd-security` · `infrastructure-as-code`                                                               | 1, 6, 8, 10     |
| Sana Khoury (Security Engineer)     | `security-engineer-sana-khoury.md`     | `mobile-penetration-testing` · `owasp-masvs-compliance`                                                  | 1, 6, 8, 10     |
| Omar Farouq (Security Engineer)     | `security-engineer-omar-farouq.md`     | `sast-dast-pipeline` · `web-application-security` · `masvs-certification` · `mobile-penetration-testing` | 1, 6, 8, 10     |
| Li Wei Chen (Security Engineer)     | `security-engineer-li-wei-chen.md`     | `supply-chain-security` · `secure-coding-training`                                                       | 1, 6, 8, 10     |
| Ingrid Solberg (Compliance Analyst) | `compliance-analyst-ingrid-solberg.md` | `compliance-auditing` · `owasp-masvs-auditing` · `compliance-documentation`                              | 1, 6, 8, 10     |

### HR Teammates (1)

| Agent                           | File                               | Skills                                              | Pipeline Stages |
| ------------------------------- | ---------------------------------- | --------------------------------------------------- | --------------- |
| Grace Muthoni (Onboarding Lead) | `onboarding-lead-grace-muthoni.md` | `competency-tracking` · `onboarding-program-design` | Recruitment     |

### Localization (7)

| Agent                 | File                                         | Skills                                 | Pipeline Stages |
| --------------------- | -------------------------------------------- | -------------------------------------- | --------------- |
| I18n Specialist       | `i18n-specialist-tomas-dvoracek.md`          | `string-extraction-and-resource-files` | 9               |
| Chinese Linguist      | `chinese-linguist-wei-chen-liu.md`           | `mobile-ui-translation`                | 9               |
| English Linguist      | `english-linguist-amelia-hartington.md`      | `mobile-ui-translation`                | 9               |
| French Linguist       | `french-linguist-isabelle-moreau-leclerc.md` | `mobile-ui-translation`                | 9               |
| Japanese Linguist     | `japanese-linguist-haruki-yoshimoto.md`      | `mobile-ui-translation`                | 9               |
| Korean Linguist       | `korean-linguist-ji-hyun-bae.md`             | `mobile-ui-translation`                | 9               |
| Localization Engineer | `localization-engineer-dario-esposito.md`    | `localization-pipeline-engineering`    | 9               |

### Brand Design (1)

| Agent                     | File                         | Skills                                                           | Pipeline Stages |
| ------------------------- | ---------------------------- | ---------------------------------------------------------------- | --------------- |
| Lena Vasquez (Prototyper) | `prototyper-lena-vasquez.md` | `web-prototype-development` · `interaction-design-specification` | 2               |

---

## Workflow Definitions

| File                                                | Description                                                                                                                                                                                                                 |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pipeline/mobile-development/pipeline.md`           | Ten-stage development pipeline: Requirements → PRD/SRD → Prototype → UML → Implementation Plan → Development → Code Review → Testing → Integrity Verification → i18n → Release                                              |
| `pipeline/mobile-development/monitoring.md`         | Progress Monitoring & Recovery System (3 layers: PROGRESS.md, session logs, checkpoints)                                                                                                                                    |
| `pipeline/mobile-development/templates/`            | 28 pipeline templates organized by stage                                                                                                                                                                                    |
| `pipeline/mobile-development/optimization-history/` | Historical optimization plans and pipeline improvement records                                                                                                                                                              |
| `pipeline/recruitment/pipeline.md`                  | Ten-stage automated recruitment pipeline: Stage 0 (Department Planning) → Role Intake → Sourcing → Screening → Interview → Vetting → Background → Offer → User Review → Onboarding (CHRO-owned, unanimous C-Suite sign-off) |

### Pipeline Stage Summary

| #   | Stage                  | Key Output                              | Responsible          |
| --- | ---------------------- | --------------------------------------- | -------------------- |
| 1   | Requirements           | PRD + SRD                               | CPO, CSO             |
| 2   | Prototype              | Web Prototype + IDS                     | CDO                  |
| 3   | UML Engineering        | UML Package + ADRs + TSD                | CTO, CIO             |
| 4   | Implementation Plan    | Plan + Gantt Chart                      | CTO                  |
| 5   | Development            | Development Codebase                    | CTO + Platform Leads |
| 6   | Code Review            | Defect Report + Sign-off                | CTO (panel)          |
| 7   | Automated Testing      | Test Suite + Results                    | CTO + Test Lead      |
| 8   | Integrity Verification | Integrity Sign-off                      | CTO (panel)          |
| 9   | i18n Engineering       | Localised Codebase + Translation Report | CTO-L + R&D          |
| 10  | Release Readiness      | Release Report + Decision               | CTO (panel) + User   |

---

## Skills Index

Skills are organized into 14 functional categories. Each category has a parent `SKILL.md` with a table of sub-guidelines in `guidelines/`.

### architecture (21 guidelines)

| Guideline                         | File                                                           | Owner            |
| --------------------------------- | -------------------------------------------------------------- | ---------------- |
| SPEC Development                  | `architecture/guidelines/spec-development.md`                  | CTO              |
| Software Architecture Design      | `architecture/guidelines/software-architecture-design.md`      | CTO              |
| Mobile Technology Strategy        | `architecture/guidelines/mobile-technology-strategy.md`        | CTO              |
| Technical Project Management      | `architecture/guidelines/technical-project-management.md`      | CTO              |
| Technology Evaluation             | `architecture/guidelines/technology-evaluation.md`             | CIO              |
| Mobile Architecture Strategy      | `architecture/guidelines/mobile-architecture-strategy.md`      | CIO              |
| Technical Selection Documentation | `architecture/guidelines/technical-selection-documentation.md` | CIO              |
| UML Engineering Package           | `architecture/guidelines/uml-engineering-package.md`           | Architect        |
| Mobile Architecture Patterns      | `architecture/guidelines/mobile-architecture-patterns.md`      | Architect        |
| Architecture Decision Records     | `architecture/guidelines/architecture-decision-records.md`     | Architect        |
| ADR Governance                    | `architecture/guidelines/adr-governance.md`                    | Dr. Rostova      |
| UML Engineering                   | `architecture/guidelines/uml-engineering.md`                   | Dr. Rostova      |
| System Design                     | `architecture/guidelines/system-design.md`                     | Dr. Rostova      |
| Code Review Participation         | `architecture/guidelines/code-review-participation.md`         | Dr. Rostova      |
| Mobile ADR Production             | `architecture/guidelines/mobile-adr-production.md`             | Dr. Rostova      |
| Architecture Review Shadowing     | `architecture/guidelines/architecture-review-shadowing.md`     | Dr. Rostova      |
| Cross-Platform Architecture       | `architecture/guidelines/cross-platform-architecture.md`       | Dr. Rostova      |
| ADR Technical Writing             | `architecture/guidelines/adr-technical-writing.md`             | Henrik Larsen    |
| Pipeline Documentation            | `architecture/guidelines/pipeline-documentation.md`            | Henrik Larsen    |
| Mobile Platform Strategy          | `architecture/guidelines/mobile-platform-strategy.md`          | Marcus Andersson |
| Mobile Platform Immersion         | `architecture/guidelines/mobile-platform-immersion.md`         | Amira Voss       |

### product-management (3 guidelines)

| Guideline               | File                                                       | Owner        |
| ----------------------- | ---------------------------------------------------------- | ------------ |
| Mobile Product Strategy | `product-management/guidelines/mobile-product-strategy.md` | CPO          |
| PRD Authorship          | `product-management/guidelines/prd-authorship.md`          | CPO          |
| PRD Fluency             | `product-management/guidelines/prd-fluency.md`             | Nina Petrova |

### design (8 guidelines)

| Guideline                        | File                                                        | Owner         |
| -------------------------------- | ----------------------------------------------------------- | ------------- |
| Mobile Design Systems            | `design/guidelines/mobile-design-systems.md`                | CDO           |
| Interaction Design Specification | `design/guidelines/interaction-design-specification.md`     | CDO / Lena    |
| IDS (CDO)                        | `design/guidelines/interaction-design-specification-cdo.md` | CDO           |
| Design to Engineering Handoff    | `design/guidelines/design-to-engineering-handoff.md`        | CDO           |
| User Research-Driven Design      | `design/guidelines/user-research-driven-design.md`          | CDO           |
| Web Prototype Development        | `design/guidelines/web-prototype-development.md`            | Lena          |
| Design Systems                   | `design/guidelines/design-systems.md`                       | Amira Voss    |
| IDS Fluency                      | `design/guidelines/ids-fluency.md`                          | Elena Vasquez |

### hr-recruiting (9 guidelines)

| Guideline                 | File                                                    | Owner         |
| ------------------------- | ------------------------------------------------------- | ------------- |
| Vet Candidate             | `hr-recruiting/guidelines/vet-candidate.md`             | CHRO          |
| Recruit Engineering       | `hr-recruiting/guidelines/recruit-engineering.md`       | CHRO          |
| Recruit Product           | `hr-recruiting/guidelines/recruit-product.md`           | CHRO          |
| Recruit Design            | `hr-recruiting/guidelines/recruit-design.md`            | CHRO          |
| Recruit Data              | `hr-recruiting/guidelines/recruit-data.md`              | CHRO          |
| Recruit Translation       | `hr-recruiting/guidelines/recruit-translation.md`       | CHRO          |
| Recruit Business          | `hr-recruiting/guidelines/recruit-business.md`          | CHRO          |
| Competency Tracking       | `hr-recruiting/guidelines/competency-tracking.md`       | Grace Muthoni |
| Onboarding Program Design | `hr-recruiting/guidelines/onboarding-program-design.md` | Grace Muthoni |

### localization (8 guidelines)

| Guideline                   | File                                                              | Owner             |
| --------------------------- | ----------------------------------------------------------------- | ----------------- |
| Language Translation Module | `localization/guidelines/language-translation-module.md`          | CTO-L             |
| Mobile UI Translation       | `localization/guidelines/mobile-ui-translation.md`                | All Linguists     |
| Chinese Translation         | `localization/guidelines/mobile-ui-translation-chinese.md`        | Wei-Chen Liu      |
| English Translation         | `localization/guidelines/mobile-ui-translation-english.md`        | Amelia Hartington |
| Japanese Translation        | `localization/guidelines/mobile-ui-translation-japanese.md`       | Haruki Yoshimoto  |
| Korean Translation          | `localization/guidelines/mobile-ui-translation-korean.md`         | Ji-Hyun Bae       |
| String Extraction           | `localization/guidelines/string-extraction-and-resource-files.md` | Tomas Dvoracek    |
| Localization Pipeline       | `localization/guidelines/localization-pipeline-engineering.md`    | Dario Esposito    |

### android (13 guidelines)

#### UI & UX

| Guideline             | File                                     | Owner         |
| --------------------- | ---------------------------------------- | ------------- |
| Jetpack Compose       | `android/ui-ux/jetpack-compose.md`       | Jan Kowalski  |
| Android Accessibility | `android/ui-ux/android-accessibility.md` | Sofia Rezende |

#### Architecture

| Guideline              | File                                             | Owner           |
| ---------------------- | ------------------------------------------------ | --------------- |
| Android Architecture   | `android/architecture/android-architecture.md`   | Tariq Al-Hassan |
| Offline-First Patterns | `android/architecture/offline-first-patterns.md` | Priya Narayanan |

#### Data & Networking

| Guideline          | File                                            | Owner          |
| ------------------ | ----------------------------------------------- | -------------- |
| Android Data Layer | `android/data-networking/android-data-layer.md` | Nina Bergstrom |
| Android Networking | `android/data-networking/android-networking.md` | Kwame Osei     |

#### Testing & Quality

| Guideline                   | File                                            | Owner          |
| --------------------------- | ----------------------------------------------- | -------------- |
| Android Testing             | `android/testing-quality/android-testing.md`    | Sofia Rezende  |
| Android Test Infrastructure | `android/testing-quality/android-test-infra.md` | Nina Bergstrom |

#### Security & CI/CD

| Guideline               | File                                                | Owner           |
| ----------------------- | --------------------------------------------------- | --------------- |
| Android Security        | `android/security-ci-cd/android-security.md`        | Priya Narayanan |
| Android Security Basics | `android/security-ci-cd/android-security-basics.md` | Kwame Osei      |
| Android CI/CD           | `android/security-ci-cd/android-ci-cd.md`           | Jan Kowalski    |

#### Language & Core

| Guideline              | File                                              | Owner              |
| ---------------------- | ------------------------------------------------- | ------------------ |
| Kotlin Advanced        | `android/language-core/kotlin-advanced.md`        | Tariq Al-Hassan    |
| Android Implementation | `android/language-core/android-implementation.md` | Kofi Asante-Mensah |

### ios (16 guidelines)

#### UI & UX

| Guideline            | File                                | Owner            |
| -------------------- | ----------------------------------- | ---------------- |
| SwiftUI              | `ios/ui-ux/swiftui.md`              | Camila Rodriguez |
| UIKit + Combine      | `ios/ui-ux/uikit-combine.md`        | Hiroshi Tanaka   |
| WidgetKit Extensions | `ios/ui-ux/widgetkit-extensions.md` | Camila Rodriguez |

#### Architecture

| Guideline          | File                                     | Owner         |
| ------------------ | ---------------------------------------- | ------------- |
| Swift Concurrency  | `ios/architecture/swift-concurrency.md`  | Lars Eriksson |
| TCA Architecture   | `ios/architecture/tca-architecture.md`   | Lars Eriksson |
| UIKit Architecture | `ios/architecture/uikit-architecture.md` | Lars Eriksson |

#### Data & Networking

| Guideline      | File                                    | Owner          |
| -------------- | --------------------------------------- | -------------- |
| Core Data      | `ios/data-networking/core-data.md`      | Hiroshi Tanaka |
| iOS Networking | `ios/data-networking/ios-networking.md` | Amara Diallo   |

#### Testing & Quality

| Guideline         | File                                       | Owner       |
| ----------------- | ------------------------------------------ | ----------- |
| iOS Testing       | `ios/testing-quality/ios-testing.md`       | Arjun Mehta |
| iOS Accessibility | `ios/testing-quality/ios-accessibility.md` | Arjun Mehta |

#### Infrastructure

| Guideline                    | File                                                  | Owner         |
| ---------------------------- | ----------------------------------------------------- | ------------- |
| iOS Implementation           | `ios/infrastructure/ios-implementation.md`            | Seo-Yeon Park |
| iOS CI/CD                    | `ios/infrastructure/ios-ci-cd.md`                     | Amara Diallo  |
| iOS Performance              | `ios/infrastructure/ios-performance.md`               | Mei Chen      |
| Core Animation               | `ios/infrastructure/core-animation.md`                | Mei Chen      |
| Swift Familiarization        | `ios/infrastructure/swift-familiarization.md`         | Dmitri Volkov |
| Combine Reactive Programming | `ios/data-networking/combine-reactive-programming.md` | Amara Diallo  |

### cross-platform (6 guidelines)

#### Flutter

| Guideline              | File                                               | Owner              |
| ---------------------- | -------------------------------------------------- | ------------------ |
| Flutter Architecture   | `cross-platform/flutter/flutter-architecture.md`   | Fatima Al-Zahra    |
| Flutter i18n           | `cross-platform/flutter/flutter-i18n.md`           | Fatima Al-Zahra    |
| Flutter Implementation | `cross-platform/flutter/flutter-implementation.md` | Mei-Ling Johansson |

#### KMP

| Guideline          | File                                       | Owner              |
| ------------------ | ------------------------------------------ | ------------------ |
| KMP Architecture   | `cross-platform/kmp/kmp-architecture.md`   | Dmitri Volkov      |
| KMP Shared Modules | `cross-platform/kmp/kmp-shared-modules.md` | Dmitri Volkov      |
| KMP Implementation | `cross-platform/kmp/kmp-implementation.md` | Mei-Ling Johansson |

### security (25 guidelines)

#### MASVS Standards

| Guideline              | File                                       | Owner           |
| ---------------------- | ------------------------------------------ | --------------- |
| OWASP MASVS Compliance | `security/masvs/owasp-masvs-compliance.md` | Sana Khoury     |
| OWASP MASVS Auditing   | `security/masvs/owasp-masvs-auditing.md`   | Ingrid Solberg  |
| Secure Coding Training | `security/masvs/secure-coding-training.md` | Li Wei Chen     |
| MASVS Overview         | `security/masvs/masvs-overview.md`         | David Okonkwo   |
| MASVS Mastery Track A  | `security/masvs/masvs-mastery-track-a.md`  | James Wright    |
| MASVS Mastery Track B  | `security/masvs/masvs-mastery-track-b.md`  | Natalia Petrova |
| MASVS Certification    | `security/masvs/masvs-certification.md`    | Omar Farouq     |

#### Penetration Testing

| Guideline                  | File                                                | Owner           |
| -------------------------- | --------------------------------------------------- | --------------- |
| Mobile Penetration Testing | `security/pentesting/mobile-penetration-testing.md` | Sana Khoury     |
| Web Application Security   | `security/pentesting/web-application-security.md`   | Omar Farouq     |
| Threat Modeling            | `security/pentesting/threat-modeling.md`            | Natalia Petrova |
| SAST/DAST Pipeline         | `security/pentesting/sast-dast-pipeline.md`         | Omar Farouq     |
| Mobile Threat Modeling     | `security/pentesting/mobile-threat-modeling.md`     | Natalia Petrova |
| Mobile Scanning Tools      | `security/pentesting/mobile-scanning-tools.md`      | James Wright    |

#### Compliance

| Guideline                | File                                              | Owner          |
| ------------------------ | ------------------------------------------------- | -------------- |
| Compliance Auditing      | `security/compliance/compliance-auditing.md`      | Ingrid Solberg |
| Compliance Documentation | `security/compliance/compliance-documentation.md` | Ingrid Solberg |
| Supply Chain Security    | `security/compliance/supply-chain-security.md`    | Li Wei Chen    |

#### Security Architecture

| Guideline                      | File                                                      | Owner          |
| ------------------------------ | --------------------------------------------------------- | -------------- |
| Mobile Security Architecture   | `security/architecture/mobile-security-architecture.md`   | CSO            |
| Application Security Hardening | `security/architecture/application-security-hardening.md` | CSO            |
| Security Risk Assessment       | `security/architecture/security-risk-assessment.md`       | CSO            |
| Emerging Threat Evaluation     | `security/architecture/emerging-threat-evaluation.md`     | CSO            |
| Security Operations            | `security/architecture/security-operations.md`            | James Wright   |
| Security Patterns              | `security/architecture/security-patterns.md`              | Viktor Horvath |
| Infrastructure Security        | `security/architecture/infrastructure-security.md`        | Elin Ström     |
| AWS Security Monitoring        | `security/architecture/aws-monitoring.md`                 | Leila Khoury   |
| CI/CD Security                 | `security/architecture/cicd-security.md`                  | Yuki Matsuda   |

### backend (21 guidelines)

#### Go

| Guideline        | File                             | Owner       |
| ---------------- | -------------------------------- | ----------- |
| Go REST API      | `backend/go/go-rest-api.md`      | Omar Hassan |
| Go Testing       | `backend/go/go-testing.md`       | Omar Hassan |
| Go Microservices | `backend/go/go-microservices.md` | Omar Hassan |

#### Python

| Guideline      | File                               | Owner         |
| -------------- | ---------------------------------- | ------------- |
| Python FastAPI | `backend/python/python-fastapi.md` | Ingrid Nilsen |

#### Database

| Guideline               | File                                          | Owner          |
| ----------------------- | --------------------------------------------- | -------------- |
| Database Architecture   | `backend/database/database-architecture.md`   | Dev Malhotra   |
| Database Sharding       | `backend/database/database-sharding.md`       | Aisha Mohammed |
| PostgreSQL Basics       | `backend/database/postgresql-basics.md`       | Ingrid Nilsen  |
| PostgreSQL Optimization | `backend/database/postgresql-optimization.md` | Ingrid Nilsen  |

#### API Patterns

| Guideline              | File                                                       | Owner          |
| ---------------------- | ---------------------------------------------------------- | -------------- |
| API Gateway Design     | `backend/api-patterns/api-gateway-design.md`               | Dev Malhotra   |
| Distributed Systems    | `backend/api-patterns/distributed-systems.md`              | Dev Malhotra   |
| Distributed Backend    | `backend/api-patterns/distributed-backend-architecture.md` | Elena Vasquez  |
| GraphQL APIs           | `backend/api-patterns/graphql-apis.md`                     | Thabo Mokoena  |
| Event Sourcing         | `backend/api-patterns/event-sourcing.md`                   | Viktor Horvath |
| Real-Time Architecture | `backend/api-patterns/real-time-architecture.md`           | Kael Jensen    |
| CQRS Architecture      | `backend/api-patterns/cqrs-architecture.md`                | Viktor Horvath |
| WebSocket Scaling      | `backend/api-patterns/websocket-scaling.md`                | Kael Jensen    |
| API Technical Writing  | `backend/api-patterns/api-technical-writing.md`            | Amina Razak    |

#### Cloud & Observability

| Guideline             | File                                     | Owner         |
| --------------------- | ---------------------------------------- | ------------- |
| AWS Fundamentals      | `backend/cloud/aws-fundamentals.md`      | Thabo Mokoena |
| AWS Architecture      | `backend/guidelines/aws-architecture.md` | Thabo Mokoena |
| Backend Observability | `backend/cloud/backend-observability.md` | Kael Jensen   |
| API Testing           | `backend/cloud/api-testing.md`           | Priya Sharma  |

### frontend-web (20 guidelines)

#### React

| Guideline                | File                                             | Owner         |
| ------------------------ | ------------------------------------------------ | ------------- |
| React State Management   | `frontend-web/react/react-state-management.md`   | Yuna Park     |
| React Testing            | `frontend-web/react/react-testing.md`            | Rafael Santos |
| React Testing Advanced   | `frontend-web/react/react-testing-advanced.md`   | Yuna Park     |
| React + FastAPI          | `frontend-web/react/react-fastapi.md`            | Sora Kim      |
| React Native Prototyping | `frontend-web/react/react-native-prototyping.md` | Sora Kim      |

#### Vue

| Guideline           | File                                    | Owner         |
| ------------------- | --------------------------------------- | ------------- |
| Vue + Vite Advanced | `frontend-web/vue/vue-vite-advanced.md` | Lucas Silva   |
| Vue Testing         | `frontend-web/vue/vue-testing.md`       | Lucas Silva   |
| Vue + .NET          | `frontend-web/vue/vue-dotnet.md`        | Marcus Wright |

#### Angular

| Guideline             | File                                          | Owner         |
| --------------------- | --------------------------------------------- | ------------- |
| Angular + Spring Boot | `frontend-web/angular/angular-spring-boot.md` | Diego Morales |
| Angular Signals       | `frontend-web/angular/angular-signals.md`     | Diego Morales |

#### Full-Stack

| Guideline           | File                                             | Owner         |
| ------------------- | ------------------------------------------------ | ------------- |
| Full-Stack MVP      | `frontend-web/full-stack/full-stack-mvp.md`      | Nina Petrova  |
| API Versioning      | `frontend-web/full-stack/api-versioning.md`      | Marcus Wright |
| Enterprise Patterns | `frontend-web/full-stack/enterprise-patterns.md` | Diego Morales |

#### Performance & Security

| Guideline                         | File                                                                     | Owner         |
| --------------------------------- | ------------------------------------------------------------------------ | ------------- |
| Frontend Performance Optimization | `frontend-web/performance-security/frontend-performance-optimization.md` | Rafael Santos |
| Frontend Performance Baseline     | `frontend-web/performance-security/frontend-performance-baseline.md`     | Amira Voss    |
| Frontend Security                 | `frontend-web/performance-security/frontend-security.md`                 | Amira Voss    |
| Advanced Accessibility            | `frontend-web/performance-security/advanced-a11y.md`                     | Elena Kim     |
| XSS Prevention                    | `frontend-web/performance-security/xss-prevention.md`                    | Elena Kim     |
| PWA Engineering                   | `frontend-web/performance-security/pwa-engineering.md`                   | Elena Kim     |
| SSR/Next.js                       | `frontend-web/react/ssr-nextjs.md`                                       | Rafael Santos |

### testing-qa (21 guidelines)

#### Mobile Testing

| Guideline                    | File                                                | Owner           |
| ---------------------------- | --------------------------------------------------- | --------------- |
| Mobile Test Automation       | `testing-qa/mobile/mobile-test-automation.md`       | Rachel Kim      |
| Espresso + XCTest            | `testing-qa/mobile/espresso-xctest.md`              | Ananya Krishnan |
| Maestro Testing              | `testing-qa/mobile/maestro-testing.md`              | Ananya Krishnan |
| Appium + Detox               | `testing-qa/mobile/appium-detox.md`                 | Tobias Weber    |
| Device Farm Management       | `testing-qa/mobile/device-farm-management.md`       | Tobias Weber    |
| Mobile Testing Fundamentals  | `testing-qa/mobile/mobile-testing-fundamentals.md`  | Ananya Krishnan |
| Mobile Unit Testing          | `testing-qa/mobile/mobile-unit-testing.md`          | Ananya Krishnan |
| Native Mobile Testing        | `testing-qa/mobile/native-mobile-testing.md`        | Tobias Weber    |
| Accessibility Testing Mobile | `testing-qa/mobile/accessibility-testing-mobile.md` | Tobias Weber    |
| Visual Regression Testing    | `testing-qa/mobile/visual-regression-testing.md`    | Tobias Weber    |

#### API & Contract Testing

| Guideline             | File                                               | Owner           |
| --------------------- | -------------------------------------------------- | --------------- |
| Automated Test Suite  | `testing-qa/api-contract/automated-test-suite.md`  | Priscilla Oduya |
| Pact Contract Testing | `testing-qa/api-contract/pact-contract-testing.md` | Priya Sharma    |

#### Performance

| Guideline              | File                                               | Owner           |
| ---------------------- | -------------------------------------------------- | --------------- |
| k6 Performance         | `testing-qa/performance/k6-performance.md`         | Priya Sharma    |
| Code Coverage Analysis | `testing-qa/performance/code-coverage-analysis.md` | Ananya Krishnan |
| axe-core WCAG Testing  | `testing-qa/performance/axe-core-wcag-testing.md`  | Aisha Patel     |

#### Strategy & Process

| Guideline                     | File                                                      | Owner           |
| ----------------------------- | --------------------------------------------------------- | --------------- |
| Quality Engineering Strategy  | `testing-qa/strategy/quality-engineering-strategy.md`     | Aisha Patel     |
| Defect Triage                 | `testing-qa/strategy/defect-triage-and-classification.md` | Priscilla Oduya |
| Unit Test Architecture        | `testing-qa/strategy/unit-test-architecture.md`           | Ananya Krishnan |
| CI/CD Test Integration        | `testing-qa/strategy/cicd-test-integration.md`            | Tobias Weber    |
| Localization Testing Strategy | `testing-qa/strategy/localization-testing-strategy.md`    | Aisha Patel     |

### devops (21 guidelines)

| Guideline              | File                                                   | Owner         |
| ---------------------- | ------------------------------------------------------ | ------------- |
| CI/CD Infrastructure   | `devops/guidelines/cicd-infrastructure-engineering.md` | Thomas Zhang  |
| Developer Platform     | `devops/guidelines/developer-platform-engineering.md`  | David Okonkwo |
| Build Optimization     | `devops/guidelines/build-optimization.md`              | Kai Nakamura  |
| Developer Analytics    | `devops/guidelines/developer-analytics.md`             | Kai Nakamura  |
| CI/CD Optimization     | `devops/guidelines/ci-cd-optimization.md`              | Zara Okonkwo  |
| Test Infrastructure    | `devops/guidelines/test-infra.md`                      | Zara Okonkwo  |
| SRE Practices          | `devops/guidelines/sre-practices.md`                   | Raihan Rahman |
| Cloud Infrastructure   | `devops/guidelines/cloud-infrastructure.md`            | Raihan Rahman |
| GCP Multi-Region       | `devops/guidelines/gcp-multi-region.md`                | Raihan Rahman |
| Infrastructure as Code | `devops/guidelines/infrastructure-as-code.md`          | Yuki Matsuda  |
| IaC & GitOps           | `devops/guidelines/iac-gitops.md`                      | Yuki Tanaka   |
| CI/CD Security         | `devops/guidelines/cicd-security.md`                   | Yuki Matsuda  |
| Secrets Management     | `devops/guidelines/secrets-management.md`              | Leila Khoury  |
| Observability Logging  | `devops/guidelines/observability-logging.md`           | Elin Ström    |
| AWS Management         | `devops/guidelines/aws-management.md`                  | Leila Nasser  |
| Monitoring & Audit     | `devops/guidelines/monitoring-audit.md`                | Leila Nasser  |
| Network Security       | `devops/guidelines/network-security-fundamentals.md`   | Leila Nasser  |
| Bazel Build System     | `devops/guidelines/bazel-build-system.md`              | Kai Nakamura  |
| Compliance Foundations | `devops/guidelines/compliance-foundations.md`          | Thomas Zhang  |
| Kubernetes at Scale    | `devops/guidelines/kubernetes-at-scale.md`             | Yuki Tanaka   |
| Container Runtime      | `devops/guidelines/container-runtime-security.md`      | Elin Ström    |

### shared (7 guidelines)

| Guideline                 | File                                            | Owner           |
| ------------------------- | ----------------------------------------------- | --------------- |
| Performance Optimization  | `shared/guidelines/performance-optimization.md` | Amira Voss      |
| WCAG Mobile Roadmap       | `shared/guidelines/wcag-mobile-roadmap.md`      | Amira Voss      |
| WebAuthn & Biometric Auth | `shared/guidelines/webauthn-biometric-auth.md`  | Sora Kim        |
| Multi-Tenant Isolation    | `shared/guidelines/multi-tenant-isolation.md`   | Marcus Wright   |
| Docker Orchestration      | `shared/guidelines/docker-orchestration.md`     | Nina Petrova    |
| Developer Documentation   | `shared/guidelines/developer-documentation.md`  | Henrik Larsen   |
| Test-Driven Development   | `shared/guidelines/test-driven-development.md`  | Ananya Krishnan |

---

## Summary

| Resource                | Count | Location                                    |
| ----------------------- | ----- | ------------------------------------------- |
| SubAgent Configurations | 77    | `agents/`                                   |
| Skill Guidelines        | 199   | `skills/*/`                                 |
| Development Pipelines   | 4     | `pipeline/{mobile,web,backend,full-stack}/` |
| Recruitment Pipeline    | 1     | `pipeline/recruitment/pipeline.md`          |

---

## Usage

### Using SubAgents

To use a SubAgent, reference it by its file name (without `.md` extension). For example:

- `cto-dr-kenji-nakamura` — for architecture, SPEC development, UML Engineering Package
- `vp-mobile-marcus-andersson` — for mobile platform engineering leadership
- `vp-web-backend-elena-vasquez` — for distributed backend architecture
- `senior-architect-dr-elena-rostova` — for ADR governance and UML engineering
- `test-lead-priscilla-oduya` — for automated testing and P0-P3 defect triage

Each SubAgent's `description` field in the YAML frontmatter indicates when to engage that agent.

### Development Pipeline Reference

The `pipeline/mobile-development/pipeline.md` file contains the authoritative 10-stage development workflow definition for mobile product development. Reference it for:

- Stage gate criteria
- Artifact requirements (In/Out)
- Responsible producers and reviewers
- Defect handling procedures

### Recruitment Pipeline Reference

The `pipeline/recruitment/pipeline.md` file contains the authoritative 10-stage automated recruitment pipeline (Stage 0 planning + Stages 1-9 execution). Reference it for:

- Department planning workflow (Stage 0) and automated hiring workflow through 90-day onboarding
- Tiered engineering assessment (L0-L3), security role assessment, design leadership review, translation competency framework
- User review gate at Stage 8 (outcome-only leadership involvement)
- P1 Technical Debt Register (DR readiness, GDPR erasure, data contract enforcement)
- Platform-specific competency mappings (iOS HIG, Android Material, paywall experimentation)
