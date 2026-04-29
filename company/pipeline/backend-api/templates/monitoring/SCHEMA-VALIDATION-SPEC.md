# Schema Validation Specification — Automated Gate Enforcement (Backend API Pipeline)

---

## 1. Purpose

This specification defines how **Stage Transition Schemas** are validated automatically at every pipeline gate for Backend API projects.

---

## 2. Validation Rules

### 2.1 Universal Rules (All Schemas)

| Rule ID     | Rule                                                                           |  Severity   |
| :---------- | :----------------------------------------------------------------------------- | :---------: |
| `V-API-001` | `gate_result` must be `"pass"` or `"pass_with_conditions"`                     | **Blocker** |
| `V-API-002` | All `sign_offs` fields must be `true`                                          | **Blocker** |
| `V-API-003` | `completed_date` must be a valid ISO 8601 date                                 | **Warning** |
| `V-API-004` | `version` must match schema version registry                                   | **Warning** |
| `V-API-005` | `constraints_forward` must include all inherited constraints from prior stages | **Blocker** |
| `V-API-006` | `produced_by.agent` must match a valid agent in the roster                     | **Warning** |

### 2.2 Stage-Specific Rules

| Schema | Rule ID      | Rule                                                                   |  Severity   |
| :----- | :----------- | :--------------------------------------------------------------------- | :---------: | ---- | ------------- | ----------- |
| `1→2`  | `V-API-101`  | `artifacts.prd.req_count` must be > 0                                  | **Blocker** |
| `1→2`  | `V-API-102`  | `artifacts.srd.sec_req_count` must be > 0                              | **Blocker** |
| `1→2`  | `V-API-103`  | `api_type` must be one of `REST                                        |   GraphQL   | gRPC | event_driven` | **Blocker** |
| `3→4`  | `V-API-301`  | `artifacts.adrs` array must have ≥ 1 entry                             | **Blocker** |
| `3→4`  | `V-API-302`  | `api_strategy.approach` must be one of allowed values                  | **Blocker** |
| `3→4`  | `V-API-303`  | `security_architecture.stride_completed` must be `true`                | **Blocker** |
| `5→6`  | `V-API-501`  | `completion_metrics.tasks_completed` must equal `tasks_total`          | **Blocker** |
| `5→6`  | `V-API-502`  | `completion_metrics.contract_tests_pass` must be `true`                | **Blocker** |
| `6→7`  | `V-API-601`  | `defect_summary.p0_resolved + p1_resolved` must equal all found P0/P1s | **Blocker** |
| `6→7`  | `V-API-602`  | `sign_offs.red_team` must be `true`                                    | **Blocker** |
| `7→8`  | `V-API-701`  | `test_summary.pass_rate_pct` must be `100`                             | **Blocker** |
| `7→8`  | `V-API-702`  | `test_summary.dast_high_findings` must be `0`                          | **Blocker** |
| `7→8`  | `V-API-703`  | `test_summary.pentest_critical` must be `0`                            | **Blocker** |
| `7→8`  | `V-API-704`  | `test_summary.contract_test_pass` must be `true`                       | **Blocker** |
| `8→9`  | `V-API-801`  | `integrity_checks.security_control_weakened` must be `false`           | **Blocker** |
| `8→9`  | `V-API-802`  | `integrity_checks.prd_features_intact` must be `true`                  | **Blocker** |
| `9→10` | `V-API-901`  | `i18n_summary.hardcoded_strings_remaining` must be `0`                 | **Blocker** |
| `9→10` | `V-API-902`  | All BLEU scores must be ≥ 0.80                                         | **Warning** |
| `10`   | `V-API-1001` | All checklist items must have `passed: true`                           | **Blocker** |
| `10`   | `V-API-1002` | `user_decision` must be `"release"` for release                        | **Blocker** |

---

## 3–7. Process, Output, Constraint Accumulation, Integration, Escalation

These sections follow the **same structure** as the Web pipeline specification. Rule ID prefixes use `V-API-` throughout. See `web-development/templates/monitoring/SCHEMA-VALIDATION-SPEC.md` for the canonical process and escalation definitions.

| Pipeline Stage | Validation Trigger                  | Schema Validated         |
| :------------: | :---------------------------------- | :----------------------- |
|  Stage 1 → 2   | VP API + CSO submit gate package    | `schema-1-to-2.json`     |
|  Stage 2 → 3   | CDO submits gate package            | `schema-2-to-3.json`     |
|  Stage 3 → 4   | CTO + CIO submit gate package       | `schema-3-to-4.json`     |
|  Stage 4 → 5   | CTO submits gate package            | `schema-4-to-5.json`     |
|  Stage 5 → 6   | CTO submits gate package            | `schema-5-to-6.json`     |
|  Stage 6 → 7   | CTO (panel) submits gate package    | `schema-6-to-7.json`     |
|  Stage 7 → 8   | CTO submits gate package            | `schema-7-to-8.json`     |
|  Stage 8 → 9   | CTO (panel) submits gate package    | `schema-8-to-9.json`     |
|  Stage 9 → 10  | CTO-L submits gate package          | `schema-9-to-10.json`    |
|    Stage 10    | CTO (panel) submits release package | `schema-10-release.json` |
