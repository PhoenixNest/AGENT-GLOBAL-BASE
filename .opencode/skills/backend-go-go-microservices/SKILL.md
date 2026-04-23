---
name: backend-go-go-microservices
description: 'Backend skill: Go Microservices'
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

## Inter-Service Communication

### Communication Patterns

```
┌─────────────┐         ┌─────────────┐
│   Service A │  gRPC   │   Service B │
│             │ ──────> │             │
│  (Client)   │  sync   │  (Server)   │
└─────────────┘         └─────────────┘

┌─────────────┐         ┌──────────────┐        ┌─────────────┐
│   Service A │  Publish │  Message Bus │ Subscribe │ Service B │
│             │ ──────> │ (NATS/Rabbit) │ ──────> │             │
└─────────────┘         └──────────────┘        └─────────────┘
```

### gRPC Service Definition

```protobuf
// proto/order/v1/order.proto
syntax = "proto3";
package order.v1;
option go_package = "github.com/company/orderservices/proto/order/v1";

service OrderService {
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);
  rpc GetOrder(GetOrderRequest) returns (GetOrderResponse);
  rpc ListOrders(ListOrdersRequest) returns (stream Order);
  rpc StreamOrderStatus(StreamOrderStatusRequest) returns (stream OrderStatusUpdate);
}

message CreateOrderRequest {
  string user_id = 1;
  repeated OrderItem items = 2;
  PaymentMethod payment_method = 3;
}

message OrderItem {
  string product_id = 1;
  int32 quantity = 2;
  Money unit_price = 3;
}

message Money {
  string currency = 1;
  int64 amount_cents = 2;
}

message CreateOrderResponse {
  string order_id = 1;
  OrderStatus status = 2;
  string payment_intent_id = 3;
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
  ORDER_STATUS_SHIPPED = 3;
  ORDER_STATUS_DELIVERED = 4;
  ORDER_STATUS_CANCELLED = 5;
}
```

### gRPC Server Implementation

```go
// cmd/server/main.go
package main

import (
    "context"
    "fmt"
    "log"
    "net"

    "github.com/company/orderservices/internal/handler"
    "github.com/company/orderservices/internal/service"
    "github.com/company/orderservices/internal/repository"
    pb "github.com/company/orderservices/proto/order/v1"
    "go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc"
    "google.golang.org/grpc"
    "google.golang.org/grpc/health"
    healthpb "google.golang.org/grpc/health/grpc_health_v1"
    "google.golang.org/grpc/reflection"
)

func main() {
    // Database connection
    db, err := repository.NewPostgresDB()
    if err != nil {
        log.Fatalf("failed to connect to database: %v", err)
    }
    defer db.Close()

    // Service layer
    orderService := service.NewOrderService(db)

    // gRPC handlers
    orderHandler := handler.NewOrderHandler(orderService)

    // gRPC server with OpenTelemetry interceptor
    server := grpc.NewServer(
        grpc.StatsHandler(otelgrpc.NewServerHandler()),
        grpc.ChainUnaryInterceptor(
            recoveryInterceptor,
            loggingInterceptor,
            authInterceptor,
        ),
    )

    // Register services
    pb.RegisterOrderServiceServer(server, orderHandler)

    // Health check
    healthChecker := health.NewServer()
    healthpb.RegisterHealthServer(server, healthChecker)
    healthChecker.SetServingStatus("order-service", healthpb.HealthCheckResponse_SERVING)

    // Reflection for development (disable in production)
    reflection.Register(server)

    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }

    log.Printf("order-service starting on :50051")
    if err := server.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

### gRPC Client with Connection Pooling

```go
// internal/client/grpc_client.go
package client

import (
    "context"
    "time"

    pb "github.com/company/orderservices/proto/payment/v1"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/keepalive"
)

type PaymentClient struct {
    conn   *grpc.ClientConn
    client pb.PaymentServiceClient
}

