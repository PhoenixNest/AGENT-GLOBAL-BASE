# core-component-00/telescope/ — CC-00 Research Archive

Research archive for the Core Component 00 Laboratory. Read this before documenting any
engineering or LLM-research investigation.

---

## What This Is

The Laboratory's dedicated instance of the workspace's research-archive pattern — a structured
repository for engineering and cutting-edge LLM research investigations owned by CC-00. See the
root `telescope/README.md` for the cross-department index.

---

## Scope

**In scope:** engineering and cutting-edge LLM research serving the five CC-00 modules —
context compression, multi-agent orchestration/memory, prompt stability, harness performance,
retrieval-augmented generation, and ASE compliance/governance audits internal to the Lab.

**Out of scope:** product-market research (→ `company/telescope/`), game-design/competitive/
live-ops research (→ `studio/casual-games/telescope/`), and workspace-wide governance research
that affects every department at once (stays at the workspace-root `telescope/` — see that
folder's CLAUDE.md for the classification rule).

---

## Directory Structure

```
core-component-00/telescope/
├── README.md               ← Archive index
├── template/                ← Report template (use this for every new report)
│   ├── research-report.md
│   └── qa-document.md
└── <YYYY-MM-DD-slug>/       ← Individual research reports
```

New investigations use the Simple shape (a single `research-report.md`) unless the investigation
genuinely produces multiple ancillary documents, in which case use the Programme shape
(`research-report.md` + one `supporting/` folder). See workspace-root `telescope/CLAUDE.md` §
Telescope Conventions for the full Simple/Programme shape rule and the four-state Status
Lifecycle — both apply here.

---

## Creating a New Research Report

1. Create a new folder: `YYYY-MM-DD-<slug>/`
2. Copy the template: `template/research-report.md` → `YYYY-MM-DD-<slug>/research-report.md`
3. Complete the report in the new folder — use the Simple shape unless the investigation
   genuinely produces multiple ancillary documents, in which case use the Programme shape
   (`research-report.md` + one `supporting/` folder)
4. Add an entry to `README.md` (the archive index), including its Status

Naming, template usage, append-only policy, versioning, and archival status follow the same
conventions as every other telescope instance — see workspace-root `telescope/CLAUDE.md` for the
full shared ruleset. This file only documents what differs for CC-00's instance (scope and
ownership).

---

## Who Can Write Here

- CC-00 research programmes are the primary contributors
- Other departments may still file here if an investigation is genuinely engineering/LLM-research
  in nature and requested through the Lab
- All reports must follow the template format and be indexed in `README.md`

---

## Ownership

- **Owner:** Dr. Elias Vance, CC-00 Laboratory Director
- **Profile:** `core-component-00/director/agent/profile.md`
- **Authority:** AGENTS.md § 6. Core Component 00
