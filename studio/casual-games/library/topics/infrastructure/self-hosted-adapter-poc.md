---
title: "Self-Hosted Adapter PoC: IAuthService"
owner: "Priya Nair, Sr. Backend Engineer"
reviewed-by: "Dr. Priya Mehta, CIO"
created: "2026-04-12"
status: "Draft"
stage: "4"
audit-condition: "C5"
tags:
  [
    "poc",
    "self-hosted",
    "iauthservice",
    "authentication",
    "migration",
    "adapter",
  ]
---

# Self-Hosted Adapter PoC: IAuthService

> **CIO Audit Finding C5:** _"The team's self-hosted capability is theoretical, not proven."_
>
> This PoC plan validates the migration path from PlayFab to self-hosted backend by implementing the most critical service — authentication — as a standalone, production-quality component.

---

## Executive Summary

Per CIO audit finding C5, the team's self-hosted capability remains **theoretical, not proven**. While our architecture (ADR-001: Platform Strategy) defines a self-hosted adapter layer, no one has demonstrated that we can actually build, deploy, and operate a self-hosted service that meets our security, performance, and integration requirements.

This PoC addresses that gap by implementing **IAuthService** — the authentication and user management service — as a fully functional self-hosted component. Auth is the highest-impact test case because:

1. **Critical path:** Auth is the first service every user interacts with; failure is non-negotiable
2. **Clear interface boundary:** IAuthService contract is well-defined, with PlayFab adapter already documented
3. **Security sensitivity:** Validates our ability to handle passwords, sessions, tokens, and rate limiting
4. **Migration indicator:** If we can't self-host auth, we can't self-host anything

**Duration:** 2-week sprint during Stage 3/4
**Owner:** Priya Nair (Sr. Backend Engineer)

---

## 1. PoC Scope

### In Scope

| Component                    | Description                                                                             |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| **IAuthService contract**    | Same interface as PlayFab adapter — drop-in replacement                                 |
| **Authentication endpoints** | Login, register, logout, session refresh, password reset                                |
| **Session management**       | JWT-based sessions with configurable TTL                                                |
| **Password security**        | bcrypt hashing (cost factor ≥ 12), minimum 8-character policy                           |
| **Rate limiting**            | Per-IP and per-account rate limiting (fail2ban-style)                                   |
| **Unity client integration** | Modified auth flow in Unity client supporting both PlayFab and self-hosted              |
| **Swap test**                | Verify client can switch between PlayFab and self-hosted auth with < 1 day adapter work |

### Out of Scope

| Component                     | Reason                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------- |
| PlayFab Economy migration     | Out of scope — tested separately in future PoC                                        |
| PlayFab Leaderboard migration | Out of scope — depends on auth PoC results                                            |
| Full backend replacement      | This PoC tests ONE service, not the full stack                                        |
| Production deployment         | PoC runs in development environment; production readiness is a separate milestone     |
| Multi-tenancy                 | Multi-tenant support will be added per ADR-007; this PoC tests single-tenant baseline |

---

## 2. PoC Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Self-Hosted Auth PoC Architecture                                       │
│                                                                          │
│  ┌──────────────┐          ┌──────────────────────┐          ┌─────────┐│
│  │  Unity Client│          │  Self-Hosted Adapter  │          │ PostgreSQL│
│  │              │◀────────▶│                      │◀────────▶│         ││
│  │  Auth Flow:  │  HTTPS   │  IAuthService        │  SQL     │ Tables: ││
│  │  • Login     │  / REST  │  ┌────────────────┐  │          │ • users ││
│  │  • Register  │          │  │ Node.js/Express │  │          │ • sessions│
│  │  • Logout    │          │  │ or Python/     │  │          │ • audit_log│
│  │  • Refresh   │          │  │ FastAPI        │  │          │         ││
│  │              │          │  └────────────────┘  │          │         ││
│  │  Swap Config:│          │                      │          └─────────┘│
│  │  AUTH_PROVIDER│          │  Security:           │                     │
│  │  = "playfab"  │          │  • bcrypt (≥12)     │                     │
│  │  or "self"    │          │  • JWT (RS256)      │                     │
│  └──────────────┘          │  • Rate limiting     │                     │
│                            │  • HTTPS (TLS 1.3)   │                     │
│                            └──────────────────────┘                     │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  IAuthService Contract (shared interface)                         │   │
│  │                                                                    │   │
│  │  interface IAuthService {                                          │   │
│  │    login(email, password): AuthResult                              │   │
│  │    register(email, password, displayName): AuthResult              │   │
│  │    logout(sessionToken): void                                      │   │
│  │    refreshSession(refreshToken): AuthResult                        │   │
│  │    resetPassword(email): void                                      │   │
│  │    validateSession(sessionToken): SessionInfo                      │   │
│  │  }                                                                 │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Technology Stack Decision

