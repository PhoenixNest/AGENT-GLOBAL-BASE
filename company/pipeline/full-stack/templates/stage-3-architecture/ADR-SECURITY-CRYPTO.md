# ADR-NNN: Cryptographic Standard Selection

| Metadata          | Value                                          |
| ----------------- | ---------------------------------------------- |
| **ADR Number**    | ADR-NNN                                        |
| **Title**         | Cryptographic Standard Selection               |
| **Status**        | Proposed                                       |
| **Decision Date** | YYYY-MM-DD                                     |
| **Authors**       | Security Architect (Natalia Petrova)           |
| **Reviewers**     | CSO (Dr. Sarah Chen), CTO (Dr. Kenji Nakamura) |
| **Stage**         | 3 — Architecture                               |
| **Category**      | Security / Cryptography                        |

---

## Context

Without standardized cryptographic standards, each platform team may independently select algorithms, libraries, and key sizes — creating an inconsistent security posture that complicates auditing, increases vulnerability surface, and makes incident response difficult. This ADR establishes the authoritative cryptographic standard for all platforms.

---

## Decision

### Symmetric Encryption

| Status         | Algorithm                | Key Size | Mode | Usage                                          |
| -------------- | ------------------------ | -------- | ---- | ---------------------------------------------- |
| **Approved**   | AES                      | 256-bit  | GCM  | All new development (authenticated encryption) |
| **Deprecated** | AES                      | 256-bit  | CBC  | Existing code only — migrate within 6 months   |
| **Prohibited** | DES, 3DES, RC4, Blowfish | —        | —    | Must not be used under any circumstance        |

**Rationale:** AES-256-GCM provides authenticated encryption (confidentiality + integrity) in a single operation. CBC requires separate MAC, creating implementation complexity and potential for encrypt-then-MAC ordering mistakes.

### Asymmetric Encryption

| Use Case                 | Algorithm | Parameters                      |
| ------------------------ | --------- | ------------------------------- |
| Key exchange             | ECDH      | Curve25519 (preferred) or P-256 |
| Digital signatures       | ECDSA     | P-256 (secp256r1)               |
| High-security signatures | ECDSA     | P-384 (secp384r1)               |
| RSA fallback             | RSA       | 4096-bit minimum, OAEP padding  |

**Rationale:** ECC provides equivalent security to RSA at much smaller key sizes (P-256 ≈ RSA-3072). Curve25519 is preferred for ECDH due to implementation simplicity and resistance to side-channel attacks.

### Hash Functions

| Status          | Algorithm      | Usage                                     |
| --------------- | -------------- | ----------------------------------------- |
| **Minimum**     | SHA-256        | All hashing requirements                  |
| **Recommended** | SHA-3 (Keccak) | New designs, HMAC construction            |
| **Prohibited**  | MD5, SHA-1     | Must not be used for any security purpose |

**Rationale:** SHA-256 remains secure for all current purposes. SHA-3 provides algorithmic diversity as a hedge against SHA-2 family breaks.

### Key Derivation

| Status         | Algorithm                             | Parameters                                  |
| -------------- | ------------------------------------- | ------------------------------------------- |
| **Preferred**  | Argon2id                              | Memory: 64MB, iterations: 3, parallelism: 4 |
| **Fallback**   | PBKDF2-SHA256                         | Iterations: 600,000 (OWASP 2023)            |
| **Prohibited** | MD5-based, SHA-1-based, plain SHA-256 | —                                           |

**Rationale:** Argon2id is the winner of the Password Hashing Competition and is recommended by OWASP. It is memory-hard, making GPU/ASIC attacks expensive. PBKDF2 is acceptable where Argon2 libraries are unavailable.

### Random Number Generation

| Platform       | API                          | Notes                                |
| -------------- | ---------------------------- | ------------------------------------ |
| Web Frontend   | `crypto.getRandomValues()`   | Web Crypto API, browser CSPRNG       |
| Backend (Go)   | `crypto/rand.Read()`         | OS-level CSPRNG                      |
| Backend (Node) | `crypto.randomBytes()`       | OpenSSL-backed CSPRNG                |
| iOS            | `SecRandomCopyBytes`         | CSPRNG, backed by kernel entropy     |
| Android        | `java.security.SecureRandom` | Not `java.util.Random`               |
| KMP            | Platform adapter             | Each platform provides native CSPRNG |
| Flutter        | Platform channel             | Delegate to native CSPRNG            |

**Prohibited:** `java.util.Random`, `arc4random()` (not CSPRNG), `Math.random()`, `crypto.pseudoRandomBytes` (Node.js, not CSPRNG), `window.crypto.getRandomValues` polyfills, any PRNG not explicitly designed for cryptographic use.

