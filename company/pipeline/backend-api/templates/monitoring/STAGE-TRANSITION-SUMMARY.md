# Stage Transition Summary — Universal Template

> **Purpose:** Mandatory summary artifact produced at every stage gate. Prevents ~15-20% cross-stage information loss.

**Project:** [Project Name]
**Stage Completed:** [N] — [Stage Name]
**Stage Advancing To:** [N+1] — [Stage Name]
**Completed:** YYYY-MM-DD
**Produced By:** [Agent Name / Role]

---

## Gate Result

| Criterion                   | Result                                   |
| :-------------------------- | :--------------------------------------- |
| **Gate decision**           | ☐ Pass / ☐ Pass with conditions / ☐ Fail |
| **Conditions (if any)**     | [List conditions]                        |
| **P0/P1 defects remaining** | [N] (must be 0 to pass)                  |
| **P2/P3 deferred by CEO**   | [N]                                      |

---

## Key Decisions Made

1. [Decision] — _Source: [ADR/PRD/SRD reference]_
2. [Decision] — _Source: [reference]_
3. [Decision] — _Source: [reference]_

---

## Artifacts Produced

| Artifact | Version | Location | Key Content (2–3 sentences) |
| :------- | :------ | :------- | :-------------------------- |
| [Name]   | v[N]    | [path]   | [Summary]                   |

---

## Constraints Carried Forward

- [ ] [Constraint 1] — _Source: [PRD §X / SRD §Y / ADR-NNN]_
- [ ] [Constraint 2] — _Source: [reference]_

---

## Open Questions / Risks for Next Stage

|  #  | Question or Risk | Impact         | Owner   | Action   |
| :-: | :--------------- | :------------- | :------ | :------- |
|  1  | [Question]       | [High/Med/Low] | [Agent] | [Action] |

---

## Defects Deferred

| ID       | Severity | Description | CEO Decision              | Reason      |
| :------- | :------- | :---------- | :------------------------ | :---------- |
| [P#-NNN] | [P2/P3]  | [Brief]     | ☐ Fix later / ☐ Won't fix | [Rationale] |

---

## Context Handoff Checklist

- [ ] All gate criteria for Stage [N] satisfied
- [ ] All P0/P1 defects resolved (0 remaining)
- [ ] Summary accurately reflects all key decisions
- [ ] All artifacts versioned and stored correctly
- [ ] Constraints include ALL inherited constraints from prior stages
- [ ] No raw artifacts required by next stage — summary is self-contained

---

**Signed by:** [Agent Name] on YYYY-MM-DD
**Verified by:** [Stage Owner / C-Suite] on YYYY-MM-DD
