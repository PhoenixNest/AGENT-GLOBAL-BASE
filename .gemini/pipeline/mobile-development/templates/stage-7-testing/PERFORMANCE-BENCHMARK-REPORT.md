# Performance Benchmark Report

**Project:** [Project Name]
**Platform:** [Android / iOS / KMP / Flutter]
**Author:** [Platform Lead / Performance Engineer]
**Date:** YYYY-MM-DD
**Version:** v1
**Referenced Artifacts:** PRD v1 (§6 Performance Thresholds), TEST-RESULTS-REPORT.md v1

---

## Purpose

Verifies that the implemented application meets the performance SLAs defined in the PRD. This report is a **mandatory Stage 7 gate input** — all PRD performance thresholds must be verified before advancing to Stage 8.

---

## 1. PRD Performance Thresholds

| Metric                    | PRD Target | Measurement Method                           | Platform | Result   | Pass/Fail       |
| ------------------------- | ---------- | -------------------------------------------- | -------- | -------- | --------------- |
| Cold start time           | [<2s]      | [Time from tap to first interactive frame]   | Android  | [X.XXs]  | ☐ Pass / ☐ Fail |
| Cold start time           | [<2s]      | [Time from tap to first interactive frame]   | iOS      | [X.XXs]  | ☐ Pass / ☐ Fail |
| Warm start time           | [<1s]      | [Time from background resume to interactive] | Android  | [X.XXs]  | ☐ Pass / ☐ Fail |
| Warm start time           | [<1s]      | [Time from background resume to interactive] | iOS      | [X.XXs]  | ☐ Pass / ☐ Fail |
| Frame rate (scroll)       | [60fps]    | [Average fps during 30s scroll of long list] | Android  | [XX fps] | ☐ Pass / ☐ Fail |
| Frame rate (scroll)       | [60fps]    | [Average fps during 30s scroll of long list] | iOS      | [XX fps] | ☐ Pass / ☐ Fail |
| Frame rate (animation)    | [60fps]    | [Average fps during standard animation]      | Android  | [XX fps] | ☐ Pass / ☐ Fail |
| Frame rate (animation)    | [60fps]    | [Average fps during standard animation]      | iOS      | [XX fps] | ☐ Pass / ☐ Fail |
| Memory usage (idle)       | [<150MB]   | [RSS after 60s idle on home screen]          | Android  | [XX MB]  | ☐ Pass / ☐ Fail |
| Memory usage (idle)       | [<150MB]   | [RSS after 60s idle on home screen]          | iOS      | [XX MB]  | ☐ Pass / ☐ Fail |
| Memory usage (peak)       | [<300MB]   | [Max RSS during heaviest user flow]          | Android  | [XX MB]  | ☐ Pass / ☐ Fail |
| Memory usage (peak)       | [<300MB]   | [Max RSS during heaviest user flow]          | iOS      | [XX MB]  | ☐ Pass / ☐ Fail |
| Network payload (cold)    | [<500KB]   | [Total bytes transferred on first launch]    | Both     | [XXX KB] | ☐ Pass / ☐ Fail |
| Network payload (typical) | [<100KB]   | [Total bytes per typical API call]           | Both     | [XXX KB] | ☐ Pass / ☐ Fail |

---

## 2. Benchmark Methodology

| Parameter             | Value                                                              |
| --------------------- | ------------------------------------------------------------------ |
| **Device (Android)**  | [Device model, Android version, RAM]                               |
| **Device (iOS)**      | [Device model, iOS version]                                        |
| **Network condition** | [WiFi / 4G / 3G — specify latency and bandwidth]                   |
| **Measurement tools** | [Android: Profiler / Perfetto; iOS: Instruments / Xcode Organizer] |
| **Sample size**       | [N runs per metric]                                                |
| **Baseline version**  | [App version / commit hash]                                        |

---

## 3. Performance Regression Comparison

| Metric                | Previous Benchmark | Current Benchmark | Delta      | Trend     |
| --------------------- | ------------------ | ----------------- | ---------- | --------- |
| Cold start (Android)  | [X.XXs]            | [X.XXs]           | [+/- X%]   | ↑ / ↓ / → |
| Cold start (iOS)      | [X.XXs]            | [X.XXs]           | [+/- X%]   | ↑ / ↓ / → |
| FPS (Android)         | [XX fps]           | [XX fps]          | [+/- X]    | ↑ / ↓ / → |
| FPS (iOS)             | [XX fps]           | [XX fps]          | [+/- X]    | ↑ / ↓ / → |
| Memory idle (Android) | [XX MB]            | [XX MB]           | [+/- X MB] | ↑ / ↓ / → |
| Memory idle (iOS)     | [XX MB]            | [XX MB]           | [+/- X MB] | ↑ / ↓ / → |

---

## 4. Pass/Fail Summary

| Platform  | Total Metrics | Pass    | Fail    | Pass Rate |
| --------- | ------------- | ------- | ------- | --------- |
| Android   | [N]           | [N]     | [N]     | [XX]%     |
| iOS       | [N]           | [N]     | [N]     | [XX]%     |
| **Total** | **[N]**       | **[N]** | **[N]** | **[XX]%** |

**Gate criterion:** 100% of PRD performance thresholds must pass. Any failed metric is classified as at minimum a **P1 defect** (major UX failure) if it exceeds the threshold by >20%, or **P2** if within 20%.

---

## 5. Recommendations

| Failed Metric | Root Cause | Remediation | Estimated Effort | Owner  |
| ------------- | ---------- | ----------- | ---------------- | ------ |
| [Metric]      | [Cause]    | [Action]    | [S/M/L]          | [Name] |

---

**Reviewed by CTO (Dr. Kenji Nakamura) on YYYY-MM-DD**
**Reviewed by CPO (Marcus Tran-Yoshida) on YYYY-MM-DD**
