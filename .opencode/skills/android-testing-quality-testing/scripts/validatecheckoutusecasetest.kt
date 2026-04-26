// STEP 1: RED — Write the failing test first
class ValidateCheckoutUseCaseTest {

    private val cartRepository = mockk<CartRepository>()
    private val paymentValidator = mockk<PaymentValidator>()
    private lateinit var useCase: ValidateCheckoutUseCase

    @Before
    fun setup() {
        useCase = ValidateCheckoutUseCase(cartRepository, paymentValidator)
    }

    @Test
    fun `given empty cart, when validate, then returns empty cart error`() = runTest {
        // Given
        every { cartRepository.getCart() } returns Cart.empty()

        // When
        val result = useCase.execute()

        // Then
        assertTrue(result.isFailure)
        assertEquals(ValidationError.EMPTY_CART, result.exceptionOrNull())
    }
}

// STEP 2: GREEN — Implement minimum code to pass
class ValidateCheckoutUseCase(
    private val cartRepository: CartRepository,
    private val paymentValidator: PaymentValidator
) {
    suspend fun execute(): Result<CheckoutValidation> {
        val cart = cartRepository.getCart()
        if (cart.items.isEmpty()) {
            return Result.failure(ValidationError.EMPTY_CART)
        }
        return Result.success(CheckoutValidation(cart))
    }
}

// STEP 3: REFACTOR — Improve code while keeping tests green
// Extract validation logic, improve naming, remove duplication
// All tests still pass — confidence that refactoring didn't break behavior