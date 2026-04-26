---
name: studio-art-particle-systems
description: Particle system creation for mobile games — Unity Particle System, custom VFX, combat effects, environmental effects, and mobile performance optimization. Owned by Javier Moreno (VFX Artist). Use during Studio Pipeline Stages 3–5 for particle effect production. Trigger: particle systems, VFX, combat effects, environmental particles, Unity Particle System, VFX Graph, mobile VFX.
version: "1.0.0"
---

# Particle Systems

**Skill ID:** particle-systems
**Role:** VFX Artist
**Seniority:** Senior

## Overview

Particle system creation for mobile games — Unity Particle System, custom VFX, combat effects, environmental effects, and mobile performance optimization.

## Tools & Frameworks

| Tool                  | Proficiency | Use Case                                       |
| --------------------- | ----------- | ---------------------------------------------- |
| Unity Particle System | Expert      | Primary particle effect creation               |
| VFX Graph             | Advanced    | GPU-based particle effects for complex systems |
| Substance Designer    | Advanced    | Particle texture creation                      |
| Shader Graph          | Advanced    | Custom particle shaders                        |

## Scenarios & Trade-offs

### Scenario 1: Combat VFX System (150+ Effects)

- **Approach:** Build reusable particle templates (impact, trail, aura, explosion) with parameter variations for different abilities
- **Trade-off:** Visual variety vs. production efficiency — unique effects per ability vs. template variations
- **Quality Bar:** Each effect reads clearly at mobile screen sizes; particle count ≤ 200 per effect; no overdraw issues

### Scenario 2: Environmental Particle Effects

- **Approach:** Create ambient particle systems (dust, leaves, fireflies, rain) that enhance atmosphere without distracting from gameplay
- **Trade-off:** Atmosphere vs. performance — ambient effects must be subtle and performant
- **Quality Bar:** Environmental effects add to mood without drawing attention away from core gameplay; ≤ 50 particles active at any time

## Quality Standards

- Particle count budget: ≤ 200 per effect, ≤ 500 per scene
- Texture size: 128×128 or 256×256 for particle textures
- Overdraw management: particle effects optimized to minimize fill rate impact
- All effects tested on mid-range devices (Snapdragon 730 / A12 Bionic)
- Effects documented with spawn conditions, duration, and cleanup behavior

## Industry References

- Unity's particle system best practices for mobile
- Riot Games' VFX design principles (clarity, readability, feedback)
- Supercell's combat VFX approach for mobile
