# Performance Benchmark Report

**Project:** [Project Name]
**Runtime:** [Go / Node.js / Python / Java]
**Author:** [Backend Lead / Performance Engineer]
**Date:** YYYY-MM-DD
**Version:** v1
**Referenced Artifacts:** PRD v1 (Performance Thresholds), TEST-RESULTS-REPORT.md v1

---

## Purpose

Verifies that the implemented API meets the performance SLAs defined in the PRD. This report is a **mandatory Stage 7 gate input** -- all PRD performance thresholds must be verified before advancing to Stage 8.

---

## 1. PRD Performance Thresholds

| Metric                        | PRD Target | Measurement Method                          | Result   | Pass/Fail       |
| ----------------------------- | ---------- | ------------------------------------------- | -------- | --------------- |
| P99 latency                   | [<500ms]   | [k6 / wrk --p99 of response times]          | [XXXms]  | Pass / Fail     |
| P95 latency                   | [<300ms]   | [k6 / wrk --p95 of response times]          | [XXXms]  | Pass / Fail     |
| P50 latency                   | [<100ms]   | [k6 / wrk --median response time]           | [XXXms]  | Pass / Fail     |
| Throughput (sustained)        | [>1000 rps]| [k6 -- constant VUs for 5 minutes]          | [N rps]  | Pass / Fail     |
| Throughput (peak)             | [>5000 rps]| [k6 -- spike test]                          | [N rps]  | Pass / Fail     |
| Error rate                    | [<0.1%]    | [HTTP 5xx / total requests]                 | [X.XX%]  | Pass / Fail     |
| Connection pool utilization   | [<80%]     | [Active connections / max pool size]        | [XX%]    | Pass / Fail     |
| DB query P99                  | [<100ms]   | [Database slow query log / pg_stat_statements] | [XXXms] | Pass / Fail  |
| Cache hit rate                | [>90%]     | [Redis INFO stats: keyspace_hits / (hits+misses)] | [XX%] | Pass / Fail |
| Memory usage (steady state)   | [<512MB]   | [RSS after 5 minutes idle under load]       | [XX MB]  | Pass / Fail     |
| Memory usage (peak)           | [<1GB]     | [Max RSS during spike test]                 | [XX MB]  | Pass / Fail     |
| GC pause time (if applicable) | [<50ms p99]| [GC metrics from runtime]                   | [XXms]   | Pass / Fail     |

---

## 2. Benchmark Methodology

| Parameter             | Value                                                              |
| --------------------- | ------------------------------------------------------------------ |
| **Test environment**  | [AWS t3.xlarge / GCP n2-standard-4 / equivalent]                   |
| **Database**          | [PostgreSQL 16 / MySQL 8.0 -- instance size, connection pool size] |
| **Cache**             | [Redis 7 -- instance size, max memory]                             |
| **Network condition** | [Internal VPC / simulated WAN latency: Xms]                        |
| **Measurement tools** | [k6 / wrk / Apache Benchmark / pg_stat_statements / Redis INFO]   |
| **Sample size**       | [N requests per endpoint, N runs per metric]                       |
| **Baseline version**  | [API version / commit hash]                                        |
| **Load profile**      | [Ramp: 0->N VUs over 60s, hold for 300s, ramp down 60s]            |

---

## 3. Per-Endpoint Latency Breakdown

| Endpoint              | P50    | P95    | P99    | Avg Body Size | Requests/min |
| --------------------- | ------ | ------ | ------ | ------------- | ------------ |
| GET /api/users/:id    | [Xms]  | [Xms]  | [Xms]  | [X KB]        | [N]          |
| POST /api/auth/login  | [Xms]  | [Xms]  | [Xms]  | [X KB]        | [N]          |
| GET /api/items        | [Xms]  | [Xms]  | [Xms]  | [X KB]        | [N]          |
| POST /api/items       | [Xms]  | [Xms]  | [Xms]  | [X KB]        | [N]          |
| GET /api/search       | [Xms]  | [Xms]  | [Xms]  | [X KB]        | [N]          |

---

