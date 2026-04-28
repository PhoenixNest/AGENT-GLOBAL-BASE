# Experimentation Spec — Stage 1 Paired Artifact Template

| Field             | Value                                                                                |
| ----------------- | ------------------------------------------------------------------------------------ |
| **Document Type** | Stage 1 paired artifact (alongside PRD + SRD)                                        |
| **Scope**         | All product pipelines (mobile, web, backend, full-stack); applied per metric in PRD  |
| **Owner**         | CPO (DRI) + Head of Data / VP Data (analytical sign-off)                             |
| **Effective**     | First Stage 1 entry post-publication                                                 |
| **Cross-Refs**    | Base pipeline Stage 1 · PRD authorship skill · Project dashboard cycle-time tracking |

---

## 1. Purpose

Every PRD already names baseline + target metrics and an instrumentation plan. The PRD does **not** specify how the post-launch measurement is run as an experiment. Without that specification, staged rollout (10% → 50% → 100%) is performed but not interpreted: there is no statistical guardrail, no minimum detectable effect, no sample-size calculation, no defined holdout, and no decision rule for early stop.

The Experimentation Spec is the missing instrument. Each PRD-defined metric that is being moved (the "primary metric") gets one Experimentation Spec. The spec is filed at Stage 1 alongside the PRD and SRD; it travels with them through all subsequent stages so that Stage 5 implementation can wire the measurement, Stage 7 testing can verify the measurement fires, and Stage 11 live ops can call the experiment per its decision rule.

---

## 2. When Required

| Condition                                                                                   | Spec required?                               |
| :------------------------------------------------------------------------------------------ | :------------------------------------------- |
| PRD names a primary metric with an explicit target (e.g., "increase D7 retention by ≥ 2pp") | **Yes**                                      |
| PRD names a guardrail metric (must not regress beyond a threshold)                          | **Yes**                                      |
| PRD launches a UI change without metric movement claims (pure design refresh)               | Recommended, not required                    |
| Backend internal change with no user-visible impact                                         | Not required                                 |
| Hotfix or P0 / P1 defect remediation                                                        | Not required (operational, not experimental) |
| Studio game release that uses retention kill criteria                                       | **Yes** (per studio §2.1)                    |

If the PRD has a primary metric and no Experimentation Spec, the Stage 1 gate **does not pass**. This is a hard gate.

---

## 3. Spec Template

The DRI fills out one instance of the template per primary or guardrail metric. The instances are named `<metric-id>-experimentation-spec.md` and live alongside the PRD.

