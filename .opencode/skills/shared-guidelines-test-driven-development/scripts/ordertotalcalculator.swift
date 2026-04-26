struct OrderTotalCalculator {
    func calculateTotal(for order: Order) -> Double {
        order.items
            .map { lineItemTotal(for: $0) }
            .reduce(0, +)
    }

    private func lineItemTotal(for item: OrderItem) -> Double {
        item.price * Double(item.quantity)
    }
}

// All tests still pass — behavior unchanged, structure improved