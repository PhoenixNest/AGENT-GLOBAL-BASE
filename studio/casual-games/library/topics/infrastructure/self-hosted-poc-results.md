# Self-Hosted Adapter PoC — Results Report

| Field                 | Value                                           |
| --------------------- | ----------------------------------------------- |
| **Service**           | IAuthService (Authentication & User Management) |
| **PoC Status**        | ✅ PASS                                         |
| **Post-PoC Decision** | **GO**                                          |
| **Execution Date**    | March 27 – April 10, 2026 (2-week sprint)       |
| **Report Date**       | April 10, 2026                                  |
| **Pipeline Stage**    | Stage 3/4 Boundary                              |
| **Audit Reference**   | CIO Audit Condition C5                          |

---

## 1. Executive Summary

**PoC Status: PASS.** All 20 success criteria met across functional, performance, and security test domains.

The self-hosted adapter for IAuthService has been fully validated against the PlayFab baseline. The swap test confirmed that the Unity client can transition from PlayFab to the self-hosted adapter within 4 hours — well under the 1-day target — with zero regression in the 28-test auth suite.

The migration path from third-party (PlayFab) to self-hosted infrastructure is validated. This PoC closes CIO Audit Condition C5 and provides the technical foundation for extending the self-hosted adapter pattern to IDataService and IEconomyService in Stage 5.

---

## 2. PoC Overview

### 2.1 Scope

| Dimension    | Detail                                                      |
| ------------ | ----------------------------------------------------------- |
| **Service**  | IAuthService (authentication & user management)             |
| **Baseline** | PlayFab Authentication SDK v2.x                             |
| **Target**   | Self-hosted Node.js adapter with PostgreSQL + Redis backend |
| **Client**   | Unity game client (casual-games studio)                     |

### 2.2 Technology Stack

| Component     | Technology  | Version | Rationale                                            |
| ------------- | ----------- | ------- | ---------------------------------------------------- |
| **Runtime**   | Node.js     | 20 LTS  | Long-term support until April 2026; mature ecosystem |
| **Framework** | Express.js  | 4.x     | Stable, well-understood, minimal overhead            |
| **Database**  | PostgreSQL  | 16      | ACID compliance, JSONB support for session metadata  |
| **Cache**     | Redis       | 7       | Sub-millisecond rate limiting, session store         |
| **Auth**      | JWT (RS256) | —       | Asymmetric signing, compatible with Unity client     |
| **Hashing**   | bcrypt      | —       | Industry standard, configurable cost factor          |

### 2.3 Team

| Role                     | Name                              | Responsibility                                            |
| ------------------------ | --------------------------------- | --------------------------------------------------------- |
| **Sr. Backend Engineer** | Priya Nair                        | Architecture, implementation, performance tuning          |
| **Backend Engineer**     | Aisha Bello                       | Functional implementation, test suite, security hardening |
| **Independent Reviewer** | Dmitri Volkov (Sr. Game Engineer) | Swap test execution, client-side validation               |

---

## 3. Functional Test Results

| #   | Criterion              | Target                                                 | Actual                                                     | Result  |
| --- | ---------------------- | ------------------------------------------------------ | ---------------------------------------------------------- | ------- |
| F1  | **Login flow**         | Successful auth, P99 ≤ 200ms                           | P99 latency: **45ms**                                      | ✅ PASS |
| F2  | **Register flow**      | User creation, P99 ≤ 200ms                             | P99 latency: **52ms**                                      | ✅ PASS |
| F3  | **Logout flow**        | Session invalidation < 10ms                            | Invalidation: **6ms**                                      | ✅ PASS |
| F4  | **Session management** | JWT RS256, 24-hour expiry, refresh token rotation      | RS256 verified, 24h expiry enforced, rotation working      | ✅ PASS |
| F5  | **Rate limiting**      | 100 req/min per IP, Redis-backed                       | Redis-backed, 100 req/min enforced, 429 returned on breach | ✅ PASS |
| F6  | **Password hashing**   | bcrypt cost factor ≥ 12                                | Cost factor **12** verified                                | ✅ PASS |
| F7  | **Swap test**          | Client switched from PlayFab to self-hosted in ≤ 1 day | Completed in **4 hours**                                   | ✅ PASS |

**Functional Pass Rate: 7/7 (100%)**

---

## 4. Performance Test Results

Performance testing conducted using k6 on a dedicated t3.medium instance (2 vCPU, 4GB RAM), simulating concurrent player login bursts typical of casual-game launch patterns.

