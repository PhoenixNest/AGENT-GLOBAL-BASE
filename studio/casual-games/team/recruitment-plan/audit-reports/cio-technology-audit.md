# Dr. Priya Mehta — Technology Infrastructure & Architecture Audit

**Auditor:** Dr. Priya Mehta, CIO
**Date:** April 12, 2026
**Scope:** Backend infrastructure, cloud services, data architecture, technology risk
**Verdict:** CONDITIONAL GO

---

## Executive Summary

The Casual Games Studio recruitment is complete (38 FTEs + 1 Contract). This audit assesses technology infrastructure readiness from Stage 3 (Vertical Slice) through Stage 5 (Full Production).

**Overall Verdict: CONDITIONAL GO**

The studio has **world-class PlayFab backend capability** through Priya Nair (Senior Backend Engineer), who is the architect of the very abstraction layer pattern the studio intends to use. The team is excellent at game development but has **gaps in data privacy, compliance, and data engineering** that the parent company must address. Two P0/P1 risks require immediate action before Stage 3 entry.

---

## Audit Checklist

### Item 1: Backend Abstraction Layer Design (IAuthService, IDataService, IEconomyService)

**Verdict: ✅ PASS**

**Evidence:**

- **Priya Nair (Senior Backend Engineer)** is the designer of the reference PlayFab abstraction pattern. Her background at PlayFab includes designing the IAuthService, IDataService, IEconomyService interfaces that became PlayFab's customer reference implementation.
- Skill file `backend-abstraction-layer.md` explicitly covers interface-based architecture, adapter patterns, and dependency injection with C# 11.0 and .NET DI Container 7.0.
- Adapter swap time target: <= 1 week of development. P99 latency target: <= 200ms.
- **Aisha Bello (Backend Engineer)** implements API wrappers conforming to these interfaces. Her skill file confirms "interface contract compliance: 100% of defined methods."

**Assessment:** Priya Nair can absolutely implement this with a self-hosting adapter. The abstraction layer pattern is her core competency — it's the reference implementation she designed at PlayFab.

**Minor concern:** Both profiles note limited experience with on-premises/bare-metal deployment. The self-hosting adapter will need infrastructure support from David Okafor (Live Ops Engineer, Kubernetes/AWS).

---

### Item 2: PlayFab Integration Capability (Cloud Script, Player Data, Leaderboards, Economy)

**Verdict: ✅ PASS**

**Evidence:**

- **Priya Nair:** 6 years PlayFab experience. Built economy service handling 50M+ daily transactions. Full SDK coverage: Cloud Script, Azure Functions, Azure Cosmos DB, Event Grid, PlayStream. Anti-cheat framework reduced fraudulent transactions by 92%.
- **Aisha Bello:** 3 live titles with PlayFab SDK integration. 50+ Cloud Script functions in C#. Full coverage of authentication, economy, and cloud script.
- **Dmitri Volkov (Sr. Game Engineer):** Lists PlayFab in his game-engineering-architecture.md skill under "Backend services (abstraction layer)."

**Assessment:** PlayFab integration capability is comprehensively covered. Priya Nair owns the architecture; Aisha Bello owns implementation. Both have shipped production titles with the exact feature set required.

---

### Item 3: Self-Hosted Server Adapter Capability (PlayFab Migration Path)

**Verdict: ⚠️ CONDITIONAL PASS**

**Evidence supporting:**

- Priya Nair's `playfab-anti-cheat.md` skill explicitly lists the trade-off: "PlayFab vs self-hosted -> PlayFab for speed-to-market; self-hosted adapter ready for migration."
- The backend abstraction layer is designed for this exact scenario — swap providers with < 1 week of adapter work.
- **David Okafor (Live Ops Engineer)** brings Kubernetes, AWS, CI/CD, and blue-green deployment expertise — the infrastructure layer needed for self-hosting.

**Gaps identified:**

- **No dedicated DevOps/Platform Engineer role.** David Okafor's skills are in CI/CD and server operations, but he's in the Live Ops division (post-launch). During Stages 3–5 (pre-launch), there is no dedicated infrastructure owner.
- **Priya Nair's honest gap:** "Primarily cloud-native; limited experience with bare-metal server deployment."
- **Aisha Bello's honest gap:** "Limited experience with server deployment, containerization, or CI/CD for backend services."

