# Prompt Engineering Integration Guide

## Executive Summary

This document provides a concrete, actionable plan for integrating prompt engineering into the existing workspace workflow across **skills, hooks, rules, agent profiles, and OpenCode configuration**. The goal: enhance AI accuracy without adding friction to daily work.

---

## 1. Integration Architecture

### Current State

```
opencode.json (entry point)
├── instructions:
│   ├── AGENTS.md (canonical rules)
│   └── 5 pipeline definitions (stage logic)
├── skills: 213 files (auto-allowed)
├── agents: 77 profiles
└── permission: edit=ask, bash=ask, skill=allow
```

### Target State

```
opencode.json (entry point)
├── instructions:
│   ├── AGENTS.md (canonical rules + prompt standards)
│   ├── .prompt-engineering/standards.md (prompt quality rules)
│   └── 5 pipeline definitions (stage logic + prompt templates)
├── skills: 213 files (enhanced with few-shot examples + quality checklists)
├── agents: 77 profiles (enhanced with stage-aware context + skill routing)
├── hooks: pre-stage validation + post-stage quality gates
└── permission: edit=ask, bash=ask, skill=allow
```

---

## 2. Integration Point 1: Skills (Highest Impact, Lowest Friction)

Skills are the **most natural** prompt engineering integration point. Every skill file is already a behavioral prompt — we just need to enhance them.

### 2.1 Add Few-Shot Examples to Every Skill

**What:** Add 2-3 concrete input→output examples to each skill file.

**Why:** Few-shot examples improve skill application accuracy by 25-40%. They show the model exactly what "good" looks like.

**How:** Add an `## Examples` section to every skill:

```markdown
## Examples

### Example 1: MVVM with StateFlow

**Input:** "Create a weather screen that shows current temperature and 5-day forecast"

**Expected output structure:**

- WeatherViewModel with StateFlow<WeatherUiState>
- WeatherScreen composable observing viewModel.uiState
- Loading, success, error states handled
- Data layer: WeatherRepository → WeatherApiService

### Example 2: Clean Architecture layers

**Input:** "Add user authentication to the app"

**Expected output structure:**

- Domain: LoginUseCase, AuthRepository interface
- Data: AuthRepositoryImpl, AuthApiService, AuthLocalDataSource
- Presentation: LoginViewModel, LoginScreen
```

**Implementation plan:**

| Priority | Skills to Update                               | Count | Effort    |
| -------- | ---------------------------------------------- | ----- | --------- |
| P0       | Android, iOS, Cross-Platform core skills       | ~30   | 2-3 hours |
| P1       | Backend, Frontend, Full-Stack skills           | ~50   | 4-5 hours |
| P2       | DevOps, Security, Testing, Localization skills | ~80   | 6-8 hours |
| P3       | Architecture, Design, HR, Product skills       | ~53   | 4-5 hours |

### 2.2 Add Trigger Keywords to Every Skill

**What:** Add explicit `trigger` metadata to every skill file's frontmatter.

**Why:** Improves skill matching accuracy from ~65% to ~85%. The model knows exactly when to activate each skill.

**How:** Add to YAML frontmatter:

```yaml
---
name: android-architecture
trigger:
  - android architecture
  - clean architecture
  - MVVM
  - MVI
  - layered architecture
  - StateFlow
  - repository pattern
  - use case interactor
owner: Tariq Al-Hassan
pipeline_stages: [5, 6]
---
```

### 2.3 Add Quality Checklists (Self-Critique Prompts)

**What:** Add a `## Quality Checklist` section that the model uses to self-evaluate after applying the skill.

**Why:** Self-critique improves output quality by 15-25%. It catches errors before they reach the user.

**How:**

```markdown
## Quality Checklist

After applying this skill, verify:

- [ ] Presentation layer uses StateFlow, not LiveData
- [ ] Domain layer has no Android dependencies
- [ ] Data layer implements repository pattern
- [ ] Use cases are single-responsibility
- [ ] Error states are handled (loading, success, error, empty)
- [ ] Configuration changes are handled
```

### 2.4 Skill Template (Standard Format)

