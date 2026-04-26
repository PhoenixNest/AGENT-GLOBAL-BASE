---
name: studio-art-shader-vfx
description: Shader-based visual effects for mobile games — custom HLSL shaders, screen-space effects, distortion, dissolve, and performance-aware shader design. Owned by Javier Moreno (VFX Artist). Use during Studio Pipeline Stages 3–5 for VFX creation and shader optimization. Trigger: shader VFX, HLSL, screen-space effects, distortion, dissolve effect, mobile shader, shader optimization.
version: "1.0.0"
---

# Shader VFX

**Skill ID:** shader-vfx
**Role:** VFX Artist
**Seniority:** Senior

## Overview

Shader-based visual effects for mobile games — custom HLSL shaders, screen-space effects, distortion, dissolve, and performance-aware shader design.

## Tools & Frameworks

| Tool         | Proficiency | Use Case                            |
| ------------ | ----------- | ----------------------------------- |
| HLSL         | Expert      | Custom shader programming           |
| Shader Graph | Expert      | Node-based shader creation          |
| Unity URP    | Advanced    | Mobile-optimized rendering pipeline |
| RenderDoc    | Advanced    | GPU debugging and optimization      |

## Scenarios & Trade-offs

### Scenario 1: Dissolve Effect for Character Death

- **Approach:** Custom shader with noise-based dissolve, edge glow, and particle emission at dissolve boundary
- **Trade-off:** Visual quality vs. shader complexity — more instructions = higher GPU cost
- **Quality Bar:** Dissolve looks organic and polished; shader instruction count ≤ 64; runs at 60fps on mid-range device

### Scenario 2: Screen-Space Distortion for Impact Effects

- **Approach:** Post-processing distortion effect triggered on hit, with radial falloff and quick decay
- **Trade-off:** Screen-space quality vs. fill rate cost — full-screen effects are expensive on mobile
- **Quality Bar:** Distortion is noticeable but not overwhelming; GPU cost ≤ 1ms per frame; limited to 50% screen area

## Quality Standards

- All custom shaders optimized for mobile (≤ 64 instructions)
- Shader variants minimized through material property blocks
- Screen-space effects limited to necessary screen area
- All shaders tested with Unity's shader analysis tools
- Fallback shaders provided for devices that don't support required features

## Industry References

- Unity URP shader optimization guide
- Mobile game shader best practices
- GPU optimization techniques for real-time VFX
