---
name: frontend-performance-baseline
description: Performance baselines are the foundation of a fast, reliable user experience. Without a baseline.
---

# Frontend Performance Baseline

## Overview

Performance baselines are the foundation of a fast, reliable user experience. Without a baseline, performance regressions creep in silently — a 50ms LCP degradation per PR compounds to a 2-second regression over 40 releases. This skill defines how to establish, measure, and enforce performance targets across all frontend web deliverables.

### Why Baselines Matter

| Problem              | How Baselines Solve It                                       |
| -------------------- | ------------------------------------------------------------ |
| Silent regression    | Automated budgets block PRs that exceed thresholds           |
| Inconsistent targets | Device-tier strategy sets realistic goals per hardware class |
| No accountability    | CI/CD integration ties performance to merge gates            |
| Lab vs. reality gap  | RUM data validates lab measurements against real users       |
| Budget creep         | Explicit budget files prevent unbounded dependency growth    |

### Scope

This skill applies to all frontend web artifacts produced during Stage 5 (Development) and verified during Stage 8 (Integrity Verification). It covers both **lab metrics** (Lighthouse CI) and **field metrics** (Real User Monitoring).

---

## Core Web Vitals Targets

Google Core Web Vitals are the primary performance signals. Targets are set per the **good** threshold for each metric.

| Metric | Full Name                 | Good Target | Needs Improvement | Poor    | Measurement      |
| ------ | ------------------------- | ----------- | ----------------- | ------- | ---------------- |
| LCP    | Largest Contentful Paint  | <= 2.5s     | 2.5s–4.0s         | > 4.0s  | Page load        |
| INP    | Interaction to Next Paint | <= 200ms    | 200ms–500ms       | > 500ms | All interactions |
| CLS    | Cumulative Layout Shift   | <= 0.1      | 0.1–0.25          | > 0.25  | Page lifecycle   |

### Additional Key Metrics

| Metric      | Good Target | Why It Matters                |
| ----------- | ----------- | ----------------------------- |
| TTFB        | <= 800ms    | Server responsiveness ceiling |
| FCP         | <= 1.8s     | First visual feedback         |
| TBT         | <= 200ms    | Main thread blocking impact   |
| Speed Index | <= 3.4s     | Perceived load speed          |

> **Note:** FID has been superseded by INP as of March 2024. Legacy references to FID should be migrated to INP. Where FID is still required by downstream consumers, target <= 100ms.

### LCP Optimization Checklist

- [ ] Server response time (TTFB) < 800ms
- [ ] Critical CSS inlined in `<head>`
- [ ] Largest image preloaded with `<link rel="preload">`
- [ ] Hero images use responsive `srcset` and `sizes`
- [ ] No render-blocking JavaScript in `<head>`
- [ ] Server-side rendering or static generation for content pages

### INP Optimization Checklist

- [ ] Long tasks (> 50ms) identified and broken up
- [ ] Event handlers debounced/throttled appropriately
- [ ] Web Workers used for heavy computation
- [ ] `requestIdleCallback` for non-critical work
- [ ] Third-party scripts loaded with `async` or `defer`

### CLS Optimization Checklist

- [ ] All images and iframes have explicit `width` and `height`
- [ ] Font loading uses `font-display: optional` or `swap` with size-adjust
- [ ] No content injected above existing content without reserved space
- [ ] Animations use `transform` and `opacity` only (avoid layout-triggering properties)
- [ ] Dynamic banners reserve space or push content predictably

---

## Device Tier Strategy

Performance targets must account for hardware diversity. A single "desktop" target hides the experience for the majority of users on constrained devices.

### Tier Definitions

| Tier          | CPU Throttling                | Network                                         | Memory  | Representative Device    |
| ------------- | ----------------------------- | ----------------------------------------------- | ------- | ------------------------ |
| **Low-end**   | 6x slowdown (Moto G4 profile) | Slow 4G (1.6 Mbps down, 750 Kbps up, 150ms RTT) | <= 2 GB | Moto G4, low-end Android |
| **Mid-range** | 4x slowdown                   | Fast 4G (9 Mbps down, 9 Mbps up, 40ms RTT)      | 3–4 GB  | Pixel 3a, iPhone SE      |
| **High-end**  | No throttling                 | Desktop Wi-Fi (unlimited, 0ms RTT)              | >= 8 GB | MacBook Pro, Pixel 8 Pro |

### Per-Tier Targets

