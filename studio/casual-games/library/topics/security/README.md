# Security Ownership Matrix

**Document ID:** SEC-001  
**Version:** v1  
**Owner:** CSO Office (Dr. Sarah Chen)  
**Date:** 2026-04-12  
**Status:** Draft — Pending Studio Lead Review

---

## Audit Conditions Satisfied

| Condition | Description                                                         | Status                                                  |
| --------- | ------------------------------------------------------------------- | ------------------------------------------------------- |
| **C1**    | Data privacy compliance ownership assigned                          | ✅ Satisfied — CSO Office retained until dedicated role |
| **C2**    | SDK security vetting process documented and integrated into Stage 1 | ✅ Satisfied — 7-step process defined below             |
| **C4**    | SRD explicitly assigns privacy/age gate/data retention owners       | ✅ Satisfied — ownership matrix maps all domains        |

---

## 1. Executive Summary

### Audit Findings

The CSO security audit of the Casual Games Studio identified **SR1–SR7 risk conditions** that must be resolved before Stage 1 (Concept) entry can be authorized:

| Risk ID | Finding                                                    | Severity    |
| ------- | ---------------------------------------------------------- | ----------- |
| SR1     | No assigned owner for data privacy compliance              | 🔴 Critical |
| SR2     | No SDK security vetting process exists                     | 🔴 Critical |
| SR3     | No penetration testing provider identified or budgeted     | 🔴 Critical |
| SR4     | SRD does not assign privacy/age gate/data retention owners | 🟠 High     |
| SR5     | Cloud Script code review lacks formal enforcement          | 🟠 High     |
| SR6     | No COPPA/GDPR-K compliance assessment                      | 🟠 High     |
| SR7     | No compliance gate review at pipeline stages               | 🟠 High     |

### Risk Assessment Summary

The studio possesses **world-class anti-cheat capability** under Priya Nair (Sr. Backend Engineer), with mature server-side validation and economy security design. However, the **compliance and governance foundation is critically underdeveloped**. No individual or team owns:

- Data privacy compliance (COPPA, GDPR-K, CCPA)
- SDK security review and vetting
- Penetration testing program management
- Age gate and parental consent flow design
- Data retention and deletion policy enforcement

### Purpose of This Document

This Security Ownership Matrix resolves audit conditions **C1, C2, and C4** by:

1. **Assigning explicit ownership** for every security domain to named individuals or the CSO Office
2. **Establishing a formal SDK vetting process** integrated into Stage 1 requirements gathering
3. **Documenting the compliance path** for privacy, age gate, and data retention governance

### CSO Oversight Commitment

Until a dedicated compliance officer or privacy engineer is recruited to the studio, the **CSO Office retains direct oversight** of all compliance, privacy, and SDK vetting activities. This is not a permanent arrangement — it is a **risk mitigation bridge** pending organizational maturity.

---

## 2. Security Ownership Matrix

### Core Security Infrastructure

| Security Domain              | Studio Owner                             | CSO Oversight                  | Stage(s)   | Deliverable               |
| ---------------------------- | ---------------------------------------- | ------------------------------ | ---------- | ------------------------- |
| Anti-cheat framework         | Priya Nair (Sr. Backend)                 | Code review at Stage 6         | 1, 5, 6, 8 | Anti-cheat design doc     |
| Server-side validation       | Priya Nair (Sr. Backend)                 | Architecture review at Stage 3 | 1, 5, 6    | Economy validation spec   |
| PlayFab SDK security         | Priya Nair + Aisha Bello                 | SDK config review at Stage 5   | 5, 7, 10   | SDK security config       |
| Client-side IL2CPP hardening | Dmitri Volkov (Sr. Game Eng)             | Build review at Stage 6        | 5, 6       | Build hardening checklist |
| Save data encryption         | Priya Nair (design) + Aisha Bello (impl) | Crypto review at Stage 6       | 5, 6       | Encryption spec           |
| TLS/transport security       | David Okafor (Live Ops Eng)              | Network review at Stage 7      | 7, 8, 10   | TLS configuration         |

