---
inclusion: fileMatch
fileMatchPattern: "**/full-stack/**"
---

# Full-Stack Development Pipeline — Platform-Specific Rules

**Authority:** AGENTS.md § 4.4 + `company/pipeline/full-stack/pipeline.md`  
**Applies To:** Full-stack application development (frontend + backend)

---

## Full-Stack Pipeline Overview

The full-stack development pipeline follows the standard 13-stage company pipeline with requirements spanning both frontend and backend concerns.

## Technology Stack

- **Frontend:** React, Vue, Angular (per ADR)
- **Backend:** Node.js, Python, Go, Java (per ADR)
- **Database:** PostgreSQL, MongoDB, Redis (per ADR)
- **Deployment:** Docker, Kubernetes, serverless (per ADR)

## Stage-Specific Full-Stack Requirements

### Stage 1: Requirements → PRD + SRD

**Full-Stack PRD Sections:**

- Frontend requirements (UI, UX, responsiveness)
- Backend requirements (API, business logic, data processing)
- Database requirements (data models, relationships, queries)
- Integration requirements (third-party services, APIs)
- Performance requirements (frontend + backend)
- Scalability requirements (horizontal scaling, load balancing)

**Full-Stack SRD Sections:**

- Frontend security (XSS, CSRF, CSP)
- Backend security (authentication, authorization, input validation)
- Database security (encryption, access control)
- API security (rate limiting, authentication)
- End-to-end security (HTTPS, secure cookies, token management)

### Stage 2: PRD → Web Prototype + IDS

**Full-Stack Design Requirements:**

- Frontend UI/UX design
- API contract design (OpenAPI/Swagger)
- Database schema design (ERD)
- System architecture diagram
- Data flow diagrams (frontend ↔ backend ↔ database)

### Stage 3: Prototype → UML Engineering Package

**Full-Stack Architecture Decisions:**

- **ADR Required:** Frontend framework
- **ADR Required:** Backend framework
- **ADR Required:** Database system
- **ADR Required:** API style (REST, GraphQL, gRPC)
- **ADR Required:** Authentication mechanism
- **ADR Required:** Deployment architecture
- **TSD Required:** Complete technology stack justification

**Full-Stack UML:**

- System architecture diagram (frontend + backend + database)
- Component hierarchy diagram (frontend)
- API architecture diagram (backend)
- Database schema diagram (ERD)
- Deployment architecture diagram

### Stage 4: UML → Implementation Plan + Gantt

**Full-Stack Tasks:**

- Frontend project scaffolding
- Backend project scaffolding
- Database schema creation
- API contract implementation
- Frontend-backend integration
- CI/CD pipeline setup (monorepo or multi-repo)

### Stage 5: Plan → Software Development

**Full-Stack Development Standards:**

- Maintain API contract consistency
- Implement proper error handling (frontend + backend)
- Use type-safe API clients (TypeScript, OpenAPI codegen)
- Implement proper state management (frontend)
- Implement proper transaction management (backend)
- Use database migrations for schema changes

### Stage 6: Development → Arch. & Conformance Review

**Full-Stack Review Criteria:**

- Frontend performance (Core Web Vitals)
- Backend performance (API response times)
- Database performance (query optimization)
- End-to-end integration testing
- Security compliance (frontend + backend)
- Code quality (both codebases)

### Stage 7: Arch. Review → Automated Testing

**Full-Stack Testing Requirements:**

- Frontend unit tests (components, utilities)
- Backend unit tests (business logic, utilities)
- Frontend integration tests (API mocking)
- Backend integration tests (database, external APIs)
- End-to-end tests (full user flows)
- API contract tests (OpenAPI validation)
- Database migration tests

**Testing Frameworks:**

- **Frontend:** Vitest, Jest, React Testing Library, Playwright
- **Backend:** Jest (Node.js), pytest (Python), testing (Go), JUnit (Java)
- **E2E:** Playwright, Cypress
- **API:** Supertest, httpx, RestAssured

### Stage 8: Testing → Integrity Verification

**Full-Stack Integrity Checks:**

- Frontend security (OWASP Top 10)
- Backend security (OWASP API Security Top 10)
- Database security (encryption, access control)
- Authentication and authorization audit
- API security audit (rate limiting, input validation)
- End-to-end security testing

### Stage 9: Integrity Verification → Translation Production

**Full-Stack Localization:**

- Frontend string externalization
- Backend error message localization
- Email template localization
- Database content localization (if applicable)
- API response message localization

### Stage 10: Translation Production → Release Readiness Check

**Full-Stack Release Checklist:**

- Frontend production build
- Backend production deployment
- Database migrations tested
- Environment variables configured (frontend + backend)
- Secrets management configured
- Monitoring configured (frontend + backend)
- Logging configured (structured logging)
- CDN configuration (frontend assets)

### Stage 11: Live Operations

**Full-Stack Live Ops:**

- Frontend monitoring (Core Web Vitals, error rate)
- Backend monitoring (API uptime, response time, error rate)
- Database monitoring (performance, connections, disk usage)
- End-to-end monitoring (user flows, conversion rates)
- Security monitoring (intrusion detection, vulnerability scanning)
- Performance optimization (frontend + backend)

## Full-Stack Technology Lock Rules

**Locked at Stage 3:**

- Frontend framework
- Backend framework
- Database system
- API style
- Authentication mechanism
- Deployment architecture

**Cannot be changed after Stage 3 approval without full re-entry.**

## Full-Stack Defect Severity

**P0 (Blocks Release):**

- Application crashes (frontend or backend)
- Data loss or corruption
- Security vulnerability (frontend or backend)
- Authentication bypass
- Payment processing failure
- Database connection failure

**P1 (Blocks Release):**

- Core feature non-functional (frontend or backend)
- API endpoint failure
- Database query failure
- Critical UI rendering issue
- Integration failure

## Performance Requirements

**Frontend Targets:**

- LCP < 2.5s
- FID < 100ms
- CLS < 0.1

**Backend Targets:**

- API p95 < 200ms
- API p99 < 500ms
- Throughput: 1000 req/s minimum

**Database Targets:**

- Simple queries < 10ms
- Complex queries < 100ms
- No queries > 1 second

## Deployment Architecture

**Monorepo Pattern:**

- Single repository for frontend + backend
- Shared tooling and CI/CD
- Coordinated versioning

**Multi-Repo Pattern:**

- Separate repositories for frontend + backend
- Independent deployment pipelines
- API contract as integration point

## Related Steering Files

- `company-pipeline-overview.md` — Core 13-stage pipeline
- `web-pipeline.md` — Frontend-specific rules
- `backend-pipeline.md` — Backend-specific rules
- `frontend-architecture.md` — Frontend patterns (manual)
- `backend-architecture.md` — Backend patterns (manual)
