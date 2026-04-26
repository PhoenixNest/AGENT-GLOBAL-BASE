# Test Doubles

## Test Doubles

### Types of Test Doubles

| Type      | Purpose                             | When to Use                                                   |
| --------- | ----------------------------------- | ------------------------------------------------------------- |
| **Stub**  | Returns canned responses            | When you need to control input to the SUT                     |
| **Mock**  | Records and verifies interactions   | When you need to verify the SUT called dependencies correctly |
| **Fake**  | Working implementation (simplified) | When you need real behavior without external systems          |
| **Spy**   | Wraps real object, records calls    | When you need partial mocking                                 |
| **Dummy** | Placeholder, never used             | When API requires a parameter you don't care about            |

### Test Double Implementation

```kotlin
// Stub — Returns canned data
class StubUserService : UserService {
    override suspend fun getUser(id: String): User = User(id, "Stub User")
    override suspend fun login(email: String, password: String): AuthToken = "stub-token"
}

// Mock — Records calls and returns configurable responses (MockK)
val mockUserService = mockk<UserService> {
    coEvery { getUser("1") } returns User("1", "Mock User")
    coEvery { login(any(), any()) } returns "mock-token"
}

// Fake — Simplified working implementation
class FakeUserService : UserService {
    private val users = mutableMapOf<String, User>()
    var loginAttempts = 0

    override suspend fun getUser(id: String): User {
        return users[id] ?: throw UserNotFoundException(id)
    }

    override suspend fun login(email: String, password: String): AuthToken {
        loginAttempts++
        if (password == "correct-password") return "valid-token"
        throw AuthenticationException("Invalid credentials")
    }

    fun addUser(user: User) { users[user.id] = user }
}
```

---
