---
name: ios-testing-quality-ios-testing
description: "Ios skill: Ios Testing"
---

# iOS Testing

**Category:** Mobile Engineering — iOS Testing
**Owner:** iOS Engineer (Arjun Mehta)

## Overview

This skill establishes comprehensive iOS testing practices covering XCTest framework, XCUITest for UI automation, snapshot testing for visual regression, mocking strategies, and test parallelization. It is foundational to Stage 7 (Automated Testing) where the 100% automated test pass rate target is enforced, and Stage 6 (Code Review) where test coverage and quality are evaluated.

## Competency Dimensions

| Dimension            | Description                                                                                                  | Proficiency Indicators                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| XCTest Framework     | Test lifecycle, async/await test support, expectations, performance testing, test suites                     | All test types covered (unit, integration, performance); async tests use native async/await; performance tests have baselines |
| XCUITest             | UI element queries, interaction recording, accessibility-based queries, launch arguments, screenshot capture | UI tests use accessibility identifiers; launch arguments configure test environment; screenshots captured on failure          |
| Snapshot Testing     | Image comparison, tolerance configuration, device-specific snapshots, dark mode snapshots, CI integration    | Snapshot tests catch visual regressions; tolerance set appropriately per device; dark/light mode snapshots maintained         |
| Mocking              | Protocol-based mocks, mock generators, stub responses, call verification, async mock support                 | All dependencies mockable via protocol; mock behavior configurable per test; call verification for side effects               |
| Test Parallelization | Test plan parallelization, device sharding, test prioritization, flaky test isolation, CI integration        | Tests run in parallel on CI; flaky tests quarantined; test execution time <30 minutes for full suite                          |

## Execution Guidance

### XCTest — Unit Testing Patterns

**Async/await test support:**

```swift
import XCTest
@testable import App

@MainActor
final class UserViewModelTests: XCTestCase {

    private var viewModel: UserViewModel!
    private var mockRepository: MockUserRepository!

    override func setUp() async throws {
        try await super.setUp()
        mockRepository = MockUserRepository()
        viewModel = UserViewModel(userRepository: mockRepository)
    }

    override func tearDown() async throws {
        viewModel = nil
        mockRepository = nil
        try await super.tearDown()
    }

    // MARK: - Async Tests

    func test_loadUser_success() async {
        // Given
        let expectedUser = User(
            id: UUID(),
            name: "John Doe",
            email: "john@example.com"
        )
        mockRepository.user = expectedUser

        // When
        await viewModel.loadUser()

        // Then
        XCTAssertEqual(viewModel.state, .loaded(expectedUser))
        XCTAssertFalse(viewModel.isLoading)
    }

    func test_loadUser_failure() async {
        // Given
        mockRepository.shouldFail = true

        // When
        await viewModel.loadUser()

        // Then
        if case .error(let message) = viewModel.state {
            XCTAssertNotNil(message)
        } else {
            XCTFail("Expected error state")
        }
    }

    // MARK: - Expectation-based Tests (for completion handlers)

    func test_fetchWithCompletion() {
        // Given
        let expectation = expectation(description: "User fetched")
        var result: Result<User, Error>?

        // When
        mockRepository.fetchUser { fetchResult in
            result = fetchResult
            expectation.fulfill()
        }

        // Then
        wait(for: [expectation], timeout: 5.0)
        XCTAssertNotNil(result)
    }

    // MARK: - Performance Tests

    func test_userParsing_performance() {
        let jsonData = generateLargeUserJSON(count: 10000)

        measure(metrics: [CPUTimeMetric()]) {
            let users = try? JSONDecoder().decode([User].self, from: jsonData)
            XCTAssertNotNil(users)
        }
    }

    // MARK: - Testing Published Properties

    func test_publishedStateChanges() async {
        // Given
        mockRepository.user = User(id: UUID(), name: "Test", email: "test@example.com")

        // Create expectation for state change
        let expectation = XCTestExpectation(description: "State changed to loaded")

        // When
        let cancellable = viewModel.$state
            .dropFirst()  // Skip initial state
            .sink { state in
                if case .loaded = state {
                    expectation.fulfill()
                }
            }

        await viewModel.loadUser()

        // Then
        await fulfillment(of: [expectation], timeout: 1.0)
        cancellable.cancel()
    }

    // MARK: - Helper Methods

    private func generateLargeUserJSON(count: Int) -> Data {
        let users = (0..<count).map { i in
            ["id": UUID().uuidString, "name": "User \(i)", "email": "user\(i)@test.com"]
        }
        return try! JSONSerialization.data(withJSONObject: users)
    }
}
```

