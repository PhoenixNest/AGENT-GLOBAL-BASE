---
name: backend-api-patterns-api-technical-writing
description: 'Backend skill: Api Technical Writing'
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

## Execution Guidance

### OpenAPI/Swagger Specification Authoring

#### Specification Structure

```yaml
openapi: 3.0.3
info:
  title: [Service Name] API
  description: |
    [2-3 paragraph description of the service, its purpose, and its primary use cases.
    Include links to getting started guides, authentication docs, and support channels.]
  version: 1.0.0
  contact:
    name: API Team
    email: api-team@company.com
    url: https://developer.company.com/support
  license:
    name: Proprietary
    url: https://company.com/legal/api-license

servers:
  - url: https://api.company.com/v1
    description: Production
  - url: https://api-staging.company.com/v1
    description: Staging

security:
  - BearerAuth: []

paths:
  /resources:
    get:
      summary: List all resources
      description: |
        Returns a paginated list of all resources accessible to the authenticated user.
        Supports filtering, sorting, and field selection via query parameters.
      operationId: listResources
      tags:
        - Resources
      parameters:
        - name: page
          in: query
          description: Page number (1-based)
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: Number of items per page
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: sort
          in: query
          description: Sort field and direction (e.g., `created_at:desc`)
          required: false
          schema:
            type: string
            pattern: '^[a-z_]+:(asc|desc)$'
        - name: fields
          in: query
          description: Comma-separated list of fields to include in response
          required: false
          schema:
            type: string
      responses:
        '200':
          description: Successful response with paginated resource list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedResourceList'
              examples:
                default:
                  $ref: '#/components/examples/ListResourcesResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '429':
          $ref: '#/components/responses/RateLimited'
      security:
        - BearerAuth: [resources:read]

    post:
      summary: Create a new resource
      description: |
        Creates a new resource with the provided attributes. Returns the created
        resource with server-generated fields (id, created_at, updated_at).
      operationId: createResource
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ResourceCreateRequest'
            examples:
              default:
                $ref: '#/components/examples/CreateResourceRequest'
      responses:
        '201':
          description: Resource created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
              examples:
                default:
                  $ref: '#/components/examples/CreateResourceResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          $ref: '#/components/responses/Conflict'
      security:
        - BearerAuth: [resources:write]

  /resources/{resourceId}:
    get:
      summary: Get a specific resource
      description: Returns a single resource by ID. Returns 404 if not found.
      operationId: getResource
      tags:
        - Resources
      parameters:
        - name: resourceId
          in: path
          required: true
          description: Unique resource identifier (UUID format)
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Successful response with resource details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
              examples:
                default:
                  $ref: '#/components/examples/GetResourceResponse'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - BearerAuth: [resources:read]

    delete:
      summary: Delete a resource
      description: |
        Soft-deletes the specified resource. The resource will be marked as deleted
        and excluded from list queries. Hard deletion occurs after 30 days per
        data retention policy.
      operationId: deleteResource
      tags:
        - Resources
      parameters:
        - name: resourceId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Resource deleted successfully (no content)
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - BearerAuth: [resources:delete]

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT access token obtained from the authentication endpoint.
        Include in the `Authorization` header as `Bearer <token>`.
        Tokens expire after 1 hour. Use refresh tokens to obtain new access tokens.

  schemas:
    Resource:
      type: object
      description: Represents a [resource type] in the system.
      properties:
        id:
          type: string
          format: uuid
          description: Unique resource identifier
          readOnly: true
        name:
          type: string
          description: Human-readable resource name
          minLength: 1
          maxLength: 255
        description:
          type: string
          description: Optional resource description
          maxLength: 1000
        status:
          type: string
          enum: [active, inactive, archived]
          description: Current resource status
          default: active
        created_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp of resource creation
          readOnly: true
        updated_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp of last resource update
          readOnly: true
      required:
        - id
        - name
        - status
        - created_at
        - updated_at

    ResourceCreateRequest:
      type: object
      description: Request body for creating a new resource.
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 255
        description:
          type: string
          maxLength: 1000
        status:
          type: string
          enum: [active, inactive]
          default: active
      required:
        - name

    PaginatedResourceList:
      type: object
      description: Paginated list of resources with metadata.
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Resource'
        meta:
          type: object
          properties:
            current_page:
              type: integer
            total_pages:
              type: integer
            total_count:
              type: integer
            per_page:
              type: integer
          required:
            - current_page
            - total_pages
            - total_count
            - per_page
        links:
          type: object
          properties:
            self:
              type: string
              format: uri
            first:
              type: string
              format: uri
            last:
              type: string
              format: uri
            next:
              type: string
              format: uri
            prev:
              type: string
              format: uri

  examples:
    ListResourcesResponse:
      value:
        data:
          - id: "550e8400-e29b-41d4-a716-446655440000"
            name: "Example Resource"
            description: "This is an example resource."
            status: "active"
            created_at: "2026-01-15T10:30:00Z"
            updated_at: "2026-01-15T10:30:00Z"
        meta:
          current_page: 1
          total_pages: 3
          total_count: 42
          per_page: 20
        links:
          self: "https://api.company.com/v1/resources?page=1&limit=20"
          first: "https://api.company.com/v1/resources?page=1&limit=20"
          last: "https://api.company.com/v1/resources?page=3&limit=20"
          next: "https://api.company.com/v1/resources?page=2&limit=20"

    CreateResourceRequest:
      value:
        name: "New Resource"
        description: "A newly created resource."

    CreateResourceResponse:
      value:
        id: "550e8400-e29b-41d4-a716-446655440001"
        name: "New Resource"
        description: "A newly created resource."
        status: "active"
        created_at: "2026-04-04T14:00:00Z"
        updated_at: "2026-04-04T14:00:00Z"

    GetResourceResponse:
      value:
        id: "550e8400-e29b-41d4-a716-446655440000"
        name: "Example Resource"
        description: "This is an example resource."
        status: "active"
        created_at: "2026-01-15T10:30:00Z"
        updated_at: "2026-01-15T10:30:00Z"

  responses:
    Unauthorized:
      description: Authentication required. Valid JWT access token not provided.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "UNAUTHORIZED"
              message: "Authentication required. Include a valid JWT access token in the Authorization header."
              status: 401

    Forbidden:
      description: Insufficient permissions for this operation.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "FORBIDDEN"
              message: "You do not have the required permissions to perform this operation."
              status: 403

    NotFound:
      description: The specified resource was not found.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "NOT_FOUND"
              message: "The specified resource does not exist or has been deleted."
              status: 404

    BadRequest:
      description: The request body is invalid. See error details for specifics.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "BAD_REQUEST"
              message: "The request body is invalid."
              status: 400
              details:
                - field: "name"
                  issue: "Name is required and cannot be empty."

    Conflict:
      description: The request conflicts with an existing resource.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "CONFLICT"
              message: "A resource with this name already exists."
              status: 409

    RateLimited:
      description: Too many requests. Retry after the specified duration.
      headers:
        Retry-After:
          schema:
            type: integer
          description: Seconds to wait before retrying.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "RATE_LIMITED"
              message: "Too many requests. Please retry after the specified duration."
              status: 429

  schemas:
    Error:
      type: object
      description: Standard error response structure.
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              description: Machine-readable error code.
            message:
              type: string
              description: Human-readable error description.
            status:
              type: integer
              description: HTTP status code.
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                    description: The field that caused the error.
                  issue:
                    type: string
                    description: Description of the validation issue.
          required:
            - code
            - message
            - status
```

