---
name: circuit-breakers-and-resilience-patterns
description: Implement circuit breakers, retry logic with exponential backoff, and fallback handlers for resilient third-party and internal service integrations.
version: "1.0.0"
---

# Circuit Breakers and Resilience Patterns

| Competency         | Description                                                         | Quality Criteria                                                                                                                               |
| ------------------ | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Circuit Breaker    | Closed/open/half-open state machine for dependency fault isolation  | Implements per-dependency breaker with configurable thresholds; emits state-change metrics; tests half-open probe path                         |
| Retry with Backoff | Exponential backoff with jitter, idempotency guards, budget control | Applies full jitter formula; enforces retry budget (max attempts + total deadline); retries only idempotent operations or after checking state |
| Fallback Handling  | Graceful degradation strategies: cached, static, or no-op responses | Fallback activates automatically on open circuit; stale data served with `Stale-While-Revalidate` header; user-facing errors are non-cryptic   |
| Bulkhead Isolation | Thread pool or semaphore partitioning per upstream dependency       | Limits concurrent calls per dependency; prevents one slow upstream from exhausting shared thread pools; configures independent timeouts        |
| Timeout Policies   | Per-call and aggregate deadline enforcement                         | Distinguishes connect timeout from read timeout; sets total deadline shorter than caller's timeout; propagates deadline via context            |

## Execution Guidance

### Circuit Breaker State Machine

The three-state model prevents cascading failures by short-circuiting calls to a failing dependency:

```
CLOSED ──(failure threshold crossed)──► OPEN
  ▲                                       │
  │                                (recovery timeout)
  │                                       ▼
  └──────(probe succeeds)────── HALF-OPEN
```

| State         | Behavior                              | Transition Trigger                          |
| ------------- | ------------------------------------- | ------------------------------------------- |
| **Closed**    | All calls pass through                | Failure rate > threshold in sliding window  |
| **Open**      | All calls fail fast (no network call) | Recovery timeout elapses → half-open        |
| **Half-Open** | Single probe call allowed             | Probe succeeds → closed; probe fails → open |

**Go implementation (hand-rolled, production-grade):**

```go
package resilience

import (
    "context"
    "errors"
    "sync"
    "time"
)

type State int

const (
    StateClosed State = iota
    StateOpen
    StateHalfOpen
)

var ErrCircuitOpen = errors.New("circuit breaker is open")

type CircuitBreaker struct {
    mu               sync.Mutex
    state            State
    failureCount     int
    successCount     int
    lastFailureTime  time.Time

    // Configuration
    failureThreshold int
    successThreshold int // successes needed to close from half-open
    timeout          time.Duration
    windowSize       int
}

func NewCircuitBreaker(failureThreshold, successThreshold int, timeout time.Duration) *CircuitBreaker {
    return &CircuitBreaker{
        failureThreshold: failureThreshold,
        successThreshold: successThreshold,
        timeout:          timeout,
    }
}

func (cb *CircuitBreaker) Execute(ctx context.Context, fn func(ctx context.Context) error) error {
    if err := cb.allowRequest(); err != nil {
        return err
    }

    err := fn(ctx)

    cb.mu.Lock()
    defer cb.mu.Unlock()

    if err != nil {
        cb.onFailure()
    } else {
        cb.onSuccess()
    }
    return err
}

func (cb *CircuitBreaker) allowRequest() error {
    cb.mu.Lock()
    defer cb.mu.Unlock()

    switch cb.state {
    case StateOpen:
        if time.Since(cb.lastFailureTime) > cb.timeout {
            cb.state = StateHalfOpen
            cb.successCount = 0
            return nil // Allow one probe
        }
        return ErrCircuitOpen
    default:
        return nil
    }
}

func (cb *CircuitBreaker) onFailure() {
    cb.failureCount++
    cb.lastFailureTime = time.Now()
    if cb.state == StateHalfOpen || cb.failureCount >= cb.failureThreshold {
        cb.state = StateOpen
        cb.failureCount = 0
    }
}

func (cb *CircuitBreaker) onSuccess() {
    if cb.state == StateHalfOpen {
        cb.successCount++
        if cb.successCount >= cb.successThreshold {
            cb.state = StateClosed
            cb.failureCount = 0
        }
    } else {
        cb.failureCount = 0
    }
}
```

**Python implementation (using `tenacity` + manual breaker via `pybreaker`):**

```python
import pybreaker
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

# Circuit breaker: open after 5 failures, try recovery after 30s
breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=30)

@breaker
def call_payment_service(payload: dict) -> dict:
    response = requests.post("https://payments.internal/charge", json=payload, timeout=3)
    response.raise_for_status()
    return response.json()
```

### Retry with Exponential Backoff and Full Jitter

**Why full jitter?** Pure exponential backoff creates synchronized retry storms when many clients fail simultaneously. Full jitter randomizes the wait within `[0, min(cap, base * 2^attempt)]`.

