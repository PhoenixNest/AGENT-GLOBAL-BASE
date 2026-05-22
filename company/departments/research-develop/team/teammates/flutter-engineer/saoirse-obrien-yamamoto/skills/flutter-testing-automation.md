---
name: flutter-testing-automation
description: Flutter testing strategy and automation infrastructure. Use when designing or expanding the widget test suite, setting up golden file testing for a design system, configuring Patrol integration tests, generating mocks with mockito or mocktail, configuring the Flutter test pipeline in CI (GitHub Actions, Bitrise, Codemagic), diagnosing test flakiness, or reporting widget test coverage metrics.
version: "1.0.0"
---

# Flutter Testing Automation

## Purpose

Flutter's testing framework is one of the best in mobile — it can test widgets without a device, snapshot visual regressions with golden files, and exercise full user flows with Patrol integration tests. The challenge is not the tools; it is building a test suite that is fast enough to run on every PR, stable enough to not produce false failures, and comprehensive enough to catch real regressions. This skill covers the strategy and infrastructure to achieve that.

---

## Testing Pyramid

```
                ┌──────────────────────────────┐
                │       Patrol / Driver        │  10–30 tests
                │   (Full device, real flows)  │  Slow; run on PRs + merge
               ┌┴──────────────────────────────┴┐
               │         Widget Tests           │  100s of tests
               │   (No device, pump widgets)    │  Fast; run on every PR
              ┌┴────────────────────────────────┴┐
              │    Unit Tests (Dart, no Flutter)  │  100s of tests
              │       (Fastest; run on every PR)  │
              └──────────────────────────────────┘
```

---

## Widget Tests

### Setup

```dart
// test/widgets/my_button_test.dart
void main() {
    testWidgets('MyButton renders correctly and responds to tap', (tester) async {
        bool tapped = false;
        await tester.pumpWidget(
            MaterialApp(
                home: Scaffold(
                    body: MyButton(
                        label: 'Confirm',
                        onTap: () => tapped = true,
                    ),
                ),
            ),
        );

        expect(find.text('Confirm'), findsOneWidget);

        await tester.tap(find.byType(MyButton));
        await tester.pump();

        expect(tapped, isTrue);
    });
}
```

### Pump Strategies

| Method                            | When to Use                                                                                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `tester.pump()`                   | Advance by one frame — use for animations where you need frame-by-frame control                                        |
| `tester.pump(Duration)`           | Advance by a duration — use to advance past animation timers                                                           |
| `tester.pumpAndSettle()`          | Run until no more frames are scheduled — use for transitions; **avoid in performance tests** (can mask animation jank) |
| `tester.runAsync(() async {...})` | Run real async operations (timers, I/O) — use when `pump` cannot advance a real Future                                 |

### Mocking with Mocktail

```dart
// Prefer mocktail over mockito — no code generation required
class MockUserRepository extends Mock implements UserRepository {}

void main() {
    late MockUserRepository repository;

    setUp(() {
        repository = MockUserRepository();
    });

    testWidgets('UserList shows users from repository', (tester) async {
        when(() => repository.observeUsers())
            .thenAnswer((_) => Stream.value([UserFixture.alice]));

        await tester.pumpWidget(
            ProviderScope(
                overrides: [
                    userRepositoryProvider.overrideWithValue(repository),
                ],
                child: const MaterialApp(home: UserList()),
            ),
        );

        await tester.pump();
        expect(find.text('Alice'), findsOneWidget);
    });
}
```

---

## Golden File Tests

Golden tests compare the rendered widget against a stored reference image. Use for design system components where pixel accuracy matters.

```dart
testWidgets('PrimaryButton golden — light theme', (tester) async {
    await tester.pumpWidget(
        MaterialApp(
            theme: AppTheme.light,
            home: const Scaffold(
                body: Center(child: PrimaryButton(label: 'Save')),
            ),
        ),
    );
    await expectLater(
        find.byType(PrimaryButton),
        matchesGoldenFile('goldens/primary_button_light.png'),
    );
});
```

