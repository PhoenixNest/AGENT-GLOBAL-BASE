# Stage 4: Interview Scores (G15) — Lars Johansson

**Role:** Rendering Engineer (G15)
**Candidate:** Lars Johansson
**Interview Period:** 2026-04-13 to 2026-04-15
**Interview Panel:** Dmitri Volkov (Sr. Game Engineer), Viktor Stahl (Sr. Engine Engineer, G13), CHRO Panel Coordinator
**Document ID:** INT-2026-G15-001

---

## Interview Component Scores

| Component                  | Score    | Max | Notes                                                                                                                                                                                                 |
| -------------------------- | -------- | --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Technical/Case Study       | 4.4      | 5.0 | Mobile shader optimization challenge — proposed shader variant reduction strategy; demonstrated GPU profiling methodology; correctly identified fill-rate bottleneck on Mali GPUs                     |
| System Design              | 4.3      | 5.0 | Designed mobile rendering pipeline with adaptive resolution scaling; addressed Metal vs Vulkan differences; proposed post-processing pipeline optimized for mobile GPU                                |
| Panel Interview            | 4.2      | 5.0 | Strong knowledge of URP mobile path; described shader compilation optimization (60% improvement); Mali GPU profiling tools architecture well explained; post-processing stack design solid            |
| Behavioral                 | 4.0      | 5.0 | Collaborated with 12 Arm partner studios on adaptive resolution; mentored junior graphics programmers; described conflict between visual quality and performance using data-driven profiling approach |
| Portfolio / Public Signals | 4.3      | 5.0 | Arm Mali profiling tools (5,000+ users); URP mobile contributor; published "Mobile Graphics Optimization" guide series; 12 partner studio adoptions                                                   |
| **Weighted Composite**     | **4.25** | 5.0 |                                                                                                                                                                                                       |

---

## Detailed Assessment by Component

### Technical/Case Study (4.4/5.0)

**Challenge:** Optimize a mobile game rendering pipeline currently achieving 45fps on mid-tier Android (Snapdragon 600 series) to reach 60fps target. The game uses 20 unique shaders, heavy overdraw from particle effects, and full-screen post-processing.

**Approach:** Lars proposed a multi-pronged optimization:

1. **Shader variant reduction** — from 20 to 8 via dynamic keyword-based branching instead of static variants (reducing compilation time and memory)
2. **Overdraw reduction** — depth-sorted transparent rendering with early-z pass for opaque geometry
3. **Post-processing optimization** — half-resolution bloom, single-pass color grading + vignette combine
4. **Adaptive resolution** — dynamic resolution scaling based on GPU frame time budget (the system he designed at Arm)

**Strengths:** Production-tested approach; systematic profiling-before-optimization methodology; realistic performance targets.
**Gaps:** Did not discuss Vulkan-specific descriptor set optimization; could have addressed Tile-Based Deferred Rendering (TBDR) more deeply.

### System Design (4.3/5.0)

**Challenge:** Design a rendering pipeline that targets both iOS Metal and Android Vulkan from a single codebase, with platform-specific optimizations while maintaining visual parity.

**Approach:** Lars designed a rendering abstraction with:

- Platform-specific render graph translating to Metal command buffers or Vulkan command pools
- Unified material system with shader cross-compilation (HLSL → MSL via SPIRV-Cross, HLSL → Vulkan SPIRV)
- Adaptive resolution scaling based on GPU frame time budget
- Post-processing pipeline with mobile-optimized passes

**Strengths:** Clean architecture; leverages URP experience; addresses both platforms.
**Gaps:** Could have discussed Metal-specific frame pacing features more deeply.

### Panel Interview (4.2/5.0)

**Key Topics Covered:**

- URP mobile path contributions (strong — described shader compilation optimization in detail)
- Mali GPU profiling tools (strong — architecture and adoption by 5,000+ developers)
- Adaptive resolution scaling (solid — 12 Arm partner studio adoptions)
- Mobile post-processing (strong — bloom, color grading, vignette optimized for mobile GPU)

**Panel Feedback:**

- **Dmitri Volkov:** "Excellent mobile graphics expertise. His profiling-first approach to optimization is exactly what we need for 60fps target."
- **Viktor Stahl:** "His rendering pipeline design complements my engine architecture well. Clean abstraction between engine and rendering layers."
- **CHRO Coordinator:** "Clear technical communicator. Answers specific with real project examples. Passionate about mobile graphics."

### Behavioral (4.0/5.0)

**STAR Response — Balancing Quality and Performance:**

- **Situation:** At Arm, a partner studio wanted cinematic-quality post-processing that would halve their frame rate on mid-tier devices.
- **Task:** Lars needed to find a compromise without compromising visual quality perception.
- **Action:** He profiled each post-processing effect, identified that bloom at full resolution consumed 40% of post-processing GPU time, and proposed half-resolution bloom with upsampling — visually indistinguishable at 50% GPU cost.
- **Result:** Studio adopted the approach across all their titles; became part of Arm's mobile optimization guide.

**Leadership Evidence:** Collaborated with 12 Arm partner studios; authored optimization guide series; mentored junior graphics programmers.

### Portfolio (4.3/5.0)

| Artifact                                                | Quality | Relevance |
| ------------------------------------------------------- | ------- | --------- |
| Arm Mali GPU profiling tools (5,000+ users)             | 5/5     | 5/5       |
| URP mobile shader optimization (60% faster compilation) | 4/5     | 5/5       |
| Mobile Graphics Optimization guide series               | 4/5     | 4/5       |
| Adaptive resolution scaling (12 studio adoptions)       | 4/5     | 5/5       |

---

## Percentile Ranking

| Percentile | Composite Score | Interpretation   |
| ---------- | --------------- | ---------------- |
| 99th       | 4.50+           | Exceptional      |
| 95th       | 4.30            | Elite — Hire     |
| **93rd**   | **4.25**        | **Elite — Hire** |
| 90th       | 4.10            | Strong — Hire    |

Lars Johansson scores **4.25/5.0**, placing him in the **93rd percentile**.

---

## Interview Panel Recommendation

| Panelist         | Recommendation | Confidence |
| ---------------- | -------------- | ---------- |
| Dmitri Volkov    | Hire           | High       |
| Viktor Stahl     | Hire           | High       |
| CHRO Coordinator | Hire           | High       |

**Consensus:** Unanimous recommendation to advance to Stage 5 (Vetting Gate).

---

**Gate Status:** ✅ Composite score 4.25/5.0 (93rd percentile). Proceeding to Stage 5.
