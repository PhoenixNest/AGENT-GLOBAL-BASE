---
name: flutter-ui-systems
description: Flutter widget architecture and custom UI systems. Use when designing or implementing a Flutter design system, building custom widgets using CustomPainter or RenderObject, implementing complex interaction patterns (drag-and-drop, gesture conflict resolution, animated transitions), setting up Riverpod state management architecture, or advising on widget composition patterns for complex screen layouts.
version: "1.0.0"
---

# Flutter UI Systems

## Purpose

Flutter's widget system is composable but composition alone cannot produce every UI surface. Custom maps, chart canvases, drag-and-drop editors, and pixel-perfect design system primitives require direct access to the rendering pipeline. This skill covers both the high-level widget composition patterns used for most product UI and the low-level `CustomPainter`/`RenderObject` pipeline required for the hardest UI problems.

---

## Widget Architecture Principles

### Stateless vs. Stateful vs. ConsumerWidget

| Widget Type                 | When to Use                                                                                         |
| --------------------------- | --------------------------------------------------------------------------------------------------- |
| `StatelessWidget`           | Display-only; all data comes from parent or `Riverpod` providers                                    |
| `StatefulWidget`            | Local ephemeral state only (animation controller, focus node, text controller) — not business state |
| `ConsumerWidget` (Riverpod) | Business state from providers; replaces `StatefulWidget` + `BLoC` for most cases                    |
| `ConsumerStatefulWidget`    | Needs both local ephemeral state AND business state from providers                                  |

**Principle:** keep `StatefulWidget` to the minimum. If state belongs to the business layer, it belongs in a Riverpod `Notifier` or `AsyncNotifier`, not in a widget's `State` class.

### Widget Composition Over Inheritance

Prefer composing small, single-purpose widgets over inheriting and overriding. A 300-line `build` method is always a decomposition problem — extract sub-widgets until each `build` method is readable in one screen.

---

## Riverpod Architecture

### Provider Types

| Provider Type              | Purpose                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------- |
| `Provider<T>`              | Immutable values and computed derivations                                               |
| `StateProvider<T>`         | Simple mutable state (toggles, filters, counters)                                       |
| `AsyncNotifierProvider<T>` | Async state with loading/error/data — the default for network and database-backed state |
| `NotifierProvider<T>`      | Synchronous mutable business state with complex mutation logic                          |
| `StreamProvider<T>`        | Wraps a `Stream<T>` (e.g., Firestore stream, SQLDelight flow)                           |
| `FutureProvider<T>`        | One-shot async data; use `AsyncNotifierProvider` for refreshable data                   |

### Scoping and Override

Scope providers to the smallest widget subtree that needs them using `ProviderScope` overrides. This is especially important for list items — providing a `currentItemProvider` override per list item avoids O(N) rebuilds.

---

## CustomPainter

Use `CustomPainter` for:

- Custom charts and data visualisations
- Canvas-based drawings (maps, diagrams)
- Pixel-level design system primitives (custom progress bars, custom sliders)
- Any surface where the standard widget tree would require hacking `ClipPath` or `Transform` into illegibility

### Skeleton

```dart
class MyPainter extends CustomPainter {
  final MyData data;
  MyPainter({required this.data}) : super(repaint: data);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blue
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke;
    canvas.drawLine(Offset.zero, Offset(size.width, size.height), paint);
  }

  @override
  bool shouldRepaint(MyPainter oldDelegate) => oldDelegate.data != data;
}
```

**Performance rules:**

- `shouldRepaint` must return `false` when the visual output would be identical — return `true` only when the data that affects drawing has changed
- Use `repaint` listenable parameter (as shown above) instead of rebuilding the `CustomPaint` widget for animation-driven repaints
- Cache `Paint` objects outside the `paint` method — creating a `Paint()` per frame is measurable overhead

---

## RenderObject (Advanced)

Use `RenderObject` when:

- `CustomPainter` is insufficient (you need custom layout, not just custom painting)
- You need to accept children and control their layout (implement `RenderBox` with `ContainerRenderObjectMixin`)
- You are building a scrollable viewport or a custom hit-testing region

`RenderObject` work is complex. Before reaching for it, verify that `CustomPainter` + `GestureDetector` + `Stack` cannot solve the problem. When it is necessary, always add a corresponding `RenderObjectWidget` and a `RenderObjectElement` to maintain the widget-element-renderObject triple correctly.

---

## Design System Implementation

When implementing a design system component:

1. **Match the IDS specification exactly** — pixel measurements, corner radii, elevation shadows, and typography weights must match the IDS document. Do not approximate.

2. **Component token system** — define a `ThemeExtension` class for every component's tokens (colour, spacing, typography). This allows `Theme.of(context).extension<ButtonTokens>()` to return the correct values for light/dark/brand themes.

3. **Accessibility** — every interactive component must set `Semantics` label, role, and state. Use `MergeSemantics` where appropriate. Test with the screen reader on both Android (TalkBack) and iOS (VoiceOver).

4. **Golden tests** — every design system component must have at least one golden test per theme variant. Goldens catch unintended visual regressions that unit tests miss.

---

## Output Standards

- No `build` method should exceed 80 lines. If it does, extract sub-widgets.
- `CustomPainter.shouldRepaint` must be implemented correctly — always; a stub that always returns `true` is a P1 performance defect.
- Every `Consumer`/`ConsumerWidget` must watch the narrowest possible slice of state — watching an entire `AsyncValue<List<T>>` when only the length is needed causes unnecessary rebuilds.
