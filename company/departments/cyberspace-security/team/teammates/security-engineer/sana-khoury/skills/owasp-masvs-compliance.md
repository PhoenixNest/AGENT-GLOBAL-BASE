---
version: "1.0.0"
---

------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MASVS Framework Mastery | Complete understanding of all 8 verification categories and 2 assessment levels | Accurately maps any mobile security finding to specific MASVS requirement; distinguishes L1 vs L2 requirements; understands MASVS-R (resilience) requirements |
| Verification Procedure Design | Ability to design test procedures for each MASVS requirement | Creates reproducible test cases for every MASVS control; produces assessment matrices that auditors can independently verify |
| Compliance Assessment Execution | Conducting systematic MASVS assessments against live applications | Completes full MASVS assessment in ≤5 business days; identifies compliance gaps with zero false negatives on L1 controls |
| Gap Analysis & Remediation | Translating compliance gaps into actionable remediation plans | Produces prioritized remediation roadmaps with effort estimates; tracks remediation to closure with evidence |
| Audit Reporting | Producing MASVS compliance reports for internal and external stakeholders | Generates reports that satisfy SOC 2, PCI-DSS, and ISO 27001 auditors; maintains audit trail for all assessments |
| Continuous Compliance | Integrating MASVS checks into CI/CD pipelines | Automates 60%+ of L1 control verification through SAST/DAST rules; maintains compliance dashboard with real-time status |

## Execution Guidance

### 1. MASVS Framework Structure

The OWASP MASVS defines **8 verification categories** across **2 assessment levels**:

| Category                                       | ID  | Description                                                      | Level 1             | Level 2             |
| ---------------------------------------------- | --- | ---------------------------------------------------------------- | ------------------- | ------------------- |
| **V1: Architecture, Design & Threat Modeling** | V1  | Systematic approach to security design and threat identification | ✓ (8 requirements)  | ✓ (3 additional)    |
| **V2: Data Storage & Privacy**                 | V2  | Protection of data at rest and privacy-preserving practices      | ✓ (10 requirements) | ✓ (3 additional)    |
| **V3: Cryptography**                           | V3  | Proper use of cryptographic primitives and key management        | ✓ (6 requirements)  | ✓ (3 additional)    |
| **V4: Authentication & Session Management**    | V4  | User identity verification and secure session handling           | ✓ (9 requirements)  | ✓ (4 additional)    |
| **V5: Network Communication**                  | V5  | Secure transmission of data over networks                        | ✓ (7 requirements)  | ✓ (3 additional)    |
| **V6: Platform Interaction**                   | V6  | Secure use of platform IPC, intents, and inter-app communication | ✓ (8 requirements)  | ✓ (2 additional)    |
| **V7: Code Quality & Build Settings**          | V7  | Code-level security hygiene and compiler/build protections       | ✓ (7 requirements)  | ✓ (2 additional)    |
| **V8: Resilience**                             | V8  | Anti-reversing, anti-tampering, and runtime protection           | —                   | ✓ (11 requirements) |

**Level Definitions:**

- **MASVS Level 1 (L1)**: Baseline security controls expected of all mobile applications. Covers secure defaults, proper platform usage, and common vulnerability prevention.
- **MASVS Level 2 (L2)**: Defense-in-depth controls for applications handling sensitive data or operating in adversarial environments. Includes V8 resilience requirements.
- **MASVS Privacy (MASVS-P)**: Optional privacy-specific verification category (emerging; track OWASP updates).

### 2. Assessment Methodology

**Phase 1: Scoping & Baseline (Day 1)**

1. **Determine assessment level**: L1 for all apps; L2 for apps handling financial transactions, PII, health data, or authentication credentials
2. **Gather application artifacts**: APK/IPA binary, source code access (if available), architecture diagrams, threat model from SRD, previous assessment reports
3. **Create assessment matrix**: Spreadsheet mapping each MASVS requirement to planned verification method (static analysis, dynamic analysis, manual review, automated tool)
4. **Identify platform-specific requirements**: Note iOS-specific controls (Keychain, Secure Enclave, App Transport Security) vs Android-specific controls (Keystore, SafetyNet/Play Integrity, SELinux)

**Phase 2: Category-by-Category Assessment (Days 2–4)**

#### V1: Architecture, Design & Threat Modeling

