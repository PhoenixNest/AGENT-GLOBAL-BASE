# Recruitment Pipeline — Artifact Schema Definitions

**Version:** 2.0 (validator model — read-only hooks)
**Date:** 2026-04-13
**Scope:** Universal — applies to both company departments and studio recruitment
**Status:** Source of truth for all hook validation logic

---

## Design Principles

| Principle                   | Rule                                                                                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **YAML frontmatter**        | Every artifact begins with `---` delimited YAML frontmatter. Hooks parse this for structured validation.                                   |
| **Markdown body**           | Human-readable content below frontmatter. Hooks do not parse body content for data extraction (frontmatter is authoritative).              |
| **Entity-agnostic paths**   | Hooks receive `entity_root` via stdin — never hardcoded. Resolves to `company/departments/<dept>/` or `studio/<studio>/team/`.             |
| **Per-candidate isolation** | Artifacts live at `{entity_root}/crew/.../pipeline-artifacts/stage{N}-*.md` (studio) or `{entity_root}/.../pipeline-artifacts/` (company). |
| **Gate status required**    | Every artifact ends with `**Gate Status:**` line indicating pipeline state.                                                                |

---

## Common Frontmatter Fields (All Artifacts)

Every artifact includes these base fields:

```yaml
---
document_id: string # e.g., "PSD-2026-G24-001"
stage: string # e.g., "stage-1", "stage-5"
entity_type: string # "studio" | "company"
entity_root: string # e.g., "studio/casual-games/team" or "company/departments/engineering"
candidate_id: string # e.g., "G24", "CAND-001"
candidate_name: string # e.g., "Anya Petrova"
role_title: string # e.g., "3D Artist #2"
role_family: string # e.g., "art", "engineering", "leadership"
seniority: string # "L0" | "L1" | "L2" | "L3" | "L4"
generated_at: string # ISO 8601 timestamp
---
```

---

## Stage 1: Position Specification Document (PSD)

**File pattern:** `stage1-psd.md`

### Frontmatter Schema

```yaml
---
document_id: string # Required. Pattern: "PSD-{YEAR}-{ID}-{SEQ}"
stage: 'stage-1' # Required. Constant.
entity_type: string # Required. "studio" | "company"
entity_root: string # Required.
candidate_id: string # Required. Assigned by system.
candidate_name: string # Required. Populated after hire.
role_title: string # Required.
role_family: string # Required. Must be in approved taxonomy.
seniority: string # Required. L0-L4.
priority: string # Required. "P0" | "P1" | "P2"
reports_to: string # Required.
compensation_band: # Required.
  min: number # Required. Non-negative.
  max: number # Required. >= min.
  currency: string # Optional. Default "USD".
competencies: # Required. Array of {name, weight}.
  - name: string # Required. Non-empty.
    weight: number # Required. 0.0-1.0.
sourcing_channels: # Optional.
  - channel: string # Required.
    weight: number # Required. Multiplier (e.g., 1.5).
assessment_battery: # Required. Array of strings.
  - string # Required. Non-empty.
generated_at: string # Required. ISO 8601.
plan_reference: # Required for Stage 1.
  quarter: string # Required. e.g., "2026-Q2"
  plan_entry_id: string # Required. Links to Stage 0 approved plan.
---
```

### Validation Rules

| Rule  | Check                                            | Severity |
| ----- | ------------------------------------------------ | -------- |
| R1-01 | `role_family` in approved taxonomy               | R1       |
| R1-02 | `compensation_band.max >= compensation_band.min` | R1       |
| R1-03 | `compensation_band.min > 0`                      | R1       |
| R1-04 | Sum of `competencies[].weight` ≈ 1.0 (±0.01)     | R1       |
| R1-05 | `seniority` in [L0, L1, L2, L3, L4]              | R1       |
| R1-06 | `priority` in [P0, P1, P2]                       | R2       |
| R1-07 | `assessment_battery` has ≥ 2 items               | R2       |
| R1-08 | `plan_reference` present (links to Stage 0 plan) | R1       |
| R1-09 | `reports_to` non-empty                           | R2       |
| R1-10 | File exists at expected path                     | R1       |

