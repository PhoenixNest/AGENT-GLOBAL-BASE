---
name: postgresql-optimization
description: This skill covers systematic approaches to PostgreSQL performance optimization across six domains: | Domain | Primary Focus | | ------------------------ | ---------------------------------------- |...
---

# PostgreSQL Optimization

## Overview

This skill covers systematic approaches to PostgreSQL performance optimization across six domains:

| Domain                   | Primary Focus                            |
| ------------------------ | ---------------------------------------- |
| Query Optimization       | Execution plans, anti-patterns, rewrites |
| Index Strategies         | B-tree, GIN, GiST, BRIN selection        |
| Connection Pooling       | PgBouncer modes and configuration        |
| Vacuum Management        | Autovacuum tuning and bloat prevention   |
| Partitioning             | Declarative partitioning by range/list   |
| Configuration Tuning     | shared_buffers, work_mem, and beyond     |
| Monitoring & Diagnostics | pg_stat_statements, pg_stat_user_tables  |
| Stage 8 Integration      | Performance verification in pipeline     |

**Principles:**

- **Measure before changing** — baseline first, then optimize
- **One variable at a time** — isolate each tuning parameter
- **Index last, not first** — fix query structure before adding indexes
- **Monitor continuously** — optimization is not a one-time activity

---

## Query Optimization

### EXPLAIN ANALYZE

`EXPLAIN ANALYZE` executes the query and shows actual row counts, timing, and execution plan.

```sql
-- Basic usage
EXPLAIN ANALYZE
SELECT u.id, u.email, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2025-01-01'
GROUP BY u.id, u.email;
```

**Key output fields:**

| Field                   | Meaning                                         |
| ----------------------- | ----------------------------------------------- |
| `Seq Scan`              | Full table scan — often indicates missing index |
| `Index Scan`            | Index lookup with table fetch                   |
| `Index Only Scan`       | Index covers all needed columns (fastest)       |
| `Bitmap Heap Scan`      | Bitmap index scan followed by heap fetch        |
| `Nested Loop`           | Efficient for small outer rows, bad for large   |
| `Hash Join`             | Good for large unsorted datasets                |
| `Merge Join`            | Requires sorted input, efficient for large sets |
| `actual rows` vs `rows` | Large mismatch = stale statistics, run ANALYZE  |

**Performance thresholds:**

| Metric                          | Warning | Critical    |
| ------------------------------- | ------- | ----------- |
| Total query time                | > 100ms | > 1s        |
| Rows planned vs actual ratio    | > 10x   | > 100x      |
| Sequential scans on large table | Any     | > 1000 rows |
| Temporary file on disk          | Any     | > work_mem  |

### Common Anti-Patterns

**Anti-pattern 1: SELECT \* in joins**

```sql
-- BAD: pulls all columns from both tables
SELECT * FROM users u JOIN orders o ON o.user_id = u.id;

-- GOOD: project only needed columns
SELECT u.id, u.email, o.total, o.created_at
FROM users u JOIN orders o ON o.user_id = u.id;
```

**Anti-pattern 2: N+1 query pattern**

```sql
-- BAD: one query per user (application loop)
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
SELECT * FROM orders WHERE user_id = 3;

-- GOOD: single query with IN clause
SELECT * FROM orders WHERE user_id IN (1, 2, 3);
```

**Anti-pattern 3: Function on indexed column**

```sql
-- BAD: prevents index usage on created_at
SELECT * FROM orders WHERE DATE(created_at) = '2025-06-01';

-- GOOD: use range comparison (index-compatible)
SELECT * FROM orders
WHERE created_at >= '2025-06-01' AND created_at < '2025-06-02';
```

**Anti-pattern 4: Implicit type casting**

```sql
-- BAD: varchar column compared to integer — causes seq scan
SELECT * FROM users WHERE phone = 1234567890;

-- GOOD: match column type
SELECT * FROM users WHERE phone = '1234567890';
```

**Anti-pattern 5: OR conditions that prevent index usage**

```sql
-- BAD: OR on different columns often prevents index usage
SELECT * FROM users WHERE email = 'test@example.com' OR phone = '123456';

-- GOOD: rewrite as UNION (each branch can use its own index)
SELECT * FROM users WHERE email = 'test@example.com'
UNION
SELECT * FROM users WHERE phone = '123456';
```

