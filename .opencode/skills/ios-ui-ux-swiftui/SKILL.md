---
name: ios-ui-ux-swiftui
description: "SwiftUI declarative UI development for native iOS apps — view composition, state management (@State, @StateObject, @Binding, @Environment), NavigationStack, custom transitions, matchedGeometryEffect, view modifiers, and performance optimization. Owned by Seo-Yeon Park (iOS Lead). Use during Stage 5 (Development) for SwiftUI UI implementation and Stage 6 (Code Review) for SwiftUI conformance. Trigger: swiftui, declarative ui, @state, @stateobject, @binding, @environment, navigationstack, matchedgeometryeffect, view modifier, custom transition, lazyvstack, drawinggroup."
prerequisites:
  - ios-architecture-swift-concurrency

version: "1.0.0"
---

# SwiftUI

**Category:** Mobile Engineering — iOS UI
**Owner:** iOS Engineer (Camila Rodriguez)

## Overview

This skill implements production-grade SwiftUI development covering declarative UI patterns, StateObject/ObservedObject lifecycle, custom transitions, view modifiers, and performance optimization. It applies to Stage 5 (Development) where all new iOS UI is built with SwiftUI, Stage 6 (Code Review) where view composition and state management are audited, and Stage 8 (Integrity Verification) where the CDO verifies IDS specifications are realized in SwiftUI implementation.

## Competency Dimensions

| Dimension                | Description                                                                                                     | Proficiency Indicators                                                                                                                    |
| ------------------------ | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Declarative UI           | View protocol, body composition, view identity, view lifecycle, environment propagation                         | Views are pure functions of state; composition over inheritance; environment used for dependency injection                                |
| State Management         | @State, @StateObject, @ObservedObject, @EnvironmentObject, @Binding, @Environment                               | Correct property wrapper selection per ownership model; no ObservableObject passed as value; binding used for two-way data flow           |
| Custom Transitions       | AnyTransition, matchedGeometryEffect, phase animator, custom transition definitions, gesture-driven transitions | Transitions are smooth and interruptible; matchedGeometryEffect for shared element transitions; custom transitions for complex animations |
| View Modifiers           | Custom modifier protocol, modifier composition, conditional modifiers, view preference system                   | Modifiers are reusable and composable; conditional modifiers use `@ViewBuilder`; preferences used for child-to-parent communication       |
| Performance Optimization | Identifiable, view diffing, lazy stacks, Equatable views, drawing group, transaction control                    | Lists use Identifiable correctly; LazyVStack/LazyHStack for large collections; drawingGroup for complex static views                      |

## Execution Guidance

### State Management — Property Wrapper Selection

**Ownership model decision tree:**

```
┌──────────────────────────────────────────────────────┐
│ Who owns the data?                                    │
├──────────────────────────────────────────────────────┤
│ This view creates & owns it → @State                  │
│ This view creates & it has reference semantics        │
│   (class) → @StateObject                              │
│ Another view creates it, this view observes →         │
│   @ObservedObject (value passed in)                   │
│ Global/app-level data → @EnvironmentObject            │
│ Two-way binding to parent's state → @Binding          │
│ Read system/app config → @Environment                 │
└──────────────────────────────────────────────────────┘
```

```swift
// MARK: - ViewModel with @StateObject

@MainActor
final class UserDetailViewModel: ObservableObject {
    @Published var user: User?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?

    private let userRepository: UserRepositoryProtocol

    init(userRepository: UserRepositoryProtocol) {
        self.userRepository = userRepository
    }

    func loadUser(id: UUID) async {
        isLoading = true
        do {
            user = try await userRepository.fetchUser(id: id)
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}

// MARK: - View with @StateObject

struct UserDetailView: View {
    let userId: UUID

    // @StateObject — this view owns the ViewModel lifecycle
    @StateObject private var viewModel: UserDetailViewModel

    // Dependency injection via initializer
    init(userId: UUID, userRepository: UserRepositoryProtocol) {
        self.userId = userId
        _viewModel = StateObject(
            wrappedValue: UserDetailViewModel(userRepository: userRepository)
        )
    }

    var body: some View {
        Group {
            switch viewModel.loadState {
            case .loading:
                ProgressView()
            case .loaded(let user):
                UserContent(user: user)
            case .error(let message):
                ErrorView(message: message)
            }
        }
        .task {
            await viewModel.loadUser(id: userId)
        }
    }
}

// MARK: - @Binding for two-way data flow

struct EditableField: View {
    @Binding var text: String
    let placeholder: String
    let label: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(label)
                .font(.caption)
                .foregroundStyle(.secondary)

            TextField(placeholder, text: $text)
                .textFieldStyle(.roundedBorder)
        }
    }
}

// Usage
struct EditProfileView: View {
    @State private var displayName: String = ""
    @State private var bio: String = ""

    var body: some View {
        Form {
            EditableField(
                text: $displayName,
                placeholder: "Your name",
                label: "Display Name"
            )
            EditableField(
                text: $bio,
                placeholder: "Tell us about yourself",
                label: "Bio"
            )
        }
    }
}

// MARK: - @Environment for global config

struct ThemeAwareView: View {
    @Environment(\.colorScheme) var colorScheme
    @Environment(\.locale) var locale
    @Environment(\.dismiss) var dismiss

    var body: some View {
        VStack {
            Text(colorScheme == .dark ? "Dark Mode" : "Light Mode")
            Button("Dismiss") {
                dismiss()
            }
        }
    }
}

// MARK: - Custom Environment Key

private struct APIBaseURLKey: EnvironmentKey {
    static let defaultValue: URL = URL(string: "https://api.example.com")!
}

extension EnvironmentValues {
    var apiBaseURL: URL {
        get { self[APIBaseURLKey.self] }
        set { self[APIBaseURLKey.self] = newValue }
    }
}

// Usage
struct ContentView: View {
    @Environment(\.apiBaseURL) var apiBaseURL

    var body: some View {
        Text("API: \(apiBaseURL.absoluteString)")
    }
}
```

