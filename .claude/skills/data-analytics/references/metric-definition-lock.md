# Metric Definition Lock

**Domain:** Data Analytics  
**Skill Type:** Metric Governance  
**Authority:** VP Data / Head of Analytics

---

## Overview

This skill covers the metric definition lock process — a parallel gate at Stage 3 that pins PRD metric definitions alongside technology decisions (ADRs/TSD). Once locked, metric definitions can only be revised through the same supersession discipline as ADRs.

## Core Competencies

1. **Metric Definition Review** — Reviewing PRD metrics for clarity, measurability, and alignment
2. **Stage 3 Lock Process** — Parallel gate alongside technology lock
3. **Metric Supersession** — Handling metric definition changes post-lock
4. **Cross-Functional Alignment** — Ensuring PM, Engineering, and Data alignment on metrics

## Metric Definition Lock Process

### Stage 1: Initial Definition

- PM defines success metrics in PRD
- VP Data reviews for statistical validity
- Experimentation Spec defines measurement methodology

### Stage 3: Lock Gate

- **Parallel to Technology Lock:** Metric definitions lock at Stage 3 approval
- **Lock Scope:** Primary metrics, guardrail metrics, instrumentation plan
- **Sign-off:** VP Data + CPO/VP Product

### Post-Lock Changes

- **Supersession Required:** New metric definition document
- **Full Re-Entry:** Return to Stage 3 for approval
- **Never Edit:** Do not modify locked metric definitions

## Metric Definition Standards

### Required Elements

1. **Metric Name:** Clear, unambiguous name
2. **Definition:** Precise calculation formula
3. **Measurement:** How and when it's measured
4. **Target:** Success threshold
5. **Guardrails:** Acceptable bounds

### Example Metric Definition

```
Metric: Day 7 Retention Rate
Definition: (Users active on Day 7) / (Users who signed up 7 days ago)
Measurement: Daily batch job at 00:00 UTC
Target: ≥ 20%
Guardrail: Must not drop below 18%
```

## Escalation Path

If metric definition changes are needed post-lock:

1. PM proposes new metric definition document
2. VP Data reviews statistical validity
3. CPO approves business rationale
4. Return to Stage 3 for full re-approval
5. Update Experimentation Spec accordingly

## Related Skills

- `experimentation-spec.md` — Experimentation specification template
- `incident-response.md` — Analytical postmortem sign-off

## Related Domains

- `product-management` — PRD authorship and product strategy
- `engineering` — Instrumentation and telemetry implementation
