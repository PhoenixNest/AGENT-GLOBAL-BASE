---
name: shared-guidelines-performance-optimization
description: "Performance engineering discipline for all frontend deliverables — from Stage 2 HTML prototypes through Stage 5 production builds and Stage 8 integrity verification — covering Core Web Vitals optimization (LCP < 2.5s, INP < 200ms, CLS < 0.1), Lighthouse CI integration, bundle analysis and code splitting (initial bundle < 170KB gzipped), rendering performance tuning, and Real User Monitoring infrastructure. Owned by Frontend Chapter Lead (Amira Voss). Use when optimizing frontend performance, setting up Lighthouse CI, analyzing bundle sizes, implementing code splitting, tuning React rendering, or setting up RUM dashboards. Trigger: performance optimization, Core Web Vitals, Lighthouse, LCP, INP, CLS, bundle analysis, code splitting, rendering performance, RUM, performance budget, frontend performance."
prerequisites:
  - shared-overview

version: "1.0.0"
---

# Frontend Performance Optimization

**Category:** Frontend Engineering / Performance
**Owner:** Frontend Chapter Lead (Amira Voss)

## Overview

This skill establishes the performance engineering discipline for all frontend deliverables — from Stage 2 HTML prototypes through Stage 5 production builds and Stage 8 integrity verification. It covers Core Web Vitals optimization, Lighthouse CI integration, bundle analysis and code splitting strategies, rendering performance tuning, and the measurement infrastructure needed to guarantee that every shipped frontend surface meets or exceeds industry performance benchmarks. Performance is not an afterthought; it is a design constraint enforced from the first prototype iteration.

## Competency Dimensions

| Dimension                     | Description                                                              | Proficiency Indicators                                                            |
| ----------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| **Core Web Vitals Mastery**   | LCP, INP, CLS optimization with field and lab measurement correlation    | LCP < 2.5s, INP < 200ms, CLS < 0.1 on 4G + mid-tier device; lab/field delta < 15% |
| **Bundle Architecture**       | Code splitting, tree shaking, dynamic imports, dependency analysis       | Initial bundle < 170KB gzipped; route-level code splitting with prefetch hints    |
| **Lighthouse CI Integration** | Automated performance gating in CI/CD with regression detection          | Lighthouse CI scores ≥ 90 on all categories; CI blocks on regression > 5%         |
| **Rendering Optimization**    | Critical rendering path, paint optimization, layout thrashing prevention | Zero forced synchronous layouts; TTI < 3.8s; frame budget 16.67ms maintained      |
| **Resource Optimization**     | Image/font optimization, HTTP/2 multiplexing, caching strategies         | All images WebP/AVIF with fallbacks; font-display: swap; cache hit ratio > 95%    |
| **Performance Monitoring**    | Real User Monitoring (RUM), performance budgets, alerting                | RUM dashboard with p75 metrics; budget alerts trigger within 1 hour of violation  |

## Execution Guidance

### Core Web Vitals — Deep Dive

**Largest Contentful Paint (LCP) — Target: < 2.5 seconds**

LCP measures when the largest content element in the viewport becomes visible. The optimization hierarchy:

```
1. Server Response Time (TTFB < 800ms)
   ├─ Edge caching (CDN) for HTML
   ├─ Database query optimization
   └─ Avoid redirect chains (each redirect = +1 RTT)

2. Render-Blocking Resources
   ├─ Inline critical CSS (first 14KB)
   ├─ Defer non-critical CSS
   ├─ async/defer all scripts; never block parser
   └─ Preload LCP image: <link rel="preload" as="image" href="...">

3. Resource Load Time
   ├─ Compress LCP image (WebP/AVIF, quality 75-85)
   ├─ Preconnect to image CDN origin
   └─ Use responsive images (srcset + sizes)

4. Element Render Delay
   ├─ Avoid client-side rendering of LCP element
   ├─ Server-render or statically generate above-the-fold content
   └─ If SPA, use streaming SSR with selective hydration
```

**Interaction to Next Paint (INP) — Target: < 200 milliseconds**

INP replaced FID in March 2024 and measures the responsiveness of ALL interactions, not just the first:

- **Break long tasks** (> 50ms) using `scheduler.yield()`, `setTimeout`, or `requestIdleCallback`
- **Debounce user input handlers** — but debounce the _work_, not the event listener (listener should respond immediately with loading state)
- **Web Workers for heavy computation** — move JSON parsing, image processing, and data transformation off the main thread
- **Avoid layout thrashing** — batch DOM reads and writes separately; never read layout properties (offsetHeight, getBoundingClientRect) immediately after writes
- **Use `content-visibility: auto`** for off-screen content sections to skip rendering work

**Cumulative Layout Shift (CLS) — Target: < 0.1**

