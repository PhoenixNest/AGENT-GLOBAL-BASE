---
name: security-architecture-security-operations
description: Security operations for mobile applications — incident response runbooks, security monitoring dashboards, vulnerability management workflows, security patch coordination, and 24/7 SOC integration for mobile product security. Owned by James Wright (Security Lead). Use during Stage 5 (Development) for security operations setup and Stage 10 (Release Readiness) for operational readiness validation. Trigger: security operations, incident response, security monitoring, vulnerability management, security patching, SOC integration, mobile security ops.
prerequisites:
  - security-overview

version: "1.0.0"
---

# Security Operations

## Overview

Comprehensive SIEM operations, SAST/DAST/SCA pipeline management, PR security review, vulnerability lifecycle management, and supply chain security. This skill enables a security engineer to build, operate, and continuously improve the security operations function across the entire software development lifecycle — from code commit to production monitoring.

## Competency Dimensions

| Dimension                | Proficiency Level | Key Capabilities                                                                     |
| ------------------------ | ----------------- | ------------------------------------------------------------------------------------ |
| SIEM Operations          | Expert            | Splunk, ELK Stack, alert tuning, threat hunting, dashboard design                    |
| SAST/DAST/SCA Pipeline   | Expert            | Tool integration, false positive reduction, policy-as-code, developer feedback loops |
| PR Security Review       | Advanced          | Threat modeling at code level, secret detection, dependency risk assessment          |
| Vulnerability Management | Expert            | Triage, SLA enforcement, remediation tracking, risk scoring (CVSS/EPSS)              |
| Supply Chain Security    | Advanced          | SBOM generation, dependency auditing, SLSA framework, provenance verification        |

## Execution Guidance

### SIEM Operations (Splunk, ELK)

**Architecture:**

- Deploy centralized log aggregation from all platforms (Android, iOS, KMP, Flutter backends)
- Ingest application logs, infrastructure metrics, network flow data, and authentication events
- Configure data retention policies: hot (7d), warm (30d), cold (1y), archive (7y) for compliance
- Implement role-based access to SIEM dashboards following least-privilege principle

**Alert Design:**

- Use statistical anomaly detection for baseline deviation (failed login spikes, unusual API call patterns)
- Create correlation rules linking multiple low-severity events into high-severity incidents
- Implement alert fatigue reduction: suppress duplicates within 5-minute windows, auto-close resolved alerts
- Escalation matrix: P0 → page security team within 5 min, P1 → within 15 min, P2 → next business day

**Threat Hunting:**

- Proactively search for IOCs (Indicators of Compromise) using MITRE ATT&CK framework mapping
- Build hypothesis-driven hunts: "If an attacker has compromised X, we would see Y in the logs"
- Document hunt findings in standardized runbooks for future automation

### SAST/DAST/SCA Pipeline Management

**SAST (Static Application Security Testing):**

- Integrate SAST tools (Semgrep, CodeQL, SonarQube) into CI pipeline at the build stage
- Configure language-specific rulesets: Swift/Objective-C for iOS, Kotlin/Java for Android, Dart for Flutter
- Set quality gates: block merge on Critical/High severity findings; warn on Medium
- Implement incremental scanning: only scan changed files and their dependencies to reduce scan time

**DAST (Dynamic Application Security Testing):**

- Deploy DAST scanners (OWASP ZAP, Burp Suite Enterprise) against staging environments
- Configure authenticated scans with test user credentials covering all user roles
- Schedule full scans nightly; incremental scans on every staging deployment
- Map DAST findings back to source code locations for developer remediation

**SCA (Software Composition Analysis):**

- Run SCA (Snyk, Dependabot, Trivy) on every commit to detect vulnerable dependencies
- Enforce allowlist/denylist policies for approved dependency versions
- Generate SBOM (Software Bill of Materials) in SPDX format for every build artifact
- Implement automated PR creation for dependency updates with security patches

### PR Security Review Checklist

For every pull request, evaluate:

1. **Authentication & Authorization:** Are new endpoints properly guarded? Is token validation implemented?
2. **Input Validation:** Is all user input sanitized? Are parameterized queries used for database operations?
3. **Secret Management:** Are API keys, tokens, or credentials hardcoded? Use secret scanning tools.
4. **Dependency Changes:** Do new dependencies introduce known vulnerabilities? Check SBOM diff.
5. **Cryptographic Implementation:** Are standard libraries used? No custom crypto implementations.
6. **Error Handling:** Do error messages leak sensitive information (stack traces, internal paths)?
7. **Rate Limiting:** Are new endpoints protected against abuse and DoS?
8. **Data Exposure:** Does the PR expose PII, financial data, or health information without encryption?

### Vulnerability Management Lifecycle

1. **Discovery:** Automated (SAST/DAST/SCA) + manual (pen testing, bug bounty)
2. **Triage:** Classify severity using CVSS 3.1 + EPSS for exploit likelihood
3. **Assignment:** Route to owning team with SLA based on severity:
   - Critical (CVSS 9.0+): 24 hours
   - High (CVSS 7.0–8.9): 7 days
   - Medium (CVSS 4.0–6.9): 30 days
   - Low (CVSS 0.1–3.9): 90 days
4. **Remediation:** Developer fixes, security engineer validates
5. **Verification:** Re-run SAST/DAST scan to confirm fix; regression test affected functionality
6. **Closure:** Document root cause, update runbooks, feed learnings into threat models

### Supply Chain Security

**SBOM Generation:**

- Generate SBOM for every platform build (Android AAB, iOS IPA, Flutter APK)
- Use Syft or CycloneDX CLI for automated SBOM creation
- Store SBOM as a build artifact alongside the binary

**Dependency Auditing:**

- Maintain a centralized dependency registry with approved versions
- Monitor for new CVEs in the dependency tree daily
- Evaluate new dependencies against criteria: active maintenance, security track record, license compatibility
- Implement dependency pinning: lock exact versions, no wildcard ranges in production

**SLSA Framework Compliance:**

- Target SLSA Level 2 for all production builds:
  - Build service (not developer workstation)
  - Build provenance (signed, tamper-evident build metadata)
  - Source integrity (verified origin, no unauthorized modifications)

## Pipeline Integration

| Pipeline Stage         | Security Operations Activity                                                |
| ---------------------- | --------------------------------------------------------------------------- |
| Stage 1 (Requirements) | Define security acceptance criteria in SRD; identify threat surface         |
| Stage 3 (Architecture) | Review architecture for security design patterns; threat model using STRIDE |
| Stage 5 (Development)  | SAST/SCA scans on every commit; PR security review checklist                |
| Stage 6 (Code Review)  | Security sign-off on Defect Report; verify no P0/P1 security defects        |
| Stage 7 (Testing)      | DAST scans against staging; vulnerability scan results in test report       |
| Stage 8 (Integrity)    | SBOM verification; dependency audit; SLSA provenance check                  |
| Stage 10 (Release)     | Final security clearance; penetration test review; compliance attestation   |

## Quality Standards

- **SIEM coverage:** 100% of production services must send logs to SIEM
- **SAST scan time:** Must complete within 10 minutes for incremental scans
- **False positive rate:** SAST findings must have <15% false positive rate after tuning
- **Vulnerability SLA compliance:** 95% of vulnerabilities remediated within SLA
- **SBOM completeness:** 100% of production builds must have an associated SBOM
- **PR review coverage:** 100% of PRs with security-impacting changes must receive security review

## Reference Materials

- MITRE ATT&CK Framework: https://attack.mitre.org/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- NIST Vulnerability Management Guide: SP 800-40 Rev. 4
- SLSA Framework: https://slsa.dev/
- SPDX Specification: https://spdx.dev/
- CVSS 3.1 Calculator: https://www.first.org/cvss/calculator/3.1
- EPSS (Exploit Prediction Scoring System): https://www.first.org/epss/