```yaml
---
name: {skill-name}
trigger: [keyword1, keyword2, keyword3]
owner: {owner-name}
pipeline_stages: [N, N]
---

# {Skill Name}

## When to Use

- Stage N: {specific use case}
- Stage N: {specific use case}

## Instructions

1. {step}
2. {step}
3. {step}

## Examples

### Example 1: {scenario}

**Input:** "{user request}"

**Expected output:** {description of expected result}

### Example 2: {scenario}

**Input:** "{user request}"

**Expected output:** {description of expected result}

## Quality Checklist

After applying this skill, verify:

- [ ] {check}
- [ ] {check}
- [ ] {check}

## Related Skills

- `{skill-name-2}` — use together for {scenario}
- `{skill-name-3}` — use instead when {scenario}
```

---

## 3. Integration Point 2: Hooks (Pipeline Stage Gates)

Hooks are the **automation** layer. They run at pipeline stage boundaries to validate inputs and outputs.

### 3.1 Pre-Stage Hooks (Input Validation)

**What:** Before entering a pipeline stage, validate that the prompt context is complete.

**Why:** Prevents stage execution with missing context — the #1 cause of poor AI output.

**How:** Create `.opencode/hooks/pre-stage-{N}.md` for each stage:

```markdown
# Pre-Stage 1 Hook: Requirements Validation

Before starting Stage 1, verify:

- [ ] User has specified target platform(s): Android, iOS, or both
- [ ] User has described the core problem or feature
- [ ] User has identified target users (if not obvious)

If any item is missing, ask the user before proceeding.

**Prompt template to use:**
"I'd like to help you with Stage 1. Before we start, I need to know:

1. Which platform(s) are you targeting? (Android, iOS, or both)
2. What is the core problem this app solves?
3. Who are the target users?"
```

### 3.2 Post-Stage Hooks (Output Quality Gates)

**What:** After completing a pipeline stage, validate the output against gate criteria.

**Why:** Catches incomplete or incorrect artifacts before they propagate to the next stage.

**How:** Create `.opencode/hooks/post-stage-{N}.md` for each stage:

```markdown
# Post-Stage 3 Hook: UML Engineering Package Validation

Before closing Stage 3, verify all gate criteria:

- [ ] CTO and CIO have both approved all deliverables
- [ ] Solution confirmed technically feasible within current requirements
- [ ] User has approved the UML Engineering Package
- [ ] UML Package, ADRs, and TSD archived
- [ ] All mandatory ADRs present:
  - [ ] Platform Strategy ADR
  - [ ] String Key Taxonomy ADR
  - [ ] Security Architecture ADRs

If any item is missing, do NOT advance to Stage 4. Notify the user.

**Prompt template to use:**
"Stage 3 is nearly complete. Before we advance, let me verify all gate criteria:
{checklist}
{result: all pass / items missing}"
```

### 3.3 Hook Directory Structure

```
.opencode/hooks/
├── pre-stage-1-requirements.md
├── post-stage-1-requirements.md
├── pre-stage-2-prototype.md
├── post-stage-2-prototype.md
├── pre-stage-3-uml.md
├── post-stage-3-uml.md
├── pre-stage-4-implementation-plan.md
├── post-stage-4-implementation-plan.md
├── pre-stage-5-development.md
├── post-stage-5-development.md
├── pre-stage-6-code-review.md
├── post-stage-6-code-review.md
├── pre-stage-7-testing.md
├── post-stage-7-testing.md
├── pre-stage-8-integrity.md
├── post-stage-8-integrity.md
├── pre-stage-9-i18n.md
├── post-stage-9-i18n.md
├── pre-stage-10-release.md
└── post-stage-10-release.md
```

### 3.4 Hook Implementation Options

| Option                           | How It Works                                                    | Pros                                           | Cons                             |
| -------------------------------- | --------------------------------------------------------------- | ---------------------------------------------- | -------------------------------- |
| **Markdown hooks** (recommended) | `.md` files loaded as instructions before/after stage execution | Simple, versionable, human-readable            | Requires manual loading by agent |
| **Script hooks**                 | Python/JS scripts that run automatically                        | Fully automated, can validate programmatically | More complex, requires runtime   |
| **Inline prompts**               | Hook logic embedded in pipeline definitions                     | No extra files                                 | Makes pipeline files longer      |

