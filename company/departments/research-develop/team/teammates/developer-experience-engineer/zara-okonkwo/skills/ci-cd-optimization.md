---
version: "1.0.0"
---

| Competency               | Description                                                                                                | Quality Criteria                                                                                                                      |
| ------------------------ | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Pipeline Parallelization | Stage decomposition, DAG-based execution, resource optimization, dependency management                     | Designs pipelines with maximum safe parallelism; reduces total pipeline time by > 50%; eliminates unnecessary sequential dependencies |
| Test Sharding            | Code ownership-based sharding, affected test detection, dynamic shard allocation, shard result aggregation | Shards tests by changed files; allocates shards dynamically based on test duration; reduces test time by > 60%                        |
| Artifact Caching         | Remote cache configuration, content-addressable storage, cache invalidation, cache warming                 | Achieves > 80% cache hit rate; designs cache keys based on content hashes; implements cache warming for common builds                 |
| Deployment Strategies    | Canary, blue-green, rolling updates, feature flags, traffic shifting                                       | Implements zero-downtime deployments; configures automated canary analysis; designs rollback triggers                                 |
| Rollback Automation      | Health check verification, automated rollback triggers, rollback testing, data migration rollback          | Configures automated rollback on health check failure; tests rollback procedures regularly; handles data migration rollback           |

## Pipeline Integration

**Stage 4 (Implementation Plan):** CI/CD pipeline designed with parallelization. Deployment strategy selected per service. Rollback procedures documented.

**Stage 5 (Development):** Pipeline implemented with test sharding. Artifact caching configured. Deployment automation deployed.

**Stage 6 (Code Review):** Pipeline configuration reviewed for correctness. Cache configuration validated. Rollback procedures tested.

**Stage 7 (Testing):** Pipeline execution time measured. Cache hit rates monitored. Deployment and rollback procedures tested in staging.

**Stage 10 (Release Readiness):** Panel confirms CI/CD pipeline operational, deployment strategy validated, rollback procedures tested.

## Quality Standards

| Metric                    | Target                                     | Measurement            |
| ------------------------- | ------------------------------------------ | ---------------------- |
| Pipeline duration (P95)   | < 15 minutes                               | CI monitoring          |
| Cache hit rate            | > 80%                                      | Cache metrics          |
| Test shard balance        | < 20% variance between shards              | Test timing analysis   |
| Deployment success rate   | > 99%                                      | Deployment tracking    |
| Rollback time             | < 5 minutes                                | Rollback drill timing  |
| Zero-downtime deployments | 100%                                       | Deployment monitoring  |
| Canary analysis accuracy  | > 95% correct promotion/rollback decisions | Canary analysis review |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
