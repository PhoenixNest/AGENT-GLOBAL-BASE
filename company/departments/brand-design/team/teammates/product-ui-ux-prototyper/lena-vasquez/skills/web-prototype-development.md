---
name: web-prototype-development
description: Production-grade interactive web prototype development for mobile product requirements. Covers single-file HTML prototype construction, gesture simulation, micro-animations, platform-specific component implementation, and browser-runnable handoff for engineering review.
version: "1.0.0"
---

# Web Prototype Development

## Purpose

Translate product requirements (PRD) into production-grade, browser-runnable interactive web prototypes delivered as single HTML files. Every prototype must be openable on a mobile device browser with no build step, fully covering all PRD requirements, and annotated with platform-specific interaction notes for iOS and Android.

## Why This Matters

Validates functional requirements and design style before engineering investment. A production-grade prototype catches 70% of UX issues before code is written, saving 3-5 days of rework per feature.

## Prototype Standards

### File Format

- Single `.html` file with all CSS and JavaScript embedded inline — no external dependencies, no build toolchain required
- Runnable on iOS Safari and Android Chrome without modification
- File name: `prototype-v{n}-{feature-slug}.html`

### Fidelity Requirements

- High-fidelity visual design: correct typography, spacing, colour system, iconography
- Gesture simulation: tap, swipe, long-press, pinch interactions implemented in JavaScript
- State coverage: all major UI states represented (empty, loading, error, populated, edge cases)
- Micro-animations: transitions between states at spec-correct duration and easing
- Responsive: adapts correctly to common iOS and Android screen sizes (375pt, 390pt, 412dp, 360dp)

### Platform Annotation

Every interactive component must carry inline comments or a visible legend distinguishing:

- iOS-specific behaviour (per HIG: swipe-back navigation, bottom sheet gestures, Dynamic Type)
- Android-specific behaviour (per Material Design 3: predictive back gesture, bottom nav, adaptive layouts)
- Shared behaviour (identical on both platforms)

## Workflow

### Step 1: PRD Intake

- Read the full PRD provided by the CPO
- Identify all product requirements, user flows, and edge cases
- Flag any requirements that are ambiguous or under-specified before beginning — resolve with CPO

### Step 2: Visual Research

- Browse Dribbble, Mobbin, and Layers for design inspiration relevant to the product domain
- Identify 3–5 reference designs that inform the visual direction
- Document references in a comment block at the top of the HTML file

### Step 3: Prototype Construction

- Build the prototype as a single HTML file
- Implement all major user flows as interactive paths
- Cover all states defined in the PRD
- Annotate platform-specific behaviours inline

### Step 4: Self-Review Against PRD

Before submitting, verify:

- [ ] Every PRD requirement has a corresponding prototype screen or flow
- [ ] All edge cases identified in Step 1 are represented
- [ ] Platform annotations are present on every interactive component
- [ ] File opens correctly on mobile browser without errors

### Step 5: Submit to CDO

- Deliver the prototype HTML file to the Chief Design Officer for review
- Attach a brief cover note: requirements covered, design references used, known gaps or deferred items

## Revision Loop

If the CDO returns the prototype for revision:

1. Note every piece of feedback precisely
2. Implement all changes
3. Increment the version number in the file name
4. Re-submit

The loop repeats until CDO, CPO, CTO, and CIO all approve.

## IDS Handoff Trigger

Upon user final confirmation of the approved prototype, this skill hands off to `interaction-design-specification.md` to produce the Interaction Design Specification before delivery to R&D.
