# AGENT-GLOBAL-BASE

A **Markdown-first, agent-native knowledge base** — an organizational simulation and LLM
engineering laboratory running under one governance framework. There is no root build system, no
entry point, and no startup script. The primary artifacts are documents: agent profiles, skill
specifications, pipeline definitions, and Python reference implementations.

---

## The Four Co-Resident Systems

| System          | Path                       | What it is                                                                                                              |
| --------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **The Company** | `company/`                 | Mobile product company — departments, pipelines, crew                                                                   |
| **The Studio**  | `studio/`                  | Casual Games Studio — 39 crew, 11-stage game pipeline                                                                   |
| **CC-00 Lab**   | `core-component-00/`       | Applied LLM research lab — five-module engineering stack                                                                |
| **ANU-00**      | `academic-neural-unit-00/` | Independent academic research entity (CS, AI, neural networks, software engineering); incubated, not governed, by CC-00 |

These systems are architecturally independent but share governance through the
**Agent Systems Engineering (ASE)** framework.

---

## Repository Map

```text
AGENT-GLOBAL-BASE/
├── AGENTS.md                    ← Full orientation guide for AI agents (read this first)
├── CLAUDE.md                    ← Claude Code operating rules (global)
│
├── company/                     ← The Company
│   ├── library/                 ← Central knowledge hub — start here for company context
│   ├── departments/             ← Agent profiles + skill files (canonical source)
│   ├── pipeline/                ← Mobile / Web / Backend API / Full-Stack / Recruitment
│   ├── recruitment/             ← Hiring cycles and templates
│   ├── optimization-history/    ← Append-only archive of optimization plans
│   └── project/                 ← Active project dashboard
│
├── studio/
│   └── casual-games/            ← Only active studio
│       ├── library/             ← Studio overview, charter, strategic brief
│       ├── pipeline/            ← 11-stage game development pipeline
│       ├── team/crew/           ← 38 FTE + 1 Contract across 7 divisions
│       └── projects/            ← Per-game folders (none scaffolded yet)
│
├── core-component-00/           ← CC-00 Lab (only place with runnable code)
│   ├── agent-systems-engineering/  ← ASE governing framework
│   ├── engineering/                ← Layers 1, 2, 3, 5
│   │   ├── prompt-engineering/         ← Layer 1 — what to write
│   │   ├── context-engineering/        ← Layer 2 — how to structure it
│   │   ├── harness-engineering/        ← Layer 3 — how to execute safely
│   │   └── multi-agent-engineering/    ← Layer 5 — how agents cooperate
│   ├── retrieval-augmented-generation/  ← Layer 4 — where to get content
│   ├── mcp-servers/                ← MCP server implementations (deployment surface)
│   └── crew/                       ← Lab Director + 11 crew (director/elias-vance/, module leads, etc.)
│
├── academic-neural-unit-00/     ← ANU-00 — independent academic research entity
│   ├── CLAUDE.md                   ← Entity operating-layer file
│   ├── formation/                  ← Formation record: charter, CEO decisions, final review
│   └── crew/                       ← Lead + 9 crew (10 FTEs total)
│
├── templates/                   ← Cross-system document templates (meeting-records/, review-records/)
│
└── telescope/                   ← Cross-department research index (company/, core-component-00/,
                                     and studio/casual-games/ each keep their own instance too —
                                     see telescope/README.md)
```

---

## The Company

**Start here:** `company/library/README.md`

### Departments & C-Suite

| Department             | C-Suite Owner                                | Core Focus                          |
| ---------------------- | -------------------------------------------- | ----------------------------------- |
| Brand Design           | CDO — Yuki Tanaka-Chen                       | Mobile UI/UX, prototyping, IDS      |
| Cyberspace Security    | CIO — Dr. Priya Mehta / CSO — Dr. Sarah Chen | Security architecture, risk         |
| Human Resources        | CHRO — Dr. Evelyn Hartwell                   | Recruitment, onboarding             |
| Legal                  | CLO — Dr. Victoria Svensson-Park             | Governance, contracts, privacy      |
| Localization           | CTO-L — Dr. Amara Osei-Mensah                | i18n pipeline, TMS, translation     |
| Product Management     | CPO — Marcus Tran-Yoshida                    | PRD authorship, product strategy    |
| Research & Development | CTO — Dr. Kenji Nakamura                     | Android, iOS, KMP, Flutter, testing |

### 13-Stage Development Pipeline

| #   | Stage                              | Key Owner         | Gate |
| --- | ---------------------------------- | ----------------- | ---- |
| 0   | Problem Validation                 | CPO               | —    |
| 1   | Requirements → PRD + SRD           | CPO, CSO          | ✅   |
| 2   | PRD → Prototype + IDS              | CDO               | ✅   |
| 3   | Prototype → UML Engineering Pkg    | CTO, CIO          | ✅   |
| 4   | UML → Implementation Plan + Gantt  | CTO               | ✅   |
| 5   | Plan → Software Development        | CTO               | —    |
| 6   | Development → Arch. Review         | CTO + full panel  | ✅   |
| 7   | Arch. Review → Automated Testing   | CTO + Test Lead   | ✅   |
| 8   | Testing → Integrity Verification   | CTO + all C-suite | —    |
| 9   | Integrity → Translation Production | CTO-L + R&D       | —    |
| 9.5 | Internal Dogfood                   | VP Quality        | —    |
| 10  | Translation → Release Readiness    | CTO + User        | ✅   |
| 11  | Live Operations (continuous)       | VP Platform       | QBR  |

