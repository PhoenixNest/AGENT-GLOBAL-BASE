# Organizational Agents Power

**Version:** 1.0.0  
**Status:** Active  
**Authority:** AGENTS.md § Part I — Workspace Identity & Agent Model

---

## Overview

The **Organizational Agents Power** provides comprehensive support for activating and managing Type A organizational agents (personas) across the Company, Studio, and CC-00 Lab systems.

This Power packages:

- **Agent Profiles**: Access to all 118 organizational agents
- **Activation Protocol**: Step-by-step agent instantiation process
- **Skill Management**: Bidirectional agent-skill mapping
- **Steering Files**: Agent-specific guidance and context

---

## What This Power Provides

### 1. Understanding Agent Types

**Type A — Organizational Agents (Personas)**

Named personas that exist as documents with defined roles, authorities, and skills. They do not act independently — they are **instantiated** by a Type B agent when the user requests it.

**Type B — AI Executor Agents (LLM Instances)**

The actual LLM instances (like you) that read profiles and execute tasks. Type B agents instantiate Type A agents on user request.

### 2. Agent Inventory

| System                       | Count | Status      | Location                                    |
| ---------------------------- | ----- | ----------- | ------------------------------------------- |
| **Company C-Suite**          | 7     | ✅ Complete | `.kiro/agents/company-*-chief-*`            |
| **Company VPs**              | 7     | ✅ Complete | `.kiro/agents/company-*-vp-*`               |
| **Company Team Supervisors** | 10    | ✅ Complete | `.kiro/agents/company-*-lead-*`             |
| **Company Senior ICs**       | 22    | ✅ Complete | `.kiro/agents/company-*-senior-*`           |
| **Company Mid/Junior ICs**   | 30    | ✅ Complete | `.kiro/agents/company-*-engineer-*`         |
| **Studio Leadership**        | 3     | ✅ Complete | `.kiro/agents/studio-*-director-*`          |
| **Studio Division Leads**    | 7     | ✅ Complete | `.kiro/agents/studio-*-lead-*`              |
| **Studio Crew**              | 29    | ✅ Complete | `.kiro/agents/studio-*`                     |
| **CC-00 Director**           | 1     | ✅ Complete | `.kiro/agents/core-component-00-director-*` |
| **Total**                    | 116   | ✅ 100%     | —                                           |

### 3. Agent Activation Protocol

When the user requests output from a specific organizational agent:

**Step 1: Read the Profile**

```typescript
readFile({
  path: ".kiro/agents/company-research-develop-chief-technology-officer-kenji-nakamura.md",
  explanation: "Reading CTO profile to understand authority and skills",
});
```

**Step 2: Invoke the Agent**

```typescript
invokeSubAgent({
  name: "company-research-develop-chief-technology-officer-kenji-nakamura",
  prompt: "Produce a technical specification for the dark mode feature",
  explanation: "Delegating SPEC authorship to CTO agent",
  contextFiles: ["company/pipeline/mobile-development/pipeline.md"],
});
```

**Step 3: Verify Output**

- Ensure output is within agent's documented authority
- Verify artifact conforms to pipeline stage specification
- Check that agent voice and perspective are maintained

---

## Agent Naming Convention

All agents follow a consistent naming pattern:

```
<system>-<department>-<role>-<name>
```

**Examples:**

- `company-research-develop-chief-technology-officer-kenji-nakamura`
- `studio-casual-games-studio-director-marcus-vogel`
- `core-component-00-director-elias-vance`

**System Values:**

- `company` — Company system agents
- `studio-casual-games` — Casual Games Studio agents
- `core-component-00` — CC-00 Lab agents

**Department Values:**

- `research-develop` — R&D department
- `product-management` — Product Management
- `brand-design` — Brand Design
- `cyberspace-security` — Cyberspace Security
- `localization` — Localization
- `human-resources` — Human Resources

---

## Agent Authority Hierarchy

```
User  ←  Absolute apex. Final authority on all decisions.
  │
  ├── Company C-suite  (CPO · CDO · CTO · CIO · CSO · CHRO · CTO-L)
  │     └── Company VPs  →  Team Supervisors  →  Teammates
  │
  ├── Studio Director  (Dr. Marcus Vogel)
  │     └── Studio Division Leads  →  Crew
  │
  └── CC-00 Lab Director  (Dr. Elias Vance)
        └── CC-00 Research Programmes
```

**Key Principles:**

- **User holds final authority** over every agent and decision
- **C-suite agents** own pipeline stage outputs
- **VP agents** own platform-specific PRDs and reviews
- **Team Supervisors** own sub-department execution
- **Teammates** are individual contributors

---

## Agent Skills

Each agent has a set of skills that define their executable capabilities:

### Skill Structure

```
.kiro/skills/
├── domain-name/
│   ├── SKILL.md              # Parent skill (router)
│   └── references/           # Sub-skills
│       ├── sub-skill-1.md
│       ├── sub-skill-2.md
│       └── sub-skill-3.md
```

### Skill Domains

