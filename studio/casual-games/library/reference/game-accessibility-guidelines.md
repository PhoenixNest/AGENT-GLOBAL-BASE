# Game Accessibility Guidelines

**Last Updated:** April 9, 2026

---

## 1. Overview

Game accessibility extends beyond WCAG 2.1 AA (which applies to meta-UI screens) to include gameplay-specific accessibility that has no equivalent in standard applications. This document covers both domains.

### Two-Tier Accessibility Model

| Tier                 | Scope                                            | Standard                      | Applies To               |
| -------------------- | ------------------------------------------------ | ----------------------------- | ------------------------ |
| **Tier 1: Meta-UI**  | Menus, settings, store, onboarding, leaderboards | WCAG 2.1 AA                   | All non-gameplay screens |
| **Tier 2: Gameplay** | Core game experience, mechanics, feedback        | Game Accessibility Guidelines | All gameplay screens     |

---

## 2. Tier 1: Meta-UI Accessibility (WCAG 2.1 AA)

### 2.1 Visual Accessibility

| Criterion              | Requirement                                    | Implementation                                                 |
| ---------------------- | ---------------------------------------------- | -------------------------------------------------------------- |
| **Contrast ratio**     | ≥ 4.5:1 for text, ≥ 3:1 for UI elements        | Use contrast checker tools; test with dark/light backgrounds   |
| **Text scaling**       | Support up to 200% text enlargement            | Use Unity's TextMeshPro with dynamic sizing                    |
| **Color independence** | Color is not the only information carrier      | Add icons, patterns, or text labels alongside color indicators |
| **Focus indicators**   | Visible focus ring on all interactive elements | Outline or highlight on focused buttons/menu items             |
| **Motion reduction**   | Option to reduce/disable animations            | Settings toggle; respect OS-level Reduce Motion setting        |

### 2.2 Motor Accessibility

| Criterion                | Requirement                                             | Implementation                                         |
| ------------------------ | ------------------------------------------------------- | ------------------------------------------------------ |
| **Tap target size**      | ≥ 44×44 points (iOS HIG) / ≥ 48×48 dp (Material Design) | All buttons and interactive elements meet minimum size |
| **Touch target spacing** | ≥ 8 points between adjacent targets                     | Adequate padding between buttons                       |
| **Alternative input**    | Support external keyboards, switch control              | Unity Input System supports external input devices     |
| **Hold vs. tap toggle**  | Option to replace hold gestures with tap                | Critical for players with motor impairments            |

### 2.3 Auditory Accessibility

| Criterion              | Requirement                                            | Implementation                                   |
| ---------------------- | ------------------------------------------------------ | ------------------------------------------------ |
| **Captions/subtitles** | All spoken dialogue and important audio cues captioned | Text overlays for narrative content              |
| **Audio indicators**   | Visual indicators for audio-only cues                  | Flash, icon, or haptic feedback for audio events |
| **Volume controls**    | Separate controls for music, SFX, and voice            | Three-slider volume control in settings          |

### 2.4 Cognitive Accessibility

| Criterion                 | Requirement                                | Implementation                                       |
| ------------------------- | ------------------------------------------ | ---------------------------------------------------- |
| **Clear language**        | Simple, direct language in UI              | Avoid jargon; use icons + text                       |
| **Consistent navigation** | Same navigation pattern across all screens | Consistent tab bar or menu structure                 |
| **Error prevention**      | Confirm destructive actions                | "Are you sure?" dialogs for purchases, data deletion |
| **Time flexibility**      | No time limits on meta-ui interactions     | Menus and settings have no timers                    |

---

## 3. Tier 2: Gameplay Accessibility

### 3.1 Visual Accessibility (Gameplay)

| Feature                                | Implementation                                                                       | Priority                |
| -------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------- |
| **Colorblind modes**                   | 3 presets: Deuteranopia, Protanopia, Tritanopia — shift game-critical color palettes | **P0** — ship with game |
| **High contrast mode**                 | Alternative color scheme with maximum contrast between game elements                 | **P1**                  |
| **Brightness/gamma control**           | In-game brightness slider for players with low vision                                | **P1**                  |
| **Visual feedback for all audio cues** | Screen flash, icon, or particle effect for sound-based events                        | **P0**                  |
| **Scalable UI elements**               | Option to increase HUD element sizes                                                 | **P1**                  |

### 3.2 Motor Accessibility (Gameplay)

| Feature                         | Implementation                                                      | Priority |
| ------------------------------- | ------------------------------------------------------------------- | -------- |
| **One-hand mode**               | All core gameplay mechanics completable with single thumb           | **P0**   |
| **Adjustable tap target sizes** | Larger hitboxes for gameplay elements                               | **P1**   |
| **Hold-to-tap conversion**      | Replace rapid-tap or hold mechanics with single-tap alternatives    | **P1**   |
| **Auto-fire option**            | Optional automatic firing/interaction for rapid-tap mechanics       | **P2**   |
| **Input buffering**             | Tolerate slight timing imprecision in player input                  | **P1**   |
| **Remappable controls**         | Allow players to reassign gameplay actions to different input zones | **P2**   |

### 3.3 Cognitive Accessibility (Gameplay)

| Feature                     | Implementation                                                    | Priority |
| --------------------------- | ----------------------------------------------------------------- | -------- |
| **Adjustable game speed**   | 0.5×, 1×, 1.5×, 2× speed options                                  | **P1**   |
| **Pause anywhere**          | Game can be paused at any moment (except competitive multiplayer) | **P0**   |
| **Simplified UI mode**      | Removes non-essential visual elements, reduces cognitive load     | **P2**   |
| **Clear objective display** | Current goal always visible on screen                             | **P0**   |
| **Progressive difficulty**  | Game adapts difficulty based on player performance                | **P1**   |
| **Practice mode**           | Low-stakes environment to learn mechanics                         | **P2**   |

### 3.4 Auditory Accessibility (Gameplay)

| Feature                                  | Implementation                                                        | Priority |
| ---------------------------------------- | --------------------------------------------------------------------- | -------- |
| **Visual indicators for all audio cues** | Directional arrows, screen flash, icon overlay for sound-based events | **P0**   |
| **Subtitles for narrative content**      | All dialogue, narration, and story content subtitled                  | **P0**   |
| **Separate volume controls**             | Music, SFX, and voice volume independently adjustable                 | **P0**   |
| **Haptic alternatives**                  | Haptic feedback as substitute for audio feedback                      | **P1**   |

---

## 4. Minimum Accessibility Requirements

### 4.1 P0 (Must Ship)

| Feature                                                | Rationale                                          |
| ------------------------------------------------------ | -------------------------------------------------- |
| Colorblind mode (3 presets)                            | ~8% of male population has color vision deficiency |
| Screen reader support for meta-UI (VoiceOver/TalkBack) | Legal requirement in many jurisdictions            |
| ≥ 4.5:1 contrast ratio for all text UI                 | WCAG 2.1 AA requirement                            |
| One-hand mode (single-thumb completable)               | Core gameplay accessibility                        |
| Visual indicators for all audio cues                   | Deaf/hard-of-hearing players                       |
| Pause anywhere                                         | Cognitive accessibility                            |
| Clear objective display                                | Cognitive accessibility                            |
| Separate volume controls (music/SFX/voice)             | Standard accessibility expectation                 |

### 4.2 P1 (Ship Within 2 Updates)

| Feature                | Rationale                     |
| ---------------------- | ----------------------------- |
| High contrast mode     | Enhanced visual accessibility |
| Adjustable game speed  | Cognitive accessibility       |
| Hold-to-tap conversion | Motor accessibility           |
| Input buffering        | Motor accessibility           |
| Progressive difficulty | Cognitive accessibility       |
| Haptic alternatives    | Auditory accessibility        |

### 4.3 P2 (Roadmap)

| Feature             | Rationale                                 |
| ------------------- | ----------------------------------------- |
| Auto-fire option    | Motor accessibility (niche but important) |
| Remappable controls | Motor accessibility                       |
| Simplified UI mode  | Cognitive accessibility                   |
| Practice mode       | Cognitive accessibility                   |

---

## 5. Accessibility Testing

### 5.1 Testing Methods

| Method                           | Description                                                  | Frequency          |
| -------------------------------- | ------------------------------------------------------------ | ------------------ |
| **Automated contrast check**     | Scan all UI elements for contrast ratio compliance           | Every build        |
| **Colorblind simulation**        | Render game through colorblind filters in Editor             | Every art update   |
| **Screen reader testing**        | Test all meta-UI with VoiceOver (iOS) and TalkBack (Android) | Every UI update    |
| **One-hand playtest**            | Complete entire game using only one thumb                    | Every milestone    |
| **External accessibility audit** | Hire accessibility consultant for comprehensive review       | Before soft launch |

### 5.2 Accessibility Checklist per Release

| Check                                   | Pass Criteria         |
| --------------------------------------- | --------------------- |
| All text meets 4.5:1 contrast ratio     | Automated scan passes |
| Colorblind mode functional and tested   | Manual verification   |
| Screen reader navigates all menus       | Manual verification   |
| All audio cues have visual alternatives | Manual verification   |
| One-hand mode completable               | Manual verification   |
| Pause works in all game states          | Manual verification   |
| Objective always visible                | Manual verification   |
| Volume controls work independently      | Manual verification   |

---

## 6. External Resources

| Resource                         | Link                                                                                                  | Focus                                               |
| -------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Game Accessibility Guidelines    | https://gameaccessibilityguidelines.com/full-list/                                                    | Comprehensive game accessibility checklist          |
| AbilityPlay                      | https://abilityplay.org/                                                                              | Game accessibility research and resources           |
| Apple Accessibility for Games    | https://developer.apple.com/accessibility/                                                            | iOS accessibility guidelines                        |
| Google Accessibility             | https://developer.android.com/guide/topics/ui/accessibility                                           | Android accessibility guidelines                    |
| W3C WCAG 2.1 AA                  | https://www.w3.org/TR/WCAG21/                                                                         | Web Content Accessibility Guidelines (meta-UI tier) |
| "Accessibility Testing in Games" | https://blog.nashtechglobal.com/accessibility-testing-in-games-why-it-matters-and-how-to-do-it-right/ | Game testing best practices                         |

---

_End of Game Accessibility Guidelines_
