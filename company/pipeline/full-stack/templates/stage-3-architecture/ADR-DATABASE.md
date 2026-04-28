# ADR: Database Architecture (Cross-Platform)

| Field         | Value                                             |
| ------------- | ------------------------------------------------- |
| **Status**    | Proposed                                          |
| **Context**   | Stage 3 — Full-Stack Cross-Platform Pipeline (P3) |
| **Decision**  | PostgreSQL + Redis + SQLite with sync engine      |
| **Date**      | YYYY-MM-DD                                        |
| **Authors**   | CIO (primary), Data Lead, Backend Lead            |
| **Reviewers** | CTO (technology), CSO (security)                  |

---

## Decision

We will use **PostgreSQL 16+** as the primary database (shared state), **Redis 7+** for caching, and **SQLite** for mobile local storage (offline-first). Data synchronization between mobile clients and backend will use a custom sync engine with vector clocks for conflict detection.

## Rationale

Full-stack cross-platform products require a unified database architecture that serves as the single source of truth for web frontends, iOS apps, Android apps, and backend services. The database must support concurrent access from multiple platforms, handle offline-first mobile scenarios, maintain data consistency across distributed clients, and comply with data residency requirements (GDPR). This ADR extends the Backend API Pipeline's `ADR-DATABASE.md` with cross-platform shared state considerations.

### 1. Database Selection: PostgreSQL (Primary) + Redis (Cache) + SQLite (Mobile Local)

**Primary Database:** PostgreSQL 16+

**Rationale:**

- **Single source of truth** — All platforms read/write to same database, ensuring consistency
- **ACID compliance** — Required for financial transactions, user data integrity across platforms
- **JSONB support** — Flexible schema for platform-specific metadata without separate tables
- **Replication** — Built-in streaming replication for read replicas (web caching, regional distribution)
- **Extensions** — PostGIS (location-based features), pgcrypto (encryption), citus (horizontal scaling)

**Cache Layer:** Redis 7+

**Use Cases:**

- Session storage (JWT blacklist, rate limiting counters shared across platforms)
- Query result caching (product catalog, user preferences)
- Distributed locks (prevent race conditions when multiple devices edit same resource)
- Pub/Sub (real-time notifications pushed to all user devices simultaneously)

**Mobile Local Database:** SQLite (iOS CoreData / Android Room)

**Use Cases:**

- Offline-first data storage (user drafts, cached content)
- Conflict tracking (vector clocks for sync resolution)
- Performance optimization (reduce network calls for frequently accessed data)

**Sync Strategy:** Mobile SQLite ↔ Backend PostgreSQL via REST/GraphQL API with conflict resolution

---

### 2. Migration Tooling: Flyway (Java/Kotlin) or golang-migrate (Go)

**Migration Standards (Same as Backend ADR-DATABASE):**

- Versioned migrations only
- Forward-only by default
- Idempotent migrations
- Checksum validation
- Zero-downtime migration strategies

**Cross-Platform Migration Coordination:**

When database schema changes affect mobile apps:

1. **Backward-compatible migrations first** — Add new columns as nullable, never drop columns immediately
2. **Deploy backend with dual-read logic** — Read from old and new columns during transition
3. **Release mobile app update** — New app version writes to new column structure
4. **Monitor adoption** — Wait until >95% of users updated mobile app
5. **Remove legacy code** — Drop old columns, remove dual-read logic

**Example: Adding `phone_number` Field**

```sql
-- Week 1: Migration (backward-compatible)
ALTER TABLE users ADD COLUMN phone_number TEXT NULL;

-- Week 2-4: Backend dual-read logic
SELECT COALESCE(phone_number_new, phone_number_old) AS phone_number FROM users;

-- Week 5-8: Mobile app rollout (new version writes to phone_number_new)

-- Week 9+: After 95% adoption
UPDATE users SET phone_number = phone_number_new WHERE phone_number IS NULL;
ALTER TABLE users DROP COLUMN phone_number_old;
```

---

### 3. Connection Pooling: PgBouncer (Transaction-Level Pooling)

**Configuration (Same as Backend ADR-DATABASE):**

- Pool mode: transaction
- Max client connections: 1000
- Default pool size: 20 per service

