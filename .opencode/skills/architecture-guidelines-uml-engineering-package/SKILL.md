---
name: architecture-guidelines-uml-engineering-package
description: 'Architecture skill: Uml Engineering Package'
---

# UML Engineering Package

## Purpose

Translate the approved web prototype, Interaction Design Specification (IDS), PRD, and SRD into a complete UML Engineering Package — the technical specification that the R&D Department implements against in Stage 5. Every diagram must be unambiguous: an engineer should be able to implement the system correctly from the UML alone, without requiring clarification.

## Package Contents

The UML Engineering Package consists of three diagram types plus a documentation layer.

### 1. Class Diagrams

Cover every major domain entity:

- All data models with fields, types, visibility modifiers, and relationships
- Inheritance hierarchies and interface implementations
- Associations, aggregations, and compositions with cardinality
- Platform-specific variants annotated (e.g., `// iOS only`, `// Android only`, `// Shared KMP`)

**Tooling:** PlantUML (`@startuml` / `@enduml`) — produce both source and rendered output.

**Minimum coverage:** One class diagram per domain layer (presentation, domain, data).

### 2. Sequence Diagrams

Cover every major user flow identified in the PRD and IDS:

- All participating actors (User, ViewModel, Repository, API, Database, etc.)
- Every message/call with method name and parameters
- Return values and their types
- Async operations marked with `async` / `await` notation
- Error paths: show what happens when each call fails

**Minimum coverage:** One sequence diagram per primary user flow; one additional diagram per significant error path.

### 3. Component Diagrams

Cover the overall system architecture:

- All major components (modules, layers, services, databases)
- Dependencies between components with direction arrows
- Interface boundaries (what each component exposes vs. consumes)
- Third-party dependencies called out explicitly (e.g., Firebase, RevenueCat, Stripe SDK)
- Platform deployment: which components are iOS-only, Android-only, or shared

**Minimum coverage:** One top-level system component diagram; one per major sub-system if complexity warrants.

### 4. Documentation Layer

Each diagram is accompanied by:

- **Purpose statement** — one sentence on what the diagram shows
- **Scope** — what is in scope and explicitly what is out of scope
- **Key decisions** — 2–3 sentences on non-obvious design choices and their rationale
- **Dependencies** — which ADRs or TSD entries govern decisions shown in this diagram
- **Open questions** — any unresolved design choices that require CTO/CIO review

## Authorship Workflow

### Step 1: Artifact Intake

Read in full, in order:

1. Final PRD (product requirements, user flows, data requirements)
2. SRD (security requirements — affect data model and API design)
3. Approved web prototype (visual structure informs component hierarchy)
4. IDS (interaction patterns inform ViewModel state machines and navigation stack)

### Step 2: Domain Modelling

- Identify all domain entities from the PRD
- Map relationships between entities
- Draft class diagram stubs before detailing methods

### Step 3: Flow Mapping

- List all user flows from PRD and IDS
- For each flow, identify all system participants
- Draft sequence diagrams top-down (happy path first, error paths second)

### Step 4: Component Decomposition

- Identify modular boundaries based on domain and team ownership
- Assign clean architecture layers: presentation / domain / data
- Map third-party dependencies to their integration points

### Step 5: CTO + CIO Joint Review

Before finalisation, submit draft package to CTO and CIO:

- Walk through each diagram
- Flag any open questions
- Incorporate feedback and regenerate affected diagrams

### Step 6: Feasibility Confirmation

After CTO + CIO review, confirm in writing:

- [ ] All PRD requirements are representable in the proposed architecture
- [ ] No technical constraint renders any requirement infeasible
- [ ] Package is ready for user submission

## Output Format

Deliver as a directory of PlantUML source files and rendered SVG/PNG exports, plus a `README.md` index:

```
uml-package/
  README.md               ← index of all diagrams with purpose statements
  class/
    class-domain.puml
    class-data.puml
    class-presentation.puml
  sequence/
    seq-[flow-name].puml  ← one file per flow
  component/
    component-system.puml
    component-[subsystem].puml
  rendered/               ← SVG exports of all diagrams
```
