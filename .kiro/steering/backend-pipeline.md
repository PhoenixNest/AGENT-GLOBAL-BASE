---
inclusion: fileMatch
fileMatchPattern: "**/backend-api/**"
---

# Backend API Development Pipeline — Platform-Specific Rules

**Authority:** AGENTS.md § 4.4 + `company/pipeline/backend-api/pipeline.md`  
**Applies To:** Backend API and server-side application development

---

## Backend Pipeline Overview

The backend API development pipeline follows the standard 13-stage company pipeline with backend-specific requirements and deliverables.

## Technology Stack

- **Languages:** Node.js (TypeScript), Python, Go, Java (per ADR)
- **Frameworks:** Express, Fastify, FastAPI, Django, Gin, Spring Boot (per ADR)
- **Databases:** PostgreSQL, MongoDB, Redis (per ADR)
- **API Style:** REST, GraphQL, gRPC (per ADR)

## Stage-Specific Backend Requirements

### Stage 1: Requirements → PRD + SRD

**Backend-Specific PRD Sections:**

- API endpoints and operations
- Data models and relationships
- Performance requirements (latency, throughput)
- Scalability requirements (concurrent users, requests/second)
- Integration requirements (third-party APIs, services)
- Data retention and archival policies

**Backend-Specific SRD Sections:**

- Authentication and authorization (OAuth 2.0, JWT, API keys)
- Data encryption (at rest, in transit)
- Rate limiting and throttling
- Input validation and sanitization
- SQL injection prevention
- API security (OWASP API Security Top 10)

### Stage 2: PRD → Web Prototype + IDS

**Backend Design Requirements:**

- API specification (OpenAPI/Swagger, GraphQL schema)
- Data model diagrams (ERD, schema diagrams)
- Authentication flow diagrams
- Integration architecture diagrams
- Error response formats

### Stage 3: Prototype → UML Engineering Package

**Backend Architecture Decisions:**

- **ADR Required:** Programming language and runtime
- **ADR Required:** Web framework
- **ADR Required:** Database system (relational, document, cache)
- **ADR Required:** API style (REST, GraphQL, gRPC)
- **ADR Required:** Authentication mechanism
- **ADR Required:** Deployment architecture (monolith, microservices)
- **TSD Required:** Complete technology stack justification

**Backend-Specific UML:**

- System architecture diagram
- Database schema diagram (ERD)
- API architecture diagram
- Authentication and authorization flow
- Deployment architecture diagram

### Stage 4: UML → Implementation Plan + Gantt

**Backend-Specific Tasks:**

- Project scaffolding and dependency setup
- Database schema creation and migrations
- API endpoint implementation plan
- Authentication and authorization setup
- Integration with third-party services
- CI/CD pipeline setup (GitHub Actions, GitLab CI)

### Stage 5: Plan → Software Development

**Backend Development Standards:**

- Follow language-specific best practices
- Implement proper error handling and logging
- Use parameterized queries (SQL injection prevention)
- Implement input validation and sanitization
- Use environment variables for configuration
- Implement proper connection pooling

### Stage 6: Development → Arch. & Conformance Review

**Backend-Specific Review Criteria:**

- API response time (p95 < 200ms, p99 < 500ms)
- Database query optimization (no N+1 queries)
- Proper indexing strategy
- Connection pooling configuration
- Error handling and logging
- Security best practices (OWASP API Security Top 10)

### Stage 7: Arch. Review → Automated Testing

**Backend Testing Requirements:**

- Unit tests (minimum 80% coverage)
- Integration tests (database, external APIs)
- API contract tests (OpenAPI validation)
- Load tests (expected throughput + 50%)
- Security tests (OWASP ZAP, SQL injection, XSS)
- Database migration tests

**Testing Frameworks:**

- **Node.js:** Jest, Vitest, Supertest
- **Python:** pytest, unittest, httpx
- **Go:** testing package, testify
- **Java:** JUnit, Mockito, RestAssured

### Stage 8: Testing → Integrity Verification

**Backend-Specific Integrity Checks:**

- OWASP API Security Top 10 compliance
- SQL injection vulnerability scan
- Authentication and authorization audit
- Secrets management audit (no hardcoded credentials)
- API rate limiting verification
- Data encryption verification (TLS 1.3, AES-256)

### Stage 9: Integrity Verification → Translation Production

**Backend Localization:**

- Error message localization
- Email template localization
- API response message localization
- Locale-specific data formatting
- Timezone handling

### Stage 10: Translation Production → Release Readiness Check

**Backend Release Checklist:**

- Production database migrations tested
- Environment variables configured
- Secrets management configured (AWS Secrets Manager, HashiCorp Vault)
- Monitoring and alerting configured (Prometheus, Grafana, Datadog)
- Logging configured (structured logging, log aggregation)
- Backup and disaster recovery plan
- API documentation published

### Stage 11: Live Operations

**Backend Live Ops:**

- API uptime monitoring (> 99.9% uptime)
- Response time monitoring (p95, p99)
- Error rate monitoring (< 0.1% error rate)
- Database performance monitoring
- Resource utilization monitoring (CPU, memory, disk)
- Security incident response
- Database backup verification

## Backend-Specific Technology Lock Rules

**Locked at Stage 3:**

- Programming language and runtime
- Web framework
- Database system
- API style (REST, GraphQL, gRPC)
- Authentication mechanism
- Deployment architecture

**Cannot be changed after Stage 3 approval without full re-entry.**

## Backend-Specific Defect Severity

**P0 (Blocks Release):**

- API crashes or returns 500 errors
- Data loss or corruption
- Security vulnerability (SQL injection, authentication bypass)
- Database connection failure
- Payment processing failure

**P1 (Blocks Release):**

- Core API endpoint non-functional
- Database query performance issue (> 1s response time)
- Authentication failure
- Integration with critical third-party service broken
- Data validation failure

## Performance Requirements

**API Response Time Targets:**

- **p50:** < 100ms
- **p95:** < 200ms
- **p99:** < 500ms

**Throughput Targets:**

- Minimum: 1000 requests/second
- Peak: 5000 requests/second (with auto-scaling)

**Database Query Targets:**

- Simple queries: < 10ms
- Complex queries: < 100ms
- No queries > 1 second

## Security Requirements

**OWASP API Security Top 10 Compliance:**

1. Broken Object Level Authorization
2. Broken Authentication
3. Broken Object Property Level Authorization
4. Unrestricted Resource Consumption
5. Broken Function Level Authorization
6. Unrestricted Access to Sensitive Business Flows
7. Server Side Request Forgery
8. Security Misconfiguration
9. Improper Inventory Management
10. Unsafe Consumption of APIs

## Related Steering Files

- `company-pipeline-overview.md` — Core 13-stage pipeline
- `backend-architecture.md` — Backend patterns (manual)
- `backend-engineering.md` — Backend engineering domain skill
- `security-architecture.md` — Security patterns (manual)
