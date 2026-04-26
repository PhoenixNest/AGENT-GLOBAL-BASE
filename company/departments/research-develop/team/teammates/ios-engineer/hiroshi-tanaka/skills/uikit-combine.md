---
version: "1.0.0"
---

| Competency                   | Description                                                                                         | Quality Criteria                                                                                                                    |
| ---------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| UIKit Architecture           | View controller lifecycle, view hierarchy, Auto Layout, custom views, delegation patterns           | View controllers are thin coordinators; custom views are reusable and testable; delegation uses weak references                     |
| Combine Reactive Programming | Publisher/Subscriber model, operators, subjects, error handling, backpressure, schedulers           | Complex event streams composed with operators; error handling at appropriate boundaries; publishers scheduled on correct queues     |
| Data Binding                 | @Published properties, BindableObject, sink subscription, assign operator, custom binding operators | UI binds to ViewModel publishers; no manual UI updates outside binding; subscription lifecycle managed correctly                    |
| MVVM with Combine            | ViewModel as publisher source, View as subscriber, unidirectional data flow, action channels        | ViewModel exposes publishers for state; View sends actions via PassthroughSubject; zero UIKit logic in ViewModel                    |
| Subscription Lifecycle       | AnyCancellable storage, cancel on deinit, subscription reuse, memory leak prevention                | All subscriptions stored and cancelled; zero retained subscriptions after view controller deallocation; leak-free under Instruments |

## Pipeline Integration

- **Stage 3 (Architecture):** ADR establishes Combine as reactive framework for UIKit screens. MVVM pattern with Combine publishers.
- **Stage 5 (Development):** Primary skill for UIKit screens using reactive patterns. All data binding, event streams, and subscription management.
- **Stage 6 (Code Review):** Combine review: subscription lifecycle, memory leak prevention, operator correctness, scheduler usage.
- **Stage 7 (Automated Testing):** Publisher testing with XCTest expectations; mock publishers for dependency injection.

## Quality Standards

- **100%** subscriptions stored in `Set<AnyCancellable>` and cancelled on deinit
- **Zero** force unwraps in Combine chains — use `compactMap` for optional filtering
- All publishers scheduled on appropriate scheduler — UI publishers on **Main**, background on **background queue**
- **Zero** UIKit logic in ViewModel — ViewModel only exposes publishers and accepts actions
- Debounce applied to **all user input** streams (search, text fields) — minimum 300ms
- Error handling at **appropriate boundary** — catch in ViewModel, not in View
- **Zero** memory leaks under Instruments Allocations — verified for all ViewControllers
- Combine operators used correctly — `flatMap` for async, `map` for sync, `switchToLatest` for cancellable chains
- All custom publishers conform to `Publisher` protocol with proper subscription lifecycle
- Test coverage for all Combine chains — publisher output verified with XCTest expectations

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
