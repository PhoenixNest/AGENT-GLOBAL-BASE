---
name: api-versioning
description: Manages REST API versioning across the product lifecycle, implementing versioning strategies (URL path, header, media type), backward compatibility patterns.
---

# API Versioning

**Category:** API Architecture
**Owner:** Full-Stack Engineer (Marcus Wright)

## Overview

Manages REST API versioning across the product lifecycle, implementing versioning strategies (URL path, header, media type), backward compatibility patterns, feature flag-driven gradual rollouts, rollback procedures for breaking changes, and multi-tenant data isolation to ensure different tenant versions coexist without conflict.

## Competency Dimensions

| Dimension                   | Description                                                                                        | Proficiency Indicators                                                                                                                           |
| --------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Versioning Strategies       | URL path (/v1/, /v2/), custom header (X-API-Version), media type (application/vnd.company.v2+json) | Selects versioning strategy based on consumer needs; implements multiple versioning approaches simultaneously; documents version lifecycle       |
| Backward Compatibility      | Non-breaking changes, additive updates, deprecated field handling, response shape preservation     | Identifies breaking vs non-breaking changes; implements additive-only changes within a version; deprecates fields gracefully with sunset headers |
| Feature Flags               | Gradual rollout, canary releases, user targeting, kill switches                                    | Implements feature flags for API behavior changes; configures rollout percentages; monitors feature flag impact                                  |
| Rollback Procedures         | Version deprecation, traffic shifting, data migration rollback, emergency rollback                 | Designs rollback procedures for each deployment; tests rollback in staging; documents rollback runbooks                                          |
| Multi-Tenant Data Isolation | Tenant-scoped data, version-aware queries, cross-tenant compatibility                              | Ensures tenant data is isolated across API versions; handles version migration per tenant; prevents data leakage between versions                |

## Execution Guidance

### API Versioning Strategies

**Strategy comparison:**

| Strategy                   | Example                                   | Pros                            | Cons                          | Best For                 |
| -------------------------- | ----------------------------------------- | ------------------------------- | ----------------------------- | ------------------------ |
| URL Path                   | `/api/v1/users`                           | Simple, visible, cacheable      | URL changes on version bump   | Public APIs, mobile apps |
| Custom Header              | `X-API-Version: 2026-04-01`               | Clean URLs, flexible versioning | Harder to test in browser     | Internal APIs, B2B       |
| Media Type (Accept header) | `Accept: application/vnd.company.v2+json` | RESTful, content negotiation    | Complex, poor tooling support | Mature API programs      |
| Query Parameter            | `/api/users?version=2`                    | Easy to test                    | Not RESTful, cache issues     | Internal testing         |

**Recommended: URL path for public APIs, header for internal APIs.**

**URL path versioning (.NET):**

```csharp
// Versioned endpoint groups
var v1 = app.MapGroup("/api/v1").WithTags("v1");
var v2 = app.MapGroup("/api/v2").WithTags("v2");

// v1 - original endpoint
v1.MapGet("/users", async (IUserService userService) =>
{
    var users = await userService.GetUsersAsync();
    return Results.Ok(users.Select(u => new UserV1Response(u)));
});

// v2 - new endpoint with additional fields
v2.MapGet("/users", async (IUserService userService) =>
{
    var users = await userService.GetUsersAsync();
    return Results.Ok(users.Select(u => new UserV2Response(u)));
});

// Versioned response DTOs
public record UserV1Response(
    Guid Id,
    string Name,
    string Email
);

public record UserV2Response(
    Guid Id,
    string Name,
    string Email,
    string Role,
    DateTime CreatedAt,
    string DisplayName  // New field in v2
);

// Versioned routing with fallback
app.MapGet("/api/users", async (
    HttpContext context,
    IUserService userService) =>
{
    var version = context.Request.Headers["X-API-Version"].FirstOrDefault() ?? "v1";

    return version switch
    {
        "v2" => Results.Ok(await GetV2Response(userService)),
        "v1" or _ => Results.Ok(await GetV1Response(userService)),
    };
});
```

**URL path versioning (FastAPI):**

```python
from fastapi import APIRouter

# Versioned routers
router_v1 = APIRouter(prefix="/api/v1", tags=["v1"])
router_v2 = APIRouter(prefix="/api/v2", tags=["v2"])

@router_v1.get("/users")
async def get_users_v1(db: Session = Depends(get_db)):
    """v1: Basic user list."""
    users = db.query(User).all()
    return [UserResponseV1.model_validate(u) for u in users]

@router_v2.get("/users")
async def get_users_v2(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """v2: Paginated user list with additional fields."""
    query = db.query(User).order_by(User.created_at.desc())
    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": [UserResponseV2.model_validate(u) for u in users],
        "total": total,
        "page": page,
        "page_size": page_size,
    }

app.include_router(router_v1)
app.include_router(router_v2)
```

