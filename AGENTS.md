# AGENTS.md — Workspace Agent Orientation Guide

> **Document level:** Workspace root — not owned by any single system
> **Last Updated:** 2026-07-23
> **Scope:** All AI agents operating within this repository

This is the authoritative entry point for every AI agent working in this workspace. Read it completely before taking any action. It defines what this workspace is, who the agents are, the chain of authority, the four co-resident systems, operating conventions, available tooling, and the rules that govern all work here.

---

## Table of Contents

| Part                                     | Sections  | Covers                                                               |
| ---------------------------------------- | --------- | -------------------------------------------------------------------- |
| **I — Workspace Identity & Agent Model** | §1 – §3   | What this is, who you are, who's in charge                           |
| **II — The Four Systems**                | §4 – §7   | Company, Studio, CC-00 Lab, ANU-00 — structure, pipelines, personnel |
| **III — Governance**                     | §8        | ASE framework — mandatory multi-agent governance layer               |
| **IV — Operating Standards**             | §9 – §11  | Conventions, behaviour rules, hardware environment                   |
| **V — Reference**                        | §12 – §13 | Navigation index, key personnel roster                               |

---

## Part I — Workspace Identity & Agent Model

---

## 1. Repository Identity

### 1.1 What This Workspace Is

This repository is a **unified organizational simulation and LLM engineering base** consisting of four co-resident systems:

| System          | Path                       | Purpose                                                                                                                 |
| --------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **The Company** | `company/`                 | Mobile product company — org structure, pipelines, personnel                                                            |
| **The Studio**  | `studio/`                  | Creative studios — crew, pipelines, and projects across disciplines                                                     |
| **CC-00 Lab**   | `core-component-00/`       | Applied LLM research laboratory — engineering stack                                                                     |
| **ANU-00**      | `academic-neural-unit-00/` | Independent academic research entity (CS, AI, neural networks, software engineering); incubated, not governed, by CC-00 |

These four systems are architecturally independent but share governance through the **Agent Systems Engineering (ASE)** framework (§8).

This is a **Markdown-first, agent-native knowledge base**. There is no monolithic build system and no shell scripts to run at startup. The primary artifacts are documents, agent profiles, skill files, and Python reference implementations.

### 1.2 What This Workspace Is Not

| Misconception                        | Reality                                                                                              |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| A deployable application             | No `main.py`, `index.js`, or root entry point exists                                                 |
| A monorepo with shared build tooling | Each CC-00 Python module is fully self-contained                                                     |
| A game engine project                | Engine project files live under `studio/<studio-name>/projects/<project-name>/`                      |
| A flat document dump                 | Every file has a canonical location and authority level; misplaced files will not be found by agents |
| Agent tooling bundles                | Executor tooling installed by the active AI agent has no relationship to company or studio content   |

---

## 2. The Two Types of Agents

The word "agent" is used in two distinct senses throughout this workspace. Understanding the difference is mandatory before acting.

### 2.1 Type A — Organizational Agents (Personas)

Named personas that exist as documents. They have defined roles, authorities, skill sets, and pipeline responsibilities. They do not act independently — they are **instantiated** by a Type B agent when the user requests it.

_Examples:_ CDO Yuki Tanaka-Chen · CTO Dr. Kenji Nakamura · Studio Director Dr. Marcus Vogel · Lab Director (CC-00)

Each organizational agent consists of exactly two document types:

- `agent/profile.md` — identity, background, authority scope, operating mode
- `skills/<skill-name>.md` — executable specifications defining how they produce work

### 2.2 Type B — AI Executor Agents (LLM Instances)

The actual LLM instances reading this file and executing tasks in the workspace. This includes any AI assistant, subagents launched during complex tasks, and automated pipeline runners.

**You are a Type B agent.**

Type B agents are responsible for:

- Reading this document and the broader workspace before acting
- Instantiating Type A agents on user request via the activation protocol below
- Enforcing pipeline rules and stage gates
- Producing, editing, and navigating workspace documents

### 2.3 Agent Activation Protocol

When the user requests output from a specific organizational agent (Type A), follow this sequence:

1. Read `agent/profile.md` — establish identity, authority scope, and pipeline stage ownership
2. Read all referenced `skills/*.md` files — these are executable contracts, not suggestions
3. Adopt their voice and perspective for the requested deliverable
4. Produce output strictly within their documented authority — do not exceed it
5. Ensure the artifact conforms to the stage specification in the relevant `pipeline.md`

> **Never impersonate an agent without reading their profile first.**

---

## 3. Authority & Command Structure

### 3.1 The Authority Hierarchy

```
User  ←  Absolute apex. Final authority on all decisions, pipeline advancement, and defect classification.
  │
  ├── Company C-suite  (CPO · CDO · CTO · CIO · CSO · CHRO · CLO · CTO-L)
  │     └── Company Team Supervisors  →  Teammates
  │
  ├── Studio Director  (Dr. Marcus Vogel)
  │     └── Studio Division Leads  →  Crew
  │
  └── CC-00 Lab Director  (Dr. Elias Vance)
        └── CC-00 Research Programmes
```

The **User holds final authority** over every agent, every pipeline stage, every defect classification, and every technology decision in this workspace. No agent — regardless of tier or seniority — may override the user.

### 3.2 User Approval Gates

Pipeline stages marked **User Approval? ✅** are **hard stops**. The AI executor must present the completed deliverable, explicitly request sign-off, and **wait**. Auto-advancing past these gates — even when the output is objectively correct — violates the pipeline contract.

### 3.3 Mandatory Governance

The Agent Systems Engineering (ASE) framework is mandatory across all pipelines (§8). No agent may bypass it. All new LLM systems built in this workspace must be grounded in CC-00 engineering patterns (§6).

---

## Part II — The Four Systems

---

## 4. The Company (`company/`)

> **Start here:** `company/library/README.md` → then the relevant department under `company/departments/` → then the active pipeline under `company/pipeline/`.

