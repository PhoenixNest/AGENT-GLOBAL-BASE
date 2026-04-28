---
name: ios-infrastructure-ios-ci-cd
description: "iOS CI/CD pipelines — Xcode Cloud configuration, Fastlane automation (Match, Gym, Pilot), TestFlight distribution, Crashlytics crash reporting, SwiftLint enforcement, and build time optimization. Owned by Seo-Yeon Park (iOS Lead). Use during Stage 5 (Development) for build infrastructure setup and Stage 10 (Release Readiness) for release pipeline validation. Trigger: xcode cloud, fastlane, match, gym, pilot, testflight, crashlytics, swiftlint, ci/cd, dsym upload, beta distribution, app store upload."
prerequisites:
  - ios-infrastructure-ios-implementation

version: "1.0.0"
---

# iOS CI/CD

**Category:** Mobile Engineering — iOS DevOps
**Owner:** Senior iOS Engineer (Amara Diallo)

## Overview

This skill establishes continuous integration and delivery pipelines for iOS applications covering Xcode Cloud configuration, Fastlane automation, TestFlight distribution, crash reporting with Crashlytics, and CI/CD workflow optimization. It applies to Stage 5 (Development) where build infrastructure is configured, Stage 6 (Code Review) where CI gates enforce quality, and Stage 7 (Automated Testing) where the full test suite runs in CI.

## Competency Dimensions

| Dimension               | Description                                                                                                       | Proficiency Indicators                                                                                            |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Xcode Cloud             | CI workflow definition, build configurations, environment variables, artifact management, parallel test execution | Workflows defined in ci_scripts; build completes <15 minutes; test results published; artifacts archived          |
| Fastlane Automation     | Match code signing, Gym build, Pilot upload, Snapshot screenshots, custom lanes, plugin management                | Code signing automated via Match; one-command build and upload; screenshot automation; lane composition           |
| TestFlight Distribution | Beta group management, build metadata, release notes automation, tester feedback integration, expiration handling | Beta builds distributed within 10 minutes of merge; tester groups auto-managed; feedback integrated into tracking |
| Crash Reporting         | Firebase Crashlytics, dSYM upload, custom keys, NDK crash handling, ANR monitoring, breadcrumb logging            | Crash-free rate >99.5%; dSYMs automatically uploaded; all crashes have actionable context                         |
| CI/CD Optimization      | Build caching, dependency pre-warming, incremental builds, parallel test sharding, workflow triggers              | CI build time <15 minutes; test suite <30 minutes; caching effective across runs; workflow triggers optimized     |

## Pipeline Integration

- **Stage 4 (Implementation Plan):** CI/CD pipeline configuration is a task in the implementation plan with estimated effort for each workflow.
- **Stage 5 (Development):** Build infrastructure configured alongside feature development. Fastlane lanes created incrementally.
- **Stage 6 (Code Review):** CI gates enforce SwiftLint, build success, and unit test pass rate. PRs cannot merge without passing CI.
- **Stage 7 (Automated Testing):** Full test suite (unit + UI) runs in CI. Test results archived and published.
- **Stage 10 (Release Readiness):** Release build artifacts produced by CI pipeline. Crash-free rate verified via Crashlytics dashboard.

## Quality Standards

- CI build time **<15 minutes** (build + all tests)
- Unit test execution **<10 minutes** in CI
- Beta releases distributed to TestFlight within **10 minutes** of merge to develop
- **100%** PRs pass SwiftLint checks before merge
- SwiftLint `force_unwrapping` set to **error** — no force unwraps allowed
- dSYMs **automatically uploaded** to Crashlytics on every build
- Crash-free user rate **>99.5%** (measured over rolling 28-day window)
- Code signing fully automated via **Match** — no manual certificate management
- Fastlane lanes are **composable** — `ci` lane = lint + test + build + beta
- TestFlight beta groups **auto-managed** — no manual tester management
- Release builds use **phased rollout** — 1% → 2% → 5% → 10% → 20% → 50% → 100%
- CI environment variables for all secrets — **zero** credentials in repository

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
