# Web Application Pipeline — Overview

**Pipeline:** Web Application (P1)
**Full Definition:** [`pipeline.md`](../../pipeline/web-development/pipeline.md)
**Monitoring:** [`monitoring.md`](../../pipeline/web-development/monitoring.md)

---

## Platform Focus

PWA, SPA, SSR web applications with Core Web Vitals, SEO, and CDN deployment.

---

## Platform Strategy Matrix

Four mutually exclusive scenarios:

| Dimension             | Frontend-Heavy                  | Backend-Heavy                   | Full-Stack                     | Lightweight         |
| --------------------- | ------------------------------- | ------------------------------- | ------------------------------ | ------------------- |
| **Stage 3 ADR**       | SSR/CSR/PWA decision            | REST/GraphQL decision           | SSR + REST + deployment        | CSR only            |
| **Stage 5 Tracks**    | W-FE + W-FS                     | W-BE + W-FS                     | W-FE + W-BE + W-FS             | W-FE only           |
| **Stage 5 Team Size** | 8                               | 8                               | 12                             | 4                   |
| **Stage 6 Review**    | Frontend ↔ Backend cross-review | Backend ↔ Frontend cross-review | All three leads cross-review   | Frontend Lead only  |
| **Stage 7 Testing**   | FE unit + E2E + perf            | BE unit + contract + load       | Full-stack E2E + all platforms | FE unit + basic E2E |
| **Stage 10**          | Vercel deploy + CDN             | API gateway + docs              | Full deployment + docs         | Vercel deploy       |

---

## Stage-Specific Highlights

### Stage 2: Prototype + IDS

- Production-grade HTML/CSS/JS prototype at 3 breakpoints (375px, 768px, 1440px)
- Responsive IDS with CSS design tokens
- WCAG 2.1 AA compliance targets, keyboard navigation, focus management

### Stage 3: ADRs (6 total)

- `ADR-WEB-STRATEGY.md` — SSR vs CSR vs PWA (14 fields: delivery model, INP <200ms, bundle budget, SEO strategy, browser matrix, hosting platform comparison)
- `ADR-SECURITY-CRYPTO.md` — Web Crypto API, HTTPS, encrypted storage
- `ADR-SECURITY-WEB-PATTERNS.md` — XSS prevention, CSRF tokens, CSP, CORS, OAuth 2.0 session security
- `ADR-SECURITY-WEB-STORAGE.md` — Cookie security (HttpOnly, Secure, SameSite), localStorage/sessionStorage encryption, IndexedDB security
- `ADR-SECURITY-WEB-PLATFORM-PATTERNS.md` — URL routing security, service worker integrity, push notification security, PWA security, open redirect prevention, clickjacking protection, prototype pollution prevention, security headers (X-Content-Type-Options, Referrer-Policy, Permissions-Policy, HSTS)
- `ADR-STRING-KEY-TAXONOMY.md` — String key naming, `key-index.csv` operationalization

### Stage 4.1: Security Implementation Specification (SIS)

- Author: Security team (Natalia Petrova + James Wright), signed off by CSO
- Content: XSS prevention (React auto-escaping, DOMPurify), CSRF (double-submit cookie), CSP (nonce-based strict-dynamic), OAuth 2.0 (PKCE, short-lived tokens), third-party script governance (SRI hashes)
- Gate: "SIS completed and CSO-signed" required before Stage 5

### Stage 5: Development

- Three tracks: W-FE (Frontend), W-BE (Backend), W-FS (Integration + Deployment)
- Design Fidelity Checkpoint at ~60%: ≥90% pass → proceed; 70-89% → remediation; <70% → STOP
- API Contract Parity verification at 30%/70% milestones
- SEO Readiness check: meta tags, structured data, sitemap.xml, robots.txt, canonical URLs

### Stage 6: Code Review

- Live demonstration: running web app on 3 browsers (Chrome, Firefox, Safari)
- Responsive layout verification at 3 breakpoints
- Lighthouse score audit (Performance, Accessibility, SEO, Best Practices)
- **Live accessibility testing**: keyboard navigation on all critical flows, screen reader announcements verified (VoiceOver on Safari or NVDA on Firefox), focus management tested on modals/dropdowns
- Bundle verification: network tab inspected for total JS/CSS payload

### Stage 7: Testing

- OWASP WSTG manual pen testing (reflected/stored/DOM-based XSS, CSRF, SQL injection, IDOR, authentication bypass, session fixation, privilege escalation, open redirect, clickjacking)
- Playwright E2E across 3 browsers
- Lighthouse CI: LCP <2.5s, INP <200ms, CLS <0.1, TTFB <800ms, TTI <3.8s
- axe-core + manual screen reader test: WCAG 2.1 AA ≥ 95%

### Stage 8: Stealthy Weakening Examples (P0)

- Relaxed CSP, removed CSRF protection, removed HSTS, downgraded TLS version, weakened cookie SameSite attribute, disabled Subresource Integrity, relaxed CORS policy

---

## Monitoring

Three-layer architecture with web-specific fields:

- Track W-FE/W-BE/W-FS with bundle/Lighthouse/SEO build tree
- Performance SLA: LCP <2.5s, INP <200ms, CLS <0.1, TTFB <800ms, TTI <3.8s
- Checkpoint fields: `bundle_size_kb`, `lighthouse_performance/accessibility/seo`, `seo_readiness`, `cdn_configured`, `preview_deployed`
- Recovery scenarios: Vercel deployment failure, SSR hydration error, CDN cache invalidation, API contract mismatch, Lighthouse regression

---

_For complete stage definitions, gate criteria, and artifact lists, see the [full pipeline definition](../../pipeline/web-development/pipeline.md)._
