# Defect Report

**Project:** [Project Name]
**Stage:** 6 — Code Review
**Version:** v1
**Date:** YYYY-MM-DD
**Reviewed By:** CTO Panel (CPO, CDO, CTO, CIO, CSO) + Platform Leads (Tier 1)

---

## Executive Summary

| Metric              | Value |
| ------------------- | ----- |
| Total defects found | [N]   |
| P0 (non-negotiable) | [N]   |
| P1 (non-negotiable) | [N]   |
| P2 (user decides)   | [N]   |
| P3 (user decides)   | [N]   |
| Review rounds       | [N]   |
| Sign-offs received  | [X/5] |

---

## Pre-Tier 1 Automated Quality Gates

**These gates MUST pass before Tier 1 cross-review begins.** If any gate fails, Tier 1 is blocked.

| Gate            | Tool                 | Result                | Failure Details          | Status          |
| --------------- | -------------------- | --------------------- | ------------------------ | --------------- |
| SAST            | Semgrep + CodeQL     | [N findings]          | [Critical/High findings] | ☐ Pass / ☐ Fail |
| Secret scanning | gitleaks             | [N secrets found]     | [Details]                | ☐ Pass / ☐ Fail |
| Dependency scan | Snyk / Dependabot    | [N vulnerabilities]   | [Critical/High CVEs]     | ☐ Pass / ☐ Fail |
| Linting         | Detekt / SwiftLint   | [N violations]        | [Details]                | ☐ Pass / ☐ Fail |
| Unit tests      | Platform test runner | [N passed / N failed] | [Failed tests]           | ☐ Pass / ☐ Fail |

**Gate Result:** ☐ All gates passed — Tier 1 may proceed / ☐ Gates failed — remediate before Tier 1

---

## Defect Details

### P0 — Critical

| ID     | Category                  | PRD Feature | Description   | Location      | Remediation    | Status            |
| ------ | ------------------------- | ----------- | ------------- | ------------- | -------------- | ----------------- |
| P0-001 | [Security / Crash / Data] | [REQ-NNN]   | [Description] | [File/module] | [Fix approach] | ☐ Open / ✅ Fixed |

### P1 — Major

| ID     | Category            | PRD Feature | Description   | Location      | Remediation    | Status            |
| ------ | ------------------- | ----------- | ------------- | ------------- | -------------- | ----------------- |
| P1-001 | [Core Feature / UX] | [REQ-NNN]   | [Description] | [File/module] | [Fix approach] | ☐ Open / ✅ Fixed |

### P2 — Minor (User Decision)

| ID     | Category           | PRD Feature | Description   | Location      | Remediation    | User Decision   | Status            |
| ------ | ------------------ | ----------- | ------------- | ------------- | -------------- | --------------- | ----------------- |
| P2-001 | [Cosmetic / Minor] | [REQ-NNN]   | [Description] | [File/module] | [Fix approach] | ☐ Fix / ☐ Defer | ☐ Open / ✅ Fixed |

### P3 — Polish (User Decision)

| ID     | Category | PRD Feature | Description   | Location      | Remediation    | User Decision   | Status            |
| ------ | -------- | ----------- | ------------- | ------------- | -------------- | --------------- | ----------------- |
| P3-001 | [Polish] | [REQ-NNN]   | [Description] | [File/module] | [Fix approach] | ☐ Fix / ☐ Defer | ☐ Open / ✅ Fixed |

---

## Platform Lead Tier 1 Review Memo

Each Platform Lead produces a written cross-review memo covering code quality, architecture conformance, and security observations.

### Android Lead → iOS Code Review

| Aspect                       | Assessment                           | Details                 |
| ---------------------------- | ------------------------------------ | ----------------------- |
| **Code quality**             | [Excellent / Good / Needs Work]      | [Specific observations] |
| **Architecture conformance** | [Matches UML/ADR / Deviations noted] | [List deviations]       |
| **Security observations**    | [Findings]                           | [File-level references] |
| **Test quality**             | [Adequate / Gaps noted]              | [Missing test areas]    |
| **Key findings**             | [Top 3 concerns]                     | [Details]               |

**Sign-off:** ☐ Approved / ☐ Approved with conditions / ☐ Rejected
**Conditions:** [List any]

### iOS Lead → Android Code Review

| Aspect                       | Assessment                           | Details                 |
| ---------------------------- | ------------------------------------ | ----------------------- |
| **Code quality**             | [Excellent / Good / Needs Work]      | [Specific observations] |
| **Architecture conformance** | [Matches UML/ADR / Deviations noted] | [List deviations]       |
| **Security observations**    | [Findings]                           | [File-level references] |
| **Test quality**             | [Adequate / Gaps noted]              | [Missing test areas]    |
| **Key findings**             | [Top 3 concerns]                     | [Details]               |

**Sign-off:** ☐ Approved / ☐ Approved with conditions / ☐ Rejected
**Conditions:** [List any]

### Cross-Platform Lead → Shared Module Review (KMP/Flutter only)