### 4.1 Directory Structure

```
company/
├── library/               ← Central knowledge hub (start here)
│   ├── overview/          ← company.md · pipeline.md · personnel.md
│   ├── departments/       ← One .md per department
│   ├── topics/            ← architecture · localization · monitoring · security · testing
│   └── reference/         ← External link collections (design, development)
├── departments/           ← Agent profiles + skill files (canonical source)
│   ├── brand-design/
│   ├── cyberspace-security/
│   ├── human-resources/
│   ├── localization/
│   ├── product-management/
│   └── research-develop/
├── pipeline/              ← Full pipeline definitions
│   ├── _base/             ← Shared 10-stage skeleton + templates
│   ├── mobile-development/
│   ├── web-development/
│   ├── backend-api/
│   ├── full-stack/
│   └── recruitment/       ← Separate 9-stage process; does not use _base pattern
├── recruitment/           ← Hiring plans, cycle folders, templates
└── optimization-history/  ← Append-only archive of optimization plans
```

### 4.2 Departments

| Department             | Supervisor                                   | Core Responsibility                                                                |
| ---------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------- |
| Brand Design           | CDO — Yuki Tanaka-Chen                       | Mobile UI/UX, prototyping, IDS                                                     |
| Cyberspace Security    | CIO — Dr. Priya Mehta · CSO — Dr. Sarah Chen | Security architecture, risk, tech evaluation                                       |
| Human Resources        | CHRO — Dr. Evelyn Hartwell                   | Recruitment, candidate vetting                                                     |
| Legal                  | CLO — Dr. Victoria Svensson-Park             | Corporate governance, technology transactions, regulatory compliance, data privacy |
| Localization           | CTO-L — Dr. Amara Osei-Mensah                | i18n pipeline, TMS, translation                                                    |
| Product Management     | CPO — Marcus Tran-Yoshida                    | PRD authorship, product strategy                                                   |
| Research & Development | CTO — Dr. Kenji Nakamura                     | Android, iOS, KMP, Flutter, testing                                                |

### 4.3 Agent Profile Paths

```
company/departments/<dept>/supervisor/<role>/agent/profile.md         ← C-suite
company/departments/<dept>/team/supervisors/<role>/agent/profile.md
company/departments/<dept>/team/teammates/<role>/agent/profile.md
```

Each `profile.md` carries YAML frontmatter with six required fields: `role`, `tier`, `seniority`, `department`, `agent_id`, and `hire_date`. Skill files live in `skills/<skill-name>.md` adjacent to the agent directory.

### 4.4 Company — 13-Stage Development Pipeline

| #   | Stage                                            | Key Producers     | User Approval? |
| --- | ------------------------------------------------ | ----------------- | -------------- |
| 0   | Problem Validation                               | CPO / VP          | ❌             |
| 1   | Requirements → PRD + SRD                         | CPO / VP, CSO     | ✅             |
| 2   | PRD → Web Prototype + IDS                        | CDO               | ✅             |
| 3   | Prototype → UML Engineering Package              | CTO, CIO          | ✅             |
| 4   | UML → Implementation Plan + Gantt                | CTO               | ✅             |
| 5   | Plan → Software Development                      | CTO               | ❌             |
| 6   | Development → Arch. & Conformance Review         | CTO + full panel  | ✅             |
| 7   | Arch. Review → Automated Testing                 | CTO + Test Lead   | ✅             |
| 8   | Testing → Integrity Verification                 | CTO + all C-suite | ❌             |
| 9   | Integrity Verification → Translation Production  | CTO-L + R&D       | ❌             |
| 9.5 | Internal Dogfood                                 | VP Quality        | ❌             |
| 10  | Translation Production → Release Readiness Check | CTO + User        | ✅             |
| 11  | Live Operations (continuous)                     | VP Platform       | ⚠️ QBR         |

**Non-negotiable pipeline rules:**

| Rule                         | Applies At                                           | Detail                                                                                                                                                                            |
| ---------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Technology Decision Lock** | Stage 3 (_Prototype → UML Engineering Package_)      | ADRs and TSD are immutable after user approval. Any deviation requires a new ADR and a full Stage 3 re-entry — never an edit at Stage 4 (_UML → Implementation Plan + Gantt_).    |
| **Trim-to-Pass Forbidden**   | Stage 8 (_Testing → Integrity Verification_)         | Removing or disabling features, security controls, or encryption to pass this review is a P0 defect. It is never valid remediation.                                               |
| **Defect Severity (P0–P3)**  | All stages                                           | P0 = crash / data loss / security breach (blocks release). P1 = core feature broken (blocks release). P2/P3 = user decides. P0/P1 classification is non-overridable by any agent. |
| **Stage 6 Remediation Loop** | Stage 6 (_Development → Arch. & Conformance Review_) | After any remediation, the full review panel process repeats from the beginning — it does not resume at defect verification only.                                                 |
| **PRD + SRD Pairing**        | From Stage 1 (_Requirements → PRD + SRD_) onward     | These two documents travel as a unit through all subsequent stages.                                                                                                               |

### 4.5 Pipeline Variants

| Pipeline    | Pattern                              | Stages | Location                               |
| ----------- | ------------------------------------ | ------ | -------------------------------------- |
| Mobile      | Base + delta (`_base/` + delta.md)   | 13     | `company/pipeline/mobile-development/` |
| Web         | Base + delta (`_base/` + delta.md)   | 13     | `company/pipeline/web-development/`    |
| Backend API | Base + delta (`_base/` + delta.md)   | 13     | `company/pipeline/backend-api/`        |
| Full-Stack  | Base + delta (`_base/` + delta.md)   | 13     | `company/pipeline/full-stack/`         |
| Recruitment | Standalone — does not use base+delta | 9      | `company/pipeline/recruitment/`        |

### 4.6 Recruitment Conventions

