---
name: architecture-guidelines-mobile-adr-production
description: Mobile ADR production for iOS and Android — ADR format, decision taxonomy, lifecycle management, supersession chains, and technology decision locking at Stage 3. Owned by Rafael Okonkwo (Software Architect). Use during Stage 3 (UML Engineering) for mobile-specific ADR authorship and Stage 8 (Integrity Verification) for ADR conformance. Trigger: mobile ADR, architecture decision mobile, ADR production, technology decision locking, mobile architecture decision.
prerequisites:
  - architecture-guidelines-architecture-decision-records

version: "1.0.0"
---

# Mobile ADR Production

**Category:** Architecture Governance
**Owner:** Software Architect / CTO / CIO

## Purpose

Create, review, and maintain Architecture Decision Records (ADRs) that document significant technical decisions for mobile platform development. This skill covers ADR format, decision taxonomy, lifecycle management, supersession chains, and the role of ADRs within Stage 3 (Architecture) where technology decisions are locked and not revisable in later stages.

## Execution Guidance

### ADR Template

```markdown
# ADR-{NNN}: {Decision Title}

| Field         | Value                                 |
| ------------- | ------------------------------------- |
| **Status**    | Accepted / Superseded / Deprecated    |
| **Date**      | YYYY-MM-DD                            |
| **Authors**   | {name, role}                          |
| **Reviewers** | {CTO, CIO, platform leads}            |
| **Stage**     | Stage 3 (Architecture)                |
| **Platform**  | iOS / Android / Cross-Platform / Both |
| **Category**  | Architecture / Data / UI / Security   |

## Context

{Describe the problem or decision that needs to be made. Include relevant constraints, requirements, and stakeholder concerns. 2-3 paragraphs.}

## Decision

{State the decision clearly. "We will use {X} for {purpose} because {reason}." One sentence, bold.}

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
| ----------- | ---- | ---- | ------------ |
| {Option A}  | ...  | ...  | {reason}     |
| {Option B}  | ...  | ...  | {reason}     |

### Consequences

**Positive:**

- {Benefit 1}
- {Benefit 2}

**Negative:**

- {Cost 1}
- {Cost 2}
- {Trade-off 1}

## Compliance

{Note any standards, guidelines, or policies this decision aligns with or deviates from.}

## References

- {Link 1}
- {Link 2}
```

### Mobile ADR Decision Taxonomy

Decisions that **must** have an ADR in mobile projects:

| Category              | Example Decisions                                   | Impact   |
| --------------------- | --------------------------------------------------- | -------- |
| Platform selection    | Native (Swift/Kotlin) vs Flutter vs React Native    | Critical |
| Architecture pattern  | MVVM vs MVI vs Clean Architecture                   | High     |
| State management      | Combine vs RxSwift vs custom; ViewModel vs Redux    | High     |
| Navigation            | Programmatic vs storyboard vs Compose Navigation    | High     |
| Persistence           | Core Data vs SQLite vs Realm vs Room                | High     |
| Networking            | URLSession + Codable vs Alamofire vs Retrofit       | Medium   |
| Dependency injection  | Manual vs Swift-DI vs Dagger/Hilt                   | Medium   |
| CI/CD platform        | GitHub Actions vs Fastlane + Bitrise vs Xcode Cloud | Medium   |
| Testing framework     | XCTest vs Quick/Nimble vs Espresso                  | Medium   |
| Minimum OS version    | iOS 15+ vs iOS 16+; API 28 vs API 31                | Critical |
| Third-party libraries | Any library with > 50KB binary impact               | Medium   |
| Security approach     | Keychain vs encrypted file storage; cert pinning    | Critical |

### ADR Lifecycle

```
Draft → Review → Accepted → (Implemented) → (Superseded) → Deprecated

Draft:       Author writes decision, lists alternatives
Review:      CTO + CIO + relevant platform leads review
Accepted:    Approved at Stage 3 gate — decision is LOCKED
Implemented: Code follows the decision (Stage 5)
Superseded:  New ADR replaces this one (requires Stage 3 re-evaluation)
Deprecated:  Decision is no longer relevant
```

**Example ADR:**

