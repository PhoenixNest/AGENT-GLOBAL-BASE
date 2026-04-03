# Pipeline Optimizations — Pre-Day 1 Requirements

**Document Type:** Pipeline Optimization Specifications
**Version:** 1.1 (v1.6 Recruitment Plan Alignment)
**Date:** April 3, 2026
**Owner:** CTO Office (Dr. Kenji Nakamura)
**Purpose:** Detailed specifications for all pipeline optimizations required before engineers begin work.
**Status:** ✅ Approved — Implementation Authorized

---

## Hiring Model Note

These optimizations are designed for the **staggered 3-phase hiring model** (VPs → Chapter Leads → Engineers in batches). Optimizations marked "Before Day 1" refer to **Phase 1 Day 1** (when VPs start). Optimizations dependent on Chapter Leads must be ready by **Phase 2 Day 1** (Week 4).

---

## 1. Pre-Review Gate (Stage 6 — Code Review)

**Current State:** 5-person C-suite panel (CPO, CDO, CTO, CIO, CSO) reviews all code directly.

**Post-Optimization State:** Three-tier review chain:

```
Individual Contributor → Chapter Lead (first-pass) → VP (second-pass) → C-suite Panel (final)
```

### Implementation Requirements

| Requirement                    | Owner                   | Deadline     |
| ------------------------------ | ----------------------- | ------------ |
| Chapter Lead review checklist  | CTO + All Chapter Leads | Before Day 1 |
| VP review checklist            | CTO + All VPs           | Before Day 1 |
| Panel escalation criteria      | CTO                     | Before Day 1 |
| Defect classification workflow | Priscilla + CTO         | Before Day 1 |

### Chapter Lead Review Checklist

- [ ] Code compiles without warnings
- [ ] All unit tests pass
- [ ] Code follows chapter coding standards
- [ ] No hardcoded strings (i18n gate)
- [ ] Security baseline checks pass (Security Champion review)
- [ ] Architecture compliance verified (ADR/TSD alignment)
- [ ] No P0/P1 defects introduced

### VP Review Checklist

- [ ] Chapter Lead review completed and signed off
- [ ] Cross-chapter dependencies reviewed
- [ ] Performance impact assessed
- [ ] Integration points verified
- [ ] No regressions in division-level tests

### Panel Escalation Criteria

Panel reviews code ONLY when:

- Chapter Lead or VP flags a P0/P1 concern
- Cross-division architectural dispute
- Security concern requiring CSO assessment
- Stage 6 gate sign-off (final approval)

---

## 2. Division-Level Test Ownership (Stage 7 — Automated Testing)

**Current State:** CTO + Priscilla own all testing for the entire codebase.

**Post-Optimization State:** Distributed test ownership:

| Division             | Test Owner                          | Scope                                                              |
| -------------------- | ----------------------------------- | ------------------------------------------------------------------ |
| Mobile Engineering   | VP of Mobile + Chapter Leads        | Unit, integration, E2E for Android/iOS/Cross-platform              |
| Web & Backend        | VP of Web & Backend + Chapter Leads | Unit, integration, API, performance tests                          |
| Platform Engineering | VP of Platform + DevOps Lead        | Infrastructure tests, CI/CD pipeline tests                         |
| Quality Engineering  | Priscilla + Test Automation Lead    | Integration tests, regression tests, cross-division test framework |

### Implementation Requirements

| Requirement                       | Owner                | Deadline     |
| --------------------------------- | -------------------- | ------------ |
| Division test ownership matrix    | CTO + Priscilla      | Before Day 1 |
| Test framework architecture       | Test Automation Lead | Before Day 1 |
| CI integration for division tests | DevOps Lead          | Before Day 1 |
| Regression test suite             | Priscilla            | Before Day 1 |
| 100% pass rate enforcement        | All VPs              | Ongoing      |

### Integration Testing (Priscilla-owned)

- Cross-division API contracts
- End-to-end user journeys spanning multiple divisions
- Performance benchmarks across the full application
- Regression testing on all fixed functionalities

---

## 3. Automated Regression Detection (Stage 8 — Integrity Verification)

**Current State:** Manual panel review verifies no functionality was removed during remediation.

