# Technology Selection Document (TSD)

**Project:** [Project Name]
**Version:** v1
**Date:** YYYY-MM-DD
**Pipeline:** Web Application (P1)
**Stage:** 3 — Architecture

---

## 1. Technology Decisions

| Layer              | Selected                    | Rationale                                           | Alternatives Considered                                                              |
| ------------------ | --------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Frontend framework | [React + Next.js]           | SSR support, ecosystem, team skills                 | Vue 3 + Nuxt (strong alternative), SvelteKit (emerging)                              |
| Styling            | [Tailwind CSS]              | Design token integration, utility-first, responsive | CSS Modules (less flexible), styled-components (runtime overhead)                    |
| State management   | [Zustand / React Context]   | Lightweight, no boilerplate                         | Redux (too heavy for this project), Jotai (atomic, but less mature)                  |
| Backend runtime    | [Node.js + TypeScript]      | Shared language with frontend, ecosystem            | Python FastAPI (strong alternative for data-heavy), Go (overkill for this project)   |
| API framework      | [REST + Express/Fastify]    | Simplicity, cacheability, tooling                   | GraphQL (overkill for this project), gRPC (not browser-native)                       |
| Database           | PostgreSQL                  | ACID, JSON support, ecosystem                       | MongoDB (schema flexibility but weaker transactions), MySQL (less advanced features) |
| ORM/Query builder  | [Prisma / Kysely]           | Type safety, migration tooling                      | raw SQL (too error-prone), Sequelize (legacy API)                                    |
| Authentication     | [NextAuth.js / OAuth 2.0]   | Built-in Next.js integration, multi-provider        | Custom auth (security risk), Auth0 (vendor lock-in)                                  |
| Hosting (frontend) | Vercel                      | Zero-config Next.js deployment, CDN, edge functions | Netlify (strong alternative), AWS CloudFront (more complex)                          |
| Hosting (backend)  | [AWS / Render]              | Managed PostgreSQL, auto-scaling                    | Heroku (simpler but more expensive), DigitalOcean (less ecosystem)                   |
| CI/CD              | GitHub Actions              | Integrated with code hosting, free for open source  | GitLab CI (strong alternative), Jenkins (too complex)                                |
| Monitoring         | [Sentry + Vercel Analytics] | Error tracking + performance, integrated            | Datadog (more comprehensive but expensive), New Relic (enterprise-focused)           |

---

## 2. Weighted Scorecard

| Criterion            | Weight   | [Selected] | [Alternative 1] | [Alternative 2] |
| -------------------- | -------- | ---------- | --------------- | --------------- |
| Team skills fit      | 25%      | 9/10       | 7/10            | 6/10            |
| Performance          | 20%      | 8/10       | 8/10            | 9/10            |
| Ecosystem/maturity   | 15%      | 9/10       | 7/10            | 6/10            |
| Developer experience | 15%      | 9/10       | 8/10            | 7/10            |
| Cost (24-month TCO)  | 10%      | 8/10       | 7/10            | 9/10            |
| Security posture     | 10%      | 9/10       | 8/10            | 7/10            |
| Scalability          | 5%       | 8/10       | 7/10            | 9/10            |
| **Weighted Score**   | **100%** | **8.6/10** | **7.5/10**      | **6.9/10**      |

---

## 3. Vendor Risk Scoring

| Vendor | Lock-In Risk (1-5) | Migration Cost (1-5) | Open-Source Risk (1-5) | Overall Risk | Exit Strategy                                           |
| ------ | ------------------ | -------------------- | ---------------------- | ------------ | ------------------------------------------------------- |
| Vercel | 3                  | 3                    | 1                      | **Medium**   | Next.js can deploy to any platform; standard output     |
| AWS    | 4                  | 4                    | 1                      | **High**     | Abstract cloud-specific services; use Terraform for IaC |
| Sentry | 2                  | 2                    | 1                      | **Low**      | Standard error format; can switch to alternative        |

---

## 4. i18n Technology Stack

| Layer             | Technology                                               | Purpose                                    |
| ----------------- | -------------------------------------------------------- | ------------------------------------------ |
| String key format | `{feature}.{screen}.{component}.{property}` dot-notation | Consistent naming convention               |
| Resource format   | JSON (`locales/{lang}/messages.json`)                    | Native JSON support in JS ecosystem        |
| i18n library      | [i18next / react-intl / vue-i18n]                        | Framework-specific i18n integration        |
| Pluralisation     | ICU Message Format                                       | Industry standard for complex plural rules |
| Key index         | `key-index.csv`                                          | Cross-platform string parity tracking      |

---

## 5. CI/CD Technology Stack

| Component       | Technology                      | Runner Type | Purpose                                      |
| --------------- | ------------------------------- | ----------- | -------------------------------------------- |
| Frontend CI     | ESLint + TSC + Vitest           | Linux       | Lint, type-check, unit test                  |
| Backend CI      | ESLint + TSC + Vitest + Docker  | Linux       | Lint, type-check, unit test, container build |
| E2E CI          | Playwright                      | Linux       | Cross-browser E2E tests                      |
| Performance CI  | Lighthouse CI                   | Linux       | Core Web Vitals regression                   |
| Security CI     | Semgrep + npm audit + OWASP ZAP | Linux       | SAST, dependency audit, DAST                 |
| Frontend deploy | Vercel CLI                      | Vercel Edge | Preview + production deploy                  |
| Backend deploy  | [AWS CLI / Render CLI]          | Linux       | Container/image deployment                   |

---

## 6. Test Technology Stack

| Layer           | Framework               | Purpose                            | Coverage Target                |
| --------------- | ----------------------- | ---------------------------------- | ------------------------------ |
| Unit (Frontend) | Vitest + RTL            | Components, hooks, utilities       | ≥80% branch, ≥90% line         |
| Unit (Backend)  | Vitest / Jest           | API routes, services, middleware   | ≥80% branch, ≥90% line         |
| Integration     | Vitest + Docker-compose | API with real DB                   | All endpoints                  |
| E2E             | Playwright              | Critical user flows, cross-browser | All critical flows             |
| API Contract    | Pact                    | Consumer-provider contracts        | 100% endpoints                 |
| Performance     | Lighthouse CI           | Core Web Vitals                    | LCP <2.5s, CLS <0.1, TTI <3.8s |
| Accessibility   | axe-core + manual       | WCAG 2.1 AA                        | ≥95% pass rate                 |
| Security        | OWASP ZAP + Semgrep     | OWASP Top 10                       | Zero critical/high             |

---

## 7. Technology Radar

| Category         | Adopt          | Trial     | Assess    | Hold          |
| ---------------- | -------------- | --------- | --------- | ------------- |
| SSR frameworks   | Next.js        | —         | SvelteKit | —             |
| Styling          | Tailwind CSS   | CSS-in-JS | —         | Inline styles |
| State management | Zustand        | —         | Jotai     | Redux         |
| Backend runtime  | Node.js + TS   | —         | Bun       | —             |
| Database         | PostgreSQL     | —         | —         | MongoDB       |
| CI/CD            | GitHub Actions | —         | —         | Jenkins       |
| Monitoring       | Sentry         | —         | Datadog   | —             |

---

**Technology Radar updated:** YYYY-MM-DD (Quarterly review)

---

## Sign-Off

| Role          | Name | Signature | Date       |
| ------------- | ---- | --------- | ---------- |
| CTO           |      |           | YYYY-MM-DD |
| CIO           |      |           | YYYY-MM-DD |
| Frontend Lead |      |           | YYYY-MM-DD |
| Backend Lead  |      |           | YYYY-MM-DD |
