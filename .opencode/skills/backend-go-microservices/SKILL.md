---
name: backend-go-microservices
description: Go microservices architecture — service decomposition, inter-service communication patterns, resilience engineering, distributed observability, and production deployment strategies. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 3 (Architecture) for service boundary design and Stage 5 (Development) for Go microservice implementation. Trigger: go microservices, service decomposition, grpc go, inter-service communication, resilience, go deployment.
prerequisites:
  - backend-go-rest-api

version: "1.0.0"
---

# Go Microservices Architecture

## Overview

This skill covers the design, implementation, and deployment of microservices in Go, including service decomposition, inter-service communication patterns, resilience engineering, distributed observability, and production deployment strategies.

### When to Use Microservices vs Monolith

| Factor               | Monolith           | Microservices                 |
| -------------------- | ------------------ | ----------------------------- |
| Team size            | 1-2 teams          | 3+ independent teams          |
| Deployment frequency | Weekly/monthly     | Multiple times per day        |
| Service boundaries   | Unclear domains    | Well-defined bounded contexts |
| Scalability needs    | Uniform scaling    | Per-service scaling           |
| Failure isolation    | Process-level only | Service-level isolation       |
| Technology diversity | Single stack       | Polyglot persistence/services |

**Decision heuristic:** Start with a modular monolith. Extract to microservices when you have clear domain boundaries, independent scaling requirements, and multiple teams that need autonomous deployment cycles.

### Go Microservices Scope

- Service decomposition using Domain-Driven Design (DDD) principles
- Inter-service communication via gRPC, REST, and async message queues
- Service discovery and registration patterns
- Resilience engineering: circuit breakers, retries, timeouts, bulkheads
- Distributed tracing with OpenTelemetry
- Configuration management and secret injection
- Deployment patterns: blue-green, canary, feature flags
- Stage 5 integration within the 10-stage pipeline

---

## Service Architecture

### Monorepo vs Polyrepo

#### Monorepo Structure

```
microservices/
├── services/
│   ├── user-service/
│   │   ├── cmd/server/main.go
│   │   ├── internal/
│   │   │   ├── handler/
│   │   │   ├── service/
│   │   │   ├── repository/
│   │   │   └── model/
│   │   ├── proto/
│   │   │   └── user/v1/user.proto
│   │   └── go.mod
│   ├── order-service/
│   │   ├── cmd/server/main.go
│   │   ├── internal/
│   │   ├── proto/
│   │   │   └── order/v1/order.proto
│   │   └── go.mod
│   └── payment-service/
│       ├── cmd/server/main.go
│       ├── internal/
│       ├── proto/
│       │   └── payment/v1/payment.proto
│       └── go.mod
├── shared/
│   ├── go-mod/
│   │   └── proto/          # Shared protobuf definitions
│   └── pkg/
│       ├── middleware/
│       ├── tracing/
│       └── config/
├── buf.yaml                 # Buf build configuration
├── buf.gen.yaml
└── Makefile
```

#### Polyrepo Structure

Each service is an independent repository with its own CI/CD pipeline.

**Monorepo advantages:**

- Shared tooling and linting
- Easier cross-service refactoring
- Atomic commits across services
- Simplified dependency management

**Polyrepo advantages:**

- Independent access control per service
- Isolated CI/CD pipelines
- Clearer service ownership
- Smaller repository size

**Recommendation for Stage 5:** Use monorepo for teams under 30 engineers; polyrepo for larger organizations with strict service isolation requirements.

### Domain-Driven Design Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                      Bounded Context                       │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ User Service │    │Order Service │    │Payment Svc   │  │
│  │              │    │              │    │              │  │
│  │ • Aggregate  │    │ • Aggregate  │    │ • Aggregate  │  │
│  │ • Repository │    │ • Repository │    │ • Repository │  │
│  │ • Handler    │    │ • Handler    │    │ • Handler    │  │
│  │ • Domain     │    │ • Domain     │    │ • Domain     │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │           │
│         └───────────────────┼───────────────────┘           │
│                             │                               │
│                    ┌────────▼────────┐                       │
│                    │  Anti-Corruption │                       │
│                    │     Layer        │                       │
│                    └─────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

**Bounded context identification:**

