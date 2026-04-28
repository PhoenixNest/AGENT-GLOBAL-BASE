# Game Studio — Development Workflow

**Document Type:** Game Studio Pipeline Definition (Independent of Parent Company)  
**Status:** C-Suite Review Complete  
**Date:** April 9, 2026  
**Related Documents:** `casual-games-studio.md`, `casual-games-asset-strategy.md`

---

## 1. Overview

The game studio operates **independently** from the parent company's 10-stage mobile app pipeline. While the parent pipeline was designed for utility-driven applications with feature-gated development, games operate under fundamentally different economics: **hit-driven, iterative, live-service, and experientially validated**.

This document defines the **complete game studio workflow** from concept through live ops, incorporating input from the CTO, CPO, CDO, and CSO.

### Design Principles

| Principle                          | Description                                                                                                                     |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Paired artifacts**               | GDD + PRD + SRD travel together from Stage 1 — creative vision, commercial viability, and security requirements are inseparable |
| **Metrics-driven gates**           | Retention (D1/D7/D30), ARPDAU, LTV:CAC, and playtest scores replace feature completion as gate criteria                         |
| **Kill gates are the default**     | A healthy studio kills 70–80% of concepts before global launch — kill is capital preservation, not failure                      |
| **Soft launch is a formal stage**  | Not a marketing tactic — a product validation stage with explicit entry/exit criteria                                           |
| **Live ops is continuous**         | Post-launch content updates follow their own operating rhythm, not the pre-launch pipeline                                      |
| **Security is non-waivable**       | Six minimum security gates apply regardless of organizational independence (CSO mandate)                                        |
| **Automated testing is mandatory** | 100% test pass rate required before soft launch — unit, integration, performance, and regression tests (CTO + Test Lead)        |

---

## 2. Pipeline Map

