---
name: security-masvs-mastery-track-b
description: MASVS Mastery Track B — engineering implementation guide for platform leads and developers covering secure coding patterns per MASVS control, platform-specific security APIs (iOS Keychain, Android Keystore), and security testing integration. Owned by Natalia Petrova (Security Engineer). Use during Stage 5 (Development) for secure coding implementation and Stage 6 (Code Review) for implementation verification. Trigger: MASVS Track B, secure coding patterns, platform security APIs, iOS Keychain, Android Keystore, security testing integration, developer security guide.
prerequisites:
  - security-overview

version: "1.0.0"
---

# MASVS Mastery Track B — Defense-in-Depth (L2)

## 1. Track B Overview: Scope and Purpose

### 1.1 Defense-in-Depth Mastery for L2 Requirements

MASVS Track B represents the **Level 2 (L2) mastery tier** — the defense-in-depth control set required for applications that handle sensitive data, operate in high-threat environments, or serve regulated industries. Where Track A (L1) establishes a baseline of security hygiene, Track B demands **proactive resilience** against sophisticated adversaries employing reverse engineering, runtime manipulation, and supply-chain attacks.

Track B is not an optional hardening layer. It is a **mandatory compliance tier** for applications whose failure modes include:

- Financial loss (fraudulent transactions, account takeover)
- Privacy violations (exposure of protected health information, biometric data)
- Regulatory non-compliance (GDPR, HIPAA, PCI-DSS, SOC 2)
- Reputational destruction (enterprise identity compromise, government data breach)

### 1.2 When Track B is Mandatory vs Optional

| Condition                               | Track A (L1) | Track B (L2)                     | Rationale                               |
| --------------------------------------- | ------------ | -------------------------------- | --------------------------------------- |
| General consumer app, no sensitive data | Required     | Not required                     | L1 baseline suffices                    |
| Banking or payments application         | Insufficient | **Mandatory**                    | Financial data, regulatory requirements |
| Healthcare application (PHI)            | Insufficient | **Mandatory**                    | HIPAA, sensitive health data            |
| Enterprise SSO / identity provider      | Insufficient | **Mandatory**                    | Credential harvesting target            |
| Government application (CUI)            | Insufficient | **Mandatory**                    | Classified data handling                |
| E-commerce with stored payment data     | Insufficient | **Mandatory**                    | PCI-DSS scope                           |
| Social media application                | Required     | Recommended                      | PII exposure risk                       |
| Gaming application                      | Required     | Optional unless in-app purchases | Financial component via IAP             |

### 1.3 Relationship to Track A (L1 Baseline)

Track B **includes all Track A controls** as a prerequisite. There is no Track B without Track A compliance. The relationship is additive:

```
Track B = Track A (all L1 controls) + L2 Enhancement Controls + V8 Resilience Category
```

| Layer        | MASVS Categories            | Description                                                                                    |
| ------------ | --------------------------- | ---------------------------------------------------------------------------------------------- |
| Track A (L1) | V1-V7 (baseline)            | Data storage, cryptography, authentication, network, platform, code quality, resilience basics |
| Track B (L2) | V1-V7 (enhanced) + V8 (new) | Defense-in-depth for all V1-V7 categories + V8 resilience against reverse engineering          |

**Key principle**: A Track B gap in any V1-V7 category is classified the same as a V8 gap — both are defense-in-depth failures. At Stage 6/8 review, Track B non-compliance is treated as a **P0 or P1 defect** depending on the severity of the exposed control.

---

## 2. V8: Resilience Against Reverse Engineering

V8 is the **defining category** of Track B. It does not exist in Track A. V8 addresses the adversary's ability to understand, modify, and repackage your application. Each sub-category below includes mastery criteria, verification procedures, and evidence requirements.

### 2.1 V8.1 — Root/Jailbreak Detection

#### Mastery Criteria

The application must detect and respond to compromised operating system environments on both iOS and Android platforms. Detection must occur at **application launch** and at **runtime intervals** (minimum every 60 seconds during active sessions).

