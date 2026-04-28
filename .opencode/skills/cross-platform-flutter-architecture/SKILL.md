---
name: cross-platform-flutter-architecture
description: Flutter cross-platform architecture — widget architecture, BLoC/Riverpod state management, platform channel design, Dart null safety, and Flutter-specific clean architecture patterns for iOS and Android. Owned by Mei-Ling Johansson (Cross-Platform Lead). Use during Stage 3 (UML Engineering) for Flutter architecture design and Stage 5 (Development) for Flutter track implementation. Trigger: Flutter architecture, Flutter state management, BLoC, Riverpod, widget architecture, platform channels, Dart architecture.
prerequisites:
  - cross-platform-overview

version: "1.0.0"
---

# Flutter Architecture

**Category:** Mobile Engineering — Cross-Platform (Flutter)
**Owner:** Cross-Platform Engineer (Fatima Al-Zahra)

## Overview

This skill implements production-grade Flutter application architecture covering widget tree optimization, BLoC state management, Riverpod for dependency injection, navigation architecture, and platform channel integration. It applies to Stage 5 (Development) where Flutter apps are built with scalable architecture, Stage 6 (Code Review) where widget composition and state management correctness are audited, and Stage 8 (Integrity Verification) where the CDO verifies IDS specifications are realized in Flutter implementation.

## Competency Dimensions

| Dimension                | Description                                                                                                   | Proficiency Indicators                                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Widget Tree Architecture | Widget/Element/RenderObject tree, const constructors, key management, widget lifecycle                        | Widget tree is optimized with const; keys used correctly for list items; build methods are pure and fast               |
| BLoC Pattern             | Event-State transformation, Cubit vs BLoC, BlocBuilder/BlocListener, event debouncing, state equality         | BLoCs are pure event processors; states are Equatable; UI reacts only to state changes; no business logic in widgets   |
| Riverpod                 | Provider types (Provider, StateProvider, StateNotifierProvider, FutureProvider), provider families, ref.watch | Providers are scoped appropriately; provider families for parameterized providers; ref.watch for reactive dependencies |
| Navigation               | GoRouter, declarative routing, nested navigation, deep linking, route guards, transition customization        | Navigation is declarative; deep links handled correctly; route guards for auth; nested navigators for tab screens      |
| Platform Channels        | MethodChannel, EventChannel, BasicMessageChannel, platform-specific implementation, error handling            | Platform channels are typed; errors propagate correctly; async platform calls don't block UI; channel setup is lazy    |

## Pipeline Integration

- **Stage 3 (Architecture):** ADR establishes Flutter architecture pattern (BLoC vs Riverpod), navigation strategy, and platform channel contracts.
- **Stage 5 (Development):** Primary skill for Flutter app development. All widgets, BLoCs, providers, navigation, and platform channels.
- **Stage 6 (Code Review):** Architecture review: BLoC purity, widget composition efficiency, provider correctness, platform channel error handling.
- **Stage 8 (Integrity Verification):** CDO verifies IDS specifications are realized. Widget tree performance profiled.

## Quality Standards

- **100%** BLoCs are pure event processors — no business logic in widgets
- All states are **Equatable** — efficient rebuild detection
- Widget build methods are **pure and fast** — no side effects, no network calls
- **const constructors** used wherever possible — widget tree optimization
- GoRouter used for **declarative navigation** — no imperative Navigator.push
- Deep links handled via **GoRouter redirect** — proper auth guards
- Platform channels are **typed and error-handled** — PlatformException caught and translated
- BLoC events are **debounced** where appropriate (search, text input)
- Provider scoping is **correct** — no over-scoped or under-scoped providers
- Widget keys used correctly — **ValueKey** for typed items, **PageStorageKey** for scroll state
- Platform channel calls are **async** — never block Flutter UI thread

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
