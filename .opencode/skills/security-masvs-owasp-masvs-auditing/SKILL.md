---
name: security-masvs-owasp-masvs-auditing
description: 'Security skill: Owasp Masvs Auditing'
---

# OWASP MASVS Auditing

**Category:** Mobile Security Compliance — MASVS Assessment
**Owner:** Compliance Analyst — Ingrid Solberg

## Overview

Specialized methodology for conducting OWASP Mobile Application Security Verification Standard (MASVS) compliance audits specifically for mobile banking and financial services applications. This skill complements the mobile penetration testing expertise of Sana Khoury by providing the compliance audit perspective — systematic verification, gap analysis, remediation guidance, and auditor-ready reporting. While Sana Khoury executes the technical testing, Ingrid Solberg manages the compliance audit framework, ensures documentation meets regulatory standards, and produces audit reports suitable for banking regulators, external auditors, and compliance officers.

## Competency Dimensions

| Dimension                        | Description                                                      | Proficiency Indicators                                                                                                                                                                                                                  |
| -------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MASVS Audit Methodology          | Structured approach to MASVS compliance auditing                 | Designs audit programs covering all V1–V8 categories; produces audit workpapers that satisfy banking regulator review; achieves zero audit findings on MASVS assessment methodology                                                     |
| Mobile Banking Security Auditing | Domain-specific knowledge of financial app security requirements | Maps MASVS controls to banking-specific regulations (FFIEC, PSD2, RBI guidelines); identifies banking-specific attack vectors (transaction manipulation, account takeover); understands regulatory expectations for mobile banking apps |
| Verification Procedures          | Detailed test procedures for each MASVS requirement              | Creates reproducible verification procedures that any auditor can execute; produces evidence packages that withstand regulatory scrutiny; maintains procedure library updated with MASVS version changes                                |
| Gap Analysis                     | Systematic identification and documentation of compliance gaps   | Produces gap analysis reports with prioritized remediation roadmaps; maps gaps to specific MASVS requirements and regulatory obligations; tracks gap closure with evidence                                                              |
| Remediation Guidance             | Actionable guidance for addressing compliance gaps               | Provides remediation guidance that is technically accurate, feasible, and aligned with MASVS intent; validates remediation effectiveness through re-testing; documents remediation evidence for auditors                                |

## Execution Guidance

### 1. MASVS Audit Program Design

**Audit Scope Definition:**

```markdown
# MASVS Audit Program

**Application:** [Mobile Banking App Name]
**Version:** [vX.Y.Z]
**Assessment Level:** MASVS L1 + L2 + MASVS-R (Resilience)
**Regulatory Context:**

- FFIEC IT Examination Handbook (US)
- PSD2 Regulatory Technical Standards (EU)
- EBA Guidelines on ICT and Security Risk Management
- Local banking authority mobile banking guidelines

**Audit Period:** [Start Date] – [End Date]
**Audit Team:** Ingrid Solberg (Lead Auditor), Sana Khoury (Technical Assessor)

## Scope Inclusions

- Mobile banking application (Android + iOS)
- API backend services
- Third-party SDKs (analytics, crash reporting, payment)
- Authentication and session management
- Transaction processing flows
- Data storage and encryption

## Scope Exclusions

- Core banking system (separate audit)
- Web banking portal (separate audit)
- ATM/branch systems (separate audit)

## Audit Approach

1. Document review (architecture, threat model, security policies)
2. Technical assessment (Sana Khoury — pen testing)
3. Compliance verification (Ingrid Solberg — MASVS audit)
4. Gap analysis and remediation planning
5. Audit report and management presentation
```

### 2. Verification Procedures — Banking-Specific

Each MASVS verification category is assessed using standardized procedures with banking-specific considerations:

#### V1: Architecture & Design — Banking Context

| Req ID | Standard Verification | Banking-Specific Addition                                                                                    |
| ------ | --------------------- | ------------------------------------------------------------------------------------------------------------ |
| 1.1.1  | Security in SDLC      | Verify threat model includes transaction fraud scenarios; security review mandatory for all banking features |
| 1.1.5  | Certificate pinning   | Verify pinning is enforced for all banking API endpoints; pin rotation procedure tested and documented       |
| 1.1.7  | Defense-in-depth      | Verify multiple independent controls protect transactions (device binding + biometric + OTP)                 |

**Verification Procedure — V1.1.5 (Certificate Pinning):**

