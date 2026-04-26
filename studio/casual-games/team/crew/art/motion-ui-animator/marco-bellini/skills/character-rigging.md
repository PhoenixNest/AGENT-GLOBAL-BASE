---
name: studio-art-character-rigging
description: 2D skeletal rigging for casual game characters — bone hierarchy, weight painting, inverse kinematics, and performance-optimized rig structures for mobile. Owned by Marco Bellini (Motion/UI Animator). Use during Studio Pipeline Stages 3–5 for character rig production. Trigger: character rigging, 2D rigging, Spine 2D, bone hierarchy, weight painting, IK, mobile rig optimization.
version: "1.0.0"
---

# Character Rigging

**Skill ID:** character-rigging
**Role:** Motion/UI Animator
**Seniority:** Senior

## Overview

2D skeletal rigging for casual game characters — bone hierarchy, weight painting, inverse kinematics, and performance-optimized rig structures for mobile.

## Tools & Frameworks

| Tool               | Proficiency | Use Case                                |
| ------------------ | ----------- | --------------------------------------- |
| Spine 2D           | Expert      | Primary rigging tool for 2D characters  |
| Unity 2D Animation | Advanced    | In-engine rig verification and tweaking |
| Photoshop          | Advanced    | Character art preparation for rigging   |

## Scenarios & Trade-offs

### Scenario 1: 20-Character Rig Library

- **Approach:** Create modular rig templates (humanoid, quadruped, blob, mechanical) that can be adapted to specific characters
- **Trade-off:** Template generality vs. character specificity — templates save time but may not fit unique proportions
- **Quality Bar:** All rigs support idle, walk, attack, death, and victory animations; bone count ≤ 30 per character

### Scenario 2: Mobile Performance Optimization

- **Approach:** Limit bone count, use texture atlases for character parts, implement LOD rigs (detailed for close-up, simplified for distant)
- **Trade-off:** Animation quality vs. CPU budget — more bones = smoother animation but higher CPU cost
- **Quality Bar:** Animation CPU cost ≤ 2ms per frame on mid-range device; bone count ≤ 30 for main characters, ≤ 15 for NPCs

## Quality Standards

- All rigs delivered with animation state machine documentation
- Bone hierarchy documented with parent-child relationships
- Weight painting reviewed for smooth deformation at joints
- Rig file size ≤ 500KB per character (including textures)

## Industry References

- Supercell's 2D character rigging pipeline
- King's modular rig template system
- Spine 2D best practices for mobile games
