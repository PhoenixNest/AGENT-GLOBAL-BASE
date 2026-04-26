# Index Strategies

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
