---
name: studio-art-mobile-art-pipeline
description: Art pipeline design for mobile games — DCC tool integration, asset optimization, Perforce version control, CI/CD for art, and automated texture compression. Owned by Renaud Leclercq (Art Director). Use during Studio Pipeline Stages 0–5 for art pipeline setup and optimization. Trigger: art pipeline, DCC tools, Perforce, asset optimization, CI/CD art, texture compression, Addressables, art automation.
version: "1.0.0"
---

# Mobile Art Pipeline

**Skill Owner:** Renaud Leclercq (Art Director)
**Applies To:** Art Pipeline Design, DCC Tool Integration, Asset Optimization, CI/CD for Art

## Tools & Frameworks

| Tool/Framework      | Version Context                        | Usage                                       |
| ------------------- | -------------------------------------- | ------------------------------------------- |
| Maya                | 2025+                                  | 3D modeling, rigging, animation             |
| Blender             | 4.2+                                   | Open-source alternative for modeling        |
| Substance Painter   | 2024.1+                                | PBR texturing, material authoring           |
| Substance Designer  | 2024.1+                                | Procedural material creation                |
| Perforce Helix Core | 2024.1+                                | Version control for large binary art assets |
| Unity Addressables  | 1.21+                                  | Asset loading optimization                  |
| Texture Compression | ASTC (mobile), ETC2 (Android fallback) | GPU texture compression formats             |

## Real-World Production Scenarios

### Scenario 1: Setting Up Art Pipeline for a New Mobile Game

**Context:** Stage 0–2 — Build the art production pipeline from scratch.
**Process:**

1. Define DCC tool chain: Maya (modeling/rigging) → Substance Painter (texturing) → Unity (engine)
2. Set up Perforce Helix Core for version control with art asset streaming
3. Create automated export scripts: Maya FBX export → Substance texture export → Unity import
4. Define naming conventions: `char_hero_v01.fbx`, `tex_hero_diffuse_1024.png`, `mat_hero_surface.mat`
5. Set up automated texture compression pipeline: source PNG → ASTC 6x6 → Unity Addressables
6. Integrate with CI/CD: art asset validation on every commit (polycount check, texture size check, naming convention check)

### Scenario 2: Reducing Art Production Time by 40%

**Context:** Pipeline audit reveals manual processes causing delays.
**Process:**

1. Map current pipeline and measure time per step
2. Identify automation opportunities: batch texture processing, automated LOD generation, template materials
3. Build custom tools: Substance batch processor, Maya LOD generator, Unity asset validator
4. Train art team on new tools and processes
5. Measure results: 40% reduction in production time, 25% fewer art-related bugs

## Trade-Off Analysis

| Decision            | Option A                    | Option B               | Trade-Off                                                                                          |
| ------------------- | --------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------- |
| Version Control     | Perforce (binary-optimized) | Git LFS                | Perforce = better for large binaries but higher cost; Git LFS = cheaper but slower for large files |
| Texture Compression | ASTC (universal)            | ASTC + ETC2 fallback   | Universal ASTC = simpler pipeline; Fallback = broader device support but 2x texture storage        |
| Asset Loading       | Unity Resources (simple)    | Addressables (complex) | Resources = easy setup but no optimization; Addressables = complex but 50%+ memory savings         |

## Measurable Quality Standards

| Standard                       | Target                   | Measurement Method                  |
| ------------------------------ | ------------------------ | ----------------------------------- |
| Pipeline Automation Rate       | ≥ 70% of steps automated | Pipeline audit checklist            |
| Asset Import Time              | ≤ 5 seconds per asset    | CI/CD pipeline metrics              |
| Texture Compression Quality    | ≥ 90% visual fidelity    | Side-by-side comparison with source |
| Art Asset Validation Pass Rate | ≥ 95% first-pass         | Automated validation results        |

## Industry Best Practice References

- **Unity Mobile Optimization Guide** — Official Unity guidelines for mobile art production
- **Supercell Art Pipeline** — Industry-standard mobile game art pipeline
- **GDC Vault: "Art Pipeline for Mobile Games"** — Multiple talks on mobile art optimization
- **ASTC Texture Compression Specification** — ARM's official documentation
