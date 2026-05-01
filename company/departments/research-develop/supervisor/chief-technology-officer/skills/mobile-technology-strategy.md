---
name: mobile-technology-strategy
description: Mobile technology strategy and emerging technology evaluation. Use when the user needs to research emerging mobile technologies, evaluate technology options, create technology selection documentation, assess competitive advantages through technology choices, or establish mobile technology roadmaps. Trigger when user mentions "technology evaluation", "emerging technologies", "technology selection", "mobile strategy", or needs to assess new technologies.
version: "1.0.0"
---

# Mobile Technology Strategy

## Purpose

Continuously research, evaluate, and select mobile technologies that establish competitive advantage. Provide systematic frameworks for assessing emerging technologies against business impact, implementation risk, and strategic positioning.

## Why This Matters

Evaluates emerging mobile technologies for competitive advantage. Missing technology strategy causes reactive adoption of trends rather than strategic capability building.

## When to Use This Skill

Use this skill when:

- Evaluating new mobile technologies, frameworks, or platforms
- Making critical technology selection decisions
- Researching emerging trends in mobile development
- Assessing competitive positioning through technology choices
- Creating technology roadmaps for mobile platforms
- Producing technology selection documentation for stakeholders

## Technology Evaluation Framework

### 1. Technology Radar Methodology

Organize technologies into four categories:

**Adopt**: Technologies we're confident in and actively using

- Proven at scale in production
- Team has expertise
- Clear ROI demonstrated

**Trial**: Technologies worth pursuing in limited scope

- Promising but not yet proven at our scale
- Pilot projects or proof-of-concepts recommended
- Monitor closely for production readiness

**Assess**: Technologies to watch and evaluate

- Emerging but not ready for investment
- Research and small experiments appropriate
- Track for future consideration

**Hold**: Technologies to avoid or phase out

- Better alternatives exist
- Strategic misalignment
- Technical or business risks too high

### 2. Evaluation Criteria

Assess each technology across these dimensions:

**Technical Merit**

- Maturity: Is this production-ready?
- Performance: Does it meet our requirements?
- Reliability: What's the failure rate and recovery story?
- Security: Are there known vulnerabilities?
- Platform support: iOS/Android coverage and version requirements

**Business Impact**

- Time to value: How quickly can we ship with this?
- Cost: Licensing, infrastructure, training, maintenance
- Competitive advantage: Does this differentiate us?
- Risk: What happens if this fails or is abandoned?

**Team Capability**

- Learning curve: How long to become productive?
- Existing expertise: Do we have skills in-house?
- Hiring market: Can we recruit for this?
- Community support: Is help available when we're stuck?

**Strategic Fit**

- Alignment with roadmap: Does this support our direction?
- Vendor lock-in: Can we switch if needed?
- Long-term viability: Will this be maintained in 3-5 years?
- Ecosystem: Does this integrate with our stack?

### 3. Comparative Analysis Process

When evaluating multiple options:

1. **Define selection criteria** with weights
   - Must-haves vs nice-to-haves
   - Relative importance of each criterion
   - Success and failure conditions

2. **Research each option** systematically
   - Official documentation
   - Production case studies
   - Community feedback and issues
   - Performance benchmarks
   - Security audits

3. **Create comparison matrix**
   - Score each option against criteria
   - Document evidence for each score
   - Calculate weighted totals
   - Identify clear winner or trade-offs

4. **Prototype critical paths**
   - Build proof-of-concept for top 2-3 options
   - Test against real requirements
   - Measure actual performance
   - Assess developer experience

5. **Document recommendation**
   - Clear recommendation with rationale
   - Trade-offs and risks
   - Implementation plan
   - Success metrics

## Mobile Technology Landscape

### iOS Platform Technologies

**UI Frameworks**

- SwiftUI: Modern declarative UI, iOS 13+
- UIKit: Mature imperative UI, all iOS versions
- Hybrid: SwiftUI + UIKit for gradual migration

**State Management**

- Combine: Apple's reactive framework
- async/await: Modern Swift concurrency
- Redux-like: TCA, ReSwift for unidirectional flow

**Networking**

- URLSession: Native networking
- Alamofire: Popular third-party wrapper
- GraphQL clients: Apollo iOS, Relay

**Local Storage**

- Core Data: Apple's ORM
- Realm: Mobile-first database
- SQLite: Direct SQL access
- UserDefaults: Simple key-value

**Cross-Platform Shared Code**

- Kotlin Multiplatform Mobile: Share business logic
- C++: Low-level shared code
- React Native/Flutter: Full cross-platform

### Android Platform Technologies

**UI Frameworks**

- Jetpack Compose: Modern declarative UI
- Views: Traditional XML-based UI
- Hybrid: Compose + Views for migration

**Architecture Components**

- ViewModel: UI state management
- LiveData/StateFlow: Observable data
- Room: SQLite ORM
- WorkManager: Background tasks

**Dependency Injection**

