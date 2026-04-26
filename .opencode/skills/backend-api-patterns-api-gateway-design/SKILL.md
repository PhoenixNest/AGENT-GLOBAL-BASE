---
name: backend-api-patterns-api-gateway-design
description: API gateway design and implementation for backend services — BFF pattern, rate limiting (token bucket, sliding window), mTLS termination, load balancing, health checks, and circuit breaker configuration at the edge. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 3 (Architecture) for gateway topology decisions and Stage 5 (Development) for gateway implementation. Trigger: api gateway, BFF pattern, rate limiting, mTLS, load balancing, circuit breaker, envoy, kong, edge routing.
prerequisites:
  - backend-api-patterns-distributed-backend-architecture

version: "1.0.0"
---

# API Gateway Design

**Category:** Backend Architecture
**Owner:** Backend Chapter Lead (Dev Malhotra)

## Overview

Designs and implements API gateway patterns that serve as the single entry point for all client traffic, providing routing, rate limiting, authentication termination, load balancing, and resilience at the edge. Covers BFF (Backend-for-Frontend) pattern implementation, gateway-level circuit breakers, and mTLS termination with downstream service propagation.

## Competency Dimensions

| Dimension               | Description                                                          | Proficiency Indicators                                                                                                                    |
| ----------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Gateway Patterns        | BFF, aggregator, proxy, gateway routing strategies                   | Selects appropriate gateway topology per client type; implements route matching with path rewriting and header manipulation               |
| Rate Limiting           | Token bucket, sliding window, leaky bucket algorithms                | Implements multi-tier rate limiting (global, per-tenant, per-user); configures burst allowances based on traffic analysis                 |
| mTLS & Security         | Mutual TLS termination, certificate rotation, downstream propagation | Configures mTLS termination at gateway with automatic cert rotation via cert-manager; propagates client identity to downstream services   |
| Load Balancing          | Round-robin, least-connections, weighted, consistent hashing         | Selects LB algorithm based on workload characteristics; implements health-aware load balancing with active health checks                  |
| Health Checks           | Active/passive probes, readiness/liveness differentiation            | Configures active health checks at gateway level with configurable intervals; implements passive health checks that detect slow responses |
| Gateway Circuit Breaker | Fault tolerance at edge, bulkhead isolation, retry policies          | Implements circuit breaker per upstream service; configures retry with jitter to prevent thundering herd                                  |

## Execution Guidance

### Gateway Pattern Selection

| Pattern                        | Use Case                                 | Pros                                    | Cons                                   |
| ------------------------------ | ---------------------------------------- | --------------------------------------- | -------------------------------------- |
| **Single Gateway**             | Small teams, unified API surface         | Simple deployment, consistent policy    | Single point of failure, team coupling |
| **BFF (Backend-for-Frontend)** | Multiple client types (web, mobile, IoT) | Client-optimized APIs, team autonomy    | Code duplication, more infrastructure  |
| **Gateway per Domain**         | Large org, domain-aligned teams          | Team ownership, independent scaling     | Cross-domain routing complexity        |
| **Aggregator Gateway**         | Legacy migration, facade pattern         | Shields clients from backend complexity | Bottleneck risk, tight coupling        |

**Decision framework:** Start with single gateway. Split to BFF when client requirements diverge significantly (e.g., mobile needs different response shapes than web). Split to gateway-per-domain when team count exceeds Dunbar's number (~150) for a single gateway codebase.

### Rate Limiting Implementation

**Token Bucket Algorithm** (Kong/Envoy configuration):

```yaml
# Envoy rate limit configuration
rate_limits:
  - actions:
      - remote_address: {} # Per-IP
      - request_headers:
          header_name: "x-api-key"
          descriptor_key: "api_key"
  - actions:
      - generic_key:
          descriptor_value: "global" # Global limit

# Token bucket parameters
token_bucket:
  max_tokens: 1000 # Burst capacity
  tokens_per_fill: 100 # Refill amount
  fill_interval: 60s # Refill period
```

**Sliding Window Log** (Redis-based, for precise limiting):

```go
type SlidingWindowLimiter struct {
    redis    *redis.Client
    key      string
    limit    int
    window   time.Duration
}

func (l *SlidingWindowLimiter) Allow(ctx context.Context, identifier string) (bool, error) {
    key := fmt.Sprintf("ratelimit:%s", identifier)
    now := time.Now().UnixNano()
    windowStart := now - l.window.Nanoseconds()

    pipe := l.redis.Pipeline()
    // Remove expired entries
    pipe.ZRemRangeByScore(ctx, key, "0", strconv.FormatInt(windowStart, 10))
    // Count current window
    pipe.ZCard(ctx, key)
    // Add current request
    pipe.ZAdd(ctx, key, redis.Z{Score: float64(now), Member: now})
    // Set TTL for key expiration
    pipe.Expire(ctx, key, l.window*2)

    results, err := pipe.Exec(ctx)
    if err != nil {
        return false, err
    }

    count := results[1].(*redis.IntCmd).Val()
    return count < int64(l.limit), nil
}
```

**Multi-tier rate limiting strategy:**

| Tier         | Scope             | Limit        | Rationale                           |
| ------------ | ----------------- | ------------ | ----------------------------------- |
| Global       | All traffic       | 50,000 req/s | Protects infrastructure capacity    |
| Per-tenant   | Organization      | 10,000 req/s | Fair usage, prevents noisy neighbor |
| Per-user     | Individual user   | 1,000 req/s  | Abuse prevention                    |
| Per-endpoint | Specific resource | Varies       | Protects expensive operations       |

