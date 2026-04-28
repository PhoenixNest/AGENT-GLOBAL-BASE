# ADR: Database Architecture

| Field         | Value                                                       |
| ------------- | ----------------------------------------------------------- |
| **Status**    | Proposed                                                    |
| **Context**   | Stage 3 — Backend API Pipeline (P2)                         |
| **Decision**  | PostgreSQL + Redis + PgBouncer + Multi-region read replicas |
| **Date**      | YYYY-MM-DD                                                  |
| **Authors**   | CIO (primary), Data Lead                                    |
| **Reviewers** | CTO (technology), CSO (security)                            |

---

## Decision

We will use **PostgreSQL 16+** as the primary database with **Redis 7+** for caching, **PgBouncer** for connection pooling (transaction-level mode), and **multi-region read replicas** for global low-latency access.

## Rationale

Backend API services require a robust database architecture that supports high availability, data consistency, zero-downtime migrations, and compliance with data residency requirements. The choice between SQL and NoSQL, migration tooling, connection pooling strategy, and read replica configuration directly impacts performance SLAs (P99 <200ms), uptime (99.9%+), and operational complexity.

### 1. Database Selection: PostgreSQL (Primary) + Redis (Cache)

**Primary Database:** PostgreSQL 16+

**Rationale:**

- **ACID compliance** — Required for financial transactions, order processing, user data integrity
- **JSONB support** — Flexible schema for semi-structured data without sacrificing relational integrity
- **Advanced indexing** — GIN, GiST, BRIN indexes for complex query patterns
- **Replication** — Built-in streaming replication for read replicas
- **Extensions** — PostGIS (geospatial), pgcrypto (encryption), pg_stat_statements (performance monitoring)
- **Maturity** — 30+ years of production use, extensive tooling ecosystem

**Cache Layer:** Redis 7+

**Use Cases:**

- Session storage (JWT blacklist, rate limiting counters)
- Query result caching (frequently accessed, rarely changed data)
- Distributed locks (prevent race conditions in concurrent operations)
- Pub/Sub (real-time notifications, event broadcasting)

**Rejected Alternatives:**

| Alternative   | Rejection Reason                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------- |
| MySQL/MariaDB | Inferior JSON support, weaker concurrency control, limited extension ecosystem                          |
| MongoDB       | Lack of ACID guarantees for multi-document transactions, eventual consistency violates SRD requirements |
| DynamoDB      | Vendor lock-in (AWS-only), limited query flexibility, cold start latency                                |
| Cassandra     | Eventual consistency model incompatible with financial transaction requirements                         |

---

### 2. Migration Tooling: Flyway (Java/Kotlin) or golang-migrate (Go)

**Selection Criteria by Language:**

| Language    | Tool           | Rationale                                                |
| ----------- | -------------- | -------------------------------------------------------- |
| Java/Kotlin | Flyway         | Native JVM integration, Spring Boot support, mature      |
| Go          | golang-migrate | Lightweight, no external dependencies, CLI + library     |
| Node.js     | Prisma Migrate | Type-safe migrations, automatic rollback generation      |
| Python      | Alembic        | SQLAlchemy integration, auto-generate from model changes |

**Migration Standards:**

1. **Versioned migrations only** — No "auto-migration" in production
2. **Forward-only by default** — Rollback scripts optional (use backup restore for critical failures)
3. **Idempotent migrations** — Safe to re-run without side effects
4. **Checksum validation** — Detect unauthorized migration file modifications
5. **Lock table** — Prevent concurrent migration execution

**Migration File Naming:**

```
V1__create_users_table.sql
V2__add_email_index.sql
V3__create_orders_table.sql
V4__alter_orders_add_payment_method.sql
```

**Zero-Downtime Migration Strategy:**

| Migration Type        | Strategy                                                                    | Downtime Required |
| --------------------- | --------------------------------------------------------------------------- | ----------------- |
| Add column (nullable) | Direct ALTER TABLE                                                          | None              |
| Add column (NOT NULL) | 1) Add nullable, 2) Backfill defaults, 3) ALTER to NOT NULL                 | None              |
| Drop column           | 1) Remove from code, 2) Deploy, 3) DROP COLUMN                              | None              |
| Rename column         | 1) Add new column, 2) Dual-write, 3) Backfill, 4) Switch reads, 5) Drop old | <1s (cutover)     |
| Change column type    | 1) Add new column (new type), 2) Backfill, 3) Switch, 4) Drop old           | <1s (cutover)     |
| Add index             | CREATE INDEX CONCURRENTLY (PostgreSQL)                                      | None              |
| Drop index            | Direct DROP INDEX                                                           | None              |

---

### 3. Connection Pooling: PgBouncer (Transaction-Level Pooling)

