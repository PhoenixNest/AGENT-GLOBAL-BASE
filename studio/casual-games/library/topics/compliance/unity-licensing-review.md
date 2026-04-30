# Unity Licensing Review — Legal & Exit Strategy Assessment

**Document Owner:** Dr. Priya Mehta, CIO
**Co-Owner:** Legal Counsel (external — to be commissioned)
**Audit Reference:** CIO Technology Audit, Item 5 (R4 — Unity Licensing Policy Change)
**Condition:** C1 — Commission Unity licensing legal review
**Severity:** 🟠 P1
**Date:** April 12, 2026
**Status:** Proposed — pending legal review commissioning

---

## 1. Executive Summary

### 1.1 Risk Statement

**R4 — Unity Licensing Policy Change** (🟠 P1, Owner: CIO)

The Casual Games Studio is building entirely on Unity 6.3 LTS with no contractual protection against licensing policy changes, no legal review of Unity's terms, and no documented exit strategy. Unity's 2024 runtime fee policy change demonstrated that licensing terms can shift materially with significant financial exposure. The CIO Technology Audit (Item 5) classified this as a **FAIL** condition, and the Strategic Brief mandated:

> "Commission Unity licensing legal review (Week 1–2). Contractually negotiate fixed pricing for 3+ years. Maintain documented exit plan (Godot/Unreal migration assessment)."

**Condition C1** from the CIO Audit requires this review to be completed by **Week 2** of studio setup as a precondition for Stage 3 (Vertical Slice) entry.

### 1.2 Action Plan

1. **Commission external legal counsel** specializing in software licensing and game engine agreements to review Unity's current Enterprise/Pro terms.
2. **Negotiate a fixed-price Unity Enterprise contract** for 3+ years, eliminating runtime fee exposure.
3. **Produce a lightweight migration assessment** (Godot and Unreal) as a documented exit strategy — 1–2 week effort.
4. **Formalize ADR-001: Unity Engine Selection with Exit Strategy** to record the decision, its consequences, and mitigation measures.

---

## 2. Current Unity Licensing Status

### 2.1 Engine Version

| Parameter          | Value          |
| ------------------ | -------------- |
| **Engine**         | Unity 6.3 LTS  |
| **Release Date**   | Q4 2025        |
| **LTS End Date**   | Q4 2027 (est.) |
| **Support Status** | Active LTS     |

### 2.2 Estimated Seat Count

| Role Category                | Estimated Seats | License Type Needed |
| ---------------------------- | --------------- | ------------------- |
| Engineering (game + backend) | 12              | Pro/Enterprise      |
| Art (3D, UI, VFX, technical) | 8               | Pro                 |
| Design / Production          | 5               | Pro                 |
| QA / Testing                 | 3               | Pro                 |
| **Total**                    | **28**          |                     |

### 2.3 Current Pricing Tier Analysis

| Tier           | Annual Cost/Seat  | Total Annual (28 seats) | Features Relevant to Studio                        |
| -------------- | ----------------- | ----------------------- | -------------------------------------------------- |
| **Personal**   | Free              | $0                      | Revenue cap $200K; no source access                |
| **Pro**        | ~$2,200           | ~$61,600                | Full engine; no source; runtime fees apply         |
| **Enterprise** | Custom (~$4,000+) | ~$112,000+              | Source access; dedicated support; negotiable terms |

**Recommendation:** The studio should pursue **Unity Enterprise** licensing given the seat count (28), the need for contractual protections, and the strategic importance of the engine to the entire product line.

### 2.4 Runtime Fee Exposure Analysis

Unity's 2024 runtime fee policy (subsequently revised after community backlash) proposed charging per-install fees once a game crossed revenue/installation thresholds. Key exposure factors:

| Factor                      | Exposure Level | Notes                                                                      |
| --------------------------- | -------------- | -------------------------------------------------------------------------- |
| **Revenue threshold**       | Medium         | Current policy exempts games below $1M annual revenue                      |
| **Install threshold**       | Medium         | Current policy exempts games below 200K lifetime installs                  |
| **Multi-title aggregation** | **High**       | If fees aggregate across all studio titles, exposure scales with portfolio |
| **Policy revision risk**    | **High**       | Unity has demonstrated willingness to change pricing terms unilaterally    |
| **Contractual protection**  | **None**       | No fixed-price contract in place; subject to Unity's standard terms        |

