---
name: ios-data-networking-combine-reactive-programming
description: 'Ios skill: Combine Reactive Programming'
---

# Combine Framework — Reactive Programming

## Overview

The Combine framework provides a declarative Swift API for processing values over time. It introduces a unified model for handling asynchronous events, replacing callback-based patterns with a composable, type-safe publisher-subscriber architecture.

**Scope:** Combine applies to iOS 13.0+, macOS 10.15+, tvOS 13.0+, and watchOS 6.0+. It is the preferred reactive framework for all modern iOS development within this company's iOS applications.

**Legacy UIKit Context:** Prior to Combine, iOS apps relied on delegate protocols, target-action patterns, notification center observers, and closure-based callbacks for asynchronous work. These approaches scatter event-hand logic across classes, lack composability, and make error propagation cumbersome. Combine unifies all these patterns under a single model where any asynchronous source becomes a `Publisher` that can be transformed, combined, and consumed by a `Subscriber`.

**Design Principle:** Think of Combine as a pipeline: Publishers emit values (or errors/completion), Operators transform those values as they flow downstream, and Subscribers consume the final results. The entire pipeline is managed through `Cancellable` handles that control the lifecycle.

---

## Core Concepts

### Publishers

A `Publisher` is a type that emits a stream of values over time. Every publisher has two associated types: `Output` (the value type it emits) and `Failure` (the error type it can emit, or `Never` if it cannot fail).

```swift
// Publishers emit Output or Failure
protocol Publisher {
    associatedtype Output
    associatedtype Failure: Error
    func receive<S: Subscriber>(subscriber: S)
        where S.Input == Output, S.Failure == Failure
}
```

**Common Publishers:**

```swift
// 1. Just — emits a single value then completes
Just(42)

// 2. Future — produces a single value asynchronously
Future<Int, Never> { promise in
    promise(.success(42))
}

// 3. URLSession.DataTaskPublisher — network requests
URLSession.shared.dataTaskPublisher(for: url)

// 4. PassthroughSubject — manual event injection
let subject = PassthroughSubject<String, Never>()
subject.send("event")
subject.send(completion: .finished)

// 5. CurrentValueSubject — holds a current value
let state = CurrentValueSubject<Int, Never>(0)
state.send(1)
print(state.value) // 1

// 6. Deferred — defers publisher creation until subscription
Deferred {
    Future<Int, Never> { promise in
        promise(.success(Int.random(in: 0...100)))
    }
}
```

### Subscribers

A `Subscriber` receives values from a publisher. It defines how many values to request and what to do when values arrive.

```swift
protocol Subscriber {
    associatedtype Input
    associatedtype Failure: Error
    func receive(subscription: Subscription)
    func receive(_ input: Input) -> Subscribers.Demand
    func receive(completion: Subscribers.Completion<Failure>)
}
```

**Common Subscription Patterns:**

```swift
// Using sink (most common — creates an anonymous subscriber)
let cancellable = publisher
    .sink(
        receiveCompletion: { completion in
            switch completion {
            case .finished: break
            case .failure(let error): print(error)
            }
        },
        receiveValue: { value in print(value) }
    )

// Using assign (binds to a property via key path)
let cancellable = publisher
    .assign(to: \.text, on: label)

// Using subscribe (custom subscriber implementation)
publisher.subscribe(customSubscriber)
```

### Operators

Operators transform, filter, combine, or otherwise manipulate the data stream between a publisher and its subscriber. Each operator returns a new publisher that wraps the upstream publisher.

```swift
// Operator chain example
publisher
    .map { $0.uppercased() }          // Transform
    .filter { $0.count > 3 }          // Filter
    .removeDuplicates()               // Deduplicate
    .debounce(for: .seconds(0.5),     // Rate-limit
              scheduler: RunLoop.main)
    .eraseToAnyPublisher()            // Type-erase
```

### Subjects

Subjects are the bridge between imperative and reactive code. They are both publishers (they emit values) and allow manual value injection.

```swift
// PassthroughSubject — does not store values, only forwards
let events = PassthroughSubject<UIEvent, Never>()
events.send(uiEvent)  // Imperative injection
events.send(completion: .finished)

// CurrentValueSubject — stores the latest value
let count = CurrentValueSubject<Int, Never>(0)
count.send(1)
print(count.value)  // Always accessible
```

**When to use which:**

