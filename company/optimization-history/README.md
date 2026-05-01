# Optimization History

This folder is the **canonical archive of operating-model optimization plans** for the company and its studios. Every plan records a structured review of pipelines, departments, personnel, and governance, plus an explicit set of recommendations with owners, due dates, and CEO audit/sign-off blocks.

> **Audit principle:** Optimization plans are versioned, auditable artifacts. Once a plan is approved, its findings transition through a defined lifecycle (Pending → In Progress → Implemented → Verified → Closed). The folder is **append-only** for active plans; superseded plans are retained for historical traceability.

---

## 1. Folder Conventions

| Convention            | Rule                                                                                                                                                                                                                                                                                                                                                                       |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Filename pattern**  | Every plan uses a dedicated sub-folder: `YYYY-MM-DD-<short-descriptive-slug>/` containing `optimization-plan.md` plus `execution-tracker.md` and any other companions. The folder owns the date prefix and the scope; contained files identify the _kind_ of artifact. **See §2 for the canonical folder pattern.**                                                        |
| **Plan ID pattern**   | `OPT-YYYY-MM-DD-NNN` where `NNN` is a zero-padded sequence number for plans created on the same day                                                                                                                                                                                                                                                                        |
| **Required sections** | Header metadata table · Executive Summary · Sources Reviewed · Strengths to Preserve · Critical Findings (P0) · Important Findings (P1) · Polish Findings (P2) · 30/60/90-Day Execution Plan · Optimization Topics (per-topic deep-dive tables) · Risk Register · Success Metrics · Out of Scope · Audit & Sign-off Block · Document Version History · Traceability Matrix |
| **Status lifecycle**  | `Draft → Awaiting Audit → Approved → In Progress → Implemented → Verified → Closed → Superseded`                                                                                                                                                                                                                                                                           |
| **Edit policy**       | Approved plans are **read-only** for content; only the audit log, status columns, and CEO Audit Notes columns may be updated. Material change = new plan that supersedes the old.                                                                                                                                                                                          |
| **Deletion policy**   | Completed and closed plans may be removed once they are no longer actively referenced. Plans being superseded should reference the newer plan in their `Supersedes` field before removal.                                                                                                                                                                                  |

---

## 2. Plan Folder Structure

Every optimization plan lives in its own dedicated sub-folder. There is no flat-file option — even the smallest plan gets a folder. The folder owns the date and the scope; the contained files identify the _kind_ of artifact, not the initiative.

### 2.1 Canonical Folder Layout

```text
company/optimization-history/
├── README.md                                 ← this index (single, top-level)
└── YYYY-MM-DD-<short-slug>/                  ← one folder per plan (always)
    ├── optimization-plan.md                  ← the plan (canonical filename — REQUIRED)
    ├── execution-tracker.md                  ← live execution state (canonical filename — REQUIRED)
    ├── migration-disagreement-log.md         ← OPTIONAL: content conflicts during a refactor
    ├── postmortem.md                         ← OPTIONAL: end-of-plan retrospective
    ├── independent-challenge-report.md       ← OPTIONAL: red-team / devil's-advocate review
    └── ...                                   ← any other companion, named for what it IS
```

### 2.2 Naming Rules (Strict)

| Rule                                                                                  | Why                                                                                                                                                                              |
| :------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The folder name is `YYYY-MM-DD-<short-slug>/` matching the plan's date and scope.     | The folder is the **identity boundary** for the initiative. The slug should name the dominant theme, not any single artifact (e.g., `operating-model-review`, not `…-and-plan`). |
| Inside the folder, the plan is **always** named `optimization-plan.md`.               | Predictable canonical entry point. Tooling and humans can locate the plan in any plan-folder by this exact name without consulting the index.                                    |
| Inside the folder, the execution tracker is **always** named `execution-tracker.md`.  | Same predictability. Plan and tracker form a paired artifact; their filenames are paired too.                                                                                    |
| Companion artifacts are named for **what they are**, not for the date or the plan ID. | The folder context already supplies date and Plan ID. Filenames like `migration-plan.md`, `postmortem.md`, `audit-log.md` are self-describing.                                   |
| Inner files **never** repeat the date prefix.                                         | The folder owns the date; repeating it produces `2026-04-20-…/2026-04-20-…` which is noise.                                                                                      |

