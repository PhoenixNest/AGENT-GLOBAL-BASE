---
inclusion: fileMatch
fileMatchPattern: "**/*.swift,**/ios/**,**/Podfile,**/Package.swift,**/project.pbxproj"
description: iOS/Swift development patterns, architecture, and best practices
version: "1.0.0"
---

# iOS Development Steering

This steering file provides iOS-specific development guidance for the workspace. Activate manually when working on iOS platform code.

## iOS Platform Context

- **Target Platform:** iOS (Mobile)
- **Primary Language:** Swift
- **Architecture Pattern:** MVVM, Clean Architecture, TCA (The Composable Architecture)
- **Build System:** Xcode, Swift Package Manager
- **Minimum iOS Version:** As defined in project-specific settings
- **Target iOS Version:** Latest stable iOS SDK

## Key iOS Patterns

### 1. SwiftUI & UIKit

- **SwiftUI:** Preferred for new UI development
- **UIKit:** Legacy support and complex custom views
- **Combine:** Reactive programming framework
- **Async/Await:** Modern concurrency patterns
- **Observation Framework:** State management (iOS 17+)

### 2. Swift Best Practices

- Use Swift concurrency (async/await, actors)
- Prefer `struct` over `class` for value types
- Use `enum` with associated values for state
- Leverage protocol-oriented programming
- Use property wrappers (@State, @Binding, @Published)

### 3. iOS-Specific Conventions

- Follow Apple Human Interface Guidelines
- Use SF Symbols for icons
- Implement proper memory management (ARC)
- Handle app lifecycle correctly
- Use dependency injection (Resolver/Swinject)

### 4. Testing

- Unit tests: XCTest
- UI tests: XCUITest
- Snapshot tests: swift-snapshot-testing
- Aim for 80%+ code coverage on business logic

### 5. Security

- Follow OWASP MASVS standards (see `company/library/topics/security.md`)
- Use Keychain for sensitive data
- Implement certificate pinning for network calls
- Use App Transport Security (ATS)
- Validate all user inputs

### 6. Performance

- Use Instruments for performance profiling
- Optimize table/collection view scrolling
- Implement proper image caching (Kingfisher/SDWebImage)
- Minimize main thread work
- Use background queues for heavy operations

### 7. Swift Concurrency

- Use `async/await` for asynchronous operations
- Use `actor` for thread-safe state management
- Use `Task` for structured concurrency
- Avoid callback hell with modern concurrency
- Handle cancellation properly

## Related Resources

- **Company Security Standards:** `company/library/topics/security.md`
- **Company Testing Standards:** `company/library/topics/testing.md`
- **iOS Engineering Skills:** `.kiro/skills/ios-engineering/`
- **Mobile Pipeline:** `.kiro/steering/mobile-pipeline.md`

## When to Activate

Activate this steering file when:

- Working on iOS-specific code (\*.swift in iOS modules)
- Reviewing iOS architecture decisions
- Implementing iOS platform features
- Debugging iOS-specific issues
- Writing iOS tests
