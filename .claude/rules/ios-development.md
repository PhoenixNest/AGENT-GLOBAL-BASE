---
paths:
  - "**/*.swift"
  - "**/ios/**"
  - "**/Podfile"
  - "**/Package.swift"
  - "**/project.pbxproj"
description: iOS/Swift development patterns and best practices
---

# iOS Development

Platform-specific guidance for iOS development. See `.claude/skills/ios-engineering/` for deep sub-skills.

---

## Key iOS Patterns

### SwiftUI & UIKit

- **SwiftUI:** Preferred for new UI development
- **UIKit:** Legacy support and complex custom views
- **Combine:** Reactive programming framework
- **Async/Await:** Modern concurrency patterns

### Swift Best Practices

- Use async/await and actors for concurrency
- Prefer `struct` over `class` for value types
- Use `enum` with associated values for state
- Leverage protocol-oriented programming

### Security (OWASP MASVS)

- Keychain for sensitive data
- Certificate pinning for network calls
- App Transport Security (ATS)
- Validate all user inputs

### Testing

- Unit tests: XCTest
- UI tests: XCUITest
- Snapshot tests: swift-snapshot-testing
- Target: 80%+ coverage on business logic

---

## Related Rules

- `mobile-pipeline.md` — Mobile development pipeline requirements
- `security-architecture.md` — OWASP MASVS standards
