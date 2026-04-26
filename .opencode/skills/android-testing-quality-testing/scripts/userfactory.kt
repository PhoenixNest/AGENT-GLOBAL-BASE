object UserFactory {
    fun create(
        id: String = "test-user-id",
        name: String = "Test User",
        email: String = "test@example.com",
        createdAt: Long = 1_000_000L
    ): User {
        return User(
            id = id,
            name = name,
            email = email,
            createdAt = createdAt,
            preferences = UserPreferencesFactory.create()
        )
    }
}

object UserPreferencesFactory {
    fun create(
        theme: Theme = Theme.LIGHT,
        notificationsEnabled: Boolean = true,
        language: String = "en"
    ): UserPreferences {
        return UserPreferences(theme, notificationsEnabled, language)
    }
}