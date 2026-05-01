# Stage Transition Schemas — JSON Contract Definitions (Backend API Pipeline)

---

## Purpose

These schemas define the **mandatory structured output** that each pipeline stage must produce when passing artifacts to the next stage. Adapted for the Backend API pipeline with API-specific fields (protocol type, contract testing, load testing, API gateway).

---

## Schema 1→2: Requirements → Design

```json
{
  "$schema": "api/stage-transition/1-to-2",
  "version": "1.0.0",
  "stage_completed": 1,
  "stage_advancing_to": 2,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "VP API + CSO", "role": "Requirements Authors" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "key_decisions": [{ "decision": "string", "source": "PRD §X | SRD §Y" }],
  "artifacts": {
    "prd": { "version": "v1", "path": "string", "req_count": 0 },
    "srd": { "version": "v1", "path": "string", "sec_req_count": 0 }
  },
  "api_type": "REST | GraphQL | gRPC | event_driven",
  "constraints_forward": [
    { "constraint": "string", "source": "PRD | SRD", "ref": "§X" }
  ],
  "open_questions": [
    { "question": "string", "impact": "high | medium | low", "owner": "string" }
  ]
}
```

## Schema 2→3: Design → Architecture

```json
{
  "$schema": "api/stage-transition/2-to-3",
  "version": "1.0.0",
  "stage_completed": 2,
  "stage_advancing_to": 3,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CDO", "role": "Design Lead" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "key_decisions": [{ "decision": "string", "source": "IDS §X" }],
  "artifacts": {
    "prototype": {
      "version": "v1",
      "path": "string",
      "format": "HTML | OpenAPI"
    },
    "ids": {
      "version": "v1",
      "path": "string",
      "endpoint_count": 0,
      "data_model_count": 0
    }
  },
  "api_design": {
    "versioning_strategy": "string",
    "pagination_model": "string",
    "error_format": "RFC 7807 | custom"
  },
  "constraints_forward": [],
  "sign_offs": { "CPO": false, "CIO": false, "CTO": false, "CDO": false }
}
```

## Schema 3→4: Architecture → Implementation Plan

```json
{
  "$schema": "api/stage-transition/3-to-4",
  "version": "1.0.0",
  "stage_completed": 3,
  "stage_advancing_to": 4,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO + CIO", "role": "Architecture Authors" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
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
  "api_strategy": {
    "approach": "rest | graphql | grpc | event_driven",
    "track_b_api": "full | light | dormant",
    "track_b_data": "full | light | dormant",
    "track_b_infra": "full | light | dormant",
    "team_size": 0
  },
  "security_architecture": {
    "auth_mechanism": "OAuth2 | JWT | API Key | mTLS",
    "rate_limiting": "string",
    "input_validation": "string",
    "stride_completed": false
  },
  "constraints_forward": [],
  "sign_offs": { "CTO": false, "CIO": false, "User": false }
}
```

## Schema 4→5: Implementation Plan → Development

```json
{
  "$schema": "api/stage-transition/4-to-5",
  "version": "1.0.0",
  "stage_completed": 4,
  "stage_advancing_to": 5,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Implementation Planner" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
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
  "technology_decision_registry": [
    { "adr_id": "ADR-NNN", "compliant": true, "notes": "string" }
  ],
  "track_assignments": {
    "track_b_api": {
      "lead": "string",
      "engineers": [],
      "status": "full | light | dormant"
    },
    "track_b_data": {
      "lead": "string",
      "engineers": [],
      "status": "full | light | dormant"
    },
    "track_b_infra": {
      "lead": "string",
      "engineers": [],
      "status": "full | light | dormant"
    }
  },
  "milestones": [
    {
      "id": "M-NNN",
      "name": "string",
      "target_date": "YYYY-MM-DD",
      "dependencies": []
    }
  ],
  "constraints_forward": [],
  "sign_offs": { "CTO": false, "User": false }
}
```

## Schema 5→6: Development → Code Review

```json
{
  "$schema": "api/stage-transition/5-to-6",
  "version": "1.0.0",
  "stage_completed": 5,
  "stage_advancing_to": 6,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Development Overseer" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "artifacts": {
    "codebase": {
      "path": "string",
      "commit_hash": "string",
      "tag": "stage-5-complete"
    },
    "development_log": { "path": "string" },
    "api_specification": {
      "path": "string",
      "format": "OpenAPI | GraphQL SDL | Protobuf"
    }
  },
  "completion_metrics": {
    "tasks_completed": 0,
    "tasks_total": 0,
    "api_coverage_pct": 0,
    "contract_tests_pass": true,
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
  "$schema": "api/stage-transition/6-to-7",
  "version": "1.0.0",
  "stage_completed": 6,
  "stage_advancing_to": 7,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Review Panel Convener" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "artifacts": {
    "defect_report": { "path": "string", "version": "v1" },
    "red_team_report": { "path": "string", "version": "v1" },
    "code_review_signoff": { "path": "string" },
    "codebase_tag": "stage-6-baseline"
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
      "constraint": "Stage 6 codebase tag is the integrity baseline for Stage 8",
      "source": "ASE Red Team Protocol"
    }
  ]
}
```

## Schema 7→8: Testing → Integrity Verification

```json
{
  "$schema": "api/stage-transition/7-to-8",
  "version": "1.0.0",
  "stage_completed": 7,
  "stage_advancing_to": 8,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Test Overseer" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "artifacts": {
    "test_results": { "path": "string", "version": "v1" },
    "load_test_results": { "path": "string" },
    "contract_test_results": { "path": "string" }
  },
  "test_summary": {
    "total_tests": 0,
    "passed": 0,
    "failed": 0,
    "pass_rate_pct": 100,
    "regression_pass": true,
    "dast_high_findings": 0,
    "pentest_critical": 0,
    "pentest_high": 0,
    "accessibility_p0": 0,
    "performance_failures": 0,
    "load_test_p99_ms": 0,
    "contract_test_pass": true
  },
  "bugs_remediated": [
    {
      "id": "BUG-NNN",
      "severity": "P0-P3",
      "status": "fixed | deferred",
      "regression_verified": true
    }
  ],
  "constraints_forward": [
    {
      "constraint": "No functionality may be removed to achieve test pass",
      "source": "agent-behavioral-constraints.md"
    }
  ]
}
```

## Schema 8→9, 9→10, 10 Release

These schemas are **structurally identical** to the Web pipeline schemas (no API-specific changes needed for i18n and release stages). See `web-development/templates/monitoring/stage-transition-schemas.md` for the canonical 8→9, 9→10, and 10-release schemas; adapt the `$schema` prefix to `api/`.

---

## Usage Rules

1. **Every stage gate must produce** a JSON file conforming to the appropriate schema.
2. **The receiving stage agent validates** the schema before processing — reject malformed handoffs.
3. **Schemas are versioned** — breaking changes require a new `version` field and a corresponding ADR.
4. **`constraints_forward`** is cumulative — each stage appends, never removes.
5. **`sign_offs`** must all be `true` before the `gate_result` can be `"pass"`.
