---
name: api-technical-writing
description: >
  API documentation authoring for backend services — OpenAPI/Swagger specification writing, endpoint reference documentation, multi-language code examples, SDK documentation, and developer portal content. Owned by Amina Razak (Technical Writer). Use during Stage 4 (Implementation Plan) for documentation planning and Stage 5 (Development) for API docs generation. Trigger: api documentation, openapi spec, swagger docs, developer portal, api reference, sdk documentation, code examples.
version: "1.0.0"
---

API technical writing skill for Amina Razak — Technical Writer (R&D department).
Produces API documentation, SDK guides, developer portal content, and engineering standards documentation.

## Owner

Amina Razak — Technical Writer, Research & Development department.
Reports to: CTO office.
Pipeline stages: 5, 6, 10.

## When to Invoke

- Authoring OpenAPI/Swagger specifications for new or updated API endpoints
- Writing endpoint reference documentation with request/response examples and error codes
- Generating multi-language code examples (Kotlin, Swift, Dart) for API documentation
- Creating SDK reference documentation with class hierarchies, method signatures, and usage patterns
- Managing developer portal content architecture, navigation, and search optimization
- Documenting API versioning strategy, deprecation notices, and migration paths
- Reviewing API documentation accuracy against implementation during code review (Stage 6)
- Validating developer portal content for release readiness (Stage 10)

## Competencies

| Competency                       | Description                                                                                                        | Quality Criteria                                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| OpenAPI/Swagger Authoring        | Write valid, comprehensive OpenAPI 3.x specifications covering all endpoints, schemas, and operations              | Publication-ready OpenAPI spec from API design docs in ≤8 hours; zero validation errors from OpenAPI linter   |
| Endpoint Reference Documentation | Write clear, structured endpoint docs with request/response examples, error codes, and authentication requirements | Engineers rate endpoint docs ≥4.3/5 for clarity; zero integration defects traced to documentation gaps        |
| Code Example Generation          | Produce accurate, production-quality code examples in Kotlin, Swift, and Dart (Flutter)                            | Examples compile and run against test environment; ≥95% example accuracy rate on automated validation         |
| SDK Documentation                | Structure SDK reference docs with class hierarchies, method signatures, usage patterns, and migration guides       | SDK docs pass developer review on first submission; adoption rate of documented patterns ≥85%                 |
| Developer Portal Content         | Manage developer portal content architecture, navigation, search optimization, and content freshness               | Portal search success rate ≥90%; content freshness score ≥95% (all pages reviewed within 90 days)             |
| API Versioning Documentation     | Document API versioning strategy, deprecation notices, migration paths, and backward compatibility guarantees      | Zero consumer breakages due to undocumented API changes; deprecation notices published ≥90 days before sunset |

## Execution Guidance

Detailed API endpoint documentation templates, code example patterns, and SDK documentation structures are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution guidance for API documentation workflows
- [`methods.md`](references/methods.md) — API documentation methods and patterns
- [`changelog.md`](references/changelog.md) — Changelog management workflow and standards

## Pipeline Integration

| Pipeline Stage                   | API Documentation Relevance                                                                                                                   |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 1–4                        | Not applicable — API documentation not in scope during requirements, design, architecture, or planning                                        |
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
