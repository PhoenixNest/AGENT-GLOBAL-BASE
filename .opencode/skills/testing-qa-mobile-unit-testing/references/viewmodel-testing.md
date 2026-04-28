# ViewModel Testing

## ViewModel Testing

ViewModel testing is a critical pattern in MVVM architecture. The ViewModel translates user actions into state changes and exposes them via StateFlow/Combine.

### Android ViewModel Testing

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {

    @get:Rule
    val mainDispatcherRule = StandardTestDispatcherRule()

    private val userRepository = mockk<UserRepository>()
    private lateinit var viewModel: UserViewModel

    @BeforeEach
    fun setUp() {
        viewModel = UserViewModel(userRepository)
    }

    @Test
    fun `initial state is loading`() = runTest {
        // No API call yet — state should be initial
        viewModel.uiState.value.shouldBeInstanceOf<UiState.Initial>()
    }

    @Test
    fun `loadUser emits loading then success`() = runTest {
        // Given
        val user = User("1", "Alice", "alice@example.com")
        coEvery { userRepository.fetchUser("1") } returns Result.Success(user)

        // When
        viewModel.loadUser("1")

        // Then — collect flow
        val states = mutableListOf<UiState>()
        val job = launch {
            viewModel.uiState.toList(states)
        }

        advanceUntilIdle()
        job.cancel()

        states shouldHaveSize 2
        states[0].shouldBeInstanceOf<UiState.Loading>()
        (states[1] as UiState.Success).user shouldBe user
    }

    @Test
    fun `loadUser emits loading then error on failure`() = runTest {
        // Given
        coEvery { userRepository.fetchUser("1") } returns
            Result.Error(NetworkException("No connection"))

        // When
        viewModel.loadUser("1")

        // Then
        val states = mutableListOf<UiState>()
        val job = launch {
            viewModel.uiState.toList(states)
        }

        advanceUntilIdle()
        job.cancel()

        states shouldHaveSize 2
        states[0].shouldBeInstanceOf<UiState.Loading>()
        (states[1] as UiState.Error).message shouldBe "No connection"
    }

    @Test
    fun `refreshUser does not emit loading when data exists`() = runTest {
        // Given — user already loaded
        val user = User("1", "Alice", "alice@example.com")
        coEvery { userRepository.fetchUser("1") } returns Result.Success(user)
        viewModel.loadUser("1")
        advanceUntilIdle()

        // Mock refresh result
        val refreshedUser = user.copy(name = "Alice Updated")
        coEvery { userRepository.fetchUser("1") } returns Result.Success(refreshedUser)

        // When
        viewModel.refreshUser()

        // Then — should NOT go through loading state on refresh
        val states = mutableListOf<UiState>()
        val job = launch {
            viewModel.uiState.toList(states)
        }

        advanceUntilIdle()
        job.cancel()

        // First state is the existing success, then refresh success
        states.last().shouldBeInstanceOf<UiState.Success>()
        (states.last() as UiState.Success).user.name shouldBe "Alice Updated"
    }
}
```

### iOS ViewModel Testing

```swift
@MainActor
final class UserViewModelTests: XCTestCase {

    var repository: MockUserRepository!
    var viewModel: UserViewModel!
    var cancellables = Set<AnyCancellable>()

    override func setUp() {
        repository = MockUserRepository()
        viewModel = UserViewModel(repository: repository)
    }

    func test_initialStateIsIdle() {
        XCTAssertTrue(viewModel.viewState is UserViewState.Idle)
    }

    func test_loadUser_emitsLoadingThenSuccess() async {
        // Given
        let user = User(id: "1", name: "Alice", email: "alice@example.com")
        repository.mockedFetchUserResult = .success(user)

        // Collect states
        let expectation = XCTestExpectation(description: "States emitted")
        expectation.expectedFulfillmentCount = 2

        var states: [UserViewState] = []
        viewModel.$viewState.sink { state in
            states.append(state)
            expectation.fulfill()
        }.store(in: &cancellables)

        // When
        viewModel.loadUser("1")

        // Then
        await fulfillment(of: [expectation], timeout: 1.0)

        XCTAssertTrue(states[0] is UserViewState.Loading)
        if case .success(let loadedUser) = states[1] {
            XCTAssertEqual(loadedUser.name, "Alice")
        }
    }

    func test_loadUser_deduplicatesConcurrentCalls() async {
        // Given
        repository.mockedFetchUserResult = .success(
            User(id: "1", name: "Alice", email: "alice@example.com")
        )

        // When — fire 3 concurrent loads
        async let result1 = viewModel.loadUser("1")
        async let result2 = viewModel.loadUser("1")
        async let result3 = viewModel.loadUser("1")

        _ = await (result1, result2, result3)

        // Then — only 1 API call should be made
        XCTAssertEqual(repository.fetchUserCallCount, 1)
    }
}
```

---
