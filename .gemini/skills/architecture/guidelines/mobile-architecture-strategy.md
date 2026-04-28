---
name: mobile-architecture-strategy
description: Design mobile-native infrastructure and architecture that respects iOS and Android platform constraints while enabling product velocity and technical excellence.
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

## Collaboration Points

- **With CPO**: Translate product requirements into technical feasibility assessments
- **With Engineering**: Review architecture proposals, challenge complexity estimates
- **With Product**: Explain platform constraints that affect product decisions

## Output Formats

Produce one of:

- **Architecture Decision Record (ADR)**: For significant decisions
- **Technical Feasibility Assessment**: For product requests
- **Platform Constraint Analysis**: When product asks "why can't we do X?"

Keep outputs under 1000 words, use diagrams when helpful.
