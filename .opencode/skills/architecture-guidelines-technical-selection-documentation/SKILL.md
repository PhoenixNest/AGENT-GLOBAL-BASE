---
name: architecture-guidelines-technical-selection-documentation
description: 'Architecture skill: Technical Selection Documentation'
---

# Technical Selection Documentation Skill

## Purpose

Produce clear, actionable technical documentation that enables executive decision-making while maintaining engineering rigor.

## When to Use

- Leadership requests technology recommendation
- Comparing multiple technology options
- Documenting significant architecture decisions
- Version upgrade analysis (e.g., React Native 0.72 vs 0.74)
- Vendor selection process

## Document Types

### 1. Technology Selection Document

**Structure:**

- **Executive Summary** (3-4 sentences): Decision, rationale, cost, timeline
- **Options Evaluated**: Table comparing 2-4 alternatives
- **Recommendation**: Which option and why
- **Total Cost of Ownership**: 3-year projection
- **Implementation Plan**: Phases, milestones, owners
- **Risk Assessment**: What could go wrong, mitigation strategies
- **Success Criteria**: Measurable outcomes

**Length:** 800-1200 words
**Audience:** C-suite, VP-level

### 2. Version Analysis Report

**Structure:**

- **Current State**: What version we're on, why
- **Target Version**: What we're considering
- **Breaking Changes**: What breaks, migration effort
- **New Capabilities**: What we gain
- **Risk Assessment**: Stability, community support, deprecation timeline
- **Recommendation**: Upgrade now / wait / skip
- **Migration Plan**: If upgrading, how and when

**Length:** 600-800 words
**Audience:** Engineering leadership, Product leadership

### 3. Architecture Decision Record (ADR)

**Structure:**

- **Status**: Proposed / Accepted / Deprecated
- **Context**: What problem are we solving?
- **Decision**: What we're doing
- **Consequences**: Positive and negative outcomes
- **Alternatives Considered**: What we rejected and why

**Length:** 400-600 words
**Audience:** Engineering team, future maintainers

## Quality Standards

### Clarity

- No jargon without definition
- Use tables for comparisons
- Lead with conclusion, then evidence
- One idea per paragraph

### Rigor

- Every claim cited (documentation, benchmarks, case studies)
- Quantify when possible (cost, time, performance)
- State assumptions explicitly
- Include confidence level (high/medium/low)

### Actionability

- Clear recommendation
- Specific next steps with owners
- Timeline with milestones
- Success criteria

## Example: Technology Selection Document

```markdown
# Technology Selection: Mobile Analytics Platform

## Executive Summary

Recommend adopting Amplitude over Mixpanel for mobile analytics. Amplitude provides superior mobile SDK performance (40% smaller bundle size), better iOS/Android platform support, and $120K lower annual cost at our scale. Implementation: 6 weeks, Q2 2026.

## Options Evaluated

| Criterion                 | Amplitude | Mixpanel | Firebase Analytics    |
| ------------------------- | --------- | -------- | --------------------- |
| Mobile SDK size           | 2.1 MB    | 3.5 MB   | 1.8 MB (bundled)      |
| iOS/Android support       | Excellent | Good     | Excellent             |
| Annual cost (100M events) | $180K     | $300K    | $0 (limited features) |
| Query flexibility         | High      | High     | Low                   |
| Data export               | Yes       | Yes      | Limited               |

## Recommendation

**Adopt Amplitude.** Best balance of mobile performance, feature completeness, and cost.

## Total Cost of Ownership (3 years)

- Licensing: $540K ($180K/year)
- Implementation: $80K (6 weeks engineering)
- Training: $10K
- **Total: $630K**

## Implementation Plan

- **Week 1-2**: SDK integration (iOS/Android)
- **Week 3-4**: Event schema migration
- **Week 5**: QA and validation
- **Week 6**: Production rollout

## Risk Assessment

- **Data migration complexity**: Medium. Mitigation: Run both platforms in parallel for 2 weeks.
- **Vendor lock-in**: Low. Standard event format, export API available.

## Success Criteria

- Mobile app bundle size increase < 3 MB
- Event delivery latency < 5 seconds
- Zero data loss during migration
- Product team can self-serve queries within 2 weeks
```

## Collaboration Points

- **With CPO**: Validate business impact, competitive implications
- **With CTO** (when hired): Validate technical depth, implementation feasibility
- **With Finance**: Validate cost projections, TCO analysis
- **With Engineering**: Validate effort estimates, technical claims

## Templates

Store reusable templates in `company/departments/research-develop/supervisor/chief-information-officer/templates/`:

- `technology-selection-template.md`
- `version-analysis-template.md`
- `adr-template.md`
