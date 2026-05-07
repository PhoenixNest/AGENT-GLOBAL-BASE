---
name: mobile-testing-fundamentals
description: Apply web and backend testing expertise to mobile testing contexts — understanding mobile-specific test categories (unit, integration, UI, E2E), Android/iOS test tooling, and mobile testing constraints (network conditions, device fragmentation) — as cross-skilling support for the mobile test team.
version: "1.0.0"
---

# Mobile Testing Fundamentals

| Competency                | Description                                                            | Quality Criteria                                                                                                          |
| ------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Mobile Test Taxonomy      | Understand Android and iOS test categories and their appropriate scope | Can correctly classify a test as unit/integration/UI/E2E; understands which runner executes each type                     |
| Network Condition Testing | Simulate degraded network conditions in mobile tests                   | Tests exercise offline mode, slow 3G, and airplane mode scenarios; app behaves correctly under each condition             |
| API Contract Testing      | Apply backend API contract knowledge to mobile API integration tests   | Mobile-specific contract tests verify JSON schema, error codes, and pagination exactly as the mobile client consumes them |
| Device Fragmentation      | Account for Android device fragmentation in test planning              | Test matrix covers top 5 device/OS combinations from analytics; CI covers min SDK and target SDK as minimum               |

## Execution Guidance

### Mobile Test Taxonomy

| Test Type   | Android Tooling         | iOS Tooling          | Runs On                 |
| ----------- | ----------------------- | -------------------- | ----------------------- |
| Unit        | JUnit 5 + MockK         | XCTest + Swift mocks | JVM / Simulator         |
| Integration | Robolectric             | XCTest               | JVM / Simulator         |
| UI          | Compose Test / Espresso | XCUITest             | Emulator / Simulator    |
| E2E         | Detox / Maestro         | Maestro              | Real device or emulator |

### Network Condition Simulation (Android)

```kotlin
// Using Android Emulator network throttling
// Via adb: emulator -netdelay gprs -netspeed gsm

// In test code via OkHttp Interceptor
class SlowNetworkInterceptor : Interceptor {
    override fun intercept(chain: Chain): Response {
        Thread.sleep(2000)  // Simulate 2s latency
        return chain.proceed(chain.request())
    }
}
```

Bridge backend API knowledge by participating in mobile API review sessions — identify mobile-specific concerns the backend team may overlook (response payload size, offline-capable endpoints, retry-safe operations).
