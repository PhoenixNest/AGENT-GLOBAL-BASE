# Skill Template Usage Guide

This guide explains how to create Kiro skills using the skill templates: `skill_template.md` (parent router) and `sub_skill_template.md` (detailed sub-skills).

---

## Table of Contents

1. [Understanding Skills](#understanding-skills)
2. [Skill Architecture](#skill-architecture)
3. [When to Create Skills](#when-to-create-skills)
4. [Parent Skill Template Guide](#parent-skill-template-guide)
5. [Sub-Skill Template Guide](#sub-skill-template-guide)
6. [Complete Workflow](#complete-workflow)
7. [Examples](#examples)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Understanding Skills

### What Are Skills?

Skills are **executable specifications** that define how agents produce work. They are not just documentation — they are contracts that agents must follow when performing specific tasks.

**Key Characteristics:**

- **Executable** — Agents follow skills as step-by-step instructions
- **Specific** — Each skill covers a narrow, well-defined capability
- **Testable** — Skills include quality criteria and validation methods
- **Reusable** — Multiple agents can use the same skill

### Skills vs. Documentation

| Aspect          | Skills                          | Documentation             |
| --------------- | ------------------------------- | ------------------------- |
| **Purpose**     | Define HOW to do work           | Explain WHAT something is |
| **Audience**    | AI agents (Type B)              | Humans and agents         |
| **Structure**   | Methodology + templates         | Narrative explanation     |
| **Validation**  | Quality criteria + checklists   | Optional                  |
| **Enforcement** | Mandatory for agents with skill | Reference only            |

### Skills in the Ecosystem

Skills are referenced by:

- **Agent profiles** — Agents list their skills in the "Agent Skills" section
- **Pipeline stages** — Stages specify which skills are required
- **Powers** — Powers package related skills together
- **Steering files** — Steering files may reference skills for context

---

## Skill Architecture

### Two-Tier Hierarchy

```
.kiro/skills/
├── domain-name/
│   ├── SKILL.md              # Parent skill (router)
│   └── references/           # Sub-skills directory
│       ├── sub-skill-1.md    # Detailed capability
│       ├── sub-skill-2.md    # Detailed capability
│       └── sub-skill-3.md    # Detailed capability
```

### Parent Skill (Router)

**Purpose:** Entry point that routes agents to specific sub-skills

**Contents:**

- Domain overview
- List of available sub-skills
- Related domains
- Activation instructions

**Size:** ~100 lines

**Example:** `.kiro/skills/product-management/SKILL.md`

### Sub-Skills (Detailed)

**Purpose:** Detailed methodology for a specific capability

**Contents:**

- Comprehensive methodology
- Templates and formats
- Quality standards
- Examples and anti-examples
- Integration guidance

**Size:** ~300-500 lines

**Example:** `.kiro/skills/product-management/references/prd-authorship.md`

---

## When to Create Skills

### Create a New Domain When:

- You have a **new discipline** not covered by existing domains
- You have **5+ related capabilities** that form a cohesive domain
- The capabilities are used by **multiple agents**
- The domain has **distinct methodology** from existing domains

**Examples:**

- `product-management` — Product strategy, PRD authorship, stage gates
- `android-engineering` — Android development, Kotlin, testing
- `llm-engineering` — LLM system design, context engineering, RAG

### Create a New Sub-Skill When:

- You have a **specific capability** within an existing domain
- The capability requires **detailed methodology** (not just documentation)
- Multiple agents need to **produce the same type of artifact**
- The capability has **quality standards** that must be enforced

**Examples:**

- `prd-authorship.md` — How to write PRDs
- `kotlin-advanced.md` — Advanced Kotlin patterns
- `context-engineering-design.md` — Context window design

### Don't Create a Skill When:

- The information is **general knowledge** (use steering files instead)
- It's **one-time guidance** (use steering files)
- It's **reference material** (use documentation)
- It's **tool-specific** (document in the tool's README)

---

## Parent Skill Template Guide

### Step-by-Step: Creating a Parent Skill

#### Step 1: Create Domain Directory

```bash
mkdir -p .kiro/skills/new-domain/references
```

#### Step 2: Copy Template

```bash
cp .kiro/templates/skill/skill_template.md .kiro/skills/new-domain/SKILL.md
```

#### Step 3: Fill in YAML Frontmatter

```yaml
---
name: new-domain
description: One-line description of what this skill domain covers
---
```

**Guidelines:**

- `name` — Use kebab-case, match directory name
- `description` — Keep under 100 characters, focus on scope

**Example:**

```yaml
---
name: product-management
description: Super-Skill router for Product Management. Dynamically loads specific sub-skills from its references/ directory covering product strategy, PRD authorship, and stage gates.
---
```

#### Step 4: Write Domain Coverage

Explain what this domain encompasses:

```markdown
## Domain Coverage

- {Major category 1}
- {Major category 2}
- {Major category 3}
- {Major category 4}
```

**Example:**

```markdown
## Domain Coverage

- Mobile product strategy and vision
- Product Requirements Document (PRD) authorship
- Product stage gates and approval workflows
- Product quality standards and acceptance criteria
```

#### Step 5: List Sub-Skills

List all sub-skills with brief descriptions:

```markdown
## How to Use

When you need expertise in {Domain Name}, explore the `references/` directory and read the highly specific sub-skill markdown files:

- `sub-skill-1.md` — {Brief description}
- `sub-skill-2.md` — {Brief description}
- `sub-skill-3.md` — {Brief description}
```

**Example:**

```markdown
## How to Use

When you need expertise in Product Management, explore the `references/` directory and read the highly specific sub-skill markdown files:

- `mobile-product-strategy.md` — Product vision, strategy, and roadmap planning
- `prd-authorship.md` — PRD structure, content, and quality standards
- `product-stage-gates.md` — Stage gate enforcement and approval workflows
```

#### Step 6: Add Related Domains

List related skill domains:

```markdown
## Related Domains

- `related-domain-1` — {Relationship}
- `related-domain-2` — {Relationship}
- `related-domain-3` — {Relationship}
```

**Example:**

```markdown
## Related Domains

- `product-design` — UI/UX design and prototyping
- `engineering` — Technical specification and implementation
- `technology-strategy` — Architecture decisions and technology selection
```

#### Step 7: Optional Sections

Add optional sections as needed:

**Available Sub-Skills Table:**

```markdown
## Available Sub-Skills

| Skill File       | Location               | Description            |
| ---------------- | ---------------------- | ---------------------- |
| `sub-skill-1.md` | `{domain}/references/` | {Detailed description} |
| `sub-skill-2.md` | `{domain}/references/` | {Detailed description} |
```

**Domain Ownership:**

```markdown
## Domain Ownership

**Primary Users:**

- {Agent Role 1} — {Usage context}
- {Agent Role 2} — {Usage context}
```

#### Step 8: Validate and Format

```bash
prettier --write .kiro/skills/new-domain/SKILL.md
```

### Parent Skill Checklist

Before finalizing a parent skill:

- [ ] YAML frontmatter is complete
- [ ] Domain coverage is clear and comprehensive
- [ ] All sub-skills are listed with descriptions
- [ ] Related domains are identified
- [ ] File is formatted with Prettier
- [ ] No placeholder text remains (`{...}`)

---

## Sub-Skill Template Guide

### Step-by-Step: Creating a Sub-Skill

#### Step 1: Copy Template

```bash
cp .kiro/templates/skill/sub_skill_template.md .kiro/skills/domain-name/references/new-skill.md
```

#### Step 2: Fill in Header

```markdown
# {Sub-Skill Name}

**Domain:** `{parent-domain-name}`  
**Version:** 1.0.0  
**Last Updated:** {YYYY-MM-DD}  
**Status:** Active
```

**Example:**

```markdown
# PRD Authorship

**Domain:** `product-management`  
**Version:** 1.0.0  
**Last Updated:** 2026-05-06  
**Status:** Active
```

#### Step 3: Write Overview

Provide a comprehensive overview:

```markdown
## Overview

{Explain what this sub-skill covers, its scope, purpose, and when to use it.}
```

**Guidelines:**

- 2-3 paragraphs
- Explain the "why" not just the "what"
- Set expectations for what agents will learn

**Example:**

```markdown
## Overview

This skill defines how to author Product Requirements Documents (PRDs) for mobile platform features. It covers PRD structure, content requirements, quality standards, and the handoff process to design and engineering teams.

PRDs are the foundational artifact in Stage 1 of the company pipeline. They translate product vision into concrete requirements that design and engineering teams can execute against. A well-written PRD reduces ambiguity, prevents scope creep, and ensures all stakeholders have a shared understanding of what will be built.

This skill is mandatory for all agents producing PRDs, including the CPO, VPs, and product managers.
```

#### Step 4: Define Scope

Clearly define what's in and out of scope:

```markdown
## Scope

**This skill covers:**

- {Capability 1}
- {Capability 2}
- {Capability 3}

**This skill does NOT cover:**

- {Out of scope 1}
- {Out of scope 2}
```

**Example:**

```markdown
## Scope

**This skill covers:**

- PRD structure and required sections
- Content quality standards for each section
- User story formatting and acceptance criteria
- Handoff process to design and engineering

**This skill does NOT cover:**

- Product strategy or vision (see `mobile-product-strategy.md`)
- Design specifications (see `product-design` domain)
- Technical specifications (see `engineering` domain)
```

#### Step 5: Document Core Concepts

Explain key concepts agents need to understand:

```markdown
## Core Concepts

### {Concept 1}

{Detailed explanation}

**Key Principles:**

1. **{Principle 1}** — {Explanation}
2. **{Principle 2}** — {Explanation}
```

**Example:**

```markdown
## Core Concepts

### User-Centered Requirements

PRDs must be written from the user's perspective, not the system's perspective. Every requirement should answer: "What problem does this solve for the user?"

**Key Principles:**

1. **Jobs-To-Be-Done Framework** — Frame requirements as jobs users are trying to accomplish
2. **Outcome-Focused** — Specify desired outcomes, not implementation details
3. **Measurable Success** — Define how success will be measured
```

#### Step 6: Define Methodology

Provide step-by-step methodology:

```markdown
## Methodology

### Step 1: {Step Name}

{Detailed description}

**Inputs:**

- {Required input 1}
- {Required input 2}

**Outputs:**

- {Expected output 1}
- {Expected output 2}

**Quality Criteria:**

- {Criterion 1}
- {Criterion 2}
```

**Example:**

```markdown
## Methodology

### Step 1: Problem Framing

Define the problem you're solving before writing requirements.

**Inputs:**

- User research findings
- Market analysis
- Stakeholder interviews

**Outputs:**

- Problem statement (2-3 sentences)
- Target user personas
- Success metrics

**Quality Criteria:**

- Problem is specific and measurable
- Target users are clearly defined
- Success metrics are quantifiable
```

#### Step 7: Provide Templates

Include templates for artifacts:

```markdown
## Templates and Formats

### {Artifact Type}

**Structure:**

\`\`\`markdown

# {Artifact Title}

## Section 1

{Content guidelines}

## Section 2

{Content guidelines}
\`\`\`

**Required Sections:**

| Section     | Purpose   | Required?   |
| ----------- | --------- | ----------- |
| {Section 1} | {Purpose} | ✅ Yes      |
| {Section 2} | {Purpose} | ⚠️ Optional |
```

#### Step 8: Define Quality Standards

Specify quality criteria:

```markdown
## Quality Standards

### Completeness Checklist

- [ ] {Requirement 1}
- [ ] {Requirement 2}
- [ ] {Requirement 3}

### Quality Metrics

| Metric     | Target   | Measurement Method |
| ---------- | -------- | ------------------ |
| {Metric 1} | {Target} | {How to measure}   |
| {Metric 2} | {Target} | {How to measure}   |
```

#### Step 9: Add Examples

Provide concrete examples:

```markdown
## Examples

### Example 1: {Scenario Name}

**Context:**
{Describe the scenario}

**Application:**
{Show how to apply the skill}

**Result:**
{Show the expected outcome}

### Anti-Example: {What NOT to Do}

**Wrong Approach:**
{Show the incorrect way}

**Why It's Wrong:**
{Explain the problems}

**Correct Approach:**
{Show the right way}
```

#### Step 10: Document Integration

Explain how this skill integrates with others:

```markdown
## Integration with Other Skills

### Prerequisites

Before using this skill, you should be familiar with:

- `{prerequisite-skill-1}` — {Why it's needed}
- `{prerequisite-skill-2}` — {Why it's needed}

### Complementary Skills

This skill works well with:

- `{complementary-skill-1}` — {How they work together}
- `{complementary-skill-2}` — {How they work together}
```

#### Step 11: Validate and Format

```bash
prettier --write .kiro/skills/domain-name/references/new-skill.md
```

### Sub-Skill Checklist

Before finalizing a sub-skill:

- [ ] Header metadata is complete
- [ ] Overview explains purpose and scope
- [ ] Scope clearly defines boundaries
- [ ] Core concepts are explained
- [ ] Methodology is step-by-step
- [ ] Templates are provided
- [ ] Quality standards are defined
- [ ] Examples are concrete and relevant
- [ ] Integration with other skills is documented
- [ ] File is formatted with Prettier
- [ ] No placeholder text remains

---

## Complete Workflow

### Creating a New Skill Domain

**Scenario:** You need to create a new skill domain for "API Design"

**Steps:**

```bash
# 1. Create directory structure
mkdir -p .kiro/skills/api-design/references

# 2. Create parent skill
cp .kiro/templates/skill/skill_template.md .kiro/skills/api-design/SKILL.md

# 3. Fill in parent skill
# - name: api-design
# - description: API design patterns, REST, GraphQL, versioning
# - Domain coverage: REST API design, GraphQL schema design, API versioning
# - Sub-skills: rest-api-design.md, graphql-schema-design.md, api-versioning.md

# 4. Create sub-skills
cp .kiro/templates/skill/sub_skill_template.md .kiro/skills/api-design/references/rest-api-design.md
cp .kiro/templates/skill/sub_skill_template.md .kiro/skills/api-design/references/graphql-schema-design.md
cp .kiro/templates/skill/sub_skill_template.md .kiro/skills/api-design/references/api-versioning.md

# 5. Fill in each sub-skill
# - Overview, scope, concepts, methodology, templates, quality standards, examples

# 6. Format all files
prettier --write .kiro/skills/api-design/**/*.md

# 7. Update skills README
# Add api-design to .kiro/skills/README.md

# 8. Link to agents
# Add api-design skills to relevant agent profiles
```

**Time Estimate:** 4-6 hours for complete domain with 3 sub-skills

---

## Examples

### Example 1: Simple Sub-Skill

**Scenario:** Document how to write commit messages

**File:** `.kiro/skills/engineering/references/commit-message-standards.md`

**Key Sections:**

```markdown
# Commit Message Standards

**Domain:** `engineering`

## Overview

This skill defines the standard format for git commit messages in this workspace.

## Methodology

### Step 1: Write Subject Line

Format: `<type>: <description>`

**Types:**

- feat — New feature
- fix — Bug fix
- docs — Documentation
- refactor — Code refactoring

### Step 2: Write Body

- Use bullet points
- Describe what changed and why
- Keep lines under 72 characters

## Templates and Formats

\`\`\`
<type>: <short description>

- Detailed change 1
- Detailed change 2
- Detailed change 3
  \`\`\`

## Quality Standards

- [ ] Subject line ≤72 characters
- [ ] Body uses bullet points
- [ ] Each bullet describes one discrete change
```

### Example 2: Complex Sub-Skill

**Scenario:** Document PRD authorship methodology

**File:** `.kiro/skills/product-management/references/prd-authorship.md`

**Key Sections:**

```markdown
# PRD Authorship

**Domain:** `product-management`

## Overview

Comprehensive guide to writing Product Requirements Documents for mobile features.

## Core Concepts

### Jobs-To-Be-Done Framework

### Outcome-Focused Requirements

### Measurable Success Criteria

## Methodology

### Step 1: Problem Framing

### Step 2: User Story Development

### Step 3: Requirements Specification

### Step 4: Success Metrics Definition

### Step 5: Handoff Preparation

## Templates and Formats

### PRD Template

\`\`\`markdown

# {Feature Name} PRD

## Executive Summary

## Problem Statement

## Goals and Success Metrics

## User Stories

## Functional Requirements

## Non-Functional Requirements

## Out of Scope

## Dependencies

## Timeline

\`\`\`

## Quality Standards

### Completeness Checklist

- [ ] All required sections present
- [ ] User stories follow format
- [ ] Success metrics are quantifiable
- [ ] Dependencies are identified

### Quality Metrics

| Metric        | Target | Measurement        |
| ------------- | ------ | ------------------ |
| Clarity score | 4.5/5  | Stakeholder survey |
| Completeness  | 100%   | Section checklist  |

## Examples

### Example 1: Good PRD

### Example 2: Bad PRD (Anti-Example)
```

---

## Best Practices

### 1. Skill Naming

**Good:**

- `prd-authorship.md` — Clear, specific
- `kotlin-advanced.md` — Technology + level
- `mobile-product-strategy.md` — Platform + domain

**Bad:**

- `product.md` — Too vague
- `how-to-write-prds.md` — Use noun phrases
- `PRD_Authorship.md` — Use kebab-case

### 2. Scope Definition

**Do:**

- Be specific about what's covered
- Explicitly state what's NOT covered
- Reference related skills for out-of-scope items

**Don't:**

- Make skills too broad (split into multiple sub-skills)
- Overlap significantly with other skills
- Leave scope ambiguous

### 3. Methodology Structure

**Do:**

- Use numbered steps
- Provide inputs, outputs, and quality criteria for each step
- Include decision points and branching logic

**Don't:**

- Write narrative prose (use structured steps)
- Skip quality criteria
- Assume prior knowledge (link to prerequisites)

### 4. Template Provision

**Do:**

- Provide complete templates with all sections
- Mark required vs. optional sections
- Include inline guidance in templates

**Don't:**

- Provide partial templates
- Use ambiguous section names
- Forget to specify format (Markdown, JSON, etc.)

### 5. Example Quality

**Do:**

- Use realistic scenarios
- Show both good and bad examples
- Explain why examples are good or bad

**Don't:**

- Use trivial examples
- Only show good examples
- Leave examples unexplained

### 6. Integration Documentation

**Do:**

- List prerequisite skills
- Identify complementary skills
- Specify downstream skills

**Don't:**

- Assume skills are used in isolation
- Forget to document dependencies
- Ignore pipeline integration

---

## Troubleshooting

### Issue: Skill Too Broad

**Symptoms:**

- Skill covers multiple distinct capabilities
- Methodology has 10+ steps
- Multiple unrelated templates

**Solution:**

- Split into multiple sub-skills
- Create a parent skill to route between them
- Each sub-skill should cover one capability

### Issue: Skill Too Narrow

**Symptoms:**

- Skill is only 2-3 steps
- No templates needed
- Could be a checklist

**Solution:**

- Combine with related sub-skill
- Convert to a section in a larger skill
- Consider if it should be a steering file instead

### Issue: Unclear Methodology

**Symptoms:**

- Steps are ambiguous
- No clear inputs/outputs
- Quality criteria missing

**Solution:**

- Add more detail to each step
- Specify inputs and outputs explicitly
- Define measurable quality criteria
- Add examples for each step

### Issue: Missing Integration

**Symptoms:**

- Skill seems isolated
- No prerequisites listed
- No related skills mentioned

**Solution:**

- Identify prerequisite knowledge
- List complementary skills
- Document pipeline integration
- Reference related domains

### Issue: Poor Examples

**Symptoms:**

- Examples are trivial
- No anti-examples
- Examples don't match methodology

**Solution:**

- Use realistic scenarios
- Add anti-examples showing common mistakes
- Ensure examples follow the methodology
- Explain why examples are good/bad

---

## Quality Checklist

### Parent Skill Quality

- [ ] YAML frontmatter complete
- [ ] Domain coverage clear
- [ ] All sub-skills listed
- [ ] Related domains identified
- [ ] Activation instructions provided
- [ ] No placeholder text
- [ ] Formatted with Prettier

### Sub-Skill Quality

- [ ] Header metadata complete
- [ ] Overview explains purpose
- [ ] Scope clearly defined
- [ ] Core concepts explained
- [ ] Methodology is step-by-step
- [ ] Templates provided
- [ ] Quality standards defined
- [ ] Examples are concrete
- [ ] Integration documented
- [ ] No placeholder text
- [ ] Formatted with Prettier

---

## Related Documentation

- **Skill Templates** — `.kiro/templates/skill/`
- **Existing Skills** — `.kiro/skills/`
- **Skills README** — `.kiro/skills/README.md`
- **Agent Templates** — `.kiro/templates/agent/`
- **AGENTS.md** — Workspace conventions

---

**Guide Version:** 1.0.0  
**Last Updated:** 2026-05-06  
**Maintained By:** Workspace governance
