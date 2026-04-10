# Pipeline

This directory contains the company's development workflow and operational pipeline definitions.

## Development Pipeline

> **File:** `development/pipeline.md`

A ten-stage state machine governing the full lifecycle of a mobile product from requirements to release. Each stage follows a consistent schema with explicit Artifacts In/Out, a Responsible Producer, Gate Criteria, and (where applicable) Defect Handling.

### Stage Summary

| #   | Stage                                                      | Key Output                                                   | Responsible Producer |
| --- | ---------------------------------------------------------- | ------------------------------------------------------------ | -------------------- |
| 1   | Requirements → PRD + SRD                                   | PRD, Security Requirements Document                          | CPO, CSO             |
| 2   | PRD → Web Prototype + IDS                                  | Web prototype (HTML), Interaction Design Specification (IDS) | CDO                  |
| 3   | Prototype → UML Engineering Package                        | UML diagrams, ADRs, Technology Selection Document (TSD)      | CTO, CIO             |
| 4   | UML → Coding Implementation Plan                           | Implementation Plan, Gantt Chart                             | CTO                  |
| 5   | Plan → Software Development                                | Development codebase                                         | CTO                  |
| 6   | Development → Code Review                                  | Defect Report, Code Review Sign-off                          | CTO (panel)          |
| 7   | Code Review → Automated Testing                            | Automated Test Suite, Test Results Report                    | CTO                  |
| 8   | Testing → Integrity Verification                           | Integrity Verification Sign-off                              | CTO (panel)          |
| 9   | Integrity Verification → Internationalization Engineering  | Localised codebase, Translation Verification Report          | CTO-L                |
| 10  | Internationalization Engineering → Release Readiness Check | Release Readiness Report, Release Decision                   | CTO (panel) + User   |

### Key Conventions

- **Defect Severity:** P0 (crash/security) and P1 (core feature broken) block release unconditionally. P2/P3 deferrals require explicit user decision.
- **Progress Sync Protocol:** Active from Stage 4. Any task exceeding estimated duration by >20% triggers CTO → CPO notification.
- **Paired Artifacts:** The PRD and SRD are archived together at Stage 1 and travel as a unit through all subsequent stages.
- **Translation:** All translation work is governed by the Language Translation Module owned by the CTO-L (Chief Translation Officer).

---

## Recruitment Pipeline

> **File:** `recruitment/pipeline.md`

A nine-stage, **fully automated** talent acquisition system. Chief Officers configure competency bars, compensation bands, assessment parameters, and sourcing channels **once per quarter**. The system executes autonomously — zero manual intervention at Stages 1–8. Leadership reviews a single **HIRING OUTCOME REPORT** at Stage 9.

#### Key Design Principles

| Principle                   | Description                                                                                                                                              |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Elite talent bar**        | Non-negotiable: all candidates must score >= 4 on >= 4 of 5 vetting dimensions, pass Red Flag Scan, and exceed 80th percentile on role-family competency |
| **Full automation**         | No manual approval gates at Stages 1–8. Only R0/R1 defects trigger human escalation                                                                      |
| **Quarterly configuration** | Chief Officers set parameters once per quarter. Changes take effect next quarter                                                                         |
| **Top-tier benchmarking**   | Practices from Google, Apple, Meta, Stripe, Netflix encoded into automation rules                                                                        |
| **Outcome-only review**     | Single HIRING OUTCOME REPORT at Stage 9 for leadership approval                                                                                          |

#### Automated Stage Summary

| #   | Stage                              | Automated By                       | Leadership Involvement                  |
| --- | ---------------------------------- | ---------------------------------- | --------------------------------------- |
| 1   | Role Intake                        | System (rule engine)               | None                                    |
| 2   | Sourcing & Pipeline                | Sourcing Agent Network             | None                                    |
| 3   | Screening & Assessment Assign      | System (competency matching)       | None                                    |
| 4   | Interview Simulation               | AI Panel + Automated Scoring       | None                                    |
| 5   | Elite Vetting Gate                 | System (5-dimension auto-score)    | None                                    |
| 6   | Background Verification            | Background Check Service           | None                                    |
| 7   | Offer Generation                   | Compensation band engine           | None                                    |
| 8   | **Hiring Outcome Report**          | System compiles → **User reviews** | **User approves/rejects**               |
| 9   | **Onboarding → 90-Day Checkpoint** | System (G2/G3/G4 automation)       | Begins ONLY after Stage 8 user approval |

#### Key Conventions

- **Tiered Urgency:** Tier 1 (Critical, 2–3 weeks), Tier 2 (Growth, 4–6 weeks), Tier 3 (Exploratory, 8–12 weeks).
- **Defect Severity:** R0 (compliance breach/security) and R1 (core process failure) are non-negotiable. R2/R3 decided by CHRO.
- **Security Gates:** G0 (Role Clearance), G1 (Identity & Background), G2 (NDA Execution), G3 (Access Provisioning), G4 (90-Day Security Posture).
- **Progress Monitoring:** Active from Stage 2. Any stage exceeding SLA by >20% triggers CHRO → Department Head notification.
- **Feedback Loop:** Post-Recruitment Retrospective feeds directly into Stage 1 improvements for continuous process optimization.

#### Pipeline Status

> **Status:** 🔴 NOT APPROVED for production use
> **Deficiency Report:** [`recruitment/DEFICIENCY-REPORT.md`](recruitment/DEFICIENCY-REPORT.md)
> **Findings:** 34 deficiencies (12 critical, 14 high, 8 medium) across 4 domains
> **Next Review:** Pending 5-phase remediation (~7 weeks to production readiness)

---

## Progress Monitoring & Recovery System

> **File:** `development/monitoring.md`

A three-layer monitoring system providing comprehensive oversight of pipeline progress, enabling rapid state assessment and seamless recovery after interruptions (e.g., power outages, session timeouts, agent handoffs).

**Mandatory for all Stage 4+ projects.**

### System Components

| Layer | Component     | Purpose                     | Location                                       |
| ----- | ------------- | --------------------------- | ---------------------------------------------- |
| 1     | `PROGRESS.md` | Real-time pipeline state    | `company/project/<project>/PROGRESS.md`        |
| 2     | Session Logs  | Detailed audit trail        | `company/project/<project>/sessions/*.md`      |
| 3     | Checkpoints   | Machine-readable milestones | `company/project/<project>/checkpoints/*.json` |

### Recovery Protocol

After any interruption:

1. Read `PROGRESS.md` → Identify current stage and last milestone
2. Read latest session log → Understand what was in progress
3. Read latest checkpoint JSON → Get exact resume point
4. Resume from documented position → No restart needed

**Full specification:** [`monitoring.md`](development/monitoring.md)