### 2.3 Cross-Reference Rules

| Direction                                                                 | Form                                                            | Example                                                                                       |
| :------------------------------------------------------------------------ | :-------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| From outside the folder → into the plan                                   | Full path: `optimization-history/<folder>/optimization-plan.md` | `[OPT-YYYY-MM-DD-NNN](../../optimization-history/YYYY-MM-DD-<slug>/optimization-plan.md)`     |
| From outside the folder → into the tracker                                | Full path: `optimization-history/<folder>/execution-tracker.md` | Same shape as above.                                                                          |
| From one file in the folder → to its sibling                              | Sibling: `./<sibling>.md`                                       | From `optimization-plan.md` to its tracker: `[execution-tracker](./execution-tracker.md)`     |
| From one file in the folder → to the index README                         | One up: `../README.md`                                          | Tracker §7 cross-ref: `[Optimization-history index](../README.md)`                            |
| From one file in the folder → to anywhere outside `optimization-history/` | One extra level: drop one more `../`                            | A file inside the folder reaches `company/library/` via `../../library/` (not `../library/`). |

### 2.4 Versioning + Audit-Log Discipline

| Practice                                                                                                                                                                                                              | Why                                                                                                                                                                                                                           |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The plan has its own `Document Version History` section (typically §13 in our standard template). The tracker has its own (typically §8). The index README has its own (§8 in this file).                             | Three separate version trails, one per artifact. A plan-content version bump does not require a tracker version bump unless the tracker was also touched.                                                                     |
| **Audit log is append-only.** Existing entries are NEVER retroactively rewritten — even if file paths or filenames change later.                                                                                      | Audit-log entries record _what was true at the time the entry was filed_. Rewriting them would erase the audit trail. Subsequent changes are documented in NEW entries that explicitly note the prior reference is now stale. |
| When a path/filename changes, add a new `§12.1 Audit Log` row (in the plan) AND a new `§13` changelog row (in the plan) AND update **all live cross-references** in companion + child files in the same edit session. | Splits the "what happened" record (audit log) from the "what was changed in this version" summary (changelog). Live references stay current; historical entries stay honest.                                                  |
| Use `git mv` (not delete + create) when moving or renaming the plan or tracker.                                                                                                                                       | Preserves `git log --follow` history across the rename, ensuring prior history survives the move.                                                                                                                             |

### 2.5 Why Folder-Only

Every plan starts as a folder for three reasons:

1. **Consistency.** One mental model — no decision required at authoring time about whether a plan will stay simple.
2. **Tool predictability.** Any agent or script can always locate a plan at `<folder>/optimization-plan.md` without branching logic.
3. **Eliminates promotion churn.** Plans frequently acquire an execution tracker, postmortem, or audit note mid-execution. Starting with a folder means this never requires a structural refactor.

---

## 3. Plan Index

| Plan ID            | Date       | Title                          | Scope                                         | Status    | Audit Decision | File                                                                                |
| ------------------ | ---------- | ------------------------------ | --------------------------------------------- | --------- | -------------- | ----------------------------------------------------------------------------------- |
| OPT-2026-05-01-001 | 2026-05-01 | ASE Compliance Gap Remediation | All 4 company pipelines + Casual Games Studio | ✅ Closed | Closed         | [`optimization-plan.md`](./2026-05-01-ase-maturity-assessment/optimization-plan.md) |

> Add new rows above this line as new optimization plans are filed.

---

## 4. Plan Status Summary

