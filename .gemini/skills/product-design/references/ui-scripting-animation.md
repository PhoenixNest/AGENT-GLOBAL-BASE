---
name: studio-engineering-ui-scripting-animation
description: UI scripting and animation for mobile games — C# UI scripting, Spine 2D integration, automated UI testing, bug fixing for game interfaces. Owned by Ryu Tanaka (Gameplay Engineer). Use during Studio Pipeline Stages 2–5 for UI development and Stage 6 (Automated Testing) for UI regression testing. Trigger: UI scripting, Spine animation, UI testing, Unity UI Toolkit, UI bug fixing, animation integration.
version: "1.0.0"
---

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

## Cross-Team Handoff and Collaboration

Ryu's UI work is inherently collaborative — animation specs come from the creative side, assets come from visual design, and test coverage is validated with QA. The following protocols govern each cross-team relationship.

### With Marco Bellini (Motion/UI Animator)

Marco Bellini (Motion/UI Animator, Creative-Design division) authors the animation specification documents that define timing, easing curves, and state transitions for UI animations. Ryu implements these specs in Unity.

**Collaboration protocol:**

1. **Marco delivers the animation spec doc** — format: timing values, curve references, state machine diagram, and reference video.
2. **Ryu implements in Unity** — using Spine 2D skeletal rigs or Unity's Animator, depending on the animation type (Spine for complex 2D character/icon animations; Animator for simple UI state transitions).
3. **Marco reviews Unity playback** — Marco reviews the implementation for timing accuracy, easing correctness, and visual fidelity against the spec.
4. **Ryu adjusts** — addresses any discrepancies Marco identifies.
5. **Joint sign-off** — both Ryu and Marco sign off before the animation enters the main branch; Ryu's sign-off confirms implementation correctness, Marco's confirms creative fidelity.

### With Amara Osei (Lead QA Engineer)

The claim that Ryu's work achieves an **"85% UI regression pass rate"** carries a specific meaning: 85% of Ryu's UI screens are covered by automated regression tests that run in CI. This coverage is not provided by the QA team — it is authored by Ryu alongside the UI features he builds.

**Protocol:**

- Ryu writes automated UI regression tests (using Appium + Unity Test Runner) **as part of each UI feature's development**, not as an afterthought.
- At Stage 6 (Automated Testing), **Amara Osei reviews Ryu's test coverage** — she verifies that the 85% screen coverage threshold is met and that the test suite correctly validates the intended UI behaviour.
- If coverage falls below threshold, Amara returns the Stage 6 submission to Ryu with a remediation request; Ryu adds the missing tests before Stage 6 can pass.

### With Elena Morozova (UI Visual Artist)

Elena Morozova (UI Visual Artist, Art division) produces the visual assets that Ryu integrates into Unity — button sprites, panel backgrounds, icon atlases, and similar static UI elements.

**Protocol:**

- Elena delivers assets via the studio's asset handoff pipeline (source format + export specs).
- If an asset **requires animation support** — for example, a button with a press/hover/disabled state animation, or an icon that pulses on unlock — Ryu and Elena **align before implementation**. This alignment conversation establishes: whether the animation is driven by Spine rig (Elena prepares accordingly), Unity Animator, or shader-based effect (Ryu specifies requirements to Lars Johansson if GPU-side).
- Ryu raises animation requirements early enough that Elena can incorporate them into the asset production schedule, rather than retrofitting animation support after an asset is delivered.
