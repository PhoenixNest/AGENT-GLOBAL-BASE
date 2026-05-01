---
version: "1.0.0"
---

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

- [Resource model](company/departments/research-develop/team/teammates/technical-writer/amina-razak/skills/models/resource.md)
- [Pagination guide](company/departments/research-develop/team/teammates/technical-writer/amina-razak/guides/pagination.md)

### Developer Portal Content Management

#### Portal Information Architecture

```text
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

| Standard                   | Requirement                                                                               |
| -------------------------- | ----------------------------------------------------------------------------------------- |
| **Content freshness**      | All pages reviewed and updated within 90 days; stale content flagged by automated audit   |
| **Version alignment**      | Documentation version matches API version; version selector on every page                 |
| **Search optimization**    | Every page has unique `<title>`, `<meta description>`, and H1; search index rebuilt daily |
| **Broken link monitoring** | Automated link check runs weekly; broken links remediated within 48 hours                 |
| **Feedback collection**    | "Was this page helpful?" widget on every page; feedback reviewed monthly                  |
| **Accessibility**          | All pages meet WCAG 2.1 AA; code examples have language labels; images have alt text      |
