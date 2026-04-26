# Memory Management

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
