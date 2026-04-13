---
title: "ADR-007: Multi-Tenant Architecture Strategy"
status: "Draft"
owner: "Priya Nair, Sr. Backend Engineer"
reviewed-by: "Dr. Priya Mehta, CIO"
created: "2026-04-12"
review-date: "2026-04-26"
stage: "3"
audit-condition: "C3"
tags:
  ["architecture", "multi-tenancy", "data-isolation", "playfab", "self-hosted"]
---

# ADR-007: Multi-Tenant Architecture Strategy

> **CIO Audit Condition C3:** _"Build for multi-tenancy from Day 1 — even with one game, architect backend as multi-tenant. Retrofit cost is 3–5× original investment."_
>
> This ADR is assigned to **Priya Nair** and will be delivered as part of the **Stage 3 UML Engineering Package**. CIO review during Stage 3 gate review.

---

## Executive Summary

Per CIO audit condition C3, this Architecture Decision Record documents the company's multi-tenant architecture strategy. The mandate is clear: **build for multi-tenancy from Day 1**, even when operating with a single game. The retrofit cost of adding multi-tenancy post-launch is estimated at 3–5× the original investment. This ADR establishes the isolation model, tenant identification strategy, and migration path for both PlayFab-native and self-hosted backend scenarios.

---

## 1. Context

### Current State

- Single game in development (casual games studio)
- Single tenant operating environment
- PlayFab selected as primary BaaS platform

### Future State (12–18 month horizon)

- 3 concurrent games operating on shared infrastructure
- Multi-tenant backend supporting per-game configuration, analytics, and billing
- Potential hybrid architecture: PlayFab-native services + self-hosted adapter layer

### Platform-Specific Considerations

| Platform        | Multi-Tenancy Model                  | Notes                                                    |
| --------------- | ------------------------------------ | -------------------------------------------------------- |
| **PlayFab**     | Native (title IDs, virtual currency) | Multi-tenancy built-in; title ID serves as tenant key    |
| **Self-Hosted** | Requires explicit design             | Must implement tenant isolation in schema, API, and auth |

> **Key Insight:** PlayFab provides multi-tenancy out of the box through title ID segregation. However, our self-hosted adapter layer (the IAuthService contract boundary) must implement explicit multi-tenancy design to support future migration.

---

## 2. Decision Drivers

| Driver                            | Priority | Description                                                                |
| --------------------------------- | -------- | -------------------------------------------------------------------------- |
| **Data isolation between games**  | P0       | Critical: No game's data may be accessible to another game's services      |
| **Shared infrastructure cost**    | P1       | Efficient resource utilization across games; avoid per-game infrastructure |
| **Per-game configuration**        | P1       | Each game requires independent feature flags, economy tuning, and settings |
| **Cross-game analytics**          | P2       | Aggregated reporting across games requires tenant-aware data pipelines     |
| **Billing and metering per game** | P1       | Cost attribution per game for P&L tracking and optimization                |

---

## 3. Options Considered

### Option A: Schema-per-Tenant

Each game gets its own database schema within a shared database instance.

| Factor               | Assessment                                                        |
| -------------------- | ----------------------------------------------------------------- |
| Isolation            | High — schema boundaries enforced by database engine              |
| Cost                 | Moderate — shared compute, separate schema objects                |
| Complexity           | Moderate — migrations must run per schema                         |
| Scalability          | Good up to ~50 tenants; schema management overhead grows          |
| Cross-tenant queries | Difficult — requires UNION across schemas or separate aggregation |

**Best for:** Self-hosted adapter services where data isolation is critical and tenant count is manageable.

---

### Option B: Row-Level Isolation

All games share the same tables; a `tenant_id` column distinguishes records.

| Factor               | Assessment                                          |
| -------------------- | --------------------------------------------------- |
| Isolation            | Moderate — depends on application-layer enforcement |
| Cost                 | Low — fully shared infrastructure                   |
| Complexity           | Low — single schema, simple queries                 |
| Scalability          | Excellent — no structural changes as tenants grow   |
| Cross-tenant queries | Easy — natural aggregation with GROUP BY tenant_id  |

**Best for:** PlayFab-native services and self-hosted services with strict query governance.

---

### Option C: Database-per-Tenant

Each game gets its own dedicated database instance.

| Factor               | Assessment                                              |
| -------------------- | ------------------------------------------------------- |
| Isolation            | Maximum — complete physical separation                  |
| Cost                 | High — dedicated compute and storage per tenant         |
| Complexity           | High — provisioning, backups, migrations per database   |
| Scalability          | Poor — infrastructure cost scales linearly with tenants |
| Cross-tenant queries | Very difficult — requires federation layer              |

**Best for:** Not recommended for our use case. Over-engineering for 3 concurrent games.

---

## 4. Decision

### Primary Decision: Option B (Row-Level Isolation) for PlayFab-Native Services

All PlayFab-native services (Economy, Leaderboards, Cloud Script) will use **row-level isolation** with `tenant_id` mapping to PlayFab's native title ID. PlayFab already enforces title-level data segregation at the platform level; our application-layer `tenant_id` provides defense-in-depth.

### Secondary Decision: Option A (Schema-per-Tenant) for Self-Hosted Adapter

If/when the self-hosted adapter layer is activated (per IAuthService migration path), **schema-per-tenant** isolation will be used. This provides stronger isolation guarantees for services that will handle authentication, user data, and potentially sensitive telemetry — areas where row-level bugs could cause cross-tenant data leaks.

### Decision Matrix

