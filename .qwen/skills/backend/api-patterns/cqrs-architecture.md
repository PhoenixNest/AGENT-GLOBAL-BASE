---
name: cqrs-architecture
description: Implements CQRS (Command Query Responsibility Segregation) architecture separating read and write models for high-performance backend systems, using event sourcing for write-side persistence and optimized read projections for query performance.
---

# CQRS Architecture — Command Query Responsibility Segregation

## 1. Overview

### Purpose

CQRS separates the **read** and **write** concerns of a system into distinct models. Instead of a single domain model handling both CRUD operations, CQRS maintains:

- **Command Model (Write Side):** Handles state mutations through explicit commands, enforcing business rules and invariants.
- **Query Model (Read Side):** Serves optimized read queries from pre-materialized views, denormalized for fast access.

```
┌──────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
└──────────────┬───────────────────────────┬───────────────────┘
               │ Commands                   │ Queries
               ▼                            ▼
┌──────────────────────────┐   ┌────────────────────────────────┐
│     Command Model         │   │       Query Model              │
│  ┌────────────────────┐  │   │  ┌──────────────────────────┐  │
│  │ Command Handlers   │  │   │  │ Read Model / Projections │  │
│  │ Aggregates         │  │   │  │ Materialized Views       │  │
│  │ Domain Events      │  │   │  │ Query Handlers           │  │
│  └────────┬───────────┘  │   │  └──────────▲───────────────┘  │
│           │               │   │             │                  │
│           ▼               │   │             │                  │
│  ┌────────────────────┐  │   │             │                  │
│  │ Event Store        │  │   │             │                  │
│  │ (Write Log)       │──┼───┘             │                  │
│  └────────────────────┘  │                 │                  │
└──────────────────────────┘                 │                  │
                                             │ Event Stream     │
                                             │ (async sync)     │
└──────────────────────────────────────────────────────────────┘
```

### When to Use CQRS

| Scenario                                  | CQRS Recommended? |
| ----------------------------------------- | ----------------- |
| Simple CRUD application                   | NO                |
| High read/write ratio imbalance           | YES               |
| Complex business rules on writes          | YES               |
| Multiple read representations needed      | YES               |
| Need for audit trail / temporal queries   | YES (with ES)     |
| Team needs independent read/write scaling | YES               |
| Small team, simple domain                 | NO                |
| Real-time dashboards / analytics          | YES               |
| Collaborative editing systems             | YES               |

**Rule:** Default to traditional CRUD. Introduce CQRS only when you have clear evidence that read and write concerns are diverging significantly.

### CQRS Maturity Levels

| Level | Description                                      |
| ----- | ------------------------------------------------ |
| L0    | No separation — standard CRUD                    |
| L1    | Separate read/write models, same data store      |
| L2    | Separate read/write models, separate data stores |
| L3    | CQRS + Event Sourcing — writes produce events    |
| L4    | Full ES with snapshots, projections, replay      |

This skill covers **L1 through L4**. Most applications should target **L1 or L2**. Reserve L3/L4 for domains requiring full auditability and replay.

---

## 2. Command Model

The command model handles all state mutations. It is the single source of truth for business logic.

### Command Structure

Every command is an explicit struct representing an intent to change state:

```go
// Command represents an intent to mutate state
type Command struct {
    ID        string            `json:"id"`
    Type      string            `json:"type"`      // "CreateOrder", "CancelOrder"
    Aggregate string            `json:"aggregate"` // aggregate type
    AggID     string            `json:"agg_id"`    // aggregate instance ID
    Data      json.RawMessage   `json:"data"`      // command payload
    Metadata  map[string]string `json:"metadata"`  // correlation ID, user ID, timestamps
    CreatedAt time.Time         `json:"created_at"`
}
```

### Command Handler Interface

```go
// CommandHandler processes commands on a specific aggregate type
type CommandHandler interface {
    Handle(ctx context.Context, cmd Command) error
}

// CommandBus routes commands to the appropriate handler
type CommandBus struct {
    handlers map[string]CommandHandler
    mu       sync.RWMutex
}

func (cb *CommandBus) Register(aggregateType string, handler CommandHandler) {
    cb.mu.Lock()
    defer cb.mu.Unlock()
    cb.handlers[aggregateType] = handler
}

func (cb *CommandBus) Dispatch(ctx context.Context, cmd Command) error {
    cb.mu.RLock()
    handler, ok := cb.handlers[cmd.Aggregate]
    cb.mu.RUnlock()
    if !ok {
        return fmt.Errorf("no handler for aggregate type: %s", cmd.Aggregate)
    }
    return handler.Handle(ctx, cmd)
}
```

### Aggregate Design (Go)

An aggregate is a consistency boundary. All invariants must hold within a single aggregate.

