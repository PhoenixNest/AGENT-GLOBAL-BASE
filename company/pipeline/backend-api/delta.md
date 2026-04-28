# Backend API Pipeline — Delta Overlay

| Field          | Value                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Pipeline**   | `backend-api`                                                                                                                         |
| **Owner**      | VP API (Alex Rivera) + VP Web & Backend (Elena Vasquez) (joint)                                                                       |
| **Surfaces**   | API services (REST / GraphQL / gRPC / WebSocket / event-driven) — selectable per-project via the 5-scenario API Strategy Matrix below |
| **Effective**  | 2026-04-21                                                                                                                            |
| **Supersedes** | `backend-api/pipeline.md` (legacy 434-line file; back-compat redirect retained until 2026-07-21).                                     |
| **Cross-Refs** | Base: [`../_base/pipeline.md`](../_base/pipeline.md) · Template: [`../_base/delta-template.md`](../_base/delta-template.md)           |

> **Reading order.** This delta is consumed _alongside_ [`../_base/pipeline.md`](../_base/pipeline.md), not instead of it. The base defines the universal 12-stage state machine, defect severity, Progress Sync Protocol, gate criteria, and the Release Readiness Checklist. This delta fills the `{{DELTA: …}}` placeholders the base reserves for backend-API-specific content. Anything in the base applies; anything contradicted by this delta IS A BUG — escalate to the Software Architect.

---

## 1. Surface / API Strategy Matrix

### 1.1 Overview

Stage 5 development executes per the **API Strategy Matrix**, which determines track activation based on the **API Strategy ADR** produced at Stage 3. The Stage 1 gate asks "What type of API service?" — this confirms the **target delivery model** (REST, GraphQL, real-time, event-driven, simple CRUD). The **implementation approach** (REST vs. GraphQL vs. gRPC vs. event-driven) is an architecture decision locked at **Stage 3**.

**Five mutually exclusive scenarios — a project selects exactly one.**

### 1.2 Decision Matrix

| Dimension                 | REST API               | GraphQL API              | Real-Time (WebSocket)         | Event-Driven Microservices    | Simple CRUD API                          |
| ------------------------- | ---------------------- | ------------------------ | ----------------------------- | ----------------------------- | ---------------------------------------- |
| **Stage 1 Gate**          | API service            | API service              | API service                   | API service                   | API service                              |
| **Stage 3 ADR**           | REST architecture      | GraphQL schema           | WebSocket architecture        | Kafka + CQRS architecture     | Simple REST                              |
| **Stage 5 Active Tracks** | B-API + B-DATA         | B-API + B-DATA (LIGHT)   | B-API + B-DATA (LIGHT) + B-RT | B-API (LIGHT) + B-DATA + B-RT | B-API (LIGHT) + B-DATA (LIGHT)           |
| **Stage 5 Team Size**     | 5                      | 4                        | 5                             | 7                             | 3                                        |
| **Stage 6 Tier 1 Review** | Backend Lead primary   | Backend Lead primary     | All three Leads               | All three Leads               | Backend Lead primary                     |
| **Stage 7 Testing**       | Unit + contract + load | Unit + contract + schema | Load + chaos + WebSocket      | Load + chaos + integration    | Unit + basic load                        |
| **Stage 9 i18n**          | Error-message catalog  | Error-message catalog    | Error-message catalog         | Error-message catalog         | Error-message catalog (optional per PRD) |
| **Stage 10 Submission**   | API gateway + docs     | API gateway + SDL        | API gateway + WS docs         | API gateway + event schema    | API gateway + docs                       |
| **CI/CD Scope**           | REST CI                | GraphQL CI               | WebSocket CI                  | Event-driven CI               | REST CI                                  |

### 1.3 Track Activation Protocol

