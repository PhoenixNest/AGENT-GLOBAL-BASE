---
name: paid-ua-management
description: Multi-platform paid user acquisition management for mobile games, covering Meta Ads, Google UAC, and Apple Search Ads.
version: "1.0.0"
---

# Paid UA Management

## Overview

This skill covers the end-to-end management of paid user acquisition campaigns across the three primary mobile game advertising platforms: Meta Ads, Google UAC (Universal App Campaigns), and Apple Search Ads.

## Tools & Platforms

| Platform           | Purpose                                       | Key Features Used                  |
| ------------------ | --------------------------------------------- | ---------------------------------- |
| Meta Ads Manager   | Prospecting, retargeting, lookalike audiences | AEO, VO, CBO, dynamic creatives    |
| Google UAC         | Intent-driven app install campaigns           | tCPA, tROAS bidding, asset groups  |
| Apple Search Ads   | Branded + competitor keyword bidding          | Search Match, custom product pages |
| AppsFlyer / Adjust | MMP attribution, SKAdNetwork configuration    | Cohort reporting, ROAS tracking    |

## Core Methodologies

### 1. Platform Allocation Strategy

| Platform      | Best For                  | Budget Allocation | CPI Range (Casual) |
| ------------- | ------------------------- | ----------------- | ------------------ |
| Meta Ads      | Prospecting, scale        | 45%               | $1.50–$2.50        |
| Google UAC    | Intent-driven, automation | 35%               | $1.80–$3.00        |
| Apple SA      | Branded, high-intent      | 15%               | $1.00–$2.00        |
| ASO (organic) | Keyword optimization      | 5% (effort)       | $0 (organic)       |

### 2. Bid Strategy Optimization

- **Start with tCPA** for new campaigns; transition to tROAS once 50+ conversions accumulated
- **Audience layering:** 1% lookalike > 2% lookalike > interest-based > broad
- **Dayparting:** Adjust bids by time of day based on historical conversion data
- **Geo-splitting:** Separate campaigns by tier-1, tier-2, tier-3 markets

### 3. Creative Performance Management

| Creative Type  | Platform Best Fit | Expected CPI Impact |
| -------------- | ----------------- | ------------------- |
| Gameplay video | Meta, Google      | Baseline            |
| UGC-style      | Meta (Reels)      | -15% to -25% CPI    |
| Playable ad    | Meta, Google      | -10% to -20% CPI    |
| Static image   | ASA               | Baseline            |

## Quality Standards

- Weekly campaign performance review (every Monday)
- Creative refresh every 2 weeks (new concepts + variants)
- CPI tracked daily; alert triggers if CPI exceeds target by > 20% for 3 consecutive days
- ROAS reported weekly (D1, D3, D7, D30)
- Attribution data reconciled monthly (MMP vs. platform vs. internal analytics)
