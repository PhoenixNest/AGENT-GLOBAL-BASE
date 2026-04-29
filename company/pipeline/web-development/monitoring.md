# Web Application Pipeline — Monitoring System

**Pipeline:** Web Application (P1)
**Version:** 1.0
**Effective Date:** April 13, 2026
**Owner:** Chief Technology Officer (CTO)
**Applicability:** All Web Application Pipeline projects from Stage 4 onward

---

## Overview

This monitoring system is specialized for the Web Application Pipeline. It follows the three-layer monitoring architecture (PROGRESS.md, session logs, checkpoint JSON) with web-specific fields, metrics, and recovery procedures.

### Why Standardized Monitoring Structure?

The three-layer monitoring architecture is shared across ALL company pipelines (Mobile, Web, Backend API, Full-Stack). This is **intentional governance design**, not copy-paste:

| Aspect                 | Why It's Standardized                                                                           | Why Content Differs                                                                                                                                |
| ---------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Three-layer structure  | Industry standard (Google SRE, Amazon Ops) — consistent tracking across all engineering domains | Each layer's **content** is platform-specific: PROGRESS.md has web fields, checkpoint.json has Lighthouse scores                                   |
| Session log format     | Universal audit trail convention — date/objectives/accomplishments are domain-agnostic          | Session **objectives** differ: web tracks component development/API integration/SEO; backend tracks endpoint implementation/migration/load testing |
| Checkpoint JSON schema | Consistent machine-readable milestone format enables cross-pipeline reporting                   | **Fields** differ: web tracks `bundle_size_kb`/`lighthouse_scores`/`seo_readiness`; backend tracks `endpoints_implemented`/`load_test_p99_ms`      |

This structure mirrors how leading technology companies (Google, Meta, Amazon) maintain **standardized governance frameworks** with **domain-specific content** across all engineering pipelines.

---

## Layer 1: PROGRESS.md (Real-Time State)

### Location

```
company/project/<project-name>/PROGRESS.md
```

### Web-Specific Fields

| Field               | Type   | Description                                                                             |
| ------------------- | ------ | --------------------------------------------------------------------------------------- |
| `pipeline_type`     | string | Always `"web-application"`                                                              |
| `web_strategy`      | string | SSR, CSR, PWA, or hybrid (from Web Strategy ADR)                                        |
| `track_structure`   | object | Track definitions (W-FE, W-BE, W-FS) with FULL/LIGHT/PRIMARY/Dormant status             |
| `performance_sla`   | object | LCP, FID, CLS, TTFB, TTI targets                                                        |
| `security_state`    | object | XSS prevention, CSRF tokens, CSP headers, OAuth 2.0 session integrity, dependency audit |
| `deployment_target` | string | Vercel (frontend) + AWS/Render (backend) + CDN                                          |

### Progress Tree Structure

```
Stage 5: Web Development
Overall: 65%
├── Web Frontend (Track W-FE — FULL): 80% (Amira Voss, 4 eng) — Ahead of schedule
├── Web Backend (Track W-BE — FULL): 55% (Dev Malhotra, 3 eng) — On track
├── Full-Stack Integration (Track W-FS — PRIMARY): 50% (Elena Vasquez, 4 eng) — API contract dependency
├── Track W-FE unused capacity: 0 engineers → all active
├── Track W-BE unused capacity: 1 engineer → reassigned to [API contract tests]
└── Track W-FS unused capacity: 0 engineers → all active
```

### Stage Status Table (Web Pipeline)