**Financial Impact Estimate:** If the studio achieves the Strategic Brief target of 5 titles with 1M+ installs each over 3 years, and Unity reinstates per-install fees at even $0.01/install, exposure = 5M installs × $0.01 = **$50,000** in unbudgeted costs. At $0.05/install (original 2024 proposal), exposure = **$250,000**.

**Conclusion:** Runtime fee exposure is a material financial risk that requires contractual mitigation.

---

## 3. Legal Review Action Items

### 3.1 Commission Unity Licensing Legal Review

| Action Item                                                                                                                            | Owner         | Timeline | Status      |
| -------------------------------------------------------------------------------------------------------------------------------------- | ------------- | -------- | ----------- |
| Engage external counsel (game industry licensing specialist)                                                                           | CIO + Legal   | Week 1   | Not started |
| Provide counsel with: Unity EULA, current pricing schedule, Strategic Brief risk register                                              | CIO           | Week 1   | Not started |
| Legal review of Unity licensing terms, including: runtime fee clauses, termination provisions, IP ownership, source code access rights | Legal Counsel | Week 1–2 | Not started |
| Deliverable: Legal Memorandum on Unity Licensing Risk                                                                                  | Legal Counsel | Week 2   | Not started |

### 3.2 Negotiate Fixed-Price Contract

| Action Item                                                                                                     | Owner       | Timeline | Status      |
| --------------------------------------------------------------------------------------------------------------- | ----------- | -------- | ----------- |
| Define contract requirements: 3-year fixed price, runtime fee waiver, source code access, dedicated support SLA | CIO         | Week 1   | Not started |
| Engage Unity Enterprise sales with requirements                                                                 | CIO + Legal | Week 2   | Not started |
| Negotiate terms, including: price lock, renewal options, termination rights, policy change protections          | CIO + Legal | Week 2–3 | Not started |
| Execute signed contract                                                                                         | CIO + Legal | Week 4   | Not started |

**Key Contract Terms to Negotiate:**

| Term                            | Desired Outcome                                         | Rationale                                         |
| ------------------------------- | ------------------------------------------------------- | ------------------------------------------------- |
| **Fixed price**                 | 3-year price lock at negotiated rate                    | Eliminates mid-contract price increases           |
| **Runtime fee waiver**          | Explicit exemption from all per-install/runtime fees    | Eliminates financial exposure from policy changes |
| **Policy change protection**    | Any material policy change triggers renegotiation right | Prevents unilateral term changes                  |
| **Termination for convenience** | 90-day notice, pro-rated refund                         | Enables exit if Unity becomes untenable           |
| **Source code escrow**          | Access to engine source if Unity ceases operations      | Mitigates business continuity risk                |
| **Multi-title coverage**        | Single license covers all studio titles                 | Simplifies licensing as portfolio grows           |

### 3.3 Review Timeline (Week 1–2)

```
Week 1 (Apr 13–19):
├── Day 1–2: Engage legal counsel, provide documentation
├── Day 3–4: Legal counsel reviews Unity EULA, pricing, risk register
├── Day 5: Initial legal findings discussion (CIO + Legal)
└── Deliverable: Preliminary legal risk assessment

Week 2 (Apr 20–26):
├── Day 1–2: Legal counsel drafts formal memorandum
├── Day 3: CIO reviews memorandum, identifies negotiation priorities
├── Day 4: CIO briefs CTO + Studio Director on legal findings
└── Deliverable: Final Legal Memorandum on Unity Licensing Risk
```

---

## 4. Exit Strategy Assessment

### 4.1 Migration Feasibility Analysis

#### 4.1.1 Codebase Migration

