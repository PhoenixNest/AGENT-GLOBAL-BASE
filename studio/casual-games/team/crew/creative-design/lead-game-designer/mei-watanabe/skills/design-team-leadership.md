---
name: studio-creative-design-design-team-leadership
description: Lead Game Designer team leadership for the Casual Games Studio — supervising four design ICs (Senior Designer, Level Designer, UX Writer, Economy Designer), running design review rituals, defining quality standards, delegating with traceability, and managing production-phase design throughput. Use when leading the design team through a pipeline stage, reviewing IC deliverables, or managing design capacity across a sprint.
version: "1.0.0"
---

# Design Team Leadership

## Purpose

Mei Watanabe leads four design ICs: Lisa Henderson (Senior Game Designer), Marcus Thompson (Level Designer), Sarah Chen (UX Writer), and Kwame Asante (Economy Designer). This skill defines how she leads them — not just what she designs herself. Leadership at this level means: clear ownership assignments, regular feedback rituals, actionable quality standards, and a design production cadence that does not bottleneck the engineering team.

## IC Ownership Model

Each IC owns a specific design domain. Mei's job is to set the creative direction and quality bar, not to do the work herself during full production. Exceptions: Mei designs directly at Stage 1 (GDD authorship) and Stage 2 (prototype) because the creative foundation requires lead-level ownership before delegation is possible.

| IC                               | Domain Ownership                                           | Stage Ownership | Mei's Role                                                                                                            |
| -------------------------------- | ---------------------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------- |
| Lisa Henderson (Senior Designer) | Overall systems design, economy/monetization design        | 1, 2, 5, 10     | Direction-setting at Stage 1–2; feedback at Stage 5; escalation path at Stage 10                                      |
| Marcus Thompson (Level Designer) | Level design, encounter design, playtesting facilitation   | 2, 3, 5         | Quality bar for level design; sign-off on level design principles document                                            |
| Sarah Chen (UX Writer)           | Player-facing copy, localization-ready text, tone-of-voice | 2, 5            | Ensures copy aligns with game feel and creative vision; escalates copy/gameplay intent conflicts to Creative Director |
| Kwame Asante (Economy Designer)  | Virtual economy, pricing, balancing                        | 1, 5, 8, 10     | Economy strategy alignment with Lead Game Designer's systems vision; review at Stage 1 and Stage 8                    |

## Design Review Ritual

### Weekly Design Review (45 minutes)

Every Tuesday. All four ICs attend. Format:

1. **(5 min)** What did each IC complete this week?
2. **(25 min)** Rotating show-and-tell: one IC presents current work; others + Mei give structured critique
3. **(10 min)** Upcoming priorities for the week; dependency calls with Engineering and Art
4. **(5 min)** Blockers surface — Mei resolves or escalates to Creative Director same day

**Critique standard:** Critique is always tied to the GDD, PRD, or stage specification — not personal preference. Mei models this and enforces it: "Does this design serve [mechanic X] as written in the GDD, Section 4.2?" not "I don't like this."

### Bi-weekly 1:1s

30 minutes with each IC, alternating week from the team review. Covers:

- What's going well?
- What's blocked or uncertain?
- Is their craft growing in the direction they want?
- Any changes needed in how Mei is supporting them?

1:1 notes are documented in Confluence so Mei can track growth and recurring themes over time.

## Quality Standards for IC Deliverables

Before Mei approves any IC deliverable for stage advancement, she checks:

| Criterion                   | What Mei Reviews                                                                               | Action if Missing                             |
| --------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **GDD/PRD alignment**       | Does the deliverable implement the agreed design intent?                                       | Revise with explicit GDD section reference    |
| **Completeness**            | Are all states, edge cases, and failure scenarios addressed?                                   | Revise — incomplete designs block engineering |
| **Measurability**           | Does the deliverable include testable success metrics?                                         | Revise — "fun" is not measurable              |
| **Localization-readiness**  | Does any text in the deliverable meet the UX Writer's string length and placeholder standards? | Route to Sarah Chen before approval           |
| **Economy coherence**       | Does the design add any currency sinks, sources, or soft barriers?                             | Route to Kwame Asante before approval         |
| **Engineering feasibility** | Has the design been reviewed by the Lead Engineer for Stage 5 feasibility?                     | Schedule feasibility call if not done         |

## Production-Phase Design Throughput (Stage 5)

During Stage 5 (Full Production), Mei shifts from "creator" to "quality guardian." The ICs generate most design output; Mei reviews, unblocks, and escalates.

**Sprint design throughput targets:**

| IC              | Sprint Deliverable Expectation                                | Mei's Review SLA                          |
| --------------- | ------------------------------------------------------------- | ----------------------------------------- |
| Lisa Henderson  | 1 system design doc or 2 economy tuning specs                 | Within 48 hours of submission             |
| Marcus Thompson | 3–5 level layouts or 1 level design principles doc            | Within 48 hours                           |
| Sarah Chen      | All copy for the sprint's new screens + 1 localization review | Within 24 hours (copy blocks engineering) |
| Kwame Asante    | 1 economy health report + tuning recommendations              | Within 48 hours                           |

**Escalation rule:** If Mei cannot review within the SLA due to capacity, she delegates the review to Lisa Henderson (Senior Designer) and notifies the Creative Director.

### Design Debt Triage

During Stage 5, design debt accumulates. Mei tracks it in Jira with a `design-debt` label:

| Priority                | Example                                                          | Triage Action                                                |
| ----------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------ |
| P1 (blocks engineering) | Missing state in a screen engineers are implementing this sprint | Resolve within the sprint — Mei designs directly             |
| P2 (degrades quality)   | Inconsistent icon usage, non-standard spacing                    | Schedule for next sprint; assign to relevant IC              |
| P3 (polish)             | Micro-interaction polish                                         | Backlog; address in Stage 6 remediation cycle or post-launch |

## Delegation Principles

- **Delegate with context:** When assigning a design task, Mei always provides: the GDD/PRD section the design serves, the constraints (screen real estate, engineering complexity), the success criteria, and the deadline
- **No silent rewrites:** If Mei disagrees with an IC's direction, she raises it in review — she does not quietly redesign the work without telling them. That undermines ownership and growth
- **Credit the work:** IC deliverables are attributed to the IC in all stage documentation — not to Mei

## Quality Standards

- All four ICs have 1:1s every two weeks without exception
- No IC deliverable advances to stage review without Mei's explicit approval signature in Confluence
- Design debt tracked in Jira; zero P1 design-debt items open at any sprint review
- Every delegation includes GDD/PRD reference, constraints, success criteria, and deadline
- Mei's review SLAs met ≥90% of sprints; any miss is flagged to the Creative Director