### Approved Role Family Taxonomy

| Context             | Role Families                                                                   |
| ------------------- | ------------------------------------------------------------------------------- |
| Company departments | engineering, product, design, data, translation, security, business, hr, devops |
| Studio              | leadership, engineering, creative-design, art, audio, production, live-ops      |

---

## Stage 2: Sourcing Shortlist

**File pattern:** `stage2-sourcing-shortlist.md`

### Frontmatter Schema

```yaml
---
document_id: string # Required. Pattern: "SRC-{YEAR}-{ID}-{SEQ}"
stage: 'stage-2' # Required.
entity_type: string # Required.
entity_root: string # Required.
candidate_id: string # Required.
candidate_name: string # Required.
role_title: string # Required.
role_family: string # Required.
seniority: string # Required.
generated_at: string # Required.
sourcing_results: # Required.
  total_raw: number # Required. ≥ 1.
  unique_after_dedup: number # Required. ≤ total_raw.
  candidate_rank: number # Required. Position in shortlist (1-based).
  sourcing_score: number # Required. 0-100.
  top_5_count: number # Required. Always 5 for this artifact view.
channels_used: # Required. ≥ 1.
  - string # Required. Non-empty channel name.
---
```

### Validation Rules

| Rule  | Check                                                               | Severity |
| ----- | ------------------------------------------------------------------- | -------- |
| R2-01 | `sourcing_results.total_raw >= 1`                                   | R1       |
| R2-02 | `sourcing_results.unique_after_dedup <= sourcing_results.total_raw` | R1       |
| R2-03 | `sourcing_results.sourcing_score` in 0-100                          | R1       |
| R2-04 | `channels_used` has ≥ 1 entry                                       | R2       |
| R2-05 | `sourcing_results.candidate_rank >= 1`                              | R1       |

---

## Stage 3: Screening Results

**File pattern:** `stage3-screening-results.md`

### Frontmatter Schema

```yaml
---
document_id: string # Required. Pattern: "SCR-{YEAR}-{ID}-{SEQ}"
stage: 'stage-3' # Required.
entity_type: string # Required.
entity_root: string # Required.
candidate_id: string # Required.
candidate_name: string # Required.
role_title: string # Required.
role_family: string # Required.
seniority: string # Required.
generated_at: string # Required.
screening: # Required.
  total_screened: number # Required. ≥ 1.
  passed: number # Required. ≥ 0.
  auto_rejected: number # Required. ≥ 0.
  candidate_score: number # Required. 0-100.
  candidate_percentile: number # Required. 0-100.
  candidate_result: string # Required. "PASS" | "AUTO_REJECT"
  percentile_threshold: number # Required. Typically 60.
rejection_reasons: # Optional. Only if auto_rejected.
  - string # Non-empty reason strings.
---
```

### Validation Rules

| Rule  | Check                                                                                 | Severity |
| ----- | ------------------------------------------------------------------------------------- | -------- |
| R3-01 | `screening.passed + screening.auto_rejected == screening.total_screened`              | R1       |
| R3-02 | If `candidate_result == "PASS"`, `candidate_percentile >= percentile_threshold`       | R0       |
| R3-03 | If `candidate_result == "AUTO_REJECT"`, `candidate_percentile < percentile_threshold` | R0       |
| R3-04 | `percentile_threshold == 60` (per pipeline spec)                                      | R1       |
| R3-05 | `candidate_score` in 0-100                                                            | R1       |

---

## Stage 4: Interview Scores

**File pattern:** `stage4-interview-scores.md`

### Frontmatter Schema

