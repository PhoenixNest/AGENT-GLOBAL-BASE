---
name: backend-api-patterns-event-sourcing
description: 'Backend skill: Event Sourcing'
---

# Event Sourcing

**Category:** Backend Architecture
**Owner:** Senior Backend Engineer (Viktor Horvath)

## Overview

Implements event sourcing as the persistence model for domain aggregates, capturing all state changes as an immutable sequence of events. Covers CQRS separation of read and write models, Kafka integration for event distribution, event schema versioning with Avro, event replay strategies for state reconstruction, and snapshot optimization for aggregate loading performance.

## Competency Dimensions

| Dimension               | Description                                                               | Proficiency Indicators                                                                                                          |
| ----------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Event Sourcing Patterns | Append-only event stores, aggregate reconstruction, temporal queries      | Designs event schemas that capture intent (not state changes); implements efficient aggregate reconstruction from event streams |
| CQRS Implementation     | Command/query separation, read model projection, eventual consistency     | Designs projections that transform event streams into query-optimized read models; handles projection lag gracefully            |
| Kafka Integration       | Topic design, consumer groups, offset management, exactly-once semantics  | Configures Kafka for event durability (acks=all, min.insync.replicas); implements consumer offset commit strategies             |
| Event Schema Versioning | Avro schema registry, backward/forward compatibility, schema migration    | Manages schema evolution with compatibility checks; handles multi-version event deserialization during rollouts                 |
| Replay Strategies       | Full replay, time-travel replay, selective replay                         | Implements replay mechanisms for rebuilding read models; supports debugging via historical state reconstruction                 |
| Snapshot Optimization   | Periodic state snapshots, snapshot-triggered compaction, merge strategies | Configures snapshot intervals based on aggregate event volume; implements efficient snapshot + delta reconstruction             |

## Execution Guidance

### Event Store Design

```go
// Core event store interface
type EventStore interface {
    Append(ctx context.Context, streamID string, expectedVersion int, events []DomainEvent) error
    Load(ctx context.Context, streamID string, fromVersion int) ([]DomainEvent, error)
    LoadSnapshot(ctx context.Context, streamID string) (*Snapshot, error)
    SaveSnapshot(ctx context.Context, streamID string, snapshot *Snapshot) error
}

// Domain event with metadata
type DomainEvent struct {
    EventID       uuid.UUID         `json:"eventId"`
    EventType     string            `json:"eventType"`
    AggregateID   string            `json:"aggregateId"`
    Version       int               `json:"version"`
    Timestamp     time.Time         `json:"timestamp"`
    Data          json.RawMessage   `json:"data"`
    Metadata      map[string]string `json:"metadata"`
}

// Optimistic concurrency check
func (es *KafkaEventStore) Append(ctx context.Context, streamID string, expectedVersion int, events []DomainEvent) error {
    // Check expected version (optimistic locking)
    currentVersion, err := es.getCurrentVersion(ctx, streamID)
    if err != nil {
        return err
    }
    if currentVersion != expectedVersion {
        return &ConcurrencyError{
            StreamID:        streamID,
            ExpectedVersion: expectedVersion,
            ActualVersion:   currentVersion,
        }
    }

    // Append events to Kafka (ordered by partition key = streamID)
    for i, event := range events {
        event.Version = expectedVersion + i + 1
        msg := &kafka.Message{
            Topic:     es.topic,
            Key:       []byte(streamID),  // Ensures ordering within stream
            Value:     serialize(event),
            Headers: []kafka.RecordHeader{
                {Key: "event_type", Value: []byte(event.EventType)},
                {Key: "aggregate_id", Value: []byte(event.AggregateID)},
                {Key: "version", Value: []byte(strconv.Itoa(event.Version))},
            },
        }
        if err := es.producer.WriteMessages(ctx, msg); err != nil {
            return fmt.Errorf("failed to append event: %w", err)
        }
    }
    return nil
}
```

### CQRS Projection Implementation