| Metric                    | Low-end   | Mid-range | High-end  |
| ------------------------- | --------- | --------- | --------- |
| LCP                       | <= 4.0s   | <= 2.5s   | <= 1.5s   |
| INP                       | <= 400ms  | <= 200ms  | <= 100ms  |
| CLS                       | <= 0.1    | <= 0.1    | <= 0.05   |
| TTI                       | <= 8.0s   | <= 3.8s   | <= 2.0s   |
| Max Bundle Size (gzipped) | <= 250 KB | <= 200 KB | <= 175 KB |

### Testing Strategy

```bash
# Low-end emulation with Lighthouse CLI
lighthouse https://example.com \
  --chrome-flags="--headless" \
  --throttling-method=devtools \
  --throttling.cpuSlowdownMultiplier=6 \
  --throttling.rttMs=150 \
  --throttling.throughputKbps=1600 \
  --output=json \
  --output-path=reports/lighthouse-lowend.json

# Mid-range emulation
lighthouse https://example.com \
  --chrome-flags="--headless" \
  --throttling-method=devtools \
  --throttling.cpuSlowdownMultiplier=4 \
  --throttling.rttMs=40 \
  --throttling.throughputKbps=9000 \
  --output=json \
  --output-path=reports/lighthouse-midrange.json
```

---

## Lighthouse CI Integration

Lighthouse CI automates performance auditing on every PR. It runs Lighthouse, compares results to budgets, and posts results as PR comments.

### Installation

```bash
npm install --save-dev @lhci/cli @lhci/server
```

### Configuration File: `lighthouserc.yml`

```yaml
ci:
  collect:
    numberOfRuns: 3
    settings:
      preset: desktop
      throttlingMethod: simulate
      throttling:
        cpuSlowdownMultiplier: 4
        rttMs: 40
        throughputKbps: 9000
    url:
      - http://localhost:3000/
      - http://localhost:3000/products
      - http://localhost:3000/checkout

  assert:
    preset: lighthouse:no-errors
    assertions:
      categories:performance:
        - minScore: 0.90
          aggregationMethod: median-run
      interactive:
        - minScore: 0.90
      first-contentful-paint:
        - maxNumericValue: 1800
      largest-contentful-paint:
        - maxNumericValue: 2500
      cumulative-layout-shift:
        - maxNumericValue: 0.1
      total-blocking-time:
        - maxNumericValue: 200

  upload:
    target: lhci
    serverBaseUrl: https://lhci.internal.company.com
```

### GitHub Actions Workflow

```yaml
name: Lighthouse CI

on:
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build application
        run: |
          npm ci
          npm run build

      - name: Serve and audit
        uses: treosh/lighthouse-ci-action@v12
        with:
          configPath: "./lighthouserc.yml"
          uploadArtifacts: true
          temporaryPublicStorage: true

      - name: Comment PR with results
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const lighthouseResults = process.env.LHCI_URL;
            // Post score summary to PR
```

### Budget Assertions Explained

| Assertion                                | Meaning                                      |
| ---------------------------------------- | -------------------------------------------- |
| `categories:performance: minScore: 0.90` | Overall performance score must be >= 90      |
| `maxNumericValue: 2500` on LCP           | LCP must not exceed 2.5 seconds (2500ms)     |
| `aggregationMethod: median-run`          | Uses median across `numberOfRuns` iterations |

---

## Performance Budgets

Budgets prevent incremental performance decay. They are enforced at build time and CI time.

### Bundle Size Budgets

```json
{
  "performance-budget": {
    "bundles": {
      "main.js": { "maxSize": "175kb" },
      "vendor.js": { "maxSize": "120kb" },
      "polyfills.js": { "maxSize": "35kb" },
      "styles.css": { "maxSize": "40kb" }
    },
    "totals": {
      "javascript": "250kb",
      "css": "50kb",
      "images": "500kb",
      "total": "800kb"
    }
  }
}
```

### Script Execution Budgets

| Category               | Budget              | Enforcement             |
| ---------------------- | ------------------- | ----------------------- |
| Main thread work (TTI) | <= 3800ms mid-range | Lighthouse CI assert    |
| Long tasks (> 50ms)    | <= 5 per page load  | Web Vitals extension    |
| Third-party JS total   | <= 100 KB gzipped   | Build-time budget check |
| Time to Interactive    | <= 3.8s mid-range   | Lighthouse CI assert    |

### Image Size Budgets

