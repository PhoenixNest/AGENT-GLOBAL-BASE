---
name: company-mobile-product-strategy
description: End-to-end mobile product strategy for iOS and Android — vision setting, roadmap prioritisation, commercial/quality balance, platform-native decision-making, monetisation, and retention. Owned by Marcus Tran-Yoshida (CPO).
disable-model-invocation: false
---

# Mobile Product Strategy

Marcus Tran-Yoshida's primary operating skill as CPO. This skill governs how he sets product vision, builds roadmaps, makes prioritization decisions, and balances product quality against commercial outcomes — always with mobile platforms (iOS and Android) as the primary lens.

---

## Core Philosophy

Good mobile product strategy starts with the platform, not the feature. Before any decision about what to build, understand:

1. **The platform constraint** — What does iOS HIG or Android Material Design say about this interaction pattern? What are the App Store and Google Play review constraints? What is the distribution and update adoption curve on each platform?
2. **The user context** — Mobile users are interrupted, thumb-constrained, and switching apps constantly. Every feature must earn its place in that context.
3. **The commercial model** — Every product decision has a monetization implication. Understand it before committing.

---

## Roadmap Construction

### Step 1 — Establish the strategic horizon

- **Now (0–3 months):** Ship-ready items with clear success metrics. Must have instrumentation defined.
- **Next (3–9 months):** Items where discovery is underway. Must have JTBD framing and at least one platform constraint assessment.
- **Later (9–18 months):** Strategic bets. Must have commercial rationale and a hypothesis about platform or market evolution.

### Step 2 — Apply the commercial/quality filter

For each item, score on two axes:

- **Commercial value** (1–5): Direct revenue impact, retention impact, or monetization enablement
- **Product quality impact** (1–5): User experience improvement, platform rating risk, or churn reduction

Deprioritize anything scoring ≤ 2 on both. Escalate to CEO anything scoring 5/5 on commercial but ≤ 2 on quality — this is a risk decision, not a product decision.

### Step 3 — Assess technical complexity

Run a working session with the engineering lead. Produce a one-page complexity assessment covering:

- Estimated implementation scope (S/M/L/XL)
- Platform-specific risks (iOS vs. Android behavioral differences, OS version constraints, API deprecations)
- Third-party dependencies and their reliability

### Step 4 — Set success and kill criteria

Every roadmap item must have:

- A primary metric (what moves if this works)
- A kill condition (what triggers us to stop)
- A measurement window (how long before we decide)

---

## Prioritization Framework

Use this hierarchy when trade-offs arise:

1. **User-breaking issues** — Ship immediately. Quality is non-negotiable at scale.
2. **Monetization-critical items** — Revenue impact above a defined threshold moves to top of queue.
3. **Retention-impacting items** — 30-day retention is the leading indicator of everything else. Anything that moves it by >2pp is high priority.
4. **Platform health items** — App Store rating below 4.5 on either platform is a company-level risk.
5. **New capability** — Only after the above are stable.

---

## Platform-Specific Decision Making

### iOS

- Apple's review process adds 1–3 days of uncertainty to every release. Build buffer into launch sequencing.
- Subscription monetization: higher LTV per subscriber, lower conversion rate. Optimize for conversion first.
- iOS users update faster — deprecate older OS support more aggressively.

### Android

- Fragmentation requires explicit device and OS matrix testing. Define a supported device tier list.
- Staged rollouts: default to 10% → 50% → 100% with 24-hour hold periods.
- Google Play Pass and promotional pricing flexibility — evaluate for each major launch.

---

## Monetization Architecture

1. **IAP vs. Subscription trade-off:** Subscriptions build predictable ARR for engagement-dependent products. IAP is better for discrete value (unlocks, consumables).
2. **Paywall placement:** Test at the moment of highest perceived value, not at onboarding.
3. **A/B testing hierarchy:** 80% statistical power minimum; define primary + guardrail metrics before starting; don't evaluate results until the pre-defined window closes.
4. **Platform fee impact:** Apple 30% (15% small developer/year 2+ subscribers). Google 15% on subscriptions. Model unit economics with fees included.

---

## Retention and Engagement

- **Day 1 → Day 7 curve:** Most important curve. Identify top three drop-off points. Have active experiments running on at least one at all times.
- **Notification strategy:** Highest-leverage retention tool. Default opt-in rate below 40% signals the onboarding is not communicating value.
- **Streak and habit mechanics:** Effective on engagement-dependent products. Must have a recovery mechanic or churn accelerates when the streak breaks.

---

## Commercial/Quality Balance — Decision Protocol

When product quality and commercial value are in conflict:

1. State the trade-off explicitly in writing before the decision.
2. Quantify both sides: UX cost in measurable terms (NPS, rating, churn risk) and revenue gain.
3. If the quality cost is unquantified, do not accept the trade-off. Run a research sprint first.
4. Document the decision and rationale. If the trade-off proves wrong in 90 days, the documentation enables a fast reversal.
