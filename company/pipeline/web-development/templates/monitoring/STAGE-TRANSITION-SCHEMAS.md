# Stage Transition Schemas — JSON Contract Definitions (Web Pipeline)

---

## Purpose

These schemas define the **mandatory structured output** that each pipeline stage must produce when passing artifacts to the next stage. They replace implicit, unstructured handoffs with explicit contracts that agents can validate before processing.

Each schema is designed to be **machine-parseable** (JSON) while remaining **human-readable** as a reference.

---

## Schema 1→2: Requirements → Design

```json
{
  "$schema": "web/stage-transition/1-to-2",
  "version": "1.0.0",
  "stage_completed": 1,
  "stage_advancing_to": 2,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "VP Web + CSO", "role": "Requirements Authors" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "key_decisions": [{ "decision": "string", "source": "PRD §X | SRD §Y" }],
  "artifacts": {
    "prd": { "version": "v1", "path": "string", "req_count": 0 },
    "srd": { "version": "v1", "path": "string", "sec_req_count": 0 }
  },
  "target_delivery_model": "SPA | SSR | PWA | hybrid",
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
  "$schema": "web/stage-transition/2-to-3",
  "version": "1.0.0",
  "stage_completed": 2,
  "stage_advancing_to": 3,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CDO", "role": "Design Lead" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "key_decisions": [{ "decision": "string", "source": "IDS §X" }],
  "artifacts": {
    "prototype": { "version": "v1", "path": "string", "format": "HTML" },
    "ids": {
      "version": "v1",
      "path": "string",
      "screen_count": 0,
      "interaction_count": 0
    }
  },
  "design_system": {
    "typography": "string",
    "color_palette": "string",
    "responsive_breakpoints": ["mobile", "tablet", "desktop"],
    "accessibility_standard": "WCAG 2.1 AA"
  },
  "constraints_forward": [],
  "sign_offs": { "CPO": false, "CIO": false, "CTO": false, "CDO": false }
}
```

## Schema 3→4: Architecture → Implementation Plan

```json
{
  "$schema": "web/stage-transition/3-to-4",
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
  "web_strategy": {
    "approach": "spa | ssr | pwa | hybrid",
    "track_w_fe": "full | light | dormant",
    "track_w_be": "full | light | dormant",
    "track_w_fs": "full | light | dormant",
    "team_size": 0
  },
  "security_architecture": {
    "auth_mechanism": "string",
    "csp_policy": "string",
    "cors_strategy": "string",
    "stride_completed": false
  },
  "constraints_forward": [],
  "sign_offs": { "CTO": false, "CIO": false, "User": false }
}
```

## Schema 4→5: Implementation Plan → Development

```json
{
  "$schema": "web/stage-transition/4-to-5",
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
    "track_w_fe": {
      "lead": "string",
      "engineers": [],
      "status": "full | light | dormant"
    },
    "track_w_be": {
      "lead": "string",
      "engineers": [],
      "status": "full | light | dormant"
    },
    "track_w_fs": {
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
  "$schema": "web/stage-transition/5-to-6",
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
    "lighthouse_audit": { "path": "string", "applicable": true }
  },
  "completion_metrics": {
    "tasks_completed": 0,
    "tasks_total": 0,
    "design_fidelity_pct": 0,
    "string_extraction_readiness": "pass | remediation_needed",
    "hardcoded_strings_remaining": 0,
    "lighthouse_scores": {
      "performance": 0,
      "accessibility": 0,
      "best_practices": 0,
      "seo": 0
    }
  },
  "progress_sync": {
    "variance_alerts_fired": 0,
    "max_task_variance_pct": 0
  },
  "constraints_forward": [],
  "sign_offs": { "CTO": false }
}
```

## Schema 6→7: Code Review → Testing

