# Distributed Systems

**Category:** Backend Architecture
**Owner:** Backend Chapter Lead (Dev Malhotra)

## Overview

Designs and operates distributed systems at scale, implementing microservices architecture with event-driven communication patterns, resilience engineering, and observability. This skill covers saga pattern orchestration, circuit breaker implementation, idempotency guarantees, and distributed tracing with OpenTelemetry across service boundaries.

## Competency Dimensions

| Dimension                  | Description                                                           | Proficiency Indicators                                                                                                                                            |
| -------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Microservices Architecture | Service decomposition, bounded contexts, inter-service communication  | Can decompose a monolith into cohesive services with clear domain boundaries; selects synchronous vs asynchronous communication based on consistency requirements |
| Event-Driven Design        | Event sourcing foundations, pub/sub patterns, event schema evolution  | Designs event schemas with forward/backward compatibility; implements dead-letter queues and retry policies with exponential backoff                              |
| Saga Pattern               | Distributed transaction management via choreography and orchestration | Implements both choreography-based and orchestration-based sagas; handles compensating transactions for partial failures                                          |
| Circuit Breakers           | Fault tolerance, bulkhead isolation, fallback strategies              | Configures circuit breaker thresholds (failure rate, slow call rate) based on SLO data; implements fallback responses that degrade gracefully                     |
| Idempotency                | Request deduplication, idempotency keys, exactly-once semantics       | Designs idempotent APIs with idempotency key storage; ensures at-least-once delivery produces exactly-once results                                                |
| Distributed Tracing        | OpenTelemetry instrumentation, trace correlation, span attributes     | Instruments all services with OTel SDK; implements trace-context propagation (W3C Trace Context); defines span attributes aligned with semantic conventions       |

## Execution Guidance

### Microservices Decomposition

Apply Domain-Driven Design bounded contexts as service boundaries. Each service owns its data schema and exposes capabilities through well-defined APIs. Use the following decision matrix for inter-service communication:

| Requirement                            | Pattern                        | Technology                            |
| -------------------------------------- | ------------------------------ | ------------------------------------- |
| Strong consistency, immediate response | Synchronous (REST/gRPC)        | gRPC with deadline, REST with timeout |
| Eventual consistency, decoupled        | Asynchronous (event streaming) | Kafka, RabbitMQ                       |
| Request aggregation                    | API Gateway / BFF              | Kong, Envoy, custom gateway           |
| Query across services                  | CQRS with read model           | Materialized views, Elasticsearch     |

### Saga Pattern Implementation

**Orchestration-based Saga** (preferred for complex workflows):

```go
type SagaOrchestrator struct {
    steps      []SagaStep
    compensations []CompensatingAction
}

type SagaStep struct {
    Name        string
    Action      func(ctx context.Context, data map[string]interface{}) error
    Compensate  func(ctx context.Context, data map[string]interface{}) error
}

func (s *SagaOrchestrator) Execute(ctx context.Context) error {
    completedSteps := []int{}

    for i, step := range s.steps {
        if err := step.Action(ctx, nil); err != nil {
            // Compensate in reverse order
            for j := len(completedSteps) - 1; j >= 0; j-- {
                compStep := s.steps[completedSteps[j]]
                compErr := compStep.Compensate(ctx, nil)
                if compErr != nil {
                    log.WithError(compErr).Errorf("Compensation failed for step: %s", compStep.Name)
                    // Alert SRE — manual intervention required
                }
            }
            return fmt.Errorf("saga failed at step %d (%s): %w", i, step.Name, err)
        }
        completedSteps = append(completedSteps, i)
    }
    return nil
}
```

**Choreography-based Saga** (simpler, fewer dependencies):

Each service listens for events from upstream services and publishes its own events. The trade-off: no central visibility into saga state, but lower coupling.

```
Order Service          Payment Service          Inventory Service
     |                        |                        |
     |-- OrderCreated ------->|                        |
     |                        |-- PaymentProcessed --->|
     |                        |                        |-- InventoryReserved -->
     |                        |                        |     (Saga Complete)
     |<-- OrderConfirmed -----|<-----------------------|
```

### Circuit Breaker Configuration

Use resilience4j (Java) or go-resilience (Go). Configuration based on SLO data:

```yaml
resilience4j.circuitbreaker:
  instances:
    paymentService:
      slidingWindowSize: 100
      slidingWindowType: COUNT_BASED
      minimumNumberOfCalls: 50
      failureRateThreshold: 50
      slowCallRateThreshold: 80
      slowCallDurationThreshold: 2s
      waitDurationInOpenState: 30s
      permittedNumberOfCallsInHalfOpenState: 10
      automaticTransitionFromOpenToHalfOpenEnabled: true
```