### XCUITest — UI Automation

```swift
import XCTest

final class UserListUITests: XCTestCase {

    var app: XCUIApplication!

    override func setUpWithError() throws {
        try super.setUpWithError()
        continueAfterFailure = false  // Fail fast on UI tests

        app = XCUIApplication()

        // Configure test environment via launch arguments
        app.launchArguments = [
            "--ui-testing",
            "--mock-server-url", "http://localhost:8080",
            "--skip-onboarding"
        ]
        app.launchEnvironment["UI_TESTING"] = "1"

        app.launch()
    }

    override func tearDownWithError() throws {
        app = nil
        try super.tearDownWithError()
    }

    // MARK: - Test Cases

    func test_userList_displaysUsers() {
        // Wait for user list to load
        let userCell = app.cells["user-cell-0"]
        XCTAssertTrue(userCell.waitForExistence(timeout: 10))

        // Verify user data displayed
        let nameLabel = app.staticTexts["user-name-0"]
        XCTAssertTrue(nameLabel.exists)
    }

    func test_userList_pullToRefresh() {
        let userCell = app.cells["user-cell-0"]
        XCTAssertTrue(userCell.waitForExistence(timeout: 10))

        // Pull to refresh
        let firstCell = app.cells.firstMatch
        firstCell.swipeDown()

        // Wait for refresh to complete
        let refreshIndicator = app.progressIndicators.firstMatch
        XCTAssertTrue(refreshIndicator.waitForExistence(timeout: 5))
        XCTAssertTrue(waitForElementToDisappear(refreshIndicator, timeout: 10))
    }

    func test_userDetail_navigateAndBack() {
        let userCell = app.cells["user-cell-0"]
        XCTAssertTrue(userCell.waitForExistence(timeout: 10))

        // Tap user cell
        userCell.tap()

        // Verify detail screen
        let detailTitle = app.navigationBars["User Detail"]
        XCTAssertTrue(detailTitle.waitForExistence(timeout: 5))

        // Navigate back
        app.buttons["Back"].tap()

        // Verify back on list
        XCTAssertTrue(userCell.exists)
    }

    func test_userDelete_swipeAndDelete() {
        let userCell = app.cells["user-cell-0"]
        XCTAssertTrue(userCell.waitForExistence(timeout: 10))

        // Swipe to delete
        userCell.swipeLeft()

        // Tap delete button
        let deleteButton = app.buttons["Delete"]
        XCTAssertTrue(deleteButton.waitForExistence(timeout: 2))
        deleteButton.tap()

        // Confirm deletion
        let confirmButton = app.alerts.buttons["Delete"]
        confirmButton.tap()

        // Verify cell removed
        XCTAssertFalse(userCell.waitForExistence(timeout: 5))
    }

    func test_errorState_displaysErrorMessage() {
        // Configure mock to return error
        app.launchEnvironment["MOCK_ERROR"] = "1"
        app.terminate()
        app.launch()

        let errorMessage = app.staticTexts["error-message"]
        XCTAssertTrue(errorMessage.waitForExistence(timeout: 10))
        XCTAssertEqual(errorMessage.label, "Network error. Please check your connection.")
    }

    // MARK: - Accessibility-Based Queries

    func test_accessibilityNavigation() {
        // Use accessibility identifiers instead of raw text
        let settingsButton = app.buttons["settings-button"]
        XCTAssertTrue(settingsButton.waitForExistence(timeout: 5))
        settingsButton.tap()

        let settingsScreen = app.navigationBars["Settings"]
        XCTAssertTrue(settingsScreen.exists)
    }

    // MARK: - Screenshot on Failure

    override func tearDownWithError() throws {
        if let testRun = testRun, testRun.hasFailed {
            let screenshot = app.screenshot()
            let attachment = XCTAttachment(screenshot: screenshot)
            attachment.lifetime = .keepAlways
            attachment.name = "\(name)-failure.png"
            add(attachment)
        }
        try super.tearDownWithError()
    }

    // MARK: - Helpers

    private func waitForElementToDisappear(_ element: XCUIElement, timeout: TimeInterval) -> Bool {
        let start = Date()
        while element.exists && Date().timeIntervalSince(start) < timeout {
            RunLoop.current.run(until: Date().addingTimeInterval(0.1))
        }
        return !element.exists
    }
}
```

