# Optimization History

This folder is the **canonical archive of operating-model optimization plans** for the company and its studios. Every plan records a structured review of pipelines, departments, personnel, and governance, plus an explicit set of recommendations with owners, due dates, and CEO audit/sign-off blocks.

> **Audit principle:** Optimization plans are versioned, auditable artifacts. Once a plan is approved, its findings transition through a defined lifecycle (Pending → In Progress → Implemented → Verified → Closed). The folder is **append-only** for active plans; superseded plans are retained for historical traceability.

---

## 1. Folder Conventions

| Convention            | Rule                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Filename pattern**  | Single-artifact plan → flat file `YYYY-MM-DD-<short-descriptive-slug>.md`. Multi-artifact plan (plan + execution tracker + companion artifacts) → sub-folder `YYYY-MM-DD-<short-descriptive-slug>/` containing `optimization-plan.md` plus `execution-tracker.md` and any other companions. The folder owns the date prefix and the scope; contained files identify the _kind_ of artifact. **See §2 for the canonical multi-artifact pattern.** |
| **Plan ID pattern**   | `OPT-YYYY-MM-DD-NNN` where `NNN` is a zero-padded sequence number for plans created on the same day                                                                                                                                                                                                                                                                                                                                              |
| **Required sections** | Header metadata table · Executive Summary · Sources Reviewed · Strengths to Preserve · Critical Findings (P0) · Important Findings (P1) · Polish Findings (P2) · 30/60/90-Day Execution Plan · Optimization Topics (per-topic deep-dive tables) · Risk Register · Success Metrics · Out of Scope · Audit & Sign-off Block · Document Version History · Traceability Matrix                                                                       |
| **Status lifecycle**  | `Draft → Awaiting Audit → Approved → In Progress → Implemented → Verified → Closed → Superseded`                                                                                                                                                                                                                                                                                                                                                 |
| **Edit policy**       | Approved plans are **read-only** for content; only the audit log, status columns, and CEO Audit Notes columns may be updated. Material change = new plan that supersedes the old.                                                                                                                                                                                                                                                                |
| **Deletion policy**   | Plans are **never deleted**. Obsolete plans are marked `Superseded` and reference the new plan in their `Supersedes` field.                                                                                                                                                                                                                                                                                                                      |

---

## 2. Multi-Artifact Plan Folder Structure (Best Practice)

When a plan ships with companion artifacts — execution tracker, migration log, postmortem, audit notes, anything supplementary — use a **dedicated sub-folder** instead of scattering dated files at the top level. The folder owns the date and the scope; the contained files identify the _kind_ of artifact, not the initiative.

This convention was retroactively applied to `OPT-2026-04-20-001` and is now the **default for any optimization plan with more than one artifact**.

### 2.1 Canonical Folder Layout

