# Advanced Prompt Patterns

## Pattern Catalog

### P-001: The Socratic Prompt

**Purpose:** Guide the model to help you think through a problem rather than giving direct answers.

```
I'm working on {problem}. Don't give me the answer directly.
Instead, ask me 3-5 probing questions that will help me arrive at the solution myself.
After I answer each question, provide feedback and ask the next question.
```

**Use cases:** Learning, interview prep, architectural thinking.

---

### P-002: The Devil's Advocate

**Purpose:** Stress-test ideas by having the model argue against them.

```
I believe that {position/decision}.

Act as a skilled debater. Present the strongest possible counterarguments:
1. At least 5 distinct arguments against my position
2. Evidence or examples supporting each counterargument
3. The strongest single argument (your best shot)
4. Conditions under which my position would be clearly wrong

After presenting the counterarguments, provide a balanced assessment of whether my position still holds.
```

**Use cases:** Decision validation, risk assessment, debate prep.

---

### P-003: The Multi-Perspective Analyzer

**Purpose:** Examine a topic from multiple stakeholder viewpoints.

```
Analyze the following situation from the perspectives of these stakeholders:

Situation: {description}

Stakeholders:
1. {stakeholder_a} — cares about {priority}
2. {stakeholder_b} — cares about {priority}
3. {stakeholder_c} — cares about {priority}

For each stakeholder:
- Their primary concerns
- How they would view the situation
- What outcome they would prefer
- Potential conflicts with other stakeholders

Synthesis: Where do interests align? Where do they conflict? What's the optimal compromise?
```

**Use cases:** Product decisions, policy analysis, team dynamics.

---

### P-004: The Incremental Refinement Loop

**Purpose:** Iteratively improve output through structured feedback cycles.

```
Step 1: Generate an initial draft of {deliverable}.

Step 2: Review your draft against these criteria:
- {criterion_1}
- {criterion_2}
- {criterion_3}

Step 3: List specific improvements needed.

Step 4: Produce a revised version incorporating all improvements.

Step 5: Compare the original and revised versions, noting what changed and why.
```

**Use cases:** Writing, code, design documents, any iterative work.

---

### P-005: The Constraint Solver

**Purpose:** Find solutions that satisfy multiple hard constraints.

```
Find a solution that satisfies ALL of the following constraints:

Hard constraints (must satisfy):
1. {constraint_1}
2. {constraint_2}
3. {constraint_3}

Soft constraints (prefer but can compromise):
1. {constraint_4}
2. {constraint_5}

For each proposed solution:
- Which hard constraints it satisfies (must be ALL)
- Which soft constraints it satisfies
- Trade-offs involved
- Why alternative approaches fail

If no solution satisfies all hard constraints, explain which constraint(s) must be relaxed and why.
```

**Use cases:** Scheduling, resource allocation, system design, optimization.

---

### P-006: The Knowledge Synthesizer

**Purpose:** Combine information from multiple sources into coherent understanding.

```
Synthesize the following sources into a unified understanding of {topic}:

Source 1: {summary_or_excerpt}
Source 2: {summary_or_excerpt}
Source 3: {summary_or_excerpt}

Provide:
1. Points of agreement across sources
2. Points of disagreement or tension
3. Unique insights from each source
4. A synthesized narrative that incorporates the strongest elements of each
5. Gaps in current understanding (what none of the sources address)
6. Recommended next research questions
```

**Use cases:** Literature review, competitive analysis, research synthesis.

---

### P-007: The Scenario Simulator

**Purpose:** Explore "what if" scenarios with structured reasoning.

```
Simulate the following scenario over a {timeframe} period:

Initial state: {current_situation}
Event: {triggering_event}

For each time period ({interval}):
1. What changes as a direct result
2. Second-order effects (consequences of consequences)
3. How different actors respond
4. New risks or opportunities that emerge

Provide:
- Best case outcome (with probability estimate)
- Most likely outcome (with probability estimate)
- Worst case outcome (with probability estimate)
- Early warning indicators to watch for
- Mitigation strategies for negative outcomes
```

**Use cases:** Risk planning, strategy, incident response prep.

---

### P-008: The Abstraction Ladder

**Purpose:** Move between concrete details and abstract principles.

