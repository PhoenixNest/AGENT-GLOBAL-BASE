# References

## References

### Official Documentation

- [Android Testing Documentation](https://developer.android.com/training/testing)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [MockK Documentation](https://mockk.io/)
- [Robolectric Documentation](https://robolectric.org/)
- [kotlinx-coroutines-test](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/)
- [Turbine (Flow Testing)](https://github.com/cashapp/turbine)
- [XCTest Documentation](https://developer.apple.com/documentation/xctest)
- [Swift Testing Documentation](https://developer.apple.com/documentation/testing)
- [Flutter Testing Cookbook](https://docs.flutter.dev/cookbook/testing)

### Libraries and Tools

| Category           | Android                          | iOS                        | Cross-Platform               |
| ------------------ | -------------------------------- | -------------------------- | ---------------------------- |
| Framework          | JUnit 5                          | XCTest, Swift Testing      | JUnit 5 (KMP), flutter_test  |
| Assertions         | Truth, Kotest                    | XCTestAssertions, #expect  | Truth, expect                |
| Mocking            | MockK                            | Manual (protocols), Cuckoo | Manual, MockK (KMP)          |
| Coroutines/Async   | kotlinx-coroutines-test, Turbine | XCTest async/await         | kotlinx-coroutines-test      |
| Android Simulation | Robolectric                      | N/A                        | N/A                          |
| Coverage           | JaCoCo                           | Xcode Coverage, Slather    | JaCoCo (KMP), lcov (Flutter) |
| Test Data          | Kotlin Faker                     | Manual factories           | Faker libraries              |

### Company Standards

- Stage 7 Pipeline Specification — `.opencode/pipeline/mobile-development/pipeline.md`
- Defect Severity System — P0/P1/P2/P3 classification
- Code Coverage Standards — 80% branch / 90% line coverage minimum
- OWASP MASVS — Security testing requirements
- WCAG 2.1 AA — Accessibility compliance targets

### Further Reading

- "Test-Driven Development by Example" — Kent Beck
- "Unit Testing Principles, Practices, and Patterns" — Vladimir Khorikov
- "Effective Testing with XCTest" — iOS-specific deep dive
- "Kotlin Coroutines: Testing" — Official Kotlin documentation
- "Clean Architecture" — Robert C. Martin (repository and use case patterns)
