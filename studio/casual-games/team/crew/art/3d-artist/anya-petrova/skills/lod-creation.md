---
name: studio-art-lod-creation
description: Level of Detail (LOD) creation for mobile games — automated and manual LOD generation, transition management, and performance optimization. Owned by Anya Petrova (3D Artist). Use during Studio Pipeline Stages 5–6 for LOD production and optimization. Trigger: LOD creation, level of detail, Simplygon, LOD generation, LOD transitions, performance optimization, mesh simplification.
version: "1.0.0"
---

# LOD Creation

**Skill ID:** lod-creation
**Role:** 3D Artist
**Seniority:** Senior

## Overview

Level of Detail (LOD) creation for mobile games — automated and manual LOD generation, transition management, and performance optimization.

## Tools & Frameworks

| Tool            | Proficiency  | Use Case                         |
| --------------- | ------------ | -------------------------------- |
| Simplygon       | Expert       | Automated LOD generation         |
| Maya            | Expert       | Manual LOD refinement            |
| Unity LOD Group | Advanced     | In-engine LOD configuration      |
| RenderDoc       | Intermediate | Verifying LOD performance impact |

## Scenarios & Trade-offs

### Scenario 1: LOD System for 100+ Assets

- **Approach:** Use Simplygon for initial LOD generation, manually refine problematic assets, configure LOD distances based on camera behavior
- **Trade-off:** Automation speed vs. quality — automated LODs may have artifacts requiring manual cleanup
- **Quality Bar:** LOD transitions are visually smooth; triangle reduction ≥ 60% from LOD0 to LOD2; no visible popping

### Scenario 2: LOD Distance Configuration

- **Approach:** Set LOD switch distances based on asset screen coverage — large assets switch closer, small assets switch farther
- **Trade-off:** Performance vs. visual quality — closer switches look better but cost more performance
- **Quality Bar:** LOD switches are not noticeable during normal camera movement; performance budget met at all camera distances

## Quality Standards

- 3 LOD levels per asset (LOD0: 100%, LOD1: 50%, LOD2: 25% triangle count)
- LOD transitions use crossfade or dithering (not hard switch)
- LOD distances configured per asset based on screen coverage
- Billboard impostors for very distant assets where appropriate
- LOD performance impact documented per scene

## Industry References

- Simplygon mobile game LOD workflows
- Unity's LOD Group best practices
- Supercell's LOD optimization pipeline
