// Domain error hierarchy
sealed interface NetworkError {
    data class ConnectionError(val message: String) : NetworkError
    data class TimeoutError(val message: String) : NetworkError
    data class ServerError(val code: Int, val message: String) : NetworkError
    data class ClientError(val code: Int, val message: String, val details: Map<String, String>? = null) : NetworkError
    data class AuthError(val message: String) : NetworkError
    object UnknownError : NetworkError
}

// Error mapper — converts HTTP responses to domain errors
object ErrorMapper {
    fun fromException(exception: Throwable): NetworkError {
        return when (exception) {
            is UnknownHostException -> NetworkError.ConnectionError("No internet connection")
            is SocketTimeoutException -> NetworkError.TimeoutError("Request timed out. Please try again.")
            is SSLHandshakeException -> NetworkError.ConnectionError("Secure connection failed")
            is ApiException -> when (exception.code) {
                401 -> NetworkError.AuthError("Session expired. Please log in again.")
                in 400..499 -> NetworkError.ClientError(exception.code, exception.message, exception.details)
                in 500..599 -> NetworkError.ServerError(exception.code, "Server error. Please try again later.")
                else -> NetworkError.UnknownError
            }
            else -> NetworkError.UnknownError
        }
    }

    fun toUserMessage(error: NetworkError): String {
        return when (error) {
            is NetworkError.ConnectionError -> "Check your internet connection and try again."
            is NetworkError.TimeoutError -> "The request took too long. Please try again."
            is NetworkError.ServerError -> "We're experiencing technical difficulties. Please try again later."
            is NetworkError.ClientError -> error.message
            is NetworkError.AuthError -> "Your session has expired. Please log in again."
            NetworkError.UnknownError -> "An unexpected error occurred. Please try again."
        }
    }
}

// Repository error handling
class UserRepositoryImpl(
    private val api: UserApi,
    private val dao: UserDao
) : UserRepository {

    override suspend fun getUser(userId: String): Result<User> {
        return try {
            val response = api.getUser(userId)
            Result.success(response.getOrThrow().toDomain())
        } catch (e: Exception) {
            val networkError = ErrorMapper.fromException(e)
            Log.e(TAG, "Failed to fetch user $userId: ${ErrorMapper.toUserMessage(networkError)}", e)
            Result.failure(networkError.toException())
        }
    }
}