#### OpenAPI Authoring Standards

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

````markdown
# GET /api/v1/resources

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
```

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

## Changelog

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| v1.0    | 2026-01-15 | Initial release                                     |
| v1.1    | 2026-03-01 | Added `fields` query parameter for sparse fieldsets |

````

### Code Example Generation

#### Multi-Language Example Standards

| Language | Audience | Framework/Library | Style Guide |
|----------|----------|------------------|-------------|
| Kotlin | Android engineers | Retrofit + Coroutines + kotlinx.serialization | Kotlin Official Coding Conventions |
| Swift | iOS engineers | URLSession + Codable (or async/await in Swift 5.5+) | Swift API Design Guidelines |
| Dart | Flutter engineers | http package + json_annotation / freezed | Effective Dart |

#### Example Quality Requirements

- **Compilable:** Every code example compiles against the current SDK version. Examples are validated by CI on every API spec change.
- **Complete:** Examples include error handling, not just the happy path. Show how to handle 401, 404, 500 responses.
- **Annotated:** Non-obvious patterns are explained with inline comments. Reference related documentation where applicable.
- **Current:** Examples are updated within 5 business days of any API change. Deprecation notices are added to examples using deprecated patterns.
- **Tested:** Examples are executed against a staging environment as part of CI pipeline. Test results reported in the example's metadata.

#### Example Template per Language

Each endpoint's code example section follows this pattern:

```markdown
### [Language] ([Platform])

#### Prerequisites
- [Required SDK/library version]
- [Authentication setup steps if not covered elsewhere]

#### Basic Usage
[Minimal example showing the simplest successful call]

#### With Error Handling
[Example showing proper error handling for common failure modes]

#### With Advanced Options
[Example showing pagination, filtering, or other advanced features]
````

### SDK Documentation

#### SDK Reference Structure