| Context                 | Max Size (uncompressed) | Max Size (optimized) | Format    |
| ----------------------- | ----------------------- | -------------------- | --------- |
| Hero image (full-width) | 200 KB                  | 80 KB                | AVIF/WebP |
| Thumbnail               | 50 KB                   | 15 KB                | WebP      |
| Icon/Logo               | 20 KB                   | 5 KB                 | SVG       |
| Background image        | 150 KB                  | 60 KB                | AVIF/WebP |

### Font Loading Budgets

| Parameter                        | Budget                                                   |
| -------------------------------- | -------------------------------------------------------- |
| Total font payload (all weights) | <= 100 KB gzipped                                        |
| Font display strategy            | `font-display: swap` or `optional`                       |
| Critical font preload            | Single WOFF2 file preloaded in `<head>`                  |
| Subsetting                       | Latin subset only for initial load; full set lazy-loaded |

```html
<!-- Preload critical font -->
<link
  rel="preload"
  href="/fonts/inter-latin-400.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>

<!-- Font face with fallback -->
@font-face { font-family: 'Inter'; src: url('/fonts/inter-latin-400.woff2')
format('woff2'); font-display: swap; size-adjust: 100%; }
```

---

## Regression Detection

Automated regression detection catches performance decay before it reaches production.

### Threshold Configuration

| Signal                 | Warning Threshold       | Fail Threshold          |
| ---------------------- | ----------------------- | ----------------------- |
| LCP increase           | +10% from baseline      | +20% from baseline      |
| INP increase           | +15% from baseline      | +30% from baseline      |
| CLS increase           | +0.02 from baseline     | +0.05 from baseline     |
| Bundle size increase   | +5% from baseline       | +10% from baseline      |
| Performance score drop | -3 points from baseline | -7 points from baseline |

### Automated Alert Workflow

```
PR opened
  → Lighthouse CI runs (3 iterations)
  → Results compared to baseline
  → If FAIL threshold:
      - Block merge (GitHub status = failure)
      - Post detailed comment with metric deltas
      - Notify #frontend-performance channel
  → If WARNING threshold:
      - Allow merge with warning comment
      - Log to performance dashboard
  → If PASS:
      - Update baseline if metrics improved
      - Post green status comment
```

### Rollback Triggers

Rollback is automatically triggered when production RUM data shows:

| Condition                                      | Action                                 |
| ---------------------------------------------- | -------------------------------------- |
| p75 LCP > 4.0s for > 10% of users after deploy | Automatic rollback to previous release |
| Crash rate spike > 2x baseline                 | Page and alert on-call engineer        |
| INP p75 > 500ms on mid-range devices           | Block further rollouts, investigate    |

---

## Real User Monitoring (RUM)

Lab metrics are necessary but insufficient. RUM captures actual user experience across the global device and network spectrum.

### Data Collection Points

| API                                              | Data Collected              | Purpose                         |
| ------------------------------------------------ | --------------------------- | ------------------------------- |
| `PerformanceObserver` (largest-contentful-paint) | LCP per page view           | Core Web Vitals field data      |
| `PerformanceObserver` (layout-shift)             | CLS per session entry       | Layout stability tracking       |
| `PerformanceObserver` (event)                    | INP per interaction         | Interaction responsiveness      |
| Navigation Timing API                            | TTFB, FCP, DOMContentLoaded | Load timeline                   |
| Resource Timing                                  | Per-resource load times     | Identify slow third-party calls |

### RUM Implementation Snippet

```javascript
import { onLCP, onINP, onCLS, onTTFB, onFCP } from "web-vitals";

function sendToAnalytics(metric) {
  // Send to your analytics endpoint
  navigator.sendBeacon(
    "/api/performance-metrics",
    JSON.stringify({
      name: metric.name,
      value: metric.value,
      delta: metric.delta,
      rating: metric.rating,
      navigationType: metric.navigationType,
      url: window.location.href,
      userAgent: navigator.userAgent,
      timestamp: Date.now(),
    }),
  );
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
onTTFB(sendToAnalytics);
onFCP(sendToAnalytics);
```

### Percentile Analysis

| Percentile   | What It Represents           | Target Use                      |
| ------------ | ---------------------------- | ------------------------------- |
| p50 (median) | Typical user experience      | Dashboard trending              |
| p75          | Edge of "typical" experience | Core Web Vitals field threshold |
| p95          | Worst 5% of experiences      | Identifying severe edge cases   |
| p99          | Worst 1% of experiences      | Crash and timeout investigation |

