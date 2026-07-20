---
paths:
  - "**/*.dart"
  - "**/commonMain/**"
  - "**/androidMain/**"
  - "**/iosMain/**"
  - "**/commonTest/**"
  - "pubspec.yaml"
description: KMP/Flutter cross-platform development patterns
---

# Cross-Platform Development

KMP and Flutter cross-platform guidance. See `.claude/skills/cross-platform-engineering/` for deep sub-skills.

---

## KMP Project Structure

```
shared/
├── commonMain/   # Shared code (business logic, models, networking)
├── androidMain/  # Android-specific
├── iosMain/      # iOS-specific
└── commonTest/   # Shared tests
```

## KMP Best Practices

- `expect`/`actual` for platform-specific implementations
- Keep business logic in `commonMain`
- Ktor for networking, SQLDelight for database (cross-platform)
- Kotlin coroutines for async operations
- Version catalogs for dependency management

## Flutter Best Practices

- BLoC or Riverpod for state management
- `const` constructors for performance
- MethodChannel for native code
- Follow Flutter style guide

## Code Sharing Strategy

**Share:** Business logic, data models, API clients, database access, validation logic

**Don't Share:** UI code, platform APIs, native integrations

---

## Related Rules

- `mobile-pipeline.md` — Mobile pipeline requirements
- `android-development.md`, `ios-development.md` — Platform layers
