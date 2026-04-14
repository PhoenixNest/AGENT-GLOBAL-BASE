# Hooks Index

Pipeline-specific hook configurations organized by owner and pipeline type.

## Structure

```
hooks/
└── company/
    └── automated-recruitment-pipeline/          # Recruitment pipeline hooks
        ├── README.md                             # Detailed documentation
        ├── hooks-config.json                     # Hook configuration (reference)
        ├── recruitment-pipeline-hooks-plan.md    # Implementation plan
        ├── schemas/
        │   └── artifact-schemas.md               # Artifact frontmatter schemas
        └── scripts/
            ├── lib/                              # Shared library (5 modules)
            │   ├── __init__.py
            │   ├── entity_resolver.py
            │   ├── audit_writer.py
            │   ├── artifact_parser.py
            │   └── validators.py
            └── ...                               # 23 hook scripts
```

## Pipelines

| Pipeline              | Location                                  | Hooks                       | Status         |
| --------------------- | ----------------------------------------- | --------------------------- | -------------- |
| Automated Recruitment | `company/automated-recruitment-pipeline/` | 23 scripts — all stages 0–9 | ✅ Implemented |

## Configuration

Hooks are registered in `.qwen/settings.json` under the `hooks` key. See `hooks-config.json` for standalone reference. Both files are kept in sync.

## Hook Execution Model

Hooks are invoked by Qwen Code at specific lifecycle events (PreToolUse, PostToolUse, UserPromptSubmit, etc.). They receive context via stdin JSON and communicate via exit code:

| Exit Code | Meaning                                          |
| --------- | ------------------------------------------------ |
| `0`       | Success — proceed to next stage                  |
| `2`       | Blocking error — pipeline stops at current stage |
| Other     | Non-blocking — logged but pipeline continues     |

## Architecture: Validator Model

Hooks **read** pipeline artifacts produced by the pipeline engine and validate them. They **never produce data artifacts**. The only files hooks write are:

- Entity-specific audit logs: `{entity_root}/audit/audit-log.jsonl`
- (Occasionally) temporary tracking files (e.g., GDPR Article 22 records)

## Priority Classification

| Priority   | Scripts                                                                                                                                                                                                                                                                                                                                                           | Pipeline Impact                     |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| **P0** (4) | `any-stage-escalate-r0-defect.py`, `any-stage-append-audit-log.py`, `validate-candidate-dossier.py`, `stage-5-validate-vetting-gate.py`                                                                                                                                                                                                                           | Pipeline integrity depends on these |
| **P1** (9) | `stage-0-validate-department-plan.py`, `stage-1-validate-role-intake.py`, `stage-3-to-6-validate-assessment-context.py`, `stage-3-validate-screening-thresholds.py`, `stage-4-validate-interview-scores.py`, `stage-5-asg02-design-review.py`, `stage-6-validate-background-check.py`, `stage-7-validate-offer-generation.py`, `stage-8-capture-user-decision.py` | Prevents cascade failures           |
| **P2** (3) | `any-stage-validate-and-send-notification.py`, `stage-0-consolidate-recruitment-plans.py`, `stage-2-validate-sourcing-shortlist.py`                                                                                                                                                                                                                               | Compliance and governance           |
| **P3** (7) | `stage-1-init-pipeline-session.py`, `stage-2-init-sourcing-agent.py`, `stage-2-aggregate-sourcing-results.py`, `stage-8-generate-hiring-outcome-report.py`, `stage-9-onboarding-checklist.py`, `monitoring-sla-check.py`, `monitoring-drift-detection.py`                                                                                                         | Operational visibility              |

## Defect Classification (R0–R3)

| Level | Definition                                            | Hook Action                               |
| ----- | ----------------------------------------------------- | ----------------------------------------- |
| R0    | Legal/compliance violation, discriminatory assessment | Pipeline PAUSED, CHRO escalation (exit 2) |
| R1    | Assessment scoring error, candidate data corruption   | Pipeline PAUSED, CHRO escalation (exit 2) |
| R2    | Notification delay, minor scheduling conflict         | Auto-resolve attempted, logged (exit 0)   |
| R3    | Cosmetic report formatting, non-blocking metadata gap | Logged for quarterly review (exit 0)      |

## Audit Trail

Each entity (studio or department) maintains its own audit log:

| Entity     | Audit Path                                         |
| ---------- | -------------------------------------------------- |
| Studio     | `studio/<studio>/team/audit/audit-log.jsonl`       |
| Department | `company/departments/<dept>/audit/audit-log.jsonl` |

Properties:

- **SHA-256 chained** — each entry's `previous_hash` links to prior `entry_hash`
- **File-locked** — `msvcrt` (Windows) or `fcntl` (Unix) prevents concurrent write corruption
- **Checksummed** — `checksum` field verifies entry integrity
- **Tamper-evident** — any modification breaks the hash chain

## Changelog

| Version | Date       | Changes                                                                                                                                          |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| v2.1    | 2026-04-13 | 38 audit fixes: file locking, path traversal, shebangs, YAML parser, dedup, entity resolution, type safety, discriminatory patterns, config sync |
| v2.0    | 2026-04-13 | Initial validator model — 23 hook scripts, entity-specific audit, YAML frontmatter schemas                                                       |
