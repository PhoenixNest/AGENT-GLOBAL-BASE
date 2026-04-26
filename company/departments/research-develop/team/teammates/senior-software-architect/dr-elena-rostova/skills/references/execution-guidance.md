---
version: "1.0.0"
---

------------------- | -------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------- |
| **Strong (Linearizable)** | Every read returns latest write | Writes are totally ordered | Financial transactions, auth tokens, inventory locks | High-write throughput paths; mobile offline scenarios |
| **Sequential** | All processes see writes in same order | Writes from single process ordered, multi-process may interleave | Chat message ordering, activity feeds | When cross-entity atomicity required |
| **Causal** | Causally related operations ordered | Concurrent writes may appear in different order | Social graph updates, collaborative editing | When strict ordering of all operations needed |
| **Eventual** | All replicas converge if no new writes | No ordering guarantee; convergence time varies | CDN content, cached reference data, analytics | Any security-critical or financial path |
| **Session** | Within a session, reads see own writes | Cross-session consistency not guaranteed | User-facing CRUD where user expects to see own changes | Cross-user collaborative features |

**Mobile Rule:** The mobile client's local database operates under eventual consistency with the backend. The sync engine must implement conflict resolution (last-write-wins, operational transforms, or CRDTs — see cross-platform-architecture skill).

### 2. Trade-off Analysis Framework

#### 2.1 Four-Dimensional Scoring Model

Every architecture decision is scored across four dimensions on a 1–5 scale (1 = poor, 5 = excellent):

```
┌──────────────────────────────────────────────────────────────────────┐
│ TRADE-OFF SCORING TEMPLATE                                          │
├──────────────────┬─────────┬─────────┬──────────────┬───────────────┤
│ Dimension        │ Weight  │ Score   │ Weighted     │ Evidence      │
│                  │         │ (1-5)   │ Score        │               │
├──────────────────┼─────────┼─────────┼──────────────┼───────────────┤
│ Performance      │ 0.30    │         │              │ Benchmarks,   │
│ (latency,        │         │         │              │ load tests,   │
│ throughput)      │         │         │              │ projections   │
├──────────────────┼─────────┼─────────┼──────────────┼───────────────┤
│ Consistency &    │ 0.25    │         │              │ CAP analysis, │
│ Correctness      │         │         │              │ edge case     │
│                  │         │         │              │ coverage      │
├──────────────────┼─────────┼─────────┼──────────────┼───────────────┤
│ Complexity &     │ 0.25    │         │              │ Component     │
│ Operational      │         │         │              │ count, dep.   │
│ Burden           │         │         │              │ graph depth,  │
│                  │         │         │              │ on-call load  │
├──────────────────┼─────────┼─────────┼──────────────┼───────────────┤
│ Team Capability  │ 0.20    │         │              │ Skill matrix, │
│ & Velocity       │         │         │              │ ramp-up time, │
│                  │         │         │              │ hiring market │
├──────────────────┼─────────┼─────────┼──────────────┼───────────────┤
│ TOTAL            │ 1.00    │ —       │ Σ(w × s)     │               │
└──────────────────┴─────────┴─────────┴──────────────┴───────────────┘

Decision threshold:
  Score ≥ 4.0  → Strong recommendation
  3.0 – 3.9    → Viable with mitigations
  < 3.0        → Reject unless no alternative exists
```

#### 2.2 Operational Complexity Scoring

Operational complexity is the hidden cost that kills projects. Score it explicitly:

| Factor               | Low (1)           | Medium (3)                      | High (5)                                        |
| -------------------- | ----------------- | ------------------------------- | ----------------------------------------------- |
| **Service Count**    | 1–3 services      | 4–8 services                    | 9+ services                                     |
| **Data Stores**      | 1 database        | 2–3 databases                   | 4+ databases + caches + queues                  |
| **Deployment Units** | Monolithic deploy | Independent services, shared CI | Independent repos, independent CI               |
| **Observability**    | Logs only         | Logs + metrics                  | Logs + metrics + distributed tracing + alerting |
| **Failure Domains**  | Single AZ         | Multi-AZ                        | Multi-region with active-active                 |
| **Team Dependency**  | Single team       | 2–3 coordinated teams           | 4+ teams with cross-cutting concerns            |

