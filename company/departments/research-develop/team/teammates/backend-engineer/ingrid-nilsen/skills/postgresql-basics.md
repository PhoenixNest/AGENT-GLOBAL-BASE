---
version: "1.0.0"
---

# Postgresql Basics

| Competency            | Description                                                                              | Quality Criteria                                                                                                                                           |
| --------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SQL Fundamentals      | JOINs (INNER, LEFT, RIGHT, FULL, CROSS), subqueries, CTEs, window functions              | Writes complex queries with CTEs instead of nested subqueries; uses window functions for ranking/aggregation; understands JOIN order impact on performance |
| Indexing              | B-tree, GIN, GiST, partial indexes, covering indexes, composite index column order       | Selects appropriate index type per query pattern; designs composite indexes with correct column order; uses EXPLAIN to verify index usage                  |
| Query Optimization    | EXPLAIN ANALYZE interpretation, sequential vs index scans, join strategies               | Reads and interprets query plans; identifies slow operations (seq scans, nested loops on large tables); optimizes queries based on plan analysis           |
| Transaction Isolation | Read Uncommitted, Read Committed, Repeatable Read, Serializable                          | Selects isolation level based on consistency requirements; understands PostgreSQL's MVCC implementation; handles serialization failures                    |
| Alembic Migrations    | Migration generation, upgrade/downgrade scripts, data migrations, environment management | Writes reversible migrations; handles data migrations separately from schema changes; manages migration ordering and dependencies                          |

## Execution Guidance

### SQL Fundamentals

**JOIN types and when to use them:**

```sql
-- INNER JOIN: only matching rows (most common)
SELECT u.name, o.total_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= NOW() - INTERVAL '30 days';

-- LEFT JOIN: all left rows, matching right rows (NULL if no match)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Anti-join pattern: find users with NO orders
SELECT u.name
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;

-- CTE (Common Table Expression): readable complex queries
WITH recent_orders AS (
    SELECT user_id, SUM(total_amount) as total_spent
    FROM orders
    WHERE created_at >= NOW() - INTERVAL '30 days'
    GROUP BY user_id
),
top_spenders AS (
    SELECT user_id, total_spent,
           RANK() OVER (ORDER BY total_spent DESC) as ranking
    FROM recent_orders
)
SELECT u.name, ts.total_spent, ts.ranking
FROM top_spenders ts
JOIN users u ON u.id = ts.user_id
WHERE ts.ranking <= 10;

-- Window functions: ranking without grouping
SELECT
    name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    AVG(salary) OVER (PARTITION BY department) as dept_avg_salary
FROM employees;

-- LATERAL JOIN: correlated subqueries that return multiple rows
SELECT u.name, latest_orders.*
FROM users u
CROSS JOIN LATERAL (
    SELECT o.id, o.total_amount, o.created_at
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY o.created_at DESC
    LIMIT 3
) latest_orders;
```

### Indexing Strategies

**B-tree index (default) — equality and range queries:**

```sql
-- Single column index
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index — column order matters!
-- Most selective column first, or column used in WHERE clause first
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);

-- This query uses the composite index efficiently:
SELECT * FROM orders
WHERE user_id = 'user-123'
ORDER BY created_at DESC
LIMIT 10;

-- This query ALSO uses the index (leftmost prefix):
SELECT * FROM orders WHERE user_id = 'user-123';

-- This query does NOT use the composite index efficiently:
SELECT * FROM orders WHERE created_at >= '2026-01-01';
-- (needs separate index on created_at)

-- Partial index — only index a subset of rows
CREATE INDEX idx_orders_pending ON orders(user_id, created_at DESC)
WHERE status = 'pending';
-- Smaller index, faster writes, perfect for filtered queries

-- Covering index (INCLUDE) — avoids table lookup for selected columns
CREATE INDEX idx_orders_user_covering ON orders(user_id)
INCLUDE (total_amount, status);
-- Query can be satisfied entirely from index (index-only scan)
SELECT user_id, total_amount, status
FROM orders WHERE user_id = 'user-123';
```

