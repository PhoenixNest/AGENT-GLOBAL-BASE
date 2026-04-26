---
version: "1.0.0"
---

| Competency                           | Description                                                                                                                                                                                                                     | Quality Criteria                                                                                                                                                                                                                                                                                                   |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **REST API Testing Methodology**     | HTTP method validation (GET, POST, PUT, PATCH, DELETE), status code verification, response schema validation, pagination/cursor testing, filter/sort/query parameter validation, content negotiation                            | Tests verify both status codes AND response body schemas; pagination tested with boundary conditions (empty result, single item, max page size); query parameters validated for SQL injection resistance; content-type negotiation tested (`Accept: application/json` vs `application/xml`)                        |
| **GraphQL Testing**                  | Query/mutation execution, introspection testing, alias usage for parallel field fetching, fragment reuse, variable injection, error path testing, batching validation, subscription testing (WebSocket)                         | Tests use variables for parameterization; introspection query validates schema completeness; error testing covers null field handling, partial failures, and field-level authorization; subscription tests verify real-time event delivery over WebSocket; batched queries validated for correct response ordering |
| **OAuth 2.0 Authentication Testing** | Authorization Code flow, Client Credentials flow, PKCE extension, token refresh lifecycle, scope validation, token revocation, unauthorized access testing, token expiry handling                                               | Tests exercise full OAuth flows with test identity providers; PKCE verifier/challenge pair validated; scope restrictions enforced (token with `read` scope cannot access `write` endpoints); token refresh returns new access token with correct expiry; revoked tokens return 401 immediately                     |
| **JWT Validation Testing**           | Token structure verification (header, payload, signature), algorithm enforcement (RS256 vs HS256), expiry (`exp`) validation, issuer (`iss`) and audience (`aud`) claims, custom claim testing, token tampering detection       | Tests decode JWT and validate each claim; algorithm confusion attacks tested (HS256 substituted for RS256); expired tokens rejected with 401; tokens with wrong `aud` rejected; custom claims (roles, permissions) correctly enforced; tampered signatures detected and rejected                                   |
| **Rate Limiting Validation**         | Rate limit header inspection (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`), burst handling, sliding window vs fixed window verification, per-endpoint rate limits, 429 response validation | Tests send requests at rate limit boundary; verify `X-RateLimit-Remaining` decrements correctly; confirm 429 returned when limit exceeded; validate `Retry-After` header accuracy; test burst tolerance (short-term exceedance allowed); per-endpoint limits verified independently                                |
| **Error Handling Testing**           | 4xx client error completeness (400, 401, 403, 404, 409, 422, 429), 5xx server error handling, error response schema consistency, error code/documentation mapping, graceful degradation                                         | Every endpoint tested for all applicable 4xx conditions; 5xx errors return structured error body (not raw stack traces); error responses follow consistent schema `{code, message, details, requestId}`; error codes documented and mapped in API spec; invalid JSON body returns 400 with descriptive message     |
| **Performance Benchmarking**         | Response time measurement (p50, p95, p99), throughput (requests/second), concurrent user simulation, resource utilization monitoring, baseline establishment, performance regression detection                                  | Benchmarks established for every endpoint under normal load; p95 response time tracked and gated in CI; concurrent user tests simulate realistic request patterns; resource utilization (CPU, memory, DB connections) monitored during load; >20% regression from baseline triggers P1 defect                      |

## Pipeline Integration

| Stage                                | Application                                                                                                                                                                                |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Stage 5** (Development)            | Author API test scaffolding alongside backend service development; validate contract compliance; test authentication flows with mock IdP                                                   |
| **Stage 6** (Code Review)            | Review API test coverage for all endpoints, error paths, and authorization scenarios; verify schema validation completeness                                                                |
| **Stage 7** (Automated Testing)      | **Primary ownership** — execute full API test suite (REST + GraphQL); validate rate limiting and error handling; run performance benchmarks; classify defects; produce Test Results Report |
| **Stage 8** (Integrity Verification) | Re-run API regression suite; verify all fixed defects resolved; confirm no API contracts broken; performance baseline comparison                                                           |

## Quality Standards

| Metric                      | Target                                              | Measurement                                                              |
| --------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------ |
| Endpoint coverage           | 100% of documented API endpoints tested             | Traced to OpenAPI/Swagger spec; untested endpoint = P1 defect            |
| Error path coverage         | 100% of applicable 4xx/5xx scenarios tested         | Each endpoint tested for at least: 400, 401, 403, 404, 422, 500          |
| Response schema validation  | 100% of responses validated against declared schema | JSON Schema or Pydantic validation in every test assertion               |
| OAuth/JWT test coverage     | 100% of auth flows and edge cases tested            | Covers: token issue, refresh, revoke, expiry, scope, algorithm confusion |
| Rate limit validation       | All rate-limited endpoints tested at boundary       | 429 response verified with correct Retry-After header                    |
| Performance gate compliance | p95 < SLA for all endpoints                         | CI fails if p95 exceeds endpoint-specific threshold                      |
| API test execution time     | < 15 minutes for full suite                         | Measured from test start to result aggregation                           |
| Contract drift detection    | Zero undetected contract changes between services   | Pact contract tests run on every API change                              |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
