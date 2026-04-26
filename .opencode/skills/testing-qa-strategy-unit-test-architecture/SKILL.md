---
name: testing-qa-strategy-unit-test-architecture
description: Unit test architecture for mobile — test directory structure, naming conventions, test double patterns (mocks, stubs, fakes), domain layer test isolation, data layer test strategies, and test maintainability standards for Android, iOS, and KMP projects. Owned by Ananya Krishnan (SDET). Use during Stage 4 (Implementation Plan) for test architecture design and Stage 5 (Development) for unit test implementation. Trigger: unit test architecture, test directory structure, test naming conventions, test doubles, domain layer tests, data layer tests, test maintainability, mobile unit tests.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
---

# Unit Test Architecture

## Overview

Unit test architecture defines the structure, organization, patterns, and tooling for testing individual components in isolation. A well-designed test architecture ensures tests are maintainable, fast, reliable, and provide meaningful coverage of business logic. This skill covers directory structures, naming conventions, DI patterns, mock framework selection, test data management, and CI/CD integration across all platforms.

## Test Pyramid Foundation

| Test Level  | Scope                  | Speed         | Cost      | Reliability | Owner             |
| ----------- | ---------------------- | ------------- | --------- | ----------- | ----------------- |
| Unit        | Single class/function  | < 1s each     | Near zero | Very high   | Developers        |
| Integration | Component interactions | 1-10s each    | Low       | High        | Developers + SDET |
| E2E         | Full user journeys     | 30s-5min each | High      | Moderate    | SDET team         |

**Target distribution**: 60-75% unit tests, 20-30% integration tests, 5-10% E2E tests.

## Directory Structure Patterns

| Approach                              | Best For              | Pros                                  | Cons                               |
| ------------------------------------- | --------------------- | ------------------------------------- | ---------------------------------- |
| **Mirror (test mirrors src)**         | Android, iOS          | Easy to find tests, clear mapping     | Can become deeply nested           |
| **Co-located (\_test beside source)** | Go, Python            | Tests next to code, natural discovery | Clutters source directory          |
| **Feature-based**                     | TCA, Compose          | Tests align with feature boundaries   | Requires feature module discipline |
| **Layer-based**                       | Layered architectures | Clear separation of concerns          | May split related tests            |

## Naming Conventions

| Platform       | Test Class Pattern      | Test Method Pattern                                     |
| -------------- | ----------------------- | ------------------------------------------------------- |
| Android/Kotlin | `{ClassName}Test`       | `given{Precondition}_when{Action}_then{ExpectedResult}` |
| iOS/Swift      | `{ClassName}Tests`      | `test_{description_of_behavior}`                        |
| Go             | `{package}_test` (file) | `{action}_returns{result}` (table-driven)               |
| Python/pytest  | `test_{module}.py`      | `test_{description_of_behavior}`                        |

## Dependency Injection for Testability

- **Android**: Hilt with `@TestInstallIn` for swapping production modules with test doubles.
- **iOS**: The Composable Architecture with `@Dependency` for mock injection in `TestStore`.
- **Go**: Constructor injection — pass interfaces, not concrete types.
- **Python**: pytest fixtures with `monkeypatch` for dependency override.

## Mock Framework Selection

| Platform       | Framework                   | Type            | Best For                                       |
| -------------- | --------------------------- | --------------- | ---------------------------------------------- |
| Android/Kotlin | MockK                       | Dynamic mocking | Any Kotlin class, objects, extension functions |
| Android/Kotlin | Turbine                     | Flow testing    | Kotlin Flow/Coroutine streams                  |
| iOS/Swift      | Hand-written test doubles   | Manual          | Swift structs, TCA, value types                |
| Go             | gomock                      | Code generation | Interfaces                                     |
| Python         | unittest.mock / pytest-mock | Built-in        | General mocking                                |

## CI/CD Integration

- Run unit tests on every PR, before merge.
- Coverage thresholds: block merge if below 80% line coverage.
- Flaky test detection: auto-quarantine tests with >5% flakiness rate.
- Parallel execution: shard tests by code ownership or historical timing.
