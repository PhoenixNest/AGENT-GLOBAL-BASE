# Backend API Pipeline — Overview

**Pipeline:** Backend API Services (P2)
**Full Definition:** [`pipeline.md`](company/library/pipeline/backend-api/pipeline.md)
**Monitoring:** [`monitoring.md`](company/library/pipeline/backend-api/monitoring.md)

---

## Platform Focus

REST, GraphQL, gRPC API services with developer portal UX, rate limiting, and API gateway deployment.

---

## Platform Strategy Matrix

Five mutually exclusive scenarios:

| Dimension             | REST API                   | GraphQL API                | Real-time (WebSocket)     | Event-Driven Microservices | Simple CRUD            |
| --------------------- | -------------------------- | -------------------------- | ------------------------- | -------------------------- | ---------------------- |
| **Stage 3 ADR**       | REST architecture          | GraphQL schema             | WebSocket architecture    | Kafka + CQRS architecture  | Simple REST            |
| **Stage 5 Tracks**    | B-API + B-DATA             | B-API + B-DATA (L)         | B-API + B-DATA (L) + B-RT | B-API (L) + B-DATA + B-RT  | B-API (L) + B-DATA (L) |
| **Stage 5 Team Size** | 5                          | 4                          | 5                         | 7                          | 3                      |
| **Stage 6 Review**    | Backend primary + Security | Backend primary + Security | All three leads           | All three leads            | Backend primary        |
| **Stage 7 Testing**   | Unit + contract + load     | Unit + contract + schema   | Load + chaos + WebSocket  | Load + chaos + integration | Unit + basic load      |
| **Stage 10**          | API gateway + docs         | API gateway + SDL          | API gateway + WS docs     | API gateway + event schema | API gateway + docs     |

---

## Stage-Specific Highlights

### Stage 2: API Specification + Developer Portal IDS

- OpenAPI/Swagger specification for REST, GraphQL SDL for GraphQL, protobuf for gRPC
- **Developer Portal IDS**: documentation layout, interactive API explorer, error response design, onboarding flow
- Interactive API mock server or Swagger UI instance with sample responses for all endpoints

### Stage 3: ADRs (8 total)

- `ADR-API-STRATEGY.md` — REST vs GraphQL vs gRPC (14 fields + data consistency model)
- `ADR-OBSERVABILITY.md` — Distributed tracing (OpenTelemetry), structured logging, metrics (Prometheus/Grafana), SLO error budgets
- `ADR-DATABASE.md` — SQL vs NoSQL, migration tooling (Flyway/golang-migrate/Prisma), connection pooling (PgBouncer/HikariCP), read replicas
- `ADR-SECURITY-CRYPTO.md` — HTTPS, encrypted storage, token signing
- `ADR-SECURITY-API-PATTERNS.md` — Rate limiting, input validation, authZ, CORS, API key rotation (header-only), output encoding, GraphQL security, webhook security
- `ADR-SECURITY-API-STORAGE.md` — Encrypted DB at rest, KMS, connection pooling security, backup encryption, audit trails, data retention/deletion
- `ADR-ACCESSIBILITY.md` — Developer portal WCAG 2.1 AA, screen reader compatibility, keyboard navigation
- `ADR-STRING-KEY-TAXONOMY.md` — String key naming, error message localization keys

### Stage 4.1: Security Implementation Specification (SIS)

- Content: rate limiting (token bucket vs sliding window), input validation (allowlist, parameterized queries, NoSQL injection prevention), authZ (RBAC/ABAC), CORS, API key rotation (header-only, never query param), network isolation (VPC, security groups, WAF), encrypted DB (AES-256), TLS 1.3, secret management (KMS, runtime credential rotation), output encoding (no verbose errors/stack traces), GraphQL security (introspection disabled in production, query depth limiting, cost analysis), webhook security (signature verification, replay protection), supply chain security (SBOM, artifact signing)

### Stage 5: Development

- API Design Conformance Review at ~60%: OpenAPI/Swagger matches implementation exactly
- **Developer Portal UI Conformance Check** at ~60%: ≥85% completeness on documentation layout, interactive explorer, error response design, onboarding flow
- Pact Contract Verification at 30%/70% milestones
- k6 load test baseline: P99, throughput, error rate within SLA targets

### Stage 6: Code Review

- Live API demonstration with k6 load test executed live against staging
- OpenAPI/Swagger documentation verified against actual API responses
- Developer Portal UX verified by CDO: documentation layout, interactive explorer, error response design, onboarding flow, WCAG 2.1 AA compliance
- Rate limiting behavior demonstrated (triggering 429 responses)

### Stage 7: Testing

- OWASP API Security Top 10 manual pen testing (BOLA, broken authentication, excessive data exposure, lack of rate limiting, broken function-level authorization, mass assignment, security misconfiguration, injection, improper assets management, insufficient logging/monitoring)
- k6 load tests: P99 < SLA, throughput > target, error rate < 0.1%
- Pact contract tests: 100% endpoint coverage
- Accessibility audit: developer portal WCAG 2.1 AA ≥ 95% (axe-core + manual screen reader test)

### Stage 8: Stealthy Weakening Examples (P0)

- Removed rate limiting, relaxed authZ, weakened encryption, relaxed input validation, increased rate limit thresholds without approval, disabled API key rotation, expanded CORS origins, removed request logging/audit trails, downgraded database encryption, disabled TLS

---

## Monitoring

Three-layer architecture with backend-specific fields:

- Track B-API/B-DATA/B-RT with k6/Pact/OpenAPI build tree
- Performance SLA: P99 <200ms, throughput >10k rps, uptime 99.9%+, error rate <0.1%
- Checkpoint fields: `endpoints_implemented/tested`, `migration_status`, `load_test_p99_ms/throughput_rps`, `error_rate_pct`, `contract_coverage_pct`, `rate_limiting_active`, `developer_docs_complete`
- Recovery scenarios: Database migration rollback, container deployment failure, API gateway routing error, rate limiting misconfiguration, Pact contract break

---

_For complete stage definitions, gate criteria, and artifact lists, see the [full pipeline definition](company/library/pipeline/backend-api/pipeline.md)._
