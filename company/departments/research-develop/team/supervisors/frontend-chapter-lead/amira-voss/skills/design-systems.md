---
name: design-systems
description: Production design system engineering — three-tier token architecture (primitive → semantic → component) with Style Dictionary transforms, composable component library design, IDS traceability matrices, semantic versioning with breaking-change governance, cross-platform consistency across iOS/Android/Web, and Storybook-based documentation with visual regression gating. Use when building, maintaining, or auditing a shared design system or component library, especially when bridging CDO/IDS specifications to engineering implementation.
version: "1.0.0"
---

# Design Systems

| Competency                     | Description                                                                                   | Quality Criteria                                                                                           |
| ------------------------------ | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Design Token Architecture**  | Multi-tier token systems (primitive → semantic → component) with platform-specific transforms | Tokens resolve correctly across iOS/Android/Web; zero manual color/spacing overrides in component code     |
| **Component Library Design**   | Composable, accessible component APIs with strict variant/prop contracts                      | Components pass axe-core automated tests; Storybook stories cover 100% of documented IDS states            |
| **Design-to-Code Handoff**     | Bidirectional traceability between IDS specifications and component implementations           | Every IDS spec maps to a component; every component traces back to an IDS spec section                     |
| **Versioning & Governance**    | Semantic versioning for design tokens and components with breaking change protocols           | Zero breaking changes shipped without major version bump; deprecation notices issued 2 sprint cycles ahead |
| **Cross-Platform Consistency** | Platform-specific implementations sharing a unified design language                           | Visual regression diffs < 2px across platforms; platform conventions respected (HIG vs Material)           |
| **Storybook Ecosystem**        | Interactive documentation with accessibility testing, visual regression, and usage guidelines | Storybook coverage ≥ 95% of production components; all stories include accessibility annotations           |

## Execution Guidance

### Design Token Architecture

**Three-tier token model** — structure tokens to enable platform flexibility while maintaining design intent:

```
Primitive Tokens (Raw values)
  └─ color.blue.500 = #3B82F6
  └─ spacing.4 = 16px
  └─ font-size.md = 16px
       ↓
Semantic Tokens (Purpose-driven aliases)
  └─ color.action.primary = {color.blue.500}
  └─ spacing.component.md = {spacing.4}
  └─ font-size.body = {font-size.md}
       ↓
Component Tokens (Component-specific overrides)
  └─ button.primary.bg = {color.action.primary}
  └─ button.primary.padding = {spacing.component.md}
```

**Implementation decision criteria:**

- Use **Style Dictionary** (Amazon) for token transformation across platforms — it handles JSON → CSS custom properties, iOS `Color.swift`, Android `colors.xml`, and TypeScript type generation from a single source
- **Never** hardcode design values in component code — always reference semantic tokens; if a token doesn't exist, the design system is incomplete, not the component
- **Platform-specific token overrides** must be explicit: `token.ios.*` and `token.android.*` namespaces prevent accidental cross-platform leakage
- Token files should be co-located with the design system package, NOT scattered across feature modules — centralize in `packages/design-tokens/`

**Token governance workflow:**

1. CDO updates IDS → identifies new/changed token requirements
2. Frontend Chapter Lead creates token PR with Style Dictionary config
3. Token PR generates platform artifacts via CI pipeline
4. Component authors consume tokens via typed imports (`import { tokens } from '@company/tokens'`)
5. Visual regression tests validate token changes don't break existing components

### Component Library Architecture

**Component composition patterns** — choose the right pattern for the right use case:

| Pattern                    | Use Case                                                                    | Example                                         | Anti-pattern                                          |
| -------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------- |
| **Compound Components**    | Components with flexible internal structure (`Button.Icon`, `Button.Label`) | `Menu` / `Menu.Item` / `Menu.Trigger`           | Prop drilling 15+ props into a monolithic component   |
| **Render Props**           | Sharing behavior with custom rendering                                      | `Tooltip` that wraps arbitrary children         | Hiding component API behind function children         |
| **Headless + Styled**      | Shared logic, platform-specific presentation                                | `@radix-ui/primitive` + custom styling          | Bundling styles with logic, preventing customization  |
| **Slot-based Composition** | Flexible content placement with controlled layout                           | `Card` with `header`, `content`, `footer` slots | 20 optional props for every possible content position |

**Component API design rules:**

- **Props must be typed** with TypeScript discriminated unions for variant/size combinations — never use `string` for variant props
- **Every component must export** a `ComponentProps` type for downstream consumers who need to extend
- **Accessibility is non-negotiable:** every component must define its ARIA role, required states, and keyboard interaction model in its Storybook docs
- **Slot composition over prop composition:** prefer `<Card.Header>` over `<Card header={<Text>...` — it's more readable and enables better TypeScript inference
- **Escape hatches:** provide `className` (CSS) or `style` (inline) props for cases where consumers need one-off customization, but document that these bypass design system governance

**Cross-platform component strategy:**

- **Web-first components** are authored in React with CSS custom properties for theming
- **React Native** implementations consume the same token system via `react-native-style-dictionary` transform
- **Platform-specific components** (e.g., iOS-style segmented control vs Android-style tabs) should share a common interface but have separate implementations — never force one platform's pattern onto another
- Component interfaces must be defined in a shared `@company/component-types` package that both web and native implementations depend on

### Storybook as Design System Gateway

**Storybook configuration standards:**

- **Stories co-located** with component source: `Button.stories.tsx` next to `Button.tsx`
- **Story organization** mirrors component hierarchy: `components/atoms/`, `components/molecules/`, `components/organisms/`
- **Every story must include:**
  - Default export with component metadata (`title`, `component`, `argTypes`)
  - At minimum: `Default`, `AllVariants`, `Accessibility` stories
  - `play` functions for interactive stories (testing user flows within Storybook)
  - `parameters.a11y` configuration with axe-core ruleset
- **Visual regression testing** via Chromatic or Storybook's built-in `@storybook/test-runner` with Percy integration
- **Docs page auto-generated** from JSDoc comments and `argTypes` — supplement with custom MDX for usage guidelines, do/don't examples, and IDS traceability references

**IDS traceability in Storybook:**

```tsx
// Button.stories.tsx
export default {
  title: "Components/Atoms/Button",
  component: Button,
  parameters: {
    ids: {
      specRef: "IDS-SECTION-4.2", // Links to Interaction Design Specification
      cdoApproval: "2026-03-15", // Date of CDO design sign-off
      wcagLevel: "AA", // Accessibility compliance target
    },
    design: {
      type: "figma",
      url: "https://figma.com/file/.../Button?node-id=...",
    },
  },
  // ...
};
```

### Design-to-Code Handoff Protocol

**The handoff is a contract, not a hand-waving exercise:**

1. **CDO delivers** IDS document with component specifications (states, variants, interaction patterns, accessibility requirements)
2. **Frontend Chapter Lead** maps IDS sections to component inventory — creates a traceability matrix
3. **Each component implementation** must reference its IDS section in code comments and Storybook parameters
4. **CDO reviews** Storybook stories (not raw code) against IDS specifications during Stage 2 gate review
5. **Discrepancies** are logged as defects in Stage 6 Code Review with P1 severity if visual/interaction mismatch is > 2px or violates WCAG requirements

**Traceability matrix format:**

```markdown
| IDS Section | Component | Storybook Story   | Status | CDO Sign-off |
| ----------- | --------- | ----------------- | ------ | ------------ |
| 4.2         | Button    | Button.stories    | ✅     | 2026-03-15   |
| 4.3         | TextField | TextField.stories | 🟡     | Pending      |
| 4.4         | Modal     | Modal.stories     | ❌     | —            |
```

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                                                        | Deliverable                                       |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Collaborate with CDO to prototype components in HTML/CSS that validate IDS specifications before engineering          | HTML prototype components, token definitions      |
| **Stage 3** (Architecture)           | Define component library architecture in UML class diagrams; register ADRs for component composition patterns         | UML component diagrams, ADRs                      |
| **Stage 5** (Development)            | Implement design system package; publish to internal registry; ensure all platform teams consume design tokens        | `@company/design-system` package                  |
| **Stage 6** (Code Review)            | Review component implementations against IDS specifications; validate Storybook coverage and accessibility compliance | Design system review sign-off                     |
| **Stage 8** (Integrity Verification) | Verify all shipped UI components match CDO's IDS specifications; run visual regression suite                          | Integrity verification report for design fidelity |
| **Stage 10** (Release Readiness)     | Confirm design realization sign-off (Stage 10, Item 2: "all CDO/IDS specifications realised")                         | CDO release sign-off                              |

## Quality Standards

| Metric                         | Target                                                   | Measurement                                                                  |
| ------------------------------ | -------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Token coverage**             | 100% of design values tokenized                          | Grep audit: zero hardcoded `#hex`, `px`, `rem` values in component source    |
| **Component-IDS traceability** | 100% of components mapped to IDS sections                | Traceability matrix audit before Stage 6 gate                                |
| **Storybook coverage**         | ≥ 95% of production components documented                | `@storybook/test-runner` coverage report                                     |
| **Accessibility compliance**   | WCAG 2.1 AA for all components                           | axe-core automated tests + manual screen reader audit                        |
| **Visual regression**          | Zero unexpected diffs in Chromatic/Percy                 | CI pipeline blocks on visual diff threshold > 2px                            |
| **Cross-platform consistency** | Platform-specific deviations documented and CDO-approved | Deviation register maintained in design system docs                          |
| **Breaking change protocol**   | Zero undocumented breaking changes                       | Semantic versioning enforced via changesets; deprecation warnings in console |
| **Design system adoption**     | 100% of feature teams consume design system packages     | Package registry analytics; zero direct CSS/inline styles in feature code    |
