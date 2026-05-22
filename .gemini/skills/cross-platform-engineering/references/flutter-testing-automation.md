---
name: flutter-testing-automation
description: Build and maintain comprehensive Flutter test suites — widget tests, golden file tests for design systems, Patrol integration tests for user flows, mock generation with mocktail, and CI pipeline configuration.
version: "1.0.0"
---

# Flutter Testing Automation

| Competency         | Description                                                   | Quality Criteria                                                                          |
| ------------------ | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Widget Tests       | Write unit tests for widgets using `flutter_test`             | ≥ 70% widget test coverage for all new code; all state transitions tested                 |
| Golden File Tests  | Create and maintain golden tests for design system primitives | Goldens updated intentionally, never accidentally; CI fails on unexpected golden mismatch |
| Patrol Integration | Write Patrol integration tests for critical user flows        | All P0 user flows have a Patrol test; tests run against real device in CI                 |
| Mock Generation    | Generate mocks with `mocktail` or `mockito`                   | Mocks generated for all external dependencies; no real HTTP or DB calls in widget tests   |

## Execution Guidance

### Widget Test Structure

```dart
group('LoginScreen', () {
  late MockAuthRepository mockAuthRepo;

  setUp(() {
    mockAuthRepo = MockAuthRepository();
    registerFallbackValue(const LoginCredentials('', ''));
  });

  testWidgets('shows error message on invalid credentials', (tester) async {
    when(() => mockAuthRepo.login(any()))
        .thenThrow(InvalidCredentialsException());

    await tester.pumpWidget(
      ProviderScope(
        overrides: [authRepositoryProvider.overrideWithValue(mockAuthRepo)],
        child: const MaterialApp(home: LoginScreen()),
      ),
    );

    await tester.tap(find.byType(LoginButton));
    await tester.pumpAndSettle();

    expect(find.text('Invalid credentials'), findsOneWidget);
  });
});
```

### Golden Test Configuration

```dart
testWidgets('PrimaryButton matches golden', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(
      home: Scaffold(
        body: PrimaryButton(label: 'Submit', onPressed: null),
      ),
    ),
  );

  await expectLater(
    find.byType(PrimaryButton),
    matchesGoldenFile('goldens/primary_button.png'),
  );
});
```

Run `flutter test --update-goldens` **only** when intentionally updating the design system.

### Patrol Integration Test Pattern

```dart
// patrol_test.dart
void main() {
  patrolTest(
    'user can log in and see home screen',
    ($) async {
      await $.pumpWidgetAndSettle(const App());

      await $(#emailField).enterText('user@example.com');
      await $(#passwordField).enterText('password123');
      await $(#loginButton).tap();

      await $.pumpAndSettle();
      expect($(HomeScreen), findsOneWidget);
    },
  );
}
```

### CI Pipeline for Flutter Tests

```yaml
# GitHub Actions
- name: Run widget tests
  run: flutter test --coverage

- name: Check coverage threshold
  run: |
    lcov --summary coverage/lcov.info | grep "lines" | awk '{print $2}' | \
    awk -F'%' '{if ($1 < 70) exit 1}'

- name: Run Patrol integration tests (device farm)
  run: |
    patrol test --target integration_test/app_test.dart \
      --device-id $BROWSERSTACK_DEVICE_ID
```
