---
name: security-masvs-masvs-mastery-track-a
description: 'Security skill: Masvs Mastery Track A'
---

# MASVS Mastery Track A

**Category:** Mobile Security — MASVS Mastery Criteria
**Owner:** Lead Security Engineer — James Wright
**Companion Docs:** `masvs-overview.md` (CSO — framework orientation), `owasp-masvs-compliance.md` (Sana Khoury — assessment procedures), `owasp-masvs-auditing.md` (Ingrid Solberg — audit methodology)

## 1. Track A Overview — Scope and Purpose

MASVS Track A defines the **standard security baseline (Level 1)** that **ALL mobile applications must meet** before release. It is not checkbox compliance — it is a **mastery framework** that requires demonstrable evidence of security competence across seven verification categories (V1–V7 at L1) plus resilience awareness (V8, L2-selected controls that impact L1 security posture).

### 1.1 Why "Mastery" vs "Met"

| Criterion         | "Met" (Checkbox)          | "Mastery" (Track A)                                                          |
| ----------------- | ------------------------- | ---------------------------------------------------------------------------- |
| **Evidence**      | "Yes, we do this"         | Reproducible proof: test results, configuration files, runtime demonstration |
| **Depth**         | Single verification point | Multiple verification angles: static + dynamic + manual review               |
| **Durability**    | Point-in-time check       | Continuous verification via CI/CD pipeline integration                       |
| **Defensibility** | Internal assertion        | Auditor-ready evidence package with chain of custody                         |
| **Regression**    | Not tracked               | Automated regression tests prevent backsliding                               |

### 1.2 Track A Coverage Matrix

| Category                                       | Level | Requirements        | Mastery Status Required For                               |
| ---------------------------------------------- | ----- | ------------------- | --------------------------------------------------------- |
| **V1: Architecture, Design & Threat Modeling** | L1    | 8 controls          | All applications                                          |
| **V2: Data Storage & Privacy**                 | L1    | 10 controls         | All applications                                          |
| **V3: Cryptography**                           | L1    | 6 controls          | All applications                                          |
| **V4: Authentication & Session Management**    | L1    | 9 controls          | All applications with user accounts                       |
| **V5: Network Communication**                  | L1    | 7 controls          | All applications with network connectivity                |
| **V6: Platform Interaction**                   | L1    | 8 controls          | All applications                                          |
| **V7: Code Quality & Build Settings**          | L1    | 7 controls          | All applications                                          |
| **V8: Resilience**                             | L2    | 4 selected controls | Applications in adversarial environments (defined in SRD) |

**Total Track A controls assessed:** 55 L1 + 4 L2-selected = **59 controls**

### 1.3 V8 L2-Selected Controls in Track A

Track A includes only V8 controls that have **direct impact on L1 security posture**. These are not the full V8 resilience suite (that is Track B). Track A selects:

| Req ID | Requirement                           | Why Included in Track A                                                   |
| ------ | ------------------------------------- | ------------------------------------------------------------------------- |
| 8.1.1  | Root/jailbreak detection and response | Rooted devices bypass all L1 storage/crypto controls                      |
| 8.2.1  | Tampering detection                   | Modified binaries can disable any L1 control at runtime                   |
| 8.3.2  | Hooking framework detection           | Frida/Xposed can bypass authentication, intercept crypto, exfiltrate data |
| 8.4.2  | Anti-debugging measures               | Debuggers can extract keys, bypass auth, manipulate logic                 |

### 1.4 Mastery Status Definitions

| Status      | Definition                                                                                             | Release Impact                             |
| ----------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------ |
| **MASTERY** | Evidence demonstrates consistent, automated, and defensible compliance across all verification methods | ✅ Proceeds to release                     |
| **MET**     | Basic compliance achieved but evidence is incomplete or point-in-time only                             | ⚠️ Conditional — requires remediation plan |
| **NOT MET** | Control absent, incorrectly implemented, or evidence contradicts claim                                 | 🚫 Release blocker — classified as P0/P1   |

---

## 2. V1: Architecture, Design and Threat Modeling — Mastery Criteria

### 2.1 Control-by-Control Mastery Requirements

#### V1.1.1 — Security Throughout SDLC

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Security activities are documented and traceable across ALL pipeline stages (1–10); security gates are automated where possible; security ownership is assigned per stage                                                                                                                    |
| **Verification Procedure** | 1. Review SRD (Stage 1) for security requirements<br>2. Verify Stage 6 code review panel includes CSO signatory<br>3. Verify SAST/DAST results are in CI/CD pipeline<br>4. Verify Stage 8 integrity verification report exists<br>5. Confirm security sign-off in Stage 10 release checklist |
| **Evidence Required**      | SRD document, Stage 6 Defect Report, Stage 8 Integrity Report, CI/CD pipeline config showing security scans, Stage 10 release checklist with CSO signature                                                                                                                                   |
| **Mastery vs Met**         | **Met** = SRD exists and Stage 6/8/10 sign-offs present. **Mastery** = Additionally, CI/CD pipeline automates security gates; defect trend analysis shows decreasing security findings over time                                                                                             |

#### V1.1.2 — Up-to-Date OS Versions and Libraries

| Attribute                  | Requirement                                                                                                                                                                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mastery Criterion**      | `minSdkVersion` / `deploymentTarget` targets an OS version receiving active security patches; all dependencies are within 2 minor versions of latest stable; automated dependency scanning is active                                                                                 |
| **Verification Procedure** | 1. Check `build.gradle` `minSdkVersion` (Android) or `Info.plist` `LSMinimumSystemVersion` (iOS)<br>2. Cross-reference with vendor security support matrix<br>3. Run SCA scan (Snyk/Dependabot) on all dependencies<br>4. Verify automated PR generation for vulnerable dependencies |
| **Evidence Required**      | Build configuration files, dependency lock files, SCA scan results, Dependabot/Snyk PR history showing automated updates                                                                                                                                                             |
| **Mastery vs Met**         | **Met** = Dependencies are current at time of review. **Mastery** = Automated dependency scanning + auto-PR workflow + SBOM generation with vulnerability alerting                                                                                                                   |

#### V1.1.3 — Runtime Integrity Verification

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | App verifies integrity of dynamically loaded code, configuration, and data at runtime; verification uses cryptographic hashes or signatures                                                                                                                                                                     |
| **Verification Procedure** | 1. Identify all runtime-loaded components (plugins, config files, dynamic feature modules)<br>2. Verify each has integrity check (SHA-256 hash, code signature)<br>3. Test integrity bypass: modify loaded component, verify app rejects it<br>4. Verify integrity check cannot be disabled via runtime hooking |
| **Evidence Required**      | Source code of integrity verification routines, test results showing rejection of modified components, Frida test proving hook resistance                                                                                                                                                                       |
| **Mastery vs Met**         | **Met** = Integrity checks exist. **Mastery** = Checks are cryptographically strong, hook-resistant, and tested against active bypass attempts                                                                                                                                                                  |

#### V1.1.4 — Principle of Least Privilege

| Attribute                  | Requirement                                                                                                                                                                                                                                                                       |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | App requests minimum permissions required; each permission is justified in documentation; runtime permission requests include user-facing context                                                                                                                                 |
| **Verification Procedure** | 1. Review Android manifest `uses-permission` / iOS `Info.plist` privacy keys<br>2. Map each permission to specific feature requirement<br>3. Verify no dangerous permissions requested without runtime justification<br>4. Test permission denial: verify app degrades gracefully |
| **Evidence Required**      | Permission mapping document, runtime permission flow screenshots, permission denial graceful degradation test results                                                                                                                                                             |
| **Mastery vs Met**         | **Met** = Permission list reviewed and justified. **Mastery** = Automated permission audit in CI/CD; any new permission requires ADR approval                                                                                                                                     |

#### V1.1.5 — Certificate Pinning

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mastery Criterion**      | Certificate pinning is configured for all production API endpoints; pin rotation procedure is documented and tested; fallback does not disable pinning                                                                                                                                                 |
| **Verification Procedure** | 1. Review pinning configuration (`network_security_config.xml` / `Info.plist` ATS / TrustKit / OkHttp `CertificatePinner`)<br>2. Verify pins cover all production domains<br>3. Test with Burp Suite proxy: verify connection is rejected<br>4. Verify pin rotation procedure works without app update |
| **Evidence Required**      | Pinning configuration files, Burp Suite test results showing rejected MITM, pin rotation test report, backup pin configuration                                                                                                                                                                         |
| **Mastery vs Met**         | **Met** = Pinning configured and tested. **Mastery** = Includes backup pins, documented rotation procedure tested within 90 days, automated pin expiry alerts                                                                                                                                          |

