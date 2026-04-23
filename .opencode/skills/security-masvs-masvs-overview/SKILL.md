---
name: security-masvs-masvs-overview
description: 'Security skill: Masvs Overview'
---

# OWASP MASVS Overview

## What is MASVS and Why We Adopt It

### Definition

The **OWASP Mobile Application Security Verification Standard (MASVS)** is the industry-standard security framework for mobile application security. Published by the Open Web Application Security Project (OWASP), MASVS provides a comprehensive set of security requirements that developers, architects, and security testers can use to design, develop, and verify mobile applications against common threats and vulnerabilities.

MASVS is not a guideline or a suggestion — it is a **verification standard**. Each control has specific, testable criteria that determine whether an application meets the requirement. This makes it uniquely suited for use as a formal security baseline in engineering pipelines.

### Industry Recognition

MASVAS is recognized globally as the authoritative mobile security standard:

| Attribute           | Detail                                                                               |
| ------------------- | ------------------------------------------------------------------------------------ |
| **Publisher**       | OWASP Foundation (open-source, community-driven)                                     |
| **Current Version** | MASVS v2.x (ongoing evolution)                                                       |
| **Scope**           | iOS, Android, cross-platform (Flutter, React Native, KMP)                            |
| **Recognition**     | Referenced by NIST, ENISA, and major regulatory bodies                               |
| **Alignment**       | Maps to OWASP Top 10, OWASP MASWE (Mobile Application Security Weakness Enumeration) |

MASVS is developed by a global community of security researchers, mobile platform engineers, and industry practitioners. It is the mobile counterpart to OWASP ASVS (Application Security Verification Standard) for web applications.

### Why Our Company Adopts MASVS

Our company adopts MASVS as the mandatory security baseline for all mobile products. This decision is driven by four factors:

| Driver                                | Rationale                                                                                                                                                                                        |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Regulatory Compliance**             | MASVS controls map directly to requirements under SOC 2 Type II, PCI-DSS, GDPR, HIPAA, and emerging mobile-specific regulations. Using MASVS as a baseline simplifies audit evidence collection. |
| **Standardized Security Engineering** | MASVS provides a common security vocabulary across Android, iOS, and cross-platform teams. Instead of platform-specific security interpretations, MASVS gives a unified control framework.       |
| **User Trust**                        | MASVS compliance is a demonstrable security posture. It signals to users, enterprise buyers, and app reviewers that the application meets recognized industry standards.                         |
| **Audit Readiness**                   | MASVS verification criteria are testable and evidence-based. This means audit evidence can be collected systematically during development rather than assembled retroactively.                   |

### Relationship to Other Standards

MASVS does not replace other security standards — it complements them. The following table shows how MASVS relates to enterprise security frameworks:

| Standard                         | Relationship to MASVS                                                                                                                                                                                                           |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SOC 2 Type II**                | MASVS provides technical control evidence for Trust Service Criteria (security, availability, processing integrity). MASVS V2-V5 map to SOC 2 CC6 (Logical and Physical Access Controls).                                       |
| **PCI-DSS**                      | For mobile payment applications, MASVS V3 (Cryptography), V4 (Authentication), and V5 (Network Communication) provide the technical controls that satisfy PCI-DSS mobile requirements (e.g., PIN entry security, tokenization). |
| **ISO 27001**                    | MASVS maps to Annex A controls for mobile-specific technical implementation. ISO 27001 defines the ISMS; MASVS defines the mobile technical controls within that ISMS.                                                          |
| **OWASP ASVS**                   | ASVS covers web applications; MASVS covers mobile. They share structural parallels (V1-V8 in both) and can be used together for applications with web and mobile components.                                                    |
| **NIST Cybersecurity Framework** | MASVS maps to NIST CSF subcategories under Protect (PR) and Detect (DE) functions for mobile-specific technical controls.                                                                                                       |

---

## MASVS Structure: V1-V8 Categories, L1/L2 Levels, MASVS-R

### The Eight Verification Categories

MASVS is organized into eight verification categories (V1 through V8). Each category groups related security controls that address a specific security domain.

#### V1: Architecture, Design and Threat Modeling

**Purpose:** Ensure the application has a well-defined security architecture based on threat modeling and secure design principles.

