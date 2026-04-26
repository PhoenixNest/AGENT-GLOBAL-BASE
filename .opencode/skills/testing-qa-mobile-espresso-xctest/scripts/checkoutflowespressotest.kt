@RunWith(AndroidJUnit4::class)
@LargeTest
class CheckoutFlowEspressoTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Before
    fun registerIdlingResources() {
        IdlingRegistry.getInstance().register(EspressoIdlingResource.countingIdlingResource)
    }

    @After
    fun unregisterIdlingResources() {
        IdlingRegistry.getInstance().unregister(EspressoIdlingResource.countingIdlingResource)
    }

    @Test
    fun completePurchase_validCard_confirmsOrder() {
        // Navigate to checkout
        onView(withId(R.id.cart_button)).perform(click())
        onView(withId(R.id.checkout_button)).perform(click())

        // Fill payment form
        onView(withId(R.id.card_number_input)).perform(typeText("4111111111111111"), closeSoftKeyboard())
        onView(withId(R.id.expiry_input)).perform(typeText("12/28"), closeSoftKeyboard())
        onView(withId(R.id.cvv_input)).perform(typeText("123"), closeSoftKeyboard())

        // Submit and verify
        onView(withId(R.id.pay_button)).perform(click())
        onView(withId(R.id.order_confirmation)).check(matches(isDisplayed()))
        onView(withId(R.id.order_confirmation)).check(matches(withText(containsString("Order confirmed"))))
    }
}