```go
type OrderAggregate struct {
    ID         string
    CustomerID string
    Items      []OrderItem
    Status     OrderStatus
    Version    int64
    events     []DomainEvent // uncommitted events
}

type OrderStatus string

const (
    StatusDraft    OrderStatus = "DRAFT"
    StatusConfirmed OrderStatus = "CONFIRMED"
    StatusCancelled OrderStatus = "CANCELLED"
)

// CreateOrder command handler
func (a *OrderAggregate) CreateOrder(cmd CreateOrderCommand) error {
    if cmd.CustomerID == "" {
        return ErrInvalidCustomerID
    }
    if len(cmd.Items) == 0 {
        return ErrEmptyOrder
    }

    a.ID = cmd.OrderID
    a.CustomerID = cmd.CustomerID
    a.Items = cmd.Items
    a.Status = StatusDraft
    a.Version++

    a.events = append(a.events, DomainEvent{
        Type:        "OrderCreated",
        AggregateID: a.ID,
        Version:     a.Version,
        Data: OrderCreatedData{
            CustomerID: a.CustomerID,
            Items:      a.Items,
        },
        Timestamp: time.Now().UTC(),
    })
    return nil
}

// CancelOrder command handler
func (a *OrderAggregate) CancelOrder(cmd CancelOrderCommand) error {
    if a.Status != StatusConfirmed && a.Status != StatusDraft {
        return fmt.Errorf("cannot cancel order in status: %s", a.Status)
    }

    a.Status = StatusCancelled
    a.Version++

    a.events = append(a.events, DomainEvent{
        Type:        "OrderCancelled",
        AggregateID: a.ID,
        Version:     a.Version,
        Data: OrderCancelledData{
            Reason: cmd.Reason,
        },
        Timestamp: time.Now().UTC(),
    })
    return nil
}

// UncommittedEvents returns events to be persisted
func (a *OrderAggregate) UncommittedEvents() []DomainEvent {
    evts := make([]DomainEvent, len(a.events))
    copy(evts, a.events)
    return evts
}

// MarkEventsCommitted clears the uncommitted events after persistence
func (a *OrderAggregate) MarkEventsCommitted() {
    a.events = a.events[:0]
}
```

### Domain Event Structure

```go
type DomainEvent struct {
    ID          string          `json:"id"`
    Type        string          `json:"type"`           // "OrderCreated"
    AggregateID string          `json:"aggregate_id"`   // "ord-123"
    Aggregate   string          `json:"aggregate"`      // "Order"
    Version     int64           `json:"version"`        // aggregate version
    Data        json.RawMessage `json:"data"`           // event payload
    Metadata    map[string]string `json:"metadata"`     // causation ID, correlation ID
    Timestamp   time.Time       `json:"timestamp"`
}
```

### Command Validation Pipeline

```go
// CommandMiddleware intercepts commands for cross-cutting concerns
type CommandMiddleware func(CommandHandler) CommandHandler

func LoggingMiddleware(next CommandHandler) CommandHandler {
    return CommandHandlerFunc(func(ctx context.Context, cmd Command) error {
        log.Printf("[CMD] Dispatching %s to %s (corr=%s)", cmd.Type, cmd.Aggregate, cmd.Metadata["correlation_id"])
        start := time.Now()
        err := next.Handle(ctx, cmd)
        log.Printf("[CMD] Completed %s in %v (err=%v)", cmd.Type, time.Since(start), err)
        return err
    })
}

func ValidationMiddleware(validators map[string]func(Command) error) CommandMiddleware {
    return func(next CommandHandler) CommandHandler {
        return CommandHandlerFunc(func(ctx context.Context, cmd Command) error {
            if validate, ok := validators[cmd.Type]; ok {
                if err := validate(cmd); err != nil {
                    return fmt.Errorf("validation failed: %w", err)
                }
            }
            return next.Handle(ctx, cmd)
        })
    }
}
```

---

## 3. Query Model

The query model serves read requests. It is **eventually consistent** with the command model, synchronized via events.

### Read Model Design

Read models are denormalized, query-optimized structures:

```go
// OrderReadModel is a denormalized view for query operations
type OrderReadModel struct {
    ID           string    `json:"id"`
    CustomerName string    `json:"customer_name"`
    TotalAmount  float64   `json:"total_amount"`
    ItemCount    int       `json:"item_count"`
    Status       string    `json:"status"`
    CreatedAt    time.Time `json:"created_at"`
    UpdatedAt    time.Time `json:"updated_at"`
    // Flattened data for fast querying — no joins needed
    CustomerEmail string   `json:"customer_email"`
    ShippingCity  string   `json:"shipping_city"`
    Tags          []string `json:"tags"` // search tokens
}
```

### Query Handler

```go
// QueryHandler serves read requests
type QueryHandler interface {
    Handle(ctx context.Context, query Query) (any, error)
}

type Query struct {
    Type     string          `json:"type"`       // "GetOrder", "ListOrders"
    Data     json.RawMessage `json:"data"`       // query parameters
    Metadata map[string]string `json:"metadata"`
}

// OrderQueryHandler implements query-side operations
type OrderQueryHandler struct {
    db *sql.DB // read-optimized database
}

func (h *OrderQueryHandler) Handle(ctx context.Context, q Query) (any, error) {
    switch q.Type {
    case "GetOrder":
        return h.GetOrder(ctx, q)
    case "ListOrders":
        return h.ListOrders(ctx, q)
    case "GetOrderStatistics":
        return h.GetStatistics(ctx, q)
    default:
        return nil, fmt.Errorf("unknown query type: %s", q.Type)
    }
}

func (h *OrderQueryHandler) ListOrders(ctx context.Context, q Query) (*OrderList, error) {
    var params ListOrdersParams
    if err := json.Unmarshal(q.Data, &params); err != nil {
        return nil, err
    }

    query := `
        SELECT id, customer_name, total_amount, item_count, status, created_at
        FROM order_read_model
        WHERE status = $1 AND created_at >= $2
        ORDER BY created_at DESC
        LIMIT $3 OFFSET $4
    `
    // ... execute query and map to OrderList
}
```

