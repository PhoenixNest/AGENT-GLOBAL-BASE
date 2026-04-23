---
name: ios-architecture-uikit-architecture
description: 'Ios skill: Uikit Architecture'
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

## Auto Layout & Constraints

### Constraint Priorities

| Priority     | Value | Use Case                                                    |
| ------------ | ----- | ----------------------------------------------------------- |
| Required     | 1000  | Must never break (intrinsic content size, critical spacing) |
| Default High | 750   | Hug content but allow Dynamic Type expansion                |
| Default Low  | 250   | Optional spacing, compressible margins                      |
| Fitting Size | 50    | `systemLayoutSizeFittingSize` calculations                  |

### Safe Constraint Pattern

```swift
final class ProductCardView: UIView {

    private let imageView = UIImageView()
    private let titleLabel = UILabel()
    private let priceLabel = UILabel()

    override init(frame: CGRect) {
        super.init(frame: frame)
        configureViews()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func configureViews() {
        [imageView, titleLabel, priceLabel].forEach {
            $0.translatesAutoresizingMaskIntoConstraints = false
            addSubview($0)
        }

        NSLayoutConstraint.activate([
            // Image pinned to top and sides
            imageView.topAnchor.constraint(equalTo: topAnchor),
            imageView.leadingAnchor.constraint(equalTo: leadingAnchor),
            imageView.trailingAnchor.constraint(equalTo: trailingAnchor),
            imageView.heightAnchor.constraint(equalTo: widthAnchor, multiplier: 0.75),

            // Title hugs content, can expand for Dynamic Type
            titleLabel.topAnchor.constraint(equalTo: imageView.bottomAnchor, constant: 8),
            titleLabel.leadingAnchor.constraint(equalTo: leadingAnchor, constant: 12),
            titleLabel.trailingAnchor.constraint(equalTo: trailingAnchor, constant: -12),

            // Price stays below title
            priceLabel.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 4),
            priceLabel.leadingAnchor.constraint(equalTo: leadingAnchor, constant: 12),
            priceLabel.trailingAnchor.constraint(equalTo: trailingAnchor, constant: -12),
            priceLabel.bottomAnchor.constraint(equalTo: bottomAnchor, constant: -12)
        ])

        titleLabel.setContentHuggingPriority(.defaultHigh, for: .vertical)
        titleLabel.setContentCompressionResistancePriority(.required, for: .vertical)
    }
}
```

### Dynamic Type Support

```swift
// Subscribe to Dynamic Type changes
override func traitCollectionDidChange(_ previousTraitCollection: UITraitCollection?) {
    super.traitCollectionDidChange(previousTraitCollection)

    guard traitCollection.hasDifferentColorAppearance(comparedTo: previousTraitCollection) ||
          traitCollection.preferredContentSizeCategory != previousTraitCollection?.preferredContentSizeCategory
    else { return }

    updateFonts()
    invalidateIntrinsicContentSize()
}

private func updateFonts() {
    titleLabel.font = UIFont.preferredFont(forTextStyle: .headline)
    priceLabel.font = UIFont.preferredFont(forTextStyle: .body)
    titleLabel.adjustsFontForContentSizeCategory = true
    priceLabel.adjustsFontForContentSizeCategory = true
}
```

### RTL Layout Support

Use `leadingAnchor` / `trailingAnchor` instead of `leftAnchor` / `rightAnchor`. UIKit automatically flips layout direction for right-to-left languages.

```swift
// Correct — auto-flips for RTL
label.leadingAnchor.constraint(equalTo: containerView.leadingAnchor, constant: 16)

// Incorrect — always LTR
label.leftAnchor.constraint(equalTo: containerView.leftAnchor, constant: 16)
```

---

## Custom Views

### Subclassing Guidelines

1. **Override `init(frame:)` and `init?(coder:)`**: Always provide both initialisers. Use a shared `configure()` method.
2. **Set `translatesAutoresizingMaskIntoConstraints = false`** on subviews — never on `self`.
3. **Provide `intrinsicContentSize`** when the view defines its own size (e.g., badges, chips).
4. **Override `layoutSubviews`** for manual frame adjustments that Auto Layout cannot express.

```swift
class BadgeView: UIView {

    var text: String = "" {
        didSet {
            label.text = text
            invalidateIntrinsicContentSize()
            setNeedsLayout()
        }
    }

    private let label = UILabel()

    override init(frame: CGRect) {
        super.init(frame: frame)
        configure()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        configure()
    }

    private func configure() {
        backgroundColor = .systemBlue
        layer.cornerRadius = 8
        layer.masksToBounds = true

        label.translatesAutoresizingMaskIntoConstraints = false
        label.textColor = .white
        label.font = .systemFont(ofSize: 12, weight: .semibold)
        label.textAlignment = .center
        addSubview(label)

        NSLayoutConstraint.activate([
            label.centerXAnchor.constraint(equalTo: centerXAnchor),
            label.centerYAnchor.constraint(equalTo: centerYAnchor),
            label.leadingAnchor.constraint(greaterThanOrEqualTo: leadingAnchor, constant: 6),
            label.trailingAnchor.constraint(lessThanOrEqualTo: trailingAnchor, constant: -6)
        ])
    }

    override var intrinsicContentSize: CGSize {
        let labelSize = label.sizeThatFits(CGSize(width: .greatestFiniteMagnitude, height: .greatestFiniteMagnitude))
        return CGSize(width: labelSize.width + 16, height: labelSize.height + 8)
    }
}
```

### When to Use `draw(_ rect:)`

