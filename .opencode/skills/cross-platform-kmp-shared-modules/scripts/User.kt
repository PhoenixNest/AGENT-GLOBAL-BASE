// MARK: - Pure Kotlin Domain (commonMain)

// Domain entity — no platform dependencies
data class User(
    val id: String,
    val name: String,
    val email: String,
    val createdAt: Instant,
    val preferences: UserPreferences
)

data class UserPreferences(
    val theme: Theme,
    val notificationsEnabled: Boolean,
    val language: String
)

enum class Theme { LIGHT, DARK, SYSTEM }

// Repository interface — defined in domain
interface UserRepository {
    fun observeUser(id: String): Flow<User>
    suspend fun fetchUser(id: String): Result<User, ApiError>
    suspend fun updateUser(user: User): Result<Unit, ApiError>
}

// Use case — pure business logic
class GetUserProfileUseCase(
    private val userRepository: UserRepository
) {
    suspend operator fun invoke(userId: String): Result<User, DomainError> {
        if (userId.isBlank()) {
            return Result.Error(DomainError.InvalidArgument("User ID cannot be empty"))
        }

        return userRepository.fetchUser(userId).mapLeft { apiError ->
            when (apiError) {
                is ApiError.NotFound -> DomainError.UserNotFound(userId)
                is ApiError.Unauthorized -> DomainError.AuthenticationRequired
                is ApiError.NetworkError -> DomainError.NetworkUnavailable
                else -> DomainError.Unknown(apiError.message)
            }
        }
    }
}

// Result type — Arrow-style
sealed class Result<out T, out E> {
    data class Success<T>(val value: T) : Result<T, Nothing>()
    data class Error<E>(val error: E) : Result<Nothing, E>()

    fun <R> map(transform: (T) -> R): Result<R, E> = when (this) {
        is Success -> Success(transform(value))
        is Error -> Error(error)
    }

    fun <F> mapLeft(transform: (E) -> F): Result<T, F> = when (this) {
        is Success -> Success(value)
        is Error -> Error(transform(error))
    }
}