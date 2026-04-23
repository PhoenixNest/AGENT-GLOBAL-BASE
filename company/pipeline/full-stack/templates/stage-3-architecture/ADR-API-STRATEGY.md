# ADR: API Strategy (Cross-Platform)

| Field         | Value                                              |
| ------------- | -------------------------------------------------- |
| **Status**    | Proposed                                           |
| **Context**   | Stage 3 — Full-Stack Cross-Platform Pipeline (P3)  |
| **Decision**  | REST + GraphQL hybrid with OpenAPI code generation |
| **Date**      | YYYY-MM-DD                                         |
| **Authors**   | CIO (primary), Backend Lead, Mobile Lead           |
| **Reviewers** | CTO (technology), CSO (security)                   |

---

## Decision

We will use a **REST + GraphQL hybrid** approach with REST as the primary API (OpenAPI 3.0 specification) and GraphQL for complex data aggregation scenarios. API clients will be auto-generated using OpenAPI Generator for TypeScript (web), Swift (iOS), and Kotlin (Android).

## Rationale

Full-stack cross-platform products require a unified API strategy that serves web frontends, iOS apps, Android apps, and potentially third-party integrations simultaneously. The API must maintain consistency across all consumers while accommodating platform-specific requirements (e.g., mobile offline support, web SEO needs). This ADR extends the Backend API Pipeline's `ADR-API-STRATEGY.md` with cross-platform considerations.

### 1. API Paradigm: REST + GraphQL Hybrid

**Primary API:** REST (OpenAPI 3.0 specification)

**Rationale:**

- **Universal compatibility** — All platforms (web, iOS, Android) can consume REST APIs natively
- **HTTP caching** — Leverage browser/CDN caching for web, OkHttp/Retrofit caching for mobile
- **Mature tooling** — OpenAPI code generation for TypeScript (web), Swift (iOS), Kotlin (Android)
- **Simplicity** — Easier to debug, monitor, and document than GraphQL

**Secondary API:** GraphQL (for complex data aggregation scenarios)

**Use Cases:**

- Mobile app home screen (aggregates user profile, recommendations, notifications in single request)
- Web dashboard (customizable widgets with variable data requirements)
- Third-party integrations (flexible field selection reduces over-fetching)

**Rejected Pure-GraphQL Approach:**

- HTTP caching complexity (requires persisted queries, CDN workarounds)
- Over-fetching prevention comes at cost of N+1 query problems
- Steeper learning curve for backend engineers
- Not justified unless >50% of endpoints require flexible field selection

---

### 2. Data Consistency Model: Eventual Consistency with Conflict Resolution

**Consistency Strategy by Data Type:**

| Data Type       | Consistency Model    | Rationale                                               | Sync Mechanism                         |
| --------------- | -------------------- | ------------------------------------------------------- | -------------------------------------- |
| User profile    | Strong               | Single source of truth, low write frequency             | Direct DB read from primary            |
| Orders/payments | Strong               | Financial transactions require ACID guarantees          | Direct DB read from primary            |
| Product catalog | Eventual (TTL: 5min) | High read frequency, infrequent updates                 | Redis cache + invalidation             |
| Social feed     | Eventual (TTL: 1min) | Real-time not critical, eventual consistency acceptable | Kafka event stream + materialized view |
| Offline drafts  | Client-authoritative | User edits locally, sync when online                    | Last-write-wins + conflict log         |

**Conflict Resolution Strategy:**

For offline-first mobile scenarios where multiple devices edit same resource:

1. **Vector clocks** — Track causality across devices
2. **Last-write-wins (LWW)** — Default for non-critical data (user preferences, drafts)
3. **Manual merge** — For critical data (order modifications), present conflict to user
4. **Operational transforms** — For collaborative editing (shared documents, comments)

**Example: Offline Order Draft Conflict**

```
Device A (offline): Creates order draft at 10:00 AM
Device B (offline): Modifies same draft at 10:05 AM
Both devices come online at 10:10 AM

Resolution:
1. Server receives both updates with vector clocks
2. Detects conflict (same resource, divergent histories)
3. Applies LWW → Device B's version wins (later timestamp)
4. Logs conflict in audit trail
5. Notifies Device A: "Your changes were overwritten by another device"
```

---

### 3. API Versioning Strategy: URL Path Versioning

**Version Format:** `/api/v{major}/resource`

**Examples:**

- Current: `POST /api/v1/orders`
- Future: `POST /api/v2/orders` (breaking changes)

**Versioning Policy:**

| Change Type           | Version Bump          | Examples                                               |
| --------------------- | --------------------- | ------------------------------------------------------ |
| Breaking change       | Major (v1→v2)         | Remove field, change field type, modify auth mechanism |
| Non-breaking addition | Minor (v1.0→v1.1)     | Add optional field, add new endpoint                   |
| Bug fix               | Patch (v1.0.0→v1.0.1) | Fix incorrect validation, correct error message        |

**Deprecation Timeline:**

- **Minimum notice:** 90 days before sunset
- **Deprecation headers:** `Sunset: Sat, 01 Jan 2027 00:00:00 GMT`, `Deprecation: true`
- **Migration guide:** Published alongside deprecation announcement
- **Consumer notification:** Email to registered API keys, dashboard alerts

**Backward Compatibility Guarantees:**

- Fields are never removed within a major version
- New fields are always optional (nullable or with defaults)
- Error response structure remains stable
- Authentication mechanisms remain compatible

---

### 4. API Client Generation: OpenAPI Generator