```markdown
# Experimentation Spec — <metric name>

| Field                 | Value                                         |
| :-------------------- | :-------------------------------------------- |
| Spec ID               | EXP-YYYY-MM-DD-<short slug>                   |
| Linked PRD            | <relative path to PRD>                        |
| Primary or guardrail? | Primary / Guardrail                           |
| Owner (DRI)           | <PM or VP>                                    |
| Analytical sign-off   | Head of Data (must sign before Stage 1 close) |
| Surface               | mobile / web / backend / full-stack / studio  |
| Status                | Draft / Stage 1 signed / Live / Concluded     |

## 1. Hypothesis

One-sentence statement of the user behavior change predicted by the feature, in the form:
"For <user segment>, shipping <feature> will move <metric> from <baseline> to <target> within <window>, because <causal mechanism>."

## 2. Metric definition

| Field                 | Value                                                     |
| :-------------------- | :-------------------------------------------------------- |
| Metric name           | <PRD metric ID, e.g. METRIC-D7-RETENTION>                 |
| Definition            | Exact computation (numerator / denominator / time window) |
| Event(s) instrumented | <event names from PRD instrumentation plan>               |
| Aggregation           | Per-user / per-session / per-cohort                       |
| Baseline (current)    | <value> ± <std error> measured over <window>              |
| Target                | <value or %-pp lift>                                      |
| Guardrail bounds      | <lower bound that, if breached, halts the rollout>        |

## 3. Statistical design

| Field                           | Value                                                                   |
| :------------------------------ | :---------------------------------------------------------------------- |
| Test type                       | A/B (two-arm) / multi-arm / interleaved / pre-post / quasi-experimental |
| Unit of randomization           | User / session / device / studio cohort                                 |
| Allocation                      | <e.g. 50/50, or 10/10/80>                                               |
| Minimum detectable effect (MDE) | <absolute or % delta the design can detect>                             |
| Power (1 − β)                   | 0.80 (default) or higher with justification                             |
| Significance (α)                | 0.05 two-sided (default) or stricter with justification                 |
| Multiple-comparison correction  | Bonferroni / BH-FDR / none — choose explicitly                          |
| Required sample size            | <per arm; computed from MDE, power, α, baseline variance>               |
| Estimated time to power         | <days at expected DAU>                                                  |

## 4. Holdout and segmentation

| Field                       | Value                                                                    |
| :-------------------------- | :----------------------------------------------------------------------- |
| Long-term holdout           | <e.g. 5% never-treated for 90 days, or "none">                           |
| Pre-registered segments     | <list segments analyzed up-front; ad-hoc slicing is reported separately> |
| Forbidden post-hoc segments | <segments that will not be analyzed; prevents p-hacking>                 |

## 5. Decision rule

The decision rule is set BEFORE launch and is binding.

| Outcome                                                                     | Action                                      |
| :-------------------------------------------------------------------------- | :------------------------------------------ |
| Primary metric ≥ target with p < α AND no guardrail breach                  | Ship 100%                                   |
| Primary metric directionally positive but p ≥ α AND no guardrail breach     | Extend test (specify duration cap up-front) |
| Primary metric flat or negative AND no guardrail breach                     | Roll back; file learning postmortem         |
| Any guardrail metric breaches its lower bound regardless of primary outcome | Roll back immediately; Sev2 minimum         |

## 6. Early-stop rules

| Condition                                                  | Action                                    |
| :--------------------------------------------------------- | :---------------------------------------- |
| Guardrail breach observed at any sample size               | Stop; roll back; Sev2 minimum             |
| Primary metric crosses pre-registered futility boundary    | Stop early for futility; conclude as flat |
| Primary metric crosses pre-registered superiority boundary | Stop early for win; ship 100%             |
| Operational issue (logging gap > 5%, data pipeline broken) | Pause; do not consume the test budget     |

Sequential testing requires α-spending plan; default is O'Brien–Fleming or Pocock; alternative requires Head of Data sign-off.

## 7. Operational details

| Field                      | Value                                                                            |
| :------------------------- | :------------------------------------------------------------------------------- |
| Feature flag name          | <flag id>                                                                        |
| Allocation service         | <internal exposure service identifier>                                           |
| Telemetry pipeline         | <log path / table / dashboard URL>                                               |
| Pre-launch QA (smoke test) | Required: assignment is balanced; events fire on both arms; logging is complete. |
| Pre-launch dashboard URL   | <URL where Head of Data and DRI can monitor live>                                |
| Conclusion review meeting  | Mandatory; date set at launch; outputs the final write-up.                       |

## 8. Conclusion write-up (filled at end-of-test)

| Field                | Value                                        |
| :------------------- | :------------------------------------------- |
| Final sample size    | <per arm>                                    |
| Observed effect size | <with confidence interval>                   |
| p-value              | <reported; corrected if multi-test>          |
| Guardrail outcomes   | <each named guardrail with observed value>   |
| Decision applied     | Per §5 / §6 rule cited                       |
| Action taken         | Shipped / Rolled back / Extended             |
| Lessons              | What was learned about the user / the system |
```

---

## 4. Statistical Defaults and Why

The defaults below are non-negotiable unless the analytical sign-off (Head of Data) explicitly approves the deviation in writing inside §3 of the spec.

| Default                        | Value                  | Why it is the default                                                                                         |
| :----------------------------- | :--------------------- | :------------------------------------------------------------------------------------------------------------ |
| Significance (α)               | 0.05 two-sided         | Industry standard; matches academic and regulatory norms.                                                     |
| Power (1 − β)                  | 0.80                   | Below this, the experiment is more likely than not to miss a real effect of MDE size.                         |
| Multiple-comparison correction | BH-FDR for ≥ 3 metrics | Bonferroni is overly conservative when many metrics are correlated; BH controls false discovery rate.         |
| Allocation                     | 50/50                  | Maximum statistical power for a fixed sample size; deviate only when blast-radius of treatment requires <50%. |
| Minimum test duration          | 7 days                 | Captures full weekly seasonality; one-day tests are not interpretable for retention or engagement metrics.    |
| Pre-registration of segments   | Required               | Post-hoc slicing inflates false positive rate; pre-registration is the only honest defense.                   |
| Sequential testing             | Permitted with α-spend | Without an α-spending plan, peeking inflates Type I error to ~25%; OBF / Pocock / mSPRT are accepted.         |

