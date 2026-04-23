# ADR-NNN: Secure Storage Mechanisms

| Metadata          | Value                                          |
| ----------------- | ---------------------------------------------- |
| **ADR Number**    | ADR-NNN                                        |
| **Title**         | Secure Storage Mechanisms                      |
| **Status**        | Proposed                                       |
| **Decision Date** | YYYY-MM-DD                                     |
| **Authors**       | Security Architect (Natalia Petrova)           |
| **Reviewers**     | CSO (Dr. Sarah Chen), CTO (Dr. Kenji Nakamura) |
| **Stage**         | 3 — Architecture                               |
| **Category**      | Security / Data Storage                        |

---

## Context

Need for platform-appropriate secure storage of sensitive data including credentials, tokens, cryptographic keys, and PII. Each mobile platform has different secure storage APIs with different security guarantees.

## Decision

### iOS Storage

- **Keychain** with `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` for highest sensitivity items (cryptographic keys, biometric tokens)
- **Secure Enclave** (`kSecAttrSecureEnclave`) for biometric-protected keys — requires iOS 9+ with Touch ID / Face ID device
- **Encrypted UserDefaults** for low-sensitivity config (not for secrets)

### Android Storage

- **Keystore** with hardware-backed storage (StrongBox on API 28+) for cryptographic keys
- **EncryptedSharedPreferences** (Jetpack Security) for general secrets, tokens, cached credentials
- **SharedPreferences MUST NOT** be used for sensitive data without encryption wrapper

### KMP Shared Module

- **Platform adapter pattern**: shared module defines `SecureStorage` interface with methods for store, retrieve, delete
- Each platform implements with native secure storage (Keychain on iOS, Keystore on Android)
- Shared module must **NOT** store secrets directly

### Flutter

- **flutter_secure_storage** plugin wrapping Keychain/Keystore
- Version pinning required in `pubspec.yaml`
- All security operations via platform channels — never store secrets in Dart isolates or memory

## Data Classification Matrix

| Classification                         | Examples                                | iOS Storage                   | Android Storage                    |
| -------------------------------------- | --------------------------------------- | ----------------------------- | ---------------------------------- |
| Critical (crypto keys, biometric refs) | Private keys, PIN refs                  | Secure Enclave                | StrongBox Keystore                 |
| High (credentials, tokens)             | Auth tokens, session cookies, passwords | Keychain (passcode-only)      | EncryptedSharedPreferences         |
| Medium (PII, preferences)              | User email, display name                | Keychain (after first unlock) | EncryptedSharedPreferences         |
| Low (app config)                       | Theme preference, cached data           | UserDefaults                  | SharedPreferences (unencrypted OK) |

## Prohibited Storage

- **Plaintext passwords** — always hash with Argon2id (see ADR-SECURITY-CRYPTO)
- **Raw credit card numbers** — tokenize via payment provider
- **Encryption keys in source code, resources, or build scripts**
- **Secrets in UserDefaults or unencrypted SharedPreferences**

## Key Management Lifecycle

- **Generation**: platform CSPRNG (`SecRandomCopyBytes` / `SecureRandom`)
- **Rotation**: critical keys rotated every 90 days, tokens rotated on session refresh
- **Destruction**: Keychain item delete with `kSecUseDataProtectionKeychain`, Keystore key deletion

## Backup Behavior

- Keychain items excluded from iCloud backup (`kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` items not backed up)
- Keystore items excluded from Google Auto Backup (hardware-backed keys never leave device)
- Auto Backup rules configured in `AndroidManifest.xml` and iOS `Info.plist`

## Data Leakage Prevention

- **iOS**: `UITextField` autocorrect disabled for sensitive inputs (`UITextAutocorrectionTypeNo`)
- **Android**: clipboard exclusion — use `FLAG_SENSITIVE_CONTENT` for `ClipData`
- **Android**: `FLAG_SECURE` on screens showing sensitive data (prevents screenshots and recents thumbnail)
- **iOS**: snapshot masking in `sceneDidEnterBackground` to prevent sensitive data in app switcher

## STRIDE Threat Reference

| STRIDE Category            | Threat                                                                                       | Mitigation                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Spoofing**               | Malicious app impersonating legitimate app to access Keychain/Keystore items                 | Access group validation, Keychain/Keystore access control lists                              |
| **Tampering**              | Backup file modification to inject malicious data or alter stored credentials                | Hardware-backed storage, encryption at rest, backup exclusion for sensitive items            |
| **Repudiation**            | User denies performing an action that required stored credential verification                | Audit logging of Keychain/Keystore access events with timestamps                             |
| **Information Disclosure** | Data-at-rest extraction from device storage via physical access or malware                   | Platform-native secure storage (Keychain/Keystore), hardware-backed encryption, DLP controls |
| **Denial of Service**      | Keychain/Keystore locked out (passcode change, device reset) rendering app unusable          | Graceful degradation: prompt user to re-authenticate and re-provision credentials            |
| **Elevation of Privilege** | Exploiting insecure storage API to access another app's credentials or higher-privilege data | Sandboxed storage, per-app Keychain/Keystore isolation, no cross-app data sharing            |

## MASVS Compliance

| MASVS ID        | Requirement                                                                  | Compliance Evidence                                 |
| --------------- | ---------------------------------------------------------------------------- | --------------------------------------------------- |
| MASVS-STORAGE-1 | App securely stores all sensitive data using platform-appropriate mechanisms | Platform adapter pattern, Keychain/Keystore usage   |
| MASVS-STORAGE-2 | App prevents insecure data storage (no plaintext secrets)                    | Data classification matrix, prohibited storage list |

## Alternatives Considered

| Alternative                                | Assessment                                                                    | Decision     |
| ------------------------------------------ | ----------------------------------------------------------------------------- | ------------ |
| Unencrypted SharedPreferences/UserDefaults | No confidentiality guarantees                                                 | **Rejected** |
| SQLCipher encrypted SQLite                 | Viable but overkill for most use cases, reserved for large encrypted datasets | **Deferred** |
| Custom file encryption                     | Platform-native storage is more auditable and battle-tested                   | **Rejected** |

## Compliance

**This decision is locked at Stage 3 gate approval.** Any deviation requires a new ADR and Stage 3 re-entry. Switching storage mechanisms after Stage 3 requires a full stage rollback (Stage 3 re-entry, ADR re-authorship, Implementation Plan re-baseline).

| Enforcement Layer | Mechanism                                                               |
| ----------------- | ----------------------------------------------------------------------- |
| Policy            | Stage 3 ADR lock                                                        |
| CI/CD             | Secure storage API usage verification in build                          |
| Code Review       | Security team reviews storage implementation during Stage 6 Tier 1      |
| Stage 8 Integrity | Anti-trim verification includes secure storage presence and correctness |

**Non-compliance classification:** Use of prohibited storage mechanisms is a **P0 defect** (security breach risk).
