// Application class — initialize and configure Crashlytics
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()

        FirebaseApp.initializeApp(this)

        // Set user identifier for crash correlation
        Firebase.auth.currentUser?.uid?.let { uid ->
            Firebase.crashlytics.setUserId(uid)
        }

        // Set custom keys for crash context
        Firebase.crashlytics.setCustomKey("app_version", BuildConfig.VERSION_NAME)
        Firebase.crashlytics.setCustomKey("build_type", BuildConfig.BUILD_TYPE)
        Firebase.crashlytics.setCustomKey("api_environment", BuildConfig.API_ENVIRONMENT)
    }
}

// Repository layer — log breadcrumb for crash context
class UserRepositoryImpl(
    private val api: UserApi,
    private val dao: UserDao
) : UserRepository {

    override suspend fun getUser(id: String): Result<User> {
        return try {
            Firebase.crashlytics.log("Fetching user: $id")
            val response = api.getUser(id)
            Result.success(response.toDomain())
        } catch (e: Exception) {
            Firebase.crashlytics.log("Failed to fetch user: $id — ${e.message}")
            Firebase.crashlytics.setCustomKey("failed_user_id", id)
            Result.failure(e)
        }
    }
}

// Non-fatal exception reporting
fun reportNonFatalException(exception: Exception, context: Map<String, String> = emptyMap()) {
    context.forEach { (key, value) ->
        Firebase.crashlytics.setCustomKey(key, value)
    }
    Firebase.crashlytics.recordException(exception)
}