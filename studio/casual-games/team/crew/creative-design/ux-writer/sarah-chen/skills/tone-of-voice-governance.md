---
name: studio-creative-design-tone-of-voice-governance
description: Casual games studio tone-of-voice governance — defining voice principles, managing the studio style guide, running copy review gates across all player-facing content, coordinating VO and dialogue budgets, and maintaining brand voice consistency from prototype through live ops. Use when establishing or evolving the studio's voice, when reviewing copy from non-UX team members, or when onboarding the localization team to the studio's tone expectations.
version: "1.0.0"
---

# Tone-of-Voice Governance

## Purpose

Own and defend the studio's player-facing voice across every touchpoint — UI copy, tutorial dialogue, error messages, push notifications, offer copy, and event text. Voice consistency is not a nice-to-have; inconsistent voice signals an unprofessional product and creates localization debt when translators receive conflicting tone signals across strings. Sarah Chen is the single owner of voice standards for the Casual Games Studio.

## Voice Principles

The studio's voice is defined by four principles. Every piece of player-facing copy is evaluated against all four:

| Principle   | What It Means                                                                                                                                                       | Pass Example                                              | Fail Example                                                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Warm**    | Friendly without being infantile. The game respects the player's intelligence while still being approachable.                                                       | "Tap to play again"                                       | "Oopsie! Try again! 🎉"                                                                                                            |
| **Direct**  | Say exactly what you mean in as few words as possible. Never pad copy to fill space.                                                                                | "No internet connection. Check your Wi-Fi and try again." | "It seems like there might be a connectivity issue at this time. Please verify your internet connection and attempt to reconnect." |
| **Playful** | Light touch of personality in non-critical contexts (victory messages, level intros). Never playful in error states or transactional copy (purchases, permissions). | "Level complete! You're on fire 🔥"                       | "Please authorize credit card expenditure to finalize transaction 🎮"                                                              |
| **Clear**   | Player always knows what will happen next. CTAs are specific actions ("Play Level 5"), not vague ("OK", "Continue", "Next").                                        | "Start Level 5"                                           | "Continue"                                                                                                                         |

## Studio Style Guide

Sarah owns the Studio Style Guide in Confluence. It is a living document updated any time a new content pattern is established. Minimum required sections:

### 1. Voice Principles (above)

### 2. Grammar and Mechanics

| Rule                            | Standard                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Sentence case for all UI labels | "Play level" not "Play Level"                                                                           |
| No Oxford comma in UI           | "Gold, gems and lives"                                                                                  |
| Numbers as numerals from 1      | "3 lives remaining" not "Three lives remaining"                                                         |
| Contractions                    | Always prefer: "You're" not "You are", "Can't" not "Cannot" — except in legal/permissions text          |
| Punctuation on tooltips/toasts  | No terminal period on single-sentence tooltips                                                          |
| Exclamation marks               | Maximum 1 per screen; zero in error states                                                              |
| Ellipsis                        | Use only for truncated text that continues; never for atmosphere ("Loading…" OK, "Almost there…" avoid) |

### 3. Terminology Glossary

A controlled vocabulary for game-specific nouns. Once a term is in the glossary, it is locked — no synonyms in copy:

```markdown
| Term     | Use                             | Never Use                                         |
| -------- | ------------------------------- | ------------------------------------------------- |
| Lives    | The player's remaining attempts | Hearts (unless game art uses hearts specifically) |
| Coins    | Primary soft currency           | Money, cash, credits                              |
| Gems     | Premium hard currency           | Diamonds, crystals, jewels                        |
| Level    | A discrete playable challenge   | Stage (reserved for pipeline usage), Map, Round   |
| Power-up | A temporary ability enhancement | Boost, Buff, Special                              |
```

### 4. Screen-Type Templates

Standard voice pattern per screen type:

```markdown
**Empty States:**
Format: "[Object] noun + [Action] verb"
Example: "No items yet. Visit the shop to get started."
Never: "Nothing here!" / "Empty!" (too blunt) or long explanations

**Error States:**
Format: "[What happened] + [What to do]"
Example: "Purchase didn't go through. Check your payment details and try again."
Never: Apologize or use exclamation marks

**Success States:**
Format: "[Achievement] + [Reward/Next step]"
Example: "Level complete! You earned 120 coins."
Playfulness: Allowed here, but keep it 3 words max of personality

**Permissions (Camera, Notifications, etc.):**
Format: "[Specific use case] + [Benefit to player]"
Example: "Turn on notifications to know when your lives are restored."
Never: Generic "Allow notifications to get a better experience"
```

## Copy Review Gates

### Gate 1 — In-Sprint Copy Review (48-hour SLA)

All copy written by non-UX team members (game designers, engineers, producers who write placeholder text) must be reviewed by Sarah before it appears in any testable build.

Submission: Drop copy in the `#copy-review` Slack channel with context (screen name, player state, string key).

Sarah's review output: `Approved` / `Revised: [corrected version]` / `Blocked: [reason — usually missing context or voice violation]`.

### Gate 2 — Prototype Review (Stage 2)

Before the playable prototype is reviewed by leadership, Sarah reviews all player-facing strings in the build. She produces a **Copy Audit Report**:

```markdown
# Copy Audit Report — [Prototype Version]

| String Key         | Current Text       | Issue                                                       | Recommendation                                      |
| ------------------ | ------------------ | ----------------------------------------------------------- | --------------------------------------------------- |
| btn_play_again     | "Try Again?"       | Question mark creates uncertainty; punctuation inconsistent | "Try Again"                                         |
| msg_level_complete | "CONGRATULATIONS!" | All caps; exclamation already conveys enthusiasm            | "Congratulations!"                                  |
| err_no_connection  | "Error 404 😢"     | Error code visible to player; emoji in error state          | "No internet. Check your connection and try again." |
```

The Copy Audit Report is submitted to the Lead Game Designer (Mei Watanabe) before the Stage 2 review with the Creative Director.

### Gate 3 — Localization Handoff Review

Before strings are exported to the TMS, Sarah reviews the full string file for:

- All placeholders use the `%s` / `{variable_name}` format (not `{{variable_name}}` or custom formats)
- No string longer than 80 characters without explicit expansion budget in comments
- All gendered forms marked with appropriate metadata flags
- Tone notes added as `developer-comment` for any string that requires cultural adaptation beyond literal translation

## In-Game Dialogue and VO

For casual games with dialogue (tutorial characters, mascots, event narratives):

### Dialogue Length Budgets

| Context                   | Max Word Count                        | Rationale                                                |
| ------------------------- | ------------------------------------- | -------------------------------------------------------- |
| Tutorial tooltip          | 12 words                              | Player is learning; every extra word increases skip rate |
| Character bark (gameplay) | 5 words                               | Interrupts flow if longer                                |
| Event narrative screen    | 40 words                              | Player is engaged; can support context                   |
| VO line (spoken)          | 8 seconds at natural pace (~20 words) | VO budget constraint                                     |

### VO Review Process

When VO is in scope, Sarah coordinates with Hiroshi Nakamura (Composer/Sound Director) on:

1. Script delivery: Sarah provides finalized script with pacing notes (pause marks, emphasis)
2. Pre-record review: Audio Designer reviews for technical pronunciation; Sarah reviews for tone
3. Post-record review: Sarah reviews recording against script and voice principles before sign-off

## Quality Standards

- Studio Style Guide reviewed and updated at the start of every new project
- 100% of in-sprint copy reviewed within 48 hours of submission
- Zero untranslatable strings (formatting issues, embedded text in images) reach the TMS export
- Copy Audit Report delivered before every Stage 2 prototype review
- No more than one voice-principle violation open per sprint (track in Jira with `voice-debt` label)
