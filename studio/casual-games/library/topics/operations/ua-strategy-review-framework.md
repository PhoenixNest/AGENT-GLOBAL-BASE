# UA Strategy Review Framework

> **Owner:** Marcus Tran-Yoshida (CPO)
> **Trigger:** Pre-Stage 8 (Soft Launch) Entry Gate
> **Participants:** Rafael Santos (UA Specialist), Aisha Nkemelu (Live Ops Lead), Marcus Tran-Yoshida (CPO), Yuki Tanaka (Data Analyst)
> **Version:** 1.0
> **Date:** 2026-04-12

---

## 1. Executive Summary

This framework is created in direct response to **CPO Audit Condition CR-2**, which identified that Rafael Santos's hyper-casual UA experience may not directly translate to the casual-game market's CPI and ROAS dynamics. Hyper-casual and casual games operate on fundamentally different unit economics — casual games have higher CPIs, longer LTV curves, and rely more heavily on midcore monetization mechanics (IAP + hybrid ads) than hyper-casual's ad-revenue-dominant model.

**Purpose:** Establish a pre-defined, structured review framework that is ready to execute before Stage 8 (Soft Launch) entry. This ensures the UA plan is validated against casual-game benchmarks before committing soft-launch budget, preventing costly misalignment between acquisition strategy and actual market performance.

**Risk if skipped:** Proceeding to soft launch with a hyper-casual-calibrated UA plan will result in inflated CPIs, missed ROAS targets, and premature kill decisions on a potentially viable casual game.

---

## 2. Review Participants

| Participant             | Role          | Responsibility in Review                                                                                                                                               |
| ----------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Rafael Santos**       | UA Specialist | Presents the full UA plan: channel mix, budgets, creative strategy, CPI targets, ROAS targets, ASO approach, SKAdNetwork configuration                                 |
| **Aisha Nkemelu**       | Live Ops Lead | Validates UA plan against LTV:CAC targets; stress-tests monetization assumptions; ensures live ops cadence can support acquired user cohorts                           |
| **Marcus Tran-Yoshida** | CPO           | Strategic oversight; validates casual-game benchmark applicability; challenges assumptions that carry over from hyper-casual; final go/no-go authority on UA readiness |
| **Yuki Tanaka**         | Data Analyst  | Provides statistical validation of all projections; runs sensitivity analyses; validates sample sizes for creative testing; flags underpowered assumptions             |

---

## 3. Review Agenda (4-Hour Session)

### Hour 1: UA Plan Presentation — Rafael Santos

| Time      | Topic                      | Deliverable                                                        |
| --------- | -------------------------- | ------------------------------------------------------------------ |
| 0–15 min  | Channel strategy overview  | Channel mix rationale, expected spend split                        |
| 15–30 min | Budget allocation          | Per-channel budget, geo-tier breakdown, pacing schedule            |
| 30–45 min | Creative testing framework | Test volume (50+ concurrent), creative formats, kill/scale cadence |
| 45–60 min | Performance targets        | CPI by channel/geo, ROAS by D7/D14/D30, ASO strategy               |

**CPO Evaluation Lens During Hour 1:**

- Are CPI targets calibrated for casual-game norms, not hyper-casual?
- Is the creative strategy built around casual-game value props (progression, collection, narrative) vs. hyper-casual hooks (instant gratification, simple mechanics)?
- Is SKAdNetwork 4.0 configured for casual-game conversion events (tutorial complete, first purchase, session 3+) rather than hyper-casual events (session count, level reached)?

### Hour 2: Casual-Game Benchmark Comparison — CPO Office

| Time      | Topic                             | Deliverable                                                              |
| --------- | --------------------------------- | ------------------------------------------------------------------------ |
| 0–20 min  | CPI benchmark analysis            | Hyper-casual vs. casual CPI comparison by channel and geo                |
| 20–35 min | Retention curve comparison        | D1/D7/D30 retention benchmarks and their impact on LTV modeling          |
| 35–50 min | Monetization benchmark comparison | ARPDAU, paywall conversion, LTV:D1 ratios                                |
| 50–60 min | Gap identification                | Explicit list of UA plan assumptions that deviate from casual-game norms |

**Benchmark Table — Hyper-Casual vs. Casual:**

| Metric                 | Hyper-Casual Range | Casual Range  | Delta            |
| ---------------------- | ------------------ | ------------- | ---------------- |
| **CPI**                | $0.50 – $1.50      | $1.50 – $4.00 | **3×–5× higher** |
| **D1 Retention**       | 25–35%             | 40–55%        | **+15–20pp**     |
| **D7 Retention**       | 5–10%              | 15–25%        | **+10–15pp**     |
| **D30 Retention**      | 1–3%               | 8–15%         | **+7–12pp**      |
| **ARPDAU**             | $0.02 – $0.05      | $0.05 – $0.15 | **2×–3× higher** |
| **LTV:D1 (vs. CPI)**   | 0.5–1.0×           | 1.5–3.0×      | **3×–5× higher** |
| **Paywall Conversion** | 1–2%               | 3–8%          | **3×–4× higher** |

