---
version: "1.0.0"
---

# API Testing

| Competency                   | Description                                                                          | Quality Criteria                                                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contract Testing             | OpenAPI/Swagger validation, schema conformance, backward compatibility checks        | Implements automated contract tests that run on every PR; detects breaking changes before merge; validates request/response against OpenAPI schema |
| Integration Testing          | Service-to-service testing, database integration, external dependency mocking        | Tests full request lifecycle through all service layers; uses testcontainers for real database dependencies; mocks external services with wiremock |
| Performance Benchmarking     | p50/p95/p99 latency analysis, throughput measurement, resource utilization profiling | Designs benchmarks that reflect production traffic patterns; identifies latency outliers; profiles CPU/memory under load                           |
| API Documentation Validation | OpenAPI spec accuracy, example correctness, endpoint completeness                    | Validates documentation matches actual API behavior; ensures all endpoints are documented with accurate request/response examples                  |
| Negative Testing             | Error path coverage, boundary condition testing, malformed input handling            | Tests all error responses return correct status codes and error bodies; validates input rejection for edge cases                                   |

## Pipeline Integration

**Stage 5 (Development):** Contract tests written alongside endpoint implementation. Integration tests added for each new service interaction. Performance benchmarks established for new endpoints.

**Stage 6 (Code Review):** Code review validates test coverage includes contract, integration, and negative tests. All endpoints must have corresponding OpenAPI documentation entries.

**Stage 7 (Testing):** Full contract test suite runs against staging environment. Performance benchmarks executed with production-like load. Negative test results reviewed for completeness.

**Stage 8 (Integrity Verification):** Panel validates test coverage meets quality standards. Documentation drift check passes. Performance benchmarks within threshold.

## Quality Standards

| Metric                     | Target                      | Measurement                          |
| -------------------------- | --------------------------- | ------------------------------------ |
| Contract test coverage     | 100% of endpoints           | OpenAPI endpoint count vs test count |
| Integration test pass rate | 100%                        | CI/CD pipeline results               |
| Performance (p95)          | Within defined thresholds   | k6/Gatling benchmark results         |
| Performance (p99)          | Within defined thresholds   | k6/Gatling benchmark results         |
| Error rate under load      | < 1%                        | Load test error metrics              |
| Documentation accuracy     | 100% match (zero drift)     | Automated drift detection            |
| Negative test coverage     | All error paths tested      | Error code coverage analysis         |
| Test execution time        | < 10 minutes for full suite | CI pipeline duration                 |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
