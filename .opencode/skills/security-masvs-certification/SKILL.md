---
name: security-masvs-certification
description: MASVS certification pathway for mobile apps — external assessor engagement, certification evidence preparation, audit coordination, compliance gap remediation, and certification maintenance for OWASP MASVS Level 1 and Level 2. Owned by Omar Farouq (Security Engineer). Use during Stage 8 (Integrity Verification) for certification preparation and Stage 10 (Release Readiness) for certification sign-off. Trigger: MASVS certification, external assessor, certification evidence, audit coordination, compliance gap, MASVS Level 1, MASVS Level 2, certification maintenance.
prerequisites:
  - security-masvs-owasp-masvs-compliance

version: "1.0.0"
---

# MASVS Certification Process

## Overview

### Certification vs. Internal Compliance

| Aspect        | Internal Compliance                      | Formal MASVS Certification                             |
| ------------- | ---------------------------------------- | ------------------------------------------------------ |
| **Purpose**   | Self-assessment for engineering teams    | Third-party validation for market/regulatory trust     |
| **Assessor**  | Internal CSO team or CTO panel           | OWASP-accredited independent assessor                  |
| **Evidence**  | Internal test reports, SAST/DAST results | Structured evidence package reviewed by external party |
| **Outcome**   | Internal sign-off (Stage 8)              | Official MASVS certification level badge               |
| **Validity**  | Per-release (tied to Stage 8)            | 12 months (annual re-certification required)           |
| **Cost**      | Internal resource cost only              | $15,000–$50,000 USD per assessment cycle               |
| **Timeline**  | Integrated into pipeline (days)          | 4–12 weeks end-to-end                                  |
| **Authority** | CSO (Dr. Sarah Chen)                     | OWASP MASVS Accredited Assessor                        |

### When to Pursue Formal Certification

| Trigger                                 | Recommended Level | Timing                          |
| --------------------------------------- | ----------------- | ------------------------------- |
| Enterprise B2B customer requirement     | MASVS L1          | Before contract signature       |
| Government/defense contract             | MASVS L1 + L2     | During Stage 1 SRD scoping      |
| Financial services / fintech app        | MASVS L2 (R)      | Before app store submission     |
| Health / medical data handling          | MASVS L2 + L3 (R) | During Stage 3 architecture     |
| High-value target app (crypto, wallets) | MASVS L2 (R) full | After Stage 8 internal sign-off |
| Competitive differentiation             | MASVS L1          | After Stage 10 release          |

### Certification Levels

| Level      | Designation            | Scope                               | Assessment Type                 |
| ---------- | ---------------------- | ----------------------------------- | ------------------------------- |
| **L1**     | MASVS Standard         | Baseline security for all apps      | Self-assessment or assessor-led |
| **L2**     | MASVS Defence-in-Depth | L1 + advanced security controls     | Assessor-led required           |
| **L2 (R)** | MASVS Resilience       | L2 + reverse-engineering resistance | Assessor-led + penetration test |
| **L3**     | MASVS Privacy          | L1 + privacy-by-design controls     | Assessor-led + privacy audit    |

---

## Accredited Assessor Engagement

### Finding an Accredited Assessor

| Step | Action                                             | Responsible              | Output                        |
| ---- | -------------------------------------------------- | ------------------------ | ----------------------------- |
| 1    | Review current OWASP accredited assessor list      | CSO                      | Shortlist of 3–5 assessors    |
| 2    | Verify assessor scope (mobile, specific platforms) | CSO                      | Scope-qualified assessor list |
| 3    | Request proposals (RFP) with timeline and cost     | CSO + CHRO (procurement) | Received proposals            |
| 4    | Evaluate proposals against criteria below          | CSO + CTO                | Scored evaluation matrix      |
| 5    | Select assessor and execute Statement of Work      | CSO + CHRO               | Signed contract               |

### Assessor Selection Criteria

| Criterion                      | Weight | Description                                             |
| ------------------------------ | ------ | ------------------------------------------------------- |
| **OWASP accreditation status** | 20%    | Current, active accreditation with no sanctions         |
| **Mobile platform expertise**  | 20%    | Demonstrated iOS + Android assessment experience        |
| **Industry domain experience** | 15%    | Prior work in your app's domain (fintech, health, etc.) |
| **Assessment timeline**        | 15%    | Ability to complete within required window              |
| **Cost competitiveness**       | 15%    | Total cost relative to market average                   |
| **Report quality sample**      | 10%    | Redacted sample report demonstrating depth              |
| **Post-assessment support**    | 5%     | Remediation guidance availability                       |

