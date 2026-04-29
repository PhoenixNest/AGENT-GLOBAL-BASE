# Stage Transition Schemas — JSON Contract Definitions (Full-Stack Pipeline)

---

## Purpose

These schemas define the **mandatory structured output** for the full-stack pipeline. The full-stack pipeline uniquely operates across **three coordinated sub-tracks** (Mobile, Web, Backend), making its schemas the most complex. Each schema includes cross-track synchronization fields.

---

## Schema 1→2: Requirements → Design

```json
{
  "$schema": "fullstack/stage-transition/1-to-2",
  "version": "1.0.0",
  "stage_completed": 1,
  "stage_advancing_to": 2,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CPO + CSO", "role": "Requirements Authors" },
  "gate_result": "pass | pass_with_conditions | fail",
  "key_decisions": [{ "decision": "string", "source": "PRD §X | SRD §Y" }],
  "artifacts": {
    "prd": { "version": "v1", "path": "string", "req_count": 0 },
    "srd": { "version": "v1", "path": "string", "sec_req_count": 0 }
  },
  "platform_scope": {
    "mobile_ios": true,
    "mobile_android": true,
    "web_spa": true,
    "backend_api": true,
    "shared_logic": true
  },
  "constraints_forward": [
    { "constraint": "string", "source": "PRD | SRD", "ref": "§X" }
  ],
  "open_questions": [
    { "question": "string", "impact": "high | medium | low", "owner": "string" }
  ]
}
```

## Schema 3→4: Architecture → Implementation Plan

```json
{
  "$schema": "fullstack/stage-transition/3-to-4",
  "version": "1.0.0",
  "stage_completed": 3,
  "stage_advancing_to": 4,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO + CIO", "role": "Architecture Authors" },
  "gate_result": "pass | pass_with_conditions | fail",
  "key_decisions": [{ "decision": "string", "source": "ADR-NNN | TSD" }],
  "artifacts": {
    "uml_package": { "version": "v1", "path": "string", "diagram_count": 0 },
    "adrs": [
      {
        "id": "ADR-NNN",
        "title": "string",
        "path": "string",
        "decision": "string"
      }
    ],
    "tsd": { "version": "v1", "path": "string" }
  },
  "fullstack_strategy": {
    "track_fs_mobile": {
      "status": "full | light | dormant",
      "platforms": ["ios", "android"]
    },
    "track_fs_web": {
      "status": "full | light | dormant",
      "approach": "spa | ssr | pwa"
    },
    "track_fs_api": {
      "status": "full | light | dormant",
      "protocol": "rest | graphql | grpc"
    },
    "shared_modules": ["auth", "data", "analytics"],
    "team_size": 0
  },
  "cross_track_sync": {
    "api_contract_owner": "string",
    "shared_schema_path": "string",
    "sync_frequency": "per_sprint | per_milestone | daily"
  },
  "security_architecture": {
    "auth_mechanism": "string",
    "token_strategy": "string",
    "e2e_encryption": false,
    "stride_completed": false
  },
  "constraints_forward": [],
  "sign_offs": { "CTO": false, "CIO": false, "User": false }
}
```

## Schema 4→5: Implementation Plan → Development

```json
{
  "$schema": "fullstack/stage-transition/4-to-5",
  "version": "1.0.0",
  "stage_completed": 4,
  "stage_advancing_to": 5,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Implementation Planner" },
  "gate_result": "pass | pass_with_conditions | fail",
  "artifacts": {
    "implementation_plan": {
      "version": "v1",
      "path": "string",
      "task_count": 0
    },
    "gantt_chart": { "path": "string", "milestone_count": 0 },
    "rtm": {
      "path": "string",
      "prd_coverage_pct": 100,
      "srd_coverage_pct": 100
    },
    "sis": { "path": "string", "cso_signed": false }
  },
  "track_assignments": {
    "track_fs_mobile": {
      "ios_lead": "string",
      "android_lead": "string",
      "engineers": [],
      "status": "full | light | dormant"
    },
    "track_fs_web": {
      "lead": "string",
      "engineers": [],
      "status": "full | light | dormant"
    },
    "track_fs_api": {
      "lead": "string",
      "engineers": [],
      "status": "full | light | dormant"
    }
  },
  "integration_milestones": [
    {
      "id": "IM-NNN",
      "name": "string",
      "target_date": "YYYY-MM-DD",
      "tracks_involved": ["fs_mobile", "fs_web", "fs_api"],
      "integration_type": "api_contract | e2e_flow | performance"
    }
  ],
  "constraints_forward": [],
  "sign_offs": { "CTO": false, "User": false }
}
```

