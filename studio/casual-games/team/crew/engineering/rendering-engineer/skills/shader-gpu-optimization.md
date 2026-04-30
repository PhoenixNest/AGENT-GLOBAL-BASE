---
name: studio-engineering-shader-gpu-optimization
description: Shader programming and GPU optimization for mobile — HLSL/GLSL/MSL, instruction count reduction, texture sampling optimization, bandwidth management. Owned by Lars Johansson (Rendering Engineer). Use during Studio Pipeline Stages 5–6 for shader optimization and Stage 6 (Automated Testing) for GPU performance validation. Trigger: shader optimization, GPU optimization, HLSL, Metal shaders, ARM Mali, texture optimization, post-processing.
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

## Stage 6 — Automated Testing: GPU Validation Gate

Lars's shader and GPU optimization work culminates at **Stage 6 (Automated Testing)**, where rendering performance is validated against the device matrix as part of the quality gate.

### What Lars Owns at Stage 6

| Validation Item                 | Method                                                                                        |
| ------------------------------- | --------------------------------------------------------------------------------------------- |
| Shader instruction count audit  | ARM Mali Offline Compiler pass on all shaders in the build; flag any over 64 ALU instructions |
| GPU frame budget validation     | RenderDoc frame capture on Tier 1 and Tier 2 devices; must be ≤ 8ms GPU frame time            |
| SRP Batcher compatibility check | Verify all materials in the build pass SRP Batcher — zero batching breaks in Frame Debugger   |
| Texture memory audit            | Confirm texture memory stays within the ≤ 200MB budget across all game scenes                 |

Lars produces a **Rendering Gate Report** at Stage 6 summarising results against each metric. This report is submitted to Amara Osei (Lead QA Engineer) as part of the Stage 6 sign-off package.

### Soft Launch Monitoring (Informational Context)

Although Lars's formal gate ownership ends at Stage 6, he monitors rendering metrics during soft launch (Stage 8) on a best-effort basis — reviewing crash reports and GPU-related ANR (Application Not Responding) events from soft launch regions. He does not own a Stage 8 sign-off gate; he provides rendering expertise in support of the backend and QA teams who do.

## References

GDC 2022 "Mobile Shader Optimization" (Qualcomm); ARM GPU documentation; "GPU Gems" series
