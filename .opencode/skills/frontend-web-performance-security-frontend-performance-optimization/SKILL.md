---
name: frontend-web-performance-security-frontend-performance-optimizat
description: Frontend performance optimization — code splitting, lazy loading, bundle analysis, image optimization, critical CSS, font loading strategies, and runtime performance tuning. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 5 (Development) for performance implementation and Stage 7 (Testing) for performance benchmarking. Trigger: performance optimization, code splitting, lazy loading, bundle analysis, critical css, font loading, web vitals optimization.
prerequisites:
  - frontend-web-overview

version: "1.0.0"
---

# Frontend Performance Optimization — React Specialization

**Category:** Frontend Engineering / Performance
**Owner:** Senior Frontend Engineer (Rafael Santos)

## Overview

This skill provides deep React-specific performance engineering expertise, covering rendering optimization through memoization strategies, virtual scrolling for large datasets, progressive loading with React.lazy and Suspense, bundle optimization at the component level, and the profiling methodology needed to identify and eliminate performance bottlenecks. React's declarative model makes it easy to write correct code but easy to write slow code — understanding the reconciliation algorithm, the conditions that trigger re-renders, and the cost of each render phase is essential for building applications that remain performant at scale. This skill applies from Stage 2 prototype validation through Stage 5 implementation and Stage 6 code review.

## Competency Dimensions

| Dimension                  | Description                                                                              | Proficiency Indicators                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **React Rendering Model**  | Deep understanding of reconciliation, commit phase, render phase, and bailout conditions | Can explain why a component re-renders; can predict render count from state update patterns   |
| **Memoization Strategies** | React.memo, useMemo, useCallback — when to use, when to avoid, measuring actual benefit  | Memoization applied only where profiling confirms benefit; zero premature optimization        |
| **Virtual Scrolling**      | react-window / react-virtualized for large lists/grids with constant memory footprint    | Lists of 10,000+ items render at 60fps; DOM node count stays constant regardless of data size |
| **Progressive Loading**    | React.lazy, Suspense boundaries, transition APIs, streaming SSR                          | Initial paint shows meaningful content within 1.5s; loading states are skeletal, not spinners |
| **Bundle Optimization**    | Route-level and component-level code splitting, dynamic imports, tree shaking analysis   | Every route is lazy-loaded; no chunk > 50KB gzipped without justification                     |
| **Performance Profiling**  | React DevTools Profiler, Chrome Performance tab, flame graphs, why-did-you-render        | Can identify the exact component and prop causing unnecessary re-renders within 5 minutes     |

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                                  | Deliverable                            |
| ------------------------------------ | ----------------------------------------------------------------------------------------------- | -------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Identify performance-sensitive components in IDS; establish rendering budgets                   | Performance notes in IDS               |
| **Stage 4** (Implementation Plan)    | Define performance optimization tasks in implementation plan and Gantt                          | Performance milestones in GANTT.md     |
| **Stage 5** (Development)            | Implement React rendering optimizations, virtual scrolling, code splitting, Suspense boundaries | Optimized React codebase               |
| **Stage 6** (Code Review)            | Review rendering patterns, memoization usage, bundle sizes, lazy loading coverage               | Performance review in DEFECT-REPORT.md |
| **Stage 8** (Integrity Verification) | Verify performance budgets met; run profiling against production build                          | Performance integrity report           |

## Quality Standards

| Metric                        | Target                                                                      | Enforcement                                      |
| ----------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------ |
| **Re-render optimization**    | No component re-renders more than once per user action (unless intentional) | React DevTools Profiler audit                    |
| **Memoization ROI**           | All memo() calls provide measurable performance benefit                     | Profiler confirms bailout on memoized components |
| **Virtual scroll**            | Lists > 100 items use virtualization                                        | Code review; audit of List/FlatList usage        |
| **Lazy loading coverage**     | 100% of routes lazy-loaded; all below-the-fold components lazy-loaded       | Import audit: zero synchronous route imports     |
| **Suspense boundaries**       | Every lazy() call wrapped in Suspense with meaningful fallback              | Code review                                      |
| **Bundle size per route**     | < 50KB gzipped per route chunk                                              | Bundle analyzer; CI gate                         |
| **Frame rate**                | ≥ 60fps for all user interactions (scroll, input, animation)                | Chrome Performance tab audit                     |
| **Memory usage**              | No memory leaks detected after 10-minute interaction session                | Chrome Memory Profiler                           |
| **useTransition usage**       | All expensive computations wrapped in startTransition                       | Code review for search/filter operations         |
| **Error boundaries**          | Every lazy-loaded component has an ErrorBoundary                            | Code review                                      |
| **Tree shaking**              | Zero unused exports in production bundle                                    | Bundle analyzer; dead code elimination audit     |
| **Context re-render control** | No component re-renders due to unrelated context changes                    | Context consumption audit                        |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
