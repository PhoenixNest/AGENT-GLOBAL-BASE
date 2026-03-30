# Research & Development Department

The company's engineering department, responsible for software architecture, platform development (Android, iOS, KMP, Flutter), automated testing, internationalization engineering, and technical project management. The CTO oversees and coordinates all R&D output from Stage 3 through Stage 10.

> Reports to the Chief Technology Officer (CTO), the Chief Information Officer (CIO), and the Chief Security Officer (CSO).

---

## C-Suite Supervisor

| Name | Role | Seniority | Profile |
| --- | --- | --- | --- |
| Dr. Kenji Nakamura | Chief Technology Officer (CTO) | C-suite | [`profile.md`](../../departments/research-develop/supervisor/chief-technology-officer/agent/profile.md) |

**CTO Skills:**

| Skill File | Purpose |
| --- | --- |
| [`spec-development.md`](../../departments/research-develop/supervisor/chief-technology-officer/skills/spec-development.md) | Technical specification development using SPEC techniques |
| [`software-architecture-design.md`](../../departments/research-develop/supervisor/chief-technology-officer/skills/software-architecture-design.md) | Software architecture design and UML modelling |
| [`mobile-technology-strategy.md`](../../departments/research-develop/supervisor/chief-technology-officer/skills/mobile-technology-strategy.md) | Technology strategy for mobile platforms |
| [`technical-project-management.md`](../../departments/research-develop/supervisor/chief-technology-officer/skills/technical-project-management.md) | Implementation planning, Gantt charts, Progress Sync Protocol, milestone tracking |

---

## Team Supervisors

| Name | Role | Sub-department | Profile |
| --- | --- | --- | --- |
| Rafael Okonkwo | Software Architect | Cross-cutting | [`profile.md`](../../departments/research-develop/team/supervisors/software-architect/agent/profile.md) |
| Priscilla Oduya | Test Lead | Cross-cutting | [`profile.md`](../../departments/research-develop/team/supervisors/test-lead/agent/profile.md) |
| Kofi Asante-Mensah | Android Development Lead | Android | [`profile.md`](../../departments/research-develop/team/supervisors/android-development-lead/agent/profile.md) |
| Seo-Yeon Park | iOS Development Lead | iOS | [`profile.md`](../../departments/research-develop/team/supervisors/ios-development-lead/agent/profile.md) |
| Mei-Ling Johansson | Cross-Platform Development Lead | KMP / Flutter | [`profile.md`](../../departments/research-develop/team/supervisors/cross-platform-development-lead/agent/profile.md) |

**Skills by role:**

| Role | Skill Files |
| --- | --- |
| Software Architect | [`uml-engineering-package.md`](../../departments/research-develop/team/supervisors/software-architect/skills/uml-engineering-package.md) · [`mobile-architecture-patterns.md`](../../departments/research-develop/team/supervisors/software-architect/skills/mobile-architecture-patterns.md) · [`architecture-decision-records.md`](../../departments/research-develop/team/supervisors/software-architect/skills/architecture-decision-records.md) |
| Test Lead | [`automated-test-suite.md`](../../departments/research-develop/team/supervisors/test-lead/skills/automated-test-suite.md) · [`defect-triage-and-classification.md`](../../departments/research-develop/team/supervisors/test-lead/skills/defect-triage-and-classification.md) |
| Android Development Lead | [`android-implementation.md`](../../departments/research-develop/team/supervisors/android-development-lead/skills/android-implementation.md) |
| iOS Development Lead | [`ios-implementation.md`](../../departments/research-develop/team/supervisors/ios-development-lead/skills/ios-implementation.md) |
| Cross-Platform Development Lead | [`kmp-implementation.md`](../../departments/research-develop/team/supervisors/cross-platform-development-lead/skills/kmp-implementation.md) · [`flutter-implementation.md`](../../departments/research-develop/team/supervisors/cross-platform-development-lead/skills/flutter-implementation.md) |

---

## Team Teammates

| Name | Role | Profile |
| --- | --- | --- |
| Tomas Dvoracek | Internationalization Specialist | [`profile.md`](../../departments/research-develop/team/teammates/internationalization-specialist/agent/profile.md) |

| Skill File | Purpose |
| --- | --- |
| [`string-extraction-and-resource-files.md`](../../departments/research-develop/team/teammates/internationalization-specialist/skills/string-extraction-and-resource-files.md) | Scans codebase for hardcoded strings; produces platform resource files (`strings.xml`, `Localizable.strings`, `Localizable.stringsdict`, JSON datasets) |

---

## Pipeline Stages

| Stage | Role |
| --- | --- |
| **Stage 3** — Prototype → UML Engineering Package | **CTO: Responsible Producer (UML).** Coordinates with CIO and R&D to produce UML diagrams (class, sequence, component) and documentation. Software Architect supports UML work. |
| **Stage 4** — UML → Coding Implementation Plan | **CTO: Responsible Producer.** Produces Implementation Plan and Gantt Chart using SPEC techniques. Technology decisions from Stage 3 are locked; the plan executes against them. |
| **Stage 5** — Plan → Software Development | **CTO: Responsible Producer.** Oversees development by platform leads (Android, iOS, Cross-Platform). Tracks progress against Gantt Chart via Progress Sync Protocol. |
| **Stage 6** — Code Review | **CTO: Convenes review panel** (CPO, CDO, CTO, CIO, CSO). Software Architect participates as reviewer. |
| **Stage 7** — Code Review → Automated Testing | **CTO + Test Lead: Responsible Producers.** Test Lead (Priscilla Oduya) designs and executes automated test suite. Target: 100% pass rate. |
| **Stage 8** — Testing → Integrity Verification | **CTO: Convenes review panel** (all C-suite + Brand Design + R&D). Platform Leads and Test Lead participate. |
| **Stage 9** — Integrity Verification → i18n Engineering | **Internationalization Specialist (Tomas Dvoracek):** Scans codebase, extracts strings, produces resource files, delivers handoff package to CTO-L. |
| **Stage 10** — Release Readiness Check | **CTO: Convenes final panel.** Signs off on architecture (with CIO) and testing criteria. Co-signs platform criterion (with CPO). |

---

## Reference Links

See [`reference/development/links.md`](../reference/development/links.md) for Android, iOS, KMP, Flutter, and security documentation.

For cross-cutting topics: [`topics/architecture.md`](../topics/architecture.md) · [`topics/testing.md`](../topics/testing.md) · [`topics/localization.md`](../topics/localization.md) · [`topics/security.md`](../topics/security.md)
