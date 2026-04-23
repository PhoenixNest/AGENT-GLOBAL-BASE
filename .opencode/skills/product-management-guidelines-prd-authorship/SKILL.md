---
name: product-management-guidelines-prd-authorship
description: "Product Management skill: Prd Authorship"
---

# PRD Authorship

Marcus writes every PRD himself — the first draft is never delegated. This is a deliberate practice rooted in the belief that the act of writing a PRD is a thinking process, not a documentation process. If you cannot write it clearly, you do not understand it clearly enough to build it.

This skill governs the structure, standards, and process Marcus uses to produce PRDs for the R&D team.

---

## PRD Philosophy

A PRD exists to align a cross-functional team on what to build, why to build it, what success looks like, and what done means. It is not a feature wish list. It is not a design spec. It is not a technical spec. It is the single source of truth that connects business intent to engineering execution.

A good PRD answers:

1. What problem are we solving, and for whom?
2. Why is this the right problem to solve now?
3. What are we building, at what scope?
4. How will we know it worked?
5. What are the platform-specific constraints that shape the solution?
6. What could go wrong, and how do we handle it?
7. What does done look like, and what triggers us to stop?

---

## Standard PRD Template

Every PRD Marcus writes follows this structure. Do not skip sections.

---

### 1. Header

```
Product: [Product / feature name]
Author: [Name]
Status: [Draft / In Review / Approved / In Development / Shipped / Sunset]
Last Updated: [Date]
Reviewers: [Engineering Lead, Design Lead, Data Science Lead, relevant stakeholders]
Platform: [iOS / Android / Both / Other]
```

---

### 2. Problem Statement (JTBD Framing)

Write in this format:

> When [situation], a [user type] wants to [motivation / job], so they can [expected outcome]. Currently, [what breaks or falls short about the existing experience].

**Good example:**

> When a new Duolingo user finishes their first lesson on iOS, a casual language learner wants to feel progress and understand what comes next, so they can build a habit around the app. Currently, the post-lesson screen shows a generic XP counter with no narrative connection to their goal, leading to 38% of users abandoning before setting a streak on Day 1.

**Do not write:**

> Users want a better onboarding experience.

---

### 3. Strategic Context

Answer in 3–5 sentences:

- Why is this the right problem to solve **now**?
- What company OKR or metric does this serve?
- What happens if we don't solve it?
- Is there a market, competitive, or platform timing reason this is urgent?

---

### 4. Scope Definition

Be explicit about what is in scope and what is not.

**In scope:**

- List specific features, user flows, or behaviors included

**Out of scope (explicitly):**

- List things that could be confused as in scope but are not
- Note follow-on work that will be a separate PRD

**Platform scope:**

- Which OS versions are supported? (e.g., iOS 16+, Android API 31+)
- Any device-specific constraints? (e.g., notch handling, foldable support)

---

### 5. Platform-Specific UX Constraints

For every mobile PRD, document:

**iOS:**

- Relevant HIG guidelines that apply
- App Store review considerations (if the feature touches payments, notifications, health data, or user-generated content)
- Haptic / gesture / navigation patterns required
- Any SwiftUI vs. UIKit considerations if known

**Android:**

- Material Design 3 component usage
- Back gesture behavior (edge-swipe vs. button)
- Notification channel requirements (if applicable)
- Minimum API level behavior differences

---

### 6. User Stories

Write in standard format:

> As a [user type], I want to [action], so that [outcome].

Include:

- Happy path (primary flow)
- At least two edge cases
- Empty/error state

**Edge Case Matrix** — for each edge case:

| Scenario                      | Expected Behavior                | Notes                       |
| ----------------------------- | -------------------------------- | --------------------------- |
| Network offline during action | Show cached state + retry prompt | Must not lose user progress |
| ...                           | ...                              | ...                         |

---

### 7. Metric Definitions and Instrumentation Spec

For every PRD, define:

**Primary metric:** What single number tells us if this worked?

- Name the metric
- Define it precisely (e.g., "30-day retention: % of users who open the app on day 30 after first install, measured on a rolling cohort basis")
- State the baseline and the target

**Guardrail metrics:** What must not get worse?

- List 2–3 guardrail metrics with acceptable degradation thresholds

**Instrumentation spec:**

- List every event that must be logged (event name, properties, trigger condition)
- Identify who is responsible for instrumentation: Product / Engineering / Data Science
- Confirm instrumentation is testable before launch gate

Example event:

```
Event: streak_recovery_tapped
Trigger: User taps "Restore Streak" button on Day N post-break
Properties:
  - user_id (string)
  - days_since_streak_break (integer)
  - streak_length_before_break (integer)
  - platform (iOS | Android)
  - screen_context (home | lesson_complete | notification_tap)
```

