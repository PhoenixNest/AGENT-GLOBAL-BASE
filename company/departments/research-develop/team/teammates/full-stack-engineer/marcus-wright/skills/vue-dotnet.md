---
version: "1.0.0"
---

| Competency                | Description                                                                             | Quality Criteria                                                                                                                                 |
| ------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Vue 3 Composition API     | ref, reactive, computed, watch, watchEffect, composables                                | Uses Composition API exclusively (no Options API); designs reusable composables; understands reactivity system internals                         |
| .NET Minimal APIs         | Endpoint routing, parameter binding, result types, filter pipeline                      | Designs RESTful endpoints with Minimal API syntax; implements validation with FluentValidation; uses endpoint filters for cross-cutting concerns |
| Entity Framework Core     | Code-first migrations, relationships, LINQ queries, performance optimization            | Designs entity models with correct relationships; writes efficient LINQ queries; configures migrations for schema evolution                      |
| Multi-Tenant Architecture | Schema-per-tenant, discriminator column, connection string routing, data isolation      | Implements tenant resolution middleware; configures EF Core for tenant isolation; designs migration strategy for multi-tenant schema             |
| Role-Based Access Control | JWT authentication, policy-based authorization, role management, permission granularity | Configures ASP.NET Core Identity with JWT; implements policy-based authorization with requirements; manages role-permission hierarchy            |

## Pipeline Integration

**Stage 5 (Development):** Vue 3 components use Composition API. .NET Minimal APIs implement all endpoints. EF Core entities configured with multi-tenant filters. RBAC policies enforced.

**Stage 6 (Code Review):** Review composable reusability. Validate EF Core query efficiency (no N+1). Check multi-tenant data isolation. Verify RBAC coverage.

**Stage 7 (Testing):** Vue component tests with Vitest. API integration tests with WebApplicationFactory. EF Core tests with SQLite in-memory. Multi-tenant isolation tests.

## Quality Standards

| Metric                     | Target                                  | Measurement            |
| -------------------------- | --------------------------------------- | ---------------------- |
| Composition API usage      | 100% new components use Composition API | Code review            |
| Multi-tenant isolation     | 0 cross-tenant data leaks               | Security audit         |
| RBAC coverage              | 100% endpoints have authorization       | Security audit         |
| EF Core query efficiency   | 0 N+1 queries                           | Query count monitoring |
| Vue reactivity correctness | 0 stale data bugs                       | Bug tracking           |
| API response time (p95)    | < 200ms                                 | Application metrics    |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
