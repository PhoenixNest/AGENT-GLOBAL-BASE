# ADR: Web Strategy

| Field         | Value                                          |
| ------------- | ---------------------------------------------- | --- | --- | ------- |
| **Status**    | Proposed                                       |
| **Context**   | Stage 3 — Web Application Pipeline             |
| **Decision**  | [SSR                                           | CSR | PWA | Hybrid] |
| **Date**      | YYYY-MM-DD                                     |
| **Authors**   | CTO (primary), Frontend Lead, Backend Lead     |
| **Reviewers** | CIO (technology), CSO (security), CDO (design) |

---

## Decision

[State the chosen approach: SSR, CSR, PWA, or hybrid. Include specific technology selections.]

## Rationale

[SEO needs, performance targets, team skills, time-to-market considerations.]

## Trade-offs

| Approach Considered | What's Gained | What's Sacrificed |
| ------------------- | ------------- | ----------------- |
| [Alternative 1]     | [Benefit]     | [Drawback]        |
| [Alternative 2]     | [Benefit]     | [Drawback]        |

## Team Capability Assessment

[Do we have the right frontend/backend balance? Skills gaps? Training needs?]

## Risk Analysis

| Risk                  | Likelihood     | Impact         | Mitigation        |
| --------------------- | -------------- | -------------- | ----------------- |
| SSR complexity        | [Low/Med/High] | [Low/Med/High] | [Mitigation plan] |
| Bundle size           | [Low/Med/High] | [Low/Med/High] | [Mitigation plan] |
| Browser compatibility | [Low/Med/High] | [Low/Med/High] | [Mitigation plan] |

## TCO Projection (24-Month)

| Cost Category     | Estimated Cost   |
| ----------------- | ---------------- |
| Hosting           | $X,XXX/month     |
| CDN               | $X,XXX/month     |
| Monitoring        | $XXX/month       |
| Developer tooling | $XXX/month       |
| **Total**         | **$XX,XXX/year** |

## Vendor Lock-In Risk Matrix

| Vendor/Dependency  | Abandonment Risk | Migration Cost | Exit Strategy |
| ------------------ | ---------------- | -------------- | ------------- |
| [Hosting platform] | [Low/Med/High]   | [$ estimate]   | [Plan]        |
| [Framework]        | [Low/Med/High]   | [$ estimate]   | [Plan]        |

## Performance SLA Alignment

| Metric | Target | Approach Can Meet? | Evidence    |
| ------ | ------ | ------------------ | ----------- |
| LCP    | <2.5s  | [Yes/No]           | [Benchmark] |
| FID    | <100ms | [Yes/No]           | [Benchmark] |
| CLS    | <0.1   | [Yes/No]           | [Benchmark] |
| TTFB   | <800ms | [Yes/No]           | [Benchmark] |

## Accessibility Mandate

WCAG 2.1 AA compliance from Stage 2 IDS. Tested in Stage 7 with axe-core + manual audit (≥95% pass rate target).

## STRIDE Threat Model

| Threat                 | Web-Specific Attack Vector | Mitigation                            |
| ---------------------- | -------------------------- | ------------------------------------- |
| Spoofing               | Phishing, fake login pages | OAuth 2.0, MFA, anti-phishing headers |
| Tampering              | XSS, DOM manipulation      | CSP headers, input sanitization       |
| Repudiation            | Session hijacking          | Secure cookies, token rotation        |
| Information Disclosure | Data exposure via API      | AuthZ enforcement, rate limiting      |
| Denial of Service      | DDoS, resource exhaustion  | CDN DDoS protection, rate limits      |
| Elevation of Privilege | Role manipulation          | Server-side authZ validation          |

## Track Activation Mapping

| Track               | Status               | Engineers | Scope   |
| ------------------- | -------------------- | --------- | ------- |
| W-FE (Web Frontend) | [FULL/LIGHT]         | [N] eng   | [Scope] |
| W-BE (Web Backend)  | [FULL/LIGHT/Dormant] | [N] eng   | [Scope] |
| W-FS (Integration)  | [PRIMARY/LIGHT]      | [N] eng   | [Scope] |

## Reassignment Plan

[If tracks are dormant or light, where do freed engineers go?]

## SEO Strategy

- Meta tags: [description, og:tags, twitter:cards]
- Structured data: [JSON-LD schema types]
- Sitemap: [auto-generated / manual]
- SSR rendering for crawlers: [Yes/No — if CSR, how?]

## Browser Support Matrix

| Browser | Minimum Version | Testing Approach    |
| ------- | --------------- | ------------------- |
| Chrome  | [N]             | Playwright          |
| Firefox | [N]             | Playwright          |
| Safari  | [N]             | Playwright (WebKit) |
| Edge    | [N]             | Playwright          |

---

**Lock-down:** Once approved at Stage 3 gate, this decision is locked — switching between strategies requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.
