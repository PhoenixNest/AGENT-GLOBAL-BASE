# Auto Layout & Constraints

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