> **Rule:** Core Web Vitals pass/fail is determined at **p75** across all field data collected over a 28-day window, per Google's field data methodology.

---

## Performance Testing Workflow

### Step-by-Step Process

```
1. Establish baseline
   └── Run Lighthouse on production URLs (3 runs each)
   └── Record median scores as baseline in PROGRESS.md

2. Set budgets
   └── Define bundle size, LCP, INP, CLS budgets per device tier
   └── Commit budgets to project repo (e.g., performance-budget.json)

3. Integrate CI
   └── Add Lighthouse CI to pipeline
   └── Configure budget assertions
   └── Enable PR comment output

4. Validate on development branch
   └── Run Lighthouse CI against feature branch
   └── Fix any budget violations before opening PR

5. Monitor production
   └── Deploy RUM instrumentation
   └── Compare field data to lab baseline weekly
   └── Investigate deltas > 10%

6. Stage 8 Integrity Verification
   └── CTO panel reviews performance metrics
   └── Verify all budgets pass on mid-range device profile
   └── Sign off or raise P1/P2 defects
```

### Tools Reference

| Tool                              | Purpose                      | Stage |
| --------------------------------- | ---------------------------- | ----- |
| Lighthouse                        | Lab performance audit        | 5, 8  |
| Lighthouse CI                     | Automated PR-level checks    | 5, 6  |
| web-vitals library                | RUM data collection          | 5, 8  |
| WebPageTest                       | Deep-dive waterfall analysis | 5     |
| Chrome DevTools Performance panel | Interactive profiling        | 5     |
| BundlePhobia                      | Dependency size checking     | 4, 5  |

---

## Stage 5 / Stage 8 Integration

### Stage 5 (Development)

During development, the CTO and platform leads are responsible for:

- Implementing performance budgets in build configuration (Vite, Webpack, esbuild)
- Running Lighthouse CI on all feature branches before PR
- Fixing any P0/P1 performance defects (e.g., LCP > 4s on mid-range)
- Logging performance metrics in `DEVELOPMENT-LOG.md` per platform
- Ensuring RUM instrumentation is wired in production builds

**Checklist for Stage 5 completion:**

- [ ] All bundle size budgets pass
- [ ] Lighthouse CI score >= 90 on mid-range profile
- [ ] No CLS violations > 0.25 on any audited page
- [ ] RUM instrumentation deployed
- [ ] `DEVELOPMENT-LOG.md` updated with performance section

### Stage 8 (Integrity Verification)

The CTO panel conducts a performance review as part of integrity verification:

| Panel Member | Performance Responsibility                                                                 |
| ------------ | ------------------------------------------------------------------------------------------ |
| CTO          | Overall architecture supports performance targets; no technical debt blocking optimization |
| CDO          | Design implementation does not introduce layout shift or render-blocking assets            |
| CSO          | Security headers (CSP, HSTS) do not add measurable latency                                 |
| Test Lead    | Performance test suite covers all critical user journeys                                   |

**Gate criteria for Stage 8 performance sign-off:**

1. Lighthouse CI passes all budget assertions on `numberOfRuns: 3`
2. No P0/P1 performance defects in DEFECT-REPORT.md
3. RUM baseline established and within 15% of lab measurements
4. Performance budgets documented and committed to repository

---

## References

| Resource                             | URL                                                          |
| ------------------------------------ | ------------------------------------------------------------ |
| Lighthouse CI Documentation          | https://github.com/GoogleChrome/lighthouse-ci                |
| Web Vitals                           | https://web.dev/articles/vitals                              |
| Core Web Vitals Thresholds           | https://web.dev/articles/defining-core-web-vitals-thresholds |
| Lighthouse Performance Scoring       | https://web.dev/articles/performance-scoring                 |
| web-vitals npm package               | https://www.npmjs.com/package/web-vitals                     |
| INP Guidance                         | https://web.dev/articles/inp                                 |
| Performance Budgets (web.dev)        | https://web.dev/articles/performance-budgets                 |
| Chrome User Experience Report (CrUX) | https://developer.chrome.com/docs/crux                       |
| OWASP Frontend Security              | https://owasp.org/www-project-web-security-testing-guide/    |

---

_This skill is owned by the Frontend Web engineering team. Questions or updates should be directed to the Frontend Lead (Amira Voss) or reviewed against the latest web.dev guidance._
