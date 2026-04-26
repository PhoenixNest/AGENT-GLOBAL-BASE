object UserFixtures {
    fun validUser(
        id: String = "user-${randomId()}",
        name: String = "John Doe",
        email: String = "john@example.com",
        age: Int = 30,
        preferences: UserPreferences = UserPreferencesFixtures.defaults()
    ): User {
        return User(id, name, email, age, preferences)
    }

    fun userWithInvalidEmail() = validUser(email = "not-an-email")
    fun userWithLongName() = validUser(name = "A".repeat(256))
    fun userWithSpecialCharacters() = validUser(
        name = "José García Müller",
        email = "jose+test@example.com"
    )
    fun emptyUser() = validUser(name = "", email = "")
    fun userWithNullFields() = validUser(name = "", email = "")
}

object OrderFixtures {
    fun pendingOrder(
        id: String = "order-${randomId()}",
        userId: String = "user-123",
        items: List<OrderItem> = listOf(OrderItemFixtures.singleItem()),
        totalAmount: Long = items.sumOf { it.unitPrice * it.quantity }
    ): Order {
        return Order(
            id = id,
            userId = userId,
            status = OrderStatus.PENDING,
            items = items,
            totalAmount = totalAmount,
            createdAt = Instant.now().toEpochMilli()
        )
    }

    fun completedOrder() = pendingOrder().copy(status = OrderStatus.DELIVERED)
    fun cancelledOrder() = pendingOrder().copy(status = OrderStatus.CANCELLED)
    fun emptyOrder() = pendingOrder(items = emptyList())
    fun orderWithManyItems(count: Int = 100) = pendingOrder(
        items = List(count) { OrderItemFixtures.randomItem() }
    )
}

object OrderItemFixtures {
    fun singleItem(
        id: String = "item-${randomId()}",
        productId: String = "prod-123",
        name: String = "Test Product",
        quantity: Int = 1,
        unitPrice: Long = 999  // $9.99
    ): OrderItem {
        return OrderItem(id, productId, name, quantity, unitPrice)
    }

    fun randomItem(): OrderItem = singleItem(
        productId = "prod-${randomId()}",
        name = "Product ${randomId()}",
        unitPrice = (100L..9999L).random()
    )
}

private fun randomId() = UUID.randomUUID().toString().take(8)