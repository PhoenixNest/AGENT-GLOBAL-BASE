---
name: design-to-engineering-handoff
description: Facilitate seamless design-engineering collaboration through technical design specs, implementation feasibility assessment, and handoff documentation that eliminates ambiguity
---

# Design-to-Engineering Handoff

## Purpose

Bridge the gap between design intent and engineering implementation through clear documentation, technical feasibility assessment, and collaborative problem-solving.

## When to Use

- Preparing designs for engineering handoff
- Assessing implementation feasibility of design concepts
- Resolving design-engineering conflicts
- Creating technical specifications for complex interactions
- Reviewing implementation against design specs

## Handoff Documentation Structure

### 1. Design Overview

```markdown
# [Feature Name]

## Business Context
- Problem: [What user problem does this solve?]
- Success Metrics: [How will we measure success?]
- Priority: [P0/P1/P2]

## Design Goals
- [Goal 1]
- [Goal 2]
- [Goal 3]

## Platform Scope
- iOS: [version support]
- Android: [version support]
```

### 2. Component Tree

```
Screen: [Name]
├── NavigationBar
│   ├── BackButton (tap → previous screen)
│   ├── Title (text: "...")
│   └── ActionButton (tap → [action])
├── ScrollView
│   ├── HeaderImage (320x180pt, aspect-fill)
│   ├── ContentStack
│   │   ├── Headline (SF Pro Display Bold 24pt)
│   │   ├── Body (SF Pro Text Regular 16pt)
│   │   └── CTAButton (tap → [action])
│   └── FooterLink (tap → [action])
└── LoadingOverlay (conditional)
```

### 3. Implementation Notes

**iOS Considerations:**

- Use SwiftUI/UIKit: [recommendation with rationale]
- Navigation: [push/modal/sheet]
- Data loading: [Combine/async-await]
- Caching strategy: [if applicable]

**Android Considerations:**

- Use Compose/Views: [recommendation with rationale]
- Navigation: [Fragment/Compose Navigation]
- Data loading: [Coroutines/Flow]
- Caching strategy: [if applicable]

### 4. API Requirements

```
Endpoint: GET /api/[resource]
Response: {
  "field1": "string",
  "field2": number,
  ...
}

Error Handling:
- 200: Success → show content
- 404: Not found → show empty state
- 500: Server error → show error with retry
- Network timeout → show offline message
```

## Feasibility Assessment Protocol

Before finalizing designs, assess with engineering:

**Technical Constraints:**

- [ ] Platform API availability (iOS/Android version support)
- [ ] Performance implications (rendering, memory, battery)
- [ ] Third-party dependencies required
- [ ] Backend API changes needed

**Implementation Complexity:**

- Simple (< 2 days): [list components]
- Medium (2-5 days): [list components]
- Complex (> 5 days): [list components]

**Risk Areas:**

- [ ] Custom animations (may need performance optimization)
- [ ] Complex gestures (may conflict with system gestures)
- [ ] Accessibility edge cases (screen reader navigation)
- [ ] Platform differences (iOS/Android parity challenges)

## Collaboration Workflow

1. **Design Draft** → Share early concepts with engineering for feasibility feedback
2. **Technical Review** → Walk through component tree, API needs, edge cases
3. **Spec Finalization** → Lock specifications, create Figma components
4. **Handoff** → Deliver complete documentation package
5. **Implementation Support** → Available for questions, review PRs
6. **QA Review** → Verify implementation matches specs

## Handoff Checklist

- [ ] Figma file organized with clear naming
- [ ] All states documented (default, loading, error, empty, disabled)
- [ ] Platform-specific variants specified
- [ ] Animations defined (duration, curve, properties)
- [ ] Accessibility requirements listed
- [ ] Component tree provided
- [ ] API requirements documented
- [ ] Edge cases identified
- [ ] Implementation notes included
- [ ] Engineering review completed

## Communication Guidelines

**When Design Needs to Push Back:**

- "This interaction pattern violates iOS HIG [section X] — users will expect [Y] instead"
- "Reducing this tap target below 44pt will fail accessibility review"
- "This animation duration feels wrong in user testing — can we try [X]ms instead?"

**When Engineering Pushes Back:**

- Listen to technical constraints
- Ask: "What's the blocker? Performance, API limitation, platform constraint?"
- Propose alternatives: "If [ideal] is too complex, would [simpler version] work?"
- Escalate if needed: "This is core to the user experience — let's discuss trade-offs with Product"

## Anti-Patterns

- **Throwing designs over the wall** — Collaborate throughout, don't disappear after handoff
- **Ignoring technical constraints** — If engineering says it's hard, believe them and find alternatives
- **Pixel-perfect obsession** — Focus on user experience, not matching Figma to the pixel
- **Missing edge cases** — Don't assume happy path; document errors, empty states, loading
