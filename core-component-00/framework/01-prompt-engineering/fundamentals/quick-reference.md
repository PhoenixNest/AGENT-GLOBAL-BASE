# Prompt Engineering Quick Reference

## Prompt Template Library

### 1. Analysis Template

```
You are a {role} expert. Analyze the following {subject}:

<context>
{relevant_background}
</context>

<input>
{data_or_content}
</input>

Provide:
1. Key findings (bullet points)
2. Supporting evidence for each finding
3. Potential blind spots or limitations
4. Actionable recommendations (ranked by impact)

Format: Markdown with clear section headers.
Length: {n} words maximum.
```

### 2. Code Review Template

```
Review the following {language} code for:
- Correctness and edge cases
- Performance (time/space complexity)
- Security vulnerabilities
- Readability and maintainability
- Best practices and idioms

<code>
{code_block}
</code>

For each issue found:
- Severity: Critical/High/Medium/Low
- Location: Line number or function name
- Description: What's wrong and why
- Fix: Corrected code snippet

Summary: Overall code quality score (1-10) with justification.
```

### 3. Architecture Design Template

```
Design a {system_type} architecture for the following requirements:

<requirements>
{functional_and_non_functional_reqs}
</requirements>

<constraints>
{budget_timeline_tech_stack}
</constraints>

Deliverables:
1. High-level architecture diagram (ASCII or description)
2. Component breakdown with responsibilities
3. Data flow description
4. Technology recommendations with justification
5. Scalability strategy
6. Failure mode analysis
7. Trade-off discussion

Format: Structured markdown with numbered sections.
```

### 4. Debugging Template

```
I'm encountering the following issue:

<symptom>
{error_message_or_behavior}
</symptom>

<context>
{relevant_code_environment_steps_to_reproduce}
</context>

<what_i_tried>
{previous_attempts}
</what_i_tried>

Please:
1. Identify the most likely root cause
2. Explain why this causes the observed symptom
3. Provide a step-by-step fix
4. Suggest how to prevent this in the future
5. List alternative causes if the primary diagnosis is wrong
```

### 5. Learning/Explanation Template

```
Explain {concept} to someone who {background_knowledge}.

Requirements:
- Start with an intuitive analogy
- Build up to the technical details
- Include a concrete example
- Address common misconceptions
- Provide resources for deeper learning

Structure:
1. What is it? (1 paragraph, plain language)
2. How does it work? (technical explanation)
3. Why does it matter? (practical significance)
4. Example (walkthrough)
5. Common pitfalls (what to avoid)
6. Next steps (where to learn more)

Tone: {educational/conversational/technical}
```

### 6. Decision Framework Template

```
I need to decide between the following options:

<option_a>
{description}
</option_a>

<option_b>
{description}
</option_b>

<option_c>
{description}
</option_c>

<criteria>
{decision_criteria_with_weights}
</criteria>

<context>
{relevant_constraints_and_goals}
</context>

Provide:
1. Evaluation matrix (criteria × options with scores)
2. Pros and cons for each option
3. Risk analysis (what could go wrong with each)
4. Recommendation with clear justification
5. Conditions under which the recommendation would change
```

### 7. Testing Template

```
Generate comprehensive tests for the following {language} code:

<code>
{code_block}
</code>

Requirements:
- Unit tests for each public function
- Edge case coverage (null, empty, boundary values)
- Error handling tests
- Integration tests (if applicable)
- Use {testing_framework}
- Include setup/teardown if needed
- Add descriptive test names

Output: Complete test file ready to run.
```

### 8. Refactoring Template

```
Refactor the following code to improve:
- Readability (naming, structure, comments)
- Performance (algorithmic efficiency)
- Maintainability (modularity, DRY principle)
- Testability (dependency injection, pure functions)

<original_code>
{code_block}
</original_code>

<constraints>
{must_preserve_behavior_target_language_version}
</constraints>

Deliverables:
1. Refactored code (complete, runnable)
2. Change log (what was changed and why)
3. Before/after complexity comparison
4. Any behavioral differences (if unavoidable)
```

---

## Prompt Anti-Patterns (What NOT to Do)

### Using "Anti-Examples" (Negative Few-Shot)

Always show the model explicitly what a _bad_ output looks like, in addition to positive examples. This prevents the model from ignoring constraints or overfitting to the positive examples.

**Good Structure:**

```
Positive Example:
Input: {valid_input}
Output: {good_output}

Negative Example (DO NOT DO THIS):
Input: {invalid_input}
Output: {bad_output} // Explain why this is bad
```

### Anti-Pattern Reference Table

| Anti-Pattern           | Example                          | Fix                                                                          |
| ---------------------- | -------------------------------- | ---------------------------------------------------------------------------- |
| **Vague goal**         | "Help me with code"              | "Review this Python function for memory leaks"                               |
| **No context**         | "Why is this slow?"              | "This SQL query takes 30s on a 1M row table. Here's the query and schema..." |
| **Contradictory**      | "Be detailed but under 50 words" | Prioritize: "Be concise (under 200 words), focusing on the top 3 issues"     |
| **Assuming knowledge** | "Fix the usual problem"          | Describe the specific symptom and context                                    |
| **Open-ended**         | "Tell me everything about X"     | "Explain X in 3 sections: basics, advanced, practical applications"          |
| **No output format**   | (nothing specified)              | "Return results as a JSON array with fields: name, score, reason"            |
| **Overloading**        | "Do A, B, C, D, E, F, and G"     | Break into sequential prompts or prioritize top 3                            |

---

## Prompt Debugging Checklist

When a prompt isn't working:

- Is the instruction clear and unambiguous?
- Is there enough context for the model to understand the task?
- Are there examples showing the expected output format?
- Is the output format explicitly specified?
- Are there conflicting or contradictory instructions?
- Is the prompt too long (diluting the key instruction)?
- Is the temperature appropriate for the task?
- Have you tested with multiple inputs to check consistency?
- Does the model have the necessary knowledge for this task?
- Would breaking this into multiple prompts help?

---

## Quick Decision Tree

```
What do you need?
├── Factual answer → Zero-shot with clear question
├── Complex reasoning → Chain-of-Thought ("think step by step")
├── Specific format → Few-shot with format examples
├── Multiple steps → Prompt chaining (stage 1 → stage 2 → ...)
├── Creative output → Higher temperature (0.7-0.9) + open-ended prompt
├── Code generation → Role + requirements + examples + test cases
├── Analysis/evaluation → Criteria + rubric + structured output
└── Decision making → Options + criteria + weighted evaluation matrix
```

---

_Quick Reference v1.1 — 2026-04-24_
