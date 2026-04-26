# Repository Testing

## Repository Testing

Repository tests verify that the data layer correctly coordinates between data sources (API, database, cache).

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserRepositoryTest {

    @get:Rule
    val mainDispatcherRule = StandardTestDispatcherRule()

    private val apiService = mockk<ApiService>()
    private val database = mockk<AppDatabase>()
    private val userDao = mockk<UserDao>()
    private lateinit var repository: UserRepository

    @BeforeEach
    fun setUp() {
        every { database.userDao() } returns userDao
        repository = UserRepository(apiService, database)
    }

    @Test
    fun `fetchUser returns cached user when available`() = runTest {
        // Given
        val cachedUser = User("1", "Alice (cached)")
        coEvery { userDao.getUserById("1") } returns cachedUser

        // When
        val result = repository.fetchUser("1")

        // Then
        (result as Result.Success).data.name shouldBe "Alice (cached)"
        coVerify(exactly = 0) { apiService.getUser(any()) } // No API call for cached data
    }

    @Test
    fun `fetchUser calls API when no cache and updates database`() = runTest {
        // Given
        coEvery { userDao.getUserById("1") } returns null
        val apiUser = UserResponse("1", "Alice (API)", "alice@example.com")
        coEvery { apiService.getUser("1") } returns apiUser
        coEvery { userDao.insertUser(any()) } returns Unit

        // When
        val result = repository.fetchUser("1")

        // Then
        (result as Result.Success).data.name shouldBe "Alice (API)"
        coVerify { apiService.getUser("1") }
        coVerify { userDao.insertUser(match { it.id == "1" }) }
    }

    @Test
    fun `fetchUser returns error when API fails and no cache`() = runTest {
        // Given
        coEvery { userDao.getUserById("1") } returns null
        coEvery { apiService.getUser("1") } throws
            java.net.SocketTimeoutException("Timeout")

        // When
        val result = repository.fetchUser("1")

        // Then
        result.shouldBeInstanceOf<Result.Error>()
    }
}
```

---