**Rule of thumb:** If total operational complexity score > 18 for a project with < 5 engineers, reject the architecture. The operational burden will consume all engineering capacity.

### 3. Architecture Pattern Comparisons

#### 3.1 Pattern Comparison Matrix

| Criterion                  | Modular Monolith            | Microservices                 | Event Sourcing                      | CQRS                         | Serverless                   |
| -------------------------- | --------------------------- | ----------------------------- | ----------------------------------- | ---------------------------- | ---------------------------- |
| **Team Size Fit**          | 1–10 engineers              | 10+ engineers, 2+ teams       | Domain-event-heavy systems          | Read/write asymmetry         | Bursty, unpredictable load   |
| **Dev Velocity (early)**   | ★★★★★                       | ★★☆☆☆                         | ★★★☆☆                               | ★★★☆☆                        | ★★★★☆                        |
| **Dev Velocity (mature)**  | ★★★☆☆                       | ★★★★★                         | ★★★★☆                               | ★★★★☆                        | ★★★★☆                        |
| **Operational Complexity** | Low                         | High                          | Very High                           | Medium-High                  | Low-Medium                   |
| **Data Consistency**       | ACID (single DB)            | Eventual (distributed)        | Eventual (projections)              | Eventual (read/write split)  | Depends on backing service   |
| **Scalability**            | Vertical + read replicas    | Horizontal per service        | Horizontal (event log)              | Horizontal (read side)       | Auto-scale (provider)        |
| **Testing Complexity**     | Integration tests           | Contract + integration + e2e  | Event replay tests                  | Read/write model tests       | Integration + provider tests |
| **Mobile Backend Fit**     | ★★★★★ (most mobile apps)    | ★★★☆☆ (only if scale demands) | ★★★★☆ (audit trail needed)          | ★★★★☆ (heavy read workloads) | ★★★☆☆ (cold start latency)   |
| **When to Choose**         | Default for mobile products | Team scaling > 10 engineers   | Audit, compliance, temporal queries | Read-heavy APIs, dashboards  | Event-driven, spiky traffic  |

#### 3.2 Event Sourcing vs. CRUD — Decision Framework

```
┌─────────────────────────────────────────────────────────────────────┐
│ EVENT SOURCING DECISION TREE                                        │
│                                                                     │
│  Does the domain require full audit trail of all changes?           │
│  ├── NO → Use CRUD. Event sourcing adds unnecessary complexity.     │
│  └── YES                                                            │
│       │                                                             │
│       Is temporal state reconstruction required?                     │
│       (e.g., "what was the order state at 2024-03-15T10:30:00?")   │
│       ├── NO → Consider CRUD + audit log table.                     │
│       └── YES                                                        │
│            │                                                        │
│            Can the event stream fit in memory for replay?           │
│            (or: can snapshotting keep replay time < 5s?)            │
│            ├── NO → Event sourcing will cause performance issues.   │
│            │        Consider CRUD with versioned tables instead.    │
│            └── YES                                                  │
│                 │                                                   │
│                 Does the team have distributed systems expertise?    │
│                 ├── NO → Hire/upscale first, then reconsider.       │
│                 │        Event sourcing without expertise = pain.   │
│                 └── YES → EVENT SOURCING IS VIABLE.                 │
│                          Proceed with:                               │
│                          - Event store (e.g., EventStoreDB)         │
│                          - Snapshot strategy                        │
│                          - Projection rebuild procedure             │
│                          - Schema migration plan for events         │
└─────────────────────────────────────────────────────────────────────┘
```

**Benchmark Data (from production systems at scale):**

