---
name: studio-art-game-ui-art
description: Complete ownership of static game UI visual assets — icons, illustrations, button states, typography, store screenshots, and promotional art with mobile-first optimization. Owned by Elena Morozova (UI Visual Artist). Use during Studio Pipeline Stages 0, 1, and 2–5 for UI art production. Trigger: game UI art, UI assets, button states, typography, store screenshots, promotional art, UI design system.
version: "1.0.0"
---

# Game UI Art

**Skill ID:** game-ui-art
**Role:** UI Visual Artist
**Seniority:** Senior

## Overview

Complete ownership of static game UI visual assets — icons, illustrations, button states, typography, store screenshots, and promotional art. Requires design-system thinking and mobile-first optimization.

## Tools & Frameworks

| Tool            | Proficiency  | Use Case                                       |
| --------------- | ------------ | ---------------------------------------------- |
| Figma           | Expert       | UI layout, design system, component libraries  |
| Photoshop       | Expert       | Icon creation, illustration, asset polish      |
| Illustrator     | Advanced     | Vector icon work, typography, logo design      |
| Unity UI (UGUI) | Intermediate | Understanding how assets integrate into engine |
| TexturePacker   | Intermediate | Sprite atlas optimization for mobile delivery  |

## Stage 0–1 — UI Style Guide Contribution

Elena's involvement begins at Stage 0 (Art Direction), well before any production UI assets are created. Her role at this stage feeds directly into the Art Style Guide owned by Renaud Leclercq (Art Director).

**Stage 0 — Art Direction:**

- **UI reference moodboards:** Elena assembles curated moodboards presenting 3–5 distinct UI visual directions — covering color temperature, visual weight, border/frame treatment, and button personality. These are reference materials, not final designs.
- **Color system candidates:** Elena proposes 2–3 candidate color systems (primary palette, accent colors, state colors for interactive elements) with contrast ratios validated against WCAG AA. The Art Director selects or synthesizes one direction.
- **Icon style exploration:** Elena creates 10–15 icon sketches across 2–3 style approaches (flat, outlined, illustrated) to define the icon vocabulary that will guide the full icon set. The chosen style is locked into the Art Style Guide.

**Stage 1 — Concept:**

- **UI mood reference sheets:** Elena produces a consolidated one-page reference sheet per major screen type (main menu, gameplay HUD, shop, reward screen) showing the approved style applied to rough wireframes. These are not polished — they communicate the visual intention to the team.
- **Initial color palette proposal:** Elena formalizes the color system candidate chosen at Stage 0 into a documented palette with hex values, usage rules (primary / secondary / state / feedback), and dark-mode variants if applicable.

## Scenarios & Trade-offs

### Scenario 1: Icon Set Design for 200+ Game Items

- **Approach:** Establish grid system, define detail levels by item rarity, create master templates, batch-produce with variations
- **Trade-off:** Consistency vs. uniqueness — rare items need more visual distinction but must fit the same grid
- **Quality Bar:** All icons readable at 48×48px on mobile; consistent stroke weight; clear rarity differentiation

### Scenario 2: Button State Library

- **Approach:** Design 5-state system (normal, hover, pressed, disabled, locked) using 9-slice scalable components
- **Trade-off:** Visual richness vs. texture memory budget — each state adds to atlas size
- **Quality Bar:** States distinguishable at glance; pressed state provides clear tactile feedback visually; disabled state communicates unavailability without confusion

### Scenario 3: Typography Hierarchy for Mobile

- **Approach:** Define 4–5 type sizes with clear hierarchy; test legibility at minimum device resolution (320px width)
- **Trade-off:** Font personality vs. readability — decorative fonts for headers, clean sans-serif for body
- **Quality Bar:** All text legible at 10pt minimum on 5-inch screen; contrast ratio ≥ 4.5:1 for body text

## Quality Standards

- All assets delivered in platform-optimized formats (PNG-8 for indexed, PNG-24 for gradients)
- Texture atlases organized by screen/context to minimize memory waste
- Design system documented with component specs for engineering handoff
- All UI art supports text expansion tolerance (+30% for localization)

## Industry References

- King's Candy Crush UI system (industry standard for casual game UI)
- Supercell's Clash Royale icon design (clarity at small sizes)
- Playful Corp's Wordament typography hierarchy
- Apple's iOS HIG icon guidelines adapted for game context
