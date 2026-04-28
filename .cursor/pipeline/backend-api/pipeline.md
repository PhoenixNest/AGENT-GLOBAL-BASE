# Backend API Pipeline

## Overview

The company's backend API development workflow is a ten-stage state machine. At each stage you are required to log the current execution phase and update the workflow's progress. Each stage follows a consistent schema: **Relevant Personnel**, **Artifacts In**, **Artifacts Out**, a designated **Responsible Producer**, explicit **Reviewers**, **Gate Criteria** that must be satisfied before the stage closes, and **Defect Handling** where applicable.

Each workflow must be assigned to a designated responsible party. Each assigned individual is regarded as a "Subagent"; as the primary "Agent," you must collaborate with these Subagents — leveraging their respective skill sets — to successfully complete every task within the workflow.

---

## Defect Severity System (P0-P3)

Applied in Stages 6, 7, and 8. All identified defects must be classified before any remediation begins.

| Level | Definition                              | Release Impact                   |
| ----- | --------------------------------------- | -------------------------------- |
| P0    | App crash / data loss / security breach | Blocks release -- non-negotiable |
| P1    | Core feature broken / major UX failure  | Blocks release -- non-negotiable |
| P2    | Minor feature degraded / cosmetic issue | User decides to fix or defer     |
| P3    | Polish / nice-to-have                   | User decides to fix or defer     |

**Authority rule:** P0/P1 classification is final and cannot be overridden. P2/P3 defects are submitted to the user, who has explicit final authority to skip or defer them.

---

## Progress Sync Protocol

Active from Stage 4 onward.

- Each completed coding task triggers an update to the progress log.
- Any task exceeding its estimated duration by **>20%** triggers an automatic CTO to CPO schedule risk notification.
- The CTO produces weekly progress summaries (status indicators, milestone percentages, risk mitigation plans) for C-suite visibility.

**Full specification:** [`monitoring.md`](monitoring.md) -- Progress Monitoring & Recovery System (mandatory for Stage 4+ projects).

---

## API Strategy Matrix

### Overview

Stage 5 development executes per the **API Strategy Matrix**, which determines track activation based on the **API Strategy ADR** produced at Stage 3. The Stage 1 gate asks "What type of API service?" -- this confirms the **target delivery model** (REST, GraphQL, real-time). The **implementation approach** (REST vs GraphQL vs gRPC vs event-driven) is an architecture decision locked at **Stage 3**.

**Five mutually exclusive scenarios -- a project selects exactly one.**

### Decision Matrix

| Dimension                 | REST API               | GraphQL API              | Real-time Service (WebSocket) | Event-Driven Microservices | Simple CRUD API        |
| ------------------------- | ---------------------- | ------------------------ | ----------------------------- | -------------------------- | ---------------------- |
| **Stage 1 Gate**          | API service            | API service              | API service                   | API service                | API service            |
| **Stage 3 ADR**           | REST architecture      | GraphQL schema           | WebSocket architecture        | Kafka + CQRS architecture  | Simple REST            |
| **Stage 5 Active Tracks** | B-API + B-DATA         | B-API + B-DATA (L)       | B-API + B-DATA (L) + B-RT     | B-API (L) + B-DATA + B-RT  | B-API (L) + B-DATA (L) |
| **Stage 5 Team Size**     | 5                      | 4                        | 5                             | 7                          | 3                      |
| **Stage 6 Tier 1 Review** | Backend primary        | Backend primary          | All three leads               | All three leads            | Backend primary        |
| **Stage 7 Testing**       | Unit + contract + load | Unit + contract + schema | Load + chaos + WebSocket      | Load + chaos + integration | Unit + basic load      |
| **Stage 10 Submission**   | API gateway + docs     | API gateway + SDL        | API gateway + WS docs         | API gateway + event schema | API gateway + docs     |
| **CI/CD Scope**           | REST CI                | GraphQL CI               | WebSocket CI                  | Event-driven CI            | REST CI                |

### Track Activation Protocol

