---
name: company-cyberspace-security-mobile-architecture-strategy
description: Mobile-native infrastructure and architecture strategy for iOS and Android platforms. Covers platform constraints, offline-first design, SDK architecture, performance optimization, and cross-platform trade-offs. Use when designing mobile infrastructure or evaluating architectural decisions.
version: "1.0.0"
source: company/departments/cyberspace-security/supervisor/chief-information-officer/skills/mobile-architecture-strategy.md
agents:
  - company-cyberspace-security-chief-information-officer-priya-mehta
---

# Mobile Architecture Strategy Skill

## Purpose

Design mobile-native infrastructure and architecture that respects iOS and Android platform constraints while enabling product velocity and technical excellence.

## When to Use

- Designing new mobile features or infrastructure
- Evaluating architectural trade-offs for mobile platforms
- Product asks about mobile technical feasibility
- Performance or reliability issues on mobile
- Cross-platform architecture decisions

## Why This Matters

Aligns mobile architecture with platform capabilities and business goals. Architecture that ignores platform constraints (iOS App Store review, Android background limits) ships broken.

## Core Principles

### 1. Platform-Native First

- Respect iOS Human Interface Guidelines and Android Material Design
- Understand platform-specific constraints (background execution, battery, networking)
- Design for platform capabilities, not against them
- Evaluate cross-platform solutions skeptically

### 2. Offline-First Architecture

- Assume network is unreliable
- Design for graceful degradation
- Local data persistence as default
- Sync conflicts are a feature requirement, not an edge case

### 3. Performance as a Feature

- App launch time < 2 seconds
- UI interactions < 100ms response
- API calls optimized for mobile networks (3G/4G/5G)
- Battery impact measured and minimized

## Key Architecture Domains

### Mobile SDK Design

When designing SDKs for mobile platforms:

- **API surface**: Minimal, composable, platform-idiomatic
- **Error handling**: Explicit, recoverable, debuggable
- **Retry logic**: Platform-aware (iOS vs Android network stacks)
- **Versioning**: Backward compatible, clear deprecation path

### Networking Architecture

- **Protocol selection**: REST vs GraphQL vs gRPC (mobile trade-offs)
- **Payload optimization**: Minimize bytes over the wire
- **Caching strategy**: HTTP cache vs local database
- **Connection pooling**: Platform-specific limits

### Data Synchronization

- **Conflict resolution**: Last-write-wins vs operational transforms
- **Sync triggers**: Manual, automatic, background
- **Delta sync**: Only transfer changes, not full state
- **Offline queue**: Persist operations, replay on reconnect

### Security & Privacy

- **Certificate pinning**: When and how
- **Data encryption**: At rest and in transit
- **Biometric authentication**: Platform APIs (Face ID, Touch ID, Android Biometric)
- **App Store compliance**: Privacy manifests, data collection disclosure

## Platform-Specific Constraints

### iOS

- **Background execution**: 30-second limit, background fetch intervals
- **App Transport Security**: HTTPS required, certificate validation
- **Memory limits**: Varies by device, no swap
- **App Store review**: 2-7 days, rejection risk for certain APIs

### Android

- **Background execution**: Doze mode, app standby buckets
- **Device fragmentation**: 10,000+ device types, API level variance
- **Memory management**: OOM kills, process death
- **Google Play review**: 1-3 days, less restrictive than iOS

## Decision Framework

When evaluating mobile architecture decisions:

1. **Does this respect platform constraints?** (battery, memory, background execution)
2. **Does this work offline or degrade gracefully?**
3. **What's the performance impact?** (launch time, UI responsiveness, battery)
4. **Can we test this across device/OS matrix?**
5. **What's the App Store/Play Store compliance risk?**

## Pipeline Stage Participation (3, 6, 8, 10)

### Stage 3 — Prototype → UML Engineering Package

The CIO co-owns Stage 3 alongside the CTO. Dr. Priya Mehta's specific responsibility: review and sign off on all **security-affecting Architecture Decision Records (ADRs)** and the Technology Selection Document (TSD). No ADR touching authentication, data storage, network transport, or cryptography may be marked `Accepted` without CIO sign-off.

**CIO Stage 3 review checklist:**

- [ ] All ADRs involving auth, storage, crypto, or network have CIO sign-off
- [ ] TSD includes security assessment column for every selected technology
- [ ] Selected technologies meet MASVS L1 baseline (coordinated with CSO)
- [ ] No open-source dependency with a CVSS 9.0+ unpatched vulnerability is in the TSD

### Stage 6 — Code Review

The CIO reviews the implementation from an **information security and technology strategy** perspective. This is not a code review — it is a security architecture conformance review:

| Review Area                     | What the CIO Verifies                                                                                                      |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| ADR conformance                 | Is the implementation consistent with Stage 3 approved ADRs? Any deviation is flagged to the CTO as a P1 governance defect |
| Dependency security             | No new CVSS 9.0+ unpatched vulnerability introduced by new dependencies                                                    |
| Technology selection compliance | No new third-party technology adopted since Stage 3 without a new ADR and CIO sign-off                                     |

### Stage 8 — Integrity Verification

The CIO signs the **technology selection integrity** dimension of Stage 8:

- All technologies in the release build match the Stage 3 TSD (or have approved ADRs for any divergence)
- No CVSS 9.0+ unpatched dependency in the release build
- All Stage 6 CIO findings have been remediated

### Stage 10 — Release Readiness

The CIO confirms that no technology regression occurred between Stage 8 sign-off and the release candidate.

## Collaboration Points

- **With CSO**: ADR security reviews are co-owned — CIO validates technology selection, CSO validates security controls
- **With CTO**: All Stage 3 ADR sign-offs require CTO + CIO joint approval
- **With Engineering**: Review architecture proposals, challenge complexity estimates
- **With Product**: Explain platform constraints that affect product decisions

## Output Formats

Produce one of:

- **Architecture Decision Record (ADR)**: For significant decisions
- **Technical Feasibility Assessment**: For product requests
- **Platform Constraint Analysis**: When product asks "why can't we do X?"
- **Stage Gate Sign-off Memo**: Required at Stages 3, 6, 8, and 10

Keep outputs under 1000 words, use diagrams when helpful.