```json
{
  "$schema": "web/stage-transition/6-to-7",
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
  "$schema": "web/stage-transition/7-to-8",
  "version": "1.0.0",
  "stage_completed": 7,
  "stage_advancing_to": 8,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Test Overseer" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "artifacts": {
    "test_results": { "path": "string", "version": "v1" },
    "performance_benchmarks": { "path": "string" },
    "browser_matrix": { "path": "string" }
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
    "lighthouse_regression": false
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

## Schema 8→9: Integrity → i18n Engineering

```json
{
  "$schema": "web/stage-transition/8-to-9",
  "version": "1.0.0",
  "stage_completed": 8,
  "stage_advancing_to": 9,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Integrity Panel Convener" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "artifacts": {
    "integrity_signoff": { "path": "string" },
    "codebase_tag": "stage-8-verified"
  },
  "integrity_checks": {
    "prd_features_intact": true,
    "ids_conformance_pct": 0,
    "uml_standards_upheld": true,
    "srd_security_enforced": true,
    "security_control_weakened": false,
    "analytics_integrity": true
  },
  "sign_offs": {
    "CPO": false,
    "CDO": false,
    "CTO": false,
    "CIO": false,
    "CSO": false,
    "brand_design": false,
    "rd": false
  },
  "target_languages": ["en", "zh", "ja", "ko", "fr"],
  "constraints_forward": [
    { "constraint": "String Key Taxonomy per ADR-NNN", "source": "Stage 3 ADR" }
  ]
}
```

## Schema 9→10: i18n → Release Readiness

```json
{
  "$schema": "web/stage-transition/9-to-10",
  "version": "1.0.0",
  "stage_completed": 9,
  "stage_advancing_to": 10,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO-L", "role": "Chief Translation Officer" },
  "gate_result": "pass | pass_with_conditions | fail",
  "harness_compliance_verified": true,
  "artifacts": {
    "localized_codebase": { "path": "string", "tag": "stage-9-localized" },
    "translation_verification": { "path": "string" },
    "string_extraction_handoff": { "path": "string" }
  },
  "i18n_summary": {
    "total_strings": 0,
    "languages_completed": [],
    "hardcoded_strings_remaining": 0,
    "bleu_scores": { "en": 0.0, "zh": 0.0, "ja": 0.0, "ko": 0.0, "fr": 0.0 },
    "structural_review_pass": true
  },
  "sign_offs": {
    "CPO_structural": false,
    "CDO_structural": false,
    "CTO_structural": false,
    "CTO_L_translation": false
  },
  "constraints_forward": []
}
```

## Schema: Stage 10 Release Decision (Terminal)

```json
{
  "$schema": "web/stage-transition/10-release",
  "version": "1.0.0",
  "stage_completed": 10,
  "completed_date": "YYYY-MM-DD",
  "produced_by": { "agent": "CTO", "role": "Release Panel Convener" },
  "release_decision": "approved | rejected | deferred",
  "harness_compliance_verified": true,
  "checklist": [
    {
      "domain": "Product",
      "criteria": "All PRD implemented",
      "sign_off": "CPO + VP Web",
      "passed": false
    },
    {
      "domain": "Design",
      "criteria": "All IDS realized, responsive verified",
      "sign_off": "CDO",
      "passed": false
    },
    {
      "domain": "Architecture",
      "criteria": "All ADR/TSD upheld",
      "sign_off": "CTO+CIO",
      "passed": false
    },
    {
      "domain": "Security",
      "criteria": "SRD enforced, CSP/CORS compliant",
      "sign_off": "CSO",
      "passed": false
    },
    {
      "domain": "Testing",
      "criteria": "100% automated pass, Lighthouse thresholds met",
      "sign_off": "CTO",
      "passed": false
    },
    {
      "domain": "Localization",
      "criteria": "All languages verified",
      "sign_off": "CTO-L",
      "passed": false
    },
    {
      "domain": "Platform",
      "criteria": "Deployment target ready (Vercel/CDN/hosting)",
      "sign_off": "CTO+CPO",
      "passed": false
    }
  ],
  "user_decision": "release | hold | cancel",
  "user_decision_date": "YYYY-MM-DD"
}
```

---

## Usage Rules

1. **Every stage gate must produce** a JSON file conforming to the appropriate schema.
2. **The receiving stage agent validates** the schema before processing — reject malformed handoffs.
3. **Schemas are versioned** — breaking changes require a new `version` field and a corresponding ADR.
4. **`constraints_forward`** is cumulative — each stage appends, never removes.
5. **`sign_offs`** must all be `true` before the `gate_result` can be `"pass"`.
