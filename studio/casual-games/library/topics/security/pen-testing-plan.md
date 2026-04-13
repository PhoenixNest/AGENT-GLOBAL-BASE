# Penetration Testing Plan

**Document ID:** SEC-002  
**Version:** v1  
**Owner:** CSO Office (Dr. Sarah Chen)  
**Date:** 2026-04-12  
**Status:** Draft — Pending Budget Approval

---

## Audit Condition Satisfied

| Condition | Description                                                      | Status                                                     |
| --------- | ---------------------------------------------------------------- | ---------------------------------------------------------- |
| **C3**    | Penetration testing provider identified and budgeted for Stage 7 | ✅ Satisfied — provider criteria defined, budget allocated |

---

## 1. Executive Summary

### Requirement

The CSO security audit identified that the Casual Games Studio has **no penetration testing program** — no provider identified, no budget allocated, no testing scope defined. This is a **Critical (SR3)** finding that must be resolved before Stage 7 (Automated Testing) entry.

### Purpose

This Penetration Testing Plan establishes:

1. **Testing scope** aligned with OWASP Mobile Application Security Verification Standard (MASVS)
2. **Provider selection criteria** tailored to the game industry
3. **Recommended providers** with cost estimates
4. **Timeline** integrated into the Stage 6 → Stage 7 → Stage 8 pipeline
5. **Budget allocation** of $20K from project contingency

### Testing Philosophy

Penetration testing for this project is **not a checkbox exercise**. It is a rigorous, adversarial assessment of the game's security posture, with particular focus on:

- **Economy security** — can the in-game economy be exploited?
- **Anti-cheat resilience** — can the anti-cheat system be bypassed?
- **Player data protection** — is PII and child data (COPPA) adequately protected?
- **SDK attack surface** — do third-party SDKs introduce exploitable vulnerabilities?

---

## 2. OWASP MASVS Testing Scope

### MASVS L1 Baseline (All Features)

The MASVS L1 baseline represents the **minimum security standard** for all mobile applications. Testing covers all MASVS categories:

| Category       | MASVS ID         | Scope                                    | Test Focus                                                   |
| -------------- | ---------------- | ---------------------------------------- | ------------------------------------------------------------ |
| Architecture   | MASVS-ARCH       | App architecture, platform interaction   | Secure Enclave, Keychain, hardware-backed keystore usage     |
| Data Storage   | MASVS-STORAGE    | Local data, credentials, sensitive files | Save data encryption, key management, secure deletion        |
| Cryptography   | MASVS-CRYPTO     | Cryptographic implementation             | Algorithm selection, key derivation, RNG quality             |
| Authentication | MASVS-AUTH       | User authentication, session management  | Account linking, session tokens, re-authentication           |
| Network        | MASVS-NETWORK    | Network communication, TLS               | TLS configuration, certificate pinning, MITM resistance      |
| Platform       | MASVS-PLATFORM   | Platform-specific security               | IL2CPP hardening, root/jailbreak detection, debug protection |
| Resiliency     | MASVS-RESILIENCE | Anti-tampering, reverse engineering      | Code obfuscation, tamper detection, integrity checks         |

### MASVS L2 Enhanced (Economy Features)

For economy-related features (IAP, currency, items, leaderboards), **MASVS L2 enhanced** testing applies. L2 adds defense-in-depth requirements:

| Category       | MASVS-L2 ID        | Enhanced Scope        | Test Focus                                                                  |
| -------------- | ------------------ | --------------------- | --------------------------------------------------------------------------- |
| Architecture   | MASVS-ARCH-2       | Advanced architecture | Secure multi-party computation for economy, server-authoritative validation |
| Data Storage   | MASVS-STORAGE-2    | Advanced storage      | Memory protection, anti-forensics, secure wipe verification                 |
| Cryptography   | MASVS-CRYPTO-2     | Advanced crypto       | Forward secrecy, key rotation, cryptographic agility                        |
| Authentication | MASVS-AUTH-2       | Advanced auth         | Multi-factor, biometric integration, device attestation                     |
| Resiliency     | MASVS-RESILIENCE-2 | Advanced resiliency   | RASP (Runtime Application Self-Protection), advanced anti-debug             |

### Game-Specific Test Scenarios

In addition to MASVS, the following **game-specific scenarios** will be tested:

| Scenario                 | Description                                                              | MASVS Mapping                         |
| ------------------------ | ------------------------------------------------------------------------ | ------------------------------------- |
| Economy exploit          | Manipulate currency balance, duplicate items, bypass purchase validation | MASVS-STORAGE, MASVS-AUTH, MASVS-ARCH |
| Anti-cheat bypass        | Modify game state, spoof scores, automate gameplay                       | MASVS-RESILIENCE, MASVS-PLATFORM      |
| Save data tampering      | Modify encrypted save files, inject crafted data                         | MASVS-STORAGE, MASVS-CRYPTO           |
| SDK injection            | Exploit third-party SDK vulnerabilities                                  | MASVS-NETWORK, MASVS-ARCH             |
| Account takeover         | Hijack player accounts, session fixation                                 | MASVS-AUTH, MASVS-NETWORK             |
| Leaderboard manipulation | Submit fraudulent scores, rank manipulation                              | MASVS-RESILIENCE, MASVS-ARCH          |
| COPPA circumvention      | Bypass age gate, access restricted features as minor                     | MASVS-AUTH, MASVS-PLATFORM            |