### Snapshot Testing — Visual Regression

```swift
import XCTest
import SnapshotTesting
@testable import App

@MainActor
final class SnapshotTests: XCTestCase {

    // MARK: - View Controller Snapshots

    func test_userListViewController_defaultState() {
        let vc = UserListViewController(viewModel: makeViewModel(users: sampleUsers))

        assertSnapshot(
            of: vc,
            as: .image(on: .iPhone15),
            named: "userList-default"
        )
    }

    func test_userListViewController_loadingState() {
        let viewModel = makeViewModel(users: [])
        viewModel.isLoading = true

        let vc = UserListViewController(viewModel: viewModel)

        assertSnapshot(
            of: vc,
            as: .image(on: .iPhone15),
            named: "userList-loading"
        )
    }

    func test_userListViewController_errorState() {
        let viewModel = makeViewModel(users: [])
        viewModel.errorMessage = "Network error"

        let vc = UserListViewController(viewModel: viewModel)

        assertSnapshot(
            of: vc,
            as: .image(on: .iPhone15),
            named: "userList-error"
        )
    }

    // MARK: - Dark Mode Snapshots

    func test_userListViewController_darkMode() {
        let vc = UserListViewController(viewModel: makeViewModel(users: sampleUsers))

        // Override trait collection for dark mode
        vc.overrideUserInterfaceStyle = .dark

        assertSnapshot(
            of: vc,
            as: .image(on: .iPhone15),
            named: "userList-darkMode"
        )
    }

    // MARK: - SwiftUI View Snapshots

    func test_userCardView() {
        let user = User(id: UUID(), name: "John Doe", email: "john@example.com")
        let view = UserCardView(user: user)

        assertSnapshot(
            of: view,
            as: .image(layout: .sizeThatFits),
            named: "userCard"
        )
    }

    // MARK: - Multi-Device Snapshots

    func test_userListViewController_multiDevice() {
        let vc = UserListViewController(viewModel: makeViewModel(users: sampleUsers))

        let devices: [Snapshotting<UIViewController, UIImage>] = [
            .image(on: .iPhoneSe),
            .image(on: .iPhone15),
            .image(on: .iPhone15ProMax),
            .image(on: .iPadMini)
        ]

        for device in devices {
            assertSnapshot(
                of: vc,
                as: device,
                named: "userList-\(device.deviceDescription)"
            )
        }
    }

    // MARK: - Helpers

    private var sampleUsers: [User] {
        [
            User(id: UUID(), name: "Alice", email: "alice@example.com"),
            User(id: UUID(), name: "Bob", email: "bob@example.com"),
            User(id: UUID(), name: "Charlie", email: "charlie@example.com")
        ]
    }

    private func makeViewModel(users: [User]) -> UserListViewModel {
        let mockRepo = MockUserRepository()
        mockRepo.users = users
        return UserListViewModel(userRepository: mockRepo)
    }
}
```

### Mocking — Protocol-Based

