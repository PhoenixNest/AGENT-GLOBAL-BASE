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
