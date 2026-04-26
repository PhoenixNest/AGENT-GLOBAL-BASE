// Retry annotation for known-flaky tests during investigation
@Retention(AnnotationRetention.RUNTIME)
@Target(AnnotationTarget.FUNCTION)
annotation class FlakyTest(val reason: String, val maxRetries: Int = 3)

// JUnit 5 extension for automatic retry
class FlakyTestExtension : InvocationInterceptor {
    override fun interceptTestMethod(
        invocation: InvocationInterceptor.Invocation<Void>,
        invocationContext: ReflectiveInvocationContext<Method>,
        extensionContext: ExtensionContext
    ) {
        val annotation = invocationContext.testMethod
            .flatMap { it.getAnnotation(FlakyTest::class.java).stream() }
            .findFirst()
            .orElse(null) ?: return invocation.proceed()

        var lastException: Throwable? = null
        repeat(annotation.maxRetries) { attempt ->
            try {
                invocation.proceed()
                return  // Test passed
            } catch (e: Throwable) {
                lastException = e
                println("Flaky test retry ${attempt + 1}/${annotation.maxRetries}: ${e.message}")
                Thread.sleep(1000) // Brief pause between retries
            }
        }
        throw lastException!!
    }
}

// Usage
@ExtendWith(FlakyTestExtension::class)
class FlakyTests {

    @FlakyTest(reason = "Network timing variability on CI", maxRetries = 3)
    @Test
    fun whenFetchData_thenReturnsResults() {
        // This test may fail due to CI network timing
        // Quarantined until root cause is fixed
    }
}