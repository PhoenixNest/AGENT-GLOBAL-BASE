---
version: "1.0.0"
---

### OpenAPI Specification Standards

| Standard                        | Requirement                                                                                             |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **OpenAPI Version**             | 3.0.3 minimum; 3.1.0 preferred when supported by tooling                                                |
| **Every endpoint documented**   | All paths, methods, parameters, request bodies, and responses must be specified                         |
| **Examples required**           | Every response schema must have at least one example; complex request bodies must have examples         |
| **Error responses complete**    | Document all possible error responses (400, 401, 403, 404, 409, 429, 500) with error codes and messages |
| **Authentication documented**   | Security schemes defined at the component level; per-operation security overrides documented            |
| **Descriptions on every field** | Every schema property has a `description` field. No undocumented fields.                                |
| **Validation constraints**      | Use `minimum`, `maximum`, `minLength`, `maxLength`, `pattern`, `enum` to document validation rules      |
| **Consistent naming**           | Operation IDs use camelCase; tags use PascalCase; parameters use snake_case                             |
| **Version in URL**              | API version included in server URL path (e.g., `/v1/`, `/v2/`)                                          |
| **Lint validation**             | All specs pass `spectral` lint rules before merge; zero warnings or errors                              |

### Endpoint Reference Documentation

#### Endpoint Doc Structure

Every endpoint documentation page follows this structure:

````markdown
# GET /api/v1/resources

**Description:** [1-2 sentences describing what this endpoint does and when to use it]

## Authentication

Required scopes: `resources:read`
Auth method: Bearer token (JWT)

## Request

### Path Parameters

| Parameter    | Type            | Required | Description                        |
| ------------ | --------------- | -------- | ---------------------------------- |
| `resourceId` | `string (UUID)` | Yes      | Unique identifier for the resource |

### Query Parameters

| Parameter | Type      | Required | Default | Description              |
| --------- | --------- | -------- | ------- | ------------------------ |
| `page`    | `integer` | No       | `1`     | Page number (1-based)    |
| `limit`   | `integer` | No       | `20`    | Items per page (max 100) |

### Request Headers

| Header          | Type     | Required | Description                   |
| --------------- | -------- | -------- | ----------------------------- |
| `Authorization` | `string` | Yes      | `Bearer <JWT access token>`   |
| `X-Request-ID`  | `string` | No       | Unique request ID for tracing |

## Response

### 200 OK

**Content-Type:** `application/json`

```json
{
  "data": [...],
  "meta": { "current_page": 1, "total_pages": 3, "total_count": 42 },
  "links": { "self": "...", "next": "..." }
}
```
````

### 401 Unauthorized

```json
{
  "error": { "code": "UNAUTHORIZED", "message": "...", "status": 401 }
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
val response = apiService.getResources(page = 1, limit = 20)
```

### Swift (iOS)

```swift
let task = URLSession.shared.dataTask(with: url) { data, response, error in ... }
```

### Dart (Flutter)

```dart
final response = await http.get(Uri.parse(url), headers: {'Authorization': 'Bearer $token'});
```

```

#### Endpoint Documentation Rules

- **One page per endpoint** — each HTTP method + path combination gets its own documentation page
- **All error responses documented** — every possible 4xx and 5xx response with error code, message, and resolution guidance
- **Code examples in all supported languages** — Kotlin (Android), Swift (iOS), Dart (Flutter) minimum
- **Rate limits documented** — per-tier rate limits shown on every endpoint page
- **Related endpoints linked** — each endpoint page links to related endpoints (e.g., GET links to POST, PUT, DELETE for the same resource)
```
