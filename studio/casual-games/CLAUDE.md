# studio/casual-games/ — Casual Games Studio

Entry point for the Casual Games Studio. Read this before doing any studio-related work.

---

## What This Is

The Casual Games Studio is the only active studio in the organization. It is a fully staffed
creative game development studio targeting the mobile casual games market, using Unity 6.3 LTS as
the primary engine. All 39 crew members are hired and the studio is Stage 0-ready. No projects have
been initiated yet.

---

## Studio Profile

| Field    | Detail                                                                     |
| -------- | -------------------------------------------------------------------------- |
| Engine   | Unity 6.3 LTS                                                              |
| Status   | All 39 crew hired · Stage 0-ready · No projects initiated                  |
| Pipeline | 11 stages (Stage 0–10) — **distinct from the company's 13-stage pipeline** |
| Crew     | 38 FTE + 1 Contract across 7 divisions                                     |

---

## Where to Start

| I need…                             | Go to                                     |
| ----------------------------------- | ----------------------------------------- |
| Studio overview, charter, brief     | `library/overview/casual-games-studio.md` |
| The 11-stage pipeline + stage gates | `pipeline/casual-games-pipeline.md`       |
| Crew roster by division             | `team/README.md`                          |
| Active or planned game projects     | `projects/`                               |
| Topics (audio, art, live-ops, etc.) | `library/topics/`                         |

---

## Directory Structure

```
studio/casual-games/
├── library/           ← Studio knowledge hub (start here)
│   ├── overview/      ← Studio charter, strategic brief
│   ├── topics/        ← Domain-specific topics (audio, art, monetization, etc.)
│   └── references/    ← External references
├── pipeline/          ← 11-stage game development pipeline
├── team/
│   └── crew/          ← 7 divisions, all 39 crew
└── projects/          ← Per-game project folders (kebab-case slugs)
```

---

## The 11-Stage Pipeline

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

**Stages marked ✅ are hard stops** — present the deliverable and wait for user sign-off before
advancing. Do not conflate these stage numbers with the company's 13-stage pipeline.

---

## Crew Divisions

| Division        | Scope                              |
| --------------- | ---------------------------------- |
| Leadership      | Studio Director, Creative Director |
| Production      | Producers, project management      |
| Creative-Design | Game design, UX/UI for games       |
| Art             | 2D/3D art, animation, VFX          |
| Audio           | Sound design, music, FMOD/Wwise    |
| Engineering     | Unity development, tools, CI       |
| Live-Ops        | Post-launch operations, analytics  |

---

## Agent Path Conventions

```
team/crew/<division>/<role>/<name>/agent/profile.md
team/crew/<division>/<role>/<name>/skills/<skill>.md
```

---

## Project Folder Conventions

- Game project folders live under `projects/` using **kebab-case slugs** (e.g., `puzzle-rush`)
- Stage 5+ projects must maintain `progress.md`, `session-log.md`, and `checkpoint.json`
- Escalation for overruns follows the escalation path in `pipeline/casual-games-pipeline.md`

---

## Critical Rules

- **This pipeline is exclusive to the Casual Games Studio.** Future studios define their own
  pipelines independently — do not assume they inherit this structure.
- **Never conflate studio stage numbers with company pipeline stage numbers.**
- Read `pipeline/casual-games-pipeline.md` before producing any stage deliverable.
- Activate crew agents via the standard protocol: read `profile.md` then all `skills/*.md` first.