| Req ID | Requirement (L1)                                                  | Verification Method                                              |
| ------ | ----------------------------------------------------------------- | ---------------------------------------------------------------- |
| 1.1.1  | Security is considered throughout the SDLC                        | Review SRD, threat model documents, security review process      |
| 1.1.2  | App uses up-to-date, supported OS versions and libraries          | Check minSdkVersion/deploymentTarget; review dependency versions |
| 1.1.3  | App verifies integrity of code and data loaded at runtime         | Check for code signature verification, integrity checks          |
| 1.1.4  | App minimizes attack surface through principle of least privilege | Review manifest permissions; verify minimal permission requests  |
| 1.1.5  | App implements appropriate certificate pinning                    | Verify pinning implementation; test pinning bypass resistance    |
| 1.1.6  | Third-party SDKs are vetted and monitored for vulnerabilities     | Review SDK vetting process; check SBOM against CVE databases     |
| 1.1.7  | App implements defense-in-depth for security controls             | Verify multiple layers of protection for sensitive operations    |
| 1.1.8  | App implements proper session management                          | Review token lifecycle, refresh mechanisms, revocation           |

**L2 Additional:**
| Req ID | Requirement (L2) | Verification Method |
|--------|-----------------|---------------------|
| 1.2.1 | App implements certificate pinning with fallback handling | Verify pinning with secure fallback (not disabling pinning) |
| 1.2.2 | App implements RASP (Runtime Application Self-Protection) | Verify RASP deployment; test detection and response capabilities |
| 1.2.3 | App uses hardware-backed security features | Verify Secure Enclave/StrongBox usage for key storage |

#### V2: Data Storage & Privacy

| Req ID | Requirement (L1)                                          | Verification Method                                          |
| ------ | --------------------------------------------------------- | ------------------------------------------------------------ |
| 2.1.1  | System credential storage facilities are used correctly   | Verify Keychain/Keystore usage; check for custom key storage |
| 2.1.2  | No sensitive data is written to local storage unencrypted | Scan filesystem for plaintext credentials, tokens, PII       |
| 2.1.3  | No sensitive data is exposed through IPC mechanisms       | Review intents, URL schemes, universal links, App Groups     |
| 2.1.4  | No sensitive data is exposed via platform-specific APIs   | Review pasteboard, notifications, screenshots, backups       |
| 2.1.5  | No sensitive data is exposed through developer features   | Verify debug features disabled in release builds             |
| 2.1.6  | No sensitive data is sent to the keyboard cache           | Verify `secureTextEntry`, keyboard type configuration        |
| 2.1.7  | No sensitive data is sent to the app switcher             | Verify app snapshot masking on background                    |
| 2.1.8  | App auto-deletes sensitive data per retention policy      | Verify data lifecycle management; test auto-deletion         |
| 2.1.9  | App's auto-generated documents are protected              | Verify file permissions on generated documents               |
| 2.1.10 | App handles sensitive data in memory securely             | Verify memory zeroing after use; check for memory dumps      |

#### V3: Cryptography

| Req ID | Requirement (L1)                                     | Verification Method                                             |
| ------ | ---------------------------------------------------- | --------------------------------------------------------------- |
| 3.1.1  | Cryptographic algorithms are industry-standard       | Verify AES-128+, RSA-2048+, ECDSA P-256+; reject DES, RC4, MD5  |
| 3.1.2  | Custom cryptographic algorithms are not used         | Verify no home-grown crypto; review all crypto implementations  |
| 3.1.3  | Cryptographic operations are implemented correctly   | Verify proper IV/nonce usage, padding modes, key sizes          |
| 3.1.4  | Keys are stored securely using platform facilities   | Verify hardware-backed Keystore/Secure Enclave for L2           |
| 3.1.5  | Random number generation is cryptographically secure | Verify `SecureRandom`, `SecRandomCopyBytes`; reject `Random`    |
| 3.1.6  | Cryptographic operations handle errors securely      | Verify constant-time comparisons; no timing leak in error paths |

#### V4: Authentication & Session Management

