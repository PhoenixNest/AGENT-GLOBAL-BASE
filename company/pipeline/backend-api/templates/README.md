# Pipeline Templates — Backend API

Ready-to-use templates for the 10-stage backend API pipeline and the Progress Monitoring & Recovery System. Templates are organized by pipeline stage.

---

## Directory Structure

```
templates/
├── README.md                                          ← this file
├── stage-1-requirements/
│   └── (API PRD + SRD templates)
├── stage-2-design/
│   └── (API Design: OpenAPI/GraphQL SDL/Protobuf)
├── stage-3-architecture/
│   └── (API ADRs: auth, rate limiting, data model)
├── stage-4-implementation-plan/
│   └── (Implementation Plan, RTM)
├── stage-5-development/
│   └── (Development Log)
├── stage-6-code-review/
│   ├── DEFECT-REPORT.md                               ← Defect Report
│   ├── RED-TEAM-REVIEW.md                             ← Red Team Adversarial Review Protocol
│   └── STAGE-TRANSITION-SUMMARY.md                    ← Stage 6 Transition Summary
├── stage-7-testing/
│   └── (Test Results, Load Testing, Contract Testing)
├── stage-8-integrity/
│   └── (Integrity Verification Sign-Off)
├── stage-9-i18n/
│   └── (String Extraction, Translation Verification)
├── stage-10-release/
│   └── (Release Checklist)
└── monitoring/
    ├── PROGRESS.md                                    ← Pipeline Progress Dashboard (Layer 1)
    ├── SESSION-LOG.md                                 ← Session Audit Trail (Layer 2)
    ├── checkpoint.json                                ← Machine-Readable Milestone (Layer 3)
    ├── STAGE-TRANSITION-SUMMARY.md                    ← Cross-Stage Context Handoff (ASE Phase 1)
    ├── STAGE-TRANSITION-SCHEMAS.md                    ← JSON Schema Contracts — API Adapted (ASE Phase 2)
    ├── INTER-AGENT-COMMUNICATION-PROTOCOL.md          ← IACP — Backend Routing (ASE Phase 2)
    ├── MVC-CONTEXT-PROFILE.md                         ← MVC Profile Template (ASE Phase 2)
    ├── KNOWLEDGE-TRANSFER-PROTOCOL.md                 ← 3-Tier Learning Loop (ASE Phase 3)
    ├── RAG-INTEGRATION-BLUEPRINT.md                   ← Semantic Retrieval Architecture (ASE Phase 3)
    ├── ADR-ASE-001.md                                 ← ASE Adoption Decision Record (ASE Phase 3)
    └── SCHEMA-VALIDATION-SPEC.md                      ← Automated Gate Enforcement — V-API- Rules (ASE Phase 3)
```

---

## Quick Reference by Stage

| Stage                   | Templates                                                                                                                                                                                                                                                                                            | Count |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| 1 — Requirements        | `PRD.md`, `SRD.md`                                                                                                                                                                                                                                                                                   | 2     |
| 2 — Design              | `API-SPECIFICATION.md` (OpenAPI/GraphQL SDL/Protobuf)                                                                                                                                                                                                                                                | 1     |
| 3 — Architecture        | ADR templates (API strategy, data modeling, auth), `TSD.md`                                                                                                                                                                                                                                          | TBD   |
| 4 — Implementation Plan | `IMPLEMENTATION-PLAN.md`, `RTM.md`                                                                                                                                                                                                                                                                   | 2     |
| 5 — Development         | `DEVELOPMENT-LOG.md`                                                                                                                                                                                                                                                                                 | 1     |
| 6 — Code Review         | `DEFECT-REPORT.md`, `RED-TEAM-REVIEW.md`, `STAGE-TRANSITION-SUMMARY.md`                                                                                                                                                                                                                              | 3     |
| 7 — Testing             | `TEST-RESULTS-REPORT.md`, `LOAD-TEST-REPORT.md`, `CONTRACT-TEST-REPORT.md`                                                                                                                                                                                                                           | 3     |
| 8 — Integrity           | `INTEGRITY-SIGNOFF.md`                                                                                                                                                                                                                                                                               | 1     |
| 9 — i18n                | `STRING-EXTRACTION-HANDOFF.md`, `TRANSLATION-VERIFICATION-REPORT.md`                                                                                                                                                                                                                                 | 2     |
| 10 — Release            | `RELEASE-CHECKLIST.md`                                                                                                                                                                                                                                                                               | 1     |
| Monitoring (all stages) | `PROGRESS.md`, `SESSION-LOG.md`, `checkpoint.json`, `STAGE-TRANSITION-SUMMARY.md`, `STAGE-TRANSITION-SCHEMAS.md`, `INTER-AGENT-COMMUNICATION-PROTOCOL.md`, `MVC-CONTEXT-PROFILE.md`, `KNOWLEDGE-TRANSFER-PROTOCOL.md`, `RAG-INTEGRATION-BLUEPRINT.md`, `ADR-ASE-001.md`, `SCHEMA-VALIDATION-SPEC.md` | 11    |

---

## Monitoring Templates

| Template                                | Layer      | ASE Phase | Domain Adaptation  |
| --------------------------------------- | ---------- | --------- | :----------------: |
| `PROGRESS.md`                           | Layer 1    | —         |    ✅ Inherited    |
| `SESSION-LOG.md`                        | Layer 2    | —         |    ✅ Inherited    |
| `checkpoint.json`                       | Layer 3    | —         |    ✅ Inherited    |
| `STAGE-TRANSITION-SUMMARY.md`           | ASE — L2   | Phase 1   |    ✅ Portable     |
| `STAGE-TRANSITION-SCHEMAS.md`           | ASE — L2   | Phase 2   |   🔧 API-adapted   |
| `INTER-AGENT-COMMUNICATION-PROTOCOL.md` | ASE — L2/3 | Phase 2   |   🔧 API-adapted   |
| `MVC-CONTEXT-PROFILE.md`                | ASE — L2   | Phase 2   |    ✅ Portable     |
| `KNOWLEDGE-TRANSFER-PROTOCOL.md`        | ASE — L3   | Phase 3   |    ✅ Portable     |
| `RAG-INTEGRATION-BLUEPRINT.md`          | ASE — L4   | Phase 3   |    ✅ Portable     |
| `ADR-ASE-001.md`                        | ASE — Gov  | Phase 3   |    ✅ Portable     |
| `SCHEMA-VALIDATION-SPEC.md`             | ASE — L3   | Phase 3   | 🔧 V-API- prefixed |
| `RED-TEAM-REVIEW.md` (stage-6)          | ASE — L3   | Phase 3   |    ✅ Portable     |

**Domain-adapted templates** contain API-specific fields: API type (REST/GraphQL/gRPC), contract testing, load testing (P99 latency), OpenAPI/GraphQL SDL/Protobuf spec, rate limiting, and B-API/B-DATA/B-INFRA track assignments.

**Validation Rule Prefix:** `V-API-NNN` (see SCHEMA-VALIDATION-SPEC.md)

---

## Usage

1. Copy the template to your project directory under the appropriate stage folder
2. Replace all `[bracketed placeholders]` with project-specific content
3. Follow the structure — all sections are mandatory unless marked optional
4. Version each artifact per the project versioning convention
