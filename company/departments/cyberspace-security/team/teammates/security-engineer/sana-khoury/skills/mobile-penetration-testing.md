---
name: mobile-penetration-testing
description: "Conduct comprehensive mobile penetration tests — static binary analysis, Frida-based dynamic instrumentation, MITM network interception, and reverse engineering — to discover exploitable vulnerabilities in Android and iOS applications."
version: "1.0.0"
---

| Competency                 | Description                                                     | Quality Criteria                                                                                                                                                                                                          |
| -------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Static Analysis            | Reverse engineering of APK/IPA binaries without execution       | Decompiles DEX to readable Java via Jadx with 95%+ recovery rate; reconstructs ProGuard-obfuscated control flow in Ghidra; identifies hardcoded secrets in native libraries (`.so`, `.dylib`) using `strings` + `objdump` |
| Dynamic Analysis           | Runtime instrumentation and behavioral analysis of running apps | Hooks 90%+ of target methods via Frida scripts in <2 hours; bypasses root/jailbreak detection, SSL pinning, and anti-debugging protections; traces cryptographic operations and key extraction at runtime                 |
| Network Interception       | MITM analysis of mobile app communication channels              | Configures Burp Suite with mobile proxy + CA certificate pinning bypass; intercepts and mutates WebSocket, gRPC, and MQTT traffic; identifies insecure API endpoints and data exposure                                    |
| Reverse Engineering        | Deep binary analysis for vulnerability discovery                | Maps native code attack surfaces in ARM64/x86_64; identifies buffer overflows, format string vulns, and insecure IPC in shared libraries; reconstructs custom encryption protocols from disassembly                       |
| Vulnerability Exploitation | Proof-of-concept exploit development                            | Develops working PoCs for identified vulnerabilities (insecure data storage, broken cryptography, intent hijacking, deep link abuse); demonstrates impact without causing data loss                                       |
| OWASP MASVS Assessment     | Structured verification against MASVS controls                  | Maps every finding to specific MASVS requirement (V1–V8); produces assessment reports that directly feed Stage 6 Code Review and Stage 8 Integrity Verification gate criteria                                             |

## Execution Guidance

### 1. Pre-Engagement Reconnaissance

**Scope Definition:**

- Confirm target app version(s), build numbers, and platform(s) (iOS, Android, or both)
- Identify the app's security tier per SRD classification (e.g., financial data = MASVS Level 2 + MSTG)
- Gather threat model from Stage 1 SRD to prioritize attack surfaces
- Confirm rules of engagement: production vs. staging environment, data handling constraints

**Information Gathering:**

- Download target APK from Play Store (using `apktool` or third-party downloaders) or obtain IPA from TestFlight/enterprise distribution
- Enumerate app's public attack surface: app store metadata, manifest-permission requests, deep link schemes, associated domains, public API endpoints
- Review app's privacy policy, security.txt, and any published security documentation
- Map the app's third-party dependencies (SDKs, libraries) using `pipdeptree` equivalent for mobile: `apktool d <apk>` → inspect `AndroidManifest.xml`, `lib/`, `assets/`

### 2. Static Analysis Phase

**Automated Static Analysis with MobSF:**

```bash
# Deploy MobSF (Docker recommended for reproducibility)
docker pull opensecurity/mobile-security-framework-mobsf
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf

# Upload APK/IPA via web UI or REST API
curl -X POST -F "file=@app-release.apk" http://localhost:8000/api/v1/upload
curl -X POST -F "hash=<returned_hash>" http://localhost:8000/api/v1/scan
```

**MobSF Output Review — Critical Checkpoints:**

1. **Manifest analysis**: exported activities/services/receivers with missing permission guards; `android:allowBackup="true"`; `android:debuggable="true"`; cleartext traffic permitted
2. **Code-level findings**: hardcoded API keys, AWS credentials, Firebase tokens; hardcoded encryption keys/IVs; insecure random number generation (`java.util.Random` vs `SecureRandom`)
3. **WebView vulnerabilities**: `setJavaScriptEnabled(true)`, `addJavascriptInterface()`, missing `setAllowFileAccess(false)` — all potential RCE vectors
4. **Platform API misuse**: insecure SharedPreferences usage, world-readable files, implicit intents with sensitive data
5. **Binary protections**: absence of code obfuscation (ProGuard/R8), missing native library strip, absent anti-tampering checks

**Manual Static Analysis — Deep Dive:**

**Jadx-GUI Decompilation:**

```bash
jadx -d output/ --deobf --deobf-min 3 app-release.apk
# --deobf enables deobfuscation; --deobf-min sets minimum name length
```

