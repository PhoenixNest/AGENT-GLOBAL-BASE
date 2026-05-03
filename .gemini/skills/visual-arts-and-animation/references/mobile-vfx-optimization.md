---
name: studio-art-mobile-vfx-optimization
description: Performance optimization of VFX for mobile platforms — particle count management, overdraw reduction, GPU profiling, and quality tier systems. Owned by Javier Moreno (VFX Artist). Use during Studio Pipeline Stages 5–6 for VFX performance tuning. Trigger: VFX optimization, mobile VFX, particle budget, overdraw reduction, GPU profiling, quality tiers, VFX performance.
version: "1.0.0"
---

# Mobile VFX Optimization

**Skill ID:** mobile-vfx-optimization
**Role:** VFX Artist
**Seniority:** Senior

## Overview

Performance optimization of VFX for mobile platforms — particle count management, overdraw reduction, GPU profiling, and quality tier systems.

## Tools & Frameworks

| Tool                   | Proficiency  | Use Case                          |
| ---------------------- | ------------ | --------------------------------- |
| Unity Profiler         | Expert       | VFX performance analysis          |
| RenderDoc              | Expert       | GPU frame debugging               |
| Frame Debugger         | Advanced     | Draw call analysis                |
| Custom profiling tools | Intermediate | VFX-specific performance tracking |

## Scenarios & Trade-offs

### Scenario 1: VFX Budget for 60fps on Mid-Range Device

- **Approach:** Profile each VFX individually, establish per-effect budgets (particle count, overdraw area, GPU time), enforce through review process
- **Trade-off:** Visual impact vs. performance budget — some effects must be simplified to maintain framerate
- **Quality Bar:** Total VFX GPU cost ≤ 3ms per frame; no single effect exceeds 1ms; 60fps maintained during peak VFX activity

### Scenario 2: Quality Tier System for VFX

- **Approach:** Design 3 quality tiers — High (full effects, 60fps devices), Medium (reduced particles, 30fps acceptable), Low (minimal effects, essential feedback only)
- **Trade-off:** Visual parity vs. device accessibility — low-end players get reduced visual experience
- **Quality Bar:** Core gameplay feedback preserved at all tiers; decorative effects are first to be reduced

## Quality Standards

- VFX GPU budget: ≤ 3ms per frame total
- Particle count budget: ≤ 500 active particles per scene
- Overdraw budget: ≤ 3x screen coverage for VFX
- All VFX tested on minimum spec device (Snapdragon 460 / A10 Fusion)
- Quality tier documentation for engineering implementation

## VFX–Audio Sync Handoff

Impact VFX and their paired SFX must be synchronized at the frame level — a mismatch of even 50ms between a visual hit and its sound destroys the sense of impact. Javier coordinates this with Kenji Takahashi (Audio Designer) through a structured handoff process.

- **Key impact frame marking:** For every VFX effect that has a perceptible impact moment (hit sparks, explosions, ability releases, reward pops), Javier marks the exact impact frame in the Unity Particle System or VFX Graph timeline and notes it in the VFX asset's metadata comment. Kenji uses this frame number to set the FMOD event trigger offset, ensuring the SFX peak aligns with the visual peak.
- **Joint review sessions:** Before each stage milestone (Stage 3 and Stage 5), Javier and Kenji run a joint audio-visual review session — playing every combat and feedback VFX with its paired SFX in-engine, on a physical device. The session produces a sync discrepancy list: each entry notes the effect name, the measured offset in milliseconds, and the responsible fix owner (animation offset in FMOD or VFX timeline shift).
- **Handoff format:** Javier maintains a shared spreadsheet row per impact VFX: `Effect Name | Impact Frame | Duration (ms) | Paired FMOD Event | Sync Status`. Kenji updates the Sync Status column after each fix cycle.

## Industry References

- Unity's mobile VFX optimization guide
- Supercell's VFX performance pipeline
- Google's Android game VFX best practices