```markdown
# ADR-003: State Management — Combine + MVVM

| Field         | Value                                           |
| ------------- | ----------------------------------------------- |
| **Status**    | Accepted                                        |
| **Date**      | 2026-03-15                                      |
| **Authors**   | Seo Yeon Park (iOS Lead)                        |
| **Reviewers** | Dr. Kenji Nakamura (CTO), Dr. Priya Mehta (CIO) |
| **Stage**     | Stage 3 (Architecture)                          |
| **Platform**  | iOS                                             |
| **Category**  | Architecture                                    |

## Context

The iOS application requires a state management approach that handles reactive UI updates, supports unit testing of business logic, and integrates with the existing UIKit codebase. The team has evaluated several options considering the iOS 15+ minimum deployment target and the existing team's familiarity with reactive patterns.

## Decision

**We will use Combine framework with MVVM pattern for all iOS state management.**

ViewModels expose state via `@Published` properties and computed signals. Views observe through `sink` or `assign(to:)`. All business logic lives in ViewModels, not ViewControllers.

### Alternatives Considered

| Alternative      | Pros                           | Cons                                          | Why Rejected                                               |
| ---------------- | ------------------------------ | --------------------------------------------- | ---------------------------------------------------------- |
| RxSwift          | Mature, extensive operators    | External dependency, steeper learning curve   | Combine is built into iOS 13+; no dependency needed        |
| Redux (ReSwift)  | Predictable state, time travel | Boilerplate-heavy, overkill for this app size | MVVM provides sufficient predictability with less ceremony |
| Delegate pattern | Simple, no framework           | Manual wiring, doesn't scale                  | Doesn't support reactive updates needed for real-time data |

### Consequences

**Positive:**

- Zero external dependencies for state management
- Native Apple framework — long-term support guaranteed
- `@Published` integrates directly with UIKit via Combine
- ViewModels are pure Swift — fully unit testable

**Negative:**

- Team needs Combine training (estimated 1 week per engineer)
- Combine debugging can be opaque — requires proper tooling
- iOS 13-14 compatibility requires careful testing (we target iOS 15+)

## Compliance

Aligns with Apple's recommended patterns (WWDC 2021: "Explore SwiftUI State Management", applicable to Combine/UIKit).

## References

- ADR-001: Platform Selection — Native iOS (Swift)
- ADR-002: Minimum iOS Version — iOS 15
- Apple Combine Documentation
```

### ADR Review Checklist

| Criterion                  | Question                                       | Gate   |
| -------------------------- | ---------------------------------------------- | ------ |
| Context is clear           | Would a new engineer understand the problem?   | Must   |
| Decision is unambiguous    | Is the "what" stated in one sentence?          | Must   |
| Alternatives are fair      | Were real alternatives evaluated?              | Must   |
| Consequences are honest    | Are trade-offs acknowledged?                   | Must   |
| Decision is implementable  | Can Stage 5 engineers act on this?             | Must   |
| No technology lock-in risk | Is the chosen solution maintainable long-term? | Should |

## Pipeline Integration

**Stage 3 (Architecture):** ADRs are produced by CTO and CIO. Once accepted at the Stage 3 gate, they are **locked** — technology decisions are not revisable in Stage 4+.

**Stage 5 (Development):** Platform leads verify that implementation matches accepted ADRs. Any deviation requires ADR amendment (not override).

**Stage 8 (Integrity Verification):** Panel verifies code conforms to all accepted ADRs. Non-conformance is a P1 defect.

**Stage 10 (Release):** Architecture sign-off (CTO + CIO) includes ADR compliance verification.

## Quality Standards

| Metric             | Target                                     | Measurement             |
| ------------------ | ------------------------------------------ | ----------------------- |
| ADR coverage       | 100% of critical decisions documented      | Architecture audit      |
| ADR clarity        | All ADRs pass review checklist             | CTO/CIO review          |
| ADR conformance    | 100% code matches accepted ADRs            | Stage 8 integrity check |
| Supersession chain | Every superseded ADR links to successor    | Manual audit            |
| ADR freshness      | No ADR older than 12 months without review | ADR index review        |

## Reference Materials

- [Michael Nygard's ADR Format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Organization](https://adr.github.io/)
- [Architecture Decision Records — ThoughtWorks](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- `company/pipeline/mobile-development/pipeline.md` — Stage 3 specification
- `company/library/topics/architecture.md` — UML engineering guidance
