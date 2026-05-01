---
name: studio-audio-interactive-music-systems
description: Interactive music system design for casual mobile games — horizontal re-sequencing, vertical layering, state-driven transitions, and looping structures that respond dynamically to gameplay without perceptible seams. Owned by Hiroshi Nakamura (Composer / Sound Director). Trigger: interactive music, adaptive music, music system, dynamic music, horizontal re-sequencing, vertical layering, music transitions.
version: "1.0.0"
---

# Interactive Music Systems

**Skill Owner:** Hiroshi Nakamura (Composer / Sound Director)
**Applies To:** Music Composition, FMOD/Wwise Event Design, Adaptive Audio Architecture

## Interactive Music Techniques

### 1. Vertical Layering (Additive/Subtractive)

Multiple synchronized tracks play simultaneously; layers are added or removed based on game state:

```
Layer A (Base):   [Always playing — low energy, sparse instrumentation]
Layer B (Mid):    [Fades in when player enters core gameplay]
Layer C (Intense):  [Fades in at high combo or critical moment]
Layer D (Victory):  [Solo layer plays on level complete]
```

**When to use:** Gameplay intensity changes are gradual and continuous (health meter, combo counter, timer urgency).

**Composition requirement:** All layers must be written to sound musical in any combination (harmonic compatibility is critical — a layer that sounds good alone but creates dissonance when combined is unusable).

### 2. Horizontal Re-Sequencing

Musical segments are arranged in sequences; the system chooses the next segment based on game state at a defined "transition point" (usually a bar or beat boundary):

```
[Intro] → [Main Loop A] ↔ [Main Loop B]
               ↕
           [Tension Sting] → [Resolution] → [Main Loop A or B]
               ↕
           [Boss/Challenge Theme]
```

**When to use:** Discrete game states (safe → combat → win → loss) where music must change character meaningfully.

**Composition requirement:** All segments that can transition to each other must be written in compatible keys and tempos. Hitpoint transitions (bar-sync) must be specified for each segment pair.

### 3. State-Driven Music

A single game parameter maps to a musical state:

| State Value  | Musical State   | Transition Type     |
| ------------ | --------------- | ------------------- |
| 0 = Menu     | Relaxed theme   | Immediate crossfade |
| 1 = Gameplay | Core loop theme | 1-bar sync          |
| 2 = Critical | Tension theme   | Immediate           |
| 3 = Victory  | Win fanfare     | Immediate           |
| 4 = Defeat   | Loss sting      | Immediate           |

## Real-World Production Scenarios

### Scenario 1: Designing the Music System for a Match-3 Core Loop

**Context:** Stage 2 (Prototype); designing the music experience for the first playable.
**Process:**

1. Define game states that need distinct music: idle menu, active gameplay, combo/high intensity, time pressure, level complete, level fail
2. Choose technique: vertical layering for gameplay intensity changes; state-driven transitions for win/fail
3. Compose a base theme (60–90 BPM, friendly and upbeat for casual audience) with 3 vertical layers
4. Prototype in FMOD Studio using placeholder audio; test transitions with Dmitri's prototype build
5. Iterate on composition based on feel in-engine — music that sounds great in isolation often needs adjustment in gameplay context

### Scenario 2: Ensuring Seamless Looping

**Context:** A gameplay music loop has an audible "click" at the loop point on mobile devices.
**Process:**

1. Check the loop start and end points in FMOD Studio — they must align to exact zero-crossings
2. If the loop has a reverb tail, fade the tail into silence 0.5s before the loop point; blend with the attack at the loop start
3. In Unity/FMOD, confirm the loop is configured as "Loop Mode: Loop" at the event level, not via `setParameterByName`
4. Test on both Android (low-latency audio via OpenSL ES / AAudio) and iOS (Core Audio)
5. Common iOS issue: buffer underrun on old devices causes a gap — increase FMOD DSP buffer size as a fallback

## Measurable Quality Standards

| Standard                       | Target                                                        | Measurement Method               |
| ------------------------------ | ------------------------------------------------------------- | -------------------------------- |
| Loop seam audibility           | 0 audible clicks/pops                                         | QA listen test (10 listeners)    |
| Music state transition latency | ≤100ms for immediate transitions; ≤1 bar for sync transitions | In-engine measurement            |
| Vertical layer harmonic issues | 0 (all layers sound musical in all combinations)              | Composer review + QA listen test |
| Music system coverage          | All defined game states have music                            | State audit against GDD          |
