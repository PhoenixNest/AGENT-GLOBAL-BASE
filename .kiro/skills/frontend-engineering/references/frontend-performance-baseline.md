---
name: frontend-performance-baseline
description: Frontend performance baseline definition, measurement, and regression prevention — Core Web Vitals targets, Performance Budget per route, RUM instrumentation, CI performance gates, and the process for setting and updating the company's web performance SLA. Use when establishing the baseline for a new web product, when investigating a CWV regression, or when defining the performance gate criteria for Stage 6 code review and Stage 8 integrity verification.
version: "1.0.0"
---

# Frontend Performance Baseline

## Purpose

Define and enforce the company's frontend performance baseline — the measurable performance floor that every web release must meet before it is allowed to ship. This is distinct from performance optimization (see `performance-optimization.md`): optimization is how you improve; the baseline is the minimum you must not fall below. Amira Voss owns the baseline definition for the company's web products.

## Core Web Vitals Targets

| Metric                                    | Target (Good) | Warning    | Block Release |
| ----------------------------------------- | ------------- | ---------- | ------------- |
| **LCP** (Largest Contentful Paint)        | ≤ 2.5s        | 2.5–4.0s   | > 4.0s        |
| **FID / INP** (Interaction to Next Paint) | ≤ 200ms       | 200–500ms  | > 500ms       |
| **CLS** (Cumulative Layout Shift)         | ≤ 0.1         | 0.1–0.25   | > 0.25        |
| **TTFB** (Time to First Byte)             | ≤ 600ms       | 600–1500ms | > 1500ms      |
| **FCP** (First Contentful Paint)          | ≤ 1.8s        | 1.8–3.0s   | > 3.0s        |

All targets measured at **P75** on real user data (RUM), not synthetic lab tests only.

## Performance Budget Per Route

Each critical route has a performance budget that Amira defines at Stage 3 (when the technology stack and page architecture are decided) and enforces at Stage 6 (Code Review) and Stage 8 (Integrity Verification):

| Route Type                   | JS Bundle (gzipped) | CSS Bundle      | Total Transfer   | Image Budget |
| ---------------------------- | ------------------- | --------------- | ---------------- | ------------ |
| **Landing / Marketing**      | ≤ 80 KB             | ≤ 20 KB         | ≤ 200 KB         | ≤ 100 KB     |
| **Authenticated app shell**  | ≤ 150 KB            | ≤ 30 KB         | ≤ 400 KB         | Lazy-loaded  |
| **Feature page**             | ≤ 50 KB (delta)     | ≤ 10 KB (delta) | ≤ 150 KB (delta) | Lazy-loaded  |
| **Checkout / Critical path** | ≤ 40 KB (delta)     | ≤ 8 KB (delta)  | ≤ 100 KB (delta) | Minimal      |

Budget enforcement in CI via Bundlesize or size-limit:

```json
// .size-limit.json
[
  {
    "path": "dist/js/main.*.js",
    "limit": "80 KB",
    "gzip": true
  },
  {
    "path": "dist/css/main.*.css",
    "limit": "20 KB",
    "gzip": true
  }
]
```

Any PR that exceeds the budget triggers a CI failure, which Amira reviews before it can be merged.

## RUM Instrumentation

Real User Monitoring is mandatory for all web products. Amira defines the RUM setup requirements:

```typescript
// Required instrumentation before Stage 8 sign-off
import { onLCP, onINP, onCLS, onFCP, onTTFB } from "web-vitals";

const reportWebVital = (metric: Metric) => {
  // Send to analytics — dataLayer, custom API, or Datadog RUM
  window.dataLayer?.push({
    event: "web_vital",
    metric_name: metric.name,
    metric_value: metric.value,
    metric_rating: metric.rating, // 'good' | 'needs-improvement' | 'poor'
    metric_id: metric.id,
    page_path: window.location.pathname,
  });
};

onLCP(reportWebVital);
onINP(reportWebVital);
onCLS(reportWebVital);
onFCP(reportWebVital);
onTTFB(reportWebVital);
```

**RUM dashboards** — Amira owns a performance dashboard in the company's analytics platform with:

- P75 CWV per route, updated daily
- 7-day trend for each metric
- Alert when any P75 metric degrades beyond the Warning threshold for 2 consecutive days

## Baseline Update Protocol

The performance baseline is a living contract — it updates when:

1. A new framework or architecture is adopted (Stage 3 triggers a baseline recalibration)
2. A major route is added or restructured
3. A new real-world performance measurement shows the baseline is systematically unachievable

**Baseline update process:**

1. Amira proposes the new baseline with evidence (RUM data, Lighthouse CI results)
2. VP Web and VP API review and approve
3. CI pipeline budget thresholds are updated
4. All active feature teams are notified before the change takes effect

## Stage 6 (Code Review) — Performance Gate

At Stage 6, Amira's performance review is mandatory before any PR touching the critical rendering path is merged:

| Check                        | Tool                 | Pass Criteria                         |
| ---------------------------- | -------------------- | ------------------------------------- |
| Bundle size                  | size-limit CI        | All budgets green                     |
| Lighthouse Performance       | Lighthouse CI        | Score ≥ 90 on all audited routes      |
| No render-blocking resources | Lighthouse CI        | 0 render-blocking scripts in `<head>` |
| No layout shift regressions  | Playwright CLS check | CLS delta < 0.05 vs. baseline         |

## Stage 8 (Integrity Verification) — Baseline Confirmation

Amira's Stage 8 sign-off confirms:

- P75 LCP, INP, CLS from the staging RUM are within "Good" thresholds
- No performance budget violations in the release build
- RUM instrumentation is live and emitting data in staging

## Quality Standards

- Performance baselines documented and version-controlled in Confluence before any product enters Stage 5
- CI performance gates block merges that exceed bundle budgets — no manual overrides without Amira's written approval
- RUM dashboard active and monitored for all products in production
- Stage 8 performance sign-off delivered within 24 hours of receiving the release candidate