| Project Type               | Track B-API (API Services) | Track B-DATA (Data Layer) | Track B-RT (Real-time & Events) | Coordinator  |
| -------------------------- | -------------------------- | ------------------------- | ------------------------------- | ------------ |
| REST API service           | **FULL** (3 eng)           | **FULL** (2 eng)          | Dormant                         | Dev Malhotra |
| GraphQL API                | **FULL** (3 eng)           | **LIGHT** (1 eng)         | Dormant                         | Dev Malhotra |
| Real-time service          | **FULL** (2 eng)           | **LIGHT** (1 eng)         | **FULL** (2 eng)                | Dev Malhotra |
| Event-driven microservices | **LIGHT** (2 eng)          | **FULL** (2 eng)          | **FULL** (3 eng)                | Dev Malhotra |
| Simple CRUD API            | **LIGHT** (2 eng)          | **LIGHT** (1 eng)         | Dormant                         | Dev Malhotra |

**Track semantics:**

| Term        | Definition                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------- |
| **FULL**    | End-to-end feature implementation, testing, and delivery for that layer. Owns the complete codebase for that layer. |
| **LIGHT**   | Integration and adaptation only (e.g., API consumer wiring, schema migration). NOT full feature implementation.     |
| **PRIMARY** | Owns the shared integration layer. Coordinates cross-service contracts and data model consistency.                  |
| **Dormant** | Track lead and engineers are reassigned to technical debt, test automation, cross-training, or SDK migration prep.  |

### Resource Reallocation Protocol

| Scenario                   | Freed Resources           | Reassignment Options                                                   |
| -------------------------- | ------------------------- | ---------------------------------------------------------------------- |
| REST API service           | B-RT eng                  | Other projects, load test infrastructure, CI/CD hardening              |
| GraphQL API                | B-DATA eng, B-RT eng      | Other projects, schema optimization, contract test automation          |
| Real-time service          | None -- all tracks active | N/A                                                                    |
| Event-driven microservices | None -- all tracks active | N/A                                                                    |
| Simple CRUD API            | B-DATA eng, all B-RT eng  | Technical debt, database optimization, documentation, monitoring setup |

### Per-Scenario CI/CD Blueprint

| CI/CD Component | REST API            | GraphQL API         | Real-time Service          | Event-Driven Microservices | Simple CRUD API |
| --------------- | ------------------- | ------------------- | -------------------------- | -------------------------- | --------------- |
| Build CI        | Go/Node lint+build  | Node/TS build       | Go build                   | Go build                   | Go/Node build   |
| Unit CI         | Go test / Jest      | Jest / Vitest       | Go test                    | Go test                    | Go test         |
| Contract CI     | Pact verification   | Schema validation   | WebSocket protocol test    | Event schema validation    | Basic API test  |
| Integration CI  | Docker-compose + DB | Docker-compose + DB | Docker-compose + WS server | Docker-compose + Kafka     | Docker-compose  |
| Load CI         | k6                  | k6                  | k6 + WebSocket test        | k6 + Kafka test            | k6 basic        |
| Security CI     | Semgrep, ZAP, audit | Semgrep, ZAP, audit | Semgrep, ZAP, audit        | Semgrep, ZAP, audit        | Semgrep, audit  |
| Deployment      | Blue-green/canary   | Blue-green/canary   | Rolling update             | Rolling update             | Blue-green      |

### API Strategy ADR Requirements

The mandatory API Strategy ADR at Stage 3 must include **all 14 fields**:

