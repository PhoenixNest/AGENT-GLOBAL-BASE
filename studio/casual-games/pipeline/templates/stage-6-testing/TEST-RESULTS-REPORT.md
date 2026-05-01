# Test Results Report — Template

> **Stage:** 6 — Automated Testing
> **Producer:** SDET Gameplay (Lead QA Engineer)
> **User Approval:** ✅ Required before advancing to Stage 7

---

## Document Control

| Field             | Value                    |
| :---------------- | :----------------------- |
| **Game Title**    | [Working title]          |
| **Build Version** | [vX.X.X]                 |
| **Test Period**   | YYYY-MM-DD to YYYY-MM-DD |
| **Author**        | [Lead QA Engineer]       |

---

## 1. Executive Summary

| Metric               | Target | Actual | Status          |
| :------------------- | :----: | :----: | :-------------- |
| Overall pass rate    |  100%  |  [X]%  | ☐ Pass / ☐ Fail |
| Total tests executed |  [N]   |  [N]   | —               |
| Total tests passed   |  [N]   |  [N]   | —               |
| Total tests failed   |   0    |  [N]   | ☐ Pass / ☐ Fail |
| P0 defects open      |   0    |  [N]   | ☐ Pass / ☐ Fail |
| P1 defects open      |   0    |  [N]   | ☐ Pass / ☐ Fail |

---

## 2. Test Results by Category

| Category              | Planned | Executed | Passed | Failed | Pass Rate |
| :-------------------- | :-----: | :------: | :----: | :----: | :-------: |
| Unit tests            |   [N]   |   [N]    |  [N]   |  [N]   |   [X]%    |
| Integration tests     |   [N]   |   [N]    |  [N]   |  [N]   |   [X]%    |
| UI / gameplay tests   |   [N]   |   [N]    |  [N]   |  [N]   |   [X]%    |
| Performance tests     |   [N]   |   [N]    |  [N]   |  [N]   |   [X]%    |
| Security tests (SAST) |   [N]   |   [N]    |  [N]   |  [N]   |   [X]%    |

---

## 3. Performance Results

| Metric                   |  Target  | Result  | Device   | Pass? |
| :----------------------- | :------: | :-----: | :------- | :---: |
| Cold start               |  < [X]s  |  [X]s   | [Device] |   ☐   |
| Steady-state FPS         | ≥ 30 fps | [X] fps | [Device] |   ☐   |
| Peak memory              | < [X] MB | [X] MB  | [Device] |   ☐   |
| Battery drain per 10 min |  < [X]%  |  [X]%   | [Device] |   ☐   |
| Network payload          | < [X] KB | [X] KB  | —        |   ☐   |

---

## 4. Security Test Results

| Test Type           | Findings      |  Severity  | Status              |
| :------------------ | :------------ | :--------: | :------------------ |
| SAST scan           | [N findings]  | [Severity] | ☐ Resolved / ☐ Open |
| IAP validation      | [Pass / Fail] |     —      | ☐                   |
| Economy integrity   | [Pass / Fail] |     —      | ☐                   |
| DAST high findings  | [N]           |    High    | ☐ Resolved / ☐ Open |
| Certificate pinning | [Pass / Fail] |     —      | ☐                   |

---

## 5. Defect Log

| ID    | Description   | Severity | Status              | Resolution   |
| :---- | :------------ | :------: | :------------------ | :----------- |
| D-001 | [Description] |   P[N]   | ☐ Open / ☐ Resolved | [Resolution] |
| D-002 | [Description] |   P[N]   | ☐ Open / ☐ Resolved | [Resolution] |

**P0 defects (must be zero to advance):** [N]
**P1 defects (must be zero to advance):** [N]
**P2/P3 defects (deferred by User decision):** [N]

---

## 6. Device Matrix Results

| Device            | OS          | Pass Rate | Critical Issues |
| :---------------- | :---------- | :-------: | :-------------- |
| [Low-end iOS]     | iOS [X]     |   [X]%    | [None / Issue]  |
| [Mid iOS]         | iOS [X]     |   [X]%    | [None / Issue]  |
| [Low-end Android] | Android [X] |   [X]%    | [None / Issue]  |
| [Mid Android]     | Android [X] |   [X]%    | [None / Issue]  |

---

## 7. Stage 6 Gate Decision

| Criterion                         | Status            |
| :-------------------------------- | :---------------- |
| 100% pass rate                    | ☐ Met / ☐ Not met |
| Zero P0 defects                   | ☐ Met / ☐ Not met |
| Zero P1 defects                   | ☐ Met / ☐ Not met |
| All performance benchmarks passed | ☐ Met / ☐ Not met |
| Zero DAST high findings           | ☐ Met / ☐ Not met |

**SDET Recommendation:** ☐ Advance to Stage 7 / ☐ Remediate and re-test

---

**Produced by:** [Lead QA Engineer] on YYYY-MM-DD
**Reviewed by:** [Studio Director] on YYYY-MM-DD
