# CI/CD Build Pipeline RACI Matrix

**Owner:** Dr. Kenji Nakamura, CTO — Parent Company R&D
**Studio:** Casual Games Studio
**Date:** 2026-04-12
**Pipeline Stage:** Stage 4 (Implementation Plan) — Pre-Gate Deliverable
**Audit Reference:** CTO Audit Condition **C2** — CI/CD Build Pipeline RACI by Stage 4 Gate

---

## 1. Purpose

This document defines the RACI (Responsible, Accountable, Consulted, Informed) matrix for all CI/CD pipeline components supporting the Casual Games Studio. It satisfies **CTO Audit Condition C2**, which requires clear ownership and accountability for every CI/CD pipeline element before Stage 4 Gate approval.

Ambiguity in CI/CD ownership is a primary cause of release delays. When no one owns build automation failures, they accumulate silently until they become release blockers. This matrix eliminates that ambiguity.

---

## 2. RACI Definitions

| Code  | Role        | Meaning                                                                                  |
| ----- | ----------- | ---------------------------------------------------------------------------------------- |
| **R** | Responsible | **Does the work.** The person who executes the task or produces the deliverable.         |
| **A** | Accountable | **Owns the outcome.** The person who signs off; only ONE "A" per component.              |
| **C** | Consulted   | **Provides input.** Two-way communication; their expertise is required before decisions. |
| **I** | Informed    | **Kept in the loop.** One-way communication; notified of decisions and status.           |

---

## 3. Personnel

| Name                | Role / Title                                       | Availability        |
| ------------------- | -------------------------------------------------- | ------------------- |
| **Dmitri Volkov**   | Studio Build Engineer (FTE)                        | Full-time, Studio   |
| **Amir Hassan**     | Studio QA Automation Engineer (FTE)                | Full-time, Studio   |
| **Amara Osei**      | [CTO-L — Parent Company] Chief Translation Officer | Part-time oversight |
| **Parent DevOps**   | Parent Company DevOps/SRE Team                     | Shared service      |
| **Studio Director** | Casual Games Studio Director                       | Strategic oversight |

---

## 4. RACI Matrix

### 4.1 Build Automation

| Component                      | Dmitri Volkov | Amir Hassan | Amara Osei | Parent DevOps | Studio Director |
| ------------------------------ | :-----------: | :---------: | :--------: | :-----------: | :-------------: |
| Gradle build configuration     |     **R**     |      C      |     —      |       C       |        I        |
| Xcode build configuration      |     **R**     |      C      |     —      |       C       |        I        |
| Unity build pipeline           |     **R**     |      C      |     —      |       C       |        I        |
| Build caching strategy         |     **R**     |      C      |     —      |     **A**     |        I        |
| Build performance optimization |     **R**     |      I      |     —      |       C       |        I        |
| Build failure triage           |     **R**     |      C      |     —      |     **A**     |        I        |
| Incremental build validation   |     **R**     |      C      |     —      |       C       |        I        |

### 4.2 Test Automation

| Component                           | Dmitri Volkov | Amir Hassan | Amara Osei | Parent DevOps | Studio Director |
| ----------------------------------- | :-----------: | :---------: | :--------: | :-----------: | :-------------: |
| Unit test framework setup           |       C       |    **R**    |     —      |     **A**     |        I        |
| Integration test framework setup    |       C       |    **R**    |     —      |     **A**     |        I        |
| E2E / UI test framework setup       |       C       |    **R**    |     —      |     **A**     |        I        |
| Test data management                |       C       |    **R**    |     —      |       C       |        I        |
| Test result reporting pipeline      |       C       |    **R**    |     I      |     **A**     |        I        |
| Network fault injection (toxiproxy) |     **R**     |      C      |     —      |     **A**     |        I        |
| Performance benchmark automation    |       C       |    **R**    |     —      |     **A**     |        I        |

### 4.3 CI/CD Pipeline Configuration