**CPO Interpretation Note:** The higher casual CPI is offset by significantly stronger retention and monetization depth. A UA plan that targets hyper-casual CPIs for a casual game will underbid and fail to acquire. A UA plan that uses casual-game CPIs without accounting for the longer LTV payback window will overreact to early negative ROAS and kill profitable cohorts prematurely.

### Hour 3: LTV:CAC Stress Test — Aisha Nkemelu + Yuki Tanaka

| Time      | Topic                             | Deliverable                                                    |
| --------- | --------------------------------- | -------------------------------------------------------------- |
| 0–15 min  | Baseline LTV model                | LTV projection using median casual-game assumptions            |
| 15–30 min | Worst-case scenario               | CPI at +50% of target, retention at –20%, monetization at –30% |
| 30–45 min | Best-case scenario                | CPI at –20% of target, retention at +15%, monetization at +25% |
| 45–60 min | Break-even & sensitivity analysis | Break-even day calculation, tornado diagram of key variables   |

**Stress Test Outputs Required:**

1. LTV:CAC ratio under baseline, worst-case, and best-case assumptions
2. Break-even day (when cumulative LTV = cumulative CAC) under each scenario
3. Sensitivity ranking: which single variable (CPI, D1 retention, D7 retention, ARPDAU, paywall conversion) has the largest impact on LTV:CAC?
4. Sample size validation: are creative test cohorts large enough to detect statistically significant CPI differences at 95% confidence?

### Hour 4: Decision & Documentation

| Time      | Topic                  | Deliverable                                                          |
| --------- | ---------------------- | -------------------------------------------------------------------- |
| 0–20 min  | Individual assessments | Each participant provides written assessment (Pass/Fail/Conditional) |
| 20–40 min | Group deliberation     | Discuss disagreements, identify required plan refinements            |
| 40–55 min | Decision               | Formal decision: PASS, ITERATE, or DEFER (see Section 6)             |
| 55–60 min | Documentation          | Sign-off captured in this document; action items logged              |

---

## 4. Casual-Game Benchmarks (Reference Table)

This table is the authoritative benchmark reference for all UA planning. Deviations from these ranges require explicit justification.

| Metric                 | Hyper-Casual  | Casual        | Source / Notes                                    |
| ---------------------- | ------------- | ------------- | ------------------------------------------------- |
| **CPI (Tier 1)**       | $0.50 – $1.50 | $1.50 – $4.00 | Meta Ads + Google UAC, US/UK/CA/AU                |
| **CPI (Tier 2)**       | $0.20 – $0.60 | $0.50 – $1.50 | Meta Ads + Google UAC, BR/IN/PH/ID                |
| **CPI (Tier 3)**       | $0.05 – $0.20 | $0.15 – $0.50 | Emerging markets                                  |
| **D1 Retention**       | 25–35%        | 40–55%        | Casual games benefit from progression hooks       |
| **D7 Retention**       | 5–10%         | 15–25%        | Collection and social features extend engagement  |
| **D30 Retention**      | 1–3%          | 8–15%         | Long-tail content drives sustained play           |
| **ARPDAU**             | $0.02 – $0.05 | $0.05 – $0.15 | Hybrid monetization (IAP + rewarded ads)          |
| **LTV:D1 (vs. CPI)**   | 0.5–1.0×      | 1.5–3.0×      | Casual games monetize later but more deeply       |
| **Paywall Conversion** | 1–2%          | 3–8%          | Casual players invest emotionally and financially |
| **D7 ROAS Target**     | 15–25%        | 25–40%        | Longer payback window requires patience           |
| **D30 ROAS Target**    | 40–60%        | 70–100%+      | Casual games approach breakeven by D30–D60        |

---

## 5. UA Plan Template (Required Submission from Rafael Santos)

Rafael Santos must submit the following UA plan document at least **5 business days** before the Stage 8 review session.

### 5.1 Channel Mix

| Channel                         | % of Budget | Rationale | Expected CPI (Tier 1) |
| ------------------------------- | ----------- | --------- | --------------------- |
| Meta Ads (Facebook + Instagram) |             |           |                       |
| Google UAC                      |             |           |                       |
| Apple Search Ads                |             |           |                       |
| TikTok Ads                      |             |           |                       |
| Other (specify)                 |             |           |                       |
| **Total**                       | **100%**    |           |                       |

### 5.2 Budget Allocation

| Geo Tier                        | Monthly Budget | Channels Active | Expected Installs/Month |
| ------------------------------- | -------------- | --------------- | ----------------------- |
| Tier 1 (US, UK, CA, AU, DE, FR) |                |                 |                         |
| Tier 2 (BR, MX, IN, PH, ID, TH) |                |                 |                         |
| Tier 3 (Other)                  |                |                 |                         |
| **Total**                       |                |                 |                         |

