# Stage 7/8 Integration

## Stage 7/8 Integration

### Stage 7 — Automated Testing Integration

Visual regression tests are part of the automated test suite executed in Stage 7.

| Stage 7 Requirement  | Visual Regression Contribution                                   |
| -------------------- | ---------------------------------------------------------------- |
| Test Suite execution | Visual regression tests run alongside unit/integration/e2e tests |
| Defect detection     | Visual diffs classified as P0-P3 defects                         |
| Results reporting    | Visual diff report included in TEST-RESULTS-REPORT.md            |
| 100% pass target     | Visual tests must pass (zero unauthorized diffs)                 |

**Visual Regression Defect Classification:**

| Visual Defect                           | Severity | Rationale                    |
| --------------------------------------- | -------- | ---------------------------- |
| Screen completely broken (blank/crash)  | P0       | Core feature non-functional  |
| Major layout broken, content unreadable | P1       | Major UX failure             |
| Minor element misalignment (5-10px)     | P2       | Cosmetic issue, user decides |
| Color shade difference (imperceptible)  | P3       | Polish issue, user decides   |
| Text truncation in RTL layout           | P1       | Core accessibility failure   |
| Button too small on specific device     | P2       | Minor UX degradation         |

**Stage 7 Visual Regression Report Format:**

```markdown
# Visual Regression Report — Stage 7
```
