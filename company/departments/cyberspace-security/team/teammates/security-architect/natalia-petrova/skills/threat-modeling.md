# Threat Modeling

## Overview

Systematic identification, analysis, and documentation of security threats across the application architecture. This skill encompasses STRIDE methodology, PASTA framework, attack tree construction, zero-trust architecture review, security code review patterns, and threat model documentation. It enables a security architect to proactively design defenses into the system rather than reactively patching vulnerabilities after deployment.

## Competency Dimensions

| Dimension               | Proficiency Level | Key Capabilities                                                                               |
| ----------------------- | ----------------- | ---------------------------------------------------------------------------------------------- |
| STRIDE Methodology      | Expert            | Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege analysis |
| PASTA Framework         | Expert            | 7-stage risk-centric threat modeling aligned with business objectives                          |
| Attack Trees            | Advanced          | Multi-path attack scenario modeling, probability-weighted threat analysis                      |
| Zero-Trust Architecture | Advanced          | Identity-centric security, microsegmentation, continuous verification                          |
| Security Code Review    | Advanced          | Identifying vulnerability patterns in code, secure coding standards enforcement                |
| Threat Documentation    | Expert            | DFD-based threat models, risk registers, mitigation tracking                                   |

## Execution Guidance

### STRIDE Methodology

Apply STRIDE systematically to each component in the system's Data Flow Diagram (DFD):

**1. Spoofing Identity:**

- Can an attacker impersonate a user, service, or system component?
- Review: Authentication mechanisms (OAuth 2.0, biometric, certificate-based)
- Mitigations: Mutual TLS, device attestation (Android Play Integrity, iOS DeviceCheck), MFA
- Platform-specific: Android Keystore for credential storage, iOS Keychain for token management

**2. Tampering with Data:**

- Can an attacker modify data in transit or at rest?
- Review: Integrity checks (HMAC, digital signatures), TLS enforcement, database access controls
- Mitigations: Certificate pinning, encrypted payloads, write-ahead logging, audit trails
- Platform-specific: Android SafetyNet/Play Integrity, iOS App Attest

**3. Repudiation:**

- Can a user or service deny performing an action?
- Review: Logging completeness, audit trail integrity, non-repudiation controls
- Mitigations: Immutable audit logs, digital signatures on transactions, centralized logging
- Platform-specific: Server-side event logging, client-side secure logging with tamper detection

**4. Information Disclosure:**

- Can an attacker access sensitive data they shouldn't?
- Review: Data classification, encryption (at rest/in transit), access controls, data minimization
- Mitigations: Field-level encryption, tokenization, least-privilege access, data masking in logs
- Platform-specific: Android Scoped Storage, iOS Data Protection classes, secure enclaves

**5. Denial of Service:**

- Can an attacker disrupt service availability?
- Review: Rate limiting, resource quotas, circuit breakers, graceful degradation
- Mitigations: API rate limiting, CDN DDoS protection, horizontal scaling, circuit breaker patterns
- Platform-specific: Android WorkManager backoff policies, iOS background task limits

**6. Elevation of Privilege:**

- Can an attacker gain higher privileges than intended?
- Review: Authorization checks, role-based access control, privilege separation
- Mitigations: RBAC/ABAC, principle of least privilege, privilege escalation monitoring
- Platform-specific: Android SELinux policies, iOS entitlements and sandboxing

### PASTA Framework (Process for Attack Simulation and Threat Analysis)

Execute all 7 stages:

| Stage                        | Activity                                                               | Output                              |
| ---------------------------- | ---------------------------------------------------------------------- | ----------------------------------- |
| 1. Define Objectives         | Identify business objectives, compliance requirements, risk tolerance  | Business risk profile               |
| 2. Define Scope              | Inventory assets, data flows, trust boundaries, external dependencies  | Technical architecture map          |
| 3. Application Decomposition | Create DFDs, identify entry points, enumerate data stores              | DFD with trust boundaries           |
| 4. Threat Analysis           | Apply STRIDE to each DFD element; enumerate threats                    | Threat catalog                      |
| 5. Vulnerability Analysis    | Map threats to known vulnerabilities (CWE, CVE); assess exploitability | Vulnerability-threat matrix         |
| 6. Attack Simulation         | Build attack trees; simulate attacker paths with probability scoring   | Attack scenarios with likelihood    |
| 7. Risk & Impact Analysis    | Calculate risk = likelihood × impact; prioritize mitigations           | Risk register with remediation plan |

### Attack Tree Construction

**Structure:**

- Root node: Attacker's ultimate goal (e.g., "Access user financial data")
- Intermediate nodes: Sub-goals that must be achieved (e.g., "Bypass authentication", "Intercept API traffic")
- Leaf nodes: Specific attack vectors (e.g., "Phishing credential", "MITM with forged certificate")

**AND/OR Gates:**

- AND: All child nodes must be achieved for parent to succeed (harder to achieve)
- OR: Any child node achieves the parent (easier to achieve)

**Scoring:**

