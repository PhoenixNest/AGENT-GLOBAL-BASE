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
└── STAGE-TRANSITION-SUMMARY.md                    ← Stage 6 Transition Summary
├── stage-7-testing/
│   └── (Test Results — per track + E2E integration)
├── stage-8-integrity/
│   └── (Integrity Verification — multi-codebase)
├── stage-9-i18n/
│   └── (String Extraction, Translation Verification)
├── stage-10-release/
│   └── (Release Checklist — coordinated multi-platform)
└── monitoring/
    ├── progress.md                                    ← Pipeline Progress Dashboard (Layer 1)
    ├── session-log.md                                 ← Session Audit Trail (Layer 2)
    ├── checkpoint.json                                ← Machine-Readable Milestone (Layer 3)
    ├── stage-transition-summary.md                    ← Cross-Stage Context Handoff (ASE Phase 1)
    ├── stage-transition-schemas.md                    ← JSON Schema Contracts — Full-Stack Adapted (ASE Phase 2)
    ├── inter-agent-communication-protocol.md          ← IACP — Cross-Track Routing (ASE Phase 2)
    ├── mvc-context-profile.md                         ← MVC Profile Template (ASE Phase 2)
    ├── knowledge-transfer-protocol.md                 ← 3-Tier Learning Loop (ASE Phase 3)
    ├── rag-integration-blueprint.md                   ← Semantic Retrieval Architecture (ASE Phase 3)
    ├── adr-ase-001.md                                 ← ASE Adoption Decision Record (ASE Phase 3)
    └── schema-validation-spec.md                      ← Automated Gate Enforcement — V-FS- Rules (ASE Phase 3)
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
| 6 — Code Review         | `DEFECT-REPORT.md`, `RED-TEAM-REVIEW.md`, `STAGE-TRANSITION-SUMMARY.md`                                                                                                                                                                                               | 3     |
| 7 — Testing             | `TEST-RESULTS-REPORT.md`, `DEVICE-MATRIX.md`, `E2E-TEST-REPORT.md`                                                                                                                                                                                                                                   | 3     |
| 8 — Integrity           | `INTEGRITY-SIGNOFF.md`                                                                                                                                                                                                                                                                               | 1     |
| 9 — i18n                | `STRING-EXTRACTION-HANDOFF.md`, `TRANSLATION-VERIFICATION-REPORT.md`                                                                                                                                                                                                                                 | 2     |
| 10 — Release            | `RELEASE-CHECKLIST.md` (coordinated multi-platform)                                                                                                                                                                                                                                                  | 1     |
| Monitoring (all stages) | `progress.md`, `session-log.md`, `checkpoint.json`, `stage-transition-summary.md`, `stage-transition-schemas.md`, `inter-agent-communication-protocol.md`, `mvc-context-profile.md`, `knowledge-transfer-protocol.md`, `rag-integration-blueprint.md`, `adr-ase-001.md`, `schema-validation-spec.md` | 11    |

---

## Monitoring Templates

| Template                                | Layer      | ASE Phase |   Domain Adaptation    |
| --------------------------------------- | ---------- | --------- | :--------------------: |
| `progress.md`                           | Layer 1    | —         |      ✅ Inherited      |
| `session-log.md`                        | Layer 2    | —         |      ✅ Inherited      |
| `checkpoint.json`                       | Layer 3    | —         |      ✅ Inherited      |
| `stage-transition-summary.md`           | ASE — L2   | Phase 1   |      ✅ Portable       |
| `stage-transition-schemas.md`           | ASE — L2   | Phase 2   | 🔧 Full-Stack adapted  |
| `inter-agent-communication-protocol.md` | ASE — L2/3 | Phase 2   | 🔧 Cross-track adapted |
| `mvc-context-profile.md`                | ASE — L2   | Phase 2   |      ✅ Portable       |
| `knowledge-transfer-protocol.md`        | ASE — L3   | Phase 3   |      ✅ Portable       |
| `rag-integration-blueprint.md`          | ASE — L4   | Phase 3   |      ✅ Portable       |
| `adr-ase-001.md`                        | ASE — Gov  | Phase 3   |      ✅ Portable       |
| `schema-validation-spec.md`             | ASE — L3   | Phase 3   |   🔧 V-FS- prefixed    |
| `RED-TEAM-REVIEW.md` (stage-6)          | ASE — L3   | Phase 3   |      ✅ Portable       |

**Domain-adapted templates** contain full-stack-specific fields: multi-platform scope, cross-track synchronization protocol, integration milestones (IM-NNN), multiple codebase tags (mobile/web/api), and FS-MOBILE/FS-WEB/FS-API track assignments.

**Unique to Full-Stack:** Integration Checkpoint Message format in IACP, cross-track conflict resolution protocol, API Contract Lock sync point.

**Validation Rule Prefix:** `V-FS-NNN` (see schema-validation-spec.md)

---

## Usage

1. Copy the template to your project directory under the appropriate stage folder
2. Replace all `[bracketed placeholders]` with project-specific content
3. Follow the structure — all sections are mandatory unless marked optional
4. Version each artifact per the project versioning convention