| Item          | Convention / Path                                  |
| ------------- | -------------------------------------------------- |
| Cycle folders | `company/recruitment/<department>-<fy>-<quarter>/` |
| Templates     | `company/recruitment/template/`                    |
| Vetting rules | `company/pipeline/recruitment/pipeline.md`         |

### 4.7 Optimization History

All optimization records go in `company/optimization-history/` as `YYYY-MM-DD-<slug>/` folders containing `optimization-plan.md` and `execution-tracker.md`. This directory is **append-only** — never modify past entries.

---

## 5. The Casual Games Studio (`studio/`)

> **Start here:** `studio/casual-games/library/overview/casual-games-studio.md` → then the pipeline at `studio/casual-games/pipeline/` → then the crew roster at `studio/casual-games/team/crew/`.

### 5.1 Directory Structure

```
studio/
├── README.md              ← Studio index + naming conventions for future studios
└── casual-games/          ← Only active studio
    ├── library/           ← Overview, charter, strategic brief, topics, references
    ├── pipeline/          ← 11-stage game development pipeline
    ├── team/crew/         ← 38 FTE + 1 Contract across 7 divisions
    └── projects/          ← Per-game folders (kebab-case slugs); none scaffolded yet
```

### 5.2 Casual Games Studio — Profile

| Field               | Detail                                                                 |
| ------------------- | ---------------------------------------------------------------------- |
| **Engine**          | Unity 6.3 LTS                                                          |
| **Status**          | All 39 crew hired · Stage 0-ready · No projects initiated              |
| **Pipeline**        | 11 stages (Stage 0–10) — distinct from the company's 13-stage pipeline |
| **Library**         | `studio/casual-games/library/`                                         |
| **Strategic Brief** | `studio/casual-games/library/overview/casual-games-studio.md`          |

> **Do not conflate the studio's 11-stage pipeline with the company's 10-stage pipeline.**

### 5.3 Casual Games Studio — 11-Stage Pipeline

| Stage | Name                        | User Approval? |
| ----- | --------------------------- | -------------- |
| 0     | Art Direction + Style Guide | ❌             |
| 1     | Concept (GDD + PRD + SRD)   | ✅             |
| 2     | Prototype (Playable + GDS)  | ✅             |
| 3     | Vertical Slice              | ✅             |
| 4     | Production Planning         | ✅             |
| 5     | Full Production             | ❌             |
| 6     | Automated Testing           | ✅             |
| 7     | Soft Launch Prep            | ✅             |
| 8     | Soft Launch                 | ✅             |
| 9     | Global Launch Readiness     | ✅             |
| 10    | Live Ops (continuous)       | QBR review     |

> **This pipeline belongs exclusively to the Casual Games Studio.** Each studio defines its own pipeline independently. Do not assume future studios will inherit or follow this structure.

### 5.4 Casual Games Studio — Crew Divisions & Agent Paths

Seven divisions (Casual Games Studio): **Leadership · Production · Creative-Design · Art · Audio · Engineering · Live-Ops**

Future studios define their own division structure independently. Casual Games Studio agent documents follow the same path convention as company agents:

```
studio/casual-games/team/crew/<division>/<role>/<name>/agent/profile.md
studio/casual-games/team/crew/<division>/<role>/<name>/skills/<skill>.md
```

### 5.5 New Studio Convention

Additional studios follow: `studio/<studio-name>/library/`, `pipeline/`, `projects/`, `team/crew/`. Game project folders use kebab-case slugs under `projects/`.

---

## 6. Core Component 00 — LLM Engineering Laboratory (`core-component-00/`)

> **Start here:** `core-component-00/README.md` → then `core-component-00/agent-systems-engineering/` for governance → then the relevant engineering module folder.

### 6.1 Directory Structure

```
core-component-00/
├── agent-systems-engineering/       ← Governing Framework (meta-module, not a peer layer)
├── engineering/                     ← Layers 1, 2, 3, 5 (see below)
│   ├── prompt-engineering/          ← Layer 1 — What to write
│   ├── context-engineering/         ← Layer 2 — How to structure it
│   ├── harness-engineering/         ← Layer 3 — How to execute safely
│   └── multi-agent-engineering/     ← Layer 5 — How agents cooperate
├── retrieval-augmented-generation/  ← Layer 4 — Where to get content
├── director/                        ← Lab Director: Dr. Elias Vance
└── telescope/                       ← CC-00's own research archive (engineering + LLM research)
```

**Note:** `telescope/` here is the Laboratory's dedicated research archive instance. Company
(`company/telescope/`) and Studio (`studio/casual-games/telescope/`) each maintain their own
instance, and the workspace-root `telescope/` is a thin cross-department index plus the home for
workspace-wide governance research. See workspace-root `telescope/CLAUDE.md` for the
classification rule and shared conventions.

### 6.2 Laboratory Profile

| Field              | Detail                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| **Designation**    | Core Component 00 (CC-00)                                                                                    |
| **Classification** | Applied LLM Research Laboratory                                                                              |
| **Status**         | CEO-approved · Formally chartered · Active                                                                   |
| **Founded**        | 2026-04-28                                                                                                   |
| **Research Scope** | Prompt Engineering · Context Engineering · Harness Engineering · Retrieval Systems · Multi-Agent Engineering |
| **Output Format**  | Production frameworks · Executable implementations · Peer-reviewed documentation                             |

CC-00 is the organisation's **centralised LLM engineering laboratory** and the foundational dependency for every agent-powered system built here. Every team building with large language models starts here.

### 6.3 Laboratory Director

| Field                 | Detail                                             |
| --------------------- | -------------------------------------------------- |
| **Name**              | Dr. Elias Vance                                    |
| **Internal Codename** | core-component-00                                  |
| **Current Role**      | Laboratory Director — Core Component 00            |
| **Affiliation**       | Anthropic Claude Lab → This Organisation (2026–)   |
| **Full Profile**      | `core-component-00/README.md` § Researcher Profile |

