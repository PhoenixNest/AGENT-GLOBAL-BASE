// UNSTABLE — causes unnecessary recompositions
data class User(var name: String, var age: Int)  // mutable var = unstable

// STABLE — safe for composition caching
data class User(val name: String, val age: Int)  // immutable val = stable

// EXPLICITLY STABLE — for classes Compose can't infer
@Stable
interface UiState {
    val isLoading: Boolean
    val users: List<UserDisplayModel>
}

// IMMUTABLE — no mutable properties at all
@Immutable
data class AppConfig(
    val apiBaseUrl: String,
    val featureFlags: Map<String, Boolean>
)