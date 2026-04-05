# UIKit & Combine

**Category:** Mobile Engineering — iOS UI & Reactive Programming
**Owner:** iOS Engineer (Hiroshi Tanaka)

## Overview

This skill implements UIKit architecture patterns integrated with Combine reactive programming covering data binding, MVVM with Combine publishers, reactive UIKit extensions, and subscription lifecycle management. It applies to Stage 5 (Development) where UIKit screens use Combine for reactive state management, Stage 6 (Code Review) where subscription correctness and memory management are audited, and Stage 7 (Automated Testing) where Combine publishers are tested with XCTest.

## Competency Dimensions

| Dimension                    | Description                                                                                         | Proficiency Indicators                                                                                                              |
| ---------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| UIKit Architecture           | View controller lifecycle, view hierarchy, Auto Layout, custom views, delegation patterns           | View controllers are thin coordinators; custom views are reusable and testable; delegation uses weak references                     |
| Combine Reactive Programming | Publisher/Subscriber model, operators, subjects, error handling, backpressure, schedulers           | Complex event streams composed with operators; error handling at appropriate boundaries; publishers scheduled on correct queues     |
| Data Binding                 | @Published properties, BindableObject, sink subscription, assign operator, custom binding operators | UI binds to ViewModel publishers; no manual UI updates outside binding; subscription lifecycle managed correctly                    |
| MVVM with Combine            | ViewModel as publisher source, View as subscriber, unidirectional data flow, action channels        | ViewModel exposes publishers for state; View sends actions via PassthroughSubject; zero UIKit logic in ViewModel                    |
| Subscription Lifecycle       | AnyCancellable storage, cancel on deinit, subscription reuse, memory leak prevention                | All subscriptions stored and cancelled; zero retained subscriptions after view controller deallocation; leak-free under Instruments |

## Execution Guidance

### MVVM with Combine — Production Pattern

**ViewModel with published state:**

```swift
import Combine
import Foundation

@MainActor
final class UserListViewModel: ObservableObject {

    // MARK: - Published State

    @Published private(set) var users: [UserDisplayModel] = []
    @Published private(set) var isLoading: Bool = false
    @Published private(set) var errorMessage: String?
    @Published private(set) var isRefreshing: Bool = false

    // MARK: - Action Subjects

    private let loadAction = PassthroughSubject<Void, Never>()
    private let refreshAction = PassthroughSubject<Void, Never>()
    private let deleteAction = PassthroughSubject<UUID, Never>()
    private var cancellables = Set<AnyCancellable>()

    // MARK: - Dependencies

    private let userRepository: UserRepositoryProtocol
    private let scheduler: AnySchedulerOf<DispatchQueue>

    init(
        userRepository: UserRepositoryProtocol,
        scheduler: AnySchedulerOf<DispatchQueue> = .main
    ) {
        self.userRepository = userRepository
        self.scheduler = scheduler

        setupBindings()
    }

    // MARK: - Public Actions

    func sendLoadAction() {
        loadAction.send(())
    }

    func sendRefreshAction() {
        refreshAction.send(())
    }

    func sendDeleteAction(for userId: UUID) {
        deleteAction.send(userId)
    }

    // MARK: - Private Bindings

    private func setupBindings() {
        // Load users on action
        loadAction
            .handleEvents(receiveOutput: { [weak self] _ in
                self?.isLoading = true
            })
            .flatMap { [weak self] _ -> AnyPublisher<[User], Error> in
                guard let self else { return Empty().eraseToAnyPublisher() }
                return userRepository.fetchUsers()
                    .receive(on: scheduler)
                    .eraseToAnyPublisher()
            }
            .sink(
                receiveCompletion: { [weak self] completion in
                    self?.isLoading = false
                    if case .failure(let error) = completion {
                        self?.errorMessage = error.localizedDescription
                    }
                },
                receiveValue: { [weak self] users in
                    self?.users = users.map { UserDisplayModel(user: $0) }
                }
            )
            .store(in: &cancellables)

        // Refresh users
        refreshAction
            .handleEvents(receiveOutput: { [weak self] _ in
                self?.isRefreshing = true
            })
            .flatMap { [weak self] _ -> AnyPublisher<[User], Error> in
                guard let self else { return Empty().eraseToAnyPublisher() }
                return userRepository.refreshUsers()
                    .receive(on: scheduler)
                    .eraseToAnyPublisher()
            }
            .sink(
                receiveCompletion: { [weak self] _ in
                    self?.isRefreshing = false
                },
                receiveValue: { [weak self] users in
                    self?.users = users.map { UserDisplayModel(user: $0) }
                }
            )
            .store(in: &cancellables)

        // Delete user
        deleteAction
            .flatMap { [weak self] userId -> AnyPublisher<Void, Error> in
                guard let self else { return Empty().eraseToAnyPublisher() }
                return userRepository.deleteUser(id: userId)
                    .receive(on: scheduler)
                    .eraseToAnyPublisher()
            }
            .sink(
                receiveCompletion: { [weak self] completion in
                    if case .failure(let error) = completion {
                        self?.errorMessage = error.localizedDescription
                    }
                },
                receiveValue: { [weak self] _ in
                    // User removed from next load
                    self?.sendLoadAction()
                }
            )
            .store(in: &cancellables)
    }

    deinit {
        cancellables.removeAll()
    }
}
```