| Metric                                | CRUD (PostgreSQL)         | Event Sourcing (EventStoreDB)                  |
| ------------------------------------- | ------------------------- | ---------------------------------------------- |
| Write latency (P95)                   | 8ms                       | 12ms                                           |
| Read latency — current state (P95)    | 5ms                       | 15ms (via projection)                          |
| Read latency — historical state (P95) | 200ms+ (temporal joins)   | 3ms (replay from snapshot)                     |
| Storage growth (1M entities/year)     | ~2 GB                     | ~8 GB (event log)                              |
| Schema migration effort               | Moderate (ALTER TABLE)    | High (event upcasters + projection rebuild)    |
| Debugging complexity                  | Low (query current state) | Medium-High (replay events, check projections) |

#### 3.3 CQRS vs. Traditional Pattern

```
CQRS IS WARRANTED WHEN:
  ✓ Read/write ratio > 10:1
  ✓ Read and write models have fundamentally different shapes
  ✓ Different teams own read vs. write optimization
  ✓ Read scaling requirements vastly exceed write scaling

CQRS IS OVERKILL WHEN:
  ✗ Read/write ratio < 5:1
  ✗ Same team owns all queries and commands
  ✗ Simple CRUD operations satisfy all use cases
  ✗ Team size < 5 engineers

MOBILE CONTEXT:
  Mobile APIs are naturally read-heavy (feed loads, profile views,
  catalog browsing). CQRS can be justified at the API gateway level:
  - Write path: command → service bus → write model → event → projection
  - Read path: cached projection → CDN edge → mobile client

  However, for most mobile products, a well-designed REST/GraphQL API
  with read replicas and caching achieves 90% of CQRS benefits at
  20% of the complexity.
```

#### 3.4 Sync vs. Async Communication

