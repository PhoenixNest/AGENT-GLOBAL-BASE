---
paths:
  - "**/*.kt"
  - "**/*.java"
  - "**/android/**"
  - "**/build.gradle.kts"
  - "**/build.gradle"
description: Android/Kotlin development patterns and best practices
---

# Android Development

Platform-specific guidance for Android development. See `.claude/skills/android-engineering/` for deep sub-skills.

---

## Key Android Patterns

### Architecture Components

- **ViewModel:** Lifecycle-aware data holders
- **StateFlow:** Observable state management
- **Room:** SQLite abstraction layer
- **WorkManager:** Background task scheduling

### Kotlin Best Practices

- Use coroutines for asynchronous operations
- Prefer `sealed class` for state management
- Use `data class` for immutable data models
- Use `by lazy` for expensive initializations

### Security (OWASP MASVS)

- Android Keystore for sensitive data
- Certificate pinning for network calls
- R8/ProGuard code obfuscation
- Validate all user inputs

### Testing

- Unit tests: JUnit + MockK
- UI tests: Espresso
- Integration tests: AndroidX Test
- Target: 80%+ coverage on business logic

---

## Related Rules

- `mobile-pipeline.md` — Mobile development pipeline requirements
- `security-architecture.md` — OWASP MASVS standards
