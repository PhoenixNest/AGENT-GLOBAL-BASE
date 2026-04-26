---
name: frontend-web-react-state-management
description: React state management architecture — Context API for dependency injection, Zustand for client state, Redux Toolkit for complex flows, state normalization, React Query for server state, and optimistic updates with rollback. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 3 (Architecture) for state tool selection and Stage 5 (Development) for store implementation. Trigger: react state management, zustand, redux toolkit, react query, context api, state normalization, optimistic updates.
prerequisites:
  - frontend-web-overview

version: "1.0.0"
---

# React State Management

**Category:** Frontend Engineering / React Architecture
**Owner:** Frontend Engineer (Yuna Park)

## Overview

This skill enables the design, implementation, and maintenance of robust React state management architectures that scale from simple component state to complex application-wide data flows. It covers Context API for low-frequency global state, Zustand for lightweight client state, Redux Toolkit for complex state with middleware requirements, state normalization for relational data, async state management with React Query patterns, and optimistic update strategies with rollback guarantees. State management is the backbone of application correctness — poorly designed state leads to stale UI, race conditions, and unpredictable behavior that no amount of testing can fully cover.

## Competency Dimensions

| Dimension                  | Description                                                                              | Proficiency Indicators                                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **State Tool Selection**   | Right tool for the right job — Context API vs Zustand vs Redux vs server state libraries | Zero over-engineering (no Redux for 3 boolean flags); zero under-engineering (no prop drilling 8 levels deep) |
| **State Normalization**    | Normalizing relational data into flat lookup tables, eliminating duplication             | No nested data duplication; O(1) entity lookup by ID; consistent update patterns                              |
| **Async State Management** | Server state separation, caching, invalidation, background refetching                    | Server state managed by React Query/SWR; client state in Zustand; zero manual loading flags                   |
| **Optimistic Updates**     | UI updates before server confirmation with automatic rollback on failure                 | Optimistic updates with undo queue; rollback within 100ms of error; user notified of sync failures            |
| **State Colocation**       | Keeping state as close to where it's used as possible                                    | No global state for component-local concerns; minimal cross-component state sharing                           |
| **State Debugging**        | DevTools integration, state inspection, time-travel debugging, action logging            | Full state history traceable; reproduction steps for any state bug within 15 minutes                          |

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                          | Deliverable                                   |
| ------------------------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Identify state requirements from IDS interactions; document state dependencies          | State requirements in IDS                     |
| **Stage 3** (Architecture)           | Define state management architecture in UML; register ADRs for state tool selection     | State management ADRs                         |
| **Stage 5** (Development)            | Implement state stores, async state management, optimistic updates, state normalization | Production state management code              |
| **Stage 6** (Code Review)            | Review state architecture, normalization, async patterns, rollback logic                | State architecture review in DEFECT-REPORT.md |
| **Stage 8** (Integrity Verification) | Verify state consistency across all user flows; test rollback scenarios                 | State integrity verification report           |

## Quality Standards

| Metric                         | Target                                                          | Enforcement                                                      |
| ------------------------------ | --------------------------------------------------------------- | ---------------------------------------------------------------- |
| **State colocation**           | State lives at the lowest common ancestor that needs it         | Code review; zero global state for component-local concerns      |
| **State tool appropriateness** | No over-engineering or under-engineering                        | Architecture review against decision matrix                      |
| **State normalization**        | No duplicated entity data in stores                             | Data shape audit; O(1) entity lookup verification                |
| **Async state separation**     | Server state managed by React Query/SWR, not manual useState    | Code review; zero manual fetch + useState patterns               |
| **Optimistic update coverage** | All user-facing mutations have optimistic updates with rollback | Code review; rollback test for each mutation                     |
| **Rollback reliability**       | 100% of failed mutations restore previous state                 | Unit tests for rollback scenarios                                |
| **State debugging**            | Full state traceable via DevTools                               | DevTools integration verified                                    |
| **Selective subscriptions**    | Components only subscribe to the state slices they need         | Zustand selector audit; zero `useStore(state => state)` patterns |
| **Context update frequency**   | Context consumers re-render < 5 times per user action           | React DevTools Profiler audit                                    |
| **State persistence**          | Persisted state is versioned and migrated safely                | Migration test for persisted state schema changes                |
| **Race condition prevention**  | No stale state from out-of-order async responses                | React Query cancellation or request ID validation                |
| **State test coverage**        | ≥ 90% of state management logic tested                          | Unit test coverage report                                        |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