## Schema 5→6: Development → Code Review

```json
{
  "$schema": "fullstack/stage-transition/5-to-6",
  "version": "1.0.0",
  "stage_completed": 5,
  "stage_advancing_to": 6,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Development Overseer" },
  "gate_result": "pass | pass_with_conditions | fail",
  "artifacts": {
    "codebases": {
      "mobile": {
        "path": "string",
        "commit_hash": "string",
        "tag": "stage-5-mobile"
      },
      "web": {
        "path": "string",
        "commit_hash": "string",
        "tag": "stage-5-web"
      },
      "api": { "path": "string", "commit_hash": "string", "tag": "stage-5-api" }
    },
    "development_log": { "path": "string" },
    "integration_test_results": { "path": "string", "e2e_pass": true }
  },
  "completion_metrics": {
    "mobile_tasks_completed": 0,
    "mobile_tasks_total": 0,
    "web_tasks_completed": 0,
    "web_tasks_total": 0,
    "api_tasks_completed": 0,
    "api_tasks_total": 0,
    "cross_track_integration_pass": true,
    "string_extraction_readiness": "pass | remediation_needed",
    "hardcoded_strings_remaining": 0
  },
  "progress_sync": { "variance_alerts_fired": 0, "max_task_variance_pct": 0 },
  "constraints_forward": [],
  "sign_offs": { "CTO": false }
}
```

## Schema 6→7: Code Review → Testing

```json
{
  "$schema": "fullstack/stage-transition/6-to-7",
  "version": "1.0.0",
  "stage_completed": 6,
  "stage_advancing_to": 7,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Review Panel Convener" },
  "gate_result": "pass | pass_with_conditions | fail",
  "artifacts": {
    "defect_reports": {
      "mobile": { "path": "string" },
      "web": { "path": "string" },
      "api": { "path": "string" }
    },
    "red_team_report": { "path": "string", "version": "v1" },
    "code_review_signoff": { "path": "string" },
    "codebase_tags": {
      "mobile": "stage-6-mobile-baseline",
      "web": "stage-6-web-baseline",
      "api": "stage-6-api-baseline"
    }
  },
  "defect_summary": {
    "total": 0,
    "p0_resolved": 0,
    "p1_resolved": 0,
    "p2_deferred": 0,
    "p3_deferred": 0,
    "review_rounds": 0
  },
  "sign_offs": {
    "CPO": false,
    "CDO": false,
    "CTO": false,
    "CIO": false,
    "CSO": false,
    "red_team": false
  },
  "constraints_forward": [
    {
      "constraint": "Stage 6 codebase tags are the integrity baselines for Stage 8",
      "source": "ASE Red Team Protocol"
    }
  ]
}
```

## Schema 7→8, 8→9, 9→10, 10 Release

Schemas 7→8 through 10 follow the **same structure** as the Web pipeline with the addition of multi-codebase integrity tracking in 8→9. See `web-development/templates/monitoring/STAGE-TRANSITION-SCHEMAS.md` for canonical definitions; adapt the `$schema` prefix to `fullstack/`.

---

## Usage Rules

1. **Every stage gate must produce** a JSON file conforming to the appropriate schema.
2. **Cross-track integration milestones** (`IM-NNN`) are unique to full-stack and must be tracked separately from per-track milestones (`M-NNN`).
3. **Multiple codebase tags** are required at Stages 5→6 and 6→7 (one per track).
4. **`constraints_forward`** is cumulative — each stage appends, never removes.
5. **`sign_offs`** must all be `true` before the `gate_result` can be `"pass"`.
