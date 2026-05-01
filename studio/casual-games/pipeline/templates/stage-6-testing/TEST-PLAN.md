# Test Plan — Template

> **Stage:** 6 — Automated Testing
> **Producer:** SDET Gameplay (Lead QA Engineer)
> **User Approval:** ✅ Required before advancing to Stage 7

---

## Document Control

| Field             | Value              |
| :---------------- | :----------------- |
| **Game Title**    | [Working title]    |
| **Build Version** | [vX.X.X]           |
| **Date**          | YYYY-MM-DD         |
| **Author**        | [Lead QA Engineer] |

---

## 1. Test Scope

### 1.1 In-Scope Features

| Feature             | Test Type               | Automation Target |
| :------------------ | :---------------------- | :---------------: |
| [Core mechanic]     | Functional + regression |       ≥ 90%       |
| [Economy system]    | Functional + security   |       ≥ 95%       |
| [IAP flow]          | Functional + edge case  |       100%        |
| [Level progression] | Regression              |       ≥ 80%       |
| [Ad integration]    | Integration             |       ≥ 80%       |

### 1.2 Out-of-Scope (This Stage)

- Live ops system (tested in Stage 8)
- Store listing metadata
- Localisation (tested in Stage 9)

---

## 2. Automation Targets

| Test Category         | Planned Count  | Automation % Target | Framework              |
| :-------------------- | :------------: | :-----------------: | :--------------------- |
| Unit tests            |      [N]       |        ≥ 90%        | [Unity Test Framework] |
| Integration tests     |      [N]       |        ≥ 80%        | [Framework]            |
| UI / gameplay tests   |      [N]       |        ≥ 70%        | [Framework]            |
| Performance tests     |      [N]       |        100%         | [Profiler + custom]    |
| Security tests (SAST) | Automated scan |        100%         | [Tool]                 |

**Overall automation target:** ≥ 80% of planned tests automated

---

## 3. Performance Test Benchmarks

| Metric                        |  Target  | Minimum Device        | Test Method        |
| :---------------------------- | :------: | :-------------------- | :----------------- |
| Cold start                    |  < [X]s  | [Low-end spec device] | Automated timing   |
| Steady-state FPS              | ≥ 30 fps | [Low-end spec device] | Profiler run       |
| Peak memory                   | < [X] MB | [Low-end spec device] | Memory profiler    |
| Battery drain per 10 min      |  < [X]%  | [Mid-range device]    | Device measurement |
| Network payload (match start) | < [X] KB | N/A                   | Network profiler   |

---

## 4. Security Test Scope

| Test Type                   | Tool                     | Target                         |
| :-------------------------- | :----------------------- | :----------------------------- |
| Static analysis (SAST)      | [Tool]                   | Zero high-severity findings    |
| IAP receipt validation test | Manual + automated       | 100% server-validated          |
| Currency economy integrity  | Automated injection test | No client-side grants possible |
| API rate limiting           | Automated stress test    | Rate limits enforced           |
| Certificate pinning         | Manual validation        | Payment endpoints pinned       |

---

## 5. Device Test Matrix

| Device Category     | OS          | Example           | Test Type       |
| :------------------ | :---------- | :---------------- | :-------------- |
| iOS — Low end       | iOS [X]     | iPhone SE (Gen 3) | Full regression |
| iOS — Mid range     | iOS [X]     | iPhone 14         | Full regression |
| iOS — Latest        | iOS [X]     | iPhone 16         | Smoke           |
| Android — Low end   | Android [X] | [Budget device]   | Full regression |
| Android — Mid range | Android [X] | [Mid device]      | Full regression |
| Android — Latest    | Android [X] | [Flagship]        | Smoke           |

---

## 6. Test Environment

| Environment | Purpose                       | Data                |
| :---------- | :---------------------------- | :------------------ |
| Development | Unit tests, local integration | Synthetic           |
| Staging     | Full regression, performance  | Sanitised prod-like |
| Device farm | Device matrix testing         | Synthetic           |

---

## 7. Exit Criteria (Stage 6 Gate)

| Criterion                       |   Required    | Actual | Pass? |
| :------------------------------ | :-----------: | :----: | :---: |
| Overall pass rate               |     100%      |        |   ☐   |
| Zero P0/P1 defects open         | 100% resolved |        |   ☐   |
| Performance benchmarks met (§3) |   All pass    |        |   ☐   |
| Security SAST findings          |   Zero high   |        |   ☐   |
| IAP validation tests            |   100% pass   |        |   ☐   |
| DAST high findings              |     Zero      |        |   ☐   |

---

**Produced by:** [Lead QA Engineer] on YYYY-MM-DD
**Approved by:** [Studio Director] on YYYY-MM-DD
