# Performance Benchmark Report

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Pipeline:** Full-Stack Cross-Platform (P3)
**Stage:** 7 — Automated Testing

---

## 1. Cross-Platform Performance Parity

This report verifies that performance targets are met on **all platforms** and that no single platform is a significant outlier compared to others.

### 1.1 Feature-Level Parity Comparison

| User Journey | Web (LCP) | iOS (Cold Start) | Android (Cold Start) | Backend (P99) | Parity Pass? |
| ------------ | --------- | ---------------- | -------------------- | ------------- | ------------ |
| App launch   | [X.XXs]   | [X.XXs]          | [X.XXs]              | [Xms]         | ☐ Yes / ☐ No |
| [Core flow]  | [X.XXs]   | [X.XXs]          | [X.XXs]              | [Xms]         | ☐ Yes / ☐ No |
| [Checkout]   | [X.XXs]   | [X.XXs]          | [X.XXs]              | [Xms]         | ☐ Yes / ☐ No |

**Parity threshold:** No platform should be >2x slower than the fastest platform for the same user journey.

### 1.2 Platform-Specific Performance Metrics

#### Web Frontend (Lighthouse CI)

| Metric      | PRD Target     | Chrome | Firefox | Safari | Pass/Fail       |
| ----------- | -------------- | ------ | ------- | ------ | --------------- |
| LCP         | <2.5s          | [X.XX] | [X.XX]  | [X.XX] | ☐ / ☐ / ☐       |
| CLS         | <0.1           | [X.XX] | [X.XX]  | [X.XX] | ☐ / ☐ / ☐       |
| TTFB        | <800ms         | [Xms]  | [Xms]   | [Xms]  | ☐ / ☐ / ☐       |
| TTI         | <3.8s          | [X.XX] | [X.XX]  | [X.XX] | ☐ / ☐ / ☐       |
| Bundle size | <200KB gzipped | [XX]KB | —       | —      | ☐ Pass / ☐ Fail |

#### iOS (Xcode Instruments)

| Metric              | PRD Target | iPhone [model] | iPad [model] | Pass/Fail |
| ------------------- | ---------- | -------------- | ------------ | --------- |
| Cold start          | <2s        | [X.XXs]        | [X.XXs]      | ☐ / ☐     |
| Warm start          | <1s        | [X.XXs]        | [X.XXs]      | ☐ / ☐     |
| Frame rate (scroll) | 60fps      | [XX]fps        | [XX]fps      | ☐ / ☐     |
| Memory (idle)       | <150MB     | [XX]MB         | [XX]MB       | ☐ / ☐     |

#### Android (Android Profiler / Perfetto)

| Metric              | PRD Target | [Device model] | [Device model] | Pass/Fail |
| ------------------- | ---------- | -------------- | -------------- | --------- |
| Cold start          | <2s        | [X.XXs]        | [X.XXs]        | ☐ / ☐     |
| Warm start          | <1s        | [X.XXs]        | [X.XXs]        | ☐ / ☐     |
| Frame rate (scroll) | 60fps      | [XX]fps        | [XX]fps        | ☐ / ☐     |
| Memory (idle)       | <150MB     | [XX]MB         | [XX]MB         | ☐ / ☐     |

#### Backend API (k6)

| Metric                      | PRD Target | Result  | Pass/Fail       |
| --------------------------- | ---------- | ------- | --------------- |
| P99 latency                 | <200ms     | [Xms]   | ☐ Pass / ☐ Fail |
| P95 latency                 | <150ms     | [Xms]   | ☐ Pass / ☐ Fail |
| Throughput                  | >10k rps   | [X] rps | ☐ Pass / ☐ Fail |
| Error rate                  | <0.1%      | [X]%    | ☐ Pass / ☐ Fail |
| DB query P99                | <50ms      | [Xms]   | ☐ Pass / ☐ Fail |
| Cache hit rate              | >90%       | [XX]%   | ☐ Pass / ☐ Fail |
| Connection pool utilization | <80%       | [XX]%   | ☐ Pass / ☐ Fail |

---

## 2. Shared Backend Bottleneck Analysis

The backend API serves all platforms (web + mobile). This section verifies that the backend is not a bottleneck for any single consumer.

### 2.1 Per-Consumer Load Distribution

| Consumer         | % of Total Requests | P99 for This Consumer | Pass/Fail       |
| ---------------- | ------------------- | --------------------- | --------------- |
| Web Frontend     | [XX]%               | [Xms]                 | ☐ Pass / ☐ Fail |
| iOS App          | [XX]%               | [Xms]                 | ☐ Pass / ☐ Fail |
| Android App      | [XX]%               | [Xms]                 | ☐ Pass / ☐ Fail |
| Third-party APIs | [XX]%               | [Xms]                 | ☐ Pass / ☐ Fail |

### 2.2 Backend Under Full Load

| Metric             | At 1x Load | At 5x Load | At 10x Load | Degradation Point |
| ------------------ | ---------- | ---------- | ----------- | ----------------- |
| P99 latency        | [Xms]      | [Xms]      | [Xms]       | [Xx load]         |
| Error rate         | [X]%       | [X]%       | [X]%        | [Xx load]         |
| DB connection pool | [XX]%      | [XX]%      | [XX]%       | [XX]%             |
| Cache hit rate     | [XX]%      | [XX]%      | [XX]%       | [XX]%             |

---

## 3. Performance Regression Comparison

### 3.1 Web Performance

