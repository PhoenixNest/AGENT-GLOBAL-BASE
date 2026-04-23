# Browser Support Matrix

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Web Application (P1)
**Stage:** 7 — Automated Testing

---

## Target Browsers

| Browser       | Minimum Version | Market Share | Testing Tool    | Status                                  |
| ------------- | --------------- | ------------ | --------------- | --------------------------------------- |
| Chrome        | [N]             | ~65%         | Playwright      | ☐ Not Tested / 🟡 In Progress / ✅ Pass |
| Firefox       | [N]             | ~3%          | Playwright      | ☐ Not Tested / 🟡 In Progress / ✅ Pass |
| Safari        | [N]             | ~18%         | Playwright (WK) | ☐ Not Tested / 🟡 In Progress / ✅ Pass |
| Edge          | [N]             | ~5%          | Playwright      | ☐ Not Tested / 🟡 In Progress / ✅ Pass |
| Mobile Chrome | [N]             | ~40% mobile  | Playwright      | ☐ Not Tested / 🟡 In Progress / ✅ Pass |
| Mobile Safari | [N]             | ~55% mobile  | Playwright (WK) | ☐ Not Tested / 🟡 In Progress / ✅ Pass |

## Responsive Breakpoints

| Breakpoint | Width  | Target Devices            | Status      |
| ---------- | ------ | ------------------------- | ----------- |
| Mobile     | 375px  | iPhone SE, small Android  | ☐ / 🟡 / ✅ |
| Tablet     | 768px  | iPad, Android tablets     | ☐ / 🟡 / ✅ |
| Desktop    | 1440px | Laptops, desktop monitors | ☐ / 🟡 / ✅ |
| Wide       | 1920px | Large monitors, ultrawide | ☐ / 🟡 / ✅ |

## Automated Testing Coverage

| Test Category            | Tool                         | Scenarios Covered | Pass Rate | Target |
| ------------------------ | ---------------------------- | ----------------- | --------- | ------ |
| Cross-browser E2E        | Playwright                   | [N]               | XX%       | 100%   |
| Visual regression        | Playwright + Percy/Snapshots | [N]               | XX%       | 100%   |
| Responsive layout        | Playwright (multi-viewport)  | [N]               | XX%       | 100%   |
| Accessibility (axe-core) | Playwright + axe             | [N]               | XX%       | ≥95%   |

## Known Browser-Specific Issues

| Issue               | Browser(s) Affected | Severity      | Root Cause | Remediation Plan | Target Date |
| ------------------- | ------------------- | ------------- | ---------- | ---------------- | ----------- |
| [Issue description] | [Browser]           | [P0/P1/P2/P3] | [Cause]    | [Plan]           | YYYY-MM-DD  |

## Manual Testing Checklist

| Check                     | Browser         | Status | Notes         |
| ------------------------- | --------------- | ------ | ------------- |
| Page loads without errors | All             | ☐ / ✅ |               |
| Critical user flows work  | All             | ☐ / ✅ |               |
| Responsive layout correct | All breakpoints | ☐ / ✅ |               |
| No console errors         | All             | ☐ / ✅ |               |
| Performance meets SLA     | All             | ☐ / ✅ | LCP, CLS, TTI |
| Accessibility scan passes | All             | ☐ / ✅ | axe-core ≥95% |
