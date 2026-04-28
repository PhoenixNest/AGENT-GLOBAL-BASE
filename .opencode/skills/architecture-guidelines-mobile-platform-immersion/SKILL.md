---
name: architecture-guidelines-mobile-platform-immersion
description: Mobile platform immersion program for new engineer onboarding — structured 30-day learning path covering architecture, pipeline processes, quality standards, and platform-specific knowledge. Owned by Dr. Kenji Nakamura (CTO). Use during recruitment onboarding and ongoing team member development. Trigger: platform immersion, engineer onboarding, mobile onboarding, new hire training, immersion program.
prerequisites:
  - architecture-overview

version: "1.0.0"
---

# Mobile Platform Immersion Program

## Purpose

This skill defines the structured immersion program for new engineers joining the mobile product company. It accelerates onboarding from weeks to days by providing a curated learning path covering the company's architecture, pipeline processes, quality standards, and platform-specific knowledge. It is used by the CTO, platform leads, and CHRO (Dr. Evelyn Hartwell) during recruitment onboarding and ongoing team member development.

## Execution Guidance

### 1. Immersion Program Structure

The program is organized into four phases over the first 30 days:

**Phase 1 — Company Orientation (Days 1–3)**:

| Topic                  | Content                                                     | Delivering Officer |
| ---------------------- | ----------------------------------------------------------- | ------------------ |
| Company structure      | Department hierarchy, agent roles, pipeline overview        | CHRO               |
| 10-stage pipeline      | Stage definitions, gate criteria, artifact requirements     | CTO                |
| Defect severity system | P0–P3 classification, triage process, user authority        | Test Lead          |
| Quality standards      | Test pyramid, quality gates, regression testing requirement | Test Lead          |
| Security baseline      | SRD overview, MASVS, frontend security patterns             | CSO                |

**Phase 2 — Platform Deep Dive (Days 4–10)**:

| Topic                 | Content                                              | Delivering Officer |
| --------------------- | ---------------------------------------------------- | ------------------ |
| Architecture patterns | MVVM, Clean Architecture, modularization strategy    | Software Architect |
| Platform codebase     | Code walkthrough of assigned platform codebase       | Platform Lead      |
| Design system         | Component library, design tokens, IDS fluency        | CDO                |
| CI/CD pipeline        | Build process, test integration, deployment workflow | CTO                |
| Testing framework     | Unit, integration, E2E test structure and execution  | Test Lead          |

**Phase 3 — Hands-On Contribution (Days 11–20)**:

- Assign a **first contribution** — a small, well-defined task that touches the critical path (e.g., add a new component variant, fix a P3 defect, write unit tests for an existing module).
- Pair with a senior team member for code review guidance.
- The contribution must go through the full pipeline process: code review → tests → merge.
- Goal: experience the full development workflow end-to-end in a low-risk context.

**Phase 4 — Independent Work (Days 21–30)**:

- Transition to regular sprint assignments.
- Continue pairing for complex tasks.
- First solo code review with platform lead oversight.
- 30-day check-in with platform lead and CHRO to assess integration.

### 2. Platform-Specific Immersion Tracks

**Android Track**:

- Android architecture components (ViewModel, LiveData, Room, Navigation).
- Jetpack Compose fundamentals.
- Kotlin coroutines and Flow.
- Android testing (JUnit, Espresso, UiAutomator).
- Android build system (Gradle, ProGuard/R8).
- Google Play deployment process.

**iOS Track**:

- SwiftUI fundamentals.
- Combine framework for reactive programming.
- Core Data for local persistence.
- iOS testing (XCTest, XCUITest).
- Xcode build system and distribution.
- App Store Connect deployment process.

**Cross-Platform Track**:

- React Native / Flutter / KMP fundamentals (based on company's selection).
- Platform channel communication (native ↔ shared code).
- Cross-platform testing strategies.
- Build and deployment for both platforms.

### 3. Knowledge Verification

At the end of Phase 2, the new engineer completes a knowledge verification exercise:

- **Architecture quiz**: Identify architectural layers in a given code sample.
- **Pipeline simulation**: Walk through the artifacts required to advance from Stage N to Stage N+1 for a hypothetical feature.
- **Code review exercise**: Review a sample PR and identify defects using the P0–P3 classification system.
- **Security checklist walkthrough**: Review a feature against the frontend security checklist.

This is not a pass/fail exam — it identifies knowledge gaps that need addressing during Phase 3.

### 4. Mentorship Assignment

Every new engineer is assigned a mentor for the first 60 days:

- **Mentor role**: Senior team member on the same platform team.
- **Mentor responsibilities**: Daily check-ins during Phase 1–2, code review guidance during Phase 3–4, escalation point for technical questions.
- **Mentor time allocation**: 10–15% of mentor's time allocated to mentoring duties during the engagement.

### 5. Ongoing Development

After the initial 30-day immersion:

**Quarterly skill development**:

- Each engineer identifies one skill area for deepening (e.g., performance optimization, accessibility, security testing).
- Dedicate 10% of sprint capacity to skill development.
- Present learnings to the team at sprint review.

**Cross-platform exposure**:

- Engineers on one platform should periodically review code on other platforms.
- Encourage contributions to shared code (KMP shared modules, design system components).
- Annual rotation opportunity: spend one sprint on a different platform team.

**Conference and community**:

- Support attendance at mobile conferences (Droidcon, WWDC, React Native EU, Flutter Engage).
- Encourage open-source contributions to mobile libraries the company uses.
- Internal tech talks: monthly sessions where team members present on topics they've explored.

### 6. Immersion Program Metrics

Track these metrics to evaluate program effectiveness:

| Metric                           | Target      | Measurement                                         |
| -------------------------------- | ----------- | --------------------------------------------------- |
| Time to first PR merged          | <15 days    | Date of onboarding → date of first merged PR        |
| Time to independent contribution | <30 days    | Date of onboarding → date of first solo PR          |
| First-PR defect rate             | <3 comments | Number of review comments on first PR               |
| 90-day retention                 | >90%        | Engineers still active at 90 days / total onboarded |
| Program satisfaction             | >4/5        | Post-program survey score                           |

## Reference Materials

- Company pipeline definition (10 stages)
- Company personnel directory
- Platform-specific codebases
- Design system documentation
- Company quality engineering strategy
- Company security requirements and SRD
