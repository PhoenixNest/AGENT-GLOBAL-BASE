---
name: studio-art-animation-specs
description: Documentation of animation specifications for engineering handoff — easing curves, duration tokens, 60fps targets, and graceful degradation for low-end devices. Owned by Marco Bellini (Motion/UI Animator). Use during Studio Pipeline Stages 4–5 for animation spec creation and engineering handoff. Trigger: animation specs, easing curves, duration tokens, animation handoff, 60fps animation, graceful degradation, animation documentation.
version: "1.0.0"
---

# Animation Specs

**Skill ID:** animation-specs
**Role:** Motion/UI Animator
**Seniority:** Senior

## Overview

Documentation of animation specifications for engineering handoff — easing curves, duration tokens, 60fps targets, and graceful degradation for low-end devices.

## Tools & Frameworks

| Tool           | Proficiency  | Use Case                                  |
| -------------- | ------------ | ----------------------------------------- |
| Google Sheets  | Expert       | Animation spec documentation              |
| Figma          | Advanced     | Visual reference for animation behavior   |
| Unity Profiler | Intermediate | Verifying animation performance in-engine |

## Spec Format

Each animation spec includes:

| Field              | Example Value                     |
| ------------------ | --------------------------------- |
| Animation Name     | `button-press-feedback`           |
| Duration           | 150ms                             |
| Easing Curve       | cubic-bezier(0.25, 0.1, 0.25, 1)  |
| Start State        | Button at scale 1.0, opacity 1.0  |
| End State          | Button at scale 0.95, opacity 0.9 |
| Keyframes          | 3 (press, hold, release)          |
| Performance Budget | ≤ 1ms CPU, ≤ 0.5ms GPU            |
| Low-End Fallback   | Scale only, no opacity change     |
| Accessibility Note | Respect reduced-motion preference |

## Scenarios & Trade-offs

### Scenario 1: Animation Spec Library for Engineering

- **Approach:** Create comprehensive spec document with all animations, organized by screen/context, with visual references and parameter values
- **Trade-off:** Specification completeness vs. engineering implementation flexibility — overly prescriptive specs may limit engineer problem-solving
- **Quality Bar:** Every animation has a spec; specs are testable (engineer can verify duration and easing match spec)

### Scenario 2: Graceful Degradation for Low-End Devices

- **Approach:** Define 3 animation quality tiers — high (60fps, all effects), medium (30fps, simplified effects), low (static states only)
- **Trade-off:** Visual consistency vs. device performance — low-end players get reduced experience
- **Quality Bar:** Core gameplay animations preserved at all tiers; decorative effects are first to be reduced

## Quality Standards

- All animations documented with easing curves (not just "ease in/out")
- Duration tokens reference design system values (fast/medium/slow)
- Performance budget specified per animation (CPU/GPU time)
- Low-end fallback defined for every animation
- Accessibility: reduced-motion preference respected

## Industry References

- Google's Material Design motion system
- Apple's Human Interface Guidelines — Animation
- Unity's animation performance best practices
