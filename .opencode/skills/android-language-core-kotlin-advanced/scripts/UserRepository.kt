// CORRECT: SupervisorJob allows sibling coroutines to survive individual failures
class UserRepository(
    private val api: UserApi,
    private val database: UserDao
) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    fun syncUsers() = scope.launch {
        // If fetchUsers fails, cacheUsers won't be affected
        // and other sibling launches continue executing
    }
}

// WRONG: GlobalScope leaks coroutines beyond component lifecycle
fun syncUsers() = GlobalScope.launch { ... }