1. **Decision statement** -- Which approach: REST, GraphQL, gRPC, or hybrid?
2. **Rationale** -- Why this approach? (consumer needs, team skills, performance requirements)
3. **Trade-offs** -- What is gained and sacrificed vs. alternatives?
4. **Team capability assessment** -- Do we have the right backend skills?
5. **Risk analysis** -- API versioning complexity, database scaling, event ordering
6. **TCO projection (24-month)** -- Infrastructure, monitoring, developer tooling, total estimated cost
7. **Vendor lock-in risk matrix** -- Framework abandonment risk, migration cost, hosting dependency
8. **Performance SLA alignment** -- P99 latency, throughput, error rate, uptime (99.9%+) -- can the chosen approach meet PRD thresholds?
9. **Security mandate** -- Rate limiting, input validation, CORS, CSRF, authZ
10. **STRIDE-based threat model** — API injection, broken auth, data exposure, DDoS
11. **Track activation mapping** — Explicit reference to which tracks are FULL, LIGHT, or Dormant per track
12. **Reassignment plan** — If tracks are dormant or light, where do freed engineers go?
13. **API versioning strategy** — URL path vs. header, deprecation timeline, backward compatibility
14. **Developer experience** — OpenAPI/Swagger docs, SDK generation, sandbox environment
15. **Feature flag governance** — Unified flag strategy, per-environment parity, kill switch protocol, staggered rollout coordination
16. **Deployment & Compliance Implications** — Cloud provider compliance (AWS/Azure/GCP region selection, data residency enforcement), third-party API/service terms review, data retention/deletion policy alignment, cross-border data transfer compliance

**Ownership:** CTO authors the ADR. Backend Lead + Data Lead provide input. CIO reviews for technology conformance. CSO reviews for security conformance. Once approved at Stage 3 gate, this decision is **locked** -- switching between strategies requires a full stage rollback (Stage 3 re-entry, ADR re-authorship, Implementation Plan re-baseline).

---

## Stage Definitions

### Stage 1: Requirements to PRD + SRD

**Relevant Personnel:** CPO (PRD), CSO (SRD)

**Artifacts In:** Raw product requirements, user research, market analysis

**Artifacts Out:**

- `PRD.md` -- Product Requirements Document (with JTBD, kill criteria, commercial assessment)
- `SRD.md` -- Security Requirements Document (expanded: rate limiting, data residency, SLA targets, GDPR compliance)

**Reviewers:** CTO, CIO, CSO, CPO

**Gate Criteria:**

1. User has confirmed target API type (REST, GraphQL, gRPC, real-time)
2. User has confirmed API consumer types (web frontend, mobile app, third-party integration, internal service)
3. PRD includes performance SLA targets (P99 latency, throughput, uptime, error rate)
4. SRD includes API-specific security requirements (rate limiting, input validation, authZ, CORS, API key lifecycle management, secret management strategy, DDoS mitigation thresholds, GraphQL-specific controls if applicable)
5. User has confirmed no further revisions are required

**Defect Handling:** P0/P1 defects block Stage 1 to 2. P2/P3 defects require user decision.

---

### Stage 2: PRD to API Specification + Developer Portal Prototype

**Relevant Personnel:** CTO (API Specification), CDO (Developer Portal Prototype)

**Artifacts In:** PRD, SRD (paired artifacts)

**Artifacts Out:**

- **API Specification** (owned by CTO/Backend Lead): OpenAPI/Swagger for REST, GraphQL SDL for GraphQL, protobuf for gRPC — includes endpoint definitions, request/response schemas, error response conventions (HTTP status codes, error payload structure), pagination/field selection patterns, rate limiting behavior documentation, versioning strategy
- **Developer Portal Prototype** (owned by CDO): Production-grade HTML/CSS/JS prototype including documentation layout, interactive API explorer (Swagger UI or equivalent), onboarding flow, error message display patterns
- **API Design Guidelines**: Naming conventions (resource naming, field naming), versioning strategy (URL path vs. header), deprecation timeline, backward compatibility rules
- **IDS** (for Developer Portal UI only): Component state matrices (for portal UI components), responsive breakpoints (portal must work on desktop/tablet), accessibility annotations (WCAG 2.1 AA), animation specs (for portal interactions)

**Reviewers:** CTO, CDO, CPO

**Gate Criteria:**

1. API specification validates (OpenAPI lint passes, GraphQL SDL validates)
2. API Design Guidelines documented and approved by Backend Lead
3. IDS includes WCAG 2.1 AA accessibility targets for **developer portal interface** (screen reader compatibility, keyboard navigation, color contrast for documentation pages and interactive explorer UI) — **not API payloads**
4. Interactive API mock server or Swagger UI instance demonstrates all endpoints with sample responses
5. CDO confirms **developer portal UX** design fidelity to PRD requirements (**not** API endpoint structure)
6. User has given final confirmation

