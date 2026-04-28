# Product Management Department

Responsible for translating user requirements into a structured, reviewable Product Requirements Document (PRD) and driving product strategy across all pipeline stages. The division operates under a **"Template Steward + Distributed Production"** model, ensuring high standards across Mobile, Web, and API surfaces.

> Reports to the Chief Product Officer (CPO) and the Chief Information Officer (CIO).

---

## Leadership

| Name                    | Role                                  | Seniority | Profile                                                                                                        |
| :---------------------- | :------------------------------------ | :-------- | :------------------------------------------------------------------------------------------------------------- |
| **Marcus Tran-Yoshida** | **Chief Product Officer (CPO)**       | C-suite   | [`profile.md`](../../departments/product-management/supervisor/chief-product-officer/agent/profile.md)         |
| **Julia Thorne**        | VP Product, Web Platforms             | VP-tier   | [`profile.md`](../../departments/product-management/team/supervisors/vp-product-web-platform/agent/profile.md) |
| **Alex Rivera**         | VP Product, API & Developer Platforms | VP-tier   | [`profile.md`](../../departments/product-management/team/supervisors/vp-product-api-platform/agent/profile.md) |

### Operating Model: Template Steward + Distributed Production

To prevent structural bottlenecks while maintaining rigorous quality, the department utilizes a distributed ownership model for Stage 1 PRD production:

- **The CPO (Marcus Tran-Yoshida)** serves as the **Template Steward**. He owns the authoritative PRD standard (`prd-authorship.md`) and provides final sign-off on all PRDs advancing to Stage 2.
- **The VPs (Julia Thorne & Alex Rivera)** serve as **Domain Producers**. They hold primary Stage 1 authority for their respective pipelines, authoring requirements with native-domain depth.

---

## Division Skills

| Skill File                                                                                                                                | Purpose                                                                              | Owner  |
| :---------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- | :----- |
| [`prd-authorship.md`](../../departments/product-management/supervisor/chief-product-officer/skills/prd-authorship.md)                     | **Company Standard:** PRD structure, acceptance criteria, and platform requirements. | CPO    |
| [`mobile-product-strategy.md`](../../departments/product-management/supervisor/chief-product-officer/skills/mobile-product-strategy.md)   | Mobile prioritisation, HIG/Material constraints, and app-store mechanics.            | CPO    |
| [`web-product-strategy.md`](../../departments/product-management/team/supervisors/vp-product-web-platform/skills/web-product-strategy.md) | Web conversion funnels, accessibility (WCAG 2.1 AA), and PWA/SPA/SSR strategy.       | VP Web |
| [`api-product-strategy.md`](../../departments/product-management/team/supervisors/vp-product-api-platform/skills/api-product-strategy.md) | OpenAPI standards, DX metrics, monetization, and API lifecycle management.           | VP API |

---

## Pipeline Stages

| Stage                                   | Role & Ownership                                                                                                                                                                                                                                                                 |
| :-------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 1** — Requirements → PRD + SRD  | **Primary Authority:** Transferred per pipeline type:<br>• **Mobile:** CPO (Marcus)<br>• **Web:** VP Web (Julia)<br>• **API:** VP API (Alex)<br>• **Full-Stack:** Joint VP Web + VP API authorship.<br><br>**Sign-off:** CPO remains the Accountable Approver for all pipelines. |
| **Stage 2** — PRD → Web Prototype + IDS | **Handoff Partner:** The relevant VP (or CPO for Mobile) reviews prototypes against the PRD. Must approve before advance.                                                                                                                                                        |
| **Stage 6** — Code Review               | **Advisor:** VPs attend as domain advisors for their pipeline; CPO verifies requirement implementation.                                                                                                                                                                          |
| **Stage 8** — Integrity Verification    | **Reviewer:** VPs co-review with the CPO to confirm features remain intact after testing (anti-pattern check).                                                                                                                                                                   |
| **Stage 9** — i18n Engineering          | **Structural Reviewer:** Alongside CDO and CTO, confirms string extraction and resource file structure.                                                                                                                                                                          |
| **Stage 10** — Release Readiness Check  | **Sign-off authority:** CPO certifies PRD verification; VPs co-sign readiness for their respective pipelines.                                                                                                                                                                    |

---

## Key Artifacts Produced

- **Product Requirements Document (PRD)** — Defines features, acceptance criteria, and platform targets. Paired with the SRD from Stage 1. Under the new model, PRDs contain platform-native extensions for Web and API surfaces.

---

## Note on Target Platforms

Before a PRD is initiated, the user must confirm the target platforms: **Android**, **iOS**, **Web**, or **API**. This choice determines which leader takes primary authorship and which domain-specific strategy skills are applied.