### mTLS Configuration

**Gateway-side mTLS termination (Envoy/Istio):**

```yaml
# istio DestinationRule for mTLS
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service-mtls
spec:
  host: payment-service.default.svc.cluster.local
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
    connectionPool:
      tcp:
        maxConnections: 1000
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 1024
        http2MaxRequests: 1024
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

**Certificate rotation via cert-manager:**

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: gateway-cert
  namespace: istio-system
spec:
  secretName: gateway-tls
  duration: 720h # 30 days
  renewBefore: 360h # 15 days before expiry
  issuerRef:
    name: internal-ca
    kind: ClusterIssuer
  dnsNames:
    - api.company.com
    - "*.internal.company.com"
```

**Downstream identity propagation:** After mTLS termination, the gateway extracts the client certificate subject and propagates it via `X-Client-Cert-Subject` header to downstream services. Services must validate this header only comes from the trusted gateway (enforced by network policy).

### Load Balancing Strategies

| Algorithm            | Best For                                     | Configuration                         |
| -------------------- | -------------------------------------------- | ------------------------------------- |
| Round Robin          | Uniform request cost, stateless services     | Default in most LBs                   |
| Least Connections    | Variable request duration, stateful services | Track active connections per upstream |
| Weighted Round Robin | Heterogeneous upstream capacity              | Assign weights based on instance size |
| Consistent Hashing   | Session affinity, cache locality             | Hash on user ID or session token      |
| Power of Two Choices | Large upstream sets, low overhead            | Randomly pick 2, select least-loaded  |

**Active health check configuration:**

```yaml
# Envoy cluster health check
health_checks:
  - timeout: 5s
    interval: 10s
    unhealthy_threshold: 3
    healthy_threshold: 2
    http_health_check:
      path: "/healthz"
      expected_statuses:
        - start: 200
          end: 299
    # Passive detection: eject after 5 consecutive 5xx
    outlier_detection:
      consecutive_gateway_failure: 5
      interval: 30s
      base_ejection_time: 30s
      max_ejection_percent: 50
```

### Gateway-Level Circuit Breaker

```yaml
# Kong circuit breaker plugin
plugins:
  - name: circuit-breaker
    config:
      timeouts:
        - 5000 # 5s timeout before counting as failure
      window_size: 60 # 60-second sliding window
      failure_threshold: 50 # 50% failure rate opens circuit
      recovery_timeout: 30 # 30s before half-open
      minimum_hits: 10 # Minimum requests before evaluating
      fallback:
        status_code: 503
        content_type: application/json
        body: '{"error":"service_unavailable","retry_after":30}'
```

**Retry policy with jitter (prevents thundering herd):**

```yaml
# Envoy retry configuration
retry_policy:
  retry_on: "5xx,reset,connect-failure,retriable-4xx"
  num_retries: 3
  per_try_timeout: 2s
  retry_host_predicate:
    - name: envoy.retry_host_predicates.previous_hosts
  host_selection_retry_max_attempts: 5
  retriable_request_headers:
    - name: ":method"
      string_match:
        exact: "GET"
  # Jitter: base_interval + random(0, base_interval)
  retry_back_off:
    base_interval: 100ms
    max_interval: 1s
```

## Pipeline Integration

**Stage 3 (UML Engineering Package):** Component diagrams must show gateway topology, routing rules, and upstream service boundaries. ADR required for gateway technology selection (Envoy, Kong, custom).

**Stage 4 (Implementation Plan):** Gateway configuration is a critical path item. Rate limiting thresholds require product input (quotas per tier). mTLS certificate infrastructure must be provisioned before Stage 5.

**Stage 5 (Development):** Gateway deployed first, then upstream services. Health check endpoints implemented in all services. Load balancer configurations validated against actual service capacity.

**Stage 6 (Code Review):** Review gateway routing rules for completeness, rate limiting configuration for fairness, mTLS chain for certificate validity, and circuit breaker settings for alignment with SLOs.

**Stage 7 (Testing):** Load testing validates rate limiting behavior. Chaos testing validates circuit breaker and retry logic. Security testing validates mTLS enforcement and certificate rotation.

**Stage 8 (Integrity Verification):** Panel verifies gateway configuration matches architecture — all routes defined, rate limits aligned with product tiers, mTLS enforced end-to-end, circuit breakers configured for all upstream services.

## Quality Standards

| Metric                       | Target                                 | Measurement                  |
| ---------------------------- | -------------------------------------- | ---------------------------- |
| Gateway availability         | 99.99%                                 | Load balancer health metrics |
| Rate limiting accuracy       | 99.9% of requests correctly classified | Rate limiter audit logs      |
| mTLS coverage                | 100% of upstream services              | Certificate inventory audit  |
| Circuit breaker coverage     | 100% of external dependencies          | Architecture review          |
| P99 gateway latency overhead | < 10ms                                 | Gateway-side tracing         |
| Health check detection time  | < 15s for upstream failure             | Health check monitoring      |
| Certificate rotation success | 100% automated, zero downtime          | cert-manager logs            |
| Load balancer efficiency     | < 5% request distribution variance     | LB metrics dashboard         |