### Engagement Checklist

- [ ] NDA executed before evidence sharing
- [ ] Statement of Work defines scope (MASVS level, platforms, app versions)
- [ ] Timeline includes kickoff, evidence review, assessment period, and report delivery
- [ ] Communication channel established (dedicated Slack/email, weekly sync)
- [ ] Escalation path defined (CSO ↔ Assessor Lead)
- [ ] Payment terms agreed (typically 50% upfront, 50% on delivery)
- [ ] Confidentiality and data handling clauses reviewed by Legal
- [ ] Assessor confirms understanding of app architecture and technology stack

---

## Evidence Package Preparation

### Evidence Package Structure

The evidence package maps to MASVS V1 through V8 categories. Each category requires specific documentation artifacts.

| Category | MASVS Domain                           | Required Evidence                                                      | Owner                |
| -------- | -------------------------------------- | ---------------------------------------------------------------------- | -------------------- |
| **V1**   | Architecture, Design & Threat Modeling | UML diagrams, ADRs, threat model, data flow diagrams                   | CTO + CSO            |
| **V2**   | Data Storage & Privacy                 | Encryption configs, Keychain/Keystore docs, data classification matrix | CSO + Platform Leads |
| **V3**   | Cryptography                           | Cipher specs, key management procedures, certificate pinning config    | CSO                  |
| **V4**   | Authentication & Session Management    | Auth flow diagrams, token lifecycle, session timeout configs           | Backend Lead + CSO   |
| **V5**   | Network Communication                  | TLS config, certificate pinning, API security controls                 | CSO + DevOps Lead    |
| **V6**   | Platform Interaction                   | Platform permission model, IPC security, intent filtering              | Platform Leads + CSO |
| **V7**   | Resilience (L2 R)                      | Obfuscation config, anti-tampering measures, root/jailbreak detection  | CSO + Platform Leads |
| **V8**   | Privacy (L3)                           | Privacy impact assessment, data minimization proof, consent flows      | CSO + CPO            |

### V1: Architecture, Design & Threat Modeling

| Evidence Item                    | Format      | Source Location                             |
| -------------------------------- | ----------- | ------------------------------------------- |
| System architecture diagram      | Mermaid/PNG | `architecture/uml/v{N}/class-diagrams/`     |
| Data flow diagram (DFD)          | Mermaid/PNG | `architecture/uml/v{N}/component-diagrams/` |
| Threat model (STRIDE or similar) | Markdown    | `security/audits/threat-model.md`           |
| Architecture Decision Records    | Markdown    | `architecture/decisions/ADR-{NNN}.md`       |
| Security Requirements Document   | Markdown    | `requirements/srd/final/SRD.md`             |

### V2: Data Storage & Privacy

| Evidence Item                                 | Format         | Source Location                              |
| --------------------------------------------- | -------------- | -------------------------------------------- |
| Data classification matrix                    | Table/Markdown | `security/compliance/data-classification.md` |
| iOS Keychain access group config              | Code + docs    | `platforms/ios/code/` + security audit       |
| Android Keystore implementation               | Code + docs    | `platforms/android/code/` + security audit   |
| EncryptedSharedPreferences / SQLCipher config | Code + docs    | Platform code + SAST report                  |
| Secure file storage verification              | Test report    | `testing/results/`                           |
| Data retention and deletion policy            | Markdown       | `security/compliance/data-retention.md`      |

### V3: Cryptography

| Evidence Item                         | Format         | Source Location                         |
| ------------------------------------- | -------------- | --------------------------------------- |
| Cipher algorithm inventory            | Table/Markdown | `security/audits/crypto-inventory.md`   |
| Key generation and rotation procedure | Markdown       | `security/compliance/key-management.md` |
| Certificate pinning implementation    | Code + config  | Platform code + network security config |
| Random number generator validation    | Test report    | `testing/results/crypto-tests/`         |
| Hash function usage audit             | SAST report    | `security/audits/sast-report.md`        |

### V4: Authentication & Session Management

