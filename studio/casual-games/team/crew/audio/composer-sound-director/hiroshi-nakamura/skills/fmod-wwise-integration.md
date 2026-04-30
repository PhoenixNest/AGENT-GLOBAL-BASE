---
name: studio-audio-fmod-wwise-integration
description: FMOD Studio and Wwise middleware integration in Unity for casual mobile games — event-based audio architecture, parameter-driven mixing, Unity Audio component replacement, and engine build optimization. Owned by Hiroshi Nakamura (Composer / Sound Director). Trigger: FMOD, Wwise, audio middleware, Unity audio, sound integration, audio events, audio parameters.
version: "1.0.0"
---

# FMOD / Wwise Integration

**Skill Owner:** Hiroshi Nakamura (Composer / Sound Director)
**Applies To:** Audio Middleware Setup, Event Architecture, Unity Integration, Audio Performance

## Studio Default: FMOD Studio

The Casual Games Studio defaults to **FMOD Studio** for audio middleware (preferred over Wwise for casual mobile games due to smaller SDK footprint and Unity package maturity). Wwise is used on projects that require its advanced spatial audio or console certification support.

## Tools & Frameworks

| Tool/Framework          | Version Context | Usage                                        |
| ----------------------- | --------------- | -------------------------------------------- |
| FMOD Studio             | 2.02+           | Audio content creation and event authoring   |
| FMOD Unity Integration  | 2.02+           | Runtime playback in Unity                    |
| Wwise                   | 2023.x          | Alternative middleware for specific projects |
| Unity                   | 6 LTS           | Game engine host                             |
| FMOD Bank Files (.bank) | N/A             | Packaged audio assets for delivery           |

## FMOD Event Architecture

### Event Naming Convention (Studio Standard)

```
<category>/<subcategory>/<name>

Examples:
  sfx/ui/button_tap
  sfx/gameplay/match_3_combo
  music/main/theme_loop
  music/meta/base_ambient
  vo/tutorial/narrator_line_01
```

### Parameter Design Principles

FMOD parameters drive adaptive audio behavior without requiring code changes:

| Parameter Type | Use Case Example                                                         |
| -------------- | ------------------------------------------------------------------------ |
| Game state     | `game_state` (0 = idle, 1 = gameplay, 2 = menu) — drives music intensity |
| Intensity      | `combo_intensity` (0.0–1.0) — crossfades between calm and excited layers |
| Danger/health  | `player_health` (0.0–1.0) — adds low-frequency rumble below 0.2          |
| Snapshot       | Pause snapshot reduces all non-UI audio by -12dB + adds low-pass filter  |

## Real-World Production Scenarios

### Scenario 1: Replacing Unity's Default Audio System with FMOD

**Context:** New Unity project; replacing Unity AudioSource with FMOD for the full audio pipeline.
**Process:**

1. Import FMOD Unity Integration package via UPM; disable Unity's built-in audio (`Project Settings → Audio → Disable Unity Audio`)
2. Set up FMOD Studio project alongside the Unity project; configure the bank output directory to `Assets/StreamingAssets/`
3. Define the Bank structure: one bank per major game module (Core, Gameplay, Meta, Music, UI)
4. Replace all `AudioSource.Play()` calls with `FMODUnity.RuntimeManager.PlayOneShot("event:/sfx/...")` or `RuntimeManager.CreateInstance` for events needing parameter control
5. Add `StudioListener` component to the main camera (replaces `AudioListener`)
6. Verify no Unity AudioSource components remain in the scene hierarchy

### Scenario 2: Implementing Adaptive Music with FMOD Parameters

**Context:** Core gameplay loop needs music that intensifies as the player builds a combo.
**Process:**

1. In FMOD Studio, create a `music/gameplay/core_loop` event with a multi-track timeline
2. Add a game parameter `combo_intensity` (0.0–1.0)
3. Map the parameter to track volume automation: base layer always at full volume; energy layer fades in from 0→1 as `combo_intensity` rises
4. From Unity, update the parameter each frame: `instance.setParameterByName("combo_intensity", normalizedComboValue)`
5. Transition should feel natural — add a short attack (0.3s) and release (1.0s) to the automation to avoid jarring snaps

### Scenario 3: Optimizing Audio Bank Size for Mobile

**Context:** FMOD banks add 22MB to APK size; target is ≤8MB.
**Process:**

1. In FMOD Studio, run the build report; identify the largest assets
2. Compress music tracks to Vorbis (q=0.6–0.8 for music, q=0.4 for SFX)
3. Reduce sample rate for SFX to 22kHz (music stays 44kHz)
4. Enable "Load on Demand" for rarely-played events; only Core and UI banks load at startup
5. Use FMOD's Bank Splitting to separate platform-specific content (Android vs. iOS audio profiles)

## Measurable Quality Standards

| Standard                       | Target                           | Measurement Method               |
| ------------------------------ | -------------------------------- | -------------------------------- |
| Total audio bank size (mobile) | ≤10MB                            | FMOD build report                |
| Audio CPU budget               | ≤5% of total frame CPU           | Unity Profiler audio thread      |
| Audio memory budget            | ≤15MB at runtime                 | Unity Memory Profiler            |
| Audio latency (SFX)            | ≤30ms from trigger to playback   | Device measurement (Android/iOS) |
| Event naming compliance        | 100% following studio convention | FMOD Studio asset audit          |
