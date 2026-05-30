---
name: studio-art-art-team-leadership
description: Art team leadership for a 6-person mobile game art division — weekly art reviews, art direction communication, pipeline governance, mentorship, and cross-discipline collaboration standards for casual game production. Owned by Renaud Leclercq (Art Director). Trigger: art team, art review, art direction, art leadership, team management, art pipeline governance, creative feedback.
version: "1.0.0"
---

# Art Team Leadership

**Skill Owner:** Renaud Leclercq (Art Director)
**Applies To:** Art Division (6 direct reports), Stage 0–5 Art Deliverables

## Art Team Structure

Renaud manages 6 direct reports across 5 specializations:

| Role               | Person                        | Primary Responsibilities                                       |
| ------------------ | ----------------------------- | -------------------------------------------------------------- |
| Technical Artist   | Lena Kovac                    | Shaders, art pipeline tools, DCC integration, mobile rendering |
| UI Visual Artist   | Elena Morozova                | UI/UX visual design, iconography, HUD elements                 |
| Motion/UI Animator | Marco Bellini                 | UI animations, VFX integration, character/motion animation     |
| 3D Artist (×2)     | Anya Petrova, Tomasz Kowalski | Character models, environment assets, props                    |
| VFX Artist         | Javier Moreno                 | Particle effects, visual feedback, hit effects                 |

## Weekly Art Review Process

The weekly art review is the primary quality gate for art production. Renaud adopted this process from Supercell, where it was adopted studio-wide:

### Review Structure (Every Monday, 60 minutes)

| Segment            | Duration | Purpose                                                                           |
| ------------------ | -------- | --------------------------------------------------------------------------------- |
| Stage check-in     | 10 min   | Each artist shares what shipped last week and what's in progress this week        |
| In-progress review | 35 min   | Artists present WIP assets; Renaud gives structured feedback (see below)          |
| Reference sharing  | 10 min   | Renaud shares new reference images, competitor analysis, or style evolution notes |
| Action items       | 5 min    | Each artist leaves with explicit revision notes logged in Confluence              |

### Feedback Framework (3-Level Structured Critique)

1. **What's working** — explicitly name what the artist got right (no empty praise — specific observations only)
2. **What to iterate** — specific, actionable revision notes. Not "this doesn't feel right" — instead "the specular highlight on this character's shield reads as plastic rather than metal — increase the roughness value and reference the shield in [reference sheet]"
3. **Priority** — P0 (blocks pipeline), P1 (must fix before Stage gate), P2 (improve if time allows)

All feedback is logged in Confluence on the asset's page by the end of the review session.

## Art Direction Communication

### Style Guide Ownership

Renaud authors and maintains the **Art Style Guide** from Stage 0. Every stylistic decision made during Stage 0 is documented with:

- Reference images (what to emulate)
- Anti-reference images (what to avoid)
- Technical specifications (color palette, texture resolution guidelines, character silhouette rules)

The Style Guide is the authoritative reference. Any artist uncertain about a creative direction consults the Style Guide first, then asks Renaud.

### Cross-Discipline Creative Communication

| Situation                                            | Renaud's Role                                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Engineering needs art for a prototype                | Renaud provides the lowest-fidelity placeholder that communicates the intent          |
| Design requests a new UI element mid-production      | Renaud evaluates scope impact and communicates timeline estimate within 24 hours      |
| Technical constraint conflicts with visual direction | Renaud and Lena Kovac find the highest-quality solution within the performance budget |
| Creative Director overrides an art decision          | Renaud implements immediately and logs the decision in the Art Decision Log           |

## Mentorship Obligations

As the Art Director, Renaud maintains the following mentorship obligations:

- Monthly 1:1 with each direct report: career goals, craft development, blockers
- Quarterly "craft deep-dive": Renaud teaches one art or leadership skill in a 60-minute workshop format (shared with full team)
- For junior artists: structured feedback on every asset they produce during their first 6 months (beyond the weekly review)

## Measurable Quality Standards

| Standard                           | Target                   | Measurement Method                    |
| ---------------------------------- | ------------------------ | ------------------------------------- |
| Weekly art review held on schedule | 100% of production weeks | Confluence meeting record             |
| Review feedback documented         | 100% of reviewed assets  | Confluence action items               |
| Art assets delivered on schedule   | ≥90% on time per sprint  | Jira sprint report                    |
| P0/P1 art QA failures at Stage 6   | 0                        | Stage 6 (Automated Testing) QA report |
| Artist satisfaction (1:1 survey)   | ≥4.0/5.0                 | Quarterly team survey                 |