| Status             | Count | Meaning                                                                                                 |
| ------------------ | ----- | ------------------------------------------------------------------------------------------------------- |
| **Draft**          | 0     | Plan is being authored                                                                                  |
| **Awaiting Audit** | 0     | Submitted to CEO for review and sign-off                                                                |
| **Approved**       | 0     | CEO has signed off; execution may begin                                                                 |
| **In Progress**    | 0     | One or more findings actively being remediated                                                          |
| **Implemented**    | 0     | All approved findings have remediation work completed; pending verification                             |
| **Verified**       | 0     | All approved findings verified by independent review (e.g., red-team / devil's advocate per FIND-P1-08) |
| **Closed**         | 1     | All approved findings verified, success metrics measured, plan retrospective complete                   |
| **Superseded**     | 0     | Replaced by a newer plan; retained for historical traceability                                          |
| **Total Plans**    | **1** |                                                                                                         |

---

## 5. How to File a New Optimization Plan

**Templates:** [`template/optimization-plan.md`](./template/optimization-plan.md) · [`template/execution-tracker.md`](./template/execution-tracker.md)

| Step | Action                                                                                                                                                                                                                                                             |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1    | Conduct the review (read pipelines, profiles, skills, audit reports as needed). Record the file list in the **Sources Reviewed** section so findings are traceable to evidence.                                                                                    |
| 2    | Copy [`template/optimization-plan.md`](./template/optimization-plan.md) as your starting point. Fill in all required sections. Use stable finding IDs (`FIND-P0-01`, `FIND-P1-01`, `FIND-P2-01` …) so the CEO can reference findings unambiguously during audit.   |
| 3    | Create a sub-folder `YYYY-MM-DD-<short-descriptive-slug>/` at the top of this folder. Save the filled-in plan template inside as `optimization-plan.md`. Copy [`template/execution-tracker.md`](./template/execution-tracker.md) inside as `execution-tracker.md`. |
| 4    | Add a row to the **Plan Index** table in §3. Update the **Plan Status Summary** counts in §4. Set status to `Draft` or `Awaiting Audit`.                                                                                                                           |
| 5    | Notify the CEO. The CEO fills in the audit log and sign-off block (§12 in the plan) directly in the plan file.                                                                                                                                                     |
| 6    | After approval, update the plan's status, the index row, and the status summary counts. As findings are remediated, update the **Status** columns within the plan and tracker. Cross-reference, version-bump, and audit-log discipline all follow §2.3 + §2.4.     |

---

## 6. Plan Lifecycle Diagram (Reference)

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

## 7. Cross-References

| Topic                         | Location                                                                                                                     |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Root governance               | Workspace root — auto-provided to all agents                                                                                 |
| Pipeline definitions          | [`company/pipeline/`](company/pipeline/)                                                                                     |
| Department roster             | [`company/library/overview/personnel.md`](company/library/overview/personnel.md)                                             |
| Pipeline overview             | [`company/library/overview/pipeline.md`](company/library/overview/pipeline.md)                                               |
| Studio (Casual Games) charter | [`studio/casual-games/library/overview/casual-games-studio.md`](studio/casual-games/library/overview/casual-games-studio.md) |

---

## 8. Document Version History

| Version | Date           | Author     | Changes                                                                                                                         |
| ------- | -------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 30, 2026 | —          | Template retained as process reference. Historical plan data cleared. Folder-only convention adopted; flat-file option removed. |
| 1.1     | May 1, 2026    | CTO Office | §3 Plan Index: OPT-2026-05-01-001 registered. §4 Status Summary: Awaiting Audit count 0 → 1; Total Plans 0 → 1.                 |
| 1.2     | May 1, 2026    | CTO Office | §3 Plan Index: OPT-2026-05-01-001 status updated to Closed. §4: Awaiting Audit 1 → 0; Closed 0 → 1.                             |

---

_This index is maintained alongside every optimization plan filed in this folder. Update §3 (Plan Index) and §4 (Status Summary) whenever a plan is added, status-changed, or superseded. Every plan MUST use the folder convention defined in §2._