| Component          | Technology                       | Rationale                                                              |
| ------------------ | -------------------------------- | ---------------------------------------------------------------------- |
| **Runtime**        | Node.js 20 LTS                   | Team expertise, existing adapter codebase in TypeScript                |
| **Framework**      | Express.js 4.x                   | Mature, well-understood, large ecosystem                               |
| **Database**       | PostgreSQL 16                    | Industry standard, strong ACID guarantees, Row-Level Security          |
| **Password Hash**  | bcrypt (Node.js)                 | Industry standard, configurable cost factor                            |
| **Session Tokens** | JWT (RS256)                      | Asymmetric signing; private key on server, public key for verification |
| **Rate Limiting**  | express-rate-limit + redis-store | Battle-tested, Redis-backed for distributed deployments                |

### 2.2 Database Schema

```sql
-- Core schema for PoC (single-tenant baseline)
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    display_name    VARCHAR(100) NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    last_login      TIMESTAMPTZ,
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE TABLE sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash      VARCHAR(255) NOT NULL,
    refresh_token   VARCHAR(255) NOT NULL UNIQUE,
    expires_at      TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    revoked         BOOLEAN DEFAULT FALSE
);

CREATE TABLE audit_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    action          VARCHAR(50) NOT NULL,  -- 'LOGIN', 'LOGOUT', 'REGISTER', 'PASSWORD_RESET'
    ip_address      INET,
    user_agent      TEXT,
    result          VARCHAR(20) NOT NULL,  -- 'SUCCESS', 'FAILURE'
    timestamp       TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);
CREATE INDEX idx_audit_log_user ON audit_log(user_id, timestamp);
```

---

## 3. Success Criteria

The PoC is considered **successful** only if ALL of the following criteria are met:

### 3.1 Functional Criteria

| #   | Criterion                                       | Pass/Fail |
| --- | ----------------------------------------------- | --------- |
| F1  | Login flow works end-to-end (email + password)  | ☐         |
| F2  | Registration flow works with validation         | ☐         |
| F3  | Logout invalidates session server-side          | ☐         |
| F4  | Session refresh works without re-authentication | ☐         |
| F5  | Password reset flow works (email-triggered)     | ☐         |
| F6  | Expired tokens are rejected                     | ☐         |
| F7  | Revoked tokens are rejected                     | ☐         |

### 3.2 Performance Criteria

| #   | Criterion                               | Target     | Measured |
| --- | --------------------------------------- | ---------- | -------- |
| P1  | Login P99 latency                       | ≤ 200ms    | ☐        |
| P2  | Registration P99 latency                | ≤ 300ms    | ☐        |
| P3  | Session validation P99 latency          | ≤ 50ms     | ☐        |
| P4  | Concurrent login throughput (100 req/s) | ≤ 1% error | ☐        |

> **Note:** P99 latency target of ≤ 200ms matches the PlayFab target, ensuring no degradation if we migrate.

### 3.3 Security Criteria

| #   | Criterion                                              | Pass/Fail |
| --- | ------------------------------------------------------ | --------- |
| S1  | Password hashing: bcrypt with cost factor ≥ 12         | ☐         |
| S2  | JWT signing: RS256 (asymmetric)                        | ☐         |
| S3  | Rate limiting: 5 failed attempts per 15 minutes per IP | ☐         |
| S4  | Account lockout after 10 consecutive failures          | ☐         |
| S5  | HTTPS enforced (TLS 1.3 minimum)                       | ☐         |
| S6  | No passwords logged (application or access logs)       | ☐         |
| S7  | SQL injection attempt blocked                          | ☐         |
| S8  | XSS attempt in display_name blocked                    | ☐         |

### 3.4 Swap Test Criterion

| #   | Criterion                                                                                        | Pass/Fail |
| --- | ------------------------------------------------------------------------------------------------ | --------- |
| SW1 | Unity client switches from PlayFab auth to self-hosted auth with < 1 day of adapter code changes | ☐         |

> **Swap Test Method:** A developer unfamiliar with the codebase (not Priya Nair) will be given the task of switching the auth provider. If they complete it in < 1 working day, the criterion passes.

---

## 4. PoC Timeline

### Week 1: Service Implementation

| Day | Task                                                                | Owner      | Deliverable                       |
| --- | ------------------------------------------------------------------- | ---------- | --------------------------------- |
| 1   | Project setup, Express scaffolding, PostgreSQL schema               | Priya Nair | Code repo, DB schema              |
| 2   | IAuthService interface definition, user registration endpoint       | Priya Nair | `/register` endpoint + unit tests |
| 3   | Login endpoint, bcrypt integration, JWT generation                  | Priya Nair | `/login` endpoint + unit tests    |
| 4   | Session management (refresh, logout, validation), rate limiting     | Priya Nair | Session endpoints + rate limiter  |
| 5   | Audit logging, error handling, input validation, security hardening | Priya Nair | Complete API with audit trail     |

### Week 2: Integration, Testing, and Documentation

