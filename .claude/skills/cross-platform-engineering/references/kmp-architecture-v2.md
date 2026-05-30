---
name: kmp-architecture
description: Architect Kotlin Multiplatform (KMP) shared modules — defining the shared/platform boundary, expect/actual implementations, and coroutine-based ViewModel layer — enabling maximum code reuse between Android and iOS without sacrificing platform-native UI quality.
version: "1.0.0"
---

# KMP Architecture

| Competency           | Description                                                             | Quality Criteria                                                                                                              |
| -------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Shared Module Design | Define the boundary between shared Kotlin code and platform-specific    | Shared module contains: domain models, use cases, repositories (interfaces), ViewModels; UI stays 100% platform-native        |
| Expect/Actual        | Design expect/actual declarations for platform-specific implementations | Expect declarations are minimal interfaces; actual implementations use platform-optimal APIs (no `@Throws` on every function) |
| KMP ViewModel Layer  | Implement shared ViewModels using kotlinx-coroutines and StateFlow      | ViewModels expose `StateFlow<UiState>` and `SharedFlow<UiEffect>`; no Android lifecycle imports in shared module              |
| Dependency Injection | Configure Koin for KMP — shared module + platform modules               | Koin modules split: shared definitions in `commonMain`, platform overrides in `androidMain`/`iosMain`                         |

## Execution Guidance

### Module Structure

```
shared/
├── commonMain/
│   ├── domain/           # Models, use cases, repository interfaces
│   ├── presentation/     # ViewModels, UiState, UiEffect
│   └── di/               # Koin shared module
├── androidMain/
│   └── di/               # Android-specific Koin overrides
└── iosMain/
    └── di/               # iOS-specific Koin overrides

androidApp/               # Android Compose UI
iosApp/                   # SwiftUI (consumes shared ViewModels via SKIE)
```

### Shared Boundary Rules

| Allowed in shared module     | Not allowed in shared module        |
| ---------------------------- | ----------------------------------- |
| Domain models (data classes) | Android Context, Activity, Fragment |
| Use cases                    | UIKit / SwiftUI / Compose types     |
| Repository interfaces        | Platform lifecycle components       |
| ViewModels (no Android deps) | SQLite direct (use SQLDelight)      |
| Network (Ktor)               | File path manipulation (use Okio)   |