- Search for cryptographic operations: `Cipher.getInstance()`, `SecretKeySpec`, `MessageDigest` — verify algorithm strength (AES-GCM ≥ 128-bit, no ECB mode, no MD5/SHA1 for integrity)
- Search for network operations: `OkHttpClient`, `Retrofit`, `NSURLSession` — verify TLS configuration, certificate pinning implementation
- Search for storage operations: `SharedPreferences`, `SQLiteOpenHelper`, `RoomDatabase` — verify encryption at rest (SQLCipher, EncryptedSharedPreferences)
- Search for authentication logic: token handling, session management, biometric integration (`BiometricPrompt`, `LAContext`)
- Review custom cryptographic implementations — flag any non-standard algorithms or home-grown key derivation

**Native Library Analysis:**

```bash
# Extract native libraries
unzip app-release.apk "lib/*" -d native-libs/

# Analyze ARM64 shared library
ghidra native-libs/lib/arm64-v8a/libcrypto.so

# Key checks in Ghidra:
# 1. Symbol table for exposed functions (should be stripped)
# 2. Strings panel for hardcoded secrets
# 3. Imports panel for dangerous APIs (system, exec, dlopen)
# 4. Cross-references to cryptographic functions
```

### 3. Dynamic Analysis Phase

**Frida Instrumentation:**

**Environment Setup:**

```bash
pip install frida frida-tools objection
# Verify device connectivity
frida-ps -U
# List running apps on device
```

**Core Frida Scripts — Production Templates:**

_Bypass SSL Pinning:_

```javascript
// ssl-unpinning.js — Android OkHttp + NSURLSession bypass
Java.perform(function () {
  // OkHttp 3.x CertificatePinner check bypass
  var CertificatePinner = Java.use("okhttp3.CertificatePinner");
  CertificatePinner.check.overload(
    "java.lang.String",
    "java.util.List",
  ).implementation = function () {};

  // TrustManager bypass — accept all certificates
  var TrustManager = Java.registerClass({
    name: "com.example.TrustManager",
    implements: [Java.use("javax.net.ssl.X509TrustManager")],
    methods: [
      {
        name: "checkClientTrusted",
        returnType: "void",
        argumentTypes: [
          "javax.security.cert.X509Certificate[]",
          "java.lang.String",
        ],
      },
      {
        name: "checkServerTrusted",
        returnType: "void",
        argumentTypes: [
          "javax.security.cert.X509Certificate[]",
          "java.lang.String",
        ],
      },
      {
        name: "getAcceptedIssuers",
        returnType: "java.security.cert.X509Certificate[]",
        argumentTypes: [],
        implementation: function () {
          return [];
        },
      },
    ],
  });
  var SSLContext = Java.use("javax.net.ssl.SSLContext");
  SSLContext.init.overload(
    "[Ljavax.net.ssl.KeyManager;",
    "[Ljavax.net.ssl.TrustManager;",
    "java.security.SecureRandom",
  ).implementation = function (km, tm, sr) {
    this.init(km, [TrustManager.$new()], sr);
  };
});
```

_Runtime Method Tracing:_

```javascript
// trace-crypto.js — Hook all cryptographic operations
Java.perform(function () {
  var Cipher = Java.use("javax.crypto.Cipher");
  Cipher.doFinal.overload("[B").implementation = function (input) {
    console.log("[CRYPTO] doFinal called");
    console.log("[CRYPTO] Input (hex): " + bytesToHex(input));
    console.log("[CRYPTO] Algorithm: " + this.getAlgorithm());
    console.log(
      "[CRYPTO] Key (hex): " + bytesToHex(this.getParameters().getEncoded()),
    );
    var result = this.doFinal(input);
    console.log("[CRYPTO] Output (hex): " + bytesToHex(result));
    return result;
  };
});
```

**Objection Runtime Exploration:**

```bash
# Launch with Frida Gadget or injected agent
objection -g com.example.app explore

# Inside objection REPL:
# Memory analysis
memory list modules              # List loaded libraries
memory search "-----BEGIN RSA"   # Search for keys in memory
memory dump all dumped.mem       # Full memory dump for forensic analysis

# Keychain/Keystore access
ios keychain                     # Dump iOS Keychain (jailbroken device)
android keystore list            # List Android Keystore entries

# Activity/Intent analysis
android intent launch_activity com.example.app.SecretActivity
android hooking list activities  # Enumerate exported activities

# File system access
file list /data/data/com.example.app/shared_prefs/
file download /data/data/com.example.app/databases/app.db .
```

**Root/Jailbreak Detection Bypass:**

```bash
# Using objection
objection -g com.example.app explore
android root disable             # Disable common root detection
ios jailbreak disable            # Disable common jailbreak detection

# Custom Frida scripts for advanced detection bypass:
# Hook SafetyNet/Play Integrity API responses
# Hook jailbreak file existence checks (/sbin/su, /Applications/Cydia.app)
# Hook PackageManager.isSafeMode() responses
```

### 4. Network Interception

**Burp Suite Configuration for Mobile:**

1. Configure Burp proxy listener on `0.0.0.0:8080`
2. Install Burp CA certificate on device:
   - Android: `adb push cacert.der /data/local/tmp/burpca.der` → install via Settings → Security → Install from storage
   - Android 7+: CA must be installed as system certificate (requires root) or use `networkSecurityConfig` override
   - iOS: AirDrop cacert.der → Install Profile → Enable in Settings → General → About → Certificate Trust Settings