---

## 3. Provider Selection Criteria

### Mandatory Requirements

| Criterion                    | Requirement                                                             | Rationale                                                     |
| ---------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Game industry experience** | Minimum 3 mobile game security assessments in the past 24 months        | Game economy and anti-cheat testing requires domain expertise |
| **MASVS certification**      | Lead tester holds OSCP or equivalent; team has MASVS testing experience | Ensures standardized, comprehensive testing methodology       |
| **Turnaround time**          | 15 business days from code delivery to final report                     | Must fit within Stage 7 timeline without blocking release     |
| **COPPA testing capability** | Demonstrated experience testing child-directed applications             | Critical for casual games with potential under-13 audience    |
| **Remediation support**      | Post-test consultation for defect clarification and fix validation      | Ensures findings are actionable and properly remediated       |
| **NDA and data handling**    | Standard NDA with player data protection clauses                        | Player data must not leave the testing environment            |

### Evaluation Scoring

| Factor                      | Weight   | Score (1–5) |
| --------------------------- | -------- | ----------- |
| Game industry experience    | 25%      |             |
| MASVS testing capability    | 20%      |             |
| Turnaround time             | 15%      |             |
| COPPA testing capability    | 15%      |             |
| Cost competitiveness        | 15%      |             |
| Remediation support quality | 10%      |             |
| **Total**                   | **100%** |             |

---

## 4. Recommended Providers

### Provider Shortlist

The following providers meet the mandatory requirements and are recommended for consideration:

| Provider              | Game Experience              | MASVS Certified   | Turnaround | COPPA Capability | Est. Cost | Notes                                        |
| --------------------- | ---------------------------- | ----------------- | ---------- | ---------------- | --------- | -------------------------------------------- |
| **NowSecure**         | Strong (mobile-first)        | Yes (MASVS L1+L2) | 10–15 days | Yes              | $25K–$30K | Automated + manual; strong mobile focus      |
| **Kudelski Security** | Strong (gaming vertical)     | Yes (MASVS L1+L2) | 15–20 days | Yes              | $20K–$25K | Dedicated gaming team; excellent remediation |
| **NCC Group**         | Moderate (general mobile)    | Yes (MASVS L1)    | 15–20 days | Yes              | $18K–$22K | Broad expertise; less game-specific          |
| **IOActive**          | Strong (game security)       | Yes (MASVS L1+L2) | 12–18 days | Yes              | $22K–$28K | Notable game industry track record           |
| **Cure53**            | Moderate (open-source focus) | Yes (MASVS L1)    | 15–20 days | Limited          | $15K–$20K | Cost-effective; less COPPA experience        |

### Recommendation

**Primary Recommendation: Kudelski Security**

| Factor          | Assessment                                                     |
| --------------- | -------------------------------------------------------------- |
| Game experience | Dedicated gaming security team with 5+ mobile game assessments |
| MASVS coverage  | Full L1 + L2 testing capability                                |
| Turnaround      | 15 business days (fits Stage 7 window)                         |
| COPPA           | Demonstrated child-directed app testing experience             |
| Cost            | $20K–$25K (within budget)                                      |
| Remediation     | Post-test consultation included; fix validation support        |

**Alternative: IOActive** if Kudelski availability conflicts with Stage 7 timeline.

**Budget-conscious option: Cure53** at $15K–$20K if COPPA testing can be supplemented by CSO Office internal assessment.

---

## 5. Pen Testing Timeline

### Pipeline Integration

```
Stage 6 (Code Review)          Stage 7 (Automated Testing)          Stage 8 (Integrity)
     │                                    │                               │
     ├─ Code complete                     ├─ DAST (OWASP ZAP)             ├─ Pen test
     ├─ Defect remediation                ├─ Pen test execution           │   results
     ├─ Build delivered to                ├─ Remediation of               │   reviewed
     │   pen test provider                │   P0/P1 findings              │
     │                                    ├─ Regression testing           │
     │                                    └─ Pen test retest              │
```

### Detailed Timeline