```swift
// MARK: - Protocol Definition

protocol UserRepositoryProtocol: Sendable {
    func fetchUsers() async throws -> [User]
    func fetchUser(id: UUID) async throws -> User
    func createUser(_ user: CreateUserRequest) async throws -> User
    func deleteUser(id: UUID) async throws
}

// MARK: - Mock Implementation

final class MockUserRepository: UserRepositoryProtocol {

    // Configurable behavior
    var users: [User] = []
    var user: User?
    var shouldFail: Bool = false
    var error: Error = NetworkError.unavailable

    // Call tracking
    var fetchUsersCallCount = 0
    var fetchUserCallCount = 0
    var createUserCallCount = 0
    var deleteUserCallCount = 0
    var deleteUserReceivedId: UUID?

    func fetchUsers() async throws -> [User] {
        fetchUsersCallCount += 1
        if shouldFail { throw error }
        return users
    }

    func fetchUser(id: UUID) async throws -> User {
        fetchUserCallCount += 1
        if shouldFail { throw error }
        return user ?? users.first(where: { $0.id == id }) ?? User(id: id, name: "", email: "")
    }

    func createUser(_ request: CreateUserRequest) async throws -> User {
        createUserCallCount += 1
        if shouldFail { throw error }
        return User(id: UUID(), name: request.name, email: request.email)
    }

    func deleteUser(id: UUID) async throws {
        deleteUserCallCount += 1
        deleteUserReceivedId = id
        if shouldFail { throw error }
    }
}

// MARK: - Usage in Tests

@MainActor
final class UserListViewModelTests: XCTestCase {

    func test_deleteUser_callsRepository() async {
        // Given
        let userId = UUID()
        let mockRepo = MockUserRepository()
        let viewModel = UserListViewModel(userRepository: mockRepo)

        // When
        await viewModel.deleteUser(id: userId)

        // Then
        XCTAssertEqual(mockRepo.deleteUserCallCount, 1)
        XCTAssertEqual(mockRepo.deleteUserReceivedId, userId)
    }

    func test_fetchUsers_propagatesError() async {
        // Given
        let mockRepo = MockUserRepository()
        mockRepo.shouldFail = true
        let viewModel = UserListViewModel(userRepository: mockRepo)

        // When
        await viewModel.loadUsers()

        // Then
        if case .error = viewModel.state {
            // Success — error state reached
        } else {
            XCTFail("Expected error state")
        }
    }
}
```

### Test Parallelization

**Xcode Test Plans:**

1. Create a Test Plan: File → New → Test Plan
2. Add all test targets
3. Enable parallelization: Edit Scheme → Test → Options → Parallelize Testing
4. Set number of workers: Based on available cores (typically 4-8)

**CI parallelization via xcodebuild:**

```bash
# Run tests in parallel
xcodebuild test \
    -workspace App.xcworkspace \
    -scheme App \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    -parallel-testing-enabled YES \
    -parallel-testing-worker-count 4 \
    -only-testing:AppTests \
    -resultBundlePath TestResults.xcresult

# Run specific test class
xcodebuild test \
    -scheme App \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    -only-testing:AppTests/UserViewModelTests

# Skip flaky tests
xcodebuild test \
    -scheme App \
    -skip-testing:AppTests/FlakyTests
```

**Flaky test quarantine:**

```swift
// Mark known flaky tests
@available(*, deprecated, message: "Flaky — quarantined until fixed in JIRA-1234")
func test_networkTimeout_retry() async {
    // This test flakes due to timing variability
    // Fixed by using TestClock instead of real time
}

// Flaky test tracking spreadsheet
// | Test Name | Flake Rate | JIRA | Owner | Fix Target |
// |-----------|-----------|------|-------|------------|
// | test_networkTimeout_retry | 8% | JIRA-1234 | Arjun | Sprint 15 |
```

## Pipeline Integration

- **Stage 5 (Development):** TDD practiced during development. Unit tests and mock implementations built alongside production code.
- **Stage 6 (Code Review):** Test coverage reviewed: domain layer >80%, presentation >60%, data layer >70%. Test quality assessed.
- **Stage 7 (Automated Testing):** Primary stage for this skill. Full test suite execution: unit tests, UI tests, snapshot tests. Target: 100% pass rate.
- **Stage 8 (Integrity Verification):** Regression test suite executed on all fixed functionalities. Snapshot tests verify no visual regressions.

## Quality Standards

- **>80%** unit test coverage on domain layer
- **>60%** test coverage on presentation layer
- **>70%** test coverage on data layer
- **100%** of public ViewModel methods have unit tests
- **100%** of core user flows have XCUITest coverage
- Snapshot tests cover **all screen states** (loading, loaded, error, empty)
- Snapshot tests cover **light and dark mode**
- Snapshot tests cover **all supported device sizes**
- **Zero** flaky tests in CI — flaky tests quarantined with JIRA tracking
- All XCUITests use **accessibility identifiers** — not raw text queries
- Screenshot captured and attached on **every UI test failure**
- Full test suite completes in **<30 minutes** on CI with parallelization
- Performance tests have **established baselines** — regression flagged automatically