**Cross-Platform Connection Distribution:**

| Platform | Estimated Connections | Rationale                                 |
| -------- | --------------------- | ----------------------------------------- |
| Web      | 400                   | High concurrency, short-lived requests    |
| iOS      | 200                   | Moderate concurrency, persistent sessions |
| Android  | 200                   | Moderate concurrency, persistent sessions |
| Backend  | 200                   | Service-to-service communication          |

**Connection Pool Monitoring:**

- Alert on `pgbouncer_waiting_clients > 10` (indicates pool exhaustion risk)
- Alert on `server_utilization > 80%` (scale up pgbouncer instances)

---

### 4. Read Replica Strategy: Multi-Region with Data Residency

**Architecture:**

```
Primary (us-east-1) — All writes, strong consistency reads
├─ Read Replica 1 (us-east-1) — Web frontend (US users)
├─ Read Replica 2 (eu-west-1) — GDPR-compliant reads (EU users)
├─ Read Replica 3 (ap-southeast-1) — Mobile apps (APAC users)
└─ Read Replica 4 (us-west-2) — Disaster recovery standby
```

**Data Residency Compliance:**

| User Region | Read Replica   | Write Path                            | GDPR Compliant?        |
| ----------- | -------------- | ------------------------------------- | ---------------------- |
| EU          | eu-west-1      | Primary (us-east-1) → async replicate | ✅ Yes (read locality) |
| US          | us-east-1      | Primary (us-east-1)                   | N/A                    |
| APAC        | ap-southeast-1 | Primary (us-east-1) → async replicate | N/A                    |

**Note:** GDPR requires EU user _personal data_ to remain in EU. Writes still go to primary (us-east-1), but personal data fields are encrypted before transmission. Read replica in EU provides low-latency access to encrypted data.

**Replication Lag Monitoring:**

- Alert threshold: >5 seconds lag (critical), >2 seconds lag (warning)
- Fallback: If lag exceeds 10 seconds, route reads to primary (accept higher latency)

---

### 5. Offline-First Sync: Conflict Resolution Strategy

**Challenge:** Mobile apps operate offline, creating local SQLite records. When connectivity restores, conflicts arise if:

- User edited same record on multiple devices
- Backend data changed while device was offline

**Conflict Resolution Strategy:**

#### Strategy 1: Last-Write-Wins (LWW) — Default for Non-Critical Data

**Use Cases:** User preferences, draft posts, shopping cart items

**Implementation:**

```json
{
  "record_id": "cart_item_123",
  "data": { "quantity": 3, "product_id": "prod_456" },
  "vector_clock": { "device_a": 5, "device_b": 3 },
  "last_modified": "2026-04-14T10:30:00Z",
  "modified_by": "device_a"
}
```

**Resolution:** Compare `last_modified` timestamps; latest wins. Log conflict for audit trail.

#### Strategy 2: Manual Merge — For Critical Data

**Use Cases:** Order modifications, payment updates, profile changes

**Implementation:**

1. Detect conflict (same record modified on multiple devices while offline)
2. Present conflict UI to user: "You made changes on iPhone and iPad. Which version should we keep?"
3. User selects version or manually merges fields
4. Server applies user's choice, logs decision

#### Strategy 3: Operational Transforms — For Collaborative Editing

**Use Cases:** Shared documents, collaborative comments, real-time chat

**Implementation:** Use CRDTs (Conflict-free Replicated Data Types) or OT (Operational Transforms) library

- Example: Yjs (JavaScript), Automerge (cross-platform)

**Sync Protocol:**

```
Mobile Device (offline) → Makes local changes → Stores in SQLite with vector clock
       ↓ (comes online)
Sync Request → POST /api/v1/sync { changes: [...], vector_clock: {...} }
       ↓
Backend → Checks for conflicts → Applies resolution strategy → Returns resolved state
       ↓
Mobile → Updates local SQLite → Notifies user if manual merge required
```

---

## Alternatives Considered

### Alternative 1: Separate Databases Per Platform

**Pros:** Platform autonomy, no cross-platform coordination needed  
**Cons:** Data inconsistency, complex synchronization, violates "single source of truth" principle  
**Rejected because:** Financial transactions require ACID guarantees across platforms; separate databases introduce eventual consistency risks.

