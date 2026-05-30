---
paths:
  - "**/full-stack/**"
description: Full-stack development pipeline platform-specific rules
---

# Full-Stack Development Pipeline — Platform-Specific Rules

**Applies To:** Full-stack application development (frontend + backend)

---

## Technology Stack

- **Frontend:** React, Vue, Angular (per ADR)
- **Backend:** Node.js, Python, Go, Java (per ADR)
- **Database:** PostgreSQL, MongoDB, Redis (per ADR)
- **Deployment:** Docker, Kubernetes, serverless (per ADR)

---

## Stage-Specific Full-Stack Requirements

### Stage 1 — PRD + SRD

Full-stack PRD covers both frontend and backend concerns: UI/UX, API, business logic, data processing, integrations, performance + scalability.

Full-stack SRD: frontend security (XSS/CSRF/CSP), backend security (auth/authorization/validation), database security, API security, end-to-end HTTPS.

### Stage 3 — UML Engineering Package

**ADRs required:** Frontend framework, backend framework, database system, API style, authentication mechanism, deployment architecture.

### Stage 6 — Arch. & Conformance Review

Frontend Core Web Vitals + backend API response times + database query optimization + end-to-end integration tests.

### Stage 7 — Automated Testing

Frontend unit + backend unit + frontend integration (API mocking) + backend integration (DB + external) + E2E (full user flows) + API contract + DB migration tests.

---

## Deployment Architecture Options

- **Monorepo:** Single repo, shared tooling, coordinated versioning
- **Multi-Repo:** Independent pipelines, API contract as integration point

---

## Full-Stack P0 Defects (Block Release)

- Application crashes (frontend or backend)
- Data loss or corruption
- Security vulnerability (either layer)
- Authentication bypass
- Database connection failure