| Platform       | Detection Mechanism                         | Required Coverage                                                |
| -------------- | ------------------------------------------- | ---------------------------------------------------------------- |
| Android        | Magisk detection (MagiskHide bypass)        | SU binary presence, test-keys build tags, dangerous app packages |
| Android        | Kernel-level root detection                 | `/system/bin/su`, `/system/xbin/su`, Superuser/SuperSU packages  |
| Android        | Play Integrity API `MEETS_DEVICE_INTEGRITY` | StrongBox-backed attestation where hardware supports it          |
| iOS            | Jailbreak file system detection             | `/Applications/Cydia.app`, `/usr/sbin/sshd`, `/etc/apt`          |
| iOS            | Jailbreak process detection                 | Cydia, Sileo, Zebra, unc0ver, checkra1n, palera1n processes      |
| iOS            | Sandbox escape detection                    | Attempt to write outside app sandbox, symlink attacks            |
| Cross-platform | Emulator detection                          | Hardware fingerprint analysis, sensor absence detection          |

#### Verification Procedures

1. **Static Analysis**: Review root detection implementation in code. Verify detection runs on cold start, warm start, and at runtime intervals.
2. **Dynamic Testing**: Install application on rooted/jailbroken device. Verify detection triggers within 5 seconds of launch.
3. **Evasion Testing**: Attempt detection bypass using MagiskHide, JailbreakDectorBypass tweaks, or Frida hooks on detection functions.
4. **Response Validation**: Verify the application takes appropriate action (graceful degradation, session termination, or admin notification). **Silent detection without response is a V8.1 failure.**

#### Evidence Requirements

| Evidence Artifact                  | Description                                                      | Location                                                |
| ---------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- |
| `root-detection-implementation.md` | Technical design document for root/jailbreak detection logic     | `company/project/<project>/security/compliance/`        |
| `root-detection-test-results.md`   | Test results across rooted and clean devices                     | `company/project/<project>/testing/results/`            |
| `evasion-test-report.md`           | Results of attempted detection bypass using common evasion tools | `company/project/<project>/security/penetration-tests/` |
| `response-behavior-log.md`         | Application response behavior when root detected                 | `company/project/<project>/testing/results/`            |

#### Response Behavior Requirements

Track B requires **more than detection** — the application must respond appropriately:

| Response Type                          | When to Use                              | Acceptable for Track B      |
| -------------------------------------- | ---------------------------------------- | --------------------------- |
| Block with user message                | High-security apps (banking, government) | ✅ Yes                      |
| Degrade functionality (read-only mode) | Medium-security apps                     | ✅ Yes with justification   |
| Log and continue                       | Low-security monitoring only             | ❌ No — insufficient for L2 |
| Silent telemetry only                  | Analytics purposes                       | ❌ No — insufficient for L2 |

### 2.2 V8.2 — Tampering Detection

#### Mastery Criteria

The application must detect unauthorized modifications to its own code, resources, and data files. Tampering detection must cover:

| Tampering Vector                | Detection Method                                                    | Platform |
| ------------------------------- | ------------------------------------------------------------------- | -------- |
| APK repackaging                 | Signature verification (package manager + manual certificate check) | Android  |
| IPA modification                | Code signature validation (`SecStaticCodeCheckValidity`)            | iOS      |
| Resource modification           | Hash-based integrity check of critical resources                    | Both     |
| Runtime code injection          | Memory region scanning for unexpected executable mappings           | Both     |
| Library substitution            | Hash verification of loaded native libraries (`.so` / `.dylib`)     | Both     |
| Database tampering              | HMAC verification of local databases                                | Both     |
| Configuration file modification | Signed configuration files with signature verification              | Both     |

#### Verification Procedures

1. **APK Repackaging Test**: Decompile APK, modify a resource, repackage with debug certificate, install. Application must detect signature mismatch.
2. **IPA Modification Test**: Extract IPA, modify a resource, re-sign with different certificate, install. Application must detect code signature failure.
3. **Runtime Injection Test**: Attempt to inject code via Frida script during runtime. Application must detect unexpected executable memory regions.
4. **Library Substitution Test**: Replace a native library with a modified version. Application must detect hash mismatch on load.

#### Evidence Requirements

| Evidence Artifact                    | Description                                                |
| ------------------------------------ | ---------------------------------------------------------- |
| `tamper-detection-design.md`         | Architecture of tampering detection mechanisms             |
| `signature-verification-results.md`  | Test results for signature verification on modified builds |
| `runtime-injection-detection-log.md` | Logs from attempted runtime injection tests                |
| `library-integrity-verification.md`  | Hash verification results for all native libraries         |

### 2.3 V8.3 — Anti-Debugging and Anti-Reversing

#### Mastery Criteria

The application must implement controls that impede dynamic analysis and reverse engineering efforts.

