---
name: angular-signals
description: Angular Signals is a reactive state management system introduced in Angular 16 that provides fine-grained reactivity to the framework.
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

## 4. Effects

### Basic Effect Usage

```typescript
import { signal, effect, inject } from "@angular/core";

@Component({
  selector: "app-logger",
  template: `...`,
})
class LoggerComponent {
  count = signal(0);

  constructor() {
    // Effect runs when dependencies change
    effect(() => {
      console.log(`Count changed to: ${this.count()}`);
    });
  }
}
```

### Effect Cleanup Functions

```typescript
import { signal, effect } from "@angular/core";

const url = signal("/api/data");

effect((onCleanup) => {
  const controller = new AbortController();

  fetch(url(), { signal: controller.signal })
    .then((response) => response.json())
    .then((data) => console.log(data));

  // Cleanup runs before effect re-executes or is destroyed
  onCleanup(() => {
    controller.abort();
  });
});
```

### Avoiding Infinite Loops

```typescript
// ❌ BAD: Writing to signal inside its own effect
const count = signal(0);
effect(() => {
  count.set(count() + 1); // Infinite loop!
});

// ✅ GOOD: Separate read and write signals
const input = signal(0);
const output = signal(0);

effect(() => {
  output.set(input() * 2); // No loop — different signal
});

// ✅ GOOD: Use computed for derived values
const doubled = computed(() => input() * 2);
```

### Effect Ordering

```typescript
import { signal, effect } from "@angular/core";

const a = signal(1);
const b = signal(2);

// Effects run in creation order by default
effect(() => console.log("Effect 1:", a()));
effect(() => console.log("Effect 2:", b()));
effect(() => console.log("Effect 3:", a() + b()));

// Use allowSignalWrites for explicit ordering when needed
effect(
  () => {
    // Rare: only use when effect must write to signals
  },
  { allowSignalWrites: true },
);
```

## 5. Signal Integration

### Signal-Based Inputs (Angular 17.1+)

```typescript
import { Component, input, computed } from "@angular/core";

@Component({
  selector: "app-user-card",
  template: `
    <h3>{{ fullName() }}</h3>
    <p>Email: {{ email() }}</p>
  `,
})
class UserCardComponent {
  // Signal input with required constraint
  firstName = input.required<string>();
  lastName = input.required<string>();

  // Signal input with default value
  email = input<string>("no-email@example.com");

  // Computed from inputs
  fullName = computed(() => `${this.firstName()} ${this.lastName()}`);
}
```

### RxJS Interoperability

```typescript
import { signal, effect } from "@angular/core";
import { toObservable, toSignal } from "@angular/core/rxjs-interop";
import { interval, map } from "rxjs";

// RxJS → Signal
const timer$ = interval(1000);
const timerSignal = toSignal(timer$, { initialValue: 0 });

// With transformation
const doubled$ = timer$.pipe(map((v) => v * 2));
const doubledSignal = toSignal(doubled$, { initialValue: 0 });

// Signal → RxJS Observable
const count = signal(0);
const count$ = toObservable(count);

// Use in template with async pipe
count$.subscribe((value) => console.log("Observable:", value));
```

### Taking Over Async Pipe

```typescript
import { Component, signal, computed } from "@angular/core";
import { toSignal } from "@angular/core/rxjs-interop";
import { HttpClient } from "@angular/common/http";
import { inject } from "@angular/core";

@Component({
  selector: "app-users",
  template: `
    @if (users(); as userList) {
      <ul>
        @for (user of userList; track user.id) {
          <li>{{ user.name }}</li>
        }
      </ul>
    } @else {
      <p>Loading...</p>
    }
  `,
})
class UsersComponent {
  private http = inject(HttpClient);

  // Replace async pipe with signal
  users = toSignal(this.http.get<User[]>("/api/users"), { initialValue: [] });
}
```

## 6. Component Architecture

### Signal-Based Components with OnPush

```typescript
import { Component, signal, ChangeDetectionStrategy } from "@angular/core";

@Component({
  selector: "app-counter",
  template: `
    <p>Count: {{ count() }}</p>
    <button (click)="increment()">Increment</button>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
class CounterComponent {
  count = signal(0);

  increment() {
    this.count.update((n) => n + 1);
  }
}
```

### Signal Queries (Angular 17.2+)

```typescript
import {
  Component,
  viewChild,
  viewChildren,
  contentChild,
  contentChildren,
} from "@angular/core";

@Component({
  selector: "app-parent",
  template: `
    <app-child #firstChild></app-child>
    <app-child></app-child>
  `,
})
class ParentComponent {
  // Single view child as signal
  firstChild = viewChild<ChildComponent>("firstChild");

  // Multiple view children as signal array
  allChildren = viewChildren(ChildComponent);

  // Content projection queries
  projectedContent = contentChild(TemplateRef);
  allProjected = contentChildren(DirectiveBase);

  ngAfterViewInit() {
    // Signals auto-update when query results change
    console.log(this.allChildren().length);
  }
}
```

### Signal-Based Component State Pattern

```typescript
import { Component, signal, computed } from "@angular/core";