**Defect Handling:** P0/P1 defects block Stage 2 to 3. P2/P3 defects require user decision.

---

### Stage 3: API Prototype to UML Engineering Package

**Relevant Personnel:** CTO (UML), CIO (ADRs, TSD)

**Artifacts In:** PRD, SRD, API specification, IDS

**Artifacts Out:**

- UML diagrams (class, sequence, component, activity)
- **9 mandatory ADRs**:
  - `ADR-API-STRATEGY.md` — REST vs GraphQL vs gRPC decision (16 fields + compliance implications, including data consistency model)
  - `ADR-FEATURE-FLAGS.md` — Unified flag strategy, per-environment parity, kill switch protocol, staggered rollout coordination
  - `ADR-OBSERVABILITY.md` — Distributed tracing (OpenTelemetry), structured logging standards, metrics collection (Prometheus/Grafana), alerting thresholds, SLO error budgets
  - `ADR-DATABASE.md` -- SQL vs NoSQL selection, migration tooling (Flyway/golang-migrate/Prisma), connection pooling strategy (PgBouncer/HikariCP), read replica strategy
  - `ADR-SECURITY-CRYPTO.md` -- Cryptography (HTTPS, encrypted storage, token signing)
  - `ADR-SECURITY-API-PATTERNS.md` -- Rate limiting, input validation, authZ enforcement, CORS, API key rotation, output encoding, GraphQL security controls, webhook security
  - `ADR-SECURITY-API-STORAGE.md` -- Encrypted database at rest, KMS, connection pooling security, backup encryption, access logging/audit trails, data retention/deletion
  - `ADR-ACCESSIBILITY.md` -- Developer portal WCAG 2.1 AA compliance, screen reader compatibility, keyboard navigation, documentation accessibility
  - `ADR-STRING-KEY-TAXONOMY.md` -- String key naming convention, error message localization keys
- `TSD.md` -- Technology Selection Document (with Technology Radar, weighted scorecard)

**Reviewers:** CTO, CIO, CPO

**Gate Criteria:**

1. All **9** ADRs + TSD authored, reviewed, and approved
2. TSD includes weighted scorecard with at least 2 alternatives per technology decision
3. UML diagrams cover data layer → domain layer → API layer → **presentation layer** (developer portal, error response design, API UX patterns)
4. API Strategy ADR locked (no changes without Stage 3 re-entry)
5. Accessibility ADR defines WCAG 2.1 AA compliance targets for developer portal
6. User has approved the UML Engineering Package

**Defect Handling:** P0/P1 defects block Stage 3 to 4. P2/P3 defects require user decision.

---

### Stage 4: UML to Coding Implementation Plan

**Relevant Personnel:** CTO

**Artifacts In:** PRD, SRD, UML package, ADRs, TSD

**Artifacts Out:**

- `IMPLEMENTATION-PLAN.md` -- Implementation Plan (with task breakdown, dependencies, estimates)
- `RTM.md` -- Requirements Traceability Matrix (PRD/SRD to implementation mapping)
- `TEST-ARCHITECTURE-DOCUMENT.md` -- Test Architecture Document (unit, integration, contract, load, security)
- `GANTT.md` -- Gantt Chart (with critical path, milestones, resource allocation)

**Reviewers:** CTO, CPO

**Gate Criteria:**

1. Implementation Plan covers all active tracks (B-API, B-DATA, B-RT) with explicit task assignments
2. RTM traces 100% of PRD requirements to implementation tasks
3. Test Architecture Document covers all test types with tools, standards, and coverage targets
4. API versioning strategy defined with deprecation timeline
5. Database migration strategy defined with rollback procedure and zero-downtime migration plan
6. SIS (Security Implementation Specification) completed and CSO-signed, referenced in CI/CD readiness section
7. Progress Sync Protocol thresholds defined (baseline estimates for >20% variance detection)
8. VP Engineering confirms buddy pairings established for all 12/20-score engineers assigned to this project's tracks (see `buddy-system-assignments.md`).
9. User has approved the plan

