# Stage 4: Interview Scores (G14) — Priya Nair

**Role:** Senior Backend Engineer (G14)
**Candidate:** Priya Nair
**Interview Period:** 2026-04-13 to 2026-04-15
**Interview Panel:** Dmitri Volkov (Sr. Game Engineer), Security Architect, CHRO Panel Coordinator
**Document ID:** INT-2026-G14-001

---

## Interview Component Scores

| Component                  | Score    | Max | Notes                                                                                                                                                                                          |
| -------------------------- | -------- | --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Technical/Case Study       | 4.6      | 5.0 | Backend abstraction layer design excellent; proposed clean interface pattern for IAuthService/IDataService/IEconomyService; demonstrated PlayFab integration architecture with Azure Functions |
| System Design              | 4.5      | 5.0 | Designed microservices migration from monolith; addressed P99 latency optimization (800ms→120ms); proposed event-driven architecture with Event Grid for real-time analytics                   |
| Panel Interview            | 4.3      | 5.0 | Deep PlayFab platform knowledge; anti-cheat framework design strong with server-authoritative validation; Cloud Script patterns well explained; discussed Cosmos DB partitioning strategies    |
| Behavioral                 | 4.2      | 5.0 | Led team of 5 at PlayFab; mentored 3 backend engineers; described introducing server-side validation standards adopted across PlayFab services                                                 |
| Portfolio / Public Signals | 4.4      | 5.0 | PlayFab economy service handling 50M+ daily transactions; anti-cheat framework (92% fraud reduction); backend abstraction layer as PlayFab reference implementation                            |
| **Weighted Composite**     | **4.38** | 5.0 |                                                                                                                                                                                                |

---

## Detailed Assessment by Component

### Technical/Case Study (4.6/5.0)

**Challenge:** Design a backend abstraction layer for a mobile game that must support PlayFab integration while keeping gameplay code platform-agnostic. The system must handle authentication, player data persistence, economy transactions, and real-time multiplayer coordination.

**Approach:** Priya designed a clean interface-based abstraction:

- `IAuthService` — login, session management, token refresh
- `IDataService` — player profile, inventory, progression persistence
- `IEconomyService` — currency, IAP, virtual goods transactions
- `IMultiplayerService` — matchmaking, session management, real-time sync

Each interface has a PlayFab-specific adapter implementing the contract, allowing gameplay code to depend only on abstractions. She demonstrated the same pattern she designed at PlayFab as the reference implementation.

**Strengths:** Clean separation of concerns; platform-agnostic gameplay code; testable via mock implementations.
**Gaps:** Could have discussed fallback behavior when PlayFab is unavailable.

### System Design (4.5/5.0)

**Challenge:** Design a backend architecture for a casual game expecting 1M DAU, with economy transactions requiring server-authoritative validation and P99 latency under 200ms.

**Approach:** Priya designed an event-driven microservices architecture:

- API Gateway routing to service-specific Azure Functions
- Cosmos DB with partitioning strategy by player ID
- Event Grid for async processing (analytics, notifications)
- Server-authoritative economy validation with anti-cheat checks before transaction commit

She described her actual migration from monolith to microservices at PlayFab, reducing P99 from 800ms to 120ms through service decomposition and database optimization.

**Strengths:** Production-tested architecture; clear latency optimization strategy; anti-cheat built into transaction flow.
**Gaps:** Did not discuss disaster recovery or multi-region failover.

### Panel Interview (4.3/5.0)

**Key Topics Covered:**

- PlayFab economy service internals (strong — described 50M+ daily transaction handling)
- Anti-cheat validation framework (strong — 92% fraud reduction through server-authoritative validation)
- Cloud Script patterns (solid — described 50+ functions for economy, progression, events)
- Cosmos DB partitioning strategy (strong — player ID partitioning for optimal query patterns)

**Panel Feedback:**

- **Dmitri Volkov:** "Exceptional backend architecture knowledge. Her abstraction layer design is exactly what we need for clean PlayFab integration."
- **Security Architect:** "Server-authoritative economy validation is the correct approach for anti-cheat. Her 92% fraud reduction speaks for itself."
- **CHRO Coordinator:** "Clear, confident communicator. Technical depth is excellent. Strong ownership of backend quality."

### Behavioral (4.2/5.0)

**STAR Response — Introducing Standards:**

- **Situation:** PlayFab services had inconsistent server-side validation, leading to exploitable gaps.
- **Task:** Priya needed to establish validation standards across all PlayFab services.
- **Action:** She designed a validation framework with pre-commit checks, server-authoritative economy rules, and automated test suites. Piloted on her team's economy service.
- **Result:** Fraudulent transactions dropped 92%. Framework adopted as PlayFab standard.

**Leadership Evidence:** Led team of 5; mentored 3 backend engineers; introduced validation standards adopted platform-wide.

### Portfolio (4.4/5.0)

| Artifact                                              | Quality | Relevance |
| ----------------------------------------------------- | ------- | --------- |
| PlayFab economy service (50M+ daily txns)             | 5/5     | 5/5       |
| Anti-cheat framework (92% fraud reduction)            | 5/5     | 5/5       |
| Backend abstraction layer (reference impl.)           | 4/5     | 5/5       |
| Monolith-to-microservices migration (P99 800ms→120ms) | 4/5     | 4/5       |

---

## Percentile Ranking

| Percentile | Composite Score | Interpretation   |
| ---------- | --------------- | ---------------- |
| 99th       | 4.50+           | Exceptional      |
| **96th**   | **4.38**        | **Elite — Hire** |
| 90th       | 4.10            | Strong — Hire    |

Priya Nair scores **4.38/5.0**, placing her in the **96th percentile**.

---

## Interview Panel Recommendation

| Panelist           | Recommendation | Confidence |
| ------------------ | -------------- | ---------- |
| Dmitri Volkov      | Strong Hire    | High       |
| Security Architect | Strong Hire    | High       |
| CHRO Coordinator   | Hire           | High       |

**Consensus:** Unanimous recommendation to advance to Stage 5 (Vetting Gate).

---

**Gate Status:** ✅ Composite score 4.38/5.0 (96th percentile). Proceeding to Stage 5.