func NewPaymentClient(addr string) (*PaymentClient, error) {
    kacp := keepalive.ClientParameters{
        Time:                10 * time.Second,
        Timeout:             time.Second,
        PermitWithoutStream: true,
    }

    conn, err := grpc.NewClient(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithKeepaliveParams(kacp),
        grpc.WithDefaultCallOptions(
            grpc.MaxCallRecvMsgSize(4*1024*1024), // 4MB
            grpc.MaxCallSendMsgSize(4*1024*1024),
        ),
        grpc.WithStatsHandler(otelgrpc.NewClientHandler()),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to dial payment service: %w", err)
    }

    return &PaymentClient{
        conn:   conn,
        client: pb.NewPaymentServiceClient(conn),
    }, nil
}

func (c *PaymentClient) Close() error {
    return c.conn.Close()
}

func (c *PaymentClient) ProcessPayment(ctx context.Context, req *pb.PaymentRequest) (*pb.PaymentResponse, error) {
    // Add timeout to prevent hanging calls
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    return c.client.ProcessPayment(ctx, req)
}
```

### Async Messaging with NATS

```go
// internal/eventbus/nats_bus.go
package eventbus

import (
    "context"
    "encoding/json"
    "fmt"
    "log"

    "github.com/nats-io/nats.go"
)

type NATSBus struct {
    conn *nats.Conn
}

func NewNATSBus(url string) (*NATSBus, error) {
    conn, err := nats.Connect(url,
        nats.MaxReconnects(-1),
        nats.ReconnectWait(time.Second),
        nats.DisconnectErrHandler(func(nc *nats.Conn, err error) {
            log.Printf("NATS disconnected (error): %v", err)
        }),
        nats.ReconnectHandler(func(nc *nats.Conn) {
            log.Printf("NATS reconnected to %s", nc.ConnectedUrl())
        }),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to NATS: %w", err)
    }

    return &NATSBus{conn: conn}, nil
}

func (b *NATSBus) Publish(ctx context.Context, subject string, payload interface{}) error {
    data, err := json.Marshal(payload)
    if err != nil {
        return fmt.Errorf("marshal error: %w", err)
    }

    msg := &nats.Msg{
        Subject: subject,
        Data:    data,
        Header:  make(nats.Header),
    }

    // Propagate trace context
    if span := trace.SpanFromContext(ctx); span.SpanContext().IsValid() {
        msg.Header.Set("traceparent", propagateTraceContext(span))
    }

    return b.conn.PublishMsg(msg)
}

func (b *NATSBus) Subscribe(ctx context.Context, subject string, handler func(context.Context, []byte) error) error {
    _, err := b.conn.Subscribe(subject, func(msg *nats.Msg) {
        childCtx := extractTraceContext(msg.Header)
        if err := handler(childCtx, msg.Data); err != nil {
            log.Printf("handler error for subject %s: %v", subject, err)
            // NATS JetStream will redeliver on error
        }
    })
    return err
}
```

### REST API Fallback Pattern

```go
// internal/handler/rest_handler.go
package handler

import (
    "encoding/json"
    "net/http"

    pb "github.com/company/orderservices/proto/order/v1"
)

type RESTHandler struct {
    grpcClient pb.OrderServiceClient
}

// Provide REST endpoints alongside gRPC for external consumers
func (h *RESTHandler) GetOrder(w http.ResponseWriter, r *http.Request) {
    orderID := r.PathValue("id")

    resp, err := h.grpcClient.GetOrder(r.Context(), &pb.GetOrderRequest{
        OrderId: orderID,
    })
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}
```

---

## Service Discovery

### Consul-Based Service Discovery

```go
// internal/discovery/consul.go
package discovery

import (
    "fmt"
    "log"
    "net"
    "strconv"

    consul "github.com/hashicorp/consul/api"
)

type ConsulDiscovery struct {
    client *consul.Client
    serviceID string
}

func NewConsulDiscovery(config *consul.Config, serviceName string) (*ConsulDiscovery, error) {
    client, err := consul.NewClient(config)
    if err != nil {
        return nil, fmt.Errorf("consul client error: %w", err)
    }

    return &ConsulDiscovery{
        client:    client,
        serviceID: serviceName,
    }, nil
}

