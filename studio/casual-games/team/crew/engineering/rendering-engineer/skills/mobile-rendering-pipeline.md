---
name: studio-engineering-mobile-rendering-pipeline
description: Mobile graphics pipeline architecture — forward/deferred rendering, render pass optimization, Metal and Vulkan platform-specific rendering paths. Owned by Lars Johansson (Rendering Engineer). Use during Studio Pipeline Stages 3–5 for rendering pipeline development and Stage 6 (Automated Testing) for rendering validation. Trigger: mobile rendering, graphics pipeline, Metal, Vulkan, URP, render pass optimization, adaptive resolution.
version: "1.0.0"
---

# Mobile Rendering Pipeline

**Skill Owner:** Lars Johansson | **Version:** 1.0 | **Date:** 2026-04-20

## Description

Mobile graphics pipeline architecture including forward/deferred rendering, render pass optimization, and platform-specific rendering paths for Metal and Vulkan.

## Tools & Frameworks

| Tool      | Version  | Context                                         |
| --------- | -------- | ----------------------------------------------- |
| Metal     | 3.2      | iOS rendering API; custom render passes         |
| Vulkan    | 1.3      | Android rendering API; explicit synchronization |
| Unity URP | 2023 LTS | Universal Render Pipeline; mobile-optimized     |
| RenderDoc | 1.20     | Frame capture and analysis                      |

## Production Scenarios

**Scenario 1: URP Mobile Path (Unity 2022)** — Contributed to URP mobile rendering path optimization. Result: Shader compilation time reduced 60%; draw call overhead reduced 25%.
**Scenario 2: Adaptive Resolution Scaling (Arm 2023)** — Designed dynamic resolution system that adjusts render target size based on GPU load and thermal state. Result: 12 Arm partner studios adopted; average fps stability improved 40%.

## Trade-offs

- Forward vs deferred rendering → forward for mobile (lower bandwidth)
- Fixed vs adaptive resolution → adaptive for thermal management
- MSAA vs FXAA → FXAA for mobile (lower cost)

## Quality Standards

- Target: 60fps on mid-tier devices (Snapdragon 778G / A14)
- Draw calls: ≤ 150 per frame
- GPU memory: ≤ 500MB for rendering
- Shader compilation: ≤ 2s for full pipeline

## References

GDC 2023 "Mobile Graphics Optimization" (Arm); "Real-Time Rendering" (Akenine-Möller); Vulkan/Metal documentation
