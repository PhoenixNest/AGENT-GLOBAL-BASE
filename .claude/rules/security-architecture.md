---
paths:
  - "**/security/**"
  - "**/*security*.md"
  - "**/*auth*.ts"
  - "**/*auth*.py"
  - "**/*auth*.kt"
  - "**/*auth*.swift"
description: Security architecture patterns and OWASP best practices
---

# Security Architecture

Security architecture guidance. See `.claude/skills/cyberspace-security/` for deep sub-skills.

---

## OWASP Top 10 (2021) — Quick Reference

| #   | Risk                      | Key Mitigation                                           |
| --- | ------------------------- | -------------------------------------------------------- |
| A01 | Broken Access Control     | RBAC, deny-by-default, validate every request            |
| A02 | Cryptographic Failures    | TLS 1.2+, AES-256, Argon2, secure key storage            |
| A03 | Injection                 | Parameterized queries, allowlist validation, ORM         |
| A04 | Insecure Design           | Threat modeling (STRIDE), security by design             |
| A05 | Security Misconfiguration | Harden configs, security headers, least privilege        |
| A06 | Vulnerable Components     | Dependency scanning (Snyk, Dependabot), patch regularly  |
| A07 | Auth Failures             | MFA, account lockout, rate limiting on auth              |
| A08 | Data Integrity Failures   | Sign code/updates, secure CI/CD, verify signatures       |
| A09 | Logging Failures          | Log all security events, centralized SIEM, alerting      |
| A10 | SSRF                      | Validate/sanitize URLs, allowlists, network segmentation |

---

## Mobile Security (OWASP MASVS)

- **Storage:** Android Keystore / iOS Keychain, encrypted at rest
- **Crypto:** AES-256, RSA-2048+, certificate pinning
- **Auth:** Biometric auth, OAuth 2.0 / OpenID Connect, session timeout
- **Network:** HTTPS only, certificate pinning, TLS certificate validation
- **Code:** Obfuscation (R8/ProGuard), root/jailbreak detection

---

## Web Security Headers

```
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
```

---

## Security Testing Layers

1. **SAST:** SonarQube, Semgrep — scan code in CI/CD
2. **DAST:** OWASP ZAP, Burp Suite — scan running app
3. **Dependency scanning:** Snyk, npm audit
4. **Pen testing:** Annual, cover auth/injection/business logic