**Decision framework for thresholds:**

| SLO Target         | Failure Rate Threshold | Slow Call Threshold | Rationale                         |
| ------------------ | ---------------------- | ------------------- | --------------------------------- |
| 99.9% availability | 1%                     | p99 latency + 50%   | Tight — catches degradation early |
| 99.5% availability | 5%                     | p99 latency + 100%  | Moderate — tolerates minor spikes |
| 99.0% availability | 10%                    | p99 latency + 200%  | Loose — avoids false trips        |

### Idempotency Key Implementation

```go
type IdempotencyStore struct {
    redis *redis.Client
    ttl   time.Duration
}

func (s *IdempotencyStore) ExecuteWithIdempotency(ctx context.Context, idempotencyKey string, handler func() (interface{}, error)) (interface{}, error) {
    key := fmt.Sprintf("idempotency:%s", idempotencyKey)

    // Check if request already processed
    cached, err := s.redis.Get(ctx, key).Result()
    if err == nil {
        var result IdempotencyRecord
        json.Unmarshal([]byte(cached), &result)
        return result.Response, nil
    }

    // Acquire lock to prevent concurrent duplicate processing
    acquired, err := s.redis.SetNX(ctx, key+":lock", "1", 30*time.Second).Result()
    if !acquired {
        return nil, ErrRequestInProgress
    }

    // Execute handler
    response, handlerErr := handler()

    // Store result
    record := IdempotencyRecord{Response: response, Error: handlerErr}
    data, _ := json.Marshal(record)
    s.redis.Set(ctx, key, data, s.ttl)
    s.redis.Del(ctx, key+":lock")

    return response, handlerErr
}
```

**Key design decisions:**

- Idempotency keys are client-generated UUIDs, passed via `Idempotency-Key` header
- TTL matches business window for duplicate detection (typically 24h)
- Lock prevents thundering herd on duplicate concurrent requests
- Response cache includes both success and error responses

### OpenTelemetry Distributed Tracing

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 1024
  tail_sampling:
    policies:
      - name: errors
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: slow-requests
        type: latency
        latency: { threshold_ms: 500 }
      - name: probabilistic
        type: probabilistic
        probabilistic: { sampling_percentage: 10 }

exporters:
  otlp/jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, tail_sampling]
      exporters: [otlp/jaeger]
```

**Required span attributes per semantic conventions:**

| Attribute           | Example                         | Required                  |
| ------------------- | ------------------------------- | ------------------------- |
| `service.name`      | `payment-service`               | Yes                       |
| `http.method`       | `POST`                          | Yes (HTTP spans)          |
| `http.status_code`  | `200`                           | Yes (HTTP spans)          |
| `db.system`         | `postgresql`                    | Yes (DB spans)            |
| `db.statement`      | `SELECT * FROM orders WHERE...` | Yes (DB spans, sanitized) |
| `messaging.system`  | `kafka`                         | Yes (messaging spans)     |
| `error`             | `true`                          | Yes (on error)            |
| `exception.message` | `Connection refused`            | Yes (on exception)        |

## Pipeline Integration

**Stage 3 (UML Engineering Package):** Component diagrams must show inter-service communication patterns, saga flows, and circuit breaker boundaries. ADRs required for saga orchestration vs choreography decisions.

**Stage 4 (Implementation Plan):** Distributed system complexity must be reflected in task estimates. Saga compensation paths require separate implementation and testing tasks.

**Stage 5 (Development):** Services developed in parallel by platform teams. OpenTelemetry instrumentation mandatory for all services before Stage 6 gate.

**Stage 6 (Code Review):** Review panel validates circuit breaker configurations, idempotency implementation, and trace coverage across all service boundaries.

**Stage 7 (Testing):** Chaos engineering tests validate circuit breaker behavior. Saga compensation tested via fault injection. Distributed trace validation ensures end-to-end visibility.

**Stage 8 (Integrity Verification):** Panel verifies that distributed system design matches implementation — saga completeness, circuit breaker coverage, trace propagation across all services.

## Quality Standards

| Metric                                   | Target                                | Measurement                   |
| ---------------------------------------- | ------------------------------------- | ----------------------------- |
| Trace coverage                           | 100% of inter-service calls           | OTel collector metrics        |
| Idempotency coverage                     | 100% of mutation endpoints            | API contract audit            |
| Circuit breaker coverage                 | All external service dependencies     | Architecture review checklist |
| Saga compensation completeness           | 100% of saga steps have compensations | Saga design document review   |
| Mean time to detect distributed failures | < 30 seconds                          | SLO monitoring                |
| P99 latency (inter-service)              | < 200ms                               | Distributed tracing data      |
| Error budget consumption                 | < 25% per rolling 30 days             | SLO dashboard                 |
