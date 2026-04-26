class GetUserProfileUseCaseTest {

    private val userRepository = mockk<UserRepository>()
    private val profileMapper = mockk<ProfileMapper>()
    private val testDispatcher = UnconfinedTestDispatcher()
    private lateinit var useCase: GetUserProfileUseCase

    @Before
    fun setup() {
        useCase = GetUserProfileUseCase(userRepository, profileMapper, testDispatcher)
    }

    @Test
    fun `given user exists, when execute, then returns mapped profile`() = runTest(testDispatcher) {
        // Given
        val user = UserFactory.create(id = "user-123", name = "John Doe")
        val profile = ProfileFactory.createFromUser(user)

        every { userRepository.getUser("user-123") } returns Result.success(user)
        every { profileMapper.toProfile(user) } returns profile

        // When
        val result = useCase.execute("user-123")

        // Then
        assertTrue(result.isSuccess)
        assertEquals(profile, result.getOrNull())

        coVerify(exactly = 1) { userRepository.getUser("user-123") }
        verify(exactly = 1) { profileMapper.toProfile(user) }
    }

    @Test
    fun `given network error, when execute, then returns network error`() = runTest(testDispatcher) {
        // Given
        every { userRepository.getUser(any()) } returns Result.failure(NetworkException())

        // When
        val result = useCase.execute("user-123")

        // Then
        assertTrue(result.isFailure)
        assertIs<NetworkException>(result.exceptionOrNull())
    }

    @Test
    fun `given null user id, when execute, then throws invalid argument`() = runTest(testDispatcher) {
        // When/Then
        assertFailsWith<IllegalArgumentException> {
            useCase.execute("")
        }
    }
}