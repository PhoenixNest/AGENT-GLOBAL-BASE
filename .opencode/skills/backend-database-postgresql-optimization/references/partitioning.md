# Partitioning

## Partitioning

### Declarative Partitioning (PostgreSQL 10+)

```sql
-- Range partitioning by date (most common — time-series data)
CREATE TABLE events (
    id BIGSERIAL,
    event_type TEXT NOT NULL,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2025_q1 PARTITION OF events
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');
CREATE TABLE events_2025_q2 PARTITION OF events
    FOR VALUES FROM ('2025-04-01') TO ('2025-07-01');
CREATE TABLE events_2025_q3 PARTITION OF events
    FOR VALUES FROM ('2025-07-01') TO ('2025-10-01');
CREATE TABLE events_2025_q4 PARTITION OF events
    FOR VALUES FROM ('2025-10-01') TO ('2026-01-01');

-- Index on each partition (indexes are NOT inherited)
CREATE INDEX idx_events_2025_q1_created ON events_2025_q1(created_at DESC);
CREATE INDEX idx_events_2025_q2_created ON events_2025_q2(created_at DESC);
-- ... repeat for each partition
```

### List Partitioning

```sql
-- Partition by region or category
CREATE TABLE tenants (
    id BIGSERIAL,
    tenant_name TEXT NOT NULL,
    data JSONB,
    region TEXT NOT NULL
) PARTITION BY LIST (region);

CREATE TABLE tenants_apac PARTITION OF tenants FOR VALUES IN ('APAC', 'SEA');
CREATE TABLE tenants_emea PARTITION OF tenants FOR VALUES IN ('EMEA', 'EU');
CREATE TABLE tenants_americas PARTITION OF tenants FOR VALUES IN ('NA', 'LATAM');
```

### Partition Management

```sql
-- Attach a new partition (PostgreSQL 11+ locks only the new partition)
CREATE TABLE events_2026_q1 (LIKE events INCLUDING DEFAULTS);
-- Load data into the new partition offline if needed
ALTER TABLE events ATTACH PARTITION events_2026_q1
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

-- Detach and archive old partitions (data retention)
ALTER TABLE events DETACH PARTITION events_2024_q1;
-- Now events_2024_q1 is a standalone table — can be dumped and dropped

-- Partition pruning verification (query planner skips irrelevant partitions)
EXPLAIN ANALYZE SELECT * FROM events WHERE created_at >= '2025-06-01';
-- Should show: Append -> events_2025_q2 only (other partitions pruned)
```

### Partitioning Best Practices

| Practice                         | Reason                                          |
| -------------------------------- | ----------------------------------------------- |
| Partition size target: 1–5 GB    | Small enough for fast maintenance               |
| Monthly or quarterly partitions  | Balance between manageability and count         |
| Always partition on WHERE column | Enables partition pruning                       |
| Create indexes on each partition | Indexes do NOT propagate to partitions          |
| Automate partition creation      | Use pg_partman extension or cron jobs           |
| Avoid > 200 partitions           | Planner overhead increases with partition count |

---
