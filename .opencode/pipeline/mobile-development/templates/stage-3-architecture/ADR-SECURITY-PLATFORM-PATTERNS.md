# ADR-NNN: Platform-Specific Security Patterns

| Metadata          | Value                                          |
| ----------------- | ---------------------------------------------- |
| **ADR Number**    | ADR-NNN                                        |
| **Title**         | Platform-Specific Security Patterns            |
| **Status**        | Proposed                                       |
| **Decision Date** | YYYY-MM-DD                                     |
| **Authors**       | Security Architect (Natalia Petrova)           |
| **Reviewers**     | CSO (Dr. Sarah Chen), CTO (Dr. Kenji Nakamura) |
| **Stage**         | 3 — Architecture                               |
| **Category**      | Security / Platform Patterns                   |

---

## 1. Context

The application targets multiple platforms (iOS, Android, with potential KMP shared module and Flutter frontend layers). While much of the business logic can be abstracted into shared code, **platform-specific security mechanisms cannot and must not be abstracted away**. Each platform provides unique security APIs, hardware-backed attestation, and OS-level protections that must be leveraged directly.

This ADR establishes the authoritative security patterns for each platform layer. These patterns are **mandatory** for all development work and are referenced by the SRD (Security Requirements Document) for all platform-specific security controls.

**Key Principle:** Security-sensitive operations must execute at the platform level, not in shared or cross-platform code. Shared modules define _interfaces_; platform adapters implement _security_.

---

## 2. iOS Patterns

### 2.1 App Attest API — Server-Side Device Identity

| Aspect                      | Detail                                                                                                                                                                                             |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API**                     | `DCAppAttestService` (DeviceCheck framework)                                                                                                                                                       |
| **Purpose**                 | Cryptographic proof that requests originate from a genuine, unmodified app running on a real Apple device                                                                                          |
| **Implementation**          | Generate key pair on first launch → Attest key with Apple → Send attestation object + clientDataHash to server → Server verifies with Apple's App Attest API → Issue session token bound to device |
| **Server-Side Requirement** | Verification **must** occur server-side. Client-side verification is meaningless (attacker can patch the verification logic).                                                                      |
| **Fallback**                | If App Attest is unavailable (iOS < 14.0, simulator, or unsupported device), fall back to DeviceCheck tokens with elevated server-side risk scoring.                                               |
| **Risk if Omitted**         | Server cannot distinguish legitimate app traffic from automated bot traffic or modified app binaries.                                                                                              |

### 2.2 DeviceCheck — Fraud Prevention

| Aspect          | Detail                                                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **API**         | `DeviceCheck` framework (`DCDevice.generateToken`)                                                                        |
| **Purpose**     | Per-device, per-developer token for server-side fraud detection (rate limiting, abuse detection, ban enforcement)         |
| **Usage**       | Include DeviceCheck token in every authenticated API request. Server correlates token with abuse signals.                 |
| **Persistence** | Token survives app reinstall. Cleared only on device factory reset.                                                       |
| **Limitation**  | Two bits per device are available for server-set state. Use for binary flags (banned / not banned, high-risk / low-risk). |

### 2.3 Secure Clipboard

| Aspect            | Detail                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------- |
| **API**           | `UIPasteboard.general.localOnly = true`                                                     |
| **Purpose**       | Prevent clipboard contents from syncing to iCloud Handoff or being accessible by other apps |
| **When to Apply** | Any sensitive data copied to clipboard: auth tokens, OTP codes, recovery phrases, PII       |
| **Expiration**    | Set `UIPasteboard.expirationDate` to limit clipboard persistence (iOS 15+)                  |

### 2.4 Screenshot Prevention via Snapshot Masking

