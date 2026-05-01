---
name: combine-reactive-programming
description: Build iOS reactive data pipelines using Apple's Combine framework — publishers, subscribers, operators, and scheduler management — for handling async events, network responses, and UI state updates in UIKit and SwiftUI applications.
version: "1.0.0"
---

# Combine Reactive Programming

| Competency           | Description                                                                  | Quality Criteria                                                                                                      |
| -------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Publisher Design     | Create and compose Combine publishers for async operations                   | Custom publishers are resource-safe; cancellables stored correctly; no retain cycles through `[weak self]` in sinks   |
| Operator Chaining    | Build operator chains for data transformation and error handling             | Chains are readable (one operator per line); `mapError` used before `replaceError` to preserve error type information |
| Scheduler Management | Route work to correct schedulers (background vs. main thread)                | Heavy work on `DispatchQueue.global()`; UI updates always on `DispatchQueue.main` via `.receive(on:)`                 |
| SwiftUI Integration  | Bridge Combine publishers to SwiftUI via `@Published` and `ObservableObject` | `@Published` properties drive UI updates; no `sink` subscriptions in View body; subscriptions live in ViewModel       |

## Execution Guidance

### Publisher Composition Pattern

```swift
func fetchUserProfile(userId: String) -> AnyPublisher<UserProfile, APIError> {
    networkClient.request(Endpoint.profile(userId))
        .decode(type: UserProfileResponse.self, decoder: JSONDecoder())
        .mapError { APIError.network($0) }
        .map(\.toUserProfile)
        .receive(on: DispatchQueue.main)
        .eraseToAnyPublisher()
}
```

### Cancellable Management

```swift
class ProfileViewModel: ObservableObject {
    @Published var profile: UserProfile?
    private var cancellables = Set<AnyCancellable>()

    func loadProfile(userId: String) {
        repository.fetchUserProfile(userId: userId)
            .sink(
                receiveCompletion: { [weak self] in /* handle */ },
                receiveValue: { [weak self] in self?.profile = $0 }
            )
            .store(in: &cancellables)  // Cancelled when ViewModel deallocates
    }
}
```

For new iOS 17+ code, prefer Swift Concurrency (`async/await`) over Combine. Use Combine for bridging existing Combine-based code or third-party publishers that have not migrated to async/await.
