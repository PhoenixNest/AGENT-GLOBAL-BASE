---
name: frontend-web-vue-dotnet
description: Vue 3 + .NET full-stack development — Vue Composition API with ref/computed/watch, .NET Minimal APIs, Entity Framework Core code-first, multi-tenant architecture, and JWT RBAC. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 5 (Development) for Vue/.NET integration. Trigger: vue dotnet, vue 3 composition api, .net minimal apis, entity framework core, multi-tenant vue, jwt authentication vue.
prerequisites:
  - frontend-web-vue-vite-advanced

version: "1.0.0"
---

# Vue 3 + .NET Integration

**Category:** Full-Stack Engineering (C#/Vue)
**Owner:** Full-Stack Engineer (Marcus Wright)

## Overview

Builds full-stack applications using Vue 3 Composition API frontend with .NET 7+ Minimal APIs backend, covering reactive state management with ref/computed/watch, Entity Framework Core with code-first migrations, multi-tenant architecture patterns, and role-based access control with JWT authentication.

## Competency Dimensions

| Dimension                 | Description                                                                             | Proficiency Indicators                                                                                                                           |
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
