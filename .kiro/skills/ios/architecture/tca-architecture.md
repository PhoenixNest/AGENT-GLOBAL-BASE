---
name: tca-architecture
description: This skill implements The Composable Architecture (TCA) for iOS applications covering reducers, stores, Effects, state management, and domain-driven feature composition.
---

# TCA Architecture

**Category:** Mobile Engineering — iOS Architecture
**Owner:** Senior iOS Engineer (Lars Eriksson)

## Overview

This skill implements The Composable Architecture (TCA) for iOS applications covering reducers, stores, Effects, state management, and domain-driven feature composition. It applies to Stage 5 (Development) where TCA provides the architectural backbone for all iOS screens, Stage 6 (Code Review) where reducer purity and effect correctness are audited, and Stage 8 (Integrity Verification) where state machine completeness is verified.

## Competency Dimensions

| Dimension        | Description                                                                                                          | Proficiency Indicators                                                                                                                       |
| ---------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Reducer Design   | Pure state transformation, action enumeration, Effect return, reducer composition with `Reduce` and `@Reducer` macro | Reducers are pure functions (same input → same output); all side effects wrapped in Effects; complex features composed from smaller reducers |
| Store Management | Store initialization, ViewStore binding, scope/sub-state derivation, lifecycle management                            | Views observe only the sub-state they need; Store lifecycle bound to view lifecycle; no direct store mutation outside reducer                |
| Effect Handling  | Async effects, cancellation, timer effects, effect IDs, effect composition                                           | Effects are cancellable by ID; long-running effects properly scoped; effect errors handled within reducer                                    |
| State Design     | Equatable state, Codable conformance, state normalization, optional child state                                      | State is always Equatable; nested state properly scoped; optional child state handles nil gracefully                                         |
| Testing          | Reducer testing with TestStore, effect assertion, time manipulation, mock dependencies                               | Every reducer action has a corresponding test; Effects verified for correctness; time-based Effects tested with TestStore scheduler          |

## Execution Guidance

### TCA Feature Module — Complete Implementation

**State and Action definition:**

```swift
import ComposableArchitecture

// MARK: - State

@ObservableState
struct UserListFeature: Equatable {
    var users: [User] = []
    var isLoading: Bool = false
    var errorMessage: String?
    var selectedUserId: UUID?

    // Derived state
    var selectedUser: User? {
        users.first { $0.id == selectedUserId }
    }

    var hasUsers: Bool { !users.isEmpty }
    var isEmptyState: Bool { !isLoading && users.isEmpty && errorMessage == nil }
}

// MARK: - Action

enum UserListFeatureAction: Equatable {
    case onAppear
    case userResponse(Result<[User], ApiError>)
    case refreshRequested
    case refreshResponse(Result<[User], ApiError>)
    case userTapped(UUID)
    case deleteButtonTapped(UUID)
    case deleteResponse(Result<Void, ApiError>)
    case dismissError
}
```

**Reducer implementation:**

```swift
@Reducer
struct UserListFeature {

    // Dependencies — injected, not created
    @Dependency(\.userRepository) var userRepository

    // MARK: - Body

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .onAppear:
                state.isLoading = true
                return .run { send in
                    await send(.userResponse(Result {
                        try await userRepository.fetchUsers()
                    }))
                }

            case .userResponse(.success(let users)):
                state.users = users
                state.isLoading = false
                state.errorMessage = nil
                return .none

            case .userResponse(.failure(let error)):
                state.isLoading = false
                state.errorMessage = error.userMessage
                return .none

            case .refreshRequested:
                state.isLoading = true
                return .run { send in
                    await send(.refreshResponse(Result {
                        try await userRepository.refreshUsers()
                    }))
                }

            case .refreshResponse(.success(let users)):
                state.users = users
                state.isLoading = false
                return .none

            case .refreshResponse(.failure(let error)):
                state.isLoading = false
                state.errorMessage = error.userMessage
                return .none

            case .userTapped(let userId):
                state.selectedUserId = userId
                return .none

            case .deleteButtonTapped(let userId):
                return .run { [userId] send in
                    await send(.deleteResponse(Result {
                        try await userRepository.deleteUser(id: userId)
                    }))
                }

            case .deleteResponse(.success):
                state.users.removeAll { $0.id == state.selectedUserId }
                state.selectedUserId = nil
                return .none

            case .deleteResponse(.failure(let error)):
                state.errorMessage = error.userMessage
                return .none

            case .dismissError:
                state.errorMessage = nil
                return .none
            }
        }
    }
}
```

**View implementation with ViewStore:**

