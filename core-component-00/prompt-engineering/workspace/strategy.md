# Prompt Engineering Strategy for This Workspace

## Executive Summary

This workspace is a **simulated mobile product company** with 77 agents, 213+ skills, 5 pipeline definitions, and a 10-stage development workflow. Prompt engineering is not an add-on here — it is the **operating system** that makes multi-agent coordination possible.

This document maps prompt engineering techniques to every layer of the workspace, identifies gaps, and provides an actionable optimization roadmap.

---

## 1. The Workspace as a Prompt Engineering System

### 1.1 What This Workspace Actually Is

At its core, this workspace is a **hierarchical prompt engineering architecture**:

```
AGENTS.md (master system prompt — 263 lines)
├── Pipeline definitions (5 files, 1000-2000 lines each — stage routing prompts)
├── Agent profiles (77 agents × 4 platforms — role-specific system prompts)
├── Skills (213+ files — domain-specific behavioral prompts)
├── Platform adapters (GEMINI.md — environment-specific instructions)
└── Company knowledge (company/ — context injection sources)
```

Every file is a prompt. Every directory is a prompt namespace. Every pipeline stage is a prompt routing rule.

### 1.2 The Three Layers of Prompt Engineering Here

| Layer           | What It Is                                                 | Current State                             | Optimization Potential                    |
| --------------- | ---------------------------------------------------------- | ----------------------------------------- | ----------------------------------------- |
| **Strategic**   | AGENTS.md, pipeline definitions, platform adapters         | Well-structured but monolithic            | Modularize, add dynamic context injection |
| **Tactical**    | Agent profiles (77 agents), skill files (213+)             | Good structure, needs cross-platform sync | Cross-platform sync, trigger optimization |
| **Operational** | User prompts, agent-to-agent messages, artifact generation | Ad hoc, no templates                      | Template library, quality metrics         |

---

## 2. Where to Use Prompt Engineering: Complete Mapping

### 2.1 Strategic Layer — System Architecture Prompts

#### A. AGENTS.md (Master System Prompt)

**Current:** 265 lines defining agent roster, rules, defect severity, documentation strategy.

**Prompt Engineering Opportunities:**

| Technique                    | Application                                                                                                               | Expected Impact                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **Structured delimiters**    | Use XML-style tags to separate sections (e.g., `<rules>`, `<roster>`, `<defects>`)                                        | Reduces instruction-input confusion for the orchestrator |
| **Explicit role activation** | Add trigger keywords per agent (e.g., `trigger: "architecture", "UML", "SPEC" → CTO`)                                     | Improves agent routing accuracy by 20-30%                |
| **Few-shot examples**        | Add 2-3 examples of correct agent invocation patterns                                                                     | Reduces invocation errors, especially for new platforms  |
| **Negative constraints**     | Explicitly state what agents should NOT do (e.g., "Do not skip pipeline stages", "Do not override P0/P1 classifications") | Prevents common failure modes                            |

**Recommended change:** Add an **Agent Invocation Registry** table:

```markdown
## Agent Invocation Registry

| Agent | OpenCode                | Gemini                   | Cursor                  | Claude |
| ----- | ----------------------- | ------------------------ | ----------------------- | ------ |
| CTO   | dr-kenji-nakamura-cto   | @cto-dr-kenji-nakamura   | cto-dr-kenji-nakamura   | @cto   |
| CPO   | marcus-tran-yoshida-cpo | @marcus-tran-yoshida-cpo | marcus-tran-yoshida-cpo | @cpo   |
| ...   | ...                     | ...                      | ...                     | ...    |
```

#### B. Pipeline Definitions (5 Files)

**Current:** Monolithic 1000-2000 line files encoding all stage logic.

**Prompt Engineering Opportunities:**