### Custom Transitions

```swift
// MARK: - Custom Transition Definition

extension AnyTransition {
    /// Slide in from leading edge with fade
    static var slideInLeading: AnyTransition {
        .asymmetric(
            insertion: .move(edge: .leading).combined(with: .opacity),
            removal: .move(edge: .trailing).combined(with: .opacity)
        )
    }

    /// Scale in from center with fade
    static var scaleIn: AnyTransition {
        .asymmetric(
            insertion: .scale(scale: 0.8).combined(with: .opacity),
            removal: .scale(scale: 1.2).combined(with: .opacity)
        )
    }

    /// Push transition like navigation stack
    static var push: AnyTransition {
        .asymmetric(
            insertion: .move(edge: .trailing),
            removal: .move(edge: .leading)
        )
    }
}

// MARK: - Matched Geometry Effect (Shared Element Transition)

struct MatchedGeometryListView: View {
    @Namespace private var animation
    @State private var selectedCard: Card?

    var body: some View {
        ZStack {
            if selectedCard == nil {
                cardGrid
            } else {
                cardDetail(card: selectedCard!)
                    .matchedGeometryEffect(
                        id: selectedCard!.id,
                        in: animation
                    )
            }
        }
        .animation(.spring(response: 0.4, dampingFraction: 0.8), value: selectedCard)
    }

    private var cardGrid: some View {
        ScrollView {
            LazyVGrid(columns: [GridItem(.adaptive(minimum: 150))]) {
                ForEach(cards) { card in
                    CardThumbnail(card: card)
                        .matchedGeometryEffect(id: card.id, in: animation)
                        .onTapGesture {
                            withAnimation {
                                selectedCard = card
                            }
                        }
                }
            }
        }
    }

    private func cardDetail(card: Card) -> some View {
        VStack {
            CardImage(image: card.image)
                .matchedGeometryEffect(id: card.id, in: animation)
            Text(card.title)
                .font(.title)
            Text(card.description)
                .font(.body)
                .foregroundStyle(.secondary)
        }
        .onTapGesture {
            withAnimation {
                selectedCard = nil
            }
        }
    }
}

// MARK: - Phase Animator (iOS 17+)

struct PhaseAnimationExample: View {
    @State private var isFavorite = false

    var body: some View {
        PhaseAnimator([false, true], trigger: isFavorite) { phase in
            Image(systemName: isFavorite ? "heart.fill" : "heart")
                .font(.system(size: 48))
                .foregroundStyle(phase ? .red : .gray)
                .scaleEffect(phase ? 1.3 : 1.0)
        } animation: { phase in
            .spring(response: 0.3, dampingFraction: 0.6)
        }
        .onTapGesture {
            isFavorite.toggle()
        }
    }
}
```

### Custom View Modifiers

