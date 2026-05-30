---
paths:
  - "**/studio/casual-games/**"
description: Casual Games Studio 11-stage pipeline rules
---

# Casual Games Studio Pipeline — 11-Stage Game Development Process

**Applies To:** All Casual Games Studio projects
**Engine:** Unity 6.3 LTS

---

## Pipeline Overview

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

> This pipeline is **distinct from the company's 13-stage pipeline**. Do not conflate them.

---

## Key Stage Requirements

**Stage 1** deliverables: GDD, PRD, SRD

**Stage 2** deliverables: Playable Prototype (core loop functional, 5–10 minutes) + GDS

**Stage 5** (Full Production): `progress.md`, `session-log.md`, `checkpoint.json` required

**Stage 6** testing: Unit > 70% coverage, performance ≥ 60 FPS, no P0/P1

**Stage 8** Soft Launch metrics: D1 retention > 40%, D7 > 20%, D30 > 10%, crash rate < 1%

---

## Game-Specific Defect Severity

- **P0:** Crash on launch, core loop broken, save corruption, payment failure, security vulnerability
- **P1:** Major gameplay bug, progression blocker, performance below 30 FPS
- **P2/P3:** User decides

---

## Project Folder Structure

```
studio/casual-games/projects/<game-slug>/
├── gdd.md, prd.md, srd.md, gds.md
├── production-plan.md
├── progress.md, session-log.md, checkpoint.json
├── builds/, assets/, unity-project/
```
