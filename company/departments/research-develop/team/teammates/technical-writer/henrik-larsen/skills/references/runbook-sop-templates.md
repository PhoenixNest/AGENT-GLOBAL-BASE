---
version: "1.0.0"
---

### Runbook Authoring

#### Runbook Structure

```markdown
# Runbook: [Activity Name]

**Category:** [Gate Review | Defect Triage | Release Check | Environment Setup | etc.]
**Frequency:** [Per stage | Weekly | Per release | Ad-hoc]
**Owner:** [Role responsible for executing the runbook]
**Last Updated:** [YYYY-MM-DD]
**Version:** vN

## Purpose

[1-2 sentences: What this runbook enables the operator to accomplish]

## Prerequisites

- [Access required: e.g., "CTO panel member access to CI/CD dashboard"]
- [Artifacts needed: e.g., "Defect Report from Stage 6 code review"]
- [Environment: e.g., "Stage environment deployed and accessible"]

## Step-by-Step Procedure

### Step 1: [Step Name]

**Action:** [Specific action the operator performs]
**Expected Result:** [What success looks like]
**Troubleshooting:** [What to do if the expected result doesn't occur]

## Decision Points

| Decision     | Condition           | Action if True      | Action if False                |
| ------------ | ------------------- | ------------------- | ------------------------------ |
| [Decision 1] | [Boolean condition] | [Proceed to step X] | [Proceed to step Y / escalate] |

## Escalation Path

| Condition     | Escalate To | Contact Method                 | SLA             |
| ------------- | ----------- | ------------------------------ | --------------- |
| [Condition 1] | [Role]      | [Slack channel / email / page] | [Response time] |

## Output Artifacts

| Artifact   | Format                 | Location                        | Owner  |
| ---------- | ---------------------- | ------------------------------- | ------ |
| [Output 1] | `.md` / `.json` / etc. | `company/project/<project>/...` | [Role] |

## Known Issues & Workarounds

| Issue     | Symptoms                     | Workaround             | Permanent Fix Tracking  |
| --------- | ---------------------------- | ---------------------- | ----------------------- |
| [Issue 1] | [What the operator observes] | [Temporary workaround] | [Link to defect or ADR] |

## Change History

| Version | Date       | Author | Changes         |
| ------- | ---------- | ------ | --------------- |
| v1      | YYYY-MM-DD | [Name] | Initial version |
```

#### Runbook Writing Principles

| Principle                      | Application                                                                                        |
| ------------------------------ | -------------------------------------------------------------------------------------------------- |
| **Operator-centric**           | Written for the person executing the runbook, not the person who designed the process.             |
| **Troubleshooting embedded**   | Every step includes "what to do if this fails" — operators should never be stuck without guidance. |
| **Decision tables, not prose** | Branching logic is expressed as tables, not paragraphs. Operators scan; they don't read novels.    |
| **Known issues current**       | Known issues section is updated within 24 hours of any new issue discovery.                        |
| **Versioned**                  | Runbooks follow the same versioning as all project documents (draft/ → vN/ → final/).              |

### SOP Creation

#### SOP Structure with RACI

```markdown
# SOP: [Procedure Name]

**SOP ID:** SOP-NNN
**Department:** [Department]
**Effective Date:** [YYYY-MM-DD]
**Review Date:** [YYYY-MM-DD — typically 12 months from effective date]
**Owner:** [Role]
**Approved By:** [Approving authority]

## Purpose / Scope / RACI Matrix / Procedure / Compliance Requirements / Training Requirements / Exceptions / Related Documents / Revision History
```

### Process Flow Diagramming

#### Mermaid Diagram Standards

All pipeline procedure documents include at least one Mermaid diagram that visualizes the stage flow. Diagrams use consistent notation:

| Element        | Mermaid Syntax          | Meaning                                           |
| -------------- | ----------------------- | ------------------------------------------------- |
| Process step   | `[Step Name]`           | Rectangular node — an action or procedure         |
| Decision point | `{Condition?}`          | Diamond node — a yes/no or pass/fail gate         |
| Artifact       | `[(Artifact Name)]`     | Database-shaped node — a document or data product |
| Actor          | `[[Actor Role]]`        | Double-bordered node — a person or role           |
| Start/End      | `([Start])` / `([End])` | Rounded node — process boundaries                 |

#### BPMN for Complex Workflows

For cross-functional SOPs involving multiple actors and handoffs, BPMN 2.0 notation is used (via BPMN.io or similar tooling):

- **Pools:** Each department or role family is a separate pool
- **Lanes:** Individual roles within a department
- **Tasks:** Service tasks (automated) vs. user tasks (manual)
- **Gateways:** Exclusive (XOR), parallel (AND), inclusive (OR)
- **Events:** Start, intermediate, end, boundary (error/escalation)

BPMN diagrams are exported as `.svg` and stored alongside the SOP document. Source `.bpmn` files are stored in a `diagrams/` subdirectory.

### Documentation-as-Code Practices

#### Repository Structure for Pipeline Documentation

```
company/pipeline/
└── development/
    ├── pipeline.md                    # Master pipeline definition
    ├── progress-monitoring.md          # Monitoring system spec
    └── procedures/                     # Stage-specific procedure docs
        ├── stage-01-requirements.md
        ├── stage-02-design.md
        └── ...
    ├── gate-reviews/                   # Gate criteria documents
    ├── runbooks/                       # Operational runbooks
    └── sops/                           # Standard Operating Procedures
```

#### CI Validation for Documentation

| Check                 | Tool           | What It Validates                                          |
| --------------------- | -------------- | ---------------------------------------------------------- |
| Markdown lint         | `markdownlint` | Formatting consistency, heading hierarchy, link validity   |
| Mermaid syntax        | `mermaid-cli`  | Diagram syntax validity                                    |
| Cross-reference check | Custom script  | All internal links resolve; no broken references           |
| Required sections     | Custom script  | Each stage doc contains all required sections per template |
| Terminology check     | Custom script  | Canonical terms used; banned terms flagged                 |
| Version consistency   | Custom script  | Version numbers in docs match git tags                     |

#### Documentation Review Workflow

```
Author drafts in draft/
      ↓
Self-review against template checklist
      ↓
Submit PR to pipeline maintainers (CTO + CHRO)
      ↓
Technical review (CTO — accuracy of pipeline mechanics)
      ↓
Process review (CHRO — clarity, completeness, usability)
      ↓
Revisions (if requested)
      ↓
Merge to vN/
      ↓
Upon stage gate approval: copy to final/
```
