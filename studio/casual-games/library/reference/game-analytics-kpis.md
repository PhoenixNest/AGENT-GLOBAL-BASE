# Game Analytics & KPIs

**Last Updated:** April 9, 2026

---

## 1. Core Game KPIs

### 1.1 Retention Metrics

| Metric              | Definition                                              | Industry Benchmark (Casual) | Our Target |
| ------------------- | ------------------------------------------------------- | --------------------------- | ---------- |
| **D1 Retention**    | % of players who return on Day 1 after install          | 25–35%                      | ≥ 40%      |
| **D7 Retention**    | % of players who return on Day 7 after install          | 8–12%                       | ≥ 15%      |
| **D30 Retention**   | % of players who return on Day 30 after install         | 3–6%                        | ≥ 5%       |
| **Day 0 Retention** | % of players who complete tutorial and play ≥ 1 session | 60–70%                      | ≥ 75%      |

**Interpretation:**

| Pattern           | Meaning                                      | Action                                          |
| ----------------- | -------------------------------------------- | ----------------------------------------------- |
| D1 high, D7 low   | Game is fun initially but lacks depth        | Add progression systems, content variety        |
| D1 low, D7 stable | Onboarding is broken; those who stay love it | Fix tutorial, first-time user experience        |
| All retention low | Core loop is not fun                         | Back to prototype — fundamental redesign needed |
| D30 > D7          | Rare — indicates strong community/loyalty    | Double down on social features                  |

### 1.2 Monetization Metrics

| Metric               | Definition                                  | Industry Benchmark (Casual) | Our Target                                  |
| -------------------- | ------------------------------------------- | --------------------------- | ------------------------------------------- |
| **ARPDAU**           | Average Revenue Per Daily Active User       | $0.02–$0.08                 | ≥ $0.05 (hyper-casual) / ≥ $0.15 (mid-core) |
| **LTV (D30)**        | Lifetime Value at Day 30                    | $0.50–$2.00                 | ≥ $1.00                                     |
| **LTV (D90)**        | Lifetime Value at Day 90                    | $1.00–$5.00                 | ≥ $3.00                                     |
| **LTV:CAC Ratio**    | Lifetime Value ÷ Customer Acquisition Cost  | 1.0–2.0                     | ≥ 1.5 (minimum) / ≥ 3.0 (healthy)           |
| **Payer Conversion** | % of players who make at least one purchase | 2–5%                        | ≥ 3%                                        |
| **ARPPU**            | Average Revenue Per Paying User             | $10–$50                     | Track for economy tuning                    |

### 1.3 Engagement Metrics

| Metric                       | Definition                                | Benchmark                  | Notes                                                             |
| ---------------------------- | ----------------------------------------- | -------------------------- | ----------------------------------------------------------------- |
| **Session Length**           | Average time per play session             | 3–8 minutes (casual)       | Longer ≠ better — casual games thrive on short, frequent sessions |
| **Sessions Per Day**         | Average sessions per DAU                  | 3–6                        | Indicates habit formation                                         |
| **DAU/MAU Ratio**            | Daily Active Users ÷ Monthly Active Users | 15–25%                     | Higher = stickier game                                            |
| **Tutorial Completion Rate** | % of players who complete onboarding      | 70–85%                     | < 60% indicates tutorial is broken                                |
| **Level Completion Rate**    | % of players who complete each level      | Varies by difficulty curve | Should be 70–90% for casual games                                 |

---

## 2. Event Taxonomy

### 2.1 Standard Events

| Event Name          | Parameters                                             | Triggered When                                  |
| ------------------- | ------------------------------------------------------ | ----------------------------------------------- |
| `game_start`        | `session_id`, `player_level`, `total_sessions`         | Player opens game                               |
| `game_end`          | `session_id`, `session_duration`, `levels_played`      | Player closes game                              |
| `level_start`       | `level_id`, `attempt_number`                           | Level begins                                    |
| `level_complete`    | `level_id`, `score`, `duration`, `stars_earned`        | Level completed successfully                    |
| `level_fail`        | `level_id`, `fail_reason`, `progress_pct`              | Level failed                                    |
| `tutorial_step`     | `step_id`, `duration`                                  | Tutorial step completed                         |
| `tutorial_complete` | `total_duration`                                       | Entire tutorial finished                        |
| `iap_purchase`      | `product_id`, `price`, `currency`, `is_first_purchase` | In-app purchase completed                       |
| `ad_impression`     | `ad_type`, `ad_placement`, `revenue`, `network`        | Ad displayed                                    |
| `ad_click`          | `ad_type`, `ad_placement`                              | Ad clicked                                      |
| `reward_claimed`    | `reward_type`, `reward_amount`, `source`               | Player claims reward (daily, achievement, etc.) |
| `currency_spent`    | `currency_type`, `amount`, `item_purchased`            | Player spends currency                          |
| `currency_earned`   | `currency_type`, `amount`, `source`                    | Player earns currency                           |
| `settings_changed`  | `setting_name`, `new_value`                            | Player changes a setting                        |
| `social_share`      | `share_type`, `platform`                               | Player shares to social media                   |