**ViewController binding:**

```swift
final class UserListViewController: UIViewController {

    // MARK: - Properties

    private let viewModel: UserListViewModel
    private let tableView = UITableView(frame: .zero, style: .plain)
    private let refreshControl = UIRefreshControl()
    private var cancellables = Set<AnyCancellable>()

    // MARK: - Initialization

    init(viewModel: UserListViewModel) {
        self.viewModel = viewModel
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    // MARK: - Lifecycle

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupBindings()
        viewModel.sendLoadAction()
    }

    // MARK: - UI Setup

    private func setupUI() {
        view.backgroundColor = .systemBackground
        title = "Users"

        // Table view
        tableView.translatesAutoresizingMaskIntoConstraints = false
        tableView.register(UserCell.self, forCellReuseIdentifier: UserCell.reuseIdentifier)
        tableView.delegate = self
        tableView.dataSource = self
        view.addSubview(tableView)

        NSLayoutConstraint.activate([
            tableView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            tableView.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])

        // Refresh control
        refreshControl.addTarget(self, action: #selector(refreshTapped), for: .valueChanged)
        tableView.refreshControl = refreshControl
    }

    // MARK: - Bindings

    private func setupBindings() {
        // Bind loading state
        viewModel.$isLoading
            .receive(on: DispatchQueue.main)
            .sink { [weak self] isLoading in
                if isLoading {
                    self?.showLoadingIndicator()
                } else {
                    self?.hideLoadingIndicator()
                }
            }
            .store(in: &cancellables)

        // Bind users to table view
        viewModel.$users
            .receive(on: DispatchQueue.main)
            .sink { [weak self] _ in
                self?.tableView.reloadData()
            }
            .store(in: &cancellables)

        // Bind error message
        viewModel.$errorMessage
            .compactMap { $0 }
            .receive(on: DispatchQueue.main)
            .sink { [weak self] message in
                self?.showErrorAlert(message)
            }
            .store(in: &cancellables)

        // Bind refresh state
        viewModel.$isRefreshing
            .receive(on: DispatchQueue.main)
            .sink { [weak self] isRefreshing in
                if isRefreshing {
                    self?.refreshControl.beginRefreshing()
                } else {
                    self?.refreshControl.endRefreshing()
                }
            }
            .store(in: &cancellables)
    }

    // MARK: - Actions

    @objc private func refreshTapped() {
        viewModel.sendRefreshAction()
    }

    // MARK: - UI Helpers

    private func showLoadingIndicator() {
        // Show overlay loading indicator
    }

    private func hideLoadingIndicator() {
        // Hide overlay loading indicator
    }

    private func showErrorAlert(_ message: String) {
        let alert = UIAlertController(
            title: "Error",
            message: message,
            preferredStyle: .alert
        )
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
}

// MARK: - UITableViewDataSource & Delegate

extension UserListViewController: UITableViewDataSource, UITableViewDelegate {

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        viewModel.users.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(
            withIdentifier: UserCell.reuseIdentifier,
            for: indexPath
        ) as? UserCell else {
            return UITableViewCell()
        }

        let user = viewModel.users[indexPath.row]
        cell.configure(with: user)
        return cell
    }

    func tableView(_ tableView: UITableView, trailingSwipeActionsConfigurationForRowAt indexPath: IndexPath) -> UISwipeActionsConfiguration? {
        let deleteAction = UIContextualAction(style: .destructive, title: "Delete") { [weak self] _, _, completion in
            let user = self?.viewModel.users[indexPath.row]
            self?.viewModel.sendDeleteAction(for: user?.id ?? UUID())
            completion(true)
        }
        return UISwipeActionsConfiguration(actions: [deleteAction])
    }
}
```

