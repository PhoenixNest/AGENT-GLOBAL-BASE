# academic-neural-unit-00/ — Academic Neural Unit 00 (ANU-00)

Entry point for Academic Neural Unit 00. Read this before doing any ANU-00-related work.

---

## What This Is

ANU-00 is an independent academic research entity chartered to investigate frontier fields —
computer science, artificial intelligence, neural networks, and software engineering — and to
build a durable, navigable knowledge base from that research. It is one of the workspace's four
co-resident systems (root `CLAUDE.md` §2), alongside The Company, The Studio, and the CC-00 Lab.

**ANU-00 is architecturally independent of `core-component-00/`.** CC-00 and its Director, Dr.
Elias Vance, held an incubation role only during formation — advisory and methodological support,
not governance, staffing, or line authority — and that involvement formally ended once ANU-00's
own Lead was hired. No ANU-00 role reports into CC-00 or any Company department. Full boundary
statement: `formation/2026-07-23-formation-meeting/formation-report.md` §2.

There is no application code under `academic-neural-unit-00/`. Runnable code lives exclusively in
`core-component-00/`.

---

## The Stage-of-Inquiry Test (Mandatory for Scoping Any ANU-00 Work)

Per the CEO-approved charter refinement (`formation-report.md` §3.1), every research question or
proposed deliverable is scoped by **stage of inquiry**, not by which field's vocabulary it uses:

| Stage                                                                | Owner  |
| -------------------------------------------------------------------- | ------ |
| Pre-implementation — "does this work / is it worth pursuing"         | ANU-00 |
| Post-validation — "given that it works, how do we build it reliably" | CC-00  |

This applies even when a question shares vocabulary with a CC-00 module (e.g., "investigate
emergent multi-agent coordination behavior" is ANU-00; "harden a coordination pattern into a
reusable orchestration module" is CC-00, per `multi-agent-engineering/`).

**Migrate-vs-task distinction (binding):** a finding migrating from an ANU-00 programme into a
future CC-00 initiative is ordinary research uptake and does not require special ratification.
ANU-00 being _tasked_ by CC-00, Dr. Vance, or the CEO to de-risk a specific item already on CC-00's
roadmap, on request, recreates the "direct link" the CEO's original ruling prohibits — decline or
escalate to the CEO instead of chartering it as an ordinary programme. Full detail:
`crew/lead/naledi-mokoena/skills/research-programme-chartering.md`.

**One universal exception — ASE governance.** Root `CLAUDE.md` §9 makes the Agent Systems
Engineering framework mandatory for all LLM-powered systems in this workspace, ANU-00 included.
Any LLM-powered tooling ANU-00 builds (e.g., its knowledge-base ingestion pipeline) is ASE-bound as
a technical standard — this is universal, not a governance link back to CC-00.

---

## Directory Structure

```
academic-neural-unit-00/
├── CLAUDE.md                              ← this file
├── README.md                              ← entity overview, charter, boundary statement
├── formation/
│   └── 2026-07-23-formation-meeting/      ← charter, CEO decisions, final review (canonical history)
└── crew/                                  ← personnel roster (10 FTEs)
    ├── README.md                          ← roster index + activation protocol
    ├── lead/naledi-mokoena/                ← ANU-00 Lead
    ├── research-science/                   ← 7 Research Scientists (flat + one pod, see crew/README.md)
    └── knowledge-systems/tobias-lindqvist/ ← knowledge-base tooling
```

---

## Crew Activation Protocol

To produce output as a named ANU-00 crew member:

1. Read `crew/<functional-area>/[<pod>/]<name>/agent/profile.md` — identity, authority scope,
   seniority.
2. Read all referenced `skills/*.md` files — executable contracts, not suggestions.
3. Adopt their voice; produce output strictly within their documented authority.
4. Escalate organizational or personnel questions to Dr. Mokoena (ANU-00 Lead) — never to Dr.
   Vance or any CC-00 crew member, and never assume CC-00 authority extends here.

**Never impersonate a crew member without reading their profile first.** Full roster, reporting
lines, and span-of-control detail: `crew/README.md`.

---

## Knowledge Base Convention

ANU-00's research output follows the workspace's existing dated research-archive pattern
(`YYYY-MM-DD-<slug>/research-report.md`), the same convention used by `company/telescope/`,
`studio/casual-games/telescope/`, and `core-component-00/telescope/` — for navigational
consistency, not as a link to any one of those archives. No knowledge-base entries exist yet as of
this file's authoring; the convention is established ahead of first use.

---

## Recruitment

Recruitment follows the standard company-wide 9-stage pipeline
(`company/pipeline/recruitment/pipeline.md`) under CHRO authority, the same as every other
department or entity in this workspace — ANU-00 has no separate hiring process of its own.
Historical hiring records: `company/recruitment/academic-neural-unit-00-fy2026-q3/`.

---

## Where to Look

| I need…                                               | Go to                                                                |
| ----------------------------------------------------- | -------------------------------------------------------------------- |
| Full charter, CC-00 boundary, all formation decisions | `formation/2026-07-23-formation-meeting/formation-report.md`         |
| Who was hired and why (candidate-level detail)        | `company/recruitment/academic-neural-unit-00-fy2026-q3/`             |
| Current roster, reporting lines, activation           | `crew/README.md`                                                     |
| A specific crew member's identity and skills          | `crew/<functional-area>/[<pod>/]<name>/`                             |
| Research-programme chartering rules                   | `crew/lead/naledi-mokoena/skills/research-programme-chartering.md`   |
| Workspace-wide conventions this entity still follows  | root `CLAUDE.md` (Prettier formatting, git workflow, ASE governance) |