**Assessment:** The _architecture_ supports migration. The _team_ has the individual pieces (Priya Nair's abstraction layer + David Okafor's infrastructure skills) but no one who has _done_ a full PlayFab-to-self-hosted migration end-to-end. This is a risk for Stage 5+ if migration is actually triggered.

**Recommendation:** Before Stage 5, commission a proof-of-concept self-hosted adapter for one service (e.g., IAuthService) to validate the migration path. This should be a Stage 3/4 ADR deliverable.

---

### Item 4: Data Export Pipeline (PlayFab Events -> Kafka -> Data Lake -> BI)

**Verdict: ⚠️ CONDITIONAL PASS**

**Evidence supporting:**

- **Aisha Bello** built a "PlayFab Events -> Kafka export pipeline" at Space Ape Games. Her skill file specifies: "Data pipeline latency: <= 30s from event to Kafka."
- **David Okafor** designed "real-time event tracking pipeline for post-deploy monitoring."
- **Yuki Tanaka (Data Analyst)** from Live Ops owns the BI/analytics consumption layer — built 10+ dashboards at Zynga, advanced SQL/Python proficiency.

**Gaps identified:**

- **Data Lake segment (S3/Azure Blob):** No one on the team has explicitly documented experience with data lake architecture or configuration. Aisha Bello's pipeline stops at Kafka. The Kafka -> Data Lake -> BI leg has no identified owner.
- **Yuki Tanaka's honest gap:** "Most work is batch-oriented; has not built real-time streaming analytics pipelines." This means the real-time Kafka consumer -> BI dashboard pipeline has a skills gap.
- **No Data Engineer role.** The pipeline requires someone to design the Kafka consumer, data lake schema, partitioning strategy, and BI integration. This falls between Aisha Bello (who handles PlayFab -> Kafka) and Yuki Tanaka (who consumes the data) with no bridge.

**Assessment:** The PlayFab Events -> Kafka segment is covered by Aisha Bello. The Data Lake -> BI segment is _partially_ covered by Yuki Tanaka (analyst, not engineer). The Kafka -> Data Lake connector has **no identified owner**.

**Recommendation:** Assign the Kafka -> Data Lake -> BI pipeline ownership to David Okafor (Live Ops Engineer) as an infrastructure task, with Aisha Bello providing the Kafka producer and Yuki Tanaka defining the BI schema requirements. Alternatively, hire or contract a Data Engineer before Stage 5.

---

### Item 5: Unity Licensing Risk

**Verdict: ❌ FAIL**

**Evidence:**

- My Strategic Brief assessment (Section 2.4) explicitly recommended: "Commission Unity licensing legal review (Week 1–2)" and "Contractually negotiate fixed pricing for 3+ years. Maintain documented exit plan (Godot/Unreal migration assessment)."
- The Strategic Brief risk register lists R4: "Unity licensing policy change" (P1, Owner: CIO).
- **No evidence in any team profile, skill file, or studio document that Unity licensing has been reviewed.** No legal review has been commissioned. No fixed-price contract negotiated. No exit plan documented.

**Assessment:** This is an unresolved P1 risk from the Strategic Brief. Unity's 2024 runtime fee policy change demonstrated real financial risk. The studio is building entirely on Unity 6.3 LTS with no contractual protection and no documented migration path.

**Recommendation:**

1. Commission Unity licensing legal review immediately (Week 1–2 of studio setup).
2. Negotiate fixed-price Unity Enterprise contract for 3+ years.
3. Commission a Godot/Unreal migration assessment (lightweight — 1–2 week effort) as a hedge.
4. Document this as ADR-001: "Unity Engine Selection with Exit Strategy."

---

### Item 6: Multi-Tenant Backend Architecture

**Verdict: ⚠️ CONDITIONAL PASS**

**Evidence supporting:**

- My Strategic Brief assessment explicitly mandated: "Build for multi-tenancy from Day 1 — even with one game, architect backend as multi-tenant. Retrofit cost is 3–5x original investment."
- **Priya Nair** migrated a monolithic architecture to microservices at PlayFab, reducing P99 latency from 800ms to 120ms. Microservices architecture inherently supports multi-tenancy patterns.
- The backend abstraction layer design supports per-tenant configuration through dependency injection.

**Gaps identified:**