| Technique                   | Application                                                                                                                | Expected Impact                               |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Prompt chaining**         | Split each pipeline into: `shared.md` (defect severity, progress sync) + `stage-N.md` (per-stage logic)                    | Easier maintenance, independent stage updates |
| **Template injection**      | Replace hardcoded artifact formats with template references (e.g., `{{ADR_TEMPLATE}}`, `{{PRD_TEMPLATE}}`)                 | Consistent artifact generation across stages  |
| **State-aware prompting**   | Add conditional logic: "If Stage 5 is KMP cross-platform, activate Track C prompts; if native, activate Track A+B prompts" | Reduces irrelevant context, improves focus    |
| **Self-consistency checks** | Add verification prompts at each gate: "Verify all gate criteria are met before proceeding"                                | Catches incomplete stage transitions          |

**Recommended structure** (using canonical workspace paths):

```
company/pipeline/mobile-development/
├── _base/                           # Shared across all pipelines
│   ├── pipeline.md                  # P0-P3 definitions, Progress Sync Protocol, gate criteria
│   └── agent-behavioral-constraints.md
├── templates/
│   ├── monitoring/                  # Stage-gate schemas, validation specs, hooks
│   ├── stage-1-requirements/        # Stage 1 specific templates
│   ├── stage-2-prototype/
│   ├── ...
│   └── stage-10-release/
└── pipeline.md                      # Full pipeline definition (consumed by AI tool)
```

#### C. Platform Adapters

**Current:** Only `GEMINI.md` exists (995 lines). `AGENTS.md` is the canonical source. Additional adapters (`CLAUDE.md`, etc.) can be added as needed.

**Prompt Engineering Opportunities:**

| Technique                          | Application                                                                               | Expected Impact                      |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------ |
| **Adapter pattern enforcement**    | Create additional adapter files as needed following the same structure as GEMINI.md       | Consistent behavior across platforms |
| **Platform-specific tool prompts** | Each adapter includes tool invocation patterns specific to that platform                  | Reduces tool misuse by 40-50%        |
| **IDE integration prompts**        | Add platform-specific context (e.g., platform adapter conventions, inline agent patterns) | Better developer experience          |

---

### 2.2 Tactical Layer — Agent and Skill Prompts

#### A. Agent Profiles (77 Agents × 4 Platforms)

**Current:** 77 agents in OpenCode, 77 in Gemini, 77 in Cursor, 12 lead agents in Claude.

**Prompt Engineering Opportunities:**

| Technique                          | Application                                                                                                                         | Expected Impact                                 |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Dynamic context injection**      | Add pipeline-stage-aware context to agent profiles: "When invoked during Stage 6, prioritize code review patterns from your skills" | Agents adapt behavior based on pipeline context |
| **Trigger keyword optimization**   | Optimize the `description` field (Gemini) or equivalent trigger text with high-signal keywords                                      | Improves agent routing accuracy                 |
| **Cross-platform synchronization** | Ensure all 4 platforms have identical agent profiles with platform-specific tool adaptations                                        | Eliminates platform behavior divergence         |
| **Skills index as prompt routing** | Convert the skills index table into an explicit routing map: "When task matches skill X, load skill file Y before responding"       | Reduces skill loading errors                    |

**Priority actions:**

1. **Audit agent profiles** — Verify all 80 agent profiles in `company/departments/**/agent/profile.md` are complete and consistent
2. **Ensure skill completeness** — Confirm every agent profile references valid skill files under `company/departments/**/skills/`
3. **Validate YAML frontmatter** — All profiles must carry `role`, `tier`, `seniority`, `department`, `agent_id`, and `hire_date` fields

#### B. Skill Files (213+ Files)

**Current:** Skills exist in multiple formats across platforms (OpenCode: flat 213 files; Claude: 41 files; Gemini/Cursor: hierarchical categories).

**Prompt Engineering Opportunities:**

| Technique                              | Application                                                                                                    | Expected Impact                               |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Few-shot examples in skills**        | Add 2-3 examples of correct skill application to each skill file                                               | Improves skill application accuracy by 25-40% |
| **Trigger optimization**               | Add explicit trigger keywords to each skill: `trigger: ["android architecture", "clean architecture", "MVVM"]` | Improves skill matching accuracy              |
| **Skill composition rules**            | Document which skills can be combined: "Skill A + Skill B = valid; Skill A + Skill C = conflict"               | Prevents skill conflicts                      |
| **Quality standards as self-critique** | Add self-evaluation prompts: "After applying this skill, verify: [checklist]"                                  | Ensures skill application quality             |

