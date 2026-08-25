# core-component-00/benchmarks/ — CC-00 Enterprise Benchmark Archive

External benchmark archive for the Core Component 00 Laboratory. Read this before running or
documenting any enterprise-level assessment of a CC-00 module or the workspace's LLM engineering
design.

---

## What This Is

A record of assessments comparing CC-00 modules — or the workspace's LLM engineering design as a
whole — against **current external, enterprise-grade / industry-standard practice**. This is
distinct from every other CC-00 record type:

- `core-component-00/telescope/` — internal research investigations (a compression strategy,
  a competitive framework survey)
- `core-component-00/maintenance-records/` — operational maintenance history (servers,
  dependencies, MCP infra)
- `crew/director/elias-vance/skills/asgf-compliance-audit.md` — internal compliance audit against
  our **own** ASGF standard

A benchmark asks "how does this compare to what production systems elsewhere are doing" — never
"does this satisfy our own rules." Its defining, non-negotiable requirement is a **live external
research pass in the same session**, every time — the assessor's training-data knowledge cutoff is
never sufficient on its own, because "enterprise-standard practice" is a moving target. See the
template's Research Freshness section.

---

## Scope

**In scope:** any assessment benchmarking a CC-00 module's implementation, architecture, or
design against current external industry/enterprise practice — Context, Harness, RAG,
Multi-Agent, Prompt Engineering, or the workspace's engineering design cross-cutting all five.

**Out of scope:** internal research investigations with no external-benchmark framing
(→ `core-component-00/telescope/`), operational maintenance work
(→ `core-component-00/maintenance-records/`), and internal ASGF compliance audits
(→ `crew/director/elias-vance/skills/asgf-compliance-audit.md`).

---

## Directory Structure

```
core-component-00/benchmarks/
├── README.md                              ← Assessment index
├── CLAUDE.md                              ← This file
├── template/
│   └── enterprise-assessment.md           ← Copy for every new assessment
├── engineering/                           ← Type-scoped, mirrors core-component-00/engineering/
│   ├── prompt-engineering/                ← Layer 1
│   │   └── <YYYY-MM-DD-slug>/
│   │       └── enterprise-assessment.md
│   ├── context-engineering/               ← Layer 2
│   │   └── <YYYY-MM-DD-slug>/
│   │       └── enterprise-assessment.md
│   ├── harness-engineering/                ← Layer 3
│   │   └── <YYYY-MM-DD-slug>/
│   │       └── enterprise-assessment.md
│   └── multi-agent-engineering/           ← Layer 5
│       └── <YYYY-MM-DD-slug>/
│           └── enterprise-assessment.md
└── retrieval-augmented-generation/        ← Layer 4 — PARALLEL to engineering/, not inside it
    └── <YYYY-MM-DD-slug>/
        └── enterprise-assessment.md
```

**Type-scoped, dated-folder-per-assessment** (established 2026-08-16 at CEO direction). The
`engineering/<module>/` layer mirrors `core-component-00/engineering/`'s own four subfolders
one-for-one — Prompt, Context, Harness, and Multi-Agent Engineering — so a reader can find a
module's benchmark history the same way they'd find its implementation. RAG
(`retrieval-augmented-generation/`) sits outside `core-component-00/engineering/` in the real
module layout (see `core-component-00/CLAUDE.md`'s note on the 2026-07-16 relocation), so its
benchmark folder sits parallel to `engineering/` at the top of `benchmarks/`, mirroring that same
real-layout distinction rather than nesting it under `engineering/` for false consistency. Within
each module folder, assessments remain dated-folder-per-topic, matching the shape already
established by `telescope/` and `maintenance-records/` for this workspace's other CC-00 archive
types.

**Layer sequence.** The five-module stack has a canonical order (see
`core-component-00/CLAUDE.md` § The Five-Module Engineering Stack): 1 Prompt → 2 Context → 3
Harness → 4 RAG → 5 Multi-Agent. Whenever assessments are run as a set (e.g. "benchmark the rest
of the stack"), conduct and report them in this layer order, not alphabetically or by folder
listing order — a later layer's design frequently assumes an earlier layer's guarantees (e.g.
Harness's token-budget enforcement assumes Context's compressor exists), so reviewing out of
order risks flagging a gap that a lower layer already explains.

---

## Creating a New Assessment

1. Create folder `engineering/<module-slug>/YYYY-MM-DD-<slug>/` in this directory (e.g.
   `engineering/context-engineering/2026-08-16-context-engineering-enterprise-assessment/`).
2. Copy `template/enterprise-assessment.md` → `<slug>/enterprise-assessment.md`.
3. Run live external research (WebSearch/WebFetch) before filling in the Benchmark Table — the
   Research Freshness section must be completed first and is not optional.
4. Fill in every section; every "Enterprise-Standard Practice" claim must trace to a source in
   Research Freshness.
5. Add an entry to `README.md` (the assessment index).
6. Run Prettier before finalizing: `prettier --write "<file-path>"`.

**Updating an existing assessment topic** (a follow-up pass on the same module): follow
`telescope/`'s versioning convention — add a dated entry to the assessment's own Version History
table rather than overwriting prior findings, or open a new dated folder if enough has changed
that it constitutes a fresh assessment rather than a revision.

---

## Who Can Write Here

- Dr. Elias Vance (Laboratory Director) — any module, plus workspace-wide assessments
- Module leads (Zhao, Asante, Almeida, Farouk) — assessments of their own owned module, per
  `crew/CLAUDE.md` § Authority Scope
- Research Engineer IIs may contribute findings but escalate the assessment's verdict to their
  module lead, same as any other module-design output

---

## Ownership

- **Owner:** Dr. Elias Vance, CC-00 Laboratory Director
- **Profile:** `core-component-00/crew/director/elias-vance/agent/profile.md`
- **Authority:** AGENTS.md § 6. Core Component 00
