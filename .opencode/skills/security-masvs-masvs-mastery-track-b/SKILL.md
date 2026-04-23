---
name: security-masvs-masvs-mastery-track-b
description: 'Security skill: Masvs Mastery Track B'
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

## 3. Enhanced L2 Requirements for V1-V7 Beyond Track A

Track B enhances every V1-V7 category beyond the L1 baseline. The following table summarizes the delta between Track A and Track B for each category.

### 3.1 V1: Architecture, Design, and Threat Modeling

| Control                   | Track A (L1)                   | Track B (L2)                                                                 | Delta    |
| ------------------------- | ------------------------------ | ---------------------------------------------------------------------------- | -------- |
| Security architecture     | Documented architecture        | Architecture includes trust boundaries, data flow diagrams, threat model     | Enhanced |
| Threat modeling           | Initial threat model performed | Threat model updated per release, includes adversarial capability assessment | Enhanced |
| Security testing strategy | Testing strategy defined       | Strategy includes penetration testing schedule, red team engagement plan     | Enhanced |

### 3.2 V2: Data Storage and Privacy

| Control                   | Track A (L1)                                | Track B (L2)                                                           | Delta    |
| ------------------------- | ------------------------------------------- | ---------------------------------------------------------------------- | -------- |
| Sensitive data encryption | Encrypted with platform keystore            | **Hardware-backed** keystore required (StrongBox, Secure Enclave)      | Enhanced |
| Key management            | Keys in platform keystore                   | Keys in hardware-backed keystore with attestation, key rotation policy | Enhanced |
| Sensitive data exposure   | No sensitive data in logs, backups          | Additional: memory scrubbing for sensitive data, secure deletion       | Enhanced |
| Keyboard cache            | Keyboard cache disabled for sensitive input | Additional: custom secure keyboard for financial input fields          | Enhanced |
| Clipboard                 | Clipboard cleared after sensitive copy      | Additional: clipboard monitoring and blocking for sensitive data       | Enhanced |
| Screenshots               | App background obscured in recents          | Additional: screenshot prevention for sensitive screens                | Enhanced |
| Local database            | SQLCipher or platform equivalent            | Additional: HMAC verification of database integrity                    | Enhanced |

#### Enhanced Data Storage Encryption — Hardware-Backed Keystores

| Platform                 | Hardware Keystore                                   | Attestation                   | Key Lifetime      |
| ------------------------ | --------------------------------------------------- | ----------------------------- | ----------------- |
| Android                  | StrongBox Keymaster (hardware security module)      | Key attestation certificate   | Hardware-enforced |
| Android < StrongBox      | TEE-backed Keystore (Trusted Execution Environment) | Software attestation          | TEE-enforced      |
| iOS                      | Secure Enclave                                      | Key attestation               | Hardware-enforced |
| Cross-platform (KMP)     | Platform-specific abstraction via KMP expect/actual | Attestation via platform APIs | Platform-specific |
| Cross-platform (Flutter) | Platform channel to native keystore                 | Attestation via native code   | Platform-specific |

**Track B Requirement**: Applications MUST use hardware-backed keystores where available. Software-based keystore fallback is acceptable only with documented justification and compensating controls.

### 3.3 V3: Cryptography

| Control                      | Track A (L1)                                                  | Track B (L2)                                                                             | Delta    |
| ---------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------- |
| Algorithm selection          | Industry-standard algorithms (AES-GCM, RSA-2048+, ECC P-256+) | Additional: quantum-resistant algorithm assessment, migration plan                       | Enhanced |
| Key length                   | Minimum per NIST guidelines                                   | Additional: 3072-bit RSA minimum for long-term secrets                                   | Enhanced |
| Key rotation                 | Keys rotated on compromise                                    | **Scheduled key rotation** policy (maximum 90 days for symmetric, 1 year for asymmetric) | Enhanced |
| Forward secrecy              | Not required at L1                                            | **Perfect forward secrecy** required for all network communications                      | Enhanced |
| Random number generation     | Platform CSPRNG                                               | Additional: hardware RNG where available, entropy source validation                      | Enhanced |
| Cryptographic implementation | vetted libraries only                                         | Additional: constant-time implementations for sensitive operations                       | Enhanced |

#### Enhanced Cryptographic Requirements — Key Rotation and Forward Secrecy

**Key Rotation Policy**:

| Key Type                  | Rotation Interval           | Rotation Trigger                          | Track B Requirement |
| ------------------------- | --------------------------- | ----------------------------------------- | ------------------- |
| Symmetric encryption keys | 90 days                     | Compromise, personnel change, scheduled   | Mandatory           |
| Asymmetric key pairs      | 1 year                      | Compromise, certificate expiry, scheduled | Mandatory           |
| API keys / tokens         | 30 days                     | Compromise, deployment, scheduled         | Mandatory           |
| Signing keys              | Per manufacturer guidelines | Compromise, certificate expiry            | Mandatory           |
| Master keys               | As per compliance framework | Compromise, audit finding, scheduled      | Mandatory           |

**Forward Secrecy Implementation**:

| Protocol              | Forward Secrecy Mechanism                            | Track B Requirement       |
| --------------------- | ---------------------------------------------------- | ------------------------- |
| TLS 1.3               | ECDHE key exchange (mandatory in TLS 1.3)            | Mandatory                 |
| TLS 1.2               | ECDHE cipher suites only, static RSA disabled        | Mandatory                 |
| End-to-end encryption | Double Ratchet Algorithm (Signal Protocol)           | Recommended for messaging |
| Local encryption      | Ephemeral session keys for each encryption operation | Mandatory                 |

### 3.4 V4: Authentication and Session Management

| Control                     | Track A (L1)                   | Track B (L2)                                                                                                 | Delta    |
| --------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------ | -------- |
| Biometric authentication    | Biometric prompt with fallback | **Biometric with cryptographic binding** (CryptoObject on Android, LocalAuthentication with keychain on iOS) | Enhanced |
| Biometric fallback          | Password/PIN fallback allowed  | Fallback requires re-authentication after 5 minutes of inactivity                                            | Enhanced |
| Multi-factor authentication | MFA recommended                | **MFA required** for sensitive operations (financial transactions, data export)                              | Enhanced |
| Session management          | Session timeout implemented    | Additional: session binding to device fingerprint, concurrent session limits                                 | Enhanced |
| Token storage               | Secure token storage           | Additional: token binding, refresh token rotation                                                            | Enhanced |
| Credential storage          | No hardcoded credentials       | Additional: credential rotation mechanism, breach detection integration                                      | Enhanced |

