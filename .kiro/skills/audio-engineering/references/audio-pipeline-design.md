---
name: studio-audio-audio-pipeline-design
description: Audio production pipeline design for casual games — Stage 0 Audio Direction Brief, supervising the Audio Designer (Kenji Takahashi) with delegation RACI, DAW-to-middleware workflow, asset naming conventions, delivery specs, and Stage 6 automated testing gate sign-off. Owned by Hiroshi Nakamura. Trigger: audio pipeline, audio production, audio direction brief, audio supervisor, audio QA, DAW workflow, Western casual audio.
version: "1.0.0"
---

# Audio Pipeline Design

**Skill Owner:** Hiroshi Nakamura (Composer / Sound Director)
**Applies To:** Audio Production Workflow, Delivery Standards, FMOD Integration, Audio QA

## Audio Pipeline Stages

```
Stage 0 (Art Direction)
  └─► Audio Brief: Tone, mood, references, BPM ranges, instrumentation palette
                              │
Stage 1 (Concept)
  └─► Music design document: state list, system design, interaction spec
                              │
Stage 2 (Prototype)
  └─► Placeholder audio: temp tracks + placeholder SFX in FMOD
      Integration in Unity prototype build
      Creative Director review and approval
                              │
Stage 3 (Vertical Slice)
  └─► Final music for core loop + 3 SFX categories
      FMOD bank structure finalized
                              │
Stage 5 (Full Production)
  └─► All audio assets produced and integrated
      FMOD bank complete; all events named per convention
                              │
Stage 6 (Automated Testing) / Stage 7 (Soft Launch Prep)
  └─► Audio QA sign-off: Amara Osei runs audio regression tests
      Performance budget verified (CPU, memory, bank size)
```

## Asset Delivery Specification

### Source Files (Hiroshi's DAW — Logic Pro / Ableton)

| Asset Type  | Format   | Sample Rate | Bit Depth | Export Requirements                                                   |
| ----------- | -------- | ----------- | --------- | --------------------------------------------------------------------- |
| Music stems | WAV/AIFF | 44.1kHz     | 24-bit    | Exported per layer (stem export); loop points marked in file metadata |
| SFX sources | WAV      | 44.1kHz     | 24-bit    | Mono for positional SFX; Stereo for UI/music                          |
| VO          | WAV      | 44.1kHz     | 16-bit    | Mono; normalized to -3dBFS; silence trimmed                           |

### FMOD Studio Output (For Unity Integration)

| Asset Type | Format | Quality | Notes                                |
| ---------- | ------ | ------- | ------------------------------------ |
| Music      | Vorbis | 0.7     | Streamed from bank                   |
| SFX        | Vorbis | 0.5     | Loaded into memory; short clips only |
| VO         | Vorbis | 0.6     | Loaded on demand; individual bank    |

## Naming Convention (Studio Standard)

### Source File Naming

```
<type>_<category>_<name>_<variant>.<ext>

Examples:
  sfx_ui_button_tap_v1.wav
  sfx_gameplay_match3_combo_04.wav
  music_gameplay_core_loop_stem_percussion.wav
  vo_tutorial_narrator_line_01.wav
```

### FMOD Event Naming

See `fmod-wwise-integration.md` § Event Naming Convention.

## Supervising the Audio Designer (Kenji Takahashi)

Hiroshi has one direct report: Kenji Takahashi (Audio Designer). Their collaboration is the engine of the audio pipeline.

### Delegation RACI

| Audio Domain               | Hiroshi (Composer/Sound Director) | Kenji Takahashi (Audio Designer)            |
| -------------------------- | --------------------------------- | ------------------------------------------- |
| **Music composition**      | **Responsible + Accountable**     | Assists with integration                    |
| **SFX design**             | Direction + final approval        | **Responsible** (designs and implements)    |
| **VO direction**           | **Responsible + Accountable**     | Assists with asset management               |
| **FMOD/Wwise integration** | Architecture decisions + review   | **Responsible** (day-to-day implementation) |
| **Audio QA**               | Final sign-off                    | **Responsible** (runs QA checklist)         |
| **Stage 0-1 audio brief**  | **Responsible** (writes)          | Reviews for implementability                |