### Backward Compatibility Patterns

**Breaking vs non-breaking change classification:**

| Change Type             | Breaking? | Example                            | Migration Strategy                   |
| ----------------------- | --------- | ---------------------------------- | ------------------------------------ |
| Add optional field      | No        | Add `role` field to response       | Add field, document, no version bump |
| Add required field      | Yes       | Require `timezone` in request      | New version or default value         |
| Remove field            | Yes       | Remove `displayName` from response | New version with deprecation period  |
| Change field type       | Yes       | `id: string` → `id: integer`       | New version                          |
| Change field name       | Yes       | `userName` → `name`                | New version, keep old as alias       |
| Change error format     | Yes       | Different error response shape     | New version                          |
| Add new endpoint        | No        | `POST /api/users/{id}/avatar`      | No version bump needed               |
| Change auth requirement | Yes       | Public → authenticated             | New version or migration period      |

**Additive-only evolution within a version:**

```python
# v1 response — can ADD fields but NOT remove or change
class UserResponseV1(BaseModel):
    id: str
    name: str
    email: str
    # Added in v1.1 — non-breaking (additive)
    role: str | None = None
    # Added in v1.2 — non-breaking (additive)
    avatar_url: str | None = None

# Deprecation with sunset header
@app.get("/api/v1/users/{user_id}")
async def get_user_v1(user_id: str, response: Response):
    response.headers["Sunset"] = "Sat, 01 Jan 2027 00:00:00 GMT"
    response.headers["Deprecation"] = "true"
    response.headers["Link"] = '</api/v2/users/{user_id}>; rel="successor-version"'

    user = await get_user(user_id)
    return UserResponseV1.model_validate(user)
```

**Response shape preservation (never break existing consumers):**

```typescript
// v1 consumer expects this shape:
// { id, name, email }

// v1.1 adds fields — v1 consumer ignores unknown fields (safe)
// { id, name, email, role, avatar_url }

// v2 changes shape — v1 consumer would break → new version needed
// { data: { id, name, email }, meta: { ... } }
```

### Feature Flags for Gradual Rollout

```typescript
// Feature flag service for API behavior changes
class APIFeatureFlags {
  private flags: Map<string, FeatureFlag> = new Map();

  async isEnabled(flag: string, userId?: string): Promise<boolean> {
    const flagConfig = this.flags.get(flag);
    if (!flagConfig) return false;

    // Percentage rollout
    if (flagConfig.rolloutPercentage !== undefined) {
      const hash = this.hashUserId(userId ?? 'anonymous');
      return hash % 100 < flagConfig.rolloutPercentage;
    }

    return flagConfig.enabled ?? false;
  }

  private hashUserId(userId: string): number {
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      hash = (hash << 5) - hash + userId.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash);
  }
}

// Feature-gated API endpoint
app.get('/api/v2/users', async (req, res) => {
  const useNewFormat = await featureFlags.isEnabled('api-v2-response-format', req.user?.id);

  const users = await userService.getUsers();

  if (useNewFormat) {
    // New paginated format
    res.json({
      data: users,
      meta: { total: users.length, page: 1 },
    });
  } else {
    // Legacy format
    res.json(users);
  }
});
```

**Feature flag rollout phases:**

```yaml
# Rollout configuration
feature: api-v2-response-format
phases:
  - name: Internal
    rollout: 100%
    audience: internal-users
    duration: 1 week

  - name: Beta
    rollout: 5%
    audience: opted-in-beta
    duration: 2 weeks

  - name: Canary
    rollout: 25%
    audience: all-users
    duration: 1 week

  - name: Expanded
    rollout: 75%
    audience: all-users
    duration: 1 week

  - name: Full
    rollout: 100%
    audience: all-users
    duration: permanent

# Monitoring during rollout
alerts:
  - metric: error_rate
    threshold: '> 1%'
    action: halt rollout

  - metric: latency_p99
    threshold: '> 500ms'
    action: halt rollout

  - metric: consumer_complaints
    threshold: '> 5 per day'
    action: review rollout
```

### Rollback Procedures

**Rollback runbook:**

