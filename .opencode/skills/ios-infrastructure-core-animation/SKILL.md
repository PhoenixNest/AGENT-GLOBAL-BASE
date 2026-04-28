---
name: ios-infrastructure-core-animation
description: "Core Animation for iOS — CALayer manipulation, keyframe animations, spring dynamics, rendering pipeline optimization, offscreen rendering elimination, and Instruments profiling. Owned by Seo-Yeon Park (iOS Lead). Use during Stage 5 (Development) for custom animations and Stage 8 (Integrity Verification) for IDS animation spec validation. Trigger: core animation, calayer, cabasicanimation, cakeyframeanimation, caspringanimation, catransaction, offscreen rendering, shadowpath, rasterization, instruments, 60fps."
prerequisites:
  - ios-ui-ux-swiftui

version: "1.0.0"
---

# Core Animation

**Category:** Mobile Engineering — iOS Animation & Rendering
**Owner:** Senior iOS Engineer (Mei Chen)

## Overview

This skill implements production-grade iOS animations using Core Animation covering CALayer manipulation, animation timing, the rendering pipeline, and performance optimization. It applies to Stage 5 (Development) where custom animations and visual effects are implemented, Stage 6 (Code Review) where animation performance and memory impact are audited, and Stage 8 (Integrity Verification) where the CDO verifies IDS animation specifications are realized.

## Competency Dimensions

| Dimension                | Description                                                                                          | Proficiency Indicators                                                                                                                 |
| ------------------------ | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| CALayer Architecture     | Layer tree vs presentation tree vs render tree, implicit vs explicit animations, layer properties    | Understands three-tree model; uses explicit animations for production; manipulates layer properties directly for performance           |
| Animation Timing         | CAMediaTiming, timing functions, keyframe animations, group animations, spring dynamics              | Animations use appropriate timing functions; keyframe animations have smooth easing; spring animations use physically-based parameters |
| Rendering Pipeline       | GPU-accelerated properties, rasterization, shouldRasterize, drawsAsynchronously, offscreen rendering | Identifies and eliminates offscreen rendering; uses rasterization strategically; animation runs at 60fps consistently                  |
| Performance Optimization | Instruments Time Profiler, Core Animation instrument, GPU Frame Capture, red/green/blue overlay      | Zero offscreen rendering passes for animated layers; animation CPU impact <5%; no dropped frames during animation                      |
| View-Layer Integration   | UIView animation vs Core Animation, layer-backed views, custom layer drawing, CATransaction          | Chooses UIView animation for simple cases, Core Animation for complex; uses CATransaction for coordinated animations                   |

## Execution Guidance

### CALayer — Three-Tree Model

**Understanding the rendering architecture:**

```
Model Layer Tree     ← What you set (immediate, no animation)
    ↓
Presentation Tree    ← What's currently displayed (animated values)
    ↓
Render Tree          ← What Core Animation sends to GPU (private)
```

```swift
// When you set a property, the model tree updates immediately
// but the presentation tree animates to the new value
layer.position = CGPoint(x: 200, y: 200)

// Model tree: position = (200, 200) — immediate
// Presentation tree: position = animating from old to (200, 200)

// To get the current animated value:
let currentPosition = layer.presentation()?.position

// To remove all animations and snap to model value:
layer.removeAllAnimations()
```

**Implicit vs Explicit Animations:**

```swift
// IMPLICIT animation — automatic for animatable layer properties
// Triggered by changing a property on a layer that's already in the hierarchy
layer.opacity = 0.5  // Automatically animates over 0.25s

// Disable implicit animations when you don't want them
CATransaction.begin()
CATransaction.setDisableActions(true)
layer.opacity = 0.5
CATransaction.commit()

// EXPLICIT animation — full control over animation parameters
let animation = CABasicAnimation(keyPath: "opacity")
animation.fromValue = 1.0
animation.toValue = 0.5
animation.duration = 0.5
animation.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
animation.fillMode = .forwards
animation.isRemovedOnCompletion = false
layer.add(animation, forKey: "fade")
```

### Keyframe Animations — Production Patterns

