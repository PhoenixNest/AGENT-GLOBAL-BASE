# Stage 4: Interview Scores (G18) — Nikolai Petrov

**Role:** Engine Engineer (G18)
**Candidate:** Nikolai Petrov
**Interview Period:** 2026-04-12 to 2026-04-14
**Interview Panel:** Dmitri Volkov (Sr. Game Engineer), Viktor Stahl (Sr. Engine Engineer, G13), CHRO Panel Coordinator
**Document ID:** INT-2026-G18-001

---

## Interview Component Scores

| Component                  | Score    | Max | Notes                                                                                                                                                                      |
| -------------------------- | -------- | --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Technical/Case Study       | 4.1      | 5.0 | C++ low-level challenge — implemented collision detection optimization with spatial partitioning; clean code with good mathematical foundations                            |
| System Design              | 3.8      | 5.0 | Physics system design exercise showed solid implementation skills; still learning to design subsystems from scratch                                                        |
| Panel Interview            | 4.1      | 5.0 | Strong knowledge of Havok SDK integration; described collision detection optimization (25% compute reduction) in detail; Vulkan rendering path well explained              |
| Behavioral                 | 3.9      | 5.0 | Team player; described collaborating with gameplay team on physics tuning; can debug straightforward issues but acknowledged struggles with multi-threaded race conditions |
| Portfolio / Public Signals | 4.2      | 5.0 | Wargaming Core Engine contributions; Havok SDK integration for WoT mobile; Vulkan rendering path for Android                                                               |
| **Weighted Composite**     | **4.08** | 5.0 |                                                                                                                                                                            |

---

## Detailed Assessment by Component

### Technical/Case Study (4.1/5.0)

**Challenge:** Optimize a collision detection system that currently consumes too much CPU time in a mobile game with 500+ physics objects.

**Approach:** Nikolai proposed a broad-phase/narrow-phase collision detection pipeline with:

- Spatial hashing for broad-phase overlap detection
- SAT (Separating Axis Theorem) for narrow-phase convex collision
- Frame-coherent processing to maximize CPU cache efficiency

**Strengths:** Strong mathematical foundations; correct spatial partitioning approach; cache-aware data layout.
**Gaps:** Did not discuss SIMD optimization; could have addressed GPU-based collision detection as alternative.

### System Design (3.8/5.0)

**Challenge:** Design a platform abstraction layer for audio system integration supporting both Android (OpenSL ES) and iOS (Core Audio).

**Approach:** Nikolai designed an audio abstraction with platform-specific backends and a unified API.

**Strengths:** Clean separation of platform-specific code; correct understanding of audio latency requirements on mobile.
**Gaps:** Relied on senior guidance for architectural decisions; no experience with audio middleware (FMOD/Wwise).

### Panel Interview (4.1/5.0)

**Key Topics Covered:**

- Havok SDK integration (strong — described WoT mobile integration in detail)
- Collision detection optimization (strong — 25% compute reduction through spatial partitioning)
- Vulkan rendering path (solid — described Android Vulkan rendering implementation)
- Mathematics background (strong — applied math degree; linear algebra, numerical methods, computational geometry)

**Panel Feedback:**

- **Dmitri Volkov:** "Solid engine engineer with good fundamentals. His physics integration work at Wargaming is exactly the level we need for mid-level engine work."
- **Viktor Stahl:** "Good implementation skills. He can take engine architecture decisions and implement them correctly. His mathematical background is strong — valuable for physics work. Still developing system design skills but that's expected."
- **CHRO Coordinator:** "Honest about limitations. Answers specific with project examples. Strong work ethic."

### Behavioral (3.9/5.0)

**STAR Response — Physics Tuning Collaboration:**

- **Situation:** Gameplay team reported that physics behavior felt "off" in mobile WoT.
- **Task:** Nikolai needed to tune physics parameters to match player expectations.
- **Action:** He profiled the physics simulation, identified that collision response timing was inconsistent due to variable timestep, and implemented fixed-timestep physics with interpolation.
- **Result:** Physics behavior became consistent and predictable. Gameplay team satisfaction improved significantly.

**Leadership Evidence:** Still developing as a leader; no formal mentoring experience; acknowledged limitations in multi-threaded debugging.

### Portfolio (4.2/5.0)

| Artifact                                           | Quality | Relevance |
| -------------------------------------------------- | ------- | --------- |
| Wargaming Core Engine contributions                | 4/5     | 5/5       |
| Havok SDK integration (WoT mobile)                 | 4/5     | 5/5       |
| Vulkan rendering path (Android)                    | 4/5     | 4/5       |
| Collision detection optimization (25% improvement) | 4/5     | 5/5       |

---

## Percentile Ranking

| Percentile | Composite Score | Interpretation  |
| ---------- | --------------- | --------------- |
| 90th       | 4.10            | Strong — Hire   |
| **88th**   | **4.08**        | **Good — Hire** |
| 80th       | 3.80            | Good — Consider |

Nikolai Petrov scores **4.08/5.0**, placing him in the **88th percentile**.

---

## Interview Panel Recommendation

| Panelist         | Recommendation | Confidence |
| ---------------- | -------------- | ---------- |
| Dmitri Volkov    | Hire           | High       |
| Viktor Stahl     | Hire           | High       |
| CHRO Coordinator | Hire           | Medium     |

**Consensus:** Unanimous recommendation to advance to Stage 5 (Vetting Gate).

---

**Gate Status:** ✅ Composite score 4.08/5.0 (88th percentile). Proceeding to Stage 5.
