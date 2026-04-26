class UserListScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    private val fakeRepository = FakeUserRepository()

    @Test
    fun whenUsersLoaded_displaysUserList() {
        // Given
        fakeRepository.users = listOf(
            UserFactory.create(id = "1", name = "Alice"),
            UserFactory.create(id = "2", name = "Bob")
        )

        // When
        composeTestRule.setContent {
            AppTheme {
                UserListScreen(
                    viewModel = UserListViewModel(
                        getUsersUseCase = GetUsersUseCase(fakeRepository),
                        deleteUserUseCase = mockk(relaxed = true)
                    )
                )
            }
        }

        // Then
        composeTestRule.onNodeWithText("Alice").assertIsDisplayed()
        composeTestRule.onNodeWithText("Bob").assertIsDisplayed()
    }

    @Test
    fun whenDeleteUser_tapped_removeUserFromList() {
        // Given
        val deletedUserIds = mutableListOf<String>()
        val deleteUserUseCase = mockk<DeleteUserUseCase>(relaxed = true) {
            coEvery { execute(any()) } answers {
                deletedUserIds.add(firstArg())
                Result.success(Unit)
            }
        }

        composeTestRule.setContent {
            AppTheme {
                UserListScreen(
                    viewModel = UserListViewModel(
                        getUsersUseCase = GetUsersUseCase(FakeUserRepository(listOf(
                            UserFactory.create(id = "1", name = "Alice")
                        ))),
                        deleteUserUseCase = deleteUserUseCase
                    )
                )
            }
        }

        // When
        composeTestRule.onNodeWithContentDescription("Delete Alice").performClick()

        // Then
        composeTestRule.waitForIdle()
        assertEquals(listOf("1"), deletedUserIds)
    }

    @Test
    fun whenLoading_showsLoadingIndicator() {
        // Given: repository that never completes (simulates loading)
        val hangingRepository = FakeUserRepository(hangForever = true)

        composeTestRule.setContent {
            AppTheme {
                UserListScreen(
                    viewModel = UserListViewModel(
                        getUsersUseCase = GetUsersUseCase(hangingRepository),
                        deleteUserUseCase = mockk(relaxed = true)
                    )
                )
            }
        }

        // Then
        composeTestRule.onNodeWithTag("loading_indicator").assertIsDisplayed()
    }
}