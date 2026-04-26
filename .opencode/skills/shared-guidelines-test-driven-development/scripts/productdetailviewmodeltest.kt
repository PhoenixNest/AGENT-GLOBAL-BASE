// Test-first approach for Android ViewModel
class ProductDetailViewModelTest {

    @Test
    fun `add to cart with valid product triggers success`() = runTest {
        // RED: Write test for add-to-cart behavior
        val repository = MockProductRepository()
        repository.productResult = Product("1", "Headphones", 99.99, true)

        val viewModel = ProductDetailViewModel(repository)
        viewModel.loadProduct("1")
        testDispatcher.scheduler.advanceUntilIdle()

        var successCalled = false
        viewModel.onAddToCartSuccess = { successCalled = true }

        viewModel.addToCart()

        assertTrue(successCalled)
        assertEquals(1, repository.addToCartCalls)
    }
}

// GREEN: Implement minimum
class ProductDetailViewModel(
    private val repository: ProductRepository
) : ViewModel() {

    var onAddToCartSuccess: (() -> Unit)? = null
    private var product: Product? = null

    fun loadProduct(id: String) {
        viewModelScope.launch {
            product = repository.getProduct(id)
        }
    }

    fun addToCart() {
        val p = product ?: return
        repository.addToCart(p)
        onAddToCartSuccess?.invoke()
    }
}

// REFACTOR: Add error handling, loading states