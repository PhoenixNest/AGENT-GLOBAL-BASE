// commonMain — using generated queries
class ItemLocalDataSource(private val database: AppDatabase) {
    fun getAll(): List<Item> = database.itemQueries.selectAll().executeAsList()
    fun insert(item: Item) = database.itemQueries.insert(item.id, item.name, item.createdAt)
}