# Incident Response — Analytical Sign-Off

**Domain:** Data Analytics  
**Skill Type:** Postmortem Analysis  
**Authority:** VP Data / Head of Analytics

---

## Overview

This skill covers the analytical sign-off on postmortems and incident response. VP Data owns the analytical sections of any postmortem where instrumentation health, metric accuracy, or error budget analysis was a contributing factor.

## Core Competencies

1. **Postmortem Analysis** — Root cause analysis from data perspective
2. **Instrumentation Health Review** — Identifying telemetry gaps or failures
3. **Error Budget Analysis** — Computing burn rates and SLO violations
4. **Corrective Action Planning** — Defining data/instrumentation improvements

## Incident Response Process

### Phase 1: Incident Detection

- Monitor error budget burn rate
- Alert on SLO violations
- Identify metric anomalies

### Phase 2: Incident Response

- Provide real-time data to incident commander
- Analyze user impact metrics
- Track recovery progress

### Phase 3: Postmortem

- **Analytical Sections:** VP Data owns data-related sections
- **Root Cause:** Identify instrumentation or metric issues
- **Impact Analysis:** Quantify user impact
- **Corrective Actions:** Define data/instrumentation improvements

## Postmortem Template — Analytical Sections

### §1: Telemetry Summary

- What telemetry was available?
- What telemetry was missing?
- Were metrics accurate?

### §2: Impact Quantification

- How many users affected?
- What was the business impact?
- How long did the incident last?

### §3: Error Budget Impact

- How much error budget was consumed?
- What is the remaining error budget?
- Are we at risk of exceeding budget?

### §4: Data/Instrumentation Gaps

- What instrumentation would have helped?
- What metrics should we add?
- What dashboards should we build?

### §5: Corrective Actions (Data)

- Instrumentation improvements
- Dashboard enhancements
- Alerting refinements

## Error Budget Analysis

### Weekly Burn Rate Computation

```
Burn Rate = (Actual Downtime) / (Error Budget Allowance)
```

### SLO Violation Tracking

- Track all SLO violations
- Compute cumulative error budget consumption
- Alert when approaching budget exhaustion

### QBR Readouts

- Co-lead QBRs with VP Platform
- Present error budget status
- Recommend SLO adjustments if needed

## Related Skills

- `experimentation-spec.md` — Experimentation specification
- `metric-definition-lock.md` — Metric definition governance

## Related Domains

- `engineering` — Software architecture and reliability
- `product-management` — Product quality and user impact
- `cyberspace-security` — Security incident response
