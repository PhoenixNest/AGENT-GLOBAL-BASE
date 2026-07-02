# company/telescope/ — Company Research Archive

Research archive for The Company. Read this before documenting any product-oriented research
investigation.

---

## What This Is

The Company's dedicated instance of the workspace's research-archive pattern — a structured
repository for product-oriented research investigations. Established 2026-07-02 as part of the
CEO-directed decentralization of the former unified workspace-root `telescope/`, which had been
exclusively CC-00-flavored. See workspace-root `telescope/README.md` for the cross-department
index and rationale.

---

## Scope

**In scope:** product-oriented research feeding the Company's 13-stage development pipeline —
competitive teardowns, JTBD/market validation studies, App Store/Play policy analyses,
pricing/paywall and monetization-model research, and post-launch feature-validation retros
(did a shipped feature hit its PRD success/kill criteria). Ties primarily to Stage 0 (Problem
Validation), Stage 1 (Requirements → PRD/SRD), and Stage 6/8/10 retros.

**Out of scope:** engineering/LLM research (→ `core-component-00/telescope/`), game-design/
competitive/live-ops research (→ `studio/casual-games/telescope/`), and workspace-wide governance
research (stays at workspace-root `telescope/`).

---

## Relationship to Other Company Knowledge Structures

Telescope is a _dated investigation log_ — point-in-time, append-only, sometimes superseded by
later work. It is distinct from, and feeds into, other Company structures:

| Structure                       | Role                                                                          |
| ------------------------------- | ----------------------------------------------------------------------------- |
| `company/telescope/`            | Raw dated investigation — the finding, as first produced                      |
| `company/library/`              | Distilled, stable summary — a finding that held up gets a line here           |
| `company/optimization-history/` | Retrospective on completed optimization cycles — different axis, do not merge |
| `recruitment/`                  | Hiring-specific market/comp research stays here, not in telescope             |

A Telescope finding is evidence, never an ADR substitute — a research report recommending a
stack or pricing-model change still routes through the real Stage 1/3 approval gates, it does not
bypass them.

---

## Directory Structure

```
company/telescope/
├── README.md              ← Archive index
└── template/               ← Report template (use this for every new report)
    ├── research-report.md
    └── qa-document.md
```

---

## Creating a New Research Report

1. Create a new folder: `YYYY-MM-DD-<slug>/`
2. Copy the template: `template/research-report.md` → `YYYY-MM-DD-<slug>/research-report.md`
3. Complete the report — for product research, extend it with a market-sizing/competitive-teardown
   table and explicit success/kill criteria where applicable, consistent with PRD gating
4. Add an entry to `README.md` (the archive index)

Naming, lifecycle, append-only policy, versioning, and quality standards follow the same shared
conventions as every other telescope instance — see workspace-root `telescope/CLAUDE.md`.

---

## Who Can Write Here

Write access is open to Company C-suite — CDO, CIO/CSO, CLO, CTO-L, CHRO — for research that
touches product decisions (e.g. a security threat-landscape study, a localization market study).
The CPO curates and indexes: final say on what's admitted to the index and whether it meets bar.

---

## Ownership

- **Curator/Owner:** Marcus Tran-Yoshida, CPO
- **Profile:** `company/departments/product-management/`
- **Authority:** `company/CLAUDE.md` § Departments & C-Suite Owners
