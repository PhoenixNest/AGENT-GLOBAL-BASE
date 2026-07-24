# Advanced Prompt Patterns

## Pattern Catalog

| ID    | Pattern                         | Purpose                                                                                    | Best For                                                     |
| ----- | ------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| P-001 | **Socratic Prompt**             | Guide thinking through probing questions rather than direct answers                        | Learning, interview prep, architectural thinking             |
| P-002 | **Devil's Advocate**            | Stress-test ideas by having the model argue against them                                   | Decision validation, risk assessment                         |
| P-003 | **Multi-Perspective Analyzer**  | Examine a topic from multiple stakeholder viewpoints                                       | Product decisions, policy analysis, team dynamics            |
| P-004 | **Incremental Refinement Loop** | Iteratively improve output through structured feedback cycles                              | Writing, code, design documents                              |
| P-005 | **Constraint Solver**           | Find solutions that satisfy multiple hard constraints                                      | Scheduling, resource allocation, system design               |
| P-006 | **Knowledge Synthesizer**       | Combine information from multiple sources into coherent understanding                      | Literature review, competitive analysis                      |
| P-007 | **Scenario Simulator**          | Explore "what if" scenarios with structured reasoning                                      | Risk planning, strategy, incident response prep              |
| P-008 | **Abstraction Ladder**          | Move between concrete details and abstract principles                                      | Learning transfer, innovation, cross-domain problem solving  |
| P-009 | **Pre-Mortem**                  | Identify failure modes before they happen                                                  | Project planning, product launches, deployments              |
| P-010 | **Teaching Test**               | Verify understanding by having the model teach the concept                                 | Learning verification, documentation                         |
| P-011 | **Format Transformer**          | Convert between representations while preserving meaning                                   | Data migration, documentation conversion                     |
| P-012 | **Priority Matrix**             | Systematically prioritise a list of items                                                  | Backlog prioritisation, feature planning                     |
| P-013 | **Persona Resolution**          | Ground a detected persona in a real, documented identity instead of freehanding voice      | Gates/optimizers that add role context, multi-agent handoffs |
| P-014 | **Delegation Routing**          | Decide whether a request should go to a single agent, a team of leads, or a broad fallback | Request triage, gate/optimizer ownership decisions           |

---

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

### P-013: Persona Resolution

**Purpose:** When a prompt names or clearly implies a specific real agent, persona, department, or
module, ground the response in that identity's actual documented profile instead of freehanding
voice or authority from the label alone.

```
A prompt or gate has detected persona/role context: {detected_label}.

Before responding in that voice:
1. Determine whether {detected_label} names a real, documented agent in this workspace (a
   Company/Studio/CC-00/ANU-00 crew member) or is a generic/hypothetical role.
2. If real: read that agent's profile.md and every skill file it references before producing
   any output. Follow the workspace's Activation Protocol exactly — do not skip straight to
   voice imitation.
3. If generic or ambiguous: do not invent a specific real identity. Either use the generic role
   as stated, or ask a clarifying question if the ambiguity is high-confidence-unresolvable.
4. Stay within that identity's documented authority scope. Do not claim authority, reporting
   lines, or module ownership the profile does not grant.

Output: a response in the resolved identity's voice, grounded in its actual profile — never a
label-only impersonation.
```

**Design constraint:** detection of a persona cue (a keyword match, a gate heuristic) is cheap and
unreliable at _resolving_ identity — that judgment requires reading the real source document.
Any consumer of this pattern (a hook, a gate, an agent) should trigger on the cue but defer
resolution to this pattern's steps, never resolve identity from the trigger alone.

**Use cases:** Prompt-optimization gates that add role/persona context (e.g. H-P01), multi-agent
handoffs, any system that lets a user address a named organizational agent directly.

---

### P-014: Delegation Routing

**Purpose:** Decide whether a request should be handled by a single agent, a team of
module/department leads, or a broad/uncategorizable fallback — and surface that decision for
confirmation rather than applying it silently.

```
A request needs an ownership decision before execution.

1. Domain match: does the request clearly belong to one documented agent, module, or department?
   → Route single-agent. Resolve via P-013 before responding in their voice.
2. Multi-domain match: does the request span more than one module/department without a single
   clean owner? → Route to that specific set of module/department leads, named explicitly — not
   a generic "the team."
3. No confident domain match: is the request genuinely too broad or unclassifiable, not just a
   heuristic miss? → Route to the designated broad fallback for the requesting system (defined
   per-system, e.g. Dr. Vance + Dr. Nwosu-Chen for CC-00-scoped requests).
4. Surface the proposed owner from step 1-3 alongside the rewritten/optimized request in the same
   confirmation step already required by the calling gate or workflow — never apply routing
   silently.

Constraint: never route across an explicit organizational-independence boundary (e.g. ANU-00's
independence from CC-00) as a standing fallback, even when convenient. A boundary violation is
not a valid "no confident match" resolution.
```

**Design constraint:** like P-013, domain detection stays heuristic (fast, approximate); routing
_decisions_ — especially fallback assignment — require model judgment and, where an
organizational-boundary rule exists, a compliance check against it before the route is proposed.

**Use cases:** Prompt-optimization gates deciding whether to hand a request to a specific agent
or team (e.g. H-P01), request-triage systems, any workflow with more than one plausible owner.

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

| If you need to...                   | Use pattern                                           |
| ----------------------------------- | ----------------------------------------------------- |
| Understand deeply                   | P-001 (Socratic), P-010 (Teaching Test)               |
| Validate decisions                  | P-002 (Devil's Advocate), P-009 (Pre-Mortem)          |
| Analyze complexity                  | P-003 (Multi-Perspective), P-008 (Abstraction Ladder) |
| Improve iteratively                 | P-004 (Incremental Refinement)                        |
| Solve constrained problems          | P-005 (Constraint Solver)                             |
| Synthesize information              | P-006 (Knowledge Synthesizer)                         |
| Plan for uncertainty                | P-007 (Scenario Simulator), P-009 (Pre-Mortem)        |
| Transform data                      | P-011 (Format Transformer)                            |
| Prioritize work                     | P-012 (Priority Matrix)                               |
| Ground a persona in a real identity | P-013 (Persona Resolution)                            |
| Decide request ownership            | P-014 (Delegation Routing)                            |

---

_Advanced Patterns v1.2 — 2026-07-24_
