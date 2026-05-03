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

## Unity 6 LTS Rendering Architecture

The Casual Games Studio uses Unity 6.3 LTS with the **Universal Render Pipeline (URP)** as its rendering foundation. Lars Johansson is the URP owner — he is the single engineer responsible for the URP configuration and rendering performance budget.

### URP Ownership Scope

| Responsibility                   | Detail                                                                                                                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **URP Asset configuration**      | Lars configures the URP Asset (shadow settings, MSAA, HDR, post-processing global settings) for the studio's target device tier |
| **Render features**              | Lars designs, implements, and reviews all custom ScriptableRenderFeature additions to the URP forward renderer                  |
| **Rendering performance budget** | Lars owns the per-frame GPU budget (≤ 150 draw calls, ≤ 8ms GPU frame time) and enforces it across all game content             |

### URP Forward Renderer with Custom Render Features

The studio uses URP's **forward renderer** (not deferred) — the correct choice for mobile targets where bandwidth is the binding constraint. Custom render features are added for:

- Custom depth pre-pass for specific transparency sorting requirements
- Outline rendering for gameplay highlight feedback (character selection, interactable objects)
- Mobile-optimised post-processing effects authored as render features to minimize overdraw

Lars reviews all render feature additions for draw call cost and GPU bandwidth impact before they enter production.

### GPU Instancing and SRP Batcher

Lars configures and maintains two Unity rendering optimisations:

- **GPU Instancing** — enabled for repeated object types (collectibles, environment props, enemies) to batch draw calls
- **SRP Batcher** — configured and validated across all materials; Lars ensures all shaders are SRP Batcher compatible (uses CBUFFER per-material layout)

Any new shader added to the project must be validated as SRP Batcher compatible before it enters the main branch. Lars performs this validation during code review.

### Frame Debugger Workflow

Lars uses Unity's Frame Debugger as the primary tool for rendering issue diagnosis:

1. Capture a frame from the target device (via USB + Android frame capture or iOS Instruments)
2. Identify draw call batching breaks (material changes, SRP Batcher incompatibilities)
3. Locate overdraw hotspots (UI layering, transparent objects)
4. Validate render feature ordering

Frame Debugger sessions are run at each Stage 6 gate and whenever a rendering regression is suspected.

## Collaboration with Lena Kovac (Technical Artist)

Lena Kovac (Technical Artist, Art division) is the primary shader author for the studio. She authors shaders using Unity's **Shader Graph** visual editor. Lars's role in this collaboration is performance and compatibility review.

### Collaboration Protocol

| Step | Owner | Action                                                                                                                                                              |
| ---- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Lena  | Authors shader in Shader Graph; targets the desired visual output for the game's art direction                                                                      |
| 2    | Lena  | Submits shader for Lars's review (via PR or direct review session)                                                                                                  |
| 3    | Lars  | Reviews shader for: (a) instruction count via ARM Mali Offline Compiler; (b) texture sample count; (c) SRP Batcher compatibility; (d) URP render pass compatibility |
| 4    | Lars  | Either approves (shader enters main branch) or returns with specific performance feedback                                                                           |
| 5    | Lena  | Iterates based on Lars's feedback; resubmits                                                                                                                        |

Lars does not dictate visual decisions — Lena owns the aesthetic. Lars's review is limited to GPU performance and URP pipeline compatibility. If a visual effect cannot meet the mobile GPU budget at acceptable quality, Lars and Lena negotiate a mobile-optimised alternative together.

## References

GDC 2023 "Mobile Graphics Optimization" (Arm); "Real-Time Rendering" (Akenine-Möller); Vulkan/Metal documentation