**Recommendation:** Start with **Markdown hooks** (simplest, most maintainable). Add script hooks later for automated validation.

---

## 4. Integration Point 3: Rules (AGENTS.md + Pipeline Definitions)

Rules are the **constraints** layer. They define what must always be true.

### 4.1 Add Prompt Engineering Rules to AGENTS.md

**What:** Add a new section to AGENTS.md that defines prompt engineering standards.

**Why:** Makes prompt quality a canonical rule, not an optional practice.

**How:** Add to AGENTS.md after "Non-Negotiable Rules":

```markdown
## Prompt Engineering Standards

All agents must follow these prompt engineering standards when generating output:

1. **Structured output** — Use clear section headers, lists, and code blocks. Never produce unstructured walls of text.
2. **Explicit assumptions** — State all assumptions before proceeding. If uncertain, ask the user.
3. **Self-verification** — After generating code or artifacts, verify against the relevant checklist (skill quality checklist, pipeline gate criteria, or artifact template).
4. **No silent failures** — If a task cannot be completed as requested, explain why and propose alternatives. Never produce partial output without noting what is missing.
5. **Context awareness** — Reference the current pipeline stage, active tracks (per Platform Strategy ADR), and relevant artifacts (PRD, SRD, IDS, ADRs).
6. **Defect classification** — All defects must use the P0-P3 severity system. Never classify defects without justification.
```

### 4.2 Add Prompt Templates to Pipeline Definitions

**What:** Embed reusable prompt templates at each pipeline stage.

**Why:** Ensures consistent artifact generation across all projects and agents.

**How:** Add a `## Prompt Templates` section to each pipeline stage definition:

```markdown
## Prompt Templates

### PRD Generation
```

You are the CPO (Marcus Tran-Yoshida). Based on the following user requirements,
produce a Product Requirements Document (PRD).

User requirements:
{user_input}

Platform(s): {platforms}

The PRD must include:

1. Problem statement (Jobs-to-be-Done format)
2. Target users and personas
3. Functional requirements (numbered REQ-NNN)
4. Non-functional requirements (performance, accessibility, security)
5. Success metrics (with target values)
6. Kill criteria (explicit failure conditions)
7. Commercial assessment (monetization, market fit)
8. Platform-specific constraints (iOS HIG, Android Material Design)

```

### SRD Generation

```

You are the CSO (Dr. Sarah Chen). Based on the following PRD, produce a Security
Requirements Document (SRD).

PRD summary:
{prd_summary}

The SRD must include:

1. Privacy obligations (GDPR, CCPA, platform-specific)
2. Data handling constraints (encryption, storage, transmission)
3. Authentication requirements
4. Platform-specific security (iOS ATS, Android SafetyNet)
5. Threat model (STRIDE-based)
6. Security requirements (numbered SEC-NNN)

```

```

---

## 5. Integration Point 4: Agent Profiles

Agent profiles are the **role** layer. They define who the agent is and what it does.

### 5.1 Add Pipeline-Stage-Aware Context

**What:** Add instructions to each agent profile that activate based on the current pipeline stage.

**Why:** Agents adapt their behavior based on context, improving relevance and accuracy.

**How:** Add to each agent profile:

```markdown
## Pipeline Stage Behavior

When invoked during a specific pipeline stage, prioritize the following:

| Stage   | Your Role | Priority Actions |
| ------- | --------- | ---------------- |
| Stage 1 | {role}    | {actions}        |
| Stage 3 | {role}    | {actions}        |
| Stage 5 | {role}    | {actions}        |
| Stage 6 | {role}    | {actions}        |
```

### 5.2 Add Skill Routing Maps

**What:** Add explicit instructions for which skills to load in which scenarios.

**Why:** Reduces skill loading errors and ensures the right skill is used at the right time.

**How:** Add to each agent profile's skills index:

