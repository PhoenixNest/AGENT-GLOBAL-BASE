---
name: go-microservices
description: Design and implement Go-based microservices with idiomatic patterns — goroutine-safe concurrency, gRPC contracts, structured logging, and OpenTelemetry instrumentation — conforming to the company's backend architecture ADRs.
version: "1.0.0"
---

# Go Microservices

| Competency          | Description                                                          | Quality Criteria                                                                                                          |
| ------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Idiomatic Go        | Write Go code following effective Go principles and team style guide | Passes `golangci-lint` with zero errors; no goroutine leaks (verified with `goleak`); error wrapping with `fmt.Errorf %w` |
| gRPC Service Design | Define Protobuf schemas and implement gRPC server/client             | Proto definitions versioned in shared repo; all RPCs have deadline propagation; streaming RPCs use context cancellation   |
| Concurrency Safety  | Design goroutine-safe shared state and work queues                   | No data races (verified with `-race` flag in CI); all channels closed by sender; WaitGroup or errgroup used correctly     |
| Observability       | Instrument services with OpenTelemetry traces, metrics, and logs     | All service entry points create spans; RED metrics (Rate, Errors, Duration) exported to the observability platform        |

## Execution Guidance

### Microservice Structure

```
service/
├── cmd/server/main.go        # Entry point — config, DI, server start
├── internal/
│   ├── handler/              # gRPC/HTTP handlers (thin)
│   ├── service/              # Business logic
│   ├── repository/           # Data access
│   └── model/                # Domain types
├── proto/                    # Protobuf definitions
└── Makefile                  # build, test, lint, generate targets
```

### gRPC Deadline Propagation

Every outgoing gRPC call must propagate context with deadline:

```go
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()
resp, err := client.Method(ctx, req)
```

Never call gRPC methods with `context.Background()` — this disables deadline propagation and creates unbounded waits.
