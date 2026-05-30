---
name: adr-template-adaptation
description: Adapt the base company ADR template for domain-specific mobile architecture decisions — extending it with mobile-specific sections (platform scope, KMP applicability, target SDK impact) — and maintain the ADR template library so all team members author compliant ADRs.
version: "1.0.0"
---

# ADR Template Adaptation

| Competency                   | Description                                                                         | Quality Criteria                                                                                                           |
| ---------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Template Extension           | Add mobile-specific fields to the base ADR template without breaking base structure | Extended template passes base template validation checklist; mobile fields are clearly marked as optional extensions       |
| Template Library Maintenance | Keep ADR templates versioned and discoverable for the team                          | Template library is version-controlled; each template has a changelog; all team members can find and use current templates |
| Authoring Guidance           | Produce ADR authoring guides for each template variant                              | Guide includes worked examples for common decision types; explains when to use base vs extended template                   |
| Template Auditing            | Periodic review of filed ADRs for template compliance                               | Quarterly audit; non-compliant ADRs are flagged to authors; compliance rate tracked as a team metric                       |

## Execution Guidance

### Mobile ADR Template Extensions

Add the following section to the base ADR template for mobile decisions:

```markdown
## Mobile Scope

| Field              | Value                                              |
| ------------------ | -------------------------------------------------- |
| Platforms affected | Android / iOS / Both / KMP Shared                  |
| Min SDK impact     | Yes — min SDK changes to [N] / No                  |
| Target SDK impact  | Yes — target SDK changes to [N] / No               |
| KMP applicability  | Shared module / Platform-specific / Not applicable |
| App size impact    | Estimated delta: [+/- N KB]                        |
```

### Template Versioning Convention

Templates follow semantic versioning:

- **MAJOR:** Breaking change to required fields (requires existing ADRs to be back-filled)
- **MINOR:** New optional field added (backward compatible)
- **PATCH:** Wording clarification, example update

Templates live at: `company/pipeline/_base/` — the canonical source of truth. Any team-specific extension must be reviewed by the Senior Software Architect before use.
