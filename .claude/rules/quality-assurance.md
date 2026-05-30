---
description: Testing/QA patterns, defect classification, and quality standards — invoke manually when writing tests or conducting reviews
---

# Quality Assurance

Testing and QA guidance. See `.claude/skills/quality-assurance/` for deep sub-skills.

---

## Defect Severity Classification

| Severity          | Definition                                                  | Response           | Fix Timeline    |
| ----------------- | ----------------------------------------------------------- | ------------------ | --------------- |
| **P0 — Critical** | Crash, data loss, security breach, complete feature failure | Immediate (1 hour) | Same day        |
| **P1 — High**     | Core feature broken, major flow impaired                    | Within 4 hours     | Within 24 hours |
| **P2 — Medium**   | Non-critical broken, workaround exists                      | 1 business day     | 1 week          |
| **P3 — Low**      | Minor issues, typos, polish                                 | 1 week             | Next sprint     |

**P0/P1 classification is non-overridable by any agent.**

---

## Test Pyramid

```
         /\
        /E2E\        10% — End-to-End
       /------\
      /Integr- \     20% — Integration
     /----------\
    /   Unit     \   70% — Unit
   /--------------\
```

**Coverage target:** 80%+ for business logic

---

## Testing Frameworks

| Platform | Unit          | UI/E2E              |
| -------- | ------------- | ------------------- |
| Android  | JUnit + MockK | Espresso, Maestro   |
| iOS      | XCTest        | XCUITest            |
| Web      | Vitest / Jest | Playwright, Cypress |
| Backend  | pytest / Jest | Supertest, httpx    |

---

## Code Review Checklist

- [ ] All tests pass
- [ ] Code coverage ≥ 80%
- [ ] No linting errors
- [ ] No security vulnerabilities
- [ ] Performance benchmarks met
- [ ] Documentation updated

---

## Release Checklist

- [ ] All P0/P1 defects resolved
- [ ] Regression testing complete
- [ ] Performance testing complete
- [ ] Security scan complete
- [ ] Accessibility audit complete (WCAG 2.1 AA)