```
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 0: Portfolio Review + Art Direction (Pre-Design)              │
│ Owners: CPO + Studio Head + Art Director + CDO                      │
│ Output: Portfolio Dashboard, Art Direction Brief, Style Guide v1,    │
│         Technical Art Constraints, Asset Production Pipeline         │
│ Gate: CDO + CPO + CTO sign-off                                      │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 1: Concept                                                     │
│ Owners: Creative Director (GDD) + CPO (PRD) + CSO (SRD)             │
│ Output: GDD v1 + PRD v1 + SRD v1 (paired artifacts),                │
│         market fit assessment, competitive landscape                 │
│ Gate: Kill Gate 1 — Clear market whitespace + differentiation        │
│ User approval required                                               │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 2: Prototype                                                   │
│ Owners: Game Director + CDO (Concept Prototype)                      │
│ Output: Concept Prototype (Figma), Playable Prototype (Unity greybox),│
│         GDS Package (Game Feel Spec, VFX Brief, Meta-UI IDS),        │
│         Tier 1 Internal Playtest Report                              │
│ Gate: Kill Gate 2 — D1 ≥ 25%, session ≥ 5 min (internal playtest)    │
│ User approval required                                               │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 3: Vertical Slice                                              │
│ Owners: Game Director + Art Director + Engineering Lead              │
│ Output: Vertical slice (one complete polished loop),                 │
│         external playtest, economy model v1, asset SBOM              │
│ Gate: Kill Gate 3 — D1 ≥ 35%, D7 ≥ 10%, playtest score ≥ 3.5/5      │
│ User approval required                                               │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 4: Production Planning                                         │
│ Owners: Producer + CPO                                               │
│ Output: Content production plan, economy model v2, LTV projection,   │
│         implementation plan + Gantt chart, asset pipeline locked     │
│ Gate: Kill Gate 4 — Projected LTV:CAC ≥ 2.0, budget feasibility      │
│ User approval required                                               │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 5: Full Production                                             │
│ Owners: Game Director + Engineering + Art + Design                   │
│ Output: Feature-complete game build, all art/assets,                  │
│         complete GDS Package, integrated analytics                   │
│ Checkpoints:                                                         │
│   • Mechanic Sprint reviews (biweekly)                               │
│   • Game Feel Checkpoint (~50%) — GDS conformance audit              │
│   • Tier 2 Focused Playtest (~50%) — external cohort (20–30)         │
│   • Visual Coherence Check (~75%) — Style Guide audit                │
│   • Tier 3 Validation Playtest (~90%) — blind cohort (50+)           │
│   • Asset security review: all third-party assets screened (CSO)     │
│ Gate: CTO internal review (compilation, performance, no user approval)│
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 6: Automated Testing                                           │
│ Owners: CTO + Test Lead                                              │
│ Output: Test suite (Edit Mode + Play Mode + E2E),                    │
│         test results report, performance benchmarks,                  │
│         regression test pass, visual regression (static UI)          │
│ Gate: 100% test pass rate, zero P0/P1 test defects,                   │
│      performance within baseline, coverage targets met               │
│ User approval required                                               │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 7: Soft Launch Prep                                            │
│ Owners: CPO + UA Lead + Analytics Lead                               │
│ Output: Soft launch build, UA plan, analytics validation,            │
│         technical performance verification, code review sign-off     │
│ Gate: Load ≤ 15s, crash-free ≥ 98%, all analytics events validated,  │
│      pen test completed (zero P0/P1), platform compliance checklist  │
│ User approval required                                               │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 8: Soft Launch                                                 │
│ Owners: CPO + UA Lead + Live Ops Designer                            │
│ Output: Live in test markets, metric dashboard, iteration log         │
│ Market progression:                                                  │
│   • Tier 1 (Week 1–2): Canada, Australia                             │
│   • Tier 2 (Week 3–4): Philippines, Brazil (if Tier 1 passes)        │
│   • Tier 3 (Week 5+): Selected EU markets (if Tier 2 passes)         │
│ Gate: Kill Gate 5 — D1 ≥ 40%, D7 ≥ 15%, D30 ≥ 5%,                   │
│      LTV:CAC ≥ 1.5, ARPDAU ≥ $0.05 (hyper-casual) / ≥ $0.15 (midcore)│
│ User approval required (decision: global / iterate / kill)           │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 9: Global Launch Readiness                                     │
│ Owners: CPO + Studio Head + Marketing                                │
│ Output: Launch build, marketing plan, community readiness,           │
│         store submission package, compliance verification report     │
│ Gate: All soft launch gates met + store submission ready +           │
│      CSO sign-off (COPPA/GDPR-K, platform policy, security controls) │
│ User issues final launch decision                                    │
└──────────────────────────────────────────────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────────┐
│ STAGE 10: Live Ops (Continuous)                                      │
│ Owners: Live Ops Product Manager + Game Director                     │
│ Output: Live ops calendar, events, balance patches, seasonal content │
│ Gate: QBR every 90 days — Full Investment / Maintenance / Sunset     │
│ Tiered update security model:                                        │
│   • Tier 1 (Content only): Asset security review                     │
│   • Tier 2 (Feature update): Code review + security regression       │
│   • Tier 3 (System change): Full security gate (SRD amendment,       │
│     pen test, platform compliance re-verification)                   │
│   • Tier 4 (Emergency hotfix): Expedited review + 72h regression     │
│ No per-cycle user approval; user reviews QBR outcomes                │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Stage Details

### Stage 0: Portfolio Review + Art Direction

**Purpose:** Establish art direction and evaluate portfolio capital allocation before any game-specific design work begins.

| Element                     | Detail                                                                                                                               |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Owners**                  | CPO + Studio Head + Art Director + CDO                                                                                               |
| **Artifacts In**            | Creative brief, market research, studio capacity assessment                                                                          |
| **Artifacts Out**           |                                                                                                                                      |
| └ Portfolio Dashboard       | All active/in-planning games tracked on single dashboard                                                                             |
| └ Art Direction Brief       | Visual style references, mood boards, competitor analysis, positioning                                                               |
| └ Style Guide v1            | Typography, iconography, UI chrome, animation principles, material language                                                          |
| └ Technical Art Constraints | Polygon budgets, texture limits, shader complexity, memory budgets, draw call targets                                                |
| └ Asset Production Pipeline | Tool chain, naming conventions, version control for art, review/approval workflow                                                    |
| **Gate Criteria**           | Art Direction Brief approved by CDO + CPO; Style Guide signed off; Technical constraints validated by CTO; Asset pipeline documented |
| **User Approval**           | Not required — internal creative alignment gate                                                                                      |
| **Estimated Duration**      | 2–3 weeks                                                                                                                            |

### Stage 1: Concept

**Purpose:** Define the game's creative vision, commercial framework, and security requirements as paired artifacts.

| Element                                   | Detail                                                                                                                              |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Owners**                                | Creative Director (GDD) + CPO (PRD) + CSO (SRD)                                                                                     |
| **Artifacts In**                          | Stage 0 Art Direction Brief, Style Guide v1                                                                                         |
| **Artifacts Out**                         |                                                                                                                                     |
| └ GDD v1 (Game Design Document)           | Core loop, mechanics, progression systems, narrative, art direction, level design                                                   |
| └ PRD v1 (Product Requirements Document)  | Target audience, platform, retention targets, monetization model, LTV:CAC thresholds, kill criteria, analytics instrumentation plan |
| └ SRD v1 (Security Requirements Document) | Anti-cheat strategy, economy exploit prevention, SDK security, data protection, COPPA/GDPR-K applicability assessment               |
| **Gate Criteria**                         | Kill Gate 1: Clear market whitespace identified; defensible differentiation hypothesis; TAM sufficient to justify investment        |
| **User Approval**                         | Required — user confirms concept direction                                                                                          |
| **Estimated Duration**                    | 2–3 weeks                                                                                                                           |

### Stage 2: Prototype

**Purpose:** Prove the core game loop is fun through a playable prototype, validated by internal playtesting.

| Element                                         | Detail                                                                                                                                         |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owners**                                      | Game Director (playable prototype) + CDO (concept prototype)                                                                                   |
| **Artifacts In**                                | GDD v1, PRD v1, SRD v1, Art Direction Brief, Style Guide v1                                                                                    |
| **Artifacts Out**                               |                                                                                                                                                |
| └ Concept Prototype                             | Figma interactive flow validating information architecture and meta-game structure                                                             |
| └ Playable Prototype                            | Unity greybox build validating game feel, control responsiveness, pacing, difficulty curve                                                     |
| └ GDS Package (Game Design Specification)       |                                                                                                                                                |
| &nbsp;&nbsp;└ Game Feel Specification           | Input latency budgets, animation timing curves, camera shake parameters, hit-stop frames, haptic choreography                                  |
| &nbsp;&nbsp;└ Visual Direction & VFX Brief      | Color palette, lighting model, particle behavior, post-processing stack, UI animation principles                                               |
| &nbsp;&nbsp;└ Meta-UI Interaction Specification | Platform-native UI for non-gameplay screens (settings, store, leaderboards, IAP) — direct IDS equivalent                                       |
| └ Tier 1 Internal Playtest Report               | Studio team (5–10 people); session duration, repeat attempts, verbal feedback                                                                  |
| └ Asset SBOM (initial)                          | All third-party assets used in prototype inventoried with license metadata                                                                     |
| **Gate Criteria**                               | Kill Gate 2: D1 ≥ 25% among non-developer internal testers; average session ≥ 5 minutes; core loop passes fun validation in ≥ 40% of playtests |
| **User Approval**                               | Required — user confirms prototype fun and direction                                                                                           |
| **Estimated Duration**                          | 3–4 weeks                                                                                                                                      |

### Stage 3: Vertical Slice

**Purpose:** One complete, polished game loop — proving the full experience from start to finish, validated by external playtesting.

| Element                    | Detail                                                                                                                  |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Owners**                 | Game Director + Art Director + Engineering Lead                                                                         |
| **Artifacts In**           | All Stage 2 outputs, approved playable prototype                                                                        |
| **Artifacts Out**          |                                                                                                                         |
| └ Vertical Slice           | One complete game loop with final-quality art, audio, VFX, and UI                                                       |
| └ Economy Model v1         | Currency sinks/sources, pricing structure, progression pacing                                                           |
| └ External Playtest Report | 20–30 external testers from target demographic; quantitative + qualitative                                              |
| └ Asset SBOM (updated)     | All assets in vertical slice registered with license + security review status                                           |
| **Gate Criteria**          | Kill Gate 3: D1 ≥ 35%, D7 ≥ 10%, playtest enjoyment score ≥ 3.5/5, no structural pay-to-win dependency in economy model |
| **User Approval**          | Required — user validates the complete loop experience                                                                  |
| **Estimated Duration**     | 4–6 weeks                                                                                                               |

### Stage 4: Production Planning

**Purpose:** Define the full content production plan, validate economic projections, and lock the implementation schedule.

| Element                       | Detail                                                                                                                                       |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owners**                    | Producer + CPO                                                                                                                               |
| **Artifacts In**              | All Stage 3 outputs, validated vertical slice                                                                                                |
| **Artifacts Out**             |                                                                                                                                              |
| └ Content Production Plan     | Level count, asset count, sprint schedule, content milestones                                                                                |
| └ Economy Model v2            | Refined with vertical slice data; LTV projection, ARPDAU modeling                                                                            |
| └ Implementation Plan + Gantt | Mechanic Sprint schedule, Content Sprint schedule, Asset Production Milestones, Art Review checkpoints                                       |
| └ Asset Pipeline (locked)     | Finalized tool chain, naming conventions, quality gate procedures                                                                            |
| **Gate Criteria**             | Kill Gate 4: Projected LTV:CAC ≥ 2.0 at realistic UA costs; content production cost within approved budget (± 30% with scope reduction path) |
| **User Approval**             | Required — user approves the production plan and budget                                                                                      |
| **Estimated Duration**        | 2–3 weeks                                                                                                                                    |

### Stage 5: Full Production

**Purpose:** Build the complete game through iterative mechanic sprints, with continuous quality validation.

| Element                             | Detail                                                                                                                                                                   |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Owners**                          | Game Director + Engineering + Art + Design                                                                                                                               |
| **Artifacts In**                    | All Stage 4 outputs, locked implementation plan                                                                                                                          |
| **Artifacts Out**                   | Feature-complete game build, all art/assets integrated, complete GDS Package, analytics fully instrumented                                                               |
| **Sprint Model**                    |                                                                                                                                                                          |
| └ Mechanic Sprints (1–2 weeks)      | Single mechanic or tightly coupled cluster; ends with playable build + revised Game Feel Spec                                                                            |
| └ System Sprints (2–3 weeks)        | Interconnected systems (combat + health + enemies + level layout); ends with integrated build + Tier 1 playtest                                                          |
| └ Content Sprints (1–2 weeks)       | Level design, narrative, mission structure, reward pacing; ends with content-complete build                                                                              |
| └ Polish Sprints (2–4 weeks)        | Visual polish, audio sync, animation refinement, VFX pass, haptic pass                                                                                                   |
| **Checkpoints**                     |                                                                                                                                                                          |
| └ Game Feel Checkpoint (~50%)       | GDS conformance audit; CDO + Game Director co-sign                                                                                                                       |
| └ Tier 2 Focused Playtest (~50%)    | External cohort (20–30); difficulty curve, onboarding clarity, monetization UX comprehension                                                                             |
| └ Visual Coherence Check (~75%)     | Style Guide audit; ≥ 90% compliance                                                                                                                                      |
| └ Tier 3 Validation Playtest (~90%) | Blind cohort (50+); first-time user experience, tutorial completion, store-to-play conversion                                                                            |
| └ Asset Security Review (ongoing)   | All third-party assets screened through CSO-mandated 4-phase pipeline (quarantine → static analysis → runtime verification → approval)                                   |
| **Gate Criteria**                   | CTO internal review: compilation clean, performance targets met (60fps stable or 30fps if target allows, load ≤ 15s), crash-free ≥ 98%, Design Fidelity Checkpoint ≥ 90% |
| **User Approval**                   | Not required — CTO internal review only                                                                                                                                  |
| **Estimated Duration**              | 8–16 weeks (scales with game scope)                                                                                                                                      |

### Stage 6: Automated Testing

**Purpose:** Validate logical correctness, performance, and regression safety through automated testing before any soft launch preparation begins.

| Element                               | Detail                                                                                                                                                            |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owners**                            | CTO + Test Lead                                                                                                                                                   |
| **Artifacts In**                      | Stage 5 outputs: feature-complete game build, all art/assets integrated, analytics instrumented                                                                   |
| **Artifacts Out**                     |                                                                                                                                                                   |
| └ Test Suite                          | Edit Mode tests (unit logic), Play Mode tests (integration/gameplay), E2E tests (Maestro — primary user flows)                                                    |
| └ Test Results Report                 | Full test execution results: pass/fail per test, coverage metrics, performance benchmarks, defect log                                                             |
| └ Performance Benchmark Report        | Memory usage, scene load times, system execution time budgets — compared against established baselines                                                            |
| └ Visual Regression Report            | Screenshot comparison for static UI screens (main menu, settings, game-over) — tolerance-based diff analysis                                                      |
| └ Regression Test Verification        | All previously fixed defects have regression tests that pass                                                                                                      |
| **Test Types**                        |                                                                                                                                                                   |
| └ Edit Mode Tests (NUnit)             | Pure C# logic: economy math, scoring calculations, save/load serialization, config validation, ScriptableObject data integrity. Fast, deterministic, CI-friendly. |
| └ Play Mode Tests (Unity Test Runner) | Gameplay flows: scene transitions, input sequences (via Input System), timer/cooldown behavior, state machine transitions, analytics event firing.                |
| └ E2E Tests (Maestro)                 | Primary user flows: install → tutorial → first level → store browse → settings change → game-over → retry. Runs on real devices or emulators.                     |
| └ Performance Tests                   | Memory budgets, load time budgets, system execution time (ms per frame for critical systems). Relative benchmarking against baseline, not absolute FPS.           |
| └ Visual Regression Tests             | Static UI screenshots compared against baseline with tolerance (1–2% for UI, 3–5% for 3D scenes). Gameplay scenes excluded (false positive rate too high).        |
| **Coverage Targets**                  |                                                                                                                                                                   |
| └ Domain/Game Logic                   | ≥ 85% — economy, scoring, progression math, data models                                                                                                           |
| └ Data Layer                          | ≥ 75% — save/load, serialization, network protocols                                                                                                               |
| └ Presentation/UI                     | ≥ 40% — view wiring, animation triggers, UI state                                                                                                                 |
| └ Overall Project                     | ≥ 50% — realistic target for Unity game code                                                                                                                      |
| **Gate Criteria**                     | 100% test pass rate (all tests green); zero P0/P1 test defects; performance within baseline tolerances (± 10%); coverage targets met; regression tests all pass   |
| **Defect Classification**             |                                                                                                                                                                   |
| └ P0                                  | Test suite crash, economy calculation error, save data corruption, crash on primary user flow                                                                     |
| └ P1                                  | Analytics not firing, IAP flow broken, scene transition failure, input not registered, accessibility violation                                                    |
| └ P2                                  | Non-critical UI state mismatch, minor performance regression (< 20% over baseline)                                                                                |
| └ P3                                  | Visual diff on non-critical screen, cosmetic test failure                                                                                                         |
| **User Approval**                     | Required — user reviews Test Results Report and makes P2/P3 disposition decisions                                                                                 |
| **Estimated Duration**                | 1–2 weeks                                                                                                                                                         |

### Stage 7: Soft Launch Prep

**Purpose:** Prepare the game for soft launch with validated analytics, UA infrastructure, and technical readiness.

| Element                         | Detail                                                                                                                      |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Owners**                      | CPO + UA Lead + Analytics Lead                                                                                              |
| **Artifacts In**                | Stage 5 outputs, feature-complete build                                                                                     |
| **Artifacts Out**               |                                                                                                                             |
| └ Soft Launch Build             | Feature-complete; live ops infrastructure operational; no "soft launch only" features                                       |
| └ UA Plan                       | Market selection rationale, budget allocation ($50K Tier 1, $100K cumulative through Tier 3), campaign creative             |
| └ Analytics Validation          | All events firing correctly; funnel definitions verified; cohort segmentation tested                                        |
| └ Technical Performance Report  | Load time, crash rate, memory usage, device matrix test results                                                             |
| └ Code Review Sign-off          | All P0/P1 defects resolved; P2/P3 documented with disposition                                                               |
| └ Penetration Test Results      | Game-specific attack vectors tested; zero open P0/P1                                                                        |
| └ Platform Compliance Checklist | App Store + Google Play policy compliance verified                                                                          |
| **Gate Criteria**               | Load ≤ 15s; crash-free ≥ 98%; all analytics events validated; pen test zero P0/P1; platform compliance checklist signed off |
| **User Approval**               | Required — user approves soft launch readiness                                                                              |
| **Estimated Duration**          | 2–3 weeks                                                                                                                   |

### Stage 8: Soft Launch

**Purpose:** Validate the game in real markets with real users. This is the ultimate product validation stage.

| Element                     | Detail                                                                                                             |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Owners**                  | CPO + UA Lead + Live Ops Designer                                                                                  |
| **Artifacts In**            | Stage 6 outputs, approved soft launch build                                                                        |
| **Artifacts Out**           |                                                                                                                    |
| └ Live Game in Test Markets |                                                                                                                    |
| └ Metric Dashboard          | Real-time tracking of D1/D7/D30, ARPDAU, LTV:CAC, conversion rate, retention curves                                |
| └ Iteration Log             | Changes made based on soft launch data                                                                             |
| **Market Progression**      |                                                                                                                    |
| └ Tier 1 (Week 1–2)         | Canada, Australia — English-speaking, high LTV proxies for US/UK. Budget: $50K                                     |
| └ Tier 2 (Week 3–4)         | Philippines, Brazil — high-volume, low-cost UA for stress-testing at scale. Budget: +$50K                          |
| └ Tier 3 (Week 5+)          | Selected EU markets (Nordics, DACH) — high-LTV validation. Budget: remaining to $100K cumulative                   |
| **Exit Conditions**         |                                                                                                                    |
| └ Global Launch             | All gate metrics met at Tier 2 or above → proceed to Stage 8                                                       |
| └ Iterate + Relaunch        | D1 ≥ 30% but < 40%, OR ARPDAU within 20% of target → 30-day remediation, re-enter Stage 7                          |
| └ Kill                      | D1 < 25% after 30 days, OR LTV:CAC < 1.0 at D90, OR playtest score declining → execute kill protocol               |
| **Gate Criteria**           | Kill Gate 5: D1 ≥ 40%, D7 ≥ 15%, D30 ≥ 5%, LTV:CAC ≥ 1.5 at D90, ARPDAU ≥ $0.05 (hyper-casual) / ≥ $0.15 (midcore) |
| **User Approval**           | Required — user decides: global launch, iterate, or kill                                                           |
| **Estimated Duration**      | 30–90 days (minimum 30, maximum 90; extensions require CPO approval)                                               |

### Stage 9: Global Launch Readiness

**Purpose:** Final preparation for worldwide release.

| Element                          | Detail                                                                                                                 |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Owners**                       | CPO + Studio Head + Marketing                                                                                          |
| **Artifacts In**                 | Stage 7 outputs, validated soft launch data                                                                            |
| **Artifacts Out**                |                                                                                                                        |
| └ Launch Build                   | All soft launch iterations incorporated; feature-frozen                                                                |
| └ Marketing Plan                 | UA campaign, ASO strategy, press kit, influencer outreach                                                              |
| └ Community Readiness            | Discord/social channels prepared, community guidelines, support infrastructure                                         |
| └ Store Submission Package       | Screenshots, descriptions, keywords, age rating, privacy policy                                                        |
| └ Compliance Verification Report | COPPA/GDPR-K compliance verified (if applicable); platform policy checklists signed off; CSO sign-off                  |
| **Gate Criteria**                | All soft launch gates met + store submission ready + CSO explicit sign-off on all security and compliance requirements |
| **User Approval**                | Required — user issues final launch decision                                                                           |
| **Estimated Duration**           | 1–2 weeks                                                                                                              |

### Stage 10: Live Ops (Continuous)

**Purpose:** Continuous post-launch content delivery, economy management, and player engagement.

| Element                                   | Detail                                                                                                                                 |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | -------------------------- |
| **Owners**                                | Live Ops Product Manager + Game Director                                                                                               |
| **Artifacts In**                          | Live game, player analytics, community feedback                                                                                        |
| **Artifacts Out**                         |                                                                                                                                        |
| └ Live Ops Calendar                       | Quarterly planning, monthly adjustment; events, seasons, battle passes, content drops                                                  |
| └ Event Design Briefs                     | Per-event PRD-lite format                                                                                                              |
| └ Economy Balance Reports                 | Weekly monitoring of currency sinks/sources, inflation control                                                                         |
| └ Content Pipeline Tracker                | What's in production, what's live, what's retired                                                                                      |
| └ Player Health Dashboard                 | Retention, revenue, sentiment tracking                                                                                                 |
| **Two-Speed Pipeline**                    |                                                                                                                                        |
| └ Content Track (fast)                    | New levels, characters, cosmetics, events. Weekly–biweekly cadence. Light review (Game Director + CDO sign-off).                       |
| └ Feature Track (standard)                | New game modes, systems, monetization features, UI overhauls. Monthly–quarterly cadence. Full gate review (same as pre-launch stages). |
| **Tiered Security Model**                 |                                                                                                                                        |
| └ Tier 1 (Content only)                   | Asset security review only                                                                                                             |
| └ Tier 2 (Feature update)                 | Code review + security regression testing                                                                                              |
| └ Tier 3 (System change)                  | Full security gate: SRD amendment, pen test, platform compliance re-verification                                                       |
| └ Tier 4 (Emergency hotfix)               | Expedited review; security regression within 72 hours                                                                                  |
| **Ongoing Requirements**                  |                                                                                                                                        |
| └ Quarterly Threat Assessment             | Emerging game-specific threats (cheat tools, economy exploits, SDK vulnerabilities)                                                    |
| └ Annual Penetration Test                 | Full pen test regardless of update cadence                                                                                             |
| └ Incident Response Plan                  | Documented and tested for security breaches, economy exploits, cheat outbreaks                                                         |
| **Gate: Quarterly Business Review (QBR)** |                                                                                                                                        |
|                                           | **Metric**                                                                                                                             | **Threshold**                                               | **Consequence**            |
|                                           | MAU trend                                                                                                                              | ≥ flat QoQ                                                  | Pass                       |
|                                           | MAU trend                                                                                                                              | Declining > 10% QoQ                                         | Warning — remediation plan |
|                                           | MAU trend                                                                                                                              | Declining > 25% QoQ × 2 quarters                            | Sunset review initiated    |
|                                           | Revenue per MAU                                                                                                                        | Stable or growing                                           | Pass                       |
|                                           | Revenue per MAU                                                                                                                        | Declining > 15% QoQ                                         | Monetization redesign      |
|                                           | Content consumption                                                                                                                    | ≥ 80% of new content within 14 days                         | Pass                       |
|                                           | Content consumption                                                                                                                    | < 50% of new content within 14 days                         | Content strategy review    |
|                                           | Community sentiment                                                                                                                    | ≥ 70% positive/neutral                                      | Pass                       |
|                                           | Community sentiment                                                                                                                    | < 50% positive                                              | Crisis protocol            |
| **QBR Outcomes**                          |                                                                                                                                        |
| └ Full Investment                         | All metrics green                                                                                                                      | Continue live ops at current or increased budget            |
| └ Maintenance Mode                        | MAU declining but revenue stable                                                                                                       | Reduce content cadence, maintain core ops                   |
| └ Sunset                                  | MAU declining > 25% × 2 quarters AND revenue declining                                                                                 | Announce sunset (90-day timeline), cease content production |
| **User Approval**                         | Not required per cycle; user reviews QBR outcomes                                                                                      |
| **Duration**                              | Continuous — ends at sunset decision                                                                                                   |

---

## 4. Kill Protocol

When any kill gate triggers:

| Step | Action                                                                                   | Timeline                |
| ---- | ---------------------------------------------------------------------------------------- | ----------------------- |
| 1    | **Immediate freeze** on all production spend for the project                             | Immediate               |
| 2    | **Post-mortem** — what was learned, what assets are reusable                             | Within 5 business days  |
| 3    | **Asset archive** — art, code, design docs preserved for potential reuse in other titles | Within 5 business days  |
| 4    | **Team reassignment** — personnel reallocated to active projects                         | Within 10 business days |
| 5    | **Portfolio update** — Kill recorded in portfolio tracker with lessons learned           | Within 10 business days |

**A kill is not a failure — it is a capital preservation decision.**

---

## 5. Security Gates (CSO Mandate — Non-Waivable)

Regardless of organizational independence, these six security gates are mandatory:

| #   | Gate                                      | Stage               | Gate Criterion                                                                                                   | Enforcer                  |
| --- | ----------------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------- |
| 1   | **Security Requirements (SRD)**           | Stage 1             | SRD authored and approved; covers anti-cheat, economy security, data protection, privacy obligations             | CSO                       |
| 2   | **Asset Security Screening**              | Stage 3–5 (ongoing) | All third-party assets inventoried and screened; no unvetted assets in codebase                                  | Studio Tech Lead + CSO    |
| 3   | **Code Review — Security Criterion**      | Stage 5/7           | All SRD security controls implemented and verified; OWASP MASVS baseline met                                     | CSO                       |
| 4   | **Penetration Testing**                   | Stage 7             | Pen test completed; zero open P0/P1 findings; P2/P3 dispositions documented                                      | CSO + external pen tester |
| 5   | **Compliance Verification**               | Stage 9             | COPPA/GDPR-K compliance verified (if applicable); platform policy checklists signed off; privacy policy accurate | CSO                       |
| 6   | **Release Readiness — Security Sign-off** | Stage 9             | CSO explicitly signs off on all security requirements being enforced; no stealthy weakening of controls          | CSO                       |

---

## 6. Design Quality Gate Matrix

| Criterion                      | Measurement                                                      | Threshold                                                          | Gate Stage                  | Owner               |
| ------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------ | --------------------------- | ------------------- |
| **Game Feel Coherence**        | Parameter consistency audit across all mechanics                 | Zero contradictions; all within Game Feel Spec tolerances          | Stage 5 (50%)               | CDO                 |
| **Animation Polish**           | State machine coverage, blend tree quality, cancellation windows | 100% state coverage; zero pops/snaps; blend transitions < 8 frames | Stage 5 (Code Review)       | CDO + Art Director  |
| **Visual Performance**         | Frame rate, draw calls, overdraw, GPU frame time                 | Stable target FPS; < 3ms GPU spikes; < 200 draw calls              | Stage 6 (Automated Testing) | CTO + Art Director  |
| **Audio-Visual Sync**          | Latency between visual event and audio feedback                  | < 50ms; zero desync in cutscenes                                   | Stage 5 (Code Review)       | CDO                 |
| **Meta-UI IDS Conformance**    | Platform-native UI compliance                                    | ≥ 95% conformance                                                  | Stage 5 (Code Review)       | CDO                 |
| **Accessibility**              | WCAG 2.1 AA for meta-UI; ≥ 5 game-specific a11y options          | WCAG 2.1 AA met; minimum 5 gameplay accessibility features         | Stage 6 (Automated Testing) | CDO                 |
| **Visual Coherence Score**     | Style Guide compliance audit                                     | ≥ 90% compliance; all elements traceable to Style Guide            | Stage 5 (~75%)              | CDO + Art Director  |
| **Haptic Choreography**        | Platform-specific haptic patterns mapped to game events          | 100% of significant events have haptic feedback                    | Stage 5 (Code Review)       | CDO                 |
| **First-Time User Experience** | Tutorial completion rate, time-to-meaningful-choice              | > 80% completion; < 3 min to first choice; < 15% confusion rate    | Stage 5 (~90%)              | CDO + Game Director |

---

## 7. User Approval Summary

| Stage    | User Approval? | Gate Focus                       |
| -------- | -------------- | -------------------------------- |
| Stage 0  | ❌ No          | Internal creative alignment      |
| Stage 1  | ✅ Yes         | Concept viability + market fit   |
| Stage 2  | ✅ Yes         | Prototype fun + direction        |
| Stage 3  | ✅ Yes         | Vertical slice quality           |
| Stage 4  | ✅ Yes         | Production plan + budget         |
| Stage 5  | ❌ No          | CTO internal review only         |
| Stage 6  | ✅ Yes         | Test results + P2/P3 disposition |
| Stage 7  | ✅ Yes         | Soft launch readiness            |
| Stage 8  | ✅ Yes         | Global / iterate / kill decision |
| Stage 9  | ✅ Yes         | Final launch decision            |
| Stage 10 | ⚠️ QBR review  | User reviews quarterly outcomes  |

---

## 8. Parent Company Pipeline Mapping

For PROGRESS.md compatibility and executive reporting, game studio stages map to parent company stages as follows:

| Game Studio Stage | Parent Company Stage            | Notes                                                  |
| ----------------- | ------------------------------- | ------------------------------------------------------ |
| Stage 0           | Pre-Stage                       | No parent equivalent                                   |
| Stage 1           | Stage 1 (Requirements)          | Direct mapping — PRD + SRD                             |
| Stage 2           | Stage 2 (Design)                | HTML Prototype → Playable Prototype; IDS → GDS Package |
| Stage 3           | Stage 3 (Architecture)          | Vertical slice adds experiential validation            |
| Stage 4           | Stage 4 (Implementation Plan)   | Direct mapping                                         |
| Stage 5           | Stage 5 (Development)           | Mechanic sprint model replaces phase-based development |
| Stage 6           | **Stage 7 (Automated Testing)** | Direct mapping — Unity Test Runner + E2E + performance |
| Stage 7           | Stage 6 (Code Review)           | Adds pen test + soft launch prep                       |
| Stage 8           | **No parent equivalent**        | Soft launch is game-specific                           |
| Stage 9           | Stage 10 (Release Readiness)    | Combines parent Stages 7–10 into single launch gate    |
| Stage 10          | **No parent equivalent**        | Live ops is game-specific continuous stage             |

---

## 9. Document Version History

| Version | Date          | Author                        | Changes                                                             |
| ------- | ------------- | ----------------------------- | ------------------------------------------------------------------- |
| v1      | April 9, 2026 | CTO + CPO + CDO + CSO         | Initial game studio workflow — consolidated four-officer assessment |
| v1.2    | April 9, 2026 | CTO + Test Lead (CEO mandate) | Inserted Stage 6 (Automated Testing); renumbered Stages 6–9 → 7–10  |

---

_End of Game Studio Development Workflow_
