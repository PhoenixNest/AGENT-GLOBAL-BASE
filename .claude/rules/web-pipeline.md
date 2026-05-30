---
paths:
  - "**/web-development/**"
description: Web development pipeline platform-specific rules
---

# Web Development Pipeline — Platform-Specific Rules

**Applies To:** Web application development (frontend-focused)

---

## Technology Stack

- **Frontend Frameworks:** React, Vue, Angular (per ADR)
- **Styling:** CSS Modules, Tailwind CSS, Styled Components (per ADR)
- **Build Tools:** Vite, Webpack, Rollup (per ADR)
- **Testing:** Vitest, Jest, Playwright, Cypress (per ADR)

---

## Stage-Specific Web Requirements

### Stage 1 — PRD + SRD

Web PRD: browser support matrix, responsive breakpoints, PWA requirements, SEO, performance budgets (LCP/FID/CLS), WCAG 2.1 AA.

Web SRD: OWASP Top 10, CSP, CORS, auth/session management, XSS/CSRF protection.

### Stage 3 — UML Engineering Package

**ADRs required:** Frontend framework, state management, routing, styling approach, build tool.

### Stage 6 — Arch. & Conformance Review

Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1. Bundle size < 200KB initial load.

### Stage 7 — Automated Testing

Unit (Vitest/Jest), component (React Testing Library/Vue Test Utils), E2E (Playwright/Cypress), visual regression (Percy/Chromatic), accessibility (axe-core).

---

## Performance Budgets

- **LCP:** < 2.5 seconds
- **FID:** < 100ms
- **CLS:** < 0.1
- **Initial bundle:** < 200KB gzipped
- **Time to Interactive:** < 3.5 seconds

---

## Web P0 Defects (Block Release)

- Application crashes or white screen
- Data loss or corruption
- Security vulnerability (OWASP Top 10)
- Authentication bypass
- Payment processing failure
