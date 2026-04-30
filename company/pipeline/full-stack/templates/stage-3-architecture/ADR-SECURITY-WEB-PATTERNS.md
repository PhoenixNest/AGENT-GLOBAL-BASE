# ADR: Web Security Patterns

**Project:** [Project Name]
**ADR ID:** ADR-[NNN]
**Status:** Proposed | Accepted | Superseded
**Author:** CIO (Dr. Priya Mehta) + CSO (Dr. Sarah Chen)
**Date:** YYYY-MM-DD
**Pipeline:** Full-Stack Cross-Platform
**Paired With:** ADR-SECURITY-CROSS-PLATFORM.md, ADR-SECURITY-CRYPTO.md

---

## Context

The full-stack application includes a web frontend surface. Web-specific security threats — XSS, CSRF, clickjacking, open redirect, prototype pollution — require a dedicated set of defence-in-depth controls beyond the shared cryptography and cross-platform auth ADRs. These patterns apply exclusively to the web frontend (Track FS-WFE) and web backend integration layer.

This ADR is a mandatory Stage 3 deliverable for all full-stack projects. It must be reviewed by the CSO and approved before Stage 5 development begins.

---

## Decision

Adopt the following web security pattern stack for this project's web surface:

### 1. Content Security Policy (CSP)

| Decision                 | Detail                                                                   |
| ------------------------ | ------------------------------------------------------------------------ |
| **CSP enforcement mode** | [Enforcing / Report-only for first 2 sprints then enforcing]             |
| **Script policy**        | [`strict-dynamic` with per-request nonce / hash-based allowlist]         |
| **Style policy**         | [`self` + design system CDN origin]                                      |
| **Frame ancestors**      | `none` (disables all embedding — adjust if third-party iframes required) |
| **Reporting endpoint**   | [URI for CSP violation reports — e.g., Sentry CSP endpoint]              |
| **Nonce implementation** | [Server-rendered nonce injected per request; not static]                 |

### 2. XSS Prevention

| Layer                   | Control                                                | Implementation                                      |
| ----------------------- | ------------------------------------------------------ | --------------------------------------------------- |
| React JSX auto-escaping | Default — do not bypass with `dangerouslySetInnerHTML` | Enforced in code review checklist                   |
| Rich content (WYSIWYG)  | DOMPurify allowlist sanitisation                       | [`DOMPurify.sanitize(html, {ALLOWED_TAGS: [...]})`] |
| URL parameters          | Validate against allowlist before rendering            | No `href` from untrusted sources                    |
| Trusted Types API       | [Enabled / Not required for this project]              | DOM sink enforcement                                |

### 3. CSRF Protection

| Decision                      | Detail                                                        |
| ----------------------------- | ------------------------------------------------------------- |
| **Pattern**                   | [Double-submit cookie / Synchroniser token / SameSite=Strict] |
| **Token header name**         | [`X-CSRF-Token`]                                              |
| **Token storage**             | [HttpOnly cookie (double-submit) / server-side session]       |
| **SameSite cookie attribute** | `Strict` for auth session cookie; `Lax` minimum for others    |
| **Exemptions**                | [Read-only GET/HEAD/OPTIONS — no state change]                |

### 4. Cookie Security

| Cookie               | HttpOnly | Secure | SameSite | Max-Age | Notes                         |
| -------------------- | -------- | ------ | -------- | ------- | ----------------------------- |
| Session token        | ✅       | ✅     | Strict   | [N] s   |                               |
| CSRF token (if used) | ❌       | ✅     | Strict   | [N] s   | Readable by JS for submission |
| Analytics consent    | ❌       | ✅     | Lax      | 365 d   |                               |
| Preference cookies   | ❌       | ✅     | Lax      | 30 d    |                               |

### 5. Security Headers

| Header                         | Value                                          | Rationale                           |
| ------------------------------ | ---------------------------------------------- | ----------------------------------- |
| `Strict-Transport-Security`    | `max-age=31536000; includeSubDomains; preload` | HSTS — enforce HTTPS                |
| `X-Content-Type-Options`       | `nosniff`                                      | Prevent MIME-type sniffing          |
| `X-Frame-Options`              | `DENY`                                         | Clickjacking protection (legacy)    |
| `Referrer-Policy`              | `strict-origin-when-cross-origin`              | Limit referrer leakage              |
| `Permissions-Policy`           | `camera=(), microphone=(), geolocation=()`     | Restrict browser API access         |
| `Cross-Origin-Opener-Policy`   | `same-origin`                                  | Isolation from cross-origin popups  |
| `Cross-Origin-Embedder-Policy` | `require-corp`                                 | Required for SharedArrayBuffer      |
| `Cross-Origin-Resource-Policy` | `same-origin`                                  | Prevent cross-origin resource reads |