| Day | Task                                                       | Owner         | Deliverable                  |
| --- | ---------------------------------------------------------- | ------------- | ---------------------------- |
| 6   | Unity client integration (auth provider config switch)     | Priya Nair    | Modified Unity auth flow     |
| 7   | End-to-end testing (all functional criteria F1–F7)         | Priya Nair    | Test results document        |
| 8   | Performance testing (load test P99 latency targets)        | Aisha Bello   | Performance benchmark report |
| 9   | Swap test (independent developer attempts provider switch) | Dmitri Volkov | Swap test results            |
| 10  | Documentation, PoC summary, go/no-go recommendation        | Priya Nair    | PoC report for CIO review    |

---

## 5. Post-PoC Decision Framework

### If PoC Succeeds (all criteria met)

| Outcome          | Action                                                                       |
| ---------------- | ---------------------------------------------------------------------------- |
| **Confidence**   | Self-hosted migration path validated for IAuthService                        |
| **Next Step**    | Expand PoC to ILeaderboardService (next most complex service)                |
| **Architecture** | Self-hosted adapter layer confirmed as viable; proceed with Stage 3 ADR lock |
| **Investment**   | Budget allocation for self-hosted infrastructure approved                    |
| **Timeline**     | Self-hosted production readiness estimated at Stage 8+                       |

### If PoC Fails (any P0 criterion unmet)

| Outcome          | Action                                                             |
| ---------------- | ------------------------------------------------------------------ |
| **Gap Analysis** | Document each failed criterion with root cause                     |
| **Reassessment** | Evaluate whether gaps are addressable with more time/budget        |
| **Strategy**     | If unaddressable: PlayFab-only strategy; self-hosted deprioritized |
| **Lessons**      | Document technical gaps for future reference                       |
| **Escalation**   | CIO convenes CTO + CSO to reassess platform strategy               |

### Partial Success (functional met, performance or swap test failed)

| Outcome         | Action                                                   |
| --------------- | -------------------------------------------------------- |
| **Functional**  | Auth service works but has performance or usability gaps |
| **Remediation** | Address specific failures; extend PoC by 1 week          |
| **Re-test**     | Re-run failed criteria only                              |
| **Decision**    | Go/no-go after remediation re-test                       |

---

## 6. Risk Assessment

| Risk                                                | Likelihood | Impact | Mitigation                                                     |
| --------------------------------------------------- | ---------- | ------ | -------------------------------------------------------------- |
| Scope creep beyond IAuthService                     | Medium     | P1     | Strict scope boundaries; CIO approval required for expansion   |
| Underestimated security requirements                | Medium     | P0     | CSO review of security criteria before PoC begins              |
| Unity client integration more complex than expected | Low        | P2     | Dedicated Day 6–7 for integration; Aisha Bello on standby      |
| Swap test takes > 1 day                             | Low        | P1     | Well-documented IAuthService interface; adapter pattern tested |
| Performance targets not met on dev hardware         | Low        | P2     | Baseline hardware: 4-core, 8GB RAM minimum                     |

---

## 7. Team and Roles

| Role                    | Person          | Responsibility                                                  |
| ----------------------- | --------------- | --------------------------------------------------------------- |
| **PoC Lead**            | Priya Nair      | Implementation, testing, documentation, go/no-go recommendation |
| **Performance Testing** | Aisha Bello     | Load testing setup, benchmark execution, results analysis       |
| **Security Review**     | Dmitri Volkov   | Security criteria validation, swap test execution, code review  |
| **CIO Oversight**       | Dr. Priya Mehta | Scope approval, risk assessment, final go/no-go decision        |
| **CSO Consultation**    | Dr. Sarah Chen  | Security criteria review, COPPA implications assessment         |

---

## 8. Deliverables

| Deliverable                         | Format          | Due Date       | Recipient     |
| ----------------------------------- | --------------- | -------------- | ------------- |
| Self-hosted auth service code       | Git repository  | Week 1, Day 5  | CTO review    |
| Unity client with dual auth support | Unity project   | Week 2, Day 6  | CDO review    |
| Functional test results             | Markdown report | Week 2, Day 7  | CIO           |
| Performance benchmark report        | Markdown report | Week 2, Day 8  | CTO, CIO      |
| Swap test results                   | Markdown report | Week 2, Day 9  | CIO           |
| PoC summary and recommendation      | Markdown report | Week 2, Day 10 | CIO, CTO, CSO |

---

## 9. Review and Sign-off

| Item                  | Detail                                    |
| --------------------- | ----------------------------------------- |
| **PoC Owner**         | Priya Nair, Sr. Backend Engineer          |
| **Performance Lead**  | Aisha Bello, Backend Engineer             |
| **Security Reviewer** | Dmitri Volkov                             |
| **CIO Approval**      | Dr. Priya Mehta                           |
| **CSO Consultation**  | Dr. Sarah Chen                            |
| **Status**            | Draft — pending Stage 4 planning approval |
| **PoC Window**        | Stage 3/4 boundary (2-week sprint)        |

---

_This document satisfies CIO Audit Condition C5. The PoC will prove or disprove our self-hosted capability with concrete, measurable criteria._
