---
name: pipeline-documentation
description: >
  Pipeline documentation authoring for mobile development — Stage 1-10 pipeline specifications, gate criteria documentation, artifact flow diagrams, and defect severity system references. Owned by Henrik Larsen (Technical Writer). Use when creating or updating pipeline documentation, monitoring systems, or progress sync protocols. Trigger: pipeline documentation, stage documentation, gate criteria, progress monitoring, development workflow documentation.
version: "1.0.0"
---

Pipeline documentation skill for Henrik Larsen — Technical Writer (R&D department).
Produces pipeline procedure documentation, gate criteria specifications, operational runbooks, SOPs, and process flow diagrams.

## Owner

Henrik Larsen — Technical Writer, Research & Development department.
Reports to: CTO office (primary), Software Architect (dotted-line).
Pipeline stages: 3, 4, 6, 8, 10.

## When to Invoke

- Writing clear, stage-by-stage procedure docs that engineers can follow without ambiguity
- Specifying gate criteria with explicit pass/fail conditions, responsible parties, and artifact requirements
- Creating operational runbooks for recurring pipeline activities (gate reviews, defect triage, release checks)
- Developing Standard Operating Procedures for cross-functional workflows with RACI matrices and escalation paths
- Producing Mermaid and BPMN diagrams that accurately represent pipeline flows, decision points, and handoffs
- Applying version control, review workflows, and CI validation to pipeline documentation (documentation-as-code)

## Competencies

| Competency                       | Description                                                                                                  | Quality Criteria                                                                                                      |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| Pipeline Procedure Documentation | Write clear, stage-by-stage procedure docs that engineers can follow without ambiguity                       | Stage procedure document produced in ≤6 hours; zero ambiguity-related questions from engineers during stage execution |
| Gate Criteria Documentation      | Specify gate criteria with explicit pass/fail conditions, responsible parties, and artifact requirements     | Gate docs pass CTO+CHRO review on first submission; zero gate disputes traced to unclear criteria                     |
| Runbook Authoring                | Create operational runbooks for recurring pipeline activities (gate reviews, defect triage, release checks)  | Runbooks enable a new engineer to execute the activity with ≤1 clarification question; rated ≥4.3/5 by users          |
| SOP Creation                     | Develop Standard Operating Procedures for cross-functional workflows with RACI matrices and escalation paths | SOPs adopted by 100% of target teams within 30 days; zero procedural deviations due to SOP gaps                       |
| Process Flow Diagramming         | Produce Mermaid and BPMN diagrams that accurately represent pipeline flows, decision points, and handoffs    | Diagrams pass accuracy review with pipeline owners; zero engineers misinterpret flow direction or decision logic      |
| Documentation-as-Code            | Apply version control, review workflows, and CI validation to pipeline documentation                         | Pipeline docs pass CI lint checks ≥98%; zero unversioned or orphaned documents in the pipeline doc tree               |

## Execution Guidance

Detailed procedure templates, gate criteria specifications, runbook structures, SOP templates, Mermaid/BPMN standards, and documentation-as-code practices are in `references/`:

- [`procedure-templates.md`](references/procedure-templates.md) — Pipeline procedure and gate criteria templates
- [`runbook-sop-templates.md`](references/runbook-sop-templates.md) — Runbook, SOP, diagramming, and documentation-as-code templates

## Pipeline Integration

| Pipeline Stage                   | Pipeline Documentation Relevance                                                                                     |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Stage 1 (Requirements)           | Procedure docs for Stage 1 guide CPO/CSO in PRD/SRD creation; gate criteria docs used by requirements gate panel     |
| Stage 2 (Design)                 | Procedure docs for Stage 2 guide CDO in prototype/IDS creation; gate criteria docs used by design gate panel         |
| Stage 3 (Architecture)           | Procedure docs for Stage 3 guide CTO/CIO in UML/ADR/TSD creation; gate criteria docs used by architecture gate panel |
| Stage 4 (Implementation Plan)    | Procedure docs for Stage 4 guide CTO in implementation plan creation; Progress Sync Protocol SOP activated           |
| Stage 5 (Development)            | Runbooks for development progress tracking; development log maintenance procedures                                   |
| Stage 6 (Code Review)            | Code review runbook; defect triage SOP; gate criteria docs used by code review panel                                 |
| Stage 7 (Testing)                | Testing procedure docs; test results reporting runbook; gate criteria docs used by testing panel                     |
| Stage 8 (Integrity Verification) | Integrity verification runbook; panel reporting procedures; gate criteria docs                                       |
| Stage 9 (i18n)                   | i18n procedure docs; translation verification reporting runbook                                                      |
| Stage 10 (Release)               | Release checklist runbook; release decision procedure; gate criteria docs used by release panel + USER               |

## Quality Standards

- **Template Compliance:** 100% of pipeline procedure documents contain all required sections per template; zero documents rejected for structural deficiencies
- **Gate Criteria Clarity:** Zero gate disputes traced to ambiguous criteria; all criteria are testable boolean conditions with named validators and specific evidence requirements
- **Runbook Usability:** Engineers executing runbooks require ≤1 clarification question per runbook execution; runbook satisfaction score ≥4.3/5
- **SOP Adoption:** 100% of target teams adopt published SOPs within 30 days; zero procedural deviations attributable to SOP gaps or ambiguities
- **Diagram Accuracy:** 100% of process flow diagrams pass accuracy review with pipeline owners; zero engineers report misinterpreting flow direction or decision logic
- **CI Pass Rate:** Pipeline documentation CI checks pass ≥98% of commits; failing commits are remediated within 24 hours
- **Review Timeliness:** Pipeline documentation reviews completed within 5 business days of submission; zero documents stalled in review for >10 business days
- **Version Currency:** 100% of pipeline documents have versions updated within 5 business days of any pipeline process change; zero documents with stale versions (>30 days since last pipeline change)
- **Cross-Reference Integrity:** Zero broken internal links or orphaned cross-references in pipeline documentation; automated link check runs on every commit