**GIN index — full-text search, JSONB, arrays:**

```sql
-- GIN index for JSONB containment queries
CREATE INDEX idx_users_metadata_gin ON users USING GIN (metadata);

-- This query uses the GIN index:
SELECT * FROM users WHERE metadata @> '{"premium": true}';

-- GIN index for full-text search
CREATE INDEX idx_posts_search ON posts USING GIN (
    to_tsvector('english', title || ' ' || body)
);

-- Full-text search query
SELECT title, ts_rank(
    to_tsvector('english', title || ' ' || body),
    query
) as rank
FROM posts, to_tsquery('english', 'database & performance') query
WHERE to_tsvector('english', title || ' ' || body) @@ query
ORDER BY rank DESC;

-- GIN index for array columns
CREATE INDEX idx_posts_tags_gin ON posts USING GIN (tags);
SELECT * FROM posts WHERE tags && ARRAY['postgresql', 'performance'];
```

**Composite index column order decision:**

```
Rule: For WHERE a = ? AND b > ? ORDER BY c:
  Index on (a, b, c) — equality first, then range, then sort

Rule: For WHERE a = ? OR b = ?:
  Separate indexes on (a) and (b) — composite index won't help OR

Rule: For WHERE a = ? AND b = ? with different selectivity:
  Put most selective column first (reduces rows scanned faster)

Exception: If queries always filter on both, order by cardinality
(lowest cardinality first = fewer distinct index entries)
```

### EXPLAIN ANALYZE

```sql
-- EXPLAIN: shows planned execution (no execution)
EXPLAIN SELECT * FROM orders WHERE user_id = 'user-123';

-- EXPLAIN ANALYZE: executes query and shows actual performance
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id)
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Reading EXPLAIN ANALYZE output:
/*
Nested Loop Left Join  (cost=0.29..125.42 rows=1000 width=48) (actual time=0.045..2.341 rows=1500 loops=1)
  ->  Seq Scan on users u  (cost=0.00..25.00 rows=500 width=32) (actual time=0.012..0.234 rows=500 loops=1)
  ->  Index Scan using idx_orders_user_id on orders o  (cost=0.29..1.50 rows=3 width=20) (actual time=0.002..0.003 rows=3 loops=500)
        Index Cond: (user_id = u.id)
Planning Time: 0.156 ms
Execution Time: 2.567 ms
*/

-- Key metrics to look for:
-- 1. Seq Scan on large table (> 1000 rows) → consider index
-- 2. Nested Loop with high loops count → consider hash join or index
-- 3. actual rows >> estimated rows → run ANALYZE to update statistics
-- 4. Execution Time > 100ms for simple queries → investigate
-- 5. Shared Hit Blocks vs Shared Read Blocks → cache efficiency

-- Update statistics (run after large data changes)
ANALYZE orders;
ANALYZE VERBOSE orders;  -- Shows what it analyzed

-- Check table statistics
SELECT schemaname, relname, last_analyze, last_autoanalyze
FROM pg_stat_user_tables
WHERE relname = 'orders';

-- Check index usage (find unused indexes)
SELECT schemaname, relname, indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
-- Low idx_scan = candidate for removal (but verify first!)
```

### Transaction Isolation Levels

```sql
-- PostgreSQL isolation levels (note: Read Uncommitted = Read Committed in PG)

-- Default: Read Committed (each statement sees committed data)
-- Suitable for: Most application queries
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Repeatable Read: all statements in transaction see same snapshot
-- Suitable for: Reports, analytics, batch processing
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Serializable: strictest, prevents all anomalies
-- Suitable for: Financial transactions, critical data integrity
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Handling serialization failures:
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Your transactional work here...
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;
-- If serialization failure occurs:
-- ERROR: could not serialize access due to concurrent update
-- Application should retry the entire transaction

-- Optimistic locking pattern (alternative to Serializable):
UPDATE orders
SET status = 'shipped', version = version + 1
WHERE id = 'order-123' AND version = 5;
-- If no rows affected, someone else updated first — handle conflict
```

**Isolation level decision matrix:**