- Hilt: Recommended by Google
- Koin: Kotlin-first, simpler
- Dagger: Powerful but complex

**Networking**

- Retrofit: Type-safe HTTP client
- OkHttp: Low-level HTTP
- Ktor: Kotlin multiplatform

**Reactive Programming**

- Kotlin Coroutines: Structured concurrency
- RxJava: Reactive extensions
- Flow: Kotlin's reactive streams

### Emerging Technologies to Track

**5G and Edge Computing**

- Ultra-low latency applications
- Edge processing for privacy
- Network slicing for QoS

**On-Device Machine Learning**

- Core ML (iOS): On-device inference
- ML Kit (Android): Google's ML APIs
- TensorFlow Lite: Cross-platform
- Privacy-preserving ML

**Augmented Reality**

- ARKit (iOS): Apple's AR framework
- ARCore (Android): Google's AR platform
- WebXR: Browser-based AR

**Wearables and IoT**

- WatchOS: Apple Watch development
- Wear OS: Android wearables
- HealthKit/Google Fit: Health data
- HomeKit/Google Home: Smart home

**App Clips and Instant Apps**

- Lightweight app experiences
- No installation required
- Discovery through NFC, QR, web

## Technology Selection Documentation

### Selection Document Template

```markdown
# Technology Selection: [Technology Name]

## Executive Summary

[2-3 sentences: What are we selecting and why?]

## Business Context

- Problem: What business need drives this?
- Opportunity: What advantage does this create?
- Timeline: When do we need this?
- Budget: What resources are available?

## Options Evaluated

1. [Option 1]
2. [Option 2]
3. [Option 3]

## Evaluation Criteria

| Criterion   | Weight | Option 1 | Option 2 | Option 3 |
| ----------- | ------ | -------- | -------- | -------- |
| Performance | 25%    | 4/5      | 3/5      | 5/5      |
| Maturity    | 20%    | 5/5      | 3/5      | 2/5      |
| Team Fit    | 20%    | 3/5      | 5/5      | 2/5      |
| Cost        | 15%    | 4/5      | 4/5      | 5/5      |
| Ecosystem   | 20%    | 5/5      | 3/5      | 3/5      |
| **Total**   |        | **4.15** | **3.65** | **3.45** |

## Detailed Analysis

### Option 1: [Name]

**Pros:**

- [Specific advantage with evidence]
- [Specific advantage with evidence]

**Cons:**

- [Specific limitation with evidence]
- [Specific limitation with evidence]

**Evidence:**

- [Case study, benchmark, or reference]

### [Repeat for other options]

## Recommendation

**Selected: [Option Name]**

**Rationale:**
[2-3 paragraphs explaining why this option best meets our needs]

**Trade-offs Accepted:**

- [What we're giving up by choosing this]

**Risks and Mitigations:**
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Medium | High | [How we'll address it] |

## Implementation Plan

1. **Phase 1**: [Pilot/POC]
2. **Phase 2**: [Limited rollout]
3. **Phase 3**: [Full adoption]

## Success Metrics

- [Metric 1]: [Target]
- [Metric 2]: [Target]
- [Metric 3]: [Target]

## Decision Authority

- Recommended by: [CTO]
- Reviewed by: [CIO, CPO]
- Approved by: [CEO/Board if needed]
- Date: [YYYY-MM-DD]
```

## Collaboration with CPO and CIO

**With Chief Product Officer:**

- Translate product requirements into technology capabilities
- Assess whether emerging technologies enable new product opportunities
- Balance innovation with execution risk
- Align technology roadmap with product roadmap

**With Chief Information Officer:**

- Coordinate on infrastructure and platform decisions
- Leverage existing technology investments
- Ensure architectural consistency
- Share research on emerging technologies

## Competitive Intelligence

Track what competitors are doing:

- Technology stack analysis from job postings
- Conference talks and blog posts
- App teardowns and reverse engineering
- Patent filings and research papers

Use competitive intelligence to:

- Identify technology gaps
- Validate technology choices
- Anticipate market shifts
- Find differentiation opportunities

## Continuous Research Process

**Weekly**: Scan tech news, release notes, community discussions
**Monthly**: Deep dive on 1-2 emerging technologies
**Quarterly**: Publish Technology Radar update
**Annually**: Strategic technology roadmap review

**Sources to monitor:**

- Apple WWDC, Google I/O announcements
- Mobile development conferences (try! Swift, Droidcon, App.js)
- GitHub trending repositories
- Hacker News, Reddit r/iOSProgramming, r/androiddev
- Technology vendor blogs and roadmaps

## Output Format

When evaluating technologies, produce:

1. **Technology Radar**: Visual representation of technology landscape
2. **Selection Document**: Detailed analysis and recommendation
3. **Proof-of-Concept**: Working code demonstrating viability
4. **Presentation**: Executive summary for stakeholders
5. **Implementation Plan**: Phased adoption strategy

Documentation should be clear enough for non-technical stakeholders while providing sufficient technical depth for engineering teams.