### Alternative 2: NoSQL Database (MongoDB/DynamoDB)

**Pros:** Flexible schema, horizontal scaling, built-in replication  
**Cons:** Eventual consistency model, weak ACID guarantees, complex multi-document transactions  
**Rejected because:** SRD requires "strong consistency for financial transactions"; PostgreSQL ACID compliance is non-negotiable.

### Alternative 3: Client-Side Database Only (No Backend Persistence)

**Pros:** Ultimate offline capability, zero server costs  
**Cons:** Data loss on device failure, no cross-device sync, impossible for multi-user collaboration  
**Rejected because:** Violates product requirements for "seamless cross-device experience."

---

## Consequences

### Positive

- **Unified data model** — Single PostgreSQL schema serves all platforms, reducing duplication
- **Offline resilience** — Mobile SQLite enables full functionality without connectivity
- **GDPR compliance** — Regional read replicas satisfy data residency requirements
- **Conflict transparency** — Users notified of data conflicts, manual merge for critical operations

### Negative

- **Sync complexity** — Team must implement conflict detection, resolution strategies, vector clock tracking (~20% additional effort)
- **Storage overhead** — Mobile SQLite databases grow over time (require periodic cleanup, archival)
- **Migration coordination** — Schema changes require careful sequencing across backend + mobile releases

### Risks & Mitigations

| Risk                               | Likelihood | Impact   | Mitigation                                                                                                                   |
| ---------------------------------- | ---------- | -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Sync conflicts cause data loss     | Medium     | Critical | Comprehensive conflict logging, user notification, manual merge UI for critical data, automated tests for conflict scenarios |
| Replication lag causes stale reads | Medium     | Medium   | Monitor lag, fallback to primary, document consistency guarantees per endpoint                                               |
| Mobile database corruption         | Low        | High     | SQLite WAL mode (write-ahead logging), automatic backup on every 100th write, cloud backup of critical data                  |
| GDPR violation (EU data in US)     | Low        | Critical | Encrypt PII fields before transmission to US primary, legal review of data flow architecture                                 |

---

## Implementation Plan

**Phase 1 (Week 1-2):** Database infrastructure

- Deploy PostgreSQL primary + 4 read replicas across regions
- Configure PgBouncer connection pools
- Set up monitoring (replication lag, connection pool metrics)

**Phase 2 (Week 3-4):** Mobile local database

- Integrate SQLite (CoreData for iOS, Room for Android)
- Define offline data models (subset of backend schema)
- Implement vector clock tracking for conflict detection

**Phase 3 (Week 5-6):** Sync mechanism

- Build REST/GraphQL sync endpoints (`POST /api/v1/sync`)
- Implement conflict resolution strategies (LWW, manual merge, OT)
- Test offline scenarios (airplane mode, background sync, conflict creation)

**Phase 4 (Week 7-8):** Data residency compliance

- Configure regional read replica routing (EU users → eu-west-1)
- Encrypt PII fields before transmission to US primary
- Legal review + GDPR compliance audit

---

## Compliance Alignment

- **GDPR Article 44-50:** Regional read replicas ensure EU user data read locality; PII encryption satisfies cross-border transfer requirements
- **PCI-DSS Requirement 3:** Encrypted database at rest (AES-256), encrypted connections (TLS 1.3)
- **SOC 2 Type II:** Audit logging of all database access, migration history tracked, conflict resolution decisions logged
- **SRD Section 5.1:** "Encrypted database at rest with AES-256, TLS 1.3 for all connections"
- **SRD Section 7.3:** "Offline-first sync with conflict resolution for mobile platforms"

---

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLite WAL Mode](https://www.sqlite.org/wal.html)
- [CRDTs for Conflict-Free Replication](https://crdt.tech/)
- [Offline-First Architecture](https://offlinefirst.org/)
- [GDPR Data Residency Requirements](https://gdpr-info.eu/art-44-gdpr/)
- SRD.md Section 5.1 (Database Security), Section 7.3 (Offline-First Sync)

---

**Lock-down:** Once approved at Stage 3 gate, this decision is locked — switching between strategies requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.
