---
name: android-language-core-implementation
description: End-to-end Android app implementation guide — Kotlin, Jetpack Compose UI, MVVM + Clean Architecture, Hilt DI, Kotlin Coroutines + Flow, Navigation Compose, Room, Retrofit, DataStore, and Google Play submission checklist. Owned by Kofi Asante-Mensah (Android Lead). Use during Stage 5 (Development) for Android feature implementation and Stage 10 (Release Readiness) for Play Store submission. Trigger: android implementation, jetpack compose, MVVM, Hilt, coroutines, navigation compose, room, retrofit, datastore, google play submission.
prerequisites:
  - android-overview

version: "1.0.0"
---

# Android Implementation

## Purpose

Implement production-grade Android applications from the UML Engineering Package, IDS, and Coding Implementation Plan. All code must be written in Kotlin, follow the established architecture pattern, and be ready for Stage 6 Code Review without known compilation or runtime bugs.

## Technology Stack

| Layer         | Technology                       | Version Policy                      |
| ------------- | -------------------------------- | ----------------------------------- |
| Language      | Kotlin                           | Latest stable                       |
| UI            | Jetpack Compose                  | Latest stable                       |
| Architecture  | MVVM + Clean Architecture        | See patterns below                  |
| DI            | Hilt                             | Latest stable                       |
| Async         | Kotlin Coroutines + Flow         | Latest stable                       |
| Navigation    | Navigation Compose               | Latest stable                       |
| Database      | Room                             | Latest stable                       |
| Network       | Retrofit + OkHttp                | Latest stable                       |
| Serialisation | kotlinx.serialization            | Prefer over Gson                    |
| Image loading | Coil (Compose-native)            | Latest stable                       |
| Preferences   | DataStore (Preferences or Proto) | Not SharedPreferences               |
| Build         | Gradle + KSP                     | Convention plugins for multi-module |

_Note: Specific versions are locked in the Technology Selection Document (TSD) produced at Stage 3. The TSD governs — this skill provides patterns, not version overrides._

## Architecture Patterns

### ViewModel + UiState

Every screen has exactly one ViewModel. UI state is exposed as a single sealed class:

```kotlin
data class HomeUiState(
    val isLoading: Boolean = false,
    val items: List<Item> = emptyList(),
    val error: String? = null
)

class HomeViewModel @Inject constructor(
    private val getItemsUseCase: GetItemsUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        loadItems()
    }

    private fun loadItems() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            getItemsUseCase()
                .onSuccess { items ->
                    _uiState.update { it.copy(isLoading = false, items = items) }
                }
                .onFailure { e ->
                    _uiState.update { it.copy(isLoading = false, error = e.message) }
                }
        }
    }
}
```

### Compose Screen Structure

```kotlin
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = hiltViewModel(),
    onNavigateToDetail: (String) -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    HomeContent(
        uiState = uiState,
        onItemClick = onNavigateToDetail
    )
}

// Separate stateless content composable — testable without ViewModel
@Composable
private fun HomeContent(
    uiState: HomeUiState,
    onItemClick: (String) -> Unit
) {
    // UI implementation
}
```

**Rules:**

- Never hoist state above what the composable needs
- Always use `collectAsStateWithLifecycle()`, not `collectAsState()`
- Preview annotations on all content composables
- No business logic in composable functions

### Repository Pattern

```kotlin
interface ItemRepository {
    suspend fun getItems(): Result<List<Item>>
    fun observeItems(): Flow<List<Item>>
}

class ItemRepositoryImpl @Inject constructor(
    private val remoteSource: ItemRemoteDataSource,
    private val localSource: ItemLocalDataSource
) : ItemRepository {
    // Implementation: local-first with remote sync
}
```

## Android-Specific Requirements

### Security

- Sensitive data: use Android Keystore for encryption keys; `EncryptedSharedPreferences` for key-value; Room with SQLCipher for encrypted databases
- Network: enforce HTTPS via network security config; implement certificate pinning per SRD requirements
- SafetyNet/Play Integrity: implement per SRD if the product requires attestation
- Never log sensitive data (PII, tokens, payment details)

### Localization

- All user-visible strings via `stringResource(R.string.key)` — zero hardcoded strings
- Plurals via `pluralStringResource(R.plurals.key, count, count)`
- Support RTL layouts: use `start`/`end` not `left`/`right` in all layout parameters

### Accessibility

- All interactive composables: `Modifier.semantics { contentDescription = "..." }`
- Touch targets: minimum 48dp × 48dp
- Test with TalkBack enabled before Stage 6

### Performance

- Minimize recomposition: use `key()` in lazy lists, stable data classes with `@Stable`
- Profile with Android Studio's Compose Compiler Metrics before Stage 6
- Use `LazyColumn`/`LazyRow` for all lists — never `Column` with `forEach`

## Google Play Submission Checklist

Before Stage 10 Release Readiness:

- [ ] `targetSdkVersion` is current year's Android release or latest stable
- [ ] App passes Play integrity check
- [ ] Privacy policy URL configured in Play Console
- [ ] All required permissions declared with rationale in Play Store listing
- [ ] APK/AAB signed with upload key (keystore documented separately)
- [ ] App Bundle (AAB) format — not APK — for Play submission
- [ ] 64-bit support confirmed (no 32-bit-only native libraries)
- [ ] App reviewed in Play Console pre-launch report

## Code Review Standards

Before submitting for Stage 6, verify:

- [ ] All features in the Coding Implementation Plan are implemented
- [ ] App compiles without warnings (treat warnings as errors: `allWarningsAsErrors = true`)
- [ ] App runs on minimum supported SDK (as specified in TSD)
- [ ] App runs on latest Android release
- [ ] No known crashes in debug or release builds
- [ ] All strings localized (zero hardcoded strings)
- [ ] All sensitive operations use Android Keystore
- [ ] Compose previews render correctly for all content composables
