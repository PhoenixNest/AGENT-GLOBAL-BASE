# Web Development Pipeline — Delta Overlay

| Field          | Value                                                                                                                       |
| -------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Pipeline**   | `web-development`                                                                                                           |
| **Owner**      | VP Web (Julia Thorne) + VP Web & Backend (Elena Vasquez) (joint)                                                            |
| **Surfaces**   | Browser web (Chromium / Firefox / WebKit) — selectable per-project via the 4-scenario Web Strategy Matrix below             |
| **Effective**  | 2026-04-21                                                                                                                  |
| **Supersedes** | `web-development/pipeline.md` (legacy 452-line file; back-compat redirect retained until 2026-07-21).                       |
| **Cross-Refs** | Base: [`../_base/pipeline.md`](../_base/pipeline.md) · Template: [`../_base/delta-template.md`](../_base/delta-template.md) |

> **Reading order.** This delta is consumed _alongside_ [`../_base/pipeline.md`](../_base/pipeline.md), not instead of it. The base defines the universal 12-stage state machine, defect severity, Progress Sync Protocol, gate criteria, and the Release Readiness Checklist. This delta fills the `{{DELTA: …}}` placeholders the base reserves for web-specific content. Anything in the base applies; anything contradicted by this delta IS A BUG — escalate to the Software Architect.

---

## 1. Surface / Web Strategy Matrix

### 1.1 Overview

Stage 5 development executes per the **Web Strategy Matrix**, which determines track activation based on the **Web Strategy ADR** produced at Stage 3. The Stage 1 gate asks "What type of web application?" — this confirms the **target delivery model** (SPA, SSR, PWA, full-stack web, or lightweight). The **implementation approach** (SSR vs CSR vs PWA vs hybrid) is an architecture decision locked at **Stage 3**.

**Four mutually exclusive scenarios — a project selects exactly one.**

### 1.2 Decision Matrix

| Dimension                 | Frontend-Heavy (SPA / Dashboard) | Backend-Heavy (Data Platform)   | Full-Stack (E-commerce / Social) | Lightweight (Landing Page) |
| ------------------------- | -------------------------------- | ------------------------------- | -------------------------------- | -------------------------- |
| **Stage 1 Gate**          | Web app                          | Web API                         | Web app + API                    | Web app                    |
| **Stage 3 ADR**           | SSR / CSR / PWA decision         | REST / GraphQL decision         | SSR + REST + deployment          | CSR only                   |
| **Stage 5 Active Tracks** | Track W-FE + Track W-FS          | Track W-BE + Track W-FS         | Track W-FE + W-BE + W-FS         | Track W-FE only            |
| **Stage 5 Team Size**     | 8                                | 8                               | 12                               | 4                          |
| **Stage 6 Tier 1 Review** | Frontend ↔ Backend cross-review  | Backend ↔ Frontend cross-review | All three leads cross-review     | Frontend Lead only         |
| **Stage 7 Testing**       | FE unit + E2E + perf             | BE unit + contract + load       | Full-stack E2E + all platforms   | FE unit + basic E2E        |
| **Stage 9 i18n**          | EN/ZH/JA/KO/FR strings.json      | Error message localization      | Both extracted via key-index.csv | Optional (per PRD)         |
| **Stage 10 Submission**   | Vercel deploy + CDN              | API gateway + docs              | Full deployment + docs           | Vercel deploy              |
| **CI/CD Scope**           | Frontend + deploy                | Backend + contract              | Full-stack CI/CD                 | Frontend CI only           |

### 1.3 Track Activation Protocol

| Project Type   | Track W-FE (Web Frontend) | Track W-BE (Web Backend) | Track W-FS (Full-Stack Integration) | Coordinator                      |
| -------------- | ------------------------- | ------------------------ | ----------------------------------- | -------------------------------- |
| Frontend-heavy | **FULL** (4 eng)          | **LIGHT** (2 eng)        | **LIGHT** (2 eng)                   | Elena Vasquez (VP Web & Backend) |
| Backend-heavy  | **LIGHT** (2 eng)         | **FULL** (4 eng)         | **LIGHT** (2 eng)                   | Elena Vasquez (VP Web & Backend) |
| Full-stack     | **FULL** (4 eng)          | **FULL** (4 eng)         | **PRIMARY** (4 eng)                 | Elena Vasquez + Amira Voss       |
| Lightweight    | **LIGHT** (2 eng)         | Dormant                  | **LIGHT** (2 eng)                   | Elena Vasquez (VP Web & Backend) |

