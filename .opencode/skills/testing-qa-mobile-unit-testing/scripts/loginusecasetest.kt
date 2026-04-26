// shared/src/commonTest/kotlin/com/company/app/LoginUseCaseTest.kt
// Runs on JVM via JUnit 5

class LoginUseCaseTest {
    private val repository = FakeUserRepository()
    private val loginUseCase = LoginUseCase(repository)

    @Test
    fun `login with valid credentials returns success`() = runTest {
        val result = loginUseCase.execute("alice@example.com", "password")
        assertTrue(result.isSuccess)
        assertEquals("Alice", result.getOrNull()?.name)
    }

    @Test
    fun `login with invalid email returns error`() = runTest {
        val result = loginUseCase.execute("", "password")
        assertTrue(result.isError)
    }
}

// Fake implementation in commonTest
class FakeUserRepository : UserRepository {
    var shouldSucceed = true
    var loginCallCount = 0

    override suspend fun login(email: String, password: String): Result<User> {
        loginCallCount++
        return if (shouldSucceed) {
            Result.Success(User("1", "Alice", email))
        } else {
            Result.Error(AuthenticationException("Invalid credentials"))
        }
    }
}