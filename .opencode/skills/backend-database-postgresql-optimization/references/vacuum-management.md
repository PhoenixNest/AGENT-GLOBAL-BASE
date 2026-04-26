# Vacuum Management

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
