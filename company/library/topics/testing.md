# Testing

Cross-cutting reference for all testing concerns: automated test suite design, defect severity classification, regression testing, and the integrity verification process. Testing spans Stages 7 and 8, with the defect severity system (P0–P3) also applying in Stage 6.

---

## Owners

| Role | Name | Department | Profile |
| --- | --- | --- | --- |
| Chief Technology Officer (CTO) | Dr. Kenji Nakamura | R&D | [`profile.md`](../../departments/research-develop/supervisor/chief-technology-officer/agent/profile.md) |
| Test Lead | Priscilla Oduya | R&D | [`profile.md`](../../departments/research-develop/team/supervisors/test-lead/agent/profile.md) |

---

## Defect Severity System (P0–P3)

Applied in Stages 6, 7, and 8. All identified defects must be classified before any remediation begins.

| Level | Definition | Release Impact |
| --- | --- | --- |
| **P0** | App crash / data loss / security breach | Blocks release — non-negotiable |
| **P1** | Core feature broken / major UX failure | Blocks release — non-negotiable |
| **P2** | Minor feature degraded / cosmetic issue | User decides to fix or defer |
| **P3** | Polish / nice-to-have | User decides to fix or defer |

**Authority rule:** P0/P1 classification is final and cannot be overridden by any party. P2/P3 defects are submitted to the user, who has explicit final authority to skip or defer them.

---

## Stage 7 — Automated Testing

**Responsible Producers:** CTO + Test Lead

### Process

1. CTO designates R&D personnel to develop test cases
2. Test Lead (Priscilla Oduya) executes the automated test suite targeting a **100% pass rate**
3. Any failing tests produce a Bug Report
4. Developers remediate bugs; testers perform **regression testing** on all affected functionalities
5. Regression must pass fully before Stage 7 closes

### Defect Handling in Stage 7

- Bugs discovered during automated testing are classified using P0–P3
- P0/P1 bugs block advancement unconditionally
- P2/P3 bugs are submitted to the user (same skip/defer authority as Stage 6)

### Gate Criteria

- [ ] 100% of test cases pass (accounting for user-approved P2/P3 deferrals)
- [ ] Regression testing on all fixed functionalities passes with no failures
- [ ] Test Results Report archived

---

## Stage 8 — Integrity Verification

**Responsible Producer:** CTO (convenes review panel)

### Purpose

Stage 8 guards against the "fixing code by trimming the product" anti-pattern — where tests are made to pass by silently removing or reducing functionality rather than fixing actual bugs.

### Review Panel

All key personnel participate: CPO, CDO, CTO, CIO, CSO, Brand Design, R&D.

### What Is Verified

The post-testing codebase is reviewed against the **full artifact set** (PRD, IDS, UML Package, SRD):

| Domain | Verification |
| --- | --- |
| Product | All PRD features remain intact |
| Design | All CDO/IDS design specifications accurately realised |
| Architecture | All UML engineering standards upheld |
| Security | All SRD security requirements remain enforced |

> Any regressions are treated as **P0/P1 defects** — functionality removal is never a valid remediation strategy.

### Gate Criteria

- [ ] No functionality reduced or removed relative to the Stage 6 Code Review baseline
- [ ] All panel members signed off
- [ ] Integrity Verification Sign-off archived

---

## Relevant Skills

| Skill File | Owner | Purpose |
| --- | --- | --- |
| [`automated-test-suite.md`](../../departments/research-develop/team/supervisors/test-lead/skills/automated-test-suite.md) | Test Lead | Automated test suite design and execution |
| [`defect-triage-and-classification.md`](../../departments/research-develop/team/supervisors/test-lead/skills/defect-triage-and-classification.md) | Test Lead | P0–P3 defect classification and triage |

---

## Reference Links

See [`reference/development/links.md`](../reference/development/links.md) for platform-specific testing documentation (Android testing, iOS XCTest, Flutter test tooling).
