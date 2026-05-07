# Kiro Skills — Domain-Based Organization

**Status:** Active  
**Last Updated:** 2026-05-07  
**Authority:** ECOSYSTEM_SPEC.md § Part VII — Skills Import & Domain Structure

---

## Overview

This directory contains Kiro skills organized into **domain-based categories** following the
[Kiro Skills specification](https://kiro.dev/docs/cli/skills/). Each domain has a parent `SKILL.md`
file that serves as a router to sub-skills in the `references/` subdirectory.

## Structure Pattern

```
.kiro/skills/
├── domain-name/
│   ├── SKILL.md              # Parent skill (router)
│   └── references/           # Sub-skills
│       ├── sub-skill-1.md
│       ├── sub-skill-2.md
│       └── sub-skill-3.md
```

## Domain Categories

### Company Domains

| Domain                | Skills | Description                                       |
| --------------------- | ------ | ------------------------------------------------- |
| `product-management`  | 8      | Product strategy, PRD authorship, stage gates     |
| `product-design`      | 6      | Mobile design systems, UI/UX, design handoff      |
| `engineering`         | 48     | Architecture, ADRs, UML, DevEx, cross-cutting     |
| `technology-strategy` | 4      | Tech evaluation, architecture strategy, ADRs      |
| `cyberspace-security` | 17     | Security architecture, hardening, risk assessment |
| `localization`        | 5      | Translation, i18n engineering, linguist ops       |
| `recruitment`         | 10     | Candidate vetting, role-specific recruitment      |
| `quality-assurance`   | 23     | Testing, defect classification, QA automation     |
| `data-analytics`      | 3      | Metrics, instrumentation, A/B testing             |

### Mobile & Platform Engineering Domains

| Domain                       | Skills | Description                                   |
| ---------------------------- | ------ | --------------------------------------------- |
| `android-engineering`        | 12     | Kotlin, Jetpack Compose, Coroutines, testing  |
| `ios-engineering`            | 17     | Swift, SwiftUI, UIKit, Combine, testing       |
| `cross-platform-engineering` | 9      | KMP, Flutter, React Native                    |
| `backend-engineering`        | 27     | APIs, databases, Go, Python, cloud, messaging |
| `frontend-engineering`       | 17     | React, Vue, Angular, SSR, a11y, performance   |

### Studio Domains

| Domain                      | Skills | Description                             |
| --------------------------- | ------ | --------------------------------------- |
| `game-development`          | 15     | Studio leadership, GDD, production, F2P |
| `audio-engineering`         | 4      | Game audio, FMOD/Wwise, chiptune, music |
| `visual-arts-and-animation` | 3      | Art direction, art pipeline, team lead  |
| `live-operations`           | 3      | Live ops strategy, community, events    |

### CC-00 Laboratory Domains

| Domain            | Skills | Description                                   |
| ----------------- | ------ | --------------------------------------------- |
| `llm-engineering` | 4      | LLM system design, context, harness, RAG, MAE |

## Total Skills: 235

## Usage

### Activating a Domain Skill

To activate a domain skill and access its sub-skills:

```typescript
discloseContext({
  name: "android-engineering",
});
```

This loads the parent `SKILL.md` which provides an overview and guides you to the specific
sub-skills in the `references/` directory.

### Accessing Sub-Skills

Sub-skills are located in the `references/` subdirectory of each domain:

```
.kiro/skills/android-engineering/references/android-implementation.md
.kiro/skills/backend-engineering/references/distributed-systems.md
.kiro/skills/quality-assurance/references/api-contract-testing.md
```

## Skill Inventory

### product-management (8 skills)

- `mobile-product-strategy.md` — Product vision, strategy, and roadmap planning
- `prd-authorship.md` — PRD structure, content, and quality standards
- `product-stage-gates.md` — Stage gate enforcement and approval workflows
- `web-product-strategy.md` — Web-native product strategy, PWA optimization, performance budgets
- `web-accessibility-governance.md` — WCAG 2.1 AA standards implementation and scaling
- `api-product-strategy.md` — API-as-Product vision, monetization modeling, developer experience
- `api-governance.md` — API lifecycle management, versioning policy, backward-compatibility
- `developer-portal-and-devrel.md` — Developer portal strategy and developer relations

### product-design (6 skills)

- `mobile-design-systems.md` — Design system architecture and component libraries
- `interaction-design-specification.md` — IDS authorship and interaction patterns
- `design-to-engineering-handoff.md` — Handoff workflows and asset delivery
- `user-research-driven-design.md` — Research methods and design validation
- `design-leadership-and-quality-gates.md` — Design review and approval processes
- `wcag-mobile-roadmap.md` — WCAG mobile accessibility roadmap and compliance strategy

### engineering (48 skills)

- `adr-governance.md` — ADR authorship and architecture review board processes
- `adr-technical-writing.md` — Technical writing for architecture decision records
- `adr-template-adaptation.md` — ADR template customisation for context
- `api-technical-writing.md` — API documentation authorship
- `architecture-decision-records.md` — ADR process fundamentals
- `architecture-review-shadowing.md` — Architecture review participation and mentorship
- `architecture-syncs.md` — Architecture sync facilitation and follow-up
- `aws-organizations,-control-tower,-scps,-cross-account-iam,-cloudtrail.md` — AWS org governance
- `build-optimization.md` — Build system optimisation patterns
- `cicd-security.md` — CI/CD pipeline security hardening
- `cloud-infrastructure.md` — Cloud infrastructure fundamentals
- `cloudwatch,-datadog,-cost-optimization,-audit-logging,-compliance-reporting.md` — Observability and cost
- `code-review-participation.md` — Code review standards and participation
- `code-review-standards.md` — Code review criteria and processes
- `compliance-foundations.md` — Compliance baseline for engineering teams
- `cross-functional-coordination.md` — Cross-team coordination patterns
- `developer-analytics.md` — Developer productivity metrics and DORA
- `developer-documentation.md` — Internal documentation standards
- `developer-platform-engineering.md` — Internal Developer Platform, CI/CD, golden-path templates
- `docker-orchestration.md` — Docker container orchestration
- `elk-stack,-fluentd,-anomaly-detection,-real-time-alerting.md` — Log aggregation and alerting
- `engineering-leadership.md` — Engineering team leadership skills
- `gcp-multi-region.md` — GCP multi-region architecture
- `github-actions,-parallel-test-execution,-ci-telemetry,-deployment-frequency.md` — CI/CD metrics
- `iac-gitops.md` — Infrastructure-as-Code and GitOps practices
- `ids-fluency.md` — IDS comprehension and design-engineering feasibility review
- `kubernetes-at-scale.md` — Kubernetes operator patterns and cluster management
- `mobile-adr-production.md` — Mobile-specific ADR production
- `mobile-architecture-patterns.md` — Mobile architecture patterns (MVVM, MVI, Clean)
- `mobile-optimization.md` — Mobile performance optimisation
- `mobile-platform-assessment.md` — Mobile platform technical assessment
- `mobile-platform-immersion.md` — Mobile platform deep-dive and onboarding
- `mobile-scanning-tools.md` — Mobile application scanning and SAST tools
- `mobile-technology-strategy.md` — Platform selection and technology evaluation for mobile
- `mobile-testing-fundamentals.md` — Mobile testing baseline competency
- `performance-optimization.md` — System-wide performance optimisation
- `pipeline-documentation.md` — Pipeline documentation standards
- `practice-uml-adr.md` — UML and ADR practice exercises
- `prd-fluency.md` — PRD comprehension and engineering translation
- `risk-management.md` — Engineering risk management
- `software-architecture-design.md` — Architecture patterns, UML, and design documentation
- `spec-development.md` — SPEC authorship, structure, and quality standards
- `sre-practices.md` — Site reliability engineering practices
- `system-design.md` — System design fundamentals and interview patterns
- `technical-project-management.md` — Project planning, execution, and delivery
- `uml-engineering-package.md` — UML engineering package production
- `uml-engineering.md` — UML diagramming and documentation
- `uml-production-certification.md` — UML production quality certification

### technology-strategy (4 skills)

- `technology-evaluation.md` — Technology assessment frameworks and evaluation criteria
- `mobile-architecture-strategy.md` — Platform architecture and strategic technology decisions
- `technical-selection-documentation.md` — TSD authorship and technology justification
- `mobile-platform-strategy.md` — KMP architecture, cross-platform code sharing, mobile org scaling

### cyberspace-security (17 skills)

- `mobile-security-architecture.md` — Security architecture patterns and mobile platform security
- `application-security-hardening.md` — OWASP MASVS compliance and hardening techniques
- `security-requirements-and-srd.md` — SRD authorship and security requirements definition
- `security-risk-assessment.md` — Risk assessment frameworks and threat modeling
- `emerging-threat-evaluation.md` — Threat intelligence and vulnerability assessment
- `masvs-overview.md` — OWASP MASVS executive briefing, mobile security gate interaction
- `threat-modeling.md` — Threat modeling methodologies (STRIDE, PASTA)
- `mobile-threat-modeling.md` — Mobile-specific threat modeling
- `security-operations.md` — Security operations and incident response
- `masvs-mastery-track-a.md` — MASVS L1 mastery track
- `masvs-mastery-track-b.md` — MASVS L2 mastery track
- `masvs-compliance-assessment,-mobile-banking-security-auditing.md` — Compliance assessment
- `container-runtime-security,-falco-rules,-ebpf-based-monitoring.md` — Container security
- `falco,-osquery,-container-security,-network-anomaly-detection.md` — Runtime security monitoring
- `network-security-fundamentals,-vpc-security,-security-groups,-nacls.md` — Network security
- `risk-assessments,-control-descriptions,-evidence-collection,-remediation-plans.md` — Risk documentation
- `webauthn,-biometric-authentication,-passkey-integration.md` — Modern authentication

### localization (5 skills)

- `language-translation-module.md` — LTM architecture, governance, and translation workflows
- `localization-engineering-and-cicd-gates.md` — i18n engineering patterns and CI/CD integration
- `linguist-operations-and-vendor-roster.md` — Vendor management and linguist coordination
- `arb-localization-engineering.md` — ARB file format, code generation, locale switching
- `string-extraction-and-resource-files.md` — String extraction and resource file management

### recruitment (10 skills)

- `vet-candidate.md` — Candidate assessment frameworks and vetting criteria
- `placement-and-profile-authoring.md` — Placement decisions and agent profile creation
- `onboarding-program-design.md` — Engineering onboarding programme design and tracking
- `recruit-business.md` — Business roles recruitment (Product, Strategy)
- `recruit-data.md` — Data roles recruitment (Analytics, Data Science)
- `recruit-design.md` — Design roles recruitment (UI/UX, Visual Design)
- `recruit-engineering.md` — Engineering roles recruitment (Mobile, Backend, Frontend)
- `recruit-product.md` — Product roles recruitment (PM, PO)
- `recruit-translation.md` — Translation roles recruitment (Linguists, i18n Engineers)
- `competency-frameworks,-role-specific-learning-paths,-milestone-tracking,-manager-dashboards.md` — Competency tracking

### quality-assurance (23 skills)

- `quality-engineering-strategy.md` — Test automation architecture, quality scorecard, release gate authority
- `axe-core-wcag-testing.md` — axe-core WCAG 2.1 AA test suite and accessibility automation
- `localization-testing-strategy.md` — Localization testing, TMS verification, pseudo-localization
- `mobile-test-automation.md` — Mobile test automation frameworks and strategies
- `defect-triage-protocol.md` — Defect triage workflows and severity classification
- `defect-triage-and-classification.md` — Defect classification P0–P3 and escalation
- `api-contract-testing.md` — Pact contract testing and consumer-driven contracts
- `automated-test-suite.md` — Automated test suite architecture and governance
- `react-testing-advanced.md` — Advanced React Testing Library, MSW, snapshot testing
- `vue-testing.md` — Vue Test Utils, Vitest, component testing
- `go-testing.md` — Go testing (testcontainers, gomock, table-driven tests)
- `backend-api-verification.md` — Backend API verification patterns
- `ci-cd-integration.md` — CI/CD test integration and quality gates
- `espresso-xctest.md` — Espresso and XCTest UI automation
- `flaky-test-detection,-auto-quarantine,-test-parallelization,-test-analytics.md` — Flaky test management
- `k6-performance.md` — k6 load and performance testing
- `maestro-testing.md` — Maestro E2E mobile testing
- `mobile-game-testing.md` — Mobile game-specific testing patterns
- `performance-profiling.md` — Application performance profiling
- `qa-team-leadership.md` — QA team leadership and strategy
- `test-automation-architecture.md` — Test automation architecture design
- `test-sharding-architecture,-parallel-execution,-shard-allocation.md` — Test sharding and parallelisation
- `unit-test-architecture.md` — Unit test architecture and patterns

### data-analytics (3 skills)

- `experimentation-spec.md` — Experimentation specification template and statistical design
- `metric-definition-lock.md` — Metric definition governance and Stage 3 lock process
- `incident-response.md` — Analytical sign-off on postmortems and error budget analysis

### android-engineering (12 skills)

- `android-implementation.md` — Android development fundamentals and project setup
- `android-architecture.md` — Android architecture patterns (MVVM, MVI, Clean Architecture)
- `android-accessibility.md` — Android accessibility (TalkBack, content descriptions, WCAG)
- `android-security.md` — Android security (MASVS L1/L2, EncryptedSharedPreferences, StrongBox)
- `android-testing.md` — Android testing (JUnit 5, Compose UI tests, Maestro, CI sharding)
- `offline-first-patterns.md` — Offline-first architecture, Room, WorkManager, sync strategies
- `jetpack-compose.md` — Jetpack Compose UI, state management, navigation, animations
- `kotlin-advanced.md` — Advanced Kotlin (coroutines, flows, DSLs, extension patterns)
- `bazel-build-system.md` — Bazel build system for Android monorepos
- `compose-ui,-state-management,-animations,-navigation-compose.md` — Advanced Compose patterns
- `github-actions,-gradle-enterprise,-paparazzi,-build-optimization.md` — Android CI/CD and build
- `retrofit,-okhttp,-custom-interceptors,-api-resilience.md` — Android networking and resilience

### ios-engineering (17 skills)

- `ios-implementation.md` — iOS development fundamentals and project setup
- `swiftui-architecture.md` — SwiftUI architecture (property wrappers, navigation, animations)
- `swiftui.md` — SwiftUI fundamentals, declarative UI patterns
- `uikit-architecture.md` — UIKit architecture and migration patterns
- `swift-concurrency.md` — Swift concurrency (async/await, actors, structured concurrency)
- `combine-reactive-programming.md` — Combine framework and reactive programming
- `tca-architecture.md` — The Composable Architecture (TCA) pattern
- `core-animation.md` — Core Animation, custom transitions, performance
- `ios-performance.md` — iOS performance profiling and optimisation
- `ios-networking.md` — iOS networking (URLSession, async/await, certificate pinning)
- `ios-ci-cd.md` — iOS CI/CD (Xcode Cloud, Fastlane, TestFlight)
- `ios-testing.md` — iOS testing (XCTest, XCUITest, snapshot testing)
- `swift-familiarization.md` — Swift language familiarisation for cross-platform engineers
- `core-data,-batch-fetching,-faulting,-migration.md` — Core Data persistence patterns
- `uikit,-combine-reactive-programming,-data-binding.md` — UIKit + Combine data binding
- `voiceover,-dynamic-type,-wcag-2.1-aa,-accessibility-testing.md` — iOS accessibility
- `widgetkit,-app-intents,-share-extension,-today-extension.md` — iOS extensions and widgets

### cross-platform-engineering (9 skills)

- `kmp-implementation.md` — Kotlin Multiplatform implementation fundamentals
- `kmp-architecture.md` — KMP architecture, shared modules, expect/actual
- `kmp-architecture-v2.md` — KMP architecture v2 patterns and compose multiplatform
- `kmp-shared-modules.md` — KMP shared business logic and data layers
- `flutter-implementation.md` — Flutter development fundamentals
- `cross-platform-architecture.md` — Cross-platform architecture decision framework
- `swift-familiarization.md` — Swift familiarisation for KMP engineers targeting iOS
- `flutter-component-library,-rtl-support,-material-design,-custom-painters.md` — Flutter UI and i18n
- `ktor-client,-coroutines,-shared-business-logic,-cross-platform-strategy.md` — Ktor and shared logic
- `react-native,-native-modules,-document-scanning,-biometric-auth.md` — React Native native integrations

### backend-engineering (27 skills)

- `distributed-systems.md` — Distributed systems fundamentals and patterns
- `distributed-backend-architecture.md` — Microservices design, event-driven architecture, Kubernetes
- `database-architecture.md` — Database design, normalisation, and selection
- `database-sharding.md` — Horizontal scaling, sharding strategies, consistent hashing
- `real-time-architecture.md` — Real-time systems, WebSockets, SSE, event streaming
- `backend-observability.md` — Observability, tracing, metrics, and logging for backends
- `websocket-scaling.md` — WebSocket scaling at high concurrency
- `event-sourcing.md` — Event sourcing pattern and CQRS integration
- `cqrs-architecture.md` — CQRS pattern design and implementation
- `security-patterns.md` — Backend security patterns (auth, authorisation, data protection)
- `enterprise-patterns.md` — Enterprise integration and design patterns
- `backend-chapter-leadership.md` — Backend chapter leadership and technical mentorship
- `api-gateway-design.md` — API gateway architecture and cross-cutting concerns
- `api-testing.md` — Backend API testing strategies
- `rest-api-design.md` — REST API design, OpenAPI 3.0, request validation, pagination
- `rest-api-versioning,-rollback,-multi-tenant-isolation.md` — API versioning and multi-tenancy
- `circuit-breakers-and-resilience-patterns.md` — Circuit breakers, retry logic, fallback handling
- `postgresql-basics.md` — PostgreSQL fundamentals for application developers
- `postgresql-query-optimization,-indexing,-execution-plans.md` — PostgreSQL performance tuning
- `aws-infrastructure.md` — AWS infrastructure (ECS, RDS, S3, IAM, CloudWatch, Terraform)
- `cicd-infrastructure-engineering.md` — CI/CD infrastructure engineering and pipeline design
- `fastapi,-async-python,-pydantic,-postgresql.md` — Python/FastAPI async API development
- `go-concurrency,-postgresql,-microservices,-error-handling.md` — Go backend development
- `go-microservices-development,-production-patterns.md` — Go microservices production patterns
- `apollo-server,-schema-stitching,-dataloader,-subscriptions.md` — GraphQL with Apollo Server
- `multi-tenant-data-isolation,-schema-separation,-tenant-context-management.md` — Multi-tenancy
- `full-stack-mvp.md` — Full-stack MVP delivery patterns

### frontend-engineering (17 skills)

- `react-testing.md` — React Testing Library, Jest, component and integration testing
- `react-testing-advanced.md` — Advanced React testing (MSW, snapshot, custom hooks) _(also in quality-assurance)_
- `redux-toolkit,-rtk-query,-cache-management,-optimistic-updates.md` — React state management
- `react,-python-fastapi,-multi-step-forms,-async-task-queues.md` — React + FastAPI full-stack
- `vue-3,-composition-api,-pinia,-composables.md` — Vue 3 development with Composition API
- `vue-testing.md` — Vue Test Utils and Vitest _(also in quality-assurance)_
- `vue-3,-.net-7,-entity-framework-core,-multi-tenant-architecture.md` — Vue + .NET full-stack
- `angular-spring-boot.md` — Angular + Spring Boot enterprise full-stack
- `angular-signals.md` — Angular Signals reactive state management
- `vite-build-optimization.md` — Vite build optimisation, HMR, code splitting, tree shaking
- `virtualized-rendering.md` — Virtualised rendering, infinite scroll, skeleton loading
- `ssr-nextjs.md` — Next.js SSR, ISR, app router patterns
- `design-systems.md` — Design system implementation and component library governance
- `frontend-security.md` — Frontend security (CSP, XSS, CSRF, secure storage)
- `xss-prevention.md` — XSS prevention techniques and sanitisation
- `frontend-performance-baseline.md` — Core Web Vitals, Lighthouse, performance baseline
- `frontend-performance-optimization.md` — Advanced frontend performance optimisation
- `advanced-a11y.md` — Advanced accessibility (ARIA, screen readers, keyboard navigation)
- `pwa-engineering.md` — Progressive Web App (service workers, offline, push)

### game-development (15 skills)

- `studio-leadership.md` — Studio vision, team leadership, and pipeline governance
- `creative-vision.md` — Creative vision definition, art direction oversight, GDD authorship
- `production-management.md` — Production planning, schedule management, dependency mapping
- `launch-readiness.md` — Launch readiness checklist, soft launch, global launch coordination
- `monetization-design.md` — Player-centric F2P monetisation, IAP design, event pass systems
- `game-design-vision.md` — Game design vision and concept development
- `systems-design.md` — Game systems design (progression, economy, meta)
- `economy-design.md` — Game economy design and balancing
- `f2p-economy-design.md` — Free-to-play economy design and ethical monetisation
- `player-retention.md` — Player retention mechanics and behavioural design
- `design-team-leadership.md` — Game design team leadership and mentorship
- `game-engineering-architecture.md` — Game engine architecture and technical design
- `unity-unreal-expertise.md` — Unity and Unreal Engine expertise
- `agile-production.md` — Agile production in game development contexts
- `jira-confluence.md` — Jira and Confluence for game production tracking

### audio-engineering (4 skills)

- `audio-pipeline-design.md` — Game audio pipeline design and asset management
- `fmod-wwise-integration.md` — FMOD and Wwise integration in Unity/Unreal
- `chiptune-composition.md` — Chiptune and retro-style music composition
- `interactive-music-systems.md` — Interactive and adaptive music systems

### visual-arts-and-animation (3 skills)

- `art-direction.md` — Art direction, style guides, and visual consistency
- `art-team-leadership.md` — Art team leadership and pipeline governance
- `mobile-art-pipeline.md` — Mobile-optimised art pipeline and asset delivery

### live-operations (3 skills)

- `live-ops-strategy.md` — Live operations planning, content updates, and community engagement
- `live-ops-strategy-studio-director.md` — Studio director-level live ops strategy and vision
- `community-strategy.md` — Community management strategy and player communication

### llm-engineering (4 skills)

- `llm-system-design.md` — LLM system architecture and design patterns
- `context-engineering-design.md` — Context window management and memory systems
- `multi-agent-orchestration-design.md` — Swarm orchestration and agent coordination
- `ase-compliance-audit.md` — ASE framework compliance and auditing

## Migration Notes

**Phase 1 (Complete):** 37 skills organized into 9 domains  
**Phase 2 (Complete):** 21 leadership skills added, 2 new domains (quality-assurance, data-analytics)  
**Phase 3 (Complete):** 5 specialized engineering domains extracted from general engineering
(android-engineering, ios-engineering, cross-platform-engineering, backend-engineering,
frontend-engineering); 3 new studio domains added (audio-engineering, live-operations);
product-design expanded; quality-assurance and cyberspace-security enriched  
**Total:** 235 skills across 19 domains

## Related Documentation

- **ECOSYSTEM_SPEC.md** — Full ecosystem specification
- **AGENTS.md** — Workspace agent orientation guide
- **Kiro Skills Docs** — https://kiro.dev/docs/cli/skills/

---

_This directory structure follows the Kiro Skills specification and is maintained according to
ECOSYSTEM_SPEC.md governance._
