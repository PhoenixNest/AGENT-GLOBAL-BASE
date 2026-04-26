# Testing Combine

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