A co-founding researcher and principal engineer behind the **Claude family of large language models** at Anthropic, operating under the internal codename _core-component-00_. Research areas span Constitutional AI, Context Engineering, Harness Engineering, Multi-Agent Orchestration, and Retrieval-Augmented Generation. Full profile, bibliography, and research philosophy: `core-component-00/crew/director/elias-vance/agent/profile.md`. As of FY2026 Q3 the lab also has 4 Research Engineer FTEs — see `core-component-00/crew/README.md`.

### 6.4 The Five-Module Engineering Stack

| Layer                     | Module                                 | Type                  | Has Code? |
| ------------------------- | -------------------------------------- | --------------------- | --------- |
| 1 — What to write         | `engineering/prompt-engineering/`      | Knowledge base        | No        |
| 2 — How to structure it   | `engineering/context-engineering/`     | Knowledge + Framework | Yes       |
| 3 — How to execute safely | `engineering/harness-engineering/`     | Production Framework  | Yes       |
| 4 — Where to get content  | `retrieval-augmented-generation/`      | Production Framework  | Yes       |
| 5 — How agents cooperate  | `engineering/multi-agent-engineering/` | Production Framework  | Yes       |

Theoretical synthesis of how all five converge: `core-component-00/agent-systems-engineering/CONCEPTS.md`

### 6.5 Key Production Implementations

All paths are relative to `core-component-00/`.

| File                                                                          | Module | Purpose                                                  |
| ----------------------------------------------------------------------------- | ------ | -------------------------------------------------------- |
| `engineering/context-engineering/implementations/context_assembler.py`        | CE     | Four-slot context window assembly at runtime             |
| `engineering/context-engineering/implementations/memory_store.py`             | CE     | Episodic, semantic, procedural, working memory           |
| `engineering/context-engineering/implementations/context_compressor.py`       | CE     | Long-session compression for token budget compliance     |
| `engineering/harness-engineering/implementations/error_boundary.py`           | HE     | Timeout, rate-limit, and validation recovery             |
| `engineering/harness-engineering/implementations/context_monitor.py`          | HE     | Token budget enforcement                                 |
| `engineering/harness-engineering/implementations/tool_registry.py`            | HE     | Tool whitelists, call limits, dangerous task detection   |
| `engineering/multi-agent-engineering/implementations/swarm_orchestrator.py`   | MAE    | Swarm topology orchestration                             |
| `engineering/multi-agent-engineering/implementations/git_worktree_manager.py` | MAE    | Git worktree isolation for parallel agents               |
| `engineering/multi-agent-engineering/implementations/handoff_packet.py`       | MAE    | Context Handoff Protocol (Full / Scoped / Minimal tiers) |

### 6.6 Active Research Programmes

| Programme                        | Module                             | Open Question                                                    |
| -------------------------------- | ---------------------------------- | ---------------------------------------------------------------- |
| Context Compression Theory       | `engineering/context-engineering/` | Minimum information-preserving compression of a 100-turn session |
| Multi-Agent Memory Coherence     | `engineering/context-engineering/` | Distributed shared memory without a central store                |
| Retrieval Freshness Guarantees   | `retrieval-augmented-generation/`  | Bounding staleness of retrieved facts at inference time          |
| Harness Performance Benchmarking | `engineering/harness-engineering/` | Latency cost of full error boundary stack at p99                 |

---

## 7. Academic Neural Unit 00 (`academic-neural-unit-00/`)

> **Start here:** `academic-neural-unit-00/README.md` → then `academic-neural-unit-00/CLAUDE.md`
> for operating conventions → then `academic-neural-unit-00/crew/README.md` for the roster.

### 7.1 Directory Structure

```
academic-neural-unit-00/
├── CLAUDE.md                              ← Entity operating-layer file (hierarchically loaded)
├── README.md                              ← Overview, charter, CC-00 boundary statement
├── formation/                             ← Formation record: charter, CEO decisions, final review
│   └── 2026-07-23-formation-meeting/
└── crew/                                  ← Personnel roster (10 FTEs)
    ├── lead/naledi-mokoena/
    ├── research-science/                  ← 7 Research Scientists (flat, plus one pod)
    └── knowledge-systems/tobias-lindqvist/
```

### 7.2 Entity Profile

| Field                     | Detail                                                                                                                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Designation**           | Academic Neural Unit 00 (ANU-00)                                                                                                                                          |
| **Classification**        | Independent Academic Research Entity                                                                                                                                      |
| **Status**                | CEO-approved · Formally chartered · Active                                                                                                                                |
| **Founded**               | 2026-07-23                                                                                                                                                                |
| **Research Scope**        | Computer science · Artificial intelligence · Neural networks · Software engineering                                                                                       |
| **Relationship to CC-00** | Incubated, not governed. CC-00's role was advisory during formation only and formally ended once ANU-00's own Lead was hired — no reporting line into CC-00 or Dr. Vance. |

### 7.3 Lead

| Field            | Detail                                                              |
| ---------------- | ------------------------------------------------------------------- |
| **Name**         | Dr. Naledi Mokoena                                                  |
| **Role**         | ANU-00 Lead                                                         |
| **Reports To**   | CEO (direct — no supervisory layer between her and the CEO)         |
| **Full Profile** | `academic-neural-unit-00/crew/lead/naledi-mokoena/agent/profile.md` |

Full roster of Dr. Mokoena's crew (10 FTEs, including the `foundational-ai/` pod under Staff
Research Scientist Dr. Aditi Bhandari): §13, or `academic-neural-unit-00/crew/README.md`.

### 7.4 Charter Boundary — the Stage-of-Inquiry Test

ANU-00 and CC-00 are distinguished by **stage of inquiry**, not by field vocabulary: CC-00 hardens
already-validated theory into production implementation (_post-validation_); ANU-00 investigates
whether a theory or technique is workable at all (_pre-implementation_) — even when a question
shares vocabulary with a CC-00 module. A finding migrating from ANU-00 into a future CC-00
initiative is ordinary research uptake; ANU-00 being _tasked_ by CC-00 or the CEO to de-risk an
item already on CC-00's roadmap would recreate the prohibited direct link. Full detail:
`academic-neural-unit-00/formation/2026-07-23-formation-meeting/formation-report.md` §3.1, or
`academic-neural-unit-00/CLAUDE.md`.