### Combine Operators — Production Patterns

**Error handling with catch and replaceError:**

```swift
// Recover from error with default value
apiClient.fetchUsers()
    .catch { error -> AnyPublisher<[User], Never> in
        // Log error, return empty array
        Logger.error("Failed to fetch users: \(error)")
        return Just([]).eraseToAnyPublisher()
    }
    .receive(on: DispatchQueue.main)
    .sink { users in
        self.users = users
    }
    .store(in: &cancellables)

// Replace error with specific value
apiClient.fetchUserProfile()
    .replaceError(with: .defaultProfile)
    .sink { profile in
        self.profile = profile
    }
    .store(in: &cancellables)
```

**Debouncing user input:**

```swift
private let searchSubject = PassthroughSubject<String, Never>()
private var cancellables = Set<AnyCancellable>()

func setupSearchBinding() {
    searchSubject
        .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
        .removeDuplicates()
        .filter { !$0.isEmpty }
        .flatMap { [weak self] query -> AnyPublisher<[SearchResult], Error> in
            guard let self else { return Empty().eraseToAnyPublisher() }
            return searchService.search(query: query)
        }
        .replaceError(with: [])
        .receive(on: DispatchQueue.main)
        .sink { [weak self] results in
            self?.searchResults = results
        }
        .store(in: &cancellables)
}

// Called from UITextField delegate
func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool {
    let newText = (textField.text as NSString?)?.replacingCharacters(in: range, with: string) ?? ""
    searchSubject.send(newText)
    return true
}
```

**Combining multiple publishers:**

```swift
// Combine latest — emits when any publisher emits
Publishers.CombineLatest(userPublisher, preferencesPublisher)
    .map { user, preferences in
        UserProfileViewModel(user: user, preferences: preferences)
    }
    .receive(on: DispatchQueue.main)
    .sink { [weak self] viewModel in
        self?.updateUI(with: viewModel)
    }
    .store(in: &cancellables)

// Merge — emits from any publisher
let tapPublisher = tapGesture.publisher
let swipePublisher = swipeGesture.publisher

Publishers.Merge(tapPublisher, swipePublisher)
    .sink { [weak self] gesture in
        self?.handleGesture(gesture)
    }
    .store(in: &cancellables)

// Zip — waits for all publishers to emit once
let userInfoPublisher = apiClient.fetchUserInfo()
let settingsPublisher = apiClient.fetchSettings()

Publishers.Zip(userInfoPublisher, settingsPublisher)
    .map { userInfo, settings in
        AppConfiguration(userInfo: userInfo, settings: settings)
    }
    .sink(
        receiveCompletion: { /* handle error */ },
        receiveValue: { [weak self] config in
            self?.applyConfiguration(config)
        }
    )
    .store(in: &cancellables)
```

### Reactive UIKit Extensions

```swift
// MARK: - UIControl Publisher Extension

extension UIControl {
    func publisher(for event: UIControl.Event) -> UIControlPublisher {
        UIControlPublisher(control: self, events: event)
    }
}

final class UIControlPublisher: Publisher {
    typealias Output = UIControl
    typealias Failure = Never

    private let control: UIControl
    private let events: UIControl.Event

    init(control: UIControl, events: UIControl.Event) {
        self.control = control
        self.events = events
    }

    func receive<S: Subscriber>(subscriber: S) where S.Input == Output, S.Failure == Failure {
        let subscription = UIControlSubscription(subscriber: subscriber, control: control, events: events)
        subscriber.receive(subscription: subscription)
    }
}

final class UIControlSubscription<S: Subscriber, Control: UIControl>: Subscription where S.Input == Control {
    private var subscriber: S?
    private weak var control: Control?

    init(subscriber: S, control: Control, events: UIControl.Event) {
        self.subscriber = subscriber
        self.control = control
        control.addTarget(self, action: #selector(eventFired), for: events)
    }

    func request(_ demand: Subscribers.Demand) {}

    func cancel() {
        subscriber = nil
    }

    @objc private func eventFired() {
        guard let control = control else { return }
        _ = subscriber?.receive(control)
    }
}

// Usage
button.publisher(for: .touchUpInside)
    .sink { _ in
        print("Button tapped")
    }
    .store(in: &cancellables)

// MARK: - UITextField Text Publisher

extension UITextField {
    var textPublisher: AnyPublisher<String, Never> {
        NotificationCenter.default
            .publisher(for: UITextField.textDidChangeNotification, object: self)
            .compactMap { ($0.object as? UITextField)?.text }
            .eraseToAnyPublisher()
    }
}

// MARK: - UIGestureRecognizer Publisher

extension UIGestureRecognizer {
    var publisher: AnyPublisher<UIGestureRecognizer, Never> {
        gesturePublisher
    }

    private var gesturePublisher: AnyPublisher<UIGestureRecognizer, Never> {
        GesturePublisher(gesture: self).eraseToAnyPublisher()
    }
}

final class GesturePublisher: Publisher {
    typealias Output = UIGestureRecognizer
    typealias Failure = Never

    private let gesture: UIGestureRecognizer

    init(gesture: UIGestureRecognizer) {
        self.gesture = gesture
    }

    func receive<S: Subscriber>(subscriber: S) where S.Input == Output, S.Failure == Failure {
        let subscription = GestureSubscription(subscriber: subscriber, gesture: gesture)
        subscriber.receive(subscription: subscription)
    }
}
```

