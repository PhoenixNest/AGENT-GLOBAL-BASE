@Entity(tableName = "orders")
data class OrderEntity(
    @PrimaryKey val id: String,
    val userId: String,
    val status: OrderStatus,
    val totalAmount: Long,  // Store as Long (cents) to avoid floating point issues
    val createdAt: Long,
    val updatedAt: Long,
    val syncStatus: SyncStatus = SyncStatus.SYNCED
)

@Entity(tableName = "order_items")
data class OrderItemEntity(
    @PrimaryKey val id: String,
    val orderId: String,
    val productId: String,
    val productName: String,
    val quantity: Int,
    val unitPrice: Long
)

// Relation with junction — one order has many items
data class OrderWithItems(
    @Embedded val order: OrderEntity,
    @Relation(
        parentColumn = "id",
        entityColumn = "orderId"
    )
    val items: List<OrderItemEntity>
)

// DAO with optimized queries
@Dao
abstract class OrderDao {

    @Query("""
        SELECT * FROM orders
        WHERE userId = :userId
        ORDER BY createdAt DESC
        LIMIT :limit OFFSET :offset
    """)
    abstract suspend fun getOrdersByUser(
        userId: String,
        limit: Int = 50,
        offset: Int = 0
    ): List<OrderEntity>

    @Query("SELECT * FROM orders WHERE userId = :userId ORDER BY createdAt DESC")
    abstract fun observeOrdersByUser(userId: String): Flow<List<OrderEntity>>

    @Transaction
    @Query("SELECT * FROM orders WHERE id = :orderId")
    abstract suspend fun getOrderWithItems(orderId: String): OrderWithItems?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    abstract suspend fun upsert(order: OrderEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    abstract suspend fun upsertAll(orders: List<OrderEntity>)

    @Transaction
    open suspend fun replaceOrdersForUser(
        userId: String,
        newOrders: List<OrderEntity>,
        newItems: List<OrderItemEntity>
    ) {
        // Delete old orders and items in single transaction
        deleteOrdersByUser(userId)
        upsertAll(newOrders)
        upsertAllItems(newItems)
    }

    @Query("DELETE FROM orders WHERE userId = :userId")
    abstract suspend fun deleteOrdersByUser(userId: String)

    @Query("DELETE FROM order_items WHERE orderId IN (SELECT id FROM orders WHERE userId = :userId)")
    abstract suspend fun deleteItemsByUser(userId: String)

    @Query("""
        SELECT COUNT(*) FROM orders
        WHERE syncStatus = :status
    """)
    abstract suspend fun getPendingSyncCount(status: SyncStatus = SyncStatus.PENDING): Int
}