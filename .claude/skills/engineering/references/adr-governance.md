---
name: adr-governance
description: Govern the Architecture Decision Record (ADR) process for security decisions — author security ADRs, review non-security ADRs for security implications, enforce ADR immutability after Stage 3 approval, and produce the compliance audit trail required by the Stage 6 Architecture & Conformance Review.
version: "1.0.0"
---

# ADR Governance

| Competency               | Description                                                         | Quality Criteria                                                                                                                        |
| ------------------------ | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Security ADR Authorship  | Write security-domain ADRs with context, decision, and consequences | ADR includes threat drivers, MASVS control mapping, rejected alternatives with security rationale, and a Stage 6 verification checklist |
| ADR Review               | Review non-security ADRs for security implications                  | Produces a security review annotation on each ADR within 48 hours; flags security implications as review conditions                     |
| Immutability Enforcement | Detect and escalate post-Stage 3 ADR modifications                  | Any change to a ratified ADR after user approval is escalated to the CTO and CSO as a P0 defect; no edits permitted without re-entry    |
| Compliance Audit Trail   | Produce Stage 6 ADR compliance evidence                             | Generates a table mapping each Stage 6 review criterion to the ADR that addresses it, with status: Compliant / Non-Compliant / N/A      |

## Execution Guidance

### Security ADR Structure

Security ADRs follow the standard company ADR format with a mandatory security annex:

```markdown
# ADR-SEC-NNN: [Title]

**Status:** [Proposed | Accepted | Superseded by ADR-SEC-NNN]
**Date:** YYYY-MM-DD
**Author(s):** [Security Architect, CIO]

## Context

[Security threat or risk that drives this decision]

## Decision

[The security control or architectural pattern adopted]

## MASVS Mapping

| MASVS Control   | Requirement Satisfied                |
| --------------- | ------------------------------------ |
| MASVS-NETWORK-1 | TLS enforcement on all API endpoints |

## Rejected Alternatives

| Alternative | Reason Rejected                          |
| ----------- | ---------------------------------------- |
| [Option]    | [Security weakness that disqualifies it] |

## Consequences

**Positive:** [Security improvement achieved]
**Negative / Trade-offs:** [Performance or complexity cost]

## Stage 6 Verification Checklist

- [ ] Implementation matches ADR decision
- [ ] MASVS controls verified in code review
- [ ] No post-approval deviations found
```

### ADR Immutability Protocol

After User approval at Stage 3, security ADRs are locked. If a deviation is discovered at Stage 6:

1. Raise as a P0 defect — "ADR Conformance Violation."
2. Escalate to CTO and CSO immediately.
3. Do not remediate by editing the ADR — open a new ADR (ADR-SEC-NNN+1) that supersedes the original.
4. The Stage 3 gate must be re-entered for any technology change implied by the new ADR.