| Project Type               | Track B-API (API Services) | Track B-DATA (Data Layer) | Track B-RT (Real-Time & Events) | Coordinator                 |
| -------------------------- | -------------------------- | ------------------------- | ------------------------------- | --------------------------- |
| REST API service           | **FULL** (3 eng)           | **FULL** (2 eng)          | Dormant                         | Dev Malhotra (Backend Lead) |
| GraphQL API                | **FULL** (3 eng)           | **LIGHT** (1 eng)         | Dormant                         | Dev Malhotra                |
| Real-time service          | **FULL** (2 eng)           | **LIGHT** (1 eng)         | **FULL** (2 eng)                | Dev Malhotra                |
| Event-driven microservices | **LIGHT** (2 eng)          | **FULL** (2 eng)          | **FULL** (3 eng)                | Dev Malhotra                |
| Simple CRUD API            | **LIGHT** (2 eng)          | **LIGHT** (1 eng)         | Dormant                         | Dev Malhotra                |

**Track semantics:**

| Term        | Definition                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------- |
| **FULL**    | End-to-end feature implementation, testing, and delivery for that layer. Owns the complete codebase for that layer. |
| **LIGHT**   | Integration and adaptation only (e.g., API consumer wiring, schema migration). NOT full feature implementation.     |
| **PRIMARY** | Owns the shared integration layer. Coordinates cross-service contracts and data-model consistency.                  |
| **Dormant** | Track lead and engineers are reassigned to technical debt, test automation, cross-training, or SDK migration prep.  |

### 1.4 Resource Reallocation Protocol

| Scenario                   | Freed Resources          | Reassignment Options                                                   |
| -------------------------- | ------------------------ | ---------------------------------------------------------------------- |
| REST API service           | B-RT engineers           | Other projects, load-test infrastructure, CI/CD hardening              |
| GraphQL API                | B-DATA + B-RT engineers  | Other projects, schema optimization, contract test automation          |
| Real-time service          | None — all tracks active | N/A                                                                    |
| Event-driven microservices | None — all tracks active | N/A                                                                    |
| Simple CRUD API            | B-DATA + all B-RT eng    | Technical debt, database optimization, documentation, monitoring setup |

### 1.5 Monitoring Adaptation

`PROGRESS.md` must reflect active tracks only. Inactive tracks show "N/A," not "0%". The Progress Sync Protocol must account for reallocated resources — reassigned engineers should not penalize a project's capacity metrics.

### 1.6 Per-Scenario CI/CD Blueprint

| CI/CD Component | REST API             | GraphQL API         | Real-Time Service          | Event-Driven Microservices | Simple CRUD API |
| --------------- | -------------------- | ------------------- | -------------------------- | -------------------------- | --------------- |
| Build CI        | Go / Node lint+build | Node / TS build     | Go build                   | Go build                   | Go / Node build |
| Unit CI         | Go test / Jest       | Jest / Vitest       | Go test                    | Go test                    | Go test         |
| Contract CI     | Pact verification    | Schema validation   | WebSocket protocol test    | Event schema validation    | Basic API test  |
| Integration CI  | Docker-compose + DB  | Docker-compose + DB | Docker-compose + WS server | Docker-compose + Kafka     | Docker-compose  |
| Load CI         | k6                   | k6                  | k6 + WebSocket test        | k6 + Kafka test            | k6 basic        |
| Security CI     | Semgrep, ZAP, audit  | Semgrep, ZAP, audit | Semgrep, ZAP, audit        | Semgrep, ZAP, audit        | Semgrep, audit  |
| Deployment      | Blue-green / canary  | Blue-green / canary | Rolling update             | Rolling update             | Blue-green      |

---

## 2. Stage 1 — PRD Stewardship (backend-API-specific)

- **PRD steward:** VP API (Alex Rivera); CPO arbitrates if PRD scope spans API + non-API products.
- **Stage 1 surface question (delta-fills the base placeholder):** "What type of API service?" (REST / GraphQL / gRPC / real-time / event-driven). The user's answer determines the API Strategy Matrix scenario at Stage 3. A second confirmation: "What API consumer types?" (web frontend, mobile app, third-party integration, internal service) — drives the SLA and security baseline.
- **Backend-specific PRD fields:** target P99 latency; throughput (RPS); availability SLO (e.g., 99.9% / 99.95%); error-rate SLO; data-residency requirements; per-consumer SLA differentiation (if any); rate-limit policy (per-IP, per-API-key, per-tenant).
- **Backend-specific SRD fields (delta-fills the base placeholder):** rate-limiting algorithm (token bucket / sliding window) + thresholds; input-validation strategy (allowlist schemas, parameterized queries, NoSQL injection prevention); authZ model (RBAC / ABAC / ReBAC); CORS policy; API key lifecycle (rotation cadence, revocation propagation); secret-management strategy (KMS / Vault); DDoS mitigation thresholds; GraphQL-specific controls (introspection disabled in production, query depth limit, cost analysis) — if applicable.

