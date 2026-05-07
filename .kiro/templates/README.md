# Kiro Templates

**Status:** Active  
**Last Updated:** 2026-05-06  
**Authority:** ECOSYSTEM_SPEC.md

---

## Overview

This directory contains standardized templates for all Kiro toolset components. These templates ensure consistency across the workspace and provide clear guidance for creating new agents, skills, powers, steering files, and hooks.

## Directory Structure

```
.kiro/templates/
├── agent/
│   ├── agent_template.md
│   └── agent_template_guide.md
├── skill/
│   ├── skill_template.md          # Parent skill (router)
│   ├── sub_skill_template.md      # Sub-skill (detailed)
│   └── skill_template_guide.md    # Comprehensive usage guide
├── power/
│   ├── power_template.md
│   └── power_template_guide.md    # Comprehensive usage guide
├── steering/
│   ├── steering_template.md
│   └── steering_template_guide.md # Comprehensive usage guide
├── hook/
│   ├── hook_template.json
│   └── hook_template_guide.md
├── README.md                       # This file
└── TEMPLATE_SUMMARY.md             # Complete summary
```

## Template Categories

### 1. Agent Templates

**Location:** `.kiro/templates/agent/`

**Purpose:** Create consistent agent profile documents for organizational agents (Type A) and custom agents (Type B).

**Files:**

- `agent_template.md` — Complete agent profile template with all sections
- `agent_template_guide.md` — Comprehensive usage guide with examples

**When to Use:**

- Creating new organizational agents (C-suite, VPs, supervisors, teammates)
- Creating custom utility agents (orchestrators, executors, assistants)
- Migrating existing agents to unified format

**Key Features:**

- Structured YAML frontmatter for programmatic parsing
- Consistent section ordering across all agent types
- Standardized skills table with paths to `.kiro/skills/`
- Invocation instructions for proper agent delegation
- Traceability footer linking back to source profiles

**Quick Start:**

```bash
# Copy template
cp .kiro/templates/agent/agent_template.md .kiro/agents/new-agent.md

# Read the guide
cat .kiro/templates/agent/agent_template_guide.md

# Fill in the template
# ...
```

### 2. Skill Templates

**Location:** `.kiro/templates/skill/`

**Purpose:** Create domain-based skill hierarchies with parent routers and detailed sub-skills.

**Files:**

- `skill_template.md` — Parent skill (router) template
- `sub_skill_template.md` — Sub-skill (detailed capability) template

**When to Use:**

- Creating new skill domains (e.g., `new-domain/`)
- Adding sub-skills to existing domains
- Documenting agent capabilities and methodologies

**Structure Pattern:**

```
.kiro/skills/
├── domain-name/
│   ├── SKILL.md              # Use skill_template.md
│   └── references/
│       ├── sub-skill-1.md    # Use sub_skill_template.md
│       ├── sub-skill-2.md    # Use sub_skill_template.md
│       └── sub-skill-3.md    # Use sub_skill_template.md
```

**Quick Start:**

```bash
# Create new domain
mkdir -p .kiro/skills/new-domain/references

# Copy parent skill template
cp .kiro/templates/skill/skill_template.md .kiro/skills/new-domain/SKILL.md

# Copy sub-skill template
cp .kiro/templates/skill/sub_skill_template.md .kiro/skills/new-domain/references/new-skill.md

# Fill in templates
# ...
```

### 3. Power Templates

**Location:** `.kiro/templates/power/`

**Purpose:** Create comprehensive power packages that bundle documentation, templates, steering files, and MCP servers.

**Files:**

- `power_template.md` — Complete power documentation template

**When to Use:**

- Creating new powers for specific domains or capabilities
- Packaging related documentation and resources
- Defining power activation and usage patterns

**Structure Pattern:**

```
.kiro/powers/
├── power-name/
│   ├── POWER.md              # Use power_template.md
│   ├── templates/            # Optional: templates
│   ├── steering/             # Optional: steering files
│   └── mcp-servers/          # Optional: MCP servers
```

**Quick Start:**

```bash
# Create new power
mkdir -p .kiro/powers/new-power

# Copy template
cp .kiro/templates/power/power_template.md .kiro/powers/new-power/POWER.md

# Fill in template
# ...
```

### 4. Steering Templates

**Location:** `.kiro/templates/steering/`