| Control       | Description                                                                             |
| ------------- | --------------------------------------------------------------------------------------- |
| **MASVS-1.1** | A security architecture is defined that addresses security requirements.                |
| **MASVS-1.2** | Threat modeling is performed and documented.                                            |
| **MASVS-1.3** | The application enforces security requirements through design, not just implementation. |
| **MASVS-1.4** | Interoperability and data exchange mechanisms are secure.                               |

**Key artifacts:** Security architecture document, threat model (STRIDE or equivalent), data flow diagrams, ADRs with security rationale.

**Pipeline ownership:** Stage 1 (SRD defines targets), Stage 3 (UML and ADRs realize architecture).

#### V2: Data Storage and Privacy

**Purpose:** Ensure sensitive data is stored securely on the device and handled according to privacy requirements.

| Control       | Description                                                                                          |
| ------------- | ---------------------------------------------------------------------------------------------------- |
| **MASVS-2.1** | No sensitive data is stored locally without adequate protection.                                     |
| **MASVS-2.2** | Sensitive data stored on the device is protected using secure storage mechanisms.                    |
| **MASVS-2.3** | Sensitive data is not exposed in application backups.                                                |
| **MASVS-2.4** | Sensitive data is not exposed in application logs.                                                   |
| **MASVS-2.5** | The app removes sensitive data from memory when no longer needed.                                    |
| **MASVS-2.6** | Sensitive data handled by the app does not leak through keyboard caches, clipboard, or UI snapshots. |
| **MASVS-2.7** | Sensitive data in network communication is protected.                                                |
| **MASVS-2.8** | Privacy requirements (GDPR, CCPA, etc.) are enforced.                                                |

**Platform mechanisms:** iOS Keychain, Android Keystore/EncryptedSharedPreferences, SQLite encryption (SQLCipher), file-based encryption.

**Pipeline ownership:** Stage 5 (platform implementation), Stage 6 (code review verification).

#### V3: Cryptography

**Purpose:** Ensure cryptographic operations are performed correctly using industry-standard algorithms and implementations.

| Control       | Description                                                                                      |
| ------------- | ------------------------------------------------------------------------------------------------ |
| **MASVS-3.1** | Cryptographic algorithms and protocols are industry-standard and not deprecated.                 |
| **MASVS-3.2** | Cryptographic keys are managed securely (generation, storage, rotation, revocation).             |
| **MASVS-3.3** | Cryptographic operations are performed using platform-provided APIs, not custom implementations. |

**Key requirements:** AES-256-GCM for symmetric encryption, RSA-2048+ or ECC (P-256) for asymmetric, SHA-256+ for hashing, TLS 1.2+ for transport.

**Prohibited:** Custom cryptographic algorithms, deprecated ciphers (DES, 3DES, RC4, MD5, SHA-1), hardcoded keys.

**Pipeline ownership:** Stage 3 (TSD selects algorithms), Stage 5 (implementation), Stage 6 (code review), Stage 8 (integrity verification).

#### V4: Authentication and Session Management

**Purpose:** Ensure users are properly authenticated and sessions are managed securely.

| Control       | Description                                                                          |
| ------------- | ------------------------------------------------------------------------------------ |
| **MASVS-4.1** | Authentication mechanisms are industry-standard and resist common attacks.           |
| **MASVS-4.2** | Session tokens are generated, stored, and invalidated securely.                      |
| **MASVS-4.3** | Biometric authentication is implemented correctly (not as sole factor for L2).       |
| **MASVS-4.4** | OAuth 2.0 / OpenID Connect flows are implemented securely (PKCE for public clients). |
| **MASVS-4.5** | Credentials are not hardcoded in the application.                                    |

**Platform considerations:** BiometricPrompt (Android), LAContext (iOS), ASWebAuthenticationSession / CustomTabs for OAuth flows.

**Pipeline ownership:** Stage 1 (SRD defines auth requirements), Stage 5 (implementation), Stage 6 (code review).

#### V5: Network Communication

**Purpose:** Ensure all network communication is secure against interception and tampering.

| Control       | Description                                                                             |
| ------------- | --------------------------------------------------------------------------------------- |
| **MASVS-5.1** | All network communication uses TLS.                                                     |
| **MASVS-5.2** | TLS certificates are validated properly (no custom trust managers accepting all certs). |
| **MASVS-5.3** | Certificate pinning is implemented for high-security applications.                      |
| **MASVS-5.4** | The app uses cleartext traffic only when explicitly required and documented.            |
| **MASVS-5.5** | WebSocket connections are secured with TLS.                                             |