---

## 3. Stage 2 — Prototype Variant (backend-API-specific)

- **Prototype format (delta-fills the base placeholder):** **machine-readable API contract** — OpenAPI / Swagger for REST, GraphQL SDL for GraphQL, protobuf for gRPC, AsyncAPI for event-driven. Plus an interactive API mock server (Swagger UI / GraphQL Playground / Postman mock) demonstrating all endpoints with sample responses.
- **IDS surface coverage:** developer-portal UX (documentation layout, interactive explorer, error-response design, onboarding flow) and developer-portal accessibility (WCAG 2.1 AA: screen-reader compatibility, keyboard navigation, color contrast). The "interaction surface" here is the developer using the docs site and the live explorer — that surface gets a full IDS the same way an end-user UI does.

---

## 4. Stage 3 — Additional Mandatory ADRs (backend-API-specific)

In addition to the universal **String Key Taxonomy ADR** and **Security Architecture ADRs** mandated by the base:

### 4.1 API Strategy ADR (mandatory for every backend project) — 14 fields

The API Strategy ADR must include:

1. **Decision statement** — REST, GraphQL, gRPC, or hybrid?
2. **Rationale** — Consumer needs, team skills, performance requirements.
3. **Trade-offs** — What is gained / sacrificed vs. alternatives.
4. **Team capability assessment** — Backend skills available?
5. **Risk analysis** — API versioning complexity, database scaling, event ordering (for event-driven).
6. **TCO projection (24-month)** — Infrastructure, monitoring, developer tooling; total estimated cost.
7. **Vendor lock-in risk matrix** — Framework abandonment risk, migration cost, hosting dependency.
8. **Performance SLA alignment** — P99 latency, throughput, error rate, uptime ≥ 99.9% — can the chosen approach meet PRD thresholds?
9. **Security mandate** — Rate limiting, input validation, CORS, CSRF (where applicable), authZ model.
10. **STRIDE-based threat model** — API injection, broken auth, data exposure, DDoS.
11. **Track activation mapping** — Which tracks are FULL / LIGHT / Dormant per track.
12. **Reassignment plan** — Where freed engineers go.
13. **API versioning strategy** — URL path vs. header vs. content negotiation; deprecation timeline; backward-compatibility policy.
14. **Developer experience** — OpenAPI / Swagger docs, SDK generation, sandbox environment, status page.

**Ownership:** CTO authors. Backend Lead + Data Lead provide input. CIO reviews for technology conformance. CSO reviews for security conformance. The ADR is versionable + supersedable per [`../_base/adr-template.md`](../_base/adr-template.md); supersession requires a documented rollback plan and triggers an Implementation-Plan re-baseline (Stage 4 re-entry minimum).

### 4.2 Backend-Specific Additional ADRs (beyond the universal canon)

- `ADR-OBSERVABILITY.md` — Distributed tracing (OpenTelemetry), structured-logging standards, metrics collection (Prometheus / Grafana), alerting thresholds, SLO error budgets.
- `ADR-DATABASE.md` — SQL vs. NoSQL selection, migration tooling (Flyway / golang-migrate / Prisma), connection-pooling strategy (PgBouncer / HikariCP), read-replica strategy.
- `ADR-SECURITY-API-PATTERNS.md` — Rate limiting, input validation, authZ enforcement, CORS, API key rotation, output encoding, GraphQL security controls, webhook security.
- `ADR-SECURITY-API-STORAGE.md` — Encrypted database at rest, KMS, connection-pooling security, backup encryption, access logging / audit trails, data retention / deletion policy.
- `ADR-ACCESSIBILITY.md` — Developer-portal WCAG 2.1 AA compliance, screen-reader compatibility, keyboard navigation, documentation accessibility.

