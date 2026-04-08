# Product Management Department

Responsible for translating user requirements into a structured, reviewable Product Requirements Document (PRD) and driving product strategy across all pipeline stages. The CPO is the primary voice of the product throughout the development lifecycle — from requirements at Stage 1 through final release sign-off at Stage 10.

> Reports to the Chief Product Officer (CPO) and the Chief Information Officer (CIO).

---

## Supervisor

| Name                | Role                        | Seniority | Profile                                                                                                |
| ------------------- | --------------------------- | --------- | ------------------------------------------------------------------------------------------------------ |
| Marcus Tran-Yoshida | Chief Product Officer (CPO) | C-suite   | [`profile.md`](../../departments/product-management/supervisor/chief-product-officer/agent/profile.md) |

**CPO Skills:**

| Skill File                                                                                                                              | Purpose                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| [`mobile-product-strategy.md`](../../departments/product-management/supervisor/chief-product-officer/skills/mobile-product-strategy.md) | Mobile product strategy, competitive analysis, roadmap prioritisation, platform-specific product decisions               |
| [`prd-authorship.md`](../../departments/product-management/supervisor/chief-product-officer/skills/prd-authorship.md)                   | Product Requirements Document authorship: feature specifications, acceptance criteria, edge cases, platform requirements |

---

## Pipeline Stages

| Stage                                   | Role                                                                                                                                                                                                                                                   |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Stage 1** — Requirements → PRD + SRD  | **Responsible Producer (PRD).** Receives user requirements, determines target platforms, produces the Product Requirements Document. Convenes CIO and CTO for review. Iterates until user confirms no further revisions. Archives PRD paired with SRD. |
| **Stage 2** — PRD → Web Prototype + IDS | **Reviewer.** Reviews CDO prototypes against the PRD. Must approve before prototypes advance.                                                                                                                                                          |
| **Stage 6** — Code Review               | **Reviewer.** Verifies all PRD requirements have been fully implemented in the codebase.                                                                                                                                                               |
| **Stage 8** — Integrity Verification    | **Reviewer.** Confirms all PRD features remain intact after the testing remediation phase (anti-pattern check: no functionality removed to achieve passing tests).                                                                                     |
| **Stage 9** — i18n Engineering          | **Structural completeness reviewer.** Alongside CDO and CTO, confirms all hardcoded strings extracted and resource files correctly structured (structure review only — not translation accuracy).                                                      |
| **Stage 10** — Release Readiness Check  | **Sign-off authority.** CPO certifies: all PRD requirements implemented and verified. Also co-signs Platform criterion (App Store / Google Play requirements met).                                                                                     |

---

## Key Artifacts Produced

- **Product Requirements Document (PRD)** — Defines features, acceptance criteria, edge cases, and platform targets. Paired with the SRD from Stage 1 and travels as a unit through all subsequent stages.

---

## Note on Target Platforms

Before the CPO begins PRD authorship, the user must confirm their intended release platforms: **Android**, **iOS**, or **both**. This decision gates Stage 1 and shapes the PRD's platform-specific requirements sections.
