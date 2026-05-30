---
name: flutter-ui-systems
description: Build advanced Flutter UI systems — CustomPainter and RenderObject pipelines, Riverpod state management, complex gesture handling, and production-grade design system implementation.
version: "1.0.0"
---

# Flutter UI Systems

| Competency                | Description                                                            | Quality Criteria                                                                               |
| ------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Custom Rendering          | Build `CustomPainter` and `RenderObject` subclasses for complex UI     | `shouldRepaint` returns false when no visual change; `paint` methods budget-compliant at 60fps |
| Widget Architecture       | Compose complex widget trees using `StatelessWidget`, `ConsumerWidget` | No unnecessary rebuilds; `const` constructors where possible; widget tests cover each widget   |
| Riverpod State Management | Implement app-wide state with Riverpod providers                       | Provider types matched to use case; no provider leaks; `AsyncNotifier` for async state         |
| Gesture Handling          | Resolve gesture conflicts in complex interactive surfaces              | `GestureRecognizer` competition resolved deterministically; no ghost touches                   |

## Execution Guidance

### CustomPainter Performance Rules

```dart
class CanvasPainter extends CustomPainter {
  final List<Widget> items;
  final Offset dragOffset;

  const CanvasPainter({required this.items, required this.dragOffset});

  @override
  void paint(Canvas canvas, Size size) {
    // Keep paint() side-effect-free and budget-conscious
    for (final item in items) {
      canvas.drawRect(item.bounds.shift(dragOffset), item.paint);
    }
  }

  @override
  bool shouldRepaint(CanvasPainter oldDelegate) {
    // CRITICAL: only repaint when visually relevant state changes
    return items != oldDelegate.items || dragOffset != oldDelegate.dragOffset;
  }
}
```

### Riverpod Provider Selection Guide

| Use Case                          | Provider Type           |
| --------------------------------- | ----------------------- |
| Immutable computed value          | `Provider`              |
| Async data fetch (once)           | `FutureProvider`        |
| Streaming data                    | `StreamProvider`        |
| Mutable state (sync)              | `NotifierProvider`      |
| Mutable state (async)             | `AsyncNotifierProvider` |
| Scoped state (per widget subtree) | `.autoDispose` variant  |

### Widget Tree Optimization Checklist

- [ ] `const` constructors on all leaf widgets that don't change
- [ ] `RepaintBoundary` wrapping expensive subtrees that don't change together
- [ ] `ListView.builder` instead of `ListView(children: [...])` for long lists
- [ ] `Consumer` or `ConsumerWidget` scoped as narrowly as possible
- [ ] No `setState` calls in response to provider changes (use `ref.listen`)
