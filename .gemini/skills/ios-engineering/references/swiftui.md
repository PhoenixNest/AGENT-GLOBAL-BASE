---
name: swiftui
description: Build production-quality SwiftUI views and navigation — using declarative composition, custom view modifiers, animation, and the SwiftUI data flow model (StateObject, ObservedObject, EnvironmentObject) — for iOS features delivered in Stage 5 development.
version: "1.0.0"
---

# swiftui

| Competency        | Description                                                   | Quality Criteria                                                                                                               |
| ----------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Declarative Views | Compose SwiftUI views using modifiers, stacks, and containers | Views are small and composable (< 100 lines); no large view bodies; custom ViewModifiers for reusable styling                  |
| Data Flow         | Use appropriate property wrappers for state management        | `@State` for local; `@StateObject` for owned observable; `@ObservedObject` for injected; `@EnvironmentObject` for shared state |
| Navigation        | Implement SwiftUI NavigationStack with programmatic routing   | NavigationStack with `NavigationPath` for programmatic navigation; deep link support via URL scheme handling                   |
| Animation         | Add intentional, accessible animations                        | Animations use `withAnimation`; reduced motion respected via `accessibilityReduceMotion` environment value                     |

## Execution Guidance

### View Composition Pattern

```swift
struct ProductListView: View {
    @StateObject private var viewModel: ProductListViewModel

    var body: some View {
        NavigationStack {
            List(viewModel.products) { product in
                NavigationLink(value: product) {
                    ProductRowView(product: product)
                }
            }
            .navigationTitle("Products")
            .navigationDestination(for: Product.self) { product in
                ProductDetailView(product: product)
            }
        }
        .task { await viewModel.loadProducts() }
    }
}
```

### Data Flow Decision Guide

| Scenario                             | Wrapper                     |
| ------------------------------------ | --------------------------- |
| Simple toggle, counter in one view   | `@State`                    |
| ViewModel owned by this view         | `@StateObject`              |
| ViewModel created and passed in      | `@ObservedObject`           |
| App-wide state (theme, auth session) | `@EnvironmentObject`        |
| Simple value passed from parent      | `let` property (no wrapper) |