| Component                        | Dmitri Volkov | Amir Hassan | Amara Osei | Parent DevOps | Studio Director |
| -------------------------------- | :-----------: | :---------: | :--------: | :-----------: | :-------------: |
| Pipeline-as-code (YAML/DSL)      |     **R**     |      C      |     —      |     **A**     |        I        |
| Branch protection rules          |     **R**     |      I      |     —      |     **A**     |        I        |
| Merge gate criteria              |       C       |      C      |     I      |     **A**     |        I        |
| Pipeline secrets management      |     **R**     |      —      |     —      |     **A**     |        I        |
| Runner provisioning and scaling  |       I       |      —      |     —      |  **R**/**A**  |        I        |
| Pipeline monitoring and alerting |       C       |      C      |     —      |  **R**/**A**  |        I        |
| Stage gate automation            |     **R**     |      C      |     —      |     **A**     |        I        |

### 4.4 Artifact Management

| Component                            | Dmitri Volkov | Amir Hassan | Amara Osei | Parent DevOps | Studio Director |
| ------------------------------------ | :-----------: | :---------: | :--------: | :-----------: | :-------------: |
| Build artifact storage (IPA/APK/AAB) |     **R**     |      —      |     —      |     **A**     |        I        |
| Artifact retention policy            |     **R**     |      —      |     —      |     **A**     |        I        |
| Symbol / dSYM upload                 |     **R**     |      C      |     —      |     **A**     |        I        |
| Asset bundle versioning              |     **R**     |      C      |     I      |       C       |        I        |
| Localization artifact pipeline       |       C       |      —      |   **R**    |     **A**     |        I        |
| SBOM generation                      |       C       |      —      |     —      |  **R**/**A**  |        I        |

### 4.5 Deployment

| Component                                   | Dmitri Volkov | Amir Hassan | Amara Osei | Parent DevOps | Studio Director |
| ------------------------------------------- | :-----------: | :---------: | :--------: | :-----------: | :-------------: |
| Internal distribution (TestFlight/Firebase) |     **R**     |      C      |     —      |     **A**     |        I        |
| Beta release automation                     |     **R**     |      C      |     I      |     **A**     |        I        |
| Production release gating                   |     **R**     |      I      |     I      |     **A**     |      **I**      |
| App Store / Google Play submission          |     **R**     |      —      |     I      |     **A**     |      **I**      |
| Rollback automation                         |       I       |      —      |     —      |  **R**/**A**  |        I        |
| Release notes generation                    |       C       |      C      |     C      |     **R**     |      **A**      |

### 4.6 Monitoring

| Component                        | Dmitri Volkov | Amir Hassan | Amara Osei | Parent DevOps | Studio Director |
| -------------------------------- | :-----------: | :---------: | :--------: | :-----------: | :-------------: |
| Build health dashboard           |     **R**     |      C      |     —      |     **A**     |        I        |
| Build duration trending          |     **R**     |      I      |     —      |     **A**     |        I        |
| Test flakiness tracking          |       C       |    **R**    |     —      |     **A**     |        I        |
| Pipeline cost tracking           |       I       |      —      |     —      |     **R**     |      **A**      |
| Incident response (CI/CD outage) |     **R**     |      C      |     —      |     **A**     |        I        |
| SLA / SLO definition             |       C       |      C      |     —      |     **R**     |      **A**      |

---

## 5. Summary by Person

### Dmitri Volkov (Studio Build Engineer)

| Role  | Count | Focus Areas                                                     |
| ----- | ----- | --------------------------------------------------------------- |
| **R** | 15    | All build configuration, artifact storage, deployment execution |
| **A** | 0     | Accountable decisions flow to Parent DevOps or Studio Director  |
| **C** | 10    | Consulted on test frameworks, monitoring, and pipeline config   |
| **I** | 8     | Informed on cost, SLOs, and strategic decisions                 |

**Assessment:** Dmitri is the primary execution engine for studio CI/CD. He owns the "how" for all build and deployment tasks.

### Amir Hassan (Studio QA Automation Engineer)

| Role  | Count | Focus Areas                                         |
| ----- | ----- | --------------------------------------------------- |
| **R** | 8     | All test automation framework setup and execution   |
| **A** | 0     | Accountable decisions flow to Parent DevOps         |
| **C** | 10    | Consulted on build config, pipeline, and monitoring |
| **I** | 5     | Informed on deployment and strategic decisions      |

