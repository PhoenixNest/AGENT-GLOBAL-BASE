# Stage 4: Interview Scores (G19) — Aisha Bello

**Role:** Backend Engineer (G19)
**Candidate:** Aisha Bello
**Interview Period:** 2026-04-12 to 2026-04-14
**Interview Panel:** Dmitri Volkov (Sr. Game Engineer), Priya Nair (Sr. Backend Engineer, G14), CHRO Panel Coordinator
**Document ID:** INT-2026-G19-001

---

## Interview Component Scores

| Component                  | Score    | Max | Notes                                                                                                                                                                    |
| -------------------------- | -------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Technical/Case Study       | 4.1      | 5.0 | PlayFab SDK integration challenge — implemented authentication and economy SDK with clean API wrapper; Cloud Script functions well-structured with proper error handling |
| System Design              | 3.8      | 5.0 | API wrapper design exercise showed solid implementation skills; implements interfaces designed by Senior Backend Engineer                                                |
| Panel Interview            | 4.0      | 5.0 | Strong PlayFab SDK knowledge; described 50+ Cloud Script functions in detail; data pipeline architecture (PlayFab Events -> Kafka) well explained                        |
| Behavioral                 | 3.9      | 5.0 | Collaborative team player; described building API wrapper layer that abstracted PlayFab from gameplay code; still developing system architecture skills                  |
| Portfolio / Public Signals | 4.1      | 5.0 | 3 live titles with PlayFab integration; 50+ Cloud Script functions; API wrapper layer design; PlayFab Events -> Kafka pipeline                                           |
| **Weighted Composite**     | **4.02** | 5.0 |                                                                                                                                                                          |

---

## Detailed Assessment by Component

### Technical/Case Study (4.1/5.0)

**Challenge:** Implement a PlayFab SDK integration for a mobile game, including authentication, economy transactions, and Cloud Script functions for player progression.

**Approach:** Aisha designed a clean integration with:

- SDK initialization with offline fallback
- Economy transaction wrapper with server-side validation
- Cloud Script functions for player progression with error handling
- Interface-based API wrapper abstracting PlayFab-specific calls from gameplay code

**Strengths:** Clean implementation following established patterns; good error handling; practical approach to SDK integration.
**Gaps:** Did not discuss rate limiting or retry strategies; could have addressed PlayFab title configuration management.

### System Design (3.8/5.0)

**Challenge:** Design an API wrapper layer that abstracts PlayFab-specific calls from gameplay code, allowing easy switching to alternative backend providers.

**Approach:** Aisha designed interface-conformant adapters with PlayFab-specific implementation behind a common interface.

**Strengths:** Followed the pattern she designed at Space Ape Games; clean separation of concerns; testable via mock implementations.
**Gaps:** Implements interfaces designed by Senior Backend Engineer rather than designing abstractions independently.

### Panel Interview (4.0/5.0)

**Key Topics Covered:**

- PlayFab SDK integration (strong — described 3 live title integrations in detail)
- Cloud Script functions (strong — 50+ functions for economy, progression, events)
- API wrapper layer design (solid — interface-conformant adapters pattern)
- Data pipeline (strong — PlayFab Events -> Kafka export for real-time analytics)

**Panel Feedback:**

- **Dmitri Volkov:** "Solid backend engineer with good PlayFab experience. Her SDK integration work at Space Ape Games is exactly the level we need for mid-level backend work."
- **Priya Nair:** "Good implementation skills. She can take backend architecture decisions and implement them correctly. Her PlayFab experience will be valuable for our Cloud Script development. Still developing abstraction design skills but that's expected."
- **CHRO Coordinator:** "Clear communicator. Answers specific with project examples. Good team collaborator."

### Behavioral (3.9/5.0)

**STAR Response — API Wrapper Design:**

- **Situation:** At Space Ape Games, gameplay code was tightly coupled to PlayFab-specific APIs, making testing difficult and provider switching impossible.
- **Task:** Aisha was tasked with creating an abstraction layer.
- **Action:** She designed interface-conformant adapters with PlayFab-specific implementations behind common interfaces (IAuthService, IEconomyService). Gameplay code depends only on interfaces.
- **Result:** Testing became possible via mock implementations. Code review feedback improved because gameplay and backend concerns were separated.

**Leadership Evidence:** Still developing as a leader; no formal mentoring experience; implements interfaces designed by senior engineers.

### Portfolio (4.1/5.0)

| Artifact                                | Quality | Relevance |
| --------------------------------------- | ------- | --------- |
| PlayFab SDK integration (3 live titles) | 4/5     | 5/5       |
| Cloud Script functions (50+)            | 4/5     | 5/5       |
| API wrapper layer design                | 4/5     | 5/5       |
| PlayFab Events -> Kafka pipeline        | 3/5     | 4/5       |

---

## Percentile Ranking

| Percentile | Composite Score | Interpretation  |
| ---------- | --------------- | --------------- |
| 90th       | 4.10            | Strong — Hire   |
| **86th**   | **4.02**        | **Good — Hire** |
| 80th       | 3.80            | Good — Consider |

Aisha Bello scores **4.02/5.0**, placing her in the **86th percentile**.

---

## Interview Panel Recommendation

| Panelist         | Recommendation | Confidence |
| ---------------- | -------------- | ---------- |
| Dmitri Volkov    | Hire           | High       |
| Priya Nair       | Hire           | High       |
| CHRO Coordinator | Hire           | Medium     |

**Consensus:** Unanimous recommendation to advance to Stage 5 (Vetting Gate).

---

**Gate Status:** ✅ Composite score 4.02/5.0 (86th percentile). Proceeding to Stage 5.