### Compliance & Governance (CSO-Retained)

| Security Domain             | Studio Owner                               | CSO Oversight                                        | Stage(s)    | Deliverable               |
| --------------------------- | ------------------------------------------ | ---------------------------------------------------- | ----------- | ------------------------- |
| SDK vetting & isolation     | **CSO Office (retained)**                  | Direct CSO review                                    | 1, 5, 8     | SDK vetting checklist     |
| Privacy policy              | **CSO Office + UX Writer (Sarah Chen)**    | CSO drafts, Sarah Chen adapts for player-facing copy | 2, 5, 8     | Privacy policy            |
| Age gate / parental consent | Priya Nair (design) + Dmitri Volkov (impl) | CSO design review                                    | 2, 5, 8     | Age gate implementation   |
| Data retention & deletion   | David Okafor (Live Ops Eng)                | CSO requirements review                              | 8, 10       | Retention/deletion policy |
| Penetration testing         | **CSO Office (retained)**                  | CSO engages external provider                        | 7           | Pen test report           |
| Compliance gate review      | **CSO Office (retained)**                  | Direct CSO gate sign-off                             | 1, 6, 8, 10 | Compliance gate report    |
| COPPA compliance            | **CSO Office (retained)**                  | Direct CSO oversight                                 | 1, 2, 5, 8  | COPPA assessment          |

### Ownership Legend

| Role                   | Name               | Function                                                                           |
| ---------------------- | ------------------ | ---------------------------------------------------------------------------------- |
| Sr. Backend Engineer   | Priya Nair         | Anti-cheat, economy validation, security design                                    |
| Cloud Script Developer | Aisha Bello        | PlayFab Cloud Script, serverless functions                                         |
| Sr. Game Engineer      | Dmitri Volkov      | Client-side implementation, IL2CPP, age gate                                       |
| Live Ops Engineer      | David Okafor       | TLS configuration, data retention infrastructure                                   |
| UX Writer              | Sarah Chen         | Privacy policy player-facing copy                                                  |
| **CSO Office**         | **Dr. Sarah Chen** | **Retained oversight: SDK vetting, privacy, COPPA, pen testing, compliance gates** |

---

## 3. Enforcement Rule: Aisha Bello Cloud Script Code Review

**This satisfies CSO condition C5.**

### Rule Statement

All Cloud Script functions authored by Aisha Bello require **dual approval** before merge:

1. **Design approval** from Priya Nair (Sr. Backend) — confirms security architecture alignment
2. **Code review** from Priya Nair or Dmitri Volkov — confirms implementation correctness

### Scope — Mandatory Review Required

The following Cloud Script categories require dual approval **without exception**:

| Category             | Examples                                                  | Risk if Unreviewed                   |
| -------------------- | --------------------------------------------------------- | ------------------------------------ |
| Economy transactions | Currency purchases, item grants, balance adjustments      | Economy exploit, inflation           |
| Purchase validation  | Receipt verification, refund handling, IAP flow           | Revenue fraud, chargeback abuse      |
| Anti-cheat logic     | Score validation, action rate limiting, anomaly detection | Cheat bypass, leaderboards corrupted |
| Data export          | Player data extraction, GDPR data subject requests        | Privacy violation, data leakage      |

### Exemptions — No Review Required

The following Cloud Script categories are **exempt** from dual approval:

| Category             | Examples                                                    | Rationale                            |
| -------------------- | ----------------------------------------------------------- | ------------------------------------ |
| UI-only Cloud Script | Settings sync, cosmetic data retrieval, display preferences | No security impact, no data mutation |

### CI/CD Integration

```yaml
# PlayFab Cloud Script pipeline — automated reviewer assignment
code_review_rules:
  - author: 'aisha.bello'
    categories:
      - economy_transactions
      - purchase_validation
      - anti_cheat_logic
      - data_export
    required_reviewers:
      - 'priya.nair' # design approval (always required)
      - 'priya.nair' # code review (primary)
      - 'dmitri.volkov' # code review (fallback)
    merge_block: true # cannot merge without both approvals

  - author: 'aisha.bello'
    categories:
      - ui_only_settings
      - cosmetic_data
      - display_preferences
    required_reviewers: []
    merge_block: false # exempt from review
```

