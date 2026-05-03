---
name: jetpack-compose
description: Build high-performance Jetpack Compose UIs — mastering composition, state hoisting, recomposition optimization, and custom layouts — delivering pixel-perfect implementations of the design system in Stage 5 development.
version: "1.0.0"
---

# Jetpack Compose

| Competency            | Description                                                        | Quality Criteria                                                                                                           |
| --------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Composition Patterns  | Write composable functions following composition principles        | Composables are small (< 80 lines), testable, and reusable; single-responsibility per composable                           |
| State Hoisting        | Apply state hoisting for stateless, reusable composables           | All composables that could be reused are stateless — state lifted to ViewModel or parent; no state inside leaf composables |
| Recomposition Control | Avoid unnecessary recompositions with `remember`, `derivedStateOf` | Recomposition count monitored with Layout Inspector; no composable recomposes on unrelated state changes                   |
| Custom Layouts        | Implement custom `Layout` composable for non-standard UI patterns  | Custom layouts use `Measurable`/`Placeable` correctly; measure pass runs in O(n) without multi-pass measurement            |

## Execution Guidance

### Recomposition Optimization

Key techniques to minimize recompositions:

```kotlin
// ❌ Causes recomposition on every count change
@Composable
fun ExpensiveItem(count: Int) { /* uses count */ }

// ✅ Only recomposes when isEven actually changes
@Composable
fun EfficientItem(count: Int) {
    val isEven by remember(count) { derivedStateOf { count % 2 == 0 } }
    // ...
}
```

### Performance Checklist

- [ ] `remember` wraps all non-trivial computations in composable scope
- [ ] `key()` used in `LazyColumn` items to preserve item state across reorders
- [ ] `Modifier.graphicsLayer` used for animated properties (avoids recomposition)
- [ ] `painterResource` / `vectorResource` cached — not recreated on recomposition
- [ ] Layout Inspector confirms no unexpected recomposition chains during interaction

### IDS Integration

Implement composables against the Internal Design System (IDS) components. Do not re-implement design tokens — consume them from the IDS theme (`MaterialTheme.colorScheme`, `MaterialTheme.typography`).