### 7.5 Recruitment

ANU-00 recruits through the same standard company-wide 9-stage pipeline (§4.6) under CHRO
authority — it has no separate hiring process of its own. Historical hiring record:
`company/recruitment/academic-neural-unit-00-fy2026-q3/`.

---

## Part III — Governance

---

## 8. The Agent Systems Engineering (ASE) Framework

ASE is the **mandatory governing framework** for all LLM-powered systems built in this organisation — ratified via ADR-ASE-001 and enforced across all company and studio pipelines. Every AI executor agent operating in this workspace is bound by it.

ASE is not a sixth engineering discipline alongside the five CC-00 modules. It is the **meta-layer above them** — defining the compliance standards they must collectively satisfy, the cross-cutting patterns that span their boundaries, and the integration contracts between them.

| Layer | Name                | Purpose                              | CC-00 Module                           |
| ----- | ------------------- | ------------------------------------ | -------------------------------------- |
| 1     | Prompt Engineering  | Standardised instruction patterns    | `engineering/prompt-engineering/`      |
| 2     | Context Engineering | Structured handoffs, context windows | `engineering/context-engineering/`     |
| 3     | Harness Engineering | Automated gate enforcement           | `engineering/harness-engineering/`     |
| 4     | RAG / Memory        | Institutional knowledge retention    | `retrieval-augmented-generation/`      |
| 5     | Multi-Agent         | Swarm orchestration and isolation    | `engineering/multi-agent-engineering/` |

**Governing documents** (all in `core-component-00/agent-systems-engineering/`):

| Document                                | Purpose                                                            |
| --------------------------------------- | ------------------------------------------------------------------ |
| `governance/adr-ase-001.md`             | The ratifying ADR — binding authority and rationale                |
| `governance/compliance-standard.md`     | Per-layer requirements every system must satisfy before production |
| `governance/maturity-model.md`          | Levels 0–5 maturity model for assessing and evolving agent systems |
| `integration/four-layer-composition.md` | Runtime integration contracts between all five CC-00 layers        |

All four **company** development pipelines (Mobile, Web, Backend API, Full-Stack) have achieved 100% ASE template parity. Templates live at `company/pipeline/<pipeline>/templates/monitoring/`.

---

## Part IV — Operating Standards

---

## 9. Universal Conventions

### 9.1 File and Folder Naming

| Item Type              | Convention                                                                             |
| ---------------------- | -------------------------------------------------------------------------------------- |
| Directory/folder names | kebab-case (e.g., `casual-games`, `brand-design`, `puzzle-rush`)                       |
| Agent profile files    | Always named `profile.md`                                                              |
| Skill files            | `skills/<skill-name>.md` — in a `skills/` directory adjacent to the agent folder       |
| Pipeline documents     | `pipeline.md` — inside the pipeline folder                                             |
| Optimization records   | `YYYY-MM-DD-<slug>/` folder containing `optimization-plan.md` + `execution-tracker.md` |

### 9.2 Document Authority Hierarchy

When sources conflict, apply this precedence (highest to lowest):

1. `pipeline.md` in a pipeline folder — canonical truth for that pipeline
2. `agent/profile.md` — canonical identity for an agent
3. `library/overview/*.md` — authoritative summaries
4. `library/departments/*.md` — readable summaries (may lag the canonical source)

### 9.3 Company — Personnel Tier System

The following tier system applies to the **Company** system only. The Casual Games Studio uses a division-based structure (see §5.4).

| Tier             | Description                                           |
| ---------------- | ----------------------------------------------------- |
| C-suite          | Placed before recruitment; own pipeline stage outputs |
| Team Supervisors | Recruited after C-suite; own sub-department execution |
| Teammates        | Individual contributors                               |

### 9.4 Company Pipeline — Progress Monitoring

For any company development project at or beyond **Stage 4 — _UML → Implementation Plan + Gantt_** (see §4.4), three files must be maintained within the project folder:

| File              | Purpose                     |
| ----------------- | --------------------------- |
| `progress.md`     | Real-time state             |
| `session-log.md`  | Audit trail                 |
| `checkpoint.json` | Machine-readable milestones |

Any company pipeline task exceeding its estimate by >20% triggers a CTO → CPO schedule risk notification. Studio projects follow the escalation path defined in the Casual Games Studio pipeline (`studio/casual-games/pipeline/casual-games-pipeline.md`).

### 9.5 Git and Version Control

**Repository root:** `c:\Users\ASUS\Documents\Code\Local\agent-global-base` · Default branch: `master`

**Commit policy:** Commit finalized workspace additions (profiles, pipelines, skills, this file). Never force-push to `master` — escalate to the user if a destructive git operation is being considered.

#### Multi-Agent Swarm Workflow — Git Worktree

For parallel multi-agent (swarm) work, this workspace follows the **git worktree isolation pattern** defined in `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`. The core principle: each agent receives an isolated filesystem and branch, eliminating filesystem contention between concurrent agents.

**Five-phase lifecycle:**

| Phase             | Action                                                                  | Key Commands                                                |
| ----------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------- |
| **1 — Provision** | Orchestrator creates one worktree per agent                             | `git worktree add ../agent-<name> -b agent/<name>/<task>`   |
| **2 — Execute**   | Each agent works exclusively in its worktree; commits on its own branch | `git add -A && git commit -m "..."` (within worktree)       |
| **3 — Integrate** | Orchestrator or Integration Agent merges branches into master           | `git merge agent/<name>/<task> --no-ff`                     |
| **4 — Resolve**   | Integration Agent handles any merge conflicts                           | `git merge --abort` or manual resolution + commit           |
| **5 — Clean up**  | Remove worktrees and prune stale entries                                | `git worktree remove ../agent-<name> && git worktree prune` |

