# Art Direction

**Skill Owner:** Renaud Leclercq (Art Director)
**Applies To:** Art Direction, Visual Pillar Definition, Art Style Guide Creation

## Tools & Frameworks

| Tool/Framework | Version Context             | Usage                                           |
| -------------- | --------------------------- | ----------------------------------------------- |
| Photoshop      | 2025+ (AI-powered features) | Concept art, mood boards, style guides          |
| Procreate      | 5.x (iPad)                  | Rapid concept sketching, visual exploration     |
| PureRef        | 1.9+                        | Reference board organization                    |
| Figma          | Latest                      | UI art direction collaboration with design team |
| Miro           | Latest                      | Visual pillar workshops with Creative Director  |

## Real-World Production Scenarios

### Scenario 1: Defining Visual Pillars for a New Casual Game

**Context:** Stage 0 (Art Direction) — Define the visual identity before any production begins.
**Process:**

1. Conduct visual research across competitor titles (top 20 grossing casual games)
2. Create mood boards for 3 distinct visual directions
3. Present to Creative Director with trade-off analysis (production cost, target audience appeal, technical feasibility)
4. Select direction and define 4-5 visual pillars (e.g., "Warm and inviting," "Hand-crafted feel," "Readable at small sizes")
5. Create art style guide covering color palette, character design principles, environment art direction, UI art direction
6. Define performance budgets (polycount, texture sizes, draw calls) for target devices

### Scenario 2: Art Pipeline Redesign

**Context:** Existing pipeline is inefficient; art production time is 40% above target.
**Process:**

1. Audit current pipeline: concept → modeling → texturing → rigging → animation → engine import
2. Identify bottlenecks: manual texture compression, no automated LOD generation, inconsistent naming conventions
3. Design new pipeline with automated steps: Substance batch processing, custom LOD tools, standardized naming
4. Implement in phases: Phase 1 (texture automation), Phase 2 (LOD tools), Phase 3 (naming conventions + CI integration)
5. Measure results: 40% production time reduction, 25% fewer art-related bugs

## Trade-Off Analysis

| Decision           | Option A                      | Option B                    | Trade-Off                                                                                          |
| ------------------ | ----------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------- |
| Art Style          | Realistic 3D                  | Stylized hand-painted       | Realistic = higher production cost; Stylized = broader audience appeal, easier mobile optimization |
| Texture Resolution | 2048x2048 per asset           | 1024x1024 + smart atlasing  | Higher res = better quality but 4x memory; Atlasing = 50% memory savings with minimal quality loss |
| Character Detail   | High-poly sculpt → retopology | Low-poly with baked normals | High-poly = better quality but 3x production time; Low-poly = faster production with good results  |

## Measurable Quality Standards

| Standard                     | Target                      | Measurement Method                                  |
| ---------------------------- | --------------------------- | --------------------------------------------------- |
| Art Style Consistency        | ≥ 95% adherence to guide    | Weekly art review with style guide checklist        |
| Performance Budget Adherence | ≤ target draw calls, memory | Unity Profiler, Xcode Instruments, Android Profiler |
| Art Review Pass Rate         | ≥ 90% first-pass approval   | Art review tracking in Jira                         |
| Production Velocity          | ≥ target assets/week        | Weekly asset production metrics                     |

## Industry Best Practice References

- **Supercell Art Review Process:** Structured weekly reviews with clear criteria, constructive feedback framework
- **GDC 2024: "Mobile Art Pipeline at Scale"** — Renaud's own talk on pipeline optimization
- **ArtStation Featured Artist Standards:** Community-recognized quality benchmarks for game art
- **Unity Best Practices: Mobile Art Optimization** — Official Unity guidelines for mobile art production
