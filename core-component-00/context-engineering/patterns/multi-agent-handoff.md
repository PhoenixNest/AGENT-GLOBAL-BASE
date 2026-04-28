# Multi-Agent Context Handoff Patterns

## The Problem

When an orchestrator agent delegates to a subagent, two failure modes emerge:

- **Over-sharing:** The orchestrator forwards its entire context window. The subagent receives irrelevant history, consumes its entire token budget processing noise, and produces lower-quality output.
- **Under-sharing:** The orchestrator forwards only the task description. The subagent lacks the decisions, constraints, and facts it needs, so it re-asks questions, makes conflicting assumptions, or produces work that contradicts the orchestrator's established direction.

Context Engineering defines a **Context Handoff Protocol** that avoids both failure modes.

---

## The Three Handoff Tiers

### Tier 1: Full Handoff

**When to use:** The subagent is continuing the exact same task with the same scope.

| What is forwarded                            | Why                                                |
| -------------------------------------------- | -------------------------------------------------- |
| System slot (full)                           | Subagent needs the same role and rules             |
| Sacred context (all decisions + commitments) | Subagent must not contradict established direction |
| Recent history (last 5 turns verbatim)       | Subagent needs immediate conversational context    |
| Retrieved content (task-relevant)            | Subagent needs the same knowledge base             |
| Working memory (current task state)          | Subagent continues from where orchestrator stopped |

**Token budget impact:** Near-full context window transferred.

```python
handoff = assembler.build_handoff(tier="full", subagent_task=task)
```

---

### Tier 2: Scoped Handoff

**When to use:** The subagent handles one bounded sub-task within a larger workflow.

| What is forwarded                                    | Why                                                  |
| ---------------------------------------------------- | ---------------------------------------------------- |
| System slot (scoped role)                            | Subagent receives a role scoped to its sub-task only |
| Sacred context (decisions relevant to sub-task only) | Prevents contradictions without full history noise   |
| Sub-task description + acceptance criteria           | Tells subagent exactly what to produce               |
| Retrieved content (sub-task-relevant only)           | Subagent gets only the knowledge it needs            |
| Working memory (current sub-step only)               | Subagent knows where it fits in the larger plan      |

**Token budget impact:** 20–40% of orchestrator's context window.

```python
handoff = assembler.build_handoff(
    tier="scoped",
    subagent_task=subtask_description,
    relevant_decisions=em.get_decisions_for_topic(subtask_topic),
    retrieved_filter=lambda doc: subtask_topic in doc.tags
)
```

---

### Tier 3: Minimal Handoff

**When to use:** The subagent is an independent specialist or a pure tool wrapper.

| What is forwarded                 | Why                                            |
| --------------------------------- | ---------------------------------------------- |
| System slot (minimal — task only) | Subagent needs just enough role context to act |
| Task description                  | What to produce                                |
| Input data only                   | No history, no memory, no retrieved context    |

**Token budget impact:** < 10% of orchestrator's context window.

```python
handoff = assembler.build_handoff(tier="minimal", subagent_task=task, input_data=data)
```

---

### Tier Selection Matrix

| Subagent Scenario                                              | Tier                | Rationale                                            |
| -------------------------------------------------------------- | ------------------- | ---------------------------------------------------- |
| Subagent continues the same task (e.g., coding after planning) | Full                | Same context needed                                  |
| Subagent writes one module in a larger system                  | Scoped              | Needs architectural decisions, not full conversation |
| Subagent performs a pure calculation                           | Minimal             | Input → output; no context needed                    |
| Subagent calls an external API                                 | Minimal             | No model reasoning required beyond the call          |
| Subagent is third-party / untrusted                            | Minimal + sanitised | Do not expose internal decisions or history          |
| Subagent is a language translator                              | Scoped              | Needs source text + style guidelines only            |
| Subagent is a security reviewer                                | Scoped              | Needs code + security requirements; not all history  |

---

## The Handoff Packet Structure

A handoff packet is a structured object — not a raw context window dump:

```python
@dataclass
class HandoffPacket:
    tier: str                         # "full" | "scoped" | "minimal"
    system: str                       # Scoped system prompt for subagent
    task: str                         # What the subagent must produce
    sacred_context: list[str]         # Verbatim decisions and commitments
    retrieved: list[dict]             # Filtered retrieved content
    working_memory: dict              # Current task state
    acceptance_criteria: list[str]    # What "done" looks like
    return_schema: dict               # Expected output format
    budget: int                       # Token budget allocated to subagent
```

The `return_schema` and `acceptance_criteria` fields are critical — they tell the subagent exactly what format to return results in, so the orchestrator can validate and integrate them without ambiguity.

---

## Result Integration

When the subagent returns its result, the orchestrator must:

1. **Validate** the result against `return_schema`
2. **Extract** any new decisions or commitments from the result
3. **Update** its own episodic memory with the subagent's outcome
4. **Update** working memory to mark the sub-task complete
5. **Re-assemble** its own context window for the next turn (incorporating the result)

```python
result = await subagent.execute(handoff_packet)

# Step 1: Validate
if not validator.check(result, handoff_packet.return_schema):
    return error_response("Subagent returned invalid format")

# Step 2-4: Update memory
orchestrator_memory.record_event("subtask_complete",
    f"Subagent produced: {result.summary}")
working_memory.mark_complete(subtask_id)

# Step 5: Re-assemble context
context = assembler.build(task_type="orchestration")
```

---

## Anti-Patterns

| Anti-Pattern                                         | Problem                                                                                          | Fix                                                             |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| **Full dump by default**                             | Subagent wastes budget on irrelevant history; slower and lower quality                           | Always select tier explicitly based on subagent's actual needs  |
| **No sacred context in scoped handoff**              | Subagent contradicts orchestrator's established decisions                                        | Always include sacred context in Tier 1 and Tier 2 handoffs     |
| **No return schema**                                 | Orchestrator cannot reliably parse or validate subagent output                                   | Always define `return_schema` in the handoff packet             |
| **Trusting third-party subagents with full context** | Internal decisions, history, and memory exposed to untrusted party                               | Always use Tier 3 minimal handoff for external/untrusted agents |
| **No result integration**                            | Subagent's output is used but not recorded in memory; next turn lacks awareness of what was done | Always record sub-task completion in episodic memory            |

---

**Version:** 1.0
**Last Updated:** 2026-04-28
**See also:** [Assembly Patterns](./assembly-patterns.md) · [context_assembler.py](../implementations/context_assembler.py) · [Memory Types](../fundamentals/memory-types.md)
