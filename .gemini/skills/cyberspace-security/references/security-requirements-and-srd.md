---
name: security-requirements-and-srd
description: Security Requirements Document (SRD) authorship at Stage 1 — defining the security requirements taxonomy, threat model scope, data classification, compliance obligations, and traceability from SRD into subsequent pipeline stages. The SRD is paired with the PRD and co-signed by the CSO before Stage 1 advances. Use when authoring the SRD for any development pipeline.
version: "1.0.0"
---

# Security Requirements and SRD

## Purpose

Author and own the Security Requirements Document (SRD) that travels as a unit with the CPO's PRD from Stage 1 onward. The SRD defines the security posture the product must achieve — not as a wishlist but as a set of binding, testable requirements that later stages (Stage 3 ADRs, Stage 6 Code Review, Stage 7 Automated Testing, Stage 8 Integrity Verification) must satisfy. An SRD without traceability to later-stage gates is not an SRD — it is a decoration.

## Why This Matters

The SRD is the upstream contract for every security decision in the pipeline. If Stage 1 does not define the security requirements clearly, Stage 3 cannot produce coherent ADRs for security-affecting technology decisions, Stage 6 has no baseline to review against, and Stage 8 has no criteria to verify. Security debt always traces back to an absent, vague, or non-binding SRD.

## SRD Authorship Process

### Step 1 — Align on Feature Scope with CPO

Before writing a single requirement, Dr. Sarah Chen reads the PRD draft in full and schedules a 1-hour walkthrough with the CPO (Marcus Tran-Yoshida) and CTO (Dr. Kenji Nakamura). The goals:

- Understand every data element the feature creates, reads, updates, or deletes
- Identify every external touchpoint (third-party SDKs, APIs, payment processors, analytics)
- Confirm the regulatory jurisdictions (GDPR, CCPA, HIPAA-adjacent) the release will operate under

This alignment produces the **Data Asset Inventory** that anchors the SRD:

```markdown
## Data Asset Inventory — [Project Name]

| Data Element    | Classification  | Storage                | Transit                | Retention        | Regulatory Scope |
| --------------- | --------------- | ---------------------- | ---------------------- | ---------------- | ---------------- |
| User email      | PII — Medium    | Server + client        | TLS 1.3                | 7 years          | GDPR, CCPA       |
| Payment token   | PII — High      | Tokenized (no raw PAN) | TLS 1.3 + cert pinning | 0 (transient)    | PCI DSS          |
| Session token   | Auth credential | Keychain / Keystore    | TLS 1.3                | Session lifetime | MASVS            |
| Gameplay events | Pseudonymous    | Analytics service      | TLS 1.3                | 2 years          | GDPR             |
```

### Step 2 — Threat Model Scope

Apply STRIDE to the feature's data flow diagram (provided by CTO from Stage 3 sequence diagrams — the SRD is written at Stage 1, so the CSO works from the PRD-level data flow, not the full UML):

| STRIDE Category            | Feature Risk                                          | Mitigations Required                                 |
| -------------------------- | ----------------------------------------------------- | ---------------------------------------------------- |
| **S**poofing               | Can an attacker impersonate a user or service?        | MFA, token rotation, device attestation              |
| **T**ampering              | Can data in transit or at rest be modified?           | TLS 1.3, cert pinning, HMAC for local data           |
| **R**epudiation            | Can a user deny an action they took?                  | Server-side audit log with tamper-evident timestamps |
| **I**nformation Disclosure | Can sensitive data be exposed?                        | MASVS storage controls, encryption at rest           |
| **D**enial of Service      | Can the feature be degraded or taken offline?         | Rate limiting, graceful degradation                  |
| **E**levation of Privilege | Can a user access data or actions beyond their scope? | Role-based access control, server-side authorization |

### Step 3 — Requirements Authoring

Each SRD requirement follows the `SR-NNN` format:

```markdown
## Security Requirements — [Project Name]

### Authentication and Session Management

**SR-001:** All user authentication shall use the company's central auth service. No feature-specific authentication implementations are permitted.

- **Verification:** Stage 6 code review — CTO + CSO verify no custom auth code exists
- **Stage 3 implication:** ADR required if third-party auth SDK is considered
- **P0 if violated**

**SR-002:** Session tokens shall be stored in Keychain (iOS) / Keystore (Android). No session token may be written to shared storage, UserDefaults, or SharedPreferences.

- **Verification:** Stage 7 SAST scan — Semgrep rule `mobile.insecure-storage`
- **MASVS mapping:** MASVS-STORAGE-1

**SR-003:** Session tokens shall expire after 24 hours of inactivity. Expired tokens shall trigger silent re-authentication without data loss.

- **Verification:** Stage 7 automated test — `SessionExpiry.spec.ts`
- **Stage 3 implication:** Backend token expiry mechanism required; CTO owns ADR

### Data Protection

**SR-004:** All PII shall be encrypted at rest using AES-256-GCM. Encryption key shall be hardware-backed (Keychain/Keystore Secure Enclave where available).

- **Verification:** Stage 7 — unit tests verify encryption; Stage 8 — CSO penetration test
- **MASVS mapping:** MASVS-CRYPTO-1

**SR-005:** No PII shall appear in application logs, crash reports, or analytics events.

- **Verification:** Stage 7 SAST — Semgrep PII-in-logs rule; Stage 8 log review
- **P0 if violated**
```

### Step 4 — Compliance Obligations Table

```markdown
## Compliance Obligations

| Framework      | Applicable?                 | Key Requirements                         | Owner             | Verification Stage       |
| -------------- | --------------------------- | ---------------------------------------- | ----------------- | ------------------------ |
| GDPR           | Yes (EU users)              | Data minimization, right to erasure, DPA | CSO + CPO         | Stage 1 SRD, Stage 8 DPA |
| CCPA           | Yes (CA users)              | Opt-out of sale, privacy notice          | CSO + CPO         | Stage 1 SRD              |
| OWASP MASVS L1 | Yes (all releases)          | All MASVS L1 controls                    | CSO + VP Platform | Stage 7/8                |
| OWASP MASVS L2 | Conditional (auth/payments) | L2 hardening controls                    | CSO               | Stage 7/8                |
| PCI DSS        | If payments                 | No raw PAN storage, TLS, tokenization    | CSO + CTO         | Stage 3 ADR              |
```

### Step 5 — SRD Review and Sign-off

The SRD is complete when:

1. All `SR-NNN` requirements have a **verification method** and **pipeline stage mapping**
2. Compliance table is complete
3. CTO has reviewed and acknowledged the Stage 3 architectural implications
4. CPO has reviewed and confirmed the SRD does not restrict any PRD-required capability without a documented trade-off

Sign-off gate at Stage 1: **CSO signs SRD, CPO signs PRD, user approves both.**

## SRD → Pipeline Traceability

| SRD Section            | Propagates To                  | How                                                                                    |
| ---------------------- | ------------------------------ | -------------------------------------------------------------------------------------- |
| Data Asset Inventory   | Stage 3 ADRs                   | CTO/CIO reference inventory when selecting storage and auth technologies               |
| STRIDE threat model    | Stage 3 SPEC                   | CTO includes threat mitigations in architecture design                                 |
| SR-NNN requirements    | Stage 6 Code Review            | Review panel checks implementation against SRD requirements; any SR violation is P0/P1 |
| SR-NNN requirements    | Stage 7 Automated Testing      | Aisha Patel (VP Quality) adds SRD-derived test cases to the test plan                  |
| SR-NNN requirements    | Stage 8 Integrity Verification | CSO signs off that all SR-NNN requirements are met in the release candidate            |
| Compliance obligations | Stage 8 Integrity Verification | CSO confirms all compliance obligations are satisfied                                  |

## Quality Standards

- SRD delivered within 3 business days of receiving the PRD draft
- Every SR-NNN requirement has a verification method and pipeline stage mapping — no unverifiable requirements
- Zero unresolved PRD/SRD conflicts at Stage 1 sign-off
- SRD reviewed by CTO for architectural implications before sign-off
- All Stage 8 CSO sign-off items trace back to SRD requirements
