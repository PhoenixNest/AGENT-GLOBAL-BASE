---
name: swift-familiarization
description: Develop working proficiency in Swift and iOS development patterns — sufficient to read, review, and contribute to the iOS codebase — enabling the cross-platform engineer to bridge KMP shared module work with iOS-specific implementation requirements.
version: "1.0.0"
---

# Swift Familiarization

| Competency         | Description                                                     | Quality Criteria                                                                                                      |
| ------------------ | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Swift Fundamentals | Read and write idiomatic Swift — optionals, closures, protocols | Can implement a feature using Swift's type system without force-unwrapping or type erasure workarounds                |
| SwiftUI Basics     | Build and modify SwiftUI views for KMP integration points       | Can add a new screen consuming a KMP shared ViewModel; understands `@State`, `@ObservedObject`, `@StateObject`        |
| iOS–KMP Bridge     | Implement the KMP-iOS interoperability layer                    | Correctly wraps KMP Kotlin coroutines as Swift async/await using `skie` or `kotlinx-coroutines-core`; no memory leaks |
| iOS Build Tools    | Operate Xcode, CocoaPods, and Swift Package Manager             | Can resolve dependency conflicts; understands scheme/target structure; can diagnose common Xcode build failures       |

## Execution Guidance

### KMP–iOS Integration Patterns

When exposing KMP shared code to iOS:

1. **Use SKIE for coroutine bridging:** Wraps suspend functions as Swift async functions automatically — eliminating manual callback bridging.
2. **Wrap shared ViewModels:** iOS ViewModels should be thin wrappers over the KMP ViewModel, converting Kotlin StateFlow to Swift `@Published` properties.
3. **Error type mapping:** Map Kotlin sealed class errors to Swift enum cases in the bridge layer — do not expose raw `KotlinThrowable` to SwiftUI.

### Learning Path

| Week | Focus                            | Exercise                                        |
| ---- | -------------------------------- | ----------------------------------------------- |
| 1    | Swift syntax and type system     | Rewrite 3 Kotlin functions in Swift             |
| 2    | SwiftUI fundamentals             | Build a simple list screen from the design spec |
| 3    | iOS app lifecycle and navigation | Add a new navigation destination to the iOS app |
| 4    | KMP–iOS bridge implementation    | Expose a KMP ViewModel to a new SwiftUI screen  |