### Subquery vs JOIN

```sql
-- Subquery (often slower, executes per-row)
SELECT u.email
FROM users u
WHERE u.id IN (SELECT user_id FROM orders WHERE total > 100);

-- JOIN with DISTINCT (often faster, single scan)
SELECT DISTINCT u.email
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.total > 100;

-- EXISTS (best for existence checks, stops at first match)
SELECT u.email
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id AND o.total > 100
);
```

---

## Index Strategies

### Index Type Selection

| Index Type | Best For                                  | Use Case Example                       |
| ---------- | ----------------------------------------- | -------------------------------------- |
| B-tree     | Equality, range, ORDER BY, LIKE 'prefix%' | Primary keys, timestamps, emails       |
| GIN        | Full-text search, arrays, JSONB           | Search, tags, metadata fields          |
| GiST       | Geometric, full-text, range overlap       | GIS, IP ranges, exclusion constraints  |
| BRIN       | Large tables with correlation             | Time-series, log data, partitions      |
| Hash       | Equality only (rarely needed)             | Simple lookups (B-tree usually better) |

### B-tree Indexes (Default)

```sql
-- Single column index
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index (column order matters — most selective first)
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);

-- Partial index (smaller, faster — only index active rows)
CREATE INDEX idx_orders_pending ON orders(created_at)
WHERE status = 'pending';

-- Covering index (Index Only Scan — no heap fetch needed)
CREATE INDEX idx_orders_covering ON orders(user_id)
INCLUDE (total, status, created_at);
```

**Composite index rules:**

- Equality columns first, then range columns
- The leftmost prefix of a composite index can be used independently
- `WHERE a = 1 AND b > 10 AND c = 'x'` → index on `(a, c, b)` is better than `(a, b, c)`

### GIN Indexes (JSONB, Full-Text, Arrays)

```sql
-- JSONB containment queries
CREATE INDEX idx_users_metadata ON users USING GIN (metadata);
SELECT * FROM users WHERE metadata @> '{"premium": true}';

-- Full-text search
CREATE INDEX idx_articles_search ON articles USING GIN (to_tsvector('english', body));
SELECT * FROM articles
WHERE to_tsvector('english', body) @@ plainto_tsquery('english', 'database optimization');

-- Array containment
CREATE INDEX idx_users_tags ON users USING GIN (tags);
SELECT * FROM users WHERE tags @> ARRAY['admin', 'active'];
```

### GiST Indexes

```sql
-- Geographic queries (PostGIS)
CREATE INDEX idx_locations_geom ON locations USING GiST (geom);
SELECT * FROM locations WHERE ST_DWithin(geom, ST_Point(106.8, -6.2), 5000);

-- Range overlap detection
CREATE INDEX idx_bookings_range ON bookings USING GiST (booking_period);
SELECT * FROM bookings WHERE booking_period && '[2025-06-01, 2025-06-07]';

-- Exclusion constraint (prevent overlapping bookings)
ALTER TABLE bookings
ADD CONSTRAINT no_overlap
EXCLUDE USING GiST (room_id WITH =, booking_period WITH &&);
```

### BRIN Indexes (Block Range INdexes)

```sql
-- Ideal for large time-series tables (millions of rows)
-- Very small index footprint compared to B-tree
CREATE INDEX idx_events_time ON events USING BRIN (created_at);

-- Only effective when data is physically ordered by the indexed column
-- Check correlation:
SELECT attname, correlation
FROM pg_stats
WHERE tablename = 'events' AND attname = 'created_at';
-- Correlation close to 1 or -1 = good for BRIN
```

### Index Maintenance

```sql
-- Find unused indexes (waste space and slow down writes)
SELECT
    schemaname, relname, indexrelname, idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Find duplicate indexes
SELECT
    a.indexrelid::regclass AS index_name,
    b.indexrelid::regclass AS duplicate_of,
    a.indrelid::regclass AS table_name
FROM pg_index a
JOIN pg_index b ON a.indrelid = b.indrelid AND a.indexrelid != b.indexrelid
WHERE a.indkey::text = b.indkey::text
    AND a.indpred IS NOT DISTINCT FROM b.indpred;

-- Remove an unused index
DROP INDEX CONCURRENTLY idx_unused_index;
```

