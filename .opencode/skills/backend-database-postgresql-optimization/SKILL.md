---
name: backend-database-postgresql-optimization
description: PostgreSQL performance optimization — query execution plan analysis, index strategies (B-tree, GIN, GiST, BRIN), connection pooling with PgBouncer, autovacuum tuning, and partition pruning. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 5 (Development) for query optimization and Stage 7 (Testing) for performance benchmarking. Trigger: postgresql optimization, query tuning, index strategy, pg_bouncer, autovacuum, partition pruning, slow query.
prerequisites:
  - backend-database-postgresql-basics

version: "1.0.0"
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
| Backend Skill Index               | `.opencode/skills/backend-overview/SKILL.md`                  |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`index-strategies.md`](references/index-strategies.md) — Index Strategies
- [`vacuum-management.md`](references/vacuum-management.md) — Vacuum Management
- [`partitioning.md`](references/partitioning.md) — Partitioning
- [`configuration-tuning.md`](references/configuration-tuning.md) — Configuration Tuning
- [`monitoring-&-diagnostics.md`](references/monitoring-&-diagnostics.md) — Monitoring & Diagnostics
- [`stage-8-integration.md`](references/stage-8-integration.md) — Stage 8 Integration
