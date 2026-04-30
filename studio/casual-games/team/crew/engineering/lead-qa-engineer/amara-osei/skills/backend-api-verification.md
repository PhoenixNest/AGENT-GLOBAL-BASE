---
name: studio-qa-backend-api-verification
description: Backend API contract verification for casual games — auth flow testing, economy transaction validation, data persistence verification, and API regression testing using contract-based testing patterns. Owned by Amara Osei (Lead QA Engineer). Trigger: API testing, backend verification, economy testing, auth flow, data persistence, contract testing, API regression.
version: "1.0.0"
---

# Backend API Verification

**Skill Owner:** Amara Osei (Lead QA Engineer)
**Applies To:** API Contract Testing, Economy Verification, Auth Flow, Data Persistence

## Tools & Frameworks

| Tool/Framework | Version Context | Usage                                                  |
| -------------- | --------------- | ------------------------------------------------------ |
| Postman        | Latest          | Manual API exploration and collection-based regression |
| Newman         | Latest          | Postman collection runner in CI/CD pipeline            |
| Charles Proxy  | 4.x             | Intercepting and modifying API traffic from the device |
| pytest         | Latest          | Python-based API test suite                            |
| Pact           | Latest          | Consumer-driven contract testing                       |
| PlayFab SDK    | Latest          | Backend service integration for economy and auth       |

## Critical API Test Categories

### 1. Authentication Flows

Every new auth system must have test coverage for:

- **Happy path:** Valid login returns expected JWT/session token; token contains correct claims
- **Expired token:** Client receives `401`; refresh token flow is triggered; session restored without user interruption
- **Invalid credentials:** Returns `401` with informative error; no stack trace exposed
- **Device ban/account suspension:** Returns appropriate error code; client surfaces correct UI state
- **Concurrent session limit:** Second device login either revokes the first session or notifies the user per design spec

### 2. Economy Transactions

Economy bugs are P0 — they directly affect monetization and player trust.

| Test Case                       | Expected Behavior                                                    |
| ------------------------------- | -------------------------------------------------------------------- |
| Purchase soft currency          | Balance increases by exact amount; transaction logged                |
| Spend soft currency (exact)     | Balance decreases; item granted; balance never goes negative         |
| Spend with insufficient balance | Returns clear error; no state change; balance unchanged              |
| Duplicate transaction (retry)   | Idempotency key prevents double-grant; same result as original       |
| Purchase hard currency (IAP)    | Receipt verified server-side; currency granted only on valid receipt |
| Concurrent purchase race        | Server enforces one grant; no double-grant under race condition      |

### 3. Data Persistence and Sync

| Test Case                               | Expected Behavior                                             |
| --------------------------------------- | ------------------------------------------------------------- |
| Save game state; retrieve on new device | All progress, currency, and inventory restored exactly        |
| Save during offline; reconnect          | Offline changes synced without data loss or duplication       |
| Conflict resolution (two devices)       | Later write wins (or design-specified merge strategy applied) |
| Server data corrupted / unavailable     | Client falls back gracefully; no local data loss              |

## Real-World Production Scenarios

### Scenario 1: API Contract Testing with the Backend Team

**Context:** New feature's API is being developed concurrently with the client. QA needs to verify the contract before implementation is complete.
**Process:**

1. Work with the Backend Lead to define the API contract in OpenAPI 3.0 format before implementation begins
2. Use Pact to write consumer-driven contract tests from the client perspective
3. Backend team runs Pact verification as part of their CI pipeline — any contract violation breaks their build
4. When the backend is ready, run the full Postman collection against the staging environment; verify 100% of contract assertions pass
5. Any deviations are P0 defects — the API does not match the agreed contract

### Scenario 2: Economy Regression Before Every Release

**Context:** New content release going live; economy changes must not introduce regressions.
**Process:**

1. Run the full economy test collection via Newman in CI/CD on the staging environment
2. Verify all transaction types: purchase, spend, grant, refund, expiration
3. Execute edge cases: zero balance spend, max balance, concurrent spend (2 parallel requests)
4. Compare response schemas against the stored baseline; any schema deviation is a P1 defect
5. Sign off only when all economy tests pass with 0 failures

## Measurable Quality Standards

| Standard                      | Target                    | Measurement Method            |
| ----------------------------- | ------------------------- | ----------------------------- |
| Economy test coverage         | 100% of transaction types | Test case traceability matrix |
| Auth flow test coverage       | All defined scenarios     | Test case traceability matrix |
| API regression suite runtime  | ≤10 minutes               | Newman execution time         |
| Economy bugs escaping to prod | 0                         | Live ops incident log         |
| P0 API issues pre-launch      | 0                         | JIRA defect log               |
