# Stage Transition Summary

> **Purpose:** Mandatory summary artifact produced at every stage gate to prevent cross-stage information loss.

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

Summarize the **top 3–5 decisions** made during this stage. Each decision should be a single sentence referencing the source artifact.

1. [Decision] — _Source: [ADR/PRD/SRD reference]_
2. [Decision] — _Source: [reference]_
3. [Decision] — _Source: [reference]_

---

## Artifacts Produced

| Artifact | Version | Location | Key Content (2–3 sentences)                                 |
| :------- | :------ | :------- | :---------------------------------------------------------- |
| [Name]   | v[N]    | [path]   | [Summary of what this artifact contains and why it matters] |
| [Name]   | v[N]    | [path]   | [Summary]                                                   |

---

## Constraints Carried Forward

Constraints that the **next stage must honor**. These originate from PRD, SRD, ADRs, or CEO decisions.

- [ ] [Constraint 1] — _Source: [PRD §X / SRD §Y / ADR-NNN]_
- [ ] [Constraint 2] — _Source: [reference]_
- [ ] [Constraint 3] — _Source: [reference]_

---

## Open Questions / Risks for Next Stage

|  #  | Question or Risk | Impact            | Owner   | Recommended Action |
| :-: | :--------------- | :---------------- | :------ | :----------------- |
|  1  | [Question]       | [High/Medium/Low] | [Agent] | [Action]           |
|  2  | [Risk]           | [Impact]          | [Agent] | [Action]           |

---

## Defects Deferred

| ID       | Severity | Description         | CEO Decision              | Reason      |
| :------- | :------- | :------------------ | :------------------------ | :---------- |
| [P#-NNN] | [P2/P3]  | [Brief description] | ☐ Fix later / ☐ Won't fix | [Rationale] |

---

## Context Handoff Checklist

The producing agent must verify the following before handing off to the next stage:

- [ ] All gate criteria for Stage [N] are satisfied
- [ ] All P0/P1 defects are resolved (0 remaining)
- [ ] This summary accurately reflects all key decisions
- [ ] All artifacts are versioned and stored at their correct paths
- [ ] Constraints section includes ALL inherited constraints from prior stages
- [ ] No raw artifacts are required by the next stage — this summary is self-contained for routing

---

**Signed by:** [Agent Name] on YYYY-MM-DD
**Verified by:** [Stage Owner / C-Suite] on YYYY-MM-DD
