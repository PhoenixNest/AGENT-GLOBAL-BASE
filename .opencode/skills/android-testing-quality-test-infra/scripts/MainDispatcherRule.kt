// Main dispatcher override rule
class MainDispatcherRule(
    private val testDispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {
    override fun starting(description: Description) {
        Dispatchers.setMain(testDispatcher)
    }

    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}

// Usage in ViewModel tests
class UserListViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private val repository = FakeUserRepository()
    private lateinit var viewModel: UserListViewModel

    @Before
    fun setup() {
        viewModel = UserListViewModel(
            getUsersUseCase = GetUsersUseCase(repository),
            deleteUserUseCase = mockk(relaxed = true)
        )
    }

    @Test
    fun `when users loaded, state emits user list`() = runTest {
        repository.users = listOf(
            UserFixtures.validUser(id = "1", name = "Alice"),
            UserFixtures.validUser(id = "2", name = "Bob")
        )

        viewModel.sendIntent(UserListIntent.LoadUsers)

        val state = viewModel.uiState.first { it.users.isNotEmpty() }
        assertEquals(2, state.users.size)
    }
}

// Fake repository for testing
class FakeUserRepository : UserRepository {
    var users: List<User> = emptyList()
    var shouldFail: Boolean = false
    var failureException: Exception = NetworkException()

    override fun observeUser(userId: String): Flow<User> = flow {
        users.find { it.id == userId }?.let { emit(it) }
    }

    override suspend fun getUser(id: String): Result<User> {
        if (shouldFail) return Result.failure(failureException)
        return users.find { it.id == id }
            ?.let { Result.success(it) }
            ?: Result.failure(UserNotFoundException(id))
    }

    override suspend fun updateUser(user: User): Result<Unit> {
        if (shouldFail) return Result.failure(failureException)
        users = users.map { if (it.id == user.id) user else it }
        return Result.success(Unit)
    }
}