| Criterion              | Synchronous (REST/gRPC)         | Asynchronous (Message Queue/Event Stream)       |
| ---------------------- | ------------------------------- | ----------------------------------------------- |
| **Latency**            | Low (single hop, P95 < 100ms)   | Higher (queue hop, P95 < 500ms)                 |
| **Coupling**           | Tight (caller waits for callee) | Loose (publisher doesn't know subscribers)      |
| **Failure Mode**       | Caller fails if callee is down  | Messages persist; retry on recovery             |
| **Debugging**          | Simple (trace single request)   | Complex (trace message through queue)           |
| **Backpressure**       | Implicit (caller blocks)        | Explicit (queue depth, consumer lag)            |
| **Mobile Backend Fit** | User-facing API responses       | Background processing, notifications, analytics |

**Rule:** User-facing mobile API responses must be synchronous (the user is waiting). Background processing (image resizing, email sending, analytics aggregation) must be asynchronous. Never make a mobile client wait for async work — return 202 Accepted with a status endpoint instead.

### 4. Capacity Planning and Scalability Projections

#### 4.1 Load Modeling from PRD Features

Every PRD feature maps to a load profile:

```
FEATURE → LOAD PROFILE MAPPING

Feature: "User uploads profile photo"
  Request: POST /api/v1/users/{id}/photo
  Payload: 2–5 MB image
  Frequency: ~0.1 req/user/day
  Daily volume (at 100K MAU): 10,000 requests
  Peak factor: 3x (morning commute) → 30,000 req / 4 hrs = 2.1 req/s
  P99 latency SLO: < 2s (includes upload + processing)
  Storage growth: 3 MB × 10,000/day = 30 GB/day = 900 GB/month
  CDN egress: 3 MB × 50 views/photo × 10,000 uploads/day = 1.5 TB/day

Resource estimate:
  - API servers: 2 instances (handles peak 2.1 req/s with room for growth)
  - Object storage: 900 GB/month growth; lifecycle policy after 2 years
  - CDN: 1.5 TB/day egress; budget accordingly
  - Image processing: async worker pool, 4 workers handles peak
```

#### 4.2 12-Month Capacity Projection Template

```
┌─────────────────────────────────────────────────────────────────────┐
│ CAPACITY PROJECTION — 12 MONTH HORIZON                              │
├──────────────────┬─────────┬─────────┬─────────┬─────────┬──────────┤
│ Metric           │ Month 1 │ Month 3 │ Month 6 │ Month 9 │ Month 12 │
├──────────────────┼─────────┼─────────┼─────────┼─────────┼──────────┤
│ MAU              │  10,000 │  50,000 │ 150,000 │ 300,000 │  500,000 │
│ API req/s (avg)  │      5  │     25  │     75  │    150  │      250 │
│ API req/s (peak) │     15  │     75  │    225  │    450  │      750 │
│ P95 Latency SLO  │  < 200ms│ < 200ms │ < 200ms │ < 200ms │  < 200ms │
│ API Instances    │      1  │      2  │      4  │      6  │       10 │
│ DB Connections   │     20  │     50  │    150  │    300  │      500 │
│ Storage (GB)     │     50  │    200  │    600  │  1,200  │    2,000 │
│ CDN Egress (TB)  │    0.5  │    2.0  │    6.0  │   12.0  │     20.0 │
│ Monthly Cost ($) │  1,200  │  2,500  │  5,800  │ 10,500  │   16,000 │
├──────────────────┴─────────┴─────────┴─────────┴─────────┴──────────┤
│ Scaling triggers:                                                    │
│   - Add API instance when avg req/s > 60% of current capacity       │
│   - Add read replica when DB connections > 70% of pool max          │
│   - Upgrade storage tier when IOPS utilization > 80% sustained      │
│   - Review CDN provider pricing at > 15 TB/month egress             │
└─────────────────────────────────────────────────────────────────────┘
```

### 5. Failure Mode Analysis

#### 5.1 Resilience Pattern Configuration

Every external dependency must have the following documented:

```yaml
# Resilience Configuration Template (per dependency)
dependency:
  name: "payment-gateway"
  criticality: P0 # Blocks core feature if down

  circuit_breaker:
    failure_threshold: 5 # Open circuit after 5 consecutive failures
    recovery_timeout_ms: 30000 # Half-open after 30s
    half_open_max_calls: 3 # Test 3 calls before closing

  retry:
    max_attempts: 3
    initial_backoff_ms: 100
    max_backoff_ms: 5000
    backoff_multiplier: 2.0
    retryable_status_codes: [502, 503, 504, 429]
    # NEVER retry 400, 401, 403, 404, 409 — these are client errors

  timeout:
    connection_ms: 3000
    request_ms: 10000

  fallback:
    strategy: "queue-and-retry-later"
    # Queue the payment request locally; retry on next sync
    # Notify user: "Payment queued, will process when service is available"

  idempotency:
    key_header: "Idempotency-Key"
    key_ttl_hours: 24
    # Every payment request carries a UUID; server deduplicates

  blast_radius:
    affected_features: ["checkout", "subscription-renewal"]
    degradation_mode: "Queue payments; allow browse to continue"
    user_impact: "Cannot complete purchase; can still browse catalog"
```

#### 5.2 Retry Budget

```
RETRY BUDGET CALCULATION:

Total request budget = Original requests + Retried requests

If retry budget is 20% of total:
  At 1000 original req/s, max 200 retried req/s
  If retries exceed budget → stop retrying, fail fast

MOBILE-SPECIFIC RETRY RULES:
  - Mobile clients must implement exponential backoff with jitter
  - Base backoff: 1s, 2s, 4s, 8s, 16s (max 5 attempts)
  - Jitter: ±50% randomization to prevent thundering herd
  - On cellular: increase backoff by 2x (cellular networks recover slower)
  - On Wi-Fi: standard backoff
  - Never retry 4xx errors except 429 (rate limit)
  - Retry budget on client: 15% of total requests
```

### 6. Technology Selection Methodology

#### 6.1 Build vs. Buy Decision Framework

```
┌─────────────────────────────────────────────────────────────────────┐
│ BUILD vs. BUY DECISION MATRIX                                       │
├──────────────────────────┬──────────┬──────────┬────────────────────┤
│ Criterion                │ Weight   │ Build    │ Buy / Managed      │
├──────────────────────────┼──────────┼──────────┼────────────────────┤
│ Core competency?         │ 0.20     │          │                    │
│ (Does it differentiate   │          │          │                    │
│  our product?)           │          │          │                    │
├──────────────────────────┼──────────┼──────────┼────────────────────┤
│ Time to market           │ 0.15     │          │                    │
│ (Weeks to production)    │          │          │                    │
├──────────────────────────┼──────────┼──────────┼────────────────────┤
│ Total cost (3-year TCO)  │ 0.20     │          │                    │
│ (Dev + infra + support)  │          │          │                    │
├──────────────────────────┼──────────┼──────────┼────────────────────┤
│ Vendor lock-in risk      │ 0.15     │          │                    │
│ (Migration cost to       │          │          │                    │
│  switch)                 │          │          │                    │
├──────────────────────────┼──────────┼──────────┼────────────────────┤
│ Maintenance burden       │ 0.15     │          │                    │
│ (On-call, patches,       │          │          │                    │
│  upgrades)               │          │          │                    │
├──────────────────────────┼──────────┼──────────┼────────────────────┤
│ Security & compliance    │ 0.10     │          │                    │
│ (SOC2, GDPR, audit)      │          │          │                    │
├──────────────────────────┼──────────┼──────────┼────────────────────┤
│ WEIGHTED TOTAL           │ 1.00     │          │                    │
└──────────────────────────┴──────────┴──────────┴────────────────────┘

RULE: If the capability is NOT core competency AND buy scores > build
      by ≥ 1.0 weighted points → BUY.
      Exception: If vendor lock-in risk is HIGH and migration cost
      exceeds 6 engineer-months → BUILD with open-source alternative.
```

#### 6.2 Vendor Lock-in Analysis

```
VENDOR LOCK-IN SCORE (per managed service):

Data Gravity (0-5): How hard is it to move your data out?
  0 = Stateless (no data)
  1 = Simple export (CSV, JSON dump)
  3 = Proprietary format, export tools exist but complex
  5 = Proprietary format, no export tools, must rebuild

API Surface (0-5): How much of your code is vendor-specific?
  0 = Standard protocol (HTTP, SQL, Kafka protocol)
  2 = Vendor SDK with thin wrapper around standard protocol
  4 = Vendor-specific query language, proprietary APIs
  5 = Deep integration into vendor ecosystem (e.g., AWS Lambda + DynamoDB + SNS + SQS)

Operational Knowledge (0-5): How much tribal knowledge is required?
  0 = Industry-standard tools, skills are transferable
  2 = Vendor-specific concepts but widely documented
  4 = Proprietary operational patterns, limited community knowledge
  5 = Only vendor experts understand the system

TOTAL LOCK-IN SCORE:
  0-5:  Low lock-in — acceptable for most services
  6-10: Medium lock-in — acceptable if service is not core competency
  11-15: High lock-in — requires explicit ADR with CTO approval
```

### 7. Decision Documentation

#### 7.1 ADR Linkage Requirements

Every system design decision must be documented as an ADR and linked to:

```
ADR STRUCTURE (per company standard):

ADR-NNN: <Title>
Status: Proposed | Accepted | Deprecated | Superseded
Date: YYYY-MM-DD
Author: Dr. Elena Rostova

Context:
  - PRD Requirement: <link to PRD section / user story>
  - UML Component: <link to component diagram>
  - Constraint: <technical, budget, timeline constraint>

Decision:
  <What was decided, in one clear sentence>

Consequences:
  Positive: <benefits>
  Negative: <costs, risks, trade-offs accepted>

Alternatives Considered:
  1. <Alternative A> — Rejected because <reason with data>
  2. <Alternative B> — Rejected because <reason with data>

Success Criteria (measurable within 90 days):
  - <Criterion 1>: <metric> < <threshold>
  - <Criterion 2>: <metric> > <threshold>

Failure Criteria:
  - <Criterion that would trigger reconsideration>

Related:
  - UML: <component/sequence diagram reference>
  - ADR: <related decision record numbers>
  - SRD: <security requirement reference if applicable>
```

#### 7.2 Architecture Risk Register

```
┌─────────────────────────────────────────────────────────────────────┐
│ ARCHITECTURE RISK REGISTER                                          │
├─────┬─────────────────┬──────────┬──────────┬───────────┬──────────┤
│ ID  │ Risk            │ Likeli-  │ Impact   │ Mitigation│ Owner    │
│     │                 │ hood (H/M│ (H/M/L)  │           │          │
│     │                 │ /L)      │          │           │          │
├─────┼─────────────────┼──────────┼──────────┼───────────┼──────────┤
│ R-1 │ Event store     │ M        │ H        │ Implement │ CTO      │
│     │ schema migration│          │          │ upcaster  │          │
│     │ breaks existing │          │          │ framework │          │
│     │ projections     │          │          │ + shadow  │          │
│     │                 │          │          │ deploy    │          │
├─────┼─────────────────┼──────────┼──────────┼───────────┼──────────┤
│ R-2 │ Mobile offline  │ H        │ M        │ Conflict  │ R&D      │
│     │ sync conflict   │          │          │ resolution│          │
│     │ rate > 5%       │          │          │ testing   │          │
│     │                 │          │          │ in Stage 7│          │
├─────┼─────────────────┼──────────┼──────────┼───────────┼──────────┤
│ R-3 │ Vendor API rate │ M        │ H        │ Request   │ CTO      │
│     │ limit exceeded  │          │          │ queuing   │          │
│     │ during peak     │          │          │ + circuit │          │
│     │                 │          │          │ breaker   │          │
└─────┴─────────────────┴──────────┴──────────┴───────────┴──────────┘
```

### 8. Mobile-Specific Considerations

#### 8.1 Offline-First Design Principles

```
MOBILE BACKEND DESIGN RULES:

1. Every write must be idempotent — mobile clients retry on reconnect
2. Every read must tolerate staleness — mark response with cache timestamp
3. Every sync operation must handle conflicts — LWW, OT, or CRDT
4. Every API response must be paginated — mobile devices have memory limits
5. Every background sync must be battery-aware — batch requests, defer non-critical
6. Every upload must support resume — chunked uploads with checkpoint tokens
7. Every push notification must be deduplicated — notification IDs, collapse keys

BACKEND IMPLICATIONS:
  - Idempotency keys on all write endpoints
  - ETag / Last-Modified headers on all read endpoints
  - Conflict resolution API (server provides both versions, client or server resolves)
  - Delta sync endpoints (only return changes since sync_token)
  - Batch endpoints (combine multiple operations in single request)
```

#### 8.2 Battery Impact Analysis

| Operation                     | Battery Cost (relative) | Mitigation                                         |
| ----------------------------- | ----------------------- | -------------------------------------------------- |
| Network request (Wi-Fi)       | 1x                      | Batch requests; defer non-critical sync            |
| Network request (Cellular)    | 3x                      | Wait for Wi-Fi when possible; compress payloads    |
| GPS location (continuous)     | 15x                     | Use geofencing API; reduce update frequency        |
| Bluetooth LE scan             | 5x                      | Use duty cycling; only scan when app is foreground |
| Wake lock (keeping CPU awake) | 8x                      | Use WorkManager/BackgroundTasks API instead        |
| Large download (>50 MB)       | 4x                      | Chunk downloads; support pause/resume              |

**Backend responsibility:** The backend must support batch operations and delta sync to minimize mobile client network activity. Every API design decision should include a battery impact assessment.
