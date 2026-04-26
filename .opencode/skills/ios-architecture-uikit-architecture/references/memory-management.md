# Memory Management

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
