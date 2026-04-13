# UI Scripting & Animation

**Skill Owner:** Ryu Tanaka | **Version:** 1.0 | **Date:** 2026-04-20

## Description

UI scripting in C#, Spine 2D animation integration, automated UI testing, and bug fixing for mobile game interfaces.

## Tools & Frameworks

| Tool             | Version  | Context                         |
| ---------------- | -------- | ------------------------------- |
| Unity UI Toolkit | 2023 LTS | UI component framework          |
| Spine 2D         | 4.2      | 2D skeletal animation runtime   |
| C#               | 11.0     | UI scripting and event handling |
| Appium           | 2.0      | Automated UI testing            |

## Production Scenarios

**Scenario 1: UI Scripting Framework (Colopl 2024)** — Built data-bound UI framework for RPG with 200+ screens. Result: UI development speed increased 50%; bug count reduced 35%.
**Scenario 2: Automated UI Test Suite (Colopl 2024)** — Created automated UI regression testing. Result: 85% of UI regressions caught before QA; 300+ bugs fixed during live ops.

## Trade-offs

- Hand-coded UI vs visual editor → visual editor for speed; hand-coded for performance
- Spine vs Unity Animator → Spine for 2D; Animator for 3D

## Quality Standards

- UI frame budget: ≤ 8ms
- UI test coverage: ≥ 70% of screens
- Bug fix acceptance rate: ≥ 95%
- Animation smoothness: 60fps on mid-tier devices

## References

Unity UI Toolkit documentation; Spine runtime guide; "Automated Testing for Games" (GDC 2023)