```
sdk-docs/
├── getting-started.md
├── authentication.md
├── configuration.md
├── reference/
│   ├── client.md              # Client class initialization and configuration
│   ├── models/
│   │   ├── resource.md        # Resource model class
│   │   ├── error.md           # Error model class
│   │   └── pagination.md      # Pagination model class
│   ├── services/
│   │   ├── resource-service.md # Resource API service methods
│   │   └── auth-service.md     # Authentication service methods
│   └── utilities/
│       ├── retry-policy.md     # Retry policy configuration
│       └── logging.md          # Logging configuration
├── guides/
│   ├── migration-v1-to-v2.md
│   ├── error-handling.md
│   ├── pagination.md
│   └── testing.md
└── changelog.md
```

#### SDK Reference Page Template

````markdown
# ResourceService

**Package:** `com.company.api.services` (Kotlin) / `CompanyAPI` (Swift) / `company_api` (Dart)
**Since:** SDK v1.0.0

## Overview

[1-2 sentences describing what this service does and when to use it]

## Initialization

```kotlin
val resourceService = apiClient.resources
```
````

## Methods

### `listResources(params: ResourceListParams): Response<PaginatedResourceList>`

Lists all resources accessible to the authenticated user.

**Parameters:**

| Parameter       | Type      | Required | Default | Description     |
| --------------- | --------- | -------- | ------- | --------------- |
| `params.page`   | `Int`     | No       | `1`     | Page number     |
| `params.limit`  | `Int`     | No       | `20`    | Items per page  |
| `params.sort`   | `String?` | No       | `null`  | Sort expression |
| `params.fields` | `String?` | No       | `null`  | Sparse fieldset |

**Returns:** `Response<PaginatedResourceList>` — Paginated list of resources

**Throws:**

- `UnauthorizedException` — Invalid or missing authentication
- `ForbiddenException` — Insufficient permissions
- `ApiException` — Server error (5xx)

**Example:**
[Code example]

**See Also:**

- [Resource model](../models/resource.md)
- [Pagination guide](../../guides/pagination.md)

```

### Developer Portal Content Management

#### Portal Information Architecture

```

Developer Portal
├── Home
│ ├── Welcome & Overview
│ ├── Quick Start (5-minute tutorial)
│ └── API Status Dashboard
├── Getting Started
│ ├── Create Account & Get API Key
│ ├── Authentication Overview
│ ├── Making Your First Request
│ └── SDK Installation & Setup
├── API Reference
│ ├── [Service 1]
│ │ ├── Overview
│ │ ├── Endpoints (one per endpoint)
│ │ ├── Models
│ │ └── Error Codes
│ ├── [Service 2]
│ │ └── ...
│ └── Postman Collection / OpenAPI Spec Download
├── Guides
│ ├── Authentication Deep Dive
│ ├── Pagination & Filtering
│ ├── Error Handling Best Practices
│ ├── Rate Limiting & Throttling
│ ├── Webhooks
│ └── Migration Guides
├── SDKs & Tools
│ ├── Kotlin SDK
│ ├── Swift SDK
│ ├── Dart SDK
│ ├── CLI Tools
│ └── Postman Collection
├── Support
│ ├── FAQ
│ ├── Contact Support
│ ├── Status Page
│ └── Community Forum
└── Changelog
├── Latest Release Notes
├── Deprecated Features
└── API Version History

```

#### Content Management Standards

| Standard | Requirement |
|----------|-------------|
| **Content freshness** | All pages reviewed and updated within 90 days; stale content flagged by automated audit |
| **Version alignment** | Documentation version matches API version; version selector on every page |
| **Search optimization** | Every page has unique `<title>`, `<meta description>`, and H1; search index rebuilt daily |
| **Broken link monitoring** | Automated link check runs weekly; broken links remediated within 48 hours |
| **Feedback collection** | "Was this page helpful?" widget on every page; feedback reviewed monthly |
| **Accessibility** | All pages meet WCAG 2.1 AA; code examples have language labels; images have alt text |

## Pipeline Integration

| Pipeline Stage | API Documentation Relevance |
|----------------|---------------------------|
| Stage 1-4 | Not applicable — API documentation not in scope during requirements, design, architecture, or planning stages |
| Stage 5 (Development) | **Primary creation stage** — API documentation authored alongside API implementation; OpenAPI spec generated or maintained as code is written |
| Stage 6 (Code Review) | API documentation reviewed as part of code review; documentation accuracy validated against implementation |
| Stage 7 (Testing) | API examples tested against staging environment; test coverage includes documentation example validation |
| Stage 8 (Integrity Verification) | Panel verifies API implementation matches documented specification; discrepancies flagged as defects |
| Stage 9 (i18n) | API documentation updated if i18n affects API (e.g., locale-specific endpoints, translation API) |
| Stage 10 (Release) | API documentation reviewed as part of release readiness; developer portal content validated for accuracy |

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
```
