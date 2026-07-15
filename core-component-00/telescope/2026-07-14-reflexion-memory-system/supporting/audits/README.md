# `supporting/audits/` — Internal Audits and Scoring

**Programme:** `2026-07-14-reflexion-memory-system`
**Established:** 2026-07-14, at the CEO's direction, after review/evaluation/scoring documents
were found filed as ordinary numbered `supporting/` documents indistinguishable from design
artifacts. **Revised:** 2026-07-14, same day, on two further CEO points: (1) a mistake log must
never be logged into, or otherwise couple with, a file belonging to a different investigation —
see the correction recorded in `mistake-log.md`'s own banner; (2) audit/scoring documents should
be categorized by the research lifecycle stage they were produced in, not left flat in one
undifferentiated folder, especially while a Programme is still early. This file documents both
the folder-level convention and, below, the stage taxonomy that revision introduced.

**Scope of this convention (corrected 2026-07-14):** this file is currently the sole authoritative
copy. An earlier version of this convention was also copied into
`core-component-00/telescope/CLAUDE.md` — the CC-00 telescope charter Claude Code auto-loads as
binding instruction for every session working in this directory — on the same day the convention
was first invented and then revised twice more. The CEO asked whether promoting a same-day,
still-changing convention directly into an auto-loaded instruction file was appropriate; on
reflection it was premature, and that edit has been reverted. `CLAUDE.md` files are not ordinary
documentation — they are instructions Claude Code treats as binding without being separately
re-read or re-approved each time, so a convention should be validated (used again by a second
Programme, or explicitly confirmed by the CEO) before being promoted there, not promoted on first
invention. Until then, this Programme's own `supporting/audits/README.md` is the only place this
convention lives; a future Programme reusing it should read this file directly, not
`core-component-00/telescope/CLAUDE.md`.

---

## Why a Separate Subfolder

A telescope Programme's `supporting/` folder holds "everything ancillary: diagrams,
deployment/migration plans, sub-investigation reports, implementation plans"
(`telescope/CLAUDE.md`). Those are all **design-artifact** documents — they describe what is being
built and why. A self-review, an adversarial evaluation, a director alignment check, or a mistake
log are a structurally different kind of document — they **score or audit** a design artifact
from outside it, often by a reviewer deliberately independent of the person who authored the
artifact being reviewed (see `crew/CLAUDE.md`'s structural-independence rule). `audits/` is that
boundary, made explicit.

This is a nested subfolder **inside** the one `supporting/` folder the Programme shape already
permits — it does not add a second subfolder at the investigation root, so it does not conflict
with `telescope/CLAUDE.md`'s "no other subfolder name is permitted at the investigation root"
rule. `supporting/` remains the only root-level subfolder; `audits/` — and the stage folders
nested inside it below — are organization within it.

---

## Stage Taxonomy (introduced 2026-07-14)

One-shot review/scoring reports are further grouped by which stage of the research lifecycle
produced them, since a review performed before any implementation exists asks fundamentally
different questions (does the proposal make sense?) than one performed after code is merged
(does the implementation match the proposal, and does it actually work?). Stage folders are
created lazily — only when the first audit for that stage actually exists, matching this
convention's existing "don't create an empty `mistake-log.md` preemptively" rule below.

| Stage folder                                           | When it applies                                                                                                                                      | Typical audit types filed here                                                                                          |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `01-design-stage/`                                     | Before any implementation is authorized — the proposal is still being reviewed for soundness, completeness, and alignment with the commissioning ask | `safety-self-review`, `director-alignment-review`                                                                       |
| `02-implementation-stage/` (reserved, not yet created) | After the CEO authorizes implementation and code exists to audit against the design                                                                  | `ase-compliance-audit`, `adversarial-evaluation` run against real code, `threshold-sensitivity-check` against real data |
| `03-operational-stage/` (reserved, not yet created)    | After deployment, auditing live behavior rather than a design or a merge                                                                             | incident-driven reviews, drift/recalibration audits                                                                     |

This Programme is currently entirely in the design stage (`research-report.md` Metadata:
"Complete — design/research only; implementation not yet authorized"), so only
`01-design-stage/` exists. The other two are documented here as reserved names so a future
reviewer creates the correctly-named folder on first use rather than inventing a new name.

**The mistake log is the one exception and stays at `audits/` root, not stage-nested.** A process
violation can occur at any stage, and nesting a single chronological, append-only log by stage
would require re-filing or splitting it as a Programme progresses through stages — churn with no
retrieval benefit, since a reader wants the full violation history in one place regardless of
which stage each entry happened in. Each entry's own `Date of violation` field is sufficient to
place it in time; a `Stage at time of violation` field may be added per-entry if a future Programme
finds that useful, without moving the file itself.

---

## Naming Convention

### Folder names

`audits/` — always this name, always nested one level inside a Programme's `supporting/` folder.
Stage folders inside it use the fixed names in the table above (`01-design-stage/`,
`02-implementation-stage/`, `03-operational-stage/`), numbered for reliable sort order regardless
of naming coincidence. Do not use `reviews/`, `evaluations/`, `qa/`, or invented stage names.

### File names — two kinds

**1. One-shot review/scoring reports** — `NN-<audit-type>.md` inside the relevant stage folder,
numbered locally within that stage (each stage folder restarts its own sequence at `01`).
`<audit-type>` is a short kebab-case label naming the review's _function_, not the reviewer's name:

| Audit type slug               | Function                                                                          | Typical reviewer role                                        |
| ----------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `safety-self-review`          | Independent completeness + adversarial safety check against the commissioning ask | Staff Safety & Evaluation Engineer                           |
| `director-alignment-review`   | Does the design stay true to the commissioned research focus, or drift            | Laboratory Director                                          |
| `adversarial-evaluation`      | Red-team a specific mechanism (e.g. a write path, a contradiction check)          | Staff Safety & Evaluation Engineer                           |
| `ase-compliance-audit`        | Formal ASE four-layer ratification check                                          | Laboratory Director (ratification) / module lead (execution) |
| `threshold-sensitivity-check` | Numeric parameter validation against synthetic or real data                       | Module lead                                                  |

Not exhaustive — add a new slug to this table the first time it's used (see the Scope note above
for why this table, not `core-component-00/telescope/CLAUDE.md`, is currently the authoritative
copy).

**2. The mistake log** — always exactly `audits/mistake-log.md` (folder root, not stage-nested, per
above), no number prefix, singular per Programme. Entry IDs inside it are investigation-scoped —
`MISTAKE-<investigation-date>-<NNN>` — so this file never shares a counter with, or needs to edit,
any other investigation's mistake log. A Programme only has a `mistake-log.md` if a process
violation or comparable finding actually arose during its execution; do not create an empty one
preemptively.

---

## Contents of This Folder

| File                                              | Stage                     | Type            | Reviewer                                 | Verdict                                        |
| ------------------------------------------------- | ------------------------- | --------------- | ---------------------------------------- | ---------------------------------------------- |
| `01-design-stage/01-safety-self-review.md`        | Design                    | One-shot review | Dr. Tomasz Wieczorek                     | Conditionally ready for CEO sign-off           |
| `01-design-stage/02-director-alignment-review.md` | Design                    | One-shot review | Dr. Elias Vance                          | Aligned, with a required framing clarification |
| `mistake-log.md`                                  | (cross-stage, not nested) | Running log     | Dr. Elias Vance (on report from the CEO) | `MISTAKE-2026-07-14-001` closed 2026-07-15     |

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-14-reflexion-memory-system`