| Metric       | Baseline | Current | Delta    | Trend     |
| ------------ | -------- | ------- | -------- | --------- |
| LCP (Chrome) | [X.XXs]  | [X.XXs] | [+/- X%] | ↑ / ↓ / → |
| CLS (Chrome) | [X.XX]   | [X.XX]  | [+/- X%] | ↑ / ↓ / → |
| TTI (Chrome) | [X.XXs]  | [X.XXs] | [+/- X%] | ↑ / ↓ / → |
| Bundle size  | [XX]KB   | [XX]KB  | [+/- X%] | ↑ / ↓ / → |

### 3.2 iOS Performance

| Metric        | Baseline | Current | Delta    | Trend     |
| ------------- | -------- | ------- | -------- | --------- |
| Cold start    | [X.XXs]  | [X.XXs] | [+/- X%] | ↑ / ↓ / → |
| FPS (scroll)  | [XX]fps  | [XX]fps | [+/- X]  | ↑ / ↓ / → |
| Memory (idle) | [XX]MB   | [XX]MB  | [+/- X%] | ↑ / ↓ / → |

### 3.3 Android Performance

| Metric        | Baseline | Current | Delta    | Trend     |
| ------------- | -------- | ------- | -------- | --------- |
| Cold start    | [X.XXs]  | [X.XXs] | [+/- X%] | ↑ / ↓ / → |
| FPS (scroll)  | [XX]fps  | [XX]fps | [+/- X]  | ↑ / ↓ / → |
| Memory (idle) | [XX]MB   | [XX]MB  | [+/- X%] | ↑ / ↓ / → |

### 3.4 Backend Performance

| Metric      | Baseline | Current | Delta    | Trend     |
| ----------- | -------- | ------- | -------- | --------- |
| P99 latency | [Xms]    | [Xms]   | [+/- X%] | ↑ / ↓ / → |
| Throughput  | [X] rps  | [X] rps | [+/- X%] | ↑ / ↓ / → |
| Error rate  | [X]%     | [X]%    | [+/- X%] | ↑ / ↓ / → |

---

## 4. Platform Parity Summary

| Platform | Performance Pass/Fail | Within Parity Threshold? | Notes   |
| -------- | --------------------- | ------------------------ | ------- |
| Web      | ☐ Pass / ☐ Fail       | ☐ Yes / ☐ No             | [Notes] |
| iOS      | ☐ Pass / ☐ Fail       | ☐ Yes / ☐ No             | [Notes] |
| Android  | ☐ Pass / ☐ Fail       | ☐ Yes / ☐ No             | [Notes] |
| Backend  | ☐ Pass / ☐ Fail       | ☐ Yes / ☐ No             | [Notes] |

**Overall parity:** ☐ Pass (all platforms within 2x of fastest) / ☐ Fail (platform divergence detected)

---

## 5. Benchmark Methodology

| Parameter               | Value                                                                      |
| ----------------------- | -------------------------------------------------------------------------- |
| **Web browsers**        | Chrome [N], Firefox [N], Safari [N] — headless via Playwright              |
| **iOS devices**         | iPhone [model] (iOS [N]), iPad [model] (iPadOS [N])                        |
| **Android devices**     | [Device model] (Android [N]), [Device model] (Android [N])                 |
| **Backend environment** | [ECS/K8s], [instance type], [DB instance], [Redis instance]                |
| **Web measurement**     | Lighthouse CI, WebPageTest, Chrome DevTools                                |
| **iOS measurement**     | Xcode Instruments (Time Profiler, Allocations, Leaks)                      |
| **Android measurement** | Android Profiler, Perfetto, Macrobenchmark                                 |
| **Backend measurement** | k6 (load profile: ramp-up 60s, sustain 300s, ramp-down 30s)                |
| **Network throttling**  | Web: 3G throttled (1.6Mbps down, 750Kbps up); Mobile: real device on Wi-Fi |

---

## 6. Optimization Opportunities

| Opportunity                    | Platform | Estimated Impact  | Effort | Priority | Status                               |
| ------------------------------ | -------- | ----------------- | ------ | -------- | ------------------------------------ |
| [e.g., Code split heavy route] | Web      | LCP -0.XXs        | Low    | P1       | ☐ Planned / 🟡 In Progress / ✅ Done |
| [e.g., Reduce image payload]   | Web      | Bundle -XX KB     | Low    | P2       | ☐ Planned / 🟡 In Progress / ✅ Done |
| [e.g., Lazy-load iOS view]     | iOS      | Cold start -0.XXs | Med    | P1       | ☐ Planned / 🟡 In Progress / ✅ Done |
| [e.g., Optimize RecyclerView]  | Android  | FPS +XXfps        | Med    | P2       | ☐ Planned / 🟡 In Progress / ✅ Done |
| [e.g., Add Redis cache layer]  | Backend  | P99 -XXms         | High   | P0       | ☐ Planned / 🟡 In Progress / ✅ Done |

---

## 7. Sign-Off

| Role                | Name | Signature | Date       |
| ------------------- | ---- | --------- | ---------- |
| Test Lead           |      |           | YYYY-MM-DD |
| Frontend Lead (Web) |      |           | YYYY-MM-DD |
| iOS Lead            |      |           | YYYY-MM-DD |
| Android Lead        |      |           | YYYY-MM-DD |
| Backend Lead        |      |           | YYYY-MM-DD |
| CTO                 |      |           | YYYY-MM-DD |