- **Always specify dimensions** on images, videos, iframes (`width` and `height` attributes, CSS `aspect-ratio`)
- **Reserve space for dynamic content** — skeletons, placeholders, or min-height on containers that will populate asynchronously
- **Never insert content above existing content** without user interaction — banners, cookies, ads must push content down from below or overlay
- **Font loading strategy:** `font-display: swap` with `size-adjust` to minimize FOUT-related layout shifts; use `ascent-override` and `descent-override` for font fallback metrics matching

### Bundle Analysis and Code Splitting

**Bundle budget allocation:**

| Category                | Budget (gzip) | Rationale                          |
| ----------------------- | ------------- | ---------------------------------- |
| Framework (React + DOM) | ~42 KB        | Non-negotiable baseline            |
| Routing                 | ~4 KB         | React Router or equivalent         |
| Design System           | ~25 KB        | Tree-shaken component library      |
| State Management        | ~8 KB         | Zustand or Redux Toolkit           |
| Business Logic          | ~50 KB        | Application-specific code          |
| Third-party             | ~40 KB        | Analytics, error tracking, etc.    |
| **Total initial**       | **~170 KB**   | Target for 3G fast connection < 3s |

**Code splitting strategies by priority:**

1. **Route-level splitting** (mandatory) — every route is a dynamic import:

   ```tsx
   const Dashboard = lazy(() => import('./pages/Dashboard'));
   // With prefetch on hover/viewport intersection
   <Link to="/dashboard" onMouseEnter={() => import('./pages/Dashboard')}>
   ```

2. **Component-level splitting** — heavy components below the fold:

   ```tsx
   const Chart = lazy(() => import("./components/Chart"));
   // Render fallback skeleton while loading
   <Suspense fallback={<ChartSkeleton />}>
     <Chart data={data} />
   </Suspense>;
   ```

3. **Vendor splitting** — separate third-party dependencies into their own chunk for better caching:

   ```js
   // vite.config.js
   build: {
     rollupOptions: {
       output: {
         manualChunks: {
           vendor: ['react', 'react-dom'],
           charts: ['recharts'],
           utils: ['lodash-es', 'date-fns'],
         },
       },
     },
   }
   ```

4. **Conditional splitting** — features behind feature flags load only when enabled:
   ```tsx
   if (featureFlags.isEnabled("new-editor")) {
     const Editor = await import("./features/NewEditor");
   }
   ```

**Bundle analysis workflow:**

- Run `npx vite-bundle-visualizer` or `webpack-bundle-analyzer` on every PR to `main`
- Set size budgets in CI: `import('lighthouse').then(lh => ...)` or use `bundlesize2`
- **Red flag:** any single chunk > 50KB gzipped without documented justification
- **Dependency audit:** quarterly review of `node_modules` — remove unused packages, prefer ESM-only packages (no CommonJS shims), replace heavy dependencies with lighter alternatives

### Lighthouse CI Integration

**CI gate configuration:**

```js
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ["http://localhost:3000/", "http://localhost:3000/dashboard"],
      settings: { preset: "desktop", chromeFlags: "--no-sandbox" },
      numberOfRuns: 3, // Median of 3 runs for stability
    },
    assert: {
      assertions: {
        "categories:performance": ["error", { minScore: 0.9 }],
        "categories:accessibility": ["error", { minScore: 0.95 }],
        "categories:best-practices": ["error", { minScore: 0.9 }],
        "categories:seo": ["warn", { minScore: 0.8 }],
        "largest-contentful-paint": ["error", { maxNumericValue: 2500 }],
        interactive: ["error", { maxNumericValue: 3800 }],
        "cumulative-layout-shift": ["error", { maxNumericValue: 0.1 }],
        "total-byte-weight": ["error", { maxNumericValue: 174080 }], // 170KB gzip
        "unused-javascript": ["warn", { maxNumericValue: 20480 }], // 20KB
      },
    },
    upload: {
      target: "temporary-public-storage", // Or Lighthouse Server
    },
  },
};
```

**Lighthouse CI in pipeline:**

- Runs on every PR to `main` against the production build
- **Fails the build** if any `error` assertion is violated
- Uploads reports to temporary storage for PR comment review
- **Regression detection:** compares current run against `main` baseline; regression > 5% on any metric blocks merge

### Rendering Performance

**React-specific rendering optimization:**

```tsx
// BEFORE: Re-renders on every parent state change
function ExpensiveList({ items, filter }) {
  const filtered = items.filter((i) => i.matches(filter)); // Runs every render
  return (
    <ul>
      {filtered.map((item) => (
        <ListItem key={item.id} {...item} />
      ))}
    </ul>
  );
}

// AFTER: Memoize computation and component
const ExpensiveList = memo(function ExpensiveList({ items, filter }) {
  const filtered = useMemo(
    () => items.filter((i) => i.matches(filter)),
    [items, filter], // Only recompute when these change
  );
  return (
    <ul>
      {filtered.map((item) => (
        <ListItem key={item.id} {...item} /> // ListItem must also be memoized
      ))}
    </ul>
  );
});
```

