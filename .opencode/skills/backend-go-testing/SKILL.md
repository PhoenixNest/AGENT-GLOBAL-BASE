---
name: backend-go-testing
description: Go testing strategies — table-driven tests, interface mocking with gomock/testify, integration testing with testcontainers, HTTP handler testing with httptest, and coverage analysis. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 7 (Automated Testing) for Go test infrastructure and Stage 5 (Development) for test-driven implementation. Trigger: go testing, table-driven tests, gomock, testify, testcontainers, httptest, go coverage.
prerequisites:
  - backend-go-rest-api

version: "1.0.0"
---

# Go Testing

**Category:** Backend Quality Engineering (Go)
**Owner:** Backend Engineer (Omar Hassan)

## Overview

Implements comprehensive testing strategies for Go applications using table-driven tests, interface mocking with gomock and testify, integration testing with testcontainers, HTTP handler testing with httptest, and test coverage analysis. Ensures tests are deterministic, fast, and provide meaningful failure output.

## Competency Dimensions

| Dimension            | Description                                                   | Proficiency Indicators                                                                                                                    |
| -------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Table-Driven Tests   | Subtests with t.Run(), test case structs, descriptive naming  | Writes tests with descriptive subtest names; uses meaningful test case names for failure output; handles error expectations per test case |
| Interface Mocking    | gomock code generation, testify mock assertions, matchers     | Generates mocks with mockgen; writes explicit expectation sequences; uses matchers for flexible argument validation                       |
| Integration Testing  | testcontainers-go, real database setup, migration application | Spins up real PostgreSQL/Redis containers for tests; applies migrations before test execution; cleans up after tests                      |
| HTTP Handler Testing | httptest.ResponseRecorder, httptest.Server, request builders  | Tests handlers without starting real server; validates response status, headers, and body; tests middleware chains                        |
| Test Coverage        | go test -cover, coverage profiles, threshold enforcement      | Achieves > 80% coverage on business logic; identifies untested paths via coverage profiles; enforces coverage thresholds in CI            |

## Pipeline Integration

**Stage 5 (Development):** Tests written alongside implementation. Table-driven tests for all business logic. HTTP handler tests for all endpoints. Integration tests for repository layer.

**Stage 6 (Code Review):** Review validates test coverage meets threshold. Mock usage is correct (no over-mocking). Integration tests cover critical database interactions. Test names are descriptive.

**Stage 7 (Testing):** Full test suite runs in CI with coverage reporting. Race detector enabled (`-race`). Benchmarks establish performance baselines.

## Quality Standards

| Metric                              | Target                                         | Measurement                       |
| ----------------------------------- | ---------------------------------------------- | --------------------------------- |
| Unit test coverage (total)          | > 80%                                          | go test -cover                    |
| Unit test coverage (business logic) | > 90%                                          | Per-package coverage analysis     |
| Test execution time                 | < 5 minutes (unit), < 15 minutes (integration) | CI pipeline duration              |
| Flaky test rate                     | 0%                                             | Test retry analysis               |
| Race detector findings              | 0                                              | go test -race                     |
| Mock expectation violations         | 0                                              | gomock/testify assertion failures |
| Benchmark regression                | < 10% degradation                              | Benchmark comparison              |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
