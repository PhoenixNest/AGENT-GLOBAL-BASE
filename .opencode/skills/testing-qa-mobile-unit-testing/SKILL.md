---
name: testing-qa-mobile-unit-testing
description: Mobile unit testing — JUnit 5 + MockK for Android, XCTest + Swift Testing for iOS, kotlin.test for KMP shared modules, test doubles, coroutine testing, and unit test architecture for mobile domain and data layers. Owned by Ananya Krishnan (SDET). Use during Stage 5 (Development) for unit test implementation and Stage 6 (Code Review) for test quality verification. Trigger: mobile unit testing, JUnit 5, MockK, XCTest, Swift Testing, kotlin.test, test doubles, coroutine testing, domain layer tests.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
---

# Mobile Unit Testing

## Overview

Unit testing is the foundation of the mobile test pyramid. This skill provides detailed guidance for writing effective unit tests across Android (Kotlin), iOS (Swift), and cross-platform (KMP/Flutter) codebases.

### Scope and Purpose

**Unit tests verify that individual functions, methods, or classes produce correct outputs for given inputs, in isolation from external dependencies.**

| Aspect              | Description                                            |
| ------------------- | ------------------------------------------------------ |
| **Scope**           | Single class, function, or module boundary             |
| **Dependencies**    | All external dependencies replaced with test doubles   |
| **Execution**       | Milliseconds per test, no I/O, no network, no database |
| **Determinism**     | Same inputs always produce same outputs                |
| **Coverage Target** | >= 80% branch coverage, >= 90% line coverage           |

### What Makes a Good Unit Test?

```
A Good Unit Test is:
├── FAST     — Executes in < 100ms
├── ISOLATED — No shared state, no order dependency
├── REPEATABLE — Same result every time, every machine
├── SELF-VALIDATING — Pass or fail, no manual inspection
├── TIMELY   — Written before or alongside production code
└── CLEAR    — Intent is obvious from reading the test name
```

### Coverage Targets

| Metric                 | Minimum Target | Rationale                                           |
| ---------------------- | -------------- | --------------------------------------------------- |
| Line Coverage          | 90%            | Most lines should be exercised                      |
| Branch Coverage        | 80%            | All if/else, when/switch paths tested               |
| Function Coverage      | 95%            | Almost every function should have at least one test |
| Critical Path Coverage | 100%           | Business logic, security, payments — no exceptions  |

**What NOT to cover:**

- Generated code (data classes, simple getters)
- Framework delegation (lifecycle methods that just call super)
- Third-party library code
- UI rendering (use dedicated UI testing tools)
- Simple property accessors

---

## Cross-Platform Unit Testing

### KMP Shared Module Testing

KMP (Kotlin Multiplatform) shared modules are tested using JUnit 5 on the JVM because shared business logic has no platform dependencies.

```kotlin
// shared/src/commonTest/kotlin/com/company/app/LoginUseCaseTest.kt
// Runs on JVM via JUnit 5

class LoginUseCaseTest {
    private val repository = FakeUserRepository()
    private val loginUseCase = LoginUseCase(repository)

    @Test
    fun `login with valid credentials returns success`() = runTest {
        val result = loginUseCase.execute("alice@example.com", "password")
        assertTrue(result.isSuccess)
        assertEquals("Alice", result.getOrNull()?.name)
    }

    @Test
    fun `login with invalid email returns error`() = runTest {
        val result = loginUseCase.execute("", "password")
        assertTrue(result.isError)
    }
}

// Fake implementation in commonTest
class FakeUserRepository : UserRepository {
    var shouldSucceed = true
    var loginCallCount = 0

    override suspend fun login(email: String, password: String): Result<User> {
        loginCallCount++
        return if (shouldSucceed) {
            Result.Success(User("1", "Alice", email))
        } else {
            Result.Error(AuthenticationException("Invalid credentials"))
        }
    }
}
```

**Gradle Configuration for KMP Testing:**

```kotlin
kotlin {
    sourceSets {
        val commonTest by getting {
            dependencies {
                implementation(kotlin("test"))
                implementation(libs.kotlinx.coroutines.test)
                implementation(libs.turbine)
            }
        }
        val jvmTest by getting {
            dependencies {
                implementation(libs.junit.jupiter)
            }
        }
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

### Flutter Widget Testing

Flutter's `flutter_test` package provides widget-level unit testing.

```dart
// test/user_card_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:app/presentation/widgets/user_card.dart';
import 'package:app/domain/models/user.dart';

void main() {
  group('UserCard Widget Tests', () {
    testWidgets('displays user name and email', (WidgetTester tester) async {
      // Given
      final user = User(
        id: '1',
        name: 'Alice Johnson',
        email: 'alice@example.com',
      );

      // When
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Then
      expect(find.text('Alice Johnson'), findsOneWidget);
      expect(find.text('alice@example.com'), findsOneWidget);
    });

    testWidgets('shows avatar when available', (WidgetTester tester) async {
      // Given
      final user = User(
        id: '1',
        name: 'Alice',
        email: 'alice@example.com',
        avatarUrl: 'https://example.com/avatar.jpg',
      );

      // When
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Then
      expect(find.byType(CircleAvatar), findsOneWidget);
    });

    testWidgets('shows initial placeholder when no avatar', (WidgetTester tester) async {
      // Given
      final user = User(
        id: '1',
        name: 'Alice Johnson',
        email: 'alice@example.com',
        avatarUrl: null,
      );

      // When
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Then
      expect(find.byType(CircleAvatar), findsNothing);
      expect(find.text('A'), findsOneWidget); // First initial
    });

    testWidgets('triggers onTap callback', (WidgetTester tester) async {
      // Given
      final user = User(id: '1', name: 'Alice', email: 'alice@example.com');
      var tapped = false;

      // When
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(
              user: user,
              onTap: () => tapped = true,
            ),
          ),
        ),
      );

      await tester.tap(find.byType(UserCard));
      await tester.pump();

      // Then
      expect(tapped, isTrue);
    });
  });
}
```

**Running Flutter Tests:**

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/user_card_test.dart

# Run with coverage
flutter test --coverage

# View coverage report
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

---

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`android-unit-testing.md`](references/android-unit-testing.md) — Android Unit Testing
- [`ios-unit-testing.md`](references/ios-unit-testing.md) — iOS Unit Testing
- [`viewmodel-testing.md`](references/viewmodel-testing.md) — ViewModel Testing
- [`repository-testing.md`](references/repository-testing.md) — Repository Testing
- [`test-doubles.md`](references/test-doubles.md) — Test Doubles
- [`code-coverage.md`](references/code-coverage.md) — Code Coverage
- [`ci-cd-integration.md`](references/ci-cd-integration.md) — CI/CD Integration
- [`stage-7-integration.md`](references/stage-7-integration.md) — Stage 7 Integration
- [`references.md`](references/references.md) — References