### CQRS vs Event Sourcing

| Aspect               | CQRS Only                     | CQRS + Event Sourcing                 |
| -------------------- | ----------------------------- | ------------------------------------- |
| Write storage        | Current state (CRUD)          | Immutable event log                   |
| Read model sync      | Application code or triggers  | Projections consume events            |
| Audit trail          | Requires separate audit table | Built-in (events are the audit trail) |
| State reconstruction | N/A — state is current        | Replay all events from beginning      |
| Complexity           | Moderate (L1/L2)              | High (L3/L4)                          |
| Debugging            | Standard debugging            | Time-travel debugging possible        |

**Recommendation:** Start with CQRS-only (L1/L2). Add Event Sourcing (L3/L4) only when you need temporal queries, audit trails, or state reconstruction.

### Materialized View Strategy

```sql
-- PostgreSQL materialized view for read model
CREATE MATERIALIZED VIEW order_summary AS
SELECT
    o.id,
    c.name AS customer_name,
    c.email AS customer_email,
    COUNT(oi.id) AS item_count,
    SUM(oi.quantity * oi.unit_price) AS total_amount,
    o.status,
    o.created_at
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id, c.name, c.email, o.status, o.created_at;

-- Refresh strategy: either scheduled or triggered by events
REFRESH MATERIALIZED VIEW CONCURRENTLY order_summary;
```

---

## 4. Event Store

The event store is the authoritative record of all state changes. It is append-only and immutable.

### Event Store Schema (PostgreSQL)

```sql
CREATE TABLE event_store (
    id            BIGSERIAL PRIMARY KEY,
    event_id      UUID NOT NULL UNIQUE,          -- global unique event ID
    aggregate_type VARCHAR(100) NOT NULL,         -- "Order", "Customer"
    aggregate_id  VARCHAR(255) NOT NULL,          -- instance ID
    event_type    VARCHAR(100) NOT NULL,          -- "OrderCreated"
    event_data    JSONB NOT NULL,                 -- event payload
    metadata      JSONB,                          -- correlation, causation, user
    version       BIGINT NOT NULL,                -- aggregate version
    timestamp     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Optimistic concurrency: prevent duplicate versions
    CONSTRAINT uq_aggregate_version
        UNIQUE (aggregate_type, aggregate_id, version)
);

-- Indexes for common query patterns
CREATE INDEX idx_event_store_by_aggregate
    ON event_store (aggregate_type, aggregate_id, version);
CREATE INDEX idx_event_store_by_type
    ON event_store (event_type);
CREATE INDEX idx_event_store_by_timestamp
    ON event_store (timestamp);

-- For catching up projections
CREATE INDEX idx_event_store_global_order
    ON event_store (id);
```

### Event Store Repository (Go)

```go
type EventStoreRepository struct {
    db *sql.DB
}

// AppendEvents persists events atomically
func (r *EventStoreRepository) AppendEvents(ctx context.Context, events []DomainEvent) error {
    if len(events) == 0 {
        return nil
    }

    tx, err := r.db.BeginTx(ctx, nil)
    if err != nil {
        return fmt.Errorf("begin transaction: %w", err)
    }
    defer tx.Rollback()

    for _, ev := range events {
        _, err := tx.ExecContext(ctx, `
            INSERT INTO event_store
                (event_id, aggregate_type, aggregate_id, event_type,
                 event_data, metadata, version, timestamp)
            VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8)
        `, ev.ID, ev.Aggregate, ev.AggregateID, ev.Type,
            ev.Data, ev.Metadata, ev.Version, ev.Timestamp)
        if err != nil {
            return fmt.Errorf("insert event %s: %w", ev.ID, err)
        }
    }

    return tx.Commit()
}

// LoadAggregateEvents retrieves all events for an aggregate instance
func (r *EventStoreRepository) LoadAggregateEvents(
    ctx context.Context,
    aggregateType, aggregateID string,
    fromVersion int64,
) ([]DomainEvent, error) {
    rows, err := r.db.QueryContext(ctx, `
        SELECT event_id, aggregate_type, aggregate_id, event_type,
               event_data, metadata, version, timestamp
        FROM event_store
        WHERE aggregate_type = $1 AND aggregate_id = $2 AND version > $3
        ORDER BY version ASC
    `, aggregateType, aggregateID, fromVersion)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var events []DomainEvent
    for rows.Next() {
        var ev DomainEvent
        if err := rows.Scan(&ev.ID, &ev.Aggregate, &ev.AggregateID,
            &ev.Type, &ev.Data, &ev.Metadata, &ev.Version, &ev.Timestamp); err != nil {
            return nil, err
        }
        events = append(events, ev)
    }
    return events, rows.Err()
}
```

### Snapshotting

Snapshots prevent unbounded event replay. Store the aggregate state at a point in time.

```sql
CREATE TABLE snapshots (
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id   VARCHAR(255) NOT NULL,
    version        BIGINT NOT NULL,
    state_data     JSONB NOT NULL,
    metadata       JSONB,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (aggregate_type, aggregate_id)
);
```

