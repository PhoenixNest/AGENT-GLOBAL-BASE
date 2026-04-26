# Data Binding Patterns

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
