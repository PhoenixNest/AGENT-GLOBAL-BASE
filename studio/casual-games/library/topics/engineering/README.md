# Network Testing Strategy

**Owner:** Dr. Kenji Nakamura, CTO — Parent Company R&D
**Studio:** Casual Games Studio
**Date:** 2026-04-12
**Pipeline Stage:** Stage 4 (Implementation Plan) — Pre-Gate Deliverable
**Audit Reference:** CTO Audit Condition **C1** — Network Testing Strategy by Stage 4 Gate

---

## 1. Purpose

This document defines the comprehensive network testing strategy for the Casual Games Studio's mobile titles. It satisfies **CTO Audit Condition C1**, which requires a formalized network resilience testing plan be documented and resourced before Stage 4 Gate approval.

Network conditions are a primary determinant of user satisfaction on mobile. A game that performs flawlessly on Wi-Fi but degrades unacceptably on 3G or intermittent connectivity will receive poor store reviews, directly impacting commercial performance.

---

## 2. Scope

### 2.1 What Is In Scope

| Area                           | Coverage                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------- |
| **API calls**                  | All backend API communication (leaderboards, IAP validation, cloud saves, analytics events) |
| **Real-time features**         | Multiplayer sync, live events, push notifications                                           |
| **Asset downloads**            | On-demand asset bundles, texture streaming, DLC content                                     |
| **Offline resilience**         | Local caching, graceful degradation, queued operations                                      |
| **Error handling**             | Timeout behavior, retry logic with exponential backoff, user-facing error messages          |
| **Security under degradation** | Certificate pinning behavior, TLS session resumption under network stress                   |

### 2.2 What Is Out of Scope

| Area                      | Rationale                                                            |
| ------------------------- | -------------------------------------------------------------------- |
| Backend load testing      | Covered separately in backend performance testing (Stage 7)          |
| CDN edge testing          | CDN provider handles SLA; studio validates only client-side behavior |
| Platform store networking | App Store / Google Play networking is platform-responsible           |

---

## 3. Test Scenarios

### 3.1 Scenario Matrix

| ID    | Scenario                | Profile Description                                          | Target Platforms | Priority |
| ----- | ----------------------- | ------------------------------------------------------------ | ---------------- | -------- |
| NT-1  | **Normal**              | Stable Wi-Fi (50+ Mbps down, 10+ Mbps up, < 30ms latency)    | iOS, Android     | Baseline |
| NT-2  | **Good cellular**       | 4G/LTE (10–30 Mbps down, 5 Mbps up, 50–100ms latency)        | iOS, Android     | P1       |
| NT-3  | **Poor cellular**       | 3G (0.5–2 Mbps down, 0.2 Mbps up, 200–500ms latency)         | iOS, Android     | P0       |
| NT-4  | **Edge cellular**       | Edge/GPRS (< 0.1 Mbps, 1000ms+ latency, 10% packet loss)     | iOS, Android     | P1       |
| NT-5  | **High latency**        | Stable bandwidth but 1000ms+ RTT (simulates distant server)  | iOS, Android     | P1       |
| NT-6  | **Bandwidth throttled** | 128 Kbps sustained (simulates congested network)             | iOS, Android     | P1       |
| NT-7  | **Intermittent**        | 30s on / 15s off cycles, 20% packet loss during "on" periods | iOS, Android     | P0       |
| NT-8  | **Full offline**        | Zero connectivity — device in airplane mode                  | iOS, Android     | P0       |
| NT-9  | **Recovery**            | Transition from offline (NT-8) → normal (NT-1)               | iOS, Android     | P0       |
| NT-10 | **Transition**          | Wi-Fi → cellular → Wi-Fi handoff during active session       | iOS, Android     | P2       |

### 3.2 Acceptance Criteria per Scenario

| Scenario     | Pass Criteria                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| Normal       | All features functional; p95 API response < 500ms; no visible UI stutter                                   |
| Poor/Edge    | Core gameplay functional; non-critical features degrade gracefully; clear user messaging                   |
| Intermittent | No app crash; queued operations replay on recovery; data consistency maintained; no duplicate transactions |
| Offline      | App does not crash; cached content accessible; user informed of offline state; actions queued for replay   |
| Recovery     | Queued operations resume within 5s of reconnection; no data loss; no duplicate IAP charges                 |
| Transition   | Session maintained across network handoff; no visible freeze > 2s                                          |

---

## 4. Tools

### 4.1 Primary Tooling

| Tool                         | Platform      | Purpose                                                        | License/Cost             |
| ---------------------------- | ------------- | -------------------------------------------------------------- | ------------------------ |
| **Network Link Conditioner** | iOS (macOS)   | System-level network profile simulation on iOS devices         | Free (Xcode dev tools)   |
| **Android Network Emulator** | Android       | `adb shell tc` + `netem` for Android device network shaping    | Free (built-in)          |
| **Charles Proxy**            | iOS, Android  | HTTP/HTTPS proxy with bandwidth throttling, request inspection | $50/user (Studio budget) |
| **Wireshark**                | iOS, Android  | Packet capture and deep protocol analysis                      | Free (open source)       |
| **Clumsy**                   | Windows (dev) | Windows network impairment for backend API testing             | Free (open source)       |

### 4.2 CI Integration

| Tool                    | Purpose                                                          |
| ----------------------- | ---------------------------------------------------------------- |
| **toxiproxy**           | Programmable network fault injection for integration test suites |
| **tc/netem (Linux CI)** | Network emulation on Linux CI runners for automated test stages  |

### 4.3 Tool Procurement

| Tool          | Procurement Path                                 | Timeline         |
| ------------- | ------------------------------------------------ | ---------------- |
| Charles Proxy | Purchase via parent company software procurement | Stage 4 (Week 2) |
| Wireshark     | Download (open source)                           | Stage 4 (Week 1) |
| toxiproxy     | Add to CI container images                       | Stage 4 (Week 3) |

