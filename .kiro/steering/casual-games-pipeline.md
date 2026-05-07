---
inclusion: fileMatch
fileMatchPattern: "**/studio/casual-games/**"
---

# Casual Games Studio Pipeline — 11-Stage Game Development Process

**Authority:** AGENTS.md § 5.3 + `studio/casual-games/pipeline/casual-games-pipeline.md`  
**Applies To:** All Casual Games Studio projects

---

## Pipeline Overview

The Casual Games Studio uses an **11-stage game development pipeline** (Stages 0-10) that is **distinct from the company's 13-stage pipeline**.

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

## Studio Profile

- **Engine:** Unity 6.3 LTS
- **Status:** All 39 crew hired, Stage 0-ready
- **Crew:** 38 FTE + 1 Contract across 7 divisions
- **Projects:** None initiated yet

## Stage-Specific Requirements

### Stage 0: Art Direction + Style Guide

**Deliverables:**

- Art direction document
- Visual style guide
- Color palette
- Typography system
- UI/UX style guide
- Reference mood boards

**Key Producers:** Creative Director, Art Director

**User Approval:** ❌ (Internal creative decision)

### Stage 1: Concept (GDD + PRD + SRD)

**Deliverables:**

- **GDD (Game Design Document):** Core gameplay, mechanics, systems
- **PRD (Product Requirements Document):** Features, scope, success metrics
- **SRD (Security Requirements Document):** Security, privacy, compliance

**Key Producers:** Studio Director, Creative Director, Game Designer

**User Approval:** ✅

**GDD Required Sections:**

- Game concept and vision
- Core gameplay loop
- Game mechanics and systems
- Player progression
- Monetization design
- Target audience
- Competitive analysis

### Stage 2: Prototype (Playable + GDS)

**Deliverables:**

- **Playable Prototype:** Core gameplay loop implemented
- **GDS (Game Design Specification):** Detailed design documentation

**Key Producers:** Game Designer, Gameplay Engineers, UI/UX Designer

**User Approval:** ✅

**Prototype Requirements:**

- Core gameplay loop functional
- Basic UI/UX implementation
- Placeholder art assets
- Playable for 5-10 minutes
- Demonstrates fun factor

### Stage 3: Vertical Slice

**Deliverable:** Polished vertical slice of the game

**Key Producers:** Full production team

**User Approval:** ✅

**Vertical Slice Requirements:**

- One complete level/section fully polished
- Final art style implemented
- Final audio implemented
- Final UI/UX implemented
- Representative of final game quality
- Playable for 15-30 minutes

### Stage 4: Production Planning

**Deliverables:**

- Production schedule (Gantt chart)
- Resource allocation plan
- Milestone definitions
- Risk assessment
- Budget breakdown

**Key Producers:** Studio Director, Executive Producer, Production Manager

**User Approval:** ✅

### Stage 5: Full Production

**Activities:**

- Implement all game content
- Create all art assets
- Implement all audio
- Implement all UI/UX
- Integrate all systems
- Optimize performance

**Key Producers:** Full production team

**User Approval:** ❌ (Continuous work)

**Production Standards:**

- Follow Unity best practices
- Maintain consistent art style
- Implement proper asset management
- Use version control (Git)
- Conduct regular playtests

### Stage 6: Automated Testing

**Deliverables:**

- Unit tests (C# code)
- Integration tests (game systems)
- Performance tests (frame rate, memory)
- Automated playthrough tests
- Test coverage report

**Key Producers:** QA Lead, QA Engineers, Gameplay Engineers

**User Approval:** ✅

**Testing Requirements:**

- Unit test coverage > 70%
- All critical paths tested
- Performance benchmarks met (60 FPS target)
- Memory usage within limits
- No critical bugs (P0/P1)

### Stage 7: Soft Launch Prep

**Deliverables:**

- Soft launch build
- Analytics integration (Firebase, Unity Analytics)
- Monetization integration (IAP, ads)
- Crash reporting (Firebase Crashlytics)
- Soft launch plan (regions, duration, metrics)

**Key Producers:** Live Ops Manager, Monetization Designer, Data Analyst

**User Approval:** ✅

**Soft Launch Checklist:**

- Build optimized for target platforms
- Analytics events implemented
- Monetization tested
- Privacy policy and terms of service
- App store assets prepared
- Support channels ready

### Stage 8: Soft Launch

**Activities:**

- Launch in selected regions
- Monitor key metrics (retention, monetization, engagement)
- Collect player feedback
- Identify issues and improvements
- Iterate based on data

**Key Producers:** Live Ops Manager, Data Analyst, Studio Director

**User Approval:** ✅ (To proceed to global launch)

**Soft Launch Metrics:**

- Day 1 retention > 40%
- Day 7 retention > 20%
- Day 30 retention > 10%
- ARPDAU (Average Revenue Per Daily Active User) > target
- Crash rate < 1%

### Stage 9: Global Launch Readiness

**Deliverables:**

- Global launch build
- Localization complete (all target languages)
- Marketing assets prepared
- App store optimization (ASO)
- Launch plan and timeline

**Key Producers:** Studio Director, Live Ops Manager, Localization Lead

**User Approval:** ✅

**Global Launch Checklist:**

- All soft launch issues resolved
- Localization tested
- Marketing campaign ready
- App store submissions complete
- Server capacity tested
- Support team trained

### Stage 10: Live Ops (Continuous)

**Activities:**

- Monitor game health metrics
- Release content updates
- Run live events
- Manage economy balance
- Respond to player feedback
- Optimize monetization

**Key Producers:** Live Ops Manager, Content Designers, Data Analyst

**User Approval:** QBR (Quarterly Business Review)

**Live Ops Metrics:**

- Daily Active Users (DAU)
- Monthly Active Users (MAU)
- Retention (D1, D7, D30)
- ARPDAU
- Lifetime Value (LTV)
- Crash rate < 1%

## Unity 6.3 LTS Standards

**Project Structure:**

- Use Assembly Definitions for modular code
- Organize assets by feature/system
- Use Addressables for asset management
- Implement proper scene management

**Performance Standards:**

- Target 60 FPS on mid-range devices
- Memory usage < 1GB on mobile
- Build size < 150MB (initial download)
- Asset bundle optimization

**Code Standards:**

- Follow C# coding conventions
- Use dependency injection (Zenject, VContainer)
- Implement proper object pooling
- Use async/await for asynchronous operations

## Game-Specific Defect Severity

**P0 (Blocks Release):**

- Game crashes on launch
- Core gameplay loop broken
- Data loss or save corruption
- Payment processing failure
- Security vulnerability

**P1 (Blocks Release):**

- Major gameplay bug
- Progression blocker
- Critical UI issue
- Audio completely broken
- Performance below 30 FPS

**P2 (User Decides):**

- Minor gameplay bug
- Visual glitch
- Audio issue (non-critical)
- Performance dip (30-60 FPS)

**P3 (User Decides):**

- Polish issue
- Minor visual inconsistency
- Typo or text issue

## Project Folder Structure

```
studio/casual-games/projects/<game-slug>/
├── README.md
├── gdd.md
├── prd.md
├── srd.md
├── gds.md
├── production-plan.md
├── progress.md
├── session-log.md
├── checkpoint.json
├── builds/
├── assets/
└── unity-project/
```

## Related Steering Files

- `unity-development.md` — Unity 6.3 LTS development patterns
- `game-design.md` — Game design document patterns

## Related Skills

- `.kiro/skills/game-development/` — Game development domain skills
  - `studio-leadership.md`
  - `live-ops-strategy.md`
