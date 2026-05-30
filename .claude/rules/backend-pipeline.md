---
paths:
  - "**/backend-api/**"
description: Backend API development pipeline platform-specific rules
---

# Backend API Development Pipeline — Platform-Specific Rules

**Applies To:** Backend API and server-side application development

---

## Technology Stack

- **Languages:** Node.js (TypeScript), Python, Go, Java (per ADR)
- **Frameworks:** Express, Fastify, FastAPI, Django, Gin, Spring Boot (per ADR)
- **Databases:** PostgreSQL, MongoDB, Redis (per ADR)
- **API Style:** REST, GraphQL, gRPC (per ADR)

---

## Stage-Specific Backend Requirements

### Stage 1 — PRD + SRD

Backend PRD: API endpoints, data models, performance (latency/throughput), scalability, integrations, data retention.

Backend SRD: Auth/authorization, encryption (at rest/in transit), rate limiting, input validation, SQL injection prevention, OWASP API Security Top 10.

### Stage 3 — UML Engineering Package

**ADRs required:** Programming language, web framework, database system, API style, authentication mechanism, deployment architecture.

### Stage 6 — Arch. & Conformance Review

API response time: p95 < 200ms, p99 < 500ms. No N+1 queries. Proper indexing.

### Stage 7 — Automated Testing

Unit (min 80%), integration (DB + external APIs), API contract, load tests (expected throughput + 50%), security tests (OWASP ZAP).

---

## Performance Targets

- **p50:** < 100ms
- **p95:** < 200ms
- **p99:** < 500ms
- **Throughput:** ≥ 1000 req/s

---

## Backend P0 Defects (Block Release)

- API crashes or 500 errors
- Data loss or corruption
- Security vulnerability (SQL injection, auth bypass)
- Database connection failure
- Payment processing failure
