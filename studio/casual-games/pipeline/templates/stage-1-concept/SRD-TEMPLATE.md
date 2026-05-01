# Security Requirements Document (SRD) — Template

> **Stage:** 1 — Concept
> **Producer:** Studio Director (Dr. Marcus Vogel) + CSO Dr. Sarah Chen (parent company)
> **Kill Gate:** KG-1 — Concept Validation
> **User Approval:** ✅ Required before advancing to Stage 2
> **Note:** Security requirements travel as a paired document with the PRD through all subsequent stages.

---

## Document Control

| Field          | Value                          |
| :------------- | :----------------------------- |
| **Game Title** | [Working title]                |
| **Version**    | v0.1 (Concept)                 |
| **Date**       | YYYY-MM-DD                     |
| **Author**     | [Studio Director]              |
| **CSO Review** | [Dr. Sarah Chen] on YYYY-MM-DD |

---

## 1. Data Classification

| Data Category                  | Sensitivity | Collected? | Stored? | Notes                      |
| :----------------------------- | :---------- | :--------: | :-----: | :------------------------- |
| Player display name            | Low         |     ☐      |    ☐    |                            |
| Device ID / advertising ID     | Medium      |     ☐      |    ☐    | GDPR/CCPA consent required |
| Purchase history               | High        |     ☐      |    ☐    | PCI DSS scope if stored    |
| Player location                | High        |     ☐      |    ☐    | Opt-in only                |
| Gameplay behaviour (analytics) | Low         |     ☐      |    ☐    | Anonymised                 |
| Social connections / friends   | Medium      |     ☐      |    ☐    |                            |
| Chat messages                  | High        |     ☐      |    ☐    | Moderation required        |

---

## 2. Authentication and Account Requirements

| Requirement                    | Selection                                                             |
| :----------------------------- | :-------------------------------------------------------------------- |
| **Account system**             | ☐ Guest (device-bound) / ☐ Social login / ☐ Email + password / ☐ None |
| **Guest-to-account migration** | ☐ Required / ☐ Not required                                           |
| **Session token expiry**       | [X hours]                                                             |
| **Multi-device sync**          | ☐ Yes / ☐ No                                                          |

---

## 3. Privacy and Compliance Requirements

| Regulation               |   Applies?   | Key Requirement                        |
| :----------------------- | :----------: | :------------------------------------- |
| GDPR (EU)                | ☐ Yes / ☐ No | Consent, right to erasure, DPA         |
| CCPA (California)        | ☐ Yes / ☐ No | Opt-out of data sale                   |
| COPPA (Under 13 / USA)   | ☐ Yes / ☐ No | Parental consent; no behavioural ads   |
| App Store privacy labels |  ✅ Always   | Apple privacy nutrition label required |
| Google Play data safety  |  ✅ Always   | Play data safety section required      |

---

## 4. Monetisation Security Requirements

| Requirement                          | Detail                                                    |
| :----------------------------------- | :-------------------------------------------------------- |
| **IAP validation**                   | Server-side receipt validation required for all purchases |
| **Receipt replay attack prevention** | Nonce or transaction ID deduplication                     |
| **Currency economy integrity**       | Server-authoritative; no client-side currency grants      |
| **Cheat/exploit prevention**         | Server-validated progression gates                        |

---

## 5. Network Security Requirements

| Requirement         | Standard                                          |
| :------------------ | :------------------------------------------------ |
| All API calls       | HTTPS only; TLS 1.2+ minimum                      |
| Certificate pinning | Required for payment endpoints                    |
| API authentication  | JWT or OAuth 2.0; no API keys in client builds    |
| Rate limiting       | Server-side rate limits on all player-facing APIs |

---

## 6. Data Retention and Deletion

| Data Type           | Retention Period                    | Deletion Method          |
| :------------------ | :---------------------------------- | :----------------------- |
| Player account data | While account is active + [X] years | Hard delete on request   |
| Analytics events    | [X] months rolling                  | Automated purge          |
| Crash reports       | [X] months                          | Automated purge          |
| Purchase records    | [X] years (tax/legal)               | Cannot delete; anonymise |

---

## 7. Security Gate Requirements (All Stages)

The following CSO security gates apply across the 11-stage pipeline:

| Gate                   | Stage | Requirement                                         |
| :--------------------- | :---: | :-------------------------------------------------- |
| SRD Review             |   1   | CSO approves this document before KG-1              |
| Asset Screening        |   3   | Third-party assets vetted for licence and malware   |
| Code Review (Security) |   5   | Security-focused code review by Lead Engineer + CSO |
| Penetration Test       |  7/8  | Full pen test before soft launch                    |
| Compliance Sign-off    |   9   | Privacy labels, GDPR/CCPA audit signed off          |
| CSO Release Sign-off   |  10   | Final CSO clearance before global launch            |

---

## 8. SRD Completeness Checklist (Kill Gate 1)

- [ ] All data categories identified and classified
- [ ] Privacy regulations determined and requirements noted
- [ ] Authentication model selected
- [ ] Monetisation security requirements defined
- [ ] Network security standards specified
- [ ] Data retention policy defined
- [ ] CSO has reviewed and approved this document

---

**Produced by:** [Studio Director] on YYYY-MM-DD
**CSO Sign-off:** [Dr. Sarah Chen] on YYYY-MM-DD — ☐ Approved / ☐ Approved with conditions / ☐ Rejected
