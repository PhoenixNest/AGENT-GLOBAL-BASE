# Schema Validation Specification — Automated Gate Enforcement

> **Addresses Gap:** Automated enforcement of JSON schema contracts

---

## 1. Purpose

This specification defines how **Stage Transition Schemas** are validated automatically at every pipeline gate — ensuring that no stage advances with missing fields, unsigned sign-offs, or unresolved P0/P1 defects.

---

## 2. Validation Rules

### 2.1 Universal Rules (All Schemas)

| Rule ID | Rule                                                                           |  Severity   |
| :------ | :----------------------------------------------------------------------------- | :---------: |
| `V-001` | `gate_result` must be `"pass"` or `"pass_with_conditions"`                     | **Blocker** |
| `V-002` | All `sign_offs` fields must be `true`                                          | **Blocker** |
| `V-003` | `completed_date` must be a valid ISO 8601 date                                 | **Warning** |
| `V-004` | `version` must match schema version registry                                   | **Warning** |
| `V-005` | `constraints_forward` must include all inherited constraints from prior stages | **Blocker** |
| `V-006` | `produced_by.agent` must match a valid agent in the roster                     | **Warning** |

### 2.2 Stage-Specific Rules

| Schema | Rule ID  | Rule                                                                   |  Severity   |
| :----- | :------- | :--------------------------------------------------------------------- | :---------: |
| `1→2`  | `V-101`  | `artifacts.prd.req_count` must be > 0                                  | **Blocker** |
| `1→2`  | `V-102`  | `artifacts.srd.sec_req_count` must be > 0                              | **Blocker** |
| `3→4`  | `V-301`  | `artifacts.adrs` array must have ≥ 1 entry                             | **Blocker** |
| `3→4`  | `V-302`  | `platform_strategy.approach` must be one of allowed values             | **Blocker** |
| `3→4`  | `V-303`  | `security_architecture.stride_completed` must be `true`                | **Blocker** |
| `5→6`  | `V-501`  | `completion_metrics.tasks_completed` must equal `tasks_total`          | **Blocker** |
| `6→7`  | `V-601`  | `defect_summary.p0_resolved + p1_resolved` must equal all found P0/P1s | **Blocker** |
| `6→7`  | `V-602`  | `sign_offs.red_team` must be `true`                                    | **Blocker** |
| `7→8`  | `V-701`  | `test_summary.pass_rate_pct` must be `100`                             | **Blocker** |
| `7→8`  | `V-702`  | `test_summary.dast_high_findings` must be `0`                          | **Blocker** |
| `7→8`  | `V-703`  | `test_summary.pentest_critical` must be `0`                            | **Blocker** |
| `8→9`  | `V-801`  | `integrity_checks.security_control_weakened` must be `false`           | **Blocker** |
| `8→9`  | `V-802`  | `integrity_checks.prd_features_intact` must be `true`                  | **Blocker** |
| `9→10` | `V-901`  | `i18n_summary.hardcoded_strings_remaining` must be `0`                 | **Blocker** |
| `9→10` | `V-902`  | All BLEU scores must be ≥ 0.80                                         | **Warning** |
| `10`   | `V-1001` | All 7 `checklist` items must have `passed: true`                       | **Blocker** |
| `10`   | `V-1002` | `user_decision` must be `"release"` for release                        | **Blocker** |

---

## 3. Validation Process

```
Stage N owner produces:
  1. STAGE-TRANSITION-SUMMARY.md (human-readable)
  2. schema-N-to-N+1.json (machine-readable)
      ↓
Orchestrator validates schema:
  1. Parse JSON — reject if malformed
  2. Run universal rules (V-001 through V-006)
  3. Run stage-specific rules (V-NNN)
  4. If any BLOCKER fails:
     → Reject handoff
     → Return error list to stage owner
     → Stage owner fixes and resubmits
  5. If only WARNINGs:
     → Log warnings
     → Allow handoff with advisory
  6. If all pass:
     → Advance to Stage N+1
     → Archive schema JSON alongside summary
```

---

## 4. Validation Output Format

When validation runs, it produces a result in this format:

```json
{
  "validation_run": {
    "schema": "stage-transition/N-to-N+1",
    "timestamp": "YYYY-MM-DDTHH:mm:ssZ",
    "result": "pass | fail | warn"
  },
  "blockers": [
    {
      "rule": "V-NNN",
      "field": "field.path",
      "expected": "value",
      "actual": "value"
    }
  ],
  "warnings": [
    { "rule": "V-NNN", "field": "field.path", "message": "Advisory text" }
  ]
}
```

---

## 5. Constraint Accumulation Validation

A special validation ensures the `constraints_forward` array is **monotonically growing** — no constraint from a prior stage may be removed.

```
For schema N-to-N+1:
  1. Load schema (N-1)-to-N (prior transition)
  2. Extract its constraints_forward array
  3. Verify ALL prior constraints appear in current schema's constraints_forward
  4. If any missing → Blocker V-005
```

This prevents the "constraint amnesia" anti-pattern where security or architectural constraints get silently dropped during later stages.

---

## 6. Integration with Pipeline

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

---

## 7. Error Escalation

| Validation Result          | Action                                              |
| :------------------------- | :-------------------------------------------------- |
| All pass                   | Stage advances normally                             |
| Warnings only              | Stage advances; warnings logged in PROGRESS.md      |
| 1+ Blockers                | Stage blocked; error list sent to stage owner       |
| 3+ consecutive rejections  | Auto-escalate to CTO via Escalation Message         |
| V-005 constraint violation | Auto-escalate to CTO + CSO (potential security gap) |
