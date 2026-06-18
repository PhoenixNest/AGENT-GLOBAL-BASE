# studio/casual-games/projects/ — Game Projects

Per-game project folders for the Casual Games Studio. No projects have been initiated yet —
this folder is ready to receive the first game project when Stage 1 is approved.

---

## What Lives Here

```
projects/
└── <game-slug>/           ← One folder per game project (kebab-case slug)
    ├── progress.md        ← Real-time production state (required at Stage 5+)
    ├── session-log.md     ← Audit trail (required at Stage 5+)
    ├── checkpoint.json    ← Machine-readable milestones (required at Stage 5+)
    └── ...                ← Stage deliverables, builds, assets (per pipeline spec)
```

---

## Folder Naming Convention

Game project folders use **kebab-case slugs**:

```
puzzle-rush/
bubble-pop-extreme/
tower-climb/
```

The slug becomes the canonical identifier for the project across all documents, pipeline references,
and monitoring files.

---

## Progress Monitoring (Stage 5+)

Any project at or beyond Stage 5 (Full Production) must maintain these three files at the project
root:

| File              | Purpose                                                        | Owner               |
| ----------------- | -------------------------------------------------------------- | ------------------- |
| `progress.md`     | Real-time production state — current stage, blockers, velocity | Production division |
| `session-log.md`  | Audit trail of all session work — timestamped entries          | Production division |
| `checkpoint.json` | Machine-readable milestones — used for automated status checks | Production division |

These files are mandatory. A Stage 5+ project without them is in a compliance gap.

---

## Pipeline Stage Ownership

Project folders receive deliverables stage by stage. Key stages that produce project-folder
artifacts:

| Stage | Deliverables Added to Project Folder                                   |
| ----- | ---------------------------------------------------------------------- |
| 1     | GDD, PRD, SRD                                                          |
| 2     | Playable prototype build, GDS                                          |
| 3     | Vertical slice build                                                   |
| 4     | Production plan, resource schedule, risk register                      |
| 5+    | `progress.md`, `session-log.md`, `checkpoint.json` (monitoring begins) |
| 6     | Test reports, defect log                                               |
| 7     | Soft-launch build, store assets, analytics config                      |

---

## Context and Session Management

For long-running Stage 5 sessions approaching context limits:

1. Apply Sacred Context principles — keep GDD, PRD, SRD, and production plan in the system slot
2. Run `ContextCompressor` if session exceeds budget
3. Use the Context Handoff Protocol for any agent transitions

Reference: `core-component-00/context-engineering/patterns/multi-agent-handoff.md`

---

## Rules

- Project folder names must be kebab-case slugs.
- `progress.md`, `session-log.md`, and `checkpoint.json` are mandatory at Stage 5+.
- Do not initiate a project folder without a GDD, PRD, and SRD approved at Stage 1.
- Escalation for schedule overruns follows the path defined in
  `studio/casual-games/pipeline/casual-games-pipeline.md`.