**Defect Handling:** P0/P1 defects block Stage 4 to 5. P2/P3 defects require user decision.

---

### Stage 4.1: Security Implementation Specification (SIS)

Before **Stage 5** begins, the security team produces a backend-specific SIS:

- **Author:** Security team (Natalia Petrova + James Wright), signed off by CSO
- **Timing:** Completed during **Stage 4**, referenced in CI/CD readiness gate before **Stage 5** Day 1
- **Content:** Translates SRD requirements into backend-specific code patterns — rate limiting implementation (token bucket vs. sliding window), input validation (allowlist schemas, parameterized queries, NoSQL injection prevention), authZ enforcement (RBAC/ABAC middleware), CORS policy configuration, API key rotation procedure (header-only, never query param), network isolation (VPC, security groups, WAF rules), encrypted database at rest (AES-256), TLS 1.3 enforcement for all connections, secret management (KMS integration, runtime credential rotation), output encoding / response filtering (no verbose errors, no stack traces), GraphQL security controls (introspection disabled in production, query depth limiting, cost analysis), webhook security (signature verification, replay protection), supply chain security (SBOM generation, artifact signing)
- **Gate Criterion:** "SIS completed and CSO-signed" is a **Stage 4**→**Stage 5** gate criterion

---

### Stage 5: Plan to Software Development

**Relevant Personnel:** CTO (oversees), Dev Malhotra (Backend Chapter Lead -- coordinates)

**Artifacts In:** Implementation Plan, Gantt Chart, RTM, TAD, SIS, ADRs, TSD

**Artifacts Out:**

- Development codebase (API services + data layer + optional real-time layer)
- Contract Verification Reports (Pact contract tests at 30% and 70% milestones)
- String Extraction Readiness audit (error messages audited for hardcoded strings)
- `DEVELOPMENT-LOG.md` -- Per-track development logs with phase completions, variance tracking, CTO weekly summaries

**Reviewers:** CTO (internal review only -- no panel)

**Gate Criteria:**

1. All Implementation Plan tasks marked complete across all active tracks
2. **API Design Conformance Review** passed at ~60% completion (OpenAPI/Swagger spec matches implementation exactly; minor gaps (≤3 undocumented endpoints/fields) AND **Developer Portal UI Conformance Check** ≥85% completeness → proceed with documented remediation plan; if **either** metric fails threshold (<85% UI OR >3 API gaps) → STOP, CTO notifies CPO; unified escalation: 85-89% UI or ≤3 API gaps → proceed with remediation and re-check at 80%)
3. String Extraction Readiness audit completed — remaining hardcoded strings ≤5%, classified as P2 (P1 if core API error affected)
4. Pact Contract Verification Reports produced at 30% and 70% milestones
5. CTO internal review checklist completed:
   - All builds pass (Go/Python/Node) with zero errors
   - API runs without errors on staging, all endpoints respond correctly
   - Developer portal UI renders correctly on staging, interactive explorer functional
   - No P0/P1 defects in bug tracker
   - API Design Conformance Review completed (OpenAPI/Swagger matches implementation)
   - Developer Portal UI Conformance Check completed
   - String Extraction Readiness completed
   - Pact contract tests pass (PACT-CONTRACT-VERIFICATION.md produced)
   - SIS requirements implemented and verified
   - `DEVELOPMENT-LOG.md` current

**Progress Sync Protocol:** Active -- any task >20% over estimate triggers CTO to CPO notification.

**Buddy System Tracking:** For any 12/20-score engineers assigned to this project, buddy pairings are tracked in `PROGRESS.md` session logs and checkpoint JSON buddy progress field. 30/60/90-day checkpoints conducted per `buddy-system-assignments.md` protocol.

**Technical Debt Allocation:** 15-20% sprint capacity reserved (calibrated per project: greenfield 20%, mature 15%, inherited up to 30%). Security debt minimum: 5% of total sprint capacity.

---

### Stage 6: Development to Code Review

**Relevant Personnel:** CTO (convenes panel)

