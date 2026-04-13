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

## Industry References

- Unity's mobile VFX optimization guide
- Supercell's VFX performance pipeline
- Google's Android game VFX best practices