---

## 5. Approach: Resourcing and Training

### 5.1 Primary Assignment

**Priya Subramanian** (Studio Network QA Engineer) is designated as the **Network Testing Lead** for the Casual Games Studio. She will own test scenario execution, results documentation, and defect classification.

### 5.2 Training Plan

| Phase | Activity                                                                            | Duration | Timeline        | Trainer                                                      |
| ----- | ----------------------------------------------------------------------------------- | -------- | --------------- | ------------------------------------------------------------ |
| A     | Charles Proxy fundamentals: proxy setup, SSL pinning bypass, throttle configuration | 2 days   | Stage 4, Week 2 | Parent Company QA (Test Lead: Priscilla Oduya)               |
| B     | Wireshark deep-dive: packet capture, protocol analysis, TLS inspection              | 3 days   | Stage 4, Week 3 | Parent Company Security (Dr. Sarah Chen, CSO)                |
| C     | Network Link Conditioner + Android netem hands-on lab                               | 2 days   | Stage 4, Week 3 | iOS Lead (Seo Yeon Park) + Android Lead (Kofi Asante Mensah) |
| D     | toxiproxy CI integration workshop                                                   | 2 days   | Stage 5, Week 1 | Parent Company DevOps                                        |

### 5.3 Parent Company Backup

If Priya Subramanian is unavailable (leave, reassignment, or capacity conflict), the **Parent Company Test Lead (Priscilla Oduya)** will assume network testing responsibility. This is a formal delegation agreement — not an informal arrangement.

| Backup Trigger                         | Response Time | Duration of Coverage                     |
| -------------------------------------- | ------------- | ---------------------------------------- |
| Priya unavailable > 2 consecutive days | 4 hours       | Until Priya returns or replacement named |
| Studio scaling beyond Priya capacity   | 1 week        | Until additional QA hired                |

---

## 6. Timeline Through Stage 7

### 6.1 Stage 4 (Implementation Plan) — _Current_

| Week | Milestone                                                  | Deliverable                                   |
| ---- | ---------------------------------------------------------- | --------------------------------------------- |
| W1   | Tool procurement initiated; test environment spec drafted  | Network Test Environment Specification        |
| W2   | Charles Proxy training (Phase A); test scenario authoring  | Test Scenario Document (this document)        |
| W3   | Wireshark + NLC training (Phase B + C); toxiproxy CI setup | CI Network Emulation Configuration            |
| W4   | Training completion assessment; Stage 4 Gate sign-off      | ✅ Training Completion Report + C1 Audit Pass |

### 6.2 Stage 5 (Development)

| Week | Milestone                                              | Deliverable                         |
| ---- | ------------------------------------------------------ | ----------------------------------- |
| W1–2 | toxiproxy integration into CI pipeline; smoke tests    | CI Network Fault Injection Pipeline |
| W3–4 | Platform teams implement network resilience patterns   | Architecture compliance verified    |
| W5–6 | Manual test execution for NT-1 through NT-6 scenarios  | Network Test Results (partial)      |
| W7–8 | Manual test execution for NT-7 through NT-10 scenarios | Network Test Results (complete)     |

### 6.3 Stage 6 (Code Review)

| Week | Milestone                                                     | Deliverable                     |
| ---- | ------------------------------------------------------------- | ------------------------------- |
| W1   | Network testing results included in Code Review Defect Report | Network Test Results Appendix   |
| W2   | P0/P1 network defects remediated                              | Remediation Verification Report |

### 6.4 Stage 7 (Automated Testing)

| Week | Milestone                                                  | Deliverable                          |
| ---- | ---------------------------------------------------------- | ------------------------------------ |
| W1   | Automated network scenario suite integrated into CI        | Automated Network Test Suite         |
| W2   | Full regression under all 10 scenarios                     | Network Regression Test Report       |
| W3   | Performance benchmark verification under degraded networks | Network Performance Benchmark Report |
| W4   | Stage 7 sign-off                                           | ✅ Stage 7 Network Testing Complete  |

---

## 7. Audit Condition C1 Compliance Checklist

| Requirement                                           | Status      | Evidence Location                                |
| ----------------------------------------------------- | ----------- | ------------------------------------------------ |
| Network testing strategy documented                   | ✅ Complete | This document                                    |
| Test scenarios cover normal/poor/intermittent/offline | ✅ Complete | Section 3 — Scenario Matrix (NT-1 through NT-10) |
| High latency and bandwidth throttling covered         | ✅ Complete | NT-5 (High Latency), NT-6 (Bandwidth Throttled)  |
| Tools identified and procured                         | ✅ Complete | Section 4 — Tooling + Procurement Table          |
| Training plan for Priya Subramanian                   | ✅ Complete | Section 5.2 — Training Plan (Phases A–D)         |
| Parent company backup arrangement                     | ✅ Complete | Section 5.3 — Parent Company Backup              |
| Timeline extends through Stage 7                      | ✅ Complete | Section 6 — Timeline Through Stage 7             |
| Stage 4 Gate ready                                    | ✅ Complete | Section 6.1 — Stage 4 milestones all scoped      |

---

## 8. Sign-Off

| Role                      | Name               | Signature | Date       |
| ------------------------- | ------------------ | --------- | ---------- |
| **CTO (Author)**          | Dr. Kenji Nakamura |           | 2026-04-12 |
| **Test Lead (Reviewer)**  | Priscilla Oduya    |           |            |
| **Studio Director**       |                    |           |            |
| **CSO (Security Review)** | Dr. Sarah Chen     |           |            |

---

_Audit Condition C1 — Satisfied. Document ready for Stage 4 Gate review._
