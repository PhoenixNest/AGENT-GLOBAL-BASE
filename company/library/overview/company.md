# Company Overview

A mobile product company organized around a structured, multi-stage development pipeline. The company specialises in building and shipping mobile applications for Android and iOS, with deep capability in cross-platform development (KMP, Flutter), internationalization, and platform security.

---

## Departments

The company is organized into six departments. Each department has a designated supervisor (C-suite or equivalent) and a team of recruited personnel.

| Department                                                   | Core Responsibility                                                                   | Supervisor(s)                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| [Brand Design](../departments/brand-design.md)               | Mobile UI/UX design, prototyping, interaction design specifications                   | Chief Design Officer (CDO)                                    |
| [Cyberspace Security](../departments/cyberspace-security.md) | Security requirements, architecture strategy, risk assessment, technology evaluation  | Chief Information Officer (CIO), Chief Security Officer (CSO) |
| [Human Resources](../departments/human-resources.md)         | Recruitment, candidate vetting across all departments                                 | Chief Human Resources Officer (CHRO)                          |
| [Localization](../departments/localization.md)               | Translation management, i18n pipeline, TMS operations across all target languages     | Chief Translation Officer (CTO-L)                             |
| [Product Management](../departments/product-management.md)   | Product requirements, strategy, PRD authorship                                        | Chief Product Officer (CPO)                                   |
| [Research & Development](../departments/research-develop.md) | Software architecture, Android/iOS/KMP/Flutter development, testing, i18n engineering | Chief Technology Officer (CTO)                                |

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

## Directory Structure

```
company/
  departments/       ← Full agent profiles and skill files
  library/           ← This knowledge hub (you are here)
  pipeline/          ← Full development pipeline definition
```

- **Agent profiles:** `departments/<dept>/supervisor/<role>/agent/profile.md` or `departments/<dept>/team/<tier>/<role>/agent/profile.md`
- **Skill files:** `departments/<dept>/.../skills/<skill-name>.md`
- **Full pipeline:** `pipeline/development/pipeline.md`
