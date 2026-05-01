---
name: architecture-review-shadowing
description: Onboard junior and mid-level engineers into the architecture review process — through structured shadowing sessions at Stage 6 reviews — building the next generation of reviewers and ensuring the team has redundant architecture review capacity.
version: "1.0.0"
---

# Architecture Review Shadowing

| Competency                       | Description                                                             | Quality Criteria                                                                                                           |
| -------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Structured Shadowing             | Design and run a graduated shadowing programme for Stage 6 reviews      | Three-stage progression: Observe → Assist → Co-lead; each stage has defined completion criteria                            |
| Review Mentorship                | Provide real-time mentorship during live architecture reviews           | Mentor provides written feedback on each review the shadower participates in; feedback references specific review criteria |
| Independent Review Certification | Certify shadowers as independent reviewers when ready                   | Certification requires: 3 observed reviews, 2 assisted reviews, 1 co-led review; certified by Senior Software Architect    |
| Capacity Planning                | Maintain a register of certified reviewers and upcoming review schedule | Review capacity never falls below 2 certified reviewers; escalate to CTO if below threshold                                |

## Execution Guidance

### Shadowing Programme Progression

| Stage     | Activities                                                             | Completion Criteria                                                               |
| --------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Observe   | Attend 3 Stage 6 reviews as silent observer; review pre-read materials | Can explain the 5 ADR conformance checkpoints without prompting                   |
| Assist    | Prepare review notes; run one ADR conformance check independently      | Notes are complete and accurate; flagged items match architect's assessment ≥ 80% |
| Co-lead   | Co-lead one full Stage 6 review; architect provides real-time guidance | Defect classification matches architect's within one severity level               |
| Certified | Independent Stage 6 reviewer                                           | Issued formal certification by Senior Software Architect                          |

### Onboarding Materials

Shadowers receive before their first session:

1. The Stage 6 pipeline specification (review scope, panel composition, remediation loop rules)
2. Three previous Stage 6 review reports (anonymized) as worked examples
3. The P0–P3 defect severity definitions
4. A copy of all active ADRs for the project under review

### Capacity Register

The Senior Software Architect maintains a register of all certified reviewers. If the total certified reviewer count falls below 2, this is escalated to the CTO as a resourcing risk — not managed silently.