**Artifacts In:** Development codebase, Contract Verification Reports, String Extraction Readiness audit, DEVELOPMENT-LOG.md

**Artifacts Out:**

- `DEFECT-REPORT.md` -- Defect Report with Architecture Compliance Audit, API Conformance Matrix, pre-Tier 1 automated quality gates
- `SIGNOFF.md` -- Code Review Sign-off (with Live API Demonstration results)

**Reviewers:** CTO (convenes), CPO, CDO, CIO, CSO, Backend Lead (Dev Malhotra), Security Lead (James Wright)

**Gate Criteria:**

1. Three-Layer Defense for ADR/TSD compliance passed:
   - **Layer 1:** Backend Leads + Data Lead attest implementations conform to locked Stage 3 ADRs and TSD technology selections
   - **Layer 2:** Dr. Elena Rostova conducts independent Architecture Compliance Audit, produces written audit memo
   - **Layer 3:** CI/CD gates passed -- dependency version pinning, prohibited technology detection, security ADR compliance (rate limiting, authZ patterns); **Security Lead (James Wright) conducts independent security pattern review** — verifies rate limiting implementation matches SIS specifications, authZ middleware correctly enforces RBAC/ABAC policies, encryption configurations match ADR-SECURITY-CRYPTO.md
2. Live API Demonstration completed -- Backend Lead demonstrates critical API flows, error handling, rate limiting behavior; k6 load test results displayed and verified against SLA targets; OpenAPI/Swagger documentation verified against actual API responses; CDO verifies developer portal UX matches IDS (documentation layout, interactive explorer, error response design, onboarding flow, WCAG 2.1 AA compliance)
3. API Conformance Matrix greater than or equal to 95% -- no undocumented endpoints or fields
4. Architecture Compliance Audit findings addressed or deferred with user approval
5. Pre-Tier 1 automated quality gates passed -- lint, type-check, unit tests, contract tests

**Defect Handling:** P0/P1 defects block Stage 6 to 7. P2/P3 defects submitted to user for fix/defer decision. CTO assigns R&D to remediate. Full review repeats until all panel sign off.

---

### Stage 7: Code Review to Automated Testing

**Relevant Personnel:** CTO (designates R&D personnel), Test Lead (Priscilla Oduya), Test Automation Lead (Rachel Kim)

**Artifacts In:** Code Review Sign-off, Defect Report (with user decisions on P2/P3)

**Artifacts Out:**

- Automated Test Suite (unit, integration, contract, load, security, chaos optional)
- `TEST-RESULTS-REPORT.md` -- Test Results Report (with DAST, load benchmarks, SLA verification)

**Reviewers:** CTO, Test Lead

**Gate Criteria:**

1. 100% automated test pass rate achieved
2. DAST (OWASP ZAP) passed -- zero critical/high findings
3. Manual penetration testing (OWASP API Security Top 10) passed -- zero critical/high findings (BOLA, broken authentication, excessive data exposure, lack of rate limiting, broken function-level authorization, mass assignment, security misconfiguration, injection, improper assets management, insufficient logging/monitoring)
4. Load benchmarks passed -- P99 < SLA target, error rate < 0.1%
5. API contract tests passed -- 100% endpoint coverage (Pact)
6. Integration tests passed -- all endpoints with real database
7. Accessibility audit passed -- developer portal WCAG 2.1 AA ≥ 95% (axe-core + manual screen reader test)
8. Regression testing passed -- all Stage 6+ fixed functionalities verified

**Defect Handling:** P0/P1 defects block Stage 7 to 8. P2/P3 defects submitted to user for fix/defer decision.

---

### Stage 8: Automated Testing to Integrity Verification

**Relevant Personnel:** CTO (convenes panel)

**Artifacts In:** Test Results Report, Defect Report (with user decisions on P2/P3)

**Artifacts Out:**

- Integrity Verification Sign-off reports from each panel member (CPO, CDO, CIO, CSO, Backend Lead, Security Lead)

**Reviewers:** CTO (convenes), CPO, CDO, CIO, CSO, Backend Lead, Security Lead

