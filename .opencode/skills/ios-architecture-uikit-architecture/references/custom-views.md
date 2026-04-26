# Custom Views

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
