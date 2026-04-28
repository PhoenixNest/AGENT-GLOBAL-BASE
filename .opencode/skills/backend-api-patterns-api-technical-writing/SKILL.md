---
name: backend-api-patterns-api-technical-writing
description: API documentation authoring for backend services — OpenAPI/Swagger specification writing, endpoint reference documentation, multi-language code examples, SDK documentation, and developer portal content. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 4 (Implementation Plan) for documentation planning and Stage 5 (Development) for API docs generation. Trigger: api documentation, openapi spec, swagger docs, developer portal, api reference, sdk documentation, code examples.
prerequisites:
  - backend-overview

version: "1.0.0"
---

# API Technical Writing

**Category:** Technical Documentation / Developer Experience
**Owner:** Technical Writer

## Overview

Authors and maintains comprehensive API documentation for all platform services, including OpenAPI/Swagger specification documents, endpoint reference documentation, code examples in multiple languages, SDK documentation, and developer portal content. API documentation is the primary interface between the platform and its consumers — internal engineers, integration partners, and (where applicable) external developers — and must be accurate, discoverable, and actionable.

This skill covers API documentation standards, OpenAPI/Swagger spec authoring, endpoint reference conventions, code example generation, SDK documentation structure, and developer portal content management. All API documentation follows documentation-as-code practices and is versioned alongside the API it describes.

## Competency Dimensions

| Dimension                        | Description                                                                                                        | Proficiency Indicators                                                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| OpenAPI/Swagger Authoring        | Write valid, comprehensive OpenAPI 3.x specifications covering all endpoints, schemas, and operations              | Can produce a publication-ready OpenAPI spec from API design docs in ≤8 hours; zero validation errors from OpenAPI linter |
| Endpoint Reference Documentation | Write clear, structured endpoint docs with request/response examples, error codes, and authentication requirements | Engineers rate endpoint docs ≥4.3/5 for clarity; zero integration defects traced to documentation gaps                    |
| Code Example Generation          | Produce accurate, production-quality code examples in Kotlin, Swift, and Dart (Flutter)                            | Examples compile and run against test environment; ≥95% example accuracy rate on automated validation                     |
| SDK Documentation                | Structure SDK reference docs with class hierarchies, method signatures, usage patterns, and migration guides       | SDK docs pass developer review on first submission; adoption rate of documented patterns ≥85%                             |
| Developer Portal Content         | Manage developer portal content architecture, navigation, search optimization, and content freshness               | Portal search success rate ≥90%; content freshness score ≥95% (all pages reviewed within 90 days)                         |
| API Versioning Documentation     | Document API versioning strategy, deprecation notices, migration paths, and backward compatibility guarantees      | Zero consumer breakages due to undocumented API changes; deprecation notices published ≥90 days before sunset             |

## Overview

[1-2 sentences describing what this endpoint does and when to use it]

## Authentication

Required scopes: `resources:read`
Auth method: Bearer token (JWT)

## Request

### Path Parameters

| Parameter    | Type            | Required | Description                        |
| ------------ | --------------- | -------- | ---------------------------------- |
| `resourceId` | `string (UUID)` | Yes      | Unique identifier for the resource |

### Query Parameters

| Parameter | Type      | Required | Default | Description                                        |
| --------- | --------- | -------- | ------- | -------------------------------------------------- |
| `page`    | `integer` | No       | `1`     | Page number (1-based)                              |
| `limit`   | `integer` | No       | `20`    | Items per page (max 100)                           |
| `sort`    | `string`  | No       | —       | Sort field and direction (e.g., `created_at:desc`) |
| `fields`  | `string`  | No       | —       | Comma-separated field list for sparse fieldsets    |

### Request Body

Not applicable for GET requests.

### Request Headers

| Header          | Type     | Required | Description                   |
| --------------- | -------- | -------- | ----------------------------- |
| `Authorization` | `string` | Yes      | `Bearer <JWT access token>`   |
| `Accept`        | `string` | No       | `application/json` (default)  |
| `X-Request-ID`  | `string` | No       | Unique request ID for tracing |

## Response

### 200 OK

**Content-Type:** `application/json`

```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Example Resource",
      "description": "This is an example resource.",
      "status": "active",
      "created_at": "2026-01-15T10:30:00Z",
      "updated_at": "2026-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "current_page": 1,
    "total_pages": 3,
    "total_count": 42,
    "per_page": 20
  },
  "links": {
    "self": "/api/v1/resources?page=1&limit=20",
    "first": "/api/v1/resources?page=1&limit=20",
    "last": "/api/v1/resources?page=3&limit=20",
    "next": "/api/v1/resources?page=2&limit=20"
  }
}
```

