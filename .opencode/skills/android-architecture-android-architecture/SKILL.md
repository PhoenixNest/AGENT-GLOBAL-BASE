---
name: android-architecture-android-architecture
description: 'Android skill: Android Architecture'
---

# Android Architecture

**Category:** Mobile Engineering — Android
**Owner:** Senior Android Engineer (Tariq Al-Hassan)

## Overview

This skill defines production-grade Android application architecture patterns including MVVM, Clean Architecture, MVI, and state management with StateFlow. It governs the structural design of Android platform code during Stage 5 (Development), ensures alignment with ADRs established in Stage 3 (Architecture), and provides the architectural baseline against which code reviews (Stage 6) and integrity verification (Stage 8) are conducted.

## Competency Dimensions

| Dimension                    | Description                                                                                    | Proficiency Indicators                                                                                                                     |
| ---------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| MVVM Pattern                 | ViewModel-View separation, LiveData/StateFlow state emission, unidirectional data flow         | ViewModel contains zero Android framework references; state emission is always explicit and testable; View observes state reactively       |
| Clean Architecture           | Layer separation (data/domain/presentation), use case interactor pattern, dependency inversion | Domain layer has zero framework dependencies; data layer implements repository interfaces defined in domain; dependency graph flows inward |
| MVI Pattern                  | Intent-State-Render cycle, deterministic state transitions, state reduction                    | All UI events funnel through Intent channel; State is immutable data class; Render function is pure mapping from State → UI                |
| StateFlow & State Management | StateFlow as single source of truth, StateReducer pattern, side effect isolation               | State transitions are atomic and traceable; side effects (navigation, one-shot events) are separated from UI state                         |
| Android Platform Internals   | Activity/Fragment lifecycle, Process Death, SavedStateHandle, Configuration Changes            | App survives process death with full state restoration; ViewModel survives configuration changes; no state loss on screen rotation         |

## Execution Guidance

### Clean Architecture Layer Definitions

**Strict dependency rule:** Inner layers know nothing about outer layers. Dependencies flow inward through interface abstraction.

```
presentation/     ← Depends on: domain
├── ui/
│   ├── screen/       # Composable screens, ViewModels
│   ├── components/   # Reusable UI components
│   └── navigation/   # Navigation graph, route definitions
└── mapper/           # Domain → UI model mappers

domain/             ← Depends on: NOTHING (pure Kotlin)
├── model/            # Domain entities (data classes)
├── repository/       # Repository interfaces (contracts)
├── usecase/          # Use case interactors (single responsibility)
└── error/            # Domain error hierarchy (sealed interface)

data/               ← Depends on: domain (implements domain interfaces)
├── repository/       # Repository implementations
├── remote/           # API clients, DTOs, network mappers
├── local/            # Database entities, DAOs, Room
└── mapper/           # DTO ↔ Domain entity mappers
```

**Dependency injection binding:**

```kotlin
// Domain layer defines the contract
interface UserRepository {
    suspend fun getUser(id: String): Result<User, DomainError>
    suspend fun updateUser(user: User): Result<Unit, DomainError>
}

// Data layer implements the contract
class UserRepositoryImpl(
    private val api: UserApi,
    private val dao: UserDao,
    private val mapper: UserMapper
) : UserRepository {
    override suspend fun getUser(id: String): Result<User, DomainError> = ...
    override suspend fun updateUser(user: User): Result<Unit, DomainError> = ...
}

// DI module binds interface to implementation
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    abstract fun bindUserRepository(impl: UserRepositoryImpl): UserRepository
}
```

### MVVM with StateFlow — Production Pattern

**ViewModel state management with explicit StateReducer:**

```kotlin
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
```

**View layer (Compose) — pure reactive rendering:**

```kotlin
@Composable
fun UserListScreen(
    viewModel: UserListViewModel = hiltViewModel(),
    navigator: AppNavigator
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    // Pure render function — no side effects in composition
    UserListContent(
        state = uiState,
        onIntent = { viewModel.sendIntent(it) },
        onDeleteUser = { viewModel.sendIntent(UserListIntent.DeleteUser(it)) }
    )

    // Side effects collected in LaunchedEffect
    LaunchedEffect(uiState.error) {
        uiState.error?.let { /* Show snackbar */ }
    }
}
```