```go
// Snapshotting policy: snapshot every N events or when aggregate size exceeds threshold
const SnapshotInterval = 100

func (a *OrderAggregate) ShouldSnapshot() bool {
    return a.Version > 0 && a.Version%SnapshotInterval == 0
}
```

### Event Versioning and Schema Evolution

```go
// Upcast events from older schemas to current schema
type EventUpcaster func(event DomainEvent) (DomainEvent, error)

var upcasters = map[string][]EventUpcaster{
    "OrderCreated": {
        v1ToV2Upcaster,
        v2ToV3Upcaster,
    },
}

func v1ToV2Upcaster(ev DomainEvent) (DomainEvent, error) {
    // Migrate v1 schema: {customer_id, items}
    // To v2 schema: {customer_id, customer_name, items, shipping_address}
    var data map[string]any
    if err := json.Unmarshal(ev.Data, &data); err != nil {
        return ev, err
    }
    if _, ok := data["schema_version"]; !ok || data["schema_version"] == 1 {
        data["schema_version"] = 2
        data["customer_name"] = "" // default for migrated events
        data["shipping_address"] = ""
    }
    newData, _ := json.Marshal(data)
    ev.Data = newData
    return ev, nil
}
```

---

## 5. Projection System

Projections consume events and build read models. They are the bridge between the event store and the query model.

### Projection Interface

```go
// Projector builds and maintains a read model from events
type Projector interface {
    // Name identifies this projector (e.g., "order-read-model")
    Name() string

    // HandleEvent processes a single event and updates the read model
    HandleEvent(ctx context.Context, event DomainEvent) error

    // Reset clears the read model for rebuilding
    Reset(ctx context.Context) error

    // Position returns the last processed event ID (for resumption)
    Position(ctx context.Context) (int64, error)
}
```

### Projection Implementation

