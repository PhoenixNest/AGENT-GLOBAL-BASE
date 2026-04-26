# Migration Strategies: UIKit to SwiftUI

## Migration Strategies: UIKit to SwiftUI

### Incremental Adoption via UIHostingController

Embed SwiftUI views inside existing UIKit navigation stacks.

```swift
// Push a SwiftUI view from a UIKit navigation controller
func navigateToSwiftUIFeature() {
    let swiftUIView = NewFeatureView(viewModel: viewModel)
    let hostingVC = UIHostingController(rootView: swiftUIView)
    hostingVC.navigationItem.title = "New Feature"
    navigationController?.pushViewController(hostingVC, animated: true)
}
```

### Presenting UIKit from SwiftUI

```swift
struct LegacyFeatureView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> LegacyFeatureViewController {
        let vc = LegacyFeatureViewController()
        vc.delegate = context.coordinator
        return vc
    }

    func updateUIViewController(_ uiViewController: LegacyFeatureViewController, context: Context) {
        // Sync state changes from SwiftUI down to UIKit
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, LegacyFeatureViewControllerDelegate {
        // Bridge UIKit delegate events to SwiftUI @Binding / @State
    }
}
```

### Migration Checklist

1. Identify a self-contained feature with minimal UIKit dependencies
2. Build the SwiftUI replacement in parallel
3. Use `UIHostingController` to embed the SwiftUI view in the existing UIKit flow
4. Validate parity via Stage 8 Integrity Verification
5. Remove the UIKit implementation after full validation

---