1. Identify aggregate roots in your domain model
2. Group related aggregates that change together
3. Define explicit context maps between bounded contexts
4. Implement anti-corruption layers for external integrations

### Service Granularity

```go
// WRONG: Service doing too much (god service)
type GodService struct {
    userRepo     UserRepository
    orderRepo    OrderRepository
    paymentRepo  PaymentRepository
    emailClient  EmailClient
    smsClient    SMSClient
    analytics    AnalyticsClient
    // ... 20 more dependencies
}

// RIGHT: Focused service with clear responsibility
type OrderService struct {
    orderRepo   OrderRepository
    paymentClient PaymentServiceClient // gRPC client to payment service
    eventBus    EventBus
}
```

**Rules of thumb:**

- A service should be understandable by one engineer in 1-2 weeks
- If a service requires changes for every new feature, it is too broad
- Database-per-service is the ideal boundary (shared DB = coupled services)
- Cross-service transactions use Saga pattern, not distributed ACID

---

## Stage 5 Integration

### SPEC Development

During Stage 5 (Development), the CTO oversees platform teams implementing microservices according to the Coding Implementation Plan from Stage 4. Each microservice should be tracked with its own development log.

**Development Log Structure:**

```
company/project/<project>/platforms/<platform>/code/
├── services/
│   ├── order-service/
│   │   ├── DEVELOPMENT-LOG.md    # Per-service development tracking
│   │   └── ...
│   └── payment-service/
│       ├── DEVELOPMENT-LOG.md
│       └── ...
└── ...
```

### Code Review Checklist (Stage 6)

```markdown
## Go Microservices Code Review Checklist

### Architecture

- [ ] Service has clear bounded context
- [ ] Dependencies flow inward (Clean Architecture)
- [ ] No circular dependencies between packages
- [ ] Protobuf definitions follow semantic versioning

### Communication

- [ ] gRPC services use proper error handling (status codes)
- [ ] Timeouts are set on all external calls
- [ ] Circuit breakers protect external service calls
- [ ] Async events include trace context

### Resilience

- [ ] Circuit breaker thresholds are appropriate
- [ ] Retry policies use exponential backoff with jitter
- [ ] Bulkheads limit concurrent requests
- [ ] Graceful shutdown handles in-flight requests

### Observability

- [ ] OpenTelemetry traces all service boundaries
- [ ] Metrics exported for Prometheus
- [ ] Structured logging with correlation IDs
- [ ] Health checks (readiness + liveness) implemented

### Security

- [ ] TLS enabled for gRPC (mTLS in production)
- [ ] Authentication/authorization on all endpoints
- [ ] Secrets injected via environment variables (not hardcoded)
- [ ] Input validation on all public APIs

### Testing

- [ ] Unit tests for domain logic
- [ ] Contract tests for gRPC interfaces
- [ ] Integration tests with testcontainers
- [ ] Chaos tests for critical failure modes
```

### Defect Classification for Microservices

| Scenario                                        | Severity | Rationale               |
| ----------------------------------------------- | -------- | ----------------------- |
| Service crashes on malformed input              | P0       | Availability failure    |
| Circuit breaker not protecting external calls   | P0       | Cascading failure risk  |
| Missing TLS on production endpoints             | P0       | Data breach risk        |
| gRPC timeout too long causing thread exhaustion | P1       | Performance degradation |
| Tracing not propagating between services        | P1       | Observability gap       |
| Health check not implemented                    | P2       | Deployment reliability  |
| Missing retry logic for transient failures      | P2       | Resilience gap          |
| No bulkhead limiting concurrent requests        | P3       | Defense-in-depth        |

---

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`inter-service-communication.md`](references/inter-service-communication.md) — Inter-Service Communication
- [`service-discovery.md`](references/service-discovery.md) — Service Discovery
- [`resilience-patterns.md`](references/resilience-patterns.md) — Resilience Patterns
- [`distributed-tracing.md`](references/distributed-tracing.md) — Distributed Tracing
- [`configuration-management.md`](references/configuration-management.md) — Configuration Management
- [`deployment-patterns.md`](references/deployment-patterns.md) — Deployment Patterns
- [`testing-strategies.md`](references/testing-strategies.md) — Testing Strategies
- [`references.md`](references/references.md) — References
