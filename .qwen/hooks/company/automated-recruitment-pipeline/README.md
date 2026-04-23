# Automated Recruitment Pipeline — Hooks System (v2.1)

**Validator Model** — hooks READ, validate, audit, and signal. They NEVER produce data artifacts.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ PIPELINE (produces artifacts)                                   │
│   Stage N executes → writes to candidate_path/pipeline-artifacts│
│   e.g., studio/casual-games/team/crew/art/3d-artist/anya-petrova│
│         /pipeline-artifacts/stage5-vetting-gate.md              │
│                                                                 │
│   Fires hook event → stdin JSON with entity context             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ HOOK (validates + coordinates)                                  │
│                                                                 │
│  1. READ artifacts from candidate_path (via stdin context)      │
│  2. PARSE YAML frontmatter (fallback: regex from markdown body) │
│  3. VALIDATE format against schema, business rules              │
│  4. VERIFY completeness (all expected files present)            │
│  5. APPEND to entity-specific audit log (file-locked)           │
│  6. EXIT 0 (proceed) or EXIT 2 (block)                          │
│                                                                 │
│  Hooks NEVER write data artifacts.                              │
│  Hooks ONLY write: entity audit-log.jsonl.                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
.qwen/hooks/company/automated-recruitment-pipeline/
├── schemas/
│   └── artifact-schemas.md          # Canonical schema for all 9 artifact types
├── scripts/
│   ├── lib/                         # Shared library (imported by all hooks)
│   │   ├── __init__.py
│   │   ├── entity_resolver.py       # Resolve entity context from stdin JSON
│   │   ├── audit_writer.py          # SHA-256 chained, file-locked audit log
│   │   ├── artifact_parser.py       # YAML frontmatter parser + regex fallback
│   │   └── validators.py            # Common validation utilities
│   ├── any-stage-append-audit-log.py
│   ├── any-stage-escalate-r0-defect.py
│   ├── any-stage-validate-and-send-notification.py
│   ├── monitoring-drift-detection.py
│   ├── monitoring-sla-check.py
│   ├── stage-0-consolidate-recruitment-plans.py
│   ├── stage-0-validate-department-plan.py
│   ├── stage-1-init-pipeline-session.py
│   ├── stage-1-validate-role-intake.py
│   ├── stage-2-aggregate-sourcing-results.py
│   ├── stage-2-init-sourcing-agent.py
│   ├── stage-2-validate-sourcing-shortlist.py
│   ├── stage-3-to-6-validate-assessment-context.py
│   ├── stage-3-validate-screening-thresholds.py
│   ├── stage-4-validate-interview-scores.py
│   ├── stage-5-asg02-design-review.py
│   ├── stage-5-validate-vetting-gate.py
│   ├── stage-6-validate-background-check.py
│   ├── stage-7-validate-offer-generation.py
│   ├── stage-8-capture-user-decision.py
│   ├── stage-8-generate-hiring-outcome-report.py
│   ├── stage-9-onboarding-checklist.py
│   └── validate-candidate-dossier.py
├── hooks-config.json                # Hook configuration (reference copy)
├── README.md                        # This file
└── recruitment-pipeline-hooks-plan.md
```

---

## Hook Scripts (23 total)

### P0 — Critical (pipeline integrity)

| Script                             | Purpose                                                       |
| ---------------------------------- | ------------------------------------------------------------- |
| `any-stage-escalate-r0-defect.py`  | Classifies R0–R3 defects (SHA-256), blocks pipeline for R0/R1 |
| `any-stage-append-audit-log.py`    | SHA-256 chained audit trail (entity-specific, file-locked)    |
| `validate-candidate-dossier.py`    | Validates ALL 9 artifacts present for a candidate             |
| `stage-5-validate-vetting-gate.py` | Enforces elite talent bar (≥4 on ≥4 of 5 dimensions)          |

### P1 — High (prevents cascade failures)

| Script                                        | Purpose                                                               |
| --------------------------------------------- | --------------------------------------------------------------------- |
| `stage-0-validate-department-plan.py`         | 12-check department plan validation + amendment support               |
| `stage-1-validate-role-intake.py`             | 8-check role intake + PSD validation + contractor L3 governance       |
| `stage-3-to-6-validate-assessment-context.py` | 6-check pre-flight before assessments                                 |
| `stage-3-validate-screening-thresholds.py`    | 60th percentile auto-reject enforcement                               |
| `stage-4-validate-interview-scores.py`        | Composite score, 80th percentile auto-reject, weight sums, bar raiser |
| `stage-5-asg02-design-review.py`              | ASG-02 design leadership review for L1+ roles                         |
| `stage-6-validate-background-check.py`        | All 5 checks present, overall_status consistency, FAIL enforcement    |
| `stage-7-validate-offer-generation.py`        | Compensation band compliance                                          |
| `stage-8-capture-user-decision.py`            | Validates Approve/Reject decision format                              |

### P2 — Medium (compliance)

| Script                                        | Purpose                                                            |
| --------------------------------------------- | ------------------------------------------------------------------ |
| `any-stage-validate-and-send-notification.py` | FCRA/GDPR compliance, adverse action workflow, Article 22 tracking |
| `stage-0-consolidate-recruitment-plans.py`    | Department plan aggregation + cross-department conflict detection  |
| `stage-2-validate-sourcing-shortlist.py`      | Top-50 constraint, dedup integrity, no duplicate emails            |

### P3 — Low (operational visibility)

| Script                                      | Purpose                                                         |
| ------------------------------------------- | --------------------------------------------------------------- |
| `stage-1-init-pipeline-session.py`          | Hiring cycle init, SLA clock                                    |
| `stage-2-init-sourcing-agent.py`            | Sourcing channel initialization                                 |
| `stage-2-aggregate-sourcing-results.py`     | Deduplication + scoring (preserves no-email candidates)         |
| `stage-8-generate-hiring-outcome-report.py` | 7-section report with real data                                 |
| `stage-9-onboarding-checklist.py`           | Equipment, accounts, buddy assignment (numeric clearance check) |
| `monitoring-sla-check.py`                   | 6 SLA metrics with type-safe validation                         |
| `monitoring-drift-detection.py`             | 6 competency bar drift metrics                                  |

---

## Audit Log

| Property | Detail                                                                             |
| -------- | ---------------------------------------------------------------------------------- |
| Format   | JSONL (one JSON object per line)                                                   |
| Chain    | SHA-256 — each entry's `previous_hash` links to prior `entry_hash`                 |
| Lock     | File-level locking (`msvcrt` on Windows, `fcntl` on Unix) prevents race conditions |
| Checksum | `checksum` field — SHA-256 hash of entry (in production, use ed25519)              |
| Location | `{entity_root}/audit/audit-log.jsonl` — never `.qwen/`                             |
| Genesis  | First entry has `previous_hash: "genesis"`                                         |

---

## Entity Resolution

Hooks receive entity context via stdin JSON. The `entity_root` determines where audit logs are written:

| entity_type | entity_root example               | Audit log location                                      |
| ----------- | --------------------------------- | ------------------------------------------------------- |
| studio      | `studio/casual-games/team`        | `studio/casual-games/team/audit/audit-log.jsonl`        |
| company     | `company/departments/engineering` | `company/departments/engineering/audit/audit-log.jsonl` |

Hooks **never** write to `.qwen/hooks/.../audit/`.

---

## Artifact Schemas

All pipeline artifacts use **YAML frontmatter + markdown body**:

```yaml
---
document_id: 'VET-2026-G24-001'
stage: 'stage-5'
entity_type: 'studio'
entity_root: 'studio/casual-games/team'
candidate_id: 'G24'
candidate_name: 'Anya Petrova'
role_title: '3D Artist #2'
role_family: 'art'
seniority: 'L2'
scores:
  impact_at_scale: 4
  craft_depth: 5
  leadership_signal: 3
  standards_signal: 4
  red_flag_scan: 'PASS'
total_score: 16
result: 'PASS'
---
# VETTING GATE — Anya Petrova (G24)

## Five-Dimension Assessment
...
```

Full schema definitions: `schemas/artifact-schemas.md`

---

## Defect Classification (R0–R3)

| Level | Definition                                            | Hook Action                               |
| ----- | ----------------------------------------------------- | ----------------------------------------- |
| R0    | Legal/compliance violation, discriminatory assessment | Pipeline PAUSED, CHRO escalation (exit 2) |
| R1    | Assessment scoring error, candidate data corruption   | Pipeline PAUSED, CHRO escalation (exit 2) |
| R2    | Notification delay, minor scheduling conflict         | Auto-resolve attempted, logged (exit 0)   |
| R3    | Cosmetic report formatting, non-blocking metadata gap | Logged for quarterly review (exit 0)      |

---

## Changelog

| Version | Date       | Changes                                                                                                                                                                        |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| v2.1    | 2026-04-13 | 38 audit fixes: file locking, path traversal, shebangs, YAML parser, dedup, entity resolution, type safety, discriminatory patterns, markdown report completeness, config sync |
| v2.0    | 2026-04-13 | Initial validator model — 23 hook scripts, entity-specific audit, YAML frontmatter schemas                                                                                     |
