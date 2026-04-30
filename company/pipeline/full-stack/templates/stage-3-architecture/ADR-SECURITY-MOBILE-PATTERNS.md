# ADR: Mobile Security Patterns

**Project:** [Project Name]
**ADR ID:** ADR-[NNN]
**Status:** Proposed | Accepted | Superseded
**Author:** CIO (Dr. Priya Mehta) + CSO (Dr. Sarah Chen)
**Date:** YYYY-MM-DD
**Pipeline:** Full-Stack Cross-Platform
**Paired With:** ADR-SECURITY-CROSS-PLATFORM.md, ADR-SECURITY-CRYPTO.md

---

## Context

The full-stack application includes native mobile surfaces (iOS and/or Android per the Multi-Platform Strategy ADR). Mobile-specific security threats — insecure storage, certificate pinning bypass, jailbreak/root detection evasion, reverse engineering, and platform-specific API abuse — require a dedicated set of controls beyond the shared cryptography and cross-platform auth ADRs. These patterns apply exclusively to the mobile track (FS-MOB).

This ADR is a mandatory Stage 3 deliverable for all full-stack projects that include a mobile surface.

---

## Decision

### 1. Secure Storage (Platform Keychain / Keystore)

| Platform | Data Type                    | Storage Mechanism                             | Accessibility                                           | Notes                            |
| -------- | ---------------------------- | --------------------------------------------- | ------------------------------------------------------- | -------------------------------- |
| iOS      | Auth tokens, encryption keys | Keychain (`SecItemAdd`)                       | `kSecAttrAccessibleWhenUnlocked`                        | Never `kSecAttrAccessibleAlways` |
| iOS      | Biometric-protected secrets  | Keychain with LocalAuth                       | `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`          | Device-bound                     |
| Android  | Auth tokens, encryption keys | EncryptedSharedPreferences (Jetpack Security) | `AES256_GCM`                                            | Hardware-backed where available  |
| Android  | Long-term secrets            | Android Keystore                              | `setUserAuthenticationRequired(true)` for sensitive ops |                                  |

### 2. Certificate Pinning