| Stage | Name                   | Status     | Entry Date | Exit Date | Artifacts Produced | User Approval? |
| ----- | ---------------------- | ---------- | ---------- | --------- | ------------------ | -------------- |
| 1     | Requirements           | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 2     | Design                 | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 3     | Architecture           | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 4     | Implementation Plan    | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 5     | Development            | ⚪ Pending | —          | —         | —                  | ❌ No          |
| 6     | Code Review            | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 7     | Automated Testing      | ⚪ Pending | —          | —         | —                  | ✅ Yes         |
| 8     | Integrity Verification | ⚪ Pending | —          | —         | —                  | ❌ No          |
| 9     | i18n Engineering       | ⚪ Pending | —          | —         | —                  | ❌ No          |
| 10    | Release Readiness      | ⚪ Pending | —          | —         | —                  | ✅ Yes         |

---

## Layer 2: Session Logs

### Location

```
company/project/<project-name>/sessions/session-<YYYYMMDD>-<HHMMSS>.md
```

### Web-Specific Session Objectives

| Category                    | Examples                                                              |
| --------------------------- | --------------------------------------------------------------------- |
| Component development       | React component creation, Vue component architecture                  |
| API endpoint implementation | REST/GraphQL endpoint development, middleware                         |
| E2E flow testing            | Playwright test scenarios, user journey validation                    |
| Performance optimization    | Bundle size reduction, Lighthouse score improvement, SSR optimization |
| Accessibility audit         | axe-core results, WCAG 2.1 AA compliance verification                 |
| CI/CD pipeline maintenance  | ESLint rule updates, deployment config changes                        |

---

## Layer 3: Checkpoint JSON

### Location

```
company/project/<project-name>/checkpoints/stage<N>-<status>.json
```

### Web-Specific Checkpoint Schema

```json
{
  "pipeline_type": "web-application",
  "stage": 5,
  "status": "in-progress",
  "progress_pct": 65,
  "web_strategy": "SSR",
  "track_breakdown": {
    "W-FE": {
      "status": "FULL",
      "progress_pct": 80,
      "owner": "Amira Voss",
      "engineers": 4
    },
    "W-BE": {
      "status": "FULL",
      "progress_pct": 55,
      "owner": "Dev Malhotra",
      "engineers": 3
    },
    "W-FS": {
      "status": "PRIMARY",
      "progress_pct": 50,
      "owner": "Elena Vasquez",
      "engineers": 4
    }
  },
  "milestone_history": [
    {
      "name": "Frontend components complete",
      "date": "2026-04-15",
      "progress_pct": 40
    },
    {
      "name": "API contract parity verified",
      "date": "2026-04-18",
      "progress_pct": 55
    }
  ],
  "performance_metrics": {
    "bundle_size_kb": 245,
    "lighthouse_scores": {
      "performance": 92,
      "accessibility": 96,
      "best_practices": 95,
      "seo": 88
    },
    "seo_readiness": "in-progress",
    "cdn_configured": true,
    "preview_deployed": true
  },
  "variance_tracking": {
    "W-FE": {
      "estimated_pct": 75,
      "actual_pct": 80,
      "variance": "+5%",
      "status": "ahead"
    },
    "W-BE": {
      "estimated_pct": 60,
      "actual_pct": 55,
      "variance": "-5%",
      "status": "on-track"
    },
    "W-FS": {
      "estimated_pct": 55,
      "actual_pct": 50,
      "variance": "-5%",
      "status": "on-track"
    }
  },
  "security_state": {
    "xss_prevention": "implemented",
    "csrf_tokens": "implemented",
    "csp_headers": "configured",
    "oauth2_session": "implemented",
    "dependency_audit": "clean"
  },
  "design_fidelity_checkpoint": {
    "completion_pct": 60,
    "pass_rate": 94,
    "status": "pass",
    "remediation_items": []
  },
  "string_extraction_readiness": {
    "audit_completed": false,
    "hardcoded_strings_found": 12,
    "threshold_pct": 5,
    "status": "pending"
  },
  "timestamp": "2026-04-20T14:30:00Z",
  "session_id": "session-20260420-143000"
}
```

---

## Design Fidelity Checkpoint Thresholds

At ~60% Stage 5 completion, the CDO conducts a formal Design Fidelity Checkpoint against the IDS:

| Pass Rate | Action                                                                                          |
| --------- | ----------------------------------------------------------------------------------------------- |
| ≥ 90%     | Proceed — no remediation needed                                                                 |
| 70–89%    | Proceed with documented remediation plan. CDO authorizes remediation tasks with deadlines.      |
| < 70%     | STOP. CTO notifies CPO. Stage 5 halts until design issues are resolved. Re-checkpoint required. |

---

## String Extraction Readiness Gate

Before Stage 6 entry, the Internationalization Specialist audits the codebase:

- Hardcoded strings are classified as **P2 defects** (or **P1 if core user flow affected**)
- Remaining hardcoded strings must be ≤ 5% of total string count
- Strings tracked in `key-index.csv` for web platform
- Placeholder integrity and truncation risk (>40% length increase) verified

---

## Recovery Scenarios

| Scenario                  | Recovery Procedure                                                                                                      |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Vercel deployment failure | Check deployment logs → rollback to last successful deploy → fix build config → redeploy                                |
| SSR hydration error       | Reproduce locally → identify component mismatch → fix SSR/CSR rendering discrepancy → test on staging                   |
| CDN cache invalidation    | Purge CDN cache → verify origin server serving latest → confirm CDN propagation                                         |
| API contract mismatch     | Compare frontend expectations with backend implementation → update OpenAPI spec or fix endpoint → re-run contract tests |
| Bundle size exceeds SLA   | Run bundle analyzer → identify large dependencies → implement code splitting or lazy loading → rebuild                  |
| Lighthouse regression     | Compare current vs. baseline scores → identify regression source → fix performance issue → re-test                      |

---

## Progress Sync Protocol

- Any track exceeding its estimated duration by **>20%** triggers an automatic CTO → CPO schedule risk notification
- The CTO produces weekly progress summaries for C-suite visibility
- Full specification: `company/pipeline/web-development/pipeline.md` — Search "Progress Sync Protocol"

---

## Agent Systems Engineering (ASE) — Governance Layer

In addition to the three-layer monitoring system above, all pipelines operate under the **ASE Framework** — a 4-layer governance methodology for multi-agent coordination. The ASE templates are co-located with the monitoring templates:

| ASE Template                            | Layer               | Purpose                                 |
| --------------------------------------- | ------------------- | --------------------------------------- |
| `STAGE-TRANSITION-SUMMARY.md`           | Context Engineering | Cross-stage context handoff             |
| `STAGE-TRANSITION-SCHEMAS.md`           | Harness Engineering | JSON schema contracts (`V-WEB-` prefix) |
| `SCHEMA-VALIDATION-SPEC.md`             | Harness Engineering | Automated validation rules              |
| `INTER-AGENT-COMMUNICATION-PROTOCOL.md` | Context + Harness   | Agent message formats and routing       |
| `MVC-CONTEXT-PROFILE.md`                | Context Engineering | Agent context window management         |
| `KNOWLEDGE-TRANSFER-PROTOCOL.md`        | RAG / Memory        | 3-tier learning loop                    |
| `RAG-INTEGRATION-BLUEPRINT.md`          | RAG / Memory        | Semantic retrieval architecture         |
| `ADR-ASE-001.md`                        | Governance          | ASE adoption decision record            |

> **Template location:** `company/pipeline/web-development/templates/monitoring/` and `templates/stage-6-code-review/`
> **Full ASE specification:** See `company/library/overview/pipeline.md` § Agent Systems Engineering (ASE) Framework.

---

## Related Documents

- **Pipeline Definition:** `company/pipeline/web-development/pipeline.md`
- **Progress Sync Protocol:** See "Progress Sync Protocol" section in pipeline.md
- **Project Directory Structure:** Refer to project root documentation
- **ASE Framework Templates:** `templates/monitoring/` (8 ASE templates + 3 base monitoring templates)
- **ASE Governance ADR:** `templates/monitoring/ADR-ASE-001.md`
