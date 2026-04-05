# Database Architecture

**Category:** Backend Infrastructure
**Owner:** Backend Chapter Lead (Dev Malhotra)

## Overview

Designs and manages PostgreSQL database architectures at scale, implementing table partitioning strategies, read replica topologies, connection pooling with PgBouncer, and automated migration pipelines. Covers data consistency patterns for distributed systems and the realities of implementing distributed transactions across microservices.

## Competency Dimensions

| Dimension                | Description                                                  | Proficiency Indicators                                                                                                            |
| ------------------------ | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| PostgreSQL Partitioning  | Range, list, and hash partitioning strategies                | Selects partitioning strategy based on query patterns; designs partition pruning-compatible queries; manages partition lifecycle  |
| Read Replicas            | Replica topology, replication lag management, read routing   | Configures streaming replication; implements read/write splitting with lag-aware routing; handles replica failover                |
| Connection Pooling       | PgBouncer configuration, pool modes, connection lifecycle    | Selects pool mode (transaction vs session) per workload; tunes pool sizes based on connection utilization metrics                 |
| Migration Strategies     | Flyway/Liquibase schema management, zero-downtime migrations | Designs backward-compatible migrations; implements expand/contract pattern; handles large table migrations without locks          |
| Data Consistency         | ACID guarantees, isolation levels, anomaly detection         | Selects isolation level per workload; implements application-level consistency checks; detects and resolves replication anomalies |
| Distributed Transactions | 2PC, saga-based compensation, eventual consistency           | Understands 2PC limitations; implements saga pattern for cross-service transactions; designs idempotent compensation actions      |

## Execution Guidance

### Table Partitioning Strategies

**Range Partitioning** — time-series data, log tables:

```sql
CREATE TABLE events (
    id UUID DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, created_at)  -- Partition key must be in PK
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE events_2026_01 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE events_2026_02 PARTITION OF events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- Default partition for out-of-range data (PostgreSQL 11+)
CREATE TABLE events_default PARTITION OF events DEFAULT;
```

**List Partitioning** — categorical data, multi-tenant:

```sql
CREATE TABLE tenant_data (
    id BIGSERIAL,
    tenant_id VARCHAR(36) NOT NULL,
    data JSONB,
    PRIMARY KEY (id, tenant_id)
) PARTITION BY LIST (tenant_id);

CREATE TABLE tenant_data_acme PARTITION OF tenant_data
    FOR VALUES IN ('acme-corp-uuid');
CREATE TABLE tenant_data_globex PARTITION OF tenant_data
    FOR VALUES IN ('globex-inc-uuid');
```

**Hash Partitioning** — uniform data distribution, load spreading:

```sql
CREATE TABLE user_sessions (
    user_id UUID NOT NULL,
    session_id UUID NOT NULL,
    data JSONB,
    PRIMARY KEY (user_id, session_id)
) PARTITION BY HASH (user_id);

CREATE TABLE user_sessions_p0 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE user_sessions_p1 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE user_sessions_p2 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE user_sessions_p3 PARTITION OF user_sessions
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

**Partitioning strategy decision matrix:**

| Query Pattern             | Strategy | Partition Key           | Rationale                           |
| ------------------------- | -------- | ----------------------- | ----------------------------------- |
| Time-range scans          | Range    | Timestamp column        | Prunes partitions efficiently       |
| Multi-tenant isolation    | List     | Tenant ID               | Physical data separation per tenant |
| Uniform load distribution | Hash     | High-cardinality column | Even distribution across partitions |
| Geographical routing      | List     | Region code             | Co-locates data by access pattern   |

### Read Replica Configuration

**Streaming replication setup:**

```postgresql
# postgresql.conf (primary)
wal_level = replica
max_wal_senders = 10
wal_keep_size = 1GB
synchronous_commit = on          -- For critical data
# synchronous_commit = remote_apply  -- Stronger: wait for replica apply

# postgresql.conf (replica)
hot_standby = on
hot_standby_feedback = on        -- Prevents vacuum conflicts
```

**Read/write splitting with lag-aware routing (Go):**

```go
type ReplicaRouter struct {
    primary    *sql.DB
    replicas   []Replica
    maxLag     time.Duration
}

type Replica struct {
    db     *sql.DB
    checker *LagChecker
}

func (r *ReplicaRouter) GetReadDB(ctx context.Context) (*sql.DB, error) {
    // Find replica with acceptable lag
    for _, replica := range r.replicas {
        lag, err := replica.checker.GetReplicationLag(ctx)
        if err == nil && lag < r.maxLag {
            return replica.db, nil
        }
    }
    // Fall back to primary if all replicas are behind
    return r.primary, nil
}

// Lag check query (PostgreSQL 12+)
const replicationLagQuery = `
    SELECT EXTRACT(EPOCH FROM replay_lag)::float
    FROM pg_stat_replication
    WHERE state = 'streaming'
    ORDER BY replay_lag DESC
    LIMIT 1;
`
```

**Replication lag monitoring alert:**

```yaml
# Prometheus alerting rule
- alert: ReplicationLagHigh
  expr: pg_replication_lag_seconds > 30
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Replica {{ $labels.instance }} lagging by {{ $value }}s"
    description: "Read queries may return stale data. Consider routing to primary."
```

### PgBouncer Connection Pooling

**Configuration modes:**

| Mode        | Behavior                                          | Use Case                                                         | Risk                            |
| ----------- | ------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------- |
| Session     | One server connection per client session          | Applications using session-level features (temp tables, PREPARE) | Higher connection count         |
| Transaction | Server connection released after each transaction | Stateless microservices (most common)                            | Cannot use session features     |
| Statement   | Server connection released after each statement   | Simple query-only workloads                                      | No multi-statement transactions |

**Production pgbouncer.ini:**

```ini
[databases]
app_db = host=primary-db port=5432 dbname=app_db

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt

pool_mode = transaction
max_client_conn = 5000
default_pool_size = 50
min_pool_size = 10
reserve_pool_size = 10
reserve_pool_timeout = 3

# Connection lifetime limits
server_lifetime = 3600          -- Max 1 hour per server connection
server_idle_timeout = 600       -- Release idle connections after 10 min
server_connect_timeout = 15     -- Timeout for new connections
server_login_retry = 15

# Query timeout
query_timeout = 30
query_wait_timeout = 120
client_idle_timeout = 0         -- Disabled (app handles idle)

# Logging
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1
stats_period = 60

admin_users = pgbouncer_admin
stats_users = monitoring
```

**Pool sizing formula:**

```
pool_size = (max_connections / num_apps) * safety_factor

Where:
  max_connections = PostgreSQL max_connections (typically 200-500)
  num_apps = number of applications sharing the pool
  safety_factor = 1.2 (20% headroom)

Example: 200 max_connections, 3 apps, 1.2 safety factor
  pool_size = (200 / 3) * 1.2 = 80
  Set default_pool_size = 80
```

### Zero-Downtime Migration Strategy (Expand/Contract)

```
Phase 1 — EXPAND: Add new column/table, write to both
  ALTER TABLE users ADD COLUMN email_normalized VARCHAR(255);
  -- Deploy code that writes to BOTH old and new columns
  -- Backfill existing data in batches

Phase 2 — CUTOVER: Switch reads to new column
  -- Deploy code that reads from new column
  -- Verify no regressions

Phase 3 — CONTRACT: Remove old column
  ALTER TABLE users DROP COLUMN email;
  -- Deploy code that no longer writes to old column
```

**Large table migration without locks (using pg_repack or manual approach):**

```sql
-- Manual approach: create new table, swap with minimal lock
CREATE TABLE users_new (LIKE users INCLUDING ALL);

-- Backfill in batches (doesn't hold long locks)
INSERT INTO users_new SELECT * FROM users WHERE id BETWEEN 1 AND 100000;
-- ... repeat for each batch ...

-- Create triggers to capture new writes during cutover
CREATE TRIGGER sync_to_new AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION sync_users_to_new();

-- Final sync of remaining changes
-- ...

-- Atomic swap (holds AccessExclusiveLock briefly)
BEGIN;
ALTER TABLE users RENAME TO users_old;
ALTER TABLE users_new RENAME TO users;
COMMIT;

-- Drop old table after verification
DROP TABLE users_old;
```

### Distributed Transactions: Reality Check

**Two-Phase Commit (2PC) — use sparingly:**

```sql
-- PostgreSQL prepared transactions
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
PREPARE TRANSACTION 'tx_001';

-- On coordinator, if all participants prepared:
COMMIT PREPARED 'tx_001';

-- On failure:
ROLLBACK PREPARED 'tx_001';
```

**Why 2PC is rarely the right answer:**

- Blocks resources until all participants commit or rollback
- Coordinator failure leaves transactions in-doubt
- Significantly reduces throughput
- Does not work across heterogeneous databases

**Preferred approach: Saga pattern with compensating transactions:**

See `distributed-systems.md` for saga implementation details. The key principle: design for eventual consistency with explicit compensation paths rather than attempting distributed ACID guarantees.

**When 2PC IS appropriate:**

- Single database, multiple schemas (PostgreSQL dblink/foreign data wrapper)
- Financial systems requiring strict atomicity within a single RDBMS
- Short-lived transactions (< 1 second expected duration)

## Pipeline Integration

**Stage 3 (UML Engineering Package):** Data model diagrams must show partitioning strategy, replica topology, and migration approach. ADR required for partitioning strategy selection and connection pooling mode.

**Stage 4 (Implementation Plan):** Migration tasks must include expand/contract phases with deployment sequencing. PgBouncer provisioning is infrastructure dependency for all services.

**Stage 5 (Development):** Database schemas implemented via migration tool. Read/write splitting code validated against replica topology. Connection pool sizes tuned based on load test data.

**Stage 6 (Code Review):** Review migration scripts for backward compatibility. Validate query plans against partitioned tables (partition pruning verification). Check connection pool configuration against capacity estimates.

**Stage 7 (Testing):** Performance tests validate partition pruning effectiveness. Failover tests validate read replica promotion. Load tests validate PgBouncer pool behavior under contention.

**Stage 8 (Integrity Verification):** Panel verifies data model matches implementation, migration strategy supports zero-downtime deployment, and connection pooling configuration supports peak load projections.

## Quality Standards

| Metric                          | Target                                                     | Measurement                 |
| ------------------------------- | ---------------------------------------------------------- | --------------------------- |
| Query performance (partitioned) | Partition pruning hits > 95%                               | EXPLAIN ANALYZE audit       |
| Replication lag (p95)           | < 1 second                                                 | pg_stat_replication         |
| Connection pool utilization     | 60-80% average                                             | PgBouncer stats             |
| Migration zero-downtime         | 100% of schema changes                                     | Deployment audit            |
| Data consistency (replicas)     | < 0.1% stale read rate                                     | Application-level checksums |
| Index efficiency                | All queries use index scans (no seq scans on large tables) | pg_stat_user_tables         |
| Backup recovery time (RTO)      | < 15 minutes                                               | DR drill results            |
| Backup data loss (RPO)          | < 1 minute                                                 | WAL archiving verification  |
