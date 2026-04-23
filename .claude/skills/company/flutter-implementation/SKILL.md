---
name: company-flutter-implementation
description: Flutter application development — Dart, widget architecture, Riverpod state management, platform channels for native API access, custom design systems, App Store and Google Play submission. Owned by Mei-Ling Johansson (Cross-Platform Lead).
disable-model-invocation: false
---

# Flutter Implementation

## Purpose

Implement production-grade cross-platform Flutter applications from the UML Engineering Package, IDS, and Coding Implementation Plan. All code is written in Dart, targets both Android and iOS from a single codebase, and follows the architecture patterns established here.

## When Flutter is the Right Choice

Use Flutter (not KMP) when:

- A single UI codebase is required for both platforms
- The project requires custom visual design that does not need to match platform-native widgets exactly
- Speed of cross-platform feature delivery is prioritised
- The TSD has selected Flutter per Stage 3 technology evaluation

## Technology Stack

| Layer            | Technology                                           |
| ---------------- | ---------------------------------------------------- |
| Language         | Dart (latest stable)                                 |
| UI               | Flutter (latest stable)                              |
| State management | Riverpod (preferred)                                 |
| Navigation       | go_router                                            |
| Networking       | dio or http                                          |
| Local storage    | drift (SQLite) or isar                               |
| Secure storage   | flutter_secure_storage                               |
| DI               | Riverpod providers (no separate DI framework needed) |
| Localisation     | flutter_localizations + ARB files                    |
| Image loading    | cached_network_image                                 |

_Specific package versions are governed by the TSD from Stage 3._

## Architecture Pattern

Flutter uses a feature-first folder structure with Riverpod for state:

```
lib/
  features/
    home/
      data/
        home_repository.dart
        home_remote_source.dart
        models/home_dto.dart
      domain/
        home_use_case.dart
        models/home_item.dart
      presentation/
        home_screen.dart
        home_controller.dart    ← Riverpod StateNotifier or Notifier
        widgets/
          home_item_card.dart
  core/
    network/               ← dio setup, interceptors
    storage/               ← drift/isar setup
    design_system/         ← shared custom widgets, tokens, theme
  main.dart
```

### Riverpod Controller Pattern

```dart
// home_controller.dart
@riverpod
class HomeController extends _$HomeController {
  @override
  Future<List<HomeItem>> build() async {
    return ref.watch(homeRepositoryProvider).fetchItems();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(homeRepositoryProvider).fetchItems(),
    );
  }
}

// home_screen.dart
class HomeScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(homeControllerProvider);

    return state.when(
      loading: () => const CircularProgressIndicator(),
      error: (e, _) => ErrorWidget(e.toString()),
      data: (items) => HomeContent(items: items),
    );
  }
}
```

## Platform Channels

For native API access not covered by Flutter plugins:

```dart
// Dart side
static const _channel = MethodChannel('com.example.app/biometrics');

Future<bool> authenticate() async {
  return await _channel.invokeMethod<bool>('authenticate') ?? false;
}
```

```kotlin
// Android (MainActivity.kt)
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.example.app/biometrics")
    .setMethodCallHandler { call, result ->
        when (call.method) {
            "authenticate" -> { /* BiometricPrompt logic */ }
            else -> result.notImplemented()
        }
    }
```

```swift
// iOS (AppDelegate.swift)
let channel = FlutterMethodChannel(
    name: "com.example.app/biometrics",
    binaryMessenger: controller.binaryMessenger
)
channel.setMethodCallHandler { call, result in
    if call.method == "authenticate" { /* LAContext logic */ }
    else { result(FlutterMethodNotImplemented) }
}
```

## Design System

Every Flutter project maintains a design system in `lib/core/design_system/`:

```
design_system/
  tokens/
    colors.dart          ← semantic color tokens (not raw hex values)
    typography.dart      ← TextStyle definitions for all type roles
    spacing.dart         ← spacing constants (4, 8, 12, 16, 24, 32...)
    radii.dart           ← border radius constants
  components/
    app_button.dart      ← primary, secondary, destructive button variants
    app_text_field.dart  ← text input with validation states
    app_card.dart        ← surface card with elevation variants
    [additional components per IDS]
  theme/
    app_theme.dart       ← ThemeData wrapping all tokens
```

Components are built against the IDS component spec — every component in the IDS maps to exactly one widget in the design system.

## Localisation

Flutter uses ARB (Application Resource Bundle) files:

```
lib/l10n/
  app_en.arb
  app_zh.arb
  app_ja.arb
  app_ko.arb
  app_fr.arb
```

```json
{
  "@@locale": "en",
  "checkoutConfirmButton": "Confirm Purchase",
  "@checkoutConfirmButton": {
    "description": "Button label on the checkout screen."
  },
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "description": "Item count with plural forms",
    "placeholders": { "count": { "type": "int" } }
  }
}
```

Usage: `AppLocalizations.of(context)!.checkoutConfirmButton`

## Security

- **Sensitive data:** `flutter_secure_storage` — wraps iOS Keychain and Android Keystore
- **Network:** Custom Dio interceptor for certificate pinning per SRD
- **No hardcoded secrets** in Dart code — use `--dart-define` for build-time configuration

## App Store and Google Play Submission

**Android (Google Play):**

- Build: `flutter build appbundle --release`
- Sign with upload keystore (separate from debug keystore)
- Minimum SDK: per TSD
- ProGuard/R8 obfuscation: enabled in release builds

**iOS (App Store):**

- Build: `flutter build ipa --release`
- Requires Xcode for signing — export IPA via Xcode archive
- Privacy manifest: `PrivacyInfo.xcprivacy` required for Flutter plugins that access sensitive APIs
- All entitlements declared in `Runner.entitlements`

## Code Review Standards

Before Stage 6:

- [ ] All features in the Coding Implementation Plan implemented
- [ ] App runs on Android minimum SDK (per TSD) and latest Android
- [ ] App runs on iOS minimum deployment target (per TSD) and latest iOS
- [ ] All strings in ARB files — zero hardcoded user-visible strings in Dart
- [ ] All sensitive data via `flutter_secure_storage`
- [ ] No `debugPrint` or `print` statements in production code paths
- [ ] All platform channels have implementations for both Android and iOS
- [ ] Design system components match IDS specifications
- [ ] `flutter analyze` passes with zero issues
