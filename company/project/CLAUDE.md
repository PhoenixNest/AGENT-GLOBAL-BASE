# company/project/ — Active Project Dashboard

Workspace for active company development projects at Stage 4 and beyond. Each project monitored
here has an approved Implementation Plan and is in active execution.

---

## What Lives Here

```
project/
└── _dashboard.md    ← Cross-project status overview (pipeline stage, health, owner)
```

Individual project monitoring files (`progress.md`, `session-log.md`, `checkpoint.json`) live
inside the relevant pipeline folder or a dedicated project subfolder — not at this level.

---

## Purpose

This folder provides a high-level dashboard view across all active company development projects.
Use `_dashboard.md` to get the current state of all projects before diving into a specific one.

---

## Mandatory Monitoring Files (Stage 4+)

Any company development project at or beyond Stage 4 (UML → Implementation Plan + Gantt) must
maintain three files:

| File              | Purpose                                                     |
| ----------------- | ----------------------------------------------------------- |
| `progress.md`     | Real-time project state — current stage, blockers, velocity |
| `session-log.md`  | Audit trail — timestamped record of all session work        |
| `checkpoint.json` | Machine-readable milestones — for automated status checks   |

Use the templates from the relevant pipeline folder:

```
company/pipeline/<type>/templates/monitoring/
```

---

## Schedule Risk Rule

Any task exceeding its estimate by **more than 20%** triggers a mandatory CTO → CPO schedule risk
notification. Document the notification in `session-log.md`.

---

## Navigation

| I need…                                    | Go to                                           |
| ------------------------------------------ | ----------------------------------------------- |
| Cross-project status overview              | `_dashboard.md`                                 |
| A specific pipeline's monitoring templates | `company/pipeline/<type>/templates/monitoring/` |
| The company's 13-stage pipeline reference  | `company/library/overview/pipeline.md`          |
| Pipeline-specific stage rules              | `company/pipeline/<type>/pipeline.md`           |
| Progress monitoring conventions            | `company/library/topics/monitoring.md`          |

---

## Rules

- Check `_dashboard.md` before starting any project execution work to understand current state.
- Do not create project monitoring files here without first reading the relevant pipeline's
  `templates/monitoring/` templates.
- Stage 4+ projects without `progress.md`, `session-log.md`, and `checkpoint.json` are in a
  compliance gap — create them immediately using the pipeline templates.
