# Monitoring & Diagnostics

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
