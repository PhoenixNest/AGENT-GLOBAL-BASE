# Full-Stack Cross-Platform Pipeline — Overview

**Pipeline:** Full-Stack Cross-Platform (P3)
**Full Definition:** [`pipeline.md`](../../pipeline/full-stack/pipeline.md)
**Monitoring:** [`monitoring.md`](../../pipeline/full-stack/monitoring.md)

---

## Platform Focus

Coordinated delivery across web + mobile + backend as a unified product with enforced feature parity (≥95% across all platforms).

---

## Platform Strategy Matrix

Three mutually exclusive scenarios:

| Dimension             | Full Product (Web + Mobile + API) | Web + API Only              | Mobile + API Only               |
| --------------------- | --------------------------------- | --------------------------- | ------------------------------- |
| **Stage 3 ADR**       | Multi-platform (all 3)            | Web + backend               | Mobile + backend                |
| **Stage 5 Tracks**    | FS-WFE + FS-WBE + FS-MOB + FS-INT | FS-WFE + FS-WBE + FS-INT    | FS-MOB + FS-WBE + FS-INT        |
| **Stage 5 Team Size** | 17–23                             | 9                           | 12–18                           |
| **Stage 6 Review**    | All leads cross-review            | Web ↔ Backend               | Mobile ↔ Backend                |
| **Stage 7 Testing**   | All platform tests + parity       | Web + backend E2E           | Mobile + backend E2E            |
| **Stage 10**          | All platforms simultaneously      | Web deployed + backend live | Mobile submitted + backend live |

---

## Stage-Specific Highlights

### Stage 2: Cross-Platform Prototype + IDS

- Web prototype at 3 breakpoints (375px, 768px, 1440px)
- **Mid-fidelity iOS wireframes** (critical screens, key flows, platform-specific navigation)
- **Mid-fidelity Android wireframes** (critical screens, key flows, platform-specific navigation)
- API specification (OpenAPI/Swagger or GraphQL SDL) with sample responses
- Developer portal low-fidelity prototype
- Cross-Platform IDS with **design token compatibility matrix** (CSS custom properties → iOS UIColor → Android ColorRes mapping)
- Platform-specific accessibility specs (Web: WCAG 2.1 AA + screen reader; iOS: VoiceOver + Dynamic Type + switch access; Android: TalkBack + font scaling)

### Stage 3: ADRs (13 total)

- `ADR-MULTI-PLATFORM-STRATEGY.md` — Which platforms, per-platform strategy, release coordination (16 fields including shared state synchronization)
- `ADR-API-STRATEGY.md` — REST vs GraphQL vs gRPC, data consistency, versioning (inherited from Backend, adapted for cross-platform)
- `ADR-OBSERVABILITY.md` — Distributed tracing across all platforms (OpenTelemetry), structured logging, per-platform SLO error budgets, cross-platform trace correlation
- `ADR-DATABASE.md` — SQL vs NoSQL, migration tooling, connection pooling, database as shared state across all platforms
- `ADR-FEATURE-FLAGS.md` — Unified flag strategy (LaunchDarkly/Unleash), per-platform flag synchronization, kill switch protocol, staggered rollout, environment parity
- `ADR-API-CLIENT-GENERATION.md` — OpenAPI Generator vs Swagger Codegen vs manual, SDK consistency across web/iOS/Android, version synchronization, breaking change detection
- `ADR-DESIGN-TOKEN-PIPELINE.md` — Style Dictionary/Figma Tokens, versioning, drift detection, per-platform mapping (CSS → iOS UIColor → Android ColorRes)
- `ADR-SECURITY-CRYPTO.md` — Per-platform: Web Crypto API, iOS CryptoKit/Keychain, Android Keystore
- `ADR-SECURITY-WEB-PATTERNS.md` — XSS, CSRF, CSP, CORS, OAuth 2.0, SRI
- `ADR-SECURITY-MOBILE-PATTERNS.md` — Certificate pinning, secure storage, root/jailbreak detection, App Attest/Play Integrity
- `ADR-SECURITY-CROSS-PLATFORM.md` — Unified auth with cross-platform session management, token revocation propagation, cross-platform data protection
- `ADR-STRING-KEY-TAXONOMY.md` — Unified across all platforms
- `ADR-ACCESSIBILITY.md` — Per-platform: Web WCAG 2.1 AA + screen reader, iOS VoiceOver + Dynamic Type, Android TalkBack + font scaling, developer portal WCAG 2.1 AA