| Domain                       | Description                                       | Agent Count |
| ---------------------------- | ------------------------------------------------- | ----------- |
| `product-management`         | Product strategy, PRD authorship, stage gates     | 10          |
| `product-design`             | Mobile design systems, UI/UX, design handoff      | 5           |
| `engineering`                | SPEC development, architecture, project mgmt      | 40          |
| `technology-strategy`        | Tech evaluation, architecture strategy, ADRs      | 5           |
| `cyberspace-security`        | Security architecture, hardening, risk assessment | 8           |
| `localization`               | Translation, i18n engineering, linguist ops       | 4           |
| `recruitment`                | Candidate vetting, role-specific recruitment      | 3           |
| `quality-assurance`          | Testing, defect classification, QA automation     | 8           |
| `data-analytics`             | Metrics, instrumentation, A/B testing             | 3           |
| `game-development`           | Studio leadership, live ops, game pipelines       | 10          |
| `visual-arts-and-animation`  | Art direction, animation, visual design           | 9           |
| `audio-engineering`          | Sound design, music, audio implementation         | 3           |
| `android-engineering`        | Android/Kotlin development                        | 8           |
| `ios-engineering`            | iOS/Swift development                             | 8           |
| `cross-platform-engineering` | KMP, Flutter, shared code                         | 4           |
| `frontend-engineering`       | Web frontend, React, Vue                          | 6           |
| `backend-engineering`        | APIs, databases, server architecture              | 8           |
| `llm-engineering`            | LLM system design, context, harness, RAG, MAE     | 1           |

---

## Common Use Cases

### 1. Pipeline Stage Execution

**Scenario**: User needs a PRD for a mobile feature

```typescript
invokeSubAgent({
  name: "company-product-management-chief-product-officer-marcus-tran-yoshida",
  prompt: "Produce a PRD for dark mode feature in the mobile app",
  explanation: "Delegating Stage 1 PRD authorship to CPO",
  contextFiles: [
    "company/pipeline/mobile-development/pipeline.md",
    "company/pipeline/mobile-development/templates/prd-template.md",
  ],
});
```

### 2. Architecture Review

**Scenario**: User needs architecture review for Stage 6

```typescript
invokeSubAgent({
  name: "company-research-develop-chief-technology-officer-kenji-nakamura",
  prompt:
    "Conduct Stage 6 architecture and conformance review for dark mode implementation",
  explanation: "Delegating Stage 6 review to CTO",
  contextFiles: [
    "company/pipeline/mobile-development/pipeline.md",
    "projects/dark-mode/spec.md",
    "projects/dark-mode/implementation/",
  ],
});
```

### 3. Security Assessment

**Scenario**: User needs SRD for Stage 1

```typescript
invokeSubAgent({
  name: "company-cyberspace-security-chief-security-officer-sarah-chen",
  prompt:
    "Produce an SRD for dark mode feature addressing security requirements",
  explanation: "Delegating Stage 1 SRD authorship to CSO",
  contextFiles: [
    "company/pipeline/mobile-development/pipeline.md",
    "company/pipeline/mobile-development/templates/srd-template.md",
    "projects/dark-mode/prd.md",
  ],
});
```

### 4. Game Design

**Scenario**: User needs GDD for a new game

```typescript
invokeSubAgent({
  name: "studio-casual-games-creative-director-sakura-ishimori",
  prompt: "Produce a GDD for a match-3 puzzle game with RPG progression",
  explanation: "Delegating Stage 1 GDD authorship to Creative Director",
  contextFiles: [
    "studio/casual-games/pipeline/casual-games-pipeline.md",
    "studio/casual-games/library/overview/casual-games-studio.md",
  ],
});
```

### 5. LLM System Design

**Scenario**: User needs CC-00 engineering guidance

```typescript
invokeSubAgent({
  name: "core-component-00-director-elias-vance",
  prompt: "Design a multi-agent RAG system for workspace knowledge retrieval",
  explanation: "Delegating LLM system design to CC-00 Director",
  contextFiles: [
    "core-component-00/README.md",
    "core-component-00/multi-agent-engineering/fundamentals/swarm-orchestration.md",
    "core-component-00/retrieval-augmented-generation/fundamentals/rag-architecture.md",
  ],
});
```

---

## Agent Management

### Listing Available Agents

```bash
ls .kiro/agents/
```

### Searching for Agents by Role

```bash
ls .kiro/agents/ | grep "chief-"        # C-suite agents
ls .kiro/agents/ | grep "vp-"           # VP agents
ls .kiro/agents/ | grep "lead-"         # Team Supervisors
ls .kiro/agents/ | grep "senior-"       # Senior ICs
ls .kiro/agents/ | grep "engineer-"     # Engineers
```

### Reading Agent Profiles

```typescript
readFile({
  path: ".kiro/agents/<agent-name>.md",
  explanation: "Reading agent profile to understand capabilities",
});
```

---

## Related Powers

- **Company Pipeline**: Company's 13-stage development pipeline
- **Casual Games Pipeline**: Studio's 11-stage game development pipeline
- **CC-00 Engineering**: LLM engineering patterns and implementations
- **MCP Development**: MCP server creation for agent tooling

---

## References

- **Agent Profiles**: `.kiro/agents/`
- **Skills**: `.kiro/skills/`
- **Company Personnel**: `company/library/overview/personnel.md`
- **Studio Crew**: `studio/casual-games/team/README.md`
- **CC-00 Director**: `core-component-00/director/agent/profile.md`
- **AGENTS.md**: § Part I — Workspace Identity & Agent Model
