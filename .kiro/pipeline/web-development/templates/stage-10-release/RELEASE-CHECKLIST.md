# Release Checklist

**Project:** [Project Name]
**Version:** v1.0.0
**Date:** YYYY-MM-DD
**Pipeline:** Web Application (P1)
**Stage:** 10 — Release Readiness

---

## 1. Release Summary

| Field | Value |
| ----- | ----- |
| **Release version** | [v1.0.0] |
| **Release date** | [YYYY-MM-DD] |
| **Deployment target** | Production (Vercel + AWS/Render) |
| **Release type** | [Major / Minor / Patch] |
| **Rollback plan** | [Vercel instant rollback / Git revert + redeploy] |

---

## 2. Release Readiness Items

| #   | Domain           | Criteria                                                | Sign-off Authority | Status          | Notes         |
| --- | ---------------- | ------------------------------------------------------- | ------------------ | --------------- | ------------- |
| 1   | **Product**      | All PRD requirements implemented                        | CPO                | ☐ Pass / ☐ Fail | See below     |
| 2   | **Design**       | All CDO/IDS specifications accurately realised          | CDO                | ☐ Pass / ☐ Fail | See below     |
| 3   | **Architecture** | All UML/ADR/TSD standards upheld                        | CTO + CIO          | ☐ Pass / ☐ Fail | See below     |
| 4   | **Security**     | SRD enforced, web security controls effective           | CSO                | ☐ Pass / ☐ Fail | See below     |
| 5   | **Testing**      | 100% automated test pass rate achieved                  | CTO                | ☐ Pass / ☐ Fail | See below     |
| 6   | **Localisation** | All target languages complete                           | CTO-L              | ☐ Pass / ☐ Fail | See below     |
| 7   | **Deployment**   | Vercel/AWS deployment verified, CDN live, DNS pointing  | CTO + CPO          | ☐ Pass / ☐ Fail | See below     |

---

## 3. Sub-Checklists

### 3.1 Product (CPO)

| Item | Status | Notes |
| ---- | ------ | ----- |
| Analytics firing on all tracked events | ☐ Yes / ☐ No | |
| IAP/monetization configured (if applicable) | ☐ Yes / ☐ No | |
| Kill condition monitoring active | ☐ Yes / ☐ No | |
| Post-launch dashboard configured | ☐ Yes / ☐ No | |
| User onboarding flow tested end-to-end | ☐ Yes / ☐ No | |

### 3.2 Design (CDO)

| Item | Status | Notes |
| ---- | ------ | ----- |
| IDS Conformance Matrix ≥ 95% | ☐ Yes / ☐ No | |
| Zero "Not Implemented" items | ☐ Yes / ☐ No | |
| WCAG 2.1 AA met (≥95% pass rate) | ☐ Yes / ☐ No | |
| Responsive breakpoints respected (375px, 768px, 1440px) | ☐ Yes / ☐ No | |
| Design tokens correctly applied | ☐ Yes / ☐ No | |
| Animation specs matched | ☐ Yes / ☐ No | |

### 3.3 Architecture (CTO + CIO)

| Item | Status | Notes |
| ---- | ------ | ----- |
| Technology Decision Registry 100% compliant | ☐ Yes / ☐ No | |
| No ADR deviations | ☐ Yes / ☐ No | |
| All dependencies pinned and audited | ☐ Yes / ☐ No | |
| CI/CD pipeline passing on main branch | ☐ Yes / ☐ No | |

### 3.4 Security (CSO)

| Item | Status | Notes |
| ---- | ------ | ----- |
| CSP headers present and correct on all pages | ☐ Yes / ☐ No | |
| XSS prevention verified (ZAP DAST clean) | ☐ Yes / ☐ No | |
| CSRF protection active on all state-changing endpoints | ☐ Yes / ☐ No | |
| Secure cookies configured (HttpOnly, Secure, SameSite) | ☐ Yes / ☐ No | |
| OAuth 2.0 session integrity verified | ☐ Yes / ☐ No | |
| Dependency audit clean (no critical/high CVEs) | ☐ Yes / ☐ No | |
| Stealthy weakening verified absent | ☐ Yes / ☐ No | |

### 3.5 Testing (CTO)

| Item | Status | Notes |
| ---- | ------ | ----- |
| 100% automated test pass rate | ☐ Yes / ☐ No | |
| DAST (OWASP ZAP) passed | ☐ Yes / ☐ No | |
| Performance benchmarks passed (LCP/CLS/TTFB/TTI) | ☐ Yes / ☐ No | |
| Accessibility audit passed (WCAG 2.1 AA ≥95%) | ☐ Yes / ☐ No | |
| Design Fidelity Test Checklist passed | ☐ Yes / ☐ No | |
| Regression tests passed | ☐ Yes / ☐ No | |

### 3.6 Localisation (CTO-L)

| Item | Status | Notes |
| ---- | ------ | ----- |
| BLEU ≥ 0.80 for all target languages | ☐ Yes / ☐ No | |
| Accessibility labels localized | ☐ Yes / ☐ No | |
| Commercial copy localized | ☐ Yes / ☐ No | |
| Locale variants distinct (FR-FR vs FR-CA, etc.) | ☐ Yes / ☐ No | |
| Placeholder integrity verified | ☐ Yes / ☐ No | |
| Text expansion handled (no UI overflow) | ☐ Yes / ☐ No | |

### 3.7 Deployment (CTO + CPO)

| Item | Status | Notes |
| ---- | ------ | ----- |
| Vercel production deployment verified | ☐ Yes / ☐ No | |
| CDN configured and propagating | ☐ Yes / ☐ No | |
| DNS pointing to production | ☐ Yes / ☐ No | |
| SSL certificate valid and auto-renewing | ☐ Yes / ☐ No | |
| Analytics firing on production | ☐ Yes / ☐ No | |
| SEO validated (meta tags, structured data, sitemap) | ☐ Yes / ☐ No | |
| Monitoring dashboards live (Sentry, Vercel Analytics) | ☐ Yes / ☐ No | |
| Error tracking alerts configured | ☐ Yes / ☐ No | |
| Rollback plan tested | ☐ Yes / ☐ No | |

---

## 4. Release Decision

| Role | Decision | Signature | Date |
| ---- | -------- | --------- | ---- |
| CTO | ☐ Approve / ☐ Conditional / ☐ Reject | | YYYY-MM-DD |
| CPO | ☐ Approve / ☐ Conditional / ☐ Reject | | YYYY-MM-DD |
| CDO | ☐ Approve / ☐ Conditional / ☐ Reject | | YYYY-MM-DD |
| CSO | ☐ Approve / ☐ Conditional / ☐ Reject | | YYYY-MM-DD |
| CTO-L | ☐ Approve / ☐ Conditional / ☐ Reject | | YYYY-MM-DD |
| **User** | **☐ Approve / ☐ Conditional / ☐ Reject** | | **YYYY-MM-DD** |

---

## 5. Post-Release Actions

| Action | Owner | Target Date | Status |
| ------ | ----- | ----------- | ------ |
| Monitor error rates for 24 hours | [Name] | YYYY-MM-DD | ☐ Done |
| Review analytics dashboard | [Name] | YYYY-MM-DD | ☐ Done |
| Collect user feedback | [Name] | YYYY-MM-DD | ☐ Done |
| Retrospective scheduled | [Name] | YYYY-MM-DD | ☐ Done |