func (d *ConsulDiscovery) Register(name string, port int, tags []string) error {
    registration := &consul.AgentServiceRegistration{
        ID:      fmt.Sprintf("%s-%s", name, generateID()),
        Name:    name,
        Port:    port,
        Tags:    tags,
        Check: &consul.AgentServiceCheck{
            GRPC:                           fmt.Sprintf("localhost:%d", port),
            GRPCUseTLS:                    false,
            Timeout:                       "3s",
            Interval:                      "10s",
            DeregisterCriticalServiceAfter: "90s",
        },
    }

    return d.client.Agent().ServiceRegister(registration)
}

func (d *ConsulDiscovery) Discover(serviceName string) ([]ServiceInstance, error) {
    entries, _, err := d.client.Health().Service(serviceName, "", true, nil)
    if err != nil {
        return nil, fmt.Errorf("service discovery error: %w", err)
    }

    var instances []ServiceInstance
    for _, entry := range entries {
        instances = append(instances, ServiceInstance{
            ID:      entry.Service.ID,
            Address: entry.Service.Address,
            Port:    entry.Service.Port,
            Tags:    entry.Service.Tags,
        })
    }

    return instances, nil
}
```

### Kubernetes DNS Discovery

```yaml
# k8s/order-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: production
spec:
  selector:
    app: order-service
  ports:
    - name: grpc
      port: 50051
      targetPort: 50051
    - name: http
      port: 8080
      targetPort: 8080
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.2.3
          ports:
            - containerPort: 50051
              name: grpc
            - containerPort: 8080
              name: http
          readinessProbe:
            grpc:
              port: 50051
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            grpc:
              port: 50051
            initialDelaySeconds: 15
            periodSeconds: 20
          env:
            - name: PAYMENT_SERVICE_ADDR
              value: 'payment-service.production.svc.cluster.local:50052'
            - name: USER_SERVICE_ADDR
              value: 'user-service.production.svc.cluster.local:50053'
```

### API Gateway Routing

```yaml
# k8s/gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: api-gateway
  namespace: production
spec:
  gatewayClassName: istio
  listeners:
    - name: grpc
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - name: gateway-tls-cert
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: order-routing
  namespace: production
spec:
  parentRefs:
    - name: api-gateway
  hostnames:
    - 'api.company.com'
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /order.v1.OrderService
      backendRefs:
        - name: order-service
          port: 50051
    - matches:
        - path:
            type: PathPrefix
            value: /payment.v1.PaymentService
      backendRefs:
        - name: payment-service
          port: 50052
```

---

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

## Distributed Tracing

### OpenTelemetry Setup

```go
// internal/tracing/otel.go
package tracing

import (
    "context"
    "fmt"
    "time"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/propagation"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
)

func InitTracer(ctx context.Context, serviceName, serviceVersion string) (*sdktrace.TracerProvider, error) {
    exporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, fmt.Errorf("create OTLP exporter: %w", err)
    }

    res, err := resource.New(ctx,
        resource.WithAttributes(
            semconv.ServiceName(serviceName),
            semconv.ServiceVersion(serviceVersion),
            semconv.DeploymentEnvironment(getEnv("ENVIRONMENT", "development")),
        ),
    )
    if err != nil {
        return nil, fmt.Errorf("create resource: %w", err)
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter,
            sdktrace.WithBatchTimeout(time.Second),
            sdktrace.WithMaxExportBatchSize(512),
        ),
        sdktrace.WithResource(res),
        sdktrace.WithSampler(sdktrace.ParentBased(sdktrace.TraceIDRatioBased(0.1))),
    )

    otel.SetTracerProvider(tp)
    otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
        propagation.TraceContext{},
        propagation.Baggage{},
    ))

    return tp, nil
}
```

### Custom Span Creation

```go
// internal/service/order_service.go
package service

import (
    "context"
    "fmt"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/codes"
)

var tracer = otel.Tracer("order-service")

