---
name: multi-tenant-isolation
description: Design and implement multi-tenant data isolation for SaaS applications — choosing between row-level security, schema-per-tenant, and database-per-tenant strategies — with PostgreSQL Row Level Security as the primary implementation pattern.
version: "1.0.0"
---

# Multi Tenant Isolation

| Competency                | Description                                                                | Quality Criteria                                                                                                                         |
| ------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Isolation Model Selection | Choose the right isolation model for the tenant count and compliance needs | Decision documented in an ADR with tenant count projections, data sensitivity analysis, and cost comparison                              |
| PostgreSQL RLS            | Implement Row Level Security policies for tenant data isolation            | RLS enabled on all multi-tenant tables; `SET app.tenant_id` used in connection pooling; policies tested with tenant cross-access attempt |
| Tenant Context Injection  | Inject tenant context securely through the request lifecycle               | Tenant ID derived from JWT claim (never from user-supplied request body); injected into DB connection before any query                   |
| Isolation Testing         | Verify tenant boundaries hold under adversarial test conditions            | Automated tests attempt cross-tenant data access; all attempts return empty result or 403; no data leakage possible                      |

## Execution Guidance

### PostgreSQL RLS Implementation

```sql
-- Enable RLS on table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create isolation policy
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Application sets tenant context on connection acquire
SET app.tenant_id = '550e8400-e29b-41d4-a716-446655440000';
```

### Isolation Model Comparison

| Model               | Tenant Scale | Isolation Level | Cost   | Best For                          |
| ------------------- | ------------ | --------------- | ------ | --------------------------------- |
| Shared DB + RLS     | 1–10K        | Logical         | Low    | SaaS with standard compliance     |
| Schema-per-tenant   | 1–500        | Logical         | Medium | Medium isolation + customization  |
| Database-per-tenant | 1–50         | Physical        | High   | Regulated industries (HIPAA etc.) |

For the company's current scale and compliance requirements, PostgreSQL RLS is the correct default. Document the decision in an ADR and revisit when tenant count approaches the model's scalability ceiling.
