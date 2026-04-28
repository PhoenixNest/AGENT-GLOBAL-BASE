---
name: studio-audio-chiptune-synthesis
description: Chiptune and retro-style music synthesis for games — Deflemask, FamiTrack, YM2612/SNR76489 chip emulation, and authentic retro sound design. Owned by Kenji Takahashi (Audio Designer). Use during Studio Pipeline Stages 3–5 for retro audio production. Trigger: chiptune synthesis, retro audio, Deflemask, FamiTrack, chip emulation, NES audio, Genesis audio, retro SFX.
version: "1.0.0"
---

# Chiptune Synthesis

**Skill ID:** chiptune-synthesis
**Role:** Audio Designer
**Seniority:** Senior

## Overview

Chiptune and retro-style music synthesis for games — Deflemask, FamiTrack, YM2612/SNR76489 chip emulation, and authentic retro sound design.

## Tools & Frameworks

| Tool        | Proficiency  | Use Case                                      |
| ----------- | ------------ | --------------------------------------------- |
| Deflemask   | Expert       | Primary chiptune composition tool             |
| FamiTrack   | Advanced     | NES-style composition                         |
| LSDJ        | Intermediate | Game Boy-style composition                    |
| VST plugins | Advanced     | Modern chiptune synthesis (Plogue Chipsounds) |

## Scenarios & Trade-offs

### Scenario 1: Retro-Themed Bonus Mode Music

- **Approach:** Compose chiptune tracks using Deflemask with authentic chip limitations (4 channels, specific waveforms); export as module files
- **Trade-off:** Authenticity vs. accessibility — authentic chiptune may feel harsh to modern ears
- **Quality Bar:** Music captures retro aesthetic while remaining pleasant; chip limitations used creatively, not as constraint

### Scenario 2: Chiptune SFX Integration

- **Approach:** Design sound effects using same synthesis techniques as music for cohesive audio identity; integrate with FMOD for parameter control
- **Trade-off:** Stylistic consistency vs. functional clarity — chiptune SFX may lack the punch of modern sound design
- **Quality Bar:** SFX are functionally clear (player understands feedback) while maintaining retro style; no audio masking issues

## Quality Standards

- All chiptune compositions documented with channel assignments and instrument settings
- Module files exported in compatible formats (DSM, FTM, VGM)
- Chiptune elements integrated with modern audio pipeline via FMOD
- Authenticity verified against reference hardware (where applicable)
- Chiptune tracks mixed to work alongside modern SFX

## Industry References

- Deflemask chiptune composition techniques
- Retro game audio analysis (NES, Genesis, Game Boy)
- Modern indie game chiptune integration (Shovel Knight, Celeste)