```swift
struct UserListView: View {
    let store: StoreOf<UserListFeature>

    var body: some View {
        WithViewStore(store, observe: { $0 }) { viewStore in
            NavigationStack {
                Group {
                    if viewStore.isLoading {
                        ProgressView()
                    } else if viewStore.isEmptyState {
                        ContentUnavailableView(
                            "No users found",
                            systemImage: "person.crop.circle.badge.questionmark"
                        )
                    } else if viewStore.errorMessage != nil {
                        errorView(viewStore: viewStore)
                    } else {
                        userList(viewStore: viewStore)
                    }
                }
                .navigationTitle("Users")
                .toolbar {
                    ToolbarItem(placement: .topBarTrailing) {
                        Button(action: { viewStore.send(.refreshRequested) }) {
                            Image(systemName: "arrow.clockwise")
                        }
                        .disabled(viewStore.isLoading)
                    }
                }
            }
        }
        .onAppear { viewStore.send(.onAppear) }
    }

    private func userList(viewStore: ViewStoreOf<UserListFeature>) -> some View {
        List(viewStore.users) { user in
            NavigationLink(value: user.id) {
                UserRowView(user: user)
            }
            .swipeActions(edge: .trailing) {
                Button(role: .destructive) {
                    viewStore.send(.deleteButtonTapped(user.id))
                } label: {
                    Label("Delete", systemImage: "trash")
                }
            }
        }
        .navigationDestination(item: viewStore.binding(
            get: \.selectedUserId,
            send: UserListFeatureAction.userTapped
        )) { userId in
            UserDetailView(
                store: store.scope(
                    state: { $0.users.first(where: { $0.id == userId }) },
                    action: { _ in .none }
                )
            )
        }
    }

    private func errorView(viewStore: ViewStoreOf<UserListFeature>) -> some View {
        VStack(spacing: 16) {
            Image(systemName: "exclamationmark.triangle")
                .font(.system(size: 48))
                .foregroundStyle(.red)
            Text(viewStore.errorMessage ?? "Unknown error")
                .multilineTextAlignment(.center)
            Button("Dismiss") {
                viewStore.send(.dismissError)
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

### Effect Management — Production Patterns

**Cancellable effects with Effect IDs:**

```swift
@Reducer
struct SearchFeature {

    @Dependency(\.searchRepository) var searchRepository
    @Dependency(\.continuousClock) var clock

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .searchQueryChanged(let query):
                state.query = query

                // Cancel previous search — debounce pattern
                return .run { [query] send in
                    // Debounce: wait 300ms before executing search
                    try await clock.sleep(for: .milliseconds(300))
                    try Task.checkCancellation()

                    await send(.searchResponse(Result {
                        try await searchRepository.search(query: query)
                    }))
                }
                .cancellable(id: SearchEffectId.search, cancelInFlight: true)

            case .searchResponse(.success(let results)):
                state.results = results
                return .none

            case .searchResponse(.failure(let error)):
                state.errorMessage = error.userMessage
                return .none
            }
        }
    }
}

private enum SearchEffectId {
    case search
}
```

**Timer effects with cancellation:**

```swift
@Reducer
struct SessionTimerFeature {

    @Dependency(\.continuousClock) var clock

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .onAppear:
                state.sessionStartTime = Date()
                state.elapsedTime = 0
                return .run { send in
                    for await _ in clock.timer(interval: .seconds(1)) {
                        await send(.tick)
                    }
                }
                .cancellable(id: SessionTimerId.timer)

            case .tick:
                state.elapsedTime += 1
                return .none

            case .onDisappear:
                // Cancel timer when view disappears
                return .cancel(id: SessionTimerId.timer)
            }
        }
    }
}

private enum SessionTimerId {
    case timer
}
```

### Dependency Injection in TCA

```swift
// MARK: - Dependency Key

private enum UserRepositoryKey: DependencyKey {
    static let liveValue: UserRepositoryProtocol = LiveUserRepository()
    static let testValue: UserRepositoryProtocol = MockUserRepository()
    static let previewValue: UserRepositoryProtocol = MockUserRepository.previewData
}

extension DependencyValues {
    var userRepository: UserRepositoryProtocol {
        get { self[UserRepositoryKey.self] }
        set { self[UserRepositoryKey.self] = newValue }
    }
}

// MARK: - Protocol

protocol UserRepositoryProtocol: Sendable {
    func fetchUsers() async throws -> [User]
    func refreshUsers() async throws -> [User]
    func deleteUser(id: UUID) async throws
}

// MARK: - Live Implementation

struct LiveUserRepository: UserRepositoryProtocol {
    func fetchUsers() async throws -> [User] {
        let (data, _) = try await URLSession.shared.data(
            from: URL(string: "https://api.example.com/users")!
        )
        return try JSONDecoder().decode([User].self, from: data)
    }

    func refreshUsers() async throws -> [User] {
        try await fetchUsers()
    }

    func deleteUser(id: UUID) async throws {
        var request = URLRequest(
            url: URL(string: "https://api.example.com/users/\(id)")!
        )
        request.httpMethod = "DELETE"
        let (_, response) = try await URLSession.shared.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 204 else {
            throw ApiError.deleteFailed
        }
    }
}

// MARK: - Mock Implementation

struct MockUserRepository: UserRepositoryProtocol {
    var users: [User] = []
    var shouldFail: Bool = false