| Evidence Item                        | Format               | Source Location                             |
| ------------------------------------ | -------------------- | ------------------------------------------- |
| Authentication flow sequence diagram | Mermaid/PNG          | `architecture/uml/v{N}/sequence-diagrams/`  |
| Token lifecycle documentation        | Markdown             | `security/audits/auth-token-lifecycle.md`   |
| Session timeout configuration        | Code + config        | Platform code + backend config              |
| Biometric authentication flow        | Code + IDS reference | Platform code + `design/interaction-specs/` |
| OAuth/OIDC implementation            | Code + config        | Backend code + platform code                |
| Password policy enforcement          | Code + config        | Backend validation + platform UI            |

### V5: Network Communication

| Evidence Item                                  | Format          | Source Location                  |
| ---------------------------------------------- | --------------- | -------------------------------- |
| TLS configuration (min version, cipher suites) | Config + docs   | `security/audits/tls-config.md`  |
| Certificate pinning setup                      | Code + pin list | Platform network security config |
| API authentication mechanism                   | Code + docs     | Backend + platform code          |
| Network traffic analysis report                | Pen test report | `security/penetration-tests/`    |
| WebView security controls                      | Code + config   | Platform code                    |

### V6: Platform Interaction

| Evidence Item                           | Format         | Source Location                        |
| --------------------------------------- | -------------- | -------------------------------------- |
| Platform permission justification       | Table/Markdown | `security/audits/permissions-audit.md` |
| IPC/broadcast security                  | Code + docs    | Platform code                          |
| Intent filtering / deep link validation | Code + docs    | Platform code                          |
| Clipboard / screenshot protection       | Code + config  | Platform code                          |
| Keyboard cache / autofill exclusion     | Code + config  | Platform code                          |
| URL scheme validation                   | Code + docs    | Platform code                          |

### V7: Resilience (L2 R Requirements)

| Evidence Item                      | Format             | Source Location                    |
| ---------------------------------- | ------------------ | ---------------------------------- |
| Code obfuscation configuration     | Config + report    | ProGuard/R8 config + build output  |
| Anti-tampering mechanisms          | Code + docs        | Platform code                      |
| Root/jailbreak detection           | Code + test report | Platform code + `testing/results/` |
| Debugger detection                 | Code + test report | Platform code                      |
| Emulator detection (if applicable) | Code + test report | Platform code                      |
| Integrity verification checks      | Code + docs        | Platform code                      |

### V8: Privacy (L3 Requirements)

| Evidence Item                      | Format               | Source Location                           |
| ---------------------------------- | -------------------- | ----------------------------------------- |
| Privacy Impact Assessment (PIA)    | Markdown             | `security/audits/privacy-assessment.md`   |
| Data minimization evidence         | Table + code         | Data map + platform code                  |
| User consent flow                  | Code + IDS reference | Platform UI + `design/interaction-specs/` |
| Data subject rights implementation | Code + docs          | Backend + platform code                   |
| Third-party SDK privacy audit      | Report               | `security/audits/sdk-privacy-audit.md`    |
| Privacy policy (in-app)            | Markdown/HTML        | `design/prototype/` + platform code       |

---

## Certification Lifecycle

### Phase 1: Initial Certification

| Step | Activity                                                 | Duration  | Responsible          |
| ---- | -------------------------------------------------------- | --------- | -------------------- |
| 1.1  | Internal MASVS self-assessment (all V1–V8)               | 1–2 weeks | CSO + team           |
| 1.2  | Gap analysis and remediation planning                    | 1 week    | CSO                  |
| 1.3  | Remediation of identified gaps                           | 2–6 weeks | Platform teams + CSO |
| 1.4  | Engage accredited assessor (see Engagement section)      | 1–2 weeks | CSO + CHRO           |
| 1.5  | Prepare evidence package (see Evidence section)          | 1–2 weeks | CSO + CTO            |
| 1.6  | Assessor kickoff and evidence submission                 | 1 day     | CSO + Assessor       |
| 1.7  | Assessor review period (may request additional evidence) | 2–4 weeks | Assessor             |
| 1.8  | Assessor report and certification decision               | 1 week    | Assessor             |
| 1.9  | Remediation of assessor findings (if any)                | 1–4 weeks | Platform teams       |
| 1.10 | Certificate issuance                                     | 1 week    | Assessor             |

**Total estimated timeline: 4–12 weeks**

### Phase 2: Annual Re-Certification

