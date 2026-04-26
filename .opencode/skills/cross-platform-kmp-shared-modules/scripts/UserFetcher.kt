// Kotlin — suspend function
class UserFetcher(private val api: UserApi) {
    suspend fun fetchUser(id: String): User {
        return api.getUser(id)
    }
}

// Swift — generated as async function
// let fetcher = UserFetcher(api: api)
// let user = try await fetcher.fetchUser(id: "123")

// Kotlin — Flow
class UserObserver(private val api: UserApi) {
    fun observeUser(id: String): Flow<User> {
        return flow {
            while (isActive) {
                val user = api.getUser(id)
                emit(user)
                delay(30_000)
            }
        }
    }
}

// Swift — generated as AsyncSequence
// for try await user in fetcher.observeUser(id: "123") {
//     print(user.name)
// }