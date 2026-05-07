---
name: { skill-domain-name }
description: { One-line description of what this skill domain covers }
---

# {Skill Domain Name}

This is the router skill for the `{skill-domain-name}` domain. It serves as an entry point for the agent to access a library of specific sub-skills located in the `references/` subdirectory.

## Domain Coverage

{Provide a brief overview of what this skill domain encompasses. List the major categories or areas of expertise covered by this domain.}

**Example:**

- Mobile product strategy and vision
- Product Requirements Document (PRD) authorship
- Product stage gates and approval workflows
- Product quality standards and acceptance criteria

## How to Use

When you need expertise in {Domain Name}, explore the `references/` directory and read the highly specific sub-skill markdown files:

{List all sub-skills with brief descriptions}

**Example:**

- `mobile-product-strategy.md` — Product vision, strategy, and roadmap planning
- `prd-authorship.md` — PRD structure, content, and quality standards
- `product-stage-gates.md` — Stage gate enforcement and approval workflows

## Available Sub-Skills

{Optional: Provide a detailed table of sub-skills with descriptions}

| Skill File         | Location                    | Description                                          |
| ------------------ | --------------------------- | ---------------------------------------------------- |
| `{sub-skill-1}.md` | `{domain-name}/references/` | {Detailed description of what this sub-skill covers} |
| `{sub-skill-2}.md` | `{domain-name}/references/` | {Detailed description of what this sub-skill covers} |
| `{sub-skill-n}.md` | `{domain-name}/references/` | {Detailed description of what this sub-skill covers} |

**Total Skills:** {N}

## Related Domains

{List related skill domains that agents might need to reference alongside this one}

**Example:**

- `product-design` — UI/UX design and prototyping
- `engineering` — Technical specification and implementation
- `technology-strategy` — Architecture decisions and technology selection

## Domain Ownership

{Optional: Specify which organizational agents primarily use this skill domain}

**Primary Users:**

- {Agent Role 1} — {Usage context}
- {Agent Role 2} — {Usage context}

**Secondary Users:**

- {Agent Role 3} — {Usage context}

## Skill Activation

To activate this domain skill and access its sub-skills:

```typescript
discloseContext({
  name: "{skill-domain-name}",
});
```

This loads the parent `SKILL.md` which provides an overview and guides you to the specific sub-skills in the `references/` directory.

## Sub-Skill Access Pattern

Sub-skills are located in the `references/` subdirectory:

```
.kiro/skills/{domain-name}/references/{sub-skill-name}.md
```

**Reading a specific sub-skill:**

```typescript
readFile({
  path: ".kiro/skills/{domain-name}/references/{sub-skill-name}.md",
  explanation: "Reading {sub-skill} to understand {specific capability}",
});
```

## Skill Maintenance

**Version:** 1.0.0  
**Last Updated:** {YYYY-MM-DD}  
**Maintained By:** {Responsible team or agent}  
**Status:** {Active|Deprecated|Under Development}

## References

- **Sub-Skills Directory:** `.kiro/skills/{domain-name}/references/`
- **Related Documentation:** {Links to relevant workspace documentation}
- **AGENTS.md:** {Relevant section references}

---

_This skill domain follows the Kiro Skills specification and is maintained according to ECOSYSTEM_SPEC.md governance._