func (s *OrderService) CreateOrder(ctx context.Context, req *CreateOrderRequest) (*Order, error) {
    ctx, span := tracer.Start(ctx, "OrderService.CreateOrder")
    defer span.End()

    span.SetAttributes(
        attribute.String("user.id", req.UserID),
        attribute.Int("order.items_count", len(req.Items)),
    )

    // Validate order
    if err := s.validateOrder(ctx, req); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, "validation failed")
        return nil, err
    }

    // Create order in database
    order, err := s.orderRepo.Create(ctx, req)
    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, "database write failed")
        return nil, err
    }

    span.SetAttributes(attribute.String("order.id", order.ID))

    // Process payment (external service call)
    _, err = s.paymentClient.ProcessPayment(ctx, &PaymentRequest{
        OrderID: order.ID,
        Amount:  order.Total,
    })
    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, "payment processing failed")
        // Compensating transaction: cancel the order
        s.orderRepo.Cancel(ctx, order.ID)
        return nil, err
    }

    // Publish order created event
    s.eventBus.Publish(ctx, "order.created", order)

    span.SetStatus(codes.Ok, "order created successfully")
    return order, nil
}
```

### Jaeger Integration

```yaml
# docker-compose.jaeger.yml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - '16686:16686' # UI
      - '4317:4317' # OTLP gRPC
      - '4318:4318' # OTLP HTTP
    environment:
      - COLLECTOR_OTLP_ENABLED=true

  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    ports:
      - '4317:4317'
      - '4318:4318'
    volumes:
      - ./otel-collector-config.yaml:/etc/otel/config.yaml
    command: ['--config', '/etc/otel/config.yaml']
    depends_on:
      - jaeger
```

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/jaeger]
```

---

## Configuration Management

### Environment-Based Configuration

```go
// internal/config/config.go
package config

import (
    "fmt"
    "os"
    "strconv"
    "time"
)

type Config struct {
    Server   ServerConfig
    Database DatabaseConfig
    GRPC     GRPCConfig
    Tracing  TracingConfig
}

type ServerConfig struct {
    Port         int
    ReadTimeout  time.Duration
    WriteTimeout time.Duration
}

type DatabaseConfig struct {
    Host            string
    Port            int
    User            string
    Password        string // Injected via secret management
    Database        string
    MaxOpenConns    int
    MaxIdleConns    int
    ConnMaxLifetime time.Duration
}

type GRPCConfig struct {
    Port             int
    MaxRecvMsgSize   int
    MaxSendMsgSize   int
    KeepaliveTime    time.Duration
}

type TracingConfig struct {
    Enabled       bool
    Endpoint      string
    SampleRate    float64
}

func Load() (*Config, error) {
    cfg := &Config{
        Server: ServerConfig{
            Port:         getEnvInt("SERVER_PORT", 8080),
            ReadTimeout:  getEnvDuration("SERVER_READ_TIMEOUT", 5*time.Second),
            WriteTimeout: getEnvDuration("SERVER_WRITE_TIMEOUT", 10*time.Second),
        },
        Database: DatabaseConfig{
            Host:            getEnv("DB_HOST", "localhost"),
            Port:            getEnvInt("DB_PORT", 5432),
            User:            getEnv("DB_USER", "postgres"),
            Password:        getEnv("DB_PASSWORD", ""),
            Database:        getEnv("DB_NAME", "orders"),
            MaxOpenConns:    getEnvInt("DB_MAX_OPEN_CONNS", 25),
            MaxIdleConns:    getEnvInt("DB_MAX_IDLE_CONNS", 5),
            ConnMaxLifetime: getEnvDuration("DB_CONN_MAX_LIFETIME", 5*time.Minute),
        },
        GRPC: GRPCConfig{
            Port:           getEnvInt("GRPC_PORT", 50051),
            MaxRecvMsgSize: getEnvInt("GRPC_MAX_RECV_MSG_SIZE", 4*1024*1024),
            MaxSendMsgSize: getEnvInt("GRPC_MAX_SEND_MSG_SIZE", 4*1024*1024),
            KeepaliveTime:  getEnvDuration("GRPC_KEEPALIVE_TIME", 10*time.Second),
        },
        Tracing: TracingConfig{
            Enabled:    getEnvBool("TRACING_ENABLED", true),
            Endpoint:   getEnv("TRACING_ENDPOINT", "otel-collector:4317"),
            SampleRate: getEnvFloat64("TRACING_SAMPLE_RATE", 0.1),
        },
    }

    return cfg, cfg.Validate()
}

func (c *Config) Validate() error {
    if c.Database.Password == "" {
        return fmt.Errorf("DB_PASSWORD is required")
    }
    if c.Server.Port <= 0 || c.Server.Port > 65535 {
        return fmt.Errorf("SERVER_PORT must be between 1 and 65535")
    }
    return nil
}

// Helper functions
func getEnv(key, fallback string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return fallback
}

func getEnvInt(key string, fallback int) int {
    if v := os.Getenv(key); v != "" {
        if n, err := strconv.Atoi(v); err == nil {
            return n
        }
    }
    return fallback
}

func getEnvBool(key string, fallback bool) bool {
    if v := os.Getenv(key); v != "" {
        if b, err := strconv.ParseBool(v); err == nil {
            return b
        }
    }
    return fallback
}

func getEnvDuration(key string, fallback time.Duration) time.Duration {
    if v := os.Getenv(key); v != "" {
        if d, err := time.ParseDuration(v); err == nil {
            return d
        }
    }
    return fallback
}

func getEnvFloat64(key string, fallback float64) float64 {
    if v := os.Getenv(key); v != "" {
        if f, err := strconv.ParseFloat(v, 64); err == nil {
            return f
        }
    }
    return fallback
}
```

