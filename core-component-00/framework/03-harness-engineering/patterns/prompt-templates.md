# Prompt Templates for Harness Engineering

Production-ready prompt templates that implement each harness pattern. Adapt these for your own use cases.

---

## Pattern 1: The Sandwich Pattern

The "Sandwich Pattern" structures a complex prompt into three distinct sections: Context, Task, and Output Format. This reduces instruction drift and improves parsing reliability.

### Template Structure

```
<system>
You are an expert {role}. Follow these guidelines:
- {guideline1}
- {guideline2}
- {guideline3}
</system>

<context>
{relevant_background_context}
</context>

<task>
{primary_task_description}

Requirements:
- {requirement1}
- {requirement2}
- {requirement3}
</task>

<output_format>
Return your response in this format:
{expected_output_schema}
</output_format>
```

### Example 1.1: Document Analysis

```markdown
<system>
You are a senior data analyst with expertise in extracting structured information from documents. Follow these guidelines:
- Be precise and concise
- Only use information explicitly present in the document
- Flag any ambiguous or contradictory information
</system>

<context>
Document excerpt: "Our quarterly revenue increased by 15% compared to last quarter, driven primarily by strong performance in the enterprise segment."
</context>

<task>
Extract key metrics and business insights from this document.

Requirements:

- Identify all numeric metrics with their context
- Note growth rates and percentages
- Identify driver segments
- Flag any uncertainties
  </task>

<output_format>
Return JSON in this format:
{
"metrics": [
{
"metric_name": "...",
"value": "...",
"period": "..."
}
],
"drivers": ["...", "..."],
"uncertainties": [...]
}
</output_format>
```

### Example 1.2: Code Review

```markdown
<system>
You are a senior software architect with 15+ years experience in distributed systems. Follow these guidelines:
- Focus on correctness, security, and performance
- Provide specific, actionable suggestions
- Use standard terminology from the relevant language ecosystem
</system>

<context>
Code snippet to review: [paste code here]
Language: Python
Architecture pattern: Event-driven
</context>

<task>
Review this code for potential issues.

Requirements:

- Identify bugs or edge cases not handled
- Check for security vulnerabilities (OWASP Top 10)
- Suggest performance improvements
- Note any architectural concerns
  </task>

<output_format>
Return JSON in this format:
{
"bugs": [
{
"location": "...",
"description": "...",
"severity": "high|medium|low",
"fix": "..."
}
],
"security_issues": [...],
"performance_suggestions": [...],
"architectural_concerns": [...]
}
</output_format>
```

---

## Pattern 2: Error Boundary Prompt Wrapper

This pattern adds error recovery hints directly into the prompt structure.

### Template Structure

```
<prompt_with_fallback_hints>
<primary_task>
{main task description}
</primary_task>

<error_recovery_guidance>
If unable to complete the primary task, try:
1. Simplified version: {simpler_approach}
2. With assumptions: {default_assumptions}
3. With placeholder data: {template_response}
</error_recovery_guidance>
</prompt_with_fallback_hints>
```

### Example: Summary with Fallbacks

```markdown
<prompt_with_fallback_hints>
<primary_task>
Summarize the following document into 3-5 sentences, capturing the main points and conclusions.

Document: {document_content}

Constraints:

- Maximum 5 sentences
- Use professional tone
- Include key findings and recommendations
  </primary_task>

<error_recovery_guidance>
If unable to complete primary task due to:

1. Length issues (document too long):
   Summarize into sections, then create overall summary from section summaries.

2. Ambiguous content (unclear main point):
   Identify the most frequently discussed topic as the main point.

3. Language barriers (unfamiliar terminology):
   Use general description of content without specific technical terms.
   </error_recovery_guidance>
   </prompt_with_fallback_hints>
```

---

## Pattern 3: Context Budget-Aware Prompt

This pattern explicitly manages context window usage for long conversations.

### Template Structure

```
<budget_aware_prompt>
<history_summary>
{summarized_previous_context}
</history_summary>

<current_request>
{current_user_input}
</current_request>

<response_requirements>
- Keep response focused on current request
- Do not repeat already-discussed information
- Reference key previous points when relevant
</response_requirements>
</budget_aware_prompt>
```

### Example: Long Conversation Summary

```markdown
<budget_aware_prompt>
<history_summary>
User has been asking about implementing a REST API in Python using FastAPI. We discussed:

1. Project structure and dependencies
2. Creating the first endpoint for user registration
3. Database models with SQLAlchemy
4. Authentication requirements

Key decisions made:

- Using Pydantic for request validation
- PostgreSQL database
- JWT-based authentication planned

User wants to proceed with implementing login endpoint now.
</history_summary>

<current_request>
Create the login endpoint that accepts username/password and returns a JWT token.
</current_request>

<response_requirements>

- Keep response focused on current request (login endpoint)
- Do not repeat already-discussed structure/dependencies
- Reference key previous points: use same models and validation approach
- Provide complete, runnable code snippet
  </response_requirements>
  </budget_aware_prompt>
```