**Track semantics:**

| Term        | Definition                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------- |
| **FULL**    | End-to-end feature implementation, testing, and delivery for that layer. Owns the complete codebase for that layer. |
| **LIGHT**   | Integration and adaptation only (e.g., API client integration, deployment wiring). NOT full feature implementation. |
| **PRIMARY** | Owns the shared integration layer that connects frontend and backend. Coordinates cross-layer contracts.            |
| **Dormant** | Track lead and engineers are reassigned to technical debt, test automation, cross-training, or other projects.      |

### 1.4 Track W-FE / W-BE — How Semantics Change

When the user chooses a project type that shifts track responsibility:

| Aspect         | FULL Track            | LIGHT Integration Track                        |
| -------------- | --------------------- | ---------------------------------------------- |
| Code ownership | 100% of layer code    | Integration wiring only                        |
| Feature work   | Full implementation   | Integration of other layer's APIs              |
| Team size      | 4 engineers           | 2 engineers                                    |
| Freed capacity | N/A                   | Reassigned to technical debt / test automation |
| CI/CD          | Full layer pipeline   | Integration build + contract verification      |
| Testing        | Full layer test suite | Contract tests + integration tests             |

### 1.5 Resource Reallocation Protocol

| Scenario       | Freed Resources                      | Reassignment Options                                                   |
| -------------- | ------------------------------------ | ---------------------------------------------------------------------- |
| Frontend-heavy | 2 W-BE eng, 2 W-FS eng               | Other projects, API contract tests, CI/CD hardening                    |
| Backend-heavy  | 2 W-FE eng, 2 W-FS eng               | Other projects, frontend test automation, performance profiling        |
| Full-stack     | None — all tracks active             | N/A                                                                    |
| Lightweight    | 4 W-FE eng, all W-BE eng, 2 W-FS eng | Technical debt, accessibility audit, documentation, SDK migration prep |

### 1.6 Monitoring Adaptation

`PROGRESS.md` must reflect active tracks only. Inactive tracks show "N/A," not "0%". The Progress Sync Protocol must account for reallocated resources — reassigned engineers should not penalize a project's capacity metrics.

### 1.7 Per-Scenario CI/CD Blueprint

| CI/CD Component    | Frontend-Heavy | Backend-Heavy | Full-Stack | Lightweight |
| ------------------ | -------------- | ------------- | ---------- | ----------- |
| ESLint + TSC       | ✅             | ✅ (BE only)  | ✅         | ✅          |
| Vitest unit tests  | ✅             | ✅ (BE only)  | ✅         | ✅          |
| Playwright E2E     | ✅             | ❌            | ✅         | Basic       |
| Lighthouse CI      | ✅             | ❌            | ✅         | ❌          |
| API contract tests | ✅ (consumer)  | ✅ (provider) | ✅ (both)  | ❌          |
| k6 load tests      | ❌             | ✅            | ✅         | ❌          |
| ZAP DAST           | ✅             | ✅            | ✅         | ✅          |
| Vercel deploy      | ✅             | ❌            | ✅ (FE)    | ✅          |
| API gateway deploy | ❌             | ✅            | ✅ (BE)    | ❌          |

### 1.8 Deployment & Compliance Implications (web-specific add-ons to the base ADR canon)

The Web Strategy ADR must address:

- **Deployment platform compliance** — Vercel/Netlify terms, AWS region selection, data residency requirements.
- **Cookie & privacy compliance** — GDPR cookie consent, CCPA data handling, third-party script governance.
- **Monetization implications** — Stripe / payment gateway integration, revenue share (if applicable), tax compliance.

---

## 2. Stage 1 — PRD Stewardship (web-specific)

