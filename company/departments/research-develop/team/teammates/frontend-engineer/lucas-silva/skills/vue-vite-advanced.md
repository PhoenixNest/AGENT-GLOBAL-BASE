---
version: "1.0.0"
---

| Competency                       | Description                                                                    | Quality Criteria                                                                        |
| -------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| **Composition API Architecture** | Composables, reactive state patterns, provide/inject, lifecycle management     | Zero Options API in new code; composables are pure, testable, and type-safe             |
| **Vite Plugin Development**      | Custom plugin creation, transform hooks, resolve hooks, dev server middleware  | Custom plugins for domain-specific transforms; zero build-time workarounds              |
| **HMR Optimization**             | Fast refresh configuration, module graph optimization, HMR boundary management | HMR updates in < 100ms; no full page reloads during development                         |
| **Code Splitting**               | Route-level, component-level, and vendor splitting with dynamic imports        | All routes lazy-loaded; vendor chunks optimally split; preload/prefetch strategy        |
| **Tree Shaking**                 | ESM-first architecture, sideEffects configuration, dead code elimination       | Zero unused exports in production bundle; package.json sideEffects correctly configured |
| **Build Optimization**           | Minification, compression, asset optimization, bundle analysis                 | Production build < 170KB gzipped initial; all assets optimized                          |

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                 | Deliverable                                 |
| ------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Validate Vue-based prototype against IDS; document component architecture      | Vue prototype, component architecture notes |
| **Stage 3** (Architecture)           | Define Vue architecture in UML; register ADRs for state management and routing | Vue architecture ADRs                       |
| **Stage 5** (Development)            | Implement Vue components, composables, Vite build configuration                | Production Vue codebase                     |
| **Stage 6** (Code Review)            | Review Composition API patterns, Vite config, code splitting, tree shaking     | Vue architecture review in DEFECT-REPORT.md |
| **Stage 8** (Integrity Verification) | Verify Vue build meets performance budgets; validate all components match IDS  | Vue integrity verification report           |

## Quality Standards

| Metric                        | Target                                                   | Enforcement                                  |
| ----------------------------- | -------------------------------------------------------- | -------------------------------------------- |
| **Composition API adoption**  | 100% of new components use `<script setup>`              | Code review; zero Options API in new code    |
| **Composable quality**        | All composables are pure, type-safe, and testable        | Code review; unit test coverage              |
| **Code splitting**            | 100% of routes lazy-loaded                               | Import audit; zero synchronous route imports |
| **Tree shaking**              | Zero unused exports in production bundle                 | Bundle analyzer; sideEffects audit           |
| **HMR performance**           | HMR updates in < 100ms                                   | Manual measurement during development        |
| **Build size**                | Initial bundle < 170KB gzipped                           | CI gate via bundle analyzer                  |
| **Type safety**               | 100% of composables and components are type-safe         | `vue-tsc --noEmit` in CI                     |
| **Provide/Inject usage**      | Only for cross-cutting concerns (theme, auth, i18n)      | Code review; no over-use of provide/inject   |
| **Lifecycle cleanup**         | All subscriptions and timers cleaned up in `onUnmounted` | Code review                                  |
| **Vite plugin quality**       | Custom plugins have tests and documentation              | Code review; plugin test coverage            |
| **Vendor chunk optimization** | No vendor chunk > 100KB without justification            | Bundle analyzer review                       |
| **CSS optimization**          | No unused CSS in production                              | PurgeCSS or similar audit                    |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
