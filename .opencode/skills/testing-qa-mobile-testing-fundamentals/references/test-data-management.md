# Test Data Management

## Test Data Management

### Principles

| Principle          | Description                                    |
| ------------------ | ---------------------------------------------- |
| **Deterministic**  | Same test data produces same results every run |
| **Isolated**       | Tests don't share or mutate shared state       |
| **Self-contained** | Tests create and clean up their own data       |
| **Representative** | Test data reflects production scenarios        |

### Strategies

**1. Factory Methods (Recommended for Unit Tests):**

```kotlin
// Kotlin — Test Data Factory
object UserTestDataFactory {
    fun validUser(
        id: String = "user-123",
        name: String = "Alice Johnson",
        email: String = "alice@example.com"
    ): User = User(id = id, name = name, email = email)

    fun userWithLongName() = validUser(
        name = "Christopher Alexander Montgomery-Smythe III",
        email = "long.name@example.com"
    )

    fun userWithSpecialCharacters() = validUser(
        name = "José García-O'Brien",
        email = "jose@example.com"
    )

    fun minimalUser() = validUser(
        name = "A",
        email = "a@b.co"
    )
}
```

```swift
// Swift — Test Data Factory
enum UserTestDataFactory {
    static func validUser(
        id: String = "user-123",
        name: String = "Alice Johnson",
        email: String = "alice@example.com"
    ) -> User {
        User(id: id, name: name, email: email)
    }

    static func userWithLongName() -> User {
        validUser(name: "Christopher Alexander Montgomery-Smythe III")
    }

    static func userWithSpecialCharacters() -> User {
        validUser(name: "José García-O'Brien")
    }

    static func minimalUser() -> User {
        validUser(name: "A", email: "a@b.co")
    }
}
```

**2. Fixture Files (Recommended for Integration/E2E):**

```json
// tests/fixtures/user-response.json
{
  "id": "user-123",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "avatar_url": "https://example.com/avatar.jpg",
  "created_at": "2024-01-15T10:30:00Z"
}
```

```kotlin
// Loading fixtures in Kotlin tests
inline fun <reified T> loadFixture(fileName: String): T {
    val json = javaClass.classLoader!!
        .getResource("fixtures/$fileName")!!
        .readText()
    return Json.decodeFromString(json)
}

@Test
fun `parse user response from API`() {
    val response: UserResponse = loadFixture("user-response.json")
    val user = response.toDomainModel()
    assertThat(user.name).isEqualTo("Alice Johnson")
}
```

**3. Mock Servers (Recommended for API Integration):**

```kotlin
// Kotlin — MockWebServer for API testing
@OptIn(ExperimentalCoroutinesApi::class)
class ApiServiceTest {
    private val mockServer = MockWebServer()
    private lateinit var apiService: ApiService

    @BeforeEach
    fun setup() {
        apiService = Retrofit.Builder()
            .baseUrl(mockServer.url("/"))
            .addConverterFactory(MoshiConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }

    @AfterEach
    fun teardown() {
        mockServer.shutdown()
    }

    @Test
    fun `fetchUser returns parsed user`() = runTest {
        val jsonResponse = loadJsonResource("user-response.json")
        mockServer.enqueue(
            MockResponse()
                .setResponseCode(200)
                .setBody(jsonResponse)
        )

        val user = apiService.fetchUser("user-123")

        assertThat(user.name).isEqualTo("Alice Johnson")
        val request = mockServer.takeRequest()
        assertThat(request.path).isEqualTo("/api/users/user-123")
    }
}
```

### Sensitive Data Handling

**NEVER commit production data or credentials to test fixtures.**

| Rule                                             | Enforcement               |
| ------------------------------------------------ | ------------------------- |
| No real passwords, tokens, API keys in test code | Pre-commit hooks, CI lint |
| No production database dumps in fixtures         | Repository policy         |
| Use synthetic data generators for large datasets | Faker libraries           |
| Mask PII in test logs                            | Log sanitization          |

```kotlin
// Use Faker for synthetic test data
val faker = Faker()
val testUser = User(
    name = faker.name().fullName(),
    email = faker.internet().emailAddress(),
    phone = faker.phoneNumber().cellPhone()
)
```

---
