---
name: flutter-performance-patterns
description: Maintain Flutter app frame budgets through profiling, RepaintBoundary placement, raster cache strategy, shader warm-up, and automated performance regression detection in CI.
version: "1.0.0"
---

# Flutter Performance Patterns

| Competency         | Description                                              | Quality Criteria                                                                                |
| ------------------ | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| DevTools Profiling | Use Flutter DevTools to identify frame budget violations | P90 frame time ≤ 16ms on target device; no janky frames in primary user flows                   |
| RepaintBoundary    | Place `RepaintBoundary` to isolate expensive subtrees    | Boundaries placed around subtrees that change independently; no unnecessary paint layers        |
| Raster Cache       | Manage raster cache for static complex content           | `RasterCache` enabled for content that renders once but scales/translates frequently            |
| Shader Warm-Up     | Pre-compile shaders to eliminate first-use jank          | `ShaderWarmUp` subclass covers all custom shaders; warm-up runs at app start before first frame |

## Execution Guidance

### Performance Investigation Workflow

```
1. Identify the janky flow
   → Use DevTools → Timeline → record the problematic interaction

2. Find the bottleneck
   → Look for frames exceeding 16ms in the timeline
   → Identify whether the issue is in the UI thread (Dart) or raster thread (GPU)

3. UI thread jank → Dart CPU profiler
   → Find hot functions in the CPU profiler
   → Common causes: heavy shouldRepaint(), large widget rebuilds, synchronous work

4. Raster thread jank → shader or layer composition issue
   → Check for SaveLayer calls (expensive compositing)
   → Check CustomPainter.paint() for expensive draw operations
   → Enable raster cache for the offending subtree

5. Verify fix
   → Re-run the performance regression suite
   → Confirm P90 frame time is below budget on the lowest-spec target device
```

### RepaintBoundary Placement Rules

```dart
// GOOD: Wrap independently animated content
RepaintBoundary(
  child: AnimatedWidget(...),  // changes independently of parent
)

// GOOD: Wrap expensive-to-paint content that doesn't change with parent
RepaintBoundary(
  child: ComplexChart(data: staticData),
)

// BAD: Wrapping everything — creates too many layers, wastes memory
// BAD: Wrapping content that always repaints with parent — no benefit
```

### Automated Performance Regression Test Pattern

```dart
testWidgets('primary feed scroll is below 16ms P90', (tester) async {
  await tester.pumpWidget(const App());
  await tester.pumpAndSettle();

  final binding = LiveTestWidgetsFlutterBinding.instance;
  binding.framePolicy = LiveTestWidgetsFlutterBindingFramePolicy.benchmarkLive;

  await tester.drag(find.byType(ListView), const Offset(0, -500));
  await tester.pumpAndSettle();

  final stats = binding.collectFrameTimings();
  final p90 = stats.map((t) => t.totalSpan.inMicroseconds).toList()
    ..sort();
  final p90Value = p90[(p90.length * 0.9).floor()];

  expect(p90Value, lessThan(16000), reason: 'P90 frame time exceeds 16ms');
});
```