### Kubernetes Secret Injection

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: order-service-secrets
  namespace: production
type: Opaque
data:
  db-password: <base64-encoded-password>
  api-key: <base64-encoded-api-key>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  template:
    spec:
      containers:
        - name: order-service
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: order-service-secrets
                  key: db-password
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: order-service-secrets
                  key: api-key
```

---

## Deployment Patterns

### Blue-Green Deployment

```yaml
# k8s/blue-green.yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service-active
spec:
  selector:
    app: order-service
    track: active
  ports:
    - port: 50051
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
      track: active
  template:
    metadata:
      labels:
        app: order-service
        track: active
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.2.3
---
# Green deployment (new version, not receiving traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
      track: preview
  template:
    metadata:
      labels:
        app: order-service
        track: preview
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.3.0
```

**Switch traffic:**

```bash
kubectl patch service order-service-active \
  -p '{"spec":{"selector":{"track":"preview"}}}'
```

### Canary Deployment

```yaml
# k8s/canary.yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
    - port: 50051
---
# Stable version (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
        version: stable
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.2.3
---
# Canary version (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
        version: canary
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.3.0
```

### Feature Flags

```go
// internal/featureflags/flags.go
package featureflags

import (
    "context"
    "sync"
)

type FeatureFlags struct {
    mu     sync.RWMutex
    flags  map[string]bool
    watchers []func(flag string, enabled bool)
}

func NewFeatureFlags() *FeatureFlags {
    return &FeatureFlags{
        flags: make(map[string]bool),
    }
}

func (ff *FeatureFlags) IsEnabled(flag string) bool {
    ff.mu.RLock()
    defer ff.mu.RUnlock()
    return ff.flags[flag]
}

func (ff *FeatureFlags) Set(flag string, enabled bool) {
    ff.mu.Lock()
    ff.flags[flag] = enabled
    ff.mu.Unlock()

    // Notify watchers
    for _, w := range ff.watchers {
        w(flag, enabled)
    }
}

// Usage in handler
func (h *OrderHandler) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.CreateOrderResponse, error) {
    if h.flags.IsEnabled("new-payment-flow") {
        return h.createOrderWithNewPaymentFlow(ctx, req)
    }
    return h.createOrderWithLegacyPaymentFlow(ctx, req)
}
```

---

## Testing Strategies

### Contract Testing with Pact

```go
// tests/contract/order_service_test.go
package contract

import (
    "context"
    "testing"

    "github.com/company/orderservices/internal/handler"
    "github.com/company/orderservices/internal/service"
    pb "github.com/company/orderservices/proto/order/v1"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/test/bufconn"
)