- **PRD steward:** VP Web (Julia Thorne); CPO arbitrates if PRD scope spans web + non-web platforms.
- **Stage 1 surface question (delta-fills the base placeholder):** "What type of web application?" (SPA, SSR, PWA, hybrid, lightweight). The user's answer determines the Web Strategy Matrix scenario at Stage 3.
- **Web-specific PRD fields:** target browser support matrix (Chrome, Firefox, Safari, Edge — minimum versions); target breakpoints (mobile 375px / tablet 768px / desktop 1440px at minimum); SEO requirements (crawlability, structured data, social sharing previews); performance SLA targets (LCP, INP, CLS, TTFB, TTI); analytics platform (GA4, Segment, Amplitude); cookie / consent posture (GDPR, CCPA, IAB TCF).
- **Web-specific SRD fields (delta-fills the base placeholder):** XSS prevention strategy (auto-escaping framework, DOMPurify for rich content); CSRF token model (double-submit cookie / synchronizer token); CSP header policy (strict-dynamic, nonce-based); cookie attributes (HttpOnly, Secure, SameSite); OAuth 2.0 / OIDC session security (PKCE, short-lived tokens); third-party script supply chain (SRI hashes); data residency and region pinning.

---

## 3. Stage 2 — Prototype Variant (web-specific)

- **Prototype format (delta-fills the base placeholder):** **production-grade HTML / CSS / JS** at all three breakpoints (375px, 768px, 1440px). The web prototype is not a throwaway mock — it serves as design validation AND becomes the initial frontend scaffold for Stage 5 (carry-forward).
- **IDS surface coverage:** WCAG 2.1 AA from Stage 2 onward; responsive breakpoints; text-expansion tolerance ≥ 40% (for i18n); RTL layout mirroring rules where Arabic / Hebrew is in scope; animation specs (prefers-reduced-motion respected); design tokens (CSS custom properties + light/dark theme parity).

---

## 4. Stage 3 — Additional Mandatory ADRs (web-specific)

In addition to the universal **String Key Taxonomy ADR** and **Security Architecture ADRs** mandated by the base:

### 4.1 Web Strategy ADR (mandatory for every web project) — 14 fields

The Web Strategy ADR must include:

1. **Decision statement** — Which approach: SSR, CSR, PWA, or hybrid?
2. **Rationale** — SEO needs, performance targets, team skills, time-to-market.
3. **Trade-offs** — What is gained and sacrificed vs. alternatives.
4. **Team capability assessment** — Frontend / backend balance available?
5. **Risk analysis** — SSR complexity, bundle size, SEO risks, browser compatibility.
6. **TCO projection (24-month)** — Hosting, CDN, monitoring; total estimated cost.
7. **Vendor lock-in risk matrix** — Framework abandonment risk, migration cost, hosting platform comparison (Vercel vs. Netlify vs. self-hosted AWS / CloudFront + S3).
8. **Performance SLA alignment** — LCP < 2.5s, INP < 200ms, CLS < 0.1, TTFB < 800ms — can the chosen approach meet PRD thresholds?
9. **Accessibility mandate** — WCAG 2.1 AA from Stage 2 IDS, tested in Stage 7.
10. **STRIDE-based threat model** — XSS, CSRF, injection, session hijacking, supply-chain attacks.
11. **Track activation mapping** — Explicit reference to which tracks are FULL / LIGHT / Dormant.
12. **Reassignment plan** — Where freed engineers go.
13. **SEO strategy** — Meta tags, sitemap, structured data, SSR rendering for crawlers.
14. **Browser support matrix** — Which browsers and versions are supported.

**Ownership:** CTO authors. Frontend Lead + Backend Lead provide input. CIO reviews for technology conformance. CSO reviews for security conformance. CDO reviews for design quality impact. The ADR is versionable + supersedable per [`../_base/adr-template.md`](../_base/adr-template.md); supersession requires a documented rollback plan and triggers an Implementation-Plan re-baseline (Stage 4 re-entry minimum).

### 4.2 Web-Specific Security ADR Topics

