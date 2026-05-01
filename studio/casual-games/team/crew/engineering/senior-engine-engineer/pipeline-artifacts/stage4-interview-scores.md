# Stage 4: Interview Scores (G13) — Viktor Stahl

**Role:** Senior Engine Engineer (G13)
**Candidate:** Viktor Stahl
**Interview Period:** 2026-04-13 to 2026-04-15
**Interview Panel:** Dmitri Volkov (Sr. Game Engineer), Software Architect, CHRO Panel Coordinator
**Document ID:** INT-2026-G13-001

---

## Interview Component Scores

| Component                  | Score    | Max | Notes                                                                                                                                                                                                                                 |
| -------------------------- | -------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Technical/Case Study       | 4.7      | 5.0 | Custom allocator design for game engine — proposed hierarchical allocator with separate pools for transient/permanent data; lock-free ring buffer for multi-threaded job queue; demonstrated deep understanding of CPU cache behavior |
| System Design              | 4.5      | 5.0 | Designed platform abstraction layer for Metal + Vulkan; addressed memory alignment requirements across platforms; proposed deterministic physics synchronization approach for cross-platform multiplayer                              |
| Panel Interview            | 4.4      | 5.0 | Deep knowledge of UE5 internals; described memory fragmentation analysis methodology; physics profiler architecture explained clearly; strong on CPU/GPU profiling techniques                                                         |
| Behavioral                 | 4.2      | 5.0 | Led engine pod of 6 at Epic; introduced engine code review standards that reduced production bugs; described mentoring 3 junior programmers                                                                                           |
| Portfolio / Public Signals | 4.4      | 5.0 | UE5 source contributor with multiple merged PRs; physics profiler used by 200+ internal developers; 3 shipped titles including Fortnite Mobile                                                                                        |
| **Weighted Composite**     | **4.42** | 5.0 |                                                                                                                                                                                                                                       |

---

## Detailed Assessment by Component

### Technical/Case Study (4.7/5.0)

**Challenge:** Design a memory management system for a mobile game engine that must handle 200MB of active game data with fragmentation below 5%, supporting allocations from 16 bytes to 10MB, with real-time defragmentation capability that does not stall the main thread.

**Approach:** Viktor proposed a hierarchical memory architecture:

1. **Transient pool** — linear allocator with periodic reset (frame-scoped data)
2. **Permanent pool** — segregated fit allocator with size-class buckets
3. **Large object pool** — buddy allocator for assets > 1MB
4. **Defragmentation** — incremental compaction using a background thread with copy-on-write semantics

He demonstrated understanding of lock-free data structures for the inter-pool communication channel and correctly identified that CPU cache line alignment is critical for mobile performance. His proposed fragmentation measurement approach (sampling-based, not full heap scan) was production-tested.

**Strengths:** Production-quality design matching real-world engine architecture; deep understanding of allocator algorithms; practical approach to defragmentation.
**Gaps:** Did not discuss memory-mapped I/O for asset streaming; could have addressed platform-specific large page support.

### System Design (4.5/5.0)

**Challenge:** Design a platform abstraction layer that enables a single C++ codebase to target iOS Metal and Android Vulkan, with platform-specific optimizations while maintaining identical gameplay behavior.

**Approach:** Viktor designed a three-layer abstraction:

- **Hardware Abstraction** — GPU feature detection, capability queries, fallback paths
- **Graphics Abstraction** — unified rendering API translating to Metal/Vulkan command submission
- **Platform Services** — input, file I/O, audio abstracted behind interfaces

He correctly identified that deterministic physics synchronization requires fixed-timestep simulation with platform-independent floating-point behavior (addressing ARM vs x86 FP differences).

**Strengths:** Clean architecture; production-tested pattern from UE5; addressed FP determinism.
**Gaps:** Could have discussed Vulkan pipeline optimization more deeply; did not address Metal's frame pacing advantages.

### Panel Interview (4.4/5.0)

**Key Topics Covered:**

- UE5 memory management internals (strong — described specific allocator changes he made)
- Physics profiler architecture (strong — explained data collection, visualization, and integration with Epic's internal tools)
- CPU/GPU profiling techniques (strong — demonstrated understanding of both sampling and instrumentation approaches)
- Cross-platform multiplayer synchronization (solid — described deterministic physics approach for Fortnite Mobile)

**Panel Feedback:**

- **Dmitri Volkov:** "Exceptional engine-level knowledge. His memory management expertise is exactly what we need. The hierarchical allocator design is production-ready."
- **Software Architect:** "His platform abstraction approach is clean and follows SOLID principles. The deterministic physics solution addresses our multiplayer requirements."
- **CHRO Coordinator:** "Technical depth is exceptional. Answers precise and well-structured. Strong ownership mindset — takes responsibility for engine quality."

### Behavioral (4.2/5.0)

**STAR Response — Introducing Engineering Standards:**

- **Situation:** At Epic, engine code reviews were ad-hoc, leading to production bugs reaching the main branch.
- **Task:** Viktor needed to establish review standards without disrupting development velocity.
- **Action:** He created a mandatory checklist covering memory safety, thread safety, performance impact, and API contract compliance. He piloted it with his pod of 6, then expanded to the full engine team.
- **Result:** Production bugs from engine changes dropped by 35%. The checklist was adopted as the standard for all engine PRs.

**Leadership Evidence:** Led engine pod of 6; mentored 3 junior programmers; introduced code review standards adopted team-wide.

### Portfolio (4.4/5.0)

| Artifact                                     | Quality | Relevance |
| -------------------------------------------- | ------- | --------- |
| UE5 memory management contributions          | 5/5     | 5/5       |
| Physics profiler (200+ users)                | 5/5     | 4/5       |
| Platform abstraction layer                   | 4/5     | 5/5       |
| Deterministic physics sync (Fortnite Mobile) | 4/5     | 5/5       |

---

## Percentile Ranking

| Percentile | Composite Score | Interpretation   |
| ---------- | --------------- | ---------------- |
| 99th       | 4.50+           | Exceptional      |
| **96th**   | **4.42**        | **Elite — Hire** |
| 90th       | 4.10            | Strong — Hire    |
| 80th       | 3.80            | Good — Consider  |

Viktor Stahl scores **4.42/5.0**, placing him in the **96th percentile**.

---

## Interview Panel Recommendation

| Panelist           | Recommendation | Confidence |
| ------------------ | -------------- | ---------- |
| Dmitri Volkov      | Strong Hire    | High       |
| Software Architect | Strong Hire    | High       |
| CHRO Coordinator   | Hire           | High       |

**Consensus:** Unanimous recommendation to advance to Stage 5 (Vetting Gate).

---

**Gate Status:** ✅ Composite score 4.42/5.0 (96th percentile) — well above 80th percentile threshold. Proceeding to Stage 5.
