---
name: company-pipeline
description: Complete 10-stage development pipeline reference for the simulated mobile product company. Use when working on any pipeline stage, understanding gate criteria, defect handling, artifact flow, or pipeline rules. Trigger when user mentions pipeline stages, PRD, SRD, UML, SPEC, code review, testing, integrity verification, localization, release readiness, or asks about the development workflow.
---

# Company Development Pipeline

This skill governs the 10-stage development pipeline for the simulated mobile product company.

## Pipeline Overview

The pipeline is a **state machine** — each stage has explicit Artifacts In/Out, a Responsible Producer, Gate Criteria, and Defect Handling. Stages must be completed in order; gate criteria must be satisfied before advancing.

## 10-Stage Summary

| #   | Stage                               | Key Output                                                                              | Responsible Producer                          |
| --- | ----------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------- |
| 1   | Requirements → PRD + SRD            | Product Requirements Document, Security Requirements Document                           | CPO (PRD), CSO (SRD)                          |
| 2   | PRD → Web Prototype + IDS           | Web prototype (single HTML file), Interaction Design Specification                      | CDO                                           |
| 3   | Prototype → UML Engineering Package | UML diagrams, Architecture Decision Records (ADRs), Technology Selection Document (TSD) | CTO (UML), CIO (ADRs + TSD)                   |
| 4   | UML → Coding Implementation Plan    | Implementation Plan, Gantt Chart                                                        | CTO                                           |
| 5   | Plan → Software Development         | Development codebase                                                                    | CTO                                           |
| 6   | Development → Code Review           | Defect Report, Code Review Sign-off                                                     | CTO (panel: CPO, CDO, CTO, CIO, CSO)          |
| 7   | Code Review → Automated Testing     | Automated Test Suite, Test Results Report                                               | CTO + Test Lead                               |
| 8   | Testing → Integrity Verification    | Integrity Verification Sign-off                                                         | CTO (panel: all C-suite + Brand Design + R&D) |
| 9   | Integrity → i18n Engineering        | Localised codebase, Translation Verification Report                                     | CTO-L + R&D                                   |
| 10  | i18n → Release Readiness Check      | Release Readiness Report, Release Decision                                              | CTO (panel) + User                            |

## Non-Negotiable Rules

1. **Pipeline stages are sequential** — gate criteria must be satisfied before advancing
2. **PRD + SRD are paired** — they travel together through all stages
3. **Technology decisions lock at Stage 3** — ADRs/TSD from Stage 3 are not revisable in Stage 4+
4. **P0/P1 defects are non-negotiable release blockers** — cannot be overridden by anyone
5. **The user has final authority over P2/P3** — always present these for user decision
6. **"Trim-to-pass" anti-pattern** — functionality removal is never valid remediation
7. **Progress Sync Protocol** — any task >20% over estimate triggers CTO → CPO notification (Stage 4+)

## Defect Severity System

| Level | Definition                             | Action             |
| ----- | -------------------------------------- | ------------------ |
| P0    | Crash / data loss / security breach    | Non-negotiable fix |
| P1    | Core feature broken / major UX failure | Non-negotiable fix |
| P2    | Minor degradation / cosmetic           | User decides       |
| P3    | Polish / nice-to-have                  | User decides       |

## Stage 10 Release Checklist

All seven must be signed off before the user issues the final release decision:

| #   | Domain                                              | Sign-off Authority |
| --- | --------------------------------------------------- | ------------------ |
| 1   | Product — all PRD requirements implemented          | CPO                |
| 2   | Design — all CDO/IDS specifications realised        | CDO                |
| 3   | Architecture — all UML/ADR/TSD standards upheld     | CTO + CIO          |
| 4   | Security — SRD enforced, OWASP MASVS compliant      | CSO                |
| 5   | Testing — 100% automated test pass rate             | CTO                |
| 6   | Localisation — all target languages complete        | CTO-L              |
| 7   | Platform — App Store / Google Play requirements met | CTO + CPO          |

## Cross-Cutting Topics

- Architecture
- Security
- Testing
- Localization