In addition to the universal `ADR-SECURITY-CRYPTO.md`:

- `ADR-SECURITY-WEB-PATTERNS.md` — XSS prevention, CSRF tokens, CSP, CORS, OAuth 2.0 session security.
- `ADR-SECURITY-WEB-STORAGE.md` — Cookie security (HttpOnly, Secure, SameSite), localStorage / sessionStorage encryption, IndexedDB security.
- `ADR-SECURITY-WEB-PLATFORM-PATTERNS.md` — URL routing security (server-side route guards, auth-required deep links); service worker integrity (scope restriction, cache integrity, update strategy); push notification security (VAPID auth, subscription management); PWA security (manifest integrity, install prompt security, origin trials); open redirect prevention; clickjacking protection (X-Frame-Options + frame-ancestors); prototype pollution prevention; Web Share API security; File API sanitization; third-party iframe sandboxing; security headers (X-Content-Type-Options, Referrer-Policy, Permissions-Policy, HSTS).

---

## 5. Stage 4 — Pipeline-Specific Plan Sections

### 5.1 Track Activation Mapping (mandatory in every Web Coding Implementation Plan)

The Track Activation Mapping is an explicit reference to the Web Strategy ADR and activation of the corresponding track configuration (FULL / LIGHT / PRIMARY / Dormant per track per §1.3 above). Personnel assignments must reflect the active tracks.

### 5.2 Web-Specific Adapter Layer

The base mandates a "platform/surface adapter layer" in dependency mapping. For web, this is the **rendering / hydration adapter layer**: SSR rendering boundary (Next.js / Remix / SvelteKit equivalent) on the server side; hydration boundary on the client; service worker boundary for PWA scenarios; CDN edge boundary for cached assets.

### 5.3 Web-Specific Database Migration Plan (mandatory at Stage 4)

Database migration strategy with rollback procedure and zero-downtime migration plan (e.g., expand-migrate-contract pattern). Migration tooling must be specified in the TSD (Flyway / Prisma Migrate / Drizzle / Atlas). For schema-less stores, document the schema-version field convention.

---

## 6. Stage 5 — Track Execution Model (web-specific)

**Lead coordinator:** **VP Web (Julia Thorne)** for product / web-frontend tracks; **VP Web & Backend (Elena Vasquez)** for backend integration; **Frontend Lead (Amira Voss)** for Track W-FE engineering quality.

**Track execution:**

- **Track W-FE (Web Frontend):** Led by Frontend Lead (Amira Voss). FULL for frontend-heavy and full-stack scenarios; LIGHT for backend-heavy and lightweight; never dormant in any web project.
- **Track W-BE (Web Backend):** Led by Backend Lead (Dev Malhotra). FULL for backend-heavy and full-stack; LIGHT for frontend-heavy; dormant for lightweight.
- **Track W-FS (Full-Stack Integration):** Led by Elena Vasquez. PRIMARY for full-stack; LIGHT otherwise. Owns the API client / RPC layer that wires W-FE ↔ W-BE.

**Cross-layer coordination:** Contract Verification Reports produced at 30% and 70% milestones — API contract parity between frontend (consumer) and backend (provider). Pact (or equivalent consumer-driven contract testing) is the canonical tool.

**SIS scope:** Web-specific SIS authored by Security team (Natalia Petrova + James Wright), CSO-signed before Stage 5 Day 1. Translates SRD into web-specific code patterns — XSS prevention (React auto-escaping, DOMPurify for rich content), CSRF token implementation (double-submit cookie pattern), CSP header configuration (strict-dynamic, nonce-based), OAuth 2.0 session security (PKCE, short-lived tokens), dependency vulnerability response, third-party script supply chain governance (SRI hashes, subresource integrity), URL routing security, service worker integrity, push notification security, PWA security, open redirect prevention, clickjacking protection, prototype pollution prevention, security headers.

**Design Fidelity Checkpoint scope:** Frontend Lead presents working builds at 3 target breakpoints (375 / 768 / 1440) and at least 2 target browsers (Chrome + Safari at minimum) for side-by-side comparison with IDS specifications. Lighthouse scores (Performance, Accessibility, Best Practices, SEO) spot-checked at the checkpoint.

