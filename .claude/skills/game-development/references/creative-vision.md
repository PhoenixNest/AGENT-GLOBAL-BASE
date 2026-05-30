---
name: creative-vision
description: Owns creative vision, art direction oversight, design quality, and Stage 0/1/2/3 creative deliverables. Defines visual pillars, co-authors GDD creative sections, directs prototype creative design, ensures vertical slice quality bar. Includes audio creative oversight (brief, direction, final approval) and UX writing creative alignment (voice drift prevention, copy for major narrative moments).
version: "1.0.0"
---

# Creative Vision

## Role

The Creative Director is the creative anchor of the studio. This skill covers the end-to-end creative leadership from Art Direction (Stage 0) through Vertical Slice (Stage 3), ensuring all creative work — art, design, narrative, audio — adheres to a unified vision.

## Pipeline Stage Ownership

| Stage | Name           | Responsibility                                                                                                 |
| ----- | -------------- | -------------------------------------------------------------------------------------------------------------- |
| 0     | Art Direction  | Defines visual pillars, approves art style guide and mood boards; owns the creative quality bar                |
| 1     | Concept        | Co-authors the GDD — creative vision, core gameplay loop, character/world design, narrative framework          |
| 2     | Prototype      | Directs prototype creative design — visual feel, audio atmosphere, UI/UX aesthetic, first-time user experience |
| 3     | Vertical Slice | Ensures the vertical slice meets the creative quality bar; approves all creative assets in the slice           |

## Execution Guidance

### Visual Pillar Development (Stage 0)

- Define 3–5 visual pillars that guide all creative decisions. Each pillar must be:
  - **Specific**: "Warm, inviting, lived-in" not "beautiful"
  - **Actionable**: Artists can design to it without interpretation ambiguity
  - **Differentiated**: Distinguishes the game from competitors in the same genre
- Create mood boards for each pillar with reference images from games, film, photography, and real-world sources
- Conduct "pillar stress tests": Take existing competitor games and evaluate whether they could pass your pillars. If yes, your pillars are not differentiated enough.

### Master Scene Methodology

- Before production begins, create one single scene — the hero moment of the game — at final production quality
- This scene includes: all visual effects, lighting, animation, UI polish, audio design
- Every team member uses the master scene as their quality reference during production
- New hires are onboarded by walking through the master scene with a senior artist
- Master scene is updated quarterly to reflect any shifts in creative direction

### Creative Conflict Resolution

- Use the "alternatives + data" framework: When creative team members disagree, each produces their preferred version AND a compromise version
- Playtest all variants with real players — the player is the tiebreaker, not the Creative Director
- Critique the work, never the person — this is a non-negotiable studio rule
- Weekly art crits (all artists, 60 min): Each artist presents work-in-progress, receives structured feedback
- Bi-weekly design reviews (design + art leads, 45 min): Review design-art integration points

### GDD Creative Authorship (Stage 1)

The Creative Director authors the following GDD sections:

- **Creative Vision Statement**: One paragraph describing the emotional experience the game delivers
- **Visual Pillars**: 3–5 pillars with mood board references
- **Core Gameplay Loop**: Player actions, feedback cycles, session structure
- **Character/World Design**: Character personalities, world lore, visual style
- **Narrative Framework**: Story structure, pacing, key narrative beats
- **First-Time User Experience**: Onboarding flow, tutorial approach, initial player motivation

### Quality Assurance Cadence

| Cadence                  | Audience           | Duration | Purpose                                                  |
| ------------------------ | ------------------ | -------- | -------------------------------------------------------- |
| Weekly art crits         | All artists        | 60 min   | Review work-in-progress, give structured feedback        |
| Bi-weekly design reviews | Design + art leads | 45 min   | Review design-art integration                            |
| Monthly playtests        | All studio         | 90 min   | Play current build, vote on top 3 issues                 |
| Quarterly vision reviews | Leadership         | 120 min  | Reaffirm or adjust visual pillars and creative direction |

## Audio Creative Oversight

Sakura's creative authority extends to audio. Audio is a creative dimension — a mismatched audio direction undermines every visual and design decision. Hiroshi Nakamura (Composer / Sound Director) is the technical and execution authority for audio; Sakura is the **creative authority**.

### Scope of Audio Creative Oversight

| Audio Area             | Sakura's Role                                                                              | Hiroshi's Role                                               |
| ---------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| **Music direction**    | Defines the emotional target for the game's soundtrack (genre, tempo, mood per game state) | Composes, arranges, and produces the music to Sakura's brief |
| **SFX palette**        | Sets the tonal register for sound effects (realistic, stylized, cartoon, premium)          | Designs and implements SFX that fulfill the tonal direction  |
| **VO direction**       | Defines character voice archetypes and delivery tone for any voiced content                | Casts, directs, and records VO                               |
| **Audio quality gate** | Final creative approval on all audio before it ships in any player-facing build            | Technical QA of audio files (loudness, format, loop points)  |

### Audio Alignment Process

1. At Stage 0 (Art Direction), Sakura writes a **Audio Direction Brief** alongside the Style Guide — 1 page defining the game's audio identity. Hiroshi builds his audio roadmap from this.
2. At Stage 2 (Prototype), Sakura reviews the first audio implementations against the brief. Any mismatch is flagged and revised before the Stage 2 playable review.
3. During Stage 5 (Full Production), Sakura reviews final audio implementations in the monthly playtest. Major audio decisions (new instruments, major SFX redesigns) require Sakura's approval before implementation.

## UX Writing Creative Alignment

Sarah Chen (UX Writer) owns voice standards and copy governance. Sakura is the **brand voice authority** — she defines the game's personality at the highest level; Sarah operationalizes it. This relationship prevents voice drift between the game's creative identity and its player-facing copy.

### How the Relationship Works

| Decision                                                                     | Owner                                             | Collaborator                                                        |
| ---------------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------- |
| Game's tone-of-voice pillars                                                 | Sakura (defines in GDD Creative Vision Statement) | Sarah (operationalizes in Style Guide)                              |
| New copy pattern for an uncharted screen type                                | Sarah (proposes, referencing GDD)                 | Sakura (approves or redirects if it conflicts with creative vision) |
| Copy for major narrative moments (event intros, boss defeats, story reveals) | Sakura (writes or approves)                       | Sarah (reviews for UX clarity and localization-readiness)           |
| Routine UI copy (buttons, tooltips, error states)                            | Sarah (owns entirely)                             | Sakura (spot-checks quarterly)                                      |

### Voice Drift Prevention

Sakura reviews Sarah's `tone-of-voice-governance.md` Style Guide at the start of every new project and whenever a major game update changes the creative identity. If the creative vision evolves (e.g., the game becomes more serious in tone for a narrative expansion), Sakura updates the GDD Creative Vision Statement and notifies Sarah within 48 hours to trigger a Style Guide revision.

## References

- `studio/casual-games/pipeline/casual-games-pipeline.md` — Studio 11-stage pipeline
- `company/pipeline/mobile-development/pipeline.md` — Parent company pipeline (Stage 2 Design, Stage 3 Architecture)
- `company/library/topics/localization.md` — Localization requirements that affect creative content structure
