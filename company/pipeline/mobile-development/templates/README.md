# Pipeline Templates

Ready-to-use templates for the 10-stage development pipeline and the Progress Monitoring & Recovery System. Templates are organized by pipeline stage.

---

## Directory Structure

```
templates/
├── README.md                                          ← this file
├── stage-1-requirements/
│   ├── PRD.md                                         ← Product Requirements Document
│   └── SRD.md                                         ← Security Requirements Document
├── stage-2-design/
│   └── IDS.md                                         ← Interaction Design Specification
├── stage-3-architecture/
│   ├── ADR-PLATFORM-STRATEGY.md                       ← Platform Strategy ADR
│   ├── ADR-STRING-KEY-TAXONOMY.md                     ← String Key Naming Convention ADR
│   ├── ADR-SECURITY-CRYPTO.md                         ← Cryptographic Standards ADR
│   ├── ADR-SECURITY-STORAGE.md                        ← Secure Storage Mechanisms ADR
│   ├── ADR-SECURITY-PINNING.md                        ← Certificate Pinning Strategy ADR
│   ├── ADR-SECURITY-PLATFORM-PATTERNS.md              ← Platform Security Patterns ADR
│   └── TSD.md                                         ← Technology Selection Document
├── stage-4-implementation-plan/
│   ├── IMPLEMENTATION-PLAN.md                         ← Coding Implementation Plan
│   ├── RTM.md                                         ← Requirements Traceability Matrix
│   └── TEST-ARCHITECTURE-DOCUMENT.md                  ← Test Architecture Document (TAD)
├── stage-5-development/
│   ├── DEVELOPMENT-LOG.md                             ← Development Log (per platform)
│   ├── SIS.md                                         ← Security Implementation Specification
│   └── CONTRACT-VERIFICATION-REPORT.md                ← KMP/Flutter Contract Verification
├── stage-6-code-review/
│   ├── DEFECT-REPORT.md                               ← Defect Report
│   ├── RED-TEAM-REVIEW.md                             ← Red Team Adversarial Review Protocol
└── STAGE-TRANSITION-SUMMARY.md                    ← Stage 6 Transition Summary
├── stage-7-testing/
│   ├── TEST-RESULTS-REPORT.md                         ← Test Results Report
│   ├── PERFORMANCE-BENCHMARK-REPORT.md                ← Performance Benchmark Results
│   └── DEVICE-MATRIX.md                               ← Minimum Device/OS Matrix
├── stage-8-integrity/
│   └── INTEGRITY-SIGNOFF.md                           ← Integrity Verification Sign-Off
├── stage-9-i18n/
│   ├── STRING-EXTRACTION-HANDOFF.md                   ← Phase A→B Handoff
│   └── TRANSLATION-VERIFICATION-REPORT.md             ← Translation Verification Report
├── stage-10-release/
│   └── RELEASE-CHECKLIST.md                           ← Release Readiness (7-Item Checklist)
└── monitoring/
    ├── progress.md                                    ← Pipeline Progress Dashboard (Layer 1)
    ├── session-log.md                                 ← Session Audit Trail (Layer 2)
    ├── checkpoint.json                                ← Machine-Readable Milestone (Layer 3)
    ├── stage-transition-summary.md                    ← Cross-Stage Context Handoff (ASE Phase 1)
    ├── stage-transition-schemas.md                    ← JSON Schema Contracts (ASE Phase 2)
    ├── inter-agent-communication-protocol.md          ← IACP Message Formats (ASE Phase 2)
    ├── mvc-context-profile.md                         ← MVC Profile Template (ASE Phase 2)
    ├── knowledge-transfer-protocol.md                 ← 3-Tier Learning Loop (ASE Phase 3)
    ├── rag-integration-blueprint.md                   ← Semantic Retrieval Architecture (ASE Phase 3)
    ├── adr-ase-001.md                                 ← ASE Adoption Decision Record (ASE Phase 3)
    └── schema-validation-spec.md                      ← Automated Gate Enforcement (ASE Phase 3)
```

---

## Quick Reference by Stage