| Req ID | Requirement (L1)                                 | Verification Method                                                    |
| ------ | ------------------------------------------------ | ---------------------------------------------------------------------- |
| 4.1.1  | Password policy follows NIST guidelines          | Verify no arbitrary complexity rules; check against breached passwords |
| 4.1.2  | Biometric authentication is implemented securely | Verify biometric prompt uses crypto-bound keys, not just flag          |
| 4.1.3  | Session tokens are properly managed              | Verify token expiration, refresh, revocation, secure storage           |
| 4.1.4  | OAuth 2.0 / OIDC is implemented correctly        | Verify PKCE, state parameter, redirect URI validation                  |
| 4.1.5  | Multi-factor authentication is supported         | Verify MFA enrollment, backup codes, recovery flow security            |
| 4.1.6  | Account lockout is implemented                   | Verify lockout thresholds, unlock mechanisms, DoS prevention           |
| 4.1.7  | Sensitive operations require re-authentication   | Verify step-up auth for payments, profile changes, data export         |
| 4.1.8  | Authentication endpoints are rate-limited        | Verify rate limiting on login, password reset, MFA verification        |
| 4.1.9  | Credentials are not hardcoded                    | Scan for hardcoded credentials, API keys, OAuth secrets                |

#### V5: Network Communication

| Req ID | Requirement (L1)                                     | Verification Method                                             |
| ------ | ---------------------------------------------------- | --------------------------------------------------------------- |
| 5.1.1  | TLS is configured correctly                          | Verify TLS 1.2+; proper cipher suites; no weak algorithms       |
| 5.1.2  | Certificate chain is validated correctly             | Verify full chain validation; no hostname verification bypass   |
| 5.1.3  | Endpoints are validated against trusted certificates | Verify certificate pinning or trusted CA enforcement            |
| 5.1.4  | App does not rely on deprecated TLS features         | Verify no SSLv3, TLS 1.0/1.1; no RC4, 3DES ciphers              |
| 5.1.5  | App only establishes secure connections              | Verify all connections are TLS; no cleartext traffic exceptions |
| 5.1.6  | App implements certificate pinning                   | Verify pinning for high-risk apps; test pin rotation procedure  |
| 5.1.7  | App protects against TLS downgrade attacks           | Verify TLS_FALLBACK_SCSV support; HSTS headers present          |

#### V6: Platform Interaction

| Req ID | Requirement (L1)                                       | Verification Method                                        |
| ------ | ------------------------------------------------------ | ---------------------------------------------------------- |
| 6.1.1  | Intents/URL schemes are properly secured               | Review exported components; verify permission guards       |
| 6.1.2  | Deep links/universal links are validated               | Verify link association files; validate incoming link data |
| 6.1.3  | App does not leak data through IPC                     | Review ContentProvider, XPC, App Group sharing             |
| 6.1.4  | App validates data from external sources               | Verify input validation on all IPC entry points            |
| 6.1.5  | App uses WebView securely                              | Verify JS disabled by default; no `addJavascriptInterface` |
| 6.1.6  | App does not process sensitive data in background      | Verify background execution restrictions for sensitive ops |
| 6.1.7  | App permissions are requested at runtime appropriately | Verify runtime permission requests with user context       |
| 6.1.8  | App handles URL scheme collisions securely             | Verify unique URL scheme; validate incoming URL data       |

#### V7: Code Quality & Build Settings

| Req ID | Requirement (L1)                                   | Verification Method                                               |
| ------ | -------------------------------------------------- | ----------------------------------------------------------------- |
| 7.1.1  | App is compiled with security-focused build flags  | Verify Stack Canary, ASLR, DEP/NX, PIE for native code            |
| 7.1.2  | App does not contain unnecessary code or resources | Verify code shrinking (R8/ProGuard); remove unused resources      |
| 7.1.3  | App implements proper error handling               | Verify no stack traces in release builds; graceful error handling |
| 7.1.4  | App does not log sensitive information             | Verify logging disabled/scrubbed in release builds                |
| 7.1.5  | Third-party dependencies are up-to-date            | Review dependency versions; check against CVE databases           |
| 7.1.6  | App implements anti-debugging protections          | Verify debug flag checks; ptrace protection (iOS); anti-Frida     |
| 7.1.7  | App is obfuscated to prevent reverse engineering   | Verify ProGuard/R8 rules; native library obfuscation              |

#### V8: Resilience (L2 Only)

