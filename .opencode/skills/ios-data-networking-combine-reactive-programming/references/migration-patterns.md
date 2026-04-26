# Migration Patterns

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
