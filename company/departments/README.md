# Departments

This directory contains all company departments. Each department holds a `supervisor/` directory for its C-suite lead (placed before recruitment) and a `team/` directory for subsequently recruited personnel, split into `supervisors/` and `teammates/` by seniority tier.

> **Reporting structure:** Each agent's `agent/profile.md` frontmatter identifies their `role`, `tier`, and `seniority`. Skill files in `skills/` define how each agent executes their responsibilities.

---

## Directory Map

```text
departments/
  brand-design/
    supervisor/chief-design-officer/
    team/teammates/product-ui-ux-prototyper/
  cyberspace-security/
    supervisor/chief-information-officer/
    supervisor/chief-security-officer/
  human-resources/
    supervisor/chief-human-resources-officer/
  localization/
    supervisor/chief-translation-officer/
    team/teammates/chinese-linguist/
    team/teammates/english-linguist/
    team/teammates/french-linguist/
    team/teammates/japanese-linguist/
    team/teammates/korean-linguist/
    team/teammates/localization-engineer/
  product-management/
    supervisor/chief-product-officer/
  research-develop/
    supervisor/chief-technology-officer/
    team/supervisors/android-development-lead/
    team/supervisors/cross-platform-development-lead/
    team/supervisors/ios-development-lead/
    team/supervisors/software-architect/
    team/supervisors/test-lead/
    team/teammates/internationalization-specialist/
```

---

## Brand Design Department

> Reports to the Chief Design Officer (CDO) and the Chief Information Officer (CIO).

Supervisor:

| Name             | Role                 | Path                                            |
| ---------------- | -------------------- | ----------------------------------------------- |
| Yuki Tanaka-Chen | Chief Design Officer | `brand-design/supervisor/chief-design-officer/` |

Skills: `mobile-design-systems` · `interaction-design-specification` · `design-to-engineering-handoff` · `user-research-driven-design`

Teammates:

| Name         | Role                     | Path                                                    |
| ------------ | ------------------------ | ------------------------------------------------------- |
| Lena Vasquez | Product UI/UX Prototyper | `brand-design/team/teammates/product-ui-ux-prototyper/` |

Skills: `web-prototype-development` · `interaction-design-specification`

Translates CPO product requirements into high-fidelity, browser-runnable HTML prototypes. Upon final approval, produces the Interaction Design Specification (IDS) and delivers both artifacts to the R&D Department and CTO at the close of Stage 2.

---

## Cyberspace Security Department

> Reports to the Chief Security Officer (CSO) and the Chief Information Officer (CIO).

Supervisors:

| Name            | Role                      | Path                                                        |
| --------------- | ------------------------- | ----------------------------------------------------------- |
| Dr. Priya Mehta | Chief Information Officer | `cyberspace-security/supervisor/chief-information-officer/` |
| Dr. Sarah Chen  | Chief Security Officer    | `cyberspace-security/supervisor/chief-security-officer/`    |

CIO Skills: `technology-evaluation` · `mobile-architecture-strategy` · `technical-selection-documentation`

CSO Skills: `mobile-security-architecture` · `application-security-hardening` · `security-risk-assessment` · `emerging-threat-evaluation`

---

## Human Resources Department

> Reports to the Chief Human Resources Officer (CHRO).

Supervisor:

| Name                | Role                          | Path                                                        |
| ------------------- | ----------------------------- | ----------------------------------------------------------- |
| Dr. Evelyn Hartwell | Chief Human Resources Officer | `human-resources/supervisor/chief-human-resources-officer/` |

Skills: `vet-candidate` · `recruit-engineering` · `recruit-product` · `recruit-design` · `recruit-data` · `recruit-business` · `recruit-translation`

---

## Localization Department

> Reports to the Chief Translation Officer (CTO-L). Activated mid-way through Stage 9, after the R&D Department delivers the string extraction handoff package.

Supervisor:

| Name                  | Role                      | Path                                                 |
| --------------------- | ------------------------- | ---------------------------------------------------- |
| Dr. Amara Osei-Mensah | Chief Translation Officer | `localization/supervisor/chief-translation-officer/` |

Skills: `language-translation-module`

Teammates:

| Name                    | Role                  | Language Pairs           | Path                                                 |
| ----------------------- | --------------------- | ------------------------ | ---------------------------------------------------- |
| Amelia Hartington       | English Linguist      | EN-US / EN-GB            | `localization/team/teammates/english-linguist/`      |
| Wei-Chen Liu            | Chinese Linguist      | ZH-CN / ZH-TW            | `localization/team/teammates/chinese-linguist/`      |
| Haruki Yoshimoto        | Japanese Linguist     | JA                       | `localization/team/teammates/japanese-linguist/`     |
| Ji-Hyun Bae             | Korean Linguist       | KO                       | `localization/team/teammates/korean-linguist/`       |
| Isabelle Moreau-Leclerc | French Linguist       | FR-FR / FR-CA            | `localization/team/teammates/french-linguist/`       |
| Dario Esposito          | Localization Engineer | (pipeline engineering)   | `localization/team/teammates/localization-engineer/` |

