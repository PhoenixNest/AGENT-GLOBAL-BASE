# Interaction Design Specification (IDS)

**Project:** [Project Name]
**Version:** v1
**Author:** CDO (Yuki Tanaka-Chen)
**Date:** YYYY-MM-DD
**Status:** Draft | Under Review | Approved
**Referenced Artifacts:** PRD v1, SRD v1, API Specification vN, Developer Portal Prototype vN

## Version History

| Version | Date       | Author | Changes                  | Communicated to Backend Leads? |
| ------- | ---------- | ------ | ------------------------ | ------------------------------ |
| v1      | YYYY-MM-DD | [Name] | Initial specification    | Yes / No                       |
| v2      | YYYY-MM-DD | [Name] | [Description of changes] | Yes / No                       |

> **Change Propagation Protocol:** During Stage 5 development, any IDS revision must be communicated to all backend leads within **24 hours**. Backend leads acknowledge receipt and submit an impact assessment within 48 hours. IDS changes that alter implemented API behaviors, error formats, or developer portal UX specifications must trigger a partial Design Fidelity Checkpoint re-run on the affected areas. Version tracking follows the repository's document versioning convention (`ids-v1/`, `ids-v2/`, `VERSIONS.md`).

---

## 1. Design Context

Brief description of the API, its design goals, target developer audience, and the API design principles being followed (RESTful conventions, GraphQL schema design, etc.).

---

## 2. API Design Conventions

| Convention Area       | Standard                                                   |
| --------------------- | ---------------------------------------------------------- |
| API style             | [REST / GraphQL / gRPC]                                    |
| Resource naming       | [Plural nouns, kebab-case: `/api/user-profiles`]           |
| HTTP method semantics | [GET=read, POST=create, PUT=replace, PATCH=update, DELETE] |
| Versioning strategy   | [URL-based `/v1/` / Header-based `API-Version: 1`]         |
| Pagination style      | [Cursor-based / Offset-based with `limit`/`offset`]        |
| Field selection       | [?fields=name,email / GraphQL field selection]             |
| Filtering syntax      | [?filter[key]=value / GraphQL filter input objects]        |
| Sorting syntax        | [?sort=-created_at / GraphQL orderBy input]                |
| Response envelope     | [Direct resource / Envelope with `data` wrapper]           |
| Error response format | [RFC 7807 Problem Details / Custom JSON error shape]       |
| Date/time format      | [ISO 8601 UTC: `2024-01-15T10:30:00Z`]                     |

---

## 3. API Endpoint Specification

### 3.1 [Resource Name] -- [HTTP Method] [Path]

```
[HTTP Method] /api/v1/[resource-path]

Request:
  Headers:
    - Authorization: Bearer <token>
    - Content-Type: application/json
  Body (if applicable):
    {
      "field1": "<type>",
      "field2": "<type>"
    }
  Query Parameters (if applicable):
    - page: integer (optional, default 1)
    - limit: integer (optional, default 20, max 100)
    - sort: string (optional)

Response (200 OK):
  {
    "data": [...],
    "meta": {
      "total": <number>,
      "page": <number>,
      "limit": <number>
    },
    "links": {
      "self": "...",
      "next": "...",
      "prev": "..."
    }
  }

Error Responses:
  400 Bad Request -- Validation error
  401 Unauthorized -- Missing or invalid token
  403 Forbidden -- Insufficient permissions
  404 Not Found -- Resource does not exist
  429 Too Many Requests -- Rate limit exceeded
  500 Internal Server Error -- Unexpected server error
```

---

## 4. Error Response Format Specification

All error responses follow a consistent format:

```json
{
  "error": {
    "code": "<machine_readable_error_code>",
    "message": "<human_readable_message>",
    "details": [
      {
        "field": "<field_name>",
        "issue": "<specific_issue>"
      }
    ],
    "trace_id": "<request_trace_id>",
    "documentation_url": "<link_to_docs>"
  }
}
```

### 4.1 Error Code Catalog

| HTTP Status | Error Code            | Message Template                        | When Returned                    |
| ----------- | --------------------- | --------------------------------------- | -------------------------------- |
| 400         | `validation_failed`   | "Request validation failed"             | Invalid request body/params      |
| 400         | `invalid_format`      | "{field} has invalid format"            | Wrong format (email, date, etc.) |
| 401         | `unauthorized`        | "Authentication required"               | Missing token                    |
| 401         | `invalid_token`       | "Invalid or expired token"              | Expired/malformed token          |
| 403         | `forbidden`           | "Insufficient permissions"              | Valid auth, wrong role           |
| 404         | `not_found`           | "{resource} not found"                  | Resource doesn't exist           |
| 429         | `rate_limit_exceeded` | "Rate limit exceeded. Retry after {N}s" | Too many requests                |
| 500         | `internal_error`      | "An unexpected error occurred"          | Server-side failure              |

---

## 5. API Playground UX Specification

### 5.1 Swagger UI / OpenAPI Explorer

| Component            | Behavior                                                |
| -------------------- | ------------------------------------------------------- |
| Endpoint listing     | Grouped by resource/tag, alphabetical within groups     |
| Request body editor  | Syntax-highlighted JSON with schema validation          |
| Try It button        | Executes real request against sandbox environment       |
| Response display     | Formatted JSON with status code and headers             |
| Authentication input | Bearer token field, persists across requests in session |
| Model/Schemas tab    | Expandable JSON Schema definitions for all types        |

### 5.2 Developer Portal UX

