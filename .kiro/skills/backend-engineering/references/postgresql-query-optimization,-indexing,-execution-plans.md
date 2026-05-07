---
name: postgresql-optimization
description: Optimize PostgreSQL database performance — index design, query plan analysis, connection pooling, and partitioning strategy — targeting sub-100ms p95 query latency for the company's backend API workloads.
version: "1.0.0"
---

# Postgresql Optimization

| Competency          | Description                                                         | Quality Criteria                                                                                                           |
| ------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Query Plan Analysis | Use EXPLAIN ANALYZE to diagnose slow queries and index utilization  | Identifies seq scans on large tables; rewrites queries to use index scans; achieves ≥ 10× improvement on diagnosed queries |
| Index Design        | Design B-tree, GIN, and partial indexes for query access patterns   | Index design matches actual query WHERE clauses; composite index column order matches query filter selectivity             |
| Connection Pooling  | Configure PgBouncer for session/transaction/statement pooling modes | PgBouncer configured in transaction mode for web workloads; max_client_conn tuned to app concurrency                       |
| Partitioning        | Implement range and list partitioning for large tables              | Partition pruning verified in EXPLAIN output; maintenance windows for partition creation documented                        |

## Execution Guidance

### Query Optimization Workflow

1. Identify slow queries from `pg_stat_statements` (order by `total_exec_time DESC`).
2. Run `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` on each top-10 query.
3. Look for: Seq Scan on tables > 10K rows, Hash Join on large tables without filter, missing index conditions.
4. Create indexes in a non-blocking manner: `CREATE INDEX CONCURRENTLY`.
5. Monitor `pg_stat_user_indexes` for unused indexes (waste write amplification).

### Key Performance Targets

| Metric                      | Target                   |
| --------------------------- | ------------------------ |
| Read query p95 latency      | < 50 ms                  |
| Write query p95 latency     | < 100 ms                 |
| Connection pool utilization | < 80% at peak            |
| Index hit ratio             | > 99%                    |
| Cache hit ratio             | > 95% (`shared_buffers`) |
