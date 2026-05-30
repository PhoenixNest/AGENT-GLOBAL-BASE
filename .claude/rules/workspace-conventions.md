---
description: Core workspace conventions and rules — always active for all sessions
---

# Workspace Conventions

Core conventions for the `agent-global-base` workspace. These rules are mandatory for all AI executor agents.

---

## File and Folder Naming

| Item Type              | Convention                                                                             |
| ---------------------- | -------------------------------------------------------------------------------------- |
| Directory/folder names | kebab-case (e.g., `casual-games`, `brand-design`, `puzzle-rush`)                       |
| Agent profile files    | Always named `profile.md`                                                              |
| Skill files            | `skills/<skill-name>.md` — adjacent to the agent folder                                |
| Pipeline documents     | `pipeline.md` — inside the pipeline folder                                             |
| Optimization records   | `YYYY-MM-DD-<slug>/` folder containing `optimization-plan.md` + `execution-tracker.md` |

---

## Document Authority Hierarchy

When sources conflict, apply this precedence (highest to lowest):

1. `pipeline.md` in a pipeline folder — canonical truth for that pipeline
2. `agent/profile.md` — canonical identity for an agent
3. `library/overview/*.md` — authoritative summaries
4. `library/departments/*.md` — readable summaries (may lag)

---

## Company Personnel Tier System

| Tier             | Description                                           |
| ---------------- | ----------------------------------------------------- |
| C-suite          | Placed before recruitment; own pipeline stage outputs |
| Team Supervisors | Recruited after C-suite; own sub-department execution |
| Teammates        | Individual contributors                               |

---

## Company Pipeline Progress Monitoring

For any company development project at or beyond **Stage 4 — _UML → Implementation Plan + Gantt_**, maintain:

| File              | Purpose                     |
| ----------------- | --------------------------- |
| `progress.md`     | Real-time state             |
| `session-log.md`  | Audit trail                 |
| `checkpoint.json` | Machine-readable milestones |

Any task exceeding estimate by >20% triggers CTO → CPO schedule risk notification.

---

## Context and Session Management

| Situation                | Action                                                                   | Reference                                                                     |
| ------------------------ | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Session boundary reached | Maintain `progress.md`, `session-log.md`, `checkpoint.json`              | —                                                                             |
| Context budget pressure  | Apply Sacred Context; run the context compressor                         | `core-component-00/context-engineering/implementations/context_compressor.py` |
| Inter-agent handoff      | Follow the three-tier Context Handoff Protocol (Full / Scoped / Minimal) | `core-component-00/context-engineering/patterns/multi-agent-handoff.md`       |

---

## Formatting Requirements

Run **Prettier** on every file created or modified before finalizing:

```powershell
prettier --write "<file-path>"
```

---

## The Three Co-Resident Systems

| System          | Path                 | Purpose                                                      |
| --------------- | -------------------- | ------------------------------------------------------------ |
| **The Company** | `company/`           | Mobile product company — org structure, pipelines, personnel |
| **The Studio**  | `studio/`            | Creative studios — crew, pipelines, and projects             |
| **CC-00 Lab**   | `core-component-00/` | Applied LLM research laboratory — engineering stack          |

---

## Agent Activation Protocol

When the user requests output from a named organizational agent (Type A):

1. Read `agent/profile.md` — establish identity and authority scope
2. Read all referenced `skills/*.md` files — executable contracts, not suggestions
3. Adopt their voice and perspective
4. Produce output strictly within their documented authority
5. Ensure the artifact conforms to the stage spec in the relevant `pipeline.md`

**Never impersonate an agent without reading their profile first.**

---

## Authority Hierarchy

```
User  ←  Absolute apex. Final authority on all decisions.
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

---

## User Approval Gates

Pipeline stages marked **User Approval? ✅** are **hard stops**. Present the completed deliverable, explicitly request sign-off, and **wait**. Never auto-advance past these gates.

---

## Mandatory Governance

The Agent Systems Engineering (ASE) framework is mandatory across all pipelines. No agent may bypass it. All new LLM systems must be grounded in CC-00 engineering patterns.
