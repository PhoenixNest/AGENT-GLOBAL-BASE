---
name: studio-audio-game-sound-design
description: Game sound design — sound effect creation, Foley recording, UI audio, combat audio, environmental ambience, and mobile audio optimization. Owned by Kenji Takahashi (Audio Designer). Use during Studio Pipeline Stages 3–5 for SFX production and audio integration. Trigger: sound design, SFX, Foley, UI audio, combat audio, environmental ambience, mobile audio, audio memory budget.
version: "1.0.0"
---

# Game Sound Design

**Skill ID:** game-sound-design
**Role:** Audio Designer
**Seniority:** Senior

## Overview

Game sound design — sound effect creation, Foley recording, UI audio, combat audio, environmental ambience, and mobile audio optimization.

## Tools & Frameworks

| Tool           | Proficiency | Use Case                               |
| -------------- | ----------- | -------------------------------------- |
| Reaper         | Expert      | Audio editing, mixing, mastering       |
| FMOD Studio    | Expert      | Audio middleware implementation        |
| Wwise          | Advanced    | Alternative audio middleware           |
| Field Recorder | Advanced    | Foley recording, environmental capture |
| Serum/Vital    | Advanced    | Synthesized sound creation             |

## Scenarios & Trade-offs

### Scenario 1: 300+ Sound Effect Library

- **Approach:** Categorize sounds by type (UI, combat, environment, ambient, feedback); establish naming convention; batch-produce with variation
- **Trade-off:** Sound variety vs. memory budget — more variations = more natural feel but higher memory cost
- **Quality Bar:** Each sound clearly communicates its function; 3+ variations per sound to avoid repetition fatigue; total audio memory ≤ 30MB

### Scenario 2: Mobile Audio Memory Budget

- **Approach:** Use compressed formats (Vorbis for music, ADPCM for SFX); implement streaming for long audio; pool short sounds in memory
- **Trade-off:** Audio quality vs. file size — higher compression = smaller files but quality loss
- **Quality Bar:** All sounds clear and impactful on mobile speakers; total audio package ≤ 50MB; no audio glitches during gameplay

## Quality Standards

- All sounds delivered in specified formats (48kHz/16-bit source, compressed delivery)
- Naming convention: `sfx_{category}_{action}_{variation}`
- Audio implementation documented with FMOD/Wwise event structure
- Sounds tested on device speakers and headphones
- Audio mixing levels balanced (SFX > music > ambience for mobile)

## Industry References

- FMOD mobile game audio best practices
- Nintendo mobile title sound design approach
- Game audio memory optimization techniques
