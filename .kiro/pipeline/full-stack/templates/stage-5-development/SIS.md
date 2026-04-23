# Security Implementation Specification (SIS)

**Project:** [Project Name]
**Platform:** [Android / iOS / KMP Shared / Flutter]
**Track:** [A / B / C]
**Authors:** Security Architect (Natalia Petrova) + Lead Security Engineer (James Wright)
**Date:** YYYY-MM-DD
**Status:** Draft | Under Review | Approved
**Version:** v1 (increment on each SRD change or Stage 6 remediation)
**Referenced Artifact:** SRD v1

## Version History

| Version | Date       | Author | Changes                  | SRD Version |
| ------- | ---------- | ------ | ------------------------ | ----------- |
| v1      | YYYY-MM-DD | [Name] | Initial specification    | SRD vX      |
| v2      | YYYY-MM-DD | [Name] | [Description of changes] | SRD vY      |

> **Change propagation:** When SRD requirements change (e.g., post-Stage-6 defect remediation), update this SIS version, increment the version number, and notify all platform leads within 24 hours. Version tracking follows the repository's document versioning convention (`sis-v1/`, `sis-v2/`, `VERSIONS.md`).

---

## 1. SRD Requirement Mapping

| SRD Requirement                      | Platform Implementation            | Code Location | Verified?    |
| ------------------------------------ | ---------------------------------- | ------------- | ------------ |
| [SRD §X.X: Encryption at rest]       | [How implemented on this platform] | [File/module] | ☐ Yes / ☐ No |
| [SRD §X.X: Certificate pinning]      | [How implemented]                  | [File/module] | ☐ Yes / ☐ No |
| [SRD §X.X: Secure storage]           | [Keychain / Keystore usage]        | [File/module] | ☐ Yes / ☐ No |
| [SRD §X.X: Root/jailbreak detection] | [Implementation approach]          | [File/module] | ☐ Yes / ☐ No |

---

## 2. Cryptographic Implementation

| Use Case        | Algorithm         | Key Size      | Key Storage         | Implementation  |
| --------------- | ----------------- | ------------- | ------------------- | --------------- |
| Data encryption | [AES-256-GCM]     | [256-bit]     | [Keychain/Keystore] | [Library/class] |
| Key derivation  | [HKDF / PBKDF2]   | [Parameters]  | [N/A]               | [Library/class] |
| Signature       | [Ed25519 / ECDSA] | [Key size]    | [Keychain/Keystore] | [Library/class] |
| Hash            | [SHA-256 / SHA-3] | [Output size] | [N/A]               | [Library/class] |

---

## 3. Network Security

| Endpoint          | Pinning  | TLS Version | Certificate Authority | Notes   |
| ----------------- | -------- | ----------- | --------------------- | ------- |
| [api.example.com] | [Yes/No] | [TLS 1.2+]  | [CA name]             | [Notes] |

---

## 4. Platform-Specific Security Patterns

### Android

| Pattern                        | Implementation  | Notes |
| ------------------------------ | --------------- | ----- |
| EncryptedSharedPreferences     | [Configuration] |       |
| BiometricPrompt                | [Configuration] |       |
| Network Security Configuration | [Configuration] |       |
| SafetyNet / Play Integrity     | [Configuration] |       |
| ProGuard/R8 obfuscation        | [Rules file]    |       |

### iOS

| Pattern               | Implementation   | Notes |
| --------------------- | ---------------- | ----- |
| Keychain access group | [Configuration]  |       |
| SecAccessControl      | [Configuration]  |       |
| TrustKit pinning      | [Configuration]  |       |
| Data Protection       | [Configuration]  |       |
| Jailbreak detection   | [Implementation] |       |

### KMP Shared Module

| Pattern                            | Implementation         | Notes                                                                                      |
| ---------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------ |
| expect/actual security interface   | [Interface definition] | Shared module defines security contracts; platforms implement                              |
| Kotlin/Native C interop validation | [Validation rules]     | All inputs validated at C boundary; no raw pointer exposure                                |
| Shared crypto delegation           | [Delegation pattern]   | Shared module must NOT implement crypto directly — delegate to platform adapters           |
| Trust boundary enforcement         | [Boundary definition]  | Shared module treated as untrusted; all security-sensitive operations in platform adapters |
| Memory safety (Kotlin/Native)      | [Safety measures]      | Freezing rules, immutability guarantees, race condition prevention                         |

### Flutter Platform Channels

| Pattern                             | Implementation           | Notes                                                                                |
| ----------------------------------- | ------------------------ | ------------------------------------------------------------------------------------ |
| flutter_secure_storage version      | [Version pinned]         | Must match ADR-SECURITY-STORAGE approved version                                     |
| local_auth plugin version           | [Version pinned]         | Biometric auth via platform channels                                                 |
| Platform channel message validation | [Serialization approach] | All messages validated before native execution; no raw data passthrough              |
| Dart-side security boundary         | [Boundary definition]    | Dart code is NOT a security boundary — assume inspectable; all crypto in native code |
| device_info_plus version            | [Version pinned]         | Device identification via platform channels                                          |
| Custom native code (if any)         | [Location]               | Any native code added for security must follow platform patterns above               |

### Web Frontend