- Assign difficulty score (1–10) to each leaf node based on required skill, resources, and detection risk
- Propagate scores up the tree: AND nodes = sum of children, OR nodes = minimum of children
- Identify the minimum-cost attack path; prioritize defenses along that path

### Zero-Trust Architecture Review

Evaluate against zero-trust pillars:

1. **Identity:** Every request authenticated, regardless of origin. No implicit trust based on network location.
2. **Device:** Every device verified and continuously assessed for compliance (OS version, security patch level, jailbreak/root detection).
3. **Network:** Microsegmentation; least-privilege network access; encrypted all traffic (TLS 1.3 minimum).
4. **Application:** Per-request authorization checks; session tokens bound to device fingerprint; short-lived tokens with refresh rotation.
5. **Data:** Classified and encrypted at rest and in transit; access logged and audited; DLP controls on data egress.
6. **Visibility & Analytics:** Continuous monitoring; anomaly detection; automated response to policy violations.

### Security Code Review Patterns

Common vulnerability patterns to identify during code review:

| Pattern                   | Language    | Vulnerability               | Detection Approach                                                |
| ------------------------- | ----------- | --------------------------- | ----------------------------------------------------------------- |
| Hardcoded secrets         | All         | Credential exposure         | Regex scan for `apiKey`, `secret`, `password` literals            |
| Insecure random           | Kotlin/Java | Predictable tokens          | Check for `java.util.Random` vs `SecureRandom`                    |
| Unsafe deserialization    | Java/Kotlin | RCE via crafted input       | Check for `ObjectInputStream.readObject()`                        |
| WebView JavaScript bridge | Kotlin/Java | XSS in WebView              | Check for `addJavascriptInterface` without `@JavascriptInterface` |
| Insecure URL loading      | Swift       | Arbitrary URL loading       | Check for `UIApplication.open` without allowlist                  |
| Keychain accessibility    | Swift       | Data accessible when locked | Check for `kSecAttrAccessible` not set to `AfterFirstUnlock`      |
| HTTP in production        | All         | Plaintext traffic           | Check for `http://` URLs, `cleartextTrafficPermitted`             |
| Overly broad file access  | Kotlin      | Data exposure               | Check for `MODE_WORLD_READABLE`, external storage writes          |

### Threat Model Documentation

Standard threat model document structure:

1. **System Overview:** Architecture summary, technology stack, deployment topology
2. **Data Flow Diagrams:** DFD Level 0 (system context), Level 1 (component level), Level 2 (detailed process)
3. **Trust Boundaries:** Explicitly mark where data crosses trust zones
4. **Threat Catalog:** Table of threats mapped to STRIDE categories with DFD element references
5. **Attack Trees:** Visual attack trees for highest-risk scenarios
6. **Risk Assessment:** Likelihood × impact scoring with CVSS references where applicable
7. **Mitigation Plan:** Each threat with proposed controls, responsible owner, target date, residual risk
8. **Assumptions & Constraints:** Security assumptions that, if invalidated, require threat model revision
9. **Revision History:** Versioned updates with change descriptions

## Pipeline Integration

| Pipeline Stage                | Threat Modeling Activity                                                                       |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| Stage 1 (Requirements)        | Identify security requirements in SRD; define threat surface boundaries                        |
| Stage 3 (Architecture)        | Execute full PASTA threat model on UML architecture; produce threat catalog and risk register  |
| Stage 4 (Implementation Plan) | Map threat mitigations to implementation tasks; ensure security work is in Gantt chart         |
| Stage 5 (Development)         | Security code reviews on PRs; validate mitigations are implemented per threat model            |
| Stage 6 (Code Review)         | Verify all P0/P1 threats from threat model have mitigations implemented and tested             |
| Stage 8 (Integrity)           | Validate that deployed system matches threat model assumptions; update if architecture changed |
| Stage 10 (Release)            | Final threat model sign-off; document any accepted residual risks                              |

## Quality Standards

- **Threat model coverage:** 100% of system components with external interfaces must have STRIDE analysis
- **Review cadence:** Threat models must be reviewed and updated at every architecture change
- **Attack tree depth:** Minimum 3 levels of depth for all attack trees
- **Mitigation tracking:** Every identified threat must have a mitigation, accepted risk rationale, or deferral with timeline
- **Code review coverage:** 100% of PRs touching security-sensitive code paths (auth, crypto, data access) must receive security code review
- **Zero-trust compliance:** All production services must pass zero-trust pillar assessment before Stage 10 release

## Reference Materials

- Microsoft STRIDE: https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- PASTA Framework: OWASP Threat Modeling Project
- MITRE ATT&CK: https://attack.mitre.org/
- CWE Top 25: https://cwe.mitre.org/top25/
- OWASP Mobile Top 10: https://owasp.org/www-project-mobile-top-10/
- NIST Zero Trust Architecture: SP 800-207
- Android Security Best Practices: https://developer.android.com/security/best-practices
- iOS Security Best Practices: https://developer.apple.com/security/
