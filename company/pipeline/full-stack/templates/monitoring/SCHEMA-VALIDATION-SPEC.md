# Schema Validation Specification — Automated Gate Enforcement (Full-Stack Pipeline)

---

## 1. Purpose

This specification defines how **Stage Transition Schemas** are validated automatically at every pipeline gate for Full-Stack projects. It includes unique cross-track validation rules.

---

## 2. Validation Rules

### 2.1 Universal Rules (All Schemas)

| Rule ID    | Rule                                                                           |  Severity   |
| :--------- | :----------------------------------------------------------------------------- | :---------: |
| `V-FS-001` | `gate_result` must be `"pass"` or `"pass_with_conditions"`                     | **Blocker** |
| `V-FS-002` | All `sign_offs` fields must be `true`                                          | **Blocker** |
| `V-FS-003` | `completed_date` must be a valid ISO 8601 date                                 | **Warning** |
| `V-FS-004` | `version` must match schema version registry                                   | **Warning** |
| `V-FS-005` | `constraints_forward` must include all inherited constraints from prior stages | **Blocker** |
| `V-FS-006` | `produced_by.agent` must match a valid agent in the roster                     | **Warning** |

### 2.2 Stage-Specific Rules

| Schema | Rule ID     | Rule                                                                   |  Severity   |
| :----- | :---------- | :--------------------------------------------------------------------- | :---------: |
| `1→2`  | `V-FS-101`  | `artifacts.prd.req_count` must be > 0                                  | **Blocker** |
| `1→2`  | `V-FS-102`  | `artifacts.srd.sec_req_count` must be > 0                              | **Blocker** |
| `1→2`  | `V-FS-103`  | At least 2 fields in `platform_scope` must be `true`                   | **Blocker** |
| `3→4`  | `V-FS-301`  | `artifacts.adrs` array must have ≥ 1 entry                             | **Blocker** |
| `3→4`  | `V-FS-302`  | `cross_track_sync.api_contract_owner` must be a valid agent            | **Blocker** |
| `3→4`  | `V-FS-303`  | `security_architecture.stride_completed` must be `true`                | **Blocker** |
| `4→5`  | `V-FS-401`  | At least 1 `integration_milestones` entry must exist                   | **Blocker** |
| `4→5`  | `V-FS-402`  | Each integration milestone must reference ≥ 2 tracks                   | **Warning** |
| `5→6`  | `V-FS-501`  | All per-track `tasks_completed` must equal `tasks_total`               | **Blocker** |
| `5→6`  | `V-FS-502`  | `cross_track_integration_pass` must be `true`                          | **Blocker** |
| `6→7`  | `V-FS-601`  | `defect_summary.p0_resolved + p1_resolved` must equal all found P0/P1s | **Blocker** |
| `6→7`  | `V-FS-602`  | `sign_offs.red_team` must be `true`                                    | **Blocker** |
| `6→7`  | `V-FS-603`  | All 3 `codebase_tags` must be present                                  | **Blocker** |
| `7→8`  | `V-FS-701`  | `test_summary.pass_rate_pct` must be `100`                             | **Blocker** |
| `7→8`  | `V-FS-702`  | `test_summary.dast_high_findings` must be `0`                          | **Blocker** |
| `7→8`  | `V-FS-703`  | `test_summary.pentest_critical` must be `0`                            | **Blocker** |
| `8→9`  | `V-FS-801`  | `integrity_checks.security_control_weakened` must be `false`           | **Blocker** |
| `8→9`  | `V-FS-802`  | `integrity_checks.prd_features_intact` must be `true`                  | **Blocker** |
| `9→10` | `V-FS-901`  | `i18n_summary.hardcoded_strings_remaining` must be `0`                 | **Blocker** |
| `9→10` | `V-FS-902`  | All BLEU scores must be ≥ 0.80                                         | **Warning** |
| `10`   | `V-FS-1001` | All 12 `checklist` domain items must have `passed: true`               | **Blocker** |
| `10`   | `V-FS-1002` | `user_decision` must be `"release"` for release                        | **Blocker** |
| All    | `V-FS-1003` | `harness_compliance_verified` must be `true`                           | **Blocker** |

---

## 3–7. Process, Output, Integration, Escalation

Follow the **same structure** as the Web pipeline specification. Rule ID prefixes use `V-FS-` throughout. See `web-development/templates/monitoring/schema-validation-spec.md` for canonical definitions.

### Full-Stack Specific: Cross-Track Validation

The orchestrator runs an additional pass after standard validation:

```
For schema 5→6 (Development → Code Review):
  1. Verify all 3 codebases (mobile, web, api) have commit hashes
  2. Verify integration_test_results.e2e_pass is true
  3. If any track is "dormant" in 3→4, verify it is not submitting artifacts at 5→6
  → Violation of any = Blocker
```

| Pipeline Stage | Validation Trigger                  | Schema Validated         |
| :------------: | :---------------------------------- | :----------------------- |
|  Stage 1 → 2   | CPO + CSO submit gate package       | `schema-1-to-2.json`     |
|  Stage 2 → 3   | CDO submits gate package            | `schema-2-to-3.json`     |
|  Stage 3 → 4   | CTO + CIO submit gate package       | `schema-3-to-4.json`     |
|  Stage 4 → 5   | CTO submits gate package            | `schema-4-to-5.json`     |
|  Stage 5 → 6   | CTO submits gate package            | `schema-5-to-6.json`     |
|  Stage 6 → 7   | CTO (panel) submits gate package    | `schema-6-to-7.json`     |
|  Stage 7 → 8   | CTO submits gate package            | `schema-7-to-8.json`     |
|  Stage 8 → 9   | CTO (panel) submits gate package    | `schema-8-to-9.json`     |
|  Stage 9 → 10  | CTO-L submits gate package          | `schema-9-to-10.json`    |
|    Stage 10    | CTO (panel) submits release package | `schema-10-release.json` |
