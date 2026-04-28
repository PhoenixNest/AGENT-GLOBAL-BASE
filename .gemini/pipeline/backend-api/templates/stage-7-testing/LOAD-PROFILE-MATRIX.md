# Load Profile Matrix

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Backend API Services (P2)
**Stage:** 7 — Automated Testing

---

## Load Test Scenarios

| Scenario    | Concurrent Users | Request Rate (rps) | Duration | Expected P99 | Expected Error Rate | Status      |
| ----------- | ---------------- | ------------------ | -------- | ------------ | ------------------- | ----------- |
| Normal load | [N]              | [N]                | [X min]  | <[X]ms       | <0.1%               | ☐ / 🟡 / ✅ |
| Peak load   | [N]              | [N]                | [X min]  | <[X]ms       | <0.5%               | ☐ / 🟡 / ✅ |
| Stress test | [N]              | [N]                | [X min]  | <[X]ms       | <1.0%               | ☐ / 🟡 / ✅ |
| Spike test  | [N] → [N]        | [N] → [N]          | [X min]  | <[X]ms       | <1.0%               | ☐ / 🟡 / ✅ |
| Soak test   | [N]              | [N]                | [X hrs]  | <[X]ms       | <0.1%               | ☐ / 🟡 / ✅ |

## Endpoint-Level Performance

| Endpoint             | Method | Avg Response | P95 Response | P99 Response | Throughput (rps) | Error Rate | Status      |
| -------------------- | ------ | ------------ | ------------ | ------------ | ---------------- | ---------- | ----------- |
| [GET /api/resource]  | GET    | [X]ms        | [X]ms        | [X]ms        | [N]              | [X]%       | ☐ / 🟡 / ✅ |
| [POST /api/resource] | POST   | [X]ms        | [X]ms        | [X]ms        | [N]              | [X]%       | ☐ / 🟡 / ✅ |

## Concurrency Limits

| Resource               | Limit   | Current Peak | Headroom | Status      |
| ---------------------- | ------- | ------------ | -------- | ----------- |
| Database connections   | [N]     | [N]          | [X]%     | ☐ / 🟡 / ✅ |
| API gateway throughput | [N] rps | [N] rps      | [X]%     | ☐ / 🟡 / ✅ |
| Worker threads         | [N]     | [N]          | [X]%     | ☐ / 🟡 / ✅ |

## k6 Test Configuration

| Parameter           | Value                        |
| ------------------- | ---------------------------- |
| Tool                | k6                           |
| Test duration       | [X] minutes                  |
| Ramp-up period      | [X] seconds                  |
| VUs (virtual users) | [N]                          |
| Iterations per VU   | [N]                          |
| Thresholds          | P99 <[X]ms, error rate <[X]% |

## Chaos Engineering (Optional)

| Failure Scenario         | Expected Behavior             | Actual Result | Status      |
| ------------------------ | ----------------------------- | ------------- | ----------- |
| Database connection drop | Graceful retry, no data loss  | [Result]      | ☐ / 🟡 / ✅ |
| API gateway timeout      | Circuit breaker activated     | [Result]      | ☐ / 🟡 / ✅ |
| Cache invalidation       | Fallback to DB, degraded perf | [Result]      | ☐ / 🟡 / ✅ |

## Performance Regression History

| Test Run | Date       | P99 (ms) | Throughput (rps) | Error Rate | Status      |
| -------- | ---------- | -------- | ---------------- | ---------- | ----------- |
| Baseline | YYYY-MM-DD | [X]ms    | [N]              | [X]%       | ✅ Pass     |
| Current  | YYYY-MM-DD | [X]ms    | [N]              | [X]%       | ☐ / 🟡 / ✅ |
