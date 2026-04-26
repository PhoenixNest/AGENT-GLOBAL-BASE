---
name: ios-architecture-uikit-architecture
description: "UIKit architecture patterns for iOS apps — view controller lifecycle, Auto Layout, navigation architecture, custom views, delegation, memory management, and incremental SwiftUI migration via UIHostingController. Owned by Seo-Yeon Park (iOS Lead). Use during Stage 5 (Development) for UIKit-based screens and legacy feature maintenance. Trigger: uikit, viewcontroller lifecycle, autolayout, uinavigationcontroller, uitabbarcontroller, custom uiview, delegation, uihostingcontroller, deep linking."
prerequisites:
  - ios-infrastructure-ios-implementation

version: "1.0.0"
---

# UIKit Architecture Patterns

## Overview

UIKit remains the foundational UI framework for iOS development. While SwiftUI is the declared future direction, a substantial portion of the production codebase — including legacy features, third-party integrations, and platform-specific behaviours — continues to rely on UIKit. This guideline covers architecture patterns for maintaining and extending UIKit-based components within the iOS platform codebase.

**Scope of this guideline:**

- View controller lifecycle management and common pitfalls
- Navigation architecture (UINavigationController, UITabBarController, deep linking)
- Auto Layout and constraint-based layout systems
- Custom view development (subclassing, drawing, intrinsic content size)
- Data binding patterns (target-action, delegation, KVO)
- Memory management and leak detection in UIKit contexts
- Testing strategies for UIKit components
- Incremental migration to SwiftUI via UIHostingController

**When to use UIKit vs. SwiftUI (Stage 5 guidance):**

| Scenario                                                   | Recommended Framework       |
| ---------------------------------------------------------- | --------------------------- |
| New feature on iOS 17+                                     | SwiftUI                     |
| Legacy feature maintenance                                 | UIKit                       |
| Complex custom drawing                                     | UIKit (Core Graphics)       |
| Deep system integration (e.g., custom keyboard extensions) | UIKit                       |
| Incremental migration                                      | UIKit + UIHostingController |

---

## View Controller Lifecycle

### Lifecycle Timing Diagram

```
loadView()
    │
    ▼
viewDidLoad() ────────────── Called once after view hierarchy is loaded
    │
    ▼
viewWillAppear(_:) ───────── Called every time before view becomes visible
    │
    ▼
viewWillLayoutSubviews() ─── Called before Auto Layout runs
    │
    ▼
viewDidLayoutSubviews() ──── Called after Auto Layout completes
    │
    ▼
viewDidAppear(_:) ────────── Called after view is on screen
    │
    ▼
... (user interaction) ...
    │
    ▼
viewWillDisappear(_:) ────── Called before view is removed/covered
    │
    ▼
viewDidDisappear(_:) ─────── Called after view is removed/covered
```

### Common Pitfalls

1. **Performing layout in `viewDidLoad`**: Frame-based calculations in `viewDidLoad` use incorrect sizes because Auto Layout has not yet run. Move layout-dependent code to `viewDidLayoutSubviews`.

2. **One-time setup in `viewWillAppear`**: `viewWillAppear` fires on every presentation. Network calls or expensive setup here cause redundant work.

3. **Ignoring `viewDidLayoutSubviews` call frequency**: This method may be called many times per presentation. Do not place expensive operations here without guards.

```swift
class ProfileViewController: UIViewController {
    private var hasPerformedInitialLayout = false

    override func viewDidLoad() {
        super.viewDidLoad()
        // One-time setup: configure subviews, set up delegates
        setupConstraints()
        viewModel.viewDidLoad()
    }

    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        guard !hasPerformedInitialLayout else { return }
        hasPerformedInitialLayout = true
        // Safe to read final frame sizes here
        adjustHeaderViewHeight()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // Re-occurring setup: refresh data, update UI state
        viewModel.refresh()
    }
}
```

---

## Navigation Patterns

### UINavigationController Architecture

```
┌──────────────────────────────────────┐
│         UINavigationController       │
│  ┌────────────────────────────────┐  │
│  │         UINavigationBar        │  │
│  ├────────────────────────────────┤  │
│  │                                │  │
│  │      RootViewController        │  │
│  │                                │  │
│  ├────────────────────────────────┤  │
│  │         DetailViewController   │  │  ← pushed onto stack
│  ├────────────────────────────────┤  │
│  │       SettingsViewController   │  │  ← pushed onto stack
│  │                                │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │           UIToolbar            │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

### Recommended Navigation Pattern

```swift
// AppCoordinator.swift — Centralised navigation orchestration
final class AppCoordinator {
    private let navigationController: UINavigationController

