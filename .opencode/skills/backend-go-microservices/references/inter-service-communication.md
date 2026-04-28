# Inter-Service Communication

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