| Req ID | Requirement (L2)                                 | Verification Method                                              |
| ------ | ------------------------------------------------ | ---------------------------------------------------------------- |
| 8.1.1  | App detects and responds to root/jailbreak       | Verify multi-method detection; graceful degradation on detection |
| 8.2.1  | App detects and responds to tampering            | Verify code signature verification; integrity checks             |
| 8.2.2  | App detects and responds to repackaging          | Verify signature verification against known certificate          |
| 8.3.1  | App detects and responds to emulators            | Verify emulator detection (not sole security control)            |
| 8.3.2  | App detects and responds to hooking frameworks   | Verify Frida/Xposed/Substrate detection; runtime integrity       |
| 8.4.1  | App implements anti-reversing measures           | Verify string encryption; control flow obfuscation               |
| 8.4.2  | App implements anti-debugging measures           | Verify multiple anti-debug techniques; runtime checks            |
| 8.5.1  | App implements RASP                              | Verify runtime monitoring; threat response mechanisms            |
| 8.5.2  | App implements continuous integrity verification | Verify periodic integrity checks throughout app lifecycle        |
| 8.5.3  | App defends against dynamic analysis             | Verify anti-instrumentation; timing-based detection              |
| 8.5.4  | App implements secure update mechanisms          | Verify update signature verification; rollback prevention        |

**Phase 3: Gap Analysis & Reporting (Day 5)**

1. **Consolidate findings**: Map all identified gaps to MASVS requirements
2. **Prioritize remediation**: Classify gaps by severity (P0–P3) and compliance impact
3. **Generate compliance report**: Produce structured MASVS assessment report
4. **Present to CSO**: Brief Dr. Chen on compliance status, critical gaps, and remediation timeline

### 3. Compliance Assessment Report Template

```markdown
# MASVS Compliance Assessment Report

**Application:** [App Name]
**Version:** [vX.Y.Z]
**Assessment Level:** MASVS L1 / L2
**Assessor:** Sana Khoury
**Date:** [YYYY-MM-DD]

## Executive Summary

| Metric                      | Value |
| --------------------------- | ----- |
| Total Requirements Assessed | XX/XX |
| Compliant                   | XX    |
| Partially Compliant         | XX    |
| Non-Compliant               | XX    |
| Overall Compliance Rate     | XX%   |

## Detailed Results by Category

### V1: Architecture, Design & Threat Modeling

| Req ID | Status     | Finding   | Severity | Remediation |
| ------ | ---------- | --------- | -------- | ----------- |
| 1.1.1  | ✅ Pass    | —         | —        | —           |
| 1.1.2  | ⚠️ Partial | [Details] | P2       | [Action]    |
| ...    | ...        | ...       | ...      | ...         |

## Compliance Score by Category

| Category | L1 Score | L2 Score (if applicable) |
| -------- | -------- | ------------------------ |
| V1       | X/X      | X/X                      |
| V2       | X/X      | X/X                      |
| ...      | ...      | ...                      |

## Critical Findings (P0/P1)

[List all P0/P1 findings with immediate remediation requirements]

## Remediation Timeline

| Finding | Severity | Estimated Effort | Target Date | Status |
| ------- | -------- | ---------------- | ----------- | ------ |
```

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                                                                                  |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 1** (SRD)                    | Informs security requirements by identifying which MASVS levels apply based on data classification and threat model; defines compliance targets for the project                              |
| **Stage 6** (Code Review)            | Serves as the authoritative compliance checklist during code review; every finding is classified and tracked; non-compliance with L1 controls generates P0/P1 defects                        |
| **Stage 8** (Integrity Verification) | Re-assesses MASVS compliance after remediation; verifies that all previously non-compliant controls are now passing; produces updated compliance matrix                                      |
| **Stage 10** (Release Readiness)     | Provides the compliance evidence for CSO release checklist item #4 (SRD enforced, OWASP MASVS compliant); signs off that all L1 requirements pass and L2 requirements meet minimum threshold |

## Quality Standards

| Metric                      | Standard                                                                                                                                                       |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Assessment Completeness** | 100% of applicable MASVS requirements assessed (L1 for all apps; L1+L2 for sensitive-data apps)                                                                |
| **Assessment Accuracy**     | Zero false negatives on L1 controls (validated by peer review); <5% false positive rate                                                                        |
| **Report Quality**          | Every non-compliant finding includes: specific MASVS requirement reference, severity classification, reproduction steps, remediation guidance, effort estimate |
| **Timeliness**              | Full MASVS assessment completed within 5 business days of engagement                                                                                           |
| **Remediation Tracking**    | 100% of P0/P1 compliance gaps tracked to closure with evidence; P2/P3 gaps tracked with user disposition                                                       |
| **Audit Readiness**         | Assessment reports formatted to satisfy external auditor review (SOC 2, PCI-DSS, ISO 27001)                                                                    |
| **Continuous Monitoring**   | Automated MASVS compliance checks integrated into CI/CD pipeline with ≤24-hour feedback cycle                                                                  |