---

## 5. Stage 4 — Pipeline-Specific Plan Sections

### 5.1 Service Decomposition Plan (mandatory in every Backend Coding Implementation Plan)

The Service Decomposition Plan defines bounded contexts, per-service responsibilities, inter-service contracts (API contracts + event schemas), and shared-data ownership rules. For monolith projects, the plan documents internal-module boundaries with the same rigor; for event-driven projects, the plan includes the event-schema registry and a topology diagram.

### 5.2 API Versioning & Deprecation Plan (mandatory)

The plan must specify the versioning strategy chosen in the API Strategy ADR (URL path / header / content negotiation), the deprecation timeline (minimum 6 months from announcement to sunset), the consumer-notification mechanism (status page + email + deprecation header), and the backward-compatibility test suite that runs against every PR.

### 5.3 Database Migration Plan (mandatory)

Database migration strategy with rollback procedure and zero-downtime migration plan (expand-migrate-contract pattern). Migration tooling specified in the TSD (Flyway / golang-migrate / Prisma Migrate / Atlas). For schema-less stores, document the schema-version field convention.

### 5.4 Backend-Specific Adapter Layer

The base mandates a "platform/surface adapter layer" in dependency mapping. For backend, this is the **transport adapter layer**: HTTP / gRPC / WebSocket transports map onto a transport-agnostic application core; database / cache / message-broker adapters live behind repository / port interfaces.

---

## 6. Stage 5 — Track Execution Model (backend-API-specific)

**Lead coordinator:** **VP API (Alex Rivera)** for product / API strategy; **Backend Lead (Dev Malhotra)** for engineering quality across all three tracks.

**Track execution:**

- **Track B-API (API Services):** Led by Backend Lead (Dev Malhotra). FULL for REST / GraphQL / real-time scenarios; LIGHT for event-driven and simple-CRUD.
- **Track B-DATA (Data Layer):** Led by Senior Backend Engineer (Aisha Mohammed). FULL for REST / event-driven; LIGHT for GraphQL / real-time / simple-CRUD.
- **Track B-RT (Real-Time & Events):** Led by Senior Backend Engineer (Kael Jensen). FULL for real-time and event-driven; dormant otherwise.

**Cross-track coordination:** Pact contract tests at 30% and 70% milestones — provider-side verification for B-API, consumer-side verification where applicable. For event-driven projects, schema-registry compatibility checks (backward / forward / full) are the equivalent gate.

**SIS scope:** Backend-specific SIS authored by Security team (Natalia Petrova + James Wright), CSO-signed before Stage 5 Day 1. Translates SRD into backend-specific code patterns — rate-limiting implementation (token bucket vs. sliding window), input validation (allowlist schemas, parameterized queries, NoSQL injection prevention), authZ enforcement (RBAC / ABAC middleware), CORS policy configuration, API key rotation procedure (header-only, never query-param), network isolation (VPC, security groups, WAF rules), encrypted database at rest (AES-256), TLS 1.3 enforcement, secret management (KMS integration, runtime credential rotation), output encoding / response filtering (no verbose errors, no stack traces in production), GraphQL security controls (introspection disabled in production, query-depth limiting, cost analysis), webhook security (signature verification, replay protection), supply-chain security (SBOM generation, artifact signing).

**Design Fidelity Checkpoint scope:** Backend Lead presents the running API on a staging environment; CDO interacts with the developer portal (docs + interactive explorer) to verify the IDS specifications. API specification (OpenAPI / SDL) is diffed against the running implementation — no undocumented endpoints / fields tolerated past the ~60% checkpoint.

**Additional Backend Stage-5 gate criteria (delta-fills the base placeholder):**

- [ ] Pact contract tests (provider-side) pass for all consumer pacts.
- [ ] API Design Conformance Review passed at ~60% completion (OpenAPI / SDL matches implementation; ≤ 3 undocumented endpoints / fields proceed with remediation plan; > 3 STOP, CTO notifies CPO).
- [ ] Developer Portal UI Conformance Check passed at ~60% completion (≥ 85% completeness on documentation layout, interactive explorer, error-response design, onboarding flow against IDS; < 85% proceed with documented remediation plan).