| Stage                   | Templates                                                                                                                                                                                                                                                                                            | Count  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 1 — Requirements        | `PRD.md`, `SRD.md`                                                                                                                                                                                                                                                                                   | 2      |
| 2 — Design              | `IDS.md`                                                                                                                                                                                                                                                                                             | 1      |
| 3 — Architecture        | 6× ADR templates, `TSD.md`                                                                                                                                                                                                                                                                           | 7      |
| 4 — Implementation Plan | `IMPLEMENTATION-PLAN.md`, `RTM.md`, `TEST-ARCHITECTURE-DOCUMENT.md`                                                                                                                                                                                                                                  | 3      |
| 5 — Development         | `DEVELOPMENT-LOG.md`, `SIS.md`, `CONTRACT-VERIFICATION-REPORT.md`                                                                                                                                                                                                                                    | 3      |
| 6 — Code Review         | `DEFECT-REPORT.md`, `RED-TEAM-REVIEW.md`, `STAGE-TRANSITION-SUMMARY.md`                                                                                                                                                                                                                              | 3      |
| 7 — Testing             | `TEST-RESULTS-REPORT.md`, `PERFORMANCE-BENCHMARK-REPORT.md`, `DEVICE-MATRIX.md`                                                                                                                                                                                                                      | 3      |
| 8 — Integrity           | `INTEGRITY-SIGNOFF.md`                                                                                                                                                                                                                                                                               | 1      |
| 9 — i18n                | `STRING-EXTRACTION-HANDOFF.md`, `TRANSLATION-VERIFICATION-REPORT.md`                                                                                                                                                                                                                                 | 2      |
| 10 — Release            | `RELEASE-CHECKLIST.md`                                                                                                                                                                                                                                                                               | 1      |
| Monitoring (all stages) | `progress.md`, `session-log.md`, `checkpoint.json`, `stage-transition-summary.md`, `stage-transition-schemas.md`, `inter-agent-communication-protocol.md`, `mvc-context-profile.md`, `knowledge-transfer-protocol.md`, `rag-integration-blueprint.md`, `adr-ase-001.md`, `schema-validation-spec.md` | 11     |
| **Total**               |                                                                                                                                                                                                                                                                                                      | **38** |

---

## Monitoring Templates

| Template                                | Layer      | Format   | When to Use                                                     |
| --------------------------------------- | ---------- | -------- | --------------------------------------------------------------- |
| `progress.md`                           | Layer 1    | Markdown | Created at project start (Stage 4+); updated at every milestone |
| `session-log.md`                        | Layer 2    | Markdown | One file per work session; created at session start             |
| `checkpoint.json`                       | Layer 3    | JSON     | One file per stage gate; updated at each internal milestone     |
| `stage-transition-summary.md`           | ASE — L2   | Markdown | Mandatory at every stage gate; prevents info loss               |
| `stage-transition-schemas.md`           | ASE — L2   | JSON     | Schema contracts for all 10 stage transitions                   |
| `inter-agent-communication-protocol.md` | ASE — L2/3 | Markdown | Message formats, routing rules, escalation paths                |
| `mvc-context-profile.md`                | ASE — L2   | Markdown | Template for agent MVC profiles; append to agent `.md` files    |
| `knowledge-transfer-protocol.md`        | ASE — L3   | Markdown | 3-tier learning loop: session → project → institutional         |
| `rag-integration-blueprint.md`          | ASE — L4   | Markdown | Semantic retrieval architecture; 3-phase evolution roadmap      |
| `adr-ase-001.md`                        | ASE — Gov  | Markdown | Formal ADR codifying ASE as permanent methodology               |
| `schema-validation-spec.md`             | ASE — L3   | Markdown | Automated gate validation rules and error escalation            |

**Full specification:** [`monitoring.md`](company/pipeline/mobile-development/monitoring.md) — Progress Monitoring & Recovery System.

---

## ADR Template Index

| ADR                                 | Stage | Purpose                                                            |
| ----------------------------------- | ----- | ------------------------------------------------------------------ |
| `ADR-PLATFORM-STRATEGY.md`          | 3     | Native vs KMP vs Flutter decision                                  |
| `ADR-STRING-KEY-TAXONOMY.md`        | 3     | `{feature}.{screen}.{component}.{property}` naming convention      |
| `ADR-SECURITY-CRYPTO.md`            | 3     | Approved/deprecated/prohibited cryptographic algorithms            |
| `ADR-SECURITY-STORAGE.md`           | 3     | Keychain/Keystore/StrongBox per data classification                |
| `ADR-SECURITY-PINNING.md`           | 3     | Certificate pinning mechanism, rotation, fallback                  |
| `ADR-SECURITY-PLATFORM-PATTERNS.md` | 3     | iOS App Attest, Android Play Integrity, platform-specific patterns |

---

## Usage

1. Copy the template to your project directory under the appropriate stage folder
2. Replace all `[bracketed placeholders]` with project-specific content
3. Follow the structure — all sections are mandatory unless marked optional
4. Version each artifact per the project versioning convention (`v1/`, `v2/`, `final/`)

## Example

```
company/project/my-app/requirements/prd/v1/PRD.md                      ← copy of stage-1-requirements/PRD.md
company/project/my-app/requirements/srd/v1/SRD.md                      ← copy of stage-1-requirements/SRD.md
company/project/my-app/design/interaction-specs/v1/IDS.md              ← copy of stage-2-design/IDS.md
company/project/my-app/architecture/decisions/ADR-001.md               ← copy of stage-3-architecture/ADR-PLATFORM-STRATEGY.md
company/project/my-app/architecture/decisions/ADR-002.md               ← copy of stage-3-architecture/ADR-SECURITY-CRYPTO.md
company/project/my-app/specs/implementation-plan/v1/IMPLEMENTATION-PLAN.md  ← copy of stage-4-implementation-plan/IMPLEMENTATION-PLAN.md
company/project/my-app/PROGRESS.md                                     ← copy of monitoring/progress.md
company/project/my-app/sessions/session-20260408-090000.md             ← copy of monitoring/session-log.md
company/project/my-app/checkpoints/stage4-in-progress.json             ← copy of monitoring/checkpoint.json
```

y of monitoring/checkpoint.json

```

```