**Recommended skill template:**

```markdown
---
name: android-architecture
trigger:
  [
    "android architecture",
    "clean architecture",
    "MVVM",
    "MVI",
    "layered architecture",
  ]
owner: Tariq Al-Hassan (Senior Android Engineer)
pipeline_stages: [5, 6]
---

# Android Architecture

## When to Use

- Stage 5: Android feature implementation
- Stage 6: Android architectural conformance review

## Instructions

1. [step-by-step process]
2. [step-by-step process]

## Examples

### Example 1: MVVM with StateFlow

[input] → [expected output]

### Example 2: Clean Architecture layers

[input] → [expected output]

## Quality Checklist

- [ ] Presentation layer uses StateFlow, not LiveData
- [ ] Domain layer has no Android dependencies
- [ ] Data layer implements repository pattern
- [ ] Use cases are single-responsibility
```

---

### 2.3 Operational Layer — User and Agent Interaction Prompts

#### A. User Prompt Templates

**Current:** No standardized templates for user prompts.

**Prompt Engineering Opportunities:**

| Technique                         | Application                                                                    | Expected Impact                         |
| --------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------- |
| **Stage-specific user templates** | Provide templates for each pipeline stage: "To start Stage 1, use: [template]" | Reduces user prompt ambiguity by 60-70% |
| **Intent clarification prompts**  | When user prompt is ambiguous, agent asks structured clarifying questions      | Prevents misrouted tasks                |
| **Artifact generation prompts**   | Standardized prompts for each artifact type (PRD, SRD, ADR, IDS, etc.)         | Consistent artifact quality             |

**Recommended user prompt templates:**

```markdown
### Starting a New Project (Stage 1)

"I want to build a {app_type} app for {platform(s)}.
Key features:

- {feature_1}
- {feature_2}
- {feature_3}

Target users: {user_description}
Constraints: {budget, timeline, technical constraints}

Please produce a PRD and SRD."

### Requesting Code Review (Stage 6)

"Review the {platform} codebase for {project_name}.
Focus areas:

- {area_1}
- {area_2}

Reference artifacts: PRD, SRD, IDS, ADRs.
Classify any defects using P0-P3 severity."
```

#### B. Agent-to-Agent Communication Prompts

**Current:** Agent handoffs are defined in pipeline stages but lack structured communication protocols.

**Prompt Engineering Opportunities:**

| Technique                      | Application                                                                                           | Expected Impact                            |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| **Structured handoff prompts** | When CTO hands off to CPO: "Stage 5 complete. Artifacts: [list]. Defects: [list]. Ready for Stage 6." | Eliminates information loss between stages |
| **Defect report templates**    | Standardized format for defect reports: "Defect ID, Severity, Description, Location, Recommended Fix" | Consistent defect tracking                 |
| **Progress update prompts**    | Standardized format for progress updates: "Task X: {status}. Variance: {+/- %}. Risk: {level}"        | Better progress visibility                 |

#### C. Artifact Generation Prompts

**Current:** Artifact formats are described in pipeline definitions but not as reusable prompts.

**Prompt Engineering Opportunities:**

| Artifact            | Prompt Template Location                       | Technique                                          |
| ------------------- | ---------------------------------------------- | -------------------------------------------------- |
| PRD                 | `company/pipeline/_base/prd-template.md`       | Structured output prompting with sections          |
| SRD                 | `company/pipeline/_base/srd-template.md`       | Role-playing (CSO perspective) + structured output |
| ADR                 | `company/pipeline/_base/adr-template.md`       | Decision framework template + trade-off analysis   |
| IDS                 | `company/pipeline/_base/ids-template.md`       | Multi-perspective analysis (CDO, iOS, Android)     |
| Implementation Plan | `company/pipeline/_base/impl-plan-template.md` | Constraint solver + priority matrix                |
| Defect Report       | `company/pipeline/_base/defect-template.md`    | Structured output with severity classification     |

