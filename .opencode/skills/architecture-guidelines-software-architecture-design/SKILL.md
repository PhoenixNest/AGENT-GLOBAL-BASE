---
name: architecture-guidelines-software-architecture-design
description: "Architecture skill: Software Architecture Design"
---

# Software Architecture Design

## Purpose

Design scalable, maintainable software architectures for mobile and backend systems. Produce clear architectural documentation including UML diagrams, component designs, and logical project structures that guide engineering teams toward high-quality implementations.

## When to Use This Skill

Use this skill when:

- A new system or major feature requires architectural design
- Existing architecture needs refactoring or modernization
- Teams need clarity on system structure and component interactions
- Architecture decisions need to be documented and justified
- Project structure needs to be organized logically
- Cross-team alignment on technical approach is required

## Architecture Design Process

### 1. Understand Requirements and Constraints

Before designing, gather:

- **Functional requirements**: What must the system do?
- **Non-functional requirements**: Performance, scalability, security, reliability targets
- **Platform constraints**: iOS/Android versions, device capabilities, network conditions
- **Team constraints**: Team size, skill levels, existing codebases
- **Business constraints**: Timeline, budget, compliance requirements

### 2. Define Architecture Principles

Establish guiding principles for this system:

- **Modularity**: How will we decompose the system into manageable pieces?
- **Separation of concerns**: How do we keep business logic separate from UI and infrastructure?
- **Testability**: How will we make this easy to test?
- **Scalability**: How will this handle growth?
- **Maintainability**: How will future engineers understand and modify this?

### 3. Design the System Structure

Create the high-level architecture:

- **Layers**: Presentation, business logic, data access, infrastructure
- **Modules/Components**: Major functional units with clear responsibilities
- **Boundaries**: What are the interfaces between components?
- **Data flow**: How does information move through the system?

### 4. Document with UML Diagrams

Use appropriate UML diagrams to communicate the design.

## UML Diagram Types and When to Use Them

### Component Diagrams

**Purpose**: Show high-level system structure and dependencies between major components.

**When to use**:

- Explaining overall system architecture
- Showing how modules relate to each other
- Documenting deployment boundaries
- Planning modularization or refactoring

**Example structure**:

```
[UI Layer] --> [Business Logic Layer] --> [Data Layer]
[Business Logic] --> [Network Service]
[Business Logic] --> [Local Storage]
```

### Class Diagrams

**Purpose**: Show object-oriented structure with classes, attributes, methods, and relationships.

**When to use**:

- Designing domain models
- Documenting API structures
- Planning inheritance hierarchies
- Showing design patterns in use

**Key elements**:

- Classes with attributes and methods
- Relationships: inheritance, composition, aggregation, association
- Interfaces and abstract classes
- Visibility modifiers (public, private, protected)

### Sequence Diagrams

**Purpose**: Show how objects interact over time for a specific scenario.

**When to use**:

- Documenting complex workflows
- Showing API call sequences
- Explaining authentication flows
- Debugging timing or ordering issues

**Key elements**:

- Actors and objects as vertical lifelines
- Messages/calls as horizontal arrows
- Activation boxes showing when objects are active
- Return values and async operations

### Activity Diagrams

**Purpose**: Show workflow or business process flow.

**When to use**:

- Documenting user journeys
- Showing decision logic
- Planning state machines
- Explaining algorithms

## Mobile Architecture Patterns

### iOS Architecture Patterns

**MVC (Model-View-Controller)**:

- Traditional iOS pattern
- ViewController handles both view and controller logic
- Good for simple screens, can become bloated

**MVVM (Model-View-ViewModel)**:

- ViewModel handles presentation logic
- View binds to ViewModel (using Combine or RxSwift)
- Better testability than MVC
- Good for complex UI with lots of state

**VIPER (View-Interactor-Presenter-Entity-Router)**:

- Highly modular, each component has single responsibility
- More boilerplate but excellent for large teams
- Clear boundaries make testing easier

**Composable Architecture (TCA)**:

- Unidirectional data flow
- State management with reducers
- Excellent for complex state and side effects
- Steep learning curve but very maintainable

### Android Architecture Patterns

**MVVM with Android Architecture Components**:

- ViewModel + LiveData/StateFlow
- Repository pattern for data access
- Room for local storage
- Current Android best practice

**MVI (Model-View-Intent)**:

- Unidirectional data flow
- Immutable state
- Good for complex state management
- Works well with Jetpack Compose

**Clean Architecture**:

- Layered approach: Presentation, Domain, Data
- Dependency inversion (inner layers don't depend on outer)
- Highly testable and maintainable
- More initial setup but scales well

## Logical Project Structure

Organize code to reflect architecture:

### iOS Project Structure Example

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

### Android Project Structure Example

```
com.myapp/
├── app/
│   └── MainActivity.kt
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

**Key principles**:

- **Feature-based organization**: Group by feature, not by layer
- **Clear boundaries**: Each feature is self-contained
- **Shared code**: Common utilities in dedicated modules
- **Scalability**: Easy to add new features without affecting existing ones

## Architecture Decision Records (ADRs)

Document important architectural decisions using ADRs.

### ADR Template

```markdown
# ADR-XXX: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-YYY]

## Context

What is the issue we're facing? What factors are driving this decision?

## Decision

What architecture or approach have we chosen?

## Consequences

What are the positive and negative outcomes of this decision?

### Positive

- Benefit 1
- Benefit 2

### Negative

- Trade-off 1
- Trade-off 2

## Alternatives Considered

What other options did we evaluate and why did we reject them?

### Alternative 1: [Name]

- Pros: ...
- Cons: ...
- Why rejected: ...
```

### When to Write an ADR

- Choosing between architectural patterns (MVC vs MVVM vs VIPER)
- Selecting third-party libraries or frameworks
- Deciding on data persistence strategy
- Choosing state management approach
- Making infrastructure decisions (CI/CD, deployment)

## Design for Mobile Platforms

### iOS-Specific Considerations

- **App lifecycle**: Handle background/foreground transitions
- **Memory constraints**: iOS aggressively terminates apps
- **App Transport Security**: HTTPS requirements
- **Background execution limits**: 30 seconds for most tasks
- **SwiftUI vs UIKit**: Choose based on minimum iOS version
- **Combine vs async/await**: Modern concurrency patterns

### Android-Specific Considerations

- **Process death**: System can kill app processes anytime
- **Fragment lifecycle**: Complex lifecycle management
- **Configuration changes**: Handle rotation and multi-window
- **Background restrictions**: Doze mode and app standby
- **Jetpack Compose vs Views**: Modern UI toolkit adoption
- **Kotlin Coroutines**: Structured concurrency

### Cross-Platform Considerations

- **Shared business logic**: Consider Kotlin Multiplatform Mobile
- **Platform-specific UI**: Native UI usually provides better UX
- **API design**: Design APIs that work well on both platforms
- **Offline-first**: Mobile networks are unreliable
- **Battery efficiency**: Minimize network calls and background work

## Architecture Quality Attributes

Evaluate designs against these criteria:

**Modularity**: Can components be developed and tested independently?

**Testability**: Can we write unit tests without complex setup?

**Scalability**: Can this handle 10x growth in users or features?

**Maintainability**: Can new engineers understand and modify this?

**Performance**: Does this meet latency and throughput requirements?

**Security**: Are we protecting user data appropriately?

**Reliability**: What happens when things fail?

## Diagramming Tools

**PlantUML**: Text-based UML diagrams, version control friendly
**Mermaid**: Markdown-compatible diagrams, renders in GitHub
**Lucidchart**: Visual diagramming tool, good for collaboration
**Draw.io**: Free, open-source diagramming
**Enterprise Architect**: Professional UML tool for complex systems

## Output Format

When designing architecture, produce:

1. **Architecture overview document** with:
   - System context and requirements
   - High-level architecture description
   - Component diagram showing major pieces
   - Key design decisions and rationale

2. **Detailed component specifications** with:
   - Responsibility of each component
   - Interfaces and contracts
   - Dependencies
   - Implementation notes

3. **UML diagrams** appropriate to the design:
   - Component diagram for structure
   - Sequence diagrams for key workflows
   - Class diagrams for domain models

4. **Project structure** showing:
   - Directory organization
   - Module boundaries
   - Naming conventions

5. **ADRs** for significant decisions

The documentation should enable engineering teams to implement the architecture with confidence and consistency.
