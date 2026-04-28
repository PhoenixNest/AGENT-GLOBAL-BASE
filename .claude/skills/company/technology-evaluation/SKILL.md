---
name: company-technology-evaluation
description: Systematic evaluation of emerging mobile technologies — research methodology, competitive analysis, TCO assessment, migration risk matrices, vendor lock-in evaluation, and executive-grade technology selection documentation. Owned by Dr. Priya Mehta (CIO).
disable-model-invocation: false
---

# Technology Evaluation Skill

## Purpose

Evaluate emerging technologies, frameworks, platforms, and vendor solutions to determine their fit for mobile-first product development. Produce clear, actionable recommendations that balance technical merit with business impact.

## When to Use

- Product or Engineering requests evaluation of a new technology, framework, or platform
- User asks "Should we use X?" or "What's the best option for Y?"
- Competitive intelligence reveals a technology gap
- Technology vendor proposes a solution
- Annual or quarterly technology roadmap planning

## Evaluation Framework

### 1. Technology Overview

- **What it is**: 2-3 sentence description
- **Current maturity**: Alpha/Beta/GA, version number, release date
- **Vendor/Community**: Who maintains it, funding model, community size
- **Adoption signal**: Notable companies using it in production

### 2. Mobile Platform Fit

- **iOS compatibility**: Minimum iOS version, platform-specific constraints
- **Android compatibility**: Minimum Android API level, platform-specific constraints
- **Cross-platform story**: Does it work on both? Trade-offs?
- **Platform-native integration**: How well does it respect platform conventions (HIG, Material Design)?

### 3. Technical Merit

- **Core capability**: What problem does it solve?
- **Performance characteristics**: Latency, throughput, resource usage
- **Developer experience**: Learning curve, documentation quality, tooling support
- **Technical debt risk**: Lock-in, migration complexity, deprecation risk

### 4. Business Impact

- **Time to value**: How long to integrate and ship?
- **Cost structure**: Licensing, infrastructure, maintenance costs
- **Competitive advantage**: Does this create differentiation or just parity?
- **Risk assessment**: What breaks if this fails?

### 5. Implementation Risk

- **Integration complexity**: Low/Medium/High, estimated engineering weeks
- **Team capability gap**: Do we have the skills? Training needed?
- **Dependency risk**: What does this depend on? Single vendor? Open source stability?
- **Migration path**: Can we reverse this decision? At what cost?

### 6. Recommendation

- **Decision**: Adopt / Trial / Watch / Pass
- **Rationale**: 2-3 sentences explaining why
- **Next steps**: Specific actions with owners and timelines
- **Success criteria**: How will we know this was the right choice?

## Output Format

Produce a markdown document titled: `Technology Evaluation: [Technology Name]`

Include all six sections above. Keep it under 1500 words. Use tables for comparison when evaluating multiple options.

## Example Scenarios

**Scenario 1**: Should we use React Native or native iOS/Android?

- Evaluate both against framework; focus on mobile platform fit and long-term maintenance cost; provide clear recommendation with migration risk assessment.

**Scenario 2**: Engineering proposes adopting GraphQL for mobile APIs

- Assess technical merit (query flexibility, payload size); evaluate mobile-specific benefits (reduced over-fetching, offline support); analyze implementation risk; recommend adoption path or alternative.

**Scenario 3**: Vendor pitches a mobile analytics platform

- Compare against existing solution and alternatives; assess cost structure and lock-in risk; evaluate data privacy implications for App Store/Play Store compliance; recommend trial, adoption, or pass.

## Quality Standards

- Every claim must be verifiable (cite documentation, benchmarks, case studies)
- No vendor marketing language — use neutral technical terminology
- Explicitly state assumptions and confidence level
- Include dissenting opinions or alternative viewpoints
- Update evaluations when new information emerges (version updates, security issues)
