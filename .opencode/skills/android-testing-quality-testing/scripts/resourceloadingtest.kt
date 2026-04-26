@RunWith(RobolectricTestRunner::class)
@Config(
    sdk = [33],
    application = TestApplication::class,
    qualifiers = "en-rUS"
)
class ResourceLoadingTest {

    @Test
    fun `loads string resources correctly`() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        val appName = context.getString(R.string.app_name)
        assertEquals("MyApp", appName)
    }

    @Test
    fun `loads drawable resources correctly`() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        val drawable = ContextCompat.getDrawable(context, R.drawable.ic_launcher)
        assertNotNull(drawable)
    }
}