| Pattern                           | Implementation                       | Notes                                                                               |
| --------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------- |
| Content Security Policy (CSP)     | [Policy directive string]            | Must block unsafe-inline, unsafe-eval; define allowed sources                       |
| XSS prevention                    | [React auto-escape + DOMPurify]      | All user input sanitized; no innerHTML/dangerouslySetInnerHTML without sanitization |
| CSRF protection                   | [Double Submit Cookie / SameSite]    | CSRF tokens for state-changing requests; SameSite=Strict on all session cookies     |
| Cookie security                   | [HttpOnly; Secure; SameSite]         | All auth cookies: HttpOnly, Secure, SameSite=Strict or Lax                          |
| Subresource Integrity (SRI)       | [SHA-384 hashes for CDN assets]      | All external scripts/stylesheets loaded with integrity attribute                    |
| HTTPS enforcement                 | [HSTS header]                        | max-age=31536000; includeSubDomains; preload                                        |
| X-Frame-Options / Frame-ancestors | [DENY / CSP frame-ancestors]         | Prevent clickjacking via CSP frame-ancestors 'none'                                 |
| Referrer-Policy                   | [strict-origin-when-cross-origin]    | Control referrer information leakage                                                |
| Permissions-Policy                | [Policy directives]                  | Restrict browser features (camera, microphone, geolocation)                         |
| Input validation                  | [Zod / Yup schema]                   | All form inputs validated client-side; never trust client-side validation alone     |
| JWT storage                       | [HttpOnly cookie (NOT localStorage)] | Auth tokens stored in HttpOnly, Secure, SameSite cookies                            |

### Backend API

| Pattern                  | Implementation                      | Notes                                                                           |
| ------------------------ | ----------------------------------- | ------------------------------------------------------------------------------- |
| Rate limiting            | [Token bucket / sliding window]     | Per-IP and per-user limits; configured per endpoint sensitivity                 |
| Input validation         | [Go validator / Zod on API]         | All inputs validated at API boundary; reject unexpected fields                  |
| Output encoding          | [JSON encoder with escaping]        | All responses properly encoded; no raw user data in responses                   |
| Authentication (authN)   | [JWT / OAuth2 / API key]            | Token validation, expiry checks, issuer/audience verification                   |
| Authorization (authZ)    | [RBAC / ABAC policy engine]         | Role-based or attribute-based access control on every endpoint                  |
| TLS configuration        | [TLS 1.2+ minimum]                  | Strong cipher suites only; HSTS enabled; certificate pinning for mobile clients |
| Request size limits      | [Max body size per endpoint]        | Prevent DoS via oversized payloads                                              |
| SQL injection prevention | [Parameterized queries only]        | No string concatenation for SQL; ORM with parameterized queries                 |
| CORS policy              | [Allowed origins, methods, headers] | Explicitly configured; no wildcard (\*) for production                          |
| Audit logging            | [Structured JSON logs]              | All authN/authZ events logged with request ID, user ID, timestamp               |
| Secret management        | [HashiCorp Vault / AWS Secrets]     | No secrets in env vars or config files; runtime secret injection                |
| API versioning           | [URL path / Accept header]          | Versioned API endpoints; backward-compatible changes within same version        |

---

## 5. PR Security Review Checklist

Every PR touching security-sensitive code must pass:

- [ ] SAST scan (Semgrep custom rules + platform-specific linter)
- [ ] No hardcoded secrets or credentials
- [ ] Cryptographic implementation matches SRD
- [ ] No new dependencies without security review
- [ ] Platform-specific security patterns followed
- [ ] Threat model (STRIDE) updated if new attack surface introduced
- [ ] Reviewed by at least one security team member

---

## 6. Security Parity Verification

| Security Control         | Android | iOS | KMP Shared | Web Frontend | Backend API | Parity Confirmed? |
| ------------------------ | ------- | --- | ---------- | ------------ | ----------- | ----------------- |
| Encryption algorithm     | [ ]     | [ ] | [ ]        | [ ]          | [ ]         | ☐ Yes / ☐ No      |
| Certificate pinning      | [ ]     | [ ] | [ ]        | [ ]          | [ ]         | ☐ Yes / ☐ No      |
| Secure storage           | [ ]     | [ ] | [ ]        | [ ]          | [ ]         | ☐ Yes / ☐ No      |
| Root/jailbreak detection | [ ]     | [ ] | [ ]        | N/A          | [ ]         | ☐ Yes / ☐ No      |
| Biometric auth           | [ ]     | [ ] | [ ]        | N/A          | N/A         | ☐ Yes / ☐ No      |
| XSS/Injection prevention | [ ]     | [ ] | [ ]        | [ ]          | [ ]         | ☐ Yes / ☐ No      |
| Auth token management    | [ ]     | [ ] | [ ]        | [ ]          | [ ]         | ☐ Yes / ☐ No      |
| Input validation         | [ ]     | [ ] | [ ]        | [ ]          | [ ]         | ☐ Yes / ☐ No      |

### Parity Verification Result

**Overall security parity:** ☐ Confirmed / ☐ Not confirmed — [N] gaps identified

| Gap ID    | Security Control | Platform Gap                             | Compensating Control | Defect Classification |
| --------- | ---------------- | ---------------------------------------- | -------------------- | --------------------- |
| [GAP-001] | [Control]        | [Platform] has [X], [Platform] lacks [Y] | [Mitigation]         | [P1/P2]               |

> **Note:** Parity verification results will be included in the Stage 8 Integrity Verification report (per ADR-SECURITY-PLATFORM-PATTERNS §6).

---

**Reviewed by Lead Security Engineer (James Wright) on YYYY-MM-DD**
**Approved by CSO (Dr. Sarah Chen) on YYYY-MM-DD**
