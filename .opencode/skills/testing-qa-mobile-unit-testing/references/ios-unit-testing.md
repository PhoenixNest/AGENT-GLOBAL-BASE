# iOS Unit Testing

## iOS Unit Testing

### Testing Stack

| Component      | Framework                             | Purpose                               |
| -------------- | ------------------------------------- | ------------------------------------- |
| Test Framework | XCTest                                | Traditional test framework            |
| Test Framework | Swift Testing                         | Modern Swift-native testing (iOS 18+) |
| Mocking        | Manual (protocols) or Cuckoo          | Dependency injection                  |
| Assertions     | XCTestAssertions / Swift Expectations | Test assertions                       |
| Async Testing  | XCTest async/await                    | Testing async/await code              |
| Code Coverage  | Xcode Coverage                        | Built-in coverage reporting           |

### Project Structure

```
App/
├── App/                    # Production code
│   ├── Data/
│   │   ├── Repository/
│   │   ├── Local/
│   │   └── Remote/
│   ├── Domain/
│   │   ├── Model/
│   │   └── UseCase/
│   └── Presentation/
│       ├── ViewModel/
│       └── Views/
└── AppTests/               # Unit tests
    ├── Data/
    │   └── Repository/
    │       └── UserRepositoryTests.swift
    └── Domain/
        └── UseCase/
            └── LoginUseCaseTests.swift
```

### XCTest Test Patterns

**Basic Test Structure:**

```swift
import XCTest
@testable import App

@MainActor
final class LoginUseCaseTests: XCTestCase {

    var userRepository: MockUserRepository!
    var loginUseCase: LoginUseCase!

    override func setUpWithError() throws {
        try super.setUpWithError()
        userRepository = MockUserRepository()
        loginUseCase = LoginUseCase(repository: userRepository)
    }

    override func tearDownWithError() throws {
        loginUseCase = nil
        userRepository = nil
        try super.tearDownWithError()
    }

    // MARK: - Valid Credentials

    func test_loginWithValidCredentials_returnsSuccess() async {
        // Given
        let email = "alice@example.com"
        let password = "SecurePass123!"
        let expectedUser = User(id: "1", name: "Alice", email: email)
        userRepository.mockedLoginResult = .success(expectedUser)

        // When
        let result = await loginUseCase.execute(email: email, password: password)

        // Then
        switch result {
        case .success(let user):
            XCTAssertEqual(user.id, "1")
            XCTAssertEqual(user.name, "Alice")
            XCTAssertEqual(user.email, email)
        case .failure:
            XCTFail("Expected success but got failure")
        }

        XCTAssertEqual(userRepository.loginCallCount, 1)
        XCTAssertEqual(userRepository.lastLoginEmail, email)
    }

    // MARK: - Invalid Credentials

    func test_loginWithEmptyEmail_returnsValidationError() async {
        // When
        let result = await loginUseCase.execute(email: "", password: "password123")

        // Then
        switch result {
        case .success:
            XCTFail("Expected validation error but got success")
        case .failure(let error):
            XCTAssertTrue(error is ValidationError)
        }
    }

    func test_loginWithWrongPassword_returnsAuthenticationError() async {
        // Given
        userRepository.mockedLoginResult = .failure(
            AuthenticationError.invalidCredentials
        )

        // When
        let result = await loginUseCase.execute(
            email: "user@test.com",
            password: "wrong"
        )

        // Then
        switch result {
        case .success:
            XCTFail("Expected auth error but got success")
        case .failure(let error):
            XCTAssertTrue(error is AuthenticationError)
        }
    }

    // MARK: - Network Failure

    func test_loginWithNetworkFailure_returnsNetworkError() async {
        // Given
        userRepository.mockedLoginResult = .failure(
            NetworkError.connectionTimeout
        )

        // When
        let result = await loginUseCase.execute(
            email: "user@test.com",
            password: "password"
        )

        // Then
        switch result {
        case .success:
            XCTFail("Expected network error but got success")
        case .failure(let error):
            XCTAssertTrue(error is NetworkError)
        }
    }
}
```

### Swift Testing (Modern, iOS 18+)