```
Take the following concrete example and analyze it at multiple levels of abstraction:

Concrete example: {specific_case}

Level 1 — Concrete: What exactly happened in this case?
Level 2 — Pattern: What pattern does this exemplify?
Level 3 — Principle: What general principle does this pattern illustrate?
Level 4 — Framework: What broader framework or theory encompasses this principle?

Now go the other direction:
Level 4 → Level 3 → Level 2 → Level 1: Apply the framework to a NEW concrete example in a different domain.

Insight: What does this cross-domain application reveal?
```

**Use cases:** Learning transfer, innovation, cross-domain problem solving.

---

### P-009: The Pre-Mortem

**Purpose:** Identify failure modes before they happen.

```
Imagine it is {future_date} and our project has failed spectacularly.

Project: {description}
Goals: {objectives}
Timeline: {schedule}

Conduct a pre-mortem analysis:
1. What are the 5 most likely causes of failure?
2. For each cause:
   - Early warning signs (what would we have noticed?)
   - Probability (low/medium/high)
   - Impact (low/medium/high)
   - Prevention strategy
   - Contingency plan if prevention fails

3. Which single failure mode would be most catastrophic?
4. What's the one thing we should do tomorrow to reduce overall risk?
```

**Use cases:** Project planning, product launches, system deployments.

---

### P-010: The Teaching Test

**Purpose:** Verify understanding by having the model teach the concept.

```
Explain {concept} as if teaching it to {audience_description}.

Requirements:
- Use the Feynman Technique: simple language, no jargon without explanation
- Include at least one analogy from everyday life
- Show a worked example from start to finish
- Anticipate and address the 3 most common misunderstandings
- End with 3 self-test questions the learner can use to verify their understanding

After the explanation, assess: What parts of this concept are still confusing? What would need a deeper dive?
```

**Use cases:** Learning verification, documentation, knowledge transfer.

---

### P-011: The Format Transformer

**Purpose:** Convert between representations while preserving meaning.

```
Transform the following {source_format} into {target_format}:

<input>
{content}
</input>

Rules:
- Preserve all information (no loss)
- Do not add information not present in the source
- Maintain the original meaning and intent
- Use {target_format} conventions correctly

Output: {target_format} only, no commentary.
```

**Use cases:** Data migration, documentation conversion, API response formatting.

---

### P-012: The Priority Matrix

**Purpose:** Systematically prioritize a list of items.

```
Prioritize the following items using a weighted scoring model:

Items to prioritize:
1. {item_1}
2. {item_2}
3. {item_3}
...

Criteria (with weights):
- Impact (40%): How much difference does this make?
- Effort (30%): How much work is required? (lower is better)
- Risk (20%): What could go wrong? (lower is better)
- Urgency (10%): How time-sensitive is this?

For each item:
- Score 1-10 on each criterion
- Calculate weighted score
- Rank by weighted score

Output: Prioritized list with scores and brief justification for each ranking.
```

**Use cases:** Backlog prioritization, feature planning, task management.

---

## Pattern Composition

Patterns can be combined for more powerful prompts:

```
P-009 (Pre-Mortem) + P-003 (Multi-Perspective) =
"Conduct a pre-mortem from the perspective of each stakeholder group."

P-006 (Knowledge Synthesizer) + P-002 (Devil's Advocate) =
"Synthesize these sources, then argue against the synthesized conclusion."

P-004 (Incremental Refinement) + P-010 (Priority Matrix) =
"Generate options, score them, refine the top 3 through iteration."
```

---

## Pattern Selection Guide

| If you need to...          | Use pattern                                           |
| -------------------------- | ----------------------------------------------------- |
| Understand deeply          | P-001 (Socratic), P-010 (Teaching Test)               |
| Validate decisions         | P-002 (Devil's Advocate), P-009 (Pre-Mortem)          |
| Analyze complexity         | P-003 (Multi-Perspective), P-008 (Abstraction Ladder) |
| Improve iteratively        | P-004 (Incremental Refinement)                        |
| Solve constrained problems | P-005 (Constraint Solver)                             |
| Synthesize information     | P-006 (Knowledge Synthesizer)                         |
| Plan for uncertainty       | P-007 (Scenario Simulator), P-009 (Pre-Mortem)        |
| Transform data             | P-011 (Format Transformer)                            |
| Prioritize work            | P-012 (Priority Matrix)                               |

---

_Advanced Patterns v1.1 — 2026-04-24_
