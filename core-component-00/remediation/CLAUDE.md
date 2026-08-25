# core-component-00/remediation/ — CC-00 Remediation Program

Execution-tracking archive for the Core Component 00 Laboratory. Read this before opening or
updating any Implementation Plan for a gap identified in `core-component-00/benchmarks/`.

---

## What This Is

A record of **execution** against the P0/P1 findings in the CC-00 enterprise benchmark series
(`core-component-00/benchmarks/`) — approach, acceptance criteria, test plan, status, and
verification for the gaps severe enough to warrant dedicated tracking. This is distinct from
every other CC-00 record type:

- `core-component-00/benchmarks/` — the point-in-time external comparison that _finds_ a gap.
  Its own Severity-Ordered Remediation Plan table names Owner/Fix/Severity per gap and does not
  change after the document is signed off — that table is the audit trail, not a live tracker.
- `core-component-00/maintenance-records/` — operational upkeep of lab infrastructure (servers,
  dependencies, GPU/CUDA, MCP processes). This folder inherits that folder's structure
  (topic folder + always-current summary + append-only `log/`) but tracks **module code and
  documentation remediation**, not infrastructure operations.
- `core-component-00/telescope/` — research investigations, not execution against a known gap.
- `crew/director/elias-vance/skills/asgf-compliance-audit.md` — internal compliance audit
  against our own ASGF standard, a different question than "is this benchmark finding fixed."

Established 2026-08-17 at CEO direction, following the same "created at CEO direction" precedent
as `benchmarks/` (2026-08-16) and `maintenance-records/` (2026-07). The CEO's 2026-08-17 sign-off
authorizes creating this archive and its five layer plans (**Gate 1** — see `pipeline.md`). It
does **not** authorize any code change to `.claude/hooks/*.py` — that requires a separate,
explicit User sign-off (**Gate 2**), not yet granted as of this folder's creation.

---

## Scope

**In scope:** Implementation Plans executing a `P0` or `P1` row from a signed-off
`core-component-00/benchmarks/**/enterprise-assessment.md` Severity-Ordered Remediation Plan, or a
`P2`/`P3` row admitted into a plan via dependency closure (it blocks or is required by an in-scope
P0/P1 row — see `pipeline.md` § Scoping Rule).

**Out of scope:** the benchmark assessments themselves (→ `core-component-00/benchmarks/`); P2/P3
rows with no dependency link to an in-scope item (tracked in this folder's `README.md` §
Remediation Backlog instead — a table, not a dedicated plan); lab infrastructure maintenance
(→ `core-component-00/maintenance-records/`); ASGF compliance audits
(→ `crew/director/elias-vance/skills/asgf-compliance-audit.md`).

---

## Directory Structure

```
core-component-00/remediation/
├── README.md                              ← Plan index + Remediation Backlog table
├── CLAUDE.md                              ← This file
├── pipeline.md                            ← Canonical stage definitions, gates, severity handling
├── template/
│   ├── implementation-plan.md             ← Copy for every new topic's main record
│   └── log-entry.md                       ← Copy for every stage/development within a topic
├── engineering/                           ← Type-scoped, mirrors benchmarks/engineering/
│   ├── prompt-engineering/
│   │   └── <YYYY-MM-DD-slug>/
│   │       ├── implementation-plan.md
│   │       └── log/
│   ├── context-engineering/
│   ├── harness-engineering/
│   └── multi-agent-engineering/
└── retrieval-augmented-generation/        ← Layer 4 — PARALLEL to engineering/, not inside it
    └── <YYYY-MM-DD-slug>/
        ├── implementation-plan.md
        └── log/
```

One folder per **layer's remediation topic** — not one folder per remediation row. A layer's
Implementation Plan bundles every in-scope item from that layer's benchmark report (see
`pipeline.md` § Scoping Rule for what qualifies), the same way `benchmarks/` bundles a whole
layer's findings into one report rather than one file per finding.

---

## Creating or Updating an Implementation Plan

**New topic:**

1. Create folder `engineering/<module-slug>/YYYY-MM-DD-<slug>/` (or
   `retrieval-augmented-generation/YYYY-MM-DD-<slug>/` for Layer 4).
2. Copy `template/implementation-plan.md` into it; fill in Metadata, the Included Items table
   (citing each item's source Benchmark Row ID — no orphan rows, same discipline as
   `benchmarks/template/enterprise-assessment.md`), and Cross-Layer Dependencies.
3. Copy `template/log-entry.md` → `<slug>/log/01-drafting.md` for the Drafting stage.
4. Add an entry to `README.md` (the plan index).
5. Run Prettier: `prettier --write "<file-path>"`.

**Follow-up on an existing topic** (a later stage, an incident, a status change): copy
`template/log-entry.md` → `<slug>/log/NN-<slug>.md` (never edit or delete a prior entry), update
the plan's header **Status** field, add a row to its Gate Log. Full rules, including the
topic-boundary test: `pipeline.md`.

---

## Who Can Write Here

Per `crew/CLAUDE.md` § Authority Scope, same mapping as `benchmarks/`:

- Dr. Elias Vance (Laboratory Director) — any plan, plus cross-layer arbitration decisions
- Module leads (Zhao, Asante, Almeida, Farouk) — plans for their own owned module
- Dr. Tomasz Wieczorek (Safety & Evaluation) — Reviewer role on any plan, and Owner on any item
  that is a Safety-scoped finding rather than a module-design finding (e.g. Prompt R4)
- Research Engineer IIs may own an individual item within a plan but do not own the plan itself

**A module lead cannot own a plan item whose fix lands outside their module's own code or docs.**
This is why Context Engineering's R1 (a fix to a Harness-owned hook) sits in the Harness
Implementation Plan, cited by the Context plan only as an external dependency — see that plan's
Cross-Layer Dependencies section.

---

## Ownership

- **Owner:** Dr. Elias Vance, CC-00 Laboratory Director
- **Profile:** `core-component-00/crew/director/elias-vance/agent/profile.md`
- **Authority:** AGENTS.md § 6. Core Component 00
