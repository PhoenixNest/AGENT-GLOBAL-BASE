# Pipeline Delta Template

> Every product pipeline (`mobile-development`, `web-development`, `backend-api`, `full-stack`) must produce a `delta.md` file conforming to this template. The delta file fills the `{{DELTA: …}}` placeholders defined in [`pipeline.md`](./pipeline.md) and adds product-specific content that does not belong in the universal base.
>
> **Recruitment is NOT required to produce a delta.** Recruitment is shape-incompatible with the product pipelines (9-stage automated vs. 10-stage gated) and remains a single self-contained file.

---

## Required Sections

| #   | Section                                      | What goes here                                                                                                                                                                                                                 |
| --- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Header metadata                              | Pipeline name, owner, target surface(s), effective date, supersedes (if any), cross-refs to base file.                                                                                                                         |
| 2   | Surface / Platform Strategy Matrix           | Product-specific scenarios + decision matrix (e.g., mobile's 5-scenario matrix; web's SPA/SSR/SSG matrix).                                                                                                                     |
| 3   | Stage 1 — PRD Stewardship                    | Who authors the PRD for this pipeline (e.g., CPO for mobile; VP Web for web; VP API for backend; joint VP Web + VP API for full-stack). Any product-specific PRD template fields.                                              |
| 4   | Stage 2 — Prototype Variant                  | Format of the prototype (HTML for web/mobile; OpenAPI/GraphQL schema for backend; HTML + API contract for full-stack). Surface-specific IDS sections (iOS HIG + Android Material for mobile; WCAG mobile-first for web; etc.). |
| 5   | Stage 3 — Additional Mandatory ADRs          | Product-specific ADRs in addition to the universal Security Architecture and String Key Taxonomy ADRs.                                                                                                                         |
| 6   | Stage 4 — Pipeline-Specific Plan Sections    | Track Activation Mapping (mobile), Service Decomposition Plan (backend), Composition Plan (full-stack), Rendering Strategy Plan (web).                                                                                         |
| 7   | Stage 5 — Track Execution Model              | Platform Leads, shared module coordination, SIS scope, design fidelity checkpoint scope.                                                                                                                                       |
| 8   | Stage 6 — Tier-1 Review Model                | Cross-review structure for this product (e.g., Android Lead ↔ iOS Lead for mobile; Frontend Lead ↔ Backend Lead for full-stack). Live demo scope.                                                                              |
| 9   | Stage 7 — Platform-Specific Testing Mandates | Espresso/XCTest (mobile); API contract tests (backend); Playwright/Cypress (web); composition tests (full-stack). DAST + Pen Test scope.                                                                                       |
| 10  | Stage 8 — Additional Integrity Checks        | Product-specific integrity checks beyond the universal anti-pattern guard.                                                                                                                                                     |
| 11  | Stage 10 — Additional Release Criteria       | Surface-specific release criteria beyond the 12-row universal checklist.                                                                                                                                                       |
| 12  | Stage 11 — Live Ops Mandates                 | Product-specific Sev ladder details, on-call composition, error budget targets.                                                                                                                                                |
| 13  | Cross-Cutting i18n Requirements              | Per-stage i18n requirements specific to this product type.                                                                                                                                                                     |
| 14  | Document Version History                     | Same shape as the base.                                                                                                                                                                                                        |

---

## Forbidden in the Delta

The following must NOT be duplicated in delta files — they belong only in [`pipeline.md`](./pipeline.md):

- The Defect Severity System table.
- The Progress Sync Protocol.
- The universal gate criteria for any stage (only product-specific _additions_ may appear in the delta).
- The 10-stage frame itself (delta refers to base by stage number; it does not redefine stages).
- The "Trim-to-Pass" anti-pattern definition (KEEP-01).
- The 12-row Release Readiness Checklist (delta may add a 13th+ row).

If the same content appears in two delta files, escalate to the Software Architect — that's a signal it should be promoted into the base.

---

## Filename and Location

```text
company/pipeline/<pipeline-type>/delta.md
```

| State                    | File                                        |
| ------------------------ | ------------------------------------------- |
| Canonical base           | `company/pipeline/_base/pipeline.md`        |
| Product-specific overlay | `company/pipeline/<pipeline-type>/delta.md` |

---

## Document Version History

| Version | Date           | Author             | Changes                                              |
| ------- | -------------- | ------------------ | ---------------------------------------------------- |
| 1.0     | April 21, 2026 | Software Architect | Initial authoritative template; section list locked. |