```swift
// Complex path animation with keyframes
func animateAlongPath(layer: CALayer, path: CGPath) {
    let animation = CAKeyframeAnimation(keyPath: "position")
    animation.path = path
    animation.duration = 2.0
    animation.calculationMode = .paced
    animation.rotationMode = .auto
    animation.timingFunctions = [
        CAMediaTimingFunction(name: .easeIn),
        CAMediaTimingFunction(name: .easeOut)
    ]

    // Keep final state
    animation.fillMode = .forwards
    animation.isRemovedOnCompletion = false

    layer.add(animation, forKey: "pathAnimation")

    // Update model tree to match final state
    if let finalPoint = path.endPoint {
        layer.position = finalPoint
    }
}

// Color transition with keyframes
func animateBackgroundColor(view: UIView, colors: [CGColor]) {
    let animation = CAKeyframeAnimation(keyPath: "backgroundColor")
    animation.values = colors
    animation.keyTimes = (0..<colors.count).map { NSNumber(value: Double($0) / Double(colors.count - 1)) }
    animation.duration = 3.0
    animation.calculationMode = .linear
    animation.repeatCount = .infinity
    animation.autoreverses = true

    view.layer.add(animation, forKey: "colorCycle")
}

// CGPath extension for end point
extension CGPath {
    var endPoint: CGPoint? {
        var endPoint = CGPoint.zero
        self.applyWithBlock { element in
            let point = element.pointee.points.pointee
            switch element.pointee.type {
            case .moveToPoint, .addLineToPoint, .addQuadCurveToPoint, .addCurveToPoint:
                endPoint = point
            case .closeSubpath:
                break
            @unknown default:
                break
            }
        }
        return endPoint
    }
}
```

### Spring Animations — Physically-Based

```swift
// CASpringAnimation for realistic spring physics
func createSpringAnimation(
    keyPath: String,
    mass: CGFloat = 1.0,
    stiffness: CGFloat = 100.0,
    damping: CGFloat = 10.0,
    initialVelocity: CGFloat = 0.0
) -> CASpringAnimation {
    let animation = CASpringAnimation(keyPath: keyPath)
    animation.mass = mass
    animation.stiffness = stiffness
    animation.damping = damping
    animation.initialVelocity = initialVelocity
    animation.duration = animation.settlingDuration // Calculated from physics
    animation.fillMode = .forwards
    animation.isRemovedOnCompletion = false
    return animation
}

// Usage
let spring = createSpringAnimation(keyPath: "transform.scale", damping: 12)
spring.toValue = 1.2
layer.add(spring, forKey: "scale")

// UIView spring animation (simpler, less control)
UIView.animate(
    withDuration: 0.5,
    delay: 0,
    usingSpringWithDamping: 0.7,
    initialSpringVelocity: 0.5,
    options: [.curveEaseOut],
    animations: {
        view.transform = CGAffineTransform(scaleX: 1.2, y: 1.2)
    }
)
```

### Rendering Pipeline — Performance Optimization

**GPU-accelerated properties (prefer these for animation):**

| Property          | GPU-Accelerated | Notes                                                   |
| ----------------- | --------------- | ------------------------------------------------------- |
| `transform`       | ✅ Yes          | Use `transform` not `frame`/`bounds`                    |
| `opacity`         | ✅ Yes          | Alpha compositing is GPU-native                         |
| `backgroundColor` | ✅ Yes          | Color changes are cheap                                 |
| `position`        | ✅ Yes          | Translation is GPU-native                               |
| `cornerRadius`    | ⚠️ Conditional  | Triggers offscreen rendering if `masksToBounds` is true |
| `shadow`          | ❌ No           | Triggers offscreen rendering — use `shadowPath`         |
| `bounds`/`frame`  | ❌ No           | Triggers layout pass — use `transform`                  |

**Eliminating offscreen rendering:**

```swift
// WRONG: Triggers offscreen rendering
view.layer.cornerRadius = 12
view.layer.masksToBounds = true  // Offscreen pass!

// BETTER: Use shaped layer (iOS 11+)
view.layer.cornerRadius = 12
// Don't set masksToBounds if you don't clip subviews

// BEST: Pre-rendered mask for complex shapes
func applyRoundedCorners(radius: CGFloat, corners: UIRectCorner) {
    let path = UIBezierPath(
        roundedRect: bounds,
        byRoundingCorners: corners,
        cornerRadii: CGSize(width: radius, height: radius)
    )
    let mask = CAShapeLayer()
    mask.path = path.cgPath
    layer.mask = mask
}
```

**Shadow optimization with shadowPath:**

```swift
// WRONG: Core Animation must calculate shadow geometry per frame
view.layer.shadowColor = UIColor.black.cgColor
view.layer.shadowOffset = CGSize(width: 0, height: 4)
view.layer.shadowOpacity = 0.3
view.layer.shadowRadius = 8
// No shadowPath — Core Animation analyzes layer content every frame

// CORRECT: Provide explicit shadow path
view.layer.shadowColor = UIColor.black.cgColor
view.layer.shadowOffset = CGSize(width: 0, height: 4)
view.layer.shadowOpacity = 0.3
view.layer.shadowRadius = 8
view.layer.shadowPath = UIBezierPath(rect: view.bounds).cgPath

// If view size changes, update shadowPath
override func layoutSubviews() {
    super.layoutSubviews()
    layer.shadowPath = UIBezierPath(rect: bounds).cgPath
}
```

**Rasterization — when and how:**