````

### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required. Include a valid JWT access token in the Authorization header.",
    "status": 401
  }
}
````

### 403 Forbidden

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You do not have the required permissions to perform this operation.",
    "status": 403
  }
}
```

### 429 Too Many Requests

**Headers:** `Retry-After: 60`

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Please retry after the specified duration.",
    "status": 429
  }
}
```

## Rate Limits

| Tier     | Requests per minute | Requests per day |
| -------- | ------------------- | ---------------- |
| Standard | 60                  | 10,000           |
| Premium  | 300                 | 100,000          |

## Code Examples

### Kotlin (Android)

```kotlin
val response = apiService.getResources(
    page = 1,
    limit = 20,
    sort = "created_at:desc"
)
if (response.isSuccessful) {
    val resources = response.body()?.data ?: emptyList()
    // Handle resources
} else {
    // Handle error: response.code(), response.errorBody()
}
```

### Swift (iOS)

```swift
let task = URLSession.shared.dataTask(with: url) { data, response, error in
    guard let data = data, error == nil else {
        // Handle error
        return
    }
    let resources = try? JSONDecoder().decode(ResourceListResponse.self, from: data)
    // Handle resources
}
task.resume()
```

### Dart (Flutter)

```dart
final response = await http.get(
  Uri.parse('https://api.company.com/v1/resources?page=1&limit=20'),
  headers: {'Authorization': 'Bearer $accessToken'},
);

if (response.statusCode == 200) {
  final resources = ResourceListResponse.fromJson(jsonDecode(response.body));
  // Handle resources
} else {
  // Handle error: response.statusCode, response.body
}
```

## Related Endpoints

- [POST /api/v1/resources](./create-resource.md) — Create a new resource
- [GET /api/v1/resources/{resourceId}](./get-resource.md) — Get a specific resource
- [DELETE /api/v1/resources/{resourceId}](./delete-resource.md) — Delete a resource

## Overview

[1-2 sentences describing what this service does and when to use it]

## Initialization

```kotlin
val resourceService = apiClient.resources
```

## Pipeline Integration

| Pipeline Stage                   | API Documentation Relevance                                                                                                                   |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 1-4                        | Not applicable — API documentation not in scope during requirements, design, architecture, or planning stages                                 |
| Stage 5 (Development)            | **Primary creation stage** — API documentation authored alongside API implementation; OpenAPI spec generated or maintained as code is written |
| Stage 6 (Code Review)            | API documentation reviewed as part of code review; documentation accuracy validated against implementation                                    |
| Stage 7 (Testing)                | API examples tested against staging environment; test coverage includes documentation example validation                                      |
| Stage 8 (Integrity Verification) | Panel verifies API implementation matches documented specification; discrepancies flagged as defects                                          |
| Stage 9 (i18n)                   | API documentation updated if i18n affects API (e.g., locale-specific endpoints, translation API)                                              |
| Stage 10 (Release)               | API documentation reviewed as part of release readiness; developer portal content validated for accuracy                                      |

## Quality Standards

- **OpenAPI Validation:** 100% of OpenAPI specs pass `spectral` lint with zero errors and zero warnings before merge
- **Endpoint Coverage:** 100% of API endpoints have complete reference documentation (request, response, errors, examples, code samples)
- **Code Example Accuracy:** ≥95% of code examples compile and execute successfully against staging environment; validated by CI on every API change
- **Documentation Freshness:** 100% of API documentation pages reviewed and updated within 90 days of last API change; zero stale pages (>90 days without review)
- **Error Documentation:** 100% of API error responses (4xx, 5xx) documented with error codes, messages, and resolution guidance
- **SDK Documentation Completeness:** 100% of public SDK classes, methods, and properties documented with descriptions, parameters, return types, and examples
- **Developer Portal Search:** ≥90% search success rate (users find relevant content within first 3 results); measured via analytics
- **Feedback Score:** ≥4.0/5 average rating on "Was this page helpful?" feedback widget across all API documentation pages
- **Version Alignment:** 100% of documentation pages display correct API version; zero instances of version mismatch between docs and implementation

---

## Reference Materials

Detailed examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
- [`changelog.md`](references/changelog.md) — Changelog Example
- [`methods.md`](references/methods.md) — HTTP Methods

```

```
