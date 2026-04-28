---
name: backend-api-patterns-cqrs-architecture
description: CQRS (Command Query Responsibility Segregation) architecture for backend systems — command/write model separation, query/read model optimization, event-driven view materialization, and eventual consistency patterns. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 3 (Architecture) for CQRS design decisions and Stage 5 (Development) for implementation. Trigger: cqrs, command query separation, read write models, event sourcing, eventual consistency, materialized views.
prerequisites:
  - backend-api-patterns-distributed-systems

version: "1.0.0"
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

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`2.-command-model.md`](references/2.-command-model.md) — 2. Command Model
- [`4.-event-store.md`](references/4.-event-store.md) — 4. Event Store
- [`5.-projection-system.md`](references/5.-projection-system.md) — 5. Projection System
- [`6.-messaging-infrastructure.md`](references/6.-messaging-infrastructure.md) — 6. Messaging Infrastructure
- [`7.-go-implementation.md`](references/7.-go-implementation.md) — 7. Go Implementation
- [`8.-anti-patterns.md`](references/8.-anti-patterns.md) — 8. Anti-Patterns
- [`9.-stage-5-integration.md`](references/9.-stage-5-integration.md) — 9. Stage 5 Integration