### MVI vs MVVM — Decision Criteria

| Criteria           | MVVM                                         | MVI                                                     |
| ------------------ | -------------------------------------------- | ------------------------------------------------------- |
| State complexity   | Moderate (2-3 state variables)               | High (complex state machines, >5 variables)             |
| Team experience    | Familiar to most Android devs                | Requires MVI/Redux background                           |
| State traceability | Implicit (multiple mutable sources possible) | Explicit (single state reduction function)              |
| Debugging          | Harder to trace state transitions            | Full state history via state reducer logging            |
| Testability        | Good (test ViewModel outputs)                | Excellent (test reducer as pure function)               |
| Recommended for    | Most screens, CRUD operations                | Complex forms, multi-step wizards, real-time dashboards |

**Company standard:** MVVM with StateFlow for 80% of screens. MVI for screens with complex state machines (payment flows, multi-step onboarding, real-time collaboration).

### Process Death & State Restoration

**Critical for Stage 8 Integrity Verification — app must survive process death without data loss:**

```kotlin
class CheckoutViewModel(
    private val savedStateHandle: SavedStateHandle,
    private val paymentUseCase: ProcessPaymentUseCase
) : ViewModel() {

    companion object {
        private const val KEY_CART = "cart_state"
        private const val KEY_STEP = "checkout_step"
    }

    // State automatically saved/restored on process death
    private var _checkoutState = MutableStateFlow(
        CheckoutState(
            cart = savedStateHandle[KEY_CART] ?: Cart.empty(),
            currentStep = savedStateHandle[KEY_STEP] ?: CheckoutStep.CART
        )
    )

    init {
        // Persist state changes to SavedStateHandle
        viewModelScope.launch {
            _checkoutState
                .onEach { state ->
                    savedStateHandle[KEY_CART] = state.cart
                    savedStateHandle[KEY_STEP] = state.currentStep
                }
                .collect()
        }
    }
}
```

### Architecture Decision Enforcement

**ADRs locked at Stage 3 are not revisable.** Current architectural mandates:

- **ADR-001:** Clean Architecture with three layers (presentation/domain/data) — no exceptions
- **ADR-002:** StateFlow as the reactive stream primitive — no LiveData in new code
- **ADR-003:** Hilt for dependency injection — no manual Dagger components
- **ADR-004:** Repository pattern as the single data access abstraction — no direct API/DB calls from ViewModel
- **ADR-005:** Sealed interfaces for error modeling — no exception-based error handling across layer boundaries

Any deviation requires a new ADR with CTO + CIO approval before implementation.

## Pipeline Integration

- **Stage 3 (Architecture):** Implements UML component diagrams and ADRs. This skill translates architectural decisions into concrete code structure.
- **Stage 4 (Implementation Plan):** Informs module decomposition, dependency graph, and task breakdown in the implementation plan and GANTT chart.
- **Stage 5 (Development):** Primary execution skill for Android platform code. All feature development follows these architectural patterns.
- **Stage 6 (Code Review):** Architecture conformance is the first review criterion. Layer violations, direct framework dependencies in domain, or bypassing the repository pattern are P0 defects.
- **Stage 8 (Integrity Verification):** Process death recovery, state restoration completeness, and architectural layer compliance are verified.

## Quality Standards

- **Zero** layer dependency violations (domain must not import from data or presentation)
- **Zero** direct API/database calls from ViewModel — all data access through repository
- **100%** UI state emitted through StateFlow — no direct View manipulation
- **100%** process death survival for user-facing state (validated via Don't Keep Activities + process kill)
- **100%** ViewModels injectable via Hilt — no manual instantiation
- **<100ms** state reduction latency (measured via tracing)
- All use cases follow single responsibility principle — one use case per file
- Domain entities are pure Kotlin data classes — zero Android framework imports
- Error types are sealed interfaces — no raw exceptions crossing layer boundaries
