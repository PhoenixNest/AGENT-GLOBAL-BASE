---
name: studio-art-shader-programming
description: HLSL/GLSL shader development and Unity URP shader optimization for mobile games — shader libraries, GPU profiling, and mobile shader performance tuning. Owned by Lena Kovac (Technical Artist). Use during Studio Pipeline Stages 2–6 (Automated Testing) for shader development and optimization. Trigger: shader programming, HLSL, GLSL, URP shaders, shader optimization, mobile shaders, GPU profiling, Shader Graph.
version: "1.0.0"
---

# Shader Programming

**Skill Owner:** Lena Kovac (Technical Artist)
**Applies To:** HLSL/GLSL Shader Development, Unity URP Shaders, Mobile Shader Optimization

## Tools & Frameworks

| Tool/Framework     | Version Context                  | Usage                            |
| ------------------ | -------------------------------- | -------------------------------- |
| Unity Shader Graph | 2024 LTS+ (URP)                  | Visual shader authoring          |
| HLSL               | Shader Model 5.0+                | Custom shader code               |
| RenderDoc          | 1.33+                            | GPU debugging and frame analysis |
| Unity URP          | 16.0+                            | Universal Render Pipeline        |
| Substance Designer | 2024.1+                          | Procedural material authoring    |
| Shader Variants    | Unity Shader Variant Collections | Shader compilation optimization  |

## Real-World Production Scenarios

### Scenario 1: Building a Mobile-Optimized Shader Library

**Context:** Need consistent, performant shaders across all game assets.
**Process:**

1. Define shader categories: character, environment, UI, VFX, post-processing
2. Build base shaders for each category with mobile-optimized feature sets
3. Implement LOD for shaders: high-quality (flagship devices), medium (mid-tier), low (budget devices)
4. Create Shader Variant Collections to pre-compile only needed variants
5. Test on target devices: measure frame time, GPU memory, shader compilation time
6. Results: shader library used across 3 game variants, 35% GPU time reduction

### Scenario 2: Optimizing URP Shaders for Mid-Tier Android

**Context:** Shaders cause frame drops on devices with Mali-G57 GPU.
**Process:**

1. Profile GPU usage: identify most expensive shader passes
2. Optimize: reduce texture samples, simplify math operations, use half precision where possible
3. Replace expensive operations: approximate complex math with lookup tables
4. Test: verify visual quality is acceptable, measure frame time improvement
5. Results: 40% GPU time reduction on Mali-G57, maintained visual quality

## Trade-Off Analysis

| Decision          | Option A               | Option B                     | Trade-Off                                                                                         |
| ----------------- | ---------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------- |
| Shader Complexity | PBR (physically-based) | Simplified mobile PBR        | PBR = realistic but expensive; Mobile PBR = 50% cheaper with 90% visual fidelity                  |
| Shader Authoring  | Shader Graph (visual)  | Hand-written HLSL            | Graph = faster iteration, team accessible; HLSL = more control, better optimization               |
| Texture Sampling  | 4K textures            | 1K-2K with smart compression | 4K = best quality but 4x memory; Smart compression = 75% memory savings with minimal quality loss |

## Measurable Quality Standards

| Standard                | Target                   | Measurement Method            |
| ----------------------- | ------------------------ | ----------------------------- |
| Shader Frame Time       | ≤ 2ms per frame          | RenderDoc GPU profiling       |
| Shader Compilation Time | ≤ 100ms per variant      | Unity build metrics           |
| Shader Variant Count    | ≤ 200 total variants     | Unity Shader Variant analysis |
| Visual Fidelity         | ≥ 90% match to reference | Side-by-side comparison       |

## Industry Best Practice References

- **Unity URP Shader Optimization Guide** — Official Unity guidelines
- **GDC: "Mobile Shader Optimization"** — Multiple talks on mobile GPU optimization
- **Khronos Group: Vulkan/Metal Best Practices** — Platform-specific GPU guidelines
- **GPUOpen: "Shader Optimization Techniques"** — AMD's official optimization guide
