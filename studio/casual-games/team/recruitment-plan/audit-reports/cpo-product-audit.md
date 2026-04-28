# Marcus Tran-Yoshida — Product & Commercial Audit

**Auditor:** Marcus Tran-Yoshida, Chief Product Officer
**Date:** April 12, 2026
**Scope:** Product roles, monetization capability, live ops capability, and kill-gate decision readiness
**Verdict:** CONDITIONAL GO

---

## Executive Summary

The Casual Games studio has been staffed to 38 FTEs + 1 Contract across 7 divisions. From a product and commercial lens, the recruitment results are **strong but not without gaps**. The Live Ops division is the crown jewel — Aisha Nkemelu (Live Ops Lead) and Yuki Tanaka (Data Analyst) are exceptional hires that directly address the P0 commercial gaps I flagged during the Strategic Brief review. However, there are **two material gaps** that require mitigation before Stage 8 (Soft Launch) and Stage 10 (Live Ops) can execute with confidence.

**Sign-off Decision: CONDITIONAL GO** — conditions detailed below.

---

## Audit Checklist

### Item 1: Live Ops Lead (Aisha Nkemelu) — Stage 8 & Stage 10 Ownership

**Verdict: ✅ PASS**

Aisha Nkemelu is the strongest hire in this recruitment wave. Her credentials are directly relevant:

- **9.5 years** in mobile F2P live ops (Playrix, King, Zynga) — exactly the pedigree needed
- **Managed Gardenscapes at 10M+ DAU** across 150+ markets — scale experience that maps to our target
- **Designed seasonal event frameworks** generating $47M incremental annual revenue — proven monetization through live ops
- **Built A/B testing infrastructure from scratch** at Playrix; ran 200+ concurrent experiments — directly applicable to soft launch iteration
- **Grew Discord from 15K to 120K** in 18 months — community management capability confirmed
- **MSc in Data Analytics** — rare for a live ops lead; can read cohort data and LTV models without hand-holding

**Pipeline Stage Ownership:** Stages 7, 8, 10 per her profile — correct mapping. She is equipped to own soft launch execution and live ops strategy.

**Honest Gap Assessment:** Her lack of PC/console experience is irrelevant for a mobile-only casual game. Her lack of hands-on engineering background is a minor risk — she relies on her 2x Live Ops Engineers for content deployment pipeline work. This is mitigated by having two senior Live Ops Engineers (David Okafor, Sofia Reyes) reporting to her.

---

### Item 2: UA Specialist (Rafael Santos) — CPI Optimization & ROAS Tracking

**Verdict: ✅ PASS**

Rafael Santos brings credible UA capability:

- **$200K+/month ad spend** managed across 20+ titles at Voodoo — real money, real scale
- **CPI of $1.20** vs. industry benchmark of $1.50–$2.50 for hyper-casual — demonstrates optimization capability
- **Built creative testing framework** with 50+ concurrent tests, weekly kill/scale decisions — systematic approach
- **SKAdNetwork 4.0 and ATT framework** expertise — critical for iOS UA post-privacy changes
- **Built ROAS tracking dashboards** connecting UA spend to LTV — understands the unit economics equation

**Noted Gaps (mitigated):**

1. **Hyper-casual bias** — His experience is in hyper-casual UA. Casual/hybrid-casual games have longer user journeys and higher LTV, requiring different creative strategies and bidding approaches. This is a _learning curve_, not a _capability gap_. The 30–90 day soft launch window provides time for adaptation.
2. **Apple Search Ads depth is developing** — He has managed ASA campaigns but not at scale. For a casual game, ASA is secondary to Meta and Google UAC; this is manageable.
3. **No team management experience** — He is a Senior IC, not a manager. Under Aisha's leadership, this is not a concern.

**Risk Assessment:** Passes the bar for soft launch and global launch UA execution. The hyper-casual-to-casual adaptation risk is acceptable within a CONDITIONAL GO framework — I recommend a **UA strategy review session with Aisha and the CPO office before Stage 8 entry** to pressure-test his UA plan against casual-game benchmarks.

---

### Item 3: Data Analyst (Yuki Tanaka) — Cohort Modeling & LTV Forecasting for Kill-Criteria Validation

**Verdict: ✅ PASS**