**Purpose:** Create steering files that provide contextual guidance and rules for specific scenarios.

**Files:**

- `steering_template.md` — Complete steering file template

**When to Use:**

- Creating auto-included guidance (always active)
- Creating file-match guidance (activates for specific files)
- Creating manual guidance (user-activated)

**Inclusion Types:**

| Type        | Activation                             | Use Case                          |
| ----------- | -------------------------------------- | --------------------------------- |
| `auto`      | Always included in all sessions        | Core conventions, mandatory rules |
| `fileMatch` | Activates when matching files are read | Context-specific guidance         |
| `manual`    | User must explicitly include via `#`   | Optional reference material       |

**Quick Start:**

```bash
# Copy template
cp .kiro/templates/steering/steering_template.md .kiro/steering/new-guidance.md

# Fill in template
# Set inclusion type in frontmatter
# ...
```

### 5. Hook Templates

**Location:** `.kiro/templates/hook/`

**Purpose:** Create hooks that automate agent actions based on IDE events.

**Files:**

- `hook_template.json` — JSON hook schema template
- `hook_template_guide.md` — Comprehensive usage guide with examples

**When to Use:**

- Automating code quality checks (linting, formatting)
- Enforcing pipeline stage gates
- Triggering security reviews
- Reminding agents of conventions

**Event Types:**

| Event Type          | Trigger                         |
| ------------------- | ------------------------------- |
| `fileEdited`        | When a user saves a file        |
| `fileCreated`       | When a user creates a file      |
| `fileDeleted`       | When a user deletes a file      |
| `promptSubmit`      | When a message is sent to agent |
| `agentStop`         | When agent execution completes  |
| `preToolUse`        | Before a tool is executed       |
| `postToolUse`       | After a tool is executed        |
| `preTaskExecution`  | Before a spec task starts       |
| `postTaskExecution` | After a spec task completes     |
| `userTriggered`     | Manual trigger by user          |

**Quick Start:**

```bash
# Copy template
cp .kiro/templates/hook/hook_template.json .kiro/hooks/new-hook.json

# Read the guide
cat .kiro/templates/hook/hook_template_guide.md

# Fill in template
# ...
```

## Template Usage Workflow

### General Workflow

1. **Identify Need** — Determine which template you need
2. **Copy Template** — Copy the appropriate template to the target location
3. **Read Guide** — Review the usage guide (if available)
4. **Fill Template** — Replace placeholders with actual content
5. **Validate** — Check against quality criteria
6. **Test** — Verify the component works as expected
7. **Commit** — Add to version control

### Quality Checklist

Before finalizing any template-based component:

- [ ] All required fields are filled in
- [ ] Placeholders (`{...}`) are replaced with actual values
- [ ] Formatting is consistent (Prettier for Markdown, valid JSON for hooks)
- [ ] Paths are correct and relative to workspace root
- [ ] Examples are relevant and accurate
- [ ] Documentation is clear and complete
- [ ] Component has been tested (if applicable)
- [ ] Version and date fields are current

## Template Maintenance

### When to Update Templates

Templates should be updated when:

- New required fields are added to components
- Best practices evolve
- New sections become standard
- Formatting conventions change
- User feedback identifies gaps or confusion

### Version Control

All templates follow semantic versioning:

- **Major version** (X.0.0) — Breaking changes to structure
- **Minor version** (0.X.0) — New sections or fields added
- **Patch version** (0.0.X) — Clarifications, examples, or fixes

### Template Governance

**Maintained By:** Workspace governance  
**Review Frequency:** Quarterly or as needed  
**Change Process:**

1. Identify need for change
2. Propose update with rationale
3. Review impact on existing components
4. Update template and guide
5. Update version and changelog
6. Communicate changes to users

## Common Patterns

### Pattern 1: Creating a New Agent

```bash
# 1. Copy template
cp .kiro/templates/agent/agent_template.md .kiro/agents/company-dept-role-name.md

# 2. Fill in YAML frontmatter
# name: company-dept-role-name
# description: One-line description
# system: company
# department: dept-name
# tier: c-suite|supervisor|teammates
# ...

# 3. Fill in all sections
# - Title
# - Background
# - Core Strengths
# - Honest Gaps
# - Assigned Role
# - Operating Mode
# - Agent Skills
# - Pipeline Stages
# - OKRs / Metrics
# - Invocation Instructions

# 4. Validate
prettier --write .kiro/agents/company-dept-role-name.md

# 5. Test invocation
# Try invoking the agent to ensure it works
```