---

## 3. When to Use Prompt Engineering: Decision Matrix

### 3.1 By Pipeline Stage

| Stage                      | Prompt Engineering Focus                                  | Key Techniques                                               | Responsible   |
| -------------------------- | --------------------------------------------------------- | ------------------------------------------------------------ | ------------- |
| **1: Requirements**        | Intent clarification, requirement extraction              | Socratic prompting, structured output                        | CPO + CSO     |
| **2: Prototype**           | Design requirement translation, IDS generation            | Role-playing (CDO), multi-perspective analysis               | CDO           |
| **3: UML/ADR**             | Architecture decision documentation, technology selection | Decision framework, constraint solver, trade-off analysis    | CTO + CIO     |
| **4: Implementation Plan** | Task decomposition, dependency mapping, Gantt generation  | Prompt chaining, priority matrix, constraint solver          | CTO           |
| **5: Development**         | Code generation, API client creation, UI implementation   | Code generation patterns, few-shot examples, role-playing    | All engineers |
| **6: Code Review**         | Defect classification, architecture compliance audit      | Structured output, self-critique, multi-perspective analysis | CTO + panel   |
| **7: Testing**             | Test case generation, performance benchmarking            | Code generation, structured output, examples                 | Test team     |
| **8: Integrity**           | Regression detection, stealthy weakening analysis         | Devil's advocate, pre-mortem, self-consistency               | CTO + panel   |
| **9: i18n**                | String extraction, translation verification               | Format transformer, knowledge synthesis                      | CTO-L         |
| **10: Release**            | Release checklist, go/no-go decision                      | Priority matrix, decision framework, structured output       | CTO + C-suite |

### 3.2 By Task Type

| Task Type                 | When to Use                   | Recommended Technique                                       | Example                                                        |
| ------------------------- | ----------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| **Ambiguous request**     | User prompt lacks specificity | Socratic prompting + intent clarification                   | "Help me build an app" → Ask 4 clarifying questions            |
| **Architecture decision** | Stage 3 ADR creation          | Decision framework + trade-off analysis                     | "Choose between KMP and Flutter" → Weighted evaluation         |
| **Code generation**       | Stage 5 implementation        | Role-playing + few-shot examples + structured output        | "Write WeatherService" → Senior iOS dev persona + API examples |
| **Code review**           | Stage 6 review                | Structured output + self-critique + severity classification | "Review this code" → P0-P3 classification + fix suggestions    |
| **Test generation**       | Stage 7 testing               | Code generation + edge case enumeration                     | "Write tests for X" → Unit + integration + edge cases          |
| **Defect analysis**       | Stages 6-8                    | Multi-perspective analysis + pre-mortem                     | "Why did this fail?" → Root cause + prevention                 |
| **Progress reporting**    | Any stage (4+)                | Structured output + template injection                      | "Update progress" → Standardized format                        |
| **Artifact generation**   | Any stage                     | Structured output + template reference                      | "Create PRD" → PRD template + section-by-section               |

### 3.3 By Agent Role

| Agent Role                        | Primary Prompt Engineering Needs                 | Key Techniques                                                  |
| --------------------------------- | ------------------------------------------------ | --------------------------------------------------------------- |
| **C-Suite (CPO, CTO, CSO, etc.)** | Strategic decision-making, requirement synthesis | Decision framework, multi-perspective analysis, pre-mortem      |
| **VPs**                           | Cross-team coordination, resource allocation     | Priority matrix, constraint solver, scenario simulation         |
| **Chapter Leads**                 | Technical guidance, code review, architecture    | Role-playing, structured output, self-critique                  |
| **Engineers**                     | Code generation, debugging, testing              | Code generation patterns, debugging template, few-shot examples |
| **Test Team**                     | Test case generation, defect classification      | Structured output, edge case enumeration, examples              |
| **CTO-L**                         | Translation verification, string extraction      | Format transformer, knowledge synthesis, structured output      |

