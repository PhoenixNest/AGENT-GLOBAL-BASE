# ADR: Cross-Platform Security

| Field         | Value                                                 |
| ------------- | ----------------------------------------------------- |
| **Status**    | Proposed                                              |
| **Context**   | Stage 3 — Full-Stack Cross-Platform Pipeline (P3)     |
| **Decision**  | Cross-platform security patterns                      |
| **Date**      | YYYY-MM-DD                                            |
| **Authors**   | CSO (primary), Security Architect, All Platform Leads |
| **Reviewers** | CTO, CIO, CDO                                         |

---

## Decision

[State the unified security patterns across all platforms.]

## Unified Auth Flow

| Aspect             | Decision                  | Rationale                    |
| ------------------ | ------------------------- | ---------------------------- |
| Authentication     | [OAuth 2.0 / OIDC]        | Cross-platform standard      |
| Token type         | [JWT / opaque]            | [Rationale]                  |
| Token storage      | Per-platform (see below)  | Platform best practices      |
| Refresh strategy   | [Rotation / fixed expiry] | [Rationale]                  |
| Session management | [Centralized service]     | Consistency across platforms |

### Per-Platform Token Storage

| Platform | Storage Method                        | Security Properties |
| -------- | ------------------------------------- | ------------------- |
| Web      | HttpOnly Secure SameSite cookies      | XSS-resistant       |
| iOS      | Keychain                              | OS-level encryption |
| Android  | EncryptedSharedPreferences / Keystore | OS-level encryption |
| Backend  | N/A (issues tokens)                   | N/A                 |

## Cross-Platform Data Protection

| Data Type    | Encryption in Transit        | Encryption at Rest      | Access Control  |
| ------------ | ---------------------------- | ----------------------- | --------------- |
| User PII     | TLS 1.3                      | AES-256 (all platforms) | Role-based      |
| Session data | TLS 1.3                      | Platform-specific       | Token-bound     |
| Sync data    | TLS 1.3 + payload encryption | N/A (transient)         | Platform-scoped |

## Platform-Specific Hardening

| Platform | Hardening Measures                                                       |
| -------- | ------------------------------------------------------------------------ |
| Web      | CSP headers, XSS prevention, CSRF tokens, input sanitization             |
| iOS      | ATS enforcement, Keychain, certificate pinning, App Attest               |
| Android  | Network Security Config, Keystore, certificate pinning, Play Integrity   |
| Backend  | Rate limiting, input validation, authZ enforcement, WAF, DDoS protection |

## Cross-Platform Security Verification

| Verification     | Tool/Method          | Frequency | Platforms Covered |
| ---------------- | -------------------- | --------- | ----------------- |
| SAST             | Semgrep / CodeQL     | Per PR    | All               |
| DAST             | OWASP ZAP            | Stage 7   | Web, Backend      |
| Pen testing      | MASVS categories     | Stage 7   | All               |
| Dependency audit | npm audit / go audit | Per PR    | All               |
| Auth parity test | Cross-platform E2E   | Stage 7   | All               |

---

**Lock-down:** Once approved at Stage 3 gate, these patterns are locked — weakening any pattern requires Stage 3 re-entry.