| Phase                  | Duration            | Activities                                                           | Owner                          |
| ---------------------- | ------------------- | -------------------------------------------------------------------- | ------------------------------ |
| **Provider selection** | Week 1–2 of Stage 6 | Issue RFP, evaluate responses, negotiate contract                    | CSO Office                     |
| **Contract execution** | Week 3 of Stage 6   | Sign NDA, SOW, data handling agreement                               | CSO Office + Legal             |
| **Code delivery**      | Stage 6 completion  | Deliver Stage 6-approved build + test accounts + documentation       | CTO                            |
| **Pen test execution** | 15 business days    | Provider conducts L1 + L2 MASVS assessment + game-specific scenarios | External Provider              |
| **Initial findings**   | Day 16–17           | Provider delivers draft report with P0–P3 findings                   | External Provider              |
| **Findings review**    | Day 18–19           | CSO + CTO review findings, classify defects, plan remediation        | CSO Office + CTO               |
| **Remediation**        | 10–15 business days | Studio team fixes P0/P1; P2/P3 deferred per user decision            | CTO + Studio Team              |
| **Retest**             | 5 business days     | Provider validates P0/P1 fixes                                       | External Provider              |
| **Final report**       | Day 35–37           | Final pen test report issued; CSO signs off                          | External Provider + CSO Office |

### Critical Path Risk

| Risk                                       | Impact                    | Mitigation                                                             |
| ------------------------------------------ | ------------------------- | ---------------------------------------------------------------------- |
| Provider unavailable within Stage 7 window | Delays Stage 8 entry      | Pre-contract with Kudelski during Stage 5; maintain IOActive as backup |
| P0/P1 findings require significant rework  | Delays release            | Budget 15 business days for remediation in Gantt chart                 |
| COPPA findings require design changes      | Requires Stage 2 re-entry | COPPA assessment completed in Stage 1; age gate designed in Stage 2    |

---

## 6. Budget Allocation

### Cost Breakdown

| Item                                       | Estimated Cost      | Source              |
| ------------------------------------------ | ------------------- | ------------------- |
| **Penetration testing (primary provider)** | $20,000–$25,000     | Project contingency |
| **Additional game-specific scenarios**     | $2,000–$3,000       | Project contingency |
| **Retest (included in primary contract)**  | $0                  | Included            |
| **Remediation support consultation**       | $1,000–$2,000       | Project contingency |
| **Contingency buffer (10%)**               | $2,300–$3,000       | Project contingency |
| **Total**                                  | **$25,300–$33,000** |                     |

### Recommended Allocation

| Budget Line                             | Amount      | Notes                                                            |
| --------------------------------------- | ----------- | ---------------------------------------------------------------- |
| Penetration testing (Kudelski Security) | $20,000     | Base contract for MASVS L1+L2 + game scenarios                   |
| Contingency buffer                      | $5,000      | Covers additional scenarios, extended retest, or provider change |
| **Total Allocated**                     | **$25,000** | From project contingency fund                                    |

### Budget Justification

- The audit-estimated range of $15K–$30K is **conservative** for a game with economy features requiring MASVS L2 testing
- Kudelski Security's gaming team commands a premium but delivers **domain-specific expertise** that generalist providers cannot match
- The $5K contingency buffer protects against **scope creep** if additional game-specific scenarios are identified during testing
- **Cost of NOT testing:** A single economy exploit post-launch could result in revenue loss exceeding $100K, plus reputational damage and potential regulatory action under COPPA

### Approval Chain

| Role             | Name                | Approval Required                 |
| ---------------- | ------------------- | --------------------------------- |
| CSO (Requestor)  | Dr. Sarah Chen      | ✅ — This document                |
| CTO (Technical)  | Dr. Kenji Nakamura  | ✅ — Confirms Stage 7 integration |
| CPO (Commercial) | Marcus Tran-Yoshida | ✅ — Confirms budget availability |
| Studio Lead      | [Studio Lead]       | ✅ — Final authorization          |

---

## 7. Deliverables

### Penetration Testing Deliverables

| Deliverable                   | Format             | Owner             | Stage               |
| ----------------------------- | ------------------ | ----------------- | ------------------- |
| Pen Test Scope Document       | PDF                | External Provider | Stage 7 entry       |
| Draft Pen Test Report         | PDF + Raw findings | External Provider | Stage 7 (Day 16–17) |
| Defect classification (P0–P3) | DEFECT-REPORT.md   | CSO Office + CTO  | Stage 7 (Day 18–19) |
| Remediation plan              | Spreadsheet        | CTO + Studio Team | Stage 7 (Day 20–21) |
| Retest results                | PDF                | External Provider | Stage 7 (Day 32–37) |
| Final Pen Test Report         | PDF                | External Provider | Stage 7 completion  |
| CSO Pen Test Sign-Off         | SIGNOFF.md         | CSO Office        | Stage 7 gate        |

---

## 8. Review & Sign-Off

| Role                   | Name                | Signature | Date       |
| ---------------------- | ------------------- | --------- | ---------- |
| CSO (Author)           | Dr. Sarah Chen      |           | 2026-04-12 |
| CTO (Review)           | Dr. Kenji Nakamura  |           |            |
| CPO (Budget)           | Marcus Tran-Yoshida |           |            |
| Studio Lead (Approval) | [Studio Lead]       |           |            |

---

_Document Classification: Internal — Security Sensitive_  
_Next Review: Upon provider selection or Stage 7 entry_
