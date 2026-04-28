---
name: studio-creative-design-game-ux-microcopy
description: Writing player-facing microcopy for mobile games — button labels, tooltips, error states, tutorial text, notification copy, and reward messages with tone-of-voice consistency. Owned by Sarah Chen (UX Writer). Use during Studio Pipeline Stages 1–5 for UX copy design and A/B testing. Trigger: microcopy, UX writing, button labels, tutorial text, error states, notification copy, FTUE copy, player-facing text.
version: "1.0.0"
---

# Game UX Microcopy

## Description

Specialized skill in writing player-facing microcopy for mobile games — button labels, tooltips, error states, tutorial text, notification copy, and reward messages. Focuses on reducing cognitive load, guiding player behavior, and maintaining tone-of-voice consistency across all player touchpoints.

## Tools & Frameworks

| Tool / Framework      | Version Context                               | Usage Scenario                                                                        |
| --------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------- |
| Figma                 | v120+ (2026) — component text workflows       | Writing copy directly in design components; testing text overflow across screen sizes |
| Notion / Zeroheight   | Current (2026)                                | Content design system documentation, style guide maintenance                          |
| A/B Testing Platforms | Firebase Remote Config, Optimizely            | Testing copy variants with statistical rigor (p < 0.05, 80% power)                    |
| Player Com Testing    | 5-user moderated playtest protocol            | Validating copy comprehension before ship                                             |
| String Key Management | Custom taxonomy (module.screen.element.state) | Organizing copy for developer handoff and TMS integration                             |

## Real-World Production Scenarios

### Scenario 1: FTUE Copy Redesign

**Context:** Player drops off during first-time user experience because tutorial text is too dense, uses jargon, and doesn't scaffold learning progressively.
**Approach:** Break tutorial into 3–5 word progressive disclosures. Each screen teaches one concept. Use active voice ("Tap the gem to collect it") instead of passive ("The gem can be collected by tapping"). Test with 5 users; measure comprehension score (can they perform the action without help?).
**Outcome:** 11% reduction in FTUE drop-off, 22% improvement in comprehension scores.

### Scenario 2: Error State Recovery

**Context:** Players encounter network errors, session timeouts, or failed purchases and see generic messages ("Error occurred" / "Something went wrong") that don't guide recovery.
**Approach:** Write error states that answer three questions: (1) What happened? (2) Is my progress safe? (3) What do I do next? Example: "Connection lost — your progress is saved. Tap Resume to continue playing."
**Outcome:** 18% reduction in support tickets related to error confusion.

### Scenario 3: Reward Notification Optimization

**Context:** Players receive rewards but don't feel the emotional impact because notification copy is transactional ("You received 50 coins") rather than celebratory.
**Approach:** A/B test 3 variants of reward copy. Variant A: transactional. Variant B: enthusiastic ("Amazing! 50 coins are yours!"). Variant C: personalized + enthusiastic ("You earned 50 coins! Keep it up!"). Measure retry rate and session length post-reward.
**Outcome:** Variant C increased retry rate by 8% and extended average session length by 1.2 minutes.

## Trade-Off Analysis

| Trade-Off                           | Decision Framework                                                                 | Example                                                                                                                 |
| ----------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Brevity vs. Clarity**             | If comprehension score < 4/5, add words. If > 4.5/5, cut words.                    | "Tap to continue" (3 words, clear) vs. "Please tap the button to proceed to the next screen" (12 words, clear but slow) |
| **Personality vs. Universality**    | Personality in celebratory contexts. Universality in error/instructional contexts. | "You crushed it! 🎉" (celebration) vs. "Connection lost — tap to retry" (error, no emoji)                               |
| **Cultural Specificity vs. Global** | Flag idioms, wordplay, and culture-specific references for localization review.    | "Hit a home run!" (US-specific) → "You nailed it!" (more universal)                                                     |
| **Designer Preference vs. Data**    | A/B test both. Let the numbers decide.                                             | Designer wants clever pun; writer wants clear label → test both, ship winner                                            |

## Measurable Quality Standards

| Metric                   | Target                                 | Measurement Method                                |
| ------------------------ | -------------------------------------- | ------------------------------------------------- |
| Comprehension Score      | ≥ 4/5 (5-user test)                    | Moderated playtest — can player act without help? |
| Text Overflow Incidents  | 0 in production                        | QA check across all supported screen sizes        |
| Localization Query Rate  | ≤ 2 queries per 100 strings            | TMS query tracking                                |
| A/B Test Win Rate        | ≥ 60% of tested variants beat baseline | Statistical analysis (p < 0.05)                   |
| Support Ticket Reduction | ≥ 15% for copy-related tickets         | Support ticket categorization                     |

## Industry Best Practice References

| Reference                                   | Source                         | Application                                  |
| ------------------------------------------- | ------------------------------ | -------------------------------------------- |
| "Writing is Designing"                      | Michael J. Metts & Andy Welfle | Foundational text for UX writing principles  |
| GDC 2025: "Microcopy That Retains"          | Sarah Chen                     | Game-specific microcopy impact measurement   |
| Nielsen Norman Group: UX Writing Guidelines | NN/g                           | General UX writing best practices            |
| Apple HIG: Typography & Language            | Apple Developer                | Platform-specific copy conventions (iOS)     |
| Material Design: Writing for Material       | Google                         | Platform-specific copy conventions (Android) |
| "Content Design"                            | Sarah Richards                 | Government-to-game content design transfer   |
| UX Writing Conf proceedings (2023–2025)     | Various                        | Current trends in game UX writing            |
