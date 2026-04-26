# Testing UIKit Components

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
