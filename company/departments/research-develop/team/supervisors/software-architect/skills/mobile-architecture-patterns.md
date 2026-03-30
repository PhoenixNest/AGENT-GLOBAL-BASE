---
name: mobile-architecture-patterns
description: Cross-platform mobile architecture design for iOS and Android — clean architecture layering, shared-core (Kotlin Multiplatform), dependency injection, monorepo modularisation, and logical project structure design.
---

# Mobile Architecture Patterns

## Purpose

Design implementable, maintainable mobile application architectures for iOS, Android, and cross-platform (KMP/Flutter) projects. Produce logical project structures, module dependency graphs, and layer separation specifications that development leads can implement directly.

## Architecture Layers (Clean Architecture)

All mobile projects use a three-layer clean architecture unless explicitly overridden by ADR:

```
Presentation Layer
  └── UI components (Compose / SwiftUI / Flutter widgets)
  └── ViewModels / Presenters / BLoCs
  └── Navigation controller

Domain Layer  ← platform-agnostic (KMP shared if applicable)
  └── Use Cases / Interactors
  └── Domain models (pure data classes)
  └── Repository interfaces (abstraction only — no implementation)

Data Layer
  └── Repository implementations
  └── Remote data sources (API clients, DTOs)
  └── Local data sources (Room / CoreData / SQLite)
  └── Data mappers (DTO ↔ Domain model)
```

**Rule:** Dependencies point inward only. Presentation depends on Domain. Data depends on Domain. Domain depends on nothing.

## Platform Patterns

### Android
- **Recommended:** MVVM + Jetpack (ViewModel, StateFlow, Hilt, Room, Retrofit)
- **Navigation:** Single-Activity with Jetpack Navigation Component; NavGraph per feature module
- **DI:** Hilt (preferred over Dagger for new projects; Koin acceptable for KMP shared modules)
- **State management:** `StateFlow` + `UiState` sealed class per screen

### iOS
- **Recommended:** MVVM + Combine (SwiftUI projects); VIPER for complex flows requiring strict testability
- **Alternative:** The Composable Architecture (TCA) for state-heavy apps with complex navigation
- **Navigation:** NavigationStack (iOS 16+); coordinator pattern for pre-16 support
- **State management:** `@Published` + `ObservableObject`; `@Observable` macro (iOS 17+)

### Cross-Platform (KMP)
- Shared module contains: domain models, use cases, repository interfaces, repository implementations (non-UI)
- Platform modules contain: UI layer, DI setup, platform-specific data sources (SQLDelight for DB, Ktor for network)
- Shared module must have zero Android/iOS SDK imports

## Modularisation Strategy

### Module Boundaries
Split by feature, not by layer:
```
:app                    ← thin shell, navigation graph
:feature:auth           ← login, register, forgot password
:feature:home           ← home screen
:feature:settings       ← settings
:core:network           ← API client, interceptors
:core:database          ← Room/SQLDelight setup
:core:ui                ← shared design system components
:core:domain            ← shared domain models + use cases
```

### Dependency Rules
- `:feature:*` modules depend on `:core:*` only — never on each other
- `:core:ui` does not depend on `:core:network` or `:core:database`
- `:app` depends on all `:feature:*` modules (for navigation wiring only)

## Logical Project Structure Output

When producing a logical project structure, deliver:
1. Module tree (as above) with one-line description of each module's responsibility
2. Dependency graph (which module imports which)
3. Build time estimate impact: identify which modules on the critical build path
4. Test boundary: which modules are unit-testable without Android/iOS SDK

## Applied to This Project

When a specific project is active, this skill is applied by:
1. Reading the PRD, SRD, and IDS to identify features and data requirements
2. Selecting the appropriate platform pattern(s) per target platform(s)
3. Designing the module structure
4. Producing the logical project structure document as input to the UML Engineering Package
