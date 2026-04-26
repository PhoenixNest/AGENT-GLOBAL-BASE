@RunWith(AndroidJUnit4::class)
class AccessibilityTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun allScreens_passAccessibilityChecks() {
        // Navigate through all screens
        onView(withId(R.id.nav_home)).perform(click())
        assertAccessibilityConformance()

        onView(withId(R.id.nav_profile)).perform(click())
        assertAccessibilityConformance()

        onView(withId(R.id.nav_settings)).perform(click())
        assertAccessibilityConformance()
    }

    private fun assertAccessibilityConformance() {
        val checkResult = AccessibilityChecker.checkRootViewWithResult()
        val issues = checkResult.runChecks()

        // Fail on any accessibility issues
        assertTrue(
            "Accessibility issues found:\n${issues.joinToString("\n") { it.getMessage() }}",
            issues.isEmpty()
        )
    }
}