| Service Type          | Isolation Model   | Tenant Identifier | Rationale                                            |
| --------------------- | ----------------- | ----------------- | ---------------------------------------------------- |
| PlayFab Economy       | Row-level         | Title ID          | PlayFab enforces segregation natively                |
| PlayFab Leaderboard   | Row-level         | Title ID          | Leaderboards are already title-scoped                |
| Self-hosted Auth      | Schema-per-tenant | Schema name       | High-sensitivity data; defense-in-depth required     |
| Self-hosted Telemetry | Schema-per-tenant | Schema name       | Large data volumes; schema partitioning aids pruning |
| Data Pipeline (Kafka) | Row-level         | tenant_id field   | Event streams carry tenant context naturally         |

---

## 5. Consequences

### Positive

- **Data isolation maintained:** Both models enforce strict tenant boundaries appropriate to the risk profile of each service
- **Shared infrastructure cost efficient:** Row-level model for PlayFab services maximizes resource utilization
- **Per-game analytics possible:** `tenant_id` enables natural aggregation and per-tenant reporting
- **Migration path preserved:** Schema-per-tenant for self-hosted services provides clean migration boundary
- **Audit-friendly:** Clear tenant boundaries support COPPA compliance auditing and data retention enforcement

### Negative

- **Row-level isolation requires careful query design:** Every query must include `tenant_id` filter; missing filters cause data leaks
- **Schema-per-tenant adds operational overhead:** Database migrations must execute per schema; backup/restore is per-schema
- **Cross-tenant reporting complexity:** Aggregated dashboards require union queries or dedicated aggregation pipelines

### Risks and Mitigations

| Risk                                           | Likelihood | Impact | Mitigation                                                    |
| ---------------------------------------------- | ---------- | ------ | ------------------------------------------------------------- |
| Cross-tenant data leak via missing `tenant_id` | Medium     | P0     | CI/CD gate: static analysis enforces tenant_id in all queries |
| Schema migration failure in schema-per-tenant  | Low        | P1     | Automated migration scripts with per-schema rollback          |
| Performance degradation from row-level queries | Low        | P2     | Composite indexes on (tenant_id, entity_id); query profiling  |
| Retrofit cost if multi-tenancy not built Day 1 | —          | —      | **This ADR mandates Day 1 multi-tenant design**               |

---

## 6. Implementation Notes

### 6.1 Database Query Enforcement

**All database queries must include `tenant_id` filter.** This is non-negotiable and will be enforced at multiple layers:

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Application Framework                          │
│ - ORM middleware auto-injects tenant_id WHERE clause    │
│ - Query builder rejects queries missing tenant_id       │
├─────────────────────────────────────────────────────────┤
│ Layer 2: API Gateway                                    │
│ - Request context includes tenant_id (from JWT/title ID)│
│ - Gateway validates tenant_id matches authenticated user│
├─────────────────────────────────────────────────────────┤
│ Layer 3: Database Policies                              │
│ - Row-level security policies (self-hosted PostgreSQL)  │
│ - Schema access restricted per service account          │
└─────────────────────────────────────────────────────────┘
```

### 6.2 API Gateway Tenant Routing

- API Gateway extracts tenant context from request (JWT claim, PlayFab title ID, or API key prefix)
- Tenant context propagated to all downstream services via request headers (`X-Tenant-ID`)
- Services reject requests missing valid tenant context with `401 Unauthorized`

### 6.3 PlayFab Title ID as Tenant Identifier

- PlayFab title ID (`{TitleId}`) serves as the canonical tenant identifier
- All PlayFab service calls are scoped to the calling game's title ID
- Cloud Script functions receive title ID in context; must propagate to external service calls

### 6.4 Self-Hosted Adapter Tenant Implementation

- IAuthService contract includes `tenant_id` in all service method signatures
- Service implementations use `tenant_id` to route to correct schema/database
- Unit tests include cross-tenant access attempt tests (must fail)

### 6.5 Code-Level Enforcement

```typescript
// Example: Tenant-aware repository pattern
interface ITenantRepository<T> {
  findById(tenantId: string, entityId: string): Promise<T | null>;
  findByQuery(tenantId: string, query: QueryFilter): Promise<T[]>;
  // No methods without tenantId parameter — compile-time enforcement
}

// Example: ORM middleware auto-injection
const tenantMiddleware = (req, res, next) => {
  const tenantId = req.headers["x-tenant-id"] || req.context.titleId;
  if (!tenantId)
    return res.status(401).json({ error: "Missing tenant context" });
  req.tenantId = tenantId;
  next();
};
```

---

## 7. Review and Governance

| Item                 | Detail                                          |
| -------------------- | ----------------------------------------------- |
| **ADR Owner**        | Priya Nair, Sr. Backend Engineer                |
| **CIO Review**       | Dr. Priya Mehta, Stage 3 gate review            |
| **CSO Consultation** | Dr. Sarah Chen (data isolation review)          |
| **CTO Consultation** | Dr. Kenji Nakamura (implementation feasibility) |
| **Status**           | Draft — pending Stage 3 gate review             |
| **Lock Date**        | Upon Stage 3 gate approval                      |
| **Re-entry Trigger** | New ADR required for any deviation              |

### Related ADRs

| ADR     | Title                 | Relationship                           |
| ------- | --------------------- | -------------------------------------- |
| ADR-001 | Platform Strategy     | Defines PlayFab + self-hosted boundary |
| ADR-003 | Cryptography Strategy | Tenant-scoped key management           |
| ADR-005 | API Pinning Strategy  | Per-tenant certificate validation      |

---

_This ADR satisfies CIO Audit Condition C3. It will be delivered as part of the Stage 3 UML Engineering Package and reviewed during the Stage 3 gate review._