**Gate Criteria:**

1. Stage 6 baseline re-verification -- all Stage 6 defects confirmed fixed, no regression
2. Per-feature PRD checklist -- each PRD requirement verified as implemented and tested
3. Stealthy weakening detection -- no security controls weakened/removed/disabled since Stage 6 (e.g., removed rate limiting, relaxed authZ, weakened encryption, relaxed input validation, increased rate limit thresholds without approval, disabled API key rotation, expanded CORS origins, removed request logging/audit trails, downgraded database encryption, disabled TLS). Any such change is classified as **P0 defect**.
4. API Conformance Matrix re-verified -- greater than or equal to 95% pass rate maintained
5. SLA verification -- P99 latency, throughput, uptime targets confirmed met

**Defect Handling:** P0/P1 defects block Stage 8 to 9. Functionality removal is **never** valid remediation.

---

### Stage 9: Integrity to i18n Engineering

**Relevant Personnel:** CTO-L (leads), Internationalization Specialist (Tomas Dvoracek), Translation Team

**Artifacts In:** Integrity Verification Sign-off, codebase

**Artifacts Out:**

- Localised codebase (error messages, developer portal content translated)
- `TRANSLATION-VERIFICATION-REPORT.md` -- Translation Verification Report (with BLEU/TER scores)

**Reviewers:** CTO-L, CTO

**Gate Criteria:**

1. All target languages translated for error messages and developer portal content
2. BLEU score greater than or equal to 0.80 for all languages
3. Error message localization verified -- no hardcoded strings
4. Developer portal content localized (API docs, guides, terms of service)

**Defect Handling:** P0/P1 defects block Stage 9 to 10. P2/P3 defects deferred to post-release if CTO-L approves.

---

### Stage 10: i18n to Release Readiness Check

**Relevant Personnel:** CTO (convenes panel), CPO, CIO, CSO, CTO-L, **User** (final decision)

**Artifacts In:** Localised codebase, Translation Verification Report, all prior stage artifacts

**Artifacts Out:**

- `RELEASE-CHECKLIST.md` -- Release Readiness Report (7-item checklist with sub-checklists)
- Release Decision (approved / conditional / rejected)

**Reviewers:** CTO (convenes), CPO, **CDO**, CIO, CSO, CTO-L + **User**

**Release Checklist (7 Items):**

| #   | Domain                                                     | Sign-off Authority | Key Sub-Checks                                                                                                                                             |
| --- | ---------------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Product — all PRD requirements implemented                 | CPO                | Analytics firing, kill condition monitoring active, post-launch dashboard ready                                                                            |
| 2   | Design — all CDO/IDS specifications accurately realised    | CDO                | **Developer Portal UX Conformance Matrix** ≥95%, developer portal UX met, error response conventions followed, developer portal WCAG 2.1 AA ≥95% pass rate |
| 3   | Architecture — all UML/ADR/TSD standards upheld            | CTO + CIO          | Technology Decision Registry 100% compliant, no ADR deviations                                                                                             |
| 4   | Security — SRD enforced, API security controls effective   | CSO                | All security controls present AND effective (rate limiting, authZ, input validation, CORS), stealthy weakening verified absent                             |
| 5   | Testing — 100% automated test pass rate achieved           | CTO                | DAST passed, load benchmarks passed, SLA verification passed                                                                                               |
| 6   | Localisation — error messages + developer portal localized | CTO-L              | BLEU ≥0.80, error messages verified, developer portal translated                                                                                           |
| 7   | Deployment — API gateway live, versioning active           | CTO + CPO          | API gateway deployed, version published, deprecation policy published, developer docs complete, sandbox environment live, monitoring dashboards live       |

**Gate Criteria:**

1. All 7 checklist items signed off
2. User has issued the final release decision

**Defect Handling:** P0/P1 defects block release. P2/P3 defects -- user has explicit final authority to fix before release or defer to post-launch.

---

**Monitoring system:** `monitoring.md` -- Backend API Pipeline monitoring system (three-layer: PROGRESS.md, session logs, checkpoint JSON).