### 2.2 Custom Events

| Event Name          | Parameters                                    | Purpose                                            |
| ------------------- | --------------------------------------------- | -------------------------------------------------- |
| `funnel_dropoff`    | `funnel_stage`, `screen_name`                 | Track where players abandon key flows              |
| `rage_quit`         | `level_id`, `death_count`, `session_duration` | Detect frustration (multiple rapid deaths + quit)  |
| `economy_imbalance` | `currency_balance`, `days_active`             | Detect players with abnormal currency accumulation |

---

## 3. Analytics Instrumentation

### 3.1 Recommended Stack

| Tool                     | Purpose                                                         | Cost                          |
| ------------------------ | --------------------------------------------------------------- | ----------------------------- |
| **GameAnalytics**        | Game-specific dashboards (retention, monetization, progression) | Free                          |
| **Firebase Analytics**   | General app analytics, funnel analysis, A/B testing             | Free tier generous            |
| **Firebase Crashlytics** | Crash reporting                                                 | Free                          |
| **Custom Backend**       | Economy tracking, fraud detection, LTV calculation              | Infrastructure cost           |
| **Unity Remote Config**  | A/B testing of game parameters                                  | Free (within Unity ecosystem) |

### 3.2 Implementation Pattern

```csharp
public class AnalyticsService : IAnalyticsService
{
    public void TrackEvent(string eventName, Dictionary<string, object> parameters = null)
    {
        // GameAnalytics
        if (parameters != null)
            GameAnalytics.NewDesignEvent(eventName, parameters);
        else
            GameAnalytics.NewDesignEvent(eventName);

        // Firebase (mirror)
        if (parameters != null)
        {
            var firebaseParams = parameters.ToDictionary(
                kvp => kvp.Key,
                kvp => new Firebase.Analytics.Parameter(kvp.Key, kvp.Value)
            );
            Firebase.Analytics.FirebaseAnalytics.LogEvent(eventName, firebaseParams.ToArray());
        }
        else
        {
            Firebase.Analytics.FirebaseAnalytics.LogEvent(eventName, null);
        }
    }

    public void TrackRevenue(string currency, int amount, string itemType = null)
    {
        GameAnalytics.NewBusinessEvent(currency, amount, itemType);
    }

    public void TrackError(string errorType, string errorMessage)
    {
        GameAnalytics.NewErrorEvent(GameAnalyticsSDK.GameAnalytics.GAErrorType.Unity, errorMessage);
    }
}
```

---

## 4. Dashboard Design

### 4.1 Executive Dashboard (C-Suite View)

| Widget                      | Metric                                | Refresh   |
| --------------------------- | ------------------------------------- | --------- |
| **DAU / MAU**               | Active users                          | Daily     |
| **D1 / D7 / D30 Retention** | Retention curves                      | Daily     |
| **ARPDAU**                  | Revenue efficiency                    | Daily     |
| **LTV:CAC**                 | Unit economics                        | Weekly    |
| **Revenue (daily)**         | Total revenue breakdown (ads vs. IAP) | Daily     |
| **Crash-free rate**         | Technical stability                   | Real-time |
| **Top 10 markets**          | Geographic distribution               | Weekly    |

### 4.2 Game Team Dashboard (Operational View)

| Widget                  | Metric                                           | Refresh |
| ----------------------- | ------------------------------------------------ | ------- |
| **Session metrics**     | Avg session length, sessions/DAU                 | Daily   |
| **Level progression**   | Funnel: how many players reach each level        | Daily   |
| **Economy health**      | Total currency in circulation, sinks vs. sources | Daily   |
| **Ad performance**      | eCPM, fill rate, impressions per DAU             | Daily   |
| **IAP conversion**      | Purchase funnel: view → click → purchase         | Daily   |
| **Rage quit rate**      | Frustration detection by level                   | Daily   |
| **Tutorial completion** | Onboarding effectiveness                         | Daily   |

