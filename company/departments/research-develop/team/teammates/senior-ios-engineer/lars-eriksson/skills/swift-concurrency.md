---
version: "1.0.0"
---

| Competency             | Description                                                                                          | Quality Criteria                                                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| async/await            | Async function design, throwing async, async sequences, async let parallelism, continuation bridging | Async functions are cancellable; errors propagate correctly; bridging from completion handlers uses checked continuations                |
| Actors & Isolation     | Actor model, MainActor annotation, isolated parameters, nonisolated access, actor reentrancy         | Shared mutable state protected by actors; UI updates on MainActor; actor reentrancy handled correctly                                    |
| Task Management        | Task creation, TaskGroup, Task priority, cancellation, Task-local values                             | Tasks bound to lifecycle; child tasks cancelled with parent; priority correctly set for user-initiated vs background work                |
| Structured Concurrency | async let, TaskGroup, withThrowingTaskGroup, unstructured vs structured tasks                        | Parallel work uses async let or TaskGroup; unstructured Task{} only for fire-and-forget with explicit lifecycle management               |
| Sendable & Data Races  | Sendable protocol, @Sendable closures, actor isolation, data race detection via Thread Sanitizer     | Zero data race warnings in TSan; all shared state is Sendable or actor-isolated; closures crossing isolation boundaries marked @Sendable |

## Execution Guidance

### async/await — Production Patterns

**Async function design with proper cancellation:**

```swift
// CORRECT: Cancellable async function
actor UserRepository {
    private var activeTask: Task<User, Error>?

    func fetchUser(id: String) async throws -> User {
        // Cancel previous in-flight request for same user
        activeTask?.cancel()

        let task = Task {
            try await apiClient.fetchUser(id: id)
        }
        activeTask = task

        let user = try await task.value
        activeTask = nil
        return user
    }

    func cancelFetch() {
        activeTask?.cancel()
        activeTask = nil
    }
}

// WRONG: Non-cancellable fire-and-forget
func fetchUser(id: String) {
    Task {
        let user = try await apiClient.fetchUser(id: id)
        // No way to cancel; no error handling
    }
}
```

**Async let for parallel decomposition:**

```swift
func loadDashboard(userId: String) async throws -> Dashboard {
    // All three fetches run in parallel
    async let userProfile = apiClient.fetchProfile(userId)
    async let orders = apiClient.fetchOrders(userId)
    async let notifications = apiClient.fetchNotifications(userId)

    // Await all results — if any fails, all are cancelled
    return try await Dashboard(
        profile: userProfile,
        orders: orders,
        notifications: notifications
    )
}

// With error handling per task
func loadDashboardResilient(userId: String) async -> Dashboard {
    async let userProfileTask = Task { try await apiClient.fetchProfile(userId) }
    async let ordersTask = Task { try await apiClient.fetchOrders(userId) }
    async let notificationsTask = Task { try await apiClient.fetchNotifications(userId) }

    let profile = try? await userProfileTask.value
    let orders = try? await ordersTask.value
    let notifications = try? await notificationsTask.value

    return Dashboard(
        profile: profile ?? .default,
        orders: orders ?? [],
        notifications: notifications ?? []
    )
}
```

**Bridging completion handlers to async/await:**

```swift
// Legacy completion handler API
extension CLLocationManager {
    func requestLocation() async throws -> CLLocation {
        try await withCheckedThrowingContinuation { continuation in
            let delegate = LocationDelegate(continuation: continuation)
            self.delegate = delegate
            self.requestLocation()
        }
    }
}

private class LocationDelegate: NSObject, CLLocationManagerDelegate {
    private let continuation: CheckedContinuation<CLLocation, Error>

    init(continuation: CheckedContinuation<CLLocation, Error>) {
        self.continuation = continuation
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.first else {
            continuation.resume(throwing: LocationError.noLocation)
            return
        }
        continuation.resume(returning: location)
    }

    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        continuation.resume(throwing: error)
    }
}
```

