# Pipeline Index

Central index of all development pipelines. Each pipeline governs a distinct product delivery track with its own 10-stage workflow.

---

## Active Pipelines

| Pipeline                                  | Status    | Description                                              | Definition                                      |
| ----------------------------------------- | --------- | -------------------------------------------------------- | ----------------------------------------------- |
| [Mobile Development](mobile-development/) | ✅ Active | Android, iOS, KMP Cross-Platform, Flutter Cross-Platform | [`pipeline.md`](mobile-development/pipeline.md) |
| [Web Development](web-development/)       | ✅ Active | PWA, SPA, SSR web applications + backend services        | [`pipeline.md`](web-development/pipeline.md)    |
| [Backend API](backend-api/)               | ✅ Active | Standalone REST/GraphQL APIs, microservices              | [`pipeline.md`](backend-api/pipeline.md)        |
| [Full-Stack Cross-Platform](full-stack/)  | ✅ Active | Coordinated web + mobile + backend delivery              | [`pipeline.md`](full-stack/pipeline.md)         |

---

## Pipeline Structure

Each pipeline follows a consistent 10-stage state machine:

| #   | Stage                                      | Key Output                              |
| --- | ------------------------------------------ | --------------------------------------- |
| 1   | Requirements → PRD + SRD                   | Product + Security Requirements         |
| 2   | PRD → Web Prototype + IDS                  | Interactive prototype + design specs    |
| 3   | Prototype → UML Engineering Package        | Architecture diagrams + ADRs + TSD      |
| 4   | UML → Coding Implementation Plan           | Implementation plan + Gantt chart       |
| 5   | Plan → Software Development                | Platform codebases                      |
| 6   | Development → Code Review                  | Defect Report + sign-off                |
| 7   | Code Review → Automated Testing            | Test suite + results report             |
| 8   | Automated Testing → Integrity Verification | Integrity sign-off                      |
| 9   | Integrity → i18n Engineering               | Localized codebase + translation report |
| 10  | i18n → Release Readiness Check             | Release decision                        |

---

## Pipeline Selection Guide

| Product Type                          | Use Pipeline              |
| ------------------------------------- | ------------------------- |
| Android app                           | Mobile Development        |
| iOS app                               | Mobile Development        |
| Android + iOS (native)                | Mobile Development        |
| Android + iOS (KMP)                   | Mobile Development        |
| Android + iOS (Flutter)               | Mobile Development        |
| Web app (PWA/SPA/SSR)                 | Web Development           |
| Backend API service                   | Backend API               |
| Full product (web + mobile + backend) | Full-Stack Cross-Platform |

---

## Historical Records

| Pipeline           | Optimization History                                                                   |
| ------------------ | -------------------------------------------------------------------------------------- |
| Mobile Development | [`mobile-development/optimization-history/`](mobile-development/optimization-history/) |

---

_Last updated: April 13, 2026_