### 5.3 Creative Testing Framework

| Parameter                  | Specification                                                    |
| -------------------------- | ---------------------------------------------------------------- |
| Concurrent active tests    | ≥ 50                                                             |
| Creative formats           | Playable, video (15s, 30s), static, UGC-style                    |
| Kill threshold             | CPI > 1.5× target after 1,000 impressions                        |
| Scale threshold            | CPI < 0.8× target after 5,000 impressions with stable conversion |
| Refresh cadence            | New creative batch every 2 weeks                                 |
| Winning creative lifecycle | Scale until CPI degrades 20% from baseline, then rotate          |

### 5.4 CPI Targets by Channel and Geo

| Channel          | Tier 1 CPI Target | Tier 2 CPI Target | Tier 3 CPI Target |
| ---------------- | ----------------- | ----------------- | ----------------- |
| Meta Ads         |                   |                   |                   |
| Google UAC       |                   |                   |                   |
| Apple Search Ads |                   |                   | N/A               |
| TikTok Ads       |                   |                   |                   |

### 5.5 ROAS Targets

| Metric         | Target | Notes                           |
| -------------- | ------ | ------------------------------- |
| D7 ROAS        |        | Casual-game benchmark: 25–40%   |
| D14 ROAS       |        | Casual-game benchmark: 50–70%   |
| D30 ROAS       |        | Casual-game benchmark: 70–100%+ |
| Break-even day |        | Target: ≤ 60 days               |

### 5.6 ASO Strategy

| Element                      | Approach |
| ---------------------------- | -------- |
| App Title                    |          |
| Subtitle / Short Description |          |
| Keyword Strategy             |          |
| Screenshot Strategy          |          |
| Video Preview                |          |
| Rating Management            |          |

### 5.7 SKAdNetwork 4.0 Configuration

| Parameter                    | Specification                                                 |
| ---------------------------- | ------------------------------------------------------------- |
| Conversion value schema      |                                                               |
| Coarse-grained value mapping |                                                               |
| Postback timer configuration |                                                               |
| Key events tracked           | (e.g., tutorial_complete, first_purchase, session_3, level_5) |
| Privacy threshold strategy   |                                                               |

---

## 6. Decision Criteria

| Decision    | Criteria                                                                                                                                                                                                                                    | Consequence                                                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PASS**    | • All casual-game benchmarks met or exceeded<br>• LTV:CAC ≥ 1.5 at conservative (worst-case) assumptions<br>• Creative testing framework meets 50+ concurrent test threshold<br>• SKAdNetwork 4.0 configured for casual-game events         | Proceed to Stage 8 (Soft Launch) with approved UA plan                                                                                                                |
| **ITERATE** | • Some benchmarks missed but within acceptable range<br>• LTV:CAC 1.2–1.5 at conservative assumptions<br>• Creative testing framework has gaps but is salvageable<br>• SKAdNetwork 4.0 configuration needs adjustment                       | UA plan requires refinement. 2-week iteration window. Re-review required before Stage 8 entry.                                                                        |
| **DEFER**   | • LTV:CAC < 1.2 at conservative assumptions<br>• CPI targets significantly below casual-game norms (indicating underbidding risk)<br>• Creative testing framework insufficient for statistical validity<br>• SKAdNetwork 4.0 not configured | Soft launch delayed. UA plan must be rebuilt with casual-game benchmarks. No Stage 8 entry until re-review achieves PASS or ITERATE with acceptable remediation plan. |

---

## 7. Output & Sign-Off

Upon completion of the review, the following outputs are produced:

1. **Completed UA Plan** — Rafael Santos's plan with all template sections filled
2. **Benchmark Comparison Matrix** — CPO office's gap analysis against casual-game norms
3. **LTV:CAC Stress Test Report** — Aisha Nkemelu and Yuki Tanaka's analysis with all three scenarios
4. **Decision Record** — Formal decision (PASS / ITERATE / DEFER) with rationale
5. **Action Items** — Specific, dated, owner-assigned tasks for any ITERATE conditions

### Sign-Off Table

| Participant         | Role          | Signature | Date | Decision |
| ------------------- | ------------- | --------- | ---- | -------- |
| Rafael Santos       | UA Specialist |           |      |          |
| Aisha Nkemelu       | Live Ops Lead |           |      |          |
| Marcus Tran-Yoshida | CPO           |           |      |          |
| Yuki Tanaka         | Data Analyst  |           |      |          |

---

> **CPO Note:** This framework exists because I have seen UA plans fail at soft launch when hyper-casual instincts are applied to casual economics. The CPI delta alone (3×–5×) is enough to blow a soft-launch budget in the first week if the UA team is bidding for hyper-casual users. This review is not optional — it is a gate criterion for Stage 8 entry.
>
> — Marcus Tran-Yoshida, CPO