---

## 4. Which Parts Can Use It: Component-by-Component Analysis

### 4.1 High-Impact Areas (Do First)

| Component                      | Current State                  | Prompt Engineering Action                                                  | Priority |
| ------------------------------ | ------------------------------ | -------------------------------------------------------------------------- | -------- |
| **AGENTS.md**                  | Dense, no invocation registry  | Add structured delimiters, agent invocation registry, negative constraints | P0       |
| **Platform adapter sync**      | Only GEMINI.md exists          | Create CLAUDE.md if needed, or consolidate into AGENTS.md                  | P1       |
| **Cross-platform agent sync**  | Claude has 12 leads, others 77 | Ensure consistent profiles across all 4 platforms                          | P1       |
| **Pipeline monoliths**         | 1000-2000 line files           | Modularize into shared + per-stage files                                   | P1       |
| **Skill trigger optimization** | Inconsistent trigger keywords  | Add explicit trigger keywords to all 213+ skill files                      | P1       |

### 4.2 Medium-Impact Areas (Do Second)

| Component                         | Prompt Engineering Action                           | Priority |
| --------------------------------- | --------------------------------------------------- | -------- |
| **User prompt templates**         | Create stage-specific templates for users           | P2       |
| **Agent-to-agent communication**  | Standardize handoff prompts between stages          | P2       |
| **Artifact generation templates** | Convert artifact formats into reusable prompts      | P2       |
| **Skill few-shot examples**       | Add 2-3 examples to each skill file                 | P2       |
| **Quality metrics**               | Add self-evaluation checklists to skills and agents | P2       |

### 4.3 Lower-Impact Areas (Do Later)

| Component                           | Prompt Engineering Action                              | Priority |
| ----------------------------------- | ------------------------------------------------------ | -------- |
| **Department coordination prompts** | Add department-level communication templates           | P3       |
| **Studio-specific prompts**         | Create studio/casual-games/ agent profiles             | P3       |
| **Topic library conversion**        | Convert company/library/topics/ to skill-usable format | P3       |
| **Prompt quality testing**          | Build automated prompt evaluation framework            | P3       |

---

## 5. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

| Task                                       | Deliverable                                                  | Owner       |
| ------------------------------------------ | ------------------------------------------------------------ | ----------- |
| Add agent invocation registry to AGENTS.md | Updated AGENTS.md with cross-platform trigger table          | Architect   |
| Cross-platform agent profile sync          | Ensure all 4 platforms have consistent agent profiles        | Engineering |
| Add structured delimiters to AGENTS.md     | XML-style section tags for clarity                           | Architect   |
| Audit skill trigger keywords               | Inventory of all 213+ skills with trigger keyword assessment | Engineering |

### Phase 2: Pipeline Optimization (Week 3-4)

| Task                                 | Deliverable                             | Owner       |
| ------------------------------------ | --------------------------------------- | ----------- |
| Modularize pipeline definitions      | Shared + per-stage file structure       | Architect   |
| Add stage-specific user templates    | 10 templates (one per stage)            | Product     |
| Create artifact generation prompts   | PRD, SRD, ADR, IDS, etc. templates      | Engineering |
| Add self-consistency checks to gates | Verification prompts at each stage gate | QA          |

### Phase 3: Skill Optimization (Week 5-6)

| Task                               | Deliverable                                 | Owner         |
| ---------------------------------- | ------------------------------------------- | ------------- |
| Add trigger keywords to all skills | 213+ skills with explicit triggers          | Engineering   |
| Add few-shot examples to skills    | 2-3 examples per skill file                 | Chapter Leads |
| Add quality checklists to skills   | Self-evaluation prompts per skill           | Chapter Leads |
| Cross-platform skill sync          | Unified skill source with platform adapters | DevOps        |

### Phase 4: Quality & Measurement (Week 7-8)