## 4. Database Query Performance

| Query Pattern                    | P50    | P95    | P99    | Times Executed | Full Scan? | Indexed? |
| -------------------------------- | ------ | ------ | ------ | -------------- | ---------- | -------- |
| User lookup by ID (PK)           | [Xms]  | [Xms]  | [Xms]  | [N]            | No         | Yes      |
| Item list with pagination        | [Xms]  | [Xms]  | [Xms]  | [N]            | No         | Yes      |
| Search with full-text index      | [Xms]  | [Xms]  | [Xms]  | [N]            | No         | Yes      |
| Aggregation (COUNT/GROUP BY)     | [Xms]  | [Xms]  | [Xms]  | [N]            | No         | Yes      |

---

## 5. Cache Performance

| Metric                     | Value    | Target   | Pass/Fail       |
| -------------------------- | -------- | -------- | --------------- |
| Overall hit rate           | [XX%]    | [>90%]   | Pass / Fail     |
| User profile cache hit rate| [XX%]    | [>90%]   | Pass / Fail     |
| Session cache hit rate     | [XX%]    | [>95%]   | Pass / Fail     |
| Cache eviction rate        | [N/sec]  | [<threshold] | Pass / Fail |
| Average cache response time| [Xms]    | [<5ms]   | Pass / Fail     |

---

## 6. Connection Pool Utilization

| Pool              | Max Size | Avg Active | Peak Active | Utilization % | Exhaustion Events? |
| ----------------- | -------- | ---------- | ----------- | ------------- | ------------------ |
| Database pool     | [N]      | [N]        | [N]         | [XX%]         | Yes / No           |
| Redis pool        | [N]      | [N]        | [N]         | [XX%]         | Yes / No           |
| HTTP client pool  | [N]      | [N]        | [N]         | [XX%]         | Yes / No           |

---

## 7. Performance Regression Comparison

| Metric                | Previous Benchmark | Current Benchmark | Delta      | Trend     |
| --------------------- | ------------------ | ----------------- | ---------- | --------- |
| P99 latency           | [XXXms]            | [XXXms]           | [+/- X%]   | Up / Down / Same |
| Throughput (rps)      | [N rps]            | [N rps]           | [+/- X%]   | Up / Down / Same |
| Error rate            | [X.XX%]            | [X.XX%]           | [+/- X%]   | Up / Down / Same |
| DB pool utilization   | [XX%]              | [XX%]             | [+/- X%]   | Up / Down / Same |
| Cache hit rate        | [XX%]              | [XX%]             | [+/- X%]   | Up / Down / Same |
| Memory (steady state) | [XX MB]            | [XX MB]           | [+/- X MB] | Up / Down / Same |

---

## 8. Pass/Fail Summary

| Category              | Total Metrics | Pass    | Fail    | Pass Rate |
| --------------------- | ------------- | ------- | ------- | --------- |
| Latency               | [N]           | [N]     | [N]     | [XX]%     |
| Throughput            | [N]           | [N]     | [N]     | [XX]%     |
| Error rate            | [N]           | [N]     | [N]     | [XX]%     |
| Resource utilization  | [N]           | [N]     | [N]     | [XX]%     |
| Database              | [N]           | [N]     | [N]     | [XX]%     |
| Cache                 | [N]           | [N]     | [N]     | [XX]%     |
| **Total**             | **[N]**       | **[N]** | **[N]** | **[XX]%** |

**Gate criterion:** 100% of PRD performance thresholds must pass. Any failed metric is classified as at minimum a **P1 defect** if it exceeds the threshold by >20%, or **P2** if within 20%.

---

## 9. Recommendations

| Failed Metric | Root Cause | Remediation | Estimated Effort | Owner  |
| ------------- | ---------- | ----------- | ---------------- | ------ |
| [Metric]      | [Cause]    | [Action]    | [S/M/L]          | [Name] |

---

**Reviewed by CTO (Dr. Kenji Nakamura) on YYYY-MM-DD**
**Reviewed by CPO (Marcus Tran-Yoshida) on YYYY-MM-DD**