| Factor                | Unity → Godot                            | Unity → Unreal                               |
| --------------------- | ---------------------------------------- | -------------------------------------------- |
| **Language**          | C# → GDScript/C# (Godot 4 supports C#)   | C# → C++/Blueprints                          |
| **Script conversion** | Moderate — C# partially reusable         | High effort — full rewrite required          |
| **Scene format**      | Manual conversion required               | Manual conversion required                   |
| **Plugin ecosystem**  | Limited — many Unity plugins unavailable | Mature — but Unity-specific plugins unusable |
| **Estimated effort**  | 4–6 weeks for 2D mini-games              | 8–12 weeks for 2D mini-games                 |

#### 4.1.2 Asset Migration

| Asset Type       | Unity → Godot               | Unity → Unreal           |
| ---------------- | --------------------------- | ------------------------ |
| 2D Sprites/UI    | ✅ Direct import (PNG, SVG) | ✅ Direct import         |
| 3D Models (FBX)  | ✅ Direct import            | ✅ Direct import         |
| Animations       | ⚠️ Manual retargeting       | ⚠️ Manual retargeting    |
| Shaders          | ❌ Full rewrite required    | ❌ Full rewrite required |
| Particle Effects | ❌ Full rebuild required    | ⚠️ Partial rebuild       |
| Audio            | ✅ Direct import            | ✅ Direct import         |

#### 4.1.3 Tooling & Pipeline

| Tool                 | Unity → Godot                                     | Unity → Unreal                                         |
| -------------------- | ------------------------------------------------- | ------------------------------------------------------ |
| Addressables         | ❌ Godot lacks equivalent; custom solution needed | ⚠️ Unreal has Primary Data Assets (partial equivalent) |
| Unity Profiler       | ❌ Godot has built-in profiler (less mature)      | ✅ Unreal Profiler is mature                           |
| Unity Test Framework | ❌ Godot test framework is basic                  | ✅ Unreal Automation Test Framework                    |
| CI/CD Build Pipeline | ⚠️ Requires rebuild of build scripts              | ⚠️ Requires rebuild of build scripts                   |
| PlayFab SDK          | ❌ No official Godot PlayFab SDK                  | ⚠️ Community Unreal PlayFab plugin exists              |

#### 4.1.4 Team Skills Assessment