```yaml
---
document_id: string # Required. Pattern: "INT-{YEAR}-{ID}-{SEQ}"
stage: 'stage-4' # Required.
entity_type: string # Required.
entity_root: string # Required.
candidate_id: string # Required.
candidate_name: string # Required.
role_title: string # Required.
role_family: string # Required.
seniority: string # Required.
generated_at: string # Required.
assessments: # Required. ≥ 2 items.
  - component: string # Required. Non-empty.
    score: number # Required. 0-5.
    weight: number # Required. 0.0-1.0.
    weighted_score: number # Required. score × weight.
composite_score: number # Required. Sum of weighted_scores.
percentile: number # Required. 0-100.
percentile_threshold: number # Required. Typically 80.
bar_raiser: string # Required. "STRONG_HIRE" | "HIRE" | "WEAK_HIRE" | "NO_HIRE"
result: string # Required. "PASS" | "AUTO_REJECT"
---
```

### Validation Rules

| Rule  | Check                                                             | Severity |
| ----- | ----------------------------------------------------------------- | -------- |
| R4-01 | `assessments` has ≥ 2 items                                       | R1       |
| R4-02 | Sum of `assessments[].weight` ≈ 1.0 (±0.01)                       | R1       |
| R4-03 | `composite_score` ≈ sum of `assessments[].weighted_score` (±0.01) | R1       |
| R4-04 | Each `assessments[].score` in 0-5                                 | R1       |
| R4-05 | If `result == "PASS"`, `percentile >= percentile_threshold`       | R0       |
| R4-06 | If `result == "AUTO_REJECT"`, `percentile < percentile_threshold` | R0       |
| R4-07 | `percentile_threshold == 80` (per pipeline spec)                  | R1       |
| R4-08 | `bar_raiser` not "NO_HIRE" when `result == "PASS"`                | R1       |

---

## Stage 5: Vetting Gate

**File pattern:** `stage5-vetting-gate.md`

### Frontmatter Schema

```yaml
---
document_id: string # Required. Pattern: "VET-{YEAR}-{ID}-{SEQ}"
stage: 'stage-5' # Required.
entity_type: string # Required.
entity_root: string # Required.
candidate_id: string # Required.
candidate_name: string # Required.
role_title: string # Required.
role_family: string # Required.
seniority: string # Required.
generated_at: string # Required.
scores: # Required.
  impact_at_scale: number # Required. 0-5. Must be ≥ 4.
  craft_depth: number # Required. 0-5. Must be ≥ 4.
  leadership_signal: number # Required. 0-5. ≥ 4 (supervisor) or ≥ 3 (IC).
  standards_signal: number # Required. 0-5. Must be ≥ 4.
  red_flag_scan: string # Required. "PASS" | "FAIL"
  avg_tenure_months: number # Required. ≥ 0.
total_score: number # Required. Sum of 4 scored dims (max 20).
dimensions_at_threshold: number # Required. Count of dims ≥ threshold.
is_supervisor: boolean # Required. Determines leadership threshold.
result: string # Required. "PASS" | "FAIL"
asg02_design_review: string # Optional. "PASS" | "FAIL" | "waived"
---
```

### Validation Rules

| Rule  | Check                                                           | Severity |
| ----- | --------------------------------------------------------------- | -------- |
| R5-01 | `scores.impact_at_scale >= 4`                                   | R0       |
| R5-02 | `scores.craft_depth >= 4`                                       | R0       |
| R5-03 | `scores.leadership_signal >= 4` (supervisor) or `>= 3` (IC)     | R0       |
| R5-04 | `scores.standards_signal >= 4`                                  | R0       |
| R5-05 | `scores.red_flag_scan == "PASS"`                                | R0       |
| R5-06 | `dimensions_at_threshold >= 4`                                  | R0       |
| R5-07 | `scores.avg_tenure_months >= 18` (or flagged)                   | R2       |
| R5-08 | `total_score == impact + craft + leadership + standards` (±0)   | R1       |
| R5-09 | If L1+ design role, `asg02_design_review` present and != "FAIL" | R1       |
| R5-10 | `result == "PASS"` iff all R5-01 through R5-06 pass             | R0       |

