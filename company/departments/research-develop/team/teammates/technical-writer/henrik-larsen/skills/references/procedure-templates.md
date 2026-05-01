---
version: "1.0.0"
---

### Pipeline Procedure Documentation

#### Documentation Structure

Each pipeline stage has a dedicated procedure document following this structure:

```markdown
# Stage N: [Stage Name] — Procedure

**Pipeline Reference:** `company/pipeline/mobile-development/pipeline.md`
**Owner:** [Responsible Producer]
**Stage:** N of 10
**Predecessor:** Stage N-1 ([Name])
**Successor:** Stage N+1 ([Name])

## Stage Overview

[2-3 paragraphs: What this stage produces, why it matters, and how it fits in the pipeline]

## Artifacts In

| Artifact     | Source Stage | Format                 | Owner  | Validation Criteria      |
| ------------ | ------------ | ---------------------- | ------ | ------------------------ |
| [Artifact 1] | Stage X      | `.md` / `.html` / etc. | [Role] | [What "good" looks like] |

## Artifacts Out

| Artifact     | Target Stage | Format                 | Owner  | Acceptance Criteria      |
| ------------ | ------------ | ---------------------- | ------ | ------------------------ |
| [Artifact 1] | Stage X+1    | `.md` / `.html` / etc. | [Role] | [What "done" looks like] |

## Procedure Steps

### Step N.1: [Step Name]

**Actor:** [Role]
**Input:** [What this step consumes]
**Action:** [Specific, actionable description]
**Output:** [What this step produces]
**Quality Check:** [How the actor verifies correctness]
**Estimated Duration:** [T-shirt size or hours]

## Gate Criteria

| #   | Criterion     | Pass Condition                | Validator | Evidence Required    |
| --- | ------------- | ----------------------------- | --------- | -------------------- |
| 1   | [Criterion]   | [Boolean condition]           | [Role]    | [Artifact or metric] |
| 2   | User Approval | [User has confirmed/approved] | USER      | [User response]      |

## Defect Handling

| Defect Type | Classification | Remediation Owner | Escalation Path            |
| ----------- | -------------- | ----------------- | -------------------------- |
| [Type 1]    | P0/P1/P2/P3    | [Role]            | [Escalation if unresolved] |

## Dependencies & Blockers

| Dependency                           | Status Check               | Blocker Resolution       |
| ------------------------------------ | -------------------------- | ------------------------ |
| [Dependency on prior stage artifact] | [How to verify it's ready] | [What to do if it's not] |
```

#### Writing Principles for Stage Procedures

| Principle                      | Application                                                                                                                                               |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Action-oriented**            | Every step begins with a verb: "Review," "Compile," "Validate," "Submit."                                                                                 |
| **Single actor per step**      | Each step has exactly one Responsible actor (per RACI). Collaboration is noted but ownership is unambiguous.                                              |
| **Testable gate criteria**     | Every gate criterion is a boolean condition. "PRD is complete" is not testable. "PRD contains all 12 required sections and has CPO sign-off" is testable. |
| **Reference, don't duplicate** | Link to upstream artifacts (PRD, SRD, UML) rather than restating their content.                                                                           |
| **Duration estimates**         | Every step includes a duration estimate. These feed the Progress Sync Protocol (>20% overrun triggers CTO → CPO notification).                            |
| **Defect-aware**               | Procedure steps include quality checks; defect discovery points are explicit.                                                                             |

### Gate Criteria Documentation

#### Gate Criteria Specification Template

```markdown
# Stage N → N+1 Gate Review — Criteria

**Stage:** N ([Name])
**Gate Review Type:** [Requirements | Design | Architecture | Implementation Plan | Development Complete | Code Review | Testing | Integrity Verification | i18n | Release]
**Panel:** [List of panel members per pipeline specification]
**User Approval Required:** [YES/NO]

## Gate Criteria

| #   | Criterion        | Pass Condition                                       | Validator | Evidence                      |
| --- | ---------------- | ---------------------------------------------------- | --------- | ----------------------------- |
| 1   | [Criterion name] | [Boolean condition]                                  | [Role]    | [Specific artifact or metric] |
| 2   | User Approval    | [User has confirmed/approved/conditionally approved] | USER      | [User response in writing]    |

## Pass/Fail Rules

- **Pass:** All criteria met, user approves (if required)
- **Conditional Pass:** All criteria met, user conditionally approves with remediation notes (advance with tracked action items)
- **Fail:** Any criterion not met, or user rejects (return to Stage N for remediation)

## Review Process

1. Stage owner presents artifacts and evidence for each criterion
2. Panel reviews evidence and raises questions
3. Panel votes on each criterion (Pass/Fail/Abstain)
4. User provides decision (if approval required)
5. Gate Review Sign-off document created with results
6. Defects documented per P0-P3 classification
7. Decision communicated to stage owner and downstream teams
```

#### Gate Criteria Writing Standards

- **Atomic criteria:** Each criterion tests exactly one condition. Compound criteria are split into separate rows.
- **Unambiguous validators:** The validator role is a specific role (CTO, CPO, USER), not a team or department.
- **Evidence-specific:** The evidence column names the exact artifact or metric that proves the criterion is met.
- **User approval explicit:** If user approval is required, it is a dedicated criterion row with the validator listed as "USER."
- **No subjective language:** Criteria use observable, verifiable conditions. "Design is good" is invalid. "Prototype implements all PRD user stories" is valid.
