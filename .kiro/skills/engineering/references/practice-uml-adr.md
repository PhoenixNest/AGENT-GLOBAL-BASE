---
name: practice-uml-adr
description: Lead architecture practice sessions that build team proficiency in producing UML diagrams and ADRs to company standards — through worked examples, peer review workshops, and targeted feedback — bringing all platform team members to Stage 3 deliverable competency.
version: "1.0.0"
---

# Practice UML ADR

| Competency                | Description                                                              | Quality Criteria                                                                                                              |
| ------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| UML Workshop Facilitation | Run hands-on workshops on Class, Sequence, and Component diagrams        | Workshops produce real artifacts for current project; participants can independently produce compliant UML after two sessions |
| ADR Workshop Facilitation | Run ADR authoring workshops using live decision scenarios                | Participants author a complete ADR from a given scenario; architect provides written feedback on each draft                   |
| Peer Review Cadence       | Establish and run weekly peer review rounds for UML and ADR drafts       | All Stage 3 drafts reviewed before CTO submission; review comments addressed in < 48 hours                                    |
| Proficiency Tracking      | Track individual team member competency levels for UML and ADR authoring | Maintains a competency matrix; identifies members needing additional coaching; updates quarterly                              |

## Execution Guidance

### UML Competency Ladder

| Level | Description                                                  | Gate                                             |
| ----- | ------------------------------------------------------------ | ------------------------------------------------ |
| 0     | No experience with UML                                       | —                                                |
| 1     | Can read and interpret UML diagrams                          | Pass a diagram interpretation quiz               |
| 2     | Can produce Class and Sequence diagrams with guidance        | Peer-reviewed diagram passes first review        |
| 3     | Can independently produce all Stage 3 required UML artifacts | Solo Stage 3 UML package approved by CTO         |
| 4     | Can review others' UML and provide constructive feedback     | Conduct 3 peer reviews rated ≥ 4/5 by recipients |

### Workshop Schedule

| Session | Topic                                | Duration  | Output                                         |
| ------- | ------------------------------------ | --------- | ---------------------------------------------- |
| 1       | UML fundamentals — Class diagrams    | 2 hours   | Draft class diagram for current sprint feature |
| 2       | Sequence diagrams for async flows    | 2 hours   | Sequence diagram for a defined API flow        |
| 3       | Component and deployment diagrams    | 2 hours   | Full Stage 3 UML package draft                 |
| 4       | ADR authoring — technology decisions | 2 hours   | Draft ADR for a live decision                  |
| 5       | ADR peer review simulation           | 1.5 hours | Peer-reviewed ADR meeting Stage 3 standards    |

Practice sessions are scheduled bi-weekly, not as blocking mandatory training but as opt-in skill-builders that directly produce project artifacts.
