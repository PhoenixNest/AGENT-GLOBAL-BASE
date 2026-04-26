---
name: ios-implementation
description: iOS application development — SwiftUI UI implementation, MVVM architecture with Swift Concurrency, Keychain security, CoreData persistence, URLSession networking with certificate pinning, iOS Human Interface Guidelines compliance, and App Store Connect submission standards.
version: "1.0.0"
---

# iOS Implementation

## Purpose

Implement production-grade iOS applications from the UML Engineering Package, IDS, and Coding Implementation Plan. All code must be written in Swift, follow the established architecture pattern, and be ready for Stage 6 Code Review without known compilation or runtime issues.

## Why This Matters

Implements iOS app features with SwiftUI and UIKit. Poor implementation causes App Store rejections, crashes, and user-facing bugs.

## Technology Stack

| Layer         | Technology                               | Version Policy                                            |
| ------------- | ---------------------------------------- | --------------------------------------------------------- |
| Language      | Swift                                    | Latest stable                                             |
| UI            | SwiftUI (primary) + UIKit (interop only) | Latest stable                                             |
| Architecture  | MVVM + Clean Architecture                | See patterns below                                        |
| Async         | Swift Concurrency (async/await, actors)  | Prefer over Combine for new code                          |
| Reactive      | Combine                                  | Use for existing pipelines; Observation framework for new |
| Navigation    | NavigationStack (iOS 16+)                | Coordinator pattern for pre-16                            |
| Persistence   | CoreData / SwiftData                     | SwiftData for iOS 17+ new projects                        |
| Network       | URLSession                               | No third-party HTTP client                                |
| Serialisation | Codable (JSONDecoder/Encoder)            |                                                           |
| DI            | Constructor injection + Environment      | No third-party DI framework                               |
| Image loading | SDWebImageSwiftUI / Kingfisher           | Per TSD                                                   |
| Build         | Xcode + Swift Package Manager            | No CocoaPods for new dependencies                         |

_Specific versions are governed by the TSD from Stage 3. The TSD overrides this table._

## Architecture Patterns

### ViewModel + Observable

```swift
@Observable
final class HomeViewModel {
    var items: [Item] = []
    var isLoading = false
    var errorMessage: String? = nil

    private let getItemsUseCase: GetItemsUseCaseProtocol

    init(getItemsUseCase: GetItemsUseCaseProtocol) {
        self.getItemsUseCase = getItemsUseCase
    }

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }
        do {
            items = try await getItemsUseCase.execute()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
```

### SwiftUI Screen Structure

```swift
struct HomeScreen: View {
    @State private var viewModel: HomeViewModel

    init(viewModel: HomeViewModel) {
        _viewModel = State(initialValue: viewModel)
    }

    var body: some View {
        HomeContent(
            items: viewModel.items,
            isLoading: viewModel.isLoading,
            errorMessage: viewModel.errorMessage
        )
        .task { await viewModel.loadItems() }
    }
}

// Separate stateless content view — previewable and testable without ViewModel
private struct HomeContent: View {
    let items: [Item]
    let isLoading: Bool
    let errorMessage: String?

    var body: some View {
        // UI implementation
    }
}

#Preview {
    HomeContent(items: Item.preview, isLoading: false, errorMessage: nil)
}
```

**Rules:**

- ViewModels are `@Observable` classes injected via constructor — not `@StateObject` + `ObservableObject` for new code
- Use `task {}` for async work tied to view lifecycle — never `onAppear` + `Task {}`
- Preview annotations on all content views with realistic preview data
- No business logic in View `body` computed properties

### Repository Pattern

```swift
protocol ItemRepository {
    func fetchItems() async throws -> [Item]
    func observeItems() -> AsyncStream<[Item]>
}

final class ItemRepositoryImpl: ItemRepository {
    private let remoteSource: ItemRemoteDataSource
    private let localSource: ItemLocalDataSource

    init(remoteSource: ItemRemoteDataSource, localSource: ItemLocalDataSource) {
        self.remoteSource = remoteSource
        self.localSource = localSource
    }
    // Local-first implementation
}
```

## iOS-Specific Requirements

### Security

- **Keychain:** All tokens, credentials, and sensitive user data stored in Keychain via `SecItemAdd`/`SecItemCopyMatching`; use `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` for most sensitive items
- **Certificate pinning:** Implement via URLSession delegate `urlSession(_:didReceive:completionHandler:)` per SRD requirements
- **App Transport Security:** No `NSAllowsArbitraryLoads` exceptions — all network connections HTTPS
- **Secure Enclave:** For biometric-protected keys, use `SecAccessControlCreateWithFlags` with `.biometryCurrentSet`
- Never log sensitive data (tokens, PII, payment details) — use `os_log` with privacy annotations

### Localization

- All user-visible strings: `String(localized: "key.name")` or `Text("key.name")` (SwiftUI auto-localizes)
- Plurals: `String(localized: "key.name \(count) items")` with stringsdict entry
- Never use `NSLocalizedString` in new SwiftUI code — use the Swift 5.9+ `String(localized:)` API
- Test in pseudo-language and right-to-left (use iOS Scheme argument `-AppleLanguages "(ar)"`)

### Accessibility

- All interactive elements: `.accessibilityLabel()` with descriptive text
- Touch targets: minimum 44×44pt via `.frame(minWidth: 44, minHeight: 44)`
- Test with VoiceOver enabled before Stage 6
- Dynamic Type: all text uses `Font` with automatic scaling; test at largest accessibility size

### HIG Compliance (per IDS)

- Navigation: use `NavigationStack` with typed `NavigationPath`; no custom back button overrides
- Bottom sheets: use `.sheet` and `.confirmationDialog` — custom sheet presentations must match detent spec in IDS
- Safe areas: all content respects `.safeAreaInset()` — no hard-coded padding for status bar or home indicator
- System haptics: `UIImpactFeedbackGenerator`, `UINotificationFeedbackGenerator` per IDS gesture vocabulary

## App Store Submission Checklist

Before Stage 10 Release Readiness:

- [ ] Deployment target matches TSD minimum iOS version
- [ ] All required entitlements present in `.entitlements` file
- [ ] Privacy manifest (`PrivacyInfo.xcprivacy`) declares all API usage and data collection
- [ ] App icons: all required sizes provided (1024×1024 App Store icon via asset catalog)
- [ ] Screenshots prepared for all required device sizes
- [ ] Archive builds successfully with distribution certificate
- [ ] TestFlight build uploaded and tested on physical devices
- [ ] App Review guidelines compliance verified (no private APIs, no undeclared background modes)

## Code Review Standards

Before submitting for Stage 6, verify:

- [ ] All features in the Coding Implementation Plan are implemented
- [ ] App compiles with zero warnings in release configuration
- [ ] App runs on minimum supported iOS version (per TSD)
- [ ] App runs on latest iOS release
- [ ] No crashes in debug or release builds on physical device
- [ ] All strings localized (zero hardcoded user-visible strings)
- [ ] All sensitive data uses Keychain (not UserDefaults)
- [ ] SwiftUI previews render correctly for all content views
- [ ] Memory Graph shows no retain cycles or leaks