**Configuration:**

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3
server_lifetime = 3600
server_idle_timeout = 600
```

**Rationale for Transaction-Level Pooling:**

- **Higher concurrency** — Connections released after each transaction, not per session
- **Better resource utilization** — 1000 client connections multiplexed onto 20 server connections
- **Prevents connection exhaustion** — Critical under load spikes (e.g., flash sales)

**Connection Pool Monitoring:**

- `pgbouncer_active_connections` — Active client connections
- `pgbouncer_waiting_clients` — Clients waiting for available connection (alert if >10)
- `pgbouncer_server_utilization` — Server connection usage % (alert if >80%)

---

### 4. Read Replica Strategy

**Architecture:**

```
Primary (us-east-1)
├─ Read Replica 1 (us-east-1) — Low-latency reads for US users
├─ Read Replica 2 (eu-west-1) — GDPR-compliant reads for EU users
└─ Read Replica 3 (ap-southeast-1) — Low-latency reads for APAC users
```

**Replication Lag Monitoring:**

- Alert threshold: >5 seconds lag (critical), >2 seconds lag (warning)
- Fallback: If lag exceeds 10 seconds, route reads to primary (accept higher latency)

**Read Routing Logic:**

```python
def get_database_connection(user_region, consistency_requirement):
    if consistency_requirement == "strong":
        return PRIMARY  # Always read from primary for strong consistency

    if user_region == "EU" and gdpr_applies:
        return REPLICA_EU  # Data residency compliance

    replica = get_least_lagged_replica(user_region)
    if replica.lag_seconds < 5:
        return replica
    else:
        return PRIMARY  # Fallback to primary if replicas too stale
```

**Write Scaling:** Not supported — All writes go to primary. For write-heavy workloads, consider sharding (see Risks section).

---

## Alternatives Considered

### Alternative 1: Single Primary, No Replicas

**Pros:** Simpler architecture, no replication lag concerns, lower cost  
**Cons:** Single point of failure, no read scaling, geographic latency for global users  
**Rejected because:** Violates SRD requirement for "99.9% uptime" and "sub-200ms P99 latency globally."

### Alternative 2: Multi-Master Replication

**Pros:** Write scaling, automatic failover  
**Cons:** Conflict resolution complexity, eventual consistency violations, higher operational overhead  
**Rejected because:** Financial transaction requirements demand strong consistency; conflict resolution introduces unacceptable risk.

### Alternative 3: Serverless Database (Aurora Serverless, PlanetScale)

**Pros:** Auto-scaling, pay-per-use, reduced operational overhead  
**Cons:** Cold start latency (2-5 seconds), vendor lock-in, unpredictable costs at scale  
**Rejected because:** Cold start latency violates P99 <200ms SLA; cost unpredictability conflicts with TCO projections.

---

## Consequences

### Positive

- **High availability** — Automatic failover to read replica promoted to primary (<30 seconds)
- **Global low latency** — Read replicas reduce P99 latency from 150ms (single region) to 40ms (edge regions)
- **Zero-downtime deployments** — Migration strategy enables continuous deployment without maintenance windows
- **Compliance** — Read replica placement satisfies GDPR data residency requirements

### Negative

- **Operational complexity** — Team must monitor replication lag, manage failover procedures, handle split-brain scenarios
- **Cost** — 4 instances (1 primary + 3 replicas) vs. 1 instance = 4x infrastructure cost
- **Eventual consistency risks** — Reads from replicas may return stale data (mitigated by strong consistency routing for critical operations)

### Risks & Mitigations

| Risk                               | Likelihood | Impact   | Mitigation                                                                              |
| ---------------------------------- | ---------- | -------- | --------------------------------------------------------------------------------------- |
| Replication lag causes stale reads | Medium     | Medium   | Monitor lag, fallback to primary, document consistency guarantees per endpoint          |
| Primary failure during failover    | Low        | High     | Automated promotion script, quarterly disaster recovery drills, RPO <5s, RTO <30s       |
| Migration failure corrupts data    | Low        | Critical | Pre-migration backup, test migrations on staging clone, rollback procedure documented   |
| Connection pool exhaustion         | Medium     | High     | Alert on waiting_clients >10, auto-scale pgbouncer instances, implement circuit breaker |

---

## Implementation Plan

**Phase 1 (Week 1-2):** Infrastructure provisioning

- Deploy PostgreSQL primary + 3 read replicas across regions
- Configure PgBouncer connection pools (transaction-level mode)
- Set up monitoring (replication lag, connection pool metrics, query performance)

**Phase 2 (Week 3-4):** Migration framework setup

- Integrate Flyway/golang-migrate into CI/CD pipeline
- Create migration template with checksums, idempotency guards
- Test zero-downtime migration strategies on staging environment

**Phase 3 (Week 5-6):** Application integration

- Implement read routing logic (consistency-aware, region-aware)
- Add connection pool monitoring to application health checks
- Configure alerting rules (replication lag >5s, pool utilization >80%)

**Phase 4 (Week 7-8):** Disaster recovery testing

- Simulate primary failure, measure failover time (target <30s)
- Test backup restoration procedure (target RTO <1 hour)
- Document runbook for common failure scenarios

---

## Compliance Alignment

- **GDPR Article 44-50:** Read replica placement ensures EU user data remains in EU region
- **PCI-DSS Requirement 3:** Encrypted database at rest (AES-256), encrypted connections (TLS 1.3)
- **SOC 2 Type II:** Audit logging of all database access, migration history tracked
- **SRD Section 5.1:** "Encrypted database at rest with AES-256, TLS 1.3 for all connections"

---

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Flyway Migration Best Practices](https://flywaydb.org/documentation/bestpractices)
- [PgBouncer Configuration Guide](https://www.pgbouncer.org/config.html)
- [Zero-Downtime PostgreSQL Migrations](https://www.braintreepayments.com/blog/safe-operations-high-volume-postgresql/)
- SRD.md Section 5.1 (Database Security Requirements)

---

**Lock-down:** Once approved at Stage 3 gate, this decision is locked — switching between strategies requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.