---

## Stage 6: Background Check

**File pattern:** `stage6-background-check.md`

### Frontmatter Schema

```yaml
---
document_id: string # Required. Pattern: "BGC-{YEAR}-{ID}-{SEQ}"
stage: 'stage-6' # Required.
entity_type: string # Required.
entity_root: string # Required.
candidate_id: string # Required.
candidate_name: string # Required.
role_title: string # Required.
role_family: string # Required.
seniority: string # Required.
generated_at: string # Required.
checks: # Required.
  employment_verification: string # Required. "CLEAR" | "FLAGGED" | "FAIL"
  education_verification: string # Required. "CLEAR" | "FLAGGED" | "FAIL"
  criminal_background: string # Required. "CLEAR" | "FLAGGED" | "FAIL"
  reference_checks: string # Required. "CLEAR" | "FLAGGED" | "FAIL"
  conflict_of_interest: string # Required. "CLEAR" | "FLAGGED" | "DISQUALIFYING" | "ACCEPTABLE_WITH_MITIGATIONS"
overall_status: string # Required. "CLEAR" | "FLAGGED" | "FAIL"
flags: # Optional. Present if any check != CLEAR.
  - check: string # Which check flagged.
    detail: string # Description of flag.
    resolved: boolean # Whether flag was resolved.
---
```

### Validation Rules

| Rule  | Check                                                                  | Severity |
| ----- | ---------------------------------------------------------------------- | -------- |
| R6-01 | All 5 checks present                                                   | R1       |
| R6-02 | If all checks "CLEAR", `overall_status == "CLEAR"`                     | R1       |
| R6-03 | If any check "FAIL" or COI "DISQUALIFYING", `overall_status == "FAIL"` | R0       |
| R6-04 | `overall_status != "CLEAR"` if any check != "CLEAR"                    | R1       |

---

## Stage 7: Offer

**File pattern:** `stage7-offer.md`

### Frontmatter Schema

```yaml
---
document_id: string # Required. Pattern: "OFF-{YEAR}-{ID}-{SEQ}"
stage: 'stage-7' # Required.
entity_type: string # Required.
entity_root: string # Required.
candidate_id: string # Required.
candidate_name: string # Required.
role_title: string # Required.
role_family: string # Required.
seniority: string # Required.
generated_at: string # Required.
offer: # Required.
  base_salary: number # Required. Must be within compensation band.
  bonus_percent: number # Optional. 0-100.
  equity_percent: number # Optional. 0-100.
  signing_bonus: number # Optional. >= 0.
  relocation: number # Optional. >= 0.
  start_date: string # Required. ISO date.
compensation_band_reference: # Required. For validation.
  min: number # Required.
  max: number # Required.
within_band: boolean # Required. base_salary within [min, max].
status: string # Required. "extended" | "accepted" | "declined" | "negotiating"
status_date: string # Required. ISO date of status change.
---
```

### Validation Rules

| Rule  | Check                                                               | Severity |
| ----- | ------------------------------------------------------------------- | -------- |
| R7-01 | `offer.base_salary` within `[compensation_band_reference.min, max]` | R0       |
| R7-02 | `within_band == true` if base_salary in range                       | R1       |
| R7-03 | `offer.base_salary > 0`                                             | R1       |
| R7-04 | `status` in [extended, accepted, declined, negotiating]             | R2       |
| R7-05 | `start_date` is valid ISO date                                      | R2       |

---

## Stage 8: Provisioning

**File pattern:** `stage8-provisioning.md`

### Frontmatter Schema