---

## Connection Pooling

### PgBouncer Modes

| Mode            | Behavior                                          | Best For               |
| --------------- | ------------------------------------------------- | ---------------------- |
| **Session**     | One server connection per client session          | Long-lived connections |
| **Transaction** | Server connection per transaction                 | Most applications      |
| **Statement**   | Server connection per statement (no transactions) | Stateless services     |

### PgBouncer Configuration

```ini
; /etc/pgbouncer/pgbouncer.ini

[databases]
myapp = host=127.0.0.1 port=5432 dbname=myapp

[pgbouncer]
listen_port = 6432
listen_addr = 0.0.0.0
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

; Pooling mode — use transaction for most web apps
pool_mode = transaction

; Max connections from pgbouncer to PostgreSQL
default_pool_size = 25
max_client_conn = 500

; When all pool slots busy, queue extra clients (prevents errors)
reserve_pool_size = 5
reserve_pool_timeout = 3

; Kill idle client connections after 10 minutes
client_idle_timeout = 600

; Return idle server connections to pool after 30 seconds
server_idle_timeout = 30

; Close server connections older than 2 hours
server_lifetime = 7200

; Log slow queries for diagnostics
log_disconnections = 1
log_connections = 1
```

### Application-Side Pool Sizing

```
pool_size = (core_count * 2) + effective_spindle_count
```

For SSD/cloud databases (most common today):

| Tier           | Recommended pool_size | PgBouncer default_pool_size |
| -------------- | --------------------- | --------------------------- |
| Small (2 CPU)  | 10–15                 | 25                          |
| Medium (4 CPU) | 20–30                 | 25                          |
| Large (8 CPU)  | 40–60                 | 50                          |
| XL (16+ CPU)   | 80–120                | 100                         |

**Rule:** With PgBouncer in transaction mode, application pool size can exceed `max_connections` because PgBouncer multiplexes clients onto a smaller server pool.

### Connection Pool Health Checks

```sql
-- PgBouncer admin commands (connect to pgbouncer database)
SHOW pools;          -- active/idle/waiting connections per pool
SHOW clients;        -- all client connections
SHOW servers;        -- all server connections
SHOW stats;          -- aggregate statistics

-- Alert thresholds
-- waiting > 0 = pool exhausted, increase default_pool_size
-- server_idle > 2 * active = pool oversized
```

---

## Vacuum Management

### How Autovacuum Works

Autovacuum runs `VACUUM` and `ANALYZE` automatically to:

1. Reclaim dead tuple space from UPDATE/DELETE operations
2. Update table statistics for the query planner
3. Prevent transaction ID wraparound (catastrophic if missed)

**Trigger conditions:**

| Operation | Default Trigger Formula                            | Example (1M row table) |
| --------- | -------------------------------------------------- | ---------------------- |
| VACUUM    | `n_dead_tup > threshold + scale * n_live`          | > 50,200 dead tuples   |
| ANALYZE   | `n_mod_since_analyze > threshold + scale * n_live` | > 50,200 modifications |

Default: `autovacuum_vacuum_threshold = 50`, `autovacuum_vacuum_scale_factor = 0.2`

### Autovacuum Tuning

```sql
-- Recommended settings for production (postgresql.conf)
autovacuum = on
autovacuum_max_workers = 4              -- 3 default, increase for many tables
autovacuum_naptime = 10s                -- 60s default, check more frequently
autovacuum_vacuum_threshold = 50
autovacuum_vacuum_insert_threshold = 10000  -- for INSERT-only tables
autovacuum_vacuum_scale_factor = 0.05   -- 0.2 default, too high for large tables
autovacuum_analyze_threshold = 50
autovacuum_analyze_scale_factor = 0.02  -- 0.1 default, more frequent stats updates

-- Increase I/O budget (allows vacuum to work faster)
autovacuum_vacuum_cost_limit = 1000     -- 200 default, increase 5x
vacuum_cost_page_hit = 1                -- 1 default
vacuum_cost_page_miss = 10              -- 10 default
vacuum_cost_page_dirty = 20             -- 20 default
```

### Per-Table Override (High-Churn Tables)

