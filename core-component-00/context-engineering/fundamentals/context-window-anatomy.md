# Context Window Anatomy

## The Four Slots

A model's context window is not a single text blob. It has four distinct functional slots. Understanding what belongs in each — and what does not — is the foundation of context engineering.

---

## Slot 1: The System Slot

**Position:** Always first in the context window.
**Authority:** Highest — defines the model's identity, rules, and constraints.
**Token Budget:** ≤ 15%

### What belongs here

| Content                         | Why                                                  |
| ------------------------------- | ---------------------------------------------------- |
| Agent role and persona          | Activates the correct knowledge cluster in the model |
| Persistent behavioural rules    | Instructions that must apply to every response       |
| Output format specification     | Structural constraints on all responses              |
| Hard safety constraints         | Lines the model must never cross, stated explicitly  |
| Skill or pipeline stage context | Which workflow stage the agent is operating in       |

### What does NOT belong here

| Forbidden Content                     | Risk                                                    |
| ------------------------------------- | ------------------------------------------------------- |
| User-supplied text (even paraphrased) | Prompt injection — user gains system-level authority    |
| Dynamic data that changes per turn    | Causes prompt bloat and instruction drift               |
| Conversation history                  | Pollutes the role context with conversational noise     |
| Retrieved documents                   | Retrieved content has lower authority than system rules |

### Best practices

- Keep the system slot **static across turns** — do not rebuild it each time
- Place the most critical constraint **last** in the system slot (recency bias in attention)
- Use structured delimiters (`<role>`, `<rules>`, `<format>`) to prevent instruction blending
- Pin model version in production — system slot interpretation varies by model version

---

## Slot 2: The Retrieved Slot

**Position:** After system, before history.
**Authority:** Informational — cited as source material, not treated as ground truth.
**Token Budget:** ≤ 30%

### What belongs here

| Content                 | Why                                                 |
| ----------------------- | --------------------------------------------------- |
| RAG-retrieved documents | External knowledge the model does not have natively |
| Episodic memory lookups | Relevant past events retrieved for the current task |
| Semantic memory lookups | Persistent facts retrieved for the current context  |
| External API responses  | Structured data from tool pre-fetches               |

### What does NOT belong here

| Forbidden Content          | Risk                                                     |
| -------------------------- | -------------------------------------------------------- |
| Unvalidated user documents | Untrusted content influences model with false authority  |
| Expired or stale data      | Model reasons from outdated facts                        |
| Entire knowledge bases     | Attention dilution — the model cannot process everything |

### Best practices

- Always label retrieved content with source and timestamp: `[Source: docs/auth.md, 2026-03-12]`
- Use relevance scoring to select the top-K most relevant chunks — do not dump all results
- Apply ACL filtering **before** assembly — never include documents the user is not authorised to see
- Place the most relevant chunk **last** in the retrieved slot (recency bias)

---

## Slot 3: The History Slot

**Position:** After retrieved, before tool outputs.
**Authority:** Contextual — informs the model of what has been said, but does not override system rules.
**Token Budget:** ≤ 40%

### What belongs here

| Content                              | Why                                                  |
| ------------------------------------ | ---------------------------------------------------- |
| Recent conversation turns            | Maintains conversational coherence                   |
| Compressed summaries of older turns  | Preserves thread without consuming full budget       |
| Decisions and commitments (verbatim) | Sacred context — must never be lost or paraphrased   |
| Key clarifications made by the user  | Prevents the model from re-asking resolved questions |

### What does NOT belong here

| Forbidden Content                           | Risk                                                   |
| ------------------------------------------- | ------------------------------------------------------ |
| Every single conversation turn uncompressed | Token budget overflow within 10–20 turns               |
| Tool results from earlier turns             | Belongs in tool output slot; mixing confuses authority |
| System-level instructions repeated          | Dilutes system slot authority                          |

### Best practices

- Apply **hierarchical compression** as sessions grow: old turns → paragraph summary → single sentence
- Preserve the **last 3–5 turns verbatim** for immediate coherence
- Store **decisions and commitments** separately in episodic memory and re-inject verbatim on every turn
- Scrub PII from history before logging and before injection into any shared context

---

## Slot 4: The Tool Output Slot

**Position:** Last in the context window, immediately before the model's response.
**Authority:** Factual — the model treats tool outputs as ground truth for the current turn.
**Token Budget:** ≤ 15%

### What belongs here

| Content                                | Why                                                |
| -------------------------------------- | -------------------------------------------------- |
| Validated tool call results            | Schema-verified data the model can reason from     |
| Structured API responses               | JSON/YAML that the model can parse and reference   |
| Calculation results                    | Numerical outputs to avoid hallucinated arithmetic |
| Real-time data (weather, prices, etc.) | Current facts that the model cannot know natively  |

### What does NOT belong here

| Forbidden Content                   | Risk                                               |
| ----------------------------------- | -------------------------------------------------- |
| Unvalidated tool responses          | Model reasons from corrupted or malicious data     |
| Verbose API prose responses         | Attention dilution; schema-reduce before injection |
| Tool call errors that were resolved | Noise; discard resolved errors                     |

### Best practices

- Always **schema-validate** tool output before injection
- **Schema-reduce** verbose responses: extract key fields, drop prose descriptions
- Place tool outputs **immediately before the model's response turn** — maximum recency effect
- For high-stakes tool outputs (financial data, medical data), inject a verification prompt alongside the data

---

## Slot Order and Why It Matters

```
[SYSTEM]      ← Read first. Sets the model's identity and rules.
[RETRIEVED]   ← Read second. Provides factual context for the task.
[HISTORY]     ← Read third. Provides conversational state.
[TOOL OUTPUT] ← Read last. Provides the most current factual data.
```

The ordering is intentional: the model's attention mechanism gives **higher weight to content near the beginning and near the end** of the context. System instructions anchor at the start (highest authority). Tool outputs anchor at the end (highest recency). History and retrieved content fill the middle.

This means: **never put your most important content in the middle of a long context.**

---

## Visual Reference: Context Window Budget

```
┌───────────────────────────────────────────────────────────┐
│ SYSTEM         [==================] 15%                   │
│                                                           │
│ RETRIEVED      [=====================================]    │
│                [=====================================] 30%│
│                                                           │
│ HISTORY        [=====================================]    │
│                [=====================================]    │
│                [=====================================] 40%│
│                                                           │
│ TOOL OUTPUT    [==================] 15%                   │
│                                                           │
│ [SAFETY BUFFER — never use last 10% of window]            │
└───────────────────────────────────────────────────────────┘
```

---

**Version:** 1.0
**Last Updated:** 2026-04-28
**See also:** [Memory Types](./memory-types.md) · [Assembly Patterns](../patterns/assembly-patterns.md) · [CONCEPTS.md](../CONCEPTS.md)
