# ADR-NNN: Cryptographic Standard Selection

| Metadata          | Value                                          |
| ----------------- | ---------------------------------------------- |
| **ADR Number**    | ADR-NNN                                        |
| **Title**         | Cryptographic Standard Selection               |
| **Status**        | Proposed                                       |
| **Decision Date** | YYYY-MM-DD                                     |
| **Authors**       | Security Architect (Natalia Petrova)           |
| **Reviewers**     | CSO (Dr. Sarah Chen), CTO (Dr. Kenji Nakamura) |
| **Stage**         | 3 -- Architecture                              |
| **Category**      | Security / Cryptography                        |

---

## Context

Without standardized cryptographic standards, backend teams may independently select algorithms, libraries, and key sizes -- creating an inconsistent security posture that complicates auditing, increases vulnerability surface, and makes incident response difficult. This ADR establishes the authoritative cryptographic standard for all backend services.

---

## Decision

### Symmetric Encryption

| Status         | Algorithm                | Key Size | Mode | Usage                                          |
| -------------- | ------------------------ | -------- | ---- | ---------------------------------------------- |
| **Approved**   | AES                      | 256-bit  | GCM  | All new development (authenticated encryption) |
| **Deprecated** | AES                      | 256-bit  | CBC  | Existing code only -- migrate within 6 months  |
| **Prohibited** | DES, 3DES, RC4, Blowfish | --       | --   | Must not be used under any circumstance        |

**Rationale:** AES-256-GCM provides authenticated encryption (confidentiality + integrity) in a single operation. CBC requires separate MAC, creating implementation complexity and potential for encrypt-then-MAC ordering mistakes.

### Asymmetric Encryption

| Use Case                 | Algorithm       | Parameters                      |
| ------------------------ | --------------- | ------------------------------- |
| Key exchange             | ECDH            | Curve25519 (preferred) or P-256 |
| JWT signing              | EdDSA (Ed25519) | --                              |
| Digital signatures       | ECDSA           | P-256 (secp256r1)               |
| High-security signatures | ECDSA           | P-384 (secp384r1)               |
| RSA fallback             | RSA             | 4096-bit minimum, OAEP padding  |

**Rationale:** ECC provides equivalent security to RSA at much smaller key sizes (P-256 approx RSA-3072). Curve25519 is preferred for ECDH due to implementation simplicity and resistance to side-channel attacks. EdDSA (Ed25519) preferred for JWT signing due to deterministic signatures and faster verification.

### Hash Functions

| Status          | Algorithm      | Usage                                     |
| --------------- | -------------- | ----------------------------------------- |
| **Minimum**     | SHA-256        | All hashing requirements                  |
| **Recommended** | SHA-3 (Keccak) | New designs, HMAC construction            |
| **Prohibited**  | MD5, SHA-1     | Must not be used for any security purpose |

**Rationale:** SHA-256 remains secure for all current purposes. SHA-3 provides algorithmic diversity as a hedge against SHA-2 family breaks.

### Password Hashing

| Status         | Algorithm                           | Parameters                                  |
| -------------- | ----------------------------------- | ------------------------------------------- |
| **Preferred**  | Argon2id                            | Memory: 64MB, iterations: 3, parallelism: 4 |
| **Fallback**   | bcrypt                              | Cost factor: 12 (OWASP 2023)                |
| **Prohibited** | MD5, SHA-1, plain SHA-256, unsalted | --                                          |

**Rationale:** Argon2id is the winner of the Password Hashing Competition and is recommended by OWASP. It is memory-hard, making GPU/ASIC attacks expensive. bcrypt is acceptable where Argon2 libraries are unavailable.

### Random Number Generation

| Runtime | API                          | Notes                        |
| ------- | ---------------------------- | ---------------------------- |
| Go      | `crypto/rand.Read`           | CSPRNG, backed by OS entropy |
| Node.js | `crypto.randomBytes`         | CSPRNG, backed by OpenSSL    |
| Python  | `secrets.token_bytes`        | CSPRNG, backed by OS         |
| Java    | `java.security.SecureRandom` | Not `java.util.Random`       |
| Rust    | `rand::rngs::OsRng`          | CSPRNG, backed by OS         |

**Prohibited:** `java.util.Random`, `Math.random()`, `Math.random` in JavaScript, any PRNG not explicitly designed for cryptographic use.

---

## TLS Configuration

