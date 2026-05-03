---
name: studio-art-character-modeling
description: 3D character modeling for mobile games — anatomy, topology, stylized and realistic styles, rigging preparation, and mobile polycount budgets. Owned by Tomasz Kowalski (3D Artist). Use during Studio Pipeline Stages 0, 2, 3, and 5 for character model production. Trigger: character modeling, 3D characters, topology, retopology, ZBrush sculpting, mobile polycount, stylized characters, rigging prep.
version: "1.0.0"
---

# Character Modeling

**Skill ID:** character-modeling
**Role:** 3D Artist
**Seniority:** Senior

## Overview

3D character modeling for mobile games — anatomy, topology, stylized and realistic styles, rigging preparation, and mobile polycount budgets.

## Tools & Frameworks

| Tool               | Proficiency  | Use Case                                |
| ------------------ | ------------ | --------------------------------------- |
| Maya               | Expert       | Primary modeling and rigging            |
| ZBrush             | Expert       | High-poly sculpting, detail work        |
| Substance Painter  | Expert       | PBR texturing, material authoring       |
| Marvelous Designer | Advanced     | Cloth simulation for character clothing |
| Unity              | Intermediate | In-engine model verification            |

## Stage 0 — Character Direction Contribution

Tomasz's contribution at Stage 0 (Art Direction) establishes the character design language that feeds the Art Style Guide. Renaud Leclercq (Art Director) owns the final Style Guide; Tomasz is the primary contributor to its character design dimension.

- **Character silhouette explorations:** Tomasz produces 10–15 silhouette thumbnails — a mix of hero, support, and NPC character archetypes — to explore the range of body proportions, shape language, and personality the game's roster can express. Silhouettes are presented in greyscale only; color is not introduced until the Art Director selects a proportion and shape direction.
- **Character proportion and style reference:** Tomasz assembles a proportion reference sheet comparing head-to-body ratio options (2:1 chibi through 6:1 near-realistic) and maps each against the game's tonal brief. He also curates a style reference board drawing from comparable casual games, illustration, and animation to anchor the team's vocabulary.
- **Style Guide character section:** Once the Art Director selects a direction, Tomasz produces the character section of the Art Style Guide: a model sheet showing front/side/back views of a representative hero character at the approved proportion; a palette swatch set for skin tones, clothing, and accessory categories; and a list of "character design rules" (e.g., maximum accessory complexity, silhouette clarity requirement, polygon budget class). All subsequent character production at Stages 2, 3, and 5 references this section.

## Scenarios & Trade-offs

### Scenario 1: Mobile Character Under 15K Triangles

- **Approach:** Start with high-poly sculpt in ZBrush, retopologize in Maya for clean edge flow, optimize for animation deformation zones
- **Trade-off:** Visual fidelity vs. triangle budget — focus detail on face/hands (high visibility), simplify torso/legs
- **Quality Bar:** Character recognizable and expressive at 15K triangles; clean topology for animation; no pinching or stretching

### Scenario 2: Stylized vs. Realistic Character Pipeline

- **Approach:** Stylized characters use hand-painted textures with simplified shading; realistic use full PBR workflow
- **Trade-off:** Production time vs. visual target — stylized can be faster but requires strong artistic judgment
- **Quality Bar:** Style consistent across all characters; meets Art Director's visual pillar definition

## Quality Standards

- All characters delivered with clean quad-dominant topology
- Edge loops follow animation deformation zones (joints, face)
- UV layouts with consistent texel density (≥ 512px per meter for main characters)
- Triangle budget: ≤ 15K for main characters, ≤ 5K for NPCs, ≤ 2K for background characters
- Normal maps baked from high-poly to low-poly with no artifacts

## Industry References

- Supercell's stylized character modeling pipeline
- Riot Games' mobile character optimization techniques
- Unity's mobile character best practices