| Decision                   | Detail                                                         |
| -------------------------- | -------------------------------------------------------------- |
| **Pinning required**       | [Yes / No — for which API endpoints]                           |
| **Pin type**               | [SPKI hash (preferred over leaf cert)]                         |
| **Primary pin**            | [SHA-256 hash of server's current SPKI]                        |
| **Backup pin(s)**          | [Minimum 2 backup pins from CA chain]                          |
| **Pin update mechanism**   | [Over-the-air config (remote fetch) / App update required]     |
| **iOS implementation**     | [TrustKit / URLSession challenge delegate / Network.framework] |
| **Android implementation** | [OkHttp CertificatePinner / Network Security Config XML]       |
| **Bypass detection**       | [Detect SSL Kill Switch / Frida SSL hooks at runtime]          |
| **Pin rotation cadence**   | [90 days / triggered by cert expiry ≥ 60 days ahead]           |

### 3. Root / Jailbreak Detection

| Decision                     | Detail                                                                    |
| ---------------------------- | ------------------------------------------------------------------------- |
| **Detection required**       | [Yes / No — required for apps handling financial/health data]             |
| **iOS approach**             | [Cydia path check + dyld_shared_cache anomaly + `fork()` return check]    |
| **Android approach**         | [Play Integrity API (replacing SafetyNet) + su binary check + prop check] |
| **Response to detection**    | [Degrade functionality / Warn user / Block access — per risk model]       |
| **Server-side risk scoring** | [Pass detection signal to backend for risk-adaptive auth]                 |
| **False positive tolerance** | [Define acceptable false positive rate for custom ROMs]                   |

### 4. App Attestation / Integrity

| Platform | Mechanism                            | Decision                                                            |
| -------- | ------------------------------------ | ------------------------------------------------------------------- |
| iOS      | App Attest API (DeviceCheck)         | [Required / Not required]                                           |
| Android  | Play Integrity API                   | [Required — replaces SafetyNet]                                     |
| Both     | Server-side attestation verification | [Verify attestation token server-side before high-value operations] |

### 5. Anti-Tampering and Obfuscation

| Control                           | Platform | Implementation                                     | Notes                                |
| --------------------------------- | -------- | -------------------------------------------------- | ------------------------------------ |
| Code obfuscation                  | Android  | [R8 full mode / ProGuard]                          | iOS Swift binary obfuscation limited |
| Resource obfuscation              | Android  | [Resource shrinking in R8]                         |                                      |
| Debug detection                   | Both     | [Check `BuildConfig.DEBUG` + ptrace anti-attach]   |                                      |
| Integrity hash verification       | Both     | [Runtime signature check against known-good hash]  |                                      |
| Dynamic instrumentation detection | Both     | [Detect Frida, Cydia Substrate, Xposed at runtime] |                                      |

### 6. Data Leakage Prevention

| Control                               | Platform | Implementation                                                           |
| ------------------------------------- | -------- | ------------------------------------------------------------------------ |
| Screenshot / screen recording blocked | Both     | Android `FLAG_SECURE`; iOS snapshot masking in `sceneDidEnterBackground` |
| Clipboard exclusion                   | Android  | `FLAG_SENSITIVE_CONTENT` on ClipData for sensitive content               |
| Autocorrect exclusion                 | iOS      | `UITextAutocorrectionTypeNo` on sensitive text fields                    |
| Background app state masking          | Both     | Blank/logo overlay before app enters background                          |
| Log scrubbing                         | Both     | No PII in `NSLog` / `Log.d`; SAST rule enforced in CI                    |

### 7. Deep Link Security

| Control                       | Platform | Decision                                                                  |
| ----------------------------- | -------- | ------------------------------------------------------------------------- |
| Universal Links / App Links   | Both     | All deep links validated against allowlist; reject unknown schemes        |
| Parameter sanitisation        | Both     | Sanitise and validate all deep link parameters before use                 |
| OAuth redirect URI validation | Both     | Strict allowlist — reject unregistered redirect URIs                      |
| Intent hijacking prevention   | Android  | Use explicit intents for sensitive operations; `android:exported="false"` |

### 8. Network Security Configuration

| Platform | Configuration                 | Decision                                                                      |
| -------- | ----------------------------- | ----------------------------------------------------------------------------- |
| Android  | `network_security_config.xml` | `cleartextTrafficPermitted="false"`; pin domains listed                       |
| iOS      | App Transport Security        | All exceptions require CSO written justification; no `NSAllowsArbitraryLoads` |

---

## Rationale

[Explain key decisions — e.g., why SPKI pinning over leaf cert, why Play Integrity API over custom root detection, which data warrants hardware-backed keystore vs. software, etc.]

---

## Trade-offs

| Benefit                                           | Cost                                                  |
| ------------------------------------------------- | ----------------------------------------------------- |
| Certificate pinning blocks MITM on API calls      | Pin rotation requires coordinated deployment          |
| Hardware Keystore protects key extraction         | No fallback if hardware not available (older devices) |
| Play Integrity / App Attest blocks scripted abuse | Requires network; adds attestation latency            |

---

## MASVS Alignment

| MASVS Category   | Covered By                                             |
| ---------------- | ------------------------------------------------------ |
| MASVS-STORAGE    | §1 Secure Storage                                      |
| MASVS-CRYPTO     | ADR-SECURITY-CRYPTO.md                                 |
| MASVS-AUTH       | ADR-SECURITY-CROSS-PLATFORM.md §Unified Auth           |
| MASVS-NETWORK    | §2 Certificate Pinning + §8 Network Security Config    |
| MASVS-PLATFORM   | §6 Data Leakage + §7 Deep Link Security                |
| MASVS-RESILIENCE | §3 Root Detection + §4 Attestation + §5 Anti-Tampering |

---

## Supersession Policy

Changes to any security pattern after Stage 3 approval require CSO written approval and a new superseding ADR. Implementation Plan re-baseline required for affected patterns.

---

## Sign-Off

| Role | Name               | Decision   | Date       |
| ---- | ------------------ | ---------- | ---------- |
| CTO  | Dr. Kenji Nakamura | ☐ Accepted | YYYY-MM-DD |
| CIO  | Dr. Priya Mehta    | ☐ Accepted | YYYY-MM-DD |
| CSO  | Dr. Sarah Chen     | ☐ Accepted | YYYY-MM-DD |
