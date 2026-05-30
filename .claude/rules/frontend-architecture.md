---
description: Frontend/Web architecture patterns — invoke manually when designing web UI
---

# Frontend Architecture

Frontend and web development patterns. See `.claude/skills/frontend-engineering/` for deep sub-skills.

---

## Component Architecture

- **Atomic Design:** Atoms → Molecules → Organisms → Templates → Pages
- **Props vs State:** Props for data flow, state for local component state
- **Controlled Components:** Parent controls component state

## State Management

- **React:** useState/useReducer (local), Redux/Zustand (global), React Query (server)
- **Vue:** ref/reactive (local), Pinia (global)
- **Angular:** Services (singleton), RxJS/NgRx

## Performance Optimization

- Code splitting with dynamic imports
- Tree shaking to remove unused code
- Image optimization: WebP, lazy loading
- Memoization: `React.memo`, `useMemo`, `useCallback`
- Web Vitals: monitor LCP, FID, CLS

## Accessibility (WCAG 2.1 AA)

- Semantic HTML, ARIA labels
- Keyboard navigation (tab, enter, escape)
- Color contrast: 4.5:1 minimum
- Screen reader testing (NVDA, JAWS, VoiceOver)

## Security

- XSS: sanitize user input, use framework escaping
- CSRF: tokens on state-changing requests
- CSP: restrict resource loading
- Secure storage: httpOnly cookies for sensitive data

---

## Related Rules

- `web-pipeline.md` — Web development pipeline
- `security-architecture.md` — Security patterns
