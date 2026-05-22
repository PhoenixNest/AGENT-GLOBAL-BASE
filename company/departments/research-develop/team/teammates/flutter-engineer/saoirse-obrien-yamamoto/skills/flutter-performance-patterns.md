---
name: flutter-performance-patterns
description: Flutter performance profiling and optimisation. Use when investigating UI jank or frame drops in a Flutter app, placing RepaintBoundary widgets, configuring raster cache strategy, implementing shader warm-up, establishing a frame budget baseline for key UI flows, setting up automated performance regression detection in CI, or advising on const widget optimisation and widget rebuild minimisation.
version: "1.0.0"
---

# Flutter Performance Patterns

## Purpose

A Flutter app that renders at 60 fps or 120 fps feels alive. One that drops frames feels broken, regardless of feature quality. Maintaining frame budget compliance is not a one-time task — it requires a measurement baseline, an understanding of Flutter's rendering pipeline, and an automated regression check that catches degradation before it ships to users.

---

## Flutter Rendering Pipeline — The Frame Budget

Each frame has a 16ms budget at 60Hz (8ms at 120Hz). The Flutter engine divides this between two threads:

| Thread            | Responsibility                    | Tools to Profile        |
| ----------------- | --------------------------------- | ----------------------- |
| **UI thread**     | Widget build, layout, compositing | DevTools "UI" track     |
| **Raster thread** | Drawing commands → GPU            | DevTools "Raster" track |

A frame drop occurs when either thread exceeds its budget. Most jank is caused by:

1. **Unnecessary rebuilds** — A widget rebuilds when its parent rebuilds, even if its visual output hasn't changed
2. **Expensive `build` methods** — Allocating large objects, doing computations, or building deeply nested trees in `build`
3. **Raster cache misses** — Complex layers being re-rasterised on every frame instead of being cached
4. **Shader compilation jank** — First-time GPU shader compilation causing stutter on specific animations
5. **Overly broad `CustomPainter.shouldRepaint`** — A painter that always returns `true` repaints on every frame

---

## Profiling with Flutter DevTools

### Step 1 — Run in Profile Mode

Always profile in profile mode on a physical device. Debug mode runs 10–20× slower and is not representative of production performance.

```
flutter run --profile
```

### Step 2 — Open DevTools Timeline

In DevTools, open the "Performance" tab. Enable "Enhance Tracing" for detailed widget build events. Record during the problematic interaction.

### Step 3 — Identify the Offending Frame

In the timeline, find frames that exceed 16ms. Click the frame to see which phase (UI or Raster) was the bottleneck:

- **UI thread spike** → expensive `build`, layout, or compositing — look for "Build" and "Layout" events in the frame detail
- **Raster thread spike** → expensive painting or shader compilation — look for "Paint" and "Compositor" events

### Step 4 — Identify the Offending Widget

Enable "Track widget builds" in DevTools. Rebuild events will be visible in the timeline with the widget class name. Look for widgets rebuilding more frequently than their visual content changes.

---

## Optimisation Techniques

### `const` Widgets

Mark widget constructors as `const` wherever possible. A `const` widget is never rebuilt — Flutter short-circuits the element reconciliation for subtrees of `const` widgets.

```dart
// Good
const SizedBox(height: 16)
const Text('Hello', style: TextStyle(fontSize: 16))

// Bad — allocates a new TextStyle on every build
Text('Hello', style: TextStyle(fontSize: 16))
```

**Tool:** `flutter analyze --suggestions` or the `prefer_const_constructors` lint rule catches missed `const` opportunities.

### `RepaintBoundary`

`RepaintBoundary` creates a new layer in the raster cache. Subtrees inside a `RepaintBoundary` are only re-rasterised when the subtree's own content changes.

Apply `RepaintBoundary` to:

- Animated widgets that change while their siblings do not (animated progress bars, spinners, live data feeds)
- Complex list items in a `ListView` where each item is independently rendered
- Map tiles or static canvas elements that do not change during scroll

**Warning:** `RepaintBoundary` costs GPU memory (the layer is cached). Do not apply it wholesale — measure before and after.

### Raster Cache Strategy

Flutter's `PictureLayer` cache is managed by the engine. To hint that a subtree should be cached:

```dart
RepaintBoundary(
    child: ComplexWidget(),
)
```

To disable raster caching for a subtree (useful when the content changes every frame and caching would waste memory):

```dart
RepaintBoundary(
    child: AnimatedWidget(),  // changes every frame — don't cache
)
```

### Shader Warm-Up

First-time shader compilation causes jank on the first animation run. Warm up shaders at app start:

```dart
// In main() before runApp
void main() async {
    WidgetsFlutterBinding.ensureInitialized();
    final shaderWarmUp = CustomShaderWarmUp();  // extend ShaderWarmUp
    await shaderWarmUp.execute();
    runApp(MyApp());
}
```

Alternatively, use `flutter drive --write-sksl-on-exit` to capture SKP shader traces from an automated run, then bundle the SKP file as an asset for warm-up.

---

## Automated Performance Regression Detection

### Establish Baselines

For each performance-critical UI flow (defined as a flow where frame drops are visible to the user):

1. Write a `flutter_driver` or Patrol integration test that exercises the flow
2. Collect frame timing data using `FlutterDriver.forceGC` and `timeline.summaryJson`
3. Record the 90th-percentile frame time as the baseline
4. Add a CI assertion: if the 90th-percentile exceeds the baseline by > 20%, fail the build

### Regression Check Template

```dart
// integration_test/performance_test.dart
testWidgets('scroll flow frame budget', (tester) async {
    final app = MaterialApp(home: MyScrollView());
    await tester.pumpWidget(app);

    // Drive the scroll
    await tester.timedDrag(
        find.byType(ListView),
        const Offset(0, -500),
        const Duration(seconds: 2),
    );

    // Assert no janky frames (> 16ms)
    final summary = await binding.retrieveTimeline();
    final jankyFrames = summary.jankyFrameCount;
    expect(jankyFrames, lessThan(3), reason: 'Too many janky frames in scroll flow');
});
```

---

## Output Standards

- Every feature that introduces a new animated component must include a `RepaintBoundary` assessment (is it needed?) documented in the PR.
- Performance baselines must be established before Stage 6 (Architecture Review) for any performance-critical screen.
- Automated performance regression checks must be in the CI pipeline before Stage 7 (Automated Testing).
