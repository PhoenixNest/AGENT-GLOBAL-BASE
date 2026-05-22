---
inclusion: auto
description: Core workspace conventions and rules from AGENTS.md
version: "1.0.0"
---

# Workspace Conventions

This steering file provides core workspace conventions that apply to all work in the `agent-global-base` workspace. These rules are extracted from AGENTS.md and are mandatory for all AI executor agents.

---

## File and Folder Naming

| Item Type              | Convention                                                                             |
| ---------------------- | -------------------------------------------------------------------------------------- |
| Directory/folder names | kebab-case (e.g., `casual-games`, `brand-design`, `puzzle-rush`)                       |
| Agent profile files    | Always named `profile.md`                                                              |
| Skill files            | `skills/<skill-name>.md` — in a `skills/` directory adjacent to the agent folder       |
| Pipeline documents     | `pipeline.md` — inside the pipeline folder                                             |
| Optimization records   | `YYYY-MM-DD-<slug>/` folder containing `optimization-plan.md` + `execution-tracker.md` |

---

## Document Authority Hierarchy

When sources conflict, apply this precedence (highest to lowest):

1. `pipeline.md` in a pipeline folder — canonical truth for that pipeline
2. `agent/profile.md` — canonical identity for an agent
3. `library/overview/*.md` — authoritative summaries
4. `library/departments/*.md` — readable summaries (may lag the canonical source)

---

## Company Personnel Tier System

The following tier system applies to the **Company** system only. The Casual Games Studio uses a division-based structure.

| Tier             | Description                                           |
| ---------------- | ----------------------------------------------------- |
| C-suite          | Placed before recruitment; own pipeline stage outputs |
| Team Supervisors | Recruited after C-suite; own sub-department execution |
| Teammates        | Individual contributors                               |

---

## Company Pipeline Progress Monitoring

For any company development project at or beyond **Stage 4 — _UML → Implementation Plan + Gantt_**, three files must be maintained within the project folder:

| File              | Purpose                     |
| ----------------- | --------------------------- |
| `progress.md`     | Real-time state             |
| `session-log.md`  | Audit trail                 |
| `checkpoint.json` | Machine-readable milestones |

Any company pipeline task exceeding its estimate by >20% triggers a CTO → CPO schedule risk notification. Studio projects follow the escalation path defined in the Casual Games Studio pipeline.

---

## Context and Session Management

For long-running work sessions — including company pipeline Stage 4 onward, Casual Games Studio pipeline Stage 5 onward, or any multi-session research task:

| Situation                | Action                                                                   | Reference                                                                     |
| ------------------------ | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Session boundary reached | Maintain `progress.md`, `session-log.md`, `checkpoint.json`              | —                                                                             |
| Context budget pressure  | Apply Sacred Context principles; run the context compressor              | `core-component-00/context-engineering/implementations/context_compressor.py` |
| Inter-agent handoff      | Follow the three-tier Context Handoff Protocol (Full / Scoped / Minimal) | `core-component-00/context-engineering/patterns/multi-agent-handoff.md`       |

---

## Formatting Requirements

Run **Prettier** on every file created or modified before finalizing:

```powershell
prettier --write "<file-path>"
```

This is mandatory per AGENTS.md § 8.7.

---

## The Three Co-Resident Systems

This workspace contains three independent systems:

| System          | Path                 | Purpose                                                             |
| --------------- | -------------------- | ------------------------------------------------------------------- |
| **The Company** | `company/`           | Mobile product company — org structure, pipelines, personnel        |
| **The Studio**  | `studio/`            | Creative studios — crew, pipelines, and projects across disciplines |
| **CC-00 Lab**   | `core-component-00/` | Applied LLM research laboratory — engineering stack                 |

Each system has its own:

- Library documentation (`library/`)
- Pipeline definitions (`pipeline/`)
- Personnel/crew structure (`departments/` or `team/crew/`)
- Agent profiles and skills

---

## Agent Types

### Type A — Organizational Agents (Personas)

Named personas that exist as documents. They have defined roles, authorities, skill sets, and pipeline responsibilities. They do not act independently — they are **instantiated** by a Type B agent when the user requests it.

Each organizational agent consists of:

- `agent/profile.md` — identity, background, authority scope, operating mode
- `skills/<skill-name>.md` — executable specifications defining how they produce work

### Type B — AI Executor Agents (LLM Instances)

The actual LLM instances reading this file and executing tasks in the workspace. **You are a Type B agent.**

---

## Agent Activation Protocol

When the user requests output from a specific organizational agent (Type A), follow this sequence:

1. Read `agent/profile.md` — establish identity, authority scope, and pipeline stage ownership
2. Read all referenced `skills/*.md` files — these are executable contracts, not suggestions
3. Adopt their voice and perspective for the requested deliverable
4. Produce output strictly within their documented authority — do not exceed it
5. Ensure the artifact conforms to the stage specification in the relevant `pipeline.md`

**Never impersonate an agent without reading their profile first.**

---

## Authority Hierarchy

```
User  ←  Absolute apex. Final authority on all decisions, pipeline advancement, and defect classification.
  │
  ├── Company C-suite  (CPO · CDO · CTO · CIO · CSO · CHRO · CTO-L · CLO)
  │     └── Company Team Supervisors  →  Teammates
  │
  ├── Studio Director  (Dr. Marcus Vogel)
  │     └── Studio Division Leads  →  Crew
  │
  └── CC-00 Lab Director  (Dr. Elias Vance)
        └── CC-00 Research Programmes
```

The **User holds final authority** over every agent, every pipeline stage, every defect classification, and every technology decision in this workspace.

---

## User Approval Gates

Pipeline stages marked **User Approval? ✅** are **hard stops**. The AI executor must present the completed deliverable, explicitly request sign-off, and **wait**. Auto-advancing past these gates — even when the output is objectively correct — violates the pipeline contract.

---

## Mandatory Governance

The Agent Systems Engineering (ASE) framework is mandatory across all pipelines. No agent may bypass it. All new LLM systems built in this workspace must be grounded in CC-00 engineering patterns.

---

_This steering file is automatically included in all Kiro sessions. It provides the foundational conventions for working in this workspace._