| Scenario               | Level                              | Rationale                              |
| ---------------------- | ---------------------------------- | -------------------------------------- |
| Simple CRUD operations | Read Committed (default)           | Good enough for most cases             |
| Read-heavy reports     | Repeatable Read                    | Consistent snapshot throughout report  |
| Financial transfers    | Serializable or optimistic locking | Prevents lost updates                  |
| Counter increments     | Explicit locking or atomic updates | `UPDATE ... SET counter = counter + 1` |
| Multi-row consistency  | Repeatable Read or Serializable    | All reads see same snapshot            |

### Alembic Migrations

```python
# alembic.ini
[alembic]
script_location = migrations
sqlalchemy.url = postgresql://user:pass@localhost:5432/app_db

# env.py — configure for async SQLAlchemy
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from app.models import Base  # Import all models

config = context.config
target_metadata = Base.metadata

def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def run_async_migrations(connection):
        await connection.run_sync(do_run_migrations)

    async def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detect column type changes
        )
        with context.begin_transaction():
            context.run_migrations()

    async def run():
        async with connectable.connect() as connection:
            await run_async_migrations(connection)
        await connectable.dispose()

    import asyncio
    asyncio.run(run())

context.config = config

# Generate migration (auto-detects model changes)
# alembic revision --autogenerate -m "add_users_table"

# migrations/versions/001_add_users_table.py
"""add users table

Revision ID: 001
Revises:
Create Date: 2026-04-04
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='user'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

def downgrade():
    op.drop_index('idx_users_email', 'users')
    op.drop_table('users')

# Data migration (separate from schema changes)
def upgrade():
    # Schema change
    op.add_column('users', sa.Column('email_normalized', sa.String(255)))

    # Data migration
    conn = op.get_bind()
    conn.execute(sa.text(
        "UPDATE users SET email_normalized = LOWER(email)"
    ))

    # Then make it required
    op.alter_column('users', 'email_normalized', nullable=False)

def downgrade():
    op.drop_column('users', 'email_normalized')
```

**Migration best practices:**

```
1. Always write reversible migrations (both upgrade() and downgrade())
2. Schema changes and data changes in separate migrations
3. Test downgrade before deploying upgrade
4. For large data migrations, use batched updates:

   UPDATE users SET email_normalized = LOWER(email)
   WHERE id IN (SELECT id FROM users WHERE email_normalized IS NULL LIMIT 10000);
   -- Repeat until all rows updated

5. Use server_default for new NOT NULL columns on existing tables:

   op.add_column('orders', sa.Column(
       'status', sa.String(20), nullable=False, server_default='pending'
   ))

6. For zero-downtime deployments, use expand/contract pattern:
   - Migration 1: ADD COLUMN (nullable)
   - Deploy code that writes to both old and new
   - Migration 2: Backfill data
   - Deploy code that reads from new
   - Migration 3: DROP old column, make new NOT NULL
```

## Pipeline Integration

**Stage 5 (Development):** All database queries reviewed for index usage. Migrations written and tested. EXPLAIN ANALYZE run on complex queries.

**Stage 6 (Code Review):** Review query patterns for efficiency. Validate index appropriateness. Check migration reversibility. Verify isolation level selection.

**Stage 7 (Testing):** Integration tests validate migrations run correctly. Query performance tests validate index usage under load. Transaction isolation tests verify concurrency behavior.

## Quality Standards

| Metric                                    | Target                                      | Measurement           |
| ----------------------------------------- | ------------------------------------------- | --------------------- |
| Query plan (no seq scans on large tables) | 0 sequential scans on tables > 10K rows     | EXPLAIN ANALYZE audit |
| Index usage                               | All indexes used by at least one query      | pg_stat_user_indexes  |
| Migration reversibility                   | 100% of migrations have working downgrade() | Migration test suite  |
| Query latency (p95)                       | < 50ms for indexed queries                  | Application metrics   |
| Deadlock rate                             | 0 deadlocks in normal operation             | PostgreSQL logs       |
| Connection pool utilization               | 60-80% average                              | PgBouncer stats       |