```swift
import Testing
@testable import App

@Suite("LoginUseCase Tests")
@MainActor
struct LoginUseCaseTests {

    var userRepository: MockUserRepository!
    var loginUseCase: LoginUseCase!

    init() async throws {
        userRepository = MockUserRepository()
        loginUseCase = LoginUseCase(repository: userRepository)
    }

    @Test("Login with valid credentials returns success")
    func loginWithValidCredentials() async {
        let expectedUser = User(id: "1", name: "Alice", email: "alice@example.com")
        userRepository.mockedLoginResult = .success(expectedUser)

        let result = await loginUseCase.execute(
            email: "alice@example.com",
            password: "SecurePass123!"
        )

        switch result {
        case .success(let user):
            #expect(user.id == "1")
            #expect(user.name == "Alice")
            #expect(user.email == "alice@example.com")
        case .failure(let error):
            Issue.record("Expected success but got \(error)")
        }
    }

    @Test("Login with empty email returns validation error")
    @Arguments(["", "   ", "\t", "\n"])
    func loginWithInvalidEmail(email: String) async {
        let result = await loginUseCase.execute(email: email, password: "password123")

        switch result {
        case .success:
            Issue.record("Expected validation error but got success")
        case .failure(let error):
            #expect(error is ValidationError)
        }
    }
}
```

### Dependency Injection Pattern

**Protocol-based DI is the standard for testable Swift code:**

```swift
// Production protocol
protocol UserRepositoryProtocol {
    func login(email: String, password: String) async -> Result<User, Error>
    func fetchUser(_ userId: String) async -> Result<User, Error>
}

// Production implementation
class UserRepository: UserRepositoryProtocol {
    private let apiClient: APIClient
    private let database: Database

    init(apiClient: APIClient, database: Database) {
        self.apiClient = apiClient
        self.database = database
    }

    func login(email: String, password: String) async -> Result<User, Error> {
        // Real implementation
    }

    func fetchUser(_ userId: String) async -> Result<User, Error> {
        // Real implementation
    }
}

// Test double
final class MockUserRepository: UserRepositoryProtocol {
    var mockedLoginResult: Result<User, Error>?
    var mockedFetchUserResult: Result<User, Error>?
    var loginCallCount = 0
    var lastLoginEmail: String?

    func login(email: String, password: String) async -> Result<User, Error> {
        loginCallCount += 1
        lastLoginEmail = email
        return mockedLoginResult!
    }

    func fetchUser(_ userId: String) async -> Result<User, Error> {
        return mockedFetchUserResult!
    }
}
```

### Async/Await Testing

```swift
@MainActor
final class ViewModelAsyncTests: XCTestCase {

    var repository: MockUserRepository!
    var viewModel: UserViewModel!

    override func setUp() {
        repository = MockUserRepository()
        viewModel = UserViewModel(repository: repository)
    }

    func test_loadUser_emitsLoadingThenSuccess() async {
        // Given
        let user = User(id: "1", name: "Alice", email: "alice@example.com")
        repository.mockedFetchUserResult = .success(user)

        // When
        let expectation = expectation(description: "State changes")
        expectation.expectedFulfillmentCount = 2

        var states: [UserViewState] = []
        viewModel.$viewState.sink { state in
            states.append(state)
            expectation.fulfill()
        }.store(in: &cancellables)

        viewModel.loadUser("1")

        // Then
        await fulfillment(of: [expectation], timeout: 1.0)

        XCTAssertTrue(states[0] is UserViewState.Loading)
        if case .success(let loadedUser) = states[1] {
            XCTAssertEqual(loadedUser.name, "Alice")
        } else {
            XCTFail("Expected success state")
        }
    }

    func test_loadUser_emitsErrorOnFailure() async {
        // Given
        repository.mockedFetchUserResult = .failure(
            NetworkError.connectionTimeout
        )

        let expectation = expectation(description: "Error state emitted")
        var emittedError: UserViewState?

        viewModel.$viewState.dropFirst().sink { state in
            emittedError = state
            expectation.fulfill()
        }.store(in: &cancellables)

        // When
        viewModel.loadUser("1")

        // Then
        await fulfillment(of: [expectation], timeout: 1.0)

        if case .error(let message) = emittedError {
            XCTAssertFalse(message.isEmpty)
        } else {
            XCTFail("Expected error state")
        }
    }
}
```

---
