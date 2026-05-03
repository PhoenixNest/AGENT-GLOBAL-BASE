---
name: studio-art-environment-art
description: 3D environment art for mobile games — scene composition, spatial storytelling, modular environment design, and mobile performance optimization. Owned by Anya Petrova (3D Artist). Use during Studio Pipeline Stages 0, 2, 3, and 5 for environment production. Trigger: environment art, modular design, spatial storytelling, scene composition, terrain generation, mobile environments, environment optimization.
version: "1.0.0"
---

# Environment Art

**Skill ID:** environment-art
**Role:** 3D Artist
**Seniority:** Senior

## Overview

3D environment art for mobile games — scene composition, spatial storytelling, modular environment design, and mobile performance optimization.

## Tools & Frameworks

| Tool               | Proficiency | Use Case                          |
| ------------------ | ----------- | --------------------------------- |
| Maya               | Expert      | Environment modeling              |
| Substance Painter  | Expert      | Environment texturing             |
| World Machine/Gaea | Advanced    | Terrain generation                |
| Unity              | Advanced    | Environment assembly and lighting |

## Stage 0 — Environment Direction Contribution

Anya's involvement at Stage 0 (Art Direction) is focused on feeding the environment dimension of the Art Style Guide. Renaud Leclercq (Art Director) owns the final Style Guide, but Anya is the primary contributor to its environment-specific content.

- **Hero environment concept sketches:** Anya produces 3–5 hero-level environment concept sketches exploring the game's possible visual worlds — covering architectural language, natural forms, scale relationships, and the visual boundary between foreground play space and background staging. These are presented to the Art Director at the Stage 0 review; one direction (or a synthesized hybrid) is selected for further development.
- **Environment mood reference sets:** Anya assembles curated reference boards per candidate environment theme — pulling from photography, illustration, and comparable games — to communicate lighting mood, color temperature, atmosphere density, and material palette. Reference sets accompany the hero sketches at the Art Director review.
- **Biome/world palette candidates:** Anya defines 2–3 candidate color palettes for the environment layer (sky, ground, foliage/structure, accent details) and maps them against Elena Morozova's UI color proposals to verify they do not conflict. The approved environment palette is recorded in the Art Style Guide and becomes the reference Anya works from at Stages 2, 3, and 5.

## Scenarios & Trade-offs

### Scenario 1: Modular Environment Kit

- **Approach:** Design modular pieces (walls, floors, corners, doors, windows) that snap together to create varied environments
- **Trade-off:** Modularity vs. uniqueness — modular pieces can feel repetitive without variation sets
- **Quality Bar:** ≥ 20 modular pieces per environment theme; seamless connections; varied enough for 50+ unique layouts

### Scenario 2: Spatial Storytelling Through Environment

- **Approach:** Use environmental details (wear patterns, object placement, lighting) to communicate narrative without text
- **Trade-off:** Environmental detail vs. performance budget — every detail costs triangles and texture memory
- **Quality Bar:** Players can infer story/setting from environment alone; details are performant (baked into textures where possible)

## Quality Standards

- Environment pieces use consistent modular grid system
- Texture atlasing for small environment details
- LOD systems for large environment pieces
- Draw call budget per environment scene: ≤ 50
- All environment art supports the game's established art style

## Industry References

- Unity's modular environment design patterns
- Supercell's environment art approach for mobile
- GDC talks on mobile environment optimization
