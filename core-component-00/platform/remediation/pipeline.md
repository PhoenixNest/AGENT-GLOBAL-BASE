# CC-00 Remediation Pipeline

Canonical stage definitions for a CC-00 remediation topic (`core-component-00/platform/remediation/`). Per
workspace convention (`templates/README.md`, `company/pipeline/*/pipeline.md`), this file — not
`CLAUDE.md`, not `README.md` — is the authoritative source of truth for pipeline stages and gates.

Modeled directly on `core-component-00/platform/maintenance-records/pipeline.md`'s six-stage,
loop-back-edge shape, with two additions this pipeline needs that maintenance topics don't: a
**Scoping Rule** (which benchmark findings become a tracked topic at all) and a **Hook-Change
Gate** (a second, explicit approval layer for any fix touching `.claude/hooks/*.py`, since those
files govern behavior every live session in this workspace depends on).

---

## Scoping Rule

Not every `Partial`/`Gap` row in a benchmark report's Severity-Ordered Remediation Plan becomes a
remediation topic. A row qualifies if **either**:

1. It is tagged `P0` or `P1` in its source benchmark report, **or**
2. It is `P2`/`P3` but sits in a genuine dependency-closure relationship with a qualifying row —
   it blocks that row's fix, or that row's fix cannot be verified without it (e.g. a P2 regression
   test that is the only thing making a P1 fix's "no silent fallthrough" claim checkable).

A `P2`/`P3` row with no such link goes to this folder's `README.md` § Remediation Backlog table
instead — named owner, no dedicated plan, revisited at the source module's next benchmark refresh.
Do not admit a row into a plan "for completeness" — an unlinked P2 in a P0/P1 plan dilutes the
plan's verification bar for no reason; that is what the backlog is for.

---

## Topology

```
Trigger → Drafting → Approval → [Hook-Change Gate, if applicable] → Execution → Verification → Close
              ↑                                                                       │
              └──────────────────────── Reopen (new problem found) ──────────────────┘
```

---

## Stages

| #   | Stage                              | Entry criterion                                                          | Exit criterion                                                                                                                                                                   | Owner                                                     | Gate                                                                                                                                                                                                                                                                                                         |
| --- | ---------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0   | **Trigger**                        | A signed-off benchmark report has one or more qualifying rows            | Folder `<YYYY-MM-DD-slug>/` created with `implementation-plan.md`; `Status: Open`                                                                                                | The layer's Owner (per `CLAUDE.md` § Who Can Write Here)  | **CEO gate (folder-level, one-time):** establishing `core-component-00/platform/remediation/` itself required CEO sign-off (granted 2026-08-17). Opening a _topic_ inside it needs no separate CEO approval — that authorization already covers all five layer plans.                                        |
| 1   | **Drafting**                       | Topic open, items not yet scoped with Approach/Acceptance/Test           | Included Items table complete for every qualifying row; `log/01-drafting-<items>-opened.md` written (see § Log File Naming); `Status: Drafted, pending review`                   | The layer's Owner                                         | None to draft; every item must cite its source Benchmark Row ID — an item with no citation is invalid, same rule as the benchmark template's "no orphan claims"                                                                                                                                              |
| 2   | **Approval**                       | A drafted plan exists                                                    | Reviewer (distinct from Owner, per `crew/CLAUDE.md`) signs off on the Approach for every item; `Status: Approved` for items with no hook change, or held at the Hook-Change Gate | The plan's named Reviewer                                 | **Required, no exception.** Unlike `maintenance-records/pipeline.md` stage 2 (where self-authorization is a valid outcome), this stage never accepts Owner-as-Reviewer — these are production module fixes, not infra upkeep.                                                                                |
| —   | **Hook-Change Gate** (conditional) | An approved item's fix touches `.claude/hooks/*.py`                      | Explicit, separate User sign-off recorded in the plan's Metadata **Hook-Change Gate** field, naming the item(s) and the date approved                                            | The User (not delegable to Reviewer, Owner, or Dr. Vance) | **Required before Execution starts on that item.** Root `CLAUDE.md` §11 documents these hooks as active protocols live sessions depend on; Approval-stage sign-off does not substitute for this. Items not touching a hook skip this gate and proceed straight to Execution.                                 |
| 3   | **Execution**                      | Item(s) cleared through stage 2 (and the Hook-Change Gate if applicable) | Changes made and logged to `log/NN-execution-<items>-<outcome>.md`, one entry per distinct action; `Status: In Progress` → `Status: Executed, pending verification`              | The item's named Owner                                    | None to execute once cleared; **if a new problem is found mid-execution**, do not keep executing — open `log/NN-incident-<items>-<outcome>.md` immediately and route to the Reopen edge below (mirrors `maintenance-records/pipeline.md` stage 3)                                                            |
| 4   | **Verification**                   | Execution stage has a testable claim                                     | Verification table in the relevant `log/` entry: actual commands/checks run and results — never a restated intention                                                             | Reviewer, distinct from the executing Owner               | **Independent-review gate, mandatory for every item in this folder** (stricter than `maintenance-records/pipeline.md`, which makes this conditional on severity) — plus a green run of the owning module's pytest suite (`core-component-00/CLAUDE.md` § Running Tests) before `Status` may read `Verified`. |
| 5   | **Close (or Reopen)**              | Verification passed, or a new problem was found                          | **Close:** `Status: Verified`. **Reopen:** append `log/NN-incident.md`, set `Status: Reopened — see <entry>`, return to stage 1                                                  | Whoever completes verification                            | **Escalation path:** if a topic stalls, escalate to Dr. Vance and note the escalation as its own `log/` entry (mirrors `maintenance-records/pipeline.md` stage 5).                                                                                                                                           |

---

## Log File Naming

A log filename must let a reader determine stage, scope, and outcome **from a directory listing
alone**, without opening the file. Bare stage names (`02-approval.md`) fail this — two different
plans' `02-approval.md` files can cover entirely different items with entirely different
outcomes, and nothing in the name says which. Format:

```
log/NN-<stage-slug>-<items>-<outcome>.md
```

| Segment      | Meaning                                                                                        | Examples                                                                            |
| ------------ | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `NN`         | Two-digit sequence, in the order stages/developments actually happened (unchanged from before) | `01`, `02`, `03`                                                                    |
| `stage-slug` | The pipeline stage this entry belongs to, kebab-case                                           | `drafting`, `approval`, `hook-change-gate`, `execution`, `verification`, `incident` |
| `items`      | Which Included Items row ID(s) this entry concerns, lowercase, hyphenated if a range or list   | `i1-i5`, `i4-i5`, `i2`                                                              |
| `outcome`    | One word, past tense, the actual result — not a restatement of the stage name                  | `opened`, `approved`, `arbitrated`, `granted`, `executed`, `verified`, `blocked`    |

Examples from this program: `01-drafting-i1-i5-opened.md`, `02-approval-i1-i2-approved.md`,
`02-approval-i1-i5-arbitrated.md` (Harness — the arbitration, not the routine sign-off, is the
notable event), `03-hook-change-gate-i4-i5-granted.md`.

This governs `core-component-00/platform/remediation/` only — it does not retroactively rename
`maintenance-records/`'s existing log files, which predate this convention and have their own.

---

## Severity (inherited, not re-derived)

Every item's severity is the value already assigned in its source benchmark report's
Severity-Ordered Remediation Plan (ASGF Scale A). This pipeline does not re-justify severity — a
plan item that disagrees with its source report's severity is a defect in the _benchmark report_,
to be corrected there (per `benchmarks/CLAUDE.md`'s update procedure), not silently re-tagged here.

---

## Topic-boundary test

A new development belongs in an **existing** topic's folder (new `log/` entry, updated `Status`)
if it concerns the same layer's Implementation Plan and was discovered during, or is a direct
follow-up to, that plan's prior stages. A genuinely different layer, or a newly-admitted item from
a _later_ benchmark refresh of the same layer, gets its own new topic folder. When ambiguous,
default to a new topic (same reasoning as `maintenance-records/pipeline.md`).

---

## Staleness bound

A topic's `Status` field must be updated within the same working session that changes what it
reports as true — identical rule to `maintenance-records/pipeline.md` § Staleness bound.

---

## Related Documentation

- `CLAUDE.md` (this folder) — directory structure, authoring mechanics.
- `README.md` (this folder) — plan index, Remediation Backlog table.
- `template/` — copy-ready templates for `implementation-plan.md` and a `log/` entry.
- `core-component-00/platform/benchmarks/` — the source reports every plan item must cite.
- `core-component-00/platform/maintenance-records/pipeline.md` — the sibling pipeline this one is modeled
  on; read there for the reasoning behind the topic/log split this pipeline reuses.
- `crew/CLAUDE.md` § Authority Scope — who can own or review what.
