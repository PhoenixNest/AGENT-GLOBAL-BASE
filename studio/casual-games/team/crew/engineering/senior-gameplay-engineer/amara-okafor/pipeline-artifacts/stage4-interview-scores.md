---
document_id: "**"
gate_status: "** ✅ Composite score 4.31/5.0 (95th percentile) — well above 80th percentile threshold. Proceeding to Stage 5."
candidate_name: "Amara Okafor"
entity_type: "studio"
stage: "stage-4"
division: "engineering"
role: "senior-gameplay-engineer"
document_type: "Interview Scores"
---

# Stage 4: Interview Scores (G12) — Amara Okafor

**Role:** Senior Gameplay Engineer #2 (G12)
**Candidate:** Amara Okafor
**Interview Period:** 2026-04-12 to 2026-04-14
**Interview Panel:** Dmitri Volkov (Sr. Game Engineer), Lead QA Engineer, CHRO Panel Coordinator
**Document ID:** INT-2026-G12-001

---

## Interview Component Scores

| Component                  | Score    | Max | Notes                                                                                                                                                                               |
| -------------------------- | -------- | --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Technical/Case Study       | 4.5      | 5.0 | UI framework architecture excellent; proposed batched rendering pattern for mobile; input pipeline design robust with clear separation of concerns                                  |
| System Design              | 4.5      | 5.0 | Designed modular UI framework with event-driven architecture; addressed scalability for 250M+ MAU; identified trade-offs between reactive and polling approaches                    |
| Panel Interview            | 4.3      | 5.0 | Strong on animation integration; Spine 2D workflow demonstrated well; networking knowledge solid with understanding of client-side prediction and server reconciliation for UI sync |
| Behavioral                 | 4.2      | 5.0 | Led UI team of 4 at King; mentored 2 junior engineers; described conflict resolution between UI and gameplay teams using data-driven approach                                       |
| Portfolio / Public Signals | 4.2      | 5.0 | 250M+ MAU UI framework (Candy Crush Saga); published optimization guide on mobile UI performance; 2 shipped titles with documented UI contributions                                 |
| **Weighted Composite**     | **4.31** | 5.0 |                                                                                                                                                                                     |

---

## Detailed Assessment by Component

### Technical/Case Study (4.5/5.0)

**Challenge:** Design a UI rendering system for a casual game targeting mid-tier Android devices (Snapdragon 600 series), with the requirement of 60fps under heavy UI load (200+ UI elements visible simultaneously).

**Approach:** Amara proposed a three-layer architecture:

1. **Static layer** — pre-baked, texture-atlased, single draw call per screen
2. **Semi-dynamic layer** — batched with dirty-rectangle invalidation
3. **Dynamic layer** — individual elements with capped draw calls

She correctly identified that the primary bottleneck is not CPU but GPU fill-rate on mobile, and proposed a solution that reduces draw calls from 120 to 35 per screen (matching her actual achievement at King). She also proposed a texture streaming system to manage memory pressure.

**Strengths:** Deep understanding of mobile GPU constraints; practical approach to batching; clear reasoning about trade-offs.
**Gaps:** Did not address Vulkan-specific optimization paths; could have discussed Metal-specific features for iOS.

### System Design (4.5/5.0)

**Challenge:** Design an input handling system that supports touch, gamepad, and keyboard, with the ability to remap controls and support accessibility features (one-handed mode, alternative input).

**Approach:** Amara designed an abstraction layer with:

- Raw input capture (platform-specific)
- Normalized input events (platform-agnostic)
- Input action mapping (configurable, data-driven)
- Contextual action resolver (game-state aware)

She demonstrated the same pattern she used at King for unifying input across 4 titles, with concrete examples of how touch swipe and gamepad D-pad both map to the same abstracted navigation action.

**Strengths:** Clean architecture; data-driven approach enables easy remapping; accessibility considered from the ground up.
**Gaps:** Did not discuss input latency measurement; could have addressed haptic feedback integration.

### Panel Interview (4.3/5.0)

**Key Topics Covered:**

- Spine 2D animation integration with gameplay events (strong — described Candy Crush character animation system in detail)
- Real-time UI synchronization for co-op features (solid — described optimistic updates with server reconciliation)
- UI performance profiling on mobile devices (strong — demonstrated use of Mali GPU profiling tools)
- Handling text expansion in localized UIs (moderate — acknowledged limited localization experience but described adaptive layout patterns)

**Panel Feedback:**

- **Dmitri Volkov:** "Excellent technical depth. Her approach to UI rendering at scale is exactly what we need. The three-layer architecture is production-tested."
- **Lead QA Engineer:** "Her approach to UI testing through data-bound components is well-structured. Would reduce our UI regression rate significantly."
- **CHRO Coordinator:** "Clear communicator. Answers specific and detailed. No deflection. Ownership mindset evident."

### Behavioral (4.2/5.0)

**STAR Response — Leading Through Technical Disagreement:**

- **Situation:** At King, the gameplay team wanted a complex animated UI element that would break the 60fps budget.
- **Task:** Amara needed to push back without blocking the feature.
- **Action:** She profiled the proposed animation, identified the bottleneck (overdraw from particle effects), and proposed an alternative using sprite sheets with frame-level GPU instancing.
- **Result:** The feature shipped at 60fps with 30% lower GPU time than the original proposal, and the animation team adopted her sprite sheet pattern for future work.

**Leadership Evidence:** Led UI team of 4; mentored 2 junior engineers; introduced UI performance benchmarks adopted team-wide.

### Portfolio (4.2/5.0)

| Artifact                               | Quality | Relevance |
| -------------------------------------- | ------- | --------- |
| Candy Crush UI framework               | 5/5     | 5/5       |
| Published mobile UI optimization guide | 4/5     | 5/5       |
| Spine 2D animation integration         | 4/5     | 4/5       |
| Input unification across 4 King titles | 4/5     | 5/5       |

---

## Percentile Ranking

| Percentile | Composite Score | Interpretation         |
| ---------- | --------------- | ---------------------- |
| 99th       | 4.50+           | Exceptional            |
| **95th**   | **4.31**        | **Elite — Hire**       |
| 90th       | 4.10            | Strong — Hire          |
| 80th       | 3.80            | Good — Consider        |
| 70th       | 3.50            | Adequate — Conditional |
| Below 70th | < 3.50          | Insufficient — Reject  |

Amara Okafor scores **4.31/5.0**, placing her in the **95th percentile** of all candidates assessed for this role family.

---

## Interview Panel Recommendation

| Panelist         | Recommendation | Confidence |
| ---------------- | -------------- | ---------- |
| Dmitri Volkov    | Strong Hire    | High       |
| Lead QA Engineer | Hire           | High       |
| CHRO Coordinator | Strong Hire    | High       |

**Consensus:** Unanimous recommendation to advance to Stage 5 (Vetting Gate).

---

**Gate Status:** ✅ Composite score 4.31/5.0 (95th percentile) — well above 80th percentile threshold. Proceeding to Stage 5.