| Step | Activity                                                     | Duration  | Responsible |
| ---- | ------------------------------------------------------------ | --------- | ----------- |
| 2.1  | Annual internal MASVS re-assessment                          | 1 week    | CSO         |
| 2.2  | Update evidence package for changes since last certification | 1 week    | CSO + CTO   |
| 2.3  | Engage same or new assessor for annual review                | 1–2 weeks | CSO + CHRO  |
| 2.4  | Assessor review (abbreviated if no significant changes)      | 1–3 weeks | Assessor    |
| 2.5  | Certificate renewal                                          | 1 week    | Assessor    |

**Total estimated timeline: 3–6 weeks**

### Phase 3: Re-Certification After Expiry

| Step | Activity                                                    | Duration   | Responsible    |
| ---- | ----------------------------------------------------------- | ---------- | -------------- |
| 3.1  | Full MASVS re-assessment (treated as initial certification) | 1–2 weeks  | CSO            |
| 3.2  | Full evidence package rebuild                               | 1–2 weeks  | CSO + CTO      |
| 3.3  | Engage assessor and complete full assessment cycle          | 4–12 weeks | CSO + Assessor |

**Note: If certification has lapsed, the app must NOT claim MASVS certification in marketing materials until re-certified.**

### Certification Status Tracking

| Status          | Definition                           | Action Required                               |
| --------------- | ------------------------------------ | --------------------------------------------- |
| **Certified**   | Active, valid certificate            | Schedule annual review 60 days before expiry  |
| **Conditional** | Certified with noted findings        | Remediate within assessor-defined window      |
| **Suspended**   | Certification paused (major finding) | Immediate remediation, re-assessment required |
| **Revoked**     | Certification withdrawn              | Cease all marketing claims, re-apply as new   |
| **Expired**     | Past validity date without renewal   | Initiate full re-certification                |

---

## Handling Conditional Certifications

### What Is a Conditional Certification?

A conditional certification means the assessor has granted certification **with specific findings** that must be remediated within a defined timeframe. It is not a failure — it is a common outcome for initial certifications.

### Conditional Certification Response Workflow

| Step | Action                                              | Timeline                   | Responsible     |
| ---- | --------------------------------------------------- | -------------------------- | --------------- |
| 1    | Receive assessor report with conditions             | Day 0                      | CSO             |
| 2    | Classify each condition by severity (P0–P3 mapping) | Day 1                      | CSO             |
| 3    | Present conditions to CTO + CPO for prioritization  | Day 2                      | CSO             |
| 4    | Create remediation plan with resource allocation    | Day 3–5                    | CTO             |
| 5    | Execute remediation (code changes, config updates)  | Per assessor window        | Platform teams  |
| 6    | Re-test remediated controls internally              | Post-remediation           | CSO + Test Lead |
| 7    | Submit remediation evidence to assessor             | Before deadline            | CSO             |
| 8    | Receive assessor confirmation of condition closure  | 1–2 weeks after submission | Assessor        |
| 9    | Update internal certification status to "Certified" | Upon confirmation          | CSO             |

### Severity Mapping: Assessor Findings to Internal P-Levels

| Assessor Finding Severity | Internal P-Level | Required Action                              | Timeline            |
| ------------------------- | ---------------- | -------------------------------------------- | ------------------- |
| **Critical**              | P0               | Immediate fix, suspend app release if active | 48 hours            |
| **Major**                 | P1               | Fix before next release                      | 2 weeks             |
| **Minor**                 | P2               | User decides fix or defer                    | Per user decision   |
| **Observation**           | P3               | Backlog for future sprint                    | Next planning cycle |

### Conditional Certification Conditions Table Template

| Condition ID | MASVS Control | Description                                                        | Severity    | Remediation Owner | Target Date | Status      |
| ------------ | ------------- | ------------------------------------------------------------------ | ----------- | ----------------- | ----------- | ----------- |
| COND-001     | V2.3          | Example: Keystore key not hardware-backed on older Android devices | Major       | Android Lead      | 2026-05-01  | Open        |
| COND-002     | V5.2          | Example: Certificate pinning not enforced on legacy API endpoints  | Minor       | Backend Lead      | 2026-05-15  | In Progress |
| COND-003     | V7.1          | Example: Obfuscation missing for third-party SDK wrappers          | Observation | iOS Lead          | 2026-06-01  | Open        |

---

## Stage 10 Integration

### How MASVS Certification Fits Into Stage 10

MASVS certification is **complementary to** but **separate from** the Stage 10 Release Readiness Check. Internal security compliance (Stage 8) is mandatory for every release. Formal MASVS certification is an optional overlay.