### Golden Test Rules

1. **One golden per theme variant** — at minimum: light, dark, and any brand variants
2. **Update goldens intentionally** — run `flutter test --update-goldens` only when a visual change is intentional; always include the updated golden in the PR
3. **Font rendering** — golden tests can fail on different platforms due to font rendering differences. Pin the font renderer by loading `Ahem` test font or using `flutter_test_config.dart` to force consistent rendering
4. **Size the widget explicitly** — `SizedBox(width: 300, height: 80, child: PrimaryButton(...))` to prevent golden dimensions from varying with font scale settings

---

## Patrol Integration Tests

Patrol replaces `flutter_driver` with a modern, stable API that supports real device interactions.

```dart
// integration_test/app_test.dart
void main() {
    patrolTest('User can log in and see dashboard', ($) async {
        await $.pumpWidgetAndSettle(const MyApp());

        await $(TextField).at(0).enterText('user@example.com');
        await $(TextField).at(1).enterText('password123');
        await $('Log In').tap();
        await $.pumpAndSettle();

        expect($('Dashboard'), findsOneWidget);
    });
}
```

### Running Patrol in CI

```yaml
# GitHub Actions — macOS runner required for iOS
- name: Run Patrol integration tests (iOS simulator)
  run: |
    patrol test --target integration_test/app_test.dart \
      --device "iPhone 15 Pro"
```

For Android:

```yaml
- name: Run Patrol integration tests (Android emulator)
  uses: reactivecircus/android-emulator-runner@v2
  with:
    api-level: 33
    script: patrol test --target integration_test/app_test.dart
```

---

## Test Coverage Reporting

```bash
# Generate LCOV coverage report
flutter test --coverage
# View coverage (install lcov: brew install lcov / apt install lcov)
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

### Coverage Targets

| Target                                   | Threshold                                               |
| ---------------------------------------- | ------------------------------------------------------- |
| Business logic (repositories, use cases) | ≥ 90% line coverage                                     |
| Widget layer (screens, components)       | ≥ 70% line coverage                                     |
| Design system components                 | 100% golden test coverage per component                 |
| Platform channels (Dart side)            | ≥ 80% line coverage via widget tests with mock channels |

Add coverage enforcement to CI:

```yaml
- name: Check coverage threshold
  run: |
    COVERAGE=$(lcov --summary coverage/lcov.info | grep "lines" | awk '{print $4}' | tr -d '%')
    if (( $(echo "$COVERAGE < 70" | bc -l) )); then
      echo "Coverage $COVERAGE% is below 70% threshold"
      exit 1
    fi
```

---

## Common Flakiness Patterns and Fixes

| Flakiness Cause                    | Symptom                                  | Fix                                                                                              |
| ---------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `pumpAndSettle` timeout            | "timed out waiting for animations"       | Replace with `pump(Duration)` for fixed-duration animations; or increase `pumpAndSettle` timeout |
| Golden font rendering varies by OS | Golden fails only on CI                  | Use `Ahem` test font or configure `flutter_test_config.dart` with a seeded font renderer         |
| Real `Future` in a widget          | Widget test never completes              | Use `tester.runAsync` or inject a fake clock                                                     |
| Platform channel in widget test    | `MissingPluginException`                 | Register a mock method channel handler in `TestDefaultBinaryMessenger`                           |
| State leaks between tests          | Test passes in isolation, fails in suite | Use `setUp`/`tearDown` to reset state; never share mutable state across tests                    |

---

## Output Standards

- No widget test should call `sleep` or `Future.delayed` — use `pump(Duration)` or `pumpAndSettle` instead.
- Golden tests must be updated in the same PR as the visual change — a PR that breaks a golden without updating it is rejected.
- Integration tests must be tagged (`@Tags(['integration'])`) so they can be excluded from the fast widget test run and included in the slower scheduled CI job.