---

## Pattern 4: Tool Use with Boundary Prompts

These prompts explicitly define tool boundaries to prevent unbounded exploration.

### Template Structure

```
<tool_bounded_prompt>
<task>
{task_description}
</task>

<available_tools>
Tool list (whitelist):
1. {tool1_name}: {tool1_description} (max calls: {limit})
2. {tool2_name}: {tool2_description} (max calls: {limit})
3. {tool3_name}: {tool3_description} (max calls: {limit})
</available_tools>

<boundaries_and_constraints>
- Maximum total tool calls per task: {max_total_calls}
- Do not discover new tools beyond whitelist
- Each tool call must be explicitly justified
- Summarize progress between tool calls
</boundaries_and_constraints>
</tool_bounded_prompt>
```

### Example: Research Task with Tool Limits

```markdown
<tool_bounded_prompt>
<task>
Research the current state of LLM-based code generation and provide a summary report.
</task>

<available_tools>
Tool list (whitelist):

1. search: Search web for recent articles (max calls: 3)
2. file_read: Read local research notes (max calls: 2)
3. calculator: Perform data analysis on findings (max calls: 2)
   </available_tools>

<boundaries_and_constraints>

- Maximum total tool calls per task: 5
- Do not discover new tools beyond whitelist
- Each tool call must be explicitly justified before making the call
- Summarize progress between tool calls
- If research is incomplete, state limitations clearly
  </boundaries_and_constraints>
  </tool_bounded_prompt>
```

---

## Pattern 5: Schema-Constrained Output Prompts

These prompts enforce strict output formats for downstream processing.

### Template Structure

```
<schema_constrained_prompt>
<task>
{task_description}
</task>

<output_schema>
Return output as valid JSON matching this schema:
{json_schema_definition}
</output_schema>

<validation_requirements>
- All required fields must be present
- Types must match the schema exactly
- No additional fields outside the schema
- Use null (not empty string) for missing data
</validation_requirements>
</schema_constrained_prompt>
```

### Example: Entity Extraction with Schema Validation

```markdown
<schema_constrained_prompt>
<task>
Extract all named entities from this text and classify them.

Text: "On March 15, 2024, Tesla announced its new AI autopilot features. CEO Elon Musk stated that the system will reach level 4 autonomy by year-end."
</task>

<output_schema>
Return output as valid JSON matching this schema:
{
"entities": [
{
"text": "...",
"type": "PERSON|ORGANIZATION|DATE|LOCATION|PRODUCT|EVENT",
"start_position": ...,
"end_position": ...
}
],
"summary": "..."
}
</output_schema>

<validation_requirements>

- All required fields must be present
- Types must match the schema exactly (use uppercase type names)
- No additional fields outside the schema
- Use null (not empty string) for missing data
- Position indices must be valid character positions in input text
  </validation_requirements>
  </schema_constrained_prompt>
```

---

## Quick Reference: Pattern Selection Guide

| Task Type                      | Recommended Pattern    | File Location                      |
| ------------------------------ | ---------------------- | ---------------------------------- |
| Complex multi-step reasoning   | Sandwich               | `patterns/prompt-templates.md`     |
| Fallback/degradation needs     | Error Boundary Wrapper | Add to existing prompts            |
| Long-running conversations     | Context Budget-Aware   | See context management guide       |
| Tool-augmented tasks           | Tool-Bounded           | `implementations/tool_registry.py` |
| Downstream processing required | Schema-Constrained     | Use JSON Schema blocks             |

---

## Best Practices for All Prompts

| Practice                                                                   | Why                                                                           |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Use delimiters** — separate sections with `<section>`, `---`, or headers | Prevents instruction blending; makes the prompt machine-parseable             |
| **Be specific about format** — never say "return in a structured format"   | Vague format requests produce inconsistent outputs; specify schema explicitly |
| **Provide examples** — include 1–2 expected output examples where possible | Few-shot examples materially improve consistency across varied inputs         |
| **Manage context budget** — summarise old turns before hitting 80% usage   | Prevents context overflow and attention dilution in long sessions             |
| **Validate outputs** — validate responses against schema before processing | Catches malformed outputs before they propagate to downstream consumers       |
| **Add error recovery hints** — include fallback approaches in the prompt   | Gives the model a graceful degradation path instead of producing an error     |

---

**Last Updated:** 2026-04-24  
**Version:** 1.0  
**Maintained by:** Claude Lab Engineering Team
