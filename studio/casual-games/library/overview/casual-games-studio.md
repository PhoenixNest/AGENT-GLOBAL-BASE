# Casual Games Studio — Strategic Brief

**Document Type:** Studio Charter & Strategic Assessment  
**Status:** Proposal — C-Suite Review Complete  
**Date:** April 9, 2026  
**Initiative:** Establish a dedicated mobile game studio focused on casual mini-games using the Unity game engine

---

## 1. Initiative Overview

Our company, currently focused on mobile platform products, intends to establish a **dedicated mobile game studio** targeting the casual mini-game market. This studio will operate as a **separate organizational unit** with its own brand identity, team, technical pipeline, and ways of working — distinct from our core app engineering organization.

### Scope

| Dimension            | Definition                                                          |
| -------------------- | ------------------------------------------------------------------- |
| **Product Category** | Casual mini-games (hybrid-casual tier — quality over volume)        |
| **Technology**       | Unity game engine (Unity 6.3 LTS), C#                               |
| **Target Platforms** | iOS + Android                                                       |
| **Monetization**     | Free-to-play: rewarded video ads + IAP + optional subscription tier |
| **Distribution**     | App Store (iOS), Google Play (Android)                              |
| **Studio Model**     | Separate department, direct reporting to User (CEO), NOT under R&D  |

---

## 2. C-Suite Assessments

### 2.1 CPO — Marcus Tran-Yoshida (Product Strategy)

**Verdict:** Conditional GO