---

## Crypto Algorithm Deprecation Policy

| Phase                | Timeline | Action                                                               |
| -------------------- | -------- | -------------------------------------------------------------------- |
| **Announcement**     | Day 0    | ADR updated, all platform leads notified                             |
| **Migration Plan**   | Day 30   | Each platform lead submits migration plan                            |
| **Migration Window** | 6 months | Deprecated algorithms replaced in all codebases                      |
| **Enforcement**      | Month 7  | CI/CD scans flag any remaining deprecated usage as P1                |
| **Quarterly Review** | Ongoing  | Approved algorithms reviewed against NIST, OWASP, industry standards |

---

## Library Selection Per Platform

| Platform           | Library              | Version  | Notes                                                                      |
| ------------------ | -------------------- | -------- | -------------------------------------------------------------------------- |
| Web Frontend       | Web Crypto API       | Native   | Browser-native; `subtle.crypto` for AES-GCM, ECDH, ECDSA                   |
| Web Frontend       | libsodium-wrappers   | Latest   | For argon2id password hashing (via WASM)                                   |
| Backend (Go)       | `crypto/*` stdlib    | Go 1.21+ | Built-in; AES-GCM, ECDSA, ECDH, SHA-256 all available                      |
| Backend (Node)     | Node.js `crypto`     | LTS      | Built-in; AES-GCM, ECDH, ECDSA available                                   |
| Backend (Node)     | `argon2` npm package | Latest   | For password hashing (native bindings to PHC winner)                       |
| iOS                | CryptoKit            | iOS 13+  | Apple's modern crypto framework                                            |
| iOS (legacy)       | CommonCrypto         | —        | Use only for algorithms not in CryptoKit                                   |
| Android            | Google Tink          | Latest   | Multi-language, well-audited                                               |
| Android (fallback) | BouncyCastle         | Latest   | Use if Tink incompatible with existing code                                |
| KMP                | Platform adapter     | —        | Shared module defines interface; platforms implement with native libraries |
| Flutter            | Platform channel     | —        | All crypto in native code — never implement in pure Dart                   |

**Implementation requirements:**

- No hardcoded encryption keys in source code, resources, or build scripts
- All encrypted data must include algorithm identifier (for future migration)
- Key rotation strategy defined per data classification (see ADR-SECURITY-STORAGE)
- Encrypt-then-MAC pattern for any custom authenticated encryption (prefer GCM to avoid this)

---

## STRIDE Threat Reference

| STRIDE Category            | Threat                                          | Mitigation                                                         |
| -------------------------- | ----------------------------------------------- | ------------------------------------------------------------------ |
| **Spoofing**               | Cryptographic key substitution                  | Algorithm enforcement, key authentication via signatures           |
| **Tampering**              | Ciphertext modification without detection       | GCM authenticated encryption (detects modification)                |
| **Information Disclosure** | Weak algorithms enabling decryption             | Approved algorithm list, deprecation enforcement                   |
| **Elevation of Privilege** | Weak key derivation enabling brute force        | Argon2id memory-hard KDF                                           |
| **Repudiation**            | Unsigned messages enabling denial               | ECDSA signatures on audit-critical operations                      |
| **Denial of Service**      | Crypto operations consuming excessive resources | Rate limiting on crypto-heavy endpoints, Argon2id parameter tuning |

---

## MASVS Compliance

| MASVS ID       | Requirement                                                             | Compliance Evidence                                      |
| -------------- | ----------------------------------------------------------------------- | -------------------------------------------------------- |
| MASVS-CRYPTO-1 | App does not rely on broken or deprecated cryptographic algorithms      | Approved algorithm list, deprecation policy, CI/CD scans |
| MASVS-CRYPTO-2 | App uses cryptographic algorithms that are industry-tested and approved | Algorithm selection rationale in this ADR                |

---

## Alternatives Considered

| Alternative                               | Why Rejected                                                                                |
| ----------------------------------------- | ------------------------------------------------------------------------------------------- |
| Custom cryptographic implementations      | Implementation risk extremely high — even experts make mistakes                             |
| Third-party crypto wrappers (non-audited) | Supply chain risk; many wrappers have vulnerabilities in their abstractions                 |
| No standardization (team choice)          | Creates audit nightmare, inconsistent security posture, impossible to deprecate             |
| libsodium / NaCl                          | Evaluated — excellent library but not available natively on iOS; adds dependency complexity |
| Web: crypto-js                            | Not maintained; Web Crypto API is native and more secure                                    |
| Backend: third-party crypto libs          | Go stdlib `crypto/*` is complete and audited; no need for external dependencies             |

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
