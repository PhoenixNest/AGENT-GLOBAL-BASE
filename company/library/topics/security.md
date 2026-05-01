# Security

Cross-cutting reference for all mobile security concerns: security requirements, platform security standards, OWASP MASVS compliance, and security review processes. The CSO owns security requirements and compliance; the CIO oversees architectural security decisions. Both participate across multiple pipeline stages.

---

## Owners

| Role                            | Name            | Department          | Profile                                                                                                       |
| ------------------------------- | --------------- | ------------------- | ------------------------------------------------------------------------------------------------------------- |
| Chief Security Officer (CSO)    | Dr. Sarah Chen  | Cyberspace Security | [`profile.md`](company/departments/cyberspace-security/supervisor/chief-security-officer/agent/profile.md)    |
| Chief Information Officer (CIO) | Dr. Priya Mehta | Cyberspace Security | [`profile.md`](company/departments/cyberspace-security/supervisor/chief-information-officer/agent/profile.md) |

---

## Security Across the Pipeline

### Stage 1 — Security Requirements Document (SRD)

The CSO produces the SRD concurrently with the CPO's PRD. The SRD covers:

- **Privacy obligations** — GDPR, CCPA, and other applicable regulations
- **Data handling constraints** — what data may be collected, stored, transmitted
- **Authentication requirements** — login mechanisms, session management, token handling
- **Encryption mandates** — data in transit and at rest
- **Platform-specific security requirements:**
  - iOS: App Transport Security (ATS), Keychain usage
  - Android: SafetyNet/Play Integrity, Keystore usage

> The SRD is paired with the PRD immediately after Stage 1 and travels as a unit through all subsequent stages.

### Stage 3 — Architecture Decision Records (ADRs) + Technology Selection Document (TSD)

The CIO produces ADRs and TSD, incorporating security constraints from the SRD into technology and architecture choices.

### Stage 6 — Code Review (Security Criterion)

The CSO owns the security review criterion during Stage 6 code review. The codebase is verified against:

1. All encryption requirements in the SRD implemented
2. Secure storage implemented correctly:
   - iOS: iOS Keychain
   - Android: Android Keystore
3. Platform security standards applied (iOS ATS, Android SafetyNet/Play Integrity)
4. **OWASP MASVS compliance** verified

### Stage 7 — Automated Testing

While the Test Lead owns Stage 7 execution, security-relevant defects discovered during automated testing must follow the notification protocol below.

**Notification Protocol:**

| Defect Type                      | Severity | Action                                                                                        |
| -------------------------------- | -------- | --------------------------------------------------------------------------------------------- |
| Security breach or vulnerability | P0       | Immediate CSO notification (within 24 hours); CSO classifies and assigns remediation priority |
| Security-adjacent defect         | P1       | CSO notified at next daily security sync; CSO confirms classification                         |
| Non-security defect              | P2/P3    | Standard defect handling — no CSO involvement required                                        |

**Security Testing Integration:** SAST/DAST pipeline results (owned by Omar Farouq) and dependency vulnerability scans are reviewed as part of Stage 7 test results. These results feed into the Stage 8 Integrity Verification security assessment.

### Stage 8 — Integrity Verification

Both CSO and CIO verify that the testing remediation phase did not silently remove or weaken any security requirements.

### Stage 10 — Release Readiness Check

**CSO sign-off criterion:** All SRD requirements enforced; OWASP MASVS compliant.

---

## OWASP Mobile Application Security

The company's security compliance baseline is the **OWASP Mobile Application Security** standard.

| Resource                                                  | Purpose                                             |
| --------------------------------------------------------- | --------------------------------------------------- |
| [OWASP MAS — mas.owasp.org](https://mas.owasp.org/)       | Official hub for both MASVS and MASTG               |
| MASVS (Mobile Application Security Verification Standard) | Defines the security requirements the app must meet |
| MASTG (Mobile Application Security Testing Guide)         | Comprehensive manual for testing those requirements |

> OWASP MAS is a living document updated continuously. Always refer to the official site for the latest version.

---

## Platform Security Standards

### iOS

- **App Transport Security (ATS)** — All network connections must use HTTPS with TLS 1.2+
- **iOS Keychain** — Mandatory for all sensitive credential and token storage
- **App Store Review Guidelines** — Security-related submission requirements

### Android

- **Android Keystore System** — Mandatory for cryptographic key storage
- **SafetyNet / Play Integrity API** — Device integrity verification
- **Google Play Developer Policies** — Security-related submission requirements

---

## Relevant Skills

| Skill File                                                                                                                                                | Owner | Purpose                                                                                                 |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------- |
| [`mobile-security-architecture.md`](company/departments/cyberspace-security/supervisor/chief-security-officer/skills/mobile-security-architecture.md)     | CSO   | Mobile security architecture design                                                                     |
| [`application-security-hardening.md`](company/departments/cyberspace-security/supervisor/chief-security-officer/skills/application-security-hardening.md) | CSO   | Encryption, secure storage, OWASP MASVS compliance                                                      |
| [`security-risk-assessment.md`](company/departments/cyberspace-security/supervisor/chief-security-officer/skills/security-risk-assessment.md)             | CSO   | SRD authorship, privacy and compliance requirements                                                     |
| [`emerging-threat-evaluation.md`](company/departments/cyberspace-security/supervisor/chief-security-officer/skills/emerging-threat-evaluation.md)         | CSO   | Threat landscape analysis                                                                               |
| [`security-requirements-and-srd.md`](company/departments/cyberspace-security/supervisor/chief-security-officer/skills/security-requirements-and-srd.md)   | CSO   | Stage 1 SRD authorship: threat modelling, SR-NNN requirements, compliance obligations, Stage 1 sign-off |
| [`technology-evaluation.md`](company/departments/cyberspace-security/supervisor/chief-information-officer/skills/technology-evaluation.md)                | CIO   | Security-aware technology evaluation                                                                    |

---

## Reference Links

See [`reference/development/links.md`](company/library/reference/development/links.md) — Security section — for OWASP MAS documentation and platform security developer guides.
