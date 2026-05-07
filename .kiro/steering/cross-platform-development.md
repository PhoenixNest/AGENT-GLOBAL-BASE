---
inclusion: manual
description: KMP/Flutter cross-platform development patterns and best practices
---

# Cross-Platform Development Steering

This steering file provides cross-platform development guidance for Kotlin Multiplatform (KMP) and Flutter projects. Activate manually when working on shared code.

## Cross-Platform Context

- **Primary Frameworks:** Kotlin Multiplatform (KMP), Flutter
- **Shared Code:** Business logic, data models, networking, storage
- **Platform-Specific:** UI, platform APIs, native integrations
- **Build System:** Gradle (KMP), Flutter CLI (Flutter)

## Kotlin Multiplatform (KMP)

### 1. Project Structure

```
shared/
├── commonMain/        # Shared code
├── androidMain/       # Android-specific
├── iosMain/          # iOS-specific
└── commonTest/       # Shared tests
```

### 2. KMP Best Practices

- Use `expect`/`actual` for platform-specific implementations
- Keep business logic in `commonMain`
- Use Ktor for networking (cross-platform)
- Use SQLDelight for database (cross-platform)
- Leverage Kotlin coroutines for async operations

### 3. Dependency Management

- Use version catalogs for dependency management
- Prefer multiplatform libraries (Ktor, SQLDelight, Koin)
- Minimize platform-specific dependencies
- Use CocoaPods for iOS dependencies

### 4. Testing Strategy

- Write tests in `commonTest` for shared logic
- Platform-specific tests in `androidTest`/`iosTest`
- Use `kotlin.test` for cross-platform testing
- Mock platform-specific code with `expect`/`actual`

## Flutter

### 1. Project Structure

```
lib/
├── main.dart
├── features/         # Feature modules
├── core/            # Shared utilities
└── platform/        # Platform channels
```

### 2. Flutter Best Practices

- Use BLoC or Riverpod for state management
- Implement proper widget composition
- Use const constructors for performance
- Leverage platform channels for native code
- Follow Flutter style guide

### 3. Platform Integration

- Use MethodChannel for platform communication
- Implement platform-specific code in native modules
- Handle platform differences gracefully
- Test on both iOS and Android

## Shared Patterns

### 1. Architecture

- **Clean Architecture:** Separate concerns (domain, data, presentation)
- **Repository Pattern:** Abstract data sources
- **Dependency Injection:** Use Koin (KMP) or GetIt (Flutter)
- **State Management:** Centralized state handling

### 2. Code Sharing Strategy

**Share:**

- Business logic
- Data models
- API clients
- Database access
- Validation logic

**Don't Share:**

- UI code (platform-specific)
- Platform APIs
- Native integrations
- Platform-specific optimizations

### 3. Testing

- Unit tests for shared business logic
- Integration tests for data layer
- Platform-specific UI tests
- Aim for 80%+ coverage on shared code

### 4. Performance

- Minimize platform boundary crossings
- Cache data appropriately
- Use lazy initialization
- Profile on both platforms
- Optimize hot paths

## Related Resources

- **Company Architecture Standards:** `company/library/topics/architecture.md`
- **Company Testing Standards:** `company/library/topics/testing.md`
- **Cross-Platform Engineering Skills:** `.kiro/skills/cross-platform-engineering/`
- **Mobile Pipeline:** `.kiro/steering/mobile-pipeline.md`

## When to Activate

Activate this steering file when:

- Working on KMP shared modules
- Implementing Flutter cross-platform features
- Reviewing cross-platform architecture
- Debugging platform-specific issues in shared code
- Writing cross-platform tests