**Platform mechanisms:** iOS ATS (App Transport Security) enforcement, Android Network Security Configuration, certificate pinning via TrustKit or platform-native APIs.

**Pipeline ownership:** Stage 3 (TSD selects TLS configuration), Stage 5 (implementation), Stage 6 (code review), Stage 7 (testing).

#### V6: Platform Interaction

**Purpose:** Ensure the application uses platform security features correctly and does not expose data through platform mechanisms.

| Control       | Description                                                                                      |
| ------------- | ------------------------------------------------------------------------------------------------ |
| **MASVS-6.1** | Intents (Android) / URL schemes / Universal Links (iOS) are secured against unauthorized access. |
| **MASVS-6.2** | IPC mechanisms do not expose sensitive functionality or data.                                    |
| **MASVS-6.3** | Permissions are requested minimally and justified.                                               |
| **MASVS-6.4** | WebViews are configured securely (no mixed content, JavaScript bridging hardened).               |
| **MASVS-6.5** | Third-party keyboards are handled securely for sensitive input.                                  |

**Pipeline ownership:** Stage 5 (platform implementation), Stage 6 (code review).

#### V7: Code Quality and Build Settings

**Purpose:** Ensure the application is built with security-hardened compiler settings and follows secure coding practices.

| Control       | Description                                                                                      |
| ------------- | ------------------------------------------------------------------------------------------------ |
| **MASVS-7.1** | The application is compiled with security-hardened build settings (PIE, stack protection, etc.). |
| **MASVS-7.2** | Debug functionality is removed from release builds.                                              |
| **MASVS-7.3** | Third-party dependencies are free of known vulnerabilities.                                      |
| **MASVS-7.4** | The application handles runtime errors without exposing sensitive information.                   |

**Build settings:** Android (minifyEnabled, shrinkResources, ProGuard/R8 rules, no debuggable flag), iOS (Strip Debug Symbols, Dead Code Stripping, Position Independent Executable, NO debug configuration).

**Pipeline ownership:** Stage 5 (build configuration), Stage 6 (code review), Stage 8 (integrity verification).

#### V8: Resilience Against Reverse Engineering

**Purpose:** Ensure the application has defensive measures against reverse engineering and tampering.

| Control       | Description                                                                                  |
| ------------- | -------------------------------------------------------------------------------------------- |
| **MASVS-8.1** | The application implements anti-reversing techniques (obfuscation, control flow flattening). |
| **MASVS-8.2** | The application detects and responds to debugging/emulator environments.                     |
| **MASVS-8.3** | The application implements integrity checks to detect tampering.                             |
| **MASVS-8.4** | The application detects and responds to hooking/frameworks (Frida, Cydia Substrate).         |
| **MASVS-8.5** | The application implements root/jailbreak detection for L2 applications.                     |

**Techniques:** Code obfuscation (ProGuard/R8, iOS LLVM obfuscation), runtime integrity checks, anti-debugging checks, root/jailbreak detection, emulator detection.

**Pipeline ownership:** Stage 5 (implementation), Stage 6 (code review), Stage 7 (testing with penetration testing), Stage 8 (integrity verification).

---

### L1 (Standard Security) vs L2 (Defense-in-Depth)

MASVS defines two assurance levels:

| Dimension        | MASVS L1 (Standard)                                | MASVS L2 (Defense-in-Depth)                                                 |
| ---------------- | -------------------------------------------------- | --------------------------------------------------------------------------- |
| **Purpose**      | Baseline security for general-purpose applications | Enhanced security for applications handling sensitive data                  |
| **Scope**        | All V1-V7 controls                                 | All V1-V7 controls + V8 (Resilience)                                        |
| **Verification** | Self-assessment or automated testing               | Self-assessment + manual penetration testing + reverse engineering analysis |
| **Depth**        | "The app does what it should"                      | "The app resists active attack attempts"                                    |
| **Assessor**     | Internal team, automated tools                     | Internal team + external accredited assessor (recommended)                  |

