---
name: flutter-native-integration
description: Flutter platform channel and native API integration. Use when implementing a platform channel (MethodChannel, EventChannel, BasicMessageChannel), bridging Flutter to native device APIs (biometrics, notifications, camera, background tasks, secure storage, deep links), writing the native Android (Kotlin) or iOS (Swift) side of a platform channel, or advising on when to use a platform channel vs. an existing plugin vs. dart:ffi.
version: "1.0.0"
---

# Flutter Native Integration

## Purpose

Flutter covers the majority of device capabilities with first-party packages and community plugins. But every production app eventually reaches the boundary: a platform API that no plugin exposes, a native SDK the client requires, or a security-sensitive capability that demands direct native implementation. Platform channels are the bridge. Done correctly, they are invisible to the Flutter layer. Done incorrectly, they produce hard-to-debug crashes, thread violations, and data corruption.

---

## Platform Channel Types

| Channel Type          | Use Case                                                            | Message Encoding                           |
| --------------------- | ------------------------------------------------------------------- | ------------------------------------------ |
| `MethodChannel`       | Request/response — Flutter calls native, native returns result      | `StandardMethodCodec` (handles most types) |
| `EventChannel`        | Native pushes events to Flutter — streams (GPS, sensors, live data) | `StandardMethodCodec`                      |
| `BasicMessageChannel` | Raw message passing with custom codec — rarely needed               | `StringCodec`, `BinaryCodec`, or custom    |

Use `MethodChannel` for 90% of cases. Use `EventChannel` for continuous streams (real-time sensor data, push notification streams, live connectivity changes).

---

## MethodChannel Implementation

### Flutter Side (Dart)

```dart
const _channel = MethodChannel('com.example.app/biometric');

Future<bool> authenticateWithBiometric() async {
  try {
    final result = await _channel.invokeMethod<bool>('authenticate', {
      'reason': 'Confirm your identity to continue',
    });
    return result ?? false;
  } on PlatformException catch (e) {
    // Handle platform-specific error codes here
    throw BiometricException(e.code, e.message);
  }
}
```

**Threading:** `invokeMethod` is async and returns on the platform thread that called the channel reply. The Flutter engine dispatches the result back to the Dart isolate automatically — no manual thread switching needed on the Dart side.

### Android Side (Kotlin)

```kotlin
// In MainActivity or a FlutterPlugin
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.example.app/biometric")
    .setMethodCallHandler { call, result ->
        when (call.method) {
            "authenticate" -> {
                val reason = call.argument<String>("reason") ?: "Authenticate"
                // IMPORTANT: MethodChannel callbacks run on the main thread
                authenticateBiometric(reason,
                    onSuccess = { result.success(true) },
                    onFailure = { result.success(false) },
                    onError = { code, msg -> result.error(code, msg, null) }
                )
            }
            else -> result.notImplemented()
        }
    }
```

**Threading rule (Android):** The `MethodCallHandler` is called on the main thread. If your native work is async, dispatch to a background thread and call `result.success(...)` or `result.error(...)` back on the main thread. Calling a `MethodChannel.Result` from a non-main thread crashes the app.

### iOS Side (Swift)

```swift
// In AppDelegate or FlutterPlugin
let channel = FlutterMethodChannel(
    name: "com.example.app/biometric",
    binaryMessenger: flutterViewController.binaryMessenger
)
channel.setMethodCallHandler { (call: FlutterMethodCall, result: @escaping FlutterResult) in
    guard call.method == "authenticate" else {
        result(FlutterMethodNotImplemented)
        return
    }
    let args = call.arguments as? [String: Any]
    let reason = args?["reason"] as? String ?? "Authenticate"
    // LAContext biometric auth — async
    let context = LAContext()
    context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics,
        localizedReason: reason) { success, error in
        DispatchQueue.main.async {  // IMPORTANT: call result on main thread
            if success { result(true) }
            else { result(false) }
        }
    }
}
```

**Threading rule (iOS):** `FlutterResult` must be called on the main thread. Any async native work must dispatch back to `DispatchQueue.main` before calling `result(...)`.

---

## EventChannel Implementation

```dart
// Flutter (Dart)
const _eventChannel = EventChannel('com.example.app/connectivity');

Stream<bool> get connectivityStream =>
    _eventChannel.receiveBroadcastStream().map((event) => event as bool);
```

```kotlin
// Android (Kotlin)
EventChannel(messenger, "com.example.app/connectivity")
    .setStreamHandler(object : EventChannel.StreamHandler {
        private var networkCallback: ConnectivityManager.NetworkCallback? = null

        override fun onListen(arguments: Any?, events: EventChannel.EventSink) {
            networkCallback = object : ConnectivityManager.NetworkCallback() {
                override fun onAvailable(network: Network) {
                    // Must call events.success on main thread
                    Handler(Looper.getMainLooper()).post { events.success(true) }
                }
                override fun onLost(network: Network) {
                    Handler(Looper.getMainLooper()).post { events.success(false) }
                }
            }
            connectivityManager.registerDefaultNetworkCallback(networkCallback!!)
        }

        override fun onCancel(arguments: Any?) {
            networkCallback?.let { connectivityManager.unregisterNetworkCallback(it) }
            networkCallback = null
        }
    })
```

---

## Platform Channel Error Handling

Define a structured error code scheme for every channel:

| Error Code Pattern      | Example                       | Meaning                         |
| ----------------------- | ----------------------------- | ------------------------------- |
| `PERMISSION_DENIED`     | `BIOMETRIC_PERMISSION_DENIED` | User denied permission          |
| `NOT_AVAILABLE`         | `BIOMETRIC_NOT_AVAILABLE`     | Feature not available on device |
| `AUTHENTICATION_FAILED` | `BIOMETRIC_FAILED`            | Auth was attempted but failed   |
| `UNEXPECTED_ERROR`      | `BIOMETRIC_UNEXPECTED`        | Unrecognised platform error     |

Document these codes in the channel's API contract. The Flutter layer maps each code to a typed exception class.

---

## When NOT to Use a Platform Channel

| Scenario                                                        | Better Approach                                                   |
| --------------------------------------------------------------- | ----------------------------------------------------------------- |
| The capability exists in a well-maintained pub.dev plugin       | Use the plugin                                                    |
| You need to call a C/C++ library                                | Use `dart:ffi` directly                                           |
| The data exchange is extremely high-frequency (>1000 calls/sec) | Use `dart:ffi` or a custom codec to reduce serialisation overhead |
| You need to embed a native view                                 | Use `PlatformView` (not a channel)                                |

---

## Output Standards

- Every platform channel must have a documented API contract (method name, arguments, return types, error codes) before implementation begins.
- Both sides of every channel (Dart + Android Kotlin + iOS Swift) must be implemented and tested together — a channel with only the Dart side done is not shippable.
- Threading requirements must be explicitly noted in code comments for every `MethodCallHandler` and `setStreamHandler` implementation.