Yuki Tanaka is an exceptional hire for kill-criteria validation:

- **LTV forecast model with 94% accuracy** used for $2M+ quarterly UA budget allocation at Zynga — this is exactly the model we need for LTV:CAC kill gate validation
- **Cohort decay modeling** using Weibull distributions and survival analysis — directly applicable to D1/D7/D30 retention tracking
- **Identified critical D7 retention leak** at Zynga leading to 2.3pp D30 retention improvement — proven ability to find and fix retention problems
- **50+ A/B tests designed** with rigorous statistical methodology — can design and interpret soft launch experiments
- **Kaggle Master (top 1% globally)** — signal of analytical rigor
- **Advanced SQL + Python (pandas, scikit-learn, statsmodels)** — production-quality analysis capability

**Kill-Criteria Coverage:** Every kill criterion I defined in the Strategic Brief is covered by Yuki's skill set:

| Kill Criterion                  | Yuki's Capability                                     |
| ------------------------------- | ----------------------------------------------------- |
| D1 >= 40%, D7 >= 15%, D30 >= 8% | Cohort decay modeling, retention curve fitting        |
| LTV:CAC >= 1.5                  | LTV forecasting model (94% accuracy backtested)       |
| ARPDAU >= $0.04                 | Revenue analytics, cohort-level monetization analysis |
| Paywall Conversion >= 3%        | A/B test design, funnel analysis                      |
| App Store Rating >= 4.2         | Not directly analytical — tracked via store APIs      |

**Honest Gap Assessment:** Her lack of real-time analytics experience is noted. For soft launch, batch-oriented daily cohort analysis is sufficient. If we need real-time dashboards during soft launch, Yuki will need engineering support for streaming data pipelines — the Backend Engineer can provide this.

---

### Item 4: Economy Designer (Kwame Asante) — F2P Monetization Experience

**Verdict: ✅ PASS**

Kwame Asante is a solid economy designer with relevant F2P experience:

- **Designed Gardenscapes economy** generating $200M+ annual revenue — worked on a top-tier casual game economy
- **Optimized IAP pricing** increasing conversion by 12% and ARPU by 8% — proven monetization impact
- **Sink/source modeling and inflation control** — core economy design skills
- **Built economy dashboard tracking 20+ health metrics** — data-driven approach

**Honest Gap Assessment:**

1. **No live ops economy management experience** — He has designed _pre-launch_ economies but has limited experience managing live economies post-launch (inflation control, emergency balancing). This is a **moderate risk** for Stage 10. **Mitigation:** Aisha Nkemelu has live ops economy balancing experience from Playrix; she will own Stage 10 economy management with Kwame in a supporting role. The dotted-line reporting from Economy Designer to Live Ops Lead for Stage 8/10 (defined in the recruitment plan) addresses this.
2. **Not a technical designer** — He cannot implement economy systems in code. He relies on engineers for implementation. This is normal for economy designers and not a gap.

---

### Item 5: Lead Game Designer (Mei Watanabe) — GDD Authorship & Systems Design

**Verdict: ✅ PASS**

Mei Watanabe is an elite hire — a perfect 20/20 vetting score:

- **14 years of game design experience** at King, Zynga, Glu — top-tier casual game pedigree
- **Redesigned Candy Crush Saga's economy** increasing D1 retention by 12% and D7 by 8% — directly applicable to our retention targets
- **Authored GDDs for 3 shipped titles** with combined 500M+ downloads — proven GDD authorship at scale
- **Designed progression system adopted as King's standard template** across 8 studios — systems design capability confirmed
- **GDC 2025 speaker + DiGRA 2023 paper** — thought leadership in the space
- **MS in Human-Computer Interaction from Carnegie Mellon** — strong UX foundation

**Kill-Criteria Relevance:** Mei's D1/D7/D30 retention design expertise directly maps to the soft launch kill criteria. Her data-driven design review process at King means she designs with analytics instrumentation in mind.

---

### Item 6: Senior Game Designer (Lisa Henderson) — Progression Loops & Monetization Design

**Verdict: ✅ PASS**

Lisa Henderson is a capable systems and economy designer:

- **Designed economy and progression systems for Gardenscapes** (50M+ DAU) — large-scale experience
- **Increased ARPDAU by 18%** through IAP features while maintaining player satisfaction — monetization design that doesn't alienate players
- **Built player psychology models** informing live ops event design — rare skill that bridges design and analytics
- **9 years of experience** at Playrix, King, Big Fish — strong casual game lineage

**Honest Gap Assessment:** She is primarily a systems/economy designer, not a narrative or level designer. The studio has dedicated Level Designer (Marcus Thompson) and UX Writer (Sarah Chen) to cover those areas. Her gap in technical implementation is normal for game designers.

---

### Item 7: Production Capacity (James Mitchell + Lena Mueller) — 2 FTEs for 33 ICs

**Verdict: ⚠️ CONDITIONAL PASS**

This is a **structural concern** I flagged during the Stage 2 review of the recruitment plan, and it remains unresolved:

- **James Mitchell (Producer):** 12 years of game production experience, delivered Golf Clash live ops content pipeline (100M+ downloads), reduced sprint cycle time by 25%. Strong credentials. However, his vetting score of 16/20 is the lowest among leadership-adjacent hires. His gap in budget management is notable for someone coordinating a $1.1M investment cap.
- **Lena Mueller (Associate Producer):** 3 years of experience — capable coordinator but mid-level. She can handle task tracking and meeting facilitation, but cannot absorb strategic production load.

**The Math:** 2 production FTEs managing a 33-person IC team across 11 pipeline stages. At peak production (Stage 5), this is **1:16.5 span** — aggressive even for experienced producers.

**Mitigating Factors:**

- The Executive Producer (James Okonkwo) provides senior production oversight above the Producer
- The Studio Director (Marcus Vogel) owns Stage 3/5/8 deliverables and will share production load
- Agile tooling (Jira/Confluence) and standardized sprint templates reduce coordination overhead

**Verdict:** Passes the bar _barely_. Per the recruitment plan's own Stage 2 review flag: _"Production bandwidth (2 FTEs for 33 ICs) will be reviewed at Stage 2 gate. If execution-level production bottlenecks are detected, a third producer will be added at that time."_ **I endorse this contingency and recommend it be triggered proactively at Stage 3 if sprint velocity metrics show degradation.**

---

### Item 8: Soft Launch Analytics Instrumentation Capability

**Verdict: ✅ PASS**

The analytics instrumentation capability for soft launch is covered by three roles working in concert:

| Role                           | Responsibility                                                                   |
| ------------------------------ | -------------------------------------------------------------------------------- |
| **Yuki Tanaka (Data Analyst)** | KPI dashboard creation, funnel definitions, cohort segmentation, A/B test design |
| **Backend Engineer**           | Data export pipeline (PlayFab Events -> Kafka), analytics pipeline connection    |
| **Live Ops Engineers (2x)**    | A/B test implementation, feature flagging, analytics event wiring                |

**Pipeline Coverage:** The Data Analyst owns Stages 5, 8, 9, 10 — ensuring analytics instrumentation begins during Full Production (Stage 5), is validated during Soft Launch Prep (Stage 7), and operates during Soft Launch (Stage 8).

**Gap Noted:** Yuki Tanaka's lack of real-time analytics experience means the soft launch dashboard will be batch-oriented (daily refresh). This is sufficient for D1/D7/D30 retention tracking but may limit real-time UA optimization during the first weeks of soft launch. **Mitigation:** The Backend Engineer's analytics pipeline can support near-real-time dashboards if Yuki pairs with engineering on the data layer.

---

### Item 9: Community Management Capability — Ownership Gap

**Verdict: ❌ FAIL**

This is the **most significant product/commercial gap** in the recruited team:

**No dedicated Community Manager has been hired.**

The recruitment plan states: _"Community/Player Support ownership is initially assigned to the Live Ops Lead — this will be clarified during recruitment execution."_ The clarification never happened.

**Current State:** Aisha Nkemelu has community strategy capability (grew Playrix Discord from 15K to 120K) and her profile includes a "Community Strategy" skill. However:

1. **She is a Principal-level strategist, not a community operator.** Growing a Discord from 15K to 120K is a strategic achievement — but day-to-day community management (moderation, player support tickets, social media responses, crisis communication) is operational work that will consume 20–30 hours/week at soft launch scale.
2. **Her span of control is already 4 direct reports** (2x Live Ops Engineers, UA Specialist, Data Analyst). Adding community operations on top of live ops strategy, content calendar, and economy balancing is unsustainable.
3. **During soft launch (Stage 8),** community management intensity peaks — this is when player sentiment directly impacts retention and store ratings. Diverting the Live Ops Lead from strategic KPI monitoring to community operations creates a **kill-gate decision risk**.

**Impact on Kill Gates:**

- **G3 (Soft Launch):** Requires monitoring of D1 retention, D7 retention, ARPDAU, crash rate, AND community sentiment. If Aisha is drowning in community tickets, she cannot make data-driven kill/iterate decisions.
- **G5 (Live Ops QBR):** Community sentiment is a formal QBR metric (< 50% positive = crisis protocol). Without dedicated community management, this metric cannot be reliably tracked or acted upon.

**Recommended Mitigation (2 options):**

| Option                         | Action                                                               | Timeline                          | Cost          |
| ------------------------------ | -------------------------------------------------------------------- | --------------------------------- | ------------- |
| **A — Hire Community Manager** | Add 1 Community Manager FTE to Live Ops division (reports to Aisha)  | Before Stage 7 (Soft Launch Prep) | $80K–$110K/yr |
| **B — Outsource to Agency**    | Contract community management agency for moderation + player support | Before Stage 8 (Soft Launch)      | $3K–$8K/month |

**I recommend Option A** — a Community Manager who can also serve as the player support lead is a better long-term investment for Stage 10 live ops. If budget constraints prevent a hire before soft launch, Option B is an acceptable bridge.

---

### Item 10: Product/Commercial Skill Gaps That Could Block Kill-Gate Decision Making

**Verdict: ⚠️ CONDITIONAL PASS**

| Gap                                                      | Risk                                                                                                            | Mitigation                                                                                                |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Community Management (see Item 9)**                    | Live Ops Lead bandwidth dilution during soft launch -> delayed or compromised kill-gate decisions               | Hire Community Manager before Stage 7, or contract agency                                                 |
| **Rafael Santos's hyper-casual-to-casual UA adaptation** | CPI and ROAS projections may be inaccurate for casual-game user journeys -> LTV:CAC miscalculation at kill gate | UA strategy review session before Stage 8 entry; Aisha to validate UA plan against casual-game benchmarks |

**No other product/commercial skill gaps were identified that would block kill-gate decision making.** The following roles are fully capable:

- **Kill Gate G1 (Stage 3):** Mei Watanabe (Lead Game Designer) + Studio Director can validate vertical slice quality
- **Kill Gate G2 (Stage 5):** James Mitchell (Producer) + Executive Producer can track budget/schedule
- **Kill Gate G3 (Stage 8):** Aisha Nkemelu (Live Ops Lead) + Yuki Tanaka (Data Analyst) + Rafael Santos (UA Specialist) can validate all soft launch KPIs
- **Kill Gate G4 (Stage 9):** Studio Director + Executive Producer can validate store readiness
- **Kill Gate G5 (Stage 10 QBR):** Aisha Nkemelu (Live Ops Lead) + Executive Producer can run quarterly business reviews

---

## Risk Assessment

### Risk Matrix

| Risk ID | Risk Description                                                                                                          | Probability | Impact     | Severity | Mitigation                                                             |
| ------- | ------------------------------------------------------------------------------------------------------------------------- | ----------- | ---------- | -------- | ---------------------------------------------------------------------- |
| CR-1    | No dedicated Community Manager — Live Ops Lead bandwidth dilution during soft launch                                      | **High**    | **High**   | 🔴 P0    | Hire Community Manager before Stage 7 (see Item 9)                     |
| CR-2    | Rafael Santos's hyper-casual UA experience may not translate to casual-game CPI/ROAS                                      | **Medium**  | **Medium** | 🟠 P1    | UA strategy review before Stage 8; Aisha validates plan                |
| CR-3    | Kwame Asante's lack of live ops economy management experience — post-launch inflation risk                                | **Medium**  | **Medium** | 🟠 P1    | Aisha Nkemelu owns Stage 10 economy; Kwame supports                    |
| CR-4    | Production bandwidth (2 FTEs for 33 ICs) — sprint velocity degradation at Stage 5 peak                                    | **Medium**  | **Medium** | 🟠 P1    | Add 3rd producer at Stage 2/3 gate if velocity metrics degrade         |
| CR-5    | Yuki Tanaka's batch-only analytics — limits real-time UA optimization during early soft launch                            | **Low**     | **Low**    | 🟡 P2    | Backend Engineer supports streaming pipeline if needed                 |
| CR-6    | No monetization strategy owner at the strategic level — Economy Designer reports to Lead Game Designer, not Live Ops Lead | **Low**     | **Medium** | 🟡 P2    | CPO office provides strategic monetization oversight during Stages 1–4 |