### Testing Combine Publishers

```swift
import XCTest
import Combine

final class UserListViewModelTests: XCTestCase {

    private var viewModel: UserListViewModel!
    private var mockRepository: MockUserRepository!
    private var cancellables = Set<AnyCancellable>()

    override func setUp() {
        super.setUp()
        mockRepository = MockUserRepository()
        viewModel = UserListViewModel(
            userRepository: mockRepository,
            scheduler: .immediate
        )
    }

    override func tearDown() {
        cancellables.removeAll()
        viewModel = nil
        super.tearDown()
    }

    func test_loadAction_emitsUsers() {
        // Given
        let expectedUsers = [
            User(id: UUID(), name: "Alice", email: "alice@example.com"),
            User(id: UUID(), name: "Bob", email: "bob@example.com")
        ]
        mockRepository.users = expectedUsers

        // When
        let expectation = XCTestExpectation(description: "Users loaded")
        viewModel.$users
            .dropFirst()  // Skip initial empty state
            .sink { users in
                XCTAssertEqual(users.count, 2)
                XCTAssertEqual(users[0].name, "Alice")
                expectation.fulfill()
            }
            .store(in: &cancellables)

        viewModel.sendLoadAction()

        // Then
        wait(for: [expectation], timeout: 1.0)
    }

    func test_loadAction_handlesError() {
        // Given
        mockRepository.shouldFail = true

        // When
        let expectation = XCTestExpectation(description: "Error emitted")
        viewModel.$errorMessage
            .dropFirst()
            .sink { message in
                XCTAssertNotNil(message)
                expectation.fulfill()
            }
            .store(in: &cancellables)

        viewModel.sendLoadAction()

        // Then
        wait(for: [expectation], timeout: 1.0)
    }
}
```

## Pipeline Integration

- **Stage 3 (Architecture):** ADR establishes Combine as reactive framework for UIKit screens. MVVM pattern with Combine publishers.
- **Stage 5 (Development):** Primary skill for UIKit screens using reactive patterns. All data binding, event streams, and subscription management.
- **Stage 6 (Code Review):** Combine review: subscription lifecycle, memory leak prevention, operator correctness, scheduler usage.
- **Stage 7 (Automated Testing):** Publisher testing with XCTest expectations; mock publishers for dependency injection.

## Quality Standards

- **100%** subscriptions stored in `Set<AnyCancellable>` and cancelled on deinit
- **Zero** force unwraps in Combine chains — use `compactMap` for optional filtering
- All publishers scheduled on appropriate scheduler — UI publishers on **Main**, background on **background queue**
- **Zero** UIKit logic in ViewModel — ViewModel only exposes publishers and accepts actions
- Debounce applied to **all user input** streams (search, text fields) — minimum 300ms
- Error handling at **appropriate boundary** — catch in ViewModel, not in View
- **Zero** memory leaks under Instruments Allocations — verified for all ViewControllers
- Combine operators used correctly — `flatMap` for async, `map` for sync, `switchToLatest` for cancellable chains
- All custom publishers conform to `Publisher` protocol with proper subscription lifecycle
- Test coverage for all Combine chains — publisher output verified with XCTest expectations