### Stage 4.1: Cross-Platform Security Implementation Specification (SIS)

- Four domains: (1) Web: XSS, CSRF, CSP, cookie security, SRI; (2) Mobile: certificate pinning, secure storage, root/jailbreak detection, App Attest/Play Integrity; (3) Backend: rate limiting, input validation, authZ, encrypted DB, TLS 1.3; (4) Cross-platform: unified auth with cross-platform session management, token revocation propagation, data sync security guarantees, API contract security verification, shared threat model

### Stage 5: Development

- Design Fidelity Checkpoint at ~60% **across all platforms**: ≥90% pass rate **per platform** (not aggregate) to proceed; 70-89% on any platform → remediation; <70% on any platform → STOP
- Cross-Platform Contract Report: API parity verified across all platforms
- String Extraction Readiness: unified key-index.csv parity across all platforms

### Stage 6: Code Review

- **Cross-Platform Live Demonstration**: CDO interacts with critical user flows on each platform (web on staging URL, iOS on simulator/device, Android on emulator/device, backend API on staging endpoint)
- Same feature exercised sequentially on each platform — behavior compared, visual differences documented
- Responsive/adaptive check: web at 3 breakpoints, mobile on 2 screen sizes per platform, backend API schema conformance
- Cross-Platform Conformance Matrix ≥ 95%

### Stage 7: Testing

- **Multi-layer pen testing**: OWASP ZAP (web + backend) + MASVS (mobile) + OWASP WSTG (web manual) + OWASP API Security Top 10 (backend manual)
- Cross-platform E2E: same user journey on web + mobile via Playwright + Maestro
- Parity test: feature parity ≥ 95% across all platforms
- Accessibility audit per platform: web (axe-core + screen reader), iOS (VoiceOver manual), Android (TalkBack manual), backend (developer portal screen reader)

### Stage 8: Stealthy Weakening Examples (P0)

- **Web:** relaxed CSP, removed CSRF, weakened cookies, downgraded TLS
- **Mobile:** removed certificate pinning, disabled root/jailbreak detection, weakened Keychain/Keystore encryption
- **Backend:** removed rate limiting, relaxed authZ, expanded CORS, disabled audit logging
- **Cross-platform:** inconsistent auth enforcement across platforms, weaker security on one platform vs. others (**attacker pivots to weakest platform**)
- Platform divergence (features differ) classified as **P1** until parity restored

---

## Monitoring

Three-layer architecture with full-stack-specific fields:

- 4-track dependency graph (FS-WFE, FS-WBE, FS-MOB, FS-INT) + platform parity status
- Performance SLA: per-platform (web: LCP/CLS; mobile: cold start/fps; backend: P99/uptime)
- Parity status: feature parity ≥ 95% tracked in real-time via Parity CI
- Checkpoint fields: `web_deployed`, `ios_submitted`, `android_submitted`, `backend_live`, `feature_parity_pct`, `web_lighthouse_performance`, `mobile_cold_start_ms`, `backend_p99_ms`, `shared_api_contract_pass`, `cross_platform_e2e_pass`, `release_coordination_status`
- Recovery scenarios: platform divergence, API version mismatch, auth flow inconsistency, release timing mismatch, CDN propagation delay

---

_For complete stage definitions, gate criteria, and artifact lists, see the [full pipeline definition](../../pipeline/full-stack/pipeline.md)._
