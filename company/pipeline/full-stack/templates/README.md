# Pipeline Templates — Full-Stack Cross-Platform

Ready-to-use templates for the 10-stage full-stack pipeline and the Progress Monitoring & Recovery System. Templates are organized by pipeline stage.

---

## Directory Structure

```
templates/
├── README.md                                          ← this file
├── stage-1-requirements/
│   └── (Full-Stack PRD + SRD — multi-platform scope)
├── stage-2-design/
│   └── (Multi-platform IDS: iOS, Android, Web)
├── stage-3-architecture/
│   └── (Cross-platform ADRs, shared modules, API contracts)
├── stage-4-implementation-plan/
│   └── (Implementation Plan, RTM, Integration Milestones)
├── stage-5-development/
│   └── (Development Log — per track)
├── stage-6-code-review/
│   ├── DEFECT-REPORT.md                               ← Defect Report (per codebase)
│   ├── RED-TEAM-REVIEW.md                             ← Red Team Adversarial Review Protocol
│   └── STAGE-TRANSITION-SUMMARY.md                    ← Stage 6 Transition Summary
├── stage-7-testing/
│   └── (Test Results — per track + E2E integration)
├── stage-8-integrity/
│   └── (Integrity Verification — multi-codebase)
├── stage-9-i18n/
│   └── (String Extraction, Translation Verification)
├── stage-10-release/
│   └── (Release Checklist — coordinated multi-platform)
└── monitoring/
    ├── PROGRESS.md                                    ← Pipeline Progress Dashboard (Layer 1)
    ├── SESSION-LOG.md                                 ← Session Audit Trail (Layer 2)
    ├── checkpoint.json                                ← Machine-Readable Milestone (Layer 3)
    ├── STAGE-TRANSITION-SUMMARY.md                    ← Cross-Stage Context Handoff (ASE Phase 1)
    ├── STAGE-TRANSITION-SCHEMAS.md                    ← JSON Schema Contracts — Full-Stack Adapted (ASE Phase 2)
    ├── INTER-AGENT-COMMUNICATION-PROTOCOL.md          ← IACP — Cross-Track Routing (ASE Phase 2)
    ├── MVC-CONTEXT-PROFILE.md                         ← MVC Profile Template (ASE Phase 2)
    ├── KNOWLEDGE-TRANSFER-PROTOCOL.md                 ← 3-Tier Learning Loop (ASE Phase 3)
    ├── RAG-INTEGRATION-BLUEPRINT.md                   ← Semantic Retrieval Architecture (ASE Phase 3)
    ├── ADR-ASE-001.md                                 ← ASE Adoption Decision Record (ASE Phase 3)
    └── SCHEMA-VALIDATION-SPEC.md                      ← Automated Gate Enforcement — V-FS- Rules (ASE Phase 3)
```

---

## Quick Reference by Stage

| Stage                   | Templates                                                                                                                                                                                                                                                                                            | Count |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| 1 — Requirements        | `PRD.md`, `SRD.md`                                                                                                                                                                                                                                                                                   | 2     |
| 2 — Design              | `IDS.md` (multi-platform responsive specs)                                                                                                                                                                                                                                                           | 1     |
| 3 — Architecture        | ADR templates (cross-platform strategy, API contracts, shared modules), `TSD.md`                                                                                                                                                                                                                     | TBD   |
| 4 — Implementation Plan | `IMPLEMENTATION-PLAN.md`, `RTM.md`                                                                                                                                                                                                                                                                   | 2     |
| 5 — Development         | `DEVELOPMENT-LOG.md` (per track: Web, Mobile, API)                                                                                                                                                                                                                                                   | 3     |
| 6 — Code Review         | `DEFECT-REPORT.md`, `RED-TEAM-REVIEW.md`, `STAGE-TRANSITION-SUMMARY.md`                                                                                                                                                                                                                              | 3     |
| 7 — Testing             | `TEST-RESULTS-REPORT.md`, `INTEGRATION-TEST-REPORT.md`, `E2E-TEST-REPORT.md`                                                                                                                                                                                                                         | 3     |
| 8 — Integrity           | `INTEGRITY-SIGNOFF.md`                                                                                                                                                                                                                                                                               | 1     |
| 9 — i18n                | `STRING-EXTRACTION-HANDOFF.md`, `TRANSLATION-VERIFICATION-REPORT.md`                                                                                                                                                                                                                                 | 2     |
| 10 — Release            | `RELEASE-CHECKLIST.md` (coordinated multi-platform)                                                                                                                                                                                                                                                  | 1     |
| Monitoring (all stages) | `PROGRESS.md`, `SESSION-LOG.md`, `checkpoint.json`, `STAGE-TRANSITION-SUMMARY.md`, `STAGE-TRANSITION-SCHEMAS.md`, `INTER-AGENT-COMMUNICATION-PROTOCOL.md`, `MVC-CONTEXT-PROFILE.md`, `KNOWLEDGE-TRANSFER-PROTOCOL.md`, `RAG-INTEGRATION-BLUEPRINT.md`, `ADR-ASE-001.md`, `SCHEMA-VALIDATION-SPEC.md` | 11    |

---

## Monitoring Templates

| Template                                | Layer      | ASE Phase |   Domain Adaptation    |
| --------------------------------------- | ---------- | --------- | :--------------------: |
| `PROGRESS.md`                           | Layer 1    | —         |      ✅ Inherited      |
| `SESSION-LOG.md`                        | Layer 2    | —         |      ✅ Inherited      |
| `checkpoint.json`                       | Layer 3    | —         |      ✅ Inherited      |
| `STAGE-TRANSITION-SUMMARY.md`           | ASE — L2   | Phase 1   |      ✅ Portable       |
| `STAGE-TRANSITION-SCHEMAS.md`           | ASE — L2   | Phase 2   | 🔧 Full-Stack adapted  |
| `INTER-AGENT-COMMUNICATION-PROTOCOL.md` | ASE — L2/3 | Phase 2   | 🔧 Cross-track adapted |
| `MVC-CONTEXT-PROFILE.md`                | ASE — L2   | Phase 2   |      ✅ Portable       |
| `KNOWLEDGE-TRANSFER-PROTOCOL.md`        | ASE — L3   | Phase 3   |      ✅ Portable       |
| `RAG-INTEGRATION-BLUEPRINT.md`          | ASE — L4   | Phase 3   |      ✅ Portable       |
| `ADR-ASE-001.md`                        | ASE — Gov  | Phase 3   |      ✅ Portable       |
| `SCHEMA-VALIDATION-SPEC.md`             | ASE — L3   | Phase 3   |   🔧 V-FS- prefixed    |
| `RED-TEAM-REVIEW.md` (stage-6)          | ASE — L3   | Phase 3   |      ✅ Portable       |

**Domain-adapted templates** contain full-stack-specific fields: multi-platform scope, cross-track synchronization protocol, integration milestones (IM-NNN), multiple codebase tags (mobile/web/api), and FS-MOBILE/FS-WEB/FS-API track assignments.

**Unique to Full-Stack:** Integration Checkpoint Message format in IACP, cross-track conflict resolution protocol, API Contract Lock sync point.

**Validation Rule Prefix:** `V-FS-NNN` (see SCHEMA-VALIDATION-SPEC.md)

---

## Usage

1. Copy the template to your project directory under the appropriate stage folder
2. Replace all `[bracketed placeholders]` with project-specific content
3. Follow the structure — all sections are mandatory unless marked optional
4. Version each artifact per the project versioning convention
