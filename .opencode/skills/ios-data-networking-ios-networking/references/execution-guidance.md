# Execution Guidance

## Execution Guidance

### URLSession — Production Configuration

```swift
// MARK: - Network Client Factory

enum NetworkClientFactory {

    static func defaultClient(
        additionalHeaders: [String: String] = [:],
        timeout: TimeInterval = 30
    ) -> URLSession {
        let configuration = URLSessionConfiguration.default
        configuration.httpAdditionalHeaders = [
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-App-Version": Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "",
            "X-Platform": "iOS",
            "X-Device-Model": deviceModel()
        ].merging(additionalHeaders) { $1 }

        configuration.timeoutIntervalForRequest = timeout
        configuration.timeoutIntervalForResource = 60
        configuration.waitsForConnectivity = true  // Wait for network instead of failing immediately
        configuration.httpMaximumConnectionsPerHost = 4

        // Cache configuration
        configuration.urlCache = URLCache(
            memoryCapacity: 50 * 1024 * 1024,  // 50MB
            diskCapacity: 200 * 1024 * 1024,   // 200MB
            diskPath: "com.example.app.cache"
        )

        return URLSession(configuration: configuration)
    }

    static func ephemeralClient() -> URLSession {
        let configuration = URLSessionConfiguration.ephemeral
        configuration.httpAdditionalHeaders = [
            "Accept": "application/json",
            "Content-Type": "application/json"
        ]
        configuration.timeoutIntervalForRequest = 15
        // No disk cache — all in-memory only
        return URLSession(configuration: configuration)
    }

    static func backgroundClient(identifier: String) -> URLSession {
        let configuration = URLSessionConfiguration.background(withIdentifier: identifier)
        configuration.isDiscretionary = true  // Let OS optimize timing
        configuration.sessionSendsLaunchEvents = true
        configuration.httpMaximumConnectionsPerHost = 2
        return URLSession(configuration: configuration)
    }

    private static func deviceModel() -> String {
        var systemInfo = utsname()
        uname(&systemInfo)
        return withUnsafePointer(to: &systemInfo.machine) {
            $0.withMemoryRebound(to: CChar.self, capacity: 1) { String(cString: $0) }
        }
    }
}
```

### Async/Await Network Layer — Modern API

```swift
// MARK: - API Client

actor APIClient {
    private let session: URLSession
    private let baseURL: URL
    private let authProvider: AuthProvider
    private let decoder: JSONDecoder

    init(
        session: URLSession = NetworkClientFactory.defaultClient(),
        baseURL: URL,
        authProvider: AuthProvider,
        decoder: JSONDecoder = .appDecoder()
    ) {
        self.session = session
        self.baseURL = baseURL
        self.authProvider = authProvider
        self.decoder = decoder
    }

    // MARK: - GET

    func get<T: Decodable>(_ endpoint: String, queryItems: [URLQueryItem] = []) async throws -> T {
        var urlComponents = URLComponents(url: baseURL.appendingPathComponent(endpoint), resolvingAgainstBaseURL: true)!
        urlComponents.queryItems = queryItems

        var request = URLRequest(url: urlComponents.url!)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        return try await execute(request, decoder: decoder)
    }

    // MARK: - POST

    func post<T: Decodable, B: Encodable>(_ endpoint: String, body: B) async throws -> T {
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder.appEncoder().encode(body)

        return try await execute(request, decoder: decoder)
    }

    // MARK: - PUT

    func put<T: Decodable, B: Encodable>(_ endpoint: String, body: B) async throws -> T {
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = "PUT"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder.appEncoder().encode(body)

        return try await execute(request, decoder: decoder)
    }

    // MARK: - DELETE

    func delete(_ endpoint: String) async throws {
        let request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        // DELETE is idempotent — safe to retry on failure
        _ = try await execute(request, decoder: decoder) as APIResponse<Void>
    }

    // MARK: - Execution

    private func execute<T: Decodable>(_ request: URLRequest, decoder: JSONDecoder) async throws -> T {
        var authenticatedRequest = try await authenticate(request)

        do {
            let (data, response) = try await session.data(for: authenticatedRequest)
            try validateResponse(response)
            return try decoder.decode(T.self, from: data)
        } catch APIError.unauthorized {
            // Token expired — refresh and retry once
            try await authProvider.refreshToken()
            authenticatedRequest = try await authenticate(request)

            let (data, response) = try await session.data(for: authenticatedRequest)
            try validateResponse(response)
            return try decoder.decode(T.self, from: data)
        } catch {
            throw mapError(error)
        }
    }

    private func authenticate(_ request: URLRequest) async throws -> URLRequest {
        guard let token = try await authProvider.accessToken() else {
            throw APIError.unauthenticated
        }

        var authenticatedRequest = request
        authenticatedRequest.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        return authenticatedRequest
    }

    private func validateResponse(_ response: URLResponse) throws {
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        switch httpResponse.statusCode {
        case 200..<300:
            return
        case 401:
            throw APIError.unauthorized
        case 400..<500:
            throw APIError.clientError(statusCode: httpResponse.statusCode)
        case 500..<600:
            throw APIError.serverError(statusCode: httpResponse.statusCode)
        default:
            throw APIError.unknown
        }
    }

    private func mapError(_ error: Error) -> APIError {
        if let apiError = error as? APIError {
            return apiError
        }

        let nsError = error as NSError
        switch (nsError.domain, nsError.code) {
        case (NSURLErrorDomain, NSURLErrorNotConnectedToInternet),
             (NSURLErrorDomain, NSURLErrorNetworkConnectionLost):
            return .networkUnavailable
        case (NSURLErrorDomain, NSURLErrorTimedOut):
            return .timeout
        case (NSURLErrorDomain, NSURLErrorCannotFindHost),
             (NSURLErrorDomain, NSURLErrorCannotConnectToHost):
            return .dnsFailure
        default:
            return .unknown
        }
    }
}

// MARK: - Error Types

enum APIError: Error, Equatable {
    case unauthenticated
    case unauthorized
    case clientError(statusCode: Int)
    case serverError(statusCode: Int)
    case networkUnavailable
    case timeout
    case dnsFailure
    case invalidResponse
    case decodingFailed(Error)
    case unknown

    var userMessage: String {
        switch self {
        case .unauthenticated:
            return "Please log in to continue."
        case .unauthorized:
            return "You don't have permission to perform this action."
        case .clientError:
            return "There was a problem with your request. Please try again."
        case .serverError:
            return "We're experiencing technical difficulties. Please try again later."
        case .networkUnavailable:
            return "Check your internet connection and try again."
        case .timeout:
            return "The request took too long. Please try again."
        case .dnsFailure:
            return "Unable to connect to the server. Please check your connection."
        case .invalidResponse:
            return "Received an invalid response from the server."
        case .decodingFailed:
            return "Unable to process the server response."
        case .unknown:
            return "An unexpected error occurred. Please try again."
        }
    }
}

// MARK: - API Response Wrapper

struct APIResponse<T: Decodable>: Decodable {
    let data: T?
    let error: APIErrorResponse?
    let meta: ResponseMeta?

    func getOrThrow() throws -> T {
        if let data = data { return data }
        throw error ?? APIErrorResponse(message: "Unknown error")
    }
}

struct APIErrorResponse: Decodable, Equatable {
    let code: String
    let message: String
    let details: [String: String]?
}

struct ResponseMeta: Decodable {
    let requestId: String
    let timestamp: String
}
```

