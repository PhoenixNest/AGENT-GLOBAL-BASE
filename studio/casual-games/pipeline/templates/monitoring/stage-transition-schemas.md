# Stage Transition Schemas — Casual Games Studio

> **ASE Layer:** 3 — Harness Engineering (gate automation) + Layer 2 — Context Engineering (handoff contracts)
> **Authority:** Studio Director Dr. Marcus Vogel
> **Reference:** `core-component-00/engineering/multi-agent-engineering/implementations/handoff_packet.py`

This document defines the **JSON schema contracts** for every stage transition and kill gate in the Casual Games Studio 11-stage pipeline. Each schema is the machine-readable counterpart to the human-readable `stage-transition-summary.md`.

---

## Schema Registry

| Transition                | Schema File           | Kill Gate | User Approval Required |
| :------------------------ | :-------------------- | :-------: | :--------------------: |
| Stage 0 → 1               | `schema-0-to-1.json`  |     —     |           ❌           |
| Stage 1 → 2 (Kill Gate 1) | `schema-1-to-2.json`  |   KG-1    |           ✅           |
| Stage 2 → 3 (Kill Gate 2) | `schema-2-to-3.json`  |   KG-2    |           ✅           |
| Stage 3 → 4 (Kill Gate 3) | `schema-3-to-4.json`  |   KG-3    |           ✅           |
| Stage 4 → 5 (Kill Gate 4) | `schema-4-to-5.json`  |   KG-4    |           ✅           |
| Stage 5 → 6               | `schema-5-to-6.json`  |     —     |           ❌           |
| Stage 6 → 7               | `schema-6-to-7.json`  |     —     |           ✅           |
| Stage 7 → 8               | `schema-7-to-8.json`  |     —     |           ✅           |
| Stage 8 → 9 (Kill Gate 5) | `schema-8-to-9.json`  |   KG-5    |           ✅           |
| Stage 9 → 10              | `schema-9-to-10.json` |     —     |           ✅           |
| Stage 10 (QBR)            | `schema-10-qbr.json`  |     —     |          QBR           |

---

## Universal Schema Fields (All Transitions)

Every schema file must include these top-level fields:

```json
{
  "schema_version": "1.0",
  "pipeline": "casual-games",
  "stage_from": 0,
  "stage_to": 1,
  "transition_date": "YYYY-MM-DD",
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "kill_gate": null,
  "sign_offs": {
    "stage_owner": true,
    "studio_director": true,
    "user_approved": false
  },
  "constraints_forward": [],
  "produced_by": {
    "agent": "role-name",
    "division": "division-name"
  }
}
```

---

## Kill Gate Schema Extensions

### Kill Gate 1 (Stage 1 → 2): Concept Validation

```json
{
  "kill_gate": "KG-1",
  "concept_validation": {
    "gdd_complete": true,
    "prd_complete": true,
    "srd_complete": true,
    "core_loop_defined": true,
    "target_audience_defined": true
  },
  "kill_gate_criteria": {
    "market_opportunity_score": 0,
    "concept_novelty_score": 0,
    "technical_feasibility_score": 0,
    "minimum_threshold_met": false
  },
  "user_decision": "proceed | iterate | kill"
}
```

### Kill Gate 2 (Stage 2 → 3): Prototype Validation

```json
{
  "kill_gate": "KG-2",
  "prototype_metrics": {
    "d1_retention_pct": 0,
    "session_length_minutes": 0,
    "fun_factor_score": 0,
    "playtest_participants": 0
  },
  "build_criteria": {
    "playable_build_complete": true,
    "gds_complete": true,
    "core_mechanics_implemented": true
  },
  "user_decision": "proceed | iterate | kill"
}
```

### Kill Gate 3 (Stage 3 → 4): Vertical Slice

```json
{
  "kill_gate": "KG-3",
  "vertical_slice_metrics": {
    "d1_retention_pct": 0,
    "d7_retention_pct": 0,
    "fun_factor_score": 0,
    "polish_level": "alpha | beta | release_candidate"
  },
  "architecture_locked": {
    "adr_game_architecture_approved": true,
    "tsd_approved": true,
    "technology_decisions_locked": true
  },
  "user_decision": "proceed | iterate | kill"
}
```

### Kill Gate 4 (Stage 4 → 5): Production Planning

```json
{
  "kill_gate": "KG-4",
  "production_plan": {
    "milestones_defined": true,
    "team_allocated": true,
    "budget_approved": true,
    "risk_register_complete": true,
    "gantt_approved": true
  },
  "user_decision": "proceed | iterate | kill"
}
```

### Kill Gate 5 (Stage 8 → 9): Soft Launch Evaluation

```json
{
  "kill_gate": "KG-5",
  "soft_launch_metrics": {
    "d1_retention_pct": 0,
    "d30_retention_pct": 0,
    "mau": 0,
    "arpdau": 0,
    "crash_free_sessions_pct": 0,
    "market_tier": "A | B | C"
  },
  "security_gates_passed": {
    "cso_sign_off": true,
    "pen_test_passed": true,
    "gdpr_compliant": true
  },
  "user_decision": "global_launch | extend_soft_launch | pivot | kill"
}
```

---

## Validation Rules

| Rule ID    | Applies To     | Rule                                                                    |  Severity   |
| :--------- | :------------- | :---------------------------------------------------------------------- | :---------: |
| `V-CG-001` | All            | `gate_result` must be `"pass"` or `"pass_with_conditions"`              | **Blocker** |
| `V-CG-002` | All            | All `sign_offs` must be `true`                                          | **Blocker** |
| `V-CG-003` | All kill gates | `user_decision` must be present                                         | **Blocker** |
| `V-CG-004` | KG-1           | All concept validation fields must be `true`                            | **Blocker** |
| `V-CG-005` | KG-2           | `playtest_participants` must be > 0                                     | **Blocker** |
| `V-CG-006` | KG-3           | `technology_decisions_locked` must be `true`                            | **Blocker** |
| `V-CG-007` | KG-4           | `budget_approved` must be `true`                                        | **Blocker** |
| `V-CG-008` | KG-5           | `cso_sign_off` must be `true`                                           | **Blocker** |
| `V-CG-009` | KG-5           | All 12 QBR `checklist` domain items must have `passed: true` (Stage 10) | **Blocker** |
| `V-CG-010` | All            | `constraints_forward` must carry forward all prior stage constraints    | **Blocker** |