    init(window: UIWindow) {
        navigationController = UINavigationController()
        window.rootViewController = navigationController
    }

    func start() {
        let rootVC = HomeViewController()
        rootVC.delegate = self
        navigationController.setViewControllers([rootVC], animated: false)
    }
}

extension AppCoordinator: HomeViewControllerDelegate {
    func didSelectProfile() {
        let profileVC = ProfileViewController()
        navigationController.pushViewController(profileVC, animated: true)
    }

    func didRequestSettings() {
        let settingsVC = SettingsViewController()
        let navVC = UINavigationController(rootViewController: settingsVC)
        navVC.modalPresentationStyle = .formSheet
        navigationController.present(navVC, animated: true)
    }
}
```

### UITabBarController with Embedded Navigation

```swift
func configureTabBarController() -> UITabBarController {
    let tabBarController = UITabBarController()

    let homeNav = UINavigationController(rootViewController: HomeViewController())
    homeNav.tabBarItem = UITabBarItem(title: "Home", image: .home, tag: 0)

    let searchNav = UINavigationController(rootViewController: SearchViewController())
    searchNav.tabBarItem = UITabBarItem(title: "Search", image: .search, tag: 1)

    let profileNav = UINavigationController(rootViewController: ProfileViewController())
    profileNav.tabBarItem = UITabBarItem(title: "Profile", image: .profile, tag: 2)

    tabBarController.viewControllers = [homeNav, searchNav, profileNav]
    return tabBarController
}
```

### Deep Link Handling

```swift
// AppDelegate or SceneDelegate
func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
    guard let url = URLContexts.first?.url else { return }
    DeepLinkRouter.navigate(to: url, from: window?.rootViewController)
}

enum DeepLinkRouter {
    static func navigate(to url: URL, from rootVC: UIViewController?) {
        let path = url.pathComponents.dropFirst() // remove leading "/"
        guard let rootVC = rootVC else { return }

        switch path.first {
        case "product":
            guard let id = path.dropFirst().first else { return }
            navigateToProduct(id, from: rootVC)
        case "settings":
            navigateToSettings(from: rootVC)
        default:
            break
        }
    }

    private static func navigateToProduct(_ id: String, from rootVC: UIViewController) {
        if let tabVC = rootVC as? UITabBarController,
           let nav = tabVC.selectedViewController as? UINavigationController {
            let detailVC = ProductDetailViewController(productId: id)
            nav.pushViewController(detailVC, animated: true)
        }
    }
}
```

---

## Stage 5 Integration

During Stage 5 (Development), UIKit components are maintained within the `platforms/ios/code/` directory. The iOS Lead (Seo-Yeon Park) ensures:

- All new view controllers follow the lifecycle patterns documented above
- Auto Layout constraints have no conflicts or ambiguities at any supported Dynamic Type size
- Delegates are declared `weak` to prevent retain cycles
- Custom views expose `intrinsicContentSize` where applicable
- Migration to SwiftUI is tracked via feature flags, enabling parallel development

---

## References

- Apple Documentation: [UIViewController Lifecycle](https://developer.apple.com/documentation/uikit/uiviewcontroller)
- Apple Documentation: [Auto Layout Guide](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/AutolayoutPG/)
- Apple Documentation: [UIHostingController](https://developer.apple.com/documentation/swiftui/uihostingcontroller)
- WWDC 2019: "UIKit: Getting Started with Modern UIKit"
- WWDC 2021: "Demystify Auto Layout performance"
- OWASP MASVS: Platform-level security for UI components (input validation, secure drawing)

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`auto-layout-&-constraints.md`](references/auto-layout-&-constraints.md) — Auto Layout & Constraints
- [`custom-views.md`](references/custom-views.md) — Custom Views
- [`data-binding-patterns.md`](references/data-binding-patterns.md) — Data Binding Patterns
- [`memory-management.md`](references/memory-management.md) — Memory Management
- [`testing-uikit-components.md`](references/testing-uikit-components.md) — Testing UIKit Components
- [`migration-strategies-uikit-to-swiftui.md`](references/migration-strategies-uikit-to-swiftui.md) — Migration Strategies: UIKit to SwiftUI