| Aspect                         | Detail                                                                                                                                                                                                                                                          |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mechanism**                  | Observe `UIApplication.userDidTakeScreenshotNotification` and respond by blurring sensitive views. For App Switcher preview, set `layer.isOpaque = true` and provide a placeholder snapshot in `AppDelegate.applicationProtectedDataWillBecomeUnavailable(_:)`. |
| **Limitation**                 | iOS does **not** provide a hard screenshot block (unlike Android's `FLAG_SECURE`). Prevention is limited to: (a) detecting screenshots and responding, (b) masking the App Switcher preview, (c) detecting screen recording via `UIScreen.isCaptured`.          |
| **Implementation**             | In `viewWillDisappear` or when entering background, overlay a blur view on sensitive content. Remove on `applicationDidBecomeActive`.                                                                                                                           |
| **Screen Recording Detection** | `UIScreen.main.isCaptured` (iOS 11+) — observe `UIScreen.capturedStateDidChangeNotification`. Pause or mask sensitive content when recording is detected.                                                                                                       |

### 2.5 Jailbreak Detection

| Aspect                | Detail                                                                                                                                                                                                                                                                                                                                                                                                            |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Detection Methods** | <ul><li>Check for Cydia URL scheme (`cydia://`)</li><li>Attempt to write outside sandbox (should fail on non-jailbroken devices)</li><li>Check for known jailbreak files: `/Applications/Cydia.app`, `/usr/sbin/sshd`, `/bin/bash`, `/etc/apt`, `/Library/MobileSubstrate/MobileSubstrate.dylib`</li><li>Check for symlinks pointing outside sandbox</li><li>Check for suspicious environment variables</li></ul> |
| **Response**          | **Do not crash** — crashing aids reverse engineering. Instead: limit functionality, elevate server-side risk scoring, log to server, and display a non-specific error.                                                                                                                                                                                                                                            |
| **Obfuscation**       | Detection logic must be obfuscated and spread across multiple modules. Single-point detection is trivially bypassed via hooking (Frida, Cydia Substrate).                                                                                                                                                                                                                                                         |
| **Limitation**        | Jailbreak detection is a **cat-and-mouse game**. It raises the bar for attackers but cannot guarantee detection of sophisticated, targeted jailbreak bypasses. Treat as a defense-in-depth layer, not a primary control.                                                                                                                                                                                          |

### 2.6 App Transport Security (ATS)

| Aspect                     | Detail                                                                                                                                                                                                                                          |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Default**                | ATS is enabled by default on iOS 9+. All connections must use HTTPS with TLS 1.2+ and valid certificates.                                                                                                                                       |
| **Exceptions**             | **No ATS exceptions are permitted without explicit CSO approval.** Any request to disable ATS (even for a single domain) requires: (a) documented business justification, (b) CSO sign-off in SRD, (c) compensating controls documented in ADR. |
| **NSAllowsArbitraryLoads** | **Prohibited** in production builds.                                                                                                                                                                                                            |
| **NSExceptionDomains**     | Permitted only for internal development builds. Must be stripped from release builds via build configuration.                                                                                                                                   |
| **Certificate Pinning**    | Required for all production API endpoints. Pin the leaf certificate or public key. Implement pin rotation with a fallback pin.                                                                                                                  |

---

## 3. Android Patterns

### 3.1 Play Integrity API

| Aspect                      | Detail                                                                                                                                                                                                                             |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API**                     | Google Play Integrity API (replaces SafetyNet Attestation)                                                                                                                                                                         |
| **Purpose**                 | Verify that the app is running on a genuine, unmodified device with a valid Play Store installation                                                                                                                                |
| **Response Tokens**         | `MEETS_DEVICE_INTEGRITY` — genuine Google-certified device<br>`MEETS_BASIC_INTEGRITY` — passes basic integrity checks (may be rooted/custom ROM)<br>`MEETS_STRONG_INTEGRITY` — hardware-backed boot integrity (Pixel, select OEMs) |
| **Server-Side Requirement** | Integrity token **must** be verified server-side via Google's Play Integrity API endpoint. Client-side verification is trivially bypassed.                                                                                         |
| **Fallback**                | If Play Services are unavailable (e.g., China market, custom ROM without GMS), implement equivalent integrity checks using hardware-backed Keystore attestation and server-side risk scoring.                                      |
| **Risk if Omitted**         | Server cannot detect modified app binaries, emulators, or automated bot traffic.                                                                                                                                                   |

### 3.2 Screenshot Prevention — FLAG_SECURE

| Aspect             | Detail                                                                                                                                                    |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API**            | `WindowManager.LayoutParams.FLAG_SECURE`                                                                                                                  |
| **Purpose**        | Prevent screenshots, screen recording, and App Switcher preview for the flagged Activity                                                                  |
| **Implementation** | Set in `Activity.onCreate()` before `setContentView()`: `window.setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE)` |
| **Scope**          | Applies per-Activity. Must be set in every Activity displaying sensitive content.                                                                         |
| **Effect**         | System blocks screenshot entirely (unlike iOS). Screen recordings show black frames. App Switcher preview is blanked.                                     |
| **Limitation**     | Cannot prevent external capture (camera photographing the screen).                                                                                        |

### 3.3 Root Detection

| Aspect                     | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Detection Methods**      | <ul><li>Check for `su` binary in PATH: `/system/bin/su`, `/system/xbin/su`, `/sbin/su`</li><li>Detect Magisk: check for Magisk package name, MagiskSU binary, Magisk mount points</li><li>Check Play Integrity API response — `MEETS_DEVICE_INTEGRITY` failure is a strong root indicator</li><li>Check for dangerous properties: `ro.debuggable=1`, `ro.secure=0`</li><li>Check for test-keys build tags (vs. release-keys)</li></ul> |
| **Response**               | Same as iOS: **do not crash**. Limit functionality, elevate server-side risk scoring, log to server, display non-specific error.                                                                                                                                                                                                                                                                                                       |
| **Obfuscation**            | Detection logic must be obfuscated and distributed. Use native code (JNI) for detection where possible — harder to patch than Java/Kotlin.                                                                                                                                                                                                                                                                                             |
| **SafetyNet Rooted Check** | Deprecated. Use Play Integrity API instead.                                                                                                                                                                                                                                                                                                                                                                                            |

### 3.4 Secure Clipboard

| Aspect          | Detail                                                                                                                                                                                |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API**         | `ClipDescription.ExtraInfo` with `ClipData.newPlainText(..., text).apply { description.extras = PersistableBundle().apply { putBoolean(ClipDescription.EXTRA_IS_SENSITIVE, true) } }` |
| **Android 13+** | Use `ClipDescription.FLAG_SENSITIVE_CONTENT` to mark clipboard data as sensitive. System will not persist or sync sensitive clipboard content.                                        |
| **Purpose**     | Prevent sensitive data from persisting in clipboard history or being accessible to other apps                                                                                         |

### 3.5 Network Security Configuration

| Aspect                  | Detail                                                                                                                                                                                                                                                                        |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **File**                | `res/xml/network_security_config.xml`                                                                                                                                                                                                                                         |
| **Cleartext Traffic**   | `<base-config cleartextTrafficPermitted="false" />` — **mandatory** for all production builds.                                                                                                                                                                                |
| **Certificate Pinning** | Use `<pin-set>` with SHA-256 digests of certificate public keys. Include `expiration` attribute for pin rotation.                                                                                                                                                             |
| **Trusted CAs**         | `<trust-anchors><certificates src="system" /></trust-anchors>` — **only system CAs**. User-installed CAs must **not** be trusted in production. Debug builds may include `<certificates src="user" />` for MITM proxy testing, but this must be stripped from release builds. |
| **Enforcement**         | Reference config in `AndroidManifest.xml`: `android:networkSecurityConfig="@xml/network_security_config"`.                                                                                                                                                                    |

### 3.6 BiometricPrompt API

| Aspect                 | Detail                                                                                                                                                                                                      |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API**                | `androidx.biometric.BiometricPrompt` (AndroidX library)                                                                                                                                                     |
| **Deprecated**         | `FingerprintManager` and `FingerprintManagerCompat` are **deprecated** and must not be used.                                                                                                                |
| **Capabilities**       | Supports fingerprint, face, and iris authentication via unified API.                                                                                                                                        |
| **Crypto Integration** | Use `BiometricPrompt.CryptoObject` wrapping a `Cipher`, `Signature`, or `Mac` instance backed by Android Keystore. Biometric authentication unlocks the keystore key — no biometric data leaves the device. |
| **Fallback**           | Provide device credential (PIN/pattern/password) fallback via `setDeviceCredentialAllowed(true)`.                                                                                                           |

---

## 4. KMP Shared Module Patterns

### 4.1 Security Abstractions as Platform Interface Definitions

| Aspect        | Detail                                                                                                                                                                                                                     |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pattern**   | Define security operations as `expect` declarations in the shared module; implement as `actual` in platform-specific source sets.                                                                                          |
| **Example**   | `expect fun encrypt(data: ByteArray, keyAlias: String): ByteArray` — shared module declares the interface; iOS and Android source sets provide platform-specific implementations using Keychain and Keystore respectively. |
| **Rationale** | Shared module code is compiled to Kotlin/JVM, Kotlin/Native (iOS), and potentially Kotlin/JS. Security implementations differ fundamentally across platforms and cannot be shared.                                         |

### 4.2 Shared Module Must NOT Implement Crypto Directly

| Aspect          | Detail                                                                                                                                                         |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Prohibition** | The shared module **must not** contain cryptographic implementations, key storage logic, or platform-specific security checks.                                 |
| **Allowed**     | Cryptographic _orchestration_ (e.g., "encrypt this payload before sending") — but the actual encryption is delegated to platform `actual` implementations.     |
| **Prohibited**  | Hardcoded keys, custom crypto algorithms, direct Keychain/Keystore calls from shared code.                                                                     |
| **Rationale**   | Shared module code may be compiled to targets where the security assumptions do not hold (e.g., Kotlin/JS runs in a browser with no hardware-backed keystore). |

### 4.3 Trust Boundary: Shared Module Is Untrusted

| Aspect                  | Detail                                                                                                                                                                              |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Model**               | The shared module is treated as an **untrusted component**. Platform adapters (the `actual` implementations) are the security boundary.                                             |
| **Validation**          | Platform adapters must validate all inputs from the shared module before passing them to security-sensitive APIs (Keychain, Keystore, BiometricPrompt, App Attest, Play Integrity). |
| **Output Sanitization** | Platform adapters must sanitize outputs before returning them to the shared module (e.g., redact key material, enforce access controls).                                            |

### 4.4 C Interop Boundary Validation for Kotlin/Native

| Aspect                 | Detail                                                                                                                                              |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Context**            | Kotlin/Native uses C interop (cinterop) to call Apple frameworks. The interop boundary is a potential attack surface.                               |
| **Validation**         | All data crossing the C interop boundary must be validated: null checks, bounds checks, type validation.                                            |
| **Memory Safety**      | Use Kotlin/Native's memory management rules. Do not manually manage memory at the C interop boundary unless absolutely necessary.                   |
| **Objective-C Bridge** | When calling Objective-C APIs from Kotlin/Native, ensure proper ARC semantics are respected. Leaked references can expose sensitive data in memory. |

---

## 5. Flutter Patterns

### 5.1 Platform Channels for All Security Operations

| Aspect          | Detail                                                                                                                                                                                   |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pattern**     | All security-sensitive operations (encryption, key storage, biometric auth, attestation, clipboard) **must** execute via platform channels (`MethodChannel`) to native iOS/Android code. |
| **Prohibition** | **No Dart-only security implementations.** Dart code runs in a VM with no hardware-backed security guarantees.                                                                           |
| **Example**     | `const platform = MethodChannel('com.app.security/crypto');` → calls native code that uses iOS Keychain or Android Keystore.                                                             |

### 5.2 Package Version Pinning

| Package                  | Purpose                     | Requirement                                                                                                                                      |
| ------------------------ | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `flutter_secure_storage` | Keychain/Keystore access    | **Version pin to exact version** (no `^` or `>=`). Review release notes for security-relevant changes before upgrading.                          |
| `local_auth`             | BiometricPrompt / LAContext | **Version pin to exact version.** Validate that underlying native APIs match this ADR (BiometricPrompt on Android, LAContext on iOS).            |
| `device_info_plus`       | Device identification       | **Version pin to exact version.** Note: this package provides device info, NOT attestation. Use App Attest / Play Integrity for device identity. |

### 5.3 Dart Code Is NOT a Security Boundary

| Aspect          | Detail                                                                                                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Reality**     | Dart bytecode can be decompiled. The Dart VM provides no tamper resistance. Sensitive logic in Dart code is trivially extractable.                                        |
| **Implication** | Do not store secrets, implement crypto, or perform security decisions in Dart. All security-sensitive operations must execute on the platform side via platform channels. |
| **Obfuscation** | Enable `--obfuscate` and `--split-debug-info` for release builds. This raises the bar slightly but is **not** a security control — treat as defense-in-depth only.        |

### 5.4 Platform Channel Message Validation

| Aspect             | Detail                                                                                                                                                      |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Risk**           | Platform channels pass messages between Dart and native code. Messages are not type-safe and can be spoofed by a compromised Dart layer.                    |
| **Validation**     | Native platform channel handlers must validate all incoming messages: type checks, value ranges, authorization checks before executing security operations. |
| **Return Values**  | Native code must not return sensitive data (key material, raw biometric data) to Dart. Return only success/failure or non-sensitive results.                |
| **Channel Naming** | Use unique, namespaced channel names to prevent collision with third-party plugins.                                                                         |

---

## 6. Cross-Platform Security Parity

| Aspect                   | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Principle**            | The **weakest platform defines the security floor**. If Android provides a capability that iOS does not (or vice versa), the gap must be documented and compensating controls must be implemented.                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Current Gap Analysis** | <ul><li>**Screenshot prevention:** Android (`FLAG_SECURE`) provides hard block. iOS provides detection + masking only. → Compensating control on iOS: screen recording detection, App Switcher masking, server-side risk scoring on screenshot events.</li><li>**Device attestation:** iOS App Attest vs. Android Play Integrity — both provide server-verifiable attestation. Parity achieved.</li><li>**Clipboard security:** Both platforms support sensitive clipboard flags. Parity achieved.</li><li>**Biometric auth:** Both platforms support modern BiometricPrompt / LAContext. Parity achieved.</li></ul> |
| **Verification**         | Security parity must be verified during **Stage 5 (Development)** via parallel testing. Any parity gap discovered must be raised as a P1 defect if it creates an asymmetric attack surface.                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Reporting**            | Parity verification results are included in the Stage 8 Integrity Verification report.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

---

## 7. STRIDE Threat Reference

| STRIDE Category            | Platform-Specific Threats                                                        | Mitigations (per this ADR)                                                                         |
| -------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Spoofing**               | Fake device identity, emulator impersonation, modified app binary                | App Attest (iOS), Play Integrity (Android), server-side verification                               |
| **Tampering**              | Jailbreak/root bypass, runtime hooking (Frida, Xposed), binary patching          | Jailbreak/root detection (obfuscated, multi-method), server-side risk scoring, certificate pinning |
| **Repudiation**            | Denied actions, forged API requests                                              | Device-bound session tokens, server-side attestation verification, audit logging                   |
| **Information Disclosure** | Clipboard exposure, screenshot capture, memory dumps, insecure storage           | Secure clipboard, FLAG_SECURE / snapshot masking, Keychain/Keystore only, `FLAG_SECURE`            |
| **Denial of Service**      | App crash via jailbreak detection bypass, resource exhaustion                    | Graceful degradation (never crash on detection), server-side rate limiting                         |
| **Elevation of Privilege** | Root/jailbreak granting access to protected resources, platform channel spoofing | Platform channel validation, trust boundary enforcement, least-privilege key access                |

---

## 8. MASVS Reference

| MASVS Category       | Relevant Controls                                                                                                | Compliance Notes                                                                                                            |
| -------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **MASVS-RESILIENCE** | R1 (Obfuscation), R2 (Anti-tampering), R3 (Anti-reversing), R4 (Runtime Integrity), R5 (Defensive Coding)        | Jailbreak/root detection, obfuscated detection logic, FLAG_SECURE, screenshot detection, graceful degradation               |
| **MASVS-PLATFORM**   | PLATFORM-1 (Platform Security Features), PLATFORM-2 (Third-Party Code), PLATFORM-3 (Inter-Process Communication) | App Attest, Play Integrity, BiometricPrompt, secure clipboard, platform channel validation, ATS/Network Security Config     |
| **MASVS-STORAGE**    | STORAGE-1 (No sensitive data in storage), STORAGE-2 (Keychain/Keystore only)                                     | All secrets stored in iOS Keychain or Android Keystore. No plaintext secrets in shared preferences, UserDefaults, or files. |
| **MASVS-NETWORK**    | NETWORK-1 (TLS only), NETWORK-2 (Certificate pinning), NETWORK-3 (Certificate validation)                        | ATS (iOS), Network Security Config (Android), certificate pinning mandatory, no cleartext in production                     |

**Compliance Level Target:** MASVS-2 (Defense in Depth) + MASVS-RESILIENCE controls.

---

## 8.1 Enforcement Table

| Enforcement Layer | Mechanism                                                                                    |
| ----------------- | -------------------------------------------------------------------------------------------- |
| Policy            | Stage 3 ADR lock — platform patterns not revisable                                           |
| CI/CD             | Platform-specific security linting (Detekt/SwiftLint rules)                                  |
| Code Review       | Security team reviews platform patterns during Stage 6 Tier 1                                |
| Stage 8 Integrity | Anti-trim verification includes platform-specific security controls presence and correctness |

---

## 8.2 STRIDE Threat Reference

| STRIDE Category            | Threat                                                                                       | Mitigation                                                                                                 |
| -------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Spoofing**               | Fake app or modified binary impersonating legitimate app                                     | App Attest (iOS), Play Integrity (Android) with server-side verification                                   |
| **Tampering**              | Runtime code modification, resource patching, or binary re-signing                           | Jailbreak/root detection, code signature validation, runtime hooking detection, obfuscated detection logic |
| **Repudiation**            | User denies performing sensitive action that should have been attested                       | Server-side attestation logs with hardware-backed device identity binding                                  |
| **Information Disclosure** | Sensitive data exposed via insecure platform APIs (clipboard, screenshots, logs)             | Secure clipboard, FLAG_SECURE, snapshot masking, no sensitive data in logs                                 |
| **Denial of Service**      | Attacker triggers false-positive in jailbreak/root detection, locking out legitimate users   | Graceful degradation: server-side risk scoring + manual review fallback                                    |
| **Elevation of Privilege** | Exploiting platform channel vulnerability to access native security APIs from untrusted code | Platform channel message validation, type checking, permission enforcement on native side                  |

---

## 9. Alternatives Considered

| Alternative                                                                                     | Description                                                             | Why Rejected                                                                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cross-platform security libraries** (e.g., `flutter_secure_storage` as the sole crypto layer) | Rely on cross-platform plugins to abstract platform security APIs       | Cross-platform plugins are thin wrappers — they still call platform APIs. Using them as the _sole_ security layer adds an unnecessary dependency chain and obscures what platform APIs are actually being called. Direct platform channel calls are more auditable. |
| **Custom cryptographic implementations in shared code**                                         | Implement AES, RSA, etc. in Kotlin shared module or Dart                | Custom crypto is **always** the wrong answer. Platform-provided crypto (Keychain, Keystore, CommonCrypto, AndroidX Security) is hardware-accelerated, FIPS-validated where applicable, and receives security updates from the OS vendor.                            |
| **No attestation — trust client-side signals**                                                  | Rely on device identifiers (IDFA, Android ID, IMEI) for device identity | All client-side identifiers are spoofable. App Attest and Play Integrity provide **server-verifiable, hardware-backed** attestation. Anything less is security theater.                                                                                             |
| **Hard screenshot block on iOS**                                                                | Attempt to block screenshots entirely on iOS                            | **Technically impossible** on iOS. Apple provides no API to block screenshots. Detection + masking + server-side risk scoring is the only viable approach.                                                                                                          |

---

## 10. Compliance

| Rule                              | Detail                                                                                                                                                                                                                                                                                                                              |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage Lock**                    | This ADR is locked at **Stage 3 (Architecture)**. Any deviation from the patterns defined herein requires **Stage 3 re-entry** and explicit **CSO approval**.                                                                                                                                                                       |
| **Deviation Process**             | If a platform pattern cannot be implemented as specified (e.g., target market lacks Play Services, iOS version requirement is too restrictive), the engineering team must: (1) document the constraint, (2) propose compensating controls, (3) submit to CSO for review, (4) if approved, amend this ADR with a versioned addendum. |
| **Audit**                         | Compliance with this ADR is verified during **Stage 6 (Code Review)** via security code review and **Stage 8 (Integrity Verification)** via platform-specific security testing.                                                                                                                                                     |
| **Non-Compliance Classification** | Failure to implement mandatory patterns from this ADR is classified as **P0** (security breach risk) if it exposes sensitive data or bypasses attestation, or **P1** (core security feature broken) for other violations.                                                                                                           |

---

## Appendix A: Version History

| Version | Date       | Author          | Change        |
| ------- | ---------- | --------------- | ------------- |
| v1      | 2026-04-08 | Natalia Petrova | Initial draft |

---

## Appendix B: Related Documents

| Document                             | Location                                        |
| ------------------------------------ | ----------------------------------------------- |
| Security Requirements Document (SRD) | `requirements/srd/SRD.md`                       |
| MASVS Compliance Baseline            | `company/library/topics/security.md`            |
| Threat Modeling Framework            | `security/pentesting/threat-modeling.md`        |
| Mobile Threat Modeling               | `security/pentesting/mobile-threat-modeling.md` |
| MASVS Track B Certification          | `security/masvs/masvs-mastery-track-b.md`       |