```
wait = random(0, min(cap_ms, base_ms * 2^attempt))
```

**Go implementation:**

```go
package resilience

import (
    "context"
    "math"
    "math/rand"
    "time"
)

type RetryConfig struct {
    MaxAttempts  int
    BaseDelay    time.Duration
    MaxDelay     time.Duration
    TotalTimeout time.Duration
}

func DefaultRetryConfig() RetryConfig {
    return RetryConfig{
        MaxAttempts:  4,
        BaseDelay:    100 * time.Millisecond,
        MaxDelay:     10 * time.Second,
        TotalTimeout: 30 * time.Second,
    }
}

func WithRetry(ctx context.Context, cfg RetryConfig, fn func(ctx context.Context) error) error {
    ctx, cancel := context.WithTimeout(ctx, cfg.TotalTimeout)
    defer cancel()

    var lastErr error
    for attempt := 0; attempt < cfg.MaxAttempts; attempt++ {
        if err := ctx.Err(); err != nil {
            return err // Total deadline exceeded
        }

        lastErr = fn(ctx)
        if lastErr == nil {
            return nil
        }

        // Do not retry on non-retriable errors (e.g. 4xx client errors)
        if !isRetriable(lastErr) {
            return lastErr
        }

        if attempt < cfg.MaxAttempts-1 {
            wait := fullJitter(cfg.BaseDelay, cfg.MaxDelay, attempt)
            select {
            case <-time.After(wait):
            case <-ctx.Done():
                return ctx.Err()
            }
        }
    }
    return lastErr
}

// Full jitter: random in [0, min(maxDelay, base * 2^attempt)]
func fullJitter(base, max time.Duration, attempt int) time.Duration {
    cap := time.Duration(math.Min(
        float64(max),
        float64(base)*math.Pow(2, float64(attempt)),
    ))
    return time.Duration(rand.Int63n(int64(cap) + 1))
}
```

**Python with tenacity (full jitter):**

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=0.1, max=10),  # Full jitter built-in
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def fetch_user_profile(user_id: str) -> dict:
    ...
```

**Retry budget rules:**

| Rule                                    | Rationale                                                   |
| --------------------------------------- | ----------------------------------------------------------- |
| Retry only idempotent operations        | POST/charge endpoints must not be retried without dedup     |
| Set total deadline < caller SLA         | Prevents cascading deadline violations up the call chain    |
| Do not retry 400-class errors           | Client errors are deterministic — retrying wastes resources |
| Propagate original error on final retry | Preserves root cause for observability                      |

### Fallback Handlers and Graceful Degradation

**Fallback priority order:**

```
1. Real-time call (circuit closed)
2. Local in-process cache (stale data acceptable)
3. Redis shared cache with TTL
4. Static default / empty response
5. User-visible degraded mode (feature disabled message)
```

**Go example with tiered fallback:**

```go
func (s *ProductService) GetRecommendations(ctx context.Context, userID string) ([]Product, error) {
    products, err := s.breaker.Execute(ctx, func(ctx context.Context) error {
        var rerr error
        products, rerr = s.recommendationsClient.Get(ctx, userID)
        return rerr
    })

    if err == nil {
        _ = s.cache.Set(ctx, cacheKey(userID), products, 5*time.Minute)
        return products, nil
    }

    // Fallback 1: local cache
    if cached, ok := s.localCache.Get(cacheKey(userID)); ok {
        return cached.([]Product), nil
    }

    // Fallback 2: shared Redis cache (stale allowed)
    if cached, rerr := s.cache.Get(ctx, cacheKey(userID)); rerr == nil {
        return cached, nil
    }

    // Fallback 3: popular items (static default)
    return s.popularItems, nil
}
```

### Bulkhead Pattern

Bulkheads prevent one dependency from exhausting resources shared by all dependencies. Implement as separate semaphore pools per upstream:

```go
type BulkheadExecutor struct {
    semaphore chan struct{}
    timeout   time.Duration
}

func NewBulkhead(maxConcurrent int, timeout time.Duration) *BulkheadExecutor {
    return &BulkheadExecutor{
        semaphore: make(chan struct{}, maxConcurrent),
        timeout:   timeout,
    }
}

func (b *BulkheadExecutor) Execute(ctx context.Context, fn func() error) error {
    ctx, cancel := context.WithTimeout(ctx, b.timeout)
    defer cancel()

    select {
    case b.semaphore <- struct{}{}: // acquire slot
        defer func() { <-b.semaphore }()
        return fn()
    case <-ctx.Done():
        return fmt.Errorf("bulkhead: concurrency limit exceeded: %w", ctx.Err())
    }
}
```

**Bulkhead sizing guideline:**

| Upstream Type             | Max Concurrent | Timeout |
| ------------------------- | -------------- | ------- |
| Critical (auth, payment)  | 50             | 2s      |
| Core (product, inventory) | 100            | 3s      |
| Optional (analytics, ads) | 20             | 500ms   |
| External third-party      | 10             | 5s      |

### Timeout Policy Design

**Two-tier timeout model:**

```
Caller SLA: 5s
  └─ Service total deadline: 4s
       ├─ DB query:    500ms
       ├─ Cache read:  100ms
       └─ RPC call:    2s (per-try 600ms × 3 attempts)