### Enforcement Mechanism

- **PlayFab DevOps pipeline** enforces reviewer assignment based on author and category tags
- **Merge is blocked** if required approvals are not present
- **Category tagging** is mandatory in Cloud Script function headers:
  ```javascript
  // CATEGORY: economy_transactions
  // AUTHOR: aisha.bello
  // REVIEW-REQUIRED: priya.nair (design + code)
  ```
- **Monthly audit** by CSO Office confirms compliance with this rule

---

## 4. SDK Security Vetting Process

**This satisfies CSO condition C2.**

### Process Integration

The SDK vetting process is a **mandatory prerequisite** for Stage 1 entry. No third-party SDK may be included in the project without completing this vetting process. The process owner is the **CSO Office** (retained).

### 7-Step SDK Vetting Process

#### Step 1: SDK Identification

| Field    | Description                                    |
| -------- | ---------------------------------------------- |
| SDK Name | Official product name                          |
| Version  | Current version and latest available           |
| Provider | Company/organization name                      |
| Purpose  | Functional reason for inclusion in the project |
| Platform | Android, iOS, Unity, PlayFab, etc.             |

#### Step 2: Privacy Policy Review

| Check           | Criteria                                                  |
| --------------- | --------------------------------------------------------- |
| Data collection | What PII, device data, or behavioral data is collected?   |
| Data sharing    | Is data shared with third parties? Under what conditions? |
| Data retention  | How long is data retained? Is deletion supported?         |
| Player consent  | Does the SDK require explicit user consent mechanisms?    |
| COPPA alignment | Is the SDK certified COPPA-compliant?                     |

**Output:** Privacy Risk Rating (Low / Medium / High / Blocker)

#### Step 3: COPPA Compliance Check

| Check                        | Criteria                                                     |
| ---------------------------- | ------------------------------------------------------------ |
| Child-directed data handling | Does the SDK comply with COPPA rules for under-13 users?     |
| Parental consent flow        | Does the SDK support verifiable parental consent?            |
| Data minimization            | Does the SDK collect only necessary data from children?      |
| Third-party sharing          | Does the SDK share child data with advertisers or analytics? |

**Output:** COPPA Compliance Status (Compliant / Conditional / Non-Compliant)

#### Step 4: Network Endpoint Analysis

| Check                 | Criteria                                          |
| --------------------- | ------------------------------------------------- |
| Domain enumeration    | All domains the SDK communicates with             |
| Protocol verification | TLS 1.2+ required; no plaintext HTTP              |
| Certificate pinning   | Does the SDK support or interfere with pinning?   |
| Endpoint geography    | Data residency implications (EU, US, China, etc.) |

**Output:** Network Security Assessment (Pass / Warning / Fail)

#### Step 5: Permission Audit

| Platform | Checks                                                                          |
| -------- | ------------------------------------------------------------------------------- |
| Android  | All declared permissions; justification for each; dangerous permission review   |
| iOS      | All Info.plist entitlements; privacy usage descriptions; background mode review |
| Unity    | Plugin permission requirements; manifest modifications                          |

**Output:** Permission Risk Assessment (Minimal / Moderate / Excessive)

#### Step 6: Auditability Assessment

| Check                  | Criteria                                                              |
| ---------------------- | --------------------------------------------------------------------- |
| Source availability    | Is source code available for review? (Open source / Partial / Closed) |
| Behavioral monitoring  | Can we monitor SDK network calls at runtime?                          |
| Telemetry transparency | Does the SDK emit observable telemetry?                               |
| Reverse engineering    | Is the SDK obfuscated in ways that prevent audit?                     |

**Output:** Auditability Score (Fully Auditable / Partially Auditable / Opaque)

#### Step 7: Provider Reputation Check