```markdown
# API Version Rollback Runbook

## Scenario: v2 endpoint causing errors

### Step 1: Assess Impact

- Check error rate in monitoring dashboard
- Identify affected consumers (by API key or user segment)
- Determine root cause (code bug, data issue, infrastructure)

### Step 2: Immediate Mitigation

# If code bug:

- Deploy previous version: kubectl rollout undo deployment/api-v2
- Or shift traffic back to v1: update load balancer weights

# If data issue:

- Run data repair script
- Or revert data migration

### Step 3: Communicate

- Notify affected consumers via status page
- Send email to API consumer mailing list
- Update API changelog

### Step 4: Root Cause Analysis

- Conduct postmortem within 48 hours
- Document findings and preventive measures
- Update testing procedures

### Step 5: Retry Deployment

- Fix identified issue
- Deploy to staging first
- Run full regression test suite
- Deploy with smaller rollout percentage
```

**Infrastructure rollback (Kubernetes):**

```yaml
# Traffic shifting with Istio
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-routing
spec:
  hosts:
    - api.company.com
  http:
    - match:
        - headers:
            x-api-version:
              exact: v2
      route:
        - destination:
            host: api-v2
            subset: stable
          weight: 90
        - destination:
            host: api-v2
            subset: canary
          weight: 10

    - route: # Default to v1
        - destination:
            host: api-v1
          weight: 100

# Emergency rollback: shift all traffic to v1
# kubectl patch virtualservice api-routing --type=json -p='[
#   {"op": "replace", "path": "/spec/http/1/route/0/weight", "value": 100}
# ]'
```

### Multi-Tenant Data Isolation

**Version-aware data queries:**

```csharp
// Each tenant can be on a different API version
public class Tenant
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public string ApiVersion { get; set; } = "v1";
    public DateTime? ApiVersionUpgradedAt { get; set; }
}

// Service layer respects tenant's API version
public class UserService
{
    public async Task<object> GetUsersForTenantAsync(Guid tenantId)
    {
        var tenant = await _tenantRepository.GetByIdAsync(tenantId);
        var users = await _userRepository.GetByTenantAsync(tenantId);

        return tenant.ApiVersion switch
        {
            "v2" => users.Select(u => new UserV2Response(u)),
            _ => users.Select(u => new UserV1Response(u)),
        };
    }
}

// Data migration for tenant version upgrade
public async Task MigrateTenantToV2Async(Guid tenantId)
{
    // 1. Validate tenant data is compatible with v2
    var compatibility = await ValidateV2Compatibility(tenantId);
    if (!compatibility.IsCompatible)
    {
        throw new MigrationException(
            $"Tenant {tenantId} has incompatible data: {compatibility.Errors}");
    }

    // 2. Run data migration
    await RunDataMigration(tenantId, "v1-to-v2");

    // 3. Update tenant version
    await _tenantRepository.UpdateVersionAsync(tenantId, "v2");

    // 4. Verify migration
    var verification = await VerifyMigration(tenantId);
    if (!verification.IsSuccess)
    {
        // Rollback
        await RollbackMigration(tenantId, "v1");
        throw new MigrationException($"Migration failed: {verification.Errors}");
    }
}
```

**Cross-version data compatibility:**

```
When multiple API versions coexist:

v1 writes: { name, email }
v2 writes: { name, email, role, avatar_url }

Both versions read from same database.
v1 reader ignores unknown fields (role, avatar_url).
v2 reader provides defaults for missing fields (role = null).

Key rules:
1. Never remove columns used by active versions
2. Use nullable columns for new fields
3. Use default values for missing data
4. Run cleanup migration only after ALL tenants upgrade
```

## Pipeline Integration

**Stage 3 (Architecture):** API versioning strategy documented with rationale. Backward compatibility policy defined. Multi-tenant version isolation approach specified.

**Stage 4 (Implementation Plan):** Version rollout phases defined with feature flag configuration. Rollback procedures documented per version. Data migration plans for version upgrades.

**Stage 5 (Development):** Versioned endpoints implemented. Feature flags configured for gradual rollout. Backward compatibility maintained within versions.

**Stage 6 (Code Review):** Review version routing correctness. Validate backward compatibility (no breaking changes within version). Check feature flag implementation. Verify multi-tenant isolation.

**Stage 10 (Release Readiness):** Panel confirms version rollout plan is ready. Rollback procedures tested. Monitoring alerts configured for rollout metrics.

## Quality Standards

| Metric                 | Target                                     | Measurement               |
| ---------------------- | ------------------------------------------ | ------------------------- |
| Backward compatibility | 0 breaking changes within a version        | API contract testing      |
| Rollout error rate     | < 1% during gradual rollout                | Monitoring during rollout |
| Rollback time          | < 15 minutes                               | Rollback drill timing     |
| Multi-tenant isolation | 0 cross-tenant data leaks                  | Security audit            |
| Deprecation compliance | Sunset headers on all deprecated endpoints | API linting               |
| Documentation accuracy | 100% of versions documented                | Documentation audit       |
| Feature flag cleanup   | 0 stale flags after full rollout           | Flag inventory audit      |