```text
company/optimization-history/
├── README.md                                 ← this index (single, top-level)
├── YYYY-MM-DD-<short-slug>.md                ← single-artifact plan (flat file, OK)
└── YYYY-MM-DD-<short-slug>/                  ← multi-artifact plan (folder)
    ├── optimization-plan.md                  ← the plan (canonical filename — REQUIRED)
    ├── execution-tracker.md                  ← live execution state (canonical filename if present)
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

| Direction                                                                 | Form                                                            | Example                                                                                                   |
| :------------------------------------------------------------------------ | :-------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| From outside the folder → into the plan                                   | Full path: `optimization-history/<folder>/optimization-plan.md` | `[OPT-2026-04-20-001](../../optimization-history/2026-04-20-operating-model-review/optimization-plan.md)` |
| From outside the folder → into the tracker                                | Full path: `optimization-history/<folder>/execution-tracker.md` | Same shape as above.                                                                                      |
| From one file in the folder → to its sibling                              | Sibling: `./<sibling>.md`                                       | From `optimization-plan.md` to its tracker: `[execution-tracker](./execution-tracker.md)`                 |
| From one file in the folder → to the index README                         | One up: `../README.md`                                          | Tracker §7 cross-ref: `[Optimization-history index](../README.md)`                                        |
| From one file in the folder → to anywhere outside `optimization-history/` | One extra level: drop one more `../`                            | A file inside the folder reaches `AGENTS.md` via `../../../AGENTS.md` (not `../../AGENTS.md`).            |

### 2.4 Versioning + Audit-Log Discipline

| Practice                                                                                                                                                                                                              | Why                                                                                                                                                                                                                           |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The plan has its own `Document Version History` section (typically §13 in our standard template). The tracker has its own (typically §8). The index README has its own (§8 in this file).                             | Three separate version trails, one per artifact. A plan-content version bump does not require a tracker version bump unless the tracker was also touched.                                                                     |
| **Audit log is append-only.** Existing entries are NEVER retroactively rewritten — even if file paths or filenames change later.                                                                                      | Audit-log entries record _what was true at the time the entry was filed_. Rewriting them would erase the audit trail. Subsequent changes are documented in NEW entries that explicitly note the prior reference is now stale. |
| When a path/filename changes, add a new `§12.1 Audit Log` row (in the plan) AND a new `§13` changelog row (in the plan) AND update **all live cross-references** in companion + child files in the same edit session. | Splits the "what happened" record (audit log) from the "what was changed in this version" summary (changelog). Live references stay current; historical entries stay honest.                                                  |
| Use `git mv` (not delete + create) when moving or renaming the plan or tracker.                                                                                                                                       | Preserves `git log --follow` history across the rename. The folder relocation of `OPT-2026-04-20-001` retained full pre-rename history through this discipline.                                                               |

### 2.5 Decision: Flat File vs. Folder

| Choice        | Use when                                                                                                                                                                                                                                                                                                                                                         |
| :------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Flat file** | The plan is a single self-contained document. No execution tracker. No anticipated companion artifacts. Examples: a small policy clarification, a single ADR-style decision recorded as an optimization plan, a one-off cleanup instruction.                                                                                                                     |
| **Folder**    | The plan ships (or will ship) with an execution tracker. OR has a multi-phase rollout requiring a migration plan / disagreement log. OR is large enough to anticipate a postmortem. **When in doubt, choose folder** — promotion from flat → folder mid-flight is cheap with `git mv` (see `OPT-2026-04-20-001` v1.3 → v1.6 history) but creates one-time churn. |

### 2.6 Promotion Path (Flat → Folder)

If a plan starts as a flat file and later acquires companion artifacts, promote it to the folder pattern in a single dedicated edit session:

1. Create the folder: `YYYY-MM-DD-<short-slug>/`.
2. `git mv <plan>.md <folder>/optimization-plan.md` (preserves history).
3. Add the companion artifact(s) inside the folder.
4. Update **all** cross-references in one pass (use `rg` / `Grep` to find every link).
5. Add a `§12.1 Audit Log` entry + `§13` changelog entry to the plan documenting the relocation as **purely structural** (no content changes to findings, owners, or due dates).
6. Add a `§7 Changelog` entry to this index README.
7. Bump the plan's version (e.g., 1.5 → 1.6) to mark the structural change.
8. Run formatter and lint check before stopping.

`OPT-2026-04-20-001` is the canonical worked example: see its v1.5 → v1.6 → v1.7 changelog and the v1.3 / v1.4 entries in this README's §8.

---

## 3. Plan Index

| Plan ID            | Date           | Title                                      | Scope                                                                                       | Status      | Audit Decision | File                                                                                                                                                                                                                                                                               |
| ------------------ | -------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------- | ----------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OPT-2026-04-20-001 | April 20, 2026 | Operating Model Review & Optimization Plan | Full company (4 pipelines + recruitment + departments + library) and `studio/casual-games/` | In Progress | Approved       | folder: [`./2026-04-20-operating-model-review/`](./2026-04-20-operating-model-review/) — plan: [`optimization-plan.md`](./2026-04-20-operating-model-review/optimization-plan.md) · live state: [`execution-tracker.md`](./2026-04-20-operating-model-review/execution-tracker.md) |

> Add new rows above this line as new optimization plans are filed.

---

## 4. Plan Status Summary

| Status             | Count | Meaning                                                                                                 |
| ------------------ | ----- | ------------------------------------------------------------------------------------------------------- |
| **Draft**          | 0     | Plan is being authored                                                                                  |
| **Awaiting Audit** | 0     | Submitted to CEO for review and sign-off                                                                |
| **Approved**       | 0     | CEO has signed off; execution may begin                                                                 |
| **In Progress**    | 1     | One or more findings actively being remediated                                                          |
| **Implemented**    | 0     | All approved findings have remediation work completed; pending verification                             |
| **Verified**       | 0     | All approved findings verified by independent review (e.g., red-team / devil's advocate per FIND-P1-08) |
| **Closed**         | 0     | All approved findings verified, success metrics measured, plan retrospective complete                   |
| **Superseded**     | 0     | Replaced by a newer plan; retained for historical traceability                                          |
| **Total Plans**    | **1** |                                                                                                         |

---

## 5. How to File a New Optimization Plan

| Step | Action                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Conduct the review (read pipelines, profiles, skills, audit reports as needed). Record the file list in the **Sources Reviewed** section so findings are traceable to evidence.                                                                                                                                                                                                                                                                                                                                         |
| 2    | Draft the plan using the required-sections list in §1. Use stable finding IDs (`FIND-P0-01`, `FIND-P1-01`, `FIND-P2-01` …) so the CEO can reference findings unambiguously during audit.                                                                                                                                                                                                                                                                                                                                |
| 3    | **Decide flat vs. folder per §2.5.** For a single-artifact plan, save as `YYYY-MM-DD-<short-descriptive-slug>.md` at the top of this folder. For a multi-artifact plan (or any plan likely to acquire an execution tracker), create a sub-folder `YYYY-MM-DD-<short-descriptive-slug>/` and save the plan inside as `optimization-plan.md` per §2.1 + §2.2. **When in doubt, choose folder.** Use today's date and a slug that names the dominant theme (e.g., `i18n-pipeline-restructure`, `studio-economy-overhaul`). |
| 4    | Add a row to the **Plan Index** table in §3. Update the **Plan Status Summary** counts in §4. Set status to `Draft` or `Awaiting Audit`.                                                                                                                                                                                                                                                                                                                                                                                |
| 5    | Notify the CEO. The CEO fills in the audit log and sign-off block (Section 12 in the standard template) directly in the plan file.                                                                                                                                                                                                                                                                                                                                                                                      |
| 6    | After approval, update the plan's status, the index row, and the status summary counts. As findings are remediated, update the **Status** and **CEO Audit Notes** columns within the plan itself. Cross-reference, version-bump, and audit-log discipline all follow §2.3 + §2.4.                                                                                                                                                                                                                                       |

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

| Topic                         | Location                                                                                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Root governance               | [`../../AGENTS.md`](../../AGENTS.md)                                                                                                     |
| Pipeline definitions          | [`../pipeline/`](../pipeline/)                                                                                                           |
| Department roster             | [`../library/overview/personnel.md`](../library/overview/personnel.md)                                                                   |
| Pipeline overview             | [`../library/overview/pipeline.md`](../library/overview/pipeline.md)                                                                     |
| Studio (Casual Games) charter | [`../../studio/casual-games/library/overview/casual-games-studio.md`](../../studio/casual-games/library/overview/casual-games-studio.md) |

---

## 8. Document Version History

| Version | Date           | Author           | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------- | -------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0     | April 20, 2026 | Operating Review | Initial index established; first plan filed (OPT-2026-04-20-001)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 1.1     | April 20, 2026 | Operating Review | Pre-audit double-review pass: required-sections list expanded to match the actual plan template (added Optimization Topics, Out of Scope, Document Version History); §2 status aligned to lifecycle bucket (`Awaiting Audit`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 1.2     | April 21, 2026 | Operating Review | OPT-2026-04-20-001 transitioned `Approved → In Progress` on Day 1 of execution. §2 row updated with status + tracker companion link. §3 status counts updated (Approved 1 → 0; In Progress 0 → 1). New artifact in folder: execution tracker `2026-04-20-execution-tracker.md`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 1.3     | April 21, 2026 | Operating Review | **Folder convention introduced for multi-artifact plans.** Per CEO directive, OPT-2026-04-20-001's plan and execution tracker were relocated into a new dedicated sub-folder `2026-04-20-operating-model-review/` and renamed to drop the redundant date prefix (`operating-model-review-and-optimization-plan.md`, `execution-tracker.md`). §1 Filename Pattern updated to document both single-file and folder-grouped patterns. §2 Plan Index file column updated to point at the new sub-folder paths. §4 Step 3 updated to advise the folder pattern when companion artifacts are anticipated. Plan and tracker headers also bumped (Plan v1.5 → v1.6; Tracker v1.0 → v1.1) with their own changelog entries.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 1.4     | April 21, 2026 | Operating Review | **Multi-artifact folder pattern codified as a documented best practice + plan filename normalized to canonical `optimization-plan.md`.** Two CEO-directed structural changes filed together. (1) The plan inside the OPT-2026-04-20-001 folder was renamed from `operating-model-review-and-optimization-plan.md` to `optimization-plan.md` because the folder name already supplies the scope; the file only needs to identify the _kind_ of artifact. (2) New top-level §2 "Multi-Artifact Plan Folder Structure (Best Practice)" added, codifying: canonical folder layout (§2.1) with a tree diagram, strict naming rules (§2.2), cross-reference rules (§2.3), versioning + audit-log discipline (§2.4), flat-vs-folder decision matrix (§2.5), and a documented promotion path from flat → folder (§2.6). Subsequent sections renumbered §2→§3 (Plan Index), §3→§4 (Status Summary), §4→§5 (How to File), §5→§6 (Lifecycle Diagram), §6→§7 (Cross-References), §7→§8 (Document Version History). §1 Filename Pattern row tightened and now points at §2 for the canonical multi-artifact pattern. §5 (formerly §4) Step 3 updated to reference §2.5 + §2.1 + §2.2. Closing line updated for the new section numbers. §3 (formerly §2) Plan Index file column updated to the new plan filename. Plan and tracker bumped accordingly (Plan v1.6 → v1.7; Tracker v1.1 → v1.2) with their own changelog + audit-log entries. **Audit posture preserved:** prior changelog entries (v1.0 – v1.3) retain their original section numbers; renumbering applies only to the live structure going forward. |

---

_This index is maintained alongside every optimization plan filed in this folder. Update §3 (Plan Index) and §4 (Status Summary) whenever a plan is added, status-changed, or superseded. Multi-artifact plans MUST follow the folder convention codified in §2._
