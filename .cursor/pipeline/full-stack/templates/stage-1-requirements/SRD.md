# Security Requirements Document (SRD)

**Project:** [Project Name]
**Version:** v1
**Author:** CSO (Dr. Sarah Chen)
**Date:** YYYY-MM-DD
**Status:** Draft | Under Review | Approved
**Paired Artifact:** PRD v1

---

## 1. Security Context

Brief description of the product's security-relevant characteristics: data sensitivity, threat landscape, regulatory requirements.

---

## 2. Privacy Requirements

| Requirement             | Detail                                          |
| ----------------------- | ----------------------------------------------- |
| Data classification     | [Public / Internal / Confidential / Restricted] |
| PII handled             | [Yes/No — list types]                           |
| GDPR/CCPA applicability | [Yes/No — jurisdictions]                        |
| Data retention policy   | [Duration and deletion requirements]            |

---

## 3. Authentication & Authorization

| Requirement                 | Detail                               |
| --------------------------- | ------------------------------------ |
| Authentication method       | [OAuth 2.0 / Biometric / PIN / etc.] |
| Session management          | [Token lifetime, refresh strategy]   |
| Authorization model         | [RBAC / ABAC / etc.]                 |
| Multi-factor authentication | [Required for which flows]           |

---

## 4. Encryption Requirements

| Data State      | Requirement                            |
| --------------- | -------------------------------------- |
| Data at rest    | [Encryption algorithm, key management] |
| Data in transit | [TLS version, cipher suites]           |
| Key storage     | [iOS Keychain / Android Keystore]      |

---

## 5. Platform-Specific Security Requirements

### 5.1 iOS

| Requirement              | Detail                                              |
| ------------------------ | --------------------------------------------------- |
| App Transport Security   | ATS enabled, no exception without CSO approval      |
| Keychain                 | `kSecAttrAccessibleWhenUnlocked` for sensitive data |
| Jailbreak detection      | [Required / Not required — implementation approach] |
| Biometric authentication | FaceID/TouchID with secure fallback                 |

### 5.2 Android

| Requirement                | Detail                                              |
| -------------------------- | --------------------------------------------------- |
| SafetyNet / Play Integrity | [Required API level, attestation type]              |
| Keystore                   | Hardware-backed where available                     |
| Root detection             | [Required / Not required — implementation approach] |
| Biometric authentication   | BiometricPrompt with CryptoObject                   |

---

## 6. Certificate Pinning

| Requirement          | Detail                                    |
| -------------------- | ----------------------------------------- |
| Pinning required     | [Yes/No — for which endpoints]            |
| Pin type             | [SPKI / Certificate / Public Key]         |
| Backup pins          | [Minimum 2, rotation strategy]            |
| Pin update mechanism | [How pins are updated without app update] |

---

## 7. Network Security

| Requirement        | Detail                                |
| ------------------ | ------------------------------------- |
| API authentication | [Bearer token, mutual TLS, etc.]      |
| Request signing    | [HMAC, timestamp, nonce requirements] |
| Rate limiting      | [Server-side and client-side]         |

---

## 8. OWASP MASVS Compliance

| MASVS Level                | Target                          | Notes          |
| -------------------------- | ------------------------------- | -------------- |
| Track A (Baseline)         | Required                        | All categories |
| Track B (Defense-in-Depth) | [Required for which categories] |                |

| Category         | Status                                | Notes |
| ---------------- | ------------------------------------- | ----- |
| MASVS-STORAGE    | [Compliant / Partial / Non-compliant] |       |
| MASVS-CRYPTO     | [Compliant / Partial / Non-compliant] |       |
| MASVS-AUTH       | [Compliant / Partial / Non-compliant] |       |
| MASVS-NETWORK    | [Compliant / Partial / Non-compliant] |       |
| MASVS-PLATFORM   | [Compliant / Partial / Non-compliant] |       |
| MASVS-RESILIENCE | [Compliant / Partial / Non-compliant] |       |

---

## 9. Supply Chain Security

| Requirement             | Detail                                                                                                                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Third-party SDK vetting | [Security review required for each SDK]                                                                                                                                                                       |
| Dependency scanning     | [Automated per PR, SAST integration]                                                                                                                                                                          |
| SBOM requirement        | [CycloneDX generated per build]                                                                                                                                                                               |
| SBOM consumption policy | Automated build gate: fail on any critical or high CVE in SBOM. Weekly manual review of medium/low findings by Security Engineer (Li Wei Chen). New dependencies require security team approval before merge. |

---

## 9.1 Deep Linking Security

| Requirement                           | Detail                                                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Universal Links / App Links           | Validate all incoming deep links against allowlist. Reject unregistered schemes.                 |
| Deep link parameter validation        | Sanitize and validate all parameters. Never trust data from deep link payloads.                  |
| OAuth redirect URI validation         | Strict allowlist matching. Reject redirects to unregistered URIs.                                |
| Intent hijacking prevention (Android) | Use explicit intents for sensitive operations. Set `android:exported="false"` where appropriate. |

---

## 9.2 Data Leakage Prevention

The following controls prevent sensitive data from leaking through non-storage channels:

| Control               | Platform | Implementation                                                                               |
| --------------------- | -------- | -------------------------------------------------------------------------------------------- |
| Clipboard exclusion   | Android  | Use `FLAG_SENSITIVE_CONTENT` on `ClipData` for sensitive clipboard operations                |
| Screenshot prevention | Android  | `FLAG_SECURE` on screens showing sensitive data (prevents screenshots + recents thumbnail)   |
| App switcher masking  | iOS      | Snapshot masking in `sceneDidEnterBackground` to prevent sensitive data in app switcher      |
| Autocorrect exclusion | iOS      | `UITextAutocorrectionTypeNo` on `UITextField` for sensitive inputs (passwords, PINs, tokens) |

> **Implementation details:** See ADR-SECURITY-STORAGE §Data Leakage Prevention for platform-specific implementation guidance.

---

## 9.3 Runtime Application Self-Protection (RASP)

| Requirement               | Detail                                                                                                        |
| ------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Anti-tampering            | Detect code signature modification, resource modification, and runtime hooking (Frida, Cydia Substrate).      |
| Runtime hooking detection | Detect common hooking frameworks (Frida, Cydia Substrate, Xposed, Magisk modules) at runtime.                 |
| Debugger detection        | Detect attached debuggers at runtime and terminate or degrade gracefully.                                     |
| Emulator detection        | Detect execution in emulator/simulator environments and flag for server-side risk scoring.                    |
| Response to detection     | On detection: (1) log event to server, (2) degrade sensitive functionality, (3) optionally terminate session. |

**MASVS Reference:** MASVS-RESILIENCE R4 (Runtime Integrity Checks)

---

## 10. Security Controls (Stage 8 Anti-Trim Clause)

The following security controls are **mandatory**. Removal, disabling, or weakening of any control is classified as a **P0 defect**:

- [ ] Encryption at rest and in transit
- [ ] Certificate pinning (if specified above)
- [ ] Root/jailbreak detection (if specified above)
- [ ] Biometric authentication (if specified above)
- [ ] Session token security
- [ ] Secure storage mechanisms (Keychain / Keystore)
- [ ] Code obfuscation

---

**Approved by CSO (Dr. Sarah Chen) on YYYY-MM-DD**
**Paired artifact: PRD v1**