```swift
// MARK: - ViewModifier Protocol

struct CardStyleModifier: ViewModifier {
    var elevation: CGFloat = 2

    func body(content: Content) -> some View {
        content
            .padding(16)
            .background {
                RoundedRectangle(cornerRadius: 12)
                    .fill(.background)
                    .shadow(color: .black.opacity(0.1), radius: elevation, x: 0, y: elevation)
            }
    }
}

extension View {
    func cardStyle(elevation: CGFloat = 2) -> some View {
        modifier(CardStyleModifier(elevation: elevation))
    }
}

// Usage
Text("Hello, World")
    .cardStyle()

// MARK: - Conditional Modifiers

extension View {
    @ViewBuilder
    func `if`<Content: View>(_ condition: Bool, transform: (Self) -> Content) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }
}

// Usage
Text("Important")
    .if(isUrgent) { $0.foregroundStyle(.red).fontWeight(.bold) }

// MARK: - View Preferences (Child-to-Parent Communication)

struct SizePreferenceKey: PreferenceKey {
    static var defaultValue: CGSize = .zero
    static func reduce(value: inout CGSize, nextValue: () -> CGSize) {
        value = nextValue()
    }
}

extension View {
    func readSize(onChange: @escaping (CGSize) -> Void) -> some View {
        background {
            GeometryReader { geometry in
                Color.clear
                    .preference(key: SizePreferenceKey.self, value: geometry.size)
            }
        }
        .onPreferenceChange(SizePreferenceKey.self, perform: onChange)
    }
}

// Usage
struct ParentView: View {
    @State private var childSize: CGSize = .zero

    var body: some View {
        VStack {
            Text("Child size: \(childSize.width)x\(childSize.height)")

            ChildView()
                .readSize { size in
                    childSize = size
                }
        }
    }
}
```

### Performance Optimization

```swift
// MARK: - Identifiable for List Performance

struct User: Identifiable, Equatable {
    let id: UUID
    let name: String
    let email: String

    // Equatable conformance for efficient diffing
    static func == (lhs: User, rhs: User) -> Bool {
        lhs.id == rhs.id &&
        lhs.name == rhs.name &&
        lhs.email == rhs.email
    }
}

// MARK: - Lazy Stacks for Large Collections

struct LargeListView: View {
    let items: [Item]  // Could be thousands

    var body: some View {
        ScrollView {
            // ✅ Lazy — only renders visible items
            LazyVStack(spacing: 8) {
                ForEach(items) { item in
                    ItemRow(item: item)
                }
            }
        }
    }
}

// MARK: - Drawing Group for Complex Static Views

struct ComplexStaticView: View {
    var body: some View {
        VStack {
            // Complex view with many subviews
            ForEach(0..<50) { i in
                Text("Item \(i)")
            }
        }
        // ✅ Renders as single bitmap — reduces render tree complexity
        .drawingGroup()
    }
}

// MARK: - Equatable View for Reduced Recomputation

struct ExpensiveView: View, Equatable {
    let data: ComplexData

    var body: some View {
        // Expensive computation
        ForEach(data.items) { item in
            ComplexItemView(item: item)
        }
    }

    // Only recompute when data changes
    static func == (lhs: ExpensiveView, rhs: ExpensiveView) -> Bool {
        lhs.data.id == rhs.data.id
    }
}

// MARK: - Transaction Control for Animation Performance

struct OptimizedAnimation: View {
    @State private var offset: CGFloat = 0

    var body: some View {
        Circle()
            .fill(.blue)
            .frame(width: 50, height: 50)
            .offset(y: offset)
            .transaction { transaction in
                // Disable animation for this specific change
                transaction.animation = .none
            }
            .onAppear {
                withAnimation(.spring()) {
                    offset = 200
                }
            }
    }
}
```

## Pipeline Integration

- **Stage 2 (Design):** IDS specifies visual design, interaction patterns, and transition behaviors for SwiftUI implementation.
- **Stage 3 (Architecture):** ADR establishes SwiftUI as the UI framework for new screens. UML component diagrams define view hierarchy.
- **Stage 5 (Development):** Primary skill for iOS UI development. All new screens built as SwiftUI views with proper state management.
- **Stage 6 (Code Review):** SwiftUI review: property wrapper correctness, view composition efficiency, transition performance, modifier reusability.
- **Stage 8 (Integrity Verification):** CDO verifies all IDS visual and interaction specifications are realized in SwiftUI.

## Quality Standards

- **100%** correct property wrapper selection per ownership model — no `@ObservedObject` for owned state
- **Zero** `ObservableObject` passed as value type — always wrapped with `@StateObject` or `@ObservedObject`
- All `List` and `ForEach` use **Identifiable** types — no `id: \.self` unless type is truly hashable
- **LazyVStack/LazyHStack** used for collections **>20 items** — no eager rendering of large collections
- Custom transitions defined as **`AnyTransition` extensions** — not inline in view body
- Matched geometry effect used for **shared element transitions** — not manual animation coordination
- Custom modifiers conform to **`ViewModifier` protocol** — not chained modifier functions
- View preferences used for **child-to-parent communication** — not closure callbacks for layout data
- `@Environment` used for **system-level and app-level config** — not for view-specific data
- All SwiftUI views are **pure functions of state** — no side effects in body computation
- Drawing group applied to **complex static views** with many subviews (>20)