interface TodoState {
  todos: Todo[];
  filter: "all" | "active" | "completed";
  searchQuery: string;
}

@Component({
  selector: "app-todo-list",
  template: `...`,
})
class TodoListComponent {
  private state = signal<TodoState>({
    todos: [],
    filter: "all",
    searchQuery: "",
  });

  todos = this.state;

  filteredTodos = computed(() => {
    const { todos, filter, searchQuery } = this.state();

    return todos
      .filter((todo) => {
        if (filter === "active") return !todo.completed;
        if (filter === "completed") return todo.completed;
        return true;
      })
      .filter((todo) =>
        todo.title.toLowerCase().includes(searchQuery.toLowerCase()),
      );
  });

  setFilter(filter: TodoState["filter"]) {
    this.state.update((s) => ({ ...s, filter }));
  }

  setSearchQuery(searchQuery: string) {
    this.state.update((s) => ({ ...s, searchQuery }));
  }
}
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

## 8. Testing Signals

### Testing Signal Values

```typescript
import { signal, computed } from "@angular/core";
import { ComponentFixture, TestBed } from "@angular/core/testing";

describe("Signal Tests", () => {
  it("should create signal with initial value", () => {
    const count = signal(0);
    expect(count()).toBe(0);
  });

  it("should update with set()", () => {
    const count = signal(0);
    count.set(5);
    expect(count()).toBe(5);
  });

  it("should update with update()", () => {
    const count = signal(0);
    count.update((n) => n + 1);
    expect(count()).toBe(1);
  });

  it("should compute derived values", () => {
    const price = signal(100);
    const tax = signal(0.1);
    const total = computed(() => price() * (1 + tax()));

    expect(total()).toBe(110);

    price.set(200);
    expect(total()).toBe(220);
  });
});
```

### Testing Effects

```typescript
import { signal, effect, EffectRef } from "@angular/core";

describe("Effect Testing", () => {
  it("should run effect when dependency changes", () => {
    const count = signal(0);
    const logSpy = jasmine.createSpy("log");

    const effectRef: EffectRef = effect(() => {
      logSpy(count());
    });

    expect(logSpy).toHaveBeenCalledWith(0);

    count.set(1);
    expect(logSpy).toHaveBeenCalledWith(1);

    effectRef.destroy();
  });

  it("should cleanup on effect destroy", () => {
    const cleanupSpy = jasmine.createSpy("cleanup");

    const effectRef = effect((onCleanup) => {
      onCleanup(() => cleanupSpy());
    });

    effectRef.destroy();
    expect(cleanupSpy).toHaveBeenCalled();
  });
});
```

### Component Integration Testing

```typescript
import { Component, signal, computed } from "@angular/core";
import { ComponentFixture, TestBed } from "@angular/core/testing";

@Component({
  selector: "app-test-counter",
  template: `
    <p data-testid="count">{{ count() }}</p>
    <p data-testid="double">{{ doubleCount() }}</p>
    <button (click)="increment()">+</button>
  `,
})
class TestCounterComponent {
  count = signal(0);
  doubleCount = computed(() => this.count() * 2);
  increment() {
    this.count.update((n) => n + 1);
  }
}

describe("CounterComponent", () => {
  let component: TestCounterComponent;
  let fixture: ComponentFixture<TestCounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestCounterComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(TestCounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should display initial count", () => {
    const countEl = fixture.nativeElement.querySelector(
      '[data-testid="count"]',
    );
    expect(countEl.textContent).toBe("0");
  });

  it("should update computed value when signal changes", () => {
    component.count.set(5);
    fixture.detectChanges();

    const doubleEl = fixture.nativeElement.querySelector(
      '[data-testid="double"]',
    );
    expect(doubleEl.textContent).toBe("10");
  });

  it("should increment on button click", () => {
    const button = fixture.nativeElement.querySelector("button");
    button.click();
    fixture.detectChanges();

    expect(component.count()).toBe(1);
  });
});
```

## 9. Performance Considerations

### Fine-Grained Updates vs Zone.js

| Approach           | Change Detection Scope   | Performance Impact |
| ------------------ | ------------------------ | ------------------ |
| Zone.js (default)  | Entire component tree    | Higher overhead    |
| OnPush + Signals   | Only affected components | Minimal overhead   |
| Zoneless + Signals | Only signal dependents   | Lowest overhead    |

### Signal Performance Benchmarks

```typescript
// Benchmark: Signal vs Zone.js change detection
import { signal } from "@angular/core";

const iterations = 10000;

// Signal-based update — O(1) per dependent
const counter = signal(0);
performance.mark("signal-start");
for (let i = 0; i < iterations; i++) {
  counter.set(i);
}
performance.mark("signal-end");
// ~2-5ms for 10,000 updates

// Zone.js triggers full change detection each time
performance.mark("zone-start");
for (let i = 0; i < iterations; i++) {
  this.zone.run(() => {
    this.value = i;
  });
}
performance.mark("zone-end");
// ~50-200ms for 10,000 updates
```