| Control                    | Implementation                                                          | Platform | Mastery Standard |
| -------------------------- | ----------------------------------------------------------------------- | -------- | ---------------- |
| Debugger detection         | `ptrace(PT_DENY_ATTACH)` on iOS, `ptrace(PTRACE_TRACEME)` on Android    | Both     | Required         |
| Debug flag check           | `android:debuggable="false"` enforcement, `isDebuggerConnected()`       | Android  | Required         |
| Timing-based detection     | Measure execution time of critical functions — debugger slows execution | Both     | Required         |
| Checksum self-verification | Application verifies its own integrity at runtime                       | Both     | Required         |
| Anti-emulator checks       | Detect emulated environment via hardware properties                     | Both     | Required         |
| Native code protection     | Strip symbols, use control flow obfuscation in critical paths           | Both     | Required         |

#### Verification Procedures

1. **Debugger Attachment Test**: Attempt to attach debugger (lldb on iOS, gdb/jdb on Android) to running application. Application must detect and respond.
2. **Timing Analysis**: Profile critical function execution with and without debugger. Verify timing anomaly detection triggers.
3. **Emulator Detection**: Run application on Genymotion, Android Emulator, or Corellium. Verify detection and appropriate response.
4. **Static Analysis Resistance**: Disassemble application with Ghidra/IDA Pro. Verify control flow obfuscation impedes analysis of critical paths.

#### Evidence Requirements

| Evidence Artifact                     | Description                                      |
| ------------------------------------- | ------------------------------------------------ |
| `anti-debug-implementation.md`        | Technical design of anti-debugging controls      |
| `debugger-attachment-test-results.md` | Results from attempted debugger attachment tests |
| `emulator-detection-report.md`        | Detection accuracy across emulator platforms     |
| `disassembly-resistance-analysis.md`  | Analysis of reverse engineering difficulty       |

### 2.4 V8.4 — Runtime Application Self-Protection (RASP)

#### Mastery Criteria

The application must implement real-time self-protection mechanisms that detect and respond to active attack patterns during runtime.

| RASP Capability             | Description                                                                 | Track B Requirement            |
| --------------------------- | --------------------------------------------------------------------------- | ------------------------------ |
| Runtime hook detection      | Detect Frida/Xposed/Substrate hooks on critical functions                   | Required                       |
| Memory integrity monitoring | Verify code sections have not been modified in memory                       | Required                       |
| Input anomaly detection     | Detect fuzzing patterns, abnormal input sequences                           | Recommended                    |
| Behavioral analysis         | Detect bot-like interaction patterns                                        | Recommended for financial apps |
| Secure crash handling       | Prevent information leakage in crash logs, implement secure crash reporting | Required                       |

#### Verification Procedures

1. **Frida Hook Detection Test**: Run Frida server on device, attach to application, attempt to hook critical functions. Application must detect and respond.
2. **Memory Modification Test**: Use Frida to modify memory contents of running application. Application must detect integrity violation.
3. **Input Fuzzing Test**: Submit abnormal input sequences at high frequency. Application must detect and rate-limit.
4. **Crash Information Leak Test**: Force application crash, examine crash logs for sensitive information. No secrets, tokens, or keys must be present.

#### Evidence Requirements

| Evidence Artifact                  | Description                                 |
| ---------------------------------- | ------------------------------------------- |
| `rasp-architecture.md`             | Design document for RASP capabilities       |
| `frida-hook-detection-results.md`  | Test results for hook detection             |
| `memory-integrity-verification.md` | Memory integrity monitoring results         |
| `crash-log-audit.md`               | Audit of crash logs for information leakage |

### 2.5 Code Obfuscation and Control Flow Flattening

#### Requirements

| Technique                | Platform | Tool                            | Requirement Level      |
| ------------------------ | -------- | ------------------------------- | ---------------------- |
| Name obfuscation         | Android  | R8/ProGuard                     | Required (L1 baseline) |
| Control flow flattening  | Android  | ProGuard commercial, DexGuard   | Required for Track B   |
| String encryption        | Android  | DexGuard, commercial obfuscator | Required for Track B   |
| Resource encryption      | Android  | DexGuard, custom implementation | Required for Track B   |
| Bitcode obfuscation      | iOS      | LLVM obfuscation, O-LLVM        | Required for Track B   |
| Symbol stripping         | iOS      | Default release build settings  | Required (L1 baseline) |
| Control flow obfuscation | iOS      | O-LLVM, commercial tools        | Required for Track B   |
| String obfuscation       | iOS      | Custom string encryption        | Required for Track B   |

#### Verification Procedures

