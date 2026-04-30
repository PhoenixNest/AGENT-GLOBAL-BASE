---
name: studio-qa-mobile-game-testing
description: Mobile game QA strategy and execution for Android and iOS — test plan authorship, device matrix management, regression testing, launch readiness verification, and exploratory testing for casual game features. Owned by Amara Osei (Lead QA Engineer). Trigger: mobile QA, game testing, device testing, regression testing, test plan, QA strategy, launch readiness.
version: "1.0.0"
---

# Mobile Game Testing

**Skill Owner:** Amara Osei (Lead QA Engineer)
**Applies To:** Android/iOS QA, Feature Testing, Regression Testing, Launch Readiness

## Tools & Frameworks

| Tool/Framework       | Version Context | Usage                                            |
| -------------------- | --------------- | ------------------------------------------------ |
| Unity Test Runner    | Built-in        | Unit and integration test execution in-engine    |
| Appium               | 2.x             | UI automation for Android and iOS                |
| Firebase Test Lab    | Latest          | Cloud device testing across real Android devices |
| TestFlight           | Latest          | iOS beta distribution and testing                |
| JIRA                 | Latest          | Test case management, defect tracking            |
| Charles Proxy        | 4.x             | Network condition simulation and interception    |
| Android Debug Bridge | Latest          | Device communication and log collection          |

## Real-World Production Scenarios

### Scenario 1: Authoring a Test Plan for a New Feature

**Context:** New feature (e.g., season pass) entering Stage 5 development.
**Process:**

1. Review the GDD and PRD with Mei Watanabe and the Lead Designer to understand acceptance criteria
2. Identify test scope: happy path, edge cases (empty state, max capacity, offline behavior), and integration touchpoints (economy, backend)
3. Author test cases in JIRA; each case specifies: preconditions, steps, expected result, and platform matrix (iOS/Android, minimum spec device)
4. Estimate effort; flag cases requiring device farm vs. manual only
5. Agree sign-off criteria with Dmitri Volkov: minimum 95% pass rate on automated suite + all P0/P1 manual cases pass before Stage 6

### Scenario 2: Managing the Device Matrix

**Context:** New title targeting global market; QA must cover Android fragmentation and iOS versions.
**Process:**

1. Define minimum spec (e.g., Android: Pixel 4a / 3GB RAM; iOS: iPhone 11)
2. Define target spec (e.g., Android: Pixel 7 / Samsung Galaxy S22; iOS: iPhone 14)
3. For critical features, test on: minimum spec, target spec, latest flagship (iOS/Android), and the most common mid-tier device in SEA/LATAM markets (Firebase Test Lab device report)
4. Automate regression suite on Firebase Test Lab (minimum + target spec) on every nightly build
5. Manual exploratory testing focuses on flagship and minimum spec; target spec is covered by automation

### Scenario 3: Launch Readiness Verification (Stage 7)

**Context:** Soft launch approaching; QA must confirm the build is launch-ready.
**Process:**

1. Execute full regression suite; require 100% pass on P0 cases, ≥95% on P1
2. Conduct 3-day exploratory testing sprint: rotate testers across all game modes, economy flows, onboarding, and edge cases
3. Verify all analytics events fire correctly (partner with Yuki Tanaka — Data Analyst)
4. Test under real network conditions: 3G, high latency, offline → reconnect
5. Submit build to TestFlight (iOS) and closed beta track (Android); collect external feedback
6. Produce **Launch Readiness Report** with: open defect count by severity, test coverage %, device matrix results, and a PASS/FAIL recommendation

## Measurable Quality Standards

| Standard                           | Target                               | Measurement Method               |
| ---------------------------------- | ------------------------------------ | -------------------------------- |
| Automated test pass rate at launch | ≥99.5%                               | Unity Test Runner + Firebase Lab |
| P0/P1 open defects at launch       | 0                                    | JIRA defect log                  |
| Regression test coverage           | ≥80% of critical paths               | Test case traceability matrix    |
| Regression testing time            | ≤60% of manual baseline (automation) | CI/CD pipeline execution time    |
| Crash rate at soft launch          | ≤0.5% of sessions                    | Firebase Crashlytics             |

## Industry Best Practice References

- **Zynga QA Playbook** (internal reference — Amara's prior methodology)
- **Google Play Android Vitals** — Crash and ANR benchmarks
- **Apple App Store Review Guidelines** — Minimum quality bar for iOS
- **ISTQB Mobile Testing Guidelines** — Industry QA standards