#### Enhanced Authentication — Biometric and MFA

**Biometric Cryptographic Binding**:

| Platform       | Mechanism                                  | Description                                                                                                 |
| -------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Android        | `BiometricPrompt.CryptoObject`             | Biometric authentication unlocks cryptographic key; key operations only possible after successful biometric |
| iOS            | `LocalAuthentication` + `SecAccessControl` | Key protected by `biometryCurrentSet`; key invalidated if biometry changes                                  |
| Cross-platform | Platform channel to native biometric API   | Abstraction layer must preserve cryptographic binding semantics                                             |

**MFA Requirements**:

| Factor Type        | Acceptable for Track B                          | Notes                                       |
| ------------------ | ----------------------------------------------- | ------------------------------------------- |
| Something you know | PIN, password, passphrase                       | Minimum 6-digit PIN or 8-character password |
| Something you have | Hardware token (FIDO2), TOTP, push notification | Hardware token preferred                    |
| Something you are  | Fingerprint, Face ID, iris scan                 | Must use platform biometric API             |
| Somewhere you are  | Geolocation verification                        | Supplemental factor only                    |

### 3.5 V5: Network Communication

| Control                        | Track A (L1)                                      | Track B (L2)                                                           | Delta    |
| ------------------------------ | ------------------------------------------------- | ---------------------------------------------------------------------- | -------- |
| TLS configuration              | TLS 1.2+ with strong cipher suites                | TLS 1.3 preferred, legacy protocol negotiation disabled                | Enhanced |
| Certificate validation         | Platform certificate validation                   | Additional: **certificate pinning** or trust-on-first-use (TOFU)       | Enhanced |
| Certificate pinning            | Not required at L1                                | **Required** for Track B — pin to leaf or intermediate certificate     | Enhanced |
| Mutual TLS (mTLS)              | Not required at L1                                | **Required** for server-to-server communication in enterprise contexts | Enhanced |
| Network security configuration | Network security config defined                   | Additional: pin set with backup pins, expiry-aware pin rotation        | Enhanced |
| WebView security               | Mixed content disabled, JavaScript bridge secured | Additional: URL allowlisting, content security policy enforcement      | Enhanced |

#### Enhanced Network Communication — Certificate Pinning and mTLS

**Certificate Pinning Implementation**:

| Platform                 | Mechanism                                              | Track B Requirement                                  |
| ------------------------ | ------------------------------------------------------ | ---------------------------------------------------- |
| Android                  | `network_security_config.xml` with `<pin-set>`         | Mandatory — pin SHA-256 digests, include backup pins |
| iOS                      | `URLSessionDelegate` with `URLAuthenticationChallenge` | Mandatory — validate against pinned certificates     |
| Cross-platform (KMP)     | Platform-specific pinning via expect/actual            | Mandatory — both platforms must implement pinning    |
| Cross-platform (Flutter) | `SecurityContext` with trusted certificates            | Mandatory — configure with pinned certificates       |

**Pin Configuration Requirements**:

| Requirement          | Description                                             |
| -------------------- | ------------------------------------------------------- |
| Minimum pins         | 2 pins (current + backup)                               |
| Maximum pins         | 4 pins (to limit trust surface)                         |
| Pin algorithm        | SHA-256 of SubjectPublicKeyInfo                         |
| Pin backup           | At least one backup pin for certificate rotation        |
| Pin expiration       | Pins reviewed and rotated with certificate renewal      |
| Pin failure response | Fail closed — reject connection if pin validation fails |

**Mutual TLS (mTLS) Requirements**:

| Scenario                  | mTLS Required      | Client Certificate Storage                   |
| ------------------------- | ------------------ | -------------------------------------------- |
| Mobile to API gateway     | Recommended        | Hardware keystore (StrongBox/Secure Enclave) |
| Service-to-service        | Mandatory          | Hardware keystore or HSM                     |
| Mobile to third-party API | If API supports it | Hardware keystore                            |

### 3.6 V6: Platform Interaction

| Control               | Track A (L1)                                   | Track B (L2)                                                                | Delta    |
| --------------------- | ---------------------------------------------- | --------------------------------------------------------------------------- | -------- |
| IPC mechanism         | Secure IPC using platform-recommended patterns | Additional: **intent validation**, permission verification on receiving end | Enhanced |
| Intent handling       | Explicit intents preferred over implicit       | Additional: intent signature verification for sensitive data transfer       | Enhanced |
| Deep link validation  | Deep links validated                           | Additional: deep link signature verification, App Links/Universal Links     | Enhanced |
| Activity exposure     | No sensitive data in activity previews         | Additional: `FLAG_SECURE` on Android, `UIScreen.captured` monitoring on iOS | Enhanced |
| File sharing          | Secure file sharing with content providers     | Additional: URI permission grant with explicit expiry                       | Enhanced |
| Cross-app data access | No inadvertent data exposure                   | Additional: explicit access control on all shared data                      | Enhanced |

#### Enhanced Platform Interaction — Secure IPC and Intent Validation

**Android Intent Security**:

| Control                       | Implementation                                                   | Track B Requirement                |
| ----------------------------- | ---------------------------------------------------------------- | ---------------------------------- |
| Intent signature verification | Verify calling app signature before processing sensitive intents | Mandatory for sensitive operations |
| Intent permission enforcement | Use `android:permission` in manifest for broadcast receivers     | Mandatory                          |
| Intent data validation        | Validate all intent extras, never trust implicit data            | Mandatory                          |
| PendingIntent immutability    | Use `FLAG_IMMUTABLE` on all PendingIntents                       | Mandatory                          |

**iOS Universal Links and IPC**:

| Control               | Implementation                                               | Track B Requirement          |
| --------------------- | ------------------------------------------------------------ | ---------------------------- |
| Universal Links       | Domain-verified deep links with `apple-app-site-association` | Mandatory for external links |
| Keychain sharing      | Keychain access groups restricted to known app IDs           | Mandatory                    |
| App Groups            | Shared containers restricted to signed app family            | Mandatory                    |
| URL scheme validation | Validate source of `openURL:` calls                          | Mandatory                    |

### 3.7 V7: Code Quality and Build Settings

| Control                   | Track A (L1)                           | Track B (L2)                                                                                   | Delta    |
| ------------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------- | -------- |
| ProGuard/R8               | Enabled for release builds             | Additional: **aggressive optimization** with custom keep rules for critical classes            | Enhanced |
| Native library protection | Native libraries stripped              | Additional: native library integrity verification, anti-tampering in native code               | Enhanced |
| Debug code removal        | Debug code removed from release builds | Additional: debug interfaces completely removed, no test hooks in production                   | Enhanced |
| Compiler security         | Stack canaries, ASLR, DEP/NX enabled   | Additional: Control Flow Guard (CFG), SafeSEH, /GS flags verified                              | Enhanced |
| Dependency scanning       | Dependencies tracked                   | Additional: **SBOM (Software Bill of Materials)** generated, dependency vulnerability scanning | Enhanced |
| Third-party SDK vetting   | SDKs evaluated before integration      | Additional: SDK runtime behavior monitoring, network call auditing                             | Enhanced |

#### Enhanced Code Quality — ProGuard/R8 Optimization and Native Library Protection

**ProGuard/R8 Configuration for Track B**:

| Optimization             | Configuration                                     | Purpose                                  |
| ------------------------ | ------------------------------------------------- | ---------------------------------------- |
| Code shrinking           | `isMinifyEnabled = true`                          | Remove unused code                       |
| Resource shrinking       | `isShrinkResources = true`                        | Remove unused resources                  |
| Obfuscation              | Default + custom rules                            | Rename classes, methods, fields          |
| Optimization             | `optimizationPasses = 5` (maximum)                | Aggressive code optimization             |
| Control flow obfuscation | Commercial tool (DexGuard)                        | Flatten control flow of critical methods |
| String encryption        | Commercial tool (DexGuard)                        | Encrypt sensitive strings                |
| Custom keep rules        | Keep only entry points, obfuscate everything else | Minimize attack surface                  |

**Native Library Protection**:

| Protection                     | Implementation                                   | Platform |
| ------------------------------ | ------------------------------------------------ | -------- |
| Library integrity verification | SHA-256 hash verification of `.so` files on load | Android  |
| Anti-debugging in native code  | `ptrace(PTRACE_TRACEME)` in JNI code             | Android  |
| Symbol stripping               | Strip all symbols from release binaries          | Both     |
| Control flow obfuscation       | O-LLVM compilation for native code               | Both     |
| Anti-tampering                 | Self-checksum verification in native code        | Both     |
| Secure initialization          | Zero sensitive data after use (`memset_s`)       | Both     |

---

## 4. Application Classification Matrix: When Track B is Mandatory

### 4.1 Financial Applications

| Sub-category           | Examples                             | Track B Mandatory | Regulatory Framework                                |
| ---------------------- | ------------------------------------ | ----------------- | --------------------------------------------------- |
| Banking applications   | Mobile banking, neobank apps         | Yes               | PSD2, GLBA, local banking regulations               |
| Payment processing     | Payment gateways, POS apps           | Yes               | PCI-DSS, EMVCo                                      |
| Trading platforms      | Stock trading, crypto exchanges      | Yes               | SEC/FINRA, MiFID II                                 |
| Insurance applications | Claims processing, policy management | Yes               | State insurance regulations, HIPAA (if health data) |
| Lending applications   | Loan origination, credit scoring     | Yes               | ECOA, FCRA, TILA                                    |
| Digital wallets        | Mobile wallets, stored value         | Yes               | PCI-DSS, e-money directives                         |

### 4.2 Healthcare Applications

| Sub-category              | Examples                         | Track B Mandatory | Regulatory Framework                    |
| ------------------------- | -------------------------------- | ----------------- | --------------------------------------- |
| EHR/EMR access            | Electronic health record viewers | Yes               | HIPAA, HITECH                           |
| Telemedicine              | Remote consultation platforms    | Yes               | HIPAA, state telemedicine laws          |
| Health tracking           | Medical device companion apps    | Yes               | HIPAA (if PHI), FDA (if medical device) |
| Prescription management   | e-Prescribing, pharmacy apps     | Yes               | DEA regulations, HIPAA                  |
| Clinical trial management | Trial data collection apps       | Yes               | HIPAA, 21 CFR Part 11                   |
| Health insurance          | Claims, eligibility verification | Yes               | HIPAA                                   |

### 4.3 Government Applications

| Sub-category            | Examples                             | Track B Mandatory     | Regulatory Framework |
| ----------------------- | ------------------------------------ | --------------------- | -------------------- |
| Citizen services        | Government service portals           | Yes (if handling PII) | FISMA, NIST 800-53   |
| Law enforcement         | Case management, evidence collection | Yes                   | CJIS Security Policy |
| Defense applications    | Military personnel, operations       | Yes                   | DoD STIGs, NISPOM    |
| Tax and revenue         | Tax filing, payment systems          | Yes                   | IRS Pub 1075, FISMA  |
| Benefits administration | Social security, veterans benefits   | Yes                   | FISMA, Privacy Act   |

### 4.4 Enterprise SSO and Identity Providers

| Sub-category           | Examples                           | Track B Mandatory | Reason                                         |
| ---------------------- | ---------------------------------- | ----------------- | ---------------------------------------------- |
| Corporate SSO          | Okta, Azure AD mobile apps         | Yes               | Credential harvesting target                   |
| Identity providers     | Auth0, Keycloak mobile SDKs        | Yes               | Single point of failure for all connected apps |
| Password managers      | 1Password, Bitwarden mobile        | Yes               | Master key compromise = total breach           |
| Certificate management | Mobile PKI, certificate enrollment | Yes               | Certificate private key protection             |

### 4.5 Decision Tree for Classification

