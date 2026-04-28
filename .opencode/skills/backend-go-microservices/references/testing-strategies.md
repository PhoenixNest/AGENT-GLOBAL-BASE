# Testing Strategies

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