**Additional Web Stage-5 gate criteria (delta-fills the base placeholder):**

- [ ] Contract Verification Reports (Pact or equivalent) produced at 30% and 70% milestones.
- [ ] API Contract Parity Report (`API-CONTRACT-PARITY-REPORT.md`) produced before the CTO internal review checklist closes.

---

## 7. Stage 6 — Tier-1 Review Model (web-specific)

**Tier-1 cross-review pairing (delta-fills the base placeholder):**

- **Frontend-heavy:** Frontend Lead ↔ Backend Lead cross-review (FE primary, BE reviews integration boundaries).
- **Backend-heavy:** Backend Lead ↔ Frontend Lead cross-review (BE primary, FE reviews consumer wiring).
- **Full-stack:** All three Leads (Frontend, Backend, Full-Stack Integration) cross-review.
- **Lightweight:** Frontend Lead only (no cross-review required).

**Live Demonstration scope (delta-fills the base placeholder):** CDO interacts with running web application on **3 target browsers** (Chrome, Firefox, Safari at minimum). Verifies responsive layout at 3 breakpoints (375 / 768 / 1440). Spot-checks Lighthouse scores. **Live accessibility testing**: keyboard navigation exercised on all critical flows; screen-reader announcements verified on at least one critical flow (VoiceOver on Safari OR NVDA on Firefox); focus management tested on modals and dropdowns.

**Web-specific security mandate (delta-fills the base placeholder):** OWASP ASVS Level 2+ compliance for application security; OWASP Top 10 (current edition) addressed in security review.

---

## 8. Stage 7 — Platform-Specific Testing Mandates (web-specific)

Delta-fills the base's `{{DELTA: pipeline-specific Stage 7 testing mandates}}`:

- **Unit tests:** Vitest (or Jest) — coverage targets per TAD; minimum 80% on shared utility code.
- **E2E tests:** Playwright — all critical user flows (login, primary feature, checkout/conversion, logout); cross-browser run on Chromium + WebKit + Firefox.
- **Component tests:** Playwright Component Tests OR Storybook + Chromatic visual regression.
- **API contract tests:** Pact (consumer-driven) — 100% endpoint coverage from the consumer side.
- **Performance benchmarks:** LCP < 2.5s, INP < 200ms, CLS < 0.1, TTFB < 800ms, TTI < 3.8s — measured on Lighthouse CI in production-equivalent staging.
- **Accessibility audit:** WCAG 2.1 AA ≥ 95% via axe-core + manual screen-reader test on critical flows (VoiceOver on Safari + NVDA on Firefox).
- **OWASP penetration-testing track (delta-fills the base placeholder):** Manual penetration test using the **OWASP Web Security Testing Guide (WSTG)** — covers reflected / stored / DOM-based XSS, CSRF, SQL injection, IDOR, authentication bypass, session fixation, privilege escalation, open redirect, clickjacking. Zero critical / high findings is the gate.
- **DAST:** OWASP ZAP (automated) — zero critical / high findings is the gate.

**Regression testing model — device / browser / OS matrix (delta-fills the base placeholder):**

| Trigger     | Web-specific scope                                                                                                              |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Per-PR      | Playwright E2E on Chromium headless + Lighthouse CI on the build artifact.                                                      |
| Nightly E2E | Full E2E on Chromium + WebKit + Firefox, plus mobile Safari simulator (iPhone 13) + mobile Chrome emulator (Pixel 6) viewports. |

---

## 9. Stage 8 — Additional Integrity Checks (web-specific)

Delta-fills the base placeholder for additional Stage-8 product-specific integrity checks:

- **Stealthy weakening — web-specific watch-list:** weaker cipher, relaxed CSP, removed CSRF protection, removed HSTS, downgraded TLS version, weakened cookie SameSite attribute, disabled Subresource Integrity, relaxed CORS policy. Any such change since Stage 6 is classified as **P0 defect**.
- **Browser-parity check:** every PRD feature must behave identically on Chrome + Firefox + Safari at the minimum supported version. Browser-specific drift is a P1 defect.
- **Lighthouse-scores re-verified at Stage 8** against PRD targets — no regression vs. Stage 6 baseline.