```
Step 1: Review network_security_config.xml (Android) / Info.plist ATS settings (iOS)
Step 2: Identify pinning implementation (OkHttp CertificatePinner / TrustKit)
Step 3: Verify pins cover all banking API domains
Step 4: Test pinning behavior:
  a. Configure Burp Suite proxy with custom CA
  b. Launch app and attempt API calls
  c. Verify calls fail with SSL handshake error
  d. Confirm no fallback to trust system CA
Step 5: Verify pin rotation procedure:
  a. Review documentation for pin update process
  b. Verify backup pins are configured
  c. Test pin rotation in staging environment
Step 6: Document results with screenshots and configuration snippets

Expected Result: App rejects connections with unpinned certificates;
  no fallback to system trust store; pin rotation tested within 90 days.
```

#### V2: Data Storage — Banking Context

| Req ID | Standard Verification               | Banking-Specific Addition                                                                                                 |
| ------ | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 2.1.2  | No sensitive data unencrypted       | Verify account numbers, balances, transaction history are encrypted; verify no cached transaction data in screenshots     |
| 2.1.4  | No sensitive data via platform APIs | Verify push notifications do not contain account details; verify clipboard is cleared after copy/paste of account numbers |
| 2.1.10 | Secure memory handling              | Verify cryptographic keys zeroed after use; verify transaction data cleared from memory after display                     |

**Verification Procedure — V2.1.2 (Encrypted Storage):**

```
Step 1: Extract app data from test device
  Android: adb backup -f backup.ab -noapk com.example.banking
  iOS: Extract via iTunes backup (encrypted) or filesystem access (jailbroken)
Step 2: Decrypt backup and examine filesystem
Step 3: Search for sensitive data patterns:
  - Account numbers (regex: \d{10,18})
  - Routing numbers (regex: \d{9})
  - Card numbers (Luhn validation)
  - Names, addresses, phone numbers
  - Session tokens, API keys
  - Transaction amounts, descriptions
Step 4: For each file found, verify encryption status:
  - SQLite databases: Check if SQLCipher encrypted
  - SharedPreferences: Check if EncryptedSharedPreferences
  - Files: Check if encrypted at application level
Step 5: Attempt to decrypt with known keys (if any) to verify encryption strength
Step 6: Document all findings with file paths, data samples, and encryption status

Expected Result: No sensitive banking data found in plaintext;
  all stored data encrypted with AES-256 or equivalent.
```

#### V4: Authentication — Banking Context

| Req ID | Standard Verification               | Banking-Specific Addition                                                                                |
| ------ | ----------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 4.1.2  | Biometric authentication            | Verify biometric auth uses CryptoObject binding (not just boolean flag); verify fallback to PIN/password |
| 4.1.4  | OAuth 2.0 / OIDC                    | Verify OAuth flow for third-party banking integrations (Open Banking / PSD2)                             |
| 4.1.7  | Re-authentication for sensitive ops | Verify step-up auth for: new payee addition, large transfers, profile changes, device binding changes    |

**Verification Procedure — V4.1.7 (Step-Up Authentication):**

```
Step 1: Identify sensitive operations requiring re-authentication:
  - Adding new payee/beneficiary
  - Transfers above threshold (verify threshold matches policy)
  - Changing registered phone number or email
  - Enrolling new device
  - Changing transaction limits
  - Exporting transaction history
Step 2: For each operation, test without re-authentication:
  a. Log in with valid credentials
  b. Navigate to sensitive operation
  c. Attempt operation without additional authentication
  d. Verify operation is blocked and re-auth is required
Step 3: Test re-authentication mechanisms:
  a. Biometric re-auth (if enrolled)
  b. PIN/password re-auth
  c. OTP re-auth (if configured)
Step 4: Verify re-authentication token is short-lived (≤5 minutes)
Step 5: Verify failed re-auth attempts are logged and rate-limited
Step 6: Document results for each operation

Expected Result: All sensitive operations require re-authentication;
  re-auth mechanisms are secure; failures are logged and rate-limited.
```

#### V8: Resilience — Banking Context (L2)

| Req ID | Standard Verification       | Banking-Specific Addition                                                                                                  |
| ------ | --------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 8.1.1  | Root/jailbreak detection    | Verify app restricts functionality on rooted/jailbroken devices (not just warning); verify detection uses multiple methods |
| 8.2.1  | Tampering detection         | Verify code integrity checks prevent modified app from connecting to banking APIs                                          |
| 8.3.2  | Hooking framework detection | Verify Frida/Xposed detection prevents dynamic analysis of banking logic                                                   |
| 8.5.1  | RASP                        | Verify RASP detects and responds to runtime attacks; verify response is appropriate (block, alert, degrade)                |

**Verification Procedure — V8.1.1 (Root/Jailbreak Detection):**