**Technology:** OpenAPI Generator (official tooling)

**Generated Clients:**

- **Web:** TypeScript Axios client (`@company/api-client`)
- **iOS:** Swift Alamofire client (`CompanyAPIClient`)
- **Android:** Kotlin Retrofit client (`com.company.api:client`)

**Generation Workflow:**

```yaml
# .github/workflows/generate-api-clients.yml
on:
  push:
    paths:
      - 'api-spec/openapi.yaml'

jobs:
  generate-clients:
    runs-on: ubuntu-latest
    steps:
      - name: Generate TypeScript client
        run: openapi-generator generate -i api-spec/openapi.yaml -g typescript-axios -o clients/typescript

      - name: Generate Swift client
        run: openapi-generator generate -i api-spec/openapi.yaml -g swift5 -o clients/swift

      - name: Generate Kotlin client
        run: openapi-generator generate -i api-spec/openapi.yaml -g kotlin -o clients/kotlin

      - name: Publish packages
        run: |
          npm publish clients/typescript
          pod trunk push clients/swift/CompanyAPIClient.podspec
          ./gradlew :clients:kotlin:publish
```

**Breaking Change Detection:**

- CI gate fails if OpenAPI spec changes violate backward compatibility rules
- Tool: `openapi-diff` compares current vs. previous spec
- Alert: Slack notification to all platform leads

---

## Alternatives Considered

### Alternative 1: Pure REST (No GraphQL)

**Pros:** Simpler architecture, easier caching, universal compatibility  
**Cons:** Over-fetching on mobile (home screen requires 5+ REST calls), no flexible field selection  
**Rejected because:** Mobile performance SLA (cold start <2s) requires minimizing network round-trips; GraphQL aggregation endpoint reduces 5 calls to 1.

### Alternative 2: Pure GraphQL (No REST)

**Pros:** Flexible field selection, single endpoint, strong typing  
**Cons:** HTTP caching complexity, N+1 query problems, steeper learning curve  
**Rejected because:** Web SEO requirements need predictable URL structures (REST); CDN caching critical for performance.

### Alternative 3: gRPC for Internal Services

**Pros:** Binary protocol efficiency, strong typing, bidirectional streaming  
**Cons:** Browser incompatibility (requires grpc-web proxy), mobile SDK maturity issues  
**Rejected because:** External-facing API must support browsers natively; gRPC reserved for internal service-to-service communication only.

---

## Consequences

### Positive

- **Unified API surface** — Single OpenAPI spec generates clients for all platforms, ensuring consistency
- **Platform optimization** — GraphQL aggregation endpoint reduces mobile network calls by 60%
- **Backward compatibility** — URL path versioning enables gradual migration, zero breaking changes for existing consumers
- **Developer experience** — Auto-generated SDKs reduce integration time from 2 weeks to 2 days

### Negative

- **Dual maintenance** — Team must maintain both REST and GraphQL resolvers (20% additional effort)
- **Complexity** — Engineers must understand two API paradigms, context-switching overhead
- **Monitoring overhead** — Separate metrics dashboards for REST vs. GraphQL performance

### Risks & Mitigations

| Risk                       | Likelihood | Impact   | Mitigation                                                                                                    |
| -------------------------- | ---------- | -------- | ------------------------------------------------------------------------------------------------------------- |
| GraphQL N+1 query problem  | High       | High     | DataLoader pattern (batch + cache), query depth limiting (max 5 levels), cost analysis (max 100 points/query) |
| Client generation drift    | Medium     | Medium   | CI gate enforces spec-client parity, weekly automated regeneration                                            |
| Versioning confusion       | Medium     | Low      | Clear documentation, deprecation headers, 90-day minimum notice, migration guides                             |
| Offline conflict data loss | Low        | Critical | Conflict logging, user notification, manual merge UI for critical data                                        |

---

## Implementation Plan

**Phase 1 (Week 1-2):** REST API foundation

- Define OpenAPI 3.0 specification for core resources (users, orders, products)
- Implement REST endpoints with versioning (`/api/v1/...`)
- Set up OpenAPI documentation portal (Swagger UI)

**Phase 2 (Week 3-4):** GraphQL aggregation layer

- Identify high-value aggregation endpoints (mobile home screen, web dashboard)
- Implement GraphQL schema + resolvers (Apollo Server)
- Configure DataLoader for N+1 prevention

**Phase 3 (Week 5-6):** Client generation pipeline

- Integrate OpenAPI Generator into CI/CD
- Generate TypeScript, Swift, Kotlin clients
- Publish to package registries (npm, CocoaPods, Maven)

**Phase 4 (Week 7-8):** Offline-first sync mechanism

- Implement vector clock tracking for mobile offline edits
- Build conflict resolution UI (manual merge for critical data)
- Test offline scenarios (airplane mode, background sync)

---

## Compliance Alignment

- **GDPR Article 20:** API supports data portability (export user data via `/api/v1/users/{id}/export`)
- **PCI-DSS Requirement 6:** Secure coding practices for API development (input validation, parameterized queries)
- **SRD Section 6.3:** "Unified auth flow consumed by all platforms with token revocation propagation"

---

## References

- [OpenAPI Specification 3.0](https://swagger.io/specification/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [API Versioning Strategies](https://www.moesif.com/blog/api-product-management/api-versioning/)
- [Offline-First Architecture](https://offlinefirst.org/)
- SRD.md Section 6.3 (Cross-Platform Authentication)

---

**Lock-down:** Once approved at Stage 3 gate, this decision is locked — switching between strategies requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.