- Use `PassthroughSubject` for event streams where past values are irrelevant (e.g., button taps, lifecycle events).
- Use `CurrentValueSubject` for state that always has a current value (e.g., user profile, settings, counters).

---

## Common Operators

### Transformation Operators

```swift
// map — transform output type
Just("hello")
    .map { $0.uppercased() }  // AnyPublisher<String, Never>

// tryMap — transform with throwing
Just("42")
    .tryMap { Int($0) }  // AnyPublisher<Int, Error>

// flatMap — transform into another publisher, merge results
Just("user123")
    .flatMap { id in
        fetchUser(id: id)  // returns AnyPublisher<User, Error>
    }

// scan — accumulate values (like reduce over time)
[1, 2, 3, 4].publisher
    .scan(0, +)  // Emits: 1, 3, 6, 10
```

### Filtering Operators

```swift
// filter — conditional passthrough
numbers.publisher
    .filter { $0 > 10 }

// removeDuplicates — skip consecutive equal values
textPublisher
    .removeDuplicates()

// compactMap — transform and filter out nils
strings.publisher
    .compactMap { URL(string: $0) }

// ignoreOutput — only care about completion
apiCallPublisher
    .ignoreOutput()
    .sink { _ in print("Completed") }
```

### Timing Operators

```swift
// debounce — emit only after a pause
searchText
    .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
    .flatMap { query in fetchResults(query) }

// throttle — limit emission rate
scrollEvents
    .throttle(for: .seconds(0.1), scheduler: RunLoop.main, latest: true)

// delay — shift emission timing
publisher
    .delay(for: .seconds(1), scheduler: RunLoop.main)
```

### Combination Operators

```swift
// merge(with:) — interleave two publishers
publisherA.merge(with: publisherB)

// combineLatest — emit tuple when any upstream emits (latest values)
combineLatest(username, password)
    .map { $0.isValid && $1.isValid }

// zip — pair emissions one-to-one
publisherA.zip(publisherB)

// append — sequence publishers
Just("first").append(Just("second"))
```

---

## Error Handling

Combine provides multiple strategies for handling errors within publisher chains.

```swift
// catch — recover from errors with a fallback publisher
apiPublisher
    .catch { error in
        Just(defaultValue)  // Must return same Output type
    }

// replaceError — substitute error with a value
apiPublisher
    .replaceError(with: defaultValue)

// retry — re-subscribe on error (up to N times)
apiPublisher
    .retry(3)
    .catch { error in Just(defaultValue) }

// mapError — transform error type
apiPublisher
    .mapError { $0 as NetworkError }

// assertNoFailure — crash on error (debugging only)
publisher
    .assertNoFailure()
```

**Recommended error handling pattern for network requests:**

```swift
func fetchUser(id: String) -> AnyPublisher<User, NetworkError> {
    URLSession.shared.dataTaskPublisher(for: userURL(id: id))
        .map(\.data)
        .decode(type: User.self, decoder: JSONDecoder())
        .mapError { error -> NetworkError in
            if let networkError = error as? NetworkError {
                return networkError
            }
            if let urlError = error as? URLError {
                return .urlError(urlError)
            }
            return .decodingError(error)
        }
        .receive(on: DispatchQueue.main)
        .eraseToAnyPublisher()
}
```

---

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

## UIKit Integration

### UIControl Publishers

UIKit controls do not natively publish events. Use extensions to bridge UIControl target-action to Combine publishers.

```swift
// UITextField text changes publisher
extension UITextField {
    var textPublisher: AnyPublisher<String, Never> {
        NotificationCenter.default
            .publisher(for: UITextField.textDidChangeNotification, object: self)
            .compactMap { ($0.object as? UITextField)?.text ?? "" }
            .eraseToAnyPublisher()
    }
}

// UIButton tap publisher
extension UIButton {
    var tapPublisher: AnyPublisher<Void, Never> {
        let subject = PassthroughSubject<Void, Never>()
        addTarget(
            closurePublisher(target: subject) { _ in subject.send(()) }
        )
        return subject.eraseToAnyPublisher()
    }
}

// UISwitch value publisher
extension UISwitch {
    var valuePublisher: AnyPublisher<Bool, Never> {
        NotificationCenter.default
            .publisher(for: UIControl.valueChangedNotification, object: self)
            .map { ($0.object as? UISwitch)?.isOn ?? false }
            .eraseToAnyPublisher()
    }
}
```