1. **Decompilation Test**: Decompile application with Jadx (Android) or Hopper (iOS). Verify that critical business logic is not readily understandable.
2. **String Extraction Test**: Extract all strings from binary. Verify that sensitive strings (API keys, URLs, cryptographic constants) are not in plaintext.
3. **Control Flow Analysis**: Generate control flow graph of critical functions. Verify that flattening impedes automated analysis.

### 2.6 White-Box Cryptography

#### Requirements

White-box cryptography protects cryptographic keys in software implementations where the adversary has full access to the execution environment.

| Requirement                  | Description                                                       | Track B Applicability                                         |
| ---------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------- |
| White-box AES implementation | Protect AES keys in software for apps performing local encryption | Required if encrypting data at rest without hardware keystore |
| White-box ECC implementation | Protect ECC keys for digital signatures in software               | Required if signing operations occur in software              |
| External encoding            | Protect intermediate values in white-box implementation           | Required                                                      |
| Table-based implementation   | Cryptographic operations implemented as table lookups             | Required                                                      |

#### Verification Procedures

1. **Key Extraction Resistance Test**: Attempt to extract cryptographic keys from white-box implementation using DCA (Differential Computation Analysis). Keys must not be recoverable.
2. **Implementation Correctness Test**: Verify white-box implementation produces correct cryptographic output for known test vectors.

---

## Appendix B: Platform-Specific Implementation Summary

| Control                  | Android                                      | iOS                                           | Cross-Platform Notes                              |
| ------------------------ | -------------------------------------------- | --------------------------------------------- | ------------------------------------------------- |
| Hardware Keystore        | StrongBox Keymaster                          | Secure Enclave                                | KMP: expect/actual; Flutter: platform channels    |
| Root/Jailbreak Detection | SU binary, test-keys, Magisk, Play Integrity | Cydia, SSH, sandbox escape, process detection | Implement separately per platform                 |
| Certificate Pinning      | `network_security_config.xml`                | `URLSessionDelegate` validation               | Configure per-platform networking                 |
| Biometric Binding        | `BiometricPrompt.CryptoObject`               | `LocalAuthentication` + `SecAccessControl`    | Ensure cryptographic binding semantics preserved  |
| Anti-Debugging           | `ptrace(PTRACE_TRACEME)`, debuggable check   | `ptrace(PT_DENY_ATTACH)`, syscall monitoring  | Native code per platform                          |
| Code Obfuscation         | R8 + DexGuard (commercial)                   | O-LLVM, symbol stripping                      | iOS AOT compilation provides baseline obfuscation |
| Tamper Detection         | APK signature verification                   | `SecStaticCodeCheckValidity`                  | Verify on every launch                            |
| RASP                     | Frida detection, memory scanning             | Frida detection, memory scanning              | Similar approach both platforms                   |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`3.-enhanced-l2-requirements-for-v1-v7-beyond-track-a.md`](references/3.-enhanced-l2-requirements-for-v1-v7-beyond-track-a.md) — 3. Enhanced L2 Requirements for V1-V7 Beyond Track A
- [`4.-application-classification-matrix:-when-track-b-is-mandatory.md`](references/4.-application-classification-matrix:-when-track-b-is-mandatory.md) — 4. Application Classification Matrix: When Track B is Mandatory
- [`5.-threat-intelligence-integration:-current-mobile-threat-landscape.md`](references/5.-threat-intelligence-integration:-current-mobile-threat-landscape.md) — 5. Threat Intelligence Integration: Current Mobile Threat Landscape
- [`6.-platform-specific-threat-patterns.md`](references/6.-platform-specific-threat-patterns.md) — 6. Platform-Specific Threat Patterns
- [`7.-stage-6-8-verification:-track-b-mastery-verification.md`](references/7.-stage-6-8-verification:-track-b-mastery-verification.md) — 7. Stage 6/8 Verification: Track B Mastery Verification
- [`8.-external-certification-path:-masvs-level-2-certification.md`](references/8.-external-certification-path:-masvs-level-2-certification.md) — 8. External Certification Path: MASVS Level 2 Certification
- [`appendix-a:-track-b-quick-reference-card.md`](references/appendix-a:-track-b-quick-reference-card.md) — Appendix A: Track B Quick Reference Card
- [`appendix-c:-masvs-v8-mapping-to-owasp-mobile-top-10.md`](references/appendix-c:-masvs-v8-mapping-to-owasp-mobile-top-10.md) — Appendix C: MASVS V8 Mapping to OWASP Mobile Top 10