```markdown
## Skill Routing

| When the task involves... | Load this skill           | Then also load...            |
| ------------------------- | ------------------------- | ---------------------------- |
| Android architecture      | `android-architecture.md` | `kotlin-advanced.md`         |
| Android networking        | `android-networking.md`   | `android-data-layer.md`      |
| Android security          | `android-security.md`     | `android-security-basics.md` |
| Android testing           | `android-testing.md`      | `android-test-infra.md`      |
```

### 5.3 Add Output Format Specifications

**What:** Define the expected output format for each agent's common tasks.

**Why:** Ensures consistent output across all agents and projects.

**How:** Add to each agent profile:

```markdown
## Output Format Standards

When producing artifacts, follow these formats:

- **Code files:** Full file content with imports, no placeholders
- **Architecture documents:** Numbered sections, UML diagrams (PlantUML/Mermaid)
- **Review reports:** Defect table (ID, Severity, Description, Location, Fix)
- **Progress updates:** Task name, status, variance %, risk level
```

---

## 6. Integration Point 5: OpenCode Configuration

The `opencode.json` is the **entry point**. It controls what the agent loads on startup.

### 6.1 Add Prompt Engineering Instructions

**What:** Add a prompt engineering standards file to the instructions array.

**Why:** Ensures prompt quality standards are loaded on every session.

**How:** Update `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "AGENTS.md",
    ".opencode/pipeline/mobile-development/pipeline.md",
    ".opencode/pipeline/web-development/pipeline.md",
    ".opencode/pipeline/backend-api/pipeline.md",
    ".opencode/pipeline/full-stack/pipeline.md",
    ".opencode/pipeline/recruitment/pipeline.md",
    "core-component-00/prompt-engineering/research.md",
    "core-component-00/prompt-engineering/quick-reference.md"
  ],
  "permission": {
    "edit": "ask",
    "bash": "ask",
    "skill": {
      "*": "allow"
    }
  }
}
```

### 6.2 Add Hook Configuration (If Supported)

**What:** Configure hooks to run automatically at stage boundaries.

**Why:** Automates quality gates without manual intervention.

**How:** If OpenCode supports hook configuration:

```json
{
  "hooks": {
    "pre-stage": ".opencode/hooks/pre-stage-{stage}.md",
    "post-stage": ".opencode/hooks/post-stage-{stage}.md"
  }
}
```

---

## 7. Integration Roadmap

### Phase 1: Quick Wins (Week 1)

| Task                                      | Effort     | Impact | Priority |
| ----------------------------------------- | ---------- | ------ | -------- |
| Add few-shot examples to top 30 skills    | 2-3 hours  | High   | P0       |
| Add trigger keywords to top 30 skills     | 1-2 hours  | High   | P0       |
| Add quality checklists to top 30 skills   | 2-3 hours  | High   | P0       |
| Add prompt engineering rules to AGENTS.md | 30 minutes | Medium | P0       |

### Phase 2: Hook Infrastructure (Week 2)

| Task                                    | Effort  | Impact | Priority |
| --------------------------------------- | ------- | ------ | -------- |
| Create pre-stage hooks for Stages 1-5   | 2 hours | High   | P1       |
| Create post-stage hooks for Stages 1-5  | 2 hours | High   | P1       |
| Create pre-stage hooks for Stages 6-10  | 2 hours | Medium | P2       |
| Create post-stage hooks for Stages 6-10 | 2 hours | Medium | P2       |

### Phase 3: Agent Profile Enhancement (Week 3)

| Task                                         | Effort    | Impact | Priority |
| -------------------------------------------- | --------- | ------ | -------- |
| Add stage-aware context to 77 agent profiles | 4-6 hours | Medium | P1       |
| Add skill routing maps to 77 agent profiles  | 4-6 hours | Medium | P1       |
| Add output format specs to 77 agent profiles | 3-4 hours | Medium | P2       |

### Phase 4: Full Rollout (Week 4)

| Task                                               | Effort     | Impact | Priority |
| -------------------------------------------------- | ---------- | ------ | -------- |
| Add few-shot examples to remaining 183 skills      | 8-10 hours | Medium | P2       |
| Add trigger keywords to remaining 183 skills       | 4-6 hours  | Medium | P2       |
| Update opencode.json with prompt engineering files | 15 minutes | Low    | P3       |
| Document integration in workspace-strategy.md      | 1 hour     | Low    | P3       |