Four pipeline variants exist — Mobile, Web, Backend API, Full-Stack — all built on a shared
`_base/` skeleton with variant-specific deltas. Recruitment is a separate standalone 9-stage
pipeline.

---

## The Casual Games Studio

**Start here:** `studio/casual-games/library/overview/casual-games-studio.md`

- **Engine:** Unity 6.3 LTS
- **Crew:** 39 people across 7 divisions (Leadership · Production · Creative-Design · Art · Audio ·
  Engineering · Live-Ops)
- **Pipeline:** 11 stages (Stage 0–10) — distinct from the company's 13-stage pipeline
- **Projects:** No games scaffolded yet; project folders live under `studio/casual-games/projects/`

**Studio Director:** Dr. Marcus Vogel · **Creative Director:** Sakura Ishimori

---

## Core Component 00 — LLM Engineering Lab

**Start here:** `core-component-00/README.md`

CC-00 is the organisation's centralised LLM engineering laboratory. Every team building with
large language models starts here. **Lab Director:** Dr. Elias Vance.

### The Five-Module Stack

| Layer | Module                                 | Has Runnable Code |
| ----- | -------------------------------------- | :---------------: |
| 1     | `engineering/prompt-engineering/`      |        No         |
| 2     | `engineering/context-engineering/`     |        Yes        |
| 3     | `engineering/harness-engineering/`     |        Yes        |
| 4     | `retrieval-augmented-generation/`      |        Yes        |
| 5     | `engineering/multi-agent-engineering/` |        Yes        |

Key production implementations live under each module's `implementations/` folder. The governing
framework — ASE — is defined in `core-component-00/agent-systems-engineering/`.

---

## Academic Neural Unit 00 (ANU-00)

**Start here:** `academic-neural-unit-00/CLAUDE.md`

ANU-00 is an independent academic research entity chartered to investigate computer science, AI,
neural networks, and software engineering, and to build a knowledge base from that research. It is
**incubated, not governed, by CC-00** — no reporting line into CC-00 or Dr. Vance. **ANU-00 Lead:**
Dr. Naledi Mokoena, 10 FTEs total. Full formation record, CEO decisions, and charter:
`academic-neural-unit-00/formation/2026-07-23-formation-meeting/formation-report.md`.

---

## Key Conventions

| Item                 | Convention                                                          |
| -------------------- | ------------------------------------------------------------------- |
| Folder names         | `kebab-case` — always                                               |
| Agent profile        | `agent/profile.md` — six required YAML frontmatter fields           |
| Skill files          | `skills/<skill-name>.md` — adjacent to the agent folder             |
| Pipeline document    | `pipeline.md` — inside the pipeline folder; the canonical source    |
| Optimization records | `company/optimization-history/YYYY-MM-DD-<slug>/` — **append-only** |
| Markdown formatting  | Run `prettier --write "<file>"` on every created or modified file   |

**Document authority when sources conflict:**
`pipeline.md` → `agent/profile.md` → `library/overview/*.md` → `library/departments/*.md`

---

## Working with Organizational Agents

Agent personas (CDO, CTO, Studio Director, Lab Director, etc.) are **documents**, not running
processes. To get output from a named agent:

1. Read their `agent/profile.md` — establishes identity and authority scope.
2. Read all referenced `skills/*.md` — these are executable contracts, not suggestions.
3. Adopt their voice and produce output strictly within their documented authority.

Profile locations:

- Company C-suite → `company/departments/<dept>/supervisor/<role>/agent/profile.md`
- Studio crew → `studio/casual-games/team/crew/<division>/<role>/<name>/agent/profile.md`
- Lab Director → `core-component-00/crew/director/elias-vance/agent/profile.md`
- ANU-00 Lead → `academic-neural-unit-00/crew/lead/naledi-mokoena/agent/profile.md`

---

## Quick Navigation

| I need…                                             | Go to                                                         |
| --------------------------------------------------- | ------------------------------------------------------------- |
| Full workspace orientation (agents)                 | `AGENTS.md`                                                   |
| Company overview / people / pipeline                | `company/library/README.md`                                   |
| A specific department's agents                      | `company/departments/`                                        |
| Studio structure + game pipeline                    | `studio/casual-games/library/overview/casual-games-studio.md` |
| LLM engineering patterns                            | `core-component-00/README.md`                                 |
| ASE governance (ADRs, compliance)                   | `core-component-00/agent-systems-engineering/`                |
| Production Python code                              | `core-component-00/engineering/<module>/implementations/`     |
| MCP server implementations                          | `core-component-00/mcp-servers/`                              |
| Research archive (cross-department index)           | `telescope/README.md`                                         |
| CC-00 engineering + LLM research                    | `core-component-00/telescope/README.md`                       |
| Company product research                            | `company/telescope/README.md`                                 |
| Studio game/market research                         | `studio/casual-games/telescope/README.md`                     |
| ANU-00 charter, crew, and boundary vs. CC-00        | `academic-neural-unit-00/CLAUDE.md`                           |
| A reusable meeting-minutes or final-review template | `templates/README.md`                                         |
