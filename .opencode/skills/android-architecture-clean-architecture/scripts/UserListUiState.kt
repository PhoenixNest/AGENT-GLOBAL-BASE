// 1. Define immutable UI state
data class UserListUiState(
    val users: List<UserDisplayModel> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val refreshTrigger: Int = 0  // Increment to trigger pull-to-refresh
)

// 2. Define user intents
sealed interface UserListIntent {
    object LoadUsers : UserListIntent
    object Refresh : UserListIntent
    data class DeleteUser(val id: String) : UserListIntent
    data class SearchQueryChanged(val query: String) : UserListIntent
}

// 3. ViewModel with StateReducer pattern
class UserListViewModel(
    private val getUsersUseCase: GetUsersUseCase,
    private val deleteUserUseCase: DeleteUserUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(UserListUiState())
    val uiState: StateFlow<UserListUiState> = _uiState.asStateFlow()

    // Intent channel — single producer, ordered processing
    private val _intents = MutableSharedFlow<UserListIntent>(
        extraBufferCapacity = 1,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )

    init {
        viewModelScope.launch {
            _intents
                .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), UserListIntent.LoadUsers)
                .collect { intent -> reduceState(intent) }
        }
    }

    fun sendIntent(intent: UserListIntent) {
        viewModelScope.launch { _intents.emit(intent) }
    }

    private suspend fun reduceState(intent: UserListIntent) {
        _uiState.update { currentState ->
            when (intent) {
                is UserListIntent.LoadUsers -> loadUsers(currentState)
                is UserListIntent.Refresh -> currentState.copy(refreshTrigger = currentState.refreshTrigger + 1, isLoading = true)
                is UserListIntent.DeleteUser -> deleteUser(currentState, intent.id)
                is UserListIntent.SearchQueryChanged -> applyFilter(currentState, intent.query)
            }
        }
    }

    private suspend fun loadUsers(current: UserListUiState): UserListUiState {
        return try {
            val users = getUsersUseCase()
            current.copy(users = users.toDisplayModels(), isLoading = false, error = null)
        } catch (e: Exception) {
            current.copy(isLoading = false, error = e.userReadableMessage())
        }
    }
}