---
name: studio-live-ops-ab-test-design
description: A/B test design and statistical analysis for casual mobile games — experiment setup, power analysis, Bayesian inference, statistical diagnostics, and decision frameworks for game feature and economy changes. Owned by Yuki Tanaka (Data Analyst). Trigger: A/B test, experiment design, statistical test, hypothesis test, feature test, split test, power analysis, Bayesian.
version: "1.0.0"
---

# A/B Test Design

**Skill Owner:** Yuki Tanaka (Data Analyst)
**Applies To:** Feature Testing, Economy Testing, Retention Experiments, Live Ops Optimization (Stages 8–10)

## Tools & Frameworks

| Tool/Framework              | Version | Usage                                               |
| --------------------------- | ------- | --------------------------------------------------- |
| Python (statsmodels, scipy) | 3.11+   | Power analysis, frequentist hypothesis tests        |
| Python (pymc, arviz)        | Latest  | Bayesian A/B testing                                |
| Pandas / NumPy              | Latest  | Data wrangling and metric calculation               |
| Tableau                     | Latest  | Test result visualization and stakeholder reporting |
| SQL (BigQuery / Redshift)   | Latest  | Cohort extraction and metric computation            |

## Experiment Design Framework

### Step 1: Define the Hypothesis

A testable hypothesis must have:

- **Change:** What are we modifying? (e.g., "Reduce the cost of the first soft-currency upgrade from 500 to 300")
- **Mechanism:** Why should this change the metric? (e.g., "Lowering the barrier to the first meaningful spend will increase the fraction of players who experience the meta-game reward loop")
- **Primary metric:** The single metric we are trying to move (e.g., D7 retention)
- **Guard metrics:** Metrics that must not regress (e.g., ARPU, ARPPU)

### Step 2: Power Analysis

Before running any experiment, calculate the required sample size:

```python
from statsmodels.stats.power import NormalIndPower

analysis = NormalIndPower()
n = analysis.solve_power(
    effect_size=0.05,   # 5% relative lift on the primary metric
    alpha=0.05,         # Type I error rate (false positive)
    power=0.80,         # 1 - Type II error (chance of detecting a real effect)
    ratio=1.0           # Equal split (50/50)
)
```

**Studio standard for casual games:**

- Minimum detectable effect: 2pp absolute or 10% relative lift (whichever is smaller)
- Confidence level: 95% (α = 0.05)
- Power: 80% (β = 0.20)
- Minimum test duration: 7 days regardless of when significance is reached (novelty effect mitigation)

### Step 3: Randomization and Assignment

- Randomize at the **user level** (never session level — this introduces selection bias)
- Use stratified randomization if the player population has a known high-variance segment (e.g., payers vs. non-payers)
- Document the randomization seed and assignment logic for reproducibility

### Step 4: Analysis

**Frequentist approach (default for binary metrics):**

```python
from scipy import stats
chi2, p_value, dof, expected = stats.chi2_contingency(
    [[control_conversions, control_non_conversions],
     [treatment_conversions, treatment_non_conversions]]
)
```

**Bayesian approach (preferred for continuous metrics like ARPU):**

- Models posterior distribution of the effect; provides the probability that treatment is better than control
- Avoids the "peeking problem" — can be evaluated at any point without inflating Type I error
- Output: "There is a 94% probability that the treatment improves ARPU by 5–12%"

### Step 5: Decision Framework

| Outcome                                         | Action                                                                         |
| ----------------------------------------------- | ------------------------------------------------------------------------------ |
| Primary metric improves, guard metrics stable   | Ship to 100%                                                                   |
| Primary metric improves, guard metric regresses | Investigate trade-off; present to Aisha Nkemelu (Live Ops Lead) for decision   |
| No significant effect                           | Iterate on hypothesis or abandon the change                                    |
| Primary metric regresses                        | Stop the test immediately; revert control                                      |
| Inconclusive after 14 days                      | Either extend (if sample is still below power requirement) or call null result |

## Common Pitfalls and Diagnostics

| Pitfall                                   | Detection                                   | Resolution                                                        |
| ----------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------- |
| Peeking (stopping early when significant) | Multiple comparisons detected               | Enforce minimum 7-day duration regardless                         |
| Novelty effect                            | Metric improves D1–D3, then decays          | Analyze Day 4+ cohort separately                                  |
| Carryover effect                          | Previous test's effect bleeds into new test | Require 3-day washout period between tests on the same population |
| Sample ratio mismatch                     | Treatment group ≠ expected 50%              | Bug in assignment logic; invalidate the test                      |
| Metric instability                        | High variance in daily metric values        | Use 7-day rolling average as the primary metric                   |

## Measurable Quality Standards

| Standard                               | Target                    | Measurement Method              |
| -------------------------------------- | ------------------------- | ------------------------------- |
| Power analysis completed before launch | 100% of experiments       | Pre-test document in Confluence |
| Minimum test duration enforced         | 100%                      | Test start/end log              |
| Statistical methodology documentation  | 100% of published results | Analysis notebook               |
| False positive rate (Type I error)     | ≤5% (α = 0.05)            | Statistical test parameters     |
| Sample ratio match                     | Within 1% of target split | Daily SRM check                 |