**Post-Optimization State:** Automated CI/CD pipeline detects functionality changes:

| Detection Type           | Mechanism                           | Owner                 |
| ------------------------ | ----------------------------------- | --------------------- |
| Feature flag monitoring  | Flag registry diff on every PR      | DevOps Lead           |
| API endpoint tracking    | OpenAPI spec diff on every PR       | Backend Chapter Lead  |
| UI component auditing    | Component registry diff on every PR | Frontend Chapter Lead |
| Test coverage regression | Coverage threshold enforcement      | Test Automation Lead  |
| Resource file integrity  | String count diff on every PR       | Tomas + DevOps Lead   |

### Implementation Requirements

| Requirement                      | Owner                 | Deadline     |
| -------------------------------- | --------------------- | ------------ |
| Feature flag registry            | DevOps Lead           | Before Day 1 |
| API endpoint tracking            | Backend Chapter Lead  | Before Day 1 |
| UI component registry            | Frontend Chapter Lead | Before Day 1 |
| Coverage threshold enforcement   | Test Automation Lead  | Before Day 1 |
| Automated trim-to-pass detection | CTO + Priscilla       | Before Day 1 |

### Trim-to-Pass Detection Rules

The pipeline MUST block any PR that:

- Removes a feature flag without CPO approval
- Removes an API endpoint without PRD update
- Removes a UI component without IDS update
- Reduces test coverage below division threshold
- Removes string resources without CTO-L approval

---

## 4. CI/CD i18n Gate (Stage 9 — Internationalization)

**Current State:** Tomas manually scans for hardcoded strings during Stage 9.

**Post-Optimization State:** Automated CI/CD gate blocks any PR with hardcoded strings:

| Check                        | Mechanism                                | Platform                               |
| ---------------------------- | ---------------------------------------- | -------------------------------------- |
| Hardcoded string detection   | Lint scan on every PR                    | Android (.kt, .java), iOS (.swift, .m) |
| Format specifier validation  | Indexed specifier enforcement            | Android (%1$s), iOS (%@)               |
| String key naming compliance | Regex validation against naming standard | All platforms                          |
| Resource file completeness   | Key count diff against baseline          | strings.xml, Localizable.strings       |

### Implementation Requirements

| Requirement                   | Owner               | Deadline     |
| ----------------------------- | ------------------- | ------------ |
| Hardcoded string lint rule    | DevOps Lead + Tomas | Before Day 1 |
| Format specifier lint rule    | DevOps Lead + Tomas | Before Day 1 |
| String key naming lint rule   | DevOps Lead + Tomas | Before Day 1 |
| CI/CD gate configuration      | DevOps Lead         | Before Day 1 |
| Grace period policy (2 weeks) | CTO + Tomas         | Before Day 1 |

### Grace Period Policy

- **Weeks 1–2:** Warnings only (engineers learn the rules)
- **Week 3+:** Errors block merge (no exceptions)

---

## 5. Progress Sync Protocol Enhancement (Stage 4+)

**Current State:** CTO produces weekly progress summaries for all work.

**Post-Optimization State:** Distributed progress reporting:

```
Individual Contributors → Chapter Leads → VPs → CTO (consolidated) → CPO (if >20% over)
```

### Implementation Requirements

| Requirement                            | Owner       | Deadline |
| -------------------------------------- | ----------- | -------- |
| Division-level weekly summary template | CTO         | Week 1   |
| VP consolidation process               | CTO         | Week 1   |
| Progress Sync Protocol automation      | DevOps Lead | Week 1–2 |
| CTO → CPO notification trigger         | CTO         | Week 1–2 |

### Weekly Summary Structure (per Division)

- Milestone completion percentage
- Tasks completed this week
- Tasks planned next week
- Risks and blockers
- Schedule variance (actual vs. estimated)
- > 20% over-estimate tasks (triggers CTO → CPO notification)
- **DORA metrics:** Deployment Frequency, Lead Time for Changes, Change Failure Rate, Mean Time to Recovery
- **SPACE metrics:** Developer Satisfaction (survey), Code Review Cycle Time, Meeting Load

---

## 6. ADR Template Enforcement (Stage 3)

**Current State:** Rafael Okonkwo produces ADRs alone.

**Post-Optimization State:** Distributed ADR authorship with centralized review:

```
Chapter Leads draft ADRs → Senior Architect reviews → Rafael approves → CIO signs off
```

### ADR Triage Classification (NEW in v1.6)

| Tier                       | Description                                                                     | Sign-off Authority                   |
| -------------------------- | ------------------------------------------------------------------------------- | ------------------------------------ |
| **Architecture-Impacting** | Changes system architecture, technology selection, or cross-division interfaces | CIO sign-off required                |
| **Implementation-Detail**  | Internal design decisions within a single chapter                               | Senior Architect sign-off sufficient |
| **Informational**          | Documents existing decisions; no new decision                                   | Logged only, no sign-off             |

### Implementation Requirements

| Requirement                  | Owner            | Deadline     |
| ---------------------------- | ---------------- | ------------ |
| ADR template (standardized)  | Rafael + CIO     | Before Day 1 |
| ADR drafting guidelines      | Rafael           | Before Day 1 |
| ADR review checklist         | Senior Architect | Before Day 1 |
| ADR registry (centralized)   | Rafael           | Before Day 1 |
| TSD compliance audit process | CIO              | Before Day 1 |

### ADR Drafting Responsibility

| Domain                   | Drafted By           | Reviewed By      |
| ------------------------ | -------------------- | ---------------- |
| Mobile architecture      | Chapter Leads        | Senior Architect |
| Web/Backend architecture | Chapter Leads        | Senior Architect |
| Platform/Infrastructure  | DevOps Lead          | Senior Architect |
| Security architecture    | Security Lead        | CSO              |
| Test architecture        | Test Automation Lead | Priscilla        |

---

## 7. Security Coordination Charter

See `../security-coordination-charter/README.md`

**Note (v1.6):** The Security Coordination Charter RACI matrices are being audited to replace all "CISO" references with "CSO" or "Lead Security Engineer" as appropriate. This audit is owned by CSO + CIO and will be completed within 5 business days of plan approval.

---

## 8. Security Champions Program

### Timeline Note (Shifted from v1.0)

**Original plan:** Security Champion selection in Week 1–2.
**Updated plan:** Security Champion selection in **Phase 2, Week 1–2** (after Chapter Leads ramp). This aligns with the staggered hiring model — Security Champions are drawn from Chapter teams that don't exist until Phase 2.

**Pre-Phase 2 Security Coverage:** CSO + first Security Engineer hire conduct all PR security reviews manually during Phase 1.

### Structure

Each Chapter Lead designates one Security Champion from their team:

| Chapter        | Security Champion              | Responsibilities                          |
| -------------- | ------------------------------ | ----------------------------------------- |
| Android        | TBD (from Android team)        | PR security review, MASVS self-assessment |
| iOS            | TBD (from iOS team)            | PR security review, MASVS self-assessment |
| Cross-Platform | TBD (from Cross-Platform team) | PR security review, MASVS self-assessment |
| Frontend       | TBD (from Frontend team)       | PR security review, XSS/CSP checks        |
| Backend        | TBD (from Backend team)        | PR security review, API security checks   |
| DevOps         | TBD (from DevOps team)         | Pipeline security, supply chain checks    |

### Implementation Requirements

| Requirement                    | Owner         | Deadline                                      |
| ------------------------------ | ------------- | --------------------------------------------- |
| Security Champion selection    | Chapter Leads | **Phase 2, Week 1–2** (shifted from Week 1–2) |
| Security Champion training     | CSO + CISO    | **Phase 2, Week 1–2**                         |
| PR security review checklist   | CSO           | **Phase 2, Week 2–3**                         |
| MASVS self-assessment template | CSO           | **Phase 2, Week 2–3**                         |

---

## 9. String Key Naming Standard

See `../string-key-naming-standard/README.md`

---

## 10. Cross-Platform String Parity Audit

### Purpose

Ensure the same string exists in Android, iOS, and cross-platform resource files with matching keys and semantics.

### Implementation Requirements

| Requirement                        | Owner               | Deadline     |
| ---------------------------------- | ------------------- | ------------ |
| key-index.csv template             | Tomas               | Before Day 1 |
| Cross-platform parity check script | Tomas + DevOps Lead | Before Day 1 |
| Parity audit in Stage 9 handoff    | Tomas               | Before Day 1 |

