---
name: studio-engineering-unity-unreal-expertise
description: Deep engine-level expertise in Unity 6 LTS and Unreal Engine 5 for casual mobile games — editor workflows, C#/C++ scripting, custom tooling, and engine-specific performance patterns. Owned by Dmitri Volkov (Senior Game Engineer). Trigger: Unity, Unreal, engine setup, editor tools, C# scripting, Blueprint, engine architecture.
version: "1.0.0"
---

# Unity / Unreal Expertise

**Skill Owner:** Dmitri Volkov (Senior Game Engineer)
**Applies To:** Engine Architecture, Editor Tooling, Scripting, Engine-Level Performance

## Tools & Frameworks

| Tool/Framework   | Version Context | Usage                                                           |
| ---------------- | --------------- | --------------------------------------------------------------- |
| Unity            | 6 LTS           | Primary game engine for all Casual Games Studio titles          |
| Unreal Engine    | 5.4+            | Secondary engine for graphically intensive projects             |
| C#               | .NET 8+         | Primary scripting language (Unity)                              |
| C++              | C++20           | Engine-level and performance-critical code (Unreal)             |
| Unity Profiler   | Built-in        | CPU/GPU/memory profiling                                        |
| RenderDoc        | 1.33+           | GPU frame capture and shader debugging                          |
| Unity DOTS       | Latest          | Data-Oriented Technology Stack for performance-critical systems |
| Unreal Blueprint | UE 5.4+         | Visual scripting for rapid prototyping                          |

## Real-World Production Scenarios

### Scenario 1: Engine Selection for a New Casual Title

**Context:** New title in pre-production; team deciding between Unity and Unreal.
**Process:**

1. Evaluate target platform (iOS/Android) and performance budget against engine overhead
2. Assess art style requirements: Unity for stylized 2D/2.5D; Unreal for realistic lighting and Lumen GI
3. Review team proficiency — Casual Games Studio is Unity-primary; Unreal adds ramp-up cost
4. Benchmark prototype scenes: render at 60fps on iPhone 12 / mid-tier Android (Pixel 6a equivalent)
5. Factor in package size — Unity IL2CPP builds typically 30–40MB smaller than equivalent UE5 builds
6. Document decision in Architecture Decision Record (ADR) at Stage 3

**Default for Casual Games Studio:** Unity 6 LTS unless a specific title demands Unreal's rendering capabilities and the team has staffed accordingly.

### Scenario 2: Implementing Custom Unity Editor Tooling

**Context:** Designers need a level-authoring tool that isn't supported by default Unity Editor.
**Process:**

1. Define the workflow in collaboration with Lead Game Designer (Mei Watanabe)
2. Implement using `UnityEditor` namespace — custom `EditorWindow`, `PropertyDrawer`, or `AssetPostprocessor` as appropriate
3. Integrate with Unity's Undo stack to prevent data loss during authoring
4. Serialize tool state via `ScriptableObject` for version control compatibility
5. Write minimal documentation (README + GIF demo) and add to internal tools registry
6. Ship the tool before Stage 5 (Full Production) so designers have it during ramp-up

### Scenario 3: Upgrading a Project to a New Unity LTS

**Context:** Mid-production Unity version upgrade required for a critical bug fix.
**Process:**

1. Create a separate git branch for the upgrade
2. Run Unity's API Updater; address all deprecated API warnings before touching gameplay code
3. Rebuild all Addressable Asset Groups and validate build sizes
4. Profile the project on target devices pre- and post-upgrade to detect regressions
5. Run the full automated test suite (Amara Osei); require zero regressions before merge
6. Merge to main only after QA sign-off

## Trade-Off Analysis

| Decision           | Option A         | Option B                | Trade-Off                                                                                   |
| ------------------ | ---------------- | ----------------------- | ------------------------------------------------------------------------------------------- |
| Scripting Runtime  | Mono             | IL2CPP                  | Mono = faster iteration; IL2CPP = better runtime performance and required for iOS App Store |
| Rendering Pipeline | Built-in (BRP)   | URP                     | BRP = broadest compatibility; URP = better performance on mobile, SRP Batcher, shader graph |
| Asset System       | Resources folder | Addressables            | Resources = simpler; Addressables = required for OTA updates and memory management at scale |
| Physics            | Unity PhysX      | DOTS Physics (Entities) | PhysX = familiar, GameObject-based; DOTS = 10–100× throughput for simulation-heavy games    |

## Measurable Quality Standards

| Standard                        | Target                                       | Measurement Method           |
| ------------------------------- | -------------------------------------------- | ---------------------------- |
| Build iteration time            | ≤ 3 minutes (incremental)                    | Unity Build Report           |
| Editor script compilation       | ≤ 30 seconds after code change               | Domain Reload time           |
| Zero engine upgrade regressions | 100% test suite pass post-upgrade            | Automated test suite (Amara) |
| Custom tool adoption            | 100% of target team using tool within 1 week | Tool usage metrics           |

## Industry Best Practice References

- **Unity 6 LTS Release Notes** — Official feature and API changelog
- **Unity Performance Optimization Guide** — Mobile-specific patterns
- **GDC 2023: "Real-Time Multiplayer Architecture at Scale"** — Dmitri Volkov (speaker)
- **Unreal Engine 5 Mobile Best Practices** — Epic Games developer documentation
