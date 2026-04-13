---
name: ltv-forecasting
description: Player lifetime value forecasting using parametric models, ML approaches, and hybrid methods for mobile game monetization prediction.
---

# LTV Forecasting

## Overview

This skill covers the design, training, and validation of player LTV (Lifetime Value) forecasting models, enabling data-driven UA budget allocation and monetization strategy.

## Tools & Methods

| Tool/Method           | Purpose                                    |
| --------------------- | ------------------------------------------ |
| Python (scikit-learn) | Random Forest, Gradient Boosting ML models |
| Python (statsmodels)  | Parametric models (Pareto/NBD, BG/NBD)     |
| SQL                   | Feature extraction from player data        |
| MLflow                | Model versioning and experiment tracking   |

## Core Methodologies

### 1. Hybrid Parametric + ML Approach

**Stage 1 — Parametric (BG/NBD Model):**

- Models purchase frequency and dropout probability
- Inputs: recency, frequency, monetary value (RFM)
- Output: expected transaction count and probability active

**Stage 2 — ML Enhancement (Gradient Boosting):**

- Adds behavioral features: session length, level progression, social interactions
- Trained on actual LTV from mature cohorts
- Output: calibrated LTV prediction with confidence intervals

### 2. Model Validation

| Validation Method  | Target                               |
| ------------------ | ------------------------------------ |
| Backtest accuracy  | ≥ 90% (MAPE ≤ 10%)                   |
| Holdout cohort R²  | ≥ 0.85                               |
| Calibration curve  | Predicted vs. actual within ±5%      |
| Feature importance | Top 5 features must be interpretable |

### 3. LTV Segmentation

| Player Type   | D90 LTV Range | UA Bid Strategy               |
| ------------- | ------------- | ----------------------------- |
| F2P Non-payer | $0–$0.50      | Organic focus, low CPI        |
| Minnow        | $0.50–$5.00   | Moderate bid, broad targeting |
| Dolphin       | $5.00–$50.00  | Aggressive bid, lookalike     |
| Whale         | $50.00+       | Premium targeting, high ROAS  |