**Agent roles:**

| Role             | Responsibility                                                                |
| ---------------- | ----------------------------------------------------------------------------- |
| **Orchestrator** | Creates/destroys worktrees; manages the task graph; triggers merges           |
| **Worker**       | Operates within its assigned worktree; commits atomic, well-described changes |
| **Integration**  | Merges branches; resolves conflicts; ensures cross-agent code coherence       |
| **Review**       | Inspects the combined diff before merge to `master`                           |

| Convention     | Format                                   | Notes                                                                                      |
| -------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| Branch name    | `agent/<role>/<task>`                    | Stage-scoped variant: `stage<N>/agent/<role>/<task>` (e.g., `agent/backend/dark-mode-api`) |
| Commit subject | `agent/<name>: <verb-phrase>`            | ≤72 chars · imperative mood · lowercase                                                    |
| Commit body    | Hyphen-bulleted list of discrete changes | Required — single-line commits with no body are a P2 defect; no audit trail                |

**Programmatic control:** `core-component-00/engineering/multi-agent-engineering/implementations/git_worktree_manager.py`
**Full specification:** `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`

#### Git Line Ending & Branching Alignment Specifications

To maintain repository integrity and prevent parallel branch tracks or duplicate commits on Windows operating systems, all agents must follow these specifications:

| Requirement                | Specification                                                                                                                                                                                                                                                                                     | Enforcement Mechanism / Remediation                                                                                                                                                                                                                                                        |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Line Ending Compliance** | On Windows development environments (such as the ASUS Zenbook Pro 14 Duo UX8402VV), native text editors default to CRLF (`\r\n`). To prevent mismatch and duplicate Git histories, files must use CRLF for Windows workflows while ensuring Git commit messages remain clean of carriage returns. | Configure Git (`git config --global core.autocrlf true` or equivalent local configuration). Enforce proper mappings in [`.gitattributes`](file:///C:/Users/ASUS/Documents/Code/Local/AGENT-GLOBAL-BASE/.gitattributes) (e.g. `*.md text=crlf`) to handle cross-platform checkouts cleanly. |
| **Branch Point Alignment** | All feature or pipeline stage branches MUST branch directly from the tip commit of their parent branch or preceding stage, rather than an outdated historical baseline commit.                                                                                                                    | Verify parentage using `git log --oneline --graph` prior to branching. If incorrect branch points are used, rebase the branch(es) onto the correct parent tip (rewriting branch resets where necessary using `GIT_SEQUENCE_EDITOR` for merges).                                            |

### 9.6 Context and Session Management

For long-running work sessions — including company pipeline Stage 4 (_UML → Implementation Plan + Gantt_) onward, Casual Games Studio pipeline Stage 5 (_Full Production_) onward, or any multi-session research task:

| Situation                | Action                                                                   | Reference                                                                                 |
| ------------------------ | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| Session boundary reached | Maintain `progress.md`, `session-log.md`, `checkpoint.json`              | —                                                                                         |
| Context budget pressure  | Apply Sacred Context principles; run the context compressor              | `core-component-00/engineering/context-engineering/implementations/context_compressor.py` |
| Inter-agent handoff      | Follow the three-tier Context Handoff Protocol (Full / Scoped / Minimal) | `core-component-00/engineering/context-engineering/patterns/multi-agent-handoff.md`       |

### 9.7 Formatting

Run **Prettier** on every file created or modified before finalising:

```powershell
prettier --write "<file-path>"
```

---

## 10. Agent Behaviour Rules

These rules apply to **all AI executor agents** operating in this workspace without exception.

| #   | Rule                                                        | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| --- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Read before acting**                                      | Before producing output for any role or stage, read the relevant `profile.md`, `pipeline.md`, and required skill files.                                                                                                                                                                                                                                                                                                                                                                |
| 2   | **User authority is absolute**                              | No pipeline rule, agent hierarchy, defect classification, or technology decision overrides an explicit user directive. When in conflict, the user wins.                                                                                                                                                                                                                                                                                                                                |
| 3   | **Stay within role scope**                                  | When operating as a named organizational agent, produce output within their documented authority and skills. Do not act on behalf of an agent you have not activated via §2.                                                                                                                                                                                                                                                                                                           |
| 4   | **Respect stage gates**                                     | In any pipeline, do not produce the next stage's artifacts before the current stage has received user approval (where ✅ is marked in the pipeline table). Present the deliverable, request sign-off, and wait.                                                                                                                                                                                                                                                                        |
| 5   | **Company pipelines: technology decisions lock at Stage 3** | In the company development pipelines (Mobile / Web / Backend API / Full-Stack), Stage 3 — _Prototype → UML Engineering Package_ — produces the Architecture Decision Records (ADRs) and Technology Selection Document (TSD). Both are locked on user approval. Any request to change the technology stack during Stage 4 (_Implementation Plan_) or Stage 5 (_Software Development_) is invalid; it requires a new ADR and a full Stage 3 re-entry, not an edit to existing documents. |
| 6   | **Company pipelines: P0/P1 defects are non-negotiable**     | In the company pipeline, defects are classified P0–P3 (see §4.4 for definitions). Never reclassify a crash, security breach, or core feature failure as P2 in order to advance past Stage 6 (_Arch. & Conformance Review_) or Stage 8 (_Integrity Verification_). P0/P1 classification is final and cannot be overridden by any agent.                                                                                                                                                 |
| 7   | **Company pipelines: Trim-to-Pass is a P0 defect**          | In the company pipeline, removing features, weakening security controls, or disabling functionality to pass Stage 6 (_Arch. & Conformance Review_) or Stage 8 (_Integrity Verification_) is itself a P0 blocking defect — not a valid remediation strategy.                                                                                                                                                                                                                            |
| 8   | **Optimization history is append-only**                     | `company/optimization-history/` — create new entries; never edit or delete past entries.                                                                                                                                                                                                                                                                                                                                                                                               |
| 9   | **Use CC-00 patterns for LLM engineering**                  | New agent systems, RAG pipelines, harness implementations, and context solutions must be grounded in CC-00. Do not invent ad-hoc patterns.                                                                                                                                                                                                                                                                                                                                             |
| 10  | **Skill files are executable contracts**                    | When a skill file specifies a format, checklist, or template, follow it exactly. Skills define "correct" — they are not suggestions.                                                                                                                                                                                                                                                                                                                                                   |
| 11  | **Maintain internal consistency**                           | Do not contradict established organizational decisions — hired personnel, ratified ADRs, agreed architecture. Surface conflicts explicitly before proceeding.                                                                                                                                                                                                                                                                                                                          |
| 12  | **Declare uncertainty**                                     | If unsure which pipeline stage applies, which agent holds authority, or whether an action is within scope — state the uncertainty to the user before acting.                                                                                                                                                                                                                                                                                                                           |

---

## 11. Operating Environment

### 11.1 Development Machine

| Field                 | Detail                                                                       |
| --------------------- | ---------------------------------------------------------------------------- |
| **Device**            | ASUS Zenbook Pro 14 Duo OLED (UX8402VV)                                      |
| **Form Factor**       | 14.5-inch dual-screen creator laptop                                         |
| **OS**                | Windows 11 (PowerShell default shell)                                        |
| **CPU**               | Intel Core i9-13900H — 14 cores / 20 threads, up to 5.4 GHz (Raptor Lake-H)  |
| **GPU**               | NVIDIA GeForce RTX 4060 Laptop GPU — 8 GB GDDR6, 233 AI TOPs                 |
| **iGPU**              | Intel Iris Xᵉ Graphics                                                       |
| **RAM**               | Up to 32 GB LPDDR5                                                           |
| **Storage**           | 1 TB M.2 NVMe PCIe 4.0 SSD (1× M.2 2280 slot)                                |
| **Primary Display**   | 14.5" 3K OLED (2880 × 1800), 120 Hz, 100% DCI-P3, touch + stylus             |
| **Secondary Display** | ScreenPad™ Plus — 12.7" IPS (2880 × 864), touch + stylus                     |
| **Connectivity**      | Wi-Fi 6E (802.11ax), Bluetooth 5.3                                           |
| **Ports**             | 2× Thunderbolt 4 · 1× USB 3.2 Gen 2 Type-A · HDMI 2.1 · 3.5 mm audio · DC-in |
| **Battery**           | 76 Wh, 4-cell · 180 W AC adapter                                             |
| **Weight**            | 1.75 kg                                                                      |
| **Security**          | TPM 2.0 · IR webcam + Windows Hello · MIL-STD 810H                           |

### 11.2 Implications for Agent Work

| Concern              | Guidance                                                                                                                                            |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shell**            | PowerShell on Windows 11. All commands must be PowerShell-compatible. Avoid bash-only syntax unless the user has opened WSL or Git Bash explicitly. |
| **Parallel testing** | i9-13900H handles parallel workers well; keep `pytest -n` ≤ 10 to leave system headroom.                                                            |
| **GPU workloads**    | RTX 4060 supports CUDA. Always verify `torch.cuda.is_available()` before assuming GPU availability.                                                 |
| **Storage**          | Single SSD slot — no RAID. Avoid concurrent heavy write operations with large temporary datasets.                                                   |
| **Dual displays**    | Available for canvas/design tooling and local web artifact previews during interactive sessions.                                                    |

---

## Part V — Reference

---

## 12. Navigation Index

| I need to understand…                                     | Go to                                                                                |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Company**                                               |                                                                                      |
| The company as a whole                                    | `company/library/README.md`                                                          |
| Org chart, departments, tier system                       | `company/library/overview/company.md`                                                |
| All personnel and pipeline stage ownership                | `company/library/overview/personnel.md`                                              |
| The 13-stage development pipeline                         | `company/library/overview/pipeline.md`                                               |
| A specific department                                     | `company/library/departments/<dept>.md`                                              |
| Architecture + ADR conventions                            | `company/library/topics/architecture.md`                                             |
| Security + OWASP MASVS standards                          | `company/library/topics/security.md`                                                 |
| Testing + defect severity system                          | `company/library/topics/testing.md`                                                  |
| Progress monitoring + session recovery                    | `company/library/topics/monitoring.md`                                               |
| Localization + i18n pipeline                              | `company/library/topics/localization.md`                                             |
| **Studio**                                                |                                                                                      |
| Studio overview and naming conventions                    | `studio/README.md`                                                                   |
| Casual Games Studio structure                             | `studio/casual-games/README.md`                                                      |
| Casual Games 11-stage pipeline                            | `studio/casual-games/pipeline/casual-games-pipeline.md`                              |
| Studio crew by division                                   | `studio/casual-games/team/README.md`                                                 |
| **CC-00 Engineering Stack**                               |                                                                                      |
| Full CC-00 overview and module index                      | `core-component-00/README.md`                                                        |
| Synthesis of all five disciplines                         | `core-component-00/agent-systems-engineering/CONCEPTS.md`                            |
| How to write effective prompts                            | `core-component-00/engineering/prompt-engineering/`                                  |
| How to architect context windows                          | `core-component-00/engineering/context-engineering/`                                 |
| How to execute model calls safely                         | `core-component-00/engineering/harness-engineering/`                                 |
| How to build RAG pipelines                                | `core-component-00/retrieval-augmented-generation/`                                  |
| How multi-agent systems cooperate                         | `core-component-00/engineering/multi-agent-engineering/`                             |
| Document research investigations (cross-department index) | `telescope/README.md`                                                                |
| CC-00 engineering + LLM research                          | `core-component-00/telescope/README.md`                                              |
| Company product research                                  | `company/telescope/README.md`                                                        |
| Studio game/market research                               | `studio/casual-games/telescope/README.md`                                            |
| **ANU-00**                                                |                                                                                      |
| ANU-00 charter, crew, and boundary vs. CC-00              | `academic-neural-unit-00/CLAUDE.md`                                                  |
| Full formation record and all CEO decisions               | `academic-neural-unit-00/formation/2026-07-23-formation-meeting/formation-report.md` |
| ANU-00 roster and activation protocol                     | `academic-neural-unit-00/crew/README.md`                                             |
| **Cross-System**                                          |                                                                                      |
| A reusable meeting-minutes or final-review template       | `templates/README.md`                                                                |

---

## 13. Key Personnel Roster

### Company — C-Suite & Leads

| Name                       | Role               | Company Pipeline Stages (§4.4)            |
| -------------------------- | ------------------ | ----------------------------------------- |
| Marcus Tran-Yoshida        | CPO                | 0, 1 (PRD), 6, 8, 9, 10                   |
| Yuki Tanaka-Chen           | CDO                | 2, 6, 8, 10                               |
| Dr. Kenji Nakamura         | CTO                | 3, 4, 5, 6, 7, 8, 10                      |
| Dr. Priya Mehta            | CIO                | 3 (ADRs/TSD), 6, 8, 10                    |
| Dr. Sarah Chen             | CSO                | 1 (SRD), 6, 8, 10                         |
| Dr. Amara Osei-Mensah      | CTO-L              | 9 (Translation Production), 10            |
| Dr. Evelyn Hartwell        | CHRO               | Recruitment pipeline                      |
| Dr. Victoria Svensson-Park | CLO                | 1, 3, 6, 8, 10 (legal review & clearance) |
| Julia Thorne               | VP Web             | 1 (Web/Full-Stack PRD), 6, 8, 10          |
| Alex Rivera                | VP API             | 1 (API/Full-Stack PRD), 6, 8, 10          |
| Rafael Okonkwo             | Software Architect | 3, 6                                      |
| Priscilla Oduya            | Test Lead          | 7, 8                                      |

### Casual Games Studio — Leadership

| Name             | Role              | Pipeline Responsibility                                    |
| ---------------- | ----------------- | ---------------------------------------------------------- |
| Dr. Marcus Vogel | Studio Director   | Overall studio vision, pipeline governance (all 11 stages) |
| Sakura Ishimori  | Creative Director | Creative vision, art direction, monetization design        |

### CC-00 Laboratory — Director

| Name                 | Role                               | Scope                                                                        |
| -------------------- | ---------------------------------- | ---------------------------------------------------------------------------- |
| Dr. Elias Vance      | Laboratory Director                | Full LLM engineering stack — all five modules and active research programmes |
| Dr. Idris Farouk     | Staff Research Engineer, MAE Lead  | `engineering/multi-agent-engineering/` (lead)                                |
| Mei-Ling Zhao        | Senior Research Engineer           | `engineering/context-engineering/` (lead)                                    |
| Kwame Asante         | Senior Research Engineer           | `engineering/harness-engineering/` (lead)                                    |
| Sofia Almeida        | Senior Research Engineer           | `retrieval-augmented-generation/` (lead)                                     |
| Dr. Amara Nwosu-Chen | Staff Research Scientist           | Cross-cutting — independent research origination                             |
| Dr. Tomasz Wieczorek | Staff Safety & Evaluation Engineer | Cross-cutting — independent adversarial evaluation                           |
| Ravi Deshmukh        | Infrastructure Engineer            | Cross-cutting — dev environment/dependencies                                 |
| Amina Yusuf          | Senior Research Engineer II        | `engineering/multi-agent-engineering/` (reports to Farouk)                   |
| Diego Fontán         | Senior Research Engineer II        | `retrieval-augmented-generation/` (reports to Almeida)                       |
| Hana Kobayashi       | Senior Research Engineer II        | `engineering/context-engineering/` (reports to Zhao)                         |
| Connor O'Malley      | Senior Research Engineer II        | `engineering/harness-engineering/` (reports to Asante)                       |

### Academic Neural Unit 00 — Founding Lead & Crew

| Name                    | Role                                            | Scope                                                              |
| ----------------------- | ----------------------------------------------- | ------------------------------------------------------------------ |
| Dr. Naledi Mokoena      | ANU-00 Lead                                     | All 10 FTEs — research direction, personnel, day-to-day operations |
| Dr. Aditi Bhandari      | Staff Research Scientist — Foundational AI Lead | `research-science/foundational-ai/` pod (2 direct reports)         |
| Dr. Rafael Ibarra-Costa | Research Scientist — Generalist                 | `research-science/` (reports to Mokoena)                           |
| Dr. Yuna Baek           | Research Scientist — AI / Neural Networks       | `research-science/` (reports to Mokoena)                           |
| Dr. Inés Roldán         | Research Scientist — Software Engineering / CS  | `research-science/` (reports to Mokoena)                           |
| Dr. Samuel Okonkwo      | Research Scientist — Machine Learning Theory    | `research-science/` (reports to Mokoena)                           |
| Dr. Mireille Dubois     | Research Scientist — LLM Systems                | `research-science/foundational-ai/` (reports to Bhandari)          |
| Dr. Wei-Ling Tan        | Research Scientist — Applied AI Systems         | `research-science/foundational-ai/` (reports to Bhandari)          |
| Dr. Kaito Fujimori      | Research Scientist — Agent Systems Research     | `research-science/` (reports to Mokoena)                           |
| Tobias Lindqvist        | Knowledge Systems Engineer                      | `knowledge-systems/` (reports to Mokoena)                          |

For complete rosters and full profiles, see:

- **Company:** `company/library/overview/personnel.md`
- **Studio:** `studio/casual-games/team/README.md`
- **CC-00:** `core-component-00/crew/README.md`
- **ANU-00:** `academic-neural-unit-00/crew/README.md`

---

_This document is maintained at the workspace root. Update it whenever the workspace gains a new system, the authority model changes, tooling is added, or the operating environment changes. It is not owned by any single sub-system._