```
                    ┌──────────────────────────────────────┐
                    │ Does the application handle ANY of:   │
                    │ - Financial data (transactions,       │
                    │   account numbers, credit scores)     │
                    │ - Protected Health Information (PHI)  │
                    │ - Classified or Controlled Unclassified│
                    │   Information (CUI)                   │
                    │ - Authentication credentials (SSO,    │
                    │   identity provider, password manager) │
                    │ - Biometric data                      │
                    └──────────────────┬───────────────────┘
                                       │
                              ┌────────▼────────┐
                              │                 │
                             YES               NO
                              │                 │
                              ▼                 ▼
                    ┌─────────────────┐  ┌──────────────────┐
                    │ Track B         │  │ Does the app      │
                    │ MANDATORY       │  │ store PII, handle │
                    │                 │  │ payments (IAP),   │
                    │ Proceed with    │  │ or operate in     │
                    │ all L2 controls │  │ high-threat env?  │
                    └─────────────────┘  └────────┬─────────┘
                                                  │
                                         ┌────────▼────────┐
                                         │                 │
                                        YES               NO
                                         │                 │
                                         ▼                 ▼
                               ┌─────────────────┐  ┌──────────────────┐
                               │ Track B         │  │ Track A (L1)     │
                               │ RECOMMENDED     │  │ SUFFICIENT       │
                               │                 │  │                  │
                               │ Document risk   │  │ Baseline L1      │
                               │ acceptance if   │  │ controls only    │
                               │ Track A chosen  │  │                  │
                               └─────────────────┘  └──────────────────┘
```

---

## 5. Threat Intelligence Integration: Current Mobile Threat Landscape

### 5.1 Frida-Based Dynamic Instrumentation Attacks

**Threat Description**: Frida is a dynamic instrumentation toolkit that allows attackers to inject JavaScript into running processes, hook functions, modify arguments, and bypass security controls in real-time.

| Attack Vector        | Description                                                           | Real-World Examples                                     |
| -------------------- | --------------------------------------------------------------------- | ------------------------------------------------------- |
| Function hooking     | Hook root detection, SSL pinning, or biometric verification functions | Multiple banking apps bypassed (2023-2025)              |
| API hooking          | Intercept cryptographic operations to extract keys                    | Key extraction from poorly implemented white-box crypto |
| Process manipulation | Modify return values of security-critical functions                   | Bypassing certificate pinning in 400+ apps              |
| Memory dumping       | Extract sensitive data from application memory                        | Session token extraction                                |

**Track B Mitigations**:

| Control                            | MASVS Reference                        | Effectiveness                                  |
| ---------------------------------- | -------------------------------------- | ---------------------------------------------- |
| Runtime hook detection (V8.4)      | Detects Frida server, hooked functions | High — when properly implemented               |
| Anti-debugging (V8.3)              | Detects debugger attachment            | Medium — Frida operates without debugger flags |
| Memory integrity monitoring (V8.4) | Detects in-memory code modification    | High — detects post-hook tampering             |
| Code obfuscation (V8.5)            | Makes function identification harder   | Medium — defense in depth                      |

### 5.2 App Repackaging Campaigns (Modded APKs)

**Threat Description**: Attackers decompile legitimate applications, insert malicious code (backdoors, ad fraud, data exfiltration), repackage, and distribute through unofficial channels.

| Campaign           | Affected Apps                            | Impact                                 |
| ------------------ | ---------------------------------------- | -------------------------------------- |
| Joker malware      | 100+ Android apps on Play Store          | Premium subscription fraud, data theft |
| CopyCat malware    | Repackaged popular apps                  | Rooting devices, ad fraud              |
| Banking trojans    | Repackaged banking apps                  | Credential theft, transaction fraud    |
| Modded gaming apps | Popular games with "unlimited resources" | Data harvesting, ad injection          |

**Track B Mitigations**:

| Control                       | MASVS Reference                                         | Effectiveness                                  |
| ----------------------------- | ------------------------------------------------------- | ---------------------------------------------- |
| Signature verification (V8.2) | Detects repackaging with different certificate          | High — primary defense                         |
| Tampering detection (V8.2)    | Detects modified resources                              | High — catches resource-level modifications    |
| Play Integrity API (V8.1)     | Verifies app installed from Play Store                  | Medium — only applies to Play-distributed apps |
| Certificate pinning (V5.3)    | Prevents repackaged app from communicating with servers | High — breaks backend connectivity             |

### 5.3 SDK Supply Chain Compromises

**Threat Description**: Third-party SDKs integrated into applications may contain malicious code, inadvertently expose data, or become compromised post-integration.

| Incident               | SDK                   | Impact                                        |
| ---------------------- | --------------------- | --------------------------------------------- |
| MobStori SDK           | Ad SDK                | Data exfiltration from 100+ apps              |
| XcodeGhost             | Compromoted Xcode IDE | App Store apps infected with malware          |
| Various analytics SDKs | Multiple              | Excessive data collection, privacy violations |

**Track B Mitigations**:

| Control                                  | MASVS Reference                               | Effectiveness                          |
| ---------------------------------------- | --------------------------------------------- | -------------------------------------- |
| SBOM generation (V7.5)                   | Full dependency inventory                     | High — enables rapid incident response |
| Dependency vulnerability scanning (V7.5) | Automated scanning for known CVEs             | High — prevents known vulnerable SDKs  |
| SDK runtime behavior monitoring (V7.6)   | Monitor SDK network calls, file access        | Medium — detects anomalous behavior    |
| Network security configuration (V5.2)    | Restrict SDK network access via domain config | Medium — limits SDK connectivity       |

### 5.4 Emulator-Based Fraud and Bot Attacks

**Threat Description**: Attackers use emulated environments to automate fraudulent activities at scale, including account creation fraud, promotion abuse, and automated attacks.

| Attack Type                        | Description                                         | Scale                |
| ---------------------------------- | --------------------------------------------------- | -------------------- |
| Account creation fraud             | Automated creation of fake accounts using emulators | Thousands per day    |
| Promotion abuse                    | Exploiting referral bonuses, sign-up rewards        | Millions in losses   |
| Bot attacks                        | Automated interaction mimicking human behavior      | Variable             |
| Emulator-based reverse engineering | Corellium, Android Emulator for analysis            | Standard RE practice |

