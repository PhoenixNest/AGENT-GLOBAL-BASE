---
inclusion: manual
description: Backend/API architecture patterns and best practices
---

# Backend Architecture Steering

This steering file provides backend and API development guidance for the workspace. Activate manually when working on server-side code.

## Backend Context

- **Architecture Style:** Microservices, RESTful APIs, GraphQL
- **Common Languages:** Node.js (TypeScript), Python, Java/Kotlin, Go
- **Databases:** PostgreSQL, MongoDB, Redis
- **Message Queues:** RabbitMQ, Kafka, AWS SQS
- **Cloud Platforms:** AWS, GCP, Azure

## Architecture Patterns

### 1. API Design

- **RESTful APIs:** Follow REST principles (resources, HTTP verbs, status codes)
- **GraphQL:** Use for complex data requirements
- **API Versioning:** Use URL versioning (`/v1/`, `/v2/`)
- **Documentation:** OpenAPI/Swagger for REST, GraphQL schema for GraphQL
- **Rate Limiting:** Implement per-client rate limits

### 2. Microservices Architecture

- **Service Boundaries:** One service per bounded context
- **Communication:** REST for synchronous, message queues for async
- **Service Discovery:** Use service mesh or API gateway
- **Data Ownership:** Each service owns its data
- **Distributed Tracing:** Implement with OpenTelemetry

### 3. Database Patterns

- **Repository Pattern:** Abstract data access
- **Database per Service:** Each microservice has its own database
- **CQRS:** Separate read and write models when needed
- **Event Sourcing:** For audit trails and complex domains
- **Migrations:** Use versioned migration tools (Flyway, Liquibase)

### 4. Caching Strategy

- **Cache Layers:** Application cache (Redis), CDN, database query cache
- **Cache Invalidation:** Time-based, event-based, or manual
- **Cache-Aside Pattern:** Load from cache, fallback to database
- **Write-Through Cache:** Update cache on write

### 5. Security

- **Authentication:** JWT, OAuth 2.0, API keys
- **Authorization:** RBAC (Role-Based Access Control)
- **Input Validation:** Validate all inputs server-side
- **SQL Injection Prevention:** Use parameterized queries
- **Rate Limiting:** Prevent abuse and DDoS
- **HTTPS Only:** Enforce TLS 1.2+
- **Secrets Management:** Use vault services (AWS Secrets Manager, HashiCorp Vault)

### 6. Error Handling

- **Consistent Error Format:** Use RFC 7807 Problem Details
- **HTTP Status Codes:** Use appropriate codes (200, 201, 400, 401, 403, 404, 500)
- **Error Logging:** Log errors with context (request ID, user ID, timestamp)
- **Graceful Degradation:** Handle downstream failures gracefully

### 7. Performance

- **Database Indexing:** Index frequently queried fields
- **Connection Pooling:** Reuse database connections
- **Async Processing:** Use message queues for long-running tasks
- **Pagination:** Implement cursor-based or offset pagination
- **Query Optimization:** Use EXPLAIN to analyze queries

### 8. Observability

- **Logging:** Structured logging (JSON format)
- **Metrics:** Track request rate, latency, error rate (RED metrics)
- **Tracing:** Distributed tracing for request flows
- **Health Checks:** Implement `/health` and `/ready` endpoints
- **Alerting:** Set up alerts for critical metrics

## API Best Practices

### 1. RESTful API Design

```
GET    /api/v1/users          # List users
GET    /api/v1/users/:id      # Get user
POST   /api/v1/users          # Create user
PUT    /api/v1/users/:id      # Update user
DELETE /api/v1/users/:id      # Delete user
```

### 2. Request/Response Format

```json
// Request
{
  "data": {
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}

// Response
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  },
  "meta": {
    "timestamp": "2026-05-06T12:00:00Z"
  }
}
```

### 3. Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

## Testing Strategy

- **Unit Tests:** Test business logic in isolation
- **Integration Tests:** Test API endpoints with real database
- **Contract Tests:** Verify API contracts (Pact, Spring Cloud Contract)
- **Load Tests:** Test performance under load (k6, JMeter)
- **Aim for 80%+ code coverage**

## Related Resources

- **Company Architecture Standards:** `company/library/topics/architecture.md`
- **Company Security Standards:** `company/library/topics/security.md`
- **Company Testing Standards:** `company/library/topics/testing.md`
- **Backend Engineering Skills:** `.kiro/skills/backend-engineering/`
- **Backend Pipeline:** `.kiro/steering/backend-pipeline.md`

## When to Activate

Activate this steering file when:

- Designing new backend services or APIs
- Reviewing backend architecture decisions
- Implementing API endpoints
- Debugging backend performance issues
- Writing backend tests