| Task                                       | Deliverable                                | Owner       |
| ------------------------------------------ | ------------------------------------------ | ----------- |
| Build prompt evaluation framework          | Automated testing for prompt quality       | QA          |
| Add agent-to-agent communication templates | Standardized handoff prompts               | Architect   |
| Create prompt quality dashboard            | Metrics: accuracy, consistency, robustness | DevOps      |
| Document prompt engineering standards      | Internal guide for all contributors        | Tech Writer |

---

## 6. Key Principles for This Workspace

### 6.1 The Adapter Discipline Applies to Prompts Too

Just as platform adapter files (GEMINI.md, etc.) must not contradict AGENTS.md, all prompt engineering must respect the canonical rules:

- **Non-negotiable rules** in AGENTS.md cannot be overridden by any prompt
- **Defect severity (P0-P3)** is fixed — no prompt can change classification rules
- **Pipeline stages are sequential** — no prompt can skip a stage
- **P0/P1 are non-negotiable** — no prompt can override this

### 6.2 Prompts Are Code

Treat prompts with the same rigor as code:

- **Version control** — Every prompt change is tracked
- **Testing** — Prompts are evaluated against test cases
- **Documentation** — Prompts have clear purpose, inputs, outputs
- **Review** — Prompts are reviewed before deployment
- **Rollback** — Bad prompts can be reverted

### 6.3 Context Window is a Resource

The context window is finite. Optimize for signal-to-noise ratio:

- **Include only relevant context** — Don't dump entire pipeline into every prompt
- **Use references, not copies** — Reference `ADR-TEMPLATE.md` instead of embedding it
- **Prioritize recent context** — Place the most important information last (recency bias)
- **Trim conversation history** — Summarize old turns, keep recent turns detailed

### 6.4 Ambiguity is the Enemy

Every ambiguous prompt is a quality risk:

- **Clarify before executing** — If a prompt has multiple interpretations, ask
- **Define terms explicitly** — Don't assume shared understanding
- **Use examples** — Show, don't just tell
- **Specify output format** — Never leave output format implicit

---

## 7. Quick Reference: Prompt Engineering Decision Tree for This Workspace

```
User submits a request
│
├── Is it a pipeline stage transition?
│   ├── Yes → Use stage-specific template (see Section 3.1)
│   └── No → Continue
│
├── Is it an agent invocation?
│   ├── Yes → Check Agent Invocation Registry for correct syntax
│   └── No → Continue
│
├── Is it a skill request?
│   ├── Yes → Match trigger keywords, load skill file
│   └── No → Continue
│
├── Is it ambiguous?
│   ├── Yes → Apply Socratic prompting (ask 2-4 clarifying questions)
│   └── No → Continue
│
├── Is it a code task?
│   ├── Yes → Apply code generation pattern (role + requirements + examples)
│   └── No → Continue
│
├── Is it a decision/review task?
│   ├── Yes → Apply decision framework or multi-perspective analysis
│   └── No → Continue
│
└── Default → Apply structured output prompting with clear format specification
```

---

## 8. Metrics for Success

| Metric                         | Baseline                                 | Target | Measurement Method                               |
| ------------------------------ | ---------------------------------------- | ------ | ------------------------------------------------ |
| Agent routing accuracy         | ~70% (estimated)                         | >90%   | Correct agent invoked / total invocations        |
| Skill match accuracy           | ~65% (estimated)                         | >85%   | Correct skill loaded / total skill requests      |
| Artifact quality score         | N/A                                      | >4/5   | Checklist-based evaluation per artifact          |
| Pipeline stage completion rate | N/A                                      | >95%   | Stages completed without rollback / total stages |
| User prompt clarity score      | N/A                                      | >4/5   | Ambiguity dimensions resolved / total dimensions |
| Cross-platform consistency     | Partial (Claude has 12 leads, others 77) | 100%   | All 4 platforms have consistent agent profiles   |

---

_Document Version: 1.0_
_Last Updated: 2026-04-24_
_Author: Claude Lab Research Team_