### Feedback Protocol

Hiroshi provides structured feedback on Kenji's SFX work:

- **Weekly SFX review (30 min):** Kenji presents SFX work-in-progress; Hiroshi gives directional feedback against the audio brief
- **Standard:** All feedback references the Stage 0 Audio Direction Brief — not subjective preference
- **Escalation:** If a SFX direction consistently misses the brief, Hiroshi and Kenji revisit the brief to determine whether the brief or the execution needs adjustment

## Stage 0 — Audio Direction Brief

The Audio Direction Brief is authored by Hiroshi at Stage 0, alongside the Creative Director's Style Guide. It is the creative specification that anchors all audio work for the project.

**Required Brief Contents:**

```markdown
# Audio Direction Brief — [Game Name]

**Date:** YYYY-MM-DD
**Composer/Sound Director:** Hiroshi Nakamura
**Creative Director:** Sakura Ishimori

## Game Audio Identity

[2 sentences: what should the audio feel like? Use sensory language, not technical language]
Example: "The audio should feel like a sunny summer afternoon — light, upbeat, never tense. Every sound rewards the player; nothing punishes."

## Music Direction

- Genre: [e.g. chiptune-inspired pop, lo-fi casual, upbeat orchestral]
- Reference tracks: [3-5 specific tracks that capture the target feel — cite artist + track]
- Tempo range: [BPM range for core gameplay loop, menu, event music]
- Instrumentation: [primary instruments/synths; what to avoid]
- Dynamic range: [how much should music change in intensity based on game state?]

## SFX Palette

- Register: [e.g. cartoon, realistic, stylized-retro]
- Key feels: [e.g. "satisfying, crunchy taps; gentle, airy level completion; celebratory but brief"]
- What to avoid: [e.g. "no harsh frequencies, no violent/aggressive sounds"]

## VO Direction (if applicable)

- Character voice archetypes: [per character]
- Delivery style: [e.g. warm and encouraging; playful and slightly sarcastic]

## Western Casual Audio Reference Touchstones

Casual games for a western audience have specific audio conventions. This brief aligns with:

- [Specific game reference + specific audio element] (e.g. "Candy Crush: short, distinct level-complete jingle — 2–3 notes, never long")
- [Second reference]
```

## Audio QA Checklist (Pre-Stage 6)

| Item                                     | Verified By                      | Pass Criteria                                              |
| ---------------------------------------- | -------------------------------- | ---------------------------------------------------------- |
| All events fire on correct game triggers | Kenji Takahashi (Audio Designer) | 100% of events in GDD fire correctly                       |
| No audible loop seams                    | Kenji + Hiroshi listen test      | 0 clicks/pops on 20 consecutive loops                      |
| All music states transition smoothly     | QA (Amara Osei team)             | No jarring cuts; transitions match spec                    |
| No audio memory or CPU budget exceedance | Amara Osei                       | Within performance budget (see `performance-profiling.md`) |
| FMOD bank size meets target              | Hiroshi                          | ≤10MB total audio banks                                    |
| All events follow naming convention      | Hiroshi                          | 100% compliance audit in FMOD Studio                       |

## Measurable Quality Standards

| Standard                                              | Target                                  | Measurement Method |
| ----------------------------------------------------- | --------------------------------------- | ------------------ |
| Audio QA sign-off by Stage 6 (Automated Testing gate) | 100% of events pass QA checklist        | QA report          |
| Source file organization                              | All in version control (Git LFS)        | Repository audit   |
| Delivery on schedule                                  | Audio assets available at Stage 5 start | Jira tracking      |
| FMOD bank rebuild time                                | ≤5 minutes                              | FMOD build log     |