---

## 7. Stage 6 — Tier-1 Review Model (backend-API-specific)

**Tier-1 cross-review pairing (delta-fills the base placeholder):**

- **REST / GraphQL / Simple CRUD:** Backend Lead primary; Data Lead reviews persistence boundaries; Security Lead (James Wright) reviews authZ enforcement.
- **Real-Time / Event-Driven:** All three Leads cross-review (B-API ↔ B-DATA ↔ B-RT); event-schema compatibility audited explicitly.

**Live Demonstration scope (delta-fills the base placeholder):** Backend Lead demonstrates **critical API flows, error handling, and rate-limiting behavior** on a production-equivalent staging environment. **k6 load-test results displayed** and verified against PRD SLA targets. **OpenAPI / Swagger documentation verified** against actual API responses (no spec drift). CDO verifies developer-portal UX matches IDS (documentation layout, interactive explorer, error-response design, onboarding flow, WCAG 2.1 AA compliance).

**Backend-specific security mandate (delta-fills the base placeholder):** OWASP API Security Top 10 (current edition) addressed in security review; OWASP ASVS Level 2+ for application security.

---

## 8. Stage 7 — Platform-Specific Testing Mandates (backend-API-specific)

Delta-fills the base's `{{DELTA: pipeline-specific Stage 7 testing mandates}}`:

- **Unit tests:** Go test / Jest / Vitest (per language stack) — coverage targets per TAD; minimum 80% on core domain code.
- **Integration tests:** Docker-compose with real database + cache + message broker as applicable. All endpoints exercised against a real persistence layer.
- **Contract tests:** Pact (provider-side) — 100% endpoint coverage from the provider side; for event-driven projects, schema-registry compatibility checks (backward / forward / full).
- **Load tests:** k6 — per-endpoint load test verifying P99 latency < SLA target, throughput ≥ SLA target, error rate < 0.1%. For real-time, WebSocket-specific load tests (concurrent connections, message-broadcast fan-out).
- **Chaos tests (real-time + event-driven only):** broker outage, network partition, replica failure injected via Toxiproxy or equivalent.
- **Accessibility audit (developer portal):** WCAG 2.1 AA ≥ 95% via axe-core + manual screen-reader test on critical flows (auth, sandbox sign-up, API explorer).
- **OWASP penetration-testing track (delta-fills the base placeholder):** Manual penetration test using the **OWASP API Security Top 10** (current edition) — covers BOLA, broken authentication, excessive data exposure, lack of rate limiting, broken function-level authorization, mass assignment, security misconfiguration, injection, improper assets management, insufficient logging / monitoring. Zero critical / high findings is the gate.
- **DAST:** OWASP ZAP (automated) — zero critical / high findings is the gate.

**Regression testing model — environment matrix (delta-fills the base placeholder):**

| Trigger     | Backend-specific scope                                                                                                |
| ----------- | --------------------------------------------------------------------------------------------------------------------- |
| Per-PR      | Unit + integration tests + Pact provider verification + Semgrep SAST.                                                 |
| Nightly E2E | Full integration suite + k6 baseline load test + ZAP DAST against staging + schema-compatibility regression (events). |

---

## 9. Stage 8 — Additional Integrity Checks (backend-API-specific)

Delta-fills the base placeholder for additional Stage-8 product-specific integrity checks:

- **Stealthy weakening — backend-specific watch-list:** removed rate limiting, relaxed authZ, weakened encryption, relaxed input validation, increased rate-limit thresholds without approval, disabled API key rotation, expanded CORS origins, removed request logging / audit trails, downgraded database encryption, disabled TLS, GraphQL introspection re-enabled in production. Any such change since Stage 6 is classified as **P0 defect**.
- **API conformance re-verification:** OpenAPI / SDL diff against the running implementation — must remain ≥ 95% conformance with no undocumented breaking changes.
- **SLA verification:** P99 latency, throughput, uptime targets confirmed met against the Stage-7 baseline (no regression).
- **Audit-log completeness:** every authZ decision, every API key issuance / rotation, every data-export action emits an audit event; verified against the Stage-3 audit-trail spec.

