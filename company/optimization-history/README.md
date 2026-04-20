# Optimization History

This folder is the **canonical archive of operating-model optimization plans** for the company and its studios. Every plan records a structured review of pipelines, departments, personnel, and governance, plus an explicit set of recommendations with owners, due dates, and CEO audit/sign-off blocks.

> **Audit principle:** Optimization plans are versioned, auditable artifacts. Once a plan is approved, its findings transition through a defined lifecycle (Pending → In Progress → Implemented → Verified → Closed). The folder is **append-only** for active plans; superseded plans are retained for historical traceability.

---

## 1. Folder Conventions

| Convention            | Rule                                                                                                                                                                                                                                                                                                                                                                       |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Filename pattern**  | `YYYY-MM-DD-<short-descriptive-slug>.md` — e.g., `2026-04-20-operating-model-review-and-optimization-plan.md`                                                                                                                                                                                                                                                              |
| **Plan ID pattern**   | `OPT-YYYY-MM-DD-NNN` where `NNN` is a zero-padded sequence number for plans created on the same day                                                                                                                                                                                                                                                                        |
| **Required sections** | Header metadata table · Executive Summary · Sources Reviewed · Strengths to Preserve · Critical Findings (P0) · Important Findings (P1) · Polish Findings (P2) · 30/60/90-Day Execution Plan · Optimization Topics (per-topic deep-dive tables) · Risk Register · Success Metrics · Out of Scope · Audit & Sign-off Block · Document Version History · Traceability Matrix |
| **Status lifecycle**  | `Draft → Awaiting Audit → Approved → In Progress → Implemented → Verified → Closed → Superseded`                                                                                                                                                                                                                                                                           |
| **Edit policy**       | Approved plans are **read-only** for content; only the audit log, status columns, and CEO Audit Notes columns may be updated. Material change = new plan that supersedes the old.                                                                                                                                                                                          |
| **Deletion policy**   | Plans are **never deleted**. Obsolete plans are marked `Superseded` and reference the new plan in their `Supersedes` field.                                                                                                                                                                                                                                                |

---

## 2. Plan Index

| Plan ID            | Date           | Title                                      | Scope                                                                                       | Status   | Audit Decision | File                                                                                                                         |
| ------------------ | -------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------- | -------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| OPT-2026-04-20-001 | April 20, 2026 | Operating Model Review & Optimization Plan | Full company (4 pipelines + recruitment + departments + library) and `studio/casual-games/` | Approved | Approved       | [`2026-04-20-operating-model-review-and-optimization-plan.md`](./2026-04-20-operating-model-review-and-optimization-plan.md) |

> Add new rows above this line as new optimization plans are filed.

---

## 3. Plan Status Summary

| Status             | Count | Meaning                                                                                                 |
| ------------------ | ----- | ------------------------------------------------------------------------------------------------------- |
| **Draft**          | 0     | Plan is being authored                                                                                  |
| **Awaiting Audit** | 0     | Submitted to CEO for review and sign-off                                                                |
| **Approved**       | 1     | CEO has signed off; execution may begin                                                                 |
| **In Progress**    | 0     | One or more findings actively being remediated                                                          |
| **Implemented**    | 0     | All approved findings have remediation work completed; pending verification                             |
| **Verified**       | 0     | All approved findings verified by independent review (e.g., red-team / devil's advocate per FIND-P1-08) |
| **Closed**         | 0     | All approved findings verified, success metrics measured, plan retrospective complete                   |
| **Superseded**     | 0     | Replaced by a newer plan; retained for historical traceability                                          |
| **Total Plans**    | **1** |                                                                                                         |

---

## 4. How to File a New Optimization Plan

| Step | Action                                                                                                                                                                                            |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Conduct the review (read pipelines, profiles, skills, audit reports as needed). Record the file list in the **Sources Reviewed** section so findings are traceable to evidence.                   |
| 2    | Draft the plan using the required-sections list in §1. Use stable finding IDs (`FIND-P0-01`, `FIND-P1-01`, `FIND-P2-01` …) so the CEO can reference findings unambiguously during audit.          |
| 3    | Save as `YYYY-MM-DD-<short-descriptive-slug>.md` in this folder. Use today's date and a slug that names the dominant theme (e.g., `i18n-pipeline-restructure`, `studio-economy-overhaul`).        |
| 4    | Add a row to the **Plan Index** table in §2. Update the **Plan Status Summary** counts in §3. Set status to `Draft` or `Awaiting Audit`.                                                          |
| 5    | Notify the CEO. The CEO fills in the audit log and sign-off block (Section 12 in the standard template) directly in the plan file.                                                                |
| 6    | After approval, update the plan's status, the index row, and the status summary counts. As findings are remediated, update the **Status** and **CEO Audit Notes** columns within the plan itself. |

---

## 5. Plan Lifecycle Diagram (Reference)

```text
                ┌──────────┐
                │  Draft   │
                └────┬─────┘
                     │ author submits
                     ▼
              ┌──────────────┐
              │ Awaiting     │
              │ Audit        │
              └────┬─────────┘
                   │ CEO reviews + signs off
        ┌──────────┴──────────┐
        ▼                     ▼
  ┌──────────┐          ┌──────────┐
  │ Approved │          │ Rejected │
  └────┬─────┘          └──────────┘
       │ owners begin remediation
       ▼
  ┌─────────────┐
  │ In Progress │
  └────┬────────┘
       │ all approved findings remediated
       ▼
  ┌──────────────┐
  │ Implemented  │
  └────┬─────────┘
       │ independent challenge round verifies
       ▼
  ┌──────────┐
  │ Verified │
  └────┬─────┘
       │ success metrics measured + retrospective complete
       ▼
  ┌──────────┐
  │  Closed  │
  └──────────┘
       │ replaced by new plan (later)
       ▼
  ┌────────────┐
  │ Superseded │
  └────────────┘
```

---

## 6. Cross-References

| Topic                         | Location                                                                                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Root governance               | [`../../AGENTS.md`](../../AGENTS.md)                                                                                                     |
| Pipeline definitions          | [`../pipeline/`](../pipeline/)                                                                                                           |
| Department roster             | [`../library/overview/personnel.md`](../library/overview/personnel.md)                                                                   |
| Pipeline overview             | [`../library/overview/pipeline.md`](../library/overview/pipeline.md)                                                                     |
| Studio (Casual Games) charter | [`../../studio/casual-games/library/overview/casual-games-studio.md`](../../studio/casual-games/library/overview/casual-games-studio.md) |

---

## 7. Document Version History

| Version | Date           | Author           | Changes                                                                                                                                                                                                                        |
| ------- | -------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0     | April 20, 2026 | Operating Review | Initial index established; first plan filed (OPT-2026-04-20-001)                                                                                                                                                               |
| 1.1     | April 20, 2026 | Operating Review | Pre-audit double-review pass: required-sections list expanded to match the actual plan template (added Optimization Topics, Out of Scope, Document Version History); §2 status aligned to lifecycle bucket (`Awaiting Audit`). |

---

_This index is maintained alongside every optimization plan filed in this folder. Update §2 (Plan Index) and §3 (Status Summary) whenever a plan is added, status-changed, or superseded._
