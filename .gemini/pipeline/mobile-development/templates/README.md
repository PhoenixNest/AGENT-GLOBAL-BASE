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
│   └── DEFECT-REPORT.md                               ← Defect Report
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
    ├── PROGRESS.md                                    ← Pipeline Progress Dashboard (Layer 1)
    ├── SESSION-LOG.md                                 ← Session Audit Trail (Layer 2)
    └── CHECKPOINT.json                                ← Machine-Readable Milestone (Layer 3)
```

---

## Quick Reference by Stage

| Stage                   | Templates                                                                       | Count  |
| ----------------------- | ------------------------------------------------------------------------------- | ------ |
| 1 — Requirements        | `PRD.md`, `SRD.md`                                                              | 2      |
| 2 — Design              | `IDS.md`                                                                        | 1      |
| 3 — Architecture        | 6× ADR templates, `TSD.md`                                                      | 7      |
| 4 — Implementation Plan | `IMPLEMENTATION-PLAN.md`, `RTM.md`, `TEST-ARCHITECTURE-DOCUMENT.md`             | 3      |
| 5 — Development         | `DEVELOPMENT-LOG.md`, `SIS.md`, `CONTRACT-VERIFICATION-REPORT.md`               | 3      |
| 6 — Code Review         | `DEFECT-REPORT.md`                                                              | 1      |
| 7 — Testing             | `TEST-RESULTS-REPORT.md`, `PERFORMANCE-BENCHMARK-REPORT.md`, `DEVICE-MATRIX.md` | 3      |
| 8 — Integrity           | `INTEGRITY-SIGNOFF.md`                                                          | 1      |
| 9 — i18n                | `STRING-EXTRACTION-HANDOFF.md`, `TRANSLATION-VERIFICATION-REPORT.md`            | 2      |
| 10 — Release            | `RELEASE-CHECKLIST.md`                                                          | 1      |
| Monitoring (all stages) | `progress.md`, `session-log.md`, `checkpoint.json`                              | 3      |
| **Total**               |                                                                                 | **27** |

---

## Monitoring Templates

| Template          | Layer   | Format   | When to Use                                                     |
| ----------------- | ------- | -------- | --------------------------------------------------------------- |
| `progress.md`     | Layer 1 | Markdown | Created at project start (Stage 4+); updated at every milestone |
| `session-log.md`  | Layer 2 | Markdown | One file per work session; created at session start             |
| `checkpoint.json` | Layer 3 | JSON     | One file per stage gate; updated at each internal milestone     |

**Full specification:** [`monitoring.md`](../monitoring.md) — Progress Monitoring & Recovery System.

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