```
Step 1: Review root/jailbreak detection implementation:
  - Android: Check for SafetyNet/Play Integrity API usage, su binary detection,
    Magisk detection, build tag checks
  - iOS: Check for Cydia/Sileo detection, file path checks, sandbox escape tests
Step 2: Test detection on clean device:
  a. Install app on non-rooted/non-jailbroken device
  b. Verify app functions normally (no false positives)
Step 3: Test detection on rooted/jailbroken device:
  a. Install app on rooted (Android) or jailbroken (iOS) device
  b. Verify detection triggers within 30 seconds of app launch
  c. Verify app response matches policy:
     - Policy Option A: Full block (app does not function)
     - Policy Option B: Restricted mode (read-only, no transactions)
     - Policy Option C: Warning + logging (not recommended for banking)
Step 4: Test detection bypass attempts:
  a. Use Frida to hook root detection functions
  b. Use Magisk Hide / Zygisk to hide root
  c. Verify detection still triggers (multi-layer detection)
Step 5: Document detection methods, response behavior, and bypass resistance

Expected Result: Root/jailbreak detected reliably; app response matches
  banking security policy; detection resistant to common bypass techniques.
```

### 3. Gap Analysis Methodology

**Gap Analysis Matrix:**

```markdown
# MASVS Gap Analysis — Mobile Banking App

| Req ID | Requirement               | Status     | Gap Description                                                | Risk Level | Remediation                                              | Effort | Target Date |
| ------ | ------------------------- | ---------- | -------------------------------------------------------------- | ---------- | -------------------------------------------------------- | ------ | ----------- |
| V1.1.5 | Certificate pinning       | ⚠️ Partial | Pinning implemented but no backup pins configured              | High       | Add backup pins; test rotation                           | 2 days | 2026-04-15  |
| V2.1.2 | Encrypted storage         | ❌ Fail    | Transaction cache stored in plaintext in app cache directory   | Critical   | Implement SQLCipher; clear cache on background           | 5 days | 2026-04-18  |
| V4.1.7 | Re-auth for sensitive ops | ⚠️ Partial | Re-auth required for transfers but not for payee addition      | High       | Add re-auth to payee addition flow                       | 3 days | 2026-04-16  |
| V6.1.5 | WebView security          | ❌ Fail    | WebView in help section loads external content with JS enabled | High       | Implement URL allowlist; disable JS for external content | 3 days | 2026-04-16  |
| V8.1.1 | Root detection            | ⚠️ Partial | Single-method detection (su binary check only)                 | Medium     | Add Play Integrity API + Magisk detection                | 4 days | 2026-04-20  |
```

**Gap Severity Classification:**

| Gap Severity | Definition                                                   | Regulatory Impact                           | Remediation SLA |
| ------------ | ------------------------------------------------------------ | ------------------------------------------- | --------------- |
| **Critical** | Control completely absent; direct regulatory violation       | Regulatory breach possible; audit failure   | 14 days         |
| **High**     | Control partially implemented; significant security weakness | Potential regulatory finding; customer risk | 30 days         |
| **Medium**   | Control implemented but with deficiencies                    | Minor audit observation                     | 60 days         |
| **Low**      | Best practice not fully implemented                          | No regulatory impact                        | 90 days         |

### 4. Remediation Guidance Framework

**For each identified gap, provide structured remediation guidance:**

````markdown
# Remediation Guidance — V2.1.2 Encrypted Storage

## Gap Description

Transaction cache is stored in plaintext in app cache directory
(`/data/data/com.example.banking/cache/transactions.db`). An attacker
with physical access to an unlocked device or via malware can extract
transaction history including account numbers, amounts, and payee details.

## MASVS Reference

V2.1.2: No sensitive data is written to local storage unencrypted.

## Risk Assessment

- **Likelihood**: Medium (requires device access or malware)
- **Impact**: High (exposure of financial data)
- **Overall**: High (per FFIEC guidelines, financial data exposure is high-impact)

## Remediation Steps

### Step 1: Implement SQLCipher for transaction database

```kotlin
// Replace standard SQLite with SQLCipher
implementation "net.zetetic:android-database-sqlcipher:4.5.4"

// Database initialization
val database = SQLiteDatabase.openOrCreateDatabase(
    context.getDatabasePath("transactions.db"),
    "encryption-key-from-keystore",  // Key from Android Keystore
    null
)
```
````

### Step 2: Migrate existing plaintext data

```kotlin
// One-time migration
val plainDb = SQLiteDatabase.openDatabase(plainDbPath, null, SQLiteDatabase.OPEN_READONLY)
val encryptedDb = SQLiteDatabase.openOrCreateDatabase(encryptedDbPath, key, null)
plainDb.rawQuery("SELECT * FROM transactions", null).use { cursor ->
    while (cursor.moveToNext()) {
        // Insert into encrypted database
    }
}
plainDb.close()
File(plainDbPath).delete()
```

