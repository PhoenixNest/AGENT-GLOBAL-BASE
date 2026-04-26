// Android — custom annotation
@Retention(AnnotationRetention.RUNTIME)
@Target(AnnotationTarget.FUNCTION)
annotation class FlakyTest

// In build.gradle:
android {
    defaultConfig {
        testInstrumentationRunnerArgument "notAnnotation", "com.company.testing.FlakyTest"
    }
}

// Swift — test plan exclusion
// In .xctestplan: exclude tests with trait "flaky" from primary test target