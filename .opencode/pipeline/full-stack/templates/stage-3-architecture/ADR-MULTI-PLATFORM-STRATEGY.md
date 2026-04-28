# ADR: Multi-Platform Strategy

| Field         | Value                                                         |
| ------------- | ------------------------------------------------------------- | ------------- | --------- | ----- |
| **Status**    | Proposed                                                      |
| **Context**   | Stage 3 — Full-Stack Cross-Platform Pipeline (P3)             |
| **Decision**  | [Web + iOS + Android                                          | Web + Android | iOS + API | etc.] |
| **Date**      | YYYY-MM-DD                                                    |
| **Authors**   | CTO (primary), All Platform Leads (Frontend, Backend, Mobile) |
| **Reviewers** | CIO (technology), CSO (security), CDO (design)                |

---

## Decision

[State which platforms are targeted and how they interoperate.]

## Platform Selection

| Platform | Approach             | Justification |
| -------- | -------------------- | ------------- |
| Web      | [SSR/CSR/PWA]        | [Reason]      |
| iOS      | [Native/KMP/Flutter] | [Reason]      |
| Android  | [Native/KMP/Flutter] | [Reason]      |
| Backend  | [REST/GraphQL/gRPC]  | [Reason]      |

## Web Approach

[SSR vs CSR vs PWA — same as Web Strategy ADR]

## Mobile Approach

[Native vs KMP vs Flutter — same as Platform Strategy ADR]

## Backend Approach

[REST vs GraphQL vs gRPC — same as API Strategy ADR]

## Integration Pattern

[How do platforms communicate? Shared API? Event-driven? Direct database?]

## Rationale

[Market needs, team skills, time-to-market.]

## Trade-offs

| Approach Considered | What's Gained | What's Sacrificed |
| ------------------- | ------------- | ----------------- |
| [Alternative 1]     | [Benefit]     | [Drawback]        |
| [Alternative 2]     | [Benefit]     | [Drawback]        |

## Team Capability Assessment

[Do we have the right cross-platform skills? All leads available?]

## Risk Analysis

| Risk                    | Likelihood | Impact | Mitigation                                       |
| ----------------------- | ---------- | ------ | ------------------------------------------------ |
| Coordination overhead   | High       | Medium | Single integration owner, clear release timeline |
| Platform divergence     | High       | High   | Parity CI, Stage 8 parity check                  |
| Release timing mismatch | Medium     | Medium | Staggered release plan (field #16)               |

## TCO Projection (24-Month)

| Platform  | Estimated Cost | Total             |
| --------- | -------------- | ----------------- |
| Web       | $XX,XXX/year   |                   |
| Mobile    | $XX,XXX/year   |                   |
| Backend   | $XX,XXX/year   |                   |
| **Total** |                | **$XXX,XXX/year** |

## Vendor Lock-In Risk Matrix

| Vendor/Dependency | Platform | Abandonment Risk | Migration Cost | Exit Strategy |
| ----------------- | -------- | ---------------- | -------------- | ------------- |
| [Hosting]         | Web      | [Low/Med/High]   | [$]            | [Plan]        |
| [Framework]       | Mobile   | [Low/Med/High]   | [$]            | [Plan]        |
| [Infrastructure]  | Backend  | [Low/Med/High]   | [$]            | [Plan]        |

## Performance SLA Alignment (Per-Platform)

| Platform | Metric     | Target | Can Meet? |
| -------- | ---------- | ------ | --------- |
| Web      | LCP        | <2.5s  | [Yes/No]  |
| iOS      | Cold Start | <2s    | [Yes/No]  |
| Android  | Cold Start | <2s    | [Yes/No]  |
| Backend  | P99        | <200ms | [Yes/No]  |

## Security Mandate

Unified auth flow, cross-platform data protection, platform-specific hardening (mobile: Keystore/Keychain; web: CSP/XSS; backend: rate limiting/injection).

## STRIDE Threat Model (Cross-Platform)

| Threat                 | Cross-Platform Attack Vector | Mitigation                            |
| ---------------------- | ---------------------------- | ------------------------------------- |
| Spoofing               | Token reuse across platforms | Platform-specific token scopes        |
| Tampering              | Inconsistent validation      | Shared validation library             |
| Information Disclosure | Data sync exposure           | Encrypted sync, field-level filtering |
| Elevation of Privilege | Role inconsistency           | Centralized authZ service             |

## Track Activation Mapping

| Track                 | Status               | Engineers | Scope   |
| --------------------- | -------------------- | --------- | ------- |
| FS-WFE (Web Frontend) | [FULL/LIGHT]         | [N] eng   | [Scope] |
| FS-WBE (Web Backend)  | [FULL/LIGHT/Dormant] | [N] eng   | [Scope] |
| FS-MOB (Mobile)       | [FULL/LIGHT/Dormant] | [N] eng   | [Scope] |
| FS-INT (Integration)  | [FULL/LIGHT]         | [N] eng   | [Scope] |

## Reassignment Plan

[If tracks are dormant or light, where do freed engineers go?]

## Release Coordination

- **Launch strategy:** [Staggered (which platform first?) / Simultaneous]
- **Dependency chain:** [Backend → Web → Mobile, or other]
- **Rollback plan:** [Per-platform rollback if one fails]

---

**Lock-down:** Once approved at Stage 3 gate, this decision is locked — switching platform combinations requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.