Shared linguist skill: `mobile-ui-translation` (present in each linguist's `skills/` directory)

Localization Engineer skill: `localization-pipeline-engineering`

The Localization Engineer runs the TMS pipeline (string intake, push, pull, validation linting). Linguists translate within the TMS. The CTO-L governs all work via the Language Translation Module and issues the Translation Verification Report.

---

## Product Management Department

> Reports to the Chief Product Officer (CPO) and the Chief Information Officer (CIO).

Supervisor:

| Name                | Role                  | Path                                                   |
| ------------------- | --------------------- | ------------------------------------------------------ |
| Marcus Tran-Yoshida | Chief Product Officer | `product-management/supervisor/chief-product-officer/` |

Skills: `mobile-product-strategy` · `prd-authorship`

---

## R&D Department

> Reports to the Chief Technology Officer (CTO), the Chief Information Officer (CIO), and the Chief Security Officer (CSO).

Sub-departments: Android Development, iOS Development, Cross-Platform Development (KMP, Flutter)

Supervisor (C-suite):

| Name               | Role                     | Path                                                    |
| ------------------ | ------------------------ | ------------------------------------------------------- |
| Dr. Kenji Nakamura | Chief Technology Officer | `research-develop/supervisor/chief-technology-officer/` |

Skills: `spec-development` · `software-architecture-design` · `mobile-technology-strategy` · `technical-project-management`

Team supervisors:

| Name               | Role                            | Sub-department | Path                                                                 |
| ------------------ | ------------------------------- | -------------- | -------------------------------------------------------------------- |
| Rafael Okonkwo     | Software Architect              | Cross-cutting  | `research-develop/team/supervisors/software-architect/`              |
| Priscilla Oduya    | Test Lead                       | Cross-cutting  | `research-develop/team/supervisors/test-lead/`                       |
| Kofi Asante-Mensah | Android Development Lead        | Android        | `research-develop/team/supervisors/android-development-lead/`        |
| Seo-Yeon Park      | iOS Development Lead            | iOS            | `research-develop/team/supervisors/ios-development-lead/`            |
| Mei-Ling Johansson | Cross-Platform Development Lead | KMP / Flutter  | `research-develop/team/supervisors/cross-platform-development-lead/` |

Architect Skills: `uml-engineering-package` · `mobile-architecture-patterns` · `architecture-decision-records`

Test Lead Skills: `automated-test-suite` · `defect-triage-and-classification`

Android Lead Skills: `android-implementation`

iOS Lead Skills: `ios-implementation`

Cross-Platform Lead Skills: `kmp-implementation` · `flutter-implementation`

Team teammates:

| Name           | Role                            | Path                                                               |
| -------------- | ------------------------------- | ------------------------------------------------------------------ |
| Tomas Dvoracek | Internationalization Specialist | `research-develop/team/teammates/internationalization-specialist/` |

Skills: `string-extraction-and-resource-files`

Owns Stage 9 i18n engineering: scans the integrity-verified codebase for hardcoded strings, produces platform resource files (`strings.xml`, `Localizable.strings`, `Localizable.stringsdict`, JSON datasets), and delivers the string extraction handoff package to the CTO-L.

---

## Pipeline Stage to Responsible Agent Index

| Stage | Name                                 | Responsible Producer(s)       | Key Agents                                                  |
| ----- | ------------------------------------ | ----------------------------- | ----------------------------------------------------------- |
| 1     | Requirements to PRD + SRD            | CPO (PRD), CSO (SRD)          | Marcus Tran-Yoshida, Dr. Sarah Chen                         |
| 2     | PRD to Web Prototype + IDS           | CDO                           | Yuki Tanaka-Chen, Lena Vasquez                              |
| 3     | Prototype to UML Engineering Package | CTO (UML), CIO (ADRs + TSD)   | Dr. Kenji Nakamura, Rafael Okonkwo, Dr. Priya Mehta         |
| 4     | UML to Coding Implementation Plan    | CTO                           | Dr. Kenji Nakamura                                          |
| 5     | Plan to Software Development         | CTO + Platform Leads          | Kofi Asante-Mensah, Seo-Yeon Park, Mei-Ling Johansson       |
| 6     | Development to Code Review           | CTO (panel)                   | All C-suite, Rafael Okonkwo                                 |
| 7     | Code Review to Automated Testing     | CTO + Test Lead               | Priscilla Oduya                                             |
| 8     | Testing to Integrity Verification    | CTO (panel)                   | All C-suite, Platform Leads, Priscilla Oduya                |
| 9     | Integrity to Internationalization    | CTO-L + R&D                   | Tomas Dvoracek, Dr. Amara Osei-Mensah, Linguist Team        |
| 10    | i18n to Release Readiness Check      | CTO (panel)                   | All C-suite + User                                          |