3. Configure device WiFi proxy to point to Burp host
4. For certificate-pinned apps: deploy Frida SSL unpinning script (see above) or use Burp's `SSL Pass-Through` for pinned domains

**Traffic Analysis Checklist:**

- [ ] All connections use TLS 1.2+ (no SSLv3, TLS 1.0, TLS 1.1)
- [ ] Certificate validation is enforced (not accepting self-signed in production)
- [ ] Sensitive data is not transmitted in URLs or headers
- [ ] API tokens are not logged or exposed in response bodies
- [ ] WebSocket connections are encrypted (wss:// not ws://)
- [ ] No sensitive data in push notification payloads (FCM/APNs)
- [ ] HTTP Strict Transport Security (HSTS) headers present on API responses
- [ ] API rate limiting and abuse prevention in place

### 5. Vulnerability Exploitation & Proof of Concept

**Common Mobile Attack Vectors:**

| Attack Vector             | Impact                                               | Testing Method                                                   |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------- |
| Insecure Data Storage     | Credential/key theft                                 | Extract app data via `adb backup` or rooted filesystem access    |
| Broken Cryptography       | Data decryption at rest/in transit                   | Identify algorithm/mode; attempt known-plaintext attack          |
| Insecure Communication    | MITM data interception                               | Burp Suite interception with/without pinning bypass              |
| Insecure Authentication   | Account takeover                                     | Token replay, session fixation, biometric bypass                 |
| Insufficient Cryptography | Key recovery                                         | Memory dumping, key extraction from Keychain/Keystore            |
| Client Code Quality       | Reverse engineering, tampering                       | Decompile, modify, repack, and resign APK/IPA                    |
| Code Tampering            | Unauthorized behavior modification                   | Patch smali/IL code, bypass license checks, inject hooks         |
| Reverse Engineering       | Intellectual property theft, vulnerability discovery | Full decompilation + analysis of business logic                  |
| Extraneous Functionality  | Unauthorized access to hidden features               | Enumerate hidden activities, debug flags, test endpoints         |
| Platform Interaction      | Intent hijacking, URL scheme abuse                   | Craft malicious intents/deep links targeting exported components |

**PoC Development Standards:**

- Demonstrate impact without destroying user data
- Use non-destructive proof-of-concept payloads
- Document exact reproduction steps (app version, device, OS version)
- Include Frida/Burp configuration used for exploitation
- Map to CVSS v3.1 score and MASVS requirement

### 6. Reporting & Defect Classification

**Finding Documentation Format:**

```markdown
### Finding #N: [Title]

**Severity:** P0/P1/P2/P3
**MASVS Reference:** V[1-8].[N]
**CVSS v3.1 Score:** X.X (Vector: ...)
**Platform:** Android / iOS / Both
**Affected Version:** vX.Y.Z (build NNN)

**Description:**
[Concise technical description of the vulnerability]

**Reproduction Steps:**

1. [Step-by-step reproduction]
2. ...

**Evidence:**
[Screenshots, code snippets, Burp HTTP history, Frida console output]

**Impact:**
[What an attacker can achieve, business impact assessment]

**Remediation:**
[Specific, actionable fix guidance with code examples where applicable]
```

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                                                                   |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 1** (SRD)                    | Provides threat intelligence input for security requirements; identifies platform-specific attack surfaces that must be addressed in SRD                                      |
| **Stage 6** (Code Review)            | Executes penetration testing as part of the review panel; produces Defect Report with findings classified P0–P3; findings feed directly into code remediation priorities      |
| **Stage 8** (Integrity Verification) | Validates that previously identified vulnerabilities have been properly remediated; conducts regression pen testing on fixed code; verifies no new attack surfaces introduced |
| **Stage 10** (Release Readiness)     | Provides final security assessment sign-off for CSO release checklist item #4 (SRD enforced, OWASP MASVS compliant)                                                           |

## Quality Standards

| Metric                       | Standard                                                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Test Coverage**            | 100% of MASVS Level 1 controls assessed; Level 2 controls assessed for apps handling financial/sensitive data            |
| **Tool Coverage**            | Minimum 3 tools per analysis phase (1 automated + 2 manual) for cross-validation                                         |
| **Finding Quality**          | Every finding includes: reproduction steps, evidence, impact assessment, remediation guidance, MASVS mapping, CVSS score |
| **False Positive Rate**      | < 5% false positive rate in reported findings (validated by peer review)                                                 |
| **Turnaround Time**          | Initial scan results within 2 business days; full report within 5 business days of engagement start                      |
| **Reproducibility**          | 100% of P0/P1 findings must be independently reproducible by a second engineer                                           |
| **Remediation Verification** | All P0/P1 fixes verified within 48 hours of remediation submission                                                       |