#### V1.1.6 — Third-Party SDK Vetting

| Attribute                  | Requirement                                                                                                                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All third-party SDKs undergo security vetting before integration; SDK inventory is maintained; vulnerabilities are monitored and patched within SLA                                                                 |
| **Verification Procedure** | 1. Generate SBOM (Syft/CycloneDX) for all SDKs<br>2. Cross-reference SBOM against CVE databases<br>3. Review SDK vetting documentation for each dependency<br>4. Verify no SDKs with known critical vulnerabilities |
| **Evidence Required**      | SBOM, SDK vetting checklist, CVE scan results, patch timeline for any identified vulnerabilities                                                                                                                    |
| **Mastery vs Met**         | **Met** = SDK inventory exists and CVE scan is clean. **Mastery** = Automated SBOM generation on every build; continuous CVE monitoring; SDK removal process for abandoned dependencies                             |

#### V1.1.7 — Defense-in-Depth

| Attribute                  | Requirement                                                                                                                                                                                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Critical security controls have at least two independent layers; compromise of one layer does not fully compromise the protected asset                                                                                                                          |
| **Verification Procedure** | 1. Identify critical assets (auth tokens, cryptographic keys, PII)<br>2. Map all protection layers for each asset<br>3. Verify layers are independent (not bypassed by same attack)<br>4. Test single-layer bypass: verify remaining layers still protect asset |
| **Evidence Required**      | Defense-in-depth mapping document, single-layer bypass test results, architecture diagrams showing layer independence                                                                                                                                           |
| **Mastery vs Met**         | **Met** = Multiple layers documented. **Mastery** = Each layer independently tested; bypass of any single layer demonstrated to be insufficient for full compromise                                                                                             |

#### V1.1.8 — Session Management

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Session tokens have defined lifecycle (creation, refresh, revocation, expiry); tokens are stored securely; server-side session invalidation is functional                                                                                                                                    |
| **Verification Procedure** | 1. Review token lifecycle implementation (JWT expiry, refresh token rotation)<br>2. Verify token storage uses Keychain/Keystore<br>3. Test token revocation: revoke token server-side, verify app cannot use it<br>4. Test token expiry: wait for expiry, verify refresh or re-auth required |
| **Evidence Required**      | Token lifecycle documentation, secure storage configuration, token revocation test results, token expiry test results                                                                                                                                                                        |
| **Mastery vs Met**         | **Met** = Token lifecycle implemented. **Mastery** = Automated token lifecycle tests in CI/CD; refresh token rotation; concurrent session management                                                                                                                                         |

---

## 3. V2: Data Storage and Privacy — Mastery Criteria

### 3.1 Control-by-Control Mastery Requirements

#### V2.1.1 — System Credential Storage

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                      |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All sensitive data (credentials, tokens, keys) stored exclusively in platform credential storage (iOS Keychain / Android Keystore); no custom encryption for credentials                                                                                                                                         |
| **Verification Procedure** | 1. Search codebase for any custom credential storage implementation<br>2. Verify all credential access uses Keychain/Keystore APIs<br>3. Test credential extraction: attempt to read credential files directly from filesystem<br>4. Verify Keychain/Keystore access controls (biometric binding, access groups) |
| **Evidence Required**      | Code search results showing no custom credential storage, Keychain/Keystore API usage documentation, filesystem extraction test results                                                                                                                                                                          |
| **Mastery vs Met**         | **Met** = Credentials stored in platform storage. **Mastery** = Access controls configured (biometric binding for sensitive keys); automated audit prevents custom credential storage from merging                                                                                                               |

#### V2.1.2 — No Plaintext Sensitive Data

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Automated scanning confirms zero instances of sensitive data (credentials, tokens, PII, financial data) in plaintext on device filesystem                                                                                                                                                                                                                           |
| **Verification Procedure** | 1. Extract full app data from test device<br>2. Run automated sensitive data scanner (regex patterns for credentials, PII, financial data)<br>3. Manually review any scanner positives for false positives<br>4. Verify encrypted databases use SQLCipher or equivalent<br>5. Verify SharedPreferences use EncryptedSharedPreferences (Android) or equivalent (iOS) |
| **Evidence Required**      | Full filesystem scan report, scanner regex patterns, false positive analysis, encryption configuration for all data stores                                                                                                                                                                                                                                          |
| **Mastery vs Met**         | **Met** = Scan completed with no findings. **Mastery** = Automated scan runs in CI/CD on every build; scan covers all data stores including caches, logs, backups, and auto-generated files                                                                                                                                                                         |

#### V2.1.3 — No IPC Data Leakage

| Attribute                  | Requirement                                                                                                                                                                                                                               |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All IPC mechanisms (intents, URL schemes, universal links, App Groups, ContentProviders) are validated for data leakage; sensitive data is never transmitted via IPC without encryption                                                   |
| **Verification Procedure** | 1. Inventory all IPC entry and exit points<br>2. Review data transmitted through each IPC mechanism<br>3. Verify sensitive data is encrypted before IPC transmission<br>4. Test IPC interception: verify intercepted data is not readable |
| **Evidence Required**      | IPC inventory document, data flow diagrams for each IPC mechanism, IPC interception test results                                                                                                                                          |
| **Mastery vs Met**         | **Met** = IPC mechanisms reviewed. **Mastery** = Automated IPC data flow analysis; all IPC channels have explicit allowlists; interception tests prove encryption effectiveness                                                           |

#### V2.1.4 — No Platform API Exposure

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                                                                                                    |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Sensitive data is protected from platform APIs: pasteboard cleared, notifications masked, screenshots prevented on sensitive screens, backups exclude sensitive data                                                                                                                                                                                                                           |
| **Verification Procedure** | 1. Verify pasteboard is cleared after sensitive copy operations<br>2. Verify push notifications do not contain sensitive data<br>3. Verify sensitive screens prevent screenshots (Android: `FLAG_SECURE`; iOS: `UIScreen.main.isCaptured`)<br>4. Verify backup configuration excludes sensitive data (Android: `android:allowBackup="false"` or backup rules; iOS: `NSFileProtectionComplete`) |
| **Evidence Required**      | Pasteboard clearing code, notification payload review, screenshot prevention test results, backup configuration files                                                                                                                                                                                                                                                                          |
| **Mastery vs Met**         | **Met** = Platform APIs reviewed and configured. **Mastery** = Each protection is tested in automated test suite; regression tests prevent removal                                                                                                                                                                                                                                             |

#### V2.1.5 — Developer Features Disabled in Release

| Attribute                  | Requirement                                                                                                                                                                                                                                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All developer features (debug logging, test interfaces, debug UI, developer menus) are disabled or removed in release builds                                                                                                                                |
| **Verification Procedure** | 1. Build release variant<br>2. Verify no debug logs in logcat/Console<br>3. Verify no debug UI elements accessible<br>4. Verify `android:debuggable="false"` (Android) / `DEBUG` flag unset (iOS)<br>5. Verify no test endpoints reachable in release build |
| **Evidence Required**      | Release build configuration, debug feature verification checklist, logcat/Console output from release build showing no debug output                                                                                                                         |
| **Mastery vs Met**         | **Met** = Release build verified manually. **Mastery** = Automated CI/CD check validates release build configuration; any debug flag causes build failure                                                                                                   |

#### V2.1.6 — Keyboard Cache Protection

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                    |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All sensitive input fields disable keyboard autocorrect and caching                                                                                                                                                                                                                                            |
| **Verification Procedure** | 1. Review all input fields handling sensitive data<br>2. Verify `secureTextEntry` / `textContentType` configuration<br>3. Verify `autocorrectionType="no"` (iOS) / `inputType` excludes text suggestions (Android)<br>4. Test keyboard cache: type sensitive data, switch apps, verify data not in suggestions |
| **Evidence Required**      | Input field configuration review, keyboard cache test results                                                                                                                                                                                                                                                  |
| **Mastery vs Met**         | **Met** = Sensitive fields configured correctly. **Mastery** = Automated lint rule prevents sensitive input fields without keyboard protection                                                                                                                                                                 |

#### V2.1.7 — App Switcher Protection

| Attribute                  | Requirement                                                                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | App snapshot is masked or cleared when app enters background                                                                                                  |
| **Verification Procedure** | 1. Launch app, navigate to sensitive screen<br>2. Background the app<br>3. Open app switcher<br>4. Verify sensitive screen content is not visible in snapshot |
| **Evidence Required**      | App switcher screenshots showing masked content, implementation code for snapshot protection                                                                  |
| **Mastery vs Met**         | **Met** = Snapshot masking tested manually. **Mastery** = Automated UI test captures app switcher state; regression test prevents removal                     |