### Signal vs RxJS Performance Comparison

| Metric                       | Signals           | RxJS                |
| ---------------------------- | ----------------- | ------------------- |
| Memory per stream            | ~100 bytes        | ~500+ bytes         |
| Subscription overhead        | None (pull-based) | Per-subscription    |
| Synchronous update           | ✅ Direct         | Requires Subject    |
| Change detection integration | ✅ Native         | Requires async pipe |
| Tree-shaking                 | ✅ Excellent      | ⚠️ Partial          |

### Optimization Techniques

```typescript
// 1. Use computed() for expensive derivations
const expensiveData = computed(() => {
  // Only runs when dependencies change
  return heavyComputation(data());
});

// 2. Use custom equality to prevent unnecessary updates
const config = signal<AppConfig>(defaultConfig, {
  equal: (a, b) => a.version === b.version,
});

// 3. Batch multiple signal updates
function updateState(newState: Partial<State>) {
  state.update((current) => ({ ...current, ...newState }));
  // Single notification to all dependents
}

// 4. Use untracked() to read signals without creating dependency
const logger = effect(() => {
  const value = mainSignal();
  const metadata = untracked(() => debugSignal());
  console.log(value, metadata);
});
```

## 10. Stage 5 Integration

### Development Workflow for Angular Signals

During Stage 5 (Development), Angular Signals code follows these practices:

1. **Signal-first design** — Prefer signals for component state before reaching for RxJS
2. **Computed over manual derivation** — Use `computed()` for all derived state
3. **Effect hygiene** — Minimize side effects; prefer computed for transformations
4. **Type safety** — Explicit signal types for complex state shapes

### Code Review Checklist — Reactive Patterns

| Check                        | Description                                    | Severity if Failed |
| ---------------------------- | ---------------------------------------------- | ------------------ |
| Signal type inference        | All signals have correct TypeScript types      | P2                 |
| No infinite effect loops     | Effects don't write to their own dependencies  | P1                 |
| Computed memoization         | Expensive derivations use `computed()`         | P2                 |
| Cleanup functions            | Effects with async work have proper cleanup    | P1                 |
| OnPush compatibility         | Signal components use OnPush change detection  | P2                 |
| No unnecessary subscriptions | RxJS only used where signals can't handle it   | P3                 |
| Signal inputs preferred      | Component inputs use `input()` over `@Input()` | P3                 |
| Template signal calls        | Signals invoked with `()` in templates         | P1                 |

### Common Defect Patterns

```typescript
// P1: Missing signal invocation in template
// ❌
template: `<p>{{ count }}</p>`;

// ✅
template: `<p>{{ count() }}</p>`;

// P1: Effect writing to own dependency
// ❌
effect(() => {
  count.set(count() + 1); // Infinite loop
});

// P2: Manual derivation instead of computed
// ❌
let doubled: number;
effect(() => {
  doubled = count() * 2;
});

// ✅
const doubled = computed(() => count() * 2);

// P2: Missing cleanup in async effect
// ❌
effect(() => {
  fetch(url())
    .then((r) => r.json())
    .then(setData);
});

// ✅
effect((onCleanup) => {
  const controller = new AbortController();
  fetch(url(), { signal: controller.signal })
    .then((r) => r.json())
    .then(setData);
  onCleanup(() => controller.abort());
});
```

## 11. References

### Related Skills

- `angular-spring-boot.md` — Full-stack Angular + Spring Boot integration patterns
- `frontend-performance-optimization.md` — Performance optimization techniques including signal-based rendering
- `angular-testing.md` — Comprehensive Angular testing strategies
- `reactive-state-management.md` — Comparison of RxJS, NgRx, and Signals approaches

### External Resources

| Resource                       | URL                                            | Description                         |
| ------------------------------ | ---------------------------------------------- | ----------------------------------- |
| Angular Signals Official Guide | https://angular.dev/guide/signals              | Official Angular documentation      |
| Angular Reactivity Blog        | https://blog.angular.dev                       | Angular team announcements          |
| Signals RFC                    | Angular GitHub discussions                     | Original signal design discussions  |
| RxJS Interop Guide             | https://angular.dev/api/core/rxjs-interop      | toSignal/toObservable documentation |
| Zoneless Angular               | https://angular.dev/guide/experiments/zoneless | Future of Angular reactivity        |

### Version Compatibility

| Angular Version | Signal Feature                                           |
| --------------- | -------------------------------------------------------- |
| 16.0            | `signal()`, `computed()`, `effect()` (developer preview) |
| 16.2            | Signals stable API                                       |
| 17.0            | `input()`, `model()` signals                             |
| 17.1            | Signal queries (`viewChild`, `contentChild`)             |
| 17.2            | `resource()` API (developer preview)                     |
| 18.0            | Zoneless mode experimental support                       |
| 19.0            | `resource()` stable, linkedSignal                        |

---

_Last updated: April 2026 | Applicable to Angular 16+ | Maintained by Frontend Chapter_
