---
version: "1.0.0"
---

| Competency       | Description                                                                                                          | Quality Criteria                                                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Reducer Design   | Pure state transformation, action enumeration, Effect return, reducer composition with `Reduce` and `@Reducer` macro | Reducers are pure functions (same input → same output); all side effects wrapped in Effects; complex features composed from smaller reducers |
| Store Management | Store initialization, ViewStore binding, scope/sub-state derivation, lifecycle management                            | Views observe only the sub-state they need; Store lifecycle bound to view lifecycle; no direct store mutation outside reducer                |
| Effect Handling  | Async effects, cancellation, timer effects, effect IDs, effect composition                                           | Effects are cancellable by ID; long-running effects properly scoped; effect errors handled within reducer                                    |
| State Design     | Equatable state, Codable conformance, state normalization, optional child state                                      | State is always Equatable; nested state properly scoped; optional child state handles nil gracefully                                         |
| Testing          | Reducer testing with TestStore, effect assertion, time manipulation, mock dependencies                               | Every reducer action has a corresponding test; Effects verified for correctness; time-based Effects tested with TestStore scheduler          |

## Pipeline Integration

- **Stage 3 (Architecture):** ADR establishes TCA as the iOS architecture pattern. UML state diagrams map to reducer state machines.
- **Stage 5 (Development):** Primary skill for iOS feature development. All screens implemented as TCA features with reducers, stores, and Effects.
- **Stage 6 (Code Review):** Architecture review: reducer purity, Effect correctness, dependency injection completeness, state Equatable conformance.
- **Stage 7 (Automated Testing):** TestStore-based reducer tests. Every reducer action has corresponding test coverage.
- **Stage 8 (Integrity Verification):** State machine completeness verified — all state transitions documented and tested.

## Quality Standards

- **100%** reducers are pure functions — same input state + action → same output state + effects
- **100%** side effects wrapped in `Effect` — no direct async calls outside Effects
- **100%** state types conform to `Equatable` — required for state diffing
- **100%** dependencies injected via `@Dependency` — no hardcoded service creation in reducers
- **100%** long-running Effects are cancellable with explicit effect IDs
- **100%** reducer actions have corresponding TestStore tests
- Views observe only needed sub-state via `observe:` closure — no full-state observation
- Child features scoped via `Scope` reducer — not embedded as full child stores
- Error handling within reducers — errors mapped to state, not thrown to views
- Deletion of `cancelInFlight: true` for debounced effects — only latest request executes

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