**Track B Mitigations**:

| Control                    | MASVS Reference                      | Effectiveness                              |
| -------------------------- | ------------------------------------ | ------------------------------------------ |
| Emulator detection (V8.1)  | Hardware fingerprint analysis        | Medium — sophisticated emulators can spoof |
| Behavioral analysis (V8.4) | Detect bot-like interaction patterns | High — when tuned properly                 |
| Device fingerprinting      | Unique device identification         | Medium — fingerprinting can be spoofed     |
| Rate limiting              | Limit operations per device/session  | High — reduces attack velocity             |

---

## 6. Platform-Specific Threat Patterns

### 6.1 iOS: Secure Enclave, Keychain, App Attest, DeviceCheck

| Capability              | Description                                                 | Track B Usage                                                                                              |
| ----------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Secure Enclave**      | Dedicated security coprocessor for cryptographic operations | Store biometric-authenticated keys, perform key operations without exposing key material to main processor |
| **Keychain**            | Encrypted credential storage                                | Store tokens, certificates, keys with access controls                                                      |
| **App Attest**          | Prove app legitimacy to backend server                      | Generate attestation keys in Secure Enclave, prove app integrity                                           |
| **DeviceCheck**         | Per-device data storage for Apple servers                   | Track device reputation, detect emulator farms                                                             |
| **CryptoKit**           | Modern Swift cryptographic API                              | Perform encryption/decryption with Secure Enclave keys                                                     |
| **LocalAuthentication** | Biometric authentication framework                          | CryptoObject-equivalent for biometric-key binding                                                          |

**iOS Track B Implementation Checklist**:

| #   | Control                       | Implementation Notes                                                |
| --- | ----------------------------- | ------------------------------------------------------------------- |
| 1   | Secure Enclave key generation | Use `SecKeyCreateRandomKey` with `SecAccessControlCreateFlags`      |
| 2   | Key protection                | `biometryCurrentSet` or `devicePasscode` access control             |
| 3   | App Attest integration        | Generate attestation key, request attestation, validate with server |
| 4   | Certificate pinning           | Implement in `URLSessionDelegate` with `URLAuthenticationChallenge` |
| 5   | Jailbreak detection           | Check for Cydia, SSH, unauthorized file paths, sandbox escape       |
| 6   | Code signature validation     | `SecStaticCodeCreate` + `SecStaticCodeCheckValidity`                |
| 7   | Anti-debugging                | `ptrace(PT_DENY_ATTACH)` on startup                                 |
| 8   | Keychain access               | Limit to `kSecAttrAccessibleWhenUnlocked`                           |

### 6.2 Android: StrongBox, Keystore, Play Integrity API, SafetyNet

| Capability                   | Description                                          | Track B Usage                                              |
| ---------------------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| **StrongBox Keymaster**      | Hardware Security Module (HSM) for key storage       | Highest assurance key storage, hardware-backed attestation |
| **Android Keystore**         | Platform key management (TEE-backed where available) | Store cryptographic keys with access controls              |
| **Play Integrity API**       | Verify app integrity and device authenticity         | Replace SafetyNet for Play-distributed apps                |
| **SafetyNet Attestation**    | Legacy device integrity verification                 | Migrate to Play Integrity; SafetyNet deprecated            |
| **BiometricPrompt**          | Standardized biometric authentication                | CryptoObject for biometric-key binding                     |
| **Hardware-backed Keystore** | Keys generated/stored in TEE or StrongBox            | Mandatory for Track B where hardware available             |

**Android Track B Implementation Checklist**:

| #   | Control                    | Implementation Notes                                            |
| --- | -------------------------- | --------------------------------------------------------------- |
| 1   | StrongBox key generation   | Use `KeyGenParameterSpec.Builder.setIsStrongBoxBacked(true)`    |
| 2   | Key attestation            | Verify hardware attestation certificate chain                   |
| 3   | Play Integrity integration | Call Play Integrity API, verify token server-side               |
| 4   | Biometric CryptoObject     | `BiometricPrompt.CryptoObject` wrapping `Cipher` or `Signature` |
| 5   | Root detection             | Check SU binaries, test-keys, dangerous packages, Magisk        |
| 6   | APK signature verification | Verify via `PackageInfo.signatures` + manual certificate check  |
| 7   | Network security config    | Configure certificate pinning in `network_security_config.xml`  |
| 8   | FLAG_SECURE                | Apply to sensitive activities to prevent screenshots            |

### 6.3 Cross-Platform: KMP/Flutter-Specific Resilience Patterns

#### Kotlin Multiplatform (KMP)

| Concern                  | Approach                                                                               | Notes                                                                                 |
| ------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Root/Jailbreak detection | `expect/actual` pattern — platform-specific implementations in Android/iOS source sets | KMP shared module defines interface, platform implementations provide detection logic |
| Keystore access          | `expect/actual` for Keychain (iOS) and Keystore (Android)                              | Shared module uses abstracted key operations                                          |
| Certificate pinning      | Platform-specific networking layer                                                     | Ktor client engine configuration per platform                                         |
| Code obfuscation         | R8 for Android portion, no direct iOS equivalent                                       | iOS native binary benefits from default symbol stripping                              |
| Anti-debugging           | Platform-specific native code                                                          | Implement in platform source sets                                                     |

#### Flutter

| Concern                  | Approach                                       | Notes                                                        |
| ------------------------ | ---------------------------------------------- | ------------------------------------------------------------ |
| Root/Jailbreak detection | Platform channels to native detection code     | Use `flutter_jailbreak_detection` or custom native code      |
| Keystore access          | Platform channels to native keystore APIs      | Use `flutter_secure_storage` plugin or custom implementation |
| Certificate pinning      | `SecurityContext` with pinned certificates     | Configure `HttpClient` with pinned certificates              |
| Code obfuscation         | Dart code is AOT-compiled; limited obfuscation | Focus on native code obfuscation via platform build settings |
| Anti-debugging           | Platform-specific native code                  | Implement via platform channels                              |