### Overall Commercial Readiness Score: **7.5 / 10**

| Dimension                        | Score | Rationale                                                     |
| -------------------------------- | ----- | ------------------------------------------------------------- |
| Live Ops Strategy                | 9/10  | Aisha Nkemelu is exceptional                                  |
| UA Capability                    | 7/10  | Rafael Santos is strong but needs casual-game adaptation      |
| Analytics & Kill-Gate Validation | 9/10  | Yuki Tanaka is elite for this purpose                         |
| Economy Design                   | 8/10  | Kwame + Lisa + Mei = strong pre-launch; Aisha covers live ops |
| Production Capacity              | 6/10  | 2 FTEs for 33 ICs is stretched                                |
| Community Management             | 3/10  | **Critical gap — no dedicated owner**                         |
| Design Leadership                | 10/10 | Mei Watanabe is a perfect 20/20 hire                          |

### What I Am NOT Flagging

For clarity, the following are **NOT concerns**:

- Data Analyst capability — Yuki Tanaka is elite for kill-gate validation
- Live Ops Lead capability — Aisha Nkemelu exceeds the bar
- Economy design capability — Kwame + Lisa + Mei = strong pre-launch; Aisha covers live ops
- Lead Game Designer capability — Mei Watanabe is a perfect hire
- Soft launch analytics — Instrumentation capability is present across 3 roles

---

## Sign-Off Decision

### CONDITIONAL GO

The Casual Games studio recruitment results demonstrate **strong product and commercial foundations** with three conditions that must be resolved before Stage 7 (Soft Launch Prep) entry:

| #   | Condition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Priority |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| C1  | **Community Manager Hire (P0):** A Community Manager or Community Management agency MUST be onboarded before Stage 7 (Soft Launch Prep). The Live Ops Lead cannot simultaneously own strategic kill-gate decision making and day-to-day community operations during soft launch. I recommend a full-time Community Manager FTE reporting to Aisha Nkemelu, budgeted at $80K–$110K/yr. If a full-time hire is not feasible before Stage 7, a contracted community management agency is an acceptable bridge. | P0       |
| C2  | **UA Strategy Review (P1):** Before Stage 8 (Soft Launch) entry, a UA strategy review must be conducted between Rafael Santos, Aisha Nkemelu, and the CPO office. The review must validate that CPI projections, ROAS targets, and creative testing frameworks are calibrated for casual-game (not hyper-casual) user journeys. The output must be a documented UA Plan with casual-game-specific benchmarks.                                                                                               | P1       |
| C3  | **Production Bandwidth Monitoring (P1):** Production capacity must be monitored at Stage 2 and Stage 3 gates. If sprint velocity metrics show degradation or the Producer reports execution-level bottlenecks, a third producer must be added immediately. The recruitment plan already flags this contingency — I am formally endorsing it as a condition of this sign-off.                                                                                                                                | P1       |

**Rationale:**

The recruited team has strong product and commercial foundations. Aisha Nkemelu is an exceptional Live Ops Lead, Yuki Tanaka is elite for kill-gate validation, and Mei Watanabe is a perfect 20/20 hire for Lead Game Designer. The Economy Designer and Senior Game Designer provide strong pre-launch economy capability.

The two material gaps are the Community Manager ownership gap (P0) and Rafael Santos's hyper-casual-to-casual UA adaptation risk (P1). Both are addressable — the Community Manager can be hired or contracted before Stage 7, and the UA strategy review can be scheduled before Stage 8. Production bandwidth (2 FTEs for 33 ICs) is a structural concern that I am formally endorsing for monitoring at Stage 2/3 gates.

---

**Signed:** Marcus Tran-Yoshida, CPO
**Date:** April 12, 2026