### Actors & MainActor — Isolation Discipline

**Actor for shared mutable state:**

```swift
actor CacheManager {
    private var cache: [String: CachedItem] = [:]
    private let maxCapacity: Int

    init(maxCapacity: Int = 100) {
        self.maxCapacity = maxCapacity
    }

    func get(_ key: String) -> CachedItem? {
        cache[key]
    }

    func set(_ key: String, value: Data, ttl: TimeInterval) {
        // Evict if at capacity
        if cache.count >= maxCapacity {
            evictOldest()
        }
        cache[key] = CachedItem(
            data: value,
            expiry: Date().addingTimeInterval(ttl)
        )
    }

    func removeExpired() {
        let now = Date()
        cache.removeAll { _, item in item.expiry < now }
    }

    private func evictOldest() {
        guard let oldestKey = cache.min(by: { $0.value.createdAt < $1.value.createdAt })?.key else { return }
        cache.removeValue(forKey: oldestKey)
    }
}
```

**MainActor for UI state management:**

```swift
@MainActor
class UserViewModel: ObservableObject {
    @Published private(set) var state: UserState = .idle
    @Published private(set) var errorMessage: String?

    private let userRepository: UserRepository
    private var task: Task<Void, Never>?

    init(userRepository: UserRepository) {
        self.userRepository = userRepository
    }

    func loadUser(id: String) {
        // Cancel previous load
        task?.cancel()

        task = Task {
            state = .loading
            do {
                let user = try await userRepository.fetchUser(id: id)
                // Check for cancellation before updating UI
                try Task.checkCancellation()
                state = .loaded(user)
            } catch is CancellationError {
                // Task was cancelled — no state update needed
            } catch {
                state = .error
                errorMessage = error.localizedDescription
            }
        }
    }

    deinit {
        task?.cancel()
    }
}

enum UserState: Equatable {
    case idle
    case loading
    case loaded(User)
    case error
}
```

**Actor reentrancy — critical pitfall:**

```swift
actor ImageDownloader {
    private var downloads: [URL: Task<UIImage, Error>] = [:]

    func downloadImage(from url: URL) async throws -> UIImage {
        // Reentrancy hazard: if we await here, another caller might
        // modify `downloads` before we continue
        if let existingTask = downloads[url] {
            return try await existingTask.value
        }

        let task = Task {
            try await performDownload(from: url)
        }
        downloads[url] = task

        defer { downloads.removeValue(forKey: url) }

        return try await task.value
    }

    private func performDownload(from url: URL) async throws -> UIImage {
        // Actual download implementation
        fatalError("Implement download")
    }
}
```

### TaskGroup — Dynamic Parallelism

```swift
func downloadAllImages(urls: [URL]) async -> [URL: UIImage] {
    await withTaskGroup(of: (URL, UIImage?).self) { group in
        var results: [URL: UIImage] = [:]

        for url in urls {
            group.addTask {
                do {
                    let image = try await ImageDownloader.shared.downloadImage(from: url)
                    return (url, image)
                } catch {
                    return (url, nil)
                }
            }
        }

        for await (url, image) in group {
            if let image = image {
                results[url] = image
            }
        }

        return results
    }
}

// Throwing task group — fails fast on first error
func fetchAllUserData(userId: String) async throws -> UserData {
    try await withThrowingTaskGroup(of: PartialUserData.self) { group in
        group.addTask { try await fetchProfile(userId) }
        group.addTask { try await fetchOrders(userId) }
        group.addTask { try await fetchPreferences(userId) }

        var profile: UserProfile?
        var orders: [Order]?
        var preferences: UserPreferences?

        for try await partial in group {
            switch partial {
            case .profile(let p): profile = p
            case .orders(let o): orders = o
            case .preferences(let p): preferences = p
            }
        }

        guard let profile, let orders, let preferences else {
            throw UserDataError.incompleteData
        }

        return UserData(profile: profile, orders: orders, preferences: preferences)
    }
}
```

