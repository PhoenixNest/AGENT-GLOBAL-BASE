---
inclusion: fileMatch
fileMatchPattern: "**/web-development/**"
---

# Web Development Pipeline — Platform-Specific Rules

**Authority:** AGENTS.md § 4.4 + `company/pipeline/web-development/pipeline.md`  
**Applies To:** Web application development (frontend-focused)

---

## Web Pipeline Overview

The web development pipeline follows the standard 13-stage company pipeline with web-specific requirements and deliverables.

## Technology Stack

- **Frontend Frameworks:** React, Vue, Angular (per ADR)
- **Styling:** CSS Modules, Tailwind CSS, Styled Components (per ADR)
- **Build Tools:** Vite, Webpack, Rollup (per ADR)
- **Testing:** Vitest, Jest, Playwright, Cypress (per ADR)

## Stage-Specific Web Requirements

### Stage 1: Requirements → PRD + SRD

**Web-Specific PRD Sections:**

- Browser support matrix (Chrome, Firefox, Safari, Edge)
- Responsive breakpoints (mobile, tablet, desktop)
- Progressive Web App (PWA) requirements
- SEO requirements
- Performance budgets (LCP, FID, CLS)
- Accessibility requirements (WCAG 2.1 Level AA)

**Web-Specific SRD Sections:**

- OWASP Top 10 compliance
- Content Security Policy (CSP)
- Cross-Origin Resource Sharing (CORS)
- Authentication and session management
- XSS and CSRF protection

### Stage 2: PRD → Web Prototype + IDS

**Web Design Requirements:**

- Responsive design system
- Component library specification
- Interaction states (hover, focus, active, disabled)
- Loading states and skeleton screens
- Error states and empty states
- Accessibility annotations (ARIA labels, roles)

### Stage 3: Prototype → UML Engineering Package

**Web Architecture Decisions:**

- **ADR Required:** Frontend framework (React, Vue, Angular)
- **ADR Required:** State management (Redux, Zustand, Pinia, NgRx)
- **ADR Required:** Routing library
- **ADR Required:** Styling approach (CSS Modules, Tailwind, Styled Components)
- **ADR Required:** Build tool (Vite, Webpack, Rollup)
- **TSD Required:** Complete technology stack justification

**Web-Specific UML:**

- Component hierarchy diagram
- State management flow diagram
- Routing architecture diagram
- API integration diagram

### Stage 4: UML → Implementation Plan + Gantt

**Web-Specific Tasks:**

- Project scaffolding and build configuration
- Component library setup
- Routing configuration
- State management setup
- API client configuration
- CI/CD pipeline setup (Vercel, Netlify, GitHub Actions)

### Stage 5: Plan → Software Development

**Web Development Standards:**

- Follow framework-specific best practices
- Implement proper component composition
- Use semantic HTML
- Implement proper error boundaries
- Support keyboard navigation
- Implement proper loading states

### Stage 6: Development → Arch. & Conformance Review

**Web-Specific Review Criteria:**

- Core Web Vitals compliance (LCP < 2.5s, FID < 100ms, CLS < 0.1)
- Lighthouse score (Performance, Accessibility, Best Practices, SEO)
- Bundle size optimization (< 200KB initial load)
- Code splitting and lazy loading
- Browser compatibility testing
- Accessibility compliance (WCAG 2.1 Level AA)

### Stage 7: Arch. Review → Automated Testing

**Web Testing Requirements:**

- Unit tests (minimum 80% coverage)
- Component tests (React Testing Library, Vue Test Utils)
- Integration tests (API mocking)
- E2E tests (Playwright, Cypress) for critical user flows
- Visual regression tests (Percy, Chromatic)
- Accessibility tests (axe-core, jest-axe)

**Testing Frameworks:**

- **Unit/Component:** Vitest, Jest, React Testing Library, Vue Test Utils
- **E2E:** Playwright, Cypress
- **Visual:** Percy, Chromatic
- **Accessibility:** axe-core, jest-axe

### Stage 8: Testing → Integrity Verification

**Web-Specific Integrity Checks:**

- OWASP Top 10 compliance verification
- Content Security Policy (CSP) validation
- Subresource Integrity (SRI) for CDN resources
- HTTPS enforcement
- Secure cookie configuration
- Authentication token security

### Stage 9: Integrity Verification → Translation Production

**Web Localization:**

- i18n library integration (react-i18next, vue-i18n, @angular/localize)
- Translation key extraction
- RTL layout support
- Locale-specific formatting (dates, numbers, currency)
- Language switcher implementation

### Stage 10: Translation Production → Release Readiness Check

**Web Release Checklist:**

- Production build optimization
- Environment variables configured
- CDN configuration
- Caching strategy implemented
- Error tracking configured (Sentry, Rollbar)
- Analytics configured (Google Analytics, Mixpanel)
- SEO metadata complete (Open Graph, Twitter Cards)

### Stage 11: Live Operations

**Web Live Ops:**

- Core Web Vitals monitoring
- Error rate monitoring (< 1% error rate)
- Performance monitoring (Real User Monitoring)
- A/B testing and feature flags
- SEO performance tracking
- User feedback collection

## Web-Specific Technology Lock Rules

**Locked at Stage 3:**

- Frontend framework (React, Vue, Angular)
- State management library
- Styling approach
- Build tool
- Routing library
- Testing frameworks

**Cannot be changed after Stage 3 approval without full re-entry.**

## Web-Specific Defect Severity

**P0 (Blocks Release):**

- Application crashes or white screen
- Data loss or corruption
- Security vulnerability (OWASP Top 10)
- Authentication bypass
- Payment processing failure

**P1 (Blocks Release):**

- Core feature non-functional
- Navigation broken
- Critical UI rendering issue
- Form submission failure
- API integration failure

## Performance Budgets

**Core Web Vitals Targets:**

- **LCP (Largest Contentful Paint):** < 2.5 seconds
- **FID (First Input Delay):** < 100 milliseconds
- **CLS (Cumulative Layout Shift):** < 0.1

**Bundle Size Targets:**

- Initial bundle: < 200KB (gzipped)
- Total page weight: < 1MB
- Time to Interactive: < 3.5 seconds

## Accessibility Requirements

**WCAG 2.1 Level AA Compliance:**

- Keyboard navigation support
- Screen reader compatibility
- Sufficient color contrast (4.5:1 for normal text)
- Focus indicators
- ARIA labels and roles
- Skip navigation links

## Related Steering Files

- `company-pipeline-overview.md` — Core 13-stage pipeline
- `frontend-architecture.md` — Frontend patterns (manual)
- `frontend-engineering.md` — Frontend engineering domain skill