| Team Member Category   | Unity Proficiency | Godot Readiness           | Unreal Readiness           |
| ---------------------- | ----------------- | ------------------------- | -------------------------- |
| Sr. Game Engineers (3) | Expert            | Moderate (C# helps)       | Low (C++ learning curve)   |
| Game Engineers (6)     | Proficient        | Moderate                  | Low                        |
| Technical Artist (1)   | Expert (HLSL)     | Moderate (GLSL migration) | Moderate (Material Editor) |
| Backend Engineers (2)  | N/A (PlayFab/C#)  | N/A                       | N/A                        |

### 4.2 Estimated Migration Cost and Timeline

| Migration Path     | Engineering Effort | Art/Asset Effort | Tooling Effort | Total Timeline | Estimated Cost (at blended $85/hr) |
| ------------------ | ------------------ | ---------------- | -------------- | -------------- | ---------------------------------- |
| **Unity → Godot**  | 320 hrs            | 160 hrs          | 120 hrs        | 4–6 weeks      | ~$51,000                           |
| **Unity → Unreal** | 640 hrs            | 240 hrs          | 200 hrs        | 8–12 weeks     | ~$91,800                           |
| **Stay on Unity**  | N/A                | N/A              | N/A            | N/A            | ~$61,600/yr (licensing)            |

### 4.3 Risk/Benefit Comparison

| Criterion                           | Stay on Unity             | Migrate to Godot                         | Migrate to Unreal                         |
| ----------------------------------- | ------------------------- | ---------------------------------------- | ----------------------------------------- |
| **Licensing cost**                  | ~$61–112K/yr (negotiable) | Free (MIT license)                       | 5% revenue share after $1M                |
| **Runtime fee risk**                | Mitigated with contract   | None (open source)                       | Moderate (Epic can change terms)          |
| **Team productivity**               | High (existing expertise) | Medium (learning curve 2–4 weeks)        | Low (steep C++ learning curve)            |
| **Asset pipeline maturity**         | High                      | Medium (improving rapidly)               | High                                      |
| **PlayFab integration**             | ✅ Official SDK           | ❌ Community only                        | ⚠️ Community plugin                       |
| **2D mini-game suitability**        | High                      | High                                     | Medium (Unreal is 3D-first)               |
| **Ecosystem & plugin availability** | High                      | Medium                                   | High                                      |
| **Long-term viability**             | Medium (policy risk)      | High (open source, growing)              | High (Epic-backed)                        |
| **Time to production readiness**    | Immediate                 | 4–6 weeks migration + 2 weeks validation | 8–12 weeks migration + 4 weeks validation |
| **Strategic fit for casual games**  | High                      | High                                     | Low (over-engineered for mini-games)      |

### 4.4 Exit Strategy Recommendation

**Primary strategy: Stay on Unity with contractual protections.**

- Negotiate 3-year fixed-price Enterprise contract with runtime fee waiver.
- Quarterly contract review to monitor policy changes.
- Maintain lightweight Godot proof-of-concept for one mini-game (2-week effort) as a validation exercise.

**Secondary strategy (trigger conditions):**

- If Unity materially changes pricing or terms during contract term → activate Godot migration.
- Godot is the recommended exit target due to: C# compatibility, 2D strengths, zero licensing cost, and alignment with casual game complexity.

**Not recommended:** Unreal Engine migration — excessive for 2D mini-games, steep learning curve, higher total cost.

---

## 5. ADR-001: Unity Engine Selection with Exit Strategy

---

adr-id: ADR-001
title: Use Unity 6.3 LTS as primary game engine with documented exit strategy
status: Proposed
date: 2026-04-12
deciders: [CTO, CIO, Studio Director, Software Architect]
supersedes: N/A

---

### Context

The Casual Games Studio is building a portfolio of casual mini-games targeting Android and iOS platforms. The engine selection affects all game engineering, art pipeline, tooling, backend integration (PlayFab), and the studio's long-term technology strategy. The CIO Technology Audit identified Unity licensing as a P1 risk (R4) due to Unity's history of unilateral policy changes (2024 runtime fee controversy) and the absence of any contractual protection or exit strategy.

**Constraints:**

- Studio has recruited 9 Unity-experienced game engineers (3 Sr. + 6 mid-level).
- PlayFab integration is required (official Unity SDK exists; Godot has community-only support).
- Stage 3 (Vertical Slice) timeline requires an engine decision before implementation planning.
- Budget supports Unity Enterprise licensing but requires contractual protections.

**Forces in tension:**

- Team expertise and productivity (strongest with Unity) vs. vendor lock-in risk.
- Speed to market (Unity is production-ready now) vs. long-term licensing uncertainty.
- PlayFab integration quality (Unity official SDK) vs. open-source flexibility (Godot).

### Decision Drivers

- **Driver 1:** Studio has 9 Unity-experienced engineers; retraining would delay Stage 3 by 4–8 weeks.
- **Driver 2:** Unity 6.3 LTS provides stability through Q4 2027.
- **Driver 3:** PlayFab official SDK supports Unity natively; migration to other engines would require custom integration work.
- **Driver 4:** Casual mini-game complexity aligns well with Unity's 2D capabilities.
- **Driver 5:** Licensing risk (R4) must be mitigated through contractual negotiation, not engine replacement.
- **Driver 6:** CIO Audit Condition C1 requires legal review and exit strategy documentation by Week 2.

### Options Considered

#### Option A: Unity 6.3 LTS (Selected)

Unity's industry-standard engine with full 2D/3D support, official PlayFab SDK, C# scripting, and a mature asset ecosystem.

**Pros:**

- Team already trained and proficient (zero ramp-up time).
- Official PlayFab SDK integration (authentication, economy, cloud script, analytics).
- Mature 2D tooling (Sprite Atlas, Tilemap, 2D Animation package).
- Large ecosystem of plugins, assets, and community support.
- LTS version provides stability through Q4 2027.

**Cons:**

- Vendor lock-in risk — Unity controls licensing terms and can change them unilaterally.
- Runtime fee exposure if not contractually mitigated.
- Annual licensing cost (~$61–112K for 28 seats at Enterprise tier).
- Closed-source engine — no ability to self-modify core engine behavior.

**Effort Estimate:** Immediate (already in use).

#### Option B: Godot 4.x

Open-source game engine (MIT license) with C# support, strong 2D capabilities, and growing ecosystem.

**Pros:**

- Zero licensing cost (MIT license — perpetual, royalty-free).
- No vendor lock-in — community-driven, open-source governance.
- C# support in Godot 4 enables partial code reuse from Unity projects.
- Lightweight and well-suited for 2D casual games.
- Growing rapidly — active development community.

**Cons:**

- No official PlayFab SDK — requires community plugin or custom integration.
- Smaller ecosystem — fewer plugins, assets, and learning resources.
- Team requires 2–4 weeks of ramp-up per engineer.
- Less mature tooling for addressable assets, profiling, and testing.
- Migration effort: 4–6 weeks for first mini-game, ~$51,000 estimated cost.

**Effort Estimate:** 4–6 weeks migration + 2 weeks validation per game.

#### Option C: Unreal Engine 5.x

Epic Games' industry-leading engine with Blueprint visual scripting, C++ support, and unparalleled 3D capabilities.

**Pros:**

- Powerful tooling and ecosystem (Marketplace, Nanite, Lumen).
- Community PlayFab plugin exists for Unreal.
- Strong long-term viability (Epic-backed, Fortnite revenue funds development).
- Free until $1M revenue threshold.

**Cons:**

- Over-engineered for 2D casual mini-games — complexity adds overhead.
- Steep learning curve (C++ or Blueprints) — team has zero Unreal experience.
- 5% revenue share after $1M (comparable risk to Unity's runtime fee).
- Migration effort: 8–12 weeks per game, ~$91,800 estimated cost.
- Larger binary size — impacts mobile download size targets.

**Effort Estimate:** 8–12 weeks migration + 4 weeks validation per game.

### Decision

**Selected Option:** Option A — Unity 6.3 LTS

**Rationale:**

Unity 6.3 LTS is the right engine choice for the Casual Games Studio because it aligns with team capability, PlayFab integration requirements, and the technical demands of 2D casual mini-games. The licensing risk (R4) is a **governance problem, not a technical problem** — it is best addressed through contractual negotiation (3-year fixed-price Enterprise agreement with runtime fee waiver) rather than engine replacement.

The cost of migrating to Godot (~$51,000 per game + 4–6 weeks delay) or Unreal (~$91,800 per game + 8–12 weeks delay) significantly exceeds the cost of Unity licensing, even under worst-case runtime fee scenarios. Furthermore, the loss of official PlayFab SDK support and team productivity during migration would impact Stage 3–5 timelines.

The decision to stay on Unity is **conditional** on successful negotiation of a fixed-price contract with runtime fee protections. If negotiations fail, or if Unity materially changes terms during the contract period, the exit strategy (Option B: Godot) will be activated.

**Decision Authority:** CIO (Dr. Priya Mehta) with CTO and Studio Director concurrence.

### Consequences

#### Positive

- Zero team ramp-up time — engineers are productive from Day 1 of Stage 3.
- Official PlayFab SDK reduces backend integration risk.
- Mature 2D tooling accelerates mini-game development.
- Large ecosystem provides access to proven solutions for common problems.

#### Negative (Accepted Trade-offs)

- Vendor lock-in — the studio is dependent on Unity's continued viability and licensing stability.
- Annual licensing cost of ~$61–112K (mitigated by multi-title amortization).
- Closed-source engine limits ability to debug or modify core engine behavior.

#### Risks

| Risk                                   | Severity | Mitigation                                                                   |
| -------------------------------------- | -------- | ---------------------------------------------------------------------------- |
| Unity changes licensing terms          | High     | 3-year fixed-price contract with runtime fee waiver; quarterly review        |
| Unity ceases operations or LTS support | Low      | Source code escrow clause in contract; Godot exit strategy documented        |
| Runtime fee reinstatement              | Medium   | Contractual waiver; if not obtained, activate Godot migration for next title |
| PlayFab SDK deprecation for Unity      | Low      | Backend abstraction layer (IAuthService, IDataService) enables provider swap |

### Implementation Notes

1. **Contract negotiation** must be completed by Week 4 (per Section 3.2 timeline). CIO owns this workstream with external legal counsel.
2. **Godot proof-of-concept:** Commission a lightweight Godot migration assessment for one mini-game (2-week effort) as a hedge. This should be completed by Stage 4.
3. **Backend abstraction layer:** Priya Nair's IAuthService/IDataService/IEconomyService pattern is the technical safety net — if engine migration becomes necessary, the backend integration layer is already designed for provider swap.
4. **ADR review cycle:** This ADR will be reviewed quarterly by the CIO to assess whether licensing conditions have changed.
5. **Stage 3 gate:** This ADR must be Accepted before Stage 3 gate approval.

### References

- Strategic Brief, Section 2.4 (Technology Risk Register, R4)
- COPPA & Platform Compliance reference — `studio/casual-games/library/reference/coppa-platform-compliance.md`
- Unity Licensing Legal Memorandum (forthcoming — Week 2 deliverable)
- Unity Enterprise Contract (forthcoming — Week 4 deliverable)
- Godot Migration Assessment (forthcoming — Stage 4 deliverable)

---

## 6. Timeline — Week-by-Week Milestones

### Week 1 (April 13–19, 2026)

| Day | Milestone                                             | Owner       | Deliverable                     |
| --- | ----------------------------------------------------- | ----------- | ------------------------------- |
| 1–2 | Engage external legal counsel                         | CIO         | Statement of Work signed        |
| 3–4 | Provide Unity EULA, pricing, risk register to counsel | CIO         | Documentation package delivered |
| 5   | Initial legal risk assessment call                    | CIO + Legal | Preliminary findings summary    |

### Week 2 (April 20–26, 2026)

| Day | Milestone                                                 | Owner         | Deliverable                   |
| --- | --------------------------------------------------------- | ------------- | ----------------------------- |
| 1–2 | Legal counsel drafts formal memorandum                    | Legal Counsel | Draft Legal Memorandum        |
| 3   | CIO reviews memorandum, identifies negotiation priorities | CIO           | Negotiation priority list     |
| 4   | Brief CTO + Studio Director on findings                   | CIO           | Leadership briefing completed |
| 5   | **Gate: C1 condition satisfied**                          | CIO           | ✅ Legal review complete      |

### Week 3 (April 27 – May 3, 2026)

| Day | Milestone                                                                      | Owner       | Deliverable                    |
| --- | ------------------------------------------------------------------------------ | ----------- | ------------------------------ |
| 1–2 | Engage Unity Enterprise sales                                                  | CIO + Legal | Initial negotiation meeting    |
| 3–4 | Present contract requirements (fixed price, runtime fee waiver, source escrow) | CIO         | Requirements document to Unity |
| 5   | First negotiation round                                                        | CIO + Legal | Term sheet draft               |

### Week 4 (May 4–10, 2026)

| Day | Milestone                                             | Owner         | Deliverable                |
| --- | ----------------------------------------------------- | ------------- | -------------------------- |
| 1–3 | Second negotiation round (counter-terms, concessions) | CIO + Legal   | Revised term sheet         |
| 4   | Final legal review of contract terms                  | Legal Counsel | Legal sign-off on contract |
| 5   | **Execute signed Unity Enterprise contract**          | CIO + Legal   | ✅ Signed contract filed   |

### Post-Contract (Ongoing)

| Milestone                            | Frequency | Owner | Notes                                             |
| ------------------------------------ | --------- | ----- | ------------------------------------------------- |
| ADR-001 review                       | Quarterly | CIO   | Assess licensing conditions, update risk rating   |
| Godot proof-of-concept (1 mini-game) | Stage 4   | CTO   | Validate exit strategy feasibility                |
| Contract renewal preparation         | Month 33  | CIO   | Begin renewal negotiations 3 months before expiry |

---

**Approved By:** Dr. Priya Mehta, CIO
**Date:** April 12, 2026
**Next Review:** April 19, 2026 (Week 1 check-in)