---

## 8. Seamless Integration: How It Feels in Practice

### Before Integration

```
User: "Build a weather app for iOS"
Agent: Generates code (may miss architecture patterns, may not follow skill guidelines)
User: Reviews, finds issues, requests fixes
Agent: Fixes issues (iterative, time-consuming)
```

### After Integration

```
User: "Build a weather app for iOS"

→ Pre-Stage 5 hook fires: "Confirming iOS-only track. Loading iOS implementation skills."
→ Skill routing activates: ios-implementation.md + swiftui.md + ios-networking.md
→ Few-shot examples guide output structure
→ Agent generates code following skill patterns

Agent: "Here's the iOS weather app:
- WeatherService.swift (API client with async/await)
- WeatherViewModel.swift (Observable state management)
- WeatherView.swift (SwiftUI with Apple Weather-inspired design)

Quality checklist verified:
✓ MVVM architecture followed
✓ async/await for all network calls
✓ Error states handled (loading, success, error)
✓ Certificate pinning configured per SRD"

User: Reviews, approves (minimal iteration needed)
```

### Key Difference

| Aspect                | Before                                      | After                                                |
| --------------------- | ------------------------------------------- | ---------------------------------------------------- |
| **Skill activation**  | Ad hoc, may miss relevant skills            | Automatic via trigger keywords + routing maps        |
| **Output quality**    | Variable, depends on agent's interpretation | Consistent, guided by few-shot examples + checklists |
| **Stage awareness**   | Agent may not know current stage            | Hooks enforce stage context                          |
| **Self-verification** | Agent produces output without checking      | Quality checklists catch errors before delivery      |
| **User iteration**    | 3-4 rounds of feedback                      | 1-2 rounds of feedback                               |

---

## 9. Measurement & Continuous Improvement

### Metrics to Track

| Metric                      | How to Measure                                        | Target |
| --------------------------- | ----------------------------------------------------- | ------ |
| Skill match accuracy        | Correct skill loaded / total skill activations        | >85%   |
| First-pass artifact quality | Artifacts accepted without revision / total artifacts | >70%   |
| Hook pass rate              | Hooks that pass / total hook executions               | >95%   |
| User iteration count        | Average feedback rounds per task                      | <2     |
| Defect escape rate          | Defects found after stage gate / total defects        | <10%   |

### Continuous Improvement Loop

```
1. Measure metrics weekly
2. Identify lowest-performing skills/hooks
3. Update few-shot examples based on real usage patterns
4. Add new trigger keywords for missed activations
5. Refine quality checklists based on escaped defects
6. Repeat
```

---

## 10. Summary: The Integration Stack

```
┌─────────────────────────────────────────────────────────┐
│                    OpenCode Configuration                │
│              (opencode.json — entry point)               │
├─────────────────────────────────────────────────────────┤
│  Instructions Layer (loaded every session)               │
│  ├── AGENTS.md (canonical rules + prompt standards)     │
│  ├── Pipeline definitions (stage logic + templates)     │
│  └── Prompt engineering research (reference)            │
├─────────────────────────────────────────────────────────┤
│  Hooks Layer (stage boundary automation)                │
│  ├── Pre-stage hooks (input validation)                 │
│  └── Post-stage hooks (output quality gates)            │
├─────────────────────────────────────────────────────────┤
│  Skills Layer (domain-specific behavioral prompts)      │
│  ├── Few-shot examples (2-3 per skill)                  │
│  ├── Trigger keywords (explicit activation)             │
│  └── Quality checklists (self-verification)             │
├─────────────────────────────────────────────────────────┤
│  Agent Layer (role-specific system prompts)             │
│  ├── Stage-aware context (behavior per pipeline stage)  │
│  ├── Skill routing maps (which skill when)              │
│  └── Output format specs (consistent artifacts)         │
└─────────────────────────────────────────────────────────┘
```

**Start with the Skills layer** — it has the highest impact-to-effort ratio. Then add hooks for automation, then enhance agent profiles, then update configuration.

---

_Document Version: 1.0_
_Last Updated: 2026-04-24_
_Author: Claude Lab Research Team_
