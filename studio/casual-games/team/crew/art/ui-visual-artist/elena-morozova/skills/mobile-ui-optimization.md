# Mobile UI Optimization

**Skill ID:** mobile-ui-optimization
**Role:** UI Visual Artist
**Seniority:** Senior

## Overview

Optimization of UI art assets for mobile platforms — texture atlasing, 9-slice scaling, asset compression, memory budgeting, and draw call reduction.

## Tools & Frameworks

| Tool               | Proficiency  | Use Case                                     |
| ------------------ | ------------ | -------------------------------------------- |
| TexturePacker      | Expert       | Sprite atlas optimization, padding, trimming |
| Unity Sprite Atlas | Advanced     | In-engine atlas management, packing policies |
| ImageOptim/TinyPNG | Advanced     | Lossless compression for UI assets           |
| Unity Profiler     | Intermediate | Verifying UI draw call and memory impact     |

## Scenarios & Trade-offs

### Scenario 1: UI Texture Atlas Optimization

- **Approach:** Group assets by screen/context, use power-of-two atlas sizes, apply tight packing with 2px padding, trim transparent pixels
- **Trade-off:** Atlas size vs. loading granularity — larger atlases reduce draw calls but increase memory if not all assets are used simultaneously
- **Quality Bar:** UI texture budget ≤ 50MB for entire game; draw calls from UI ≤ 15 per screen

### Scenario 2: 9-Slice Scalable Components

- **Approach:** Design button/panel components with fixed corners and scalable centers; document slice coordinates for engineering
- **Trade-off:** Design flexibility vs. engineering simplicity — more complex shapes require more slices
- **Quality Bar:** Components scale from 48px to 400px width without visual distortion; corners maintain visual integrity

### Scenario 3: Multi-DPI Asset Delivery

- **Approach:** Produce assets at 1×, 2×, 3× resolutions; use Android resource qualifiers and iOS @2x/@3x naming
- **Trade-off:** APK/IPA size vs. visual quality — include only necessary resolutions per platform
- **Quality Bar:** No pixelation at any target device resolution; asset size impact documented per platform

## Quality Standards

- All UI assets delivered with documented memory budget per screen
- Texture atlases organized by screen flow to enable lazy loading
- 9-slice coordinates provided in engineering handoff documentation
- Compression format: ASTC 4×4 for mobile UI textures (best quality/size ratio)
- UI draw call budget: ≤ 15 per screen, ≤ 50 total for all active screens

## Industry References

- Unity's UI optimization best practices for mobile
- Supercell's asset optimization pipeline (GDC talk references)
- Google's Android UI performance guidelines