### Sendable & Data Race Prevention

**Sendable conformance rules:**

```swift
// Value types are automatically Sendable if all properties are Sendable
struct User: Sendable {
    let id: String
    let name: String
    let email: String
    let createdAt: Date
}

// Classes must be marked final and have immutable properties
final class AppConfig: Sendable {
    let apiBaseURL: URL
    let apiKey: String
    let timeout: TimeInterval

    init(apiBaseURL: URL, apiKey: String, timeout: TimeInterval) {
        self.apiBaseURL = apiBaseURL
        self.apiKey = apiKey
        self.timeout = timeout
    }
}

// @Sendable closures — capture Sendable values only
func performRequest<T: Sendable>(
    _ request: URLRequest,
    decoder: JSONDecoder = .init()
) async throws -> T {
    let (data, response) = try await URLSession.shared.data(for: request)

    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw APIError.invalidResponse
    }

    return try decoder.decode(T.self, from: data)
}

// WRONG: Capturing non-Sendable state in @Sendable closure
actor Counter {
    var count = 0

    func startCounting() {
        Task { @MainActor in
            // ERROR: `count` is actor-isolated, can't be captured in MainActor closure
            for _ in 0..<100 {
                count += 1
                print(count)
                try? await Task.sleep(for: .seconds(0.1))
            }
        }
    }
}

// CORRECT: Pass values across isolation boundary explicitly
actor Counter {
    var count = 0

    func startCounting() {
        Task { @MainActor in
            for _ in 0..<100 {
                let currentCount = await self.increment()
                print(currentCount)
                try? await Task.sleep(for: .seconds(0.1))
            }
        }
    }

    func increment() -> Int {
        count += 1
        return count
    }
}
```

### Thread Sanitizer — Data Race Detection

**Enable in Xcode scheme for debug builds:**

1. Edit Scheme → Run → Diagnostics
2. Check "Thread Sanitizer"
3. Run app and exercise concurrent code paths
4. Review TSan warnings in Xcode console

**Common TSan warnings and fixes:**

| Warning                         | Cause                                               | Fix                                       |
| ------------------------------- | --------------------------------------------------- | ----------------------------------------- |
| Simultaneous access to variable | Mutable shared state without synchronization        | Use actor or `@MainActor`                 |
| Data race on property           | Class property read/written from multiple threads   | Make property `let` or protect with actor |
| Non-Sendable capture            | Closure captures non-Sendable type across isolation | Mark type as `Sendable` or restructure    |

## Pipeline Integration

- **Stage 3 (Architecture):** ADRs establish Swift concurrency as the async paradigm (no completion handlers in new code). Actor model for shared state.
- **Stage 5 (Development):** Primary skill for all asynchronous iOS code. All network calls, database operations, and background work use async/await with proper cancellation.
- **Stage 6 (Code Review):** Concurrency review: cancellation handling, actor isolation correctness, Sendable conformance, no data races, structured concurrency discipline.
- **Stage 7 (Automated Testing):** Async tests use `XCTest` async/await support. Actor-isolated state tested with `await` access.

## Quality Standards

- **Zero** completion handler APIs in new code — async/await exclusively
- **100%** async functions are cancellable — `Task.checkCancellation()` at suspension points
- **100%** shared mutable state protected by actors — no mutable class properties accessed from multiple threads
- **Zero** data race warnings in Thread Sanitizer (clean TSan run required before Stage 6 sign-off)
- **100%** UI state updates on `@MainActor` — actor-to-MainActor transitions are explicit
- All `Task{}` creations have explicit lifecycle management (stored and cancelled in `deinit`)
- Parallel work uses `async let` or `TaskGroup` — never manual Task creation for parallelism
- All types crossing isolation boundaries conform to `Sendable`
- Continuation bridging uses `withCheckedThrowingContinuation` — never unchecked continuations in production
- Task priority set explicitly — user-initiated work uses `.userInitiated`, background work uses `.background`
