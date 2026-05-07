---
name: uikit-architecture
description: Architect and maintain UIKit-based iOS applications — applying MVVM-C (Coordinator pattern), programmatic Auto Layout, and UIKit lifecycle expertise — for maintaining and migrating the legacy UIKit codebase alongside SwiftUI development.
version: "1.0.0"
---

# Uikit Architecture

| Competency           | Description                                                         | Quality Criteria                                                                                                     |
| -------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| MVVM-C Pattern       | Implement Model-View-ViewModel-Coordinator architecture in UIKit    | Coordinators own navigation; ViewModels have no UIKit imports; ViewControllers are thin binding layers               |
| Programmatic Layout  | Build UIKit layouts in code without Interface Builder               | No XIB/NIB files; constraints activated in `setupConstraints()`; no magic number constraints — uses layout constants |
| UIKit Lifecycle      | Handle UIViewController lifecycle correctly for resource management | Resources acquired in `viewDidLoad`; deallocated in `deinit`; no view manipulation before `viewDidLoad` completes    |
| UIKit-SwiftUI Bridge | Integrate SwiftUI views into UIKit using UIHostingController        | `UIHostingController` correctly embedded; SwiftUI state bridged via `@ObservedObject`; memory managed correctly      |

## Execution Guidance

### Coordinator Pattern

```swift
protocol Coordinator: AnyObject {
    var childCoordinators: [Coordinator] { get set }
    var navigationController: UINavigationController { get }
    func start()
}

class AppCoordinator: Coordinator {
    var childCoordinators: [Coordinator] = []
    var navigationController: UINavigationController

    func start() {
        let productListVC = ProductListViewController()
        productListVC.delegate = self
        navigationController.pushViewController(productListVC, animated: false)
    }
}
```

### UIKit-SwiftUI Migration Strategy

For gradual migration from UIKit to SwiftUI:

| Approach                                   | When to Use                                               |
| ------------------------------------------ | --------------------------------------------------------- |
| New screens in SwiftUI                     | All new features after the migration ADR is ratified      |
| SwiftUI inside UIKit (UIHostingController) | Isolated new components within existing flows             |
| UIKit inside SwiftUI (UIViewRepresentable) | Components without SwiftUI equivalent yet                 |
| Full screen replacement                    | When the screen is refactored anyway (bug fix / redesign) |

Do not rewrite UIKit screens solely for migration — rewrite only when there is a functional justification.
