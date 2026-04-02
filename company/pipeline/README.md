# Pipeline

This directory contains the company's development workflow definitions.

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
