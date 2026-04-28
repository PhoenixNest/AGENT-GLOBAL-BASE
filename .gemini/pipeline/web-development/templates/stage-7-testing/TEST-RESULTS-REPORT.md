# Test Results Report

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Web Application (P1)
**Stage:** 7 — Automated Testing

---

## 1. Test Summary

| Category                 | Total   | Passed  | Failed  | Skipped | Pass Rate |
| ------------------------ | ------- | ------- | ------- | ------- | --------- |
| Unit (Frontend)          | [N]     | [N]     | [N]     | [N]     | [XX]%     |
| Unit (Backend)           | [N]     | [N]     | [N]     | [N]     | [XX]%     |
| Integration              | [N]     | [N]     | [N]     | [N]     | [XX]%     |
| E2E (Playwright)         | [N]     | [N]     | [N]     | [N]     | [XX]%     |
| API Contract (Pact)      | [N]     | [N]     | [N]     | [N]     | [XX]%     |
| Performance (Lighthouse) | [N]     | [N]     | [N]     | [N]     | [XX]%     |
| Accessibility (axe-core) | [N]     | [N]     | [N]     | [N]     | [XX]%     |
| Security (ZAP DAST)      | [N]     | [N]     | [N]     | [N]     | [XX]%     |
| **Total**                | **[N]** | **[N]** | **[N]** | **[N]** | **[XX]%** |

---

## 2. Frontend Unit Tests

| Framework    | Tests | Pass | Fail | Skip | Coverage (Branch) | Coverage (Line) |
| ------------ | ----- | ---- | ---- | ---- | ----------------- | --------------- |
| Vitest + RTL | [N]   | [N]  | [N]  | [N]  | [XX]%             | [XX]%           |

**Target:** ≥80% branch, ≥90% line

---

## 3. Backend Unit Tests

| Framework   | Tests | Pass | Fail | Skip | Coverage (Branch) | Coverage (Line) |
| ----------- | ----- | ---- | ---- | ---- | ----------------- | --------------- |
| Vitest/Jest | [N]   | [N]  | [N]  | [N]  | [XX]%             | [XX]%           |

**Target:** ≥80% branch, ≥90% line

---

## 4. E2E Tests (Playwright)

| Browser         | Tests | Pass | Fail | Skip | Duration |
| --------------- | ----- | ---- | ---- | ---- | -------- |
| Chrome          | [N]   | [N]  | [N]  | [N]  | [X min]  |
| Firefox         | [N]   | [N]  | [N]  | [N]  | [X min]  |
| Safari (WebKit) | [N]   | [N]  | [N]  | [N]  | [X min]  |

### Critical User Flows

| Flow                       | Chrome          | Firefox         | Safari          | Notes |
| -------------------------- | --------------- | --------------- | --------------- | ----- |
| Login → Dashboard → Logout | ☐ Pass / ☐ Fail | ☐ Pass / ☐ Fail | ☐ Pass / ☐ Fail |       |
| [Core feature flow]        | ☐ Pass / ☐ Fail | ☐ Pass / ☐ Fail | ☐ Pass / ☐ Fail |       |
| [Checkout/payment flow]    | ☐ Pass / ☐ Fail | ☐ Pass / ☐ Fail | ☐ Pass / ☐ Fail |       |

---

## 5. API Contract Tests (Pact)

| Consumer       | Provider      | Tests | Pass | Fail | Coverage        |
| -------------- | ------------- | ----- | ---- | ---- | --------------- |
| [Web Frontend] | [Backend API] | [N]   | [N]  | [N]  | [XX]% endpoints |

**Target:** 100% endpoint coverage

---

## 6. Performance Tests

| Metric | PRD Target | Result  | Pass/Fail       |
| ------ | ---------- | ------- | --------------- |
| LCP    | <2.5s      | [X.XXs] | ☐ Pass / ☐ Fail |
| CLS    | <0.1       | [X.XX]  | ☐ Pass / ☐ Fail |
| TTFB   | <800ms     | [Xms]   | ☐ Pass / ☐ Fail |
| TTI    | <3.8s      | [X.XXs] | ☐ Pass / ☐ Fail |