```sql
-- Aggressive vacuum for orders table (high UPDATE/DELETE rate)
ALTER TABLE orders SET (
    autovacuum_vacuum_scale_factor = 0.01,
    autovacuum_vacuum_threshold = 100,
    autovacuum_analyze_scale_factor = 0.005,
    autovacuum_analyze_threshold = 50
);

-- Very large table that should rarely vacuum
ALTER TABLE audit_log SET (
    autovacuum_vacuum_scale_factor = 0.05,
    autovacuum_vacuum_threshold = 10000
);
```

### Diagnosing Bloat

```sql
-- Check dead tuple ratio across tables
SELECT
    schemaname,
    relname,
    n_live_tup,
    n_dead_tup,
    ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
    last_autovacuum,
    last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- dead_pct > 10% = investigate, > 30% = urgent
-- If last_autovacuum is NULL or very old = autovacuum is not keeping up

-- Manual vacuum for urgent cases (runs immediately, blocks nothing)
VACUUM ANALYZE orders;

-- Full vacuum (exclusive lock, use with caution)
-- VACUUM FULL orders;  -- rewrites table, blocks all access
```

---

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

## Configuration Tuning

### Memory Settings

```ini
# postgresql.conf — memory configuration

# shared_buffers: 25% of system RAM (up to 8GB, beyond that diminishing returns)
# 4GB RAM -> 1GB, 16GB RAM -> 4GB, 64GB RAM -> 8GB (cap at 8-12GB)
shared_buffers = 2GB

# effective_cache_size: estimate of OS disk cache available
# Set to 50-75% of total RAM
effective_cache_size = 12GB

# work_mem: per-operation memory for sorts, hashes, joins
# Total potential usage = work_mem * max_connections * operations
# Be conservative — this is PER operation, PER connection
work_mem = 64MB

# maintenance_work_mem: for VACUUM, CREATE INDEX, ALTER TABLE
# Can be large since few concurrent maintenance operations
maintenance_work_mem = 512MB

# huge_pages: try to reduce TLB pressure on large memory systems
huge_pages = try
```

### WAL and Durability

```ini
# Write-Ahead Log configuration

# wal_level: replica needed for streaming replication
wal_level = replica

# max_wal_senders: for replication and pg_basebackup
max_wal_senders = 5

# wal_buffers: auto-tuned from shared_buffers usually fine
# wal_buffers = -1  # default: auto-tune from shared_buffers (1/32, min 64kB)

# synchronous_commit: balance durability vs performance
# on = safe (default), off = ~1s data loss risk, 3x throughput gain
synchronous_commit = on

# checkpoint settings
checkpoint_completion_target = 0.9    -- spread checkpoint I/O over time
checkpoint_timeout = 15min            -- 5min default, increase for write-heavy
max_wal_size = 2GB                    -- 1GB default, increase for write-heavy
min_wal_size = 512MB                  -- 80MB default
```

### Query Planner Hints

```ini
# Enable/disable plan types (use as temporary diagnostics, not permanent fixes)
enable_seqscan = on          -- keep on; disabling seqscan rarely helps
enable_hashjoin = on
enable_nestloop = on
enable_bitmapscan = on

# Random page cost — lower for SSDs
random_page_cost = 1.1       -- 4.0 default (HDD), 1.1 for SSD/cloud

# Effective I/O concurrency — lower for cloud storage
effective_io_concurrency = 200  -- 1 default (HDD), 200 for SSD
```

---

## Monitoring & Diagnostics

### pg_stat_statements Extension

```sql
-- Enable extension (requires shared_preload_libraries = 'pg_stat_statements' in postgresql.conf)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 queries by total execution time
SELECT
    query,
    calls,
    ROUND(total_exec_time::numeric, 2) AS total_ms,
    ROUND(mean_exec_time::numeric, 2) AS avg_ms,
    rows,
    shared_blks_hit,
    shared_blks_read,
    ROUND(100.0 * shared_blks_hit / NULLIF(shared_blks_hit + shared_blks_read, 0), 2) AS cache_hit_pct
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Queries with worst average latency (potential optimization targets)
SELECT query, calls, ROUND(mean_exec_time::numeric, 2) AS avg_ms
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Low cache hit ratio queries (missing indexes or too-small shared_buffers)
SELECT query, cache_hit_pct, shared_blks_read
FROM (
    SELECT
        query,
        ROUND(100.0 * shared_blks_hit / NULLIF(shared_blks_hit + shared_blks_read, 0), 2) AS cache_hit_pct,
        shared_blks_read
    FROM pg_stat_statements
) sub
WHERE shared_blks_read > 10000
ORDER BY cache_hit_pct ASC;
-- cache_hit_pct < 95% = investigate, < 90% = critical
```