```go
// Projection reads events and builds read model
type Projection struct {
    Name       string
    Handler    func(context.Context, DomainEvent) error
    Position   int  // Last processed event version
}

type ProjectionEngine struct {
    eventStore   EventStore
    projections  []*Projection
    readStore    *sql.DB
}

func (pe *ProjectionEngine) Run(ctx context.Context) error {
    for _, proj := range pe.projections {
        go func(p *Projection) {
            for {
                events, err := pe.eventStore.Load(ctx, p.Name, p.Position)
                if err != nil {
                    log.Errorf("Projection %s failed to load events: %v", p.Name, err)
                    time.Sleep(5 * time.Second)
                    continue
                }
                if len(events) == 0 {
                    time.Sleep(100 * time.Millisecond) // Polling interval
                    continue
                }
                for _, event := range events {
                    if err := p.Handler(ctx, event); err != nil {
                        log.Errorf("Projection %s failed on event %s: %v", p.Name, event.EventID, err)
                        // Dead letter: skip or retry based on error type
                        continue
                    }
                    p.Position = event.Version
                    pe.savePosition(ctx, p.Name, p.Position)
                }
            }
        }(proj)
    }
    <-ctx.Done()
    return nil
}
```

**Projection types and their use cases:**

| Projection Type       | Purpose                             | Example                                                    |
| --------------------- | ----------------------------------- | ---------------------------------------------------------- |
| Entity projection     | Rebuilds individual aggregate state | User profile from UserCreated, EmailChanged events         |
| Read model projection | Builds query-optimized views        | Order search index from OrderPlaced, OrderShipped events   |
| Counter projection    | Maintains running totals            | Total revenue from PaymentReceived events                  |
| Denormalizer          | Cross-aggregate joins               | Order details with customer name from Order + User streams |

### Kafka Integration for Event Distribution

**Topic design principles:**

```
# Topic naming convention
events.{bounded-context}.{aggregate-type}.{version}

# Examples
events.ordering.order.v1
events.billing.payment.v1
events.identity.user.v1
```

**Kafka producer configuration for durability:**

```properties
# Producer config (Guaranteed delivery)
bootstrap.servers=kafka-1:9092,kafka-2:9092,kafka-3:9092
acks=all                          # Wait for all ISR to acknowledge
retries=2147483647                # Retry indefinitely
max.in.flight.requests.per.connection=5  # For idempotent producer
enable.idempotence=true           # Exactly-once producer
compression.type=lz4              # Balance speed/size
linger.ms=5                       # Small batching delay
batch.size=32768                  # 32KB batches
```

**Consumer configuration:**

```properties
# Consumer config
group.id=order-projection-v1
auto.offset.reset=earliest        # Start from beginning for new consumers
enable.auto.commit=false          # Manual commit after processing
max.poll.records=500              # Batch size per poll
session.timeout.ms=30000          # Consumer liveness check
max.poll.interval.ms=300000       # Max time between polls (5 min)
isolation.level=read_committed    # Only read committed transactions
```

### Event Schema Versioning with Avro

**Schema evolution rules:**

| Change Type               | Compatibility      | Example                                                               |
| ------------------------- | ------------------ | --------------------------------------------------------------------- |
| Add optional field        | Backward + Forward | `{ "name": "discount", "type": ["null", "double"], "default": null }` |
| Remove field with default | Backward           | Field had default, readers ignore it                                  |
| Rename field              | Breaking           | Requires alias: `{ "name": "newName", "aliases": ["oldName"] }`       |
| Change field type         | Breaking           | `int` → `long` is OK; `string` → `int` is not                         |
| Add enum value            | Forward only       | Old readers reject new values                                         |

**Avro schema definition:**

```json
{
  "type": "record",
  "name": "OrderPlaced",
  "namespace": "com.company.events.ordering",
  "fields": [
    { "name": "orderId", "type": "string" },
    { "name": "customerId", "type": "string" },
    {
      "name": "items",
      "type": {
        "type": "array",
        "items": {
          "type": "record",
          "name": "OrderItem",
          "fields": [
            { "name": "productId", "type": "string" },
            { "name": "quantity", "type": "int" },
            { "name": "price", "type": "double" }
          ]
        }
      }
    },
    { "name": "totalAmount", "type": "double" },
    { "name": "discount", "type": ["null", "double"], "default": null },
    { "name": "currency", "type": "string", "default": "USD" },
    {
      "name": "metadata",
      "type": [
        "null",
        {
          "type": "map",
          "values": "string"
        }
      ],
      "default": null
    }
  ]
}
```

**Schema Registry integration:**

```bash
# Register schema (backward compatible)
curl -X POST http://schema-registry:8081/subjects/order-planned-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{
    "schema": "{...avro schema...}",
    "metadata": {
      "properties": {
        "owner": "ordering-team",
        "contact": "viktor@company.com"
      }
    }
  }'

# Check compatibility
curl -X POST http://schema-registry:8081/compatibility/subjects/order-placed-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{...new schema...}"}'
```

