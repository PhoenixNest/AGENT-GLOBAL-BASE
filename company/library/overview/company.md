# Company Overview

A mobile product company organized around a structured, multi-stage development pipeline. The company specialises in building and shipping mobile applications for Android and iOS, with deep capability in cross-platform development (KMP, Flutter), internationalization, and platform security.

---

## Departments

The company is organized into six departments. Each department has a designated supervisor (C-suite or equivalent) and a team of recruited personnel.

| Department                                                                | Core Responsibility                                                                   | Supervisor(s)                                                 |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| [Brand Design](company/library/departments/brand-design.md)               | Mobile UI/UX design, prototyping, interaction design specifications                   | Chief Design Officer (CDO)                                    |
| [Cyberspace Security](company/library/departments/cyberspace-security.md) | Security requirements, architecture strategy, risk assessment, technology evaluation  | Chief Information Officer (CIO), Chief Security Officer (CSO) |
| [Human Resources](company/library/departments/human-resources.md)         | Recruitment, candidate vetting across all departments                                 | Chief Human Resources Officer (CHRO)                          |
| [Localization](company/library/departments/localization.md)               | Translation management, i18n pipeline, TMS operations across all target languages     | Chief Translation Officer (CTO-L)                             |
| [Product Management](company/library/departments/product-management.md)   | Product requirements, strategy, PRD authorship                                        | Chief Product Officer (CPO)                                   |
| [Research & Development](company/library/departments/research-develop.md) | Software architecture, Android/iOS/KMP/Flutter development, testing, i18n engineering | Chief Technology Officer (CTO)                                |

---

## Reporting Lines

```
User
 ├── CPO  (Product Management)
 ├── CDO  (Brand Design)        → reports to CIO
 ├── CTO  (R&D)                 → reports to CIO, CSO
 ├── CIO  (Cyberspace Security) → oversees Brand Design, Product Management, R&D
 ├── CSO  (Cyberspace Security) → oversees R&D
 ├── CHRO (Human Resources)
 └── CTO-L (Localization)
```

> The CIO occupies a cross-department oversight role: Brand Design, Product Management, and R&D all report to the CIO in addition to their primary supervisors.

---

## Personnel Tier System

All personnel are classified into one of three tiers:

| Tier                 | Description                                                                                                            |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **C-suite**          | Department supervisors placed before recruitment. Set strategy, own pipeline stage outputs, convene review panels.     |
| **Team Supervisors** | Senior leads recruited after C-suite. Own sub-department execution (e.g., Android Lead, iOS Lead, Software Architect). |
| **Teammates**        | Individual contributors. Execute work within the direction set by supervisors.                                         |

For the full personnel roster, see [`personnel.md`](personnel.md).

---

## Agent Systems Engineering (ASE) Framework

The company operates under the **Agent Systems Engineering (ASE)** methodology — a 4-layer governance framework for multi-agent coordination. It is mandatory across all development pipelines and ratified via ADR-ASE-001.

|        Layer        | Purpose                              | Examples                                |
| :-----------------: | :----------------------------------- | :-------------------------------------- |
| Prompt Engineering  | Standardised agent instructions      | 79 agent profiles, 199 skill guidelines |
| Context Engineering | Structured handoffs, context windows | MVC profiles, stage transition schemas  |
| Harness Engineering | Automated gate enforcement           | Schema validation, red team review      |
|    RAG / Memory     | Institutional knowledge retention    | KTP, RAG blueprint, embedding stores    |

> **Full specification:** See [`pipeline.md`](pipeline.md) § Agent Systems Engineering (ASE) Framework.

---

## Development Pipelines

The company operates **4 development pipelines** and **1 recruitment pipeline**:

| Pipeline           | Scope                                | Template Location                      |
| :----------------- | :----------------------------------- | :------------------------------------- |
| Mobile Development | iOS, Android, KMP, Flutter           | `company/pipeline/mobile-development/` |
| Web Development    | PWA, SPA, SSR                        | `company/pipeline/web-development/`    |
| Backend API        | REST, GraphQL, gRPC                  | `company/pipeline/backend-api/`        |
| Full-Stack         | Coordinated web + mobile + backend   | `company/pipeline/full-stack/`         |
| Recruitment        | 9-stage hiring pipeline (CHRO-owned) | `company/pipeline/recruitment/`        |

> **Full specification:** [`pipeline.md`](pipeline.md)

---

## Directory Structure

```
company/
  departments/       ← Full agent profiles and skill files
  library/           ← This knowledge hub (you are here)
  pipeline/          ← Full development pipeline definition
```

- **Agent profiles:** `departments/<dept>/supervisor/<role>/agent/profile.md` or `departments/<dept>/team/<tier>/<role>/agent/profile.md`
- **Skill files:** `departments/<dept>/.../skills/<skill-name>.md`
- **Pipeline definitions:** `pipeline/<pipeline-name>/pipeline.md`
- **ASE templates:** `company/pipeline/<pipeline-name>/templates/monitoring/`
