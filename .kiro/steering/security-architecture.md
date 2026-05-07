---
inclusion: fileMatch
fileMatchPattern: "**/security/**,**/*security*.md,**/*auth*.ts,**/*auth*.py,**/*auth*.kt,**/*auth*.swift"
description: Security architecture patterns and OWASP best practices
version: "1.0.0"
---

# Security Architecture Steering

This steering file provides security architecture guidance for the workspace. Activate manually when working on security-sensitive features or conducting security reviews.

## Security Context

- **Standards:** OWASP Top 10, OWASP MASVS (Mobile), OWASP ASVS (Web)
- **Compliance:** GDPR, CCPA, SOC 2, ISO 27001
- **Security Testing:** SAST, DAST, penetration testing
- **Threat Modeling:** STRIDE, PASTA

## OWASP Top 10 (2021)

### 1. Broken Access Control

**Risks:**

- Unauthorized access to resources
- Privilege escalation
- Insecure direct object references (IDOR)

**Mitigations:**

- Implement RBAC (Role-Based Access Control)
- Deny by default, allow explicitly
- Validate access on every request
- Use secure session management
- Log access control failures

### 2. Cryptographic Failures

**Risks:**

- Exposure of sensitive data
- Weak encryption algorithms
- Improper key management

**Mitigations:**

- Use TLS 1.2+ for data in transit
- Use AES-256 for data at rest
- Use bcrypt/Argon2 for password hashing
- Store keys in secure vaults (AWS KMS, HashiCorp Vault)
- Never hardcode secrets in code

### 3. Injection

**Risks:**

- SQL injection
- NoSQL injection
- Command injection
- LDAP injection

**Mitigations:**

- Use parameterized queries/prepared statements
- Use ORM frameworks properly
- Validate and sanitize all inputs
- Use allowlists for input validation
- Escape special characters

### 4. Insecure Design

**Risks:**

- Missing security controls
- Inadequate threat modeling
- Insecure architecture

**Mitigations:**

- Conduct threat modeling (STRIDE)
- Implement security by design
- Use secure design patterns
- Perform security architecture reviews
- Document security requirements

### 5. Security Misconfiguration

**Risks:**

- Default credentials
- Unnecessary features enabled
- Verbose error messages
- Missing security headers

**Mitigations:**

- Harden all configurations
- Disable unnecessary features
- Use security headers (CSP, HSTS, X-Frame-Options)
- Implement least privilege
- Regular security audits

### 6. Vulnerable and Outdated Components

**Risks:**

- Known vulnerabilities in dependencies
- Unpatched software
- End-of-life components

**Mitigations:**

- Maintain dependency inventory
- Use dependency scanning (Snyk, Dependabot)
- Keep dependencies up to date
- Remove unused dependencies
- Monitor security advisories

### 7. Identification and Authentication Failures

**Risks:**

- Weak passwords
- Credential stuffing
- Session hijacking
- Broken authentication

**Mitigations:**

- Implement MFA (Multi-Factor Authentication)
- Use strong password policies
- Implement account lockout
- Use secure session management
- Implement rate limiting on auth endpoints

### 8. Software and Data Integrity Failures

**Risks:**

- Unsigned code/updates
- Insecure CI/CD pipelines
- Untrusted deserialization

**Mitigations:**

- Sign all code and updates
- Verify digital signatures
- Secure CI/CD pipelines
- Use integrity checks (checksums, hashes)
- Avoid deserializing untrusted data

### 9. Security Logging and Monitoring Failures

**Risks:**

- Undetected breaches
- Insufficient audit trails
- Missing security alerts

**Mitigations:**

- Log all security events
- Implement centralized logging
- Set up security alerts
- Monitor for anomalies
- Retain logs for compliance

### 10. Server-Side Request Forgery (SSRF)

**Risks:**

- Access to internal resources
- Port scanning
- Cloud metadata access

**Mitigations:**

- Validate and sanitize URLs
- Use allowlists for external requests
- Disable unnecessary protocols
- Implement network segmentation
- Use firewalls and WAF

## Mobile Security (OWASP MASVS)