func TestOrderServiceContract(t *testing.T) {
    // Setup in-memory gRPC server
    lis := bufconn.Listen(1024 * 1024)
    server := grpc.NewServer()

    // Use test doubles for dependencies
    orderService := service.NewOrderService(newTestDB())
    orderHandler := handler.NewOrderHandler(orderService)
    pb.RegisterOrderServiceServer(server, orderHandler)

    go server.Serve(lis)
    defer server.Stop()

    // Create client
    conn, err := grpc.NewClient("passthrough://bufnet",
        grpc.WithContextDialer(func(ctx context.Context, s string) (net.Conn, error) {
            return lis.Dial()
        }),
        grpc.WithTransportCredentials(insecure.NewCredentials()),
    )
    if err != nil {
        t.Fatalf("failed to connect: %v", err)
    }
    defer conn.Close()

    client := pb.NewOrderServiceClient(conn)

    // Test contract
    resp, err := client.CreateOrder(context.Background(), &pb.CreateOrderRequest{
        UserId: "user-123",
        Items: []*pb.OrderItem{
            {ProductId: "prod-1", Quantity: 2, UnitPrice: &pb.Money{Currency: "USD", AmountCents: 1999}},
        },
    })
    if err != nil {
        t.Fatalf("CreateOrder failed: %v", err)
    }

    if resp.OrderId == "" {
        t.Error("expected non-empty order_id")
    }
    if resp.Status != pb.OrderStatus_ORDER_STATUS_PENDING {
        t.Errorf("expected PENDING, got %v", resp.Status)
    }
}
```

### Integration Testing

```go
// tests/integration/order_service_test.go
package integration

import (
    "context"
    "testing"
    "time"

    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/wait"
)

func TestOrderServiceWithRealDatabase(t *testing.T) {
    ctx := context.Background()

    // Start PostgreSQL container
    pgContainer, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
        ContainerRequest: testcontainers.ContainerRequest{
            Image:        "postgres:15",
            ExposedPorts: []string{"5432/tcp"},
            Env: map[string]string{
                "POSTGRES_USER":     "test",
                "POSTGRES_PASSWORD": "test",
                "POSTGRES_DB":       "orders_test",
            },
            WaitingFor: wait.ForLog("database system is ready to accept connections"),
        },
        Started: true,
    })
    if err != nil {
        t.Fatalf("failed to start PostgreSQL: %v", err)
    }
    defer pgContainer.Terminate(ctx)

    // Get connection details
    port, _ := pgContainer.MappedPort(ctx, "5432")
    host, _ := pgContainer.Host(ctx)

    // Run tests against real database
    // ...
}
```

### Chaos Testing

```go
// tests/chaos/network_chaos_test.go
package chaos

import (
    "context"
    "testing"
    "time"

    "github.com/stretchr/testify/assert"
)

func TestOrderServiceUnderNetworkPartition(t *testing.T) {
    // Setup: Start all services
    // Introduce network partition between order-service and payment-service
    // Verify: order-service handles gracefully (circuit breaker opens)
    // Verify: requests are queued or rejected with appropriate error
    // Recover: Restore network connectivity
    // Verify: Circuit breaker transitions to half-open, then closed
}

func TestOrderServiceUnderHighLoad(t *testing.T) {
    // Setup: Start order-service with limited resources
    // Send 1000 concurrent requests
    // Verify: Service does not crash
    // Verify: Bulkhead limits concurrent requests
    // Verify: Response times degrade gracefully
    // Verify: No data corruption under concurrent writes
}
```

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

## References

### Related Skills

- `backend/go-api-design` — REST API design patterns in Go
- `backend/graphql` — GraphQL schema design and implementation
- `backend/api-patterns/websocket-scaling` — Real-time communication patterns
- `devops/kubernetes` — Container orchestration and deployment
- `security/service-security` — Microservice security best practices
- `testing-qa/contract-testing` — Service contract validation

### External Resources

- [gRPC Go Documentation](https://pkg.go.dev/google.golang.org/grpc)
- [OpenTelemetry Go SDK](https://opentelemetry.io/docs/instrumentation/go/)
- [HashiCorp Consul](https://developer.hashicorp.com/consul)
- [NATS Documentation](https://docs.nats.io/)
- [Circuit Breaker Pattern (Martin Fowler)](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Building Microservices (Sam Newman)](https://samnewman.io/books/building_microservices_2nd_edition/)
- [Go Clean Architecture](https://github.com/bxcodec/go-clean-arch)
- [Buf Protobuf Tooling](https://buf.build/)
