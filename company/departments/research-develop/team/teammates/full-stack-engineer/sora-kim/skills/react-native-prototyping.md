---
version: "1.0.0"
---

| Competency                 | Description                                                                                      | Quality Criteria                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Component Architecture     | Functional components, hooks, context, custom hooks, component composition                       | Designs reusable component library; implements custom hooks for shared logic; uses composition over inheritance                           |
| Native Module Bridges      | Native module creation, promise-based APIs, event emitters, type-safe bridges                    | Creates native modules for platform-specific features; implements TypeScript interfaces for native APIs; handles native errors gracefully |
| Document Scanning          | react-native-vision-camera integration, frame processing, edge detection, perspective correction | Implements camera-based document scanning with real-time preview; integrates with document processing backend                             |
| Biometric Authentication   | Face ID, Touch ID, fingerprint, fallback flows, secure storage                                   | Implements biometric auth with graceful fallback; stores sensitive data in Keychain/Keystore; handles enrollment flows                    |
| Cross-Platform UI Patterns | Platform-specific styling, responsive layouts, accessibility, dark mode                          | Designs UI that adapts to both platforms; implements proper accessibility; supports dynamic color schemes                                 |

## Pipeline Integration

**Stage 5 (Development):** Component library implemented with cross-platform support. Native modules built for both iOS and Android. Document scanning integrated with frame processing. Biometric auth with fallback flows.

**Stage 6 (Code Review):** Review native module TypeScript interfaces. Validate cross-platform UI consistency. Check accessibility implementation. Verify permission handling.

**Stage 7 (Testing):** Component unit tests. Native module integration tests. E2E tests with Detox. Accessibility audits.

## Quality Standards

| Metric                        | Target                      | Measurement               |
| ----------------------------- | --------------------------- | ------------------------- |
| Cross-platform UI consistency | < 5% visual difference      | Visual regression testing |
| Native module crash rate      | 0 crashes                   | Crash reporting           |
| Biometric auth fallback       | 100% users can authenticate | Auth flow testing         |
| Document detection accuracy   | > 90% confidence            | Detection metrics         |
| Accessibility score           | WCAG 2.1 AA                 | Accessibility audit       |
| App startup time (cold)       | < 2 seconds                 | Performance monitoring    |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
