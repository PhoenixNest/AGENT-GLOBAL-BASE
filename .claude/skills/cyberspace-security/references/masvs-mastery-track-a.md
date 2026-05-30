---
name: masvs-mastery-track-a
description: OWASP MASVS Track A (MASVS-STORAGE, MASVS-CRYPTO, MASVS-AUTH) mastery — audit mobile applications for data-at-rest security, cryptographic implementation correctness, and authentication control adequacy, producing findings that map directly to MASVS control IDs.
version: "1.0.0"
---

# MASVS Mastery Track A

| Competency       | Description                                                           | Quality Criteria                                                                                                                              |
| ---------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| MASVS-STORAGE    | Secure data storage on Android and iOS — SharedPreferences, Keychain  | Identifies plaintext storage of sensitive data; verifies KeyStore/Keychain usage; flags world-readable files and unencrypted SQLite databases |
| MASVS-CRYPTO     | Cryptographic API usage review — cipher selection, key management     | Detects deprecated algorithms (ECB mode, MD5, SHA-1); verifies IV randomness; confirms key derivation uses PBKDF2/Argon2 with adequate rounds |
| MASVS-AUTH       | Authentication control review — session tokens, biometric integration | Validates token expiry, secure storage of credentials; verifies biometric confirmation uses `setUserAuthenticationRequired(true)` on Android  |
| Findings Mapping | MASVS control ID citation in security findings                        | Every finding includes the exact MASVS control ID, severity (Critical/High/Medium/Low), and a concrete remediation recommendation             |

## Execution Guidance

### MASVS-STORAGE Assessment

Review data storage paths for sensitive information (PII, credentials, session tokens, cryptographic keys):

- **Android:** Check `SharedPreferences` for plaintext secrets; verify `EncryptedSharedPreferences` is used for sensitive keys; audit `Room`/SQLite databases for encryption (SQLCipher); check for world-readable file permissions (`MODE_WORLD_READABLE`).
- **iOS:** Confirm sensitive data uses `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` or stricter; verify Keychain access groups are scoped correctly; check `UserDefaults` for accidental PII storage.

### MASVS-CRYPTO Assessment

| Check          | Pass Condition                                |
| -------------- | --------------------------------------------- |
| Cipher mode    | AES-GCM or AES-CBC with PKCS7 (no ECB)        |
| Key length     | AES-256 minimum for data at rest              |
| IV generation  | `SecureRandom` or OS CSPRNG — never hardcoded |
| Hash functions | SHA-256 or SHA-3 (MD5 and SHA-1 are findings) |
| Key derivation | PBKDF2 (≥ 310,000 iterations) or Argon2id     |

### MASVS-AUTH Assessment

Verify that session management controls meet MASVS L1/L2 thresholds:

- Token lifetime ≤ 15 minutes for sensitive operations; refresh tokens ≤ 7 days.
- Biometric authentication requires `setUserAuthenticationRequired(true)` and invalidates keys on new biometric enrollment.
- Password-based authentication must enforce minimum length ≥ 12 and check against breach databases (HaveIBeenPwned API).
