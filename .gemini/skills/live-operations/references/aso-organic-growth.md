---
name: studio-live-ops-aso-organic-growth
description: App Store Optimization (ASO) and organic user acquisition for casual mobile games — keyword research, store listing optimization, conversion rate optimization, and rating/review strategies for Apple App Store and Google Play. Owned by Rafael Santos (UA Specialist). Trigger: ASO, App Store Optimization, organic growth, keyword ranking, store listing, Google Play, App Store, ratings, reviews, conversion rate.
version: "1.0.0"
---

# ASO & Organic Growth

**Skill Owner:** Rafael Santos (UA Specialist)
**Applies To:** App Store and Google Play Optimization, Stage 8 (Soft Launch) through Stage 10 (Live Ops)

## Tools & Frameworks

| Tool                | Usage                                                            |
| ------------------- | ---------------------------------------------------------------- |
| AppFollow           | Keyword ranking tracking, competitor analysis, review management |
| Sensor Tower        | Keyword research, category ranking, download estimates           |
| AppTweak            | A/B test tracking, screenshot performance analysis               |
| Google Play Console | Direct A/B testing for store listings (Android)                  |
| App Store Connect   | Store listing management, sales and trends (iOS)                 |
| MobileAction        | Competitor keyword gap analysis                                  |

## ASO Pillars

### 1. Keyword Strategy

**Research process:**

1. Seed list: 20–30 keywords from the game's core mechanic, genre, and comparable titles
2. Expand using Sensor Tower's keyword suggestions and competitor keyword lists
3. Prioritize by **opportunity score:** high search volume + low competitor ranking difficulty + semantic relevance to the game
4. Final keyword list: 10–15 primary keywords (title/subtitle), 100 secondary keywords (keyword field — iOS only)

**iOS keyword field (100 characters):**

- Comma-separated, no spaces after commas (saves characters)
- Do not repeat words already in the title or subtitle
- Localize the keyword field for every major market (EN, ZH-TW, JA, KO, PT-BR, FR, DE)

**Google Play:**

- Keywords must appear naturally in the short description (80 characters) and full description (4,000 characters)
- The Play algorithm reads full description text — do not keyword-stuff; write naturally with 2–3 mentions of primary keywords

### 2. Store Listing Conversion Rate Optimization (CVR)

**A/B testing (Google Play Console):**

- Test one variable at a time: icon, feature graphic, screenshot 1 (the most impactful), or short description
- Run each test for a minimum of 7 days and 1,000 impressions before reading results
- Winning variant must show ≥5% relative lift in install CVR at ≥90% confidence before shipping

**Screenshot best practices:**

- Screenshot 1: show the core gameplay loop — the hook must be visible within 3 seconds without reading any text
- Screenshot text overlays: max 5 words per screenshot; use the platform's recommended font size
- No UI chrome in screenshots for iOS — App Store guidelines prohibit device frames unless using Apple's official mockup templates

**Icon design:**

- Highest-impact creative decision on CVR; coordinate with Renaud Leclercq (Art Director) and Elena Morozova (UI Visual Artist)
- Test 3–5 icon concepts before committing to the global launch icon
- Icons with a character face, strong contrast, and minimal detail outperform cluttered compositions in casual genre

### 3. Ratings and Review Strategy

**Ratings solicitation timing:**

- Trigger the native iOS/Android ratings prompt after a **positive emotional moment** — immediately after a level win, achievement unlock, or streak milestone
- Never prompt after a failure or when the player is showing signs of frustration (repeated restarts)
- iOS: maximum 3 solicitations per 365 days per device (SKStoreReviewRequest API enforces this)
- Android: Google Play In-App Review API has similar limits; honor them

**Review management:**

- Rafael monitors AppFollow daily during soft launch and first 30 days post-global launch
- Respond to every 1-star and 2-star review within 48 hours (empathic, non-defensive response; direct to support if bug-related)
- Positive 4/5-star reviews receive a brief thank-you response monthly (batched)

**Rating recovery playbook:**

- If average rating drops below 4.0: audit the most recent 1-star reviews for a pattern → if a specific bug is cited, P1 hot-fix with App Store expedited review → post an update response to all affected reviews

## Organic Growth Measurement

| Metric                             | Target                         | Measurement Tool                          |
| ---------------------------------- | ------------------------------ | ----------------------------------------- |
| Keyword ranking (primary keywords) | Top 10 for 3+ primary keywords | Sensor Tower / AppFollow                  |
| Store listing CVR                  | ≥30% (casual game benchmark)   | App Store Connect / Play Console          |
| Average app rating                 | ≥4.3 stars (both stores)       | AppFollow                                 |
| Organic install share              | ≥25% of total installs         | Attribution platform (Adjust / AppsFlyer) |
| Review response rate               | 100% of 1–2 star reviews       | AppFollow                                 |

## Measurable Quality Standards

| Standard                              | Target                                | Measurement Method                |
| ------------------------------------- | ------------------------------------- | --------------------------------- |
| ASO audit completed pre-soft launch   | Yes                                   | Confluence checklist              |
| Store listing A/B test conducted      | ≥1 test per element pre-global launch | Google Play Console records       |
| Keyword set localized                 | All primary markets                   | AppFollow locale tracking         |
| Rating solicitation timing compliance | 100% (only after positive moments)    | Implementation review with Dmitri |