| Stage 10 Checklist Item                                | MASVS Certification Relationship                                   |
| ------------------------------------------------------ | ------------------------------------------------------------------ |
| 1. Product — PRD implemented                           | If PRD includes MASVS commitment, certification is required        |
| 2. Design — IDS specifications realised                | Design must support security UX (consent flows, biometric prompts) |
| 3. Architecture — UML/ADR/TSD upheld                   | V1 evidence draws directly from Stage 3 artifacts                  |
| 4. Security — SRD enforced, OWASP MASVS compliant      | **Direct overlap** — Stage 8 IS the internal MASVS assessment      |
| 5. Testing — 100% automated test pass rate             | Test coverage must include V2–V7 control validation                |
| 6. Localisation — all target languages complete        | Privacy translations (V8) must be accurate in all languages        |
| 7. Platform — App Store / Google Play requirements met | MASVS certification may strengthen platform security review        |

### Pre-Certification Gate Checklist

Before engaging an external assessor, the CSO must confirm:

- [ ] Stage 8 Integrity Verification signed off with zero open security findings
- [ ] All V1–V8 evidence items compiled and internally reviewed
- [ ] No P0 or P1 security defects in the defect tracking system
- [ ] SRD (Security Requirements Document) covers all MASVS controls for the target level
- [ ] Platform leads have confirmed all security controls are implemented and tested
- [ ] Legal has reviewed privacy claims (V8) for accuracy
- [ ] CTO has approved resource allocation for assessor engagement
- [ ] CPO has confirmed MASVS certification aligns with product roadmap

### Post-Certification Obligations

| Obligation                                         | Frequency          | Responsible |
| -------------------------------------------------- | ------------------ | ----------- |
| Update MASVS badge in app marketing                | Upon certification | CPO         |
| Publish certification status (if public)           | Upon certification | CPO         |
| Annual re-certification assessment                 | Every 12 months    | CSO         |
| Internal MASVS control re-verification             | Every 6 months     | CSO         |
| Evidence package update on significant app changes | Per change         | CSO + CTO   |
| Report certification changes to assessor           | Within 30 days     | CSO         |

---

## Cost and Timeline

### Cost Breakdown by Certification Level

| Level      | Assessor Fee    | Internal Preparation | Remediation Reserve | Total Estimated Cost |
| ---------- | --------------- | -------------------- | ------------------- | -------------------- |
| **L1**     | $8,000–$15,000  | $3,000–$7,000        | $2,000–$5,000       | **$13,000–$27,000**  |
| **L2**     | $12,000–$25,000 | $5,000–$10,000       | $5,000–$15,000      | **$22,000–$50,000**  |
| **L2 (R)** | $18,000–$35,000 | $7,000–$15,000       | $8,000–$20,000      | **$33,000–$70,000**  |
| **L3**     | $15,000–$30,000 | $5,000–$12,000       | $5,000–$15,000      | **$25,000–$57,000**  |

> **Note:** Costs are in USD and represent 2025–2026 market rates. Actual costs vary by assessor, app complexity, and geographic region. Internal preparation costs reflect engineering time valued at standard contractor rates.

### Timeline by Certification Level

| Level      | Preparation Phase | Assessment Phase | Remediation Phase | Total Range     |
| ---------- | ----------------- | ---------------- | ----------------- | --------------- |
| **L1**     | 2–3 weeks         | 2–4 weeks        | 1–2 weeks         | **5–9 weeks**   |
| **L2**     | 3–5 weeks         | 3–5 weeks        | 2–4 weeks         | **8–14 weeks**  |
| **L2 (R)** | 4–6 weeks         | 4–6 weeks        | 2–6 weeks         | **10–18 weeks** |
| **L3**     | 3–5 weeks         | 3–5 weeks        | 2–4 weeks         | **8–14 weeks**  |

### Timeline Compression Strategies

| Strategy                                                        | Time Saved | Risk                         | Applicability |
| --------------------------------------------------------------- | ---------- | ---------------------------- | ------------- |
| Parallel evidence compilation (V1–V8 teams work simultaneously) | 1–2 weeks  | Low                          | All levels    |
| Pre-engagement with assessor before Stage 8 complete            | 1 week     | Medium (evidence may change) | L1, L2        |
| Use of prior certification evidence (re-certification only)     | 1–3 weeks  | Low                          | Annual only   |
| Expedited assessor (premium pricing)                            | 1–2 weeks  | Low (cost increase ~20%)     | All levels    |