### key-index.csv Structure

```
key,android_resource,ios_resource,cross_platform_resource,character_limit,context,platforms
```

**Note (v1.6):** The parity check will be automated — generated from resource files at build time, not manually maintained. Assigned to DevOps Lead + Tomas.

---

## 11. Technical Debt Allocation (NEW in v1.6)

Per Waydev 2026: _"Allocate 15–20% of each sprint to debt reduction and track it visibly on roadmaps. 2026 context: 80% of technical debt will be architectural."_

| Practice                      | Implementation                                                                             |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| **Sprint capacity reserve**   | Every sprint reserves 15–20% capacity for technical debt reduction                         |
| **Dedicated debt backlog**    | Tracked separately from feature work; visible in all sprint planning                       |
| **ADR remediation timelines** | ADRs that introduce architectural debt must include a remediation timeline and review date |
| **Debt metrics**              | Tracked via DORA Change Failure Rate and code churn metrics                                |

---

## 12. Async-First Workflows (NEW in v1.6)

Per Waydev 2026: _"Cut meetings by 40–60% to protect deep work. Document decisions like code, enforce response SLAs, and mandate daily 4-hour meeting-free focus blocks."_

| Practice                      | Implementation                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------------ |
| **4-hour daily focus blocks** | No meetings 9am–1pm or 1pm–5pm (team decides)                                                    |
| **Async panel reviews**       | Panel members submit written feedback before synchronous decision meeting                        |
| **Response SLAs**             | 24h operational (PR reviews, defect triage); 72h strategic (ADR reviews, architecture decisions) |
| **Documentation-as-code**     | All decisions documented in ADRs; PRs require written rationale                                  |

---

## 13. Knowledge Democratization & Bus Factor Audit (NEW in v1.6)

Per Waydev 2026: _"Combat critical knowledge silos (typically a 'bus factor' of 1–2) by treating documentation as version-controlled, reviewed code. Target a bus factor of 5+ for all critical systems."_

| Practice                       | Implementation                                                           |
| ------------------------------ | ------------------------------------------------------------------------ |
| **Bus factor audit (Stage 8)** | Each critical system must have 5+ engineers who can operate it           |
| **Documentation-as-code**      | ADRs, TSDs, runbooks require PR + review like any code change            |
| **Cross-training mandate**     | Each Chapter runs monthly knowledge-sharing sessions; attendance tracked |
| **Target**                     | Bus factor ≥ 5 for all critical systems by end of FY2026 Q2              |

---

## 14. Security Scaling Roadmap (NEW in v1.6)

Per NeonTri 2025 Cybersecurity Investment Roadmap:

| Headcount                 | Security Investment                                             | Key Metric                             |
| ------------------------- | --------------------------------------------------------------- | -------------------------------------- |
| 1–50 (current)            | SAST/DAST in CI/CD; 1 security engineer; secure coding training | Time to patch critical vulnerabilities |
| 50–150 (end of FY2026 Q2) | 2–3 person SecOps team; bug bounty; vendor security reviews     | % of assets with vulnerability scans   |
| 150–500+ (future)         | 24/7 SOC; quarterly red/blue team; automated compliance         | MTTD & MTTR                            |

**Action:** By end of FY2026 Q2, hire **2 additional Security Engineers** (total 3) to form SecOps team. Evaluate bug bounty program and vendor security review process.

---

## Optimization Priority Summary

| Priority            | Optimizations                                                                                                               | Deadline                          |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| **Critical (4)**    | Pre-Review Gate, Division Test Ownership, Automated Regression Detection, CI/CD i18n Gate                                   | Before Day 1                      |
| **High (6)**        | Progress Sync (+ DORA/SPACE), ADR Enforcement (+ Triage), Security Charter, Security Champions, String Naming, Parity Audit | Before Day 1 or Week 1–2          |
| **High (2, NEW)**   | Technical Debt Allocation (15–20%), Async-First Workflows                                                                   | Stage 4 (Gantt) / Week 1          |
| **Medium (2, NEW)** | Bus Factor Audit (Stage 8), Security Scaling Roadmap                                                                        | Stage 8 design / End of FY2026 Q2 |
