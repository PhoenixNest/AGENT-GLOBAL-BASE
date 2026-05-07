---
name: uml-production-certification
description: Certify that Stage 3 UML Engineering Packages meet the company quality standard before CTO submission — reviewing Class, Sequence, Component, and Deployment diagrams for completeness, consistency, and alignment with the approved ADRs, and issuing a formal certification sign-off.
version: "1.0.0"
---

# UML Production Certification

| Competency             | Description                                                               | Quality Criteria                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| UML Completeness       | Verify all required diagram types are present for the stage               | Stage 3 package includes: Class, Sequence (happy path + error paths), Component, and Deployment diagrams — no exceptions       |
| ADR-UML Alignment      | Verify that UML diagrams implement the architecture decisions in the ADRs | Each ADR technology choice is traceable to a component or class in the UML; divergences are P0 defects                         |
| Notation Compliance    | Verify UML notation conforms to UML 2.5 standard                          | Arrowhead semantics correct (association vs dependency vs realization); multiplicities specified on all relationships          |
| Certification Sign-off | Issue formal certification for CTO review submission                      | Certification memo includes: diagram inventory, ADR alignment check results, notation issues found and resolved, sign-off date |

## Execution Guidance

### Stage 3 UML Package Checklist

Before issuing certification, verify:

| Item                      | Check                                                                |
| ------------------------- | -------------------------------------------------------------------- |
| Class diagrams            | All domain entities, relationships, multiplicities, and key methods  |
| Sequence diagrams         | Happy path + at least 2 error paths per major flow                   |
| Component diagram         | All services, libraries, and their interfaces; deployment boundaries |
| Deployment diagram        | Physical/cloud node layout; network zones; data store placement      |
| ADR cross-reference table | Each ADR decision traceable to a specific diagram element            |
| Security annotations      | Security control points (auth gates, encryption boundaries) labeled  |

### Certification Memo Format

```markdown
# UML Engineering Package Certification

**Project:** [Project name]
**Stage:** Stage 3
**Review Date:** YYYY-MM-DD
**Certified by:** Dr. Elena Rostova, Senior Software Architect

## Certification Verdict: PASS / FAIL

## Diagram Inventory

| Diagram Type    | File                  | Status       |
| --------------- | --------------------- | ------------ |
| Class           | class-diagram.md      | ✅ Compliant |
| Sequence — auth | sequence-auth.md      | ✅ Compliant |
| Component       | component-diagram.md  | ✅ Compliant |
| Deployment      | deployment-diagram.md | ✅ Compliant |

## Issues Found

[None / List of issues with resolution status]
```

A **FAIL** verdict means the package cannot be submitted to the CTO for Stage 3 approval. All issues must be resolved and re-certification completed before submission.
