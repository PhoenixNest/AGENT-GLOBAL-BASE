---
name: shared-guidelines-multi-tenant-isolation
description: "Multi-tenant data isolation strategies, schema separation patterns, and tenant context management for SaaS applications — covering three isolation models (Silo, Bridge, Pool), application-level tenant enforcement with Row-Level Security, tenant provisioning workflows, and cryptographic data shredding for decommissioning. Use during Stage 5 (Development) and Stage 6 (Code Review) for multi-tenant architecture conformance. Trigger: multi-tenant, tenant isolation, SaaS architecture, tenant context, row-level security, tenant provisioning, data isolation, schema separation, tenant decommissioning."
prerequisites:
  - shared-overview

version: "1.0.0"
---

# Multi-Tenant Data Isolation

## Overview

This skill covers multi-tenant data isolation strategies, schema separation patterns, and tenant context management for SaaS applications. It is used by full-stack engineers during Stage 5 (Development) and Stage 6 (Code Review) for multi-tenant architecture conformance.

## Multi-Tenant Isolation Models

**Three isolation strategies** (trade-off: cost vs. security):

| Model                                | Description                           | Cost   | Isolation                      | Use Case                         |
| ------------------------------------ | ------------------------------------- | ------ | ------------------------------ | -------------------------------- |
| Silo (separate DB per tenant)        | Each tenant has dedicated database    | High   | Strong                         | Enterprise, regulated industries |
| Bridge (shared DB, separate schemas) | One database, schema per tenant       | Medium | Moderate                       | Mid-market SaaS                  |
| Pool (shared DB, shared schema)      | One database, tenant_id on all tables | Low    | Logical (application-enforced) | Self-serve, high-volume SaaS     |

## Pool Model: Tenant Context Management

**Application-level enforcement**:

```typescript
async function tenantMiddleware(req, res, next) {
  const tenantId = extractTenantId(req);
  req.tenantContext = { tenantId, schema: "public" };
  next();
}

class TenantRepository {
  async findAll(tenantContext) {
    return db.query("SELECT * FROM records WHERE tenant_id = $1", [
      tenantContext.tenantId,
    ]);
  }
}
```

**Critical safeguards**:

- Row-level security (RLS) policies in PostgreSQL as defense-in-depth.
- No tenant_id in URL paths (use subdomain or JWT claim).
- Automated test: every query must include tenant filter.

## Tenant Provisioning and Lifecycle

1. Tenant record created in management database.
2. Infrastructure provisioned (namespace, database, storage bucket).
3. Default configuration applied (roles, quotas, branding).
4. Health check: verify all provisioned resources are accessible.
5. Tenant activated: DNS record created, welcome email sent.

**Decommissioning**:

- Grace period: tenant marked as `pending_deletion` for 30 days.
- Data purging: cryptographic shredding (destroy encryption keys).
- Infrastructure cleanup: automated teardown.
