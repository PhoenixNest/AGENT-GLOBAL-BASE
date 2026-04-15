# Defect Report

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Web Application (P1)
**Stage:** 6 — Code Review

---

## 1. Review Summary

| Field                | Value                                                           |
| -------------------- | --------------------------------------------------------------- |
| **Web Strategy**     | [SSR / CSR / PWA / Hybrid]                                      |
| **Review date**      | YYYY-MM-DD                                                      |
| **Reviewers**        | CTO (convenes), CPO, CDO, CIO, CSO, Frontend Lead, Backend Lead |
| **Tier 1 reviewers** | Frontend Lead (Amira Voss), Backend Lead (Dev Malhotra)         |

### Defect Counts

| Severity | Found | Fixed | Open (blocking) | Open (deferred) |
| -------- | ----- | ----- | --------------- | --------------- |
| P0       | [N]   | [N]   | [N]             | [N]             |
| P1       | [N]   | [N]   | [N]             | [N]             |
| P2       | [N]   | [N]   | [N]             | [N]             |
| P3       | [N]   | [N]   | [N]             | [N]             |

---

## 2. Three-Layer Defense Results

### Layer 1: Platform Lead Attestation

| Lead                        | Attestation                   | Findings   |
| --------------------------- | ----------------------------- | ---------- |
| Frontend Lead (Amira Voss)  | ☐ Confirmed / ☐ Not confirmed | [Findings] |
| Backend Lead (Dev Malhotra) | ☐ Confirmed / ☐ Not confirmed | [Findings] |

### Layer 2: Architecture Compliance Audit

| Auditor           | Date       | Findings   |
| ----------------- | ---------- | ---------- |
| Dr. Elena Rostova | YYYY-MM-DD | [Findings] |

### Layer 3: CI/CD Gates

| Gate                               | Status          | Details   |
| ---------------------------------- | --------------- | --------- |
| Dependency version pinning         | ☐ Pass / ☐ Fail | [Details] |
| Prohibited technology detection    | ☐ Pass / ☐ Fail | [Details] |
| Security ADR compliance (CSP, XSS) | ☐ Pass / ☐ Fail | [Details] |

---

## 3. Live Demonstration Results

| Check                            | Browser | Result          | Notes       |
| -------------------------------- | ------- | --------------- | ----------- |
| Application loads without errors | Chrome  | ☐ Pass / ☐ Fail |             |
| Application loads without errors | Firefox | ☐ Pass / ☐ Fail |             |
| Application loads without errors | Safari  | ☐ Pass / ☐ Fail |             |
| Critical user flows functional   | All     | ☐ Pass / ☐ Fail |             |
| Responsive layout at 375px       | Chrome  | ☐ Pass / ☐ Fail |             |
| Responsive layout at 768px       | Chrome  | ☐ Pass / ☐ Fail |             |
| Responsive layout at 1440px      | Chrome  | ☐ Pass / ☐ Fail |             |
| Lighthouse performance score     | Chrome  | [XX]/100        | Target: ≥90 |

---

## 4. IDS Conformance Matrix

| IDS Section | Requirement                                                       | Browser | Conformance  | Defect ID (if any) |
| ----------- | ----------------------------------------------------------------- | ------- | ------------ | ------------------ |
| IDS §1      | Responsive breakpoints (375px, 768px, 1440px)                     | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §2      | Navigation pattern matches spec                                   | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §3      | Component states (default, hover, focus, active, disabled)        | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §4      | Visual specs (colors, typography, spacing, border-radius)         | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §5      | Gesture/interaction conventions (click, hover, keyboard)          | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §6      | State diagrams (all transitions)                                  | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §7      | Edge case UIs (no network, empty state, error, permission denied) | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §8      | Animation specs (duration, easing, interruptibility)              | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §9      | Design tokens correctly applied                                   | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §10     | Accessibility (screen reader, focus, contrast, keyboard)          | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §11     | Internationalization (text expansion, RTL if applicable)          | All     | ☐ Yes / ☐ No | [P#-XXX or None]   |

**Overall IDS Conformance:** [XX]% — Target: ≥95%

---

## 5. Architecture Compliance Audit Findings

| Finding   | Severity    | ADR Reference | Description   | Remediation   | Assigned To | Target Date |
| --------- | ----------- | ------------- | ------------- | ------------- | ----------- | ----------- |
| [Finding] | P0/P1/P2/P3 | ADR-XXX       | [Description] | [Remediation] | [Name]      | YYYY-MM-DD  |

---

## 6. Defect List

| Defect ID | Severity | Category                    | Description   | Location      | Status                          | Assigned To |
| --------- | -------- | --------------------------- | ------------- | ------------- | ------------------------------- | ----------- |
| P0-001    | P0       | [Security/Performance/etc.] | [Description] | [File/screen] | ☐ Open / ✅ Fixed               | [Name]      |
| P1-001    | P1       | [UX/Functionality]          | [Description] | [File/screen] | ☐ Open / ✅ Fixed               | [Name]      |
| P2-001    | P2       | [Cosmetic/Minor]            | [Description] | [File/screen] | ☐ Open / ✅ Fixed / ⏭ Deferred | [Name]      |
| P3-001    | P3       | [Polish]                    | [Description] | [File/screen] | ☐ Open / ✅ Fixed / ⏭ Deferred | [Name]      |

---

## 7. Automated Quality Gates

| Gate                              | Status          | Details                |
| --------------------------------- | --------------- | ---------------------- |
| ESLint (zero blocking violations) | ☐ Pass / ☐ Fail | [N violations]         |
| TypeScript (zero type errors)     | ☐ Pass / ☐ Fail | [N errors]             |
| Vitest unit tests (≥80% branch)   | ☐ Pass / ☐ Fail | [XX]% branch coverage  |
| Playwright component tests        | ☐ Pass / ☐ Fail | [N] passed, [N] failed |

---

## 8. User Decisions on P2/P3 Defects

| Defect ID | Severity | Description   | User Decision    | Notes   |
| --------- | -------- | ------------- | ---------------- | ------- |
| P2-001    | P2       | [Description] | ☐ Fix / ⏭ Defer | [Notes] |
| P3-001    | P3       | [Description] | ☐ Fix / ⏭ Defer | [Notes] |

---

## 9. Sign-Off

| Panel Member   | Sign-off                                | Date       | Notes |
| -------------- | --------------------------------------- | ---------- | ----- |
| CTO (convenes) | ☐ Approved / ☐ Conditional / ☐ Rejected | YYYY-MM-DD |       |
| CPO            | ☐ Approved / ☐ Conditional / ☐ Rejected | YYYY-MM-DD |       |
| CDO            | ☐ Approved / ☐ Conditional / ☐ Rejected | YYYY-MM-DD |       |
| CIO            | ☐ Approved / ☐ Conditional / ☐ Rejected | YYYY-MM-DD |       |
| CSO            | ☐ Approved / ☐ Conditional / ☐ Rejected | YYYY-MM-DD |       |
| Frontend Lead  | ☐ Approved / ☐ Conditional / ☐ Rejected | YYYY-MM-DD |       |
| Backend Lead   | ☐ Approved / ☐ Conditional / ☐ Rejected | YYYY-MM-DD |       |
