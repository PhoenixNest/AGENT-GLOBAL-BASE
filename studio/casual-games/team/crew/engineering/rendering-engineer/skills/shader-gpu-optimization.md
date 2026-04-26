---
name: studio-engineering-shader-gpu-optimization
description: Shader programming and GPU optimization for mobile — HLSL/GLSL/MSL, instruction count reduction, texture sampling optimization, bandwidth management. Owned by Lars Johansson (Rendering Engineer). Use during Studio Pipeline Stages 5–6 for shader optimization and Stage 8 (Soft Launch) for GPU performance validation. Trigger: shader optimization, GPU optimization, HLSL, Metal shaders, ARM Mali, texture optimization, post-processing.
version: "1.0.0"
---

# Shader & GPU Optimization

**Skill Owner:** Lars Johansson | **Version:** 1.0 | **Date:** 2026-04-20

## Description

Shader programming (HLSL/GLSL/MSL) and GPU optimization techniques for mobile devices including instruction count reduction, texture sampling optimization, and bandwidth management.

## Tools & Frameworks

| Tool                      | Version | Context                     |
| ------------------------- | ------- | --------------------------- |
| HLSL                      | SM 5.0+ | Shader programming for URP  |
| Metal Shading Language    | 2.4     | iOS GPU shaders             |
| GLSL                      | 3.20    | Android/OpenGL ES shaders   |
| ARM Mali Offline Compiler | r42p0   | Shader instruction analysis |

## Production Scenarios

**Scenario 1: Mobile Post-Processing Stack (Unity 2022)** — Implemented bloom, color grading, and vignette for URP mobile. Result: Post-processing GPU cost reduced 45% vs previous implementation; visually equivalent output.
**Scenario 2: Shader Compilation Optimization (Unity 2023)** — Reduced shader variant count through keyword stripping and platform-specific shader variants. Result: Compilation time reduced 60%; app size reduced 30MB.

## Trade-offs

- Shader complexity vs visual quality → quality at mobile budget
- Runtime vs baked lighting → baked for static; minimal realtime for dynamic
- Texture resolution vs memory → compressed formats (ASTC) with mipmaps

## Quality Standards

- Shader instruction count: ≤ 64 ALU, ≤ 16 texture for mobile
- GPU frame budget: ≤ 8ms (50% of 16.67ms frame)
- Texture memory: ≤ 200MB total
- Bandwidth: ≤ 8GB/s sustained

## References

GDC 2022 "Mobile Shader Optimization" (Qualcomm); ARM GPU documentation; "GPU Gems" series