```

**Context propagation in Go (deadline-aware):**

```go
// Always derive from incoming context — never use context.Background() for outbound calls
func (s *OrderService) ProcessOrder(ctx context.Context, order Order) error {
    // Outbound call: inherits deadline from parent ctx automatically
    user, err := s.userClient.Get(ctx, order.UserID)
    if err != nil {
        return fmt.Errorf("get user: %w", err)
    }

    // Tighter deadline for a non-critical enrichment call
    enrichCtx, cancel := context.WithTimeout(ctx, 200*time.Millisecond)
    defer cancel()
    metadata, _ := s.metadataClient.Enrich(enrichCtx, order.ID) // non-blocking failure

    return s.store.Save(ctx, order, user, metadata)
}
```

### Observability Integration

Instrument every resilience boundary. Metrics to emit:

| Metric                        | Type      | Labels                                 |
| ----------------------------- | --------- | -------------------------------------- |
| `circuit_breaker_state`       | Gauge     | `dependency`, `state`                  |
| `circuit_breaker_transitions` | Counter   | `dependency`, `from_state`, `to_state` |
| `retry_attempt_total`         | Counter   | `dependency`, `attempt`, `outcome`     |
| `fallback_activated_total`    | Counter   | `dependency`, `fallback_tier`          |
| `bulkhead_rejected_total`     | Counter   | `dependency`                           |
| `bulkhead_queue_depth`        | Histogram | `dependency`                           |

**Prometheus registration example (Go):**

```go
var (
    circuitState = prometheus.NewGaugeVec(prometheus.GaugeOpts{
        Name: "circuit_breaker_state",
        Help: "Current state of circuit breaker (0=closed, 1=open, 2=half-open)",
    }, []string{"dependency"})

    retryTotal = prometheus.NewCounterVec(prometheus.CounterOpts{
        Name: "retry_attempt_total",
        Help: "Total retry attempts by dependency, attempt number, and outcome",
    }, []string{"dependency", "attempt", "outcome"})
)
```

**Alerting rules:**

```yaml
# Alert when a circuit has been open for > 2 minutes
- alert: CircuitBreakerOpenTooLong
  expr: circuit_breaker_state{state="open"} > 0 for 2m
  labels:
    severity: warning
  annotations:
    summary: "Circuit breaker open for {{ $labels.dependency }}"

# Alert when retry rate is high (indicates systemic instability)
- alert: HighRetryRate
  expr: rate(retry_attempt_total{attempt!="0"}[5m]) > 0.1
  labels:
    severity: warning
```

## Pipeline Integration

**Stage 3 (UML Engineering Package):** Architecture Decision Record required for resilience topology — which dependencies get circuit breakers, which get bulkheads, retry budget per service. ADR documents the chosen libraries (`pybreaker`, hand-rolled Go, Resilience4j) and timeout budget allocation tree.

**Stage 5 (Development):** Implement circuit breakers before integration testing begins. All outbound service calls must be wrapped. Retry logic must be reviewed against idempotency guarantees documented in Stage 3. Fallback tiers must be tested independently.

**Stage 6 (Architecture & Conformance Review):** Review checklist — (1) Every external/third-party call has a circuit breaker; (2) Retry config includes jitter; (3) No retry on non-idempotent operations without dedup key; (4) Bulkhead pools sized per upstream criticality; (5) All resilience boundaries emit Prometheus metrics; (6) Fallback behavior is tested, not assumed.

**Stage 7 (Automated Testing):** Chaos tests validate circuit breaker transitions. Fault injection (WireMock, Toxiproxy) tests retry behavior and fallback activation. Load tests verify bulkhead limits hold under concurrent traffic.

**Stage 8 (Integrity Verification):** Panel confirms no outbound call is unprotected. Trim-to-pass rule applies — removing resilience wrapping to pass performance benchmarks is a P0 defect.

## Quality Standards

| Metric                      | Target                            | Measurement                          |
| --------------------------- | --------------------------------- | ------------------------------------ |
| Circuit breaker coverage    | 100% of external dependencies     | Architecture review checklist        |
| Retry jitter implementation | Full jitter formula (not fixed)   | Code review                          |
| Fallback activation rate    | < 1% of requests in steady state  | `fallback_activated_total` counter   |
| Bulkhead rejection rate     | < 0.1% of requests                | `bulkhead_rejected_total` counter    |
| Mean time to circuit open   | < 10s from first failure spike    | `circuit_breaker_transitions` timing |
| Retry success rate          | > 80% of retried requests succeed | `retry_attempt_total` by outcome     |
| Timeout budget accuracy     | Service deadline < 80% of SLA     | Distributed tracing span durations   |