### HTTP Caching Strategy

```swift
// MARK: - Cache Policy Selection

enum CachePolicy {
    /// Always fetch from network, cache response
    case networkFirst

    /// Use cache if available, refresh in background
    case cacheFirst(maxAge: TimeInterval)

    /// Only use cache, never hit network
    case cacheOnly

    /// Never use cache, always hit network
    case networkOnly

    var urlRequestCachePolicy: URLRequest.CachePolicy {
        switch self {
        case .networkFirst:
            return .useProtocolCachePolicy  // Respects Cache-Control headers
        case .cacheFirst:
            return .returnCacheDataElseLoad
        case .cacheOnly:
            return .returnCacheDataDontLoad
        case .networkOnly:
            return .reloadIgnoringLocalCacheData
        }

```

    }

}

// MARK: - Conditional Requests (ETag)

actor ConditionalRequestCache {
private var etags: [String: String] = [:] // URL -> ETag
private var lastModified: [String: String] = [:]

    func applyConditionalHeaders(to request: inout URLRequest) {
        let urlString = request.url?.absoluteString ?? ""
        if let etag = etags[urlString] {
            request.setValue(etag, forHTTPHeaderField: "If-None-Match")
        }
        if let modified = lastModified[urlString] {
            request.setValue(modified, forHTTPHeaderField: "If-Modified-Since")
        }
    }

    func storeResponseHeaders(_ response: HTTPURLResponse, for url: String) {
        if let etag = response.allHeaderFields["ETag"] as? String {
            etags[url] = etag
        }
        if let modified = response.allHeaderFields["Last-Modified"] as? String {
            lastModified[url] = modified
        }
    }

    func invalidate(url: String) {
        etags.removeValue(forKey: url)
        lastModified.removeValue(forKey: url)
    }

}

// MARK: - Stale-While-Revalidate Pattern

actor StaleWhileRevalidateCache<T: Decodable> {
private struct CachedEntry {
let data: T
let timestamp: Date
let maxAge: TimeInterval
}

    private var cache: [String: CachedEntry] = [:]
    private let apiClient: APIClient

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func fetch(
        _ endpoint: String,
        maxAge: TimeInterval = 300,
        decoder: JSONDecoder
    ) async throws -> T {
        let key = endpoint

        // Check cache
        if let entry = cache[key], Date().timeIntervalSince(entry.timestamp) < maxAge {
            // Fresh cache — return immediately, refresh in background
            Task.detached {
                try? await self.refresh(endpoint, key: key, decoder: decoder)
            }
            return entry.data
        }

        // Stale or missing — fetch from network
        let freshData: T = try await apiClient.get(endpoint)

        cache[key] = CachedEntry(
            data: freshData,
            timestamp: Date(),
            maxAge: maxAge
        )

        return freshData
    }

    private func refresh(_ endpoint: String, key: String, decoder: JSONDecoder) async throws {
        let freshData: T = try await apiClient.get(endpoint)
        cache[key] = CachedEntry(
            data: freshData,
            timestamp: Date(),
            maxAge: cache[key]?.maxAge ?? 300
        )
    }

    func invalidate(endpoint: String) {
        cache.removeValue(forKey: endpoint)
    }

}