**Cross-Platform Track B Considerations**:

| Consideration             | Risk                                                                | Mitigation                                                          |
| ------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Platform channel security | Inter-platform communication may expose data                        | Encrypt sensitive data passed through platform channels             |
| Dependency divergence     | Platform-specific dependencies may have different security postures | Maintain synchronized dependency versions, audit both platforms     |
| Testing complexity        | Security testing must cover both platform implementations           | Separate test suites for Android and iOS platform channels          |
| Code sharing limitations  | Security-critical code often cannot be shared                       | Implement security controls natively, share only non-security logic |

---

## 7. Stage 6/8 Verification: Track B Mastery Verification

### 7.1 Stage 6 Code Review — Track B Verification

At Stage 6 (Code Review), Track B compliance is verified through systematic review of all L2 controls. The review panel includes the CTO, CSO, and CPO.

#### Code Review Checklist — Track B

| Category            | Check                                                                | Pass/Fail | Notes |
| ------------------- | -------------------------------------------------------------------- | --------- | ----- |
| V8.1 Root Detection | Root/jailbreak detection implemented on both platforms               |           |       |
| V8.1 Root Detection | Detection runs on cold start, warm start, and at runtime intervals   |           |       |
| V8.1 Root Detection | Appropriate response behavior implemented (block, degrade, or alert) |           |       |
| V8.2 Tampering      | APK/IPA signature verification implemented                           |           |       |
| V8.2 Tampering      | Resource integrity verification implemented                          |           |       |
| V8.2 Tampering      | Runtime code injection detection implemented                         |           |       |
| V8.3 Anti-Debug     | Debugger detection implemented                                       |           |       |
| V8.3 Anti-Debug     | Timing-based detection implemented                                   |           |       |
| V8.3 Anti-Debug     | Emulator detection implemented                                       |           |       |
| V8.4 RASP           | Frida hook detection implemented                                     |           |       |
| V8.4 RASP           | Memory integrity monitoring implemented                              |           |       |
| V8.4 RASP           | Secure crash handling implemented (no info leakage)                  |           |       |
| V8.5 Obfuscation    | Code obfuscation enabled and verified                                |           |       |
| V8.5 Obfuscation    | String encryption for sensitive strings                              |           |       |
| V8.6 White-Box      | White-box cryptography implemented (if applicable)                   |           |       |
| V1-V7 Enhanced      | Hardware-backed keystore used where available                        |           |       |
| V1-V7 Enhanced      | Key rotation policy implemented                                      |           |       |
| V1-V7 Enhanced      | Certificate pinning configured                                       |           |       |
| V1-V7 Enhanced      | Biometric cryptographic binding implemented                          |           |       |
| V1-V7 Enhanced      | MFA implemented for sensitive operations                             |           |       |

#### Defect Classification for Track B Gaps

| Gap                                            | Classification | Rationale                                                       |
| ---------------------------------------------- | -------------- | --------------------------------------------------------------- |
| No root/jailbreak detection on either platform | P0             | Complete absence of V8.1 — critical defense-in-depth gap        |
| Root detection with no response behavior       | P1             | Detection without action provides false sense of security       |
| No tampering detection (V8.2)                  | P0             | Application can be repackaged without detection                 |
| No anti-debugging (V8.3)                       | P1             | Application is trivially analyzable at runtime                  |
| No RASP capabilities (V8.4)                    | P1             | No runtime self-protection against active attacks               |
| Obfuscation disabled                           | P1             | Code is readily analyzable, facilitates reverse engineering     |
| Software keystore without justification        | P1             | Hardware keystore is Track B requirement                        |
| No certificate pinning                         | P1             | Network traffic is interceptable via MitM                       |
| No biometric cryptographic binding             | P2             | Biometric authentication exists but not cryptographically bound |
| No key rotation policy                         | P2             | Keys remain valid indefinitely                                  |
| Missing backup pins                            | P3             | Certificate rotation may cause connectivity failure             |

### 7.2 Stage 8 Integrity Verification — Track B Checklist

Stage 8 (Integrity Verification) validates that all Track B controls function correctly in the integrated application.

#### Integrity Verification Checklist — Track B

| #   | Verification                               | Method                                                  | Expected Result                            |
| --- | ------------------------------------------ | ------------------------------------------------------- | ------------------------------------------ |
| 1   | Root detection triggers on rooted device   | Install on rooted device, launch app                    | Detection within 5 seconds                 |
| 2   | Root detection bypass attempt (MagiskHide) | Run with MagiskHide enabled                             | Detection still triggers                   |
| 3   | APK repackaging detected                   | Repackage with different certificate                    | Signature verification fails               |
| 4   | IPA modification detected                  | Modify IPA, re-sign with different cert                 | Code signature validation fails            |
| 5   | Debugger attachment detected               | Attach lldb/gdb to running app                          | Detection and response                     |
| 6   | Emulator environment detected              | Run on Genymotion/Corellium                             | Emulator detection triggers                |
| 7   | Frida hook detected                        | Hook critical function with Frida                       | Hook detection triggers                    |
| 8   | Memory modification detected               | Modify memory via Frida                                 | Integrity violation detected               |
| 9   | Certificate pinning enforced               | Attempt MitM with trusted CA cert                       | Connection rejected                        |
| 10  | Hardware keystore used                     | Inspect key generation parameters                       | Key is hardware-backed                     |
| 11  | Biometric key binding works                | Authenticate with biometric, attempt key access without | Key access only after successful biometric |
| 12  | Crash log information audit                | Force crash, examine crash log                          | No sensitive information leaked            |
| 13  | Obfuscation verified                       | Decompile with Jadx/Hopper                              | Critical logic not readily understandable  |
| 14  | String encryption verified                 | Extract strings from binary                             | Sensitive strings not in plaintext         |
| 15  | Key rotation executed                      | Wait for rotation interval or trigger manually          | Old keys invalidated, new keys active      |

### 7.3 Evidence Package Structure for L2 Compliance

The following evidence package must be assembled for Track B compliance sign-off:

```
company/project/<project>/security/compliance/track-b-evidence/
├── README.md                          # Evidence package index
├── V8-resilience/
│   ├── root-detection-implementation.md
│   ├── root-detection-test-results.md
│   ├── evasion-test-report.md
│   ├── tamper-detection-design.md
│   ├── signature-verification-results.md
│   ├── runtime-injection-detection-log.md
│   ├── anti-debug-implementation.md
│   ├── debugger-attachment-test-results.md
│   ├── emulator-detection-report.md
│   ├── rasp-architecture.md
│   ├── frida-hook-detection-results.md
│   ├── memory-integrity-verification.md
│   ├── crash-log-audit.md
│   ├── obfuscation-verification-report.md
│   └── whitebox-crypto-implementation.md (if applicable)
├── V1-V7-enhanced/
│   ├── hardware-keystore-attestation.md
│   ├── key-rotation-policy.md
│   ├── certificate-pinning-config.md
│   ├── biometric-crypto-binding-verification.md
│   ├── mfa-implementation-evidence.md
│   ├── forward-secrecy-verification.md
│   └── native-library-protection-report.md
├── threat-model/
│   ├── initial-threat-model.md
│   ├── threat-model-update-latest.md
│   └── adversarial-capability-assessment.md
├── penetration-test/
│   ├── penetration-test-report.md
│   ├── remediation-verification.md
│   └── residual-risk-assessment.md
└── compliance-matrix/
    ├── track-a-compliance-matrix.md
    ├── track-b-compliance-matrix.md
    └── gap-remediation-plan.md (if any gaps exist)
```

### 7.4 Defect Classification for Track B Gaps

Track B defects are classified using the standard P0-P3 system, with Track B gaps generally classified at higher severity due to the defense-in-depth nature:

| Scenario                                  | Classification | Reasoning                                       |
| ----------------------------------------- | -------------- | ----------------------------------------------- |
| Complete absence of V8 category           | P0             | Entire defense-in-depth layer missing           |
| V8 control implemented but non-functional | P0             | False sense of security is as bad as no control |
| V8 control functional but with bypass     | P1             | Control is partially effective                  |
| V1-V7 enhancement missing                 | P1-P2          | Depends on specific control and risk assessment |
| V8 control suboptimal but functional      | P2             | Control works but could be improved             |
| Documentation/evidence gap                | P2-P3          | Control implemented but evidence incomplete     |

---

## 8. External Certification Path: MASVS Level 2 Certification

### 8.1 Engaging Accredited MASVS Assessors

MASVS Level 2 certification requires assessment by an accredited assessor or qualified security professional.

| Step | Action                                       | Responsible Party | Timeline                    |
| ---- | -------------------------------------------- | ----------------- | --------------------------- |
| 1    | Identify accredited assessor                 | CSO + CTO         | 2-4 weeks                   |
| 2    | Request proposal and statement of work       | CSO               | 1-2 weeks                   |
| 3    | Execute NDA and assessment agreement         | Legal + CSO       | 1 week                      |
| 4    | Provide evidence package to assessor         | CSO + CTO         | Concurrent with step 3      |
| 5    | Assessor conducts review (on-site or remote) | Assessor          | 2-4 weeks                   |
| 6    | Assessor issues findings report              | Assessor          | 1 week after review         |
| 7    | Remediate any findings                       | Development team  | Per finding severity        |
| 8    | Assessor validates remediation               | Assessor          | 1-2 weeks                   |
| 9    | Certification issued                         | Assessor          | Upon successful remediation |

#### Sources for Accredited Assessors

| Source                         | Description                                                  |
| ------------------------------ | ------------------------------------------------------------ |
| OWASP MASVS community          | List of qualified assessors familiar with the standard       |
| Mobile security firms          | Specialized mobile application security consultancies        |
| Big Four advisory firms        | Deloitte, PwC, EY, KPMG mobile security practices            |
| Boutique mobile security firms | Firms specializing exclusively in mobile security assessment |

### 8.2 Preparing Evidence Packages for External Review

| Evidence Category          | Required Artifacts                                      | Preparation Notes                              |
| -------------------------- | ------------------------------------------------------- | ---------------------------------------------- |
| Architecture documentation | System architecture, data flow diagrams, threat model   | Ensure diagrams are current and accurate       |
| Security requirements      | PRD security section, SRD                               | Map requirements to MASVS categories           |
| Implementation evidence    | Code review reports, test results, configuration files  | Organize by MASVS category (V1-V8)             |
| Testing results            | Unit tests, integration tests, penetration test reports | Include both automated and manual test results |
| Compliance matrix          | Track A + Track B compliance matrix                     | Self-assessment before external assessment     |
| Remediation evidence       | Evidence of finding remediation                         | Show before/after for each remediated finding  |

#### Evidence Package Organization

```
track-b-certification-package/
├── README.md                    # Package overview and index
├── 01-executive-summary.md      # High-level overview for assessors
├── 02-compliance-matrix.md      # Self-assessment against MASVS L2
├── 03-architecture/             # Architecture documentation
├── 04-implementation/           # Implementation evidence by category
│   ├── V1-architecture-design/
│   ├── V2-data-storage-privacy/
│   ├── V3-cryptography/
│   ├── V4-authentication-session/
│   ├── V5-network-communication/
│   ├── V6-platform-interaction/
│   ├── V7-code-quality-build/
│   └── V8-resilience-re/
├── 05-testing/                  # Testing evidence
│   ├── unit-tests/
│   ├── integration-tests/
│   ├── penetration-tests/
│   └── regression-tests/
├── 06-remediation/              # Remediation evidence
│   ├── findings-and-remediation.md
│   └── residual-risk-assessment.md
└── 07-appendix/                 # Supporting documentation
    ├── glossary.md
    ├── abbreviations.md
    └── references.md
```

### 8.3 Managing Certification Lifecycle

#### Certification Validity and Renewal

| Aspect                           | Requirement                              | Notes                                                 |
| -------------------------------- | ---------------------------------------- | ----------------------------------------------------- |
| Initial certification            | Valid for 12 months from issuance        | Assessor may specify different period                 |
| Annual re-assessment             | Required to maintain certification       | May be streamlined if no significant changes          |
| Significant change re-assessment | Required for major architectural changes | New platforms, major feature additions                |
| Incident-triggered re-assessment | Required after security incident         | Breach, vulnerability disclosure, compromise          |
| Continuous compliance            | Ongoing self-assessment against MASVS    | Internal team monitors compliance between assessments |

