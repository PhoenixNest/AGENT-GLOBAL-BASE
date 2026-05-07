# Experimentation Specification

**Domain:** Data Analytics  
**Skill Type:** Experimentation Governance  
**Authority:** VP Data / Head of Analytics

---

## Overview

This skill covers the Experimentation Specification template and statistical design for A/B testing and experimentation governance. The Experimentation Spec is a paired artifact with the PRD at Stage 1 and requires VP Data sign-off.

## Core Competencies

1. **Statistical Design** — Sequential testing, multi-arm bandit allocation, sample size calculation
2. **Experimentation Governance** — Sign-off authority on every primary-metric PRD
3. **Metric Definition** — Defining success metrics, guardrails, and decision rules
4. **Minimum Detectable Effect (MDE)** — Setting appropriate MDE thresholds

## Experimentation Spec Template

The Experimentation Spec template is located at:

```
company/pipeline/_base/experimentation-spec-template.md
```

## Key Sections

### §1: Hypothesis Statement

- Null hypothesis (H0)
- Alternative hypothesis (H1)
- Expected effect size

### §2: Primary Metric

- Metric definition
- Measurement methodology
- Success criteria

### §3: Statistical Design

- Sample size calculation
- Significance level (α)
- Statistical power (1-β)
- Minimum detectable effect (MDE)

### §4: Guardrail Metrics

- Metrics that must not regress
- Acceptable degradation thresholds

### §5: Decision Rule

- Launch criteria
- Kill criteria
- Iteration criteria

## Review Process

1. **Submission:** PM submits Experimentation Spec with PRD at Stage 1
2. **Review:** VP Data reviews within 48-hour SLA
3. **Sign-off:** VP Data approves or requests revisions
4. **Lock:** Spec is locked at Stage 3 alongside metric definitions

## Related Skills

- `metric-definition-lock.md` — Metric definition governance
- `incident-response.md` — Analytical postmortem sign-off

## Related Domains

- `product-management` — PRD authorship and product metrics
- `engineering` — Instrumentation and telemetry implementation
