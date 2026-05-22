---
name: flutter-native-integration
description: Implement Flutter platform channels for native API access — MethodChannel and EventChannel patterns, biometric auth, push notification routing, deep link handling, and background task bridges on both iOS and Android.
version: "1.0.0"
---

# Flutter Native Integration

| Competency         | Description                                                        | Quality Criteria                                                                              |
| ------------------ | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| MethodChannel      | Implement request/response communication with native platform code | Dart and native handlers on correct threads; all error cases handled; channel name namespaced |
| EventChannel       | Implement streaming event sources from native code to Flutter      | Stream cleaned up when Flutter side disposes; backpressure handled on native side             |
| Biometric Auth     | Implement Face ID / fingerprint authentication with secure storage | Auth challenge on correct thread; credentials stored in Keychain (iOS) / Keystore (Android)   |
| Push Notifications | Implement push notification reception and deep-link routing        | Foreground and background notification handling; deep-link routes to correct screen           |

## Execution Guidance

### MethodChannel Threading Rules

| Platform | Channel Handler Thread   | UI Update Thread   |
| -------- | ------------------------ | ------------------ |
| Android  | `Looper.getMainLooper()` | Same — main thread |
| iOS      | `DispatchQueue.main`     | Same — main thread |

```dart
// Dart side
static const _channel = MethodChannel('com.company.app/biometric');

Future<bool> authenticate() async {
  try {
    return await _channel.invokeMethod<bool>('authenticate') ?? false;
  } on PlatformException catch (e) {
    debugPrint('Biometric auth failed: ${e.code} - ${e.message}');
    return false;
  }
}
```

```kotlin
// Android — MainActivity.kt
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.company.app/biometric")
    .setMethodCallHandler { call, result ->
        if (call.method == "authenticate") {
            biometricPrompt.authenticate(
                promptInfo,
                object : BiometricPrompt.AuthenticationCallback() {
                    override fun onAuthenticationSucceeded(r: AuthenticationResult) {
                        result.success(true)
                    }
                    override fun onAuthenticationFailed() {
                        result.success(false)
                    }
                }
            )
        }
    }
```

### EventChannel Pattern for Real-Time Data

```dart
// Dart — subscribe to native events
static const _locationChannel = EventChannel('com.company.app/location');

Stream<LocationUpdate> get locationStream =>
    _locationChannel.receiveBroadcastStream().map(
      (event) => LocationUpdate.fromMap(Map<String, dynamic>.from(event))
    );
```

```swift
// iOS — AppDelegate.swift
private var locationEventSink: FlutterEventSink?

FlutterEventChannel(name: "com.company.app/location", binaryMessenger: controller.binaryMessenger)
    .setStreamHandler(self)

func onListen(withArguments arguments: Any?, eventSink events: @escaping FlutterEventSink) -> FlutterError? {
    locationEventSink = events
    startLocationUpdates()
    return nil
}

func onCancel(withArguments arguments: Any?) -> FlutterError? {
    stopLocationUpdates()
    locationEventSink = nil
    return nil
}
```
