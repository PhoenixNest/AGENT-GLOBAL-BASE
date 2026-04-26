@RunWith(AndroidJUnit4::class)
class MigrationTest {
    private val TEST_DB = "migration-test.db"

    @Test
    fun migrate2To3_containsCorrectData() {
        // Create database at version 2
        val helper = MigrationTestHelper(
            InstrumentationRegistry.getInstrumentation(),
            AppDatabase::class.java
        )
        val db2 = helper.createDatabase(TEST_DB, 2).apply {
            execSQL("INSERT INTO users (id, name, email) VALUES ('1', 'Test', 'test@example.com')")
            close()
        }

        // Migrate to version 3
        val db3 = helper.runMigrationsAndValidate(TEST_DB, 3, true, MIGRATION_2_3)

        // Verify data preserved
        val cursor = db3.query("SELECT lastSyncedAt FROM users WHERE id = '1'")
        assertTrue(cursor.moveToFirst())
        assertEquals(0, cursor.getLong(0))
    }
}