### 1. Data Storage

- Use Android Keystore / iOS Keychain
- Encrypt sensitive data at rest
- Avoid storing sensitive data in logs
- Clear sensitive data from memory
- Use secure file permissions

### 2. Cryptography

- Use platform crypto APIs
- Use strong algorithms (AES-256, RSA-2048+)
- Implement certificate pinning
- Validate TLS certificates
- Use secure random number generation

### 3. Authentication

- Implement biometric authentication
- Use secure token storage
- Implement session timeout
- Use OAuth 2.0 / OpenID Connect
- Implement device binding

### 4. Network Communication

- Use HTTPS only
- Implement certificate pinning
- Validate server certificates
- Use secure WebSocket (WSS)
- Implement request signing

### 5. Platform Interaction

- Validate all intents (Android)
- Secure IPC mechanisms
- Validate URL schemes (iOS)
- Implement secure deep linking
- Validate WebView content

### 6. Code Quality

- Obfuscate code (R8/ProGuard, SwiftShield)
- Remove debug code
- Implement root/jailbreak detection
- Use anti-tampering techniques
- Implement runtime integrity checks

### 7. Resilience

- Implement anti-debugging
- Detect emulators/simulators
- Implement anti-hooking
- Obfuscate sensitive logic
- Implement integrity verification

## Web Security

### 1. Security Headers

```
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
```

### 2. CORS Configuration

```javascript
// Secure CORS configuration
app.use(
  cors({
    origin: ["https://trusted-domain.com"],
    credentials: true,
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: ["Content-Type", "Authorization"],
  }),
);
```

### 3. Input Validation

```typescript
// Server-side validation
function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email) && email.length <= 254;
}

// Sanitize HTML
import DOMPurify from "dompurify";
const clean = DOMPurify.sanitize(dirty);
```

## API Security

### 1. Authentication

- Use JWT with short expiration
- Implement refresh tokens
- Use API keys for service-to-service
- Implement OAuth 2.0 for third-party
- Use mTLS for high-security scenarios

### 2. Authorization

- Implement RBAC or ABAC
- Validate permissions on every request
- Use least privilege principle
- Implement resource-level authorization
- Log authorization failures

### 3. Rate Limiting

```typescript
// Rate limiting example
const rateLimit = require("express-rate-limit");

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP",
});

app.use("/api/", limiter);
```

## Security Testing

### 1. Static Analysis (SAST)

- Use SonarQube, Checkmarx, or Semgrep
- Scan code for vulnerabilities
- Enforce security rules in CI/CD
- Fix high/critical issues before merge

### 2. Dynamic Analysis (DAST)

- Use OWASP ZAP, Burp Suite
- Test running applications
- Scan for runtime vulnerabilities
- Perform authenticated scans

### 3. Dependency Scanning

- Use Snyk, Dependabot, or npm audit
- Scan for known vulnerabilities
- Update vulnerable dependencies
- Monitor security advisories

### 4. Penetration Testing

- Conduct annual pen tests
- Test authentication and authorization
- Test for injection vulnerabilities
- Test business logic flaws
- Remediate findings

## Incident Response

### 1. Detection

- Monitor security logs
- Set up alerts for anomalies
- Use SIEM tools
- Implement intrusion detection

### 2. Response

- Have incident response plan
- Isolate affected systems
- Preserve evidence
- Notify stakeholders
- Document incident

### 3. Recovery

- Restore from backups
- Patch vulnerabilities
- Reset credentials
- Conduct post-mortem
- Update security controls

## Related Resources

- **Company Security Standards:** `company/library/topics/security.md`
- **Company Architecture Standards:** `company/library/topics/architecture.md`
- **Cyberspace Security Skills:** `.kiro/skills/cyberspace-security/`
- **CSO Profile:** `company/departments/cyberspace-security/supervisor/chief-security-officer/agent/profile.md`

## When to Activate

Activate this steering file when:

- Implementing authentication or authorization
- Handling sensitive data
- Conducting security reviews
- Responding to security incidents
- Implementing security controls
- Reviewing code for security vulnerabilities