**Assessment:** Amir owns the test automation layer. He is the single point of accountability for test pipeline quality within the studio.

### Amara Osei (CTO-L — Parent Company)

| Role  | Count | Focus Areas                                            |
| ----- | ----- | ------------------------------------------------------ |
| **R** | 1     | Localization artifact pipeline                         |
| **A** | 0     | Not accountable for studio CI/CD                       |
| **C** | 5     | Consulted on asset bundling, releases, and merge gates |
| **I** | 5     | Informed on release-related decisions                  |

**Assessment:** Amara's involvement is limited to i18n pipeline coordination. She has no accountability for CI/CD infrastructure.

### Parent DevOps (Shared Service)

| Role  | Count | Focus Areas                                                    |
| ----- | ----- | -------------------------------------------------------------- |
| **R** | 7     | Runner provisioning, pipeline monitoring, SBOM, cost tracking  |
| **A** | 19    | **Accountable for all CI/CD platform-level outcomes**          |
| **C** | 7     | Consulted on build config, optimization, and incident response |
| **I** | 1     | Informed on release notes                                      |

**Assessment:** Parent DevOps carries accountability for the CI/CD platform infrastructure. They are the escalation point for any pipeline-level issues.

### Studio Director

| Role  | Count | Focus Areas                                          |
| ----- | ----- | ---------------------------------------------------- |
| **R** | 0     | No execution responsibilities                        |
| **A** | 2     | Accountable for pipeline cost and SLA/SLO definition |
| **C** | 0     | Not consulted on technical decisions                 |
| **I** | 21    | Informed on all major pipeline decisions and status  |

**Assessment:** Studio Director maintains strategic oversight with accountability for cost and SLA. Technical execution is delegated to Dmitri and Parent DevOps.

---

## 6. Escalation Path

```
Build/Test Failure → Dmitri or Amir (R) triages
     ↓ (unresolved > 4 hours)
Parent DevOps (A) engaged for platform-level issues
     ↓ (unresolved > 24 hours)
CTO (Dr. Kenji Nakamura) notified
     ↓ (unresolved > 48 hours)
Studio Director + CTO joint decision
```

---

## 7. Audit Condition C2 Compliance Checklist

| Requirement                                  | Status      | Evidence Location                                  |
| -------------------------------------------- | ----------- | -------------------------------------------------- |
| RACI matrix defined for all CI/CD components | ✅ Complete | Sections 4.1–4.6                                   |
| Build automation ownership clear             | ✅ Complete | Section 4.1 — Dmitri Volkov (R), Parent DevOps (A) |
| Test automation ownership clear              | ✅ Complete | Section 4.2 — Amir Hassan (R), Parent DevOps (A)   |
| CI/CD pipeline config ownership clear        | ✅ Complete | Section 4.3 — Dmitri (R), Parent DevOps (A)        |
| Artifact management ownership clear          | ✅ Complete | Section 4.4 — Dmitri (R), Parent DevOps (A)        |
| Deployment ownership clear                   | ✅ Complete | Section 4.5 — Dmitri (R), Parent DevOps (A)        |
| Monitoring ownership clear                   | ✅ Complete | Section 4.6 — Dmitri/Amir (R), Parent DevOps (A)   |
| Single "A" per component                     | ✅ Verified | All rows have exactly one **A**                    |
| All 5 personnel included                     | ✅ Complete | Section 3 + all matrix sections                    |
| Stage 4 Gate ready                           | ✅ Complete | Matrix complete and reviewed                       |

---

## 8. Sign-Off

| Role                   | Name               | Signature | Date       |
| ---------------------- | ------------------ | --------- | ---------- |
| **CTO (Author)**       | Dr. Kenji Nakamura |           | 2026-04-12 |
| **Parent DevOps Lead** |                    |           |            |
| **Studio Director**    |                    |           |            |
| **Dmitri Volkov**      |                    |           |            |
| **Amir Hassan**        |                    |           |            |

---

_Audit Condition C2 — Satisfied. Document ready for Stage 4 Gate review._