### 4.3 Live Ops Dashboard (Post-Launch View)

| Widget                   | Metric                                    | Refresh   |
| ------------------------ | ----------------------------------------- | --------- |
| **Event participation**  | % of DAU participating in current event   | Real-time |
| **Event revenue**        | Revenue generated by current event        | Real-time |
| **Content consumption**  | How fast players consume new content      | Daily     |
| **Community sentiment**  | Social media sentiment analysis           | Daily     |
| **Leaderboard activity** | Number of submissions, score distribution | Hourly    |

---

## 5. Funnel Analysis

### 5.1 Core Funnels to Track

| Funnel                         | Steps                                                                         | Drop-off Alert Threshold                                 |
| ------------------------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------- |
| **First-Time User Experience** | Install → Open → Tutorial Start → Tutorial Complete → First Level Complete    | > 25% drop between any two steps                         |
| **Purchase Funnel**            | Browse Store → Select Item → View Price → Confirm Purchase → Payment Complete | > 40% drop between any two steps                         |
| **Ad Engagement**              | Ad Available → Ad Loaded → Ad Displayed → Ad Completed → Rewarded Claimed     | > 20% drop between any two steps                         |
| **Level Progression**          | Level N Start → Level N Complete → Level N+1 Start → Level N+1 Complete       | Increasing drop-off per level indicates difficulty spike |

### 5.2 Cohort Analysis

| Cohort Dimension         | Purpose                                                            |
| ------------------------ | ------------------------------------------------------------------ |
| **Acquisition source**   | Organic vs. paid vs. cross-promotion — compare LTV                 |
| **Geography**            | Different markets have different retention/monetization patterns   |
| **Device tier**          | High-end vs. mid-range vs. low-end — performance impacts retention |
| **Acquisition date**     | Track whether retention improves with game updates                 |
| **Acquisition campaign** | Which UA campaigns bring highest-LTV players                       |

---

## 6. A/B Testing Framework

### 6.1 What to A/B Test in Games

| Category         | Examples                                                              |
| ---------------- | --------------------------------------------------------------------- |
| **Onboarding**   | Tutorial length, tutorial style (interactive vs. video), skip option  |
| **Monetization** | Paywall timing, price points, bundle composition, discount percentage |
| **Difficulty**   | Level difficulty, enemy health, reward amounts                        |
| **Ad placement** | Ad frequency, placement timing, rewarded vs. interstitial ratio       |
| **UI/UX**        | Button color/placement, screen layout, animation speed                |
| **Economy**      | Currency earn rates, item prices, daily reward amounts                |

### 6.2 A/B Test Design

```
Test: "Does showing a discount popup on Day 3 increase IAP conversion?"

Control Group (50%): No popup
Treatment Group (50%): Discount popup on Day 3

Metrics to track:
  - Primary: IAP conversion rate (Day 3–7)
  - Guardrail: D7 retention (ensure popup doesn't hurt retention)
  - Secondary: ARPDAU, revenue per payer

Statistical power: 80%
Minimum detectable effect: 10% relative improvement
Duration: 14 days (minimum)
```

---

## 7. External Resources

| Resource                                          | Link                                                                                                | Focus                           |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------- |
| GameAnalytics Academy                             | https://gameanalytics.com/academy/                                                                  | Game analytics best practices   |
| "Game Retention Strategies: Metrics & Benchmarks" | https://www.juegostudio.com/blog/how-to-increase-user-retention-and-increase-your-games-lifetime    | Retention deep dive             |
| "Player Retention Metrics"                        | https://countly.com/blog/player-retention-analytics-the-metrics-that-predict-long-term-game-success | Beyond D1/D7/D30                |
| "What Are Game Metrics"                           | https://kevurugames.com/blog/what-are-game-metrics-and-why-do-they-matter/                          | Game metrics overview           |
| Firebase for Games                                | https://firebase.google.com/docs/games                                                              | Firebase game integration guide |
| Unity Remote Config                               | https://unity.com/solutions/remote-config                                                           | A/B testing and remote config   |

---

_End of Game Analytics & KPIs_