| Check                 | Criteria                                                |
| --------------------- | ------------------------------------------------------- |
| Security history      | Known CVEs, breach history, public incidents            |
| CVE database          | Search NVD, GitHub Security Advisories, Snyk            |
| Community reputation  | Developer forums, Stack Overflow, Reddit sentiment      |
| Vendor responsiveness | Mean time to patch, security disclosure policy          |
| Business continuity   | Company stability, open-source alternative availability |

**Output:** Provider Reputation Score (Excellent / Good / Fair / Poor)

### SDK Vetting Report Template

```markdown
# SDK Vetting Report: [SDK Name] v[Version]

## Summary

- **Provider:** [Company]
- **Purpose:** [Why we need it]
- **Platform(s):** [Android / iOS / Unity]
- **Overall Determination:** PASS / WARNING / FAIL

## Step Results

| Step                         | Result      | Rating                                |
| ---------------------------- | ----------- | ------------------------------------- |
| 1. Identification            | ✅ Complete | —                                     |
| 2. Privacy Policy Review     | [Summary]   | [Low/Med/High/Blocker]                |
| 3. COPPA Compliance          | [Summary]   | [Compliant/Conditional/Non-Compliant] |
| 4. Network Endpoint Analysis | [Summary]   | [Pass/Warning/Fail]                   |
| 5. Permission Audit          | [Summary]   | [Minimal/Moderate/Excessive]          |
| 6. Auditability Assessment   | [Summary]   | [Full/Partial/Opaque]                 |
| 7. Provider Reputation       | [Summary]   | [Excellent/Good/Fair/Poor]            |

## Risk Summary

- **Critical Risks:** [List]
- **Mitigations:** [List]
- **Residual Risk:** [Assessment]

## Recommendation

- [ ] Approve for inclusion
- [ ] Approve with conditions: [List]
- [ ] Reject — [Reason]

**Reviewed by:** [Name, CSO Office]  
**Date:** [YYYY-MM-DD]
```

### Determination Logic

| Outcome     | Criteria                                                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **PASS**    | No High/Blocker privacy risks; COPPA Compliant or Conditional with mitigations; Network Pass; Provider Good or Excellent                                           |
| **WARNING** | Medium privacy risk with mitigations; COPPA Conditional; Network Warning or Partial auditability; Provider Fair — requires CSO sign-off and documented mitigations |
| **FAIL**    | Any Blocker privacy risk; COPPA Non-Compliant; Network Fail; Opaque auditability with high risk; Provider Poor — SDK cannot be included                            |

---

## 5. Privacy Compliance Path

### CSO Office Retained Oversight

The following privacy and compliance domains remain under **direct CSO Office oversight** until a dedicated compliance capability is established at the studio level:

| Domain                                                    | CSO Responsibility                                                            | Linked Studio Resource                        | Stage(s)   |
| --------------------------------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------- | ---------- |
| **COPPA/GDPR-K compliance assessment**                    | CSO conducts assessment; coordinates with CIO's COPPA assessment plan         | CIO COPPA Assessment Plan                     | 1, 2, 5, 8 |
| **Privacy policy authoring and review**                   | CSO drafts legal/compliance content; UX Writer adapts for player-facing copy  | UX Writer (Sarah Chen)                        | 2, 5, 8    |
| **Age gate and parental consent flow design**             | CSO reviews design for compliance; Priya Nair designs flow; Dmitri implements | Priya Nair (design), Dmitri Volkov (impl)     | 2, 5, 8    |
| **Data retention and deletion policy**                    | CSO sets requirements; David Okafor implements infrastructure                 | David Okafor (Live Ops Eng)                   | 8, 10      |
| **Penetration testing provider selection and management** | CSO selects provider, manages engagement, reviews results                     | External provider (see `pen-testing-plan.md`) | 7          |

### Compliance Gate Sign-Off

At each pipeline gate review, the CSO Office will verify:

| Gate              | Verification                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 1 Gate**  | SDK vetting complete for all proposed SDKs; COPPA assessment initiated; privacy owner assigned                                        |
| **Stage 6 Gate**  | SDK vetting re-validated for any new SDKs added during development; Cloud Script review rule enforced; privacy policy draft complete  |
| **Stage 8 Gate**  | Age gate implemented and tested; data retention policy documented; pen test completed and remediated                                  |
| **Stage 10 Gate** | All compliance requirements satisfied; privacy policy finalized; COPPA assessment signed off; release authorized for target platforms |