| Aspect                         | Assessment                       | Details                                  |
| ------------------------------ | -------------------------------- | ---------------------------------------- |
| **Shared module code quality** | [Excellent / Good / Needs Work]  | [Specific observations]                  |
| **API contract compliance**    | [Contract verified / Deviations] | [Reference Contract Verification Report] |
| **Security observations**      | [Findings]                       | [File-level references]                  |
| **Platform adapter quality**   | [Adequate / Gaps noted]          | [Details]                                |
| **Key findings**               | [Top 3 concerns]                 | [Details]                                |

**Sign-off:** ☐ Approved / ☐ Approved with conditions / ☐ Rejected
**Conditions:** [List any]

---

## Architecture Compliance Audit (Layer 2 — ADR/TSD Enforcement)

**Auditor:** Senior Architect (Dr. Elena Rostova)
**Date:** YYYY-MM-DD
**Scope:** Independent audit of codebase against all Stage 3 ADRs and TSD

### ADR Compliance Audit

| ADR                              | Compliant?   | Deviations Found | Defect IDs | Notes |
| -------------------------------- | ------------ | ---------------- | ---------- | ----- |
| ADR-NNN (Platform Strategy)      | ☐ Yes / ☐ No | [N]              | [P#-XXX]   |       |
| ADR-NNN (String Key Taxonomy)    | ☐ Yes / ☐ No | [N]              | [P#-XXX]   |       |
| ADR-NNN (Security: Cryptography) | ☐ Yes / ☐ No | [N]              | [P#-XXX]   |       |
| ADR-NNN (Security: Storage)      | ☐ Yes / ☐ No | [N]              | [P#-XXX]   |       |
| ADR-NNN (Security: Pinning)      | ☐ Yes / ☐ No | [N]              | [P#-XXX]   |       |
| ADR-NNN (Security: Platform)     | ☐ Yes / ☐ No | [N]              | [P#-XXX]   |       |
| TSD vN                           | ☐ Yes / ☐ No | [N]              | [P#-XXX]   |       |

**Audit Result:** ☐ Pass / ☐ Fail — [N] ADR deviations found
**Signed by Senior Architect (Dr. Elena Rostova) on YYYY-MM-DD**

---

## IDS Conformance Matrix

Row-by-row mapping of every IDS specification item to its implementation status. Completed by CDO during Stage 6 Code Review.

### Component Conformance

| IDS Section | IDS Item                     | Implemented? | Fidelity Rating       | Deviation Notes          | Defect ID (if any) |
| ----------- | ---------------------------- | ------------ | --------------------- | ------------------------ | ------------------ |
| IDS §3.1    | [Screen name] component tree | ☐ Yes / ☐ No | Exact / Minor / Major | [Describe any deviation] | [P#-XXX or None]   |
| IDS §3.2    | [Screen name] component tree | ☐ Yes / ☐ No | Exact / Minor / Major | [Describe any deviation] | [P#-XXX or None]   |

### Gesture Conformance

| IDS Section | Gesture             | Target | Implemented? | Matches Spec? | Deviation Notes        | Defect ID (if any) |
| ----------- | ------------------- | ------ | ------------ | ------------- | ---------------------- | ------------------ |
| IDS §5      | [e.g., Swipe right] | [Card] | ☐ Yes / ☐ No | ☐ Yes / ☐ No  | [e.g., Distance wrong] | [P#-XXX or None]   |

### State Conformance

| IDS Section | State Flow          | All States Present? | All Transitions Working? | Defect ID (if any) |
| ----------- | ------------------- | ------------------- | ------------------------ | ------------------ |
| IDS §6.1    | [Feature/flow name] | ☐ Yes / ☐ No        | ☐ Yes / ☐ No             | [P#-XXX or None]   |

### Edge Case Conformance

| IDS Section | Edge Case  | Platform | Implemented? | Matches Spec? | Defect ID (if any) |
| ----------- | ---------- | -------- | ------------ | ------------- | ------------------ |
| IDS §7      | No network | Android  | ☐ Yes / ☐ No | ☐ Yes / ☐ No  | [P#-XXX or None]   |
| IDS §7      | No network | iOS      | ☐ Yes / ☐ No | ☐ Yes / ☐ No  | [P#-XXX or None]   |

### Accessibility Conformance

| IDS Section | A11y Requirement     | Platform | Implemented? | Meets WCAG 2.1 AA? | Defect ID (if any) |
| ----------- | -------------------- | -------- | ------------ | ------------------ | ------------------ |
| IDS §10.1   | Screen reader labels | iOS      | ☐ Yes / ☐ No | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §10.1   | Screen reader labels | Android  | ☐ Yes / ☐ No | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §10.2   | Touch targets        | Android  | ☐ Yes / ☐ No | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §10.2   | Touch targets        | iOS      | ☐ Yes / ☐ No | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §10.3   | Contrast ratios      | Both     | ☐ Yes / ☐ No | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §10.4   | Focus order          | Both     | ☐ Yes / ☐ No | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §10.5   | Dynamic type (200%)  | iOS      | ☐ Yes / ☐ No | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §10.5   | Dynamic type (200%)  | Android  | ☐ Yes / ☐ No | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §10.6   | Reduced motion       | Both     | ☐ Yes / ☐ No | ☐ Yes / ☐ No       | [P#-XXX or None]   |

### Visual Specifications Conformance

| IDS Section | Screen   | Spec Item     | Expected Value    | Actual Value | Fidelity Rating       | Defect ID (if any) |
| ----------- | -------- | ------------- | ----------------- | ------------ | --------------------- | ------------------ |
| IDS §4.1    | [Screen] | Background    | [Token/hex]       | [Value]      | Exact / Minor / Major | [P#-XXX or None]   |
| IDS §4.1    | [Screen] | Typography    | [Type ramp]       | [Value]      | Exact / Minor / Major | [P#-XXX or None]   |
| IDS §4.1    | [Screen] | Spacing       | [8dp grid]        | [Value]      | Exact / Minor / Major | [P#-XXX or None]   |
| IDS §4.1    | [Screen] | Corner radius | [Component token] | [Value]      | Exact / Minor / Major | [P#-XXX or None]   |
| IDS §4.1    | [Screen] | Elevation     | [Elevation token] | [Value]      | Exact / Minor / Major | [P#-XXX or None]   |

### Design Tokens Conformance

| IDS Section | Token            | Expected (Android)   | Expected (iOS)     | Applied Correctly? | Defect ID (if any) |
| ----------- | ---------------- | -------------------- | ------------------ | ------------------ | ------------------ |
| IDS §9      | color.primary    | @color/primary       | AssetColor.primary | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §9      | spacing.md       | 16dp                 | 16pt               | ☐ Yes / ☐ No       | [P#-XXX or None]   |
| IDS §9      | typography.body1 | TextAppearance.Body1 | UIFont.body        | ☐ Yes / ☐ No       | [P#-XXX or None]   |

### Platform Conventions Conformance

| IDS Section | Convention         | Platform | Expected            | Matches?     | Defect ID (if any) |
| ----------- | ------------------ | -------- | ------------------- | ------------ | ------------------ |
| IDS §2      | Navigation pattern | iOS      | [HIG pattern]       | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §2      | Navigation pattern | Android  | [MD3 pattern]       | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §2      | Transition style   | iOS      | [Push/Modal/Sheet]  | ☐ Yes / ☐ No | [P#-XXX or None]   |
| IDS §2      | Transition style   | Android  | [Slide/Shared/Fade] | ☐ Yes / ☐ No | [P#-XXX or None]   |

### Animation Conformance

| IDS Section | Animation           | Duration Matches? | Easing Matches? | Trigger Matches? | Defect ID (if any) |
| ----------- | ------------------- | ----------------- | --------------- | ---------------- | ------------------ |
| IDS §8      | [Screen transition] | ☐ Yes / ☐ No      | ☐ Yes / ☐ No    | ☐ Yes / ☐ No     | [P#-XXX or None]   |

### Conformance Summary

| Category              | Total Items | Exact Match | Minor Deviation | Major Deviation | Not Implemented | Conformance % |
| --------------------- | ----------- | ----------- | --------------- | --------------- | --------------- | ------------- |
| Components            | [N]         | [N]         | [N]             | [N]             | [N]             | [XX]%         |
| Gestures              | [N]         | [N]         | [N]             | [N]             | [N]             | [XX]%         |
| States                | [N]         | [N]         | [N]             | [N]             | [N]             | [XX]%         |
| Edge Cases            | [N]         | [N]         | [N]             | [N]             | [N]             | [XX]%         |
| Accessibility         | [N]         | [N]         | [N]             | [N]             | [N]             | [XX]%         |
| Animations            | [N]         | [N]         | [N]             | [N]             | [N]             | [XX]%         |
| Visual Specifications | [N]         | [N]         | [N]             | [N]             | [N]             | [XX]%         |
| Design Tokens         | [N]         | [N]         | [N]             | [N]             | [N]             | [XX]%         |
| Platform Conventions  | [N]         | [N]         | [N]             | [N]             | [N]             | [XX]%         |
| **Overall**           | **[N]**     | **[N]**     | **[N]**         | **[N]**         | **[N]**         | **[XX]%**     |

**Overall conformance ≥ 95% required for CDO sign-off.** Any "Major Deviation" or "Not Implemented" item is automatically classified as at least **P1** (P0 if it blocks a core user flow).

---

## C-Suite Panel Sign-Off

| Role | Name                | Sign-off     | Date |
| ---- | ------------------- | ------------ | ---- |
| CPO  | Marcus Tran-Yoshida | ☐ Yes / ☐ No |      |
| CDO  | Yuki Tanaka-Chen    | ☐ Yes / ☐ No |      |
| CTO  | Dr. Kenji Nakamura  | ☐ Yes / ☐ No |      |
| CIO  | Dr. Priya Mehta     | ☐ Yes / ☐ No |      |
| CSO  | Dr. Sarah Chen      | ☐ Yes / ☐ No |      |

---

**All P0 and P1 defects must be resolved before advancement.**
**User has made decisions on all P2/P3 defects.**
**Remediation completed and re-review passed on YYYY-MM-DD**
