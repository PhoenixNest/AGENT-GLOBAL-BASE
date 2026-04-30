---
name: studio-art-mobile-rendering-optimization
description: Mobile rendering optimization for casual games using Unity URP — shader optimization, draw call reduction, overdraw analysis, LOD implementation, and GPU profiling on iOS and Android. Owned by Lena Kovac (Technical Artist). Use during Studio Pipeline Stages 2–6 (Automated Testing). Trigger: rendering optimization, mobile rendering, overdraw, draw calls, LOD, URP, shader optimization, GPU performance, fill rate.
version: "1.0.0"
---

# Mobile Rendering Optimization

**Skill Owner:** Lena Kovac (Technical Artist)
**Applies To:** Unity URP, Mobile GPU Optimization, Shader Authoring, Rendering Performance

## Rendering Budget (Studio Baseline)

Set in collaboration with Dmitri Volkov; enforced by Lena at the art pipeline level:

| Budget                | Target (Min Spec)               | Target (Flagship) | Measurement Tool           |
| --------------------- | ------------------------------- | ----------------- | -------------------------- |
| Draw calls per frame  | ≤150                            | ≤300              | Unity Frame Debugger       |
| Batches (SRP Batcher) | ≤100                            | ≤200              | Unity Statistics overlay   |
| Shader complexity     | ≤8 texture samples per fragment | N/A               | RenderDoc shader inspector |
| Overdraw (fill rate)  | ≤2× (average)                   | ≤3×               | Scene View overdraw mode   |
| Texture memory (VRAM) | ≤80MB                           | ≤120MB            | RenderDoc memory view      |

## Optimization Techniques

### 1. Draw Call Reduction

**Static Batching:** Enable for non-moving environment assets. Lena audits all environment assets at Stage 3 and marks eligible objects for static batching.

**SRP Batcher:** Unity URP's SRP Batcher reduces draw calls for objects sharing the same shader variant. To maximize batching:

- Consolidate materials — avoid creating a unique material per asset when a shared material with property overrides suffices
- Do not break batching by mixing built-in and URP shaders in the same scene

**GPU Instancing:** Required for any object rendered >20 times in the same scene (grass, coins, particles). Lena writes GPU-instanced variants of the relevant shaders.

**Texture Atlasing:** UI sprites are atlased into sprite sheets (Unity Sprite Atlas) — one draw call for the entire UI layer vs. N individual draws.

### 2. Shader Optimization

**Mobile Shader Design Rules (Lena's standards):**

| Rule                                                              | Reason                                                       |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| Use half precision (`half`) for all color and normal calculations | Mobile GPUs compute `half` in 1 cycle vs. 2 for `float`      |
| Avoid `discard` in fragment shaders                               | Discard prevents early-z culling; use alpha blending instead |
| Pre-compute in vertex shader, not fragment shader                 | Vertex shader runs N×M fewer times than fragment shader      |
| Use ASTC compression for all color textures                       | 4–8bpp vs. 32bpp for RGBA32; frees GPU memory bandwidth      |
| Limit texture samples per fragment to ≤8                          | Mobile GPUs have limited texture unit parallelism            |

### 3. Overdraw Reduction

Overdraw occurs when multiple fragments are rendered to the same pixel (e.g., layered UI, particle effects over background, transparent materials).

**Analysis:** Open Unity's Scene View → Overdraw mode. High-overdraw areas appear bright. Target: average overdraw ≤2× (each pixel rendered no more than twice).

**Mitigation for UI:** Set `Canvas.renderMode` to `Screen Space - Overlay` only for the top-level HUD. Secondary UI panels use a camera-space canvas to enable proper clipping.

**Mitigation for Particles:** All particle systems reviewed by Lena and Javier Moreno (VFX Artist) for overdraw contribution at the Stage 3 milestone.

## Real-World Production Scenarios

### Scenario 1: Diagnosing a GPU Bottleneck

**Context:** Unity Profiler shows `Gfx.WaitForPresent` is consuming 30% of frame time on minimum spec Android.
**Process:**

1. Open RenderDoc; capture a frame during the problematic game state
2. Review the draw call list: are there batches that should be merged? Is there a shader with high fragment complexity?
3. Check the overdraw pass: is there a specific layer (particles, UI, effects) causing extreme overdraw?
4. Check texture bandwidth: are large uncompressed textures being sampled in the bottleneck pass?
5. Resolve in priority order: reduce overdraw → reduce texture samples → reduce draw calls → simplify shader

### Scenario 2: Implementing Mobile-Optimized URP Shaders for Characters

**Context:** Existing characters use the URP Lit shader; Renaud wants higher-quality rendering but within mobile constraints.
**Process:**

1. Author a custom URP shader using Shader Graph that bakes AO into the vertex color channel (avoiding a second texture sample)
2. Implement a simplified specular model: use a Matcap texture instead of real-time specular calculation
3. Add an optional rim light driven by a global shader parameter (one cost for the entire scene)
4. Profile on minimum spec device: target <5ms GPU time for character rendering pass

## Measurable Quality Standards

| Standard                        | Target                           | Measurement Method             |
| ------------------------------- | -------------------------------- | ------------------------------ |
| Draw calls at launch            | ≤150 on minimum spec             | Unity Frame Debugger           |
| Overdraw (average)              | ≤2× across gameplay scene        | Unity Scene View overdraw mode |
| No custom shader without review | 100% of shaders reviewed by Lena | Shader asset audit             |
| GPU budget compliance           | ≤8ms GPU frame time (60fps)      | RenderDoc timing               |
