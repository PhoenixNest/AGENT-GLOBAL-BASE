---
name: spec-development
description: Comprehensive technical specification (SPEC) development for software projects. Use when the user needs to create technical specifications, interpret product requirements into technical documentation, break down business requirements into implementation plans, create phased project plans, or author detailed technical documentation for development teams. Trigger when user mentions "SPEC", "technical specification", "requirements breakdown", "implementation plan", or needs to translate product requirements into technical documentation.
version: "1.0.0"
---

# SPEC Development

## Purpose

Transform product requirements and business needs into comprehensive technical specifications (SPECs) that guide engineering teams through implementation. A well-crafted SPEC bridges product vision and technical execution, providing clarity on what to build, how to build it, and how to measure success.

## Why This Matters

Creates comprehensive technical specifications from requirements. Missing specs cause implementation gaps, scope creep, and Stage 6 code review failures.

## When to Use This Skill

Use this skill when:

- Product requirements need to be translated into technical specifications
- A new feature or system requires detailed technical planning
- Business stakeholders need technical documentation they can understand
- Engineering teams need clear implementation guidance
- Complex projects require phased delivery planning
- Cross-functional alignment is needed before development begins

## SPEC Structure

A comprehensive SPEC follows this structure:

### 1. Business Context

Start by explaining why this work matters. Include:

- Problem statement: What user or business problem are we solving?
- Success criteria: How will we know this succeeded?
- Stakeholders: Who cares about this and why?
- Constraints: Timeline, budget, compliance, or technical limitations

This section should be readable by non-technical stakeholders. Avoid jargon.

### 2. Technical Approach

Explain the solution at a high level before diving into details:

- Architecture overview: How does this fit into the existing system?
- Key technical decisions: What are the major choices and why?
- Trade-offs considered: What alternatives did we reject and why?
- Dependencies: What other systems, teams, or work does this rely on?

### 3. Detailed Design

This is the core technical content. Include:

- **Architecture diagrams**: Use UML component diagrams, sequence diagrams, or system diagrams to show structure and interactions
- **API contracts**: Define interfaces, request/response formats, error codes
- **Data models**: Schema definitions, relationships, migration strategy
- **Component specifications**: Break down each major component with its responsibilities, interfaces, and implementation notes

### 4. Implementation Plan

Break the work into phases:

- **Phase 1, 2, 3...**: Each phase should be independently deployable and provide incremental value
- **Task breakdown**: List specific engineering tasks with effort estimates
- **Dependencies**: What must be done before what?
- **Rollout strategy**: How will we deploy this safely? Feature flags? Gradual rollout?

### 5. Success Metrics and Monitoring

Define how we'll measure success:

- **Key metrics**: What numbers should move? By how much?
- **Instrumentation**: What events, logs, or metrics need to be added?
- **Monitoring and alerts**: What could go wrong? How will we detect it?

### 6. Migration and Rollback

For changes to existing systems:

- **Migration path**: How do we move from current state to new state?
- **Backward compatibility**: Do we need to support the old system during transition?
- **Rollback procedure**: If this fails in production, how do we revert?

## Requirements Decomposition Process

When given product requirements, follow this process:

1. **Clarify the intent**: Before writing anything, ensure you understand what the product team actually wants and why. Ask questions about edge cases, success criteria, and constraints.

2. **Identify technical implications**: What systems are affected? What new components are needed? What existing code needs to change?

3. **Break down into components**: Decompose the feature into logical technical components. Each component should have a clear responsibility and well-defined interfaces.

4. **Sequence the work**: Determine what can be built in parallel vs. what has dependencies. Organize into phases that deliver incremental value.

5. **Estimate complexity**: For each component and phase, provide effort estimates (in person-weeks or story points, depending on team conventions). Call out areas of high uncertainty.

6. **Identify risks**: What could go wrong? What are the unknowns? What external dependencies might cause delays?

## Phased Implementation Planning

Break large projects into phases that:

- Deliver incremental value (each phase should ship something useful)
- Reduce risk (validate assumptions early, tackle unknowns first)
- Enable parallel work (minimize blocking dependencies between teams)
- Allow for course correction (learn from each phase before committing to the next)

Typical phasing patterns:

- **Proof of concept → MVP → Full feature**: Validate the approach before full investment
- **Backend → Frontend → Polish**: Build the foundation before the UI
- **Core functionality → Edge cases → Optimization**: Get the happy path working first
- **Internal tool → Beta → General availability**: Test with friendly users before broad rollout

## Collaboration with Product and IT

SPECs are most effective when they bridge product and engineering:

**With Product (CPO)**:

- Translate product requirements into technical feasibility assessments
- Challenge assumptions when technical constraints affect product vision
- Propose alternative approaches that achieve product goals with less complexity
- Provide effort estimates to inform prioritization decisions

**With IT/Infrastructure (CIO)**:

- Align on technology choices and platform constraints
- Coordinate on shared infrastructure needs
- Ensure architectural decisions support long-term technical strategy
- Leverage existing tools and patterns where appropriate

## Writing Style

- **Be specific**: "Reduce API latency to <200ms p95" not "make it faster"
- **Explain the why**: Don't just say what to build, explain why this approach was chosen
- **Use diagrams**: A good diagram is worth a thousand words
- **Call out uncertainty**: If something is unclear or risky, say so explicitly
- **Make it scannable**: Use headings, bullet points, and formatting so readers can find what they need

## Common Pitfalls to Avoid

- **Over-specifying implementation details**: Leave room for engineering judgment during implementation
- **Ignoring non-functional requirements**: Performance, security, scalability, and observability matter
- **Skipping the "why"**: Without context, engineers can't make good decisions when they encounter unexpected situations
- **Assuming perfect execution**: Plan for things to go wrong; include monitoring, rollback, and debugging considerations
- **Writing for yourself**: Remember that others will read this months later when you've moved on

## Output Format

When creating a SPEC, produce a markdown document with:

- Clear section headings following the structure above
- Embedded diagrams (using mermaid, PlantUML, or image files)
- Code examples for API contracts and data models
- Tables for comparing alternatives or listing tasks
- Links to related documentation, PRDs, or design docs

The SPEC should be comprehensive enough that an engineering team can implement it without constant clarification, but not so prescriptive that it removes all engineering judgment.