### Table-Level Statistics

```sql
-- Table access patterns (find hot tables)
SELECT
    relname,
    seq_scan,                    -- sequential scans (bad on large tables)
    idx_scan,                    -- index scans (good)
    n_tup_ins, n_tup_upd, n_tup_del,
    n_live_tup, n_dead_tup
FROM pg_stat_user_tables
ORDER BY seq_scan + idx_scan DESC;

-- Missing index candidates (high seq_scan, large tables)
SELECT
    relname,
    seq_scan,
    pg_size_pretty(pg_total_relation_size(relid)) AS table_size
FROM pg_stat_user_tables
WHERE seq_scan > 1000
    AND pg_total_relation_size(relid) > 10 * 1024 * 1024  -- > 10MB
ORDER BY seq_scan DESC;

-- Lock detection
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.query AS blocked_query,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.query AS blocking_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.relation = blocked_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

### Long-Running Query Detection

```sql
-- Queries running longer than 30 seconds
SELECT
    pid,
    now() - pg_stat_activity.query_start AS duration,
    state,
    query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '30 seconds'
    AND state != 'idle'
ORDER BY duration DESC;
```

---

## Stage 8 Integration

### Performance Verification in Integrity Gate

At **Stage 8 (Integrity Verification)**, the CTO panel must verify that performance requirements defined in the SRD (Stage 1) are met. PostgreSQL optimization is part of this verification.

**Stage 8 Performance Checklist:**

| Check                                                                 | SRD Reference | Pass/Fail |
| --------------------------------------------------------------------- | ------------- | --------- |
| All queries < 100ms p95 (or SRD-defined SLA)                          | SRD-00X       | [ ]       |
| No queries with cache_hit_pct < 95%                                   | SRD-00X       | [ ]       |
| All tables have appropriate indexes (no seq scans on >10K row tables) | SRD-00X       | [ ]       |
| Connection pool sizing matches deployment tier                        | SRD-00X       | [ ]       |
| Autovacuum keeping pace (dead tuple ratio < 5%)                       | SRD-00X       | [ ]       |
| No P0/P1 performance regressions vs baseline                          | —             | [ ]       |

### Performance Regression Test

```sql
-- Baseline query performance (run before and after changes)
-- Save results as performance baseline in project/testing/results/
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT /* baseline query */ ... ;

-- Compare before/after:
-- 1. Total execution time should not increase > 10%
-- 2. Row estimates should not diverge > 2x
-- 3. Buffer hit ratio should not decrease > 5%
-- 4. No new sequential scans on tables > 10K rows
```

**If performance degrades:**

1. Identify the regressed query via `pg_stat_statements`
2. Compare execution plans (EXPLAIN ANALYZE before vs after)
3. Check for: missing indexes, statistics staleness (run ANALYZE), configuration changes
4. **Do not** remove functionality to "fix" performance (trim-to-pass anti-pattern, Stage 8 guard)

---

## References

| Resource                          | Description                                                   |
| --------------------------------- | ------------------------------------------------------------- |
| PostgreSQL Documentation          | https://www.postgresql.org/docs/                              |
| Use The Index, Luke               | https://use-the-index-luke.com/                               |
| PgBouncer Documentation           | https://www.pgbouncer.org/                                    |
| pg_stat_statements Guide          | https://www.postgresql.org/docs/current/pgstatstatements.html |
| pg_partman (partition management) | https://github.com/pgpartman/pg_partman                       |
| postgresqltuner                   | https://github.com/jfcoz/postgresqltuner                      |
| PGTune                            | https://pgtune.leopard.in.ua/                                 |
| EXPLAIN Visualizer                | https://explain.dalibo.com/                                   |
| Backend Skill Index               | `.cursor/skills/backend/SKILL.md`                             |