**L1 is sufficient for:** General-purpose consumer apps, content apps, utility apps without sensitive data.

**L2 is mandatory for:** Financial applications (banking, payments), healthcare applications, government services, enterprise SSO, applications handling PII at scale, applications in regulated industries.

Our company's default posture is **L1 for consumer products and L2 for any product handling financial, health, or government data**. The CSO makes the final determination per project during Stage 1 SRD creation.

---

### MASVS-R (Resilience) Addendum

MASVS-R is a supplementary set of resilience requirements that can be applied in addition to L1 or L2. It focuses on the application's ability to detect and respond to active attack attempts.

| MASVS-R Control | Description                                                               |
| --------------- | ------------------------------------------------------------------------- |
| **MASVS-R.1**   | Runtime application self-protection (RASP) mechanisms are implemented.    |
| **MASVS-R.2**   | The application detects and responds to dynamic analysis tools.           |
| **MASVS-R.3**   | The application detects and responds to repackaging/tampering.            |
| **MASVS-R.4**   | The application implements anti-emulator checks for targeted deployments. |

MASVS-R is **optional for L1** and **recommended for L2** applications. The CSO determines MASVS-R applicability during Stage 1 SRD creation.

---

## Pipeline Integration: Mapping to Stages 1, 6, 8, 10

MASVS is enforced by the CSO (Dr. Sarah Chen) through the Cyberspace Security department across four pipeline stages:

### Stage 1: Requirements — Defining MASVS Compliance Targets

**Producer:** CSO (with CPO for PRD alignment)
**Artifact:** SRD (Security Requirements Document)
**Location:** `company/project/<project>/requirements/srd/`

At Stage 1, the SRD defines:

| SRD Section               | MASVS Mapping                                          |
| ------------------------- | ------------------------------------------------------ |
| Security baseline         | MASVS L1 or L2 determination                           |
| MASVS control selection   | Per-category (V1-V8) applicability matrix              |
| MASVS-R applicability     | MASVS-R control selection                              |
| Platform security targets | iOS ATS, Android Keystore, Play Integrity / App Attest |
| Compliance evidence plan  | How each MASVS control will be verified downstream     |

**Gate criterion:** "User has confirmed target platform(s)" — this includes confirming the MASVS level (L1 or L2).

### Stage 6: Code Review — Defect Classification Using MASVS Criteria

**Producer:** CTO (panel) with CSO review
**Artifact:** DEFECT-REPORT.md
**Location:** `company/project/<project>/reviews/code-review/`

At Stage 6, the code review panel classifies defects against MASVS controls:

| MASVS Category                            | Defect Classification     |
| ----------------------------------------- | ------------------------- |
| Any MASVS L1 control failure              | P0 or P1 (blocks release) |
| Any MASVS L2 control failure              | P0 or P1 (blocks release) |
| Any MASVS-R control failure (if selected) | P1 (blocks release)       |
| MASVS control partially implemented       | P2 (user decides)         |
| MASVS control exceeds requirements        | P3 (polish)               |

**Gate criterion:** "User has reviewed Defect Report and made decisions on P2/P3 defects."

### Stage 8: Integrity Verification — MASVS Compliance Confirmation

**Producer:** CTO (panel) with CSO, CPO, CTO-L
**Artifact:** Integrity Verification Sign-off (includes MASVS compliance matrix)
**Location:** `company/project/<project>/reviews/integrity-verification/`

At Stage 8, the panel verifies:

| Verification                                                 | Responsible          |
| ------------------------------------------------------------ | -------------------- |
| All MASVS V1-V7 controls are implemented per SRD             | CSO                  |
| All MASVS V8 controls (if L2) are implemented                | CSO + Platform Leads |
| All MASVS-R controls (if selected) are implemented           | CSO                  |
| Regression testing on all fixed MASVS-related defects passed | Test Lead            |
| No "trim-to-pass" anti-pattern (functionality removal)       | CTO Panel            |

**Gate criterion:** Panel sign-off only — no user approval required at this stage.

### Stage 10: Release Readiness — MASVS Gate Checklist Item #4

**Producer:** CTO (panel) + USER
**Artifact:** RELEASE-CHECKLIST-7-ITEM.md
**Location:** `company/project/<project>/reviews/release/`

Stage 10 includes 7 sign-off items. Item #4 is the MASVS compliance gate:

| #   | Domain                                         | Sign-off Authority | MASVS Reference             |
| --- | ---------------------------------------------- | ------------------ | --------------------------- |
| 4   | Security — SRD enforced, OWASP MASVS compliant | CSO                | All V1-V8 controls verified |

**Gate criterion:** "User has issued the final release decision." All 7 items must be signed off.

---

## Level Definitions: L1 vs L2

### When L1 is Sufficient

| Application Type                 | Rationale                                                            |
| -------------------------------- | -------------------------------------------------------------------- |
| Content/consumer apps            | No sensitive user data, no financial transactions                    |
| Utility apps (calculator, notes) | Minimal attack surface, no network communication with sensitive data |
| Entertainment/gaming apps        | Low regulatory exposure, no PII handling                             |
| Internal tools (non-sensitive)   | Limited data sensitivity, controlled user population                 |

**L1 control set:** All V1 through V7 controls. V8 is not required.

### When L2 is Mandatory

| Application Type       | Rationale                                        | Mandatory Controls              |
| ---------------------- | ------------------------------------------------ | ------------------------------- |
| Banking/financial apps | Regulatory compliance, financial data protection | All V1-V8 + MASVS-R recommended |
| Healthcare apps        | HIPAA, sensitive health data                     | All V1-V8                       |
| Government services    | Official data handling, public trust             | All V1-V8                       |
| Enterprise SSO         | Corporate credential handling                    | All V1-V8 + MASVS-R recommended |
| Payment processing     | PCI-DSS compliance                               | All V1-V8 + MASVS-R recommended |
| PII at scale           | GDPR, CCPA compliance                            | All V1-V8                       |

**L2 control set:** All V1 through V8 controls. MASVS-R is recommended but determined by CSO during Stage 1.

### L2-Selected Controls for Sensitive Applications

For applications that exceed standard L2 requirements, the CSO may select additional controls:

| Additional Control                | Applicability                                     |
| --------------------------------- | ------------------------------------------------- |
| MASVS-R.1 (RASP)                  | High-value target applications                    |
| MASVS-R.2 (Anti-dynamic-analysis) | Applications with proprietary algorithms          |
| MASVS-R.3 (Anti-repackaging)      | Applications targeting regions with high piracy   |
| MASVS-R.4 (Anti-emulator)         | Applications with location-based fraud prevention |

---

## Assessment Workflow: Verification at Each Gate

### Self-Assessment Methodology

MASVS self-assessment is performed by the CSO (or delegated Security Engineer) at each relevant pipeline stage:

| Step | Activity                                      | Responsible     | Stage    |
| ---- | --------------------------------------------- | --------------- | -------- |
| 1    | Identify applicable MASVS controls from SRD   | CSO             | Stage 1  |
| 2    | Create verification checklist per control     | CSO             | Stage 1  |
| 3    | Implement controls per platform conventions   | Platform Leads  | Stage 5  |
| 4    | Verify controls via code review               | CTO Panel + CSO | Stage 6  |
| 5    | Verify controls via automated testing         | Test Lead       | Stage 7  |
| 6    | Confirm compliance via integrity verification | CSO             | Stage 8  |
| 7    | Final sign-off at release readiness           | CSO             | Stage 10 |

### Evidence Collection Requirements

For each MASVS control, the following evidence must be collected:

| Evidence Type               | Description                                                                    | Collection Point |
| --------------------------- | ------------------------------------------------------------------------------ | ---------------- |
| **Design evidence**         | ADRs, UML diagrams, threat models showing control is addressed in architecture | Stage 3          |
| **Implementation evidence** | Source code references, configuration files, platform API usage                | Stage 5          |
| **Test evidence**           | Unit tests, integration tests, penetration test results                        | Stage 7          |
| **Review evidence**         | Code review sign-off, panel verification notes                                 | Stage 6, 8       |
| **Runtime evidence**        | Play Integrity / App Attest results, crash reports, security monitoring        | Stage 10         |

Evidence is stored in `company/project/<project>/security/` with subdirectories:

- `audits/` — Security audit reports
- `compliance/` — MASVS control-by-control evidence
- `penetration-tests/` — Penetration test results

### Panel Review Process

At each MASVS-related gate review (Stages 6, 8, 10), the panel follows this process:

1. **CSO presents MASVS compliance matrix** — showing each control as Pass/Fail/Partial
2. **Panel reviews failures** — any Fail is classified as P0/P1 defect
3. **Panel reviews partials** — classified as P2 defects (user decides)
4. **Panel signs off** — if all mandatory controls Pass, gate is approved
5. **User reviews P2/P3** — at Stages 6 and 7, user makes final decision on deferrable items

### External Certification Path

For applications requiring formal MASVS certification (beyond self-assessment):

| Step | Action                                         | Notes                                                    |
| ---- | ---------------------------------------------- | -------------------------------------------------------- |
| 1    | Engage accredited MASVS assessor               | OWASP maintains list of accredited assessors             |
| 2    | Provide SRD + compliance evidence              | From `security/compliance/` directory                    |
| 3    | Assessor performs independent verification     | Includes manual testing and reverse engineering analysis |
| 4    | Assessor issues certification report           | Report is stored in `security/audits/`                   |
| 5    | Report is included in Stage 10 release package | Part of release readiness evidence                       |

External certification is **recommended for L2 applications** in regulated industries and **mandatory for government contracts** that require it.

---

## Release Gate Model: How MASVS Compliance Gates Release Decisions

### P0 Defects for MASVS Non-Compliance

The following conditions are classified as **P0 defects** (non-negotiable release blockers):

| Condition                                                    | MASVS Reference | Rationale                            |
| ------------------------------------------------------------ | --------------- | ------------------------------------ |
| Any mandatory L1 control fails verification                  | V1-V7           | Baseline security is not met         |
| Any mandatory L2 control fails verification                  | V1-V8           | Defense-in-depth is not met          |
| Cleartext transmission of sensitive data                     | V5.1, V5.4      | Data interception risk               |
| Hardcoded credentials or cryptographic keys                  | V4.5, V3.2      | Immediate compromise vector          |
| Custom TLS certificate validation accepting all certificates | V5.2            | Man-in-the-middle vulnerability      |
| Sensitive data in application logs (release build)           | V2.4            | Data exfiltration via logcat/Console |
| No biometric fallback security                               | V4.3            | Authentication bypass                |
| Missing root/jailbreak detection for L2 app                  | V8.5            | Defense-in-depth failure             |

### Release Blocking Criteria

A release is **blocked** if any of the following are true:

| Criterion                                                                             | Description                    |
| ------------------------------------------------------------------------------------- | ------------------------------ |
| Any P0 MASVS defect exists                                                            | Non-negotiable — must be fixed |
| Any P1 MASVS defect exists                                                            | Non-negotiable — must be fixed |
| MASVS compliance matrix has any "Fail" on mandatory controls                          | Equivalent to P0               |
| MASVS compliance matrix has unresolved "Partial" on mandatory controls (user decides) | P2 — user may defer            |
| External assessor (if engaged) issues non-compliant determination                     | P0 — must be remediated        |

### Exception Process

MASVS exceptions follow this process:

| Step | Action                                                                          | Authority              |
| ---- | ------------------------------------------------------------------------------- | ---------------------- |
| 1    | CSO identifies a control that cannot be implemented due to technical constraint | CSO                    |
| 2    | CSO documents exception request with risk assessment and compensating controls  | CSO                    |
| 3    | CTO + CPO review exception request                                              | CTO + CPO              |
| 4    | User approves or rejects exception                                              | User (final authority) |
| 5    | If approved, exception is documented in SRD addendum                            | CSO                    |
| 6    | Exception is re-reviewed at each release cycle                                  | CSO                    |

**Important:** Exceptions are **rare and temporary**. An exception for one release does not grant a permanent waiver. The CSO must re-evaluate at each release cycle.

---

## Business Impact: Regulatory, Audit, and User Trust Implications

### SOC 2 Type II Evidence

MASVS compliance provides direct evidence for SOC 2 Type II audits:

| SOC 2 Trust Service Criterion             | MASVS Mapping                      | Evidence Provided                        |
| ----------------------------------------- | ---------------------------------- | ---------------------------------------- |
| CC6.1 — Logical access security           | V4 (Authentication)                | Auth implementation, session management  |
| CC6.2 — System access authentication      | V4.1, V4.2, V4.4                   | OAuth/PKCE flows, token management       |
| CC6.3 — System access authorization       | V6 (Platform Interaction)          | IPC security, permission model           |
| CC6.6 — Security measures against threats | V1 (Architecture), V8 (Resilience) | Threat model, anti-reversing             |
| CC7.1 — Detection of changes              | V7 (Code Quality)                  | Build settings, dependency scanning      |
| CC7.2 — Monitoring for anomalies          | V8 (Resilience)                    | Root/jailbreak detection, anti-tampering |
| CC8.1 — Change management                 | V7.3 (Dependency management)       | Third-party vulnerability management     |

### PCI-DSS Mobile Payment Compliance

For applications processing payment card data:

| PCI-DSS Requirement                              | MASVS Mapping                                  |
| ------------------------------------------------ | ---------------------------------------------- |
| Requirement 2 — Do not use vendor defaults       | V4.5 (No hardcoded credentials)                |
| Requirement 3 — Protect stored data              | V2 (Data Storage), V3 (Cryptography)           |
| Requirement 4 — Encrypt transmission             | V5 (Network Communication)                     |
| Requirement 6 — Secure systems and software      | V7 (Code Quality)                              |
| Requirement 8 — Identify and authenticate access | V4 (Authentication)                            |
| Requirement 22 — Mobile payment acceptance       | V2, V3, V4, V5 (comprehensive mobile controls) |

### User Trust and App Store Requirements

| Platform                   | MASVS Relevance                                                                                                                                       |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **App Store (Apple)**      | MASVS V5 (TLS), V2 (Keychain), V6 (ATS enforcement) align with Apple's App Review Guidelines section 5 (Privacy)                                      |
| **Google Play**            | MASVS V2 (EncryptedSharedPreferences), V5 (Network Security Configuration), V8 (Play Integrity) align with Google Play Data Safety requirements       |
| **Enterprise procurement** | Enterprise buyers increasingly request MASVS compliance as part of security due diligence. Having a MASVS compliance report accelerates sales cycles. |

### Competitive Differentiation

| Factor                         | With MASVS                                         | Without MASVS                      |
| ------------------------------ | -------------------------------------------------- | ---------------------------------- |
| Security posture communication | Demonstrable, industry-recognized standard         | Self-declared, unverifiable claims |
| Audit preparation              | Systematic evidence collection throughout pipeline | Retroactive evidence assembly      |
| Incident response              | Controls map directly to incident investigation    | Ad hoc investigation process       |
| Enterprise sales               | Accelerated due to verifiable security posture     | Extended security review cycles    |
| Regulatory inquiries           | Direct compliance mapping                          | Interpretive mapping required      |

---

## References

### Related Skills

| Skill                             | Description                                                                                                                                                                        |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `owasp-masvs-compliance.md`       | Detailed compliance methodology — how to perform MASVS verification per control, evidence collection, and compliance matrix generation.                                            |
| `masvs-mastery-track-a.md`        | Security team mastery track — deep dive into MASVS controls for CSO and Security Engineers, including verification techniques and common failure patterns.                         |
| `masvs-mastery-track-b.md`        | Engineering team mastery track — MASVS implementation guidance for platform leads and developers, covering secure coding patterns per control.                                     |
| `mobile-security-architecture.md` | Mobile security architecture patterns — how MASVS controls are realized in Android and iOS architecture, including secure storage, TLS configuration, and authentication patterns. |

### External Resources

| Resource                   | URL                                    | Description                                                                                             |
| -------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| OWASP MASVS Official       | `https://mas.owasp.org/MASVS/`         | The authoritative MASVS documentation, including full control descriptions and verification procedures. |
| OWASP MASWE                | `https://mas.owasp.org/MASWE/`         | Mobile Application Security Weakness Enumeration — the weakness database that MASVS controls address.   |
| OWASP MSTG                 | `https://mas.owasp.org/MSTG/`          | Mobile Security Testing Guide — companion guide for testing MASVS controls.                             |
| OWASP MASVS v2.0 Changelog | `https://mas.owasp.org/MASVS/changes/` | Version history and changes from MASVS v1 to v2.                                                        |

---

_This skill is part of the company's Security skill set. It is maintained by the Cyberspace Security department under the direction of the CSO (Dr. Sarah Chen). For questions or updates, route through the CSO._