### Pattern 2: Creating a New Skill Domain

```bash
# 1. Create domain directory
mkdir -p .kiro/skills/new-domain/references

# 2. Copy parent skill template
cp .kiro/templates/skill/skill_template.md .kiro/skills/new-domain/SKILL.md

# 3. Fill in parent skill
# - Domain coverage
# - Sub-skill list
# - Related domains

# 4. Create sub-skills
cp .kiro/templates/skill/sub_skill_template.md .kiro/skills/new-domain/references/skill-1.md
cp .kiro/templates/skill/sub_skill_template.md .kiro/skills/new-domain/references/skill-2.md

# 5. Fill in sub-skills
# - Overview
# - Methodology
# - Templates
# - Quality standards
# - Examples

# 6. Update skills README
# Add new domain to .kiro/skills/README.md
```

### Pattern 3: Creating a New Hook

```bash
# 1. Copy template
cp .kiro/templates/hook/hook_template.json .kiro/hooks/new-hook.json

# 2. Fill in hook
# {
#   "name": "Hook Name",
#   "version": "1.0.0",
#   "description": "What it does",
#   "when": {
#     "type": "fileEdited",
#     "patterns": ["*.ts"]
#   },
#   "then": {
#     "type": "runCommand",
#     "command": "npm run lint"
#   }
# }

# 3. Validate JSON
# Ensure valid JSON syntax

# 4. Test hook
# Save a matching file and verify hook triggers
```

## Examples by Use Case

### Use Case 1: Onboarding New Team Member

**Scenario:** New teammate needs to create their agent profile

**Steps:**

1. Copy agent template
2. Read agent template guide
3. Fill in background, strengths, gaps
4. List skills from existing skill domains
5. Specify pipeline stages
6. Add OKRs and metrics
7. Validate and commit

**Time:** ~30 minutes

### Use Case 2: Adding New Capability

**Scenario:** Need to document a new skill for agents

**Steps:**

1. Identify appropriate skill domain
2. Copy sub-skill template
3. Document methodology and standards
4. Provide examples and anti-examples
5. Update parent skill router
6. Link to agent profiles
7. Validate and commit

**Time:** ~1-2 hours

### Use Case 3: Enforcing New Convention

**Scenario:** Need to enforce a new coding standard

**Steps:**

1. Copy hook template
2. Define event trigger (e.g., fileEdited)
3. Specify file patterns
4. Choose action (askAgent or runCommand)
5. Test hook behavior
6. Document in steering file
7. Commit hook and steering

**Time:** ~15-30 minutes

## Troubleshooting

### Issue: Template Placeholders Not Replaced

**Symptoms:**

- `{placeholder}` text appears in final document
- Validation fails due to invalid values

**Solution:**

- Search for all `{` and `}` characters
- Replace each placeholder with actual value
- Use find-and-replace for common placeholders

### Issue: Template Structure Doesn't Fit

**Symptoms:**

- Some sections don't apply to your use case
- Need additional sections not in template

**Solution:**

- Mark optional sections as such or remove them
- Add custom sections as needed
- Document deviations in comments
- Consider proposing template update

### Issue: Validation Errors

**Symptoms:**

- Prettier fails
- JSON is invalid
- Paths don't resolve

**Solution:**

- Run Prettier: `prettier --write <file>`
- Validate JSON: Use JSON validator
- Check paths are relative to workspace root
- Verify all required fields are present

## Related Documentation

- **AGENTS.md** — Workspace agent orientation guide
- **ECOSYSTEM_SPEC.md** — Full ecosystem specification
- **.kiro/agents/** — Agent profiles
- **.kiro/skills/** — Skill domains
- **.kiro/powers/** — Power packages
- **.kiro/steering/** — Steering files
- **.kiro/hooks/** — Hook definitions

## Support

For questions or issues with templates:

1. Review the relevant template guide
2. Check existing examples in the workspace
3. Consult AGENTS.md for conventions
4. Ask the user for clarification

---

**Templates Version:** 1.0.0  
**Last Updated:** 2026-05-06  
**Maintained By:** Workspace governance  
**Review Frequency:** Quarterly

_These templates follow Kiro specifications and are maintained according to ECOSYSTEM_SPEC.md governance._