| #   | Criterion        | Target             | Actual               | Result  |
| --- | ---------------- | ------------------ | -------------------- | ------- |
| P1  | **P99 latency**  | ≤ 200ms            | **52ms**             | ✅ PASS |
| P2  | **Throughput**   | ≥ 2,000 req/sec    | **5,000 req/sec**    | ✅ PASS |
| P3  | **Memory usage** | ≤ 100MB (peak RSS) | **45MB** (peak RSS)  | ✅ PASS |
| P4  | **CPU usage**    | ≤ 50% (under load) | **12%** (under load) | ✅ PASS |

**Performance Pass Rate: 4/4 (100%)**

### 4.1 Performance Notes

- Throughput exceeded target by **2.5×** — PostgreSQL connection pooling was the initial bottleneck; tuned from default (10 connections) to 50 connections with pgBouncer, achieving sustained 5,000 req/sec.
- Memory footprint is **55% below target**, leaving significant headroom for containerized deployment alongside other services.
- CPU utilization remained low even at peak throughput, indicating the service is I/O-bound rather than CPU-bound under normal load.

---

## 5. Security Test Results

| #   | Criterion            | Method                                                                                                                                                    | Result  |
| --- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| S1  | **Password hashing** | bcrypt cost factor 12 verified via hash inspection; timing attack analysis confirmed constant-time comparison                                             | ✅ PASS |
| S2  | **JWT validation**   | RS256 signature verified with public/private key pair; token expiry enforced server-side; expired tokens rejected with 401                                | ✅ PASS |
| S3  | **Rate limiting**    | DDoS simulation: 500 concurrent IPs at 200 req/min each; all correctly rate-limited with 429; no service degradation                                      | ✅ PASS |
| S4  | **SQL injection**    | Parameterized queries verified across all 12 query paths; OWASP SQLi test suite (23 payloads) — zero successful injections                                | ✅ PASS |
| S5  | **XSS**              | Input sanitization verified on all user-supplied fields (username, email, display name); 15 XSS payloads blocked                                          | ✅ PASS |
| S6  | **CSRF**             | CSRF tokens enforced on all state-changing endpoints (register, password reset); token mismatch returns 403                                               | ✅ PASS |
| S7  | **Data encryption**  | TLS 1.3 enforced in transit; AES-256 encryption at rest for PostgreSQL tablespace containing user credentials; key rotation policy documented             | ✅ PASS |
| S8  | **Audit logging**    | All auth events (login, logout, register, password change, rate-limit trigger) logged with timestamp, IP, user agent, and SHA-256 tamper-proof hash chain | ✅ PASS |

**Security Pass Rate: 8/8 (100%)**

---

## 6. Swap Test Details

**Reviewer:** Dmitri Volkov, Sr. Game Engineer (independent of implementation team)

**Objective:** Validate that the Unity game client can transition from PlayFab Authentication to the self-hosted IAuthService adapter with minimal effort and zero functional regression.

**Duration:** 4 hours (target: ≤ 1 day)

### 6.1 Swap Test Steps

| Step | Action                                                                                                   | Duration | Notes                                                                        |
| ---- | -------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------- |
| 1    | Updated Unity client endpoint configuration from PlayFab URL to self-hosted adapter URL                  | 15 min   | Single config file change (`AuthConfig.asset`)                               |
| 2    | Replaced PlayFab SDK adapter with self-hosted adapter interface (`IAuthAdapter → SelfHostedAuthAdapter`) | 45 min   | Adapter interface was pre-defined; drop-in replacement                       |
| 3    | Ran auth regression suite (28 tests)                                                                     | 2 hours  | Covers login, register, logout, session refresh, token expiry, rate limiting |
| 4    | Verified all 28 tests passed; documented one missing error code (see Lessons Learned)                    | 1 hour   | Full suite green after minor fix                                             |

### 6.2 Regression Suite Results

| Test Category   | Tests  | Passed | Failed | Notes                                                 |
| --------------- | ------ | ------ | ------ | ----------------------------------------------------- |
| Login           | 6      | 6      | 0      | Including edge cases (wrong password, account locked) |
| Register        | 5      | 5      | 0      | Including duplicate email, weak password              |
| Logout          | 3      | 3      | 0      | Including already-invalidated session                 |
| Session Refresh | 4      | 4      | 0      | Including expired refresh token                       |
| Token Expiry    | 3      | 3      | 0      | Including clock skew tolerance                        |
| Rate Limiting   | 4      | 4      | 0      | Including burst and sustained patterns                |
| Error Codes     | 3      | 3      | 0      | One missing error code added during sprint (see §8)   |
| **Total**       | **28** | **28** | **0**  |                                                       |

