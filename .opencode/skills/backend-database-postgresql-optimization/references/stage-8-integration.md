# Stage 8 Integration

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
