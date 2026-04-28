# Resilience Patterns

## Resilience Patterns

### Circuit Breaker Implementation

```go
// internal/resilience/circuit_breaker.go
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

type CircuitBreaker struct {
    mu sync.Mutex

    state           State
    failureCount    int
    successCount    int
    failureThreshold int
    successThreshold int
    timeout         time.Duration
    lastFailureTime time.Time

    // Metrics
    TotalRequests     int64
    SuccessfulRequests int64
    FailedRequests    int64
    RejectedRequests  int64
}

func NewCircuitBreaker(failureThreshold, successThreshold int, timeout time.Duration) *CircuitBreaker {
    return &CircuitBreaker{
        state:            StateClosed,
        failureThreshold: failureThreshold,
        successThreshold: successThreshold,
        timeout:          timeout,
    }
}

var ErrCircuitOpen = errors.New("circuit breaker is open")

func (cb *CircuitBreaker) Execute(ctx context.Context, fn func() error) error {
    cb.mu.Lock()

    switch cb.state {
    case StateOpen:
        if time.Since(cb.lastFailureTime) > cb.timeout {
            cb.state = StateHalfOpen
            cb.successCount = 0
        } else {
            cb.RejectedRequests++
            cb.mu.Unlock()
            return ErrCircuitOpen
        }
    case StateHalfOpen:
        // Allow one request through
    case StateClosed:
        // Allow request
    }

    cb.TotalRequests++
    cb.mu.Unlock()

    err := fn()

    cb.mu.Lock()
    defer cb.mu.Unlock()

    if err != nil {
        cb.FailedRequests++
        cb.failureCount++
        cb.lastFailureTime = time.Now()

        if cb.state == StateHalfOpen {
            cb.state = StateOpen
            return err
        }

        if cb.failureCount >= cb.failureThreshold {
            cb.state = StateOpen
        }
    } else {
        cb.SuccessfulRequests++

        if cb.state == StateHalfOpen {
            cb.successCount++
            if cb.successCount >= cb.successThreshold {
                cb.state = StateClosed
                cb.failureCount = 0
            }
        } else if cb.state == StateClosed {
            // Reset failure count on success
            cb.failureCount = 0
        }
    }

    return err
}

func (cb *CircuitBreaker) State() State {
    cb.mu.Lock()
    defer cb.mu.Unlock()
    return cb.state
}
```

### Retry with Exponential Backoff

```go
// internal/resilience/retry.go
package resilience

import (
    "context"
    "math"
    "math/rand"
    "time"
)

type RetryConfig struct {
    MaxAttempts      int
    InitialBackoff   time.Duration
    MaxBackoff       time.Duration
    Multiplier       float64
    Jitter           bool
    RetryableErrors  map[string]bool
}

func DefaultRetryConfig() RetryConfig {
    return RetryConfig{
        MaxAttempts:    3,
        InitialBackoff: 100 * time.Millisecond,
        MaxBackoff:     5 * time.Second,
        Multiplier:     2.0,
        Jitter:         true,
        RetryableErrors: map[string]bool{
            "UNAVAILABLE":        true,
            "DEADLINE_EXCEEDED":  true,
            "RESOURCE_EXHAUSTED": true,
        },
    }
}

func WithRetry(ctx context.Context, config RetryConfig, fn func(context.Context) error) error {
    var lastErr error

    for attempt := 0; attempt < config.MaxAttempts; attempt++ {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
        }

        lastErr = fn(ctx)
        if lastErr == nil {
            return nil
        }

        if !isRetryable(lastErr, config.RetryableErrors) {
            return lastErr
        }

        if attempt < config.MaxAttempts-1 {
            backoff := calculateBackoff(attempt, config)
            time.Sleep(backoff)
        }
    }

    return lastErr
}

func calculateBackoff(attempt int, config RetryConfig) time.Duration {
    backoff := float64(config.InitialBackoff) * math.Pow(config.Multiplier, float64(attempt))
    if config.Jitter {
        backoff = backoff * (0.5 + rand.Float64())
    }
    if backoff > float64(config.MaxBackoff) {
        backoff = float64(config.MaxBackoff)
    }
    return time.Duration(backoff)
}

func isRetryable(err error, retryableErrors map[string]bool) bool {
    // Check gRPC status codes or custom error types
    for code := range retryableErrors {
        if containsErrorCode(err, code) {
            return true
        }
    }
    return false
}
```

### Timeout and Bulkhead Patterns

```go
// internal/resilience/bulkhead.go
package resilience

import (
    "context"
    "errors"
    "sync"
)

var ErrBulkheadFull = errors.New("bulkhead: maximum concurrency reached")

type Bulkhead struct {
    mu       sync.Mutex
    sem      chan struct{}
    maxConcurrent int
}

func NewBulkhead(maxConcurrent int) *Bulkhead {
    return &Bulkhead{
        sem:           make(chan struct{}, maxConcurrent),
        maxConcurrent: maxConcurrent,
    }
}

func (b *Bulkhead) Execute(ctx context.Context, fn func() error) error {
    select {
    case b.sem <- struct{}{}:
        defer func() { <-b.sem }()
        return fn()
    case <-ctx.Done():
        return ctx.Err()
    default:
        return ErrBulkheadFull
    }
}

// Combined: Circuit Breaker + Bulkhead + Timeout
type ResilientClient struct {
    cb        *CircuitBreaker
    bulkhead  *Bulkhead
    timeout   time.Duration
}

func NewResilientClient(addr string) *ResilientClient {
    return &ResilientClient{
        cb:       NewCircuitBreaker(5, 3, 30*time.Second),
        bulkhead: NewBulkhead(100),
        timeout:  5 * time.Second,
    }
}

func (c *ResilientClient) Call(ctx context.Context, fn func(context.Context) error) error {
    ctx, cancel := context.WithTimeout(ctx, c.timeout)
    defer cancel()

    return c.cb.Execute(ctx, func() error {
        return c.bulkhead.Execute(ctx, func() error {
            return fn(ctx)
        })
    })
}
```

---
