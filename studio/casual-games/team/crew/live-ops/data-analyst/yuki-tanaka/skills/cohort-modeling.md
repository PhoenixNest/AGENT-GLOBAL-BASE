---
name: cohort-modeling
description: Cohort decay modeling, retention curve analysis, and player segmentation for mobile game analytics.
version: "1.0.0"
---

# Cohort Modeling

## Overview

This skill covers the design, implementation, and interpretation of cohort analysis models for mobile game player behavior, including retention curve fitting, decay modeling, and player segmentation.

## Tools & Methods

| Tool/Method            | Purpose                                         |
| ---------------------- | ----------------------------------------------- |
| Python (statsmodels)   | Weibull distribution fitting, survival analysis |
| Python (scikit-learn)  | K-means clustering for player segmentation      |
| SQL (window functions) | Cohort data extraction and aggregation          |
| Tableau                | Cohort retention heatmap visualization          |

## Core Methodologies

### 1. Cohort Decay Modeling

**Weibull Distribution Fit:**

- Survival function: S(t) = exp(-(t/λ)^k)
- λ (scale): characteristic lifetime of the cohort
- k (shape): decay pattern (k < 1: rapid early churn; k > 1: gradual decline)

**Model Validation:**

- Kolmogorov-Smirnov test for goodness of fit
- Backtest against held-out cohorts
- Target: R² ≥ 0.90 on D1–D30 retention data

### 2. Player Segmentation

| Segment | Characteristics                    | % of Players | Key Metric to Track   |
| ------- | ---------------------------------- | ------------ | --------------------- |
| Casual  | Low session frequency, low spend   | 60–70%       | D1/D7 retention       |
| Engaged | Medium frequency, occasional spend | 20–30%       | D30 retention, ARPPU  |
| Whale   | High frequency, high spend         | 1–5%         | LTV, churn risk score |

### 3. Retention Curve Analysis

- **D1 Retention:** Measures first-impression quality (onboarding, tutorial, early gameplay)
- **D7 Retention:** Measures early engagement loop effectiveness
- **D30 Retention:** Measures long-term content depth and meta-game engagement

**Diagnostic Approach:** If D1 is strong but D7 drops sharply → content/engagement loop issue. If D7 is strong but D30 drops → meta-game/content depth issue.
