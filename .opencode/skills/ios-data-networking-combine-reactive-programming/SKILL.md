---
name: ios-data-networking-combine-reactive-programming
description: "Combine reactive programming for iOS apps — publishers, subscribers, operators, subjects, error handling, SwiftUI @Published integration, UIKit bridging, and cancellable lifecycle management. Owned by Seo-Yeon Park (iOS Lead). Use during Stage 5 (Development) for reactive state management in UIKit screens and Stage 7 (Automated Testing) for publisher testing. Trigger: combine, publisher, subscriber, @published, observableobject, passthroughsubject, currentvaluesubject, anycancellable, debounce, flatmap, sink, assign."
prerequisites:
  - ios-data-networking-ios-networking

version: "1.0.0"
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

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`error-handling.md`](references/error-handling.md) — Error Handling
- [`swiftui-integration.md`](references/swiftui-integration.md) — SwiftUI Integration
- [`uikit-integration.md`](references/uikit-integration.md) — UIKit Integration
- [`memory-management.md`](references/memory-management.md) — Memory Management
- [`testing-combine.md`](references/testing-combine.md) — Testing Combine
- [`migration-patterns.md`](references/migration-patterns.md) — Migration Patterns
