---
paths:
  - "**/*.go"
  - "**/*.rb"
  - "company/**/backend/**"
  - "company/**/api/**"
  - "studio/**/backend/**"
  - "studio/**/api/**"
  - "company/**/*.py"
  - "studio/**/*.py"
description: Backend/API architecture patterns
---

# Backend Architecture

Backend and API development patterns. See `.claude/skills/backend-engineering/` for deep sub-skills.

---

## Key Architecture Patterns

### API Design

- RESTful APIs: resources, HTTP verbs, status codes, URL versioning (`/v1/`)
- GraphQL: for complex data requirements
- Documentation: OpenAPI/Swagger or GraphQL schema
- Rate limiting: per-client rate limits mandatory

### Database Patterns

- Repository Pattern, Database per Service (microservices)
- CQRS for complex domains, Event Sourcing for audit trails
- Migrations: Flyway or Liquibase

### Security

- Authentication: JWT (short expiry), OAuth 2.0, API keys
- Authorization: RBAC — validate on every request
- Input validation: server-side always
- Parameterized queries: SQL injection prevention
- Secrets: AWS Secrets Manager or HashiCorp Vault

### Error Handling

- Consistent error format: RFC 7807 Problem Details
- HTTP status codes: 200, 201, 400, 401, 403, 404, 500
- Log errors with context (request ID, user ID, timestamp)

### Observability

- Structured logging (JSON format)
- RED metrics (Rate, Errors, Duration)
- Distributed tracing with OpenTelemetry
- Health/readiness endpoints

---

## Related Rules

- `backend-pipeline.md` — Backend API development pipeline
- `security-architecture.md` — Security patterns