---

## 5. Guardrail Library

A guardrail metric is a metric you do **not** want to move adversely, regardless of the treatment effect on the primary. Every spec must declare at least one guardrail from the library below, plus any feature-specific guardrail.

| Surface    | Standing guardrail (always required)          | Lower bound (default)                            |
| :--------- | :-------------------------------------------- | :----------------------------------------------- |
| Mobile     | Crash-free sessions rate                      | ≥ 99.5% (no regression > 0.1pp from baseline)    |
| Mobile     | App startup time (P95)                        | ≤ baseline + 100 ms                              |
| Web        | Largest Contentful Paint (P75)                | ≤ baseline + 100 ms                              |
| Web        | JS error rate                                 | ≤ baseline × 1.1                                 |
| Backend    | API P99 latency                               | ≤ baseline × 1.05                                |
| Backend    | API error rate (5xx)                          | ≤ baseline + 0.05pp                              |
| Full-stack | Cross-surface session continuity success rate | ≥ baseline                                       |
| Studio     | D1 retention; D7 retention                    | Per studio retention thresholds (see studio doc) |
| Universal  | Daily active users (DAU)                      | ≥ baseline (no regression)                       |
| Universal  | Net Promoter Score (if surveyed)              | ≥ baseline (no regression)                       |

---

## 6. Lifecycle Hooks

| Pipeline stage                | Spec activity                                                                                                             |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| Stage 1                       | Spec authored; Head of Data signs §3 + §5; spec filed alongside PRD/SRD as paired artifact.                               |
| Stage 3 (UML/ADRs)            | Spec referenced when ADR governs telemetry / feature-flag service architecture.                                           |
| Stage 4 (Implementation Plan) | Tasks created for instrumentation, allocation service wiring, dashboard creation. Pre-launch smoke test added to Stage 5. |
| Stage 5 (Development)         | Instrumentation implemented; smoke test passes (assignment balance + event completeness).                                 |
| Stage 7 (Automated Testing)   | Telemetry-firing test cases verify the spec's events fire correctly under both arms.                                      |
| Stage 9.5 (Dogfood)           | Spec instrumentation runs in dogfood; reading sanity-checked for noise level + variance.                                  |
| Stage 10 (Release)            | Spec goes live with the feature flag; pre-registered dashboard handed to DRI + Head of Data.                              |
| Stage 11 (Live Ops)           | Spec runs to power; conclusion meeting at end-of-test; §8 filled; decision per §5 / §6 executed; spec status → Concluded. |

---

## 7. Independent Challenge Requirement

If a spec has **≥ 5 declared metrics across primary + guardrails** OR **the test allocation is asymmetric (one arm < 25%)** OR **the feature is irreversible (data migration, schema change, currency change)**, the spec must pass an Independent Challenge round per `_base/independent-challenge-template.md` before Stage 1 close.

The challenger applies the five attack vectors specifically to:

- **V-1 Completeness:** What guardrails are missing? Is there a metric the spec authors didn't see?
- **V-2 Sufficiency:** Is the MDE actually achievable in the planned test duration? Is the holdout adequate?
- **V-3 Trim-to-Pass:** Has any guardrail been silently dropped relative to the standing guardrail library above?
- **V-4 Counter-evidence:** Cite at least one prior experiment in this domain that reached opposite conclusions.
- **V-5 Same-parties closure:** Confirm Head of Data signed-off independently of the DRI.

---

## 8. Owner Handoff

| Touch point                                     | Owner                           |
| :---------------------------------------------- | :------------------------------ |
| Spec authorship                                 | DRI (PM / VP)                   |
| Statistical design sign-off (§3, §4 deviations) | Head of Data / VP Data          |
| Pre-launch smoke test sign-off                  | Test Lead                       |
| Live monitoring                                 | DRI + Head of Data              |
| Decision execution per §5 / §6                  | DRI (informs CPO)               |
| Postmortem on rollback                          | DRI + relevant on-call engineer |
| Spec retirement (status → Concluded)            | DRI                             |

---

## 9. Document Version History

| Version | Date           | Author             | Changes                                                                                                                                                                                                                                                                 |
| :------ | :------------- | :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 21, 2026 | CPO + Head of Data | Initial template publication. Spec required for any PRD with a primary metric. Statistical defaults locked. Standing guardrail library by surface. Stage-1 paired-artifact rule entered into base pipeline. Independent Challenge required for high-blast-radius specs. |