### Replay Strategies

```go
// Full replay — rebuild entire read model from scratch
func (pe *ProjectionEngine) FullReplay(ctx context.Context, projectionName string) error {
    // Reset position to 0
    pe.resetPosition(ctx, projectionName, 0)
    // Clear existing read model
    pe.clearReadModel(ctx, projectionName)
    // Process all events from beginning
    return pe.Run(ctx)
}

// Time-travel replay — reconstruct state at specific point in time
func (pe *ProjectionEngine) ReplayToTimestamp(ctx context.Context, projectionName string, targetTime time.Time) error {
    events, err := pe.eventStore.Load(ctx, projectionName, 0)
    if err != nil {
        return err
    }

    state := make(map[string]interface{})
    for _, event := range events {
        if event.Timestamp.After(targetTime) {
            break
        }
        state = pe.applyEvent(state, event)
    }
    return pe.saveState(ctx, projectionName, state)
}

// Selective replay — replay specific event types
func (pe *ProjectionEngine) SelectiveReplay(ctx context.Context, projectionName string, eventTypes []string) error {
    events, err := pe.eventStore.Load(ctx, projectionName, 0)
    if err != nil {
        return err
    }

    typeSet := make(map[string]bool)
    for _, t := range eventTypes {
        typeSet[t] = true
    }

    for _, event := range events {
        if typeSet[event.EventType] {
            if err := pe.applyEventToReadModel(ctx, event); err != nil {
                return err
            }
        }
    }
    return nil
}
```

### Snapshot Optimization

```go
// Snapshot strategy: snapshot every N events or when aggregate size exceeds threshold
const (
    SnapshotInterval    = 100   // Events between snapshots
    SnapshotSizeThreshold = 10 * 1024  // 10KB max snapshot size
)

func (es *EventStoreWithSnapshot) LoadAggregate(ctx context.Context, aggregateID string) (*Aggregate, error) {
    // Load latest snapshot
    snapshot, err := es.LoadSnapshot(ctx, aggregateID)
    startVersion := 0
    state := make(map[string]interface{})

    if err == nil && snapshot != nil {
        state = snapshot.State
        startVersion = snapshot.Version
    }

    // Load events since snapshot
    events, err := es.Load(ctx, aggregateID, startVersion)
    if err != nil {
        return nil, err
    }

    // Apply events to snapshot state
    for _, event := range events {
        state = es.applyEvent(state, event)
    }

    // Check if we should create a new snapshot
    if len(events) >= SnapshotInterval {
        newSnapshot := &Snapshot{
            AggregateID: aggregateID,
            Version:     startVersion + len(events),
            State:       state,
            CreatedAt:   time.Now(),
        }
        es.SaveSnapshot(ctx, aggregateID, newSnapshot)
    }

    return &Aggregate{ID: aggregateID, State: state, Version: startVersion + len(events)}, nil
}
```

## Pipeline Integration

**Stage 3 (UML Engineering Package):** Sequence diagrams must show event flow from command → event store → projection → read model. ADR required for event sourcing adoption decision (vs CRUD persistence).

**Stage 5 (Development):** Event store implementation must include concurrency control. Projections must handle replay gracefully. Kafka topic configuration must enforce ordering per aggregate stream.

**Stage 6 (Code Review):** Review event schema compatibility guarantees. Validate snapshot creation triggers. Check projection error handling (dead letter behavior). Verify Kafka configuration for durability.

**Stage 7 (Testing):** Replay tests validate full and selective replay correctness. Schema evolution tests validate backward compatibility. Performance tests validate aggregate loading with and without snapshots.

## Quality Standards

| Metric                     | Target                                  | Measurement                    |
| -------------------------- | --------------------------------------- | ------------------------------ |
| Event schema compatibility | 100% backward compatible                | Schema Registry validation     |
| Projection lag (p95)       | < 5 seconds                             | Projection position monitoring |
| Snapshot efficiency        | Aggregate loads < 200ms (with snapshot) | Aggregate loading metrics      |
| Event ordering guarantee   | 100% within stream                      | Kafka partition key audit      |
| Replay correctness         | 100% state match after replay           | State comparison tests         |
| Consumer group lag         | < 1000 events                           | Kafka consumer lag monitoring  |
| Event store throughput     | > 10,000 events/sec                     | Kafka producer metrics         |
