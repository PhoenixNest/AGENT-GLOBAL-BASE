---
name: studio-art-mobile-3d-optimization
description: Optimization of 3D assets for mobile platforms — polycount budgeting, texture compression, LOD systems, draw call reduction, and memory management. Owned by Tomasz Kowalski (3D Artist). Use during Studio Pipeline Stages 5–6 for 3D performance optimization. Trigger: 3D optimization, polycount budget, LOD system, draw call reduction, texture compression, mobile 3D, GPU instancing.
version: "1.0.0"
---

# Mobile 3D Optimization

**Skill ID:** mobile-3d-optimization
**Role:** 3D Artist
**Seniority:** Senior

## Overview

Optimization of 3D assets for mobile platforms — polycount budgeting, texture compression, LOD systems, draw call reduction, and memory management.

## Tools & Frameworks

| Tool           | Proficiency  | Use Case                     |
| -------------- | ------------ | ---------------------------- |
| Unity Profiler | Advanced     | Runtime performance analysis |
| RenderDoc      | Intermediate | GPU frame debugging          |
| Simplygon      | Advanced     | Automated LOD generation     |
| TexturePacker  | Intermediate | Texture atlas optimization   |

## Scenarios & Trade-offs

### Scenario 1: Scene with 50 Assets Under 100 Draw Calls

- **Approach:** Combine static meshes, use texture atlasing, implement GPU instancing for repeated objects, merge materials where possible
- **Trade-off:** Asset flexibility vs. draw call count — combined meshes are harder to update individually
- **Quality Bar:** ≤ 100 draw calls for entire scene; 60fps maintained on mid-range device

### Scenario 2: LOD System for Mobile

- **Approach:** Create 3 LOD levels per asset (LOD0: full detail, LOD1: 50% triangles, LOD2: 25% triangles); use distance-based switching
- **Trade-off:** Visual pop-in vs. performance — aggressive LOD switching saves performance but may be noticeable
- **Quality Bar:** LOD transitions are smooth (crossfade or dithered); triangle reduction ≥ 60% from LOD0 to LOD2

## Quality Standards

- Triangle budget per scene documented and enforced
- Texture memory budget per scene: ≤ 50MB
- Draw call budget per scene: ≤ 100
- All assets have LODs where screen coverage justifies them
- Mobile-specific optimizations: vertex color usage, lightmap atlasing, occlusion culling support

## Industry References

- Unity's mobile optimization guide
- Supercell's mobile 3D performance pipeline
- Google's Android game performance best practices