---

### 8. Technical Feasibility Pre-Assessment

Before finalizing the PRD, Marcus runs a working session with the engineering lead. Document the output:

**Complexity estimate:** S / M / L / XL

- S: < 1 sprint, no new infrastructure
- M: 1–2 sprints, may touch existing systems
- L: 3–5 sprints, requires new infrastructure or significant refactor
- XL: 6+ sprints, architectural change required

**Platform-specific risks:**

- List any known iOS-specific implementation risks
- List any known Android-specific risks (fragmentation, API differences)
- Flag any third-party dependency risks

**Open technical questions** (must be resolved before development starts):

- List each open question and the owner responsible for answering it

---

### 9. Launch Sequencing

Define the rollout plan:

| Phase            | Audience                                           | Criteria to Advance                                               |
| ---------------- | -------------------------------------------------- | ----------------------------------------------------------------- |
| Internal dogfood | Internal team                                      | No P0 bugs, instrumentation verified                              |
| 10% rollout      | iOS: 10% of US users / Android: staged rollout 10% | Primary metric moving in right direction, no guardrail regression |
| 50% rollout      | Same cohort expansion                              | 48-hour hold, no anomalies                                        |
| 100%             | Full release                                       | Sign-off from Marcus + Engineering Lead                           |

For App Store / Google Play submissions:

- Note review lead time buffer (iOS: +3 business days minimum)
- Confirm App Store metadata (screenshots, description) is updated if UI changes

---

### 10. Success and Kill Criteria

**Success:**

> This feature is considered successful if [primary metric] improves by [X%] within [measurement window] with no regression in [guardrail metric].

**Kill condition:**

> We will stop and roll back / sunset this feature if:
>
> - [Primary metric] does not improve by [threshold] after [window]
> - [Guardrail metric] degrades by more than [threshold]
> - A P0 platform issue is discovered that cannot be resolved within [timeframe]

**Measurement window:** [Specific date range or event-triggered window]

---

### 11. Dependencies and Risks

| Dependency           | Owner       | Risk if Delayed        |
| -------------------- | ----------- | ---------------------- |
| Backend API endpoint | Engineering | Blocks iOS development |
| ...                  | ...         | ...                    |

| Risk                | Likelihood | Mitigation                               |
| ------------------- | ---------- | ---------------------------------------- |
| App Store rejection | Medium     | Pre-review guidelines check in PRD phase |
| ...                 | ...        | ...                                      |

---

## PRD Review Process

Before a PRD is approved:

1. **Self-review** — Marcus reads the PRD 24 hours after writing it. Answers: "Would an engineer who has never spoken to me understand exactly what to build?"
2. **Engineering lead review** — Engineering lead signs off on feasibility pre-assessment and instrumentation spec
3. **Design lead review** — Design confirms UX constraints are correctly captured
4. **Data science review** — DS confirms metric definitions are measurable and instrumentation spec is complete
5. **Approval** — Marcus sets status to "Approved" only after all three reviews are complete

---

## Common PRD Failure Modes

Avoid these:

| Failure Mode                        | Why It Fails                                 | Fix                                                                                 |
| ----------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------- |
| Vague success criteria              | Engineering ships, no one knows if it worked | Always define a primary metric with a number and a window                           |
| Missing platform constraints        | iOS build works, Android breaks              | Always fill the platform constraint section, even if it says "no differences known" |
| No kill condition                   | Feature lingers past usefulness              | Every PRD must have an explicit kill trigger                                        |
| Instrumentation defined post-launch | Cannot measure success                       | Instrumentation spec is a launch blocker, not a post-launch task                    |
| Scope creep via omission            | "Out of scope" not stated                    | Always write the "Out of scope" section explicitly                                  |

---

## PRD Quality Bar

Marcus applies this checklist before approving any PRD (his own or a teammate's):

- [ ] Problem statement written in JTBD format with a quantified current-state gap
- [ ] Strategic context explains why now, not just why
- [ ] Scope includes an explicit "out of scope" list
- [ ] Platform constraints filled for every platform in scope
- [ ] Edge case matrix has at least 3 entries
- [ ] Primary metric is precisely defined with baseline and target
- [ ] Guardrail metrics listed with degradation thresholds
- [ ] Every metric has a corresponding instrumentation event defined
- [ ] Technical feasibility pre-assessment complete with complexity rating
- [ ] Launch sequencing includes rollout phases and App Store/Play timing
- [ ] Success criteria has a number, a metric, and a time window
- [ ] Kill condition is explicit and actionable
- [ ] All three review sign-offs obtained before "Approved" status
