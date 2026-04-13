# Prop Modeling

**Skill ID:** prop-modeling
**Role:** 3D Artist
**Seniority:** Senior

## Overview

3D prop modeling for mobile games — rapid production pipeline, UV mapping, texturing, and mobile optimization for small-to-medium assets.

## Tools & Frameworks

| Tool              | Proficiency  | Use Case                                |
| ----------------- | ------------ | --------------------------------------- |
| Maya              | Expert       | Prop modeling and UV layout             |
| Substance Painter | Expert       | Prop texturing                          |
| ZBrush            | Intermediate | High-detail sculpting for complex props |
| Unity             | Intermediate | In-engine prop verification             |

## Scenarios & Trade-offs

### Scenario 1: 200 Props in 3 Months

- **Approach:** Establish prop templates (crates, barrels, plants, rocks, furniture), batch-produce variations using texture swaps and scale changes
- **Trade-off:** Production speed vs. individual uniqueness — templates ensure consistency but may feel repetitive
- **Quality Bar:** All props match established art style; ≤ 2K triangles each; 512×512 or 256×256 textures

### Scenario 2: Prop UV Efficiency

- **Approach:** Use shared UV layouts for prop families (all crates share one UV template); pack multiple small props onto single texture atlas
- **Trade-off:** UV flexibility vs. texture efficiency — shared UVs save texture memory but limit per-prop variation
- **Quality Bar:** Texel density consistent across all props; no wasted UV space; texture atlases organized by material type

## Quality Standards

- Prop triangle budget: ≤ 2K for standard props, ≤ 5K for hero props
- Texture resolution: 256×256 for small props, 512×512 for medium props
- Clean UV layouts with minimal stretching
- Props designed for reuse across multiple levels/environments
- Naming convention: `prop_{category}_{name}_{variant}`

## Industry References

- Unity's prop modeling best practices
- Mobile game asset production pipelines
- Modular prop design patterns
