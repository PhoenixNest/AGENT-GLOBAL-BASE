# Backpressure Handling

## Backpressure Handling

### Rate Limiting

```go
// internal/ratelimit/rate_limiter.go
package ratelimit

import (
    "sync"
    "time"
)

type TokenBucket struct {
    mu         sync.Mutex
    tokens     float64
    maxTokens  float64
    refillRate float64 // tokens per second
    lastRefill time.Time
}

func NewTokenBucket(maxTokens float64, refillRate float64) *TokenBucket {
    return &TokenBucket{
        tokens:     maxTokens,
        maxTokens:  maxTokens,
        refillRate: refillRate,
        lastRefill: time.Now(),
    }
}

func (tb *TokenBucket) Allow() bool {
    tb.mu.Lock()
    defer tb.mu.Unlock()

    now := time.Now()
    elapsed := now.Sub(tb.lastRefill).Seconds()
    tb.tokens = min(tb.maxTokens, tb.tokens+elapsed*tb.refillRate)
    tb.lastRefill = now

    if tb.tokens >= 1 {
        tb.tokens--
        return true
    }
    return false
}

// Per-client rate limiter registry
type ClientRateLimiter struct {
    mu       sync.RWMutex
    limiters map[string]*TokenBucket
    maxTokens float64
    refillRate float64
}

func NewClientRateLimiter(maxTokens, refillRate float64) *ClientRateLimiter {
    return &ClientRateLimiter{
        limiters:  make(map[string]*TokenBucket),
        maxTokens: maxTokens,
        refillRate: refillRate,
    }
}

func (rl *ClientRateLimiter) Allow(clientID string) bool {
    rl.mu.RLock()
    limiter, ok := rl.limiters[clientID]
    rl.mu.RUnlock()

    if !ok {
        rl.mu.Lock()
        limiter = NewTokenBucket(rl.maxTokens, rl.refillRate)
        rl.limiters[clientID] = limiter
        rl.mu.Unlock()
    }

    return limiter.Allow()
}
```

### Message Queuing with Consumer Lag Monitoring

```go
// internal/websocket/backpressure.go
package websocket

import (
    "sync/atomic"
    "time"
)

type BackpressureMonitor struct {
    // Per-client metrics
    droppedMessages atomic.Int64
    queueDepth      atomic.Int64
    lastMessageTime atomic.Int64
}

func (b *BackpressureMonitor) RecordEnqueue() {
    b.queueDepth.Add(1)
    b.lastMessageTime.Store(time.Now().UnixNano())
}

func (b *BackpressureMonitor) RecordDequeue() {
    b.queueDepth.Add(-1)
}

func (b *BackpressureMonitor) RecordDrop() {
    b.droppedMessages.Add(1)
}

func (b *BackpressureMonitor) GetQueueDepth() int64 {
    return b.queueDepth.Load()
}

func (b *BackpressureMonitor) GetDroppedMessages() int64 {
    return b.droppedMessages.Load()
}

// Check if client is healthy
func (b *BackpressureMonitor) IsHealthy() bool {
    depth := b.GetQueueDepth()
    dropped := b.GetDroppedMessages()

    // Unhealthy if queue depth > 500 or dropped > 100
    return depth < 500 && dropped < 100
}

// Adaptive message dropping
func (c *Client) SendWithBackpressure(data []byte) bool {
    if !c.backpressure.IsHealthy() {
        // Adaptive: reduce message frequency for unhealthy clients
        c.backpressure.RecordDrop()
        return false
    }

    select {
    case c.send <- data:
        c.backpressure.RecordEnqueue()
        return true
    default:
        c.backpressure.RecordDrop()
        return false
    }
}
```

---
