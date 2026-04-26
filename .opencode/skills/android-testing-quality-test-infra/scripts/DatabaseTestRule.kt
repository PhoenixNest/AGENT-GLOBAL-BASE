class DatabaseTestRule(
    private val context: Context
) : TestWatcher() {

    lateinit var database: AppDatabase
        private set

    override fun starting(description: Description) {
        database = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)
            .allowMainThreadQueries() // Safe for tests
            .build()
    }

    override fun finished(description: Description) {
        database.close()
    }

    fun seedWithTestData() {
        database.userDao().upsert(UserFixtures.validUser())
        database.userDao().upsert(UserFixtures.validUser(id = "user-456", name = "Jane Doe"))
        database.orderDao().upsert(OrderFixtures.pendingOrder(userId = "user-123"))
        database.orderDao().upsert(OrderFixtures.completedOrder(userId = "user-456"))
    }
}