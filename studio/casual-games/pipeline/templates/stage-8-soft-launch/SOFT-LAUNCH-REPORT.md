# Soft Launch Report — Template

> **Stage:** 8 — Soft Launch
> **Producer:** Live Ops Lead + Studio Director (Dr. Marcus Vogel)
> **Kill Gate:** KG-5 — Soft Launch Evaluation
> **User Approval:** ✅ Required — decision gates global launch vs extend/kill

---

## Document Control

| Field                      | Value           |
| :------------------------- | :-------------- |
| **Game Title**             | [Working title] |
| **Soft Launch Markets**    | [Markets]       |
| **Soft Launch Start Date** | YYYY-MM-DD      |
| **Report Date**            | YYYY-MM-DD      |
| **Report Period**          | [N weeks]       |
| **Author**                 | [Live Ops Lead] |

---

## 1. Retention Metrics

| Metric                  | Target (KG-5) | Actual | Trend   | Pass? |
| :---------------------- | :-----------: | :----: | :------ | :---: |
| D1 Retention            |    ≥ [X]%     |        | [↑/↓/→] |   ☐   |
| D7 Retention            |    ≥ [X]%     |        | [↑/↓/→] |   ☐   |
| D14 Retention           |    ≥ [X]%     |        | [↑/↓/→] |   ☐   |
| D30 Retention           |    ≥ [X]%     |        | [↑/↓/→] |   ☐   |
| Sticky factor (DAU/MAU) |    ≥ [X]%     |        | [↑/↓/→] |   ☐   |

---

## 2. Revenue Metrics

| Metric                     | Target (KG-5) | Actual | Trend   | Pass? |
| :------------------------- | :-----------: | :----: | :------ | :---: |
| ARPDAU                     |   ≥ $[X.XX]   |        | [↑/↓/→] |   ☐   |
| Conversion rate (% paying) |    ≥ [X]%     |        | [↑/↓/→] |   ☐   |
| LTV (D30 estimate)         |   ≥ $[X.XX]   |        | [↑/↓/→] |   ☐   |
| LTV:CAC ratio              |    ≥ [X.X]    |        | [↑/↓/→] |   ☐   |

---

## 3. Engagement Metrics

| Metric                           |  Target   | Actual | Trend |
| :------------------------------- | :-------: | :----: | :---- |
| Average sessions per DAU per day |   ≥ [X]   |        |       |
| Average session length           | ≥ [X] min |        |       |
| Levels completed per session     |   ≥ [X]   |        |       |
| MAU at [N] weeks                 | ≥ [N,NNN] |        |       |

---

## 4. Technical Health

| Metric                  | Target  | Actual | Pass? |
| :---------------------- | :-----: | :----: | :---: |
| Crash-free session rate | ≥ 99.0% |        |   ☐   |
| ANR rate (Android)      | ≤ 0.5%  |        |   ☐   |
| API error rate          | ≤ 1.0%  |        |   ☐   |
| Average load time       | < [X]s  |        |   ☐   |

---

## 5. Market Tier Assessment

> Reference: `MARKET-TIER-CRITERIA.md`

| Tier       | Definition                                                           | Does this game qualify? |
| :--------- | :------------------------------------------------------------------- | :---------------------: |
| **Tier A** | KG-5 metrics significantly exceed thresholds; launch globally now    |            ☐            |
| **Tier B** | KG-5 metrics meet thresholds; standard global launch                 |            ☐            |
| **Tier C** | KG-5 metrics partially met; targeted release or extended soft launch |            ☐            |
| **Kill**   | KG-5 metrics not met; project killed or pivoted                      |            ☐            |

**Assessment rationale:** [2–3 sentences]

---

## 6. KG-5 Security Gates

| Gate                                                   |   Status    | Notes |
| :----------------------------------------------------- | :---------: | :---- |
| CSO final sign-off                                     | ☐ Approved  |       |
| Pen test (if new vulnerabilities found in soft launch) |  ☐ Passed   |       |
| GDPR/CCPA compliance confirmed in all launch markets   | ☐ Confirmed |       |
| No PII incidents during soft launch                    | ☐ Confirmed |       |

**CSO Sign-off:** [Dr. Sarah Chen] — ☐ Cleared for global launch

---

## 7. Kill Gate 5 Decision

| Criterion              | Status            |
| :--------------------- | :---------------- |
| D30 retention ≥ target | ☐ Met / ☐ Not met |
| ARPDAU ≥ target        | ☐ Met / ☐ Not met |
| LTV:CAC ≥ target       | ☐ Met / ☐ Not met |
| Crash-free rate ≥ 99%  | ☐ Met / ☐ Not met |
| CSO sign-off           | ☐ Cleared         |

**Studio Director recommendation:** ☐ Global launch / ☐ Extended soft launch / ☐ Pivot / ☐ Kill

**Rationale:** [2–3 sentences]

---

**Produced by:** [Live Ops Lead] on YYYY-MM-DD
**Studio Director:** [Dr. Marcus Vogel] on YYYY-MM-DD
**Awaiting User (CEO) global launch decision.**