### Budget Planning Template

| Budget Category          | Line Items                              | Estimated Cost | Actual Cost | Variance |
| ------------------------ | --------------------------------------- | -------------- | ----------- | -------- |
| **Assessor Fees**        | Assessment, report, re-assessment       |                |             |          |
| **Internal Preparation** | Engineering time, documentation         |                |             |          |
| **Tooling**              | SAST/DAST licenses, obfuscation tools   |                |             |          |
| **Remediation**          | Code changes, re-testing                |                |             |          |
| **Legal**                | Contract review, privacy review         |                |             |          |
| **Marketing**            | Badge usage, certification announcement |                |             |          |
| **Contingency**          | 15% of total                            |                |             |          |
| **Total**                |                                         |                |             |          |

---

## References

### Primary Sources

| Document                                   | Source           | URL                                                |
| ------------------------------------------ | ---------------- | -------------------------------------------------- |
| OWASP MASVS                                | OWASP Foundation | https://mas.owasp.org/MASVS/                       |
| OWASP MASVS V1–V8 Controls                 | OWASP Foundation | https://mas.owasp.org/MASVS/                       |
| OWASP MSTG (Mobile Security Testing Guide) | OWASP Foundation | https://mas.owasp.org/MSTG/                        |
| MASVS Assessor Accreditation Program       | OWASP            | https://owasp.org/www-project-mobile-app-security/ |

### Internal Company Documents

| Document                             | Location                                | Purpose                                     |
| ------------------------------------ | --------------------------------------- | ------------------------------------------- |
| Security Requirements Document (SRD) | `requirements/srd/final/SRD.md`         | Maps MASVS controls to project requirements |
| Threat Model                         | `security/audits/threat-model.md`       | V1 evidence source                          |
| SAST/DAST Reports                    | `security/audits/`                      | V2–V7 evidence source                       |
| Penetration Test Reports             | `security/penetration-tests/`           | V5, V7 evidence source                      |
| Privacy Assessment                   | `security/audits/privacy-assessment.md` | V8 evidence source                          |
| Architecture Diagrams                | `architecture/uml/v{N}/`                | V1 evidence source                          |
| Stage 8 Integrity Report             | `reviews/integrity-verification/final/` | Pre-certification gate check                |

### Related Skills

| Skill                       | Category       | When to Use                                       |
| --------------------------- | -------------- | ------------------------------------------------- |
| `owasp-masvs-controls`      | security/masvs | Mapping specific MASVS controls to implementation |
| `threat-modeling`           | security/      | Stage 1 SRD creation, V1 evidence                 |
| `penetration-testing`       | security/      | V5, V7 evidence generation                        |
| `privacy-impact-assessment` | security/      | V8 evidence generation                            |
| `crypto-standards`          | security/      | V3 evidence generation                            |

### Certification Body Contacts

| Organization                 | Accreditation Status                       | Contact                    |
| ---------------------------- | ------------------------------------------ | -------------------------- |
| OWASP MASVS Assessor Program | Primary accrediting body                   | https://owasp.org/         |
| Independent security firms   | May hold OWASP accreditation               | Per firm                   |
| Platform-specific programs   | Apple Security Assessment, Google Security | Platform developer portals |

---

## Quick Reference Checklist: MASVS Certification Readiness

```
PRE-CERTIFICATION CHECKLIST
============================

  Internal Compliance
  ─────────────────────
  [ ] Stage 8 signed off (zero open P0/P1)
  [ ] All V1–V8 evidence compiled
  [ ] SRD covers all MASVS controls for target level
  [ ] No open security defects in tracking system
  [ ] Legal reviewed privacy claims (V8)
  [ ] CTO approved resource allocation
  [ ] CPO confirmed product roadmap alignment

  Assessor Engagement
  ─────────────────────
  [ ] NDA executed
  [ ] Statement of Work signed
  [ ] Kickoff meeting scheduled
  [ ] Evidence package delivered to assessor
  [ ] Communication channel established
  [ ] Escalation path defined

  Timeline & Budget
  ─────────────────────
  [ ] Budget approved (assessor + internal + remediation)
  [ ] Timeline agreed with assessor
  [ ] Contingency reserve allocated (15%)
  [ ] Internal team assigned for assessor queries
  [ ] Post-certification marketing plan drafted
```
