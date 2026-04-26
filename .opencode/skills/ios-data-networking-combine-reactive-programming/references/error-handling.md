# Error Handling

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
