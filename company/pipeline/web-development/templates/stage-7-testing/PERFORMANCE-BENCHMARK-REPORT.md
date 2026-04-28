# Performance Benchmark Report

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Web Application (P1)
**Stage:** 7 — Automated Testing

---

## 1. Web Performance Metrics

| Metric                         | PRD Target     | Measurement Method           | Browser | Result  | Pass/Fail       |
| ------------------------------ | -------------- | ---------------------------- | ------- | ------- | --------------- |
| LCP (Largest Contentful Paint) | <2.5s          | Lighthouse CI (3G throttled) | Chrome  | [X.XXs] | ☐ Pass / ☐ Fail |
| LCP (Largest Contentful Paint) | <2.5s          | Lighthouse CI (3G throttled) | Firefox | [X.XXs] | ☐ Pass / ☐ Fail |
| LCP (Largest Contentful Paint) | <2.5s          | Lighthouse CI (3G throttled) | Safari  | [X.XXs] | ☐ Pass / ☐ Fail |
| CLS (Cumulative Layout Shift)  | <0.1           | Lighthouse CI                | Chrome  | [X.XX]  | ☐ Pass / ☐ Fail |
| CLS (Cumulative Layout Shift)  | <0.1           | Lighthouse CI                | Firefox | [X.XX]  | ☐ Pass / ☐ Fail |
| CLS (Cumulative Layout Shift)  | <0.1           | Lighthouse CI                | Safari  | [X.XX]  | ☐ Pass / ☐ Fail |
| TTFB (Time to First Byte)      | <800ms         | WebPageTest                  | Chrome  | [Xms]   | ☐ Pass / ☐ Fail |
| TTI (Time to Interactive)      | <3.8s          | Lighthouse CI                | Chrome  | [X.XXs] | ☐ Pass / ☐ Fail |
| TTI (Time to Interactive)      | <3.8s          | Lighthouse CI                | Firefox | [X.XXs] | ☐ Pass / ☐ Fail |
| TTI (Time to Interactive)      | <3.8s          | Lighthouse CI                | Safari  | [X.XXs] | ☐ Pass / ☐ Fail |
| Bundle size (initial)          | <200KB gzipped | Webpack/Vite analysis        | —       | [XX]KB  | ☐ Pass / ☐ Fail |
| Bundle size (total)            | <500KB gzipped | Webpack/Vite analysis        | —       | [XX]KB  | ☐ Pass / ☐ Fail |

---

## 2. Test Environment

| Parameter              | Value                                           |
| ---------------------- | ----------------------------------------------- |
| **Browser versions**   | Chrome [N], Firefox [N], Safari [N]             |
| **Network throttling** | 3G (1.6Mbps down, 750Kbps up, 150ms RTT)        |
| **Device emulation**   | Moto G4 (mobile), iPad (tablet), Desktop 1440px |
| **Measurement tools**  | Lighthouse CI, WebPageTest, Chrome DevTools     |
| **Server environment** | [Vercel staging / local dev server]             |

---

## 3. Lighthouse Scores

| Category       | Chrome | Firefox | Safari | Target |
| -------------- | ------ | ------- | ------ | ------ |
| Performance    | [XX]   | [XX]    | [XX]   | ≥90    |
| Accessibility  | [XX]   | [XX]    | [XX]   | ≥95    |
| Best Practices | [XX]   | [XX]    | [XX]   | ≥90    |
| SEO            | [XX]   | [XX]    | [XX]   | ≥90    |

---

## 4. Performance Regression History

| Metric       | Baseline | Current | Delta    | Trend     |
| ------------ | -------- | ------- | -------- | --------- |
| LCP (Chrome) | [X.XXs]  | [X.XXs] | [+/- X%] | ↑ / ↓ / → |
| CLS (Chrome) | [X.XX]   | [X.XX]  | [+/- X%] | ↑ / ↓ / → |
| TTI (Chrome) | [X.XXs]  | [X.XXs] | [+/- X%] | ↑ / ↓ / → |
| Bundle size  | [XX]KB   | [XX]KB  | [+/- X%] | ↑ / ↓ / → |

---

## 5. API Performance

| Endpoint             | Method | Avg Response | P95 Response | P99 Response | Throughput (rps) | Error Rate | Status      |
| -------------------- | ------ | ------------ | ------------ | ------------ | ---------------- | ---------- | ----------- |
| [GET /api/resource]  | GET    | [X]ms        | [X]ms        | [X]ms        | [N]              | [X]%       | ☐ / 🟡 / ✅ |
| [POST /api/resource] | POST   | [X]ms        | [X]ms        | [X]ms        | [N]              | [X]%       | ☐ / 🟡 / ✅ |

---

## 6. Optimization Opportunities

| Opportunity                            | Estimated Impact | Effort         | Priority   | Status                               |
| -------------------------------------- | ---------------- | -------------- | ---------- | ------------------------------------ |
| [e.g., Code split heavy component]     | [LCP -0.XXs]     | [Low/Med/High] | [P0/P1/P2] | ☐ Planned / 🟡 In Progress / ✅ Done |
| [e.g., Image optimization (WebP/AVIF)] | [LCP -0.XXs]     | [Low/Med/High] | [P0/P1/P2] | ☐ Planned / 🟡 In Progress / ✅ Done |

---

## 7. Sign-Off

| Role          | Name | Signature | Date       |
| ------------- | ---- | --------- | ---------- |
| Test Lead     |      |           | YYYY-MM-DD |
| Frontend Lead |      |           | YYYY-MM-DD |
| CTO           |      |           | YYYY-MM-DD |
