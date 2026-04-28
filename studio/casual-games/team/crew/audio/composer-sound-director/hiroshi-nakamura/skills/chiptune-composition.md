---
name: studio-audio-chiptune-composition
description: Chiptune music composition and interactive audio system design for casual games — Deflemask/FamiTrack production, FMOD integration, and adaptive music systems. Owned by Hiroshi Nakamura (Composer / Sound Director). Use during Studio Pipeline Stages 3–5 for music composition and audio system setup. Trigger: chiptune composition, interactive music, FMOD, Deflemask, FamiTrack, game music, adaptive audio, NES chiptune.
version: "1.0.0"
---

# Chiptune Composition

**Skill Owner:** Hiroshi Nakamura (Composer / Sound Director)
**Applies To:** Chiptune Music Composition, Deflemask/FamiTrack Production, Game Audio Direction

## Tools & Frameworks

| Tool/Framework | Version Context | Usage                                 |
| -------------- | --------------- | ------------------------------------- |
| Deflemask      | 0.12.1+         | Chiptune composition (multi-system)   |
| FamiTracker    | 0.5.0+          | NES/Famicom chiptune composition      |
| FL Studio      | 21.2+           | DAW for mixing, mastering, production |
| FMOD Studio    | 2.02.18+        | Audio middleware integration          |
| Wwise          | 2024.1+         | Audio middleware integration          |
| Unity Audio    | 2024 LTS+       | Engine-level audio integration        |
| Audacity       | 3.4+            | Audio editing, cleanup                |

## Real-World Production Scenarios

### Scenario 1: Composing Original Chiptune Score for a Casual Game

**Context:** Need original music that fits a cozy, retro-inspired casual game.
**Process:**

1. Define audio direction: warm chiptune sounds, nostalgic but not dated, accessible to casual audience
2. Compose main themes: title screen (upbeat, welcoming), gameplay (looping, non-intrusive), victory (celebratory), defeat (encouraging)
3. Create variations: each theme has 2-3 variations for extended play sessions to prevent listener fatigue
4. Export stems: separate channels for FM, pulse, triangle, noise, DPCM (NES-style)
5. Integrate with FMOD: set up interactive music system that transitions between states based on gameplay
6. Test in-engine: verify music doesn't compete with SFX, volume levels appropriate for mobile speakers
7. Results: 15 original tracks, seamless interactive transitions, positive player feedback on audio

### Scenario 2: Setting Up Interactive Music System

**Context:** Music should respond dynamically to player actions and game state.
**Process:**

1. Design music states: idle, active gameplay, tense (time running out), victory, defeat
2. Define transitions: smooth crossfades between states, no abrupt cuts
3. Implement in FMOD: use parameters (game state, player score, time remaining) to control music
4. Test transitions: verify smooth crossfades, appropriate timing, no audio artifacts
5. Optimize for mobile: reduce concurrent voice count, use compressed audio formats
6. Results: interactive music system that enhances player engagement without distraction

## Trade-Off Analysis

| Decision          | Option A                                 | Option B                                      | Trade-Off                                                                                         |
| ----------------- | ---------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Composition Style | Authentic NES-style (4 channels + noise) | Modern chiptune (hybrid with modern elements) | Authentic = nostalgic but limited; Modern = broader appeal but less authentic                     |
| Audio Format      | Uncompressed WAV                         | Compressed Vorbis/ADPCM                       | Uncompressed = best quality but large files; Compressed = 80% smaller with acceptable quality     |
| Music System      | Simple looping tracks                    | Interactive adaptive music                    | Simple = easy to implement but static; Interactive = engaging but complex to design and implement |

## Measurable Quality Standards

| Standard                    | Target                    | Measurement Method         |
| --------------------------- | ------------------------- | -------------------------- |
| Track Count                 | ≥ 15 original tracks      | Music delivery checklist   |
| Audio Quality               | ≥ 44.1kHz, 16-bit minimum | Audio file analysis        |
| Interactive Transition Time | ≤ 2 seconds crossfade     | FMOD profiler              |
| File Size (all music)       | ≤ 50MB total              | Build size analysis        |
| Player Feedback             | ≥ 4.0/5.0 audio rating    | Post-launch player surveys |

## Industry Best Practice References

- **Inti Creates Audio Pipeline** — Industry-standard chiptune game audio
- **GDC: "Chiptune Music in Modern Games"** — Multiple talks on retro audio design
- **FMOD Studio Documentation** — Official interactive audio middleware guide
- **Bandcamp Chiptune Community** — Independent chiptune artist community standards
