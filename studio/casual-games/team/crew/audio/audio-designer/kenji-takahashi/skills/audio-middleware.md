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

## Industry References

- FMOD adaptive music implementation guide
- Wwise mobile game audio optimization
- Unity audio middleware integration best practices