````

### Retry Strategy with Circuit Breaker

```swift
// MARK: - Retry Configuration

struct RetryConfiguration {
    let maxRetries: Int
    let baseDelay: TimeInterval
    let maxDelay: TimeInterval
    let retryableStatusCodes: Set<Int>
    let retryableErrors: Set<APIError>

    static let `default` = RetryConfiguration(
        maxRetries: 3,
        baseDelay: 1.0,
        maxDelay: 30.0,
        retryableStatusCodes: [408, 429, 500, 502, 503, 504],
        retryableErrors: [.networkUnavailable, .timeout]
    )

    static let aggressive = RetryConfiguration(
        maxRetries: 5,
        baseDelay: 0.5,
        maxDelay: 60.0,
        retryableStatusCodes: [408, 429, 500, 502, 503, 504],
        retryableErrors: [.networkUnavailable, .timeout, .dnsFailure]
    )
}

// MARK: - Retry with Exponential Backoff

func executeWithRetry<T>(
    _ operation: () async throws -> T,
    configuration: RetryConfiguration = .default
) async throws -> T {
    var lastError: Error?

    for attempt in 0...configuration.maxRetries {
        do {
            return try await operation()
        } catch let error as APIError where configuration.retryableErrors.contains(error) {
            lastError = error
            if attempt < configuration.maxRetries {
                let delay = calculateBackoff(
                    attempt: attempt,
                    baseDelay: configuration.baseDelay,
                    maxDelay: configuration.maxDelay
                )
                try await Task.sleep(for: .seconds(delay))
            }
        } catch let error as URLError where isRetryableURLError(error) {
            lastError = error
            if attempt < configuration.maxRetries {
                let delay = calculateBackoff(
                    attempt: attempt,
                    baseDelay: configuration.baseDelay,
                    maxDelay: configuration.maxDelay
                )
                try await Task.sleep(for: .seconds(delay))
            }
        } catch {
            throw error  // Non-retryable error — fail immediately
        }
    }

    throw lastError ?? APIError.unknown
}

private func calculateBackoff(attempt: Int, baseDelay: TimeInterval, maxDelay: TimeInterval) -> TimeInterval {
    let exponential = baseDelay * pow(2.0, Double(attempt))
    let jitter = Double.random(in: 0...exponential)
    return min(jitter, maxDelay)
}

private func isRetryableURLError(_ error: URLError) -> Bool {
    switch error.code {
    case .notConnectedToInternet, .networkConnectionLost, .timedOut:
        return true
    default:
        return false
    }
}

// MARK: - Circuit Breaker

actor CircuitBreaker {
    enum State {
        case closed  // Normal operation
        case open    // Failing — reject requests
        case halfOpen  // Testing recovery
    }

    private var state: State = .closed
    private var failureCount = 0
    private let failureThreshold: Int
    private let recoveryTimeout: TimeInterval
    private var lastFailureTime: Date?

    init(failureThreshold: Int = 5, recoveryTimeout: TimeInterval = 60) {
        self.failureThreshold = failureThreshold
        self.recoveryTimeout = recoveryTimeout
    }

    func canExecute() -> Bool {
        switch state {
        case .closed:
            return true
        case .open:
            if let lastFailure = lastFailureTime,
               Date().timeIntervalSince(lastFailure) > recoveryTimeout {
                state = .halfOpen
                return true
            }
            return false
        case .halfOpen:
            return true
        }
    }

    func recordSuccess() {
        failureCount = 0
        state = .closed
    }

    func recordFailure() {
        failureCount += 1
        lastFailureTime = Date()
        if failureCount >= failureThreshold {
            state = .open
        }
    }
}
````

### Reachability Monitoring

```swift
import Network

@MainActor
final class NetworkMonitor: ObservableObject {
    private let monitor = NWPathMonitor()
    private let queue = DispatchQueue(label: "NetworkMonitor")

    @Published private(set) var isConnected = false
    @Published private(set) var connectionType: ConnectionType = .unknown

    enum ConnectionType {
        case wifi, cellular, ethernet, unknown
    }

    init() {
        monitor.pathUpdateHandler = { [weak self] path in
            Task { @MainActor [weak self] in
                self?.isConnected = path.status == .satisfied
                self?.connectionType = path.connectionType
            }
        }
        monitor.start(queue: queue)
    }

    deinit {
        monitor.cancel()
    }
}

extension NWPath {
    var connectionType: NetworkMonitor.ConnectionType {
        if usesInterfaceType(.wifi) { return .wifi }
        if usesInterfaceType(.cellular) { return .cellular }
        if usesInterfaceType(.wiredEthernet) { return .ethernet }
        return .unknown
    }
}
```