**Performance optimization decision tree:**

```
Is the component slow?
  ├─ Profile with React DevTools Profiler
  ├─ Check re-render count (is it rendering unnecessarily?)
  │   ├─ YES → memo() + useMemo/useCallback
  │   └─ NO → Check render cost per frame
  │       ├─ High cost → Virtualize lists (react-window), split into smaller components
  │       └─ Low cost but frequent → Check state update frequency (batch with flushSync?)
  └─ Check bundle size
      ├─ Large → Code split, tree shake, lazy load
      └─ Small → Check network waterfall (waterfall chart in DevTools)
```

**Critical rendering path optimization:**

- **Inline critical CSS** (above-the-fold styles) directly in `<style>` tag — target ≤ 14KB
- **Defer non-critical CSS** with `media="print" onload="this.media='all'"` pattern
- **Preload key resources:** `<link rel="preload" as="script" href="/main.js">`
- **Preconnect to third-party origins:** `<link rel="preconnect" href="https://cdn.example.com">`
- **DNS-prefetch for domains used later:** `<link rel="dns-prefetch" href="https://analytics.example.com">`

### Performance Monitoring in Production

**Real User Monitoring (RUM) implementation:**

- Use `web-vitals` library from Google to capture CWV metrics from real users
- Send to analytics backend with dimension tags: `page`, `country`, `connection`, `device`
- Track **p75** (75th percentile) — this is what Google uses for Core Web Vitals assessment
- Set up alerting when p75 exceeds targets for > 1 hour (not instantaneous spikes)

```ts
import { onLCP, onINP, onCLS } from "web-vitals";

function sendToAnalytics(metric) {
  // Batch and send to analytics
  // Include: metric.name, metric.value, metric.rating,
  //          page URL, connection type, device memory
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                                                   | Deliverable                                                |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Establish performance budgets for prototype; validate that IDS design patterns don't introduce layout shift risk | Performance budget document, prototype Lighthouse baseline |
| **Stage 3** (Architecture)           | Define performance architecture in UML; register ADRs for SSR vs CSR vs SSG strategy                             | Performance ADRs, UML deployment diagrams                  |
| **Stage 4** (Implementation Plan)    | Include performance testing tasks in implementation plan and Gantt                                               | Performance milestones in GANTT.md                         |
| **Stage 5** (Development)            | Implement performance monitoring, code splitting, and optimization across all platforms                          | Optimized production builds, RUM instrumentation           |
| **Stage 6** (Code Review)            | Review bundle sizes, code splitting strategies, and rendering patterns                                           | Performance review section in DEFECT-REPORT.md             |
| **Stage 8** (Integrity Verification) | Run Lighthouse CI against production build; verify all performance budgets met                                   | Performance integrity verification report                  |
| **Stage 10** (Release Readiness)     | Confirm performance standards met as part of architecture sign-off                                               | Performance sign-off contribution to release checklist     |

## Quality Standards

| Metric                          | Target                                                 | Enforcement                                                     |
| ------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------- |
| **LCP**                         | < 2.5s (p75, field)                                    | RUM dashboard; Lighthouse CI < 2.5s (lab)                       |
| **INP**                         | < 200ms (p75, field)                                   | RUM dashboard; Lighthouse CI < 200ms (lab)                      |
| **CLS**                         | < 0.1 (p75, field)                                     | RUM dashboard; Lighthouse CI < 0.1 (lab)                        |
| **Lighthouse Performance**      | ≥ 90                                                   | CI gate — fails build if below threshold                        |
| **Lighthouse Accessibility**    | ≥ 95                                                   | CI gate — fails build if below threshold                        |
| **Initial bundle size**         | < 170KB gzipped                                        | CI gate via `bundlesize2` or Lighthouse `total-byte-weight`     |
| **Single chunk max**            | < 50KB gzipped                                         | Bundle analyzer review in Stage 6                               |
| **Code coverage — performance** | All routes lazy-loaded                                 | Audit: zero synchronous route imports                           |
| **Third-party script impact**   | < 50KB total, all deferred/async                       | Third-party audit; CI blocks on synchronous third-party scripts |
| **Font loading**                | No FOIT/FOUT, font-display: swap                       | Lighthouse audit; visual inspection                             |
| **Image optimization**          | 100% WebP/AVIF with fallbacks, responsive srcset       | Lighthouse `uses-optimized-images` audit                        |
| **Performance regression**      | Zero regressions > 5% without documented justification | Lighthouse CI comparison against `main` baseline                |