#### Certification Lifecycle Process

```
┌─────────────────┐
│ Initial         │
│ Certification   │
│ (Full Assessment)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Continuous      │
│ Monitoring      │
│ (Self-Assessment)│
└────────┬────────┘
         │
    ┌────▼─────┐
    │          │
    ▼          ▼
┌─────────┐  ┌──────────────────┐
│ Annual   │  │ Significant       │
│ Renewal  │  │ Change Detected   │
│ (Streamlined│  │ (Triggered        │
│  Assessment)│  │  Assessment)     │
└─────┬───┘  └────────┬─────────┘
      │                │
      └────────┬───────┘
               ▼
      ┌─────────────────┐
      │ Updated         │
      │ Certification   │
      │ Issued/Revoked  │
      └─────────────────┘
```

### 8.4 Handling Certification Disputes or Conditional Certifications

#### Dispute Resolution Process

| Step | Action                                                 | Timeline                              |
| ---- | ------------------------------------------------------ | ------------------------------------- |
| 1    | Assessor issues findings report                        | Per assessment agreement              |
| 2    | Organization reviews findings                          | 5 business days                       |
| 3    | Organization may dispute findings with evidence        | 10 business days from findings report |
| 4    | Independent review of disputed findings                | As agreed by both parties             |
| 5    | Final determination by assessment body                 | 15 business days from dispute         |
| 6    | Certification issued with or without disputed findings | Per final determination               |

#### Conditional Certification Scenarios

| Scenario                                  | Condition                                             | Resolution Path                                          |
| ----------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------- |
| Minor findings open                       | Certification issued with conditions                  | Remediate within agreed timeframe (typically 30-90 days) |
| Major findings with compensating controls | Certification issued pending remediation              | Implement permanent remediation, verify with assessor    |
| Architecture documentation incomplete     | Certification conditional on documentation completion | Complete documentation within agreed timeframe           |
| Testing coverage gaps                     | Certification conditional on test completion          | Execute missing tests, submit results                    |
| Pending third-party SDK remediation       | Certification conditional on SDK vendor fix           | Apply vendor patch or implement compensating controls    |

#### Conditional Certification Tracking

| Condition                            | Identified Date | Agreed Resolution Date | Status      | Notes                             |
| ------------------------------------ | --------------- | ---------------------- | ----------- | --------------------------------- |
| (Example) V8.4 RASP incomplete       | 2026-04-01      | 2026-05-01             | In Progress | Implementing Frida hook detection |
| (Example) Key rotation not automated | 2026-04-01      | 2026-04-15             | Complete    | Automated rotation deployed       |

---

## Appendix A: Track B Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────────────┐
│ MASVS TRACK B — QUICK REFERENCE                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ MANDATORY FOR: Banking, Healthcare, Government, Enterprise SSO           │
│ RECOMMENDED FOR: Social media, E-commerce with stored payment data       │
│ OPTIONAL FOR: General consumer apps, gaming (unless IAP)                 │
├─────────────────────────────────────────────────────────────────────────┤
│ TRACK B = TRACK A (V1-V7 L1) + V1-V7 L2 ENHANCEMENTS + V8 RESILIENCE    │
├─────────────────────────────────────────────────────────────────────────┤
│ V8 CATEGORIES (Track B exclusive):                                      │
│   V8.1 Root/Jailbreak Detection — detect and respond                    │
│   V8.2 Tampering Detection — signature + integrity verification         │
│   V8.3 Anti-Debugging — debugger detection, timing analysis             │
│   V8.4 RASP — hook detection, memory integrity, behavioral analysis     │
│   V8.5 Obfuscation — code, string, control flow obfuscation             │
│   V8.6 White-Box Cryptography — key protection in software              │
├─────────────────────────────────────────────────────────────────────────┤
│ KEY L2 ENHANCEMENTS:                                                    │
│   - Hardware-backed keystores (StrongBox, Secure Enclave)               │
│   - Certificate pinning + mTLS                                         │
│   - Biometric cryptographic binding                                     │
│   - MFA for sensitive operations                                        │
│   - Key rotation policy (90 days symmetric, 1 year asymmetric)          │
│   - Perfect forward secrecy                                             │
│   - SBOM + dependency scanning                                          │
│   - Native library protection                                           │
├─────────────────────────────────────────────────────────────────────────┤
│ STAGE 6/8 VERIFICATION:                                                 │
│   - Code review against Track B checklist                               │
│   - Integrity verification with 15-point checklist                      │
│   - Evidence package assembly                                           │
│   - Defect classification: V8 gaps typically P0-P1                      │
└─────────────────────────────────────────────────────────────────────────┘
```

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

## Appendix C: MASVS V8 Mapping to OWASP Mobile Top 10

| OWASP Mobile Top 10           | MASVS V8 Coverage      | Track B Contribution                         |
| ----------------------------- | ---------------------- | -------------------------------------------- |
| M1: Improper Platform Usage   | V8.1, V8.2, V8.3       | Ensures platform security features utilized  |
| M2: Insecure Data Storage     | V8.2 (integrity)       | Protects stored data from modification       |
| M3: Insecure Communication    | V8.4 (RASP)            | Detects active MitM attacks                  |
| M4: Insecure Authentication   | V8.3, V8.4             | Prevents authentication bypass via debugging |
| M5: Insufficient Cryptography | V8.6 (white-box)       | Protects keys in software implementations    |
| M6: Insecure Authorization    | V8.2 (tampering)       | Prevents authorization logic modification    |
| M7: Client Code Quality       | V8.5 (obfuscation)     | Reduces attack surface through obfuscation   |
| M8: Code Tampering            | V8.2, V8.3, V8.4       | Direct coverage across multiple controls     |
| M9: Reverse Engineering       | V8.3, V8.4, V8.5, V8.6 | Direct coverage across all V8 categories     |
| M10: Extraneous Functionality | V8.2 (tampering)       | Detects unauthorized functionality addition  |