### 6. CORS Configuration

| Setting                       | Value                                                        | Rationale                      |
| ----------------------------- | ------------------------------------------------------------ | ------------------------------ |
| **Allowed origins**           | [Explicit list — no wildcard `*` for credentialled requests] | Explicit allowlist             |
| **Allowed methods**           | `GET, POST, PUT, DELETE, OPTIONS`                            | No `TRACE`, `CONNECT`          |
| **Allowed headers**           | `Content-Type, Authorization, X-CSRF-Token`                  | Minimal set                    |
| **Credentials**               | `true` only for same-site origins                            | Required for cookie-based auth |
| **Max-age (preflight cache)** | `86400` (24 hours)                                           | Reduce preflight overhead      |

### 7. OAuth 2.0 Session Security (Web Surface)

| Decision                   | Detail                                                   |
| -------------------------- | -------------------------------------------------------- |
| **Grant type**             | [Authorization Code + PKCE]                              |
| **Token storage**          | [Memory-only (no localStorage) / Secure HttpOnly cookie] |
| **Access token lifetime**  | [15 minutes]                                             |
| **Refresh token rotation** | [Enabled — single-use refresh tokens]                    |
| **Silent refresh**         | [iframe-based / service-worker-based]                    |
| **Logout**                 | [Clear tokens + revoke refresh token at server]          |

### 8. Subresource Integrity (SRI)

| Resource Type           | SRI Required | Hash Algorithm | Fallback Strategy      |
| ----------------------- | ------------ | -------------- | ---------------------- |
| CDN-hosted scripts      | ✅           | SHA-384        | Inline fallback bundle |
| Third-party stylesheets | ✅           | SHA-384        | Inline critical CSS    |
| First-party assets      | ❌           | N/A            | Same-origin guarantee  |

### 9. Open Redirect Prevention

All redirects (login, logout, OAuth callback) validate the destination URL against a strict allowlist:

- [ ] Relative-only redirects accepted
- [ ] Absolute URLs validated against allowlist before redirect
- [ ] `open_redirect` SAST rule active in CI pipeline

### 10. Prototype Pollution Prevention

- [ ] Object.freeze applied to configuration objects
- [ ] JSON.parse with prototype check or use of `Object.create(null)` for dynamic objects
- [ ] ESLint rule `no-prototype-builtins` enabled

---

## Rationale

[Explain the specific choices made above — e.g., why nonce-based CSP over hash-based, why double-submit cookie CSRF over synchroniser token, etc.]

---

## Trade-offs

| Benefit                                      | Cost                                           |
| -------------------------------------------- | ---------------------------------------------- |
| Defence-in-depth against XSS + CSRF + MITM   | Additional server-side per-request nonce cost  |
| CSP violation reporting provides visibility  | Report pipeline requires a reporting endpoint  |
| SRI prevents CDN compromise from propagating | Manual hash update required on each CDN update |

---

## Compliance

- OWASP ASVS Level 2 — §2 (Authentication), §3 (Session), §5 (Validation), §8 (Data Protection), §12 (Files), §13 (API), §14 (Config)
- OWASP Top 10 2021: A03 Injection (XSS), A01 Broken Access Control (CSRF/CORS), A05 Security Misconfiguration (headers)

---

## Security Implementation Specification Reference

The SIS produced at Stage 4.1 translates this ADR into concrete code-level patterns for each developer. The SIS is the implementation reference; this ADR is the decision record.

---

## Supersession Policy

Changes to any security pattern after Stage 3 approval require:

1. A new superseding ADR referencing this ADR by ID
2. CSO written approval
3. Stage 4 Implementation Plan re-baseline for affected patterns

---

## Sign-Off

| Role | Name               | Decision   | Date       |
| ---- | ------------------ | ---------- | ---------- |
| CTO  | Dr. Kenji Nakamura | ☐ Accepted | YYYY-MM-DD |
| CIO  | Dr. Priya Mehta    | ☐ Accepted | YYYY-MM-DD |
| CSO  | Dr. Sarah Chen     | ☐ Accepted | YYYY-MM-DD |