```go
type OrderReadModelProjector struct {
    db *sql.DB
}

func (p *OrderReadModelProjector) Name() string {
    return "order-read-model"
}

func (p *OrderReadModelProjector) HandleEvent(ctx context.Context, ev DomainEvent) error {
    tx, err := p.db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback()

    switch ev.Type {
    case "OrderCreated":
        return p.handleOrderCreated(tx, ev)
    case "OrderConfirmed":
        return p.handleOrderConfirmed(tx, ev)
    case "OrderCancelled":
        return p.handleOrderCancelled(tx, ev)
    case "OrderItemAdded":
        return p.handleOrderItemAdded(tx, ev)
    default:
        // Ignore events not relevant to this projection
        return nil
    }
}

func (p *OrderReadModelProjector) handleOrderCreated(tx *sql.Tx, ev DomainEvent) error {
    var data OrderCreatedData
    if err := json.Unmarshal(ev.Data, &data); err != nil {
        return err
    }

    _, err := tx.Exec(`
        INSERT INTO order_read_model
            (id, customer_name, total_amount, item_count, status, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    `, ev.AggregateID, data.CustomerName, data.TotalAmount,
        len(data.Items), "DRAFT", ev.Timestamp, ev.Timestamp)
    return err
}

func (p *OrderReadModelProjector) handleOrderConfirmed(tx *sql.Tx, ev DomainEvent) error {
    _, err := tx.Exec(`
        UPDATE order_read_model
        SET status = 'CONFIRMED', updated_at = $1
        WHERE id = $2
    `, ev.Timestamp, ev.AggregateID)
    return err
}
```

### Projection Rebuilding

```go
// ProjectionRebuilder replays all events to rebuild a read model
type ProjectionRebuilder struct {
    eventStore *EventStoreRepository
    projector  Projector
}

func (r *ProjectionRebuilder) Rebuild(ctx context.Context) error {
    // 1. Reset the projector
    if err := r.projector.Reset(ctx); err != nil {
        return fmt.Errorf("reset projector: %w", err)
    }

    // 2. Stream all events in order
    events, err := r.eventStore.LoadAllEvents(ctx, 0)
    if err != nil {
        return fmt.Errorf("load events: %w", err)
    }

    // 3. Replay each event
    for _, ev := range events {
        if err := r.projector.HandleEvent(ctx, ev); err != nil {
            return fmt.Errorf("handle event %s (%s): %w", ev.Type, ev.ID, err)
        }
    }

    log.Printf("Projection rebuilt: %s, processed %d events", r.projector.Name(), len(events))
    return nil
}
```

### Eventual Consistency Guarantees

```
┌─────────────────────────────────────────────────────────────────┐
│              Eventual Consistency Timeline                       │
│                                                                 │
│  Time ───────────────────────────────────────────────►          │
│                                                                 │
│  Command: [CreateOrder] ──► EventStore (immediate)              │
│                                │                                │
│                                ▼                                │
│                         [OrderCreated] event                    │
│                                │                                │
│                                ▼                                │
│  Projection:          [Process event] ──► [Update read model]   │
│                                                 │               │
│                                ◄────────────────┘               │
│                                                                 │
│  Query:   [GetOrder] ──► [Read model] ──► [Return result]      │
│                                                                 │
│  Consistency window: typically < 100ms (same-process)           │
│  Consistency window: typically < 1s (async queue)              │
└─────────────────────────────────────────────────────────────────┘
```

| Guarantee      | Implementation                        | Latency      |
| -------------- | ------------------------------------- | ------------ |
| Synchronous    | Projection runs in same transaction   | < 10ms       |
| Near-real-time | Projection runs via in-memory channel | < 100ms      |
| Eventually     | Projection runs via message queue     | < 1s         |
| Scheduled      | Projection runs on cron/interval      | Configurable |

---

## 6. Messaging Infrastructure

The messaging layer transports events from the command model to the query model.

### Outbox Pattern

The outbox pattern guarantees at-least-once event delivery alongside database writes.

```sql
CREATE TABLE outbox (
    id            BIGSERIAL PRIMARY KEY,
    event_id      UUID NOT NULL UNIQUE,
    aggregate_type VARCHAR(100),
    aggregate_id  VARCHAR(255),
    event_type    VARCHAR(100),
    payload       JSONB NOT NULL,
    metadata      JSONB,
    status        VARCHAR(20) NOT NULL DEFAULT 'PENDING', -- PENDING, SENT, FAILED
    retry_count   INT NOT NULL DEFAULT 0,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ
);

CREATE INDEX idx_outbox_status
    ON outbox (status, created_at) WHERE status = 'PENDING';
```

```go
// OutboxPublisher reads pending events and publishes to message broker
type OutboxPublisher struct {
    db       *sql.DB
    publisher EventPublisher
    pollInterval time.Duration
}

func (p *OutboxPublisher) Run(ctx context.Context) error {
    ticker := time.NewTicker(p.pollInterval)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case <-ticker.C:
            if err := p.publishPending(ctx); err != nil {
                log.Printf("outbox publish error: %v", err)
            }
        }
    }
}

func (p *OutboxPublisher) publishPending(ctx context.Context) error {
    rows, err := p.db.QueryContext(ctx, `
        SELECT id, event_id, event_type, payload, metadata
        FROM outbox
        WHERE status = 'PENDING'
        ORDER BY created_at ASC
        LIMIT 100
        FOR UPDATE SKIP LOCKED
    `)
    if err != nil {
        return err
    }
    defer rows.Close()

    for rows.Next() {
        var id int64
        var eventID, eventType string
        var payload json.RawMessage
        var metadata map[string]string

        if err := rows.Scan(&id, &eventID, &eventType, &payload, &metadata); err != nil {
            return err
        }

        if err := p.publisher.Publish(ctx, eventType, payload); err != nil {
            p.markFailed(ctx, id)
            continue
        }

        p.markSent(ctx, id)
    }
    return nil
}
```

### Idempotency in Event Processing

```go
// IdempotentProcessor ensures events are processed exactly once
type IdempotentProcessor struct {
    db *sql.DB
}

func (p *IdempotentProcessor) IsProcessed(ctx context.Context, eventID string) (bool, error) {
    var exists bool
    err := p.db.QueryRowContext(ctx,
        `SELECT EXISTS(SELECT 1 FROM processed_events WHERE event_id = $1)`,
        eventID).Scan(&exists)
    return exists, err
}

func (p *IdempotentProcessor) MarkProcessed(ctx context.Context, eventID string, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx,
        `INSERT INTO processed_events (event_id, processed_at) VALUES ($1, NOW())`,
        eventID)
    return err
}

// Processed events table
// CREATE TABLE processed_events (
//     event_id       UUID PRIMARY KEY,
//     projector_name VARCHAR(100),
//     processed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
// );
```

### Kafka Consumer Group for Projections

```go
func StartProjectionConsumers(ctx context.Context, projectors map[string]Projector) error {
    config := &kafka.ConsumerConfig{
        GroupID: "projections",
        Topics:  []string{"domain-events"},
    }

    consumer, err := kafka.NewConsumer(config)
    if err != nil {
        return err
    }

    for _, projector := range projectors {
        go func(p Projector) {
            // Each projector resumes from its own position
            pos, _ := p.Position(ctx)
            log.Printf("Starting projector %s from position %d", p.Name(), pos)

            messages, err := consumer.ConsumeFrom(ctx, p.Name(), pos)
            if err != nil {
                log.Printf("Consume error for %s: %v", p.Name(), err)
                return
            }

            for msg := range messages {
                var ev DomainEvent
                if err := json.Unmarshal(msg.Value, &ev); err != nil {
                    log.Printf("Unmarshal error: %v", err)
                    continue
                }

                if err := p.HandleEvent(ctx, ev); err != nil {
                    log.Printf("Projection error: %v", err)
                    // Do NOT acknowledge — will be retried
                    continue
                }

                consumer.Acknowledge(msg)
            }
        }(projector)
    }

    return nil
}
```

---

## 7. Go Implementation

### Full Pipeline: Command to Projection

```
┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│  Client   │───►│ Command Bus  │───►│  Aggregate  │───►│ Event Store  │
└──────────┘    └──────────────┘    └─────────────┘    └──────┬───────┘
                                                              │
                                                              ▼
┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│  Query    │◄───│ Query Handler│◄───│ Read Model  │◄───│ Projection   │
│  Client   │    │              │    │ (materialized│    │ Worker       │
└──────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

### Goroutine-Based Event Processor

```go
// EventProcessor orchestrates the command-to-projection pipeline
type EventProcessor struct {
    commandBus     *CommandBus
    eventStore     *EventStoreRepository
    outbox         *OutboxRepository
    projectors     map[string]Projector
    eventChannel   chan DomainEvent
    errChannel     chan error
    wg             sync.WaitGroup
    processorCount int
}

func NewEventProcessor(opts ...Option) *EventProcessor {
    ep := &EventProcessor{
        eventChannel:   make(chan DomainEvent, 1000), // buffered channel
        errChannel:     make(chan error, 100),
        projectors:     make(map[string]Projector),
        processorCount: runtime.NumCPU(),
    }
    for _, opt := range opts {
        opt(ep)
    }
    return ep
}

// Start launches worker goroutines
func (ep *EventProcessor) Start(ctx context.Context) error {
    // Launch projection workers
    for i := 0; i < ep.processorCount; i++ {
        ep.wg.Add(1)
        go ep.projectionWorker(ctx, i)
    }

    // Launch error handler
    ep.wg.Add(1)
    go ep.errorHandler(ctx)

    log.Printf("Event processor started with %d projection workers", ep.processorCount)
    return nil
}

func (ep *EventProcessor) projectionWorker(ctx context.Context, id int) {
    defer ep.wg.Done()

    for {
        select {
        case <-ctx.Done():
            log.Printf("Projection worker %d shutting down", id)
            return
        case event, ok := <-ep.eventChannel:
            if !ok {
                return
            }

            // Each projector processes events independently
            for name, projector := range ep.projectors {
                if err := projector.HandleEvent(ctx, event); err != nil {
                    ep.errChannel <- fmt.Errorf("projector %s: %w", name, err)
                }
            }
        }
    }
}

// PublishEvents sends events to the processing pipeline
func (ep *EventProcessor) PublishEvents(ctx context.Context, events []DomainEvent) error {
    for _, ev := range events {
        select {
        case ep.eventChannel <- ev:
        case <-ctx.Done():
            return ctx.Err()
        }
    }
    return nil
}

func (ep *EventProcessor) Stop() {
    close(ep.eventChannel)
    ep.wg.Wait()
    close(ep.errChannel)
    log.Println("Event processor stopped")
}
```

### Complete Command Flow with Event Publishing

```go
// CommandExecutionService orchestrates the full command lifecycle
type CommandExecutionService struct {
    commandBus     *CommandBus
    eventStore     *EventStoreRepository
    outbox         *OutboxRepository
    eventProcessor *EventProcessor
}

func (s *CommandExecutionService) ExecuteCommand(ctx context.Context, cmd Command) error {
    // 1. Load aggregate from event store (or snapshot)
    aggregate, err := s.loadAggregate(ctx, cmd.Aggregate, cmd.AggID)
    if err != nil {
        return err
    }

    // 2. Execute command on aggregate
    if err := s.commandBus.Dispatch(ctx, cmd); err != nil {
        return fmt.Errorf("command failed: %w", err)
    }

    // 3. Get uncommitted events
    events := aggregate.UncommittedEvents()
    if len(events) == 0 {
        return nil
    }

    // 4. Persist events to event store (atomic)
    if err := s.eventStore.AppendEvents(ctx, events); err != nil {
        return fmt.Errorf("append events: %w", err)
    }

    // 5. Write events to outbox (same transaction as step 4 ideally)
    if err := s.outbox.Write(ctx, events); err != nil {
        return fmt.Errorf("write outbox: %w", err)
    }

    // 6. Publish events to projection pipeline
    if err := s.eventProcessor.PublishEvents(ctx, events); err != nil {
        return fmt.Errorf("publish events: %w", err)
    }

    // 7. Mark events as committed on aggregate
    aggregate.MarkEventsCommitted()

    // 8. Save snapshot if needed
    if aggregate.ShouldSnapshot() {
        if err := s.eventStore.SaveSnapshot(ctx, aggregate); err != nil {
            log.Printf("Snapshot save failed (non-fatal): %v", err)
        }
    }

    return nil
}
```

### Interface Segregation for Testing

```go
// Define interfaces for all external dependencies
type (
    EventStorer interface {
        AppendEvents(ctx context.Context, events []DomainEvent) error
        LoadAggregateEvents(ctx context.Context, aggregateType, aggregateID string, fromVersion int64) ([]DomainEvent, error)
        SaveSnapshot(ctx context.Context, agg Snapshotable) error
        LoadSnapshot(ctx context.Context, aggregateType, aggregateID string) (*Snapshot, error)
    }

    EventPublisher interface {
        Publish(ctx context.Context, eventType string, data json.RawMessage) error
    }

    ProjectorRegistry interface {
        GetProjector(name string) (Projector, error)
        ListProjectors() []string
    }
)
```

---

## 8. Anti-Patterns

### Over-Engineering

**Problem:** Implementing full CQRS + ES for a simple CRUD application.

```
BAD:
┌─────────┐   ┌──────────┐   ┌──────────┐   ┌───────────┐   ┌─────────┐
│ Command │──►│ Aggregate│──►│  Event   │──►│  Outbox   │──►│  Kafka  │
│         │   │          │   │  Store   │   │           │   │         │
└─────────┘   └──────────┘   └──────────┘   └───────────┘   └─────────┘

For: Storing a user's todo list with 10 items

GOOD:
┌─────────┐   ┌───────────┐   ┌──────────┐
│  REST   │──►│  Handler  │──►│ PostgreSQL│
│  API    │   │           │   │  CRUD     │
└─────────┘   └───────────┘   └──────────┘
```

**Detection Checklist:**

- [ ] Does this application have fewer than 5 domain entities?
- [ ] Are there no complex business invariants to enforce?
- [ ] Is the read/write ratio less than 10:1?
- [ ] Does the team have fewer than 3 developers?
- [ ] Is there no need for audit trails or temporal queries?

If 3+ are YES → Use CRUD, not CQRS.

### Premature CQRS

**Problem:** Implementing separate read/write models from day one without evidence of divergence.

**Correct Approach:**

1. Start with a single model (CRUD)
2. Monitor: Are read queries becoming complex? Are writes slowing down reads?
3. **Only then** split into CQRS — you can do this incrementally
4. Begin with L1 (same database, separate models), evolve to L2 (separate databases) as needed

### Distributed Transactions

**Problem:** Trying to maintain ACID consistency across command and query models.

```go
// BAD: Trying to update command-side and query-side in one transaction
func (s *Service) BadApproach(ctx context.Context) error {
    tx := s.commandDB.Begin()
    defer tx.Rollback()

    // Write to command model
    s.commandRepo.Save(ctx, entity, tx)

    // Try to update read model in same transaction
    s.queryRepo.Update(ctx, readModel, tx) // WRONG — different database

    return tx.Commit() // Will fail or create consistency issues
}

// GOOD: Accept eventual consistency
func (s *Service) GoodApproach(ctx context.Context) error {
    // 1. Write to command model
    events := s.commandService.ProcessCommand(ctx, cmd)

    // 2. Persist events (atomic with outbox)
    s.eventStore.Append(ctx, events)
    s.outbox.Write(ctx, events)

    // 3. Projections will eventually update read model
    // No need for distributed transaction
    return nil
}
```

### Event-Carried State Transfer (Subtle Anti-Pattern)

**Problem:** Including all aggregate state in every event instead of just the delta.

```go
// BAD: Including entire aggregate in every event
type OrderCreatedEvent struct {
    SchemaVersion int              `json:"schema_version"`
    OrderID       string           `json:"order_id"`
    FullOrderState OrderAggregate  `json:"full_order"` // NO — massive payload
}

// GOOD: Include only what changed
type OrderCreatedEvent struct {
    SchemaVersion int            `json:"schema_version"`
    OrderID       string         `json:"order_id"`
    CustomerID    string         `json:"customer_id"`
    Items         []OrderItem    `json:"items"`
    TotalAmount   float64        `json:"total_amount"`
}
```

### Projection Fan-Out Without Backpressure

**Problem:** A single event triggers N projections, all running concurrently without rate limiting.

```go
// BAD: Unbounded goroutine creation
func (p *EventFanOut) HandleEvent(ctx context.Context, ev DomainEvent) error {
    for _, projector := range p.projectors {
        go func(proj Projector) {
            proj.HandleEvent(ctx, ev) // Could create thousands of goroutines
        }(projector)
    }
    return nil
}

// GOOD: Bounded worker pool with channel
func (p *EventFanOut) HandleEvent(ctx context.Context, ev DomainEvent) error {
    for _, projector := range p.projectors {
        select {
        case p.eventChannel <- ProjectorEvent{Projector: projector, Event: ev}:
        case <-ctx.Done():
            return ctx.Err()
        }
    }
    return nil
}
```

---

## 9. Stage 5 Integration

### SPEC Development Checklist

When developing CQRS architecture into the implementation plan (Stage 4 → Stage 5):

| #   | Item                                                    | Owner | Status |
| --- | ------------------------------------------------------- | ----- | ------ |
| 1   | Command model interfaces and implementations defined    | CTO   | [ ]    |
| 2   | Aggregate consistency boundaries documented             | CTO   | [ ]    |
| 3   | Event store schema designed and reviewed                | CTO   | [ ]    |
| 4   | Projection system interface defined                     | CTO   | [ ]    |
| 5   | Outbox pattern implementation specified                 | CTO   | [ ]    |
| 6   | Idempotency strategy documented                         | CSO   | [ ]    |
| 7   | Event versioning and upcasting strategy defined         | CTO   | [ ]    |
| 8   | Consistency model documented (sync vs async)            | CTO   | [ ]    |
| 9   | Error handling and retry policies specified             | CTO   | [ ]    |
| 10  | Performance benchmarks defined for read and write paths | CTO   | [ ]    |

### Code Review Checklist (Stage 6)

| #   | Check                                                           | Severity |
| --- | --------------------------------------------------------------- | -------- |
| 1   | Commands are explicit structs (not generic maps)                | P1       |
| 2   | Aggregates enforce invariants before emitting events            | P0       |
| 3   | Events are immutable after persistence                          | P0       |
| 4   | Event store uses optimistic concurrency control                 | P0       |
| 5   | Outbox table writes are in same transaction as event store      | P0       |
| 6   | Projections are idempotent (safe to replay)                     | P1       |
| 7   | Event processors use bounded channels (no unbounded goroutines) | P1       |
| 8   | Projection position is checkpointed after each event            | P1       |
| 9   | Error handling includes dead-letter queue for poison events     | P2       |
| 10  | Context propagation for cancellation across pipeline            | P1       |
| 11  | Snapshot strategy defined and implemented                       | P2       |
| 12  | Event upcasters tested for all schema versions                  | P1       |
| 13  | No distributed transactions between command and query models    | P0       |
| 14  | Read model queries do not touch event store tables              | P1       |

### Testing Requirements (Stage 7)

#### Unit Tests

```go
func TestOrderAggregate_CreateOrder(t *testing.T) {
    agg := NewOrderAggregate()

    cmd := CreateOrderCommand{
        OrderID:    "ord-001",
        CustomerID: "cust-123",
        Items: []OrderItem{
            {ProductID: "prod-1", Quantity: 2, UnitPrice: 19.99},
        },
    }

    err := agg.CreateOrder(cmd)
    assert.NoError(t, err)

    events := agg.UncommittedEvents()
    assert.Len(t, events, 1)
    assert.Equal(t, "OrderCreated", events[0].Type)
    assert.Equal(t, int64(1), events[0].Version)
}

func TestOrderAggregate_CannotCancelShippedOrder(t *testing.T) {
    agg := GivenOrderInStatus("SHIPPED")

    err := agg.CancelOrder(CancelOrderCommand{Reason: "changed mind"})
    assert.Error(t, err)
    assert.Empty(t, agg.UncommittedEvents()) // No events emitted
}
```

#### Integration Tests

```go
func TestProjection_RebuildFromEvents(t *testing.T) {
    // 1. Load known events
    events := loadTestFixtures("testdata/order-events.json")

    // 2. Create fresh projector
    projector := NewOrderReadModelProjector(testDB)
    projector.Reset(context.Background())

    // 3. Replay all events
    for _, ev := range events {
        err := projector.HandleEvent(context.Background(), ev)
        require.NoError(t, err)
    }

    // 4. Verify read model state
    model := projector.GetOrder("ord-001")
    assert.Equal(t, "CONFIRMED", model.Status)
    assert.Equal(t, 39.98, model.TotalAmount)
    assert.Equal(t, 2, model.ItemCount)
}

func TestOutbox_AtLeastOnceDelivery(t *testing.T) {
    // 1. Write events to outbox
    outbox.Write(context.Background(), testEvents)

    // 2. Simulate publisher failure and retry
    publisher := NewOutboxPublisher(testDB, mockBroker)
    publisher.Run(context.Background())

    // 3. Verify all events eventually published
    published := mockBroker.GetPublished()
    assert.Len(t, published, len(testEvents))
}
```

#### Performance Tests

| Test                       | Target       | Measurement Method                   |
| -------------------------- | ------------ | ------------------------------------ |
| Command throughput         | > 1000 cmd/s | Concurrent command dispatch          |
| Projection lag             | < 100ms p99  | Event timestamp to read model update |
| Event store append latency | < 10ms p99   | Direct insert benchmark              |
| Query response time        | < 50ms p99   | Read model query benchmark           |
| Projection rebuild time    | Documented   | Full replay from event zero          |

---

## 10. References

### Internal Skills

| Skill                                         | Topic                                          |
| --------------------------------------------- | ---------------------------------------------- |
| `backend/api-patterns/event-sourcing.md`      | Event Sourcing patterns, replay, snapshots     |
| `backend/api-patterns/distributed-systems.md` | Distributed consistency, Saga, 2PC             |
| `backend/database/postgresql-optimization.md` | PostgreSQL performance for event stores        |
| `backend/api-patterns/clean-architecture.md`  | Layered architecture with domain-driven design |
| `shared/test-driven-development.md`           | TDD practices for Go                           |

### External Resources

| Resource                          | Author          | URL                                                                                               |
| --------------------------------- | --------------- | ------------------------------------------------------------------------------------------------- |
| CQRS Pattern                      | Martin Fowler   | https://martinfowler.com/bliki/CQRS.html                                                          |
| CQRS Documents                    | Greg Young      | https://cqrs.nu/Faq                                                                               |
| Event Sourcing                    | Martin Fowler   | https://martinfowler.com/eaaDev/EventSourcing.html                                                |
| Implementing Domain-Driven Design | Vaughn Vernon   | Book (Red Book)                                                                                   |
| Event Store Documentation         | Event Store Ltd | https://www.eventstore.com/docs                                                                   |
| Outbox Pattern                    | Debezium        | https://debezium.io/blog/2019/02/19/reliable-microservices-data-exchange-with-the-outbox-pattern/ |

### Verification Summary

Before deploying CQRS to production, confirm:

- [ ] All commands are validated before aggregate execution
- [ ] Aggregates enforce all invariants before emitting events
- [ ] Events are persisted atomically with outbox writes
- [ ] Projections are idempotent and resumable from any position
- [ ] Event schema versioning and upcasting are tested
- [ ] Consistency window meets product requirements (documented)
- [ ] Projection rebuild has been tested end-to-end
- [ ] Performance benchmarks meet targets (see Stage 7 table above)
- [ ] Error handling includes retry with exponential backoff
- [ ] Dead-letter queue captures poison events for manual inspection
- [ ] No P0 or P1 defects from the Stage 6 code review checklist
- [ ] User has approved the implementation plan (Stage 4 gate)