---

## 6. Timeline — Condition Satisfaction Milestones

### Week 1 (April 12–18, 2026)

| Day | Milestone                                                   | Owner      | Status         |
| --- | ----------------------------------------------------------- | ---------- | -------------- |
| Mon | Security Ownership Matrix drafted (this document)           | CSO Office | ✅ Complete    |
| Tue | SDK Vetting Process defined (Section 4)                     | CSO Office | ✅ Complete    |
| Wed | Pen Testing Plan drafted (see `pen-testing-plan.md`)        | CSO Office | ✅ Complete    |
| Thu | Aisha Bello Cloud Script review rule communicated to studio | CSO Office | 🟡 In Progress |
| Fri | COPPA/GDPR-K compliance assessment initiated                | CSO Office | 🟡 In Progress |

### Week 2 (April 19–25, 2026)

| Day | Milestone                                              | Owner                    | Status     |
| --- | ------------------------------------------------------ | ------------------------ | ---------- |
| Mon | First SDK vetting completed (PlayFab Core SDK)         | CSO Office + Priya Nair  | ⬜ Pending |
| Tue | Privacy policy draft v1 (CSO legal content)            | CSO Office               | ⬜ Pending |
| Wed | Age gate flow design review (Priya Nair + Dmitri)      | CSO Office               | ⬜ Pending |
| Thu | Pen testing provider shortlist finalized               | CSO Office               | ⬜ Pending |
| Fri | Cloud Script CI/CD review rule implemented in pipeline | Priya Nair + Aisha Bello | ⬜ Pending |

### Week 3 (April 26 – May 2, 2026)

| Day | Milestone                                         | Owner                     | Status     |
| --- | ------------------------------------------------- | ------------------------- | ---------- |
| Mon | Data retention/deletion requirements defined      | CSO Office + David Okafor | ⬜ Pending |
| Tue | Privacy policy player-facing copy drafted         | UX Writer (Sarah Chen)    | ⬜ Pending |
| Wed | COPPA assessment draft complete                   | CSO Office                | ⬜ Pending |
| Thu | Pen testing provider selected and budget approved | CSO Office + Studio Lead  | ⬜ Pending |
| Fri | **All C1–C5 conditions verified satisfied**       | CSO Office                | ⬜ Pending |

### Condition Satisfaction Summary

| Condition                                                                   | Document                            | Target Date | Owner                    |
| --------------------------------------------------------------------------- | ----------------------------------- | ----------- | ------------------------ |
| **C1:** Data privacy compliance ownership assigned                          | SECURITY-OWNERSHIP-MATRIX.md §2, §5 | Week 1      | CSO Office               |
| **C2:** SDK security vetting process documented and integrated into Stage 1 | SECURITY-OWNERSHIP-MATRIX.md §4     | Week 1      | CSO Office               |
| **C3:** Penetration testing provider identified and budgeted                | PEN-TESTING-PLAN.md                 | Week 3      | CSO Office               |
| **C4:** SRD explicitly assigns privacy/age gate/data retention owners       | SECURITY-OWNERSHIP-MATRIX.md §2     | Week 1      | CSO Office               |
| **C5:** Cloud Script code review enforcement                                | SECURITY-OWNERSHIP-MATRIX.md §3     | Week 2      | Priya Nair + Aisha Bello |

---

## 7. Review & Sign-Off

| Role                   | Name               | Signature | Date       |
| ---------------------- | ------------------ | --------- | ---------- |
| CSO (Author)           | Dr. Sarah Chen     |           | 2026-04-12 |
| CTO (Review)           | Dr. Kenji Nakamura |           |            |
| Studio Lead (Approval) | [Studio Lead]      |           |            |

---

_Document Classification: Internal — Security Sensitive_  
_Next Review: Upon studio compliance officer hire or Stage 6 gate review_
