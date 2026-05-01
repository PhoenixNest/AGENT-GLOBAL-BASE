---
name: cqrs-architecture
description: Design and implement CQRS (Command Query Responsibility Segregation) architecture patterns — separating write models from read models, implementing event sourcing for audit trails, and building eventually consistent read projections optimized for mobile API consumption patterns.
version: "1.0.0"
---

# CQRS Architecture

| Competency           | Description                                                     | Quality Criteria                                                                                                          |
| -------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Command Model        | Design the write side — commands, command handlers, aggregates  | Commands are validated before dispatch; aggregates emit domain events; no query logic in command handlers                 |
| Query Model          | Design the read side — projections optimized for query patterns | Read models are denormalized for the specific query; p95 read latency ≤ 20ms; projections rebuilt-able from event history |
| Event Sourcing       | Implement event store for aggregate state persistence           | Events are append-only and immutable; aggregate state rebuilt from event replay; event schema versioned with upcasters    |
| Eventual Consistency | Manage consistency lag between command and query sides          | Replication lag documented (target: < 500ms p95); client handles eventual consistency with optimistic updates             |

## Execution Guidance

### CQRS Flow

```
Mobile Client
    ↓ POST /commands/create-order
Command Handler → Validate → Aggregate.handle() → Emit OrderCreated event
    ↓ Publish to event bus
Event Handler → Update read projection (order_list_view, order_detail_view)
    ↓
Mobile Client → GET /orders/123
Query Handler → Read from read projection → Return optimized response
```

### Read Model Design for Mobile

Mobile APIs have specific needs — design read projections around them:

| Mobile Query Pattern      | Read Model Design                                       |
| ------------------------- | ------------------------------------------------------- |
| List with summary         | Denormalized list view with thumbnail URL, title, price |
| Detail view               | Complete detail projection — all fields in one DB read  |
| User dashboard aggregates | Pre-computed stats updated on relevant events           |

Never let mobile clients join tables — the read model should answer the query in a single index lookup. If a mobile screen requires data from 3+ tables, it needs its own read projection.