```yaml
---
document_id: string # Required. Pattern: "PRO-{YEAR}-{ID}-{SEQ}"
stage: 'stage-8' # Required.
entity_type: string # Required.
entity_root: string # Required.
candidate_id: string # Required.
candidate_name: string # Required.
role_title: string # Required.
role_family: string # Required.
seniority: string # Required.
generated_at: string # Required.
provisioning: # Required.
  accounts_created: boolean # Required.
  equipment_ordered: boolean # Required.
  software_licenses: boolean # Required.
  buddy_assigned: boolean # Required. Buddy name in body.
  clearance_level: string # Required. "L0"-"L4" or "L2" for contractors.
  manager_briefing: boolean # Required.
  documentation_sent: boolean # Required.
contractor: boolean # Required. If true, clearance must be L2 minimum.
auto_revocation_date: string # Required if contractor. ISO date.
---
```

### Validation Rules

| Rule  | Check                                                   | Severity |
| ----- | ------------------------------------------------------- | -------- |
| R8-01 | All `provisioning.*` boolean fields are `true`          | R1       |
| R8-02 | If `contractor == true`, `clearance_level >= "L2"`      | R0       |
| R8-03 | If `contractor == true`, `auto_revocation_date` present | R1       |
| R8-04 | `buddy_assigned == true`                                | R2       |

---

## Stage 9: Hiring Outcome Report

**File pattern:** `stage9-hiring-outcome-report.md`

### Frontmatter Schema

```yaml
---
document_id: string # Required. Pattern: "HIR-{YEAR}-{ID}-{SEQ}"
stage: 'stage-9' # Required.
entity_type: string # Required.
entity_root: string # Required.
candidate_id: string # Required.
candidate_name: string # Required.
role_title: string # Required.
role_family: string # Required.
seniority: string # Required.
generated_at: string # Required.
hiring_cycle_id: string # Required.
final_decision: string # Required. "HIRED" | "NOT_HIRED" | "ROLLED_BACK"
time_to_fill_days: number # Required. >= 0.
vetting_total: number # Required. 0-20.
composite_score: number # Required. 0-5.
composite_percentile: number # Required. 0-100.
offer_accepted: boolean # Required.
placement_path: string # Required. Relative path to crew/department folder.
reports_to: string # Required.
start_date: string # Required. ISO date.
sections_complete: number # Required. Must be 7 for full report.
---
```

### Validation Rules

| Rule  | Check                                                    | Severity |
| ----- | -------------------------------------------------------- | -------- |
| R9-01 | `sections_complete == 7`                                 | R1       |
| R9-02 | `final_decision` in [HIRED, NOT_HIRED, ROLLED_BACK]      | R1       |
| R9-03 | If `final_decision == "HIRED"`, `offer_accepted == true` | R0       |
| R9-04 | `time_to_fill_days >= 0`                                 | R2       |
| R9-05 | `vetting_total` in 0-20                                  | R1       |
| R9-06 | `placement_path` exists on filesystem                    | R1       |
| R9-07 | `reports_to` non-empty                                   | R2       |

---

## Entity Resolution

Hooks receive `entity_type` and `entity_root` via stdin. The audit log path is derived as:

```
audit_log_path = "{entity_root}/audit/audit-log.jsonl"
```

| entity_type | entity_root example               | Audit log location                                      |
| ----------- | --------------------------------- | ------------------------------------------------------- |
| studio      | `studio/casual-games/team`        | `studio/casual-games/team/audit/audit-log.jsonl`        |
| company     | `company/departments/engineering` | `company/departments/engineering/audit/audit-log.jsonl` |

Hooks **must never** write to `.qwen/hooks/.../audit/`. All audit entries go to the entity-specific audit directory, creating it if needed.

---

## Migration Notes

Existing artifacts (39 crew members × 9 stages = 351 files in Casual Games studio) currently lack YAML frontmatter. The migration script (`migration/migrate-frontmatter.py`) will:

1. Parse existing markdown to extract data via regex
2. Insert YAML frontmatter matching the schemas above
3. Preserve the existing markdown body unchanged
4. Write audit entry documenting the migration

Fallback: If frontmatter is missing, hooks parse via regex and emit R2 warning. Missing frontmatter does not block the pipeline but is logged for remediation.