#### V2.1.8 — Data Retention Auto-Deletion

| Attribute                  | Requirement                                                                                                                                                                                                                                                           |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | App auto-deletes sensitive data per defined retention policy; deletion is verifiable and irreversible                                                                                                                                                                 |
| **Verification Procedure** | 1. Review data retention policy document<br>2. Identify all data types with retention periods<br>3. Test auto-deletion: create data, wait for retention period, verify deletion<br>4. Verify deleted data cannot be recovered (including backups, caches, thumbnails) |
| **Evidence Required**      | Data retention policy, auto-deletion implementation code, deletion verification test results                                                                                                                                                                          |
| **Mastery vs Met**         | **Met** = Retention policy documented and tested. **Mastery** = Automated retention enforcement with audit log; deletion covers all storage locations including system caches                                                                                         |

#### V2.1.9 — Generated Document Protection

| Attribute                  | Requirement                                                                                                                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Files generated by the app (exports, downloads, reports) have appropriate file permissions and encryption                                                                                    |
| **Verification Procedure** | 1. Generate sample documents via app<br>2. Check file permissions on generated files<br>3. Verify files are not world-readable<br>4. Verify files are encrypted if containing sensitive data |
| **Evidence Required**      | Generated file permission listings, encryption status of generated documents                                                                                                                 |
| **Mastery vs Met**         | **Met** = Generated files have correct permissions. **Mastery** = Automated file permission check on all generated outputs; encryption applied by default                                    |

#### V2.1.10 — Secure Memory Handling

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Sensitive data in memory (keys, tokens, passwords) is zeroed after use; memory dumps do not reveal sensitive data                                                                                                                                                                               |
| **Verification Procedure** | 1. Identify all locations where sensitive data is held in memory<br>2. Verify explicit memory zeroing after use (not relying on GC)<br>3. Take memory dump during sensitive operation<br>4. Scan memory dump for sensitive data patterns<br>5. Verify zeroing is not optimized away by compiler |
| **Evidence Required**      | Memory handling code review, memory dump scan results, compiler optimization analysis                                                                                                                                                                                                           |
| **Mastery vs Met**         | **Met** = Memory zeroing implemented. **Mastery** = Memory dump testing proves data removal; compiler barriers prevent optimization; automated memory safety tests in CI/CD                                                                                                                     |

---

## 4. V3: Cryptography — Mastery Criteria

### 4.1 Control-by-Control Mastery Requirements

#### V3.1.1 — Industry-Standard Algorithms

| Attribute                  | Requirement                                                                                                                                                                                                                                                       |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Only industry-standard, NIST-approved cryptographic algorithms are used; deprecated algorithms are blocked at build time                                                                                                                                          |
| **Verification Procedure** | 1. Inventory all cryptographic operations in codebase<br>2. Verify algorithm compliance: AES-128+, RSA-2048+, ECDSA P-256+, SHA-256+<br>3. Verify NO usage of: DES, 3DES, RC4, MD5, SHA-1 (for signatures)<br>4. Run SAST rule to detect non-compliant algorithms |
| **Evidence Required**      | Cryptographic inventory, SAST scan results showing no deprecated algorithms, algorithm compliance matrix                                                                                                                                                          |
| **Mastery vs Met**         | **Met** = All algorithms are current. **Mastery** = SAST rule blocks deprecated algorithms at PR level; automated alert on algorithm deprecation announcements                                                                                                    |

#### V3.1.2 — No Custom Cryptography

| Attribute                  | Requirement                                                                                                                                                                                                                                                           |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | No home-grown cryptographic algorithms, protocols, or implementations; all crypto uses vetted libraries                                                                                                                                                               |
| **Verification Procedure** | 1. Search codebase for custom crypto implementations<br>2. Verify all crypto operations use platform or vetted library (Bouncy Castle, CryptoKit, libsodium)<br>3. Review any "encryption-like" operations (encoding, obfuscation) to confirm not mistaken for crypto |
| **Evidence Required**      | Code search results for custom crypto, approved crypto library list, all crypto call sites mapped to approved libraries                                                                                                                                               |
| **Mastery vs Met**         | **Met** = No custom crypto found. **Mastery** = Automated SAST rule detects custom crypto patterns; approved crypto library list is version-pinned                                                                                                                    |

#### V3.1.3 — Correct Cryptographic Implementation

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Cryptographic operations use correct parameters: proper IV/nonce generation, secure padding modes, appropriate key sizes, no ECB mode                                                                                                                                                                           |
| **Verification Procedure** | 1. Review each crypto operation for correct parameter usage<br>2. Verify IVs are random and unique per operation (never reused)<br>3. Verify padding mode is secure (PKCS7, OAEP — never PKCS1 v1.5 for encryption)<br>4. Verify no ECB mode usage<br>5. Test with known test vectors to confirm correct output |
| **Evidence Required**      | Crypto parameter review checklist, test vector verification results, IV uniqueness test                                                                                                                                                                                                                         |
| **Mastery vs Met**         | **Met** = Parameters are correct. **Mastery** = Automated crypto parameter validation in CI/CD; known-answer tests run as unit tests                                                                                                                                                                            |

#### V3.1.4 — Secure Key Storage

| Attribute                  | Requirement                                                                                                                                                                                                                                                                              |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Cryptographic keys are stored exclusively in hardware-backed credential storage (iOS Secure Enclave / Android StrongBox); keys never leave secure hardware                                                                                                                               |
| **Verification Procedure** | 1. Verify key generation uses hardware-backed Keystore/Secure Enclave<br>2. Verify keys are non-exportable<br>3. Test key extraction: attempt to export key from secure storage<br>4. Verify key usage is bound to authentication (biometric/device credential) for sensitive operations |
| **Evidence Required**      | Key generation code, hardware-backed storage confirmation, key extraction attempt results, authentication binding configuration                                                                                                                                                          |
| **Mastery vs Met**         | **Met** = Keys stored in platform secure storage. **Mastery** = Hardware-backed (not just software Keystore); keys are non-exportable; authentication binding enforced; key rotation automated                                                                                           |

#### V3.1.5 — Cryptographically Secure RNG

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All random number generation uses cryptographically secure PRNG; no use of `Random`, `rand()`, or similar non-secure generators                                                                                                                                                                   |
| **Verification Procedure** | 1. Search codebase for all random number generation<br>2. Verify usage of `SecureRandom` (Android), `SecRandomCopyBytes` (iOS), or vetted library<br>3. Verify NO usage of `java.util.Random`, `arc4random` (without security context), `rand()`<br>4. Run SAST rule to detect insecure RNG usage |
| **Evidence Required**      | RNG inventory, SAST scan results for insecure RNG, secure RNG usage documentation                                                                                                                                                                                                                 |
| **Mastery vs Met**         | **Met** = All RNG is secure. **Mastery** = SAST rule blocks insecure RNG at PR level; statistical RNG quality tests run in CI/CD                                                                                                                                                                  |

#### V3.1.6 — Secure Error Handling in Crypto

| Attribute                  | Requirement                                                                                                                                                                                                                                                                             |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Cryptographic operations handle errors without leaking information; comparisons are constant-time; error messages do not reveal crypto internals                                                                                                                                        |
| **Verification Procedure** | 1. Review crypto error handling paths<br>2. Verify signature/MAC comparisons use constant-time comparison<br>3. Verify error messages are generic (no "invalid padding" vs "invalid key" distinction)<br>4. Test timing side-channel: measure response time for valid vs invalid inputs |
| **Evidence Required**      | Error handling code review, constant-time comparison verification, timing side-channel test results                                                                                                                                                                                     |
| **Mastery vs Met**         | **Met** = Error handling reviewed. **Mastery** = Timing tests prove no side-channel leakage; automated SAST detects non-constant-time comparisons                                                                                                                                       |

---

## 5. V4: Authentication and Session Management — Mastery Criteria

### 5.1 Control-by-Control Mastery Requirements

#### V4.1.1 — NIST-Compliant Password Policy

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Password policy follows NIST SP 800-63B: minimum 8 characters, no arbitrary complexity requirements, checks against breached password databases, no periodic forced rotation                                                                                                                      |
| **Verification Procedure** | 1. Review password policy implementation<br>2. Verify minimum length ≥ 8<br>3. Verify NO mandatory special character/uppercase/number requirements<br>4. Verify integration with breached password database (Have I Been Pwned API or equivalent)<br>5. Verify no forced periodic rotation policy |
| **Evidence Required**      | Password policy document, breached password check implementation, password validation test results                                                                                                                                                                                                |
| **Mastery vs Met**         | **Met** = Policy follows NIST guidelines. **Mastery** = Breached password check is automated and real-time; password strength meter provides user guidance without arbitrary rules                                                                                                                |

#### V4.1.2 — Secure Biometric Authentication

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                                                    |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Biometric authentication is bound to cryptographic operations (not just a boolean flag); fallback to PIN/password is available; biometric prompts use platform-standard UI                                                                                                                                                                     |
| **Verification Procedure** | 1. Verify biometric auth uses `CryptoObject` (Android) or `LAContext` with key binding (iOS)<br>2. Verify biometric success triggers cryptographic operation (key release, signature)<br>3. Test biometric bypass: attempt to spoof biometric prompt without actual biometric<br>4. Verify fallback to PIN/password when biometric unavailable |
| **Evidence Required**      | Biometric implementation code showing crypto binding, biometric bypass test results, fallback flow documentation                                                                                                                                                                                                                               |
| **Mastery vs Met**         | **Met** = Biometric auth uses platform APIs. **Mastery** = Crypto-bound keys; bypass attempts documented and mitigated; fallback is equally secure; biometric enrollment verification                                                                                                                                                          |

#### V4.1.3 — Session Token Management

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Session tokens have defined lifecycle with expiry, refresh, revocation, and secure storage; tokens are rotated on privilege change                                                                                                                                                              |
| **Verification Procedure** | 1. Review token lifecycle: creation, storage, refresh, revocation<br>2. Verify tokens stored in Keychain/Keystore<br>3. Test token expiry and refresh flow<br>4. Test token revocation: revoke server-side, verify app handles gracefully<br>5. Verify token rotation on login/privilege change |
| **Evidence Required**      | Token lifecycle documentation, secure storage configuration, token expiry/revocation/rotation test results                                                                                                                                                                                      |
| **Mastery vs Met**         | **Met** = Token lifecycle implemented. **Mastery** = Automated token lifecycle tests; refresh token rotation (not reuse); concurrent session limits enforced; token binding to device                                                                                                           |

#### V4.1.4 — OAuth 2.0 / OIDC Compliance

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                             |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | OAuth 2.0 / OIDC implementation follows RFC 6749 / OpenID Connect Core: PKCE for public clients, state parameter, redirect URI validation, secure token handling                                                                                                                                                        |
| **Verification Procedure** | 1. Verify PKCE (code_verifier/code_challenge) is used for all OAuth flows<br>2. Verify state parameter is random and validated on callback<br>3. Verify redirect URI is validated against allowlist<br>4. Verify tokens are stored securely (not in URL, not in logs)<br>5. Test authorization code interception attack |
| **Evidence Required**      | OAuth implementation code, PKCE verification, redirect URI validation logic, authorization code interception test results                                                                                                                                                                                               |
| **Mastery vs Met**         | **Met** = OAuth follows spec. **Mastery** = Automated OAuth flow tests; PKCE enforced at code level; redirect URI validation tested against injection attacks                                                                                                                                                           |

#### V4.1.5 — Multi-Factor Authentication

| Attribute                  | Requirement                                                                                                                                                                                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mastery Criterion**      | MFA is supported with secure enrollment, backup codes, and recovery flow; recovery flow does not weaken overall authentication                                                                                                                                           |
| **Verification Procedure** | 1. Review MFA enrollment flow<br>2. Verify backup codes are single-use and securely generated<br>3. Test recovery flow: verify it requires equivalent identity proof<br>4. Verify MFA bypass is not possible through alternative auth paths<br>5. Test MFA rate limiting |
| **Evidence Required**      | MFA enrollment documentation, backup code generation and storage, recovery flow security review, MFA bypass test results                                                                                                                                                 |
| **Mastery vs Met**         | **Met** = MFA implemented with backup codes. **Mastery** = Recovery flow security-reviewed; backup codes are cryptographically random; MFA enrollment rate-limited; phishing-resistant MFA options available                                                             |

#### V4.1.6 — Account Lockout

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Account lockout prevents brute-force attacks with configurable thresholds, progressive delays, and secure unlock mechanism                                                                                                                                                                                  |
| **Verification Procedure** | 1. Review lockout threshold configuration<br>2. Test lockout trigger: attempt configured number of failed logins<br>3. Verify progressive delay increases with each failed attempt<br>4. Verify unlock mechanism does not create DoS vulnerability<br>5. Test lockout bypass through alternative auth paths |
| **Evidence Required**      | Lockout configuration, lockout trigger test results, progressive delay verification, DoS vulnerability assessment                                                                                                                                                                                           |
| **Mastery vs Met**         | **Met** = Lockout implemented. **Mastery** = Progressive delay is exponential; lockout does not enable DoS (account-specific lockout, not IP-based); automated lockout testing in CI/CD                                                                                                                     |

#### V4.1.7 — Re-Authentication for Sensitive Operations

| Attribute                  | Requirement                                                                                                                                                                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mastery Criterion**      | Sensitive operations require step-up authentication; re-auth token is short-lived; failed re-auth attempts are logged and rate-limited                                                                                                                                               |
| **Verification Procedure** | 1. Identify all sensitive operations (per SRD)<br>2. Test each operation without re-auth: verify blocked<br>3. Test re-auth mechanisms: verify they are secure<br>4. Verify re-auth token expires within ≤5 minutes<br>5. Verify failed re-auth attempts are logged and rate-limited |
| **Evidence Required**      | Sensitive operations list, re-auth test results for each operation, re-auth token expiry verification, rate limiting test results                                                                                                                                                    |
| **Mastery vs Met**         | **Met** = Re-auth required for sensitive operations. **Mastery** = Each sensitive operation tested independently; re-auth is crypto-bound; failed attempts trigger alerting                                                                                                          |

#### V4.1.8 — Rate Limiting on Auth Endpoints

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Authentication endpoints (login, password reset, MFA verification) are rate-limited at both client and server level                                                                                                                                                                               |
| **Verification Procedure** | 1. Identify all authentication endpoints<br>2. Verify rate limiting is configured per endpoint<br>3. Test rate limit trigger: send requests at configured rate<br>4. Verify rate limit response is informative but not revealing<br>5. Verify rate limit cannot be bypassed via parallel requests |
| **Evidence Required**      | Rate limiting configuration, rate limit trigger test results, parallel request bypass test                                                                                                                                                                                                        |
| **Mastery vs Met**         | **Met** = Rate limiting configured. **Mastery** = Rate limiting is adaptive (adjusts based on threat intelligence); client-side rate limiting complements server-side; rate limit events feed into SIEM                                                                                           |

#### V4.1.9 — No Hardcoded Credentials

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mastery Criterion**      | Zero hardcoded credentials, API keys, OAuth secrets, or encryption keys in source code or binaries                                                                                                                                                                                               |
| **Verification Procedure** | 1. Run secrets scanning (git-secrets, truffleHog, gitleaks) on entire repository<br>2. Run binary analysis to detect embedded secrets<br>3. Verify all secrets are loaded from secure configuration (environment variables, secret manager)<br>4. Verify pre-commit hook prevents secret commits |
| **Evidence Required**      | Secrets scan results (repository and binary), secret management configuration, pre-commit hook configuration                                                                                                                                                                                     |
| **Mastery vs Met**         | **Met** = Scan completed with no findings. **Mastery** = Pre-commit hook + CI/CD secrets scan on every PR; automated secret rotation; no secrets in build artifacts                                                                                                                              |

---

## 6. V5: Network Communication — Mastery Criteria

### 6.1 Control-by-Control Mastery Requirements

#### V5.1.1 — TLS Configuration

| Attribute                  | Requirement                                                                                                                                                                                                                                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | TLS 1.2+ is enforced; cipher suites are restricted to strong algorithms; weak algorithms (RC4, 3DES, DES, MD5) are explicitly disabled                                                                                                                      |
| **Verification Procedure** | 1. Review TLS configuration (`network_security_config.xml` / ATS settings)<br>2. Verify minimum TLS version is 1.2<br>3. Verify cipher suite allowlist excludes weak algorithms<br>4. Test with testssl.sh or equivalent: verify no weak cipher negotiation |
| **Evidence Required**      | TLS configuration files, testssl.sh results, cipher suite allowlist                                                                                                                                                                                         |
| **Mastery vs Met**         | **Met** = TLS 1.2+ configured. **Mastery** = TLS 1.3 preferred with fallback to 1.2; cipher suite allowlist is minimal; automated TLS configuration testing in CI/CD                                                                                        |

#### V5.1.2 — Certificate Chain Validation

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Full certificate chain validation is performed; hostname verification is never disabled; custom trust managers validate the complete chain                                                                                                                                                              |
| **Verification Procedure** | 1. Review certificate validation implementation<br>2. Verify hostname verification is enabled and not overridden<br>3. Test with self-signed certificate: verify rejection<br>4. Test with expired certificate: verify rejection<br>5. Test with valid certificate for wrong hostname: verify rejection |
| **Evidence Required**      | Certificate validation code, self-signed/expired/wrong-hostname test results                                                                                                                                                                                                                            |
| **Mastery vs Met**         | **Met** = Chain validation implemented. **Mastery** = All validation test cases automated; custom trust manager (if any) is security-reviewed; hostname verification cannot be disabled at runtime                                                                                                      |

#### V5.1.3 — Trusted Certificate Enforcement

| Attribute                  | Requirement                                                                                                                                                                                                                               |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | App only trusts certificates from approved CAs or pinned certificates; system CA trust store is not used without restriction                                                                                                              |
| **Verification Procedure** | 1. Review trust store configuration<br>2. Verify app does not trust all system CAs (or restricts to specific CAs)<br>3. Test with certificate from untrusted CA: verify rejection<br>4. If using pinning, verify pins cover all endpoints |
| **Evidence Required**      | Trust store configuration, untrusted CA test results, pinning coverage documentation                                                                                                                                                      |
| **Mastery vs Met**         | **Met** = Trusted certificates configured. **Mastery** = Trust store is minimal (specific CAs or pins only); automated CA rotation monitoring; pinning with backup pins                                                                   |

#### V5.1.4 — No Deprecated TLS Features

| Attribute                  | Requirement                                                                                                                                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mastery Criterion**      | SSLv3, TLS 1.0, TLS 1.1 are explicitly disabled; deprecated cipher suites (RC4, 3DES) are not available                                                                                                                  |
| **Verification Procedure** | 1. Review TLS configuration for deprecated protocol/algorithm references<br>2. Test negotiation of TLS 1.0: verify rejection<br>3. Test negotiation of TLS 1.1: verify rejection<br>4. Test RC4 cipher: verify rejection |
| **Evidence Required**      | TLS configuration, deprecated protocol/cipher rejection test results                                                                                                                                                     |
| **Mastery vs Met**         | **Met** = Deprecated features disabled. **Mastery** = Automated TLS version/cipher testing; alerts on deprecated protocol support in dependencies                                                                        |

#### V5.1.5 — Secure Connections Only

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                           |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All network connections use TLS; no cleartext traffic exceptions; ATS configured to disallow arbitrary loads (iOS); cleartext traffic disabled (Android)                                                                                                                                              |
| **Verification Procedure** | 1. Review network configuration for cleartext exceptions<br>2. Verify `android:usesCleartextTraffic="false"` (Android)<br>3. Verify `NSAllowsArbitraryLoads = false` (iOS)<br>4. Test all network connections: verify none are cleartext<br>5. Review any exception domains: verify each is justified |
| **Evidence Required**      | Network configuration files, cleartext traffic test results, exception domain justification (if any)                                                                                                                                                                                                  |
| **Mastery vs Met**         | **Met** = No cleartext traffic. **Mastery** = Zero exception domains; automated cleartext detection in CI/CD; any cleartext attempt causes build failure                                                                                                                                              |

#### V5.1.6 — Certificate Pinning (Network)

| Attribute                  | Requirement                                                                                                                                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Certificate pinning is implemented for all production endpoints; pin rotation is tested; pin failure does not fall back to trust system CA                                                                                 |
| **Verification Procedure** | 1. Review pinning implementation<br>2. Verify pins cover all production domains<br>3. Test pin rotation procedure<br>4. Test pin failure behavior: verify no fallback to system CA<br>5. Verify backup pins are configured |
| **Evidence Required**      | Pinning configuration, pin rotation test report, pin failure behavior documentation, backup pin configuration                                                                                                              |
| **Mastery vs Met**         | **Met** = Pinning implemented. **Mastery** = Backup pins configured; rotation tested within 90 days; automated pin expiry alerts; pinning bypass resistance tested                                                         |

#### V5.1.7 — TLS Downgrade Protection

| Attribute                  | Requirement                                                                                                                                                                                                        |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mastery Criterion**      | App protects against TLS downgrade attacks; HSTS headers are present on all endpoints; TLS_FALLBACK_SCSV is supported                                                                                              |
| **Verification Procedure** | 1. Verify TLS_FALLBACK_SCSV is enabled<br>2. Review server HSTS header configuration<br>3. Test TLS downgrade attempt: verify connection is rejected<br>4. Verify HSTS preload list inclusion for critical domains |
| **Evidence Required**      | TLS_FALLBACK_SCSV configuration, HSTS header review, TLS downgrade test results                                                                                                                                    |
| **Mastery vs Met**         | **Met** = Downgrade protection configured. **Mastery** = HSTS preloaded for all critical domains; automated downgrade protection testing; server-side TLS configuration monitored                                  |

---

## 7. V6: Platform Interaction — Mastery Criteria

### 7.1 Control-by-Control Mastery Requirements

#### V6.1.1 — Secured Intents/URL Schemes

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mastery Criterion**      | All exported components (activities, services, receivers, providers) have appropriate permission guards; URL schemes validate incoming data                                                                                                                                                |
| **Verification Procedure** | 1. Review Android manifest for `exported` components<br>2. Verify each exported component has permission guard or explicit `exported="false"`<br>3. Review iOS URL schemes: verify handled URLs validate incoming data<br>4. Test intent/URL injection: verify malformed input is rejected |
| **Evidence Required**      | Manifest review, URL scheme validation logic, intent/URL injection test results                                                                                                                                                                                                            |
| **Mastery vs Met**         | **Met** = Exported components reviewed. **Mastery** = Automated manifest audit; any new exported component requires security review; URL scheme validation tested against OWASP test cases                                                                                                 |

#### V6.1.2 — Deep Link/Universal Link Validation

| Attribute                  | Requirement                                                                                                                                                                                                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Deep links and universal links are validated against allowlist; incoming link data is sanitized before use                                                                                                                                                                |
| **Verification Procedure** | 1. Review deep link/universal link configuration<br>2. Verify link association files (assetlinks.json / apple-app-site-association) are correct<br>3. Verify incoming link data is validated before use<br>4. Test deep link injection: verify malicious link is rejected |
| **Evidence Required**      | Deep link configuration, link association files, deep link injection test results                                                                                                                                                                                         |
| **Mastery vs Met**         | **Met** = Deep links validated. **Mastery** = Automated deep link validation tests; allowlist is version-controlled; any new deep link requires security review                                                                                                           |

#### V6.1.3 — No IPC Data Leakage

| Attribute                  | Requirement                                                                                                                                                                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mastery Criterion**      | ContentProviders, XPC services, and App Groups do not expose sensitive data; shared data is encrypted or access-controlled                                                                                                                                                           |
| **Verification Procedure** | 1. Inventory all IPC data sharing mechanisms<br>2. Verify ContentProviders have appropriate permission guards<br>3. Verify XPC services have entitlement validation<br>4. Verify App Group data is encrypted<br>5. Test IPC data extraction: verify sensitive data is not accessible |
| **Evidence Required**      | IPC inventory, permission/entitlement configuration, IPC data extraction test results                                                                                                                                                                                                |
| **Mastery vs Met**         | **Met** = IPC mechanisms reviewed. **Mastery** = Automated IPC data flow analysis; all IPC channels have explicit access controls; data extraction tests prove protection                                                                                                            |

#### V6.1.4 — External Data Validation

| Attribute                  | Requirement                                                                                                                                                                                                           |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All data received from external sources (IPC, network, files, user input) is validated before use                                                                                                                     |
| **Verification Procedure** | 1. Identify all external data entry points<br>2. Verify input validation at each entry point<br>3. Test with malformed input: verify graceful rejection<br>4. Verify validation is defense-in-depth (client + server) |
| **Evidence Required**      | External data entry point inventory, input validation code, malformed input test results                                                                                                                              |
| **Mastery vs Met**         | **Met** = Input validation implemented. **Mastery** = Automated fuzzing of all entry points; validation rules are version-controlled; validation coverage tracked in CI/CD                                            |

#### V6.1.5 — Secure WebView Usage

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                 |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | WebView has JavaScript disabled by default; no `addJavascriptInterface` (Android); no `JSContext` injection (iOS); URL allowlist enforced                                                                                                                                                   |
| **Verification Procedure** | 1. Review all WebView instances<br>2. Verify JavaScript is disabled by default<br>3. Verify no `addJavascriptInterface` usage (Android)<br>4. Verify no `JSContext` injection (iOS)<br>5. Verify URL allowlist is enforced<br>6. Test WebView XSS: verify injected scripts are not executed |
| **Evidence Required**      | WebView configuration, URL allowlist, WebView XSS test results                                                                                                                                                                                                                              |
| **Mastery vs Met**         | **Met** = WebView configured securely. **Mastery** = Automated WebView security scanning; any WebView changes require security review; XSS tests run in CI/CD                                                                                                                               |

#### V6.1.6 — Background Data Protection

| Attribute                  | Requirement                                                                                                                                                                                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | App does not process sensitive data in background; background execution is restricted for sensitive operations                                                                                                                                                             |
| **Verification Procedure** | 1. Review background execution code<br>2. Verify sensitive operations (auth, crypto, data processing) pause on background<br>3. Verify sensitive data is cleared from memory on background<br>4. Test: background app during sensitive operation, verify data is protected |
| **Evidence Required**      | Background execution review, memory clearing code, background protection test results                                                                                                                                                                                      |
| **Mastery vs Met**         | **Met** = Background protection implemented. **Mastery** = Automated background state testing; memory dump on background proves data clearing; regression tests prevent removal                                                                                            |

#### V6.1.7 — Runtime Permission Requests

| Attribute                  | Requirement                                                                                                                                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All dangerous permissions are requested at runtime with user-facing context; permission rationale is provided; permission denial is handled gracefully                                                                      |
| **Verification Procedure** | 1. Review all runtime permission requests<br>2. Verify each request includes user-facing rationale<br>3. Verify permission denial is handled gracefully<br>4. Test permission request flow: verify user experience is clear |
| **Evidence Required**      | Runtime permission request code, permission rationale text, permission denial handling test results                                                                                                                         |
| **Mastery vs Met**         | **Met** = Runtime permissions requested. **Mastery** = Permission request timing is contextual (not at app launch); denial handling preserves core functionality; permission request A/B tested for user comprehension      |

#### V6.1.8 — URL Scheme Collision Protection

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | App URL scheme is unique and registered; incoming URLs are validated to prevent collision-based attacks                                                                                                                                                                                         |
| **Verification Procedure** | 1. Verify URL scheme uniqueness (reverse domain notation)<br>2. Verify URL scheme is registered (Android: intent-filter; iOS: CFBundleURLSchemes)<br>3. Verify incoming URLs are validated against expected format<br>4. Test URL scheme collision: verify app does not process unintended URLs |
| **Evidence Required**      | URL scheme registration, URL validation logic, collision test results                                                                                                                                                                                                                           |
| **Mastery vs Met**         | **Met** = URL scheme registered and validated. **Mastery** = URL scheme is cryptographically unique; incoming URL validation tested against known collision patterns; automated URL scheme scanning in CI/CD                                                                                    |

---

## 8. V7: Code Quality and Build Settings — Mastery Criteria

### 8.1 Control-by-Control Mastery Requirements

#### V7.1.1 — Security-Focused Build Flags

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Native code is compiled with: Stack Canary, ASLR, DEP/NX, PIE; build configuration is verified in CI/CD                                                                                                                                                                                                                    |
| **Verification Procedure** | 1. Review build configuration for native code (CMake, ndk-build, Xcode build settings)<br>2. Verify Stack Canary is enabled (`-fstack-protector-strong`)<br>3. Verify ASLR is enabled (PIE: `-fPIE -pie`)<br>4. Verify DEP/NX is enabled (`-z noexecstack`)<br>5. Verify with `readelf` or `checksec` on compiled binaries |
| **Evidence Required**      | Build configuration files, `checksec` / `readelf` output on compiled binaries, CI/CD build flag verification                                                                                                                                                                                                               |
| **Mastery vs Met**         | **Met** = Build flags configured. **Mastery** = Automated `checksec` verification on every build; any missing flag causes build failure; build configuration is version-controlled                                                                                                                                         |

#### V7.1.2 — No Unnecessary Code or Resources

| Attribute                  | Requirement                                                                                                                                                                                                                                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Release builds use code shrinking (R8/ProGuard); unused resources are removed; debug code is stripped                                                                                                                                                       |
| **Verification Procedure** | 1. Review R8/ProGuard configuration<br>2. Verify code shrinking is enabled for release builds<br>3. Verify resource shrinking is enabled<br>4. Verify debug code is stripped (BuildConfig.DEBUG checks)<br>5. Compare release APK/IPA size with debug build |
| **Evidence Required**      | R8/ProGuard configuration, resource shrinking configuration, release vs debug build size comparison                                                                                                                                                         |
| **Mastery vs Met**         | **Met** = Code shrinking enabled. **Mastery** = Automated size comparison in CI/CD; unused code detection flags new code; ProGuard rules are version-controlled and reviewed                                                                                |

#### V7.1.3 — Proper Error Handling

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                       |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Release builds do not expose stack traces or error details; errors are handled gracefully with user-friendly messages; errors are logged securely                                                                                                                                                                 |
| **Verification Procedure** | 1. Review error handling code<br>2. Verify stack traces are not included in release build error messages<br>3. Verify error messages are user-friendly but not revealing<br>4. Verify errors are logged to secure logging (not logcat/Console in release)<br>5. Test error scenarios: verify graceful degradation |
| **Evidence Required**      | Error handling code review, release build error message samples, secure logging configuration                                                                                                                                                                                                                     |
| **Mastery vs Met**         | **Met** = Error handling reviewed. **Mastery** = Automated error message scanning in CI/CD; all error paths tested; error handling is part of code review checklist                                                                                                                                               |

#### V7.1.4 — No Sensitive Data in Logs

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Release builds have logging disabled or scrubbed; no sensitive data (credentials, tokens, PII) appears in any log output                                                                                                                                                                                                   |
| **Verification Procedure** | 1. Review logging implementation<br>2. Verify logging is disabled or uses release-safe logger in release builds<br>3. Run automated log scan: search for sensitive data patterns in log output<br>4. Verify `BuildConfig.DEBUG` guards all debug logging (Android)<br>5. Verify `#if DEBUG` guards all debug logging (iOS) |
| **Evidence Required**      | Logging configuration, log scan results, debug guard verification                                                                                                                                                                                                                                                          |
| **Mastery vs Met**         | **Met** = Logging disabled in release. **Mastery** = Automated log scanning in CI/CD; SAST rule detects sensitive data in log statements; pre-commit hook prevents debug logging without guards                                                                                                                            |

#### V7.1.5 — Dependency Currency

| Attribute                  | Requirement                                                                                                                                                                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | All third-party dependencies are within 2 minor versions of latest stable; dependencies with known critical vulnerabilities are updated within 48 hours                                                                                                 |
| **Verification Procedure** | 1. Run SCA scan (Snyk/Dependabot/OSS Index) on all dependencies<br>2. Verify no dependencies with critical or high CVEs<br>3. Verify dependency versions are within support window<br>4. Review dependency update timeline for any recent critical CVEs |
| **Evidence Required**      | SCA scan results, dependency version report, CVE remediation timeline for any identified vulnerabilities                                                                                                                                                |
| **Mastery vs Met**         | **Met** = Dependencies are current and clean. **Mastery** = Automated SCA scanning on every PR; auto-PR generation for vulnerable dependencies; SBOM generated per build; dependency update SLA tracked                                                 |

#### V7.1.6 — Anti-Debugging Protections

| Attribute                  | Requirement                                                                                                                                                                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Release builds include anti-debugging checks; debuggers are detected and app responds appropriately                                                                                                                                               |
| **Verification Procedure** | 1. Review anti-debugging implementation<br>2. Verify `android:debuggable="false"` in release manifest<br>3. Verify `ptrace` protection (iOS)<br>4. Verify Frida/Xposed detection<br>5. Test with debugger attached: verify detection and response |
| **Evidence Required**      | Anti-debugging code, debugger attachment test results, Frida/Xposed detection test results                                                                                                                                                        |
| **Mastery vs Met**         | **Met** = Anti-debugging implemented. **Mastery** = Multiple anti-debugging techniques (not single check); detection is runtime-continuous; bypass attempts documented and mitigated; anti-debugging tested in CI/CD with instrumentation         |

#### V7.1.7 — Code Obfuscation

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Release builds are obfuscated to prevent reverse engineering; class names, method names, and string literals are obfuscated                                                                                                                                                                                 |
| **Verification Procedure** | 1. Review ProGuard/R8 obfuscation rules<br>2. Verify class and method name obfuscation is enabled<br>3. Verify string encryption (if implemented)<br>4. Test decompilation of release build: verify obfuscation effectiveness<br>5. Verify obfuscation mapping is stored securely (for crash symbolication) |
| **Evidence Required**      | Obfuscation configuration, decompilation test results, obfuscation mapping storage procedure                                                                                                                                                                                                                |
| **Mastery vs Met**         | **Met** = Obfuscation enabled. **Mastery** = Obfuscation effectiveness measured (decompilation analysis); string encryption for sensitive strings; obfuscation rules are version-controlled and reviewed                                                                                                    |

---

## 9. V8: Resilience — Selected L2 Controls in Track A

### 9.1 Control-by-Control Mastery Requirements

#### V8.1.1 — Root/Jailbreak Detection

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Multi-method root/jailbreak detection is implemented; detection triggers appropriate response (block, restrict, or alert); detection is resistant to common bypass techniques                                                                                                                                                          |
| **Verification Procedure** | 1. Review root/jailbreak detection implementation<br>2. Verify multiple detection methods are used (not single check)<br>3. Test on clean device: verify no false positives<br>4. Test on rooted/jailbroken device: verify detection triggers<br>5. Test bypass attempts (Frida hooking, Magisk Hide): verify detection still triggers |
| **Evidence Required**      | Root detection implementation code, false positive test results, rooted device detection test results, bypass resistance test results                                                                                                                                                                                                  |
| **Mastery vs Met**         | **Met** = Root detection implemented. **Mastery** = Multi-method detection (≥3 independent methods); bypass resistance proven; detection response is policy-appropriate; detection updated with new root methods                                                                                                                       |

#### V8.2.1 — Tampering Detection

| Attribute                  | Requirement                                                                                                                                                                                                                                                                   |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | App detects code and data tampering at runtime; modified app cannot connect to production APIs                                                                                                                                                                                |
| **Verification Procedure** | 1. Review tampering detection implementation<br>2. Verify code signature verification at runtime<br>3. Verify integrity checks on critical code paths<br>4. Test with modified APK/IPA: verify detection triggers<br>5. Verify modified app cannot connect to production APIs |
| **Evidence Required**      | Tampering detection code, modified binary test results, API connection test for modified app                                                                                                                                                                                  |
| **Mastery vs Met**         | **Met** = Tampering detection implemented. **Mastery** = Multiple integrity checks (signature + hash + runtime); detection is continuous (not just at launch); tampering response prevents all production access                                                              |

#### V8.3.2 — Hooking Framework Detection

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                        |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | App detects and responds to runtime hooking frameworks (Frida, Xposed, Substrate); hooking detection is resistant to bypass                                                                                                                                                                        |
| **Verification Procedure** | 1. Review hooking detection implementation<br>2. Verify detection of Frida server, frida-gadget, Frida indicators<br>3. Verify detection of Xposed modules (Android)<br>4. Test with Frida attached: verify detection triggers<br>5. Test with Frida stealth mode: verify detection still triggers |
| **Evidence Required**      | Hooking detection code, Frida detection test results, Xposed detection test results, stealth mode bypass test results                                                                                                                                                                              |
| **Mastery vs Met**         | **Met** = Hooking detection implemented. **Mastery** = Detection covers multiple frameworks; stealth mode resistance proven; detection is continuous; hooking events feed into SIEM                                                                                                                |

#### V8.4.2 — Anti-Debugging Measures

| Attribute                  | Requirement                                                                                                                                                                                                                                                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mastery Criterion**      | Multiple anti-debugging techniques are implemented; debugger attachment is detected and responded to; anti-debugging cannot be bypassed via single technique                                                                                                                                                              |
| **Verification Procedure** | 1. Review anti-debugging implementation<br>2. Verify multiple techniques (debug flag, ptrace, timing checks, emulator detection)<br>3. Test with debugger attached: verify detection<br>4. Test with debugger in stealth mode: verify detection<br>5. Verify anti-debugging cannot be bypassed by hooking single function |
| **Evidence Required**      | Anti-debugging code, debugger detection test results, stealth mode test results, bypass resistance analysis                                                                                                                                                                                                               |
| **Mastery vs Met**         | **Met** = Anti-debugging implemented. **Mastery** = Multiple independent techniques; continuous detection (not just at launch); bypass resistance proven; anti-debugging tested in automated pipeline                                                                                                                     |

---

## 10. Mastery Evidence Requirements

### 10.1 Evidence Classification

| Evidence Type          | Description                                                           | Mastery Requirement                                              |
| ---------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Static Evidence**    | Configuration files, source code, build settings, SAST results        | Must be version-controlled and traceable to specific commit      |
| **Dynamic Evidence**   | Runtime test results, penetration test findings, behavior observation | Must be reproducible with documented test procedure              |
| **Automated Evidence** | CI/CD pipeline results, automated scan outputs, continuous monitoring | Must run on every build or PR; results must be persisted         |
| **Manual Evidence**    | Expert review findings, threat model analysis, architecture review    | Must be documented with reviewer identity, date, and conclusions |

### 10.2 Evidence Package Structure

For each MASVS control assessed, the mastery evidence package must contain:

```
masvs-evidence/
├── V1/
│   ├── V1.1.1/
│   │   ├── static/          # SRD, pipeline configs, sign-off docs
│   │   ├── dynamic/         # Test results demonstrating security gates
│   │   ├── automated/       # CI/CD scan results
│   │   └── manual/          # Expert review notes
│   ├── V1.1.2/
│   │   └── ...
│   └── ...
├── V2/
│   └── ...
├── ...
└── SUMMARY.md               # Mastery status summary for all controls
```

### 10.3 Mastery vs Met vs Not Met — Decision Matrix

| Control Status | Evidence Completeness             | Automation Level                | Reproducibility                                     | Auditor Confidence                        |
| -------------- | --------------------------------- | ------------------------------- | --------------------------------------------------- | ----------------------------------------- |
| **MASTERY**    | 100% of evidence types present    | Automated verification in CI/CD | Any auditor can reproduce with documented procedure | High — evidence is self-defending         |
| **MET**        | Static + manual evidence present  | Manual or periodic verification | Reproducible with expert guidance                   | Medium — evidence requires interpretation |
| **NOT MET**    | Evidence missing or contradictory | No verification                 | Cannot be reproduced                                | Low — control requires remediation        |

### 10.4 Continuous Mastery Maintenance

| Activity                            | Frequency         | Owner                         | Automation     |
| ----------------------------------- | ----------------- | ----------------------------- | -------------- |
| SAST scan (MASVS rules)             | Every PR          | CTO (pipeline)                | Automated      |
| SCA scan (dependency CVEs)          | Every PR          | CTO (pipeline)                | Automated      |
| Secrets scan (gitleaks)             | Every commit      | CTO (pipeline)                | Automated      |
| DAST scan (OWASP ZAP)               | Nightly           | James Wright                  | Automated      |
| MASVS compliance matrix update      | Per release       | James Wright                  | Semi-automated |
| Penetration test (MASVS validation) | Per major release | Sana Khoury                   | Manual         |
| Audit evidence package assembly     | Per audit cycle   | James Wright + Ingrid Solberg | Semi-automated |

---

## 11. Stage 6 Defect Classification — MASVS Findings

### 11.1 Classification Principles

MASVS findings are classified using the P0–P3 defect severity system. The classification is based on **security impact**, not compliance status.

### 11.2 P0 — Security Breach / Data Loss

| MASVS Category     | P0 Finding Examples                                                                 |
| ------------------ | ----------------------------------------------------------------------------------- |
| V2: Data Storage   | Plaintext credentials or encryption keys in app filesystem                          |
| V3: Cryptography   | Custom crypto algorithm; hardcoded encryption key; ECB mode for sensitive data      |
| V4: Authentication | No authentication on sensitive endpoints; hardcoded credentials; OAuth without PKCE |
| V5: Network        | Cleartext transmission of credentials; no TLS; certificate validation disabled      |
| V7: Code Quality   | Debug build released with logging enabled and secrets exposed                       |

**Release Impact:** Non-negotiable release blocker. Must be remediated before Stage 6 sign-off.

### 11.3 P1 — Core Feature Broken / Major Security Weakness

| MASVS Category     | P1 Finding Examples                                                                                |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| V1: Architecture   | No threat model for sensitive feature; unvetted SDK with known critical CVE                        |
| V2: Data Storage   | Sensitive data in backups without encryption; keyboard cache exposure of passwords                 |
| V3: Cryptography   | Deprecated algorithm (3DES, MD5); non-secure RNG for token generation                              |
| V4: Authentication | Session token without expiry; no rate limiting on auth endpoints; biometric without crypto binding |
| V5: Network        | Missing certificate pinning for high-risk endpoints; TLS 1.0/1.1 support                           |
| V6: Platform       | WebView with JS enabled and no URL allowlist; exported component without permission guard          |
| V7: Code Quality   | No code obfuscation; stack traces in release build error messages                                  |

**Release Impact:** Non-negotiable release blocker. Must be remediated before Stage 6 sign-off.

### 11.4 P2 — Minor Feature Degraded / Security Improvement

| MASVS Category     | P2 Finding Examples                                                                    |
| ------------------ | -------------------------------------------------------------------------------------- |
| V1: Architecture   | Dependency update automation not implemented; SBOM not generated per build             |
| V2: Data Storage   | Auto-deletion not covering all cache locations; generated file permissions not optimal |
| V3: Cryptography   | Key rotation not automated; IV generation not using CSPRNG (but still unique)          |
| V4: Authentication | MFA recovery flow could be strengthened; password policy not fully NIST-aligned        |
| V5: Network        | Certificate pinning without backup pins; HSTS not preloaded                            |
| V6: Platform       | URL scheme not using reverse domain notation; permission rationale could be clearer    |
| V7: Code Quality   | Obfuscation rules not covering all classes; resource shrinking not fully optimized     |

**Release Impact:** User decides to fix or defer. If deferred, must have documented remediation plan with target date.

### 11.5 P3 — Polish / Nice-to-Have

| MASVS Category     | P3 Finding Examples                                                                           |
| ------------------ | --------------------------------------------------------------------------------------------- |
| V1: Architecture   | Threat model documentation could be more detailed                                             |
| V2: Data Storage   | Data retention policy documentation could include more examples                               |
| V3: Cryptography   | Crypto library could be upgraded to latest minor version (current version is still supported) |
| V4: Authentication | MFA enrollment UX could be improved                                                           |
| V5: Network        | TLS configuration could prefer TLS 1.3 over 1.2 (1.2 is still acceptable)                     |
| V6: Platform       | Permission request timing could be more contextual                                            |
| V7: Code Quality   | Build size could be reduced with additional resource shrinking                                |

**Release Impact:** User decides to fix or defer. No remediation plan required for deferral.

### 11.6 Defect Classification Decision Tree

```
Is sensitive data (credentials, keys, PII, financial data) exposed in plaintext or cleartext?
├── YES → P0
└── NO → Is a core security control (auth, encryption, TLS, certificate validation) absent or disabled?
    ├── YES → P1
    └── NO → Is a security control partially implemented or could be strengthened?
        ├── YES → P2
        └── NO → Is this a best practice improvement with minimal security impact?
            ├── YES → P3
            └── NO → Not a security finding
```

---

## 12. Audit Defensibility — Presenting Mastery Evidence

### 12.1 Auditor Expectations

External auditors (SOC 2, PCI-DSS, ISO 27001) expect:

| Auditor Requirement               | MASVS Track A Mapping               | Evidence Provided                           |
| --------------------------------- | ----------------------------------- | ------------------------------------------- |
| **Security controls are defined** | MASVS V1–V7 control descriptions    | This document + `owasp-masvs-compliance.md` |
| **Controls are implemented**      | Mastery evidence per control        | Evidence package (Section 10.2)             |
| **Controls are tested**           | Verification procedures per control | Test results in evidence package            |
| **Controls are monitored**        | CI/CD pipeline integration          | Pipeline configs, scan results              |
| **Controls are maintained**       | Continuous mastery maintenance      | Maintenance schedule, remediation tracking  |
| **Controls are reviewed**         | Stage 6/8/10 sign-offs              | Sign-off documents, panel reports           |

### 12.2 Evidence Presentation Strategy

**For SOC 2 Auditors:**

1. Present MASVS Track A as the control framework (maps to SOC 2 Trust Services Criteria)
2. Show evidence package for each control with mastery status
3. Demonstrate CI/CD pipeline automation for continuous control verification
4. Provide defect tracking showing P0/P1 findings are remediated before release

**For PCI-DSS Auditors:**

1. Map MASVS V2 (data storage), V3 (cryptography), V5 (network) to PCI-DSS requirements 3, 4, 6
2. Show encryption key management evidence (V3.1.4)
3. Show TLS configuration evidence (V5.1.1–V5.1.7)
4. Show code review and vulnerability management evidence (V7)

**For ISO 27001 Auditors:**

1. Map MASVS Track A to ISO 27001 Annex A controls (A.9 Access Control, A.10 Cryptography, A.12 Operations, A.14 System Development)
2. Show risk assessment linkage (threat model → MASVS controls → evidence)
3. Show continuous monitoring and improvement evidence
4. Provide audit trail for all security decisions

### 12.3 Audit Readiness Checklist

| Readiness Item                                                      | Status | Owner                |
| ------------------------------------------------------------------- | ------ | -------------------- |
| MASVS Track A evidence package complete for all 59 controls         | ☐      | James Wright         |
| All P0/P1 findings remediated with evidence                         | ☐      | James Wright + CTO   |
| CI/CD pipeline security scans documented                            | ☐      | CTO                  |
| Penetration test results from Sana Khoury available                 | ☐      | Sana Khoury          |
| MASVS compliance report from Ingrid Solberg available               | ☐      | Ingrid Solberg       |
| Stage 6 Defect Report signed off                                    | ☐      | CTO Panel            |
| Stage 8 Integrity Verification signed off                           | ☐      | CTO Panel            |
| Stage 10 Release Checklist Item #4 (CSO security sign-off) complete | ☐      | CSO (Dr. Sarah Chen) |

### 12.4 Common Auditor Questions and Prepared Responses

| Auditor Question                                      | Prepared Response                                                                                                                                               | Supporting Evidence                                               |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| "How do you ensure security controls don't regress?"  | CI/CD pipeline runs automated security scans (SAST, SCA, secrets) on every PR and build; any regression causes build failure                                    | Pipeline configuration, scan results, build failure logs          |
| "Who verifies the security controls are effective?"   | Independent verification by CSO (Dr. Sarah Chen) at Stage 6/8/10; penetration testing by Sana Khoury; MASVS compliance audit by Ingrid Solberg                  | Stage 6/8/10 sign-offs, pen test reports, audit reports           |
| "How do you handle newly discovered vulnerabilities?" | Automated SCA scanning detects new CVEs; SLA tracking ensures remediation within 48h (critical), 7d (high); escalation to CTO on SLA breach                     | SCA scan results, remediation timeline, escalation logs           |
| "What is your process for third-party SDK security?"  | SDK vetting checklist before integration; SBOM generation for all dependencies; continuous CVE monitoring; removal process for abandoned SDKs                   | SDK vetting docs, SBOM, CVE monitoring alerts                     |
| "How do you protect cryptographic keys?"              | Hardware-backed storage (Secure Enclave / StrongBox); keys never leave secure hardware; authentication binding for sensitive operations; automated key rotation | Key management code, hardware storage confirmation, rotation logs |

---

## Appendix A — Track A to SOC 2 Trust Services Criteria Mapping

| MASVS Category     | SOC 2 TSC    | Description                                |
| ------------------ | ------------ | ------------------------------------------ |
| V1: Architecture   | CC6.1, CC7.1 | Logical access security, system monitoring |
| V2: Data Storage   | CC6.6, CC6.7 | Data encryption, data integrity            |
| V3: Cryptography   | CC6.6        | Cryptographic controls                     |
| V4: Authentication | CC6.1, CC6.2 | User authentication, authorization         |
| V5: Network        | CC6.6, CC6.7 | Network security, data transmission        |
| V6: Platform       | CC6.1, CC6.6 | Platform security, data handling           |
| V7: Code Quality   | CC8.1, CC9.1 | Change management, risk mitigation         |

## Appendix B — Track A to PCI-DSS Mapping

| MASVS Category   | PCI-DSS Requirement         | Description                                      |
| ---------------- | --------------------------- | ------------------------------------------------ |
| V2: Data Storage | Req 3: Protect stored data  | Encryption of cardholder data                    |
| V3: Cryptography | Req 3, Req 4                | Strong cryptography for storage and transmission |
| V5: Network      | Req 4: Encrypt transmission | TLS for cardholder data in transit               |
| V7: Code Quality | Req 6: Secure systems       | Secure development, vulnerability management     |

## Appendix C — Version History

| Version | Date       | Author       | Changes                                                                                                                                                          |
| ------- | ---------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v1      | 2026-04-06 | James Wright | Initial authoring — MASVS Track A mastery criteria for all 8 categories (V1–V7 L1 + V8 L2-selected), Stage 6 defect classification, audit defensibility guidance |

---

_End of MASVS Mastery Track A skill file. Authored by James Wright, Lead Security Engineer — Security Operations & Application Security._
