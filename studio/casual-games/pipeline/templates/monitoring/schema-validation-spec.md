# Schema Validation Specification — Casual Games Studio

> **ASE Layer:** 3 — Harness Engineering (gate automation)
> **Authority:** Studio Director Dr. Marcus Vogel
> **Reference:** `stage-transition-schemas.md`, `harness-config.md`

This specification defines how stage transition schemas are validated at every kill gate and user approval gate — ensuring no stage advances with missing fields, unsigned sign-offs, or unmet kill gate criteria.

---

## 1. Universal Rules (All Schemas)

| Rule ID    | Rule                                                                         |  Severity   |
| :--------- | :--------------------------------------------------------------------------- | :---------: |
| `V-CG-001` | `gate_result` must be `"pass"` or `"pass_with_conditions"`                   | **Blocker** |
| `V-CG-002` | All `sign_offs` fields must be `true`                                        | **Blocker** |
| `V-CG-003` | `transition_date` must be a valid ISO 8601 date                              |   Warning   |
| `V-CG-004` | `schema_version` must match schema registry                                  |   Warning   |
| `V-CG-005` | `constraints_forward` must carry all inherited constraints from prior stages | **Blocker** |
| `V-CG-006` | `produced_by.agent` must match a valid crew member in the roster             |   Warning   |
| `V-CG-007` | `harness_compliance_verified` must be `true` for all transitions             | **Blocker** |

---

## 2. Kill Gate Rules

### Kill Gate 1 (Stage 1 → 2): Concept Validation

| Rule ID     | Rule                                                      |  Severity   |
| :---------- | :-------------------------------------------------------- | :---------: |
| `V-KG1-001` | `concept_validation.gdd_complete` must be `true`          | **Blocker** |
| `V-KG1-002` | `concept_validation.prd_complete` must be `true`          | **Blocker** |
| `V-KG1-003` | `concept_validation.srd_complete` must be `true`          | **Blocker** |
| `V-KG1-004` | `kill_gate_criteria.minimum_threshold_met` must be `true` | **Blocker** |
| `V-KG1-005` | `user_decision` must be present                           | **Blocker** |

### Kill Gate 2 (Stage 2 → 3): Prototype Validation

| Rule ID     | Rule                                                    |  Severity   |
| :---------- | :------------------------------------------------------ | :---------: |
| `V-KG2-001` | `build_criteria.playable_build_complete` must be `true` | **Blocker** |
| `V-KG2-002` | `build_criteria.gds_complete` must be `true`            | **Blocker** |
| `V-KG2-003` | `prototype_metrics.playtest_participants` must be > 0   | **Blocker** |
| `V-KG2-004` | `user_decision` must be present                         | **Blocker** |

### Kill Gate 3 (Stage 3 → 4): Vertical Slice

| Rule ID     | Rule                                                                |  Severity   |
| :---------- | :------------------------------------------------------------------ | :---------: |
| `V-KG3-001` | `architecture_locked.adr_game_architecture_approved` must be `true` | **Blocker** |
| `V-KG3-002` | `architecture_locked.tsd_approved` must be `true`                   | **Blocker** |
| `V-KG3-003` | `architecture_locked.technology_decisions_locked` must be `true`    | **Blocker** |
| `V-KG3-004` | `user_decision` must be present                                     | **Blocker** |

### Kill Gate 4 (Stage 4 → 5): Production Planning

| Rule ID     | Rule                                                    |  Severity   |
| :---------- | :------------------------------------------------------ | :---------: |
| `V-KG4-001` | `production_plan.budget_approved` must be `true`        | **Blocker** |
| `V-KG4-002` | `production_plan.milestones_defined` must be `true`     | **Blocker** |
| `V-KG4-003` | `production_plan.risk_register_complete` must be `true` | **Blocker** |
| `V-KG4-004` | `user_decision` must be present                         | **Blocker** |

### Kill Gate 5 (Stage 8 → 9): Soft Launch Evaluation

| Rule ID     | Rule                                                         |  Severity   |
| :---------- | :----------------------------------------------------------- | :---------: |
| `V-KG5-001` | `security_gates_passed.cso_sign_off` must be `true`          | **Blocker** |
| `V-KG5-002` | `security_gates_passed.pen_test_passed` must be `true`       | **Blocker** |
| `V-KG5-003` | `security_gates_passed.gdpr_compliant` must be `true`        | **Blocker** |
| `V-KG5-004` | `soft_launch_metrics.crash_free_sessions_pct` must be ≥ 99.0 | **Blocker** |
| `V-KG5-005` | `user_decision` must be present                              | **Blocker** |

### Stage 10 — QBR

| Rule ID     | Rule                                               |  Severity   |
| :---------- | :------------------------------------------------- | :---------: | ------- | ----------- |
| `V-QBR-001` | All QBR scorecard metrics must be populated        | **Blocker** |
| `V-QBR-002` | `outcome_routing` must be one of: `full_investment | maintenance | sunset` | **Blocker** |

---

## 3. Validation Process

```
Stage N owner produces:
  1. stage-transition-summary.md (human-readable)
  2. schema-N-to-N+1.json (machine-readable)
      ↓
Studio Director validates schema:
  1. Parse JSON — reject if malformed
  2. Run universal rules (V-CG-001 through V-CG-006)
  3. Run kill gate rules if applicable (V-KGN-NNN)
  4. If any BLOCKER fails:
     → Reject handoff
     → Return error list to stage owner
     → Stage owner fixes and resubmits
  5. If only Warnings:
     → Log warnings
     → Allow handoff with advisory
  6. If all pass:
     → Submit kill-gate-report.md to User (if kill gate)
     → Advance to Stage N+1 on User approval
     → Archive schema JSON alongside stage-transition-summary.md
```

---

## 4. Pipeline Stage Trigger Table

|  Stage   | Validation Trigger                            | Schema Validated      |
| :------: | :-------------------------------------------- | :-------------------- |
|  0 → 1   | Studio Director completes art direction       | `schema-0-to-1.json`  |
|  1 → 2   | Studio Director submits KG-1 package          | `schema-1-to-2.json`  |
|  2 → 3   | Studio Director submits KG-2 package          | `schema-2-to-3.json`  |
|  3 → 4   | Studio Director submits KG-3 package          | `schema-3-to-4.json`  |
|  4 → 5   | Studio Director submits KG-4 package          | `schema-4-to-5.json`  |
|  5 → 6   | Lead Engineer submits production complete     | `schema-5-to-6.json`  |
|  6 → 7   | SDET Lead submits test results                | `schema-6-to-7.json`  |
|  7 → 8   | Studio Director submits soft launch prep      | `schema-7-to-8.json`  |
|  8 → 9   | Studio Director submits KG-5 package          | `schema-8-to-9.json`  |
|  9 → 10  | Studio Director submits global launch package | `schema-9-to-10.json` |
| 10 (QBR) | Live Ops Lead submits QBR report              | `schema-10-qbr.json`  |
