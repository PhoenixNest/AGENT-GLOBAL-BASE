---
name: company-software-architecture-design
description: Software architecture design with UML modelling — system design using PlantUML/Mermaid, architecture patterns (clean, MVVM, VIPER, TCA), logical project structures, dependency graphs, system interaction models. Owned by Dr. Kenji Nakamura (CTO).
disable-model-invocation: false
---

# Software Architecture Design

## Purpose

Design scalable, maintainable software architectures for mobile and backend systems. Produce clear architectural documentation including UML diagrams, component designs, and logical project structures that guide engineering teams toward high-quality implementations.

## Architecture Design Process

### 1. Understand Requirements and Constraints

- **Functional requirements**: What must the system do?
- **Non-functional requirements**: Performance, scalability, security, reliability targets
- **Platform constraints**: iOS/Android versions, device capabilities, network conditions
- **Team constraints**: Team size, skill levels, existing codebases
- **Business constraints**: Timeline, budget, compliance requirements

### 2. Define Architecture Principles

- **Modularity**: How will we decompose the system into manageable pieces?
- **Separation of concerns**: How do we keep business logic separate from UI and infrastructure?
- **Testability**: How will we make this easy to test?
- **Scalability**: How will this handle growth?
- **Maintainability**: How will future engineers understand and modify this?

### 3. Design the System Structure

- **Layers**: Presentation, business logic, data access, infrastructure
- **Modules/Components**: Major functional units with clear responsibilities
- **Boundaries**: What are the interfaces between components?
- **Data flow**: How does information move through the system?

---

## UML Diagram Types and When to Use Them

### Component Diagrams

**Purpose**: Show high-level system structure and dependencies between major components.

**When to use**: Explaining overall system architecture, showing how modules relate, documenting deployment boundaries, planning modularization or refactoring.

```
[UI Layer] --> [Business Logic Layer] --> [Data Layer]
[Business Logic] --> [Network Service]
[Business Logic] --> [Local Storage]
```

### Class Diagrams

**Purpose**: Show object-oriented structure with classes, attributes, methods, and relationships.

**When to use**: Designing domain models, documenting API structures, planning inheritance hierarchies, showing design patterns in use.

**Key elements**: Classes with attributes and methods; relationships (inheritance, composition, aggregation, association); interfaces and abstract classes; visibility modifiers.

### Sequence Diagrams

**Purpose**: Show how objects interact over time for a specific scenario.

**When to use**: Documenting complex workflows, showing API call sequences, explaining authentication flows, debugging timing or ordering issues.

**Key elements**: Actors and objects as vertical lifelines; messages/calls as horizontal arrows; activation boxes; return values and async operations.

### Activity Diagrams

**Purpose**: Show workflow or business process flow.

**When to use**: Documenting user journeys, showing decision logic, planning state machines, explaining algorithms.

---

## Mobile Architecture Patterns

### iOS Architecture Patterns

**MVVM (Model-View-ViewModel)**: ViewModel handles presentation logic. View binds to ViewModel (using Combine or async/await). Better testability than MVC. Good for complex UI with lots of state.

**VIPER (View-Interactor-Presenter-Entity-Router)**: Highly modular, each component has single responsibility. More boilerplate but excellent for large teams. Clear boundaries make testing easier.

**Composable Architecture (TCA)**: Unidirectional data flow. State management with reducers. Excellent for complex state and side effects.

### Android Architecture Patterns

**MVVM with Android Architecture Components**: ViewModel + StateFlow; Repository pattern; Room for local storage. Current Android best practice.

**Clean Architecture**: Layered approach: Presentation, Domain, Data. Dependency inversion (inner layers don't depend on outer). Highly testable and maintainable.

---

## Logical Project Structure

### iOS Project Structure

```
MyApp/
├── App/
│   ├── AppDelegate.swift
│   └── SceneDelegate.swift
├── Features/
│   ├── Authentication/
│   │   ├── Views/
│   │   ├── ViewModels/
│   │   └── Models/
│   └── Home/
│       ├── Views/
│       ├── ViewModels/
│       └── Models/
├── Core/
│   ├── Networking/
│   ├── Storage/
│   └── Analytics/
└── Shared/
    ├── UI/
    └── Extensions/
```

### Android Project Structure

```
com.myapp/
├── features/
│   ├── authentication/
│   │   ├── ui/
│   │   ├── viewmodel/
│   │   └── data/
│   └── home/
│       ├── ui/
│       ├── viewmodel/
│       └── data/
├── core/
│   ├── network/
│   ├── database/
│   └── analytics/
└── shared/
    ├── ui/
    └── utils/
```

**Key principles**: Feature-based organization; clear boundaries; shared utilities in dedicated modules; easy to add new features without affecting existing ones.

---

## Architecture Decision Records (ADRs)

Document important architectural decisions using ADRs. Template:

```markdown
# ADR-XXX: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-YYY]

## Context

What is the issue we're facing? What factors are driving this decision?

## Decision

What architecture or approach have we chosen?

## Consequences

### Positive

- Benefit 1

### Negative

- Trade-off 1

## Alternatives Considered

### Alternative 1: [Name]

- Pros: ...
- Cons: ...
- Why rejected: ...
```

When to write an ADR: choosing between architectural patterns; selecting third-party libraries or frameworks; deciding on data persistence strategy; choosing state management approach.

---

## Mobile-Specific Considerations

### iOS

- App lifecycle: handle background/foreground transitions
- Memory constraints: iOS aggressively terminates apps
- App Transport Security: HTTPS requirements
- Background execution limits: 30 seconds for most tasks

### Android

- Process death: system can kill app processes anytime
- Configuration changes: handle rotation and multi-window
- Background restrictions: Doze mode and app standby
- Jetpack Compose vs Views: modern UI toolkit adoption

### Cross-Platform

- **Offline-first**: Mobile networks are unreliable
- **Battery efficiency**: Minimize network calls and background work
- **Shared business logic**: Consider Kotlin Multiplatform Mobile

---

## Output Format

When designing architecture, produce:

1. **Architecture overview document** — system context, component diagram, key design decisions
2. **Detailed component specifications** — responsibilities, interfaces, dependencies, implementation notes
3. **UML diagrams** — component diagram for structure, sequence diagrams for key workflows, class diagrams for domain models
4. **Project structure** — directory organization, module boundaries, naming conventions
5. **ADRs** for significant decisions
