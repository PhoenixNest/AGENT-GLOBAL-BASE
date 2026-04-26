# SwiftUI Integration

## SwiftUI Integration

### @Published Property Wrapper

`@Published` exposes a property as a publisher, enabling SwiftUI views to react to state changes.

```swift
class SearchViewModel: ObservableObject {
    @Published var query: String = ""
    @Published var results: [Item] = []
    @Published var isLoading: Bool = false

    private var cancellables = Set<AnyCancellable>()

    init() {
        $query
            .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
            .removeDuplicates()
            .filter { !$0.isEmpty }
            .flatMap { [weak self] query -> AnyPublisher<[Item], Never> in
                guard let self else { return Empty().eraseToAnyPublisher() }
                return self.search(query: query)
                    .replaceError(with: [])
                    .eraseToAnyPublisher()
            }
            .assign(to: \.results, on: self)
            .store(in: &cancellables)
    }
}
```

### ObservableObject Pattern

```swift
class UserProfileViewModel: ObservableObject {
    @Published var user: User?
    @Published var errorMessage: String?

    private let userService: UserService
    private var cancellables = Set<AnyCancellable>()

    init(userService: UserService) {
        self.userService = userService
    }

    func loadProfile(userId: String) {
        isLoading = true
        userService.fetchUser(id: userId)
            .receive(on: DispatchQueue.main)
            .handleEvents(
                receiveSubscription: { _ in self.isLoading = true },
                receiveOutput: { _ in self.isLoading = false },
                receiveCompletion: { _ in self.isLoading = false },
                receiveCancel: { self.isLoading = false }
            )
            .sink(
                receiveCompletion: { completion in
                    if case .failure(let error) = completion {
                        self.errorMessage = error.localizedDescription
                    }
                },
                receiveValue: { self.user = $0 }
            )
            .store(in: &cancellables)
    }
}
```

---