---

## 10. Stage 10 — Additional Release Criteria (web-specific)

Delta-fills the base placeholder for additional Stage-10 product-specific release criteria:

- **Deployment package complete:** Vercel / Netlify / AWS deployment configuration; CDN configured; DNS pointing; SSL certificate verified; domain verified; analytics firing on production endpoints; SEO validated (sitemap.xml, robots.txt, structured data live); monitoring dashboards live (Web Vitals + error rate + LCP / INP / CLS).
- **Cookie & consent compliance:** GDPR consent banner live (where applicable); CCPA "Do Not Sell" link live (where applicable); cookie inventory matches policy.
- **Smoke tests post-deploy:** Playwright smoke suite executes against production within 5 minutes of release; on failure, automatic rollback per the rollback runbook.

---

## 11. Stage 11 — Live Ops Mandates (web-specific)

Delta-fills the base placeholder for product-specific live-ops mandates:

- **Web Vitals SLOs (rolling 7-day, p75):** LCP ≤ 2.5s; INP ≤ 200ms; CLS ≤ 0.1.
- **Error-rate SLO:** uncaught JS error rate ≤ 0.5% of sessions; 5xx rate ≤ 0.1% of requests.
- **Hosting-rejection / vendor-incident escalation playbook:** documented chain — VP Web → CTO → CPO → CEO; max 1h to first response for production-down incidents.
- **Per-deploy hold rules:** if synthetic monitoring (Lighthouse CI on production) shows a Web Vitals regression > 10% vs. baseline, deploy is rolled back automatically; on-call DRI re-enables only after triage.
- **Cookie / consent drift detection:** weekly automated scan of production cookies vs. declared inventory; drift opens a P1 ticket.

---

## 12. Cross-Cutting i18n Requirements

i18n is a continuous concern from Stage 2 onward. Web-specific application:

| Stage   | Web i18n requirement                                                                                                                                                                                                                                                              |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 1 | PRD declares target locales explicitly; locale list locked; URL strategy decided (path-based `/zh/`, subdomain, or accept-language).                                                                                                                                              |
| Stage 2 | Pseudo-localized strings injected into the HTML prototype; IDS includes RTL layout mirroring rules for Arabic / Hebrew if in scope; text-expansion tolerance ≥ 40%.                                                                                                               |
| Stage 3 | String Key Taxonomy ADR uses the canonical `{feature}.{screen}.{component}.{property}` shape; `key-index.csv` cross-platform parity scheme defined for projects that share strings with mobile / API.                                                                             |
| Stage 5 | Locale-aware components from first commit. Zero-hardcoded-strings rule enforced by CI on every PR (e.g., ESLint rule + grep gate). Date / number / currency formatted via `Intl` API; never hand-rolled.                                                                          |
| Stage 7 | Pseudo-locale screenshot regression on every PR (Playwright + visual diff). Locale-coverage tests on the nightly E2E job (each target locale renders critical flows without truncation / overflow / RTL bugs).                                                                    |
| Stage 9 | Translation accuracy only (i18n engineering already complete). CTO-L issues Translation Verification Report (BLEU ≥ 0.80; placeholder integrity verified; text-expansion tolerance verified at ≤ 40%; accessibility labels — ARIA, alt text, screen-reader content — translated). |

---

## 13. Document Version History

| Version | Date           | Author                               | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------- | -------------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.1     | April 21, 2026 | Software Architect + VP Web + VP W&B | Initial overlay. Web-specific content (4-scenario Web Strategy Matrix, Track W-FE / W-BE / W-FS activation, per-scenario CI/CD blueprint, Web Strategy ADR 14-field requirement, web-specific Stage 1/2/3/4/5/6/7/8/10/11 sections, cross-cutting i18n table) extracted from the legacy `web-development/pipeline.md` (452 lines). Pairs with [`../_base/pipeline.md`](../_base/pipeline.md) to produce a derived view equivalent to the legacy file. |
