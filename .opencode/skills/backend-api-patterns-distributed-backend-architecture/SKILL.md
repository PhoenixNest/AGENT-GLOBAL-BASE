---
name: backend-api-patterns-distributed-backend-architecture
description: Distributed backend architecture for high-scale systems — microservices design with domain-driven boundaries, service decomposition, inter-service communication patterns, and scalability strategies for 220M+ MAU. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 3 (Architecture) for service boundary design and Stage 5 (Development) for distributed system implementation. Trigger: distributed architecture, microservices boundaries, domain-driven design, service decomposition, high scale, maa.
prerequisites:
  - backend-api-patterns-distributed-systems

version: "1.0.0"
---

# Distributed Backend Architecture

## Purpose

Design and operate backend systems serving 220M+ MAU with sub-500ms P99 latency, 99.99% availability, and zero-downtime deployments. Own the architecture for all web and backend services in the 10-stage pipeline — from PRD requirements (Stage 1) through release sign-off (Stage 10).

## Microservices Design with Domain-Driven Design

### Service Boundary Identification

Use event storming to identify bounded contexts — the foundation of service boundaries:

```
Event Storming Process:
1. Gather domain experts + engineering team (2-hour workshop)
2. Identify domain events (past-tense business facts): "OrderPlaced", "PaymentProcessed"
3. Identify commands that produce events: "PlaceOrder", "ProcessPayment"
4. Identify aggregates (consistency boundaries): Order, Payment, Inventory
5. Draw bounded contexts around cohesive aggregates
6. Identify context maps: how do bounded contexts communicate?
```

**Rule:** One microservice = one bounded context. If a service spans multiple bounded contexts, it is too large. Split at the aggregate boundary.

### Inter-Service Communication Patterns

| Pattern                        | When to Use                                                 | Technology                                                        | Trade-off                                                                                             |
| ------------------------------ | ----------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Synchronous (request/response) | Real-time user-facing queries requiring immediate response  | gRPC with protobuf                                                | Tight coupling; cascading failures if downstream is slow. Always implement circuit breaker + timeout. |
| Asynchronous (event-driven)    | Side effects, eventual consistency, audit trails, analytics | Kafka with Avro schemas                                           | Eventual consistency (not suitable for real-time user queries); requires idempotent consumers         |
| Saga (distributed transaction) | Multi-service business transactions requiring compensation  | Kafka + choreography (preferred) or orchestration (complex sagas) | Complexity increases with saga participants; compensation logic must be idempotent                    |
| API Composition                | User-facing queries spanning multiple services              | Backend-for-Frontend (BFF) pattern                                | BFF becomes a critical dependency; cache aggressively                                                 |

### Database-per-Service Pattern

**Rule:** No two services share a database. Each service owns its data model and is the only writer to its tables.

| Data Requirement                | Technology            | Use Case                                                        |
| ------------------------------- | --------------------- | --------------------------------------------------------------- |
| Transactional (OLTP)            | PostgreSQL 15+        | Order management, user accounts, payment records                |
| Read-optimized (CQRS read side) | Elasticsearch 8.x     | Search, filtering, full-text queries                            |
| Session/cache                   | Redis 7.x (clustered) | Session storage, rate limiting counters, real-time leaderboards |
| Time-series/analytics           | TimescaleDB           | Metrics, audit logs, usage analytics                            |
| Document/BLOB                   | S3 + DynamoDB         | User-uploaded files, feature flags, configuration               |

**Data consistency across services:** Use the Outbox Pattern — write to a local `outbox` table within the same transaction as the business data, then a separate process (Debezium CDC or polling) publishes the event to Kafka. This guarantees at-least-once delivery without distributed transactions.

## Event-Driven Architecture (Kafka)

### Topic Design Standards

```
Topic naming: {domain}.{entity}.{event-type}
Examples:
  orders.order.created
  orders.order.cancelled
  payments.payment.processed
  users.user.profile_updated
```

**Partition key selection:** Choose the key that ensures related events land in the same partition (preserving order). For orders: `orderId`. For user events: `userId`. Do NOT use timestamps or random UUIDs as partition keys — they destroy ordering guarantees.

### Event Schema with Avro + Schema Registry