- Casual mini-games represent ~45% of mobile game downloads, but the competitive bar has risen dramatically — Voodoo, SayGames, and Rollic have industrialized the pipeline
- **Our asymmetric advantage:** retention engineering, subscription monetization architecture, and A/B testing infrastructure (Duolingo DNA)
- **Recommended monetization:** Free-to-play with rewarded video (primary), IAP for cosmetic/functional items, monthly subscription removing ads and unlocking premium content
- **Soft launch is non-negotiable** — validate in 3–5 Tier-2 markets (Canada, Australia, Philippines, Brazil, Norway) before global UA spend
- **Kill criteria (all must be met) — retention thresholds are genre-calibrated.** Each title declares its genre at Stage 0/1 of the studio pipeline; that declaration locks the applicable retention row for the rest of the title's life. Genre is reviewed only on a documented pivot (which itself is a Stage-0 re-entry). Non-retention criteria (LTV:CAC, ARPDAU, paywall conversion, App Store rating) remain genre-blind because they reflect business-model viability, not engagement curves.

  | Genre                                                    | D1 Retention | D7 Retention | D30 Retention | Industry anchor                                              |
  | :------------------------------------------------------- | :----------: | :----------: | :-----------: | :----------------------------------------------------------- |
  | **Hybrid-casual** _(this studio's default per §1 Scope)_ |    ≥ 35%     |    ≥ 12%     |     ≥ 5%      | Voodoo / SayGames / Rollic top-quartile titles               |
  | **Mid-core puzzle**                                      |    ≥ 40%     |    ≥ 18%     |     ≥ 8%      | King "Candy-Crush-class" releases; deeper meta loops         |
  | **Pure-casual**                                          |    ≥ 30%     |    ≥ 10%     |     ≥ 4%      | King's Candy Crush averages D1 ~30%; mass-market expectation |
  - LTV:CAC ≥ 1.5 _(genre-blind)_
  - ARPDAU ≥ $0.04 _(genre-blind)_
  - Paywall Conversion ≥ 3% _(genre-blind)_
  - App Store Rating ≥ 4.2 _(genre-blind)_

  > **Genre-lookup audit rule.** The Stage 0 / Stage 1 PRD must explicitly cite which genre row applies to that title. The Studio Director and CPO co-sign the genre lock. If a title fails its genre-row retention floor, the kill decision is non-negotiable — it is **not** valid to retroactively reclassify a hybrid-casual title to "pure-casual" to dodge the 35% D1 floor. Reclassification triggers a Stage 0 re-entry and a new soft launch.

- **Investment cap:** $1.1M total for Phase 0 + Phase 1. No exceptions.
- **Risk:** Single-title strategy has unacceptable risk; multi-title strategy multiplies cost. Portfolio approach required.

### 2.2 CTO — Dr. Kenji Nakamura (Technical Architecture)

**Verdict:** Approve with conditions

- **Unity is the correct technology choice** for casual mini-games — mature 2D tooling, cross-platform deployment, monetization SDK ecosystem
- **Lock to Unity 6.3 LTS** (supported through December 2027) — avoid tech stream/beta releases for production; evaluate Unity 6.7 LTS when released Q4 2026
- **Critical skills gap:** Our existing mobile engineers (Kotlin/Swift/Dart/Flutter) have zero Unity/C# transferability. Core game development must be staffed with experienced Unity developers.
- **Recommended Phase 1 hiring:**
  - Lead Unity Developer (Senior, 5+ years, 2+ shipped titles) — P0
  - Unity Developer (Mid-level) × 2 — P0
  - Technical Artist — P1
  - Game Designer / Producer — P1
  - QA Specialist (Game Testing) — P2
- **Unity must be treated as a standalone platform** — not an extension of existing mobile app architecture
- **App binary size budget:** <50 MB initial download. Use Addressables for all non-critical assets.
- **Performance budget:** 30 FPS minimum, 150 MB RAM maximum, target Android 8+ with 2 GB RAM
- **Pipeline adaptation needed:** Our 10-stage development pipeline requires game-specific modifications (GDD as paired artifact, playable prototype instead of HTML, gameplay review alongside code review, device matrix testing)
- **Proof-of-concept first:** Ship 1 simple mini-game (single mechanic, 2-week prototype target) before committing to full studio model

### 2.3 CDO — Yuki Tanaka-Chen (Design & UX)

**Verdict:** Conditional approval

- **Games and apps share a screen but not a design language.** Our app design system's principles (efficiency, clarity, minimalism) actively work against game engagement.
- **Brand architecture: House of Brands.** Parent company → Game Studio (endorsed brand) → Individual game titles (standalone brands). Each game failure should not poison the parent brand.
- **Design principles for casual games:**
  - Session length: 30-second loops compounding into 20-minute engagement
  - Zero-tutorial ideal — first interaction IS the tutorial
  - Juice (screen shake, particles, haptics) is the value proposition, not decoration
  - Failure must feel like "almost won" — instant retry in <1 second
- **Platform-native meta UI:** Game canvas identical across platforms, but menus/settings/store/IAP use platform-native wrappers (iOS HIG on iOS, Material on Android)
- **Day-one accessibility requirements:**
  - Colorblind mode (3 presets, never use color as sole information carrier)
  - Motor accessibility (adjustable tap targets, one-hand mode, auto-fire option)
  - Cognitive load controls (adjustable game speed, pause-anywhere)
  - Screen reader support for all menus
  - Visual indicators for all audio cues
- **Live ops design:** Permanent design sprint cycle — seasonal content, events, progression tracks. Design team never stops designing.
- **Prerequisites:** Separate game design headcount (3 FTEs minimum), game accessibility consultant, Unity designer tooling, Game IDS Template authored before implementation

### 2.4 CIO — Dr. Priya Mehta (Technology Strategy & Information Systems)

**Verdict:** Conditionally Approve

- **First-year technology investment:** $2.4M–$3.8M (infrastructure, tooling, licensing, talent enablement — excluding personnel costs)
- **Build vs. Buy backend:** Recommend **PlayFab (Microsoft)** as primary game backend — strongest feature completeness with moderate vendor lock-in. Unity Gaming Services is attractive but creates unacceptable lock-in given Unity's pricing instability.
- **Self-hosting is not recommended** for a greenfield studio — engineering cost of building multiplayer infrastructure would divert 6–12 months from game development
- **Game analytics operate at 10–100× the event volume** of existing mobile app telemetry — requires separate data pipeline
- **Proposed data architecture:** PlayFab Events → Kafka (existing) → Data Lake (S3/Azure Blob) → BI Dashboards (Game BI + Executive Reporting)
- **Unity licensing risk:** Runtime fee policy volatility demonstrated in 2024. Contractually negotiate fixed pricing for 3+ years. Maintain documented exit plan (Godot/Unreal migration assessment).
- **COPPA compliance is critical** — if any game targets or attracts users under 13, COPPA compliance is mandatory with significant penalties. This is new regulatory ground for the company.
- **Build for multi-tenancy from Day 1** — even with one game, architect backend as multi-tenant. Retrofit cost is 3–5× original investment.
- **Immediate actions:**
  1. Commission Unity licensing legal review (Week 1–2)
  2. COPPA compliance assessment (Week 1–3)
  3. PlayFab technical evaluation (Week 3–6)
  4. Recruit Game Technical Director (Week 1–12)

### 2.5 CHRO — Dr. Evelyn Hartwell (Human Resources & Organizational Design)

**Verdict:** Proceed with conditions

- **Current mobile app engineers cannot build games.** Zero skill overlap for core game development roles.
- **Minimum viable team:** 8–12 people. Cannot ship a credible game with fewer.
- **Compensation premium:** 15–25% above current mobile app engineering benchmarks across all game studio roles
- **Organizational structure:** Establish as a **separate department** under a new **Studio Head / CCO** (external hire, game industry veteran). NOT under R&D.
- **Rationale for separation:**
  - R&D culture is pipeline-driven; game development is iterative and playtest-driven
  - Our 10-stage pipeline assumes utility apps — forcing a game team through gate reviews is "like putting a race car through a DMV inspection"
  - Unity/C# has nothing to do with our Kotlin/Swift/Dart/Flutter stack
  - Game developers report to creative directors and producers, not engineering managers
- **Recruiting strategy:** Shipped title poaching (most effective) → Game jams → Unity communities → Conferences → LinkedIn (least effective). ~85% of good game talent is passive.
- **Employer brand challenge:** Our current brand signals "enterprise, process, compliance" — repellent to game talent who seek creative freedom and shipped games. We need a separate studio identity before recruiting.
- **Critical retention principle:** Game developers stay for the game, not the company. If the game is cancelled or creatively compromised, they leave regardless of compensation.
- **Onboarding:** Requires a completely separate track — play immersion, creative onboarding, game culture integration. Cannot reuse existing engineering onboarding.
- **Recommended sequence:**
  1. Hire Studio Head first (external, 2+ shipped casual games)
  2. Establish department separately (own budget, own reporting)
  3. Recruit founding team as a unit (Producer, Lead Designer, Lead Unity Dev within 60 days)
  4. Build employer brand before job postings

---

## 3. Unified Risk Register

| ID  | Risk                                                              | Severity | Owner     | Mitigation                                                              |
| --- | ----------------------------------------------------------------- | -------- | --------- | ----------------------------------------------------------------------- |
| R1  | No internal game dev expertise — first title quality insufficient | 🔴 P0    | CHRO      | Hire Studio Head + Lead Unity Developer before project kickoff          |
| R2  | Capital burn without proven unit economics                        | 🔴 P0    | CPO       | Cap Phase 0+1 at $1.1M; hard kill criteria; soft launch validation      |
| R3  | COPPA / minors data compliance failure                            | 🔴 P0    | CIO + CSO | Legal review before any game design finalized                           |
| R4  | Unity licensing policy change                                     | 🟠 P1    | CIO       | Fixed-price contract 3+ years; exit plan documented                     |
| R5  | Brand dilution from game failures                                 | 🟠 P1    | CDO       | House of brands architecture; separate studio identity                  |
| R6  | Cultural mismatch with game talent — retention risk               | 🟠 P1    | CHRO      | Separate department; creative autonomy; Studio Head authority           |
| R7  | App binary size exceeds platform/download limits                  | 🟠 P1    | CTO       | <50 MB budget; Addressables from Day 1; weekly profiling                |
| R8  | Performance degradation on low-end Android devices                | 🟠 P1    | CTO       | Define minimum device spec; 15+ device testing matrix; 30 FPS floor     |
| R9  | Game economy fails to achieve target ARPDAU                       | 🟠 P1    | CPO       | Soft launch; A/B test via Remote Config; hire experienced Game Designer |
| R10 | Third-party SDK conflicts (ads, analytics, IAP)                   | 🟡 P2    | CTO       | SDK compatibility matrix; pre-release device testing                    |

---

## 4. Recommended Phased Approach

### Phase 0: Foundation (6–8 weeks)

| Action                                          | Owner             | Budget             |
| ----------------------------------------------- | ----------------- | ------------------ |
| Hire Studio Head / CCO (external game veteran)  | CHRO              | Included in hiring |
| Commission Unity licensing legal review         | CIO + Legal       | $10K–$20K          |
| COPPA compliance assessment                     | CSO + Legal       | $10K–$20K          |
| Recruit Lead Unity Developer (contract advisor) | CHRO + CTO        | $10K–$20K          |
| Commission 3 game concept briefs                | CPO + Studio Head | $10K–$20K          |
| Procure Unity Pro licenses + tooling            | CIO               | $40K–$80K          |
| **Phase 0 Total**                               |                   | **$80K–$160K**     |

### Phase 1: Proof-of-Concept (4–6 months)

| Action                                         | Owner             | Budget                      |
| ---------------------------------------------- | ----------------- | --------------------------- |
| Hire founding team (6 roles — see Section 2.2) | CHRO              | Included in personnel       |
| Build single-title MVP                         | CTO + Studio Head | $300K–$500K                 |
| Instrument full analytics suite                | CIO + Test Lead   | $50K–$100K                  |
| Soft launch in Canada + Australia              | CPO               | $100K–$200K (UA test spend) |
| Iterate based on data (60–90 days)             | CPO + Studio Head | $50K–$100K                  |
| **Phase 1 Total**                              |                   | **$500K–$900K**             |

### Phase 2: Go/No-Go Decision

- **If benchmarks met** (all kill criteria from Section 2.1): Expand team to 12–15, begin second title, invest in UA infrastructure
- **If benchmarks missed:** Wind down studio, retain learnings, no further investment. **No sunk cost fallacy.**

### Combined Investment Cap: $1.1M (Phase 0 + Phase 1)

---

## 5. Organizational Structure

```
User (CEO)
 │
 ├── Studio Head / CCO (new hire — game industry veteran)
 │    ├── Game Producer (1–2)
 │    ├── Game Designer (1–2)
 │    ├── Lead Unity Developer
 │    ├── Unity Developer × 2
 │    ├── Technical Artist
 │    └── Game QA
 │
 ├── CTO (existing — advisory on technical governance)
 ├── CPO (existing — advisory on product-market fit)
 ├── CDO (existing — advisory on visual quality bar)
 ├── CIO (existing — technology governance, infrastructure)
 └── CHRO (existing — recruiting, onboarding)
```

**Key principle:** The game studio is a separate department with its own budget, identity, and ways of working. Existing C-suite officers serve in advisory and governance roles, not direct management.

---

## 6. Pipeline Adaptation for Game Development

Our standard 10-stage pipeline requires the following game-specific adaptations:

| Stage    | Standard Process       | Game Studio Adaptation                                                                   |
| -------- | ---------------------- | ---------------------------------------------------------------------------------------- |
| Stage 1  | PRD + SRD              | Add **Game Design Document (GDD)** as paired artifact                                    |
| Stage 2  | HTML Prototype + IDS   | **Unity playable prototype** + Game IDS                                                  |
| Stage 3  | UML + ADRs + TSD       | Add GDD → technical mapping; UML for game state machines                                 |
| Stage 4  | Implementation Plan    | Add milestone delivery: vertical slice → alpha → beta → soft launch → global             |
| Stage 5  | Platform code          | **Unity project** + content/asset pipeline as parallel workstream                        |
| Stage 6  | Code Review            | Add **gameplay review** (playtest for game feel, balance, fun factor)                    |
| Stage 7  | Automated Testing      | Add **device matrix testing** (20+ Android devices), performance benchmarks, playtesting |
| Stage 8  | Integrity Verification | Add **live ops readiness check** (remote config, analytics, monetization, cloud save)    |
| Stage 9  | i18n Engineering       | Add text expansion for game UI; cultural adaptation for game content                     |
| Stage 10 | Release Readiness      | Add platform game requirements: age rating (ESRB/PEGI/GRAC), loot box compliance         |

---

## 7. First-Year Technology Investment Summary

| Category                                     | Estimated Cost  |
| -------------------------------------------- | --------------- |
| Unity Pro / Enterprise licenses              | $40K–$80K       |
| Game backend platform (PlayFab)              | $60K–$240K      |
| CDN and edge infrastructure                  | $30K–$60K       |
| CI/CD for game builds                        | $25K–$50K       |
| Analytics & telemetry infrastructure         | $20K–$40K       |
| Device testing matrix (15+ physical devices) | $15K–$30K       |
| Third-party SDKs and services                | $20K–$40K       |
| Legal (licensing review, COPPA compliance)   | $20K–$40K       |
| **Total Technology Investment**              | **$230K–$580K** |

_Note: Personnel costs (8–12 hires at 15–25% premium) are additional and not included above._

---

## 8. Decision Status

| Officer | Verdict                    | Conditions                                                  |
| ------- | -------------------------- | ----------------------------------------------------------- |
| CPO     | ✅ Conditional GO          | Cap at $1.1M; hard kill criteria                            |
| CTO     | ✅ Approve with conditions | Dedicated team; PoC first; separate pipeline                |
| CDO     | ✅ Conditional approval    | Separate brand; game design headcount; accessibility        |
| CIO     | ✅ Conditional GO          | Unity licensing locked; COPPA resolved; Tech Director hired |
| CHRO    | ✅ Proceed with conditions | Studio Head first; separate department; not under R&D       |

**Overall Status:** C-Suite consensus for conditional approval. **Awaiting User (CEO) final go/no-go decision.**

---

## 9. Document Version History

| Version | Date           | Author                | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------- | -------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v1      | April 9, 2026  | C-Suite Panel         | Initial charter — consolidated CPO, CTO, CDO, CIO, CHRO assessments                                                                                                                                                                                                                                                                                                                                                                    |
| v1.1    | April 9, 2026  | CTO correction        | Updated Unity version: "2023 LTS" → "Unity 6.3 LTS" (Unity changed versioning scheme)                                                                                                                                                                                                                                                                                                                                                  |
| v1.2    | April 21, 2026 | Studio Director + CPO | **§2.1 retention kill thresholds calibrated by genre.** Replaced the genre-blind D1 ≥ 40% / D7 ≥ 15% / D30 ≥ 8% with a 3-row genre-calibrated table — Hybrid-casual ≥ 35/12/5 (this studio's default), Mid-core puzzle ≥ 40/18/8, Pure-casual ≥ 30/10/4. Added a genre-lookup audit rule preventing post-hoc reclassification to dodge a stricter row. Non-retention criteria (LTV:CAC, ARPDAU, paywall conversion, rating) unchanged. |

---

_End of Casual Games Studio Strategic Brief_