```swift
// Use rasterization for complex static content that doesn't change
// Rasterization caches the layer as a bitmap
view.layer.shouldRasterize = true
view.layer.rasterizationScale = UIScreen.main.scale

// ⚠️ WARNING: Rasterization is expensive if the layer changes frequently
// Only use when:
// 1. Layer has complex sublayer hierarchy
// 2. Layer content doesn't change often
// 3. Layer is animated (translation, opacity, transform)
//
// Don't use when:
// 1. Layer content changes every frame
// 2. Layer size changes (requires re-rasterization)
// 3. Layer is simple (overhead > benefit)
```

### CATransaction — Coordinated Animations

```swift
// Coordinate multiple animations with transaction
CATransaction.begin()
CATransaction.setAnimationDuration(0.4)
CATransaction.setAnimationTimingFunction(CAMediaTimingFunction(name: .easeInEaseOut))
CATransaction.setCompletionBlock {
    // Called when all animations in this transaction complete
    print("All animations finished")
}

// All layer changes within this block animate together
layer.opacity = 0.5
layer.transform = CATransform3DMakeScale(0.8, 0.8, 1.0)
layer.position = CGPoint(x: 100, y: 100)

CATransaction.commit()

// Nested transactions with different durations
CATransaction.begin()
CATransaction.setAnimationDuration(1.0)

CATransaction.begin()
CATransaction.setAnimationDuration(0.3)
layer.opacity = 0.5  // Animates over 0.3s
CATransaction.commit()

layer.transform = CATransform3DMakeScale(0.8, 0.8, 1.0)  // Animates over 1.0s

CATransaction.commit()
```

### Custom Layer Drawing — Performance Considerations

```swift
// Custom layer with async drawing
class GraphLayer: CALayer {
    var data: [CGFloat] = [] {
        didSet {
            // Redraw on main thread for layer property changes
            setNeedsDisplay()
        }
    }

    // Enable async drawing for complex content
    override class func needsDisplay(forKey key: String) -> Bool {
        if key == #keyPath(data) { return true }
        return super.needsDisplay(forKey: key)
    }

    override func draw(in ctx: CGContext) {
        guard !data.isEmpty else { return }

        let width = bounds.width
        let height = bounds.height
        let stepX = width / CGFloat(max(data.count - 1, 1))

        ctx.setStrokeColor(UIColor.systemBlue.cgColor)
        ctx.setLineWidth(2.0)
        ctx.setLineJoin(.round)

        let path = CGMutablePath()
        for (index, value) in data.enumerated() {
            let x = CGFloat(index) * stepX
            let y = height - (value * height)
            if index == 0 {
                path.move(to: CGPoint(x: x, y: y))
            } else {
                path.addLine(to: CGPoint(x: x, y: y))
            }
        }

        ctx.addPath(path)
        ctx.strokePath()
    }
}
```

### Instruments — Animation Performance Profiling

**Core Animation instrument settings:**

1. Open Instruments → Core Animation
2. Enable "Color Offscreen-Rendered Yellow" — yellow = offscreen rendering
3. Enable "Color Misaligned Images Green" — green = scaled images
4. Enable "Color Blended Layers Red" — red = overdraw
5. Record while exercising animations

**Target metrics:**

| Metric            | Target                               | How to Check                    |
| ----------------- | ------------------------------------ | ------------------------------- |
| Frame Rate        | 60fps (or 120fps on ProMotion)       | Core Animation instrument       |
| Offscreen Renders | 0 for animated layers                | Color Offscreen-Rendered Yellow |
| CPU Usage         | <5% during animation                 | Time Profiler instrument        |
| GPU Utilization   | <70% sustained                       | GPU Frame Capture               |
| Memory            | No growth during repeated animations | Allocations instrument          |

## Pipeline Integration

- **Stage 2 (Design):** IDS specifies animation behaviors, durations, easing curves, and transition patterns.
- **Stage 5 (Development):** Primary skill for custom animations, visual effects, and rendering optimization. All animations follow Core Animation best practices.
- **Stage 6 (Code Review):** Animation review: performance profiling results, offscreen rendering elimination, memory impact, timing function appropriateness.
- **Stage 8 (Integrity Verification):** CDO verifies IDS animation specifications are realized. Instruments profiling confirms 60fps target.

## Quality Standards

- All animations run at **60fps** (120fps on ProMotion devices) — zero dropped frames
- **Zero** offscreen rendering passes for animated layers (verified via Core Animation instrument)
- GPU-accelerated properties (`transform`, `opacity`) used for animation — never `frame`/`bounds`
- Shadow performance optimized with explicit `shadowPath` — no dynamic shadow calculation
- Rasterization used only for **complex static content** — never for frequently-changing layers
- All animations have appropriate **timing functions** — no linear animations for user-facing transitions
- Animation duration **<500ms** for micro-interactions, **<1000ms** for transitions
- Custom layer drawing uses `drawsAsynchronously = true` for complex content
- CATransaction used for **coordinated multi-property animations**
- All animations respect UIAccessibility's `reduceMotion` setting — provide alternative transitions