| Section         | Content                                                       |
| --------------- | ------------------------------------------------------------- |
| Getting Started | Quickstart guide, API key generation, first API call          |
| Authentication  | OAuth 2.0 flow, API key management, token refresh             |
| API Reference   | Auto-generated from OpenAPI spec, interactive examples        |
| Error Reference | Complete error code catalog with troubleshooting guidance     |
| SDK Downloads   | Language-specific SDKs with installation instructions         |
| Rate Limits     | Per-tier rate limit documentation, upgrade path               |
| Changelog       | API version history, breaking changes, deprecation notices    |
| Status Page     | Real-time API status, incident history, scheduled maintenance |

---

## 6. State Diagrams

### 6.1 [Resource Lifecycle]

```
[Created] ──(update)──▶ [Modified] ──(delete)──▶ [Deleted]
    │                                              │
    │──(view)──▶ [Active] ◀──(restore)────────────│
```

### 6.2 [Authentication Flow]

```
[Unauthenticated] ──(login)──▶ [Authenticated] ──(token expires)──▶ [Token Expired]
                                     │                                    │
                                     │──(logout)──▶ [Logged Out]          │──(refresh)──▶ [Authenticated]
                                     │                                    │
                                     │──(token revoked)──▶ [Revoked] ◀────│
```

---

## 7. Edge Case Matrices

| Scenario                 | API Behavior                                         | HTTP Status | Error Code               |
| ------------------------ | ---------------------------------------------------- | ----------- | ------------------------ |
| Missing auth token       | Reject with 401, no resource access                  | 401         | `unauthorized`           |
| Invalid auth token       | Reject with 401, specific error message              | 401         | `invalid_token`          |
| Insufficient permissions | Reject with 403, explain required role               | 403         | `forbidden`              |
| Resource not found       | Return 404, do not leak existence of other resources | 404         | `not_found`              |
| Rate limit exceeded      | Return 429 with Retry-After header                   | 429         | `rate_limit_exceeded`    |
| Invalid request body     | Return 400 with field-level validation errors        | 400         | `validation_failed`      |
| Database unavailable     | Return 503 with retry guidance                       | 503         | `service_unavailable`    |
| Timeout                  | Return 504, request logged for investigation         | 504         | `gateway_timeout`        |
| Malformed JSON           | Return 400, "Invalid JSON in request body"           | 400         | `invalid_format`         |
| Content-Type mismatch    | Return 415, "Unsupported Media Type"                 | 415         | `unsupported_media_type` |

---

## 8. Pagination Specification

### 8.1 Cursor-Based Pagination (Recommended)

```
Request: GET /api/v1/items?limit=20&cursor=<opaque_cursor>

Response:
{
  "data": [...],
  "meta": {
    "limit": 20,
    "has_more": true
  },
  "links": {
    "next": "/api/v1/items?limit=20&cursor=eyJpZCI6MTAwfQ"
  }
}
```

### 8.2 Offset-Based Pagination (Legacy)

```
Request: GET /api/v1/items?offset=0&limit=20

Response:
{
  "data": [...],
  "meta": {
    "total": 1500,
    "offset": 0,
    "limit": 20
  },
  "links": {
    "self": "/api/v1/items?offset=0&limit=20",
    "next": "/api/v1/items?offset=20&limit=20",
    "prev": null
  }
}
```

---

## 9. Field Selection Convention

Consumers can request specific fields to reduce response payload:

```
Request: GET /api/v1/users?fields=id,name,email

Response:
{
  "data": [
    { "id": "uuid-1", "name": "Alice", "email": "alice@example.com" }
  ]
}
```

**Rules:**

- Invalid field names return 400 with field-level error
- Primary key (`id`) always included regardless of field selection
- Nested field selection: `?fields=id,name,address.city,address.country`

---

## 10. Response Headers

| Header                  | When Present           | Value                                   |
| ----------------------- | ---------------------- | --------------------------------------- |
| `X-Request-Id`          | Always                 | Unique request trace ID                 |
| `X-RateLimit-Limit`     | Always                 | Maximum requests per window             |
| `X-RateLimit-Remaining` | Always                 | Remaining requests in current window    |
| `X-RateLimit-Reset`     | Always                 | Unix timestamp when window resets       |
| `Retry-After`           | On 429                 | Seconds until rate limit resets         |
| `Location`              | On 201 Created         | URL of newly created resource           |
| `Link`                  | On paginated responses | RFC 8288 link header (next, prev, etc.) |
| `X-Total-Count`         | On paginated responses | Total number of resources               |

---

## 11. Internationalization Design Considerations

### 11.1 API Error Message Localization

API error messages are localized based on the `Accept-Language` header or the user's locale preference stored in their profile.

| Language Family  | Expansion Rate | Impact on Error Messages                        |
| ---------------- | -------------- | ----------------------------------------------- |
| Germanic (DE)    | +25% to +35%   | Error messages may be longer; verify truncation |
| Romance (FR, ES) | +20% to +30%   | Error messages may be longer                    |
| CJK (ZH, JA, KO) | -30% to -40%   | Messages compress; verify clarity               |

#### Error Message Design Rules

- Error messages must be actionable and specific in all target languages
- Machine-readable `error.code` never changes (locale-independent)
- Human-readable `error.message` is localized per Accept-Language
- `documentation_url` always points to the locale-appropriate docs page

### 11.2 Developer Portal Internationalization

| Rule              | Detail                                                                        |
| ----------------- | ----------------------------------------------------------------------------- |
| Navigation        | Portal navigation labels localized per user locale                            |
| Code examples     | Code blocks remain in English; comments may be localized                      |
| Error reference   | Complete error catalog localized for all target languages                     |
| Search            | Portal search supports all target languages with locale-specific tokenization |
| Date/time display | Formatted per locale convention (ISO 8601 for API, locale format for portal)  |

---

_Approved by CDO (Yuki Tanaka-Chen) on YYYY-MM-DD_
_Archived alongside: API Specification vN, Developer Portal Prototype vN_
