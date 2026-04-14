# Recruitment Pipeline — Hooks Implementation Plan (v2.0)

## Overview

This document maps Qwen Code CLI's hook system to the automated recruitment pipeline (`company/pipeline/recruitment/pipeline.md`). Each hook is a **system-enforced validator** that reads pipeline artifacts, validates format and business rules, and signals pass/fail to the pipeline engine.

**Key principle: Hooks are validators, NOT producers.** The pipeline produces artifacts; hooks verify them.

---

## Priority Classification

| Priority | Definition                                                     |
| -------- | -------------------------------------------------------------- |
| **P0**   | Non-negotiable — pipeline integrity depends on this            |
| **P1**   | Critical — prevents cascade failures and garbage-in            |
| **P2**   | Important — compliance and governance requirements             |
| **P3**   | Nice-to-have — operational visibility and lifecycle management |

---

## Hook Inventory (19 scripts across 10 event types)

| #   | Hook Event           | Pipeline Stage | Script                                        | Priority |
| --- | -------------------- | -------------- | --------------------------------------------- | -------- |
| 1   | `UserPromptSubmit`   | Stage 0        | `stage-0-validate-department-plan.py`         | P1       |
| 2   | `SubagentStart`      | Stage 0        | `stage-0-consolidate-recruitment-plans.py`    | P2       |
| 3   | `UserPromptSubmit`   | Stage 1        | `stage-1-validate-role-intake.py`             | P1       |
| 4   | `SessionStart`       | Stage 1        | `stage-1-init-pipeline-session.py`            | P3       |
| 5   | `SubagentStart`      | Stage 2        | `stage-2-init-sourcing-agent.py`              | P3       |
| 6   | `SubagentStop`       | Stage 2        | `stage-2-aggregate-sourcing-results.py`       | P3       |
| 7   | `PreToolUse`         | Stages 3–6     | `stage-3-to-6-validate-assessment-context.py` | P1       |
| 8   | `PostToolUse`        | Stage 3        | `stage-3-validate-screening-thresholds.py`    | P1       |
| 9   | `PostToolUse`        | Stage 5        | `validate-candidate-dossier.py`               | P0       |
| 10  | `PostToolUse`        | Stage 7        | `stage-7-validate-offer-generation.py`        | P1       |
| 11  | `PostToolUse`        | Stage 8        | `stage-8-generate-hiring-outcome-report.py`   | P3       |
| 12  | `PostToolUse`        | Stage 9        | `stage-9-onboarding-checklist.py`             | P3       |
| 13  | `PreToolUse`         | Stage 5        | `stage-5-asg02-design-review.py`              | P1       |
| 14  | `SessionEnd`         | Stage 5        | `stage-5-validate-vetting-gate.py`            | P0       |
| 15  | `SessionEnd`         | Stage 8        | `stage-8-generate-hiring-outcome-report.py`   | P3       |
| 16  | `UserPromptSubmit`   | Stage 8        | `stage-8-capture-user-decision.py`            | P1       |
| 17  | `PostToolUse`        | All stages     | `any-stage-append-audit-log.py`               | P0       |
| 18  | `PostToolUseFailure` | All stages     | `any-stage-escalate-r0-defect.py`             | P0       |
| 19  | `Notification`       | All stages     | `any-stage-validate-and-send-notification.py` | P2       |

---

## Not Applicable (2 of 12 Qwen Code events)

| Hook Event          | Reason                                                          |
| ------------------- | --------------------------------------------------------------- |
| `Stop`              | Pipeline stages run to completion or fail with R0/R1 escalation |
| `PermissionRequest` | Permissions pre-configured via RBAC, not requested at runtime   |

---

## Entity-Specific Audit Logs

All hooks write audit entries to the entity-specific audit log, determined by `entity_root`:

| Entity Type  | Entity Root                  | Audit Log Path                                     |
| ------------ | ---------------------------- | -------------------------------------------------- |
| Studio       | `studio/<name>/team`         | `studio/<name>/team/audit/audit-log.jsonl`         |
| Company Dept | `company/departments/<dept>` | `company/departments/<dept>/audit/audit-log.jsonl` |

Hooks **never** write to `.qwen/hooks/.../audit/`.

---

## Status

**ALL PHASES IMPLEMENTED** — 19 Python scripts across 10 hook events.
**TESTING:** 22/22 tests pass (`tests/test-integration.py`).
**MIGRATION:** 297 studio artifacts migrated to YAML frontmatter format.
