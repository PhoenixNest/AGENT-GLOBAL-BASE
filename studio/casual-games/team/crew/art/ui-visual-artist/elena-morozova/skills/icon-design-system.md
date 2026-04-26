---
name: studio-art-icon-design-system
description: Systematic approach to game icon creation — grid systems, detail levels, production pipelines, and quality control for large icon sets (100–500+ icons). Owned by Elena Morozova (UI Visual Artist). Use during Studio Pipeline Stages 3–5 for icon production. Trigger: icon design, icon system, rarity icons, item icons, icon grid, icon pipeline, icon localization.
version: "1.0.0"
---

# Icon Design System

**Skill ID:** icon-design-system
**Role:** UI Visual Artist
**Seniority:** Senior

## Overview

Systematic approach to game icon creation — grid systems, detail levels, production pipelines, and quality control for large icon sets (100–500+ icons).

## Tools & Frameworks

| Tool               | Proficiency  | Use Case                                      |
| ------------------ | ------------ | --------------------------------------------- |
| Photoshop          | Expert       | Primary icon creation with layer organization |
| Figma              | Advanced     | Icon grid system, variant management          |
| Substance Designer | Intermediate | Procedural icon textures for consistency      |
| Custom scripts     | Intermediate | Batch processing, naming conventions          |

## Scenarios & Trade-offs

### Scenario 1: 200+ Item Icon Set with 5 Rarity Tiers

- **Approach:** Define base grid (128×128), create 5 detail-level templates, establish color palette per rarity, produce icons in batches
- **Trade-off:** Production speed vs. individual polish — templates ensure consistency but may feel formulaic if not varied
- **Quality Bar:** Each icon recognizable at 32×32px; rarity visually obvious without reading text; consistent lighting direction

### Scenario 2: Icon Localization Support

- **Approach:** Design icons without embedded text; use universal visual metaphors; create region-specific variants when cultural context matters
- **Trade-off:** Universal appeal vs. cultural specificity — some icons need regional variants (e.g., currency symbols)
- **Quality Bar:** Icons understandable across all target markets; no cultural insensitivity; region variants clearly versioned

## Quality Standards

- All icons follow consistent lighting direction (top-left primary light source)
- Stroke widths consistent across icon set (minimum 2px at 128×128)
- Color palette constrained to game's defined palette with rarity-specific accent colors
- Icons delivered in multiple resolutions: 32×32, 48×48, 64×64, 128×128, 256×256
- Naming convention: `icon_{category}_{item}_{variant}_{size}.png`

## Industry References

- Diablo inventory icon system (gold standard for clarity + personality)
- Genshin Impact material icon set (consistency across 1000+ items)
- King's Candy Crush boost icon design (casual game clarity benchmark)