Override `draw(_:)` only when Core Graphics drawing is required (custom shapes, charts, progress rings). For composed layouts, prefer Auto Layout with subviews.

```swift
class CircularProgressView: UIView {
    var progress: CGFloat = 0.0 { didSet { setNeedsDisplay() } }

    override func draw(_ rect: CGRect) {
        guard let context = UIGraphicsGetCurrentContext() else { return }

        let center = CGPoint(x: bounds.midX, y: bounds.midY)
        let radius = min(bounds.width, bounds.height) / 2 - lineWidth / 2

        // Background ring
        let backgroundPath = UIBezierPath(
            arcCenter: center, radius: radius,
            startAngle: -.pi / 2, endAngle: .pi * 1.5, clockwise: true
        )
        context.setStrokeColor(UIColor.systemGray4.cgColor)
        context.setLineWidth(lineWidth)
        backgroundPath.stroke()

        // Progress arc
        let endAngle = -.pi / 2 + (.pi * 2 * progress)
        let progressPath = UIBezierPath(
            arcCenter: center, radius: radius,
            startAngle: -.pi / 2, endAngle: endAngle, clockwise: true
        )
        context.setStrokeColor(UIColor.systemBlue.cgColor)
        context.setLineWidth(lineWidth)
        context.setLineCap(.round)
        progressPath.stroke()
    }
}
```

---

## Data Binding Patterns

### Target-Action

```swift
button.addTarget(self, action: #selector(didTapButton), for: .touchUpInside)

@objc private func didTapButton() {
    viewModel.onButtonTapped()
}
```

### Delegation (Preferred for loose coupling)

```swift
protocol SettingsViewControllerDelegate: AnyObject {
    func settingsViewController(_ vc: SettingsViewController, didChangeTheme theme: Theme)
}

class SettingsViewController: UIViewController {
    weak var delegate: SettingsViewControllerDelegate?

    private func applyTheme(_ theme: Theme) {
        delegate?.settingsViewController(self, didChangeTheme: theme)
    }
}
```

### Key-Value Observing (Limited Use)

Use KVO only when observing system properties that lack closure-based alternatives.

```swift
private var observation: NSKeyValueObservation?

override func viewDidLoad() {
    super.viewDidLoad()
    observation = viewModel.observe(\.isLoading, options: [.new]) { [weak self] _, change in
        guard let newValue = change.newValue else { return }
        DispatchQueue.main.async {
            self?.activityIndicator.isHidden = !newValue
        }
    }
}

deinit {
    observation?.invalidate()
}
```

---

## Memory Management

### Strong / Weak / Unowned Guidelines

| Relationship                   | Modifier                                        | When to Use                                                     |
| ------------------------------ | ----------------------------------------------- | --------------------------------------------------------------- |
| Parent → child view/controller | `strong`                                        | Ownership is intended; lifecycle is tied to parent              |
| Child → parent (delegate)      | `weak`                                          | Prevent retain cycles; delegate should not own parent           |
| Closure capturing `self`       | `[weak self]`                                   | Self may be deallocated before closure fires                    |
| Closure capturing `self`       | `[unowned self]`                                | Self is guaranteed to exist for closure lifetime (rare, unsafe) |
| IBOutlet properties            | `weak` (top-level views) or `strong` (subviews) | Top-level nib views are already retained by the view hierarchy  |

### Common Leak Patterns

```swift
// LEAK: strong reference cycle through closure
class MyViewController: UIViewController {
    var onComplete: (() -> Void)?

    func setup() {
        onComplete = {
            self.dismiss(animated: true)  // captures `self` strongly
        }
    }
}

// FIXED: weak self in closure
class MyViewController: UIViewController {
    var onComplete: (() -> Void)?

    func setup() {
        onComplete = { [weak self] in
            self?.dismiss(animated: true)
        }
    }
}
```

### Leak Detection (Instruments)

1. Open Xcode → Product → Profile → Leaks
2. Run the suspect flow (present and dismiss the view controller)
3. Check the "Cycles & Roots" instrument for retain cycles
4. Look for `UIViewController` instances that survive dismissal

```swift
// Debug helper: log deallocation
deinit {
    #if DEBUG
    print("\(type(of: self)) deallocated")
    #endif
}
```

---

## Testing UIKit Components

### View Controller Testing

```swift
import XCTest
@testable import MyApp

final class ProfileViewControllerTests: XCTestCase {

    func test_viewDidLoad_configuresTitle() {
        let vc = ProfileViewController()
        _ = vc.view // Triggers viewDidLoad

        XCTAssertEqual(vc.navigationItem.title, "Profile")
    }

    func test_viewWillAppear_refreshesViewModel() {
        let mockViewModel = MockProfileViewModel()
        let vc = ProfileViewController(viewModel: mockViewModel)
        _ = vc.view

        vc.beginAppearanceTransition(true, animated: false)
        vc.endAppearanceTransition()

        XCTAssertTrue(mockViewModel.refreshCalled)
    }
}
```

### Constraint Conflict Testing

```swift
func test_constraints_noAmbiguity() {
    let view = ProductCardView()
    view.frame = CGRect(x: 0, y: 0, width: 375, height: 200)
    _ = view.viewIfLoaded

    let constraints = view.constraintsAffectingLayout(for: .horizontal)
    XCTAssertTrue(constraints.allSatisfy { !$0.isActive == false })

    // Force layout and check for conflicts
    view.setNeedsLayout()
    view.layoutIfNeeded()
    XCTAssertFalse(view.hasAmbiguousLayout, "ProductCardView has ambiguous layout")
}
```

---

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
