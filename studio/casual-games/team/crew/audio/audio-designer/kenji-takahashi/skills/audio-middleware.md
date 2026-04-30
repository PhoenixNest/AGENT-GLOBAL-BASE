---
name: studio-audio-audio-middleware
description: Audio middleware implementation for games — FMOD and Wwise integration, adaptive music systems, parameter-driven audio, and mobile audio optimization. Owned by Kenji Takahashi (Audio Designer). Use during Studio Pipeline Stages 4–5 for audio middleware setup and integration. Trigger: audio middleware, FMOD, Wwise, adaptive music, parameter-driven audio, audio events, bank optimization, Unity audio integration.
version: "1.0.0"
---

# Audio Middleware

**Skill ID:** audio-middleware
**Role:** Audio Designer
**Seniority:** Senior

## Overview

Audio middleware implementation for games — FMOD and Wwise integration, adaptive music systems, parameter-driven audio, and mobile audio optimization.

## Tools & Frameworks

| Tool                    | Proficiency | Use Case                         |
| ----------------------- | ----------- | -------------------------------- |
| FMOD Studio             | Expert      | Primary audio middleware         |
| Wwise                   | Advanced    | Alternative middleware expertise |
| Unity FMOD Integration  | Expert      | Engine integration and scripting |
| Unity Wwise Integration | Advanced    | Alternative engine integration   |

## Scenarios & Trade-offs

### Scenario 1: Adaptive Music System

- **Approach:** Design multi-layer music tracks (base, rhythm, melody, intensity) that respond to gameplay state via FMOD parameters
- **Trade-off:** Musical complexity vs. memory cost — more layers = richer adaptation but more memory
- **Quality Bar:** Music transitions are seamless; parameter changes feel natural; memory cost ≤ 10MB for adaptive music system

### Scenario 2: Event-Driven Audio Architecture

- **Approach:** Design FMOD event hierarchy matching game architecture; implement parameter modulation for contextual audio; optimize bank loading
- **Trade-off:** Audio granularity vs. implementation complexity — more events = more control but harder to manage
- **Quality Bar:** Every game action has appropriate audio feedback; event structure is maintainable; bank loading is optimized for memory

## Quality Standards

- FMOD/Wwise project organized with clear event hierarchy
- All audio events documented with trigger conditions and parameter ranges
- Bank loading strategy optimized for memory (load-on-demand vs. preload)
- Audio middleware integrated with game's state machine
- Performance profiling completed on target devices

## Director Review and Approval Path

All major audio implementation decisions require review and approval by Hiroshi Nakamura (Composer/Sound Director, Contract) before they are committed to production. This applies to any decision that shapes the middleware architecture or user-facing audio behaviour at a systemic level.

**Decisions that require Hiroshi's approval:**

- FMOD or Wwise event hierarchy structure for a new game (the top-level bus/group organization, not individual events)
- Audio bus routing and mixer topology (how stems feed into buses, which buses receive effects processing)
- Snapshot configurations for state-based audio (combat, menu, cutscene, low-health — the parameter ranges and blend curves)
- Adaptive music system layer architecture (which stems are layered, the parameter logic that drives transitions)

**Approval process:**

1. Kenji drafts an **Audio Implementation Proposal** document for each new game's middleware setup. The proposal covers: proposed event hierarchy diagram, bus routing schematic, snapshot list with trigger conditions, and rationale for any non-standard configuration choices.
2. Kenji submits the proposal to Hiroshi via email with a 3-business-day review window.
3. Hiroshi returns one of three responses: **Approved** (Kenji proceeds to implementation), **Revision Requested** (Hiroshi notes specific changes required; Kenji revises and resubmits), or **Escalate to Creative Director** (Hiroshi forwards to Sakura Ishimori for a creative direction call).
4. Kenji does not begin production middleware implementation until an Approved response is received. Prototype-phase placeholder setups (e.g., a temporary flat event hierarchy used during Stage 2 prototyping) do not require formal approval but must be flagged as placeholders in the project.

## Industry References

- FMOD adaptive music implementation guide
- Wwise mobile game audio optimization
- Unity audio middleware integration best practices
