# studio/casual-games/pipeline/ — Game Development Pipeline

Canonical source for the Casual Games Studio 11-stage pipeline. The `casual-games-pipeline.md`
inside this folder is the highest-authority document for all studio pipeline work.

---

## Canonical Document

```
pipeline/casual-games-pipeline.md    ← READ THIS FIRST for any pipeline stage work
```

---

## The 11-Stage Pipeline at a Glance

| Stage | Name                        | Primary Owner                       | User Approval? |
| ----- | --------------------------- | ----------------------------------- | -------------- |
| 0     | Art Direction + Style Guide | Creative Director                   | ❌             |
| 1     | Concept (GDD + PRD + SRD)   | Studio Director + Creative Director | ✅             |
| 2     | Prototype (Playable + GDS)  | Production + Engineering            | ✅             |
| 3     | Vertical Slice              | Engineering + Art + Audio           | ✅             |
| 4     | Production Planning         | Studio Director + Production        | ✅             |
| 5     | Full Production             | All divisions                       | ❌             |
| 6     | Automated Testing           | Engineering                         | ✅             |
| 7     | Soft Launch Prep            | Production + Live-Ops               | ✅             |
| 8     | Soft Launch                 | Studio Director                     | ✅             |
| 9     | Global Launch Readiness     | All divisions                       | ✅             |
| 10    | Live Ops (continuous)       | Live-Ops division                   | QBR review     |

---

## Stage Gate Rules

- Stages marked ✅ are **hard stops** — present the deliverable, request user sign-off, and wait.
  Never auto-advance past a ✅ gate.
- Stage 10 (Live Ops) is reviewed on a Quarterly Business Review (QBR) cadence rather than a
  one-time gate.

---

## Progress Monitoring (Stage 5+)

Projects at or beyond Stage 5 (Full Production) must maintain:

| File              | Purpose                     |
| ----------------- | --------------------------- |
| `progress.md`     | Real-time production state  |
| `session-log.md`  | Audit trail of session work |
| `checkpoint.json` | Machine-readable milestones |

These files live inside the game project folder under `projects/<game-slug>/`.

---

## Key Deliverables by Stage

| Stage | Key Deliverables                                  |
| ----- | ------------------------------------------------- |
| 0     | Art Direction Document, Style Guide               |
| 1     | Game Design Document (GDD), PRD, SRD              |
| 2     | Playable Prototype, Game Design Spec (GDS)        |
| 3     | Vertical Slice build (target platform)            |
| 4     | Production Plan, resource schedule, risk register |
| 5     | Feature-complete build per production plan        |
| 6     | Test reports, defect log, pass/fail criteria      |
| 7     | Store assets, soft-launch build, analytics setup  |
| 8     | Soft-launch live — limited market                 |
| 9     | Global launch build, localization complete        |
| 10    | Live-ops cadence: content updates, analytics, QBR |

---

## Critical Warning

**This pipeline belongs exclusively to the Casual Games Studio.** Do not apply these stage numbers
or gate rules to company development pipelines (Mobile, Web, Backend API, Full-Stack). Those are
a separate 13-stage process under `company/pipeline/`. Stage numbering does not transfer across
systems.