### NotificationCenter Publishers

`NotificationCenter` natively publishes via the `publisher(for:object:)` method:

```swift
NotificationCenter.default
    .publisher(for: UIApplication.didEnterBackgroundNotification)
    .sink { _ in
        // Handle background transition
    }
    .store(in: &cancellables)

// Keyboard notifications with value extraction
NotificationCenter.default
    .publisher(for: UIResponder.keyboardWillShowNotification)
    .compactMap { notification in
        notification.userInfo?[UIResponder.keyboardFrameEndUserInfoKey] as? CGRect
    }
    .sink { keyboardFrame in
        // Adjust layout for keyboard
    }
    .store(in: &cancellables)
```

---

## Memory Management

### Cancellable Lifecycle

Every subscription creates a `Cancellable`. If not stored, the subscription is immediately cancelled. The standard pattern is to store cancellables in a `Set<AnyCancellable>` owned by the subscriber.

```swift
class MyViewModel: ObservableObject {
    private var cancellables = Set<AnyCancellable>()

    func setupBindings() {
        publisher
            .sink { value in print(value) }
            .store(in: &cancellables)
    }

    // cancellables are automatically cancelled when MyViewModel deinitializes
}
```

**Key Rules:**

| Rule                | Pattern                                                  |
| ------------------- | -------------------------------------------------------- |
| Store in Set        | `.store(in: &cancellables)` — standard pattern           |
| Manual cancellation | `cancellable.cancel()` — when you need explicit control  |
| Automatic cleanup   | `store(in:)` deallocates when the owner deallocates      |
| Avoid retain cycles | Use `[weak self]` in operator closures that capture self |

```swift
// Correct: weak self in flatMap
publisher
    .flatMap { [weak self] value -> AnyPublisher<String, Never> in
        guard let self else { return Empty().eraseToAnyPublisher() }
        return self.transform(value)
    }

// Incorrect: strong self capture (retain cycle risk)
publisher
    .flatMap { value -> AnyPublisher<String, Never> in
        self.transform(value)  // Strong capture
    }
```

### assign(to:on:) Memory Behavior

`assign(to:on:)` does not create a retain cycle when the target object is the same object that owns the cancellables set, because the assignment uses a key path rather than a closure capture. However, when assigning to a different object, use `[weak self]` patterns instead.

---

## Testing Combine

### XCTest Expectations for Publishers

```swift
func testSearchPublisherEmitsResults() {
    let expectation = XCTestExpectation(description: "Emits results")
    var receivedResults: [String] = []

    viewModel.search(query: "test")
        .sink(
            receiveCompletion: { completion in
                if case .failure(let error) = completion {
                    XCTFail("Unexpected error: \(error)")
                }
            },
            receiveValue: { results in
                receivedResults = results
                expectation.fulfill()
            }
        )
        .store(in: &cancellables)

    wait(for: [expectation], timeout: 2.0)
    XCTAssertEqual(receivedResults, ["expected"])
}
```

### Testing Operators with XCTestExpectation

```swift
func testDebounceDeliversOnlyLastValue() {
    let expectation = XCTestExpectation(description: "Debounce delivers")
    var output: [String] = []

    let subject = PassthroughSubject<String, Never>()

    subject
        .debounce(for: .milliseconds(100), scheduler: RunLoop.main)
        .sink { value in
            output.append(value)
            expectation.fulfill()
        }
        .store(in: &cancellables)

    subject.send("a")
    subject.send("b")
    subject.send("c")  // Only this should be emitted after debounce

    wait(for: [expectation], timeout: 1.0)
    XCTAssertEqual(output, ["c"])
}
```

### Testing with TestScheduler

For deterministic testing, use a test scheduler instead of `RunLoop.main`:

```swift
let scheduler = DispatchQueue.test

publisher
    .debounce(for: .seconds(1), scheduler: scheduler)
    .sink { values.append($0) }
    .store(in: &cancellables)

scheduler.advance(by: .seconds(0.5))  // Before debounce window
XCTAssertEqual(values, [])

scheduler.advance(by: .seconds(0.6))  // After debounce window
XCTAssertEqual(values, ["expected"])
```

### Testing Completion and Error Cases

