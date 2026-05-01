# Product Requirements Document (PRD) — Template

> **Stage:** 1 — Concept
> **Producer:** Studio Director (Dr. Marcus Vogel)
> **Kill Gate:** KG-1 — Concept Validation
> **User Approval:** ✅ Required before advancing to Stage 2

---

## Document Control

| Field          | Value             |
| :------------- | :---------------- |
| **Game Title** | [Working title]   |
| **Version**    | v0.1 (Concept)    |
| **Date**       | YYYY-MM-DD        |
| **Author**     | [Studio Director] |

---

## 1. Problem Statement

> What player need or market gap does this game address?

[2–3 sentences describing the unmet player need, the market opportunity, and why now is the right time to build this game]

---

## 2. Success Metrics

### 2.1 Primary KPIs

| Metric                             | Target    | Measurement Method |
| :--------------------------------- | :-------- | :----------------- |
| D1 Retention                       | ≥ [X]%    | Analytics events   |
| D7 Retention                       | ≥ [X]%    | Analytics events   |
| D30 Retention                      | ≥ [X]%    | Analytics events   |
| ARPDAU                             | ≥ $[X.XX] | Revenue / DAU      |
| MAU at 3 months post-global launch | ≥ [X,XXX] | Analytics          |

### 2.2 Kill Gate Thresholds (summary)

| Kill Gate             | Key Metric               | Threshold            |
| :-------------------- | :----------------------- | :------------------- |
| KG-1 (Concept)        | Concept validation score | Internal review pass |
| KG-2 (Prototype)      | D1 retention (playtest)  | ≥ [X]%               |
| KG-3 (Vertical Slice) | D7 retention (playtest)  | ≥ [X]%               |
| KG-5 (Soft Launch)    | D30 MAU                  | ≥ [X,XXX]            |

---

## 3. Platform Requirements

| Requirement           |        iOS         |      Android       |
| :-------------------- | :----------------: | :----------------: |
| Minimum OS version    |      iOS [X]       |    Android [X]     |
| Target device tiers   | [Low / Mid / High] | [Low / Mid / High] |
| Offline play required |    ☐ Yes / ☐ No    |    ☐ Yes / ☐ No    |
| Push notifications    |    ☐ Yes / ☐ No    |    ☐ Yes / ☐ No    |
| IAP required          |    ☐ Yes / ☐ No    |    ☐ Yes / ☐ No    |

---

## 4. Functional Requirements

### 4.1 Core Gameplay

| ID     | Requirement                      | Priority |
| :----- | :------------------------------- | :------: |
| FR-001 | [Core mechanic requirement]      |    P0    |
| FR-002 | [Progression system requirement] |    P0    |
| FR-003 | [Session management requirement] |    P0    |

### 4.2 Monetisation

| ID     | Requirement                  | Priority |
| :----- | :--------------------------- | :------: |
| MR-001 | [IAP requirement]            |    P0    |
| MR-002 | [Ad integration requirement] |    P1    |

### 4.3 Social / Retention

| ID     | Requirement                  | Priority |
| :----- | :--------------------------- | :------: |
| RR-001 | [Daily reward requirement]   |    P1    |
| RR-002 | [Social feature requirement] |    P2    |

---

## 5. Non-Functional Requirements

| Category            | Requirement                                        |
| :------------------ | :------------------------------------------------- |
| **Performance**     | App launch cold start < [X]s on target device tier |
| **Crash-free rate** | ≥ 99% crash-free sessions                          |
| **Localisation**    | [Languages] from launch                            |
| **Accessibility**   | Colour-blind mode; scalable text                   |
| **Data privacy**    | GDPR and CCPA compliant                            |

---

## 6. Out of Scope (Concept Stage)

The following are explicitly out of scope for Kill Gate 1 and will be addressed in later stages:

- Full art asset production (Stage 5)
- Backend infrastructure design (Stage 3)
- Localisation (Stage 9)
- Live ops systems (Stage 10)

---

## 7. Assumptions and Dependencies

| Type           | Description                                                                  |
| :------------- | :--------------------------------------------------------------------------- |
| **Assumption** | [e.g. Unity 6.3 LTS supports all required platform features]                 |
| **Dependency** | [e.g. Stage 0 Art Direction must be complete before concept art is produced] |
| **Constraint** | [e.g. Total budget cap per studio charter]                                   |

---

**Produced by:** [Studio Director] on YYYY-MM-DD
**Reviewed by:** [Creative Director] on YYYY-MM-DD
