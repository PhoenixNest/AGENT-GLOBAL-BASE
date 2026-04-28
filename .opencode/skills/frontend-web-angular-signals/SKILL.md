---
name: frontend-web-angular-signals
description: Angular Signals reactive state management — fine-grained reactivity, computed signals, effect tracking, and optimized change detection for Angular 16+. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 5 (Development) for Angular component implementation and Stage 6 (Code Review) for reactive pattern validation. Trigger: angular signals, angular reactivity, computed signals, effect tracking, angular change detection, angular 16.
prerequisites:
  - frontend-web-overview

version: "1.0.0"
---

# Angular Signals — Reactive Programming Guide

## 1. Overview

Angular Signals is a reactive state management system introduced in Angular 16 that provides fine-grained reactivity to the framework. Signals enable Angular to track exactly which parts of an application depend on specific pieces of state, allowing for optimized change detection and more predictable data flow.

### When to Use Signals

| Scenario                   | Recommended Approach                    |
| -------------------------- | --------------------------------------- |
| Simple component state     | ✅ Signals                              |
| Complex async data streams | ⚠️ RxJS + Signals                       |
| Global application state   | ✅ NgRx/Signals or custom signal stores |
| Form state management      | ✅ Signal-based forms (Angular 17+)     |
| HTTP data fetching         | ⚠️ RxJS → Signal conversion             |

Signals complement RxJS rather than replacing it entirely. Use signals for synchronous state and RxJS for complex asynchronous event processing.

## 2. Signal Creation

### Basic Signal Usage

```typescript
import { signal, Signal, WritableSignal } from "@angular/core";

// Writable signal with type inference
const count = signal<number>(0);
// WritableSignal<number>

// Readonly signal (derived from writable)
const readonlyCount: Signal<number> = count.asReadonly();

// Signal with complex types
interface User {
  id: number;
  name: string;
  email: string;
}

const user = signal<User | null>(null);
```

### Signal Mutation Methods

```typescript
import { signal } from "@angular/core";

const todos = signal<string[]>([]);

// .set() — replace value entirely
todos.set(["Learn Signals", "Build app"]);

// .update() — compute new value from current
todos.update((current) => [...current, "Test signals"]);

// .mutate() — modify value in place (for mutable objects)
interface Cart {
  items: { name: string; quantity: number }[];
}

const cart = signal<Cart>({ items: [] });
cart.mutate((state) => {
  state.items.push({ name: "Widget", quantity: 1 });
});
```

### Signal Initialization Patterns

```typescript
import { signal, inject, OnInit } from "@angular/core";

// Immediate initialization
const theme = signal<"light" | "dark">("light");

// Lazy initialization with factory
const expensiveState = signal(() => computeInitialState());

// Initialized from service
class TodoService {
  getInitialTodos() {
    return ["Default todo"];
  }
}

@Component({
  selector: "app-todo",
  template: `...`,
})
class TodoComponent {
  private todoService = inject(TodoService);
  todos = signal(this.todoService.getInitialTodos());
}
```

## 3. Computed Signals

### Creating Derived State

```typescript
import { signal, computed } from "@angular/core";

const count = signal(0);
const doubleCount = computed(() => count() * 2);

// Complex derived state
interface Product {
  name: string;
  price: number;
  quantity: number;
}

const cartItems = signal<Product[]>([
  { name: "Widget", price: 9.99, quantity: 2 },
  { name: "Gadget", price: 24.99, quantity: 1 },
]);

const subtotal = computed(() =>
  cartItems().reduce((sum, item) => sum + item.price * item.quantity, 0),
);

const taxRate = signal(0.08);
const tax = computed(() => subtotal() * taxRate());
const total = computed(() => subtotal() + tax());
```

### Memoization and Performance

Computed signals are **memoized** — they only recalculate when their dependencies change:

```typescript
const userId = signal(1);
const userProfile = computed(() => {
  console.log("Computing profile...");
  return fetchUserProfile(userId());
});

// First read: logs "Computing profile..."
// Second read: returns cached value (no log)
// After userId.set(2): recalculates on next read
```

**Performance characteristics:**

| Operation              | Complexity     | Notes                  |
| ---------------------- | -------------- | ---------------------- |
| Signal read            | O(1)           | Direct value access    |
| Signal write           | O(dependents)  | Notifies dependents    |
| Computed read (cached) | O(1)           | Returns memoized value |
| Computed read (stale)  | O(computation) | Recalculates once      |

### Equality Functions for Custom Comparison

```typescript
import { signal, computedEqual } from "@angular/core";

// Prevent unnecessary notifications for equivalent values
const items = signal<Product[]>([], {
  equal: (a, b) => JSON.stringify(a) === JSON.stringify(b),
});

// Custom equality for Date objects
const lastUpdated = signal(new Date(), {
  equal: (a, b) => a.getTime() === b.getTime(),
});
```

## 7. Migration Patterns

### BehaviorSubject → Signal Migration

| Pattern       | RxJS (Before)            | Signals (After)       |
| ------------- | ------------------------ | --------------------- |
| State storage | `BehaviorSubject<T>`     | `signal<T>`           |
| Read value    | `subject.value`          | `signal()`            |
| Update value  | `subject.next(value)`    | `signal.set(value)`   |
| Derived state | `subject.pipe(map(...))` | `computed(() => ...)` |
| Side effects  | `subject.subscribe(...)` | `effect(() => ...)`   |
| Completion    | `subject.complete()`     | `effect.destroy()`    |

### Incremental Migration Strategy

```typescript
// Phase 1: Coexistence — keep RxJS, add signals where convenient
import { toSignal } from "@angular/core/rxjs-interop";

class MixedComponent {
  // Keep existing RxJS service
  data$ = this.dataService.getData();

  // Convert to signal for template use
  data = toSignal(this.data$, { initialValue: [] });
}

// Phase 2: Signal-first — new code uses signals
class SignalFirstComponent {
  state = signal<ComponentState>({ items: [], loading: false });

  filteredItems = computed(() =>
    this.state().items.filter((item) => item.active),
  );

  loadItems() {
    this.dataService.getData().subscribe((items) => {
      this.state.update((s) => ({ ...s, items }));
    });
  }
}

// Phase 3: Full signals — replace RxJS where possible
class PureSignalComponent {
  state = signal<ComponentState>({ items: [], loading: false });

  // Use resource API for async data (Angular 19+)
  items = resource({
    loader: () => this.dataService.fetchItems(),
  });
}
```

### Migration Checklist

- [ ] Identify all `BehaviorSubject` instances in component
- [ ] Replace with `signal<T>` for synchronous state
- [ ] Convert `.pipe(map(...))` chains to `computed()`
- [ ] Replace `.subscribe()` side effects with `effect()`
- [ ] Use `toSignal()` for remaining RxJS observables
- [ ] Update templates from `| async` to direct signal calls
- [ ] Remove unused RxJS imports
- [ ] Verify change detection behavior with OnPush

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`4.-effects.md`](references/4.-effects.md) — 4. Effects
- [`5.-signal-integration.md`](references/5.-signal-integration.md) — 5. Signal Integration
- [`6.-component-architecture.md`](references/6.-component-architecture.md) — 6. Component Architecture
- [`8.-testing-signals.md`](references/8.-testing-signals.md) — 8. Testing Signals
- [`9.-performance-considerations.md`](references/9.-performance-considerations.md) — 9. Performance Considerations
- [`10.-stage-5-integration.md`](references/10.-stage-5-integration.md) — 10. Stage 5 Integration
- [`11.-references.md`](references/11.-references.md) — 11. References
