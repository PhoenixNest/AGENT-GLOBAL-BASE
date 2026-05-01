---
name: angular-signals
description: Build Angular applications using the Signals reactivity model — replacing Zone.js-based change detection with fine-grained reactive state, `computed` derivations, and `effect` side-effects — achieving ≥30% rendering performance improvement on complex dashboards.
version: "1.0.0"
---

# Angular Signals

| Competency         | Description                                                           | Quality Criteria                                                                                                        |
| ------------------ | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Signal State       | Use `signal()` and `computed()` for reactive UI state                 | No `BehaviorSubject` for simple component state; computed values used for derived state; no unnecessary signal reads    |
| OnPush + Signals   | Combine `ChangeDetectionStrategy.OnPush` with signals for performance | All components use OnPush; change detection triggered only by signal updates, input changes, or async events            |
| Effect Management  | Use `effect()` for side effects with proper cleanup                   | Effects cleaned up on component destroy; no circular signal dependencies; effects limited to side-effects (not state)   |
| Migration Strategy | Migrate Zone.js-based components to signals incrementally             | Migration follows the Angular signals migration guide; Observable streams bridged using `toSignal()` / `toObservable()` |

## Execution Guidance

### Signal vs. Observable Decision Matrix

| Scenario                        | Use Signal                   | Use Observable                     |
| ------------------------------- | ---------------------------- | ---------------------------------- |
| Component-local UI state        | ✅ `signal()`                | —                                  |
| Derived/computed values         | ✅ `computed()`              | —                                  |
| HTTP requests                   | —                            | ✅ `HttpClient` returns Observable |
| WebSocket streams               | —                            | ✅ RxJS Subject/Observable         |
| Bridging HTTP to template state | ✅ `toSignal(http.get(...))` | —                                  |

### Performance Pattern

```typescript
// Instead of BehaviorSubject + async pipe
readonly count = signal(0);
readonly doubled = computed(() => this.count() * 2);

increment() {
  this.count.update(v => v + 1);
}
```

With `ChangeDetectionStrategy.OnPush`, Angular re-renders only the components where signals have changed — not the entire component tree.