```swift
func testPublisherEmitsError() {
    let expectation = XCTestExpectation(description: "Emits error")

    failingPublisher
        .sink(
            receiveCompletion: { completion in
                if case .failure(let error) = completion {
                    XCTAssertEqual(error as? MyError, MyError.networkFailure)
                    expectation.fulfill()
                }
            },
            receiveValue: { _ in XCTFail("Should not emit value") }
        )
        .store(in: &cancellables)

    wait(for: [expectation], timeout: 1.0)
}
```

---

## Migration Patterns

### Delegate to Combine

```swift
// BEFORE: Delegate pattern
class LocationManager: NSObject, CLLocationManagerDelegate {
    weak var delegate: LocationManagerDelegate?
    private let locationManager = CLLocationManager()

    func startUpdating() {
        locationManager.delegate = self
        locationManager.startUpdatingLocation()
    }

    func locationManager(_ manager: CLLocationManager,
                         didUpdateLocations locations: [CLLocation]) {
        delegate?.didUpdate(locations: locations)
    }
}

// AFTER: Combine publisher
class LocationManager: NSObject {
    private let locationManager = CLLocationManager()
    private let locationSubject = PassthroughSubject<[CLLocation], Never>()

    var locationPublisher: AnyPublisher<[CLLocation], Never> {
        locationSubject.eraseToAnyPublisher()
    }

    override init() {
        super.init()
        locationManager.delegate = self
    }

    func startUpdating() {
        locationManager.startUpdatingLocation()
    }
}

extension LocationManager: CLLocationManagerDelegate {
    func locationManager(_ manager: CLLocationManager,
                         didUpdateLocations locations: [CLLocation]) {
        locationSubject.send(locations)
    }
}

// Consumer usage
locationManager.locationPublisher
    .map { $0.last }
    .compactMap { $0 }
    .sink { location in
        print("Location: \(location.coordinate)")
    }
    .store(in: &cancellables)
```

### Closure to Combine

```swift
// BEFORE: Closure-based API
func fetchUser(id: String, completion: @escaping (Result<User, Error>) -> Void)

// AFTER: Publisher-based API
func fetchUser(id: String) -> AnyPublisher<User, Error> {
    Future { promise in
        self.fetchUser(id: id) { result in
            promise(result)
        }
    }
    .eraseToAnyPublisher()
}

// OR using URLSession directly
func fetchUser(id: String) -> AnyPublisher<User, Error> {
    URLSession.shared.dataTaskPublisher(for: url)
        .map(\.data)
        .decode(type: User.self, decoder: JSONDecoder())
        .eraseToAnyPublisher()
}
```

### Target-Action to Combine

```swift
// BEFORE: Target-action
button.addTarget(self, action: #selector(didTap), for: .touchUpInside)
@objc func didTap() { ... }

// AFTER: Publisher
button.tapPublisher
    .sink { [weak self] in self?.handleTap() }
    .store(in: &cancellables)
```

---

## Stage 5 Integration

During Stage 5 (Development), Combine patterns are integrated into platform codebases as follows:

1. **ViewModel layer:** All view models use `ObservableObject` with `@Published` properties for state. Publishers handle data fetching, validation, and inter-component communication.

2. **Network layer:** `URLSession.DataTaskPublisher` is the primary network primitive. Wrap with `map`, `decode`, `mapError`, and `receive(on:)` to create typed, main-thread-delivered publishers.

3. **Repository layer:** Repositories expose publishers, not closures. Internal implementation may use URLSession, Core Data, or cache — consumers see only publishers.

4. **Cancellation policy:** All cancellables are stored in `Set<AnyCancellable>` owned by the subscribing object (typically a ViewModel). ViewModels are deallocated when their hosting view controller is dismissed, triggering automatic cancellation.

5. **Threading:** Use `subscribe(on:)` for upstream work (network, disk) and `receive(on:)` for downstream delivery (UI updates). The iOS Lead ensures all publishers that touch UI deliver on `DispatchQueue.main`.

6. **Testing:** All Combine-based view models have unit tests using XCTest expectations. Publishers are tested for correct value emission, error handling, and completion behavior.

---

## References

- Apple Developer Documentation: Combine Framework
- WWDC 2019: Introducing Combine
- WWDC 2021: Demystify Combine
- Combine Framework in Practice (Apple sample code)
- `.opencode/skills/ios-ui-ux-swiftui/SKILL.md` — SwiftUI patterns
- `.opencode/skills/ios-data-networking-ios-networking/SKILL.md` — Network layer patterns