```json
{
  "type": "record",
  "name": "OrderCreatedEvent",
  "namespace": "com.company.orders.events",
  "fields": [
    { "name": "orderId", "type": "string" },
    { "name": "userId", "type": "string" },
    { "name": "items", "type": { "type": "array", "items": "OrderItem" } },
    {
      "name": "totalAmount",
      "type": {
        "type": "bytes",
        "logicalType": "decimal",
        "precision": 10,
        "scale": 2
      }
    },
    {
      "name": "timestamp",
      "type": { "type": "long", "logicalType": "timestamp-millis" }
    }
  ]
}
```

**Compatibility rule:** BACKWARD compatible (new consumers can read old events). Additive changes only — new fields must have defaults. Removing or renaming fields requires a migration plan with dual-write period.

### Dead Letter Queue Pattern

When a consumer cannot process an event after retries (max 3, exponential backoff starting at 1s), send to `{topic}.dlq` for manual investigation. DLQ messages must include:

- Original event payload
- Consumer group ID
- Error message + stack trace
- Retry count + timestamps
- Offset information for reprocessing

Monitor DLQ depth — a growing DLQ indicates a systemic issue, not a transient failure. Alert on DLQ depth >100 messages.

## Kubernetes Orchestration + Istio Service Mesh

### Deployment Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0 # zero-downtime — always have N replicas
      maxSurge: 1
  template:
    spec:
      containers:
        - name: orders-service
          image: registry.company.com/orders-service:v2.3.1
          resources:
            requests: { cpu: 250m, memory: 512Mi }
            limits: { cpu: 500m, memory: 1Gi }
          readinessProbe:
            httpGet: { path: /ready, port: 8080 }
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /health, port: 8080 }
            initialDelaySeconds: 30
            periodSeconds: 10
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                topologyKey: kubernetes.io/hostname
                labelSelector: { matchLabels: { app: orders-service } }
```

**Pod anti-affinity** ensures replicas are spread across nodes — a single node failure does not take down all instances of a service.

### Istio Traffic Management

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: orders-canary
spec:
  hosts: [orders-service]
  http:
    - route:
        - destination: { host: orders-service, subset: v2.3.1 }
          weight: 90
        - destination: { host: orders-service, subset: v2.4.0-rc1 }
          weight: 10
      timeout: 2s
      retries:
        attempts: 3
        perTryTimeout: 500ms
```

Canary deployments with automatic analysis: monitor error rate, P99 latency, and business KPIs for the canary subset. If any metric degrades >5% vs. stable, auto-rollback.

## Observability at Scale

### OpenTelemetry Instrumentation (All Services)

Every service MUST emit:

| Signal      | Instrumentation                                                                                                  | Propagation                                                     |
| ----------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Traces**  | OpenTelemetry SDK with auto-instrumentation + manual span creation for business-critical paths                   | W3C Trace Context header propagation across all HTTP/gRPC calls |
| **Metrics** | RED method per service endpoint: Rate (requests/sec), Errors (failed requests/sec), Duration (latency histogram) | Labels: service_name, endpoint, method, status_code, version    |
| **Logs**    | Structured JSON logging with trace_id, span_id, user_id (if authenticated) correlation                           | Log aggregation via Fluent Bit → Loki/Elasticsearch             |

### SLO Management with Multi-Window, Multi-Burn-Rate Alerting

| SLO           | Target | Window  | Burn Rate  | Alert Severity |
| ------------- | ------ | ------- | ---------- | -------------- |
| Availability  | 99.9%  | 30 days | 14.4x (2h) | Page           |
| Availability  | 99.9%  | 30 days | 6x (5h)    | Page           |
| Availability  | 99.9%  | 30 days | 1x (1d)    | Ticket         |
| Latency (P99) | <500ms | 30 days | 14.4x (2h) | Page           |
| Latency (P99) | <500ms | 30 days | 1x (1d)    | Ticket         |

**Burn rate** = how fast you're consuming your error budget. At 14.4x burn rate, you exhaust your monthly error budget in 2 hours — that warrants an immediate page.

## Quality Standards

- All services must have `/health` and `/ready` endpoints
- P99 latency SLA: <500ms for user-facing APIs, <100ms for internal service calls
- Error rate target: <0.1% for all production services
- Test coverage: unit ≥80%, integration ≥70%, contract tests for all inter-service boundaries
- No service may be deployed without OpenTelemetry instrumentation and Grafana dashboards
- All services must participate in chaos engineering quarterly (kill a pod, verify zero user impact)
- SLO dashboards must be visible to ALL engineers, not just the service owners