| Requirement            | Value                                                |
| ---------------------- | ---------------------------------------------------- |
| Minimum version        | TLS 1.3 (TLS 1.2 permitted only with CSO waiver)     |
| Approved cipher suites | TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256 |
| Key exchange           | X25519 (preferred) or P-256                          |
| Certificate type       | ECDSA P-256 (preferred) or RSA 4096-bit              |
| Certificate management | ACME automated renewal (Let's Encrypt or cloud CA)   |

---

## Crypto Algorithm Deprecation Policy

| Phase                | Timeline | Action                                                               |
| -------------------- | -------- | -------------------------------------------------------------------- |
| **Announcement**     | Day 0    | ADR updated, all backend leads notified                              |
| **Migration Plan**   | Day 30   | Each backend lead submits migration plan                             |
| **Migration Window** | 6 months | Deprecated algorithms replaced in all codebases                      |
| **Enforcement**      | Month 7  | CI/CD scans flag any remaining deprecated usage as P1                |
| **Quarterly Review** | Ongoing  | Approved algorithms reviewed against NIST, OWASP, industry standards |

---

## Library Selection Per Runtime

| Runtime | Library                  | Version      | Notes                                              |
| ------- | ------------------------ | ------------ | -------------------------------------------------- |
| Go      | `crypto/*` (stdlib)      | Go 1.21+     | Well-audited, maintained by Go team                |
| Go      | `golang.org/x/crypto`    | Latest       | Supplemental (Argon2, bcrypt, ed25519)             |
| Node.js | `crypto` (stdlib)        | Node 20+     | OpenSSL-backed, sufficient for most needs          |
| Node.js | `@noble/curves`          | Latest       | Pure-JS elliptic curve crypto (Ed25519, secp256k1) |
| Python  | `cryptography`           | Latest       | Well-audited, PyCA maintained                      |
| Python  | `hashlib` (stdlib)       | Python 3.10+ | SHA-2/SHA-3, HMAC                                  |
| Java    | Bouncy Castle            | Latest       | Comprehensive crypto provider                      |
| Java    | `java.security` (stdlib) | Java 17+     | Baseline crypto, JSSE for TLS                      |

**Implementation requirements:**

- No hardcoded encryption keys in source code, config files, or environment variables
- All encrypted data must include algorithm identifier (for future migration)
- Key rotation strategy defined per data classification
- Encrypt-then-MAC pattern for any custom authenticated encryption (prefer GCM to avoid this)
- API keys stored as bcrypt-hashed values in database; never stored plaintext

---

## STRIDE Threat Reference

| STRIDE Category            | Threat                                          | Mitigation                                                         |
| -------------------------- | ----------------------------------------------- | ------------------------------------------------------------------ |
| **Spoofing**               | Cryptographic key substitution                  | Algorithm enforcement, key authentication via signatures           |
| **Tampering**              | Ciphertext modification without detection       | GCM authenticated encryption (detects modification)                |
| **Information Disclosure** | Weak algorithms enabling decryption             | Approved algorithm list, deprecation enforcement                   |
| **Elevation of Privilege** | Weak key derivation enabling brute force        | Argon2id memory-hard KDF                                           |
| **Repudiation**            | Unsigned messages enabling denial               | ECDSA/EdDSA signatures on audit-critical operations                |
| **Denial of Service**      | Crypto operations consuming excessive resources | Rate limiting on crypto-heavy endpoints, Argon2id parameter tuning |

---

## Alternatives Considered

| Alternative                               | Why Rejected                                                                           |
| ----------------------------------------- | -------------------------------------------------------------------------------------- |
| Custom cryptographic implementations      | Implementation risk extremely high -- even experts make mistakes                       |
| Third-party crypto wrappers (non-audited) | Supply chain risk; many wrappers have vulnerabilities in their abstractions            |
| No standardization (team choice)          | Creates audit nightmare, inconsistent security posture, impossible to deprecate        |
| libsodium / NaCl                          | Evaluated -- excellent library but adds dependency complexity across multiple runtimes |

---

## Compliance

**This decision is locked at Stage 3 gate approval.** Any deviation requires a new ADR and Stage 3 re-entry with CSO approval.

| Enforcement Layer   | Mechanism                                                           |
| ------------------- | ------------------------------------------------------------------- |
| Policy              | Stage 3 ADR lock                                                    |
| SAST                | Automated detection of prohibited algorithms (Semgrep/CodeQL rules) |
| Dependency Scanning | Library version pinning verified against TSD                        |
| Code Review         | Security team reviews crypto usage during Stage 6 Tier 1            |
| Stage 8 Integrity   | Anti-trim verification includes crypto algorithm compliance         |

**Non-compliance classification:** Use of prohibited algorithms is a **P0 defect** (security breach risk). Use of deprecated algorithms outside migration window is a **P1 defect**.