    func fetchUsers() async throws -> [User] {
        if shouldFail { throw ApiError.networkError }
        return users
    }

    func refreshUsers() async throws -> [User] {
        if shouldFail { throw ApiError.networkError }
        return users
    }

    func deleteUser(id: UUID) async throws {
        if shouldFail { throw ApiError.networkError }
    }
}

extension MockUserRepository {
    static var previewData: Self {
        Self(users: [
            User(id: UUID(), name: "John Doe", email: "john@example.com"),
            User(id: UUID(), name: "Jane Smith", email: "jane@example.com")
        ])
    }
}
```

### Reducer Testing — TestStore

```swift
@MainActor
final class UserListFeatureTests: XCTestCase {

    func test_onAppear_loadsUsers() async {
        let store = TestStore(initialState: UserListFeature()) {
            UserListFeature()
        } withDependencies: {
            $0.userRepository.fetchUsers = { [
                User(id: UUID(uuidString: "00000000-0000-0000-0000-000000000001")!,
                     name: "John Doe", email: "john@example.com")
            ] }
        }

        await store.send(.onAppear) {
            $0.isLoading = true
        }

        await store.receive(.userResponse(.success([
            User(id: UUID(uuidString: "00000000-0000-0000-0000-000000000001")!,
                 name: "John Doe", email: "john@example.com")
        ]))) {
            $0.users = [
                User(id: UUID(uuidString: "00000000-0000-0000-0000-000000000001")!,
                     name: "John Doe", email: "john@example.com")
            ]
            $0.isLoading = false
            $0.errorMessage = nil
        }
    }

    func test_onAppear_handlesError() async {
        let store = TestStore(initialState: UserListFeature()) {
            UserListFeature()
        } withDependencies: {
            $0.userRepository.fetchUsers = { throw ApiError.networkError }
        }

        await store.send(.onAppear) {
            $0.isLoading = true
        }

        await store.receive(.userResponse(.failure(.networkError))) {
            $0.isLoading = false
            $0.errorMessage = "Network error. Please check your connection."
        }
    }

    func test_deleteUser_removesFromList() async {
        let userId = UUID()
        let initialState = UserListFeature(
            users: [User(id: userId, name: "John", email: "john@example.com")],
            selectedUserId: userId
        )

        let store = TestStore(initialState: initialState) {
            UserListFeature()
        } withDependencies: {
            $0.userRepository.deleteUser = { _ in }
        }

        await store.send(.deleteButtonTapped(userId))

        await store.receive(.deleteResponse(.success)) {
            $0.users = []
            $0.selectedUserId = nil
        }
    }
}
```

### Feature Composition — Parent/Child Reducers

```swift
@Reducer
struct AppFeature {
    @ObservableState
    struct State: Equatable {
        var userList = UserListFeature.State()
        var userDetail: UserDetailFeature.State?
        var settings = SettingsFeature.State()
    }

    enum Action: Equatable {
        case userList(UserListFeature.Action)
        case userDetail(UserDetailFeature.Action)
        case settings(SettingsFeature.Action)
    }

    var body: some ReducerOf<Self> {
        Scope(state: \.userList, action: \.userList) {
            UserListFeature()
        }
        Scope(state: \.userDetail, action: \.userDetail) {
            UserDetailFeature()
        }
        Scope(state: \.settings, action: \.settings) {
            SettingsFeature()
        }

        Reduce { state, action in
            switch action {
            case .userList(.userTapped(let userId)):
                // Navigate to detail
                state.userDetail = UserDetailFeature.State(userId: userId)
                return .none

            case .userDetail(.dismiss):
                state.userDetail = nil
                return .none

            default:
                return .none
            }
        }
    }
}
```

## Pipeline Integration

- **Stage 3 (Architecture):** ADR establishes TCA as the iOS architecture pattern. UML state diagrams map to reducer state machines.
- **Stage 5 (Development):** Primary skill for iOS feature development. All screens implemented as TCA features with reducers, stores, and Effects.
- **Stage 6 (Code Review):** Architecture review: reducer purity, Effect correctness, dependency injection completeness, state Equatable conformance.
- **Stage 7 (Automated Testing):** TestStore-based reducer tests. Every reducer action has corresponding test coverage.
- **Stage 8 (Integrity Verification):** State machine completeness verified — all state transitions documented and tested.

## Quality Standards

- **100%** reducers are pure functions — same input state + action → same output state + effects
- **100%** side effects wrapped in `Effect` — no direct async calls outside Effects
- **100%** state types conform to `Equatable` — required for state diffing
- **100%** dependencies injected via `@Dependency` — no hardcoded service creation in reducers
- **100%** long-running Effects are cancellable with explicit effect IDs
- **100%** reducer actions have corresponding TestStore tests
- Views observe only needed sub-state via `observe:` closure — no full-state observation
- Child features scoped via `Scope` reducer — not embedded as full child stores
- Error handling within reducers — errors mapped to state, not thrown to views
- Deletion of `cancelInFlight: true` for debounced effects — only latest request executes
