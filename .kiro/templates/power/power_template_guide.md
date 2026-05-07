# Power Template Usage Guide

This guide explains how to create Kiro Powers using the `power_template.md` template.

---

## Table of Contents

1. [Understanding Powers](#understanding-powers)
2. [Power Architecture](#power-architecture)
3. [When to Create Powers](#when-to-create-powers)
4. [Step-by-Step Guide](#step-by-step-guide)
5. [Section-by-Section Guide](#section-by-section-guide)
6. [Complete Examples](#complete-examples)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Understanding Powers

### What Are Powers?

Powers are **comprehensive packages** that bundle documentation, templates, steering files, and optionally MCP servers for a specific domain or capability. They provide everything an agent needs to work effectively in that domain.

**Key Characteristics:**

- **Comprehensive** — Include all resources for a domain
- **Self-Contained** — Everything needed is in one place
- **Activatable** — Can be loaded on-demand via `kiroPowers` tool
- **Documented** — Include usage guides and examples

### Powers vs. Skills

| Aspect         | Powers                         | Skills                     |
| -------------- | ------------------------------ | -------------------------- |
| **Scope**      | Broad domain or system         | Specific capability        |
| **Contents**   | Docs, templates, steering, MCP | Methodology only           |
| **Activation** | Via `kiroPowers` tool          | Via `discloseContext` tool |
| **Structure**  | Directory with multiple files  | Single markdown file       |
| **Purpose**    | Package related resources      | Define how to do work      |

### Powers in the Ecosystem

Powers package:

- **Documentation** — Pipeline specs, overviews, guides
- **Templates** — PRD, SRD, ADR, TSD templates
- **Steering Files** — Conditional guidance
- **MCP Servers** — Optional tool integrations
- **Skills** — References to related skills

---

## Power Architecture

### Directory Structure

```
.kiro/powers/
├── power-name/
│   ├── POWER.md              # Main documentation (use template)
│   ├── templates/            # Optional: templates
│   │   ├── template-1.md
│   │   └── template-2.md
│   ├── steering/             # Optional: steering files
│   │   ├── steering-1.md
│   │   └── steering-2.md
│   └── mcp-servers/          # Optional: MCP server configs
│       └── server-config.json
```

### POWER.md Structure

The main `POWER.md` file follows this structure:

1. **Header** — Version, status, authority
2. **Overview** — What the power provides
3. **Capabilities** — Detailed capability documentation
4. **Usage** — How to activate and use
5. **Governance** — Rules and best practices
6. **Examples** — Quick start examples
7. **Reference** — Detailed reference information
8. **Troubleshooting** — Common issues and solutions

---

## When to Create Powers

### Create a Power When:

- You have a **complete system** to package (e.g., pipeline, framework)
- You need to bundle **multiple resources** (docs, templates, steering)
- The domain has **complex workflows** requiring comprehensive guidance
- Multiple agents need **consistent access** to the same resources
- You want to **optionally include MCP servers** for tool integration

**Examples:**

- `company-pipeline` — 13-stage development pipeline with templates
- `cc00-engineering` — LLM engineering stack with implementations
- `organizational-agents` — Agent activation and management

### Don't Create a Power When:

- You only have **documentation** (use steering files)
- You only have **methodology** (use skills)
- The scope is **too narrow** (single capability)
- Resources are **already well-organized** elsewhere

---

## Step-by-Step Guide

### Step 1: Plan Your Power

**Questions to Answer:**

1. What domain or system does this power cover?
2. What resources will it package?
3. Who will use this power?
4. What workflows does it support?
5. Does it need MCP servers?

**Example Plan:**

```
Power: API Development
Domain: Backend API development
Resources:
- API design guidelines
- OpenAPI templates
- API testing templates
- Versioning strategy docs
Users: Backend engineers, API architects
Workflows: API design, implementation, testing, versioning
MCP: No
```

### Step 2: Create Directory Structure

```bash
# Create power directory
mkdir -p .kiro/powers/power-name

# Create optional subdirectories
mkdir -p .kiro/powers/power-name/templates
mkdir -p .kiro/powers/power-name/steering
mkdir -p .kiro/powers/power-name/mcp-servers
```

### Step 3: Copy Template

```bash
cp .kiro/templates/power/power_template.md .kiro/powers/power-name/POWER.md
```

### Step 4: Fill in Header

```markdown
# {Power Name} Power

**Version:** 1.0.0  
**Status:** {Active|Under Development|Deprecated}  
**Authority:** {Reference to governing document}
```

**Example:**

```markdown
# API Development Power

**Version:** 1.0.0  
**Status:** Active  
**Authority:** AGENTS.md § Backend Engineering Standards
```

### Step 5: Write Overview

```markdown
## Overview

The **{Power Name} Power** provides comprehensive support for {description}.

This Power packages:

- **{Component 1}**: {Description}
- **{Component 2}**: {Description}
- **{Component 3}**: {Description}
```

### Step 6: Document Capabilities

For each major capability, provide:

- Detailed description
- Key features
- Access patterns
- Examples

### Step 7: Write Usage Instructions

```markdown
## How to Use This Power

### Activate the Power

\`\`\`typescript
kiroPowers({
action: "activate",
powerName: "{power-name}",
});
\`\`\`

### Basic Usage Pattern

{Step-by-step guide}
```

### Step 8: Add Governance Rules

Document mandatory rules and best practices:

```markdown
## Governance and Rules

### Mandatory Rules

1. **{Rule 1}** — {Explanation}
2. **{Rule 2}** — {Explanation}
```

### Step 9: Provide Examples

Include 3-5 quick start examples:

```markdown
## Quick Start Examples

### Example 1: {Use Case}

**Scenario:** {Description}

**Steps:**

\`\`\`typescript
// Implementation
\`\`\`
```

### Step 10: Add Reference Material

Include detailed reference information:

- Templates overview
- Configuration options
- API reference (if applicable)
- Troubleshooting guide

### Step 11: Validate and Format

```bash
prettier --write .kiro/powers/power-name/POWER.md
```

---

## Section-by-Section Guide

### Header Section

**Required Fields:**

```markdown
# {Power Name} Power

**Version:** 1.0.0  
**Status:** Active  
**Authority:** {Reference}
```

**Guidelines:**

- Use title case for power name
- Start with version 1.0.0
- Status: Active (production), Under Development (WIP), Deprecated (obsolete)
- Authority: Reference to AGENTS.md or other governing doc

### Overview Section

**Purpose:** High-level summary of what the power provides

**Structure:**

```markdown
## Overview

The **{Power Name} Power** provides comprehensive support for {description}.

This Power packages:

- **{Component 1}**: {Brief description}
- **{Component 2}**: {Brief description}
- **{Component 3}**: {Brief description}
- **{Component 4}**: {Brief description}
```

**Guidelines:**

- First paragraph: One-sentence summary
- Bullet list: 3-5 major components
- Keep descriptions brief (one line each)

### What This Power Provides Section

**Purpose:** Detailed capability documentation

**Structure:**

```markdown
## What This Power Provides

### 1. {Major Capability 1}

{Detailed description}

**Key Features:**

- {Feature 1}
- {Feature 2}
- {Feature 3}

**Access Pattern:**

\`\`\`
{path/to/resources}
\`\`\`

### 2. {Major Capability 2}

{Continue for all capabilities}
```

**Guidelines:**

- Number each capability (1, 2, 3...)
- Provide detailed description (2-3 paragraphs)
- List key features as bullets
- Show access patterns (paths, commands)
- Include tables for structured data

### How to Use This Power Section

**Purpose:** Activation and usage instructions

**Structure:**

```markdown
## How to Use This Power

### Activate the Power

\`\`\`typescript
kiroPowers({
action: "activate",
powerName: "{power-name}",
});
\`\`\`

**What happens when you activate:**

1. {Step 1}
2. {Step 2}
3. {Step 3}

### Basic Usage Pattern

**Step 1: {Action}**

{Description}

**Step 2: {Action}**

{Description}
```

**Guidelines:**

- Always show activation code
- Explain what activation does
- Provide step-by-step basic usage
- Include code examples

### Key Concepts Section

**Purpose:** Explain important concepts users need to understand

**Structure:**

```markdown
## Key Concepts

### {Concept 1}

{Explanation}

**Important Rules:**

| Rule         | Applies To | Detail        |
| ------------ | ---------- | ------------- |
| **{Rule 1}** | {Scope}    | {Explanation} |
| **{Rule 2}** | {Scope}    | {Explanation} |
```

**Guidelines:**

- Focus on concepts unique to this power
- Use tables for rules and constraints
- Provide examples for complex concepts

### Governance and Rules Section

**Purpose:** Document mandatory rules and best practices

**Structure:**

```markdown
## Governance and Rules

### Mandatory Rules

1. **{Rule 1}** — {Explanation and rationale}
2. **{Rule 2}** — {Explanation and rationale}

### Best Practices

1. **{Practice 1}** — {Explanation}
2. **{Practice 2}** — {Explanation}

### Common Violations

| Violation     | Impact        | Prevention     |
| ------------- | ------------- | -------------- |
| {Violation 1} | {What breaks} | {How to avoid} |
```

**Guidelines:**

- Separate mandatory rules from best practices
- Explain rationale for each rule
- Document common violations and prevention

### Quick Start Examples Section

**Purpose:** Provide concrete usage examples

**Structure:**

```markdown
## Quick Start Examples

### Example 1: {Use Case}

**Scenario:** {Description}

**Steps:**

\`\`\`typescript
// 1. {Action}
{code}

// 2. {Action}
{code}

// 3. {Action}
{code}
\`\`\`

**Expected Result:**
{What should happen}
```

**Guidelines:**

- Provide 3-5 examples
- Cover common use cases
- Include complete, runnable code
- Show expected results

### Reference Guide Section

**Purpose:** Detailed reference information

**Structure:**

```markdown
## Reference Guide

### {Reference Category 1}

{Detailed information}

### {Reference Category 2}

{Detailed information}
```

**Common Categories:**

- Templates overview
- Configuration options
- API reference
- File structure
- Command reference

### Troubleshooting Section

**Purpose:** Help users solve common problems

**Structure:**

```markdown
## Troubleshooting

### Issue: {Problem Description}

**Symptoms:**

- {Symptom 1}
- {Symptom 2}

**Solution:**

{Step-by-step resolution}

\`\`\`typescript
// Example solution code
\`\`\`
```

**Guidelines:**

- Document 5-10 common issues
- Provide clear symptoms
- Give step-by-step solutions
- Include code examples

### Footer Section

**Purpose:** Metadata and maintenance information

**Structure:**

```markdown
---

**Power Maintained By:** {Team or agents}  
**Last Updated:** {YYYY-MM-DD}  
**Status:** {Active|Under Development|Deprecated}  
**Support Contact:** {How to get help}

---

_This power follows the Kiro Powers specification and is maintained according to ECOSYSTEM_SPEC.md governance._
```

---

## Complete Examples

### Example 1: Simple Power (No MCP)

**Scenario:** Create a power for code review standards

**File:** `.kiro/powers/code-review/POWER.md`

```markdown
# Code Review Power

**Version:** 1.0.0  
**Status:** Active  
**Authority:** AGENTS.md § Code Quality Standards

---

## Overview

The **Code Review Power** provides comprehensive support for conducting code reviews across all engineering teams.

This Power packages:

- **Review Checklists**: Platform-specific review criteria
- **Review Templates**: Structured review comment templates
- **Steering Files**: Auto-activated review guidance
- **Best Practices**: Code review methodology

---

## What This Power Provides

### 1. Review Checklists

Platform-specific checklists for thorough code reviews:

- **Android**: Kotlin style, architecture patterns, testing
- **iOS**: Swift style, memory management, UI patterns
- **Backend**: API design, database queries, error handling
- **Frontend**: Component structure, accessibility, performance

**Location:** `.kiro/powers/code-review/checklists/`

### 2. Review Templates

Structured templates for review comments:

- **Blocking Issue Template**: For P0/P1 defects
- **Suggestion Template**: For improvements
- **Question Template**: For clarifications
- **Praise Template**: For excellent code

**Location:** `.kiro/powers/code-review/templates/`

---

## How to Use This Power

### Activate the Power

\`\`\`typescript
kiroPowers({
action: "activate",
powerName: "code-review",
});
\`\`\`

### Basic Usage Pattern

**Step 1: Select Checklist**

Choose the appropriate platform checklist.

**Step 2: Review Code**

Go through each checklist item systematically.

**Step 3: Document Findings**

Use templates to structure your comments.

---

## Quick Start Examples

### Example 1: Android Code Review

\`\`\`typescript
// 1. Activate power
kiroPowers({ action: "activate", powerName: "code-review" });

// 2. Read Android checklist
readFile({
path: ".kiro/powers/code-review/checklists/android-checklist.md",
explanation: "Loading Android review criteria"
});

// 3. Conduct review using checklist
// 4. Document findings using templates
\`\`\`

---

## References

- **Checklists**: `.kiro/powers/code-review/checklists/`
- **Templates**: `.kiro/powers/code-review/templates/`
- **AGENTS.md**: § Code Quality Standards

---

**Power Maintained By:** Engineering Leadership  
**Last Updated:** 2026-05-06
```

### Example 2: Complex Power (With MCP)

**Scenario:** Create a power for database operations

**File:** `.kiro/powers/database-ops/POWER.md`

```markdown
# Database Operations Power

**Version:** 1.0.0  
**Status:** Active  
**Authority:** AGENTS.md § Data Management Standards

---

## Overview

The **Database Operations Power** provides comprehensive support for database design, migration, and operations.

This Power packages:

- **Schema Design Guidelines**: Database design patterns
- **Migration Templates**: SQL migration templates
- **MCP Server**: Database query and inspection tools
- **Steering Files**: Auto-activated database guidance

---

## What This Power Provides

### 1. Schema Design Guidelines

Comprehensive database design documentation:

- **Normalization**: When and how to normalize
- **Indexing Strategy**: Index design patterns
- **Partitioning**: Table partitioning strategies
- **Constraints**: Foreign keys, checks, unique constraints

### 2. Migration Templates

SQL migration templates for common operations:

- **Add Column**: Safe column addition
- **Add Index**: Concurrent index creation
- **Add Table**: Table creation with constraints
- **Data Migration**: Safe data transformation

### 3. MCP Server (Optional)

Database inspection and query tools:

- `inspect_schema` — View table structure
- `explain_query` — Analyze query performance
- `check_indexes` — Verify index usage
- `validate_migration` — Test migration safety

**Configuration:** `.kiro/powers/database-ops/mcp-servers/database-mcp.json`

---

## How to Use This Power

### Activate the Power

\`\`\`typescript
kiroPowers({
action: "activate",
powerName: "database-ops",
});
\`\`\`

### With MCP Server

If you want to use the database inspection tools:

1. Configure MCP server in `.kiro/settings/mcp.json`
2. Activate the power
3. Use MCP tools via `kiroPowers` tool

---

## Quick Start Examples

### Example 1: Design New Table

\`\`\`typescript
// 1. Activate power
kiroPowers({ action: "activate", powerName: "database-ops" });

// 2. Read schema design guidelines
readFile({
path: ".kiro/powers/database-ops/guidelines/schema-design.md",
explanation: "Loading schema design patterns"
});

// 3. Use table creation template
readFile({
path: ".kiro/powers/database-ops/templates/add-table.sql",
explanation: "Loading table creation template"
});

// 4. Design table following guidelines
\`\`\`

### Example 2: Inspect Existing Schema (MCP)

\`\`\`typescript
// 1. Activate power
kiroPowers({ action: "activate", powerName: "database-ops" });

// 2. Use MCP tool to inspect schema
kiroPowers({
action: "use",
powerName: "database-ops",
serverName: "database-mcp",
toolName: "inspect_schema",
arguments: { table: "users" }
});
\`\`\`

---

## MCP Server Configuration

### Setup

Add to `.kiro/settings/mcp.json`:

\`\`\`json
{
"mcpServers": {
"database-mcp": {
"command": "uvx",
"args": ["database-mcp-server@latest"],
"env": {
"DB_CONNECTION_STRING": "postgresql://localhost/mydb"
}
}
}
}
\`\`\`

### Available Tools

| Tool                 | Purpose                   | Arguments           |
| -------------------- | ------------------------- | ------------------- |
| `inspect_schema`     | View table structure      | `table: string`     |
| `explain_query`      | Analyze query performance | `query: string`     |
| `check_indexes`      | Verify index usage        | `table: string`     |
| `validate_migration` | Test migration safety     | `migration: string` |

---

## References

- **Guidelines**: `.kiro/powers/database-ops/guidelines/`
- **Templates**: `.kiro/powers/database-ops/templates/`
- **MCP Config**: `.kiro/powers/database-ops/mcp-servers/`

---

**Power Maintained By:** Data Engineering Team  
**Last Updated:** 2026-05-06
```

---

## Best Practices

### 1. Power Naming

**Good:**

- `company-pipeline` — Clear, descriptive
- `cc00-engineering` — Recognizable acronym
- `organizational-agents` — Specific domain

**Bad:**

- `power1` — Not descriptive
- `my-power` — Too generic
- `CompanyPipeline` — Use kebab-case

### 2. Scope Definition

**Do:**

- Package related resources together
- Include everything needed for the domain
- Provide comprehensive documentation

**Don't:**

- Mix unrelated resources
- Create overlapping powers
- Leave gaps in coverage

### 3. Documentation Quality

**Do:**

- Provide clear activation instructions
- Include multiple examples
- Document all capabilities thoroughly
- Add troubleshooting section

**Don't:**

- Assume prior knowledge
- Skip examples
- Leave capabilities undocumented
- Forget troubleshooting

### 4. Template Organization

**Do:**

- Group templates by type
- Provide clear naming
- Include usage instructions

**Don't:**

- Mix templates with other files
- Use ambiguous names
- Forget to document templates

### 5. MCP Integration

**Do:**

- Make MCP servers optional
- Provide clear setup instructions
- Document all tools
- Include configuration examples

**Don't:**

- Require MCP for basic usage
- Assume MCP is configured
- Leave tools undocumented
- Skip configuration examples

---

## Troubleshooting

### Issue: Power Too Large

**Symptoms:**

- POWER.md exceeds 1000 lines
- Too many capabilities
- Difficult to navigate

**Solution:**

- Split into multiple powers
- Move detailed docs to separate files
- Use references instead of inline content

### Issue: Unclear Activation

**Symptoms:**

- Users don't know how to activate
- Activation doesn't work as expected
- Missing dependencies

**Solution:**

- Add clear activation section
- Document prerequisites
- Provide activation examples
- Test activation process

### Issue: Missing Examples

**Symptoms:**

- Users struggle to use the power
- Unclear how to apply capabilities
- No concrete guidance

**Solution:**

- Add 3-5 quick start examples
- Cover common use cases
- Include complete code
- Show expected results

### Issue: Poor Organization

**Symptoms:**

- Hard to find information
- Inconsistent structure
- Missing sections

**Solution:**

- Follow template structure
- Use consistent headings
- Add table of contents
- Group related content

---

## Quality Checklist

Before finalizing a power:

- [ ] Header metadata complete
- [ ] Overview explains purpose
- [ ] All capabilities documented
- [ ] Activation instructions clear
- [ ] Usage patterns provided
- [ ] Governance rules defined
- [ ] 3-5 examples included
- [ ] Reference material complete
- [ ] Troubleshooting section added
- [ ] Templates organized (if applicable)
- [ ] MCP documented (if applicable)
- [ ] File formatted with Prettier
- [ ] No placeholder text remains

---

## Related Documentation

- **Power Template** — `.kiro/templates/power/power_template.md`
- **Existing Powers** — `.kiro/powers/`
- **Skills** — `.kiro/skills/`
- **Steering Files** — `.kiro/steering/`
- **AGENTS.md** — Workspace conventions

---

**Guide Version:** 1.0.0  
**Last Updated:** 2026-05-06  
**Maintained By:** Workspace governance
