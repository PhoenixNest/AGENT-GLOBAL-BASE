---
name: studio-art-pbr-texturing
description: Physically-Based Rendering texturing for mobile games — material authoring, texture map creation, mobile-optimized PBR workflows, and ASTC compression. Owned by Tomasz Kowalski (3D Artist). Use during Studio Pipeline Stages 3–5 for PBR texture production. Trigger: PBR texturing, Substance Painter, material authoring, texture maps, ORM packing, mobile PBR, stylized PBR.
version: "1.0.0"
---

# PBR Texturing

**Skill ID:** pbr-texturing
**Role:** 3D Artist
**Seniority:** Senior

## Overview

Physically-Based Rendering texturing for mobile games — material authoring, texture map creation, mobile-optimized PBR workflows.

## Tools & Frameworks

| Tool               | Proficiency  | Use Case                       |
| ------------------ | ------------ | ------------------------------ |
| Substance Painter  | Expert       | Primary texturing tool         |
| Substance Designer | Advanced     | Procedural material creation   |
| Quixel Mixer       | Intermediate | Alternative texturing workflow |
| Photoshop          | Advanced     | Texture editing, mask creation |

## Scenarios & Trade-offs

### Scenario 1: Mobile PBR Texture Budget

- **Approach:** Use 1024×1024 textures for hero assets, 512×512 for standard assets, 256×256 for props; pack maps efficiently (ORM in RGB)
- **Trade-off:** Texture resolution vs. memory budget — higher resolution looks better but increases VRAM usage
- **Quality Bar:** Textures look sharp at camera distance; no visible pixelation; total texture memory per character ≤ 8MB

### Scenario 2: Stylized PBR vs. Traditional Hand-Painted

- **Approach:** Hybrid approach — PBR base materials with hand-painted detail overlays for stylized look
- **Trade-off:** Physical accuracy vs. artistic style — stylized games may intentionally break PBR rules
- **Quality Bar:** Consistent visual style across all assets; materials read correctly under game lighting

## Quality Standards

- Texture maps: Albedo, Normal, Metallic, Roughness, AO (packed as ORM)
- Texture resolution matched to asset importance and screen coverage
- Seamless tiling for repeated surfaces
- Consistent material language across all assets
- Texture compression: ASTC 4×4 or 6×6 for mobile

## Industry References

- Substance Painter mobile game texturing workflows
- Unity's URP PBR material guidelines
- Supercell's stylized texturing approach