- **No one owns the multi-tenancy design explicitly.** Priya Nair's skills cover microservices and abstraction layers, but multi-tenancy (tenant isolation, data partitioning, per-tenant configuration, billing metering) is a distinct architectural concern.
- **No data architect or database specialist** on the team. Multi-tenancy requires decisions about schema-per-tenant vs. row-level isolation vs. database-per-tenant, and no one on the roster has documented expertise in this area.
- Dmitri Volkov's honest gap: "Backend infrastructure and cloud services are outside his core competency (delegated to Senior Backend Engineer)."

**Assessment:** The team has the _capability_ to build multi-tenant architecture (Priya Nair's microservices background), but no one has been explicitly assigned this responsibility, and no team member has documented multi-tenancy design experience.

**Recommendation:**

1. Assign multi-tenancy design ownership to Priya Nair as a Stage 3 deliverable.
2. Require an ADR specifically on multi-tenant architecture strategy (data isolation model, tenant onboarding, cross-tenant data sharing boundaries).
3. I (CIO) will review this ADR during Stage 3 gate review.

---

### Item 7: Technology Risk Register — Unresolved Risks from Strategic Brief

**Verdict: ⚠️ CONDITIONAL PASS**

Reviewing the Strategic Brief risk register:

| ID  | Risk                                       | Severity | Status        | Assessment                                                                        |
| --- | ------------------------------------------ | -------- | ------------- | --------------------------------------------------------------------------------- |
| R1  | No internal game dev expertise             | P0       | Resolved      | Recruitment complete — 38 FTEs hired including experienced game engineers         |
| R2  | Capital burn without proven unit economics | P0       | Pending       | Depends on Phase 1 execution and soft launch results — not a technology risk      |
| R3  | COPPA / minors data compliance failure     | P0       | Not addressed | No evidence COPPA compliance assessment has begun. No privacy engineer on roster. |
| R4  | Unity licensing policy change              | P1       | Not addressed | See Item 5 above. No legal review, no contract, no exit plan.                     |
| R5  | Brand dilution from game failures          | P1       | Addressed     | House of brands architecture established in Strategic Brief                       |
| R6  | Cultural mismatch with game talent         | P1       | Mitigated     | Separate department structure established                                         |
| R7  | App binary size exceeds limits             | P1       | Pending       | Technology exists (Addressables, IL2CPP) but not yet implemented                  |
| R8  | Performance on low-end Android             | P1       | Team capable  | Viktor Stahl + Priya Subramanian bring deep profiling/optimization expertise      |
| R9  | Game economy fails ARPDAU target           | P1       | Pending       | Business risk, not technology                                                     |
| R10 | Third-party SDK conflicts                  | P2       | Pending       | SDK vetting process defined in game-security-anti-cheat.md but not yet executed   |

**Unresolved technology risks requiring immediate action:**

- **R3 (COPPA):** No privacy engineer, no compliance assessment initiated. The data pipeline (PlayFab Events -> Kafka -> Data Lake) processes player data that may include minors' data. This is a legal and technical risk.
- **R4 (Unity licensing):** See Item 5.
- **R10 (SDK conflicts):** SDK vetting checklist exists in `game-security-anti-cheat.md` Section 5.2, but no one has been assigned SDK compatibility assessment.

---

### Item 8: Infrastructure/Technology Skill Gaps — Stage 3 and Stage 5 Blockers

**Verdict: ⚠️ CONDITIONAL PASS**

| Gap Area                                  | Impact on Stage 3 (Vertical Slice)                           | Impact on Stage 5 (Full Production)                                       | Mitigation Available                                |
| ----------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------- | --------------------------------------------------- |
| **No Data Engineer**                      | Low — analytics can be deferred                              | **High** — Kafka -> Data Lake -> BI pipeline has no owner                 | Assign to David Okafor + contract support           |
| **No Privacy/Compliance Engineer**        | **Medium** — COPPA affects data collection design from Day 1 | **High** — production data collection without COPPA compliance is illegal | Engage legal counsel + CSO (Dr. Sarah Chen)         |
| **No dedicated DevOps/Platform Engineer** | Low — cloud services (PlayFab) handle infrastructure         | **Medium** — self-hosted migration path, CI/CD for backend services       | David Okafor can cover; Priya Nair can design       |
| **No Database Specialist**                | Low — PlayFab manages data                                   | **Medium** — multi-tenancy design, data lake schema                       | Priya Nair (Cosmos DB experience) + external review |
| **Unity licensing unresolved**            | **High** — all development assumes Unity                     | **High** — sunk cost increases with each sprint                           | Immediate legal review required                     |
| **COPPA compliance unresolved**           | **High** — data architecture must be COPPA-aware from Day 1  | **Critical** — production launch without COPPA = legal liability          | CSO engagement required immediately                 |

**Critical finding:** The team is **excellent at game development** but has **no coverage for data privacy, compliance, or data engineering.** These are not game-specific skills — they're infrastructure and governance skills that the parent company should provide to the studio.

---

## Risk Assessment

### Risk Summary Matrix

| Risk                            | Likelihood | Impact   | Severity | Owner       | Timeline  |
| ------------------------------- | ---------- | -------- | -------- | ----------- | --------- |
| Unity licensing change          | Medium     | High     | P1       | CIO + Legal | Immediate |
| COPPA compliance failure        | Medium     | Critical | P0       | CIO + CSO   | Immediate |
| Data pipeline gap (Kafka->Lake) | Low        | Medium   | P2       | CIO         | Stage 4–5 |
| Self-hosted migration untested  | Low        | Medium   | P2       | Sr. Backend | Stage 5   |
| Multi-tenancy design undefined  | Low        | Medium   | P2       | Sr. Backend | Stage 3   |
| SDK compatibility conflicts     | Medium     | Low      | P3       | CTO         | Stage 4   |

### Key Observations

1. **The backend team is world-class for PlayFab integration.** Priya Nair and Aisha Bello together represent one of the strongest PlayFab backend pairs I've seen in any mobile game studio. The abstraction layer pattern is the right architectural choice, and both engineers have shipped it in production.

2. **The data pipeline has a structural gap.** PlayFab -> Kafka is covered. Kafka -> Data Lake -> BI is not. This is not a skills problem per se — it's a _role_ problem. No Data Engineer was recruited.

3. **COPPA is the highest-priority unresolved risk.** If any game attracts users under 13, the entire data architecture (PlayFab Events -> Kafka -> Data Lake -> BI) must be COPPA-compliant. This affects data collection, storage, retention, and access policies. No one on the studio roster has privacy engineering expertise.

4. **Unity licensing is a governance gap, not a technical gap.** The team can build on Unity. The question is contractual and financial. This needs legal engagement, not engineering.

5. **The team's self-hosted capability is theoretical, not proven.** The abstraction layer _supports_ migration, but no one has executed a full migration from PlayFab to self-hosted. A proof-of-concept is needed before Stage 5.

---

## Sign-Off Decision

### CONDITIONAL GO

| #   | Condition                                         | Owner       | Deadline | Priority |
| --- | ------------------------------------------------- | ----------- | -------- | -------- |
| C1  | Commission Unity licensing legal review           | CIO + Legal | Week 2   | P1       |
| C2  | Initiate COPPA compliance assessment              | CIO + CSO   | Week 3   | P0       |
| C3  | Assign multi-tenancy ADR to Priya Nair            | CIO         | Stage 3  | P2       |
| C4  | Assign Kafka -> Data Lake -> BI ownership         | CIO         | Stage 4  | P2       |
| C5  | Commission self-hosted adapter PoC (IAuthService) | Sr. Backend | Stage 4  | P2       |

**Rationale:**

**What's strong:**

- Backend abstraction layer design: World-class capability (Priya Nair designed the PlayFab reference pattern)
- PlayFab integration: Two engineers with combined 9 years of PlayFab experience and shipped titles
- Anti-cheat and server-side validation: Priya Nair's 92% fraud reduction record
- Game engineering architecture: Dmitri Volkov's Niantic/Unity Technologies background
- Infrastructure operations: David Okafor's 99.95% uptime track record at 5M DAU

**What needs attention:**

- Unity licensing: Unresolved P1 risk. Legal review is overdue per Strategic Brief timeline.
- COPPA compliance: Unresolved P0 risk. Data architecture decisions made without COPPA awareness will be costly to retrofit.
- Data pipeline: Kafka -> Data Lake -> BI segment has no owner.
- Multi-tenancy: Not yet assigned. Must be Stage 3 deliverable.

**What does NOT block Stage 3:**

- Self-hosted migration (can be deferred to Stage 4–5 with PoC)
- Data pipeline completion (can be built incrementally)
- Multi-tenancy (must be designed in Stage 3, but doesn't block starting)

**What DOES block Stage 3 if not addressed:**

- COPPA compliance assessment — data collection architecture cannot be finalized without knowing COPPA requirements.

---

**Signed:** Dr. Priya Mehta, CIO
**Date:** April 12, 2026
