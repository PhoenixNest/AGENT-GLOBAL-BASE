# ADR: Cryptography

| Field              | Value                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------- |
| **Status**         | Proposed                                                                                    |
| **Context**        | Stage 3 — Web Application Pipeline (P1)                                                     |
| **Decision**       | Web application cryptography standards                                                      |
| **Date**           | YYYY-MM-DD                                                                                  |
| **Authors**        | CSO (primary), Security Architect                                                           |
| **Reviewers**      | CTO, CIO                                                                                    |

---

## Decision

[State the chosen cryptography standards for the web application.]

## TLS Configuration

| Setting | Value | Rationale |
| ------- | ----- | --------- |
| Minimum TLS version | TLS 1.3 | Latest, most secure |
| Cipher suites | [ECDHE + AES-256-GCM, ECDHE + ChaCha20-Poly1305] | Forward secrecy + authenticated encryption |
| Certificate management | [Vercel managed / Let's Encrypt auto-renewal] | Automatic rotation |
| HSTS | max-age=31536000; includeSubDomains; preload | Prevent downgrade attacks |

## Password Hashing

| Algorithm | Parameters | Rationale |
| --------- | ---------- | --------- |
| bcrypt | Work factor 12+ | Industry standard, well-audited |
| argon2id (alternative) | Memory: 64MB, Iterations: 3, Parallelism: 4 | Memory-hard, resistant to GPU attacks |

## JWT Signing

| Algorithm | Key Size | Rationale |
| --------- | -------- | --------- |
| RS256 | 2048-bit RSA minimum | Asymmetric, well-supported |
| EdDSA (Ed25519) | 256-bit | Faster, smaller signatures |

## Data Encryption (at Rest)

| Data Type | Algorithm | Key Management | Implementation |
| --------- | --------- | -------------- | -------------- |
| PII in database | AES-256-GCM | AWS KMS / HashiCorp Vault | Application-level encryption |
| Session tokens | Encrypted at rest | Application key | Server-side session store |
| Backup data | AES-256 | Cloud provider managed | Automatic |

## Random Number Generation

| Context | Implementation | Rationale |
| ------- | -------------- | --------- |
| Token generation | `crypto.randomBytes()` (Node.js) / `crypto.getRandomValues()` (browser) | CSPRNG, backed by OS entropy |
| CSRF tokens | `crypto.randomBytes(32).toString('hex')` | 256-bit entropy |
| Nonces | `crypto.randomUUID()` (v4 UUID) | Cryptographically unique |

## Cryptographic Libraries

| Library | Version | Purpose | Assessment |
| ------- | ------- | ------- | ---------- |
| Web Crypto API | Browser native | Client-side hashing, random generation | Well-audited, standard API |
| Node.js crypto module | Built-in | Server-side hashing, random generation | Standard library, well-maintained |
| bcrypt / argon2 | Latest stable | Password hashing | Industry standard |
| jsonwebtoken / jose | Latest stable | JWT signing/verification | Well-maintained, audited |

## Alternatives Considered

| Alternative | Assessment |
| ----------- | ---------- |
| libsodium / NaCl | Excellent library but adds dependency complexity; Web Crypto API preferred for browser-native operations |
| CryptoJS | Deprecated; use Web Crypto API instead |

## Compliance

| Standard | Requirement | Status |
| -------- | ----------- | ------ |
| NIST SP 800-131A | Approved algorithms only | ✅ Compliant |
| OWASP Cryptographic Storage Cheat Sheet | All recommendations followed | ✅ Compliant |
| GDPR (data encryption) | PII encrypted at rest | ✅ Compliant |

---

**Lock-down:** Once approved at Stage 3 gate, these cryptographic standards are locked — weakening any standard requires Stage 3 re-entry.
