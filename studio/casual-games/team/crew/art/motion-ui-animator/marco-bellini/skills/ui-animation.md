---
name: studio-art-ui-animation
description: Animation of game UI elements — button presses, screen transitions, reward celebrations, loading animations, and micro-interactions with mobile performance constraints. Owned by Marco Bellini (Motion/UI Animator). Use during Studio Pipeline Stages 3–5 for UI animation production. Trigger: UI animation, screen transitions, reward celebration, micro-interactions, DOTween, Spine 2D, easing curves.
version: "1.0.0"
---

# UI Animation

**Skill ID:** ui-animation
**Role:** Motion/UI Animator
**Seniority:** Senior

## Overview

Animation of game UI elements — button presses, screen transitions, reward celebrations, loading animations, and micro-interactions. Requires understanding of animation principles, mobile performance constraints, and player psychology.

## Tools & Frameworks

| Tool             | Proficiency | Use Case                                   |
| ---------------- | ----------- | ------------------------------------------ |
| Spine 2D         | Expert      | 2D skeletal animation for UI elements      |
| Unity Animator   | Expert      | State machine animation for UI transitions |
| After Effects    | Advanced    | Prototyping, motion design reference       |
| Lottie/Bodymovin | Advanced    | Vector animation export for UI             |
| DOTween          | Expert      | Code-based animation for Unity UI          |

## Scenarios & Trade-offs

### Scenario 1: Screen Transition System

- **Approach:** Design 5 transition types (slide, fade, zoom, flip, dissolve) with consistent timing (200–400ms) and easing curves
- **Trade-off:** Visual flair vs. perceived speed — overly elaborate transitions feel slow to players
- **Quality Bar:** All transitions feel snappy (≤ 400ms); easing curves match game personality; graceful degradation on low-end devices

### Scenario 2: Reward Celebration Animation

- **Approach:** Layered animation — screen shake, particle burst, number counter, sound sync, haptic feedback
- **Trade-off:** Excitement vs. repetition — celebrations must feel rewarding on first and 100th viewing
- **Quality Bar:** First-time celebration is 3+ seconds with full effects; repeat celebrations compress to 1.5 seconds with option to skip

## Quality Standards

- All animations target 60fps on mid-range devices (Snapdragon 730 / A12 Bionic)
- Easing curves documented with cubic-bezier values for engineering handoff
- Animation duration tokens defined in design system (fast: 150ms, medium: 300ms, slow: 500ms)
- All animations have skip/cancel support for accessibility

## Industry References

- Supercell's UI animation standards (snappy, clear, never obstructive)
- King's reward celebration design (layered, satisfying, skippable)
- Apple's iOS animation guidelines (easing, duration, spring physics)
