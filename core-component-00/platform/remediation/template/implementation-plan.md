# Implementation Plan — [Layer Name]

<!-- Copy this file into a NEW FOLDER core-component-00/platform/remediation/engineering/<module-slug>/YYYY-MM-DD-<slug>/
     (or retrieval-augmented-generation/YYYY-MM-DD-<slug>/ for Layer 4) — not into template/ itself
     — per core-component-00/platform/remediation/CLAUDE.md § Directory Structure. This file inside it is
     always named `implementation-plan.md`.

     Governed by core-component-00/platform/remediation/pipeline.md — read it before opening a topic,
     especially the Scoping Rule (which benchmark rows qualify) and the Hook-Change Gate (a second,
     separate approval required before executing any fix touching .claude/hooks/*.py).

     This file is the SHORT, always-current summary — Zhao's "working memory" framing, same as
     core-component-00/platform/maintenance-records/template/maintenance-record.md. The full account of
     each stage lives in log/ instead. -->

---

## Metadata

| Field                       | Value                                                                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Plan ID**                 | `YYYY-MM-DD-<layer-slug>-remediation`                                                                                                                              |
| **Layer**                   | [1 Prompt / 2 Context / 3 Harness / 4 RAG / 5 Multi-Agent]                                                                                                         |
| **Source Benchmark Report** | [Link to the signed-off `enterprise-assessment.md` this plan executes against]                                                                                     |
| **Owner**                   | [Name, role — must hold documented authority over the code/docs this plan changes, per `crew/CLAUDE.md`]                                                           |
| **Reviewer**                | [Name, role — MUST be different from Owner; no self-authorization exception in this pipeline]                                                                      |
| **Hook-Change Gate**        | [N/A — no item touches `.claude/hooks/*.py`] OR [Pending User sign-off — item(s) `Rn` blocked at this gate] OR [Granted YYYY-MM-DD by User — item(s) `Rn` cleared] |
| **Status**                  | [Open / Drafted, pending review / Approved / In Progress / Executed, pending verification / Verified / Reopened — see log/NN-....md]                               |

**Reviewer requirement.** No item in this plan may reach `Status: Verified` on the strength of
Owner self-verification — see `pipeline.md` stage 4. This is stricter than
`maintenance-records/`'s equivalent gate, which allows self-authorization for low-severity infra
work; every item here is a production module fix.

---

## Included Items

One row per item admitted under `pipeline.md`'s Scoping Rule — every row must cite its source
Benchmark Row ID. An item with no citation is invalid per the same "no orphan claims" discipline
`benchmarks/template/enterprise-assessment.md` uses.

| ID  | Source Row          | Gap (restated, one line) | Severity (inherited)                  | Item Owner                          | Approach                        | Acceptance Criteria              | Test Plan                        | Target Date  | Item Status                                             |
| --- | ------------------- | ------------------------ | ------------------------------------- | ----------------------------------- | ------------------------------- | -------------------------------- | -------------------------------- | ------------ | ------------------------------------------------------- |
| I1  | [Rn, source report] | [one-line restatement]   | [P0-P3, inherited — do not re-derive] | [Name — may differ from plan Owner] | [Concrete engineering approach] | [Observable, testable condition] | [Specific commands/tests to run] | [YYYY-MM-DD] | [Not Started / In Progress / Blocked / Done / Verified] |

**Rules.**

- **Severity is inherited, never re-derived here** — see `pipeline.md` § Severity.
- **Item Owner may differ from the plan's Metadata Owner** (e.g. a co-owned item), but must still
  hold documented authority over that item's specific fix per `crew/CLAUDE.md`.
- **"Blocked" status must name what it's blocked on** in the Cross-Layer Dependencies section
  below or in the item's own `log/` entry — a bare "Blocked" with no stated cause is not
  citable status.

---

## Cross-Layer Dependencies

<!-- Name any item in THIS plan that depends on, conflicts with, or coordinates with an item in
     ANOTHER layer's plan. State the relationship explicitly — "depends on" (cannot start until
     the other item clears), "conflicts with" (the two items' Approaches contradict and need one
     arbitrated decision before either proceeds — name who arbitrates), or "coordinates with"
     (shared underlying code/resource, independently executable). An item claimed here as an
     external dependency owned by another plan must NOT also appear in this plan's Included Items
     table — it is owned there, not here. -->

[None / table: This Item | Related Item (other plan) | Relationship | Arbitrated By (if conflict)]

---

## Gate Log

Per `pipeline.md`. One row per stage reached so far, oldest first.

| Stage       | Entry                                                                          | Summary                |
| ----------- | ------------------------------------------------------------------------------ | ---------------------- |
| 0 — Trigger | `core-component-00/platform/remediation/.../log/01-drafting-<items>-opened.md` | [one-sentence summary] |

<!-- Add a row per subsequent stage reached, including the Hook-Change Gate if this plan has any
     hook-touching item, and any Reopen edge per pipeline.md's loop-back. Name each log file
     log/NN-<stage-slug>-<items>-<outcome>.md per pipeline.md § Log File Naming — never a bare
     stage name like "02-approval.md". -->

---

## Open Follow-Up Items

[None / table, each with an owner and target date]

---

## Related Records

- **Source benchmark report:** [path]
- **Backlog items for this layer (P2/P3, not in this plan):** `core-component-00/platform/remediation/README.md` § Remediation Backlog
- [Any other related plan, maintenance record, or ADR]
