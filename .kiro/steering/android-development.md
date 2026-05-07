---
inclusion: fileMatch
fileMatchPattern: "**/*.kt,**/*.java,**/android/**,**/build.gradle.kts,**/build.gradle"
description: Android/Kotlin development patterns, architecture, and best practices
version: "1.0.0"
---

# Android Development Steering

This steering file provides Android-specific development guidance for the workspace. Activate manually when working on Android platform code.

## Android Platform Context

- **Target Platform:** Android (Mobile)
- **Primary Language:** Kotlin
- **Architecture Pattern:** MVVM, Clean Architecture
- **Build System:** Gradle (Kotlin DSL)
- **Minimum SDK:** As defined in project-specific build.gradle.kts
- **Target SDK:** Latest stable Android SDK

## Key Android Patterns

### 1. Architecture Components

- **ViewModel:** Lifecycle-aware data holders
- **LiveData/StateFlow:** Observable data holders
- **Room:** SQLite abstraction layer
- **WorkManager:** Background task scheduling
- **Navigation Component:** Fragment navigation

### 2. Kotlin Best Practices

- Use Kotlin coroutines for asynchronous operations
- Prefer `sealed class` for state management
- Use `data class` for immutable data models
- Leverage Kotlin extensions for cleaner code
- Use `by lazy` for expensive initializations

### 3. Android-Specific Conventions

- Follow Material Design 3 guidelines
- Use ViewBinding or Compose for UI
- Implement proper lifecycle management
- Handle configuration changes correctly
- Use dependency injection (Hilt/Koin)

### 4. Testing

- Unit tests: JUnit + MockK
- UI tests: Espresso
- Integration tests: AndroidX Test
- Aim for 80%+ code coverage on business logic

### 5. Security

- Follow OWASP MASVS standards (see `company/library/topics/security.md`)
- Use Android Keystore for sensitive data
- Implement certificate pinning for network calls
- Obfuscate code with R8/ProGuard
- Validate all user inputs

### 6. Performance

- Use Android Profiler for performance analysis
- Optimize RecyclerView with DiffUtil
- Implement proper image loading (Coil/Glide)
- Minimize main thread work
- Use WorkManager for background tasks

## Related Resources

- **Company Security Standards:** `company/library/topics/security.md`
- **Company Testing Standards:** `company/library/topics/testing.md`
- **Android Engineering Skills:** `.kiro/skills/android-engineering/`
- **Mobile Pipeline:** `.kiro/steering/mobile-pipeline.md`

## When to Activate

Activate this steering file when:

- Working on Android-specific code (_.kt, _.java in Android modules)
- Reviewing Android architecture decisions
- Implementing Android platform features
- Debugging Android-specific issues
- Writing Android tests
