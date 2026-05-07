# Steering Template Usage Guide

This guide explains how to create Kiro steering files using the `steering_template.md` template.

---

## Table of Contents

1. [Understanding Steering Files](#understanding-steering-files)
2. [Inclusion Types](#inclusion-types)
3. [When to Create Steering Files](#when-to-create-steering-files)
4. [Step-by-Step Guide](#step-by-step-guide)
5. [Section-by-Section Guide](#section-by-section-guide)
6. [Complete Examples](#complete-examples)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Understanding Steering Files

### What Are Steering Files?

Steering files provide **contextual guidance and rules** that help agents work effectively in specific scenarios. They are automatically or manually included in agent context based on inclusion rules.

**Key Characteristics:**

- **Contextual** — Provide guidance for specific situations
- **Conditional** — Can auto-activate based on file patterns
- **Mandatory** — Rules in steering files must be followed
- **Lightweight** — Focused on specific topics or workflows

### Steering Files vs. Skills

| Aspect          | Steering Files               | Skills                          |
| --------------- | ---------------------------- | ------------------------------- |
| **Purpose**     | Provide guidance and rules   | Define how to do work           |
| **Activation**  | Auto, fileMatch, or manual   | Via `discloseContext` tool      |
| **Structure**   | Principles, rules, workflows | Methodology, templates, quality |
| **Scope**       | Broad guidance               | Specific capability             |
| **Enforcement** | Mandatory rules              | Executable specifications       |

### Steering Files in the Ecosystem

Steering files are used for:

- **Workspace conventions** — Core rules (always active)
- **Pipeline guidance** — Pipeline-specific rules (fileMatch)
- **Technology guidance** — Platform-specific rules (fileMatch)
- **Reference material** — Optional documentation (manual)

---

## Inclusion Types

### 1. Auto Inclusion

**When to Use:** Core conventions that apply to ALL work

**Activation:** Always included in every Kiro session

**Frontmatter:**

```yaml
---
inclusion: auto
description: { Description }
version: "1.0.0"
---
```

**Examples:**

- `workspace-conventions.md` — Core workspace rules
- `git-workflow.md` — Git safety and worktree patterns

**Use Cases:**

- Mandatory workspace conventions
- Universal safety rules
- Core agent behavior rules
- Fundamental principles

### 2. File Match Inclusion

**When to Use:** Context-specific guidance that activates for certain files

**Activation:** Activates when files matching the pattern are read into context

**Frontmatter:**

```yaml
---
inclusion: fileMatch
fileMatchPattern: { pattern }
description: { Description }
version: "1.0.0"
---
```

**Pattern Examples:**

- `README*` — Activates for README files
- `*.pipeline.md` — Activates for pipeline documents
- `company/pipeline/**` — Activates for any file in company/pipeline
- `**/*.test.ts` — Activates for test files

**Examples:**

- `mobile-pipeline.md` — Mobile pipeline rules (pattern: `company/pipeline/mobile-development/**`)
- `android-development.md` — Android guidance (pattern: `**/*android*`)

**Use Cases:**

- Pipeline-specific rules
- Platform-specific guidance
- Technology-specific conventions
- Domain-specific best practices

### 3. Manual Inclusion

**When to Use:** Optional reference material

**Activation:** User must explicitly include via context key (`#`)

**Frontmatter:**

```yaml
---
inclusion: manual
description: { Description }
version: "1.0.0"
---
```

**Examples:**

- Advanced reference material
- Optional deep-dives
- Historical documentation
- Specialized guidance

**Use Cases:**

- Optional reference documentation
- Advanced topics
- Historical context
- Specialized scenarios

---

## When to Create Steering Files

### Create a Steering File When:

- You have **general guidance** that doesn't fit in a skill
- You need **conditional activation** based on file context
- You want to provide **reference material** without methodology
- You need to document **rules and conventions**
- The guidance applies to **multiple agents** or scenarios

**Examples:**

- Workspace conventions
- Pipeline-specific rules
- Platform-specific guidance
- Git workflow patterns
- Security best practices

### Don't Create a Steering File When:

- You need **detailed methodology** (use skills instead)
- You're documenting **a specific capability** (use skills)
- You need **templates and quality standards** (use skills)
- The content is **agent-specific** (put in agent profile)
- It's **one-time information** (use documentation)

---

## Step-by-Step Guide

### Step 1: Determine Inclusion Type

**Questions to Answer:**

1. Should this be always active? → `auto`
2. Should it activate for specific files? → `fileMatch`
3. Should it be optional? → `manual`

### Step 2: Create File

```bash
cp .kiro/templates/steering/steering_template.md .kiro/steering/new-guidance.md
```

### Step 3: Fill in Frontmatter

```yaml
---
inclusion: { auto|fileMatch|manual }
fileMatchPattern: { pattern } # Only for fileMatch
description: { One-line description }
version: "1.0.0"
---
```

**Example (Auto):**

```yaml
---
inclusion: auto
description: Core workspace conventions and rules from AGENTS.md
version: "1.0.0"
---
```

**Example (FileMatch):**

```yaml
---
inclusion: fileMatch
fileMatchPattern: company/pipeline/mobile-development/**
description: Mobile pipeline-specific rules and conventions
version: "1.0.0"
---
```

**Example (Manual):**

```yaml
---
inclusion: manual
description: Advanced Git worktree patterns for complex scenarios
version: "1.0.0"
---
```

### Step 4: Write Introduction

```markdown
# {Steering File Title}

{Brief introduction explaining what this steering file covers and when it should be used.}
```

### Step 5: Document Inclusion Behavior

```markdown
## Inclusion Behavior

**Inclusion Type:** `{auto|fileMatch|manual}`

{Explain when this steering file is activated}
```

### Step 6: Define Purpose and Scope

```markdown
## Purpose and Scope

### What This Steering File Covers

- {Topic 1}
- {Topic 2}
- {Topic 3}

### What This Steering File Does NOT Cover

- {Out of scope 1}
- {Out of scope 2}
```

### Step 7: Document Core Principles

```markdown
## Core Principles

### Principle 1: {Principle Name}

{Detailed explanation}

**Rationale:**
{Why this principle exists}

**Application:**
{How to apply in practice}
```

### Step 8: Define Rules and Conventions

```markdown
## Rules and Conventions

### {Rule Category}

| Rule         | Applies To | Detail        |
| ------------ | ---------- | ------------- |
| **{Rule 1}** | {Scope}    | {Explanation} |
| **{Rule 2}** | {Scope}    | {Explanation} |
```

### Step 9: Add Workflows (If Applicable)

```markdown
## Workflows and Processes

### {Workflow Name}

**Steps:**

1. **{Step 1}** — {Description}
2. **{Step 2}** — {Description}
3. **{Step 3}** — {Description}
```

### Step 10: Validate and Format

```bash
prettier --write .kiro/steering/new-guidance.md
```

---

## Section-by-Section Guide

### Frontmatter (Required)

```yaml
---
inclusion: { auto|fileMatch|manual }
fileMatchPattern: { pattern } # Only for fileMatch
description: { One-line description }
version: "1.0.0"
---
```

**Guidelines:**

- `inclusion` — Choose based on activation needs
- `fileMatchPattern` — Use glob patterns for fileMatch
- `description` — Keep under 100 characters
- `version` — Start with "1.0.0"

### Title and Introduction (Required)

```markdown
# {Steering File Title}

{Brief introduction}
```

**Guidelines:**

- Use title case for title
- Introduction: 1-2 paragraphs
- Explain what and when

### Inclusion Behavior (Required)

```markdown
## Inclusion Behavior

**Inclusion Type:** `{type}`

{Explanation of when activated}
```

**Guidelines:**

- Clearly state inclusion type
- Explain activation conditions
- Provide examples if fileMatch

### Purpose and Scope (Required)

```markdown
## Purpose and Scope

### What This Steering File Covers

- {Topic 1}
- {Topic 2}

### What This Steering File Does NOT Cover

- {Out of scope 1}
- {Out of scope 2}

### When to Use This Guidance

**Use this when:**

- {Scenario 1}
- {Scenario 2}

**Do NOT use this when:**

- {Anti-pattern 1}
- {Anti-pattern 2}
```

**Guidelines:**

- Be specific about scope
- Explicitly state what's NOT covered
- Provide usage scenarios

### Core Principles (Required)

```markdown
## Core Principles

### Principle 1: {Name}

{Explanation}

**Rationale:**
{Why}

**Application:**
{How}

**Examples:**

**Good:**
\`\`\`
{Example}
\`\`\`

**Bad:**
\`\`\`
{Counter-example}
\`\`\`
```

**Guidelines:**

- 3-5 core principles
- Explain rationale
- Show application
- Provide examples

### Rules and Conventions (Required)

```markdown
## Rules and Conventions

### {Category}

| Rule         | Applies To | Detail        |
| ------------ | ---------- | ------------- |
| **{Rule 1}** | {Scope}    | {Explanation} |
| **{Rule 2}** | {Scope}    | {Explanation} |
```

**Guidelines:**

- Group rules by category
- Use tables for clarity
- Be specific about scope
- Explain each rule

### Workflows and Processes (Optional)

```markdown
## Workflows and Processes

### {Workflow Name}

{Description}

**Steps:**

1. **{Step 1}** — {Description}
2. **{Step 2}** — {Description}
```

**Guidelines:**

- Include if guidance involves processes
- Use numbered steps
- Provide examples

### Standards and Formats (Optional)

```markdown
## Standards and Formats

### {Standard Category}

| Item Type | Convention   | Example   |
| --------- | ------------ | --------- |
| {Item 1}  | {Convention} | {Example} |
| {Item 2}  | {Convention} | {Example} |
```

**Guidelines:**

- Document naming conventions
- Provide format specifications
- Include examples

### Decision Trees (Optional)

```markdown
## Decision Trees

### When to {Decision Point}

\`\`\`
Question: {Question}
├─ If {Condition A}
│ └─ Action: {What to do}
├─ If {Condition B}
│ └─ Action: {What to do}
\`\`\`
```

**Guidelines:**

- Use for complex decisions
- Provide clear conditions
- Show all branches

### Templates and Examples (Optional)

```markdown
## Templates and Examples

### {Template Name}

**Purpose:** {What for}

**Format:**

\`\`\`markdown
{template-content}
\`\`\`
```

**Guidelines:**

- Include if guidance involves artifacts
- Provide complete templates
- Show examples

### Anti-Patterns (Optional)

```markdown
## Anti-Patterns

### Anti-Pattern 1: {Name}

**Description:** {What it looks like}

**Why It's Wrong:**
{Explanation}

**Example:**

\`\`\`
// BAD
{bad-example}
\`\`\`

**Correct Approach:**

\`\`\`
// GOOD
{good-example}
\`\`\`
```

**Guidelines:**

- Document common mistakes
- Explain why they're wrong
- Show correct approach

### Best Practices (Required)

```markdown
## Best Practices

1. **{Practice 1}** — {Explanation}
2. **{Practice 2}** — {Explanation}
3. **{Practice 3}** — {Explanation}
```

**Guidelines:**

- List 5-10 best practices
- Explain rationale
- Be specific

### Common Mistakes (Optional)

```markdown
## Common Mistakes

| Mistake     | Impact        | Prevention     |
| ----------- | ------------- | -------------- |
| {Mistake 1} | {What breaks} | {How to avoid} |
| {Mistake 2} | {What breaks} | {How to avoid} |
```

**Guidelines:**

- Document frequent errors
- Explain impact
- Provide prevention strategies

### Related Steering Files (Optional)

```markdown
## Related Steering Files

- **{File 1}** — `.kiro/steering/{file-1}.md` — {Relationship}
- **{File 2}** — `.kiro/steering/{file-2}.md` — {Relationship}
```

**Guidelines:**

- Link to related guidance
- Explain relationships
- Help navigation

### References (Required)

```markdown
## References

### Internal Documentation

- **AGENTS.md** — {Section references}
- **{Doc 1}** — `{path}` — {Description}

### External Resources

- **{Resource 1}** — {URL} — {Description}
```

**Guidelines:**

- Reference AGENTS.md sections
- Link to related docs
- Include external resources

### Maintenance (Required)

```markdown
## Maintenance

**Version:** 1.0.0  
**Last Updated:** {YYYY-MM-DD}  
**Maintained By:** {Team/agent}  
**Review Frequency:** {How often}

### Version History

| Version | Date   | Changes         |
| ------- | ------ | --------------- |
| 1.0.0   | {Date} | Initial version |
```

**Guidelines:**

- Track version history
- Document maintenance ownership
- Specify review frequency

---

## Complete Examples

### Example 1: Auto Inclusion (Core Conventions)

**File:** `.kiro/steering/workspace-conventions.md`

```yaml
---
inclusion: auto
description: Core workspace conventions and rules from AGENTS.md
version: "1.0.0"
---
```

```markdown
# Workspace Conventions

This steering file provides core workspace conventions that apply to all work in the `agent-global-base` workspace.

---

## Inclusion Behavior

**Inclusion Type:** `auto`

This file is automatically included in all Kiro sessions. It is always active regardless of context.

---

## Purpose and Scope

### What This Steering File Covers

- File and folder naming conventions
- Document authority hierarchy
- Company personnel tier system
- Pipeline progress monitoring
- Context and session management

### When to Use This Guidance

**Use this when:**

- Creating any new files or folders
- Resolving conflicting documentation
- Understanding organizational structure
- Managing long-running sessions

---

## Core Principles

### Principle 1: Consistent Naming

All files and folders use kebab-case naming.

**Rationale:**
Consistency enables predictable navigation and programmatic access.

**Application:**

- Directories: `casual-games`, `brand-design`
- Files: `profile.md`, `pipeline.md`

**Examples:**

**Good:**
\`\`\`
company/departments/research-develop/
.kiro/skills/product-management/
\`\`\`

**Bad:**
\`\`\`
company/departments/ResearchDevelop/
.kiro/skills/ProductManagement/
\`\`\`

---

## Rules and Conventions

### File and Folder Naming

| Item Type              | Convention                |
| ---------------------- | ------------------------- |
| Directory/folder names | kebab-case                |
| Agent profile files    | Always named `profile.md` |
| Skill files            | `skills/<skill-name>.md`  |
| Pipeline documents     | `pipeline.md`             |

---

## Best Practices

1. **Always use kebab-case** — Never use camelCase or PascalCase for files/folders
2. **Follow authority hierarchy** — When sources conflict, use the precedence order
3. **Maintain progress files** — For Stage 4+ projects, keep progress.md updated
4. **Run Prettier** — Format all files before committing

---

## References

### Internal Documentation

- **AGENTS.md** — § 8.1 File and Folder Naming
- **AGENTS.md** — § 8.2 Document Authority Hierarchy

---

**Version:** 1.0.0  
**Last Updated:** 2026-05-06  
**Maintained By:** Workspace governance
```

### Example 2: FileMatch Inclusion (Pipeline-Specific)

**File:** `.kiro/steering/mobile-pipeline.md`

```yaml
---
inclusion: fileMatch
fileMatchPattern: company/pipeline/mobile-development/**
description: Mobile pipeline-specific rules and conventions
version: "1.0.0"
---
```

```markdown
# Mobile Pipeline Guidance

This steering file provides mobile-specific guidance for the company's 13-stage development pipeline.

---

## Inclusion Behavior

**Inclusion Type:** `fileMatch`

**Pattern:** `company/pipeline/mobile-development/**`

This file activates when any file in the mobile development pipeline directory is read into context.

---

## Purpose and Scope

### What This Steering File Covers

- Mobile-specific pipeline rules
- Android and iOS platform considerations
- Mobile testing requirements
- Mobile security standards

### What This Steering File Does NOT Cover

- General pipeline rules (see `company-pipeline-overview.md`)
- Web or backend pipelines
- Studio pipelines

---

## Core Principles

### Principle 1: Platform Parity

Android and iOS implementations must have feature parity unless explicitly documented otherwise.

**Rationale:**
Users expect consistent experiences across platforms.

**Application:**

- Design features for both platforms simultaneously
- Document platform-specific variations in PRD
- Test on both platforms before release

---

## Rules and Conventions

### Mobile-Specific Rules

| Rule                         | Applies To   | Detail                                   |
| ---------------------------- | ------------ | ---------------------------------------- |
| **Platform Parity Required** | All features | Android and iOS must match               |
| **Device Testing Required**  | Stage 7      | Test on real devices, not just emulators |
| **App Store Compliance**     | Stage 10     | Verify compliance before release         |

---

## Workflows and Processes

### Mobile Testing Workflow

**Steps:**

1. **Unit Tests** — Run on both platforms
2. **Integration Tests** — Test platform-specific integrations
3. **Device Testing** — Test on real devices (min 3 per platform)
4. **Performance Testing** — Verify 60fps on mid-range devices

---

## Best Practices

1. **Test on real devices** — Emulators don't catch all issues
2. **Consider offline scenarios** — Mobile apps often lose connectivity
3. **Optimize for battery** — Monitor battery usage during testing
4. **Follow platform guidelines** — iOS HIG and Android Material Design

---

## References

### Internal Documentation

- **AGENTS.md** — § 4.4 Company Pipeline
- **company-pipeline-overview.md** — General pipeline rules

---

**Version:** 1.0.0  
**Last Updated:** 2026-05-06  
**Maintained By:** VP Mobile
```

### Example 3: Manual Inclusion (Reference Material)

**File:** `.kiro/steering/advanced-git-patterns.md`

```yaml
---
inclusion: manual
description: Advanced Git worktree patterns for complex multi-agent scenarios
version: "1.0.0"
---
```

```markdown
# Advanced Git Patterns

This steering file provides advanced Git patterns for complex scenarios.

---

## Inclusion Behavior

**Inclusion Type:** `manual`

This file must be explicitly included via context key (`#`). It is not automatically activated.

---

## Purpose and Scope

### What This Steering File Covers

- Advanced worktree patterns
- Complex merge strategies
- Multi-agent conflict resolution
- Performance optimization

### When to Use This Guidance

**Use this when:**

- Managing 5+ concurrent agents
- Dealing with complex merge conflicts
- Optimizing worktree performance
- Implementing custom merge strategies

---

## Advanced Patterns

### Pattern 1: Hierarchical Worktrees

For complex task graphs with dependencies:

\`\`\`
master
├── agent/orchestrator/main
│ ├── agent/backend/api
│ └── agent/frontend/ui
└── agent/database/schema
\`\`\`

**Implementation:**

\`\`\`bash

# Create orchestrator worktree

git worktree add ../agent-orchestrator -b agent/orchestrator/main

# Create dependent worktrees

cd ../agent-orchestrator
git worktree add ../agent-backend -b agent/backend/api
git worktree add ../agent-frontend -b agent/frontend/ui
\`\`\`

---

## Best Practices

1. **Limit worktree depth** — Max 2 levels of hierarchy
2. **Clean up regularly** — Remove unused worktrees daily
3. **Monitor disk usage** — Worktrees consume disk space
4. **Use sparse checkouts** — For large repositories

---

## References

### Internal Documentation

- **git-workflow.md** — Basic Git patterns
- **AGENTS.md** — § 8.5 Git and Version Control

---

**Version:** 1.0.0  
**Last Updated:** 2026-05-06  
**Maintained By:** DevOps Lead
```

---

## Best Practices

### 1. Inclusion Type Selection

**Auto Inclusion:**

- Use sparingly (only 2-3 files)
- Core conventions only
- Universal rules

**FileMatch Inclusion:**

- Most common type
- Context-specific guidance
- Use specific patterns

**Manual Inclusion:**

- Reference material
- Advanced topics
- Optional deep-dives

### 2. Pattern Specificity

**Good Patterns:**

- `company/pipeline/mobile-development/**` — Specific directory
- `**/*android*` — Technology-specific
- `*.pipeline.md` — File type-specific

**Bad Patterns:**

- `**/*` — Too broad
- `*` — Matches everything
- `company/**` — Too general

### 3. Scope Definition

**Do:**

- Be specific about what's covered
- Explicitly state what's NOT covered
- Provide usage scenarios

**Don't:**

- Make steering files too broad
- Overlap with other steering files
- Include methodology (use skills)

### 4. Rule Documentation

**Do:**

- Use tables for rules
- Explain rationale
- Provide examples

**Don't:**

- List rules without explanation
- Forget to show examples
- Leave scope ambiguous

### 5. Maintenance

**Do:**

- Track version history
- Document ownership
- Specify review frequency
- Update regularly

**Don't:**

- Let steering files become stale
- Forget to update version
- Leave outdated information

---

## Troubleshooting

### Issue: Steering File Not Activating

**Symptoms:**

- FileMatch pattern not triggering
- Expected guidance not appearing

**Solution:**

- Check pattern syntax (use glob patterns)
- Verify file paths match pattern
- Test pattern with actual files
- Check frontmatter is valid YAML

### Issue: Too Many Auto Inclusions

**Symptoms:**

- Context bloat
- Slow agent responses
- Conflicting guidance

**Solution:**

- Convert to fileMatch inclusion
- Split into multiple files
- Make some manual inclusion
- Review necessity of auto inclusion

### Issue: Unclear Guidance

**Symptoms:**

- Agents don't follow rules
- Inconsistent application
- Confusion about scope

**Solution:**

- Add more examples
- Clarify scope section
- Provide decision trees
- Add anti-patterns

### Issue: Overlapping Steering Files

**Symptoms:**

- Multiple files cover same topic
- Conflicting rules
- Confusion about which to follow

**Solution:**

- Consolidate related guidance
- Clarify scope boundaries
- Reference related files
- Establish precedence

---

## Quality Checklist

Before finalizing a steering file:

- [ ] Frontmatter is complete and valid
- [ ] Inclusion type is appropriate
- [ ] FileMatch pattern is specific (if applicable)
- [ ] Title and introduction are clear
- [ ] Inclusion behavior is documented
- [ ] Purpose and scope are defined
- [ ] Core principles are explained
- [ ] Rules are documented with examples
- [ ] Best practices are listed
- [ ] References are included
- [ ] Maintenance section is complete
- [ ] File is formatted with Prettier
- [ ] No placeholder text remains

---

## Related Documentation

- **Steering Template** — `.kiro/templates/steering/steering_template.md`
- **Existing Steering Files** — `.kiro/steering/`
- **Skills** — `.kiro/skills/`
- **Powers** — `.kiro/powers/`
- **AGENTS.md** — Workspace conventions

---

**Guide Version:** 1.0.0  
**Last Updated:** 2026-05-06  
**Maintained By:** Workspace governance