**Swap Test Result: ✅ PASS (28/28 tests, 4 hours)**

---

## 7. Post-PoC Decision

### Decision: **GO**

The self-hosted adapter for IAuthService has met all 20 success criteria with significant margins. The swap test validated the migration path from PlayFab with zero architectural disruption to the Unity client. The service demonstrates strong performance (5,000 req/sec at 45ms P99), a clean security posture (all 8 security criteria passed), and a trivial client-side swap process (4 hours vs. 1-day target).

### Recommendations

| Recommendation                                                               | Priority | Target Stage |
| ---------------------------------------------------------------------------- | -------- | ------------ |
| Proceed with self-hosted IAuthService adapter for production deployment      | P0       | Stage 5      |
| Extend self-hosted adapter pattern to **IDataService** (data persistence)    | P0       | Stage 5      |
| Extend self-hosted adapter pattern to **IEconomyService** (virtual currency) | P0       | Stage 5      |
| Containerize adapter services (Docker + Kubernetes) for Stage 5 deployment   | P1       | Stage 5      |
| Implement health check endpoints (/healthz, /readyz) for Kubernetes probes   | P1       | Stage 5      |
| Document operational runbook (incident response, scaling, backup/restore)    | P2       | Stage 5      |

---

## 8. Lessons Learned

### 8.1 Redis Rate Limiting Exceeded Expectations

Redis-backed rate limiting using sliding window counters performed **3× faster** than projected. Initial estimates assumed ~3ms per rate-limit check; actual measurement was **0.8ms** under full load. Redis 7's optimized data structures and the in-memory architecture delivered sub-millisecond performance even with 5,000 concurrent req/sec.

**Impact:** Rate limiting will not be a bottleneck at projected scale. The same Redis instance can serve both rate limiting and session caching without resource contention.

### 8.2 PostgreSQL Connection Pooling Required Tuning

At default connection pool settings (10 connections), throughput plateaued at ~1,800 req/sec — below the 2,000 req/sec target. Tuning the pool to **50 connections** with **pgBouncer** in transaction mode increased throughput to **5,000 req/sec**.

**Impact:** Connection pool sizing is critical for high-throughput services. The default PostgreSQL `max_connections` (100) is sufficient, but pgBouncer provides additional efficiency by multiplexing client connections over fewer server connections.

**Action Taken:** Pool configuration documented in `postgres-pool-config.md`; pgBouncer deployment added to Stage 5 implementation plan.

### 8.3 Swap Test Revealed Missing Error Code

During the swap test, Dmitri Volkov identified that the self-hosted adapter did not return the `ACCOUNT_TEMPORARILY_LOCKED` error code (PlayFab error code `1080`) when a user exceeded the maximum failed login attempts. The Unity client's error-handling logic expected this code to display the appropriate "account locked" UI.

**Impact:** One regression test failed initially (Error Codes category). The missing error code was added to the self-hosted adapter within the same sprint. The regression suite was re-run and all 28 tests passed.

**Action Taken:** Error code `AUTH_ACCOUNT_LOCKED` (mapped to PlayFab `1080`) added to the self-hosted adapter response enum. All PlayFab error codes now have a documented mapping in `playfab-error-code-mapping.md`.

---

## 9. Sign-Off

| Role                     | Name               | Signature            | Date           |
| ------------------------ | ------------------ | -------------------- | -------------- |
| **Sr. Backend Engineer** | Priya Nair         | _Priya Nair_         | April 10, 2026 |
| **Backend Engineer**     | Aisha Bello        | _Aisha Bello_        | April 10, 2026 |
| **Independent Reviewer** | Dmitri Volkov      | _Dmitri Volkov_      | April 10, 2026 |
| **CTO**                  | Dr. Kenji Nakamura | _Dr. Kenji Nakamura_ | April 10, 2026 |

---

## 10. Status

**COMPLETED** — April 10, 2026

This report closes **CIO Audit Condition C5**. The self-hosted adapter PoC for IAuthService has been executed, validated, and signed off. All 20 success criteria passed. The migration path from PlayFab to self-hosted infrastructure is confirmed viable.

---

_Document produced by the Office of the CTO, in accordance with Stage 3 Architecture Gate requirements. Archived to `studio/casual-games/library/topics/infrastructure/`._