### Step 3: Clear cache on background

```kotlin
override fun onTrimMemory(level: Int) {
    super.onTrimMemory(level)
    if (level >= TRIM_MEMORY_UI_HIDDEN) {
        clearTransactionCache()
    }
}
```

### Step 4: Verify encryption

- Run `file transactions.db` — should show "SQLite 3.x" (encrypted)
- Attempt to open with standard SQLite client — should fail
- Verify all sensitive columns are encrypted

## Testing

1. Install app on test device
2. Perform 10+ transactions
3. Background the app
4. Extract app data
5. Verify transaction database is encrypted
6. Verify cache is cleared after backgrounding

## Estimated Effort

- Development: 3 days
- Testing: 1 day
- Code review: 0.5 days
- Total: 4.5 days

## Validation Criteria

- [ ] Transaction database is SQLCipher-encrypted
- [ ] Encryption key sourced from Android Keystore
- [ ] Cache cleared on app background
- [ ] No plaintext financial data in app storage
- [ ] MASVS V2.1.2 verification passes

````

### 5. Audit Report Template — MASVS

```markdown
# MASVS Compliance Audit Report

**Application:** [Mobile Banking App]
**Version:** [vX.Y.Z]
**Assessment Level:** MASVS L1 + L2 + MASVS-R
**Audit Period:** [Start] – [End]
**Lead Auditor:** Ingrid Solberg
**Technical Assessor:** Sana Khoury

## Executive Summary

The MASVS compliance audit of [Application] was conducted during the period
[dates]. The audit assessed [XX] requirements across 8 verification categories.

| Category | Compliant | Partial | Non-Compliant | Compliance Rate |
|----------|-----------|---------|---------------|-----------------|
| V1: Architecture | X | X | X | XX% |
| V2: Data Storage | X | X | X | XX% |
| V3: Cryptography | X | X | X | XX% |
| V4: Authentication | X | X | X | XX% |
| V5: Network | X | X | X | XX% |
| V6: Platform Interaction | X | X | X | XX% |
| V7: Code Quality | X | X | X | XX% |
| V8: Resilience | X | X | X | XX% |
| **Overall** | **XX** | **XX** | **XX** | **XX%** |

## Critical Findings
[List all Critical and High gaps with regulatory impact assessment]

## Regulatory Mapping
| MASVS Gap | FFIEC Impact | PSD2 Impact | Local Regulator Impact |
|-----------|-------------|-------------|----------------------|
| V2.1.2 | IT Handbook Ch. III | RTS Art. 15 | [Assessment] |
| V4.1.7 | IT Handbook Ch. IV | RTS Art. 22 | [Assessment] |

## Recommendations
[Prioritized recommendations with business justification]

## Conclusion
[Overall compliance assessment and release readiness opinion]

## Signatures
Lead Auditor: Ingrid Solberg — Date: [YYYY-MM-DD]
Technical Assessor: Sana Khoury — Date: [YYYY-MM-DD]
CSO Review: Dr. Sarah Chen — Date: [YYYY-MM-DD]
````

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Stage 1** (SRD)                    | Identifies MASVS compliance requirements for banking applications; maps regulatory obligations to MASVS controls                                 |
| **Stage 6** (Code Review)            | Conducts MASVS compliance assessment as part of code review; produces gap analysis with remediation guidance; findings included in Defect Report |
| **Stage 8** (Integrity Verification) | Re-assesses MASVS compliance after remediation; verifies all gaps are closed; produces updated compliance matrix                                 |
| **Stage 10** (Release Readiness)     | Provides MASVS compliance audit report for CSO release checklist item #4; confirms regulatory compliance for mobile banking applications         |

## Quality Standards

| Metric                   | Standard                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Audit Coverage**       | 100% of MASVS L1 + L2 requirements assessed for banking applications                                                                             |
| **Audit Accuracy**       | Zero false negatives on Critical/High gaps (validated by peer review); zero regulatory findings post-audit                                       |
| **Report Quality**       | Audit reports meet banking regulator standards; include all required elements (scope, methodology, findings, remediation, conclusion)            |
| **Remediation Tracking** | 100% of Critical gaps remediated within 14 days; 100% of High gaps within 30 days                                                                |
| **Regulatory Mapping**   | Every MASVS gap mapped to applicable regulatory requirement (FFIEC, PSD2, local)                                                                 |
| **Audit Efficiency**     | Audit completed within planned timeline; zero scope extensions; management presentation delivered within 5 business days of fieldwork completion |
