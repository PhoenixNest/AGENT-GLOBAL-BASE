class CheckoutViewModel(
    private val savedStateHandle: SavedStateHandle,
    private val paymentUseCase: ProcessPaymentUseCase
) : ViewModel() {

    companion object {
        private const val KEY_CART = "cart_state"
        private const val KEY_STEP = "checkout_step"
    }

    // State automatically saved/restored on process death
    private var _checkoutState = MutableStateFlow(
        CheckoutState(
            cart = savedStateHandle[KEY_CART] ?: Cart.empty(),
            currentStep = savedStateHandle[KEY_STEP] ?: CheckoutStep.CART
        )
    )

    init {
        // Persist state changes to SavedStateHandle
        viewModelScope.launch {
            _checkoutState
                .onEach { state ->
                    savedStateHandle[KEY_CART] = state.cart
                    savedStateHandle[KEY_STEP] = state.currentStep
                }
                .collect()
        }
    }
}