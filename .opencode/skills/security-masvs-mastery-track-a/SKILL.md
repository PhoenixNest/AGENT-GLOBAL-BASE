---
name: security-masvs-mastery-track-a
description: MASVS Mastery Track A — deep security verification for CSO and Security Engineers covering all V1-V8 MASVS categories, advanced penetration testing techniques, cryptographic validation, and security architecture audit methodologies. Owned by James Wright (Security Lead). Use during Stage 6 (Code Review) for security verification and Stage 8 (Integrity Verification) for deep security audit. Trigger: MASVS Track A, security verification, penetration testing, cryptographic validation, security audit, MASVS V1-V8, advanced security testing.
prerequisites:
  - security-overview

version: "1.0.0"
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

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`4.-v3:-cryptography-—-mastery-criteria.md`](references/4.-v3:-cryptography-—-mastery-criteria.md) — 4. V3: Cryptography — Mastery Criteria
- [`5.-v4:-authentication-and-session-management-—-mastery-criteria.md`](references/5.-v4:-authentication-and-session-management-—-mastery-criteria.md) — 5. V4: Authentication and Session Management — Mastery Criteria
- [`6.-v5:-network-communication-—-mastery-criteria.md`](references/6.-v5:-network-communication-—-mastery-criteria.md) — 6. V5: Network Communication — Mastery Criteria
- [`7.-v6:-platform-interaction-—-mastery-criteria.md`](references/7.-v6:-platform-interaction-—-mastery-criteria.md) — 7. V6: Platform Interaction — Mastery Criteria
- [`8.-v7:-code-quality-and-build-settings-—-mastery-criteria.md`](references/8.-v7:-code-quality-and-build-settings-—-mastery-criteria.md) — 8. V7: Code Quality and Build Settings — Mastery Criteria
- [`9.-v8:-resilience-—-selected-l2-controls-in-track-a.md`](references/9.-v8:-resilience-—-selected-l2-controls-in-track-a.md) — 9. V8: Resilience — Selected L2 Controls in Track A
- [`10.-mastery-evidence-requirements.md`](references/10.-mastery-evidence-requirements.md) — 10. Mastery Evidence Requirements
- [`11.-stage-6-defect-classification-—-masvs-findings.md`](references/11.-stage-6-defect-classification-—-masvs-findings.md) — 11. Stage 6 Defect Classification — MASVS Findings
- [`12.-audit-defensibility-—-presenting-mastery-evidence.md`](references/12.-audit-defensibility-—-presenting-mastery-evidence.md) — 12. Audit Defensibility — Presenting Mastery Evidence
- [`appendix-b-—-track-a-to-pci-dss-mapping.md`](references/appendix-b-—-track-a-to-pci-dss-mapping.md) — Appendix B — Track A to PCI-DSS Mapping
- [`appendix-c-—-version-history.md`](references/appendix-c-—-version-history.md) — Appendix C — Version History