---

## 10. Stage 10 — Additional Release Criteria (backend-API-specific)

Delta-fills the base placeholder for additional Stage-10 product-specific release criteria:

- **API gateway live:** API gateway deployed; version published; deprecation policy published; developer docs complete; sandbox environment live; monitoring dashboards live (latency / error-rate / throughput / SLO burn-down).
- **SDK / client artifacts published** (where in scope per Stage 3 ADR field 14): generated client SDKs (OpenAPI Generator / Swagger Codegen) published to language registries; semantic-version tags pushed.
- **Status page live:** uptime status page reachable from the developer portal; incident-history pre-populated.

---

## 11. Stage 11 — Live Ops Mandates (backend-API-specific)

Delta-fills the base placeholder for product-specific live-ops mandates:

- **SLOs (rolling 7-day):** P99 latency ≤ PRD target; uptime ≥ 99.9% (or PRD-defined); error rate ≤ 0.1%.
- **Error-budget policy:** when 50% of the quarter's error budget is consumed, the on-call DRI raises a yellow-flag review; at 90% consumption, all non-essential changes freeze until budget recovers.
- **API-deprecation escalation:** breaking changes require ≥ 6-month consumer notice + a deprecation header on every response in the deprecation window; any consumer still calling a sunset endpoint at T-30 days triggers a CSM outreach + a P2 ticket.
- **Webhook delivery SLO:** ≥ 99% delivery within 10 seconds; redelivery queue with exponential backoff up to 24 hours.
- **Per-deploy hold rules:** if synthetic monitoring (k6 against production) shows P99 regression > 20% vs. baseline, deploy is rolled back automatically; on-call DRI re-enables only after triage.

---

## 12. Cross-Cutting i18n Requirements

i18n is a continuous concern from Stage 2 onward. Backend-API-specific application is narrower than UI-bearing pipelines but still substantive:

| Stage   | Backend-API i18n requirement                                                                                                                                                                                                                                    |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 1 | PRD declares whether the API surfaces user-facing strings (error messages, status text, developer portal copy). If yes, target locales locked.                                                                                                                  |
| Stage 2 | Developer-portal IDS includes locale-aware copy decisions (e.g., language-switcher placement, language-detection from `Accept-Language`).                                                                                                                       |
| Stage 3 | String Key Taxonomy ADR uses the canonical `{feature}.{screen}.{component}.{property}` shape, adapted for API error catalogs (e.g., `errors.auth.token_expired.message`). Developer-portal accessibility ADR includes language-switcher accessibility.          |
| Stage 5 | Locale-aware error catalog from first commit. Zero-hardcoded-strings rule enforced by CI on every PR (lint rule or grep gate). Per-request locale negotiation (`Accept-Language` header) honored; default fallback language documented in the API Strategy ADR. |
| Stage 7 | Locale-coverage tests: for every supported locale, every error code in the catalog returns a non-fallback translation. Developer-portal screenshot / smoke regression in each target locale.                                                                    |
| Stage 9 | Translation accuracy only (i18n engineering already complete). CTO-L issues Translation Verification Report (BLEU ≥ 0.80; placeholder integrity verified; developer-portal copy + error messages verified).                                                     |

---

## 13. Document Version History

| Version | Date           | Author                               | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------- | -------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0.1     | April 21, 2026 | Software Architect + VP API + VP W&B | Initial overlay. Backend-API-specific content (5-scenario API Strategy Matrix, Track B-API / B-DATA / B-RT activation, per-scenario CI/CD blueprint, API Strategy ADR 14-field requirement, backend-specific Stage 1/2/3/4/5/6/7/8/10/11 sections, cross-cutting i18n table for error catalogs + developer portal) extracted from the legacy `backend-api/pipeline.md` (434 lines). Pairs with [`../_base/pipeline.md`](../_base/pipeline.md) to produce a derived view equivalent to the legacy file. |
