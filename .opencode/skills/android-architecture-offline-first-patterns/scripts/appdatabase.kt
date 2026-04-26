@Database(
    entities = [UserEntity::class, OrderEntity::class],
    version = 3,
    exportSchema = true  // Exports schema to build output for diff verification
)
abstract class AppDatabase : RoomDatabase() {

    companion object {
        private val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL("ALTER TABLE users ADD COLUMN lastSyncedAt INTEGER NOT NULL DEFAULT 0")
            }
        }

        private val MIGRATION_2_3 = object : Migration(2, 3) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL("CREATE INDEX IF NOT EXISTS index_users_email ON users(email)")
            }
        }

        fun build(context: Context): AppDatabase {
            return Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
                .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
                // NEVER use fallbackToDestructiveMigration in production
                .build()
        }
    }
}