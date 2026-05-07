---
inclusion: fileMatch
fileMatchPattern: "**/gdd.md,**/gds.md,**/game-design/**"
description: Game design document patterns and best practices
version: "1.0.0"
---

# Game Design Document Patterns

**Authority:** Casual Games Studio design standards  
**Applies To:** All game design documentation in the Casual Games Studio

---

## GDD (Game Design Document) Structure

### Required Sections

#### 1. Game Overview

- **Game Title:** Working title and final title (if different)
- **Genre:** Primary and secondary genres
- **Platform:** Target platforms (iOS, Android, PC, etc.)
- **Target Audience:** Age range, demographics, player motivations
- **Unique Selling Points:** What makes this game special?

#### 2. Game Concept

- **High Concept:** One-sentence description
- **Core Gameplay Loop:** What does the player do repeatedly?
- **Game Pillars:** 3-5 core design principles
- **Inspiration:** Reference games and what we're learning from them

#### 3. Gameplay Mechanics

- **Core Mechanics:** Primary player actions and interactions
- **Secondary Mechanics:** Supporting systems and features
- **Controls:** Input mapping and control schemes
- **Difficulty Curve:** How challenge scales over time

#### 4. Game Systems

- **Progression System:** How players advance and unlock content
- **Economy System:** Currencies, resources, and their flow
- **Reward System:** What players earn and when
- **Social Features:** Multiplayer, leaderboards, guilds, etc.

#### 5. Content Structure

- **Levels/Stages:** Number and variety of levels
- **Characters:** Playable and non-playable characters
- **Items/Collectibles:** What players can collect or use
- **Environments:** Settings and locations

#### 6. Monetization Design

- **Business Model:** Free-to-play, premium, subscription, etc.
- **IAP (In-App Purchases):** What can players buy?
- **Ad Integration:** Where and when ads appear
- **Conversion Funnels:** How we guide players to spend

#### 7. Meta Game

- **Long-Term Goals:** What keeps players engaged beyond core loop?
- **Events:** Limited-time events and seasonal content
- **Collections:** Long-term collection mechanics
- **Achievements:** Achievement system design

#### 8. User Experience

- **Onboarding:** How new players learn the game
- **UI/UX Flow:** Screen flow and navigation
- **Feedback Systems:** How the game communicates to players
- **Accessibility:** Features for players with disabilities

#### 9. Technical Considerations

- **Performance Targets:** Frame rate, memory, battery usage
- **Platform Requirements:** Minimum OS versions, device specs
- **Network Requirements:** Online/offline functionality
- **Data Storage:** Save system and cloud sync

#### 10. Competitive Analysis

- **Competitor Games:** Similar games in the market
- **Market Positioning:** How we differentiate
- **Lessons Learned:** What we're taking from competitors

## GDS (Game Design Specification) Structure

The GDS is a more detailed, technical document that expands on the GDD:

### Required Sections

#### 1. Detailed Mechanics Specification

- **Formulas:** Mathematical formulas for game systems
- **State Machines:** Behavior state machines for characters/systems
- **Data Tables:** Spreadsheets for balancing (damage, health, costs, etc.)
- **Edge Cases:** How systems handle unusual situations

#### 2. Content Specifications

- **Level Design:** Detailed level layouts and objectives
- **Character Stats:** Complete stat sheets for all characters
- **Item Database:** Full item list with properties
- **Dialogue Scripts:** All in-game text and dialogue

#### 3. UI/UX Specifications

- **Screen Mockups:** Wireframes or mockups for all screens
- **Interaction Flows:** Detailed user flow diagrams
- **Animation Specifications:** UI animation timing and easing
- **Localization Notes:** Text that needs special handling

#### 4. Audio Specifications

- **Music Tracks:** List of music tracks and where they play
- **Sound Effects:** Complete SFX list with trigger conditions
- **Voice Over:** VO script and character casting notes
- **Audio Mixing:** Volume levels and audio priorities

#### 5. Art Specifications

- **Art Style Guide:** Visual style reference and guidelines
- **Asset List:** Complete list of required art assets
- **Animation List:** All character and object animations
- **VFX List:** Visual effects and particle systems

## Design Patterns for Casual Games

### Core Loop Design

**Effective Core Loops:**

1. **Match-3:** Match → Clear → Cascade → Reward
2. **Merge:** Merge → Unlock → Expand → Merge
3. **Idle:** Collect → Upgrade → Automate → Prestige
4. **Puzzle:** Solve → Progress → Unlock → Solve

**Core Loop Principles:**

- Should be completable in 30-60 seconds
- Should be satisfying and rewarding
- Should have clear goals and feedback
- Should scale in complexity over time

### Progression Design

**Progression Layers:**

1. **Short-Term:** Level completion, immediate rewards
2. **Medium-Term:** Chapter completion, character unlocks
3. **Long-Term:** Collections, achievements, mastery

**Progression Pacing:**

- Early game: Fast progression, frequent rewards
- Mid game: Balanced progression, strategic choices
- Late game: Slow progression, prestige systems

### Monetization Design

**F2P Best Practices:**

- **Value Proposition:** Players should feel they're getting value
- **Non-Intrusive:** Don't interrupt core gameplay
- **Optional:** Never require payment to progress
- **Fair:** Avoid pay-to-win mechanics

**IAP Categories:**

1. **Consumables:** Currencies, boosters, lives
2. **Durables:** Characters, skins, permanent upgrades
3. **Subscriptions:** Battle pass, VIP membership
4. **Bundles:** Starter packs, limited-time offers

### Retention Design

**Day 1 Retention (Target: 40%+):**

- Smooth onboarding (< 2 minutes)
- Quick wins and rewards
- Clear next steps
- Compelling hook

**Day 7 Retention (Target: 20%+):**

- Meaningful progression
- New content unlocks
- Social features
- Daily rewards

**Day 30 Retention (Target: 10%+):**

- Deep meta game
- Live events
- Community features
- Prestige systems

## Balancing Guidelines

### Economy Balancing

**Currency Flow:**

- **Sources:** Where players earn currency
- **Sinks:** Where players spend currency
- **Balance:** Ensure sinks > sources to create scarcity

**Pricing Formula:**

```
Price = Base_Cost × (Multiplier ^ Level)
```

Example: Upgrade costs increase exponentially

### Difficulty Balancing

**Difficulty Curve:**

- Start easy (success rate: 90%+)
- Gradually increase (success rate: 70-80%)
- Occasional difficulty spikes for variety
- Never impossible (success rate: > 50%)

### Reward Balancing

**Reward Frequency:**

- Small rewards: Every 30-60 seconds
- Medium rewards: Every 5-10 minutes
- Large rewards: Every 30-60 minutes
- Epic rewards: Daily or weekly

## Playtesting Guidelines

### Internal Playtesting

- **Frequency:** Weekly during production
- **Duration:** 30-60 minute sessions
- **Focus:** Specific features or systems
- **Feedback:** Structured feedback forms

### External Playtesting

- **Frequency:** Monthly or at milestones
- **Duration:** 1-2 hour sessions
- **Focus:** Overall experience and fun factor
- **Feedback:** Surveys and interviews

### Metrics to Track

- **Engagement:** Session length, sessions per day
- **Retention:** D1, D7, D30 retention rates
- **Monetization:** Conversion rate, ARPDAU, LTV
- **Progression:** Level completion rates, time to complete
- **Friction Points:** Where players quit or get stuck

## Documentation Best Practices

### Writing Style

- Use clear, concise language
- Include visual aids (diagrams, mockups, flowcharts)
- Use examples to illustrate concepts
- Keep it up-to-date as design evolves

### Version Control

- Use version numbers (v1.0, v1.1, v2.0)
- Track major changes in changelog
- Archive old versions for reference
- Use collaborative tools (Google Docs, Confluence)

### Collaboration

- Share early and often with team
- Incorporate feedback from all disciplines
- Use design reviews for major decisions
- Document design rationale

## Related Steering Files

- `casual-games-pipeline.md` — Studio pipeline overview
- `unity-development.md` — Unity implementation patterns

## Related Skills

- `.kiro/skills/game-development/` — Game development domain skills
  - `studio-leadership.md`
  - `live-ops-strategy.md`

## Resources

- Game Design Patterns: https://gameprogrammingpatterns.com/
- F2P Design: https://www.deconstructoroffun.com/
- GDC Vault: https://www.gdcvault.com/