---

## 7. Accessibility Tests

| Tool                       | Tests        | Pass | Fail | Skip | Pass Rate |
| -------------------------- | ------------ | ---- | ---- | ---- | --------- |
| axe-core (automated)       | [N]          | [N]  | [N]  | [N]  | [XX]%     |
| Manual audit (WCAG 2.1 AA) | [N criteria] | [N]  | [N]  | [N]  | [XX]%     |

**Target:** ≥95% pass rate

---

## 8. Security Tests (DAST — OWASP ZAP)

| Category                  | Findings | Critical | High | Medium | Low |
| ------------------------- | -------- | -------- | ---- | ------ | --- |
| XSS                       | [N]      | [N]      | [N]  | [N]    | [N] |
| CSRF                      | [N]      | [N]      | [N]  | [N]    | [N] |
| SQL Injection             | [N]      | [N]      | [N]  | [N]    | [N] |
| Broken Authentication     | [N]      | [N]      | [N]  | [N]    | [N] |
| Security Misconfiguration | [N]      | [N]      | [N]  | [N]    | [N] |

**Target:** Zero critical/high findings

---

## 9. Regression Tests

| Feature        | Previously Defective | Re-tested       | Pass/Fail | Notes   |
| -------------- | -------------------- | --------------- | --------- | ------- |
| [Feature name] | [Defect ID]          | ☐ Pass / ☐ Fail |           | [Notes] |

**Target:** All Stage 6+ fixed functionalities verified

---

## 10. Design Fidelity Test Checklist

| IDS Section | Requirement                                       | Browser | Pass/Fail       | Notes |
| ----------- | ------------------------------------------------- | ------- | --------------- | ----- |
| IDS §1      | Responsive breakpoints (375px, 768px, 1440px)     | All     | ☐ Pass / ☐ Fail |       |
| IDS §2      | Typography scale and font families                | All     | ☐ Pass / ☐ Fail |       |
| IDS §3      | Color tokens and contrast ratios                  | All     | ☐ Pass / ☐ Fail |       |
| IDS §4      | Component states (hover, focus, active, disabled) | All     | ☐ Pass / ☐ Fail |       |
| IDS §5      | Animation specs (duration, easing)                | All     | ☐ Pass / ☐ Fail |       |
| IDS §6      | Accessibility (screen reader, keyboard nav)       | All     | ☐ Pass / ☐ Fail |       |

---

## 11. Defect Summary

| Severity | New | Open | Resolved |
| -------- | --- | ---- | -------- |
| P0       | [N] | [N]  | [N]      |
| P1       | [N] | [N]  | [N]      |
| P2       | [N] | [N]  | [N]      |
| P3       | [N] | [N]  | [N]      |

---

## 12. Sign-Off

| Criterion                             | Status          | Notes   |
| ------------------------------------- | --------------- | ------- |
| 100% automated test pass rate         | ☐ Pass / ☐ Fail | [Notes] |
| DAST passed (zero critical/high)      | ☐ Pass / ☐ Fail | [Notes] |
| Performance benchmarks passed         | ☐ Pass / ☐ Fail | [Notes] |
| Accessibility audit passed (≥95%)     | ☐ Pass / ☐ Fail | [Notes] |
| API contract tests passed (100%)      | ☐ Pass / ☐ Fail | [Notes] |
| E2E tests passed (all critical flows) | ☐ Pass / ☐ Fail | [Notes] |
| Design Fidelity Test Checklist passed | ☐ Pass / ☐ Fail | [Notes] |
| Regression tests passed               | ☐ Pass / ☐ Fail | [Notes] |

**Test Lead Sign-off:** [Name] — YYYY-MM-DD
**CTO Sign-off:** [Name] — YYYY